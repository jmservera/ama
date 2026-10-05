from __future__ import annotations

import argparse
import base64
import binascii
import json
import logging
import mimetypes
import os
import re
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from .domain import ACTOR_LABELS, CLOSURE_REASONS, EVENT_OUTCOMES, GATE_LABELS
from .imports import MAX_WORKBOOK_BYTES, parse_workbook
from .storage import Store
from .agents import PROMPT_VERSION, configured_model, run_agent

LOG = logging.getLogger("properwarm")
PACKAGE_DIR = Path(__file__).resolve().parent
WEB_DIR = PACKAGE_DIR.parent / "web"
MAX_JSON_BYTES = (MAX_WORKBOOK_BYTES + 2) // 3 * 4 + 1_000_000
CASE_ROUTE = re.compile(r"^/api/cases/([^/]+)/(appointment|close|reopen|review|controls|advance|agent-run|agent-review)$")


class PrototypeServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address: tuple[str, int], store: Store):
        self.store = store
        self.pending_imports: dict[str, tuple[float, Any]] = {}
        self.pending_lock = threading.Lock()
        self.model = configured_model()
        self.agent_lock = threading.Lock()
        super().__init__(address, RequestHandler)


class RequestHandler(BaseHTTPRequestHandler):
    server: PrototypeServer

    def log_message(self, format_string: str, *args: Any) -> None:
        LOG.info(json.dumps({
            "event": "http_request", "request_id": getattr(self, "request_id", None),
            "message": format_string % args,
            "duration_ms": round((time.perf_counter() - getattr(self, "request_start", time.perf_counter())) * 1000, 2),
        }))

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Request-ID", getattr(self, "request_id", "not-recorded"))
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'",
        )
        super().end_headers()

    def do_GET(self) -> None:
        self.request_id = uuid.uuid4().hex
        self.request_start = time.perf_counter()
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/api/health":
                mode = (
                    "local-synthetic-only"
                    if self.server.server_address[0] == "127.0.0.1"
                    else "internal-container-synthetic-only"
                )
                self._json(HTTPStatus.OK, {"status": "ok", "mode": mode})
            elif parsed.path == "/favicon.ico":
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
            elif parsed.path == "/api/overview":
                self._json(HTTPStatus.OK, self.server.store.overview())
            elif parsed.path == "/api/agents":
                self._json(HTTPStatus.OK, {
                    "configured": self.server.model is not None,
                    "model": self.server.model.model if self.server.model else None,
                    "prompt_version": PROMPT_VERSION,
                    "reason": "Azure configuration present; connectivity and quality require evaluation."
                    if self.server.model else "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT; authenticate with Entra ID.",
                })
            elif parsed.path == "/api/cases":
                query = parse_qs(parsed.query)
                self._json(
                    HTTPStatus.OK,
                    {
                        "cases": self.server.store.list_cases(
                            query.get("q", [""])[0][:100],
                            query.get("filter", [""])[0][:20],
                        )
                    },
                )
            elif parsed.path.startswith("/api/cases/"):
                candidate_id = unquote(parsed.path.removeprefix("/api/cases/"))
                case = self.server.store.get_case(candidate_id)
                if case is None:
                    self._error(HTTPStatus.NOT_FOUND, "Synthetic case was not found.")
                else:
                    self._json(HTTPStatus.OK, case)
            elif parsed.path == "/api/settings":
                overview = self.server.store.overview()
                self._json(
                    HTTPStatus.OK,
                    {
                        "threshold": overview["threshold"],
                        "version": overview["threshold_version"],
                        "outcomes": EVENT_OUTCOMES,
                        "gates": GATE_LABELS,
                        "actors": sorted(ACTOR_LABELS),
                        "closure_reasons": sorted(CLOSURE_REASONS),
                        "is_synthetic": True,
                        "mode": (
                            "local"
                            if self.server.server_address[0] == "127.0.0.1"
                            else "internal-container"
                        ),
                    },
                )
            elif parsed.path == "/api/export":
                self._json(HTTPStatus.OK, self.server.store.export_bundle())
            elif parsed.path == "/":
                self._file(WEB_DIR / "index.html")
            elif parsed.path in ("/assets/app.js", "/assets/app.css"):
                file_path = WEB_DIR / parsed.path.removeprefix("/assets/")
                self._file(file_path)
            else:
                self._error(HTTPStatus.NOT_FOUND, "Route was not found.")
        except (OSError, ValueError, KeyError):
            LOG.exception("Request failed: %s", self.path)
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "Could not load prototype data.")
        except Exception:
            LOG.exception("Unexpected GET failure: %s", self.path)
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "Unexpected local prototype error.")

    def do_POST(self) -> None:
        self.request_id = uuid.uuid4().hex
        self.request_start = time.perf_counter()
        try:
            body = self._read_json()
            path = urlparse(self.path).path
            if path == "/api/settings":
                result = self.server.store.update_threshold(
                    body.get("threshold"), body.get("actor", "")
                )
                self._json(HTTPStatus.OK, result)
                return
            if path == "/api/import/preview":
                self._preview_import(body)
                return
            if path == "/api/import/commit":
                self._commit_import(body)
                return
            match = CASE_ROUTE.fullmatch(path)
            if not match:
                self._error(HTTPStatus.NOT_FOUND, "Route was not found.")
                return
            candidate_id, action = unquote(match.group(1)), match.group(2)
            if action == "agent-run":
                if self.server.model is None:
                    self._error(HTTPStatus.SERVICE_UNAVAILABLE, "Azure model is not configured; no AI proposal was generated.")
                    return
                if body.get("actor") not in ACTOR_LABELS:
                    raise ValueError("Choose a supported synthetic reviewer label.")
                case = self.server.store.get_case(candidate_id)
                if case is None:
                    raise KeyError("Synthetic case was not found.")
                if not self.server.agent_lock.acquire(blocking=False):
                    self._error(HTTPStatus.CONFLICT, "Another bounded agent run is active; wait before retrying.")
                    return
                try:
                    run = run_agent(
                        case, self.server.model,
                        on_started=lambda started: self.server.store.save_agent_run(started, body["actor"]),
                    )
                    saved = self.server.store.save_agent_run(run, body["actor"])
                    LOG.info(json.dumps({
                        "event": "agent_run", "request_id": self.request_id,
                        "run_id": saved["run_id"], "state": saved["state"],
                        "duration_ms": saved["duration_ms"], "usage": saved["usage"],
                    }))
                    self._json(HTTPStatus.OK, saved)
                finally:
                    self.server.agent_lock.release()
            elif action == "agent-review":
                self._json(HTTPStatus.OK, self.server.store.review_agent_run(
                    candidate_id, str(body.get("run_id", "")), str(body.get("decision", "")), body.get("actor", ""),
                ))
            elif action == "appointment":
                result = self.server.store.record_appointment(
                    candidate_id,
                    body.get("outcome", ""),
                    body.get("appointment_confirmed"),
                    body.get("actor", ""),
                )
                self._json(HTTPStatus.CREATED, result)
            elif action == "close":
                self.server.store.close_case(
                    candidate_id, body.get("actor", ""), body.get("reason", "")
                )
                self._json(HTTPStatus.OK, {"closed": True, "counter_reset": True})
            elif action == "reopen":
                self.server.store.reopen_case(candidate_id, body.get("actor", ""))
                self._json(HTTPStatus.OK, {"active": True, "new_case_episode": True})
            elif action == "review":
                self.server.store.record_review(candidate_id, body.get("actor", ""))
                self._json(HTTPStatus.CREATED, {"recorded": True})
            elif action == "controls":
                controls = body.get("controls")
                if not isinstance(controls, dict):
                    raise ValueError("controls must be an object.")
                self.server.store.update_controls(
                    candidate_id, controls, body.get("actor", "")
                )
                self._json(HTTPStatus.OK, {"saved": True})
            elif action == "advance":
                result = self.server.store.advance_case(candidate_id, body.get("actor", ""))
                self._json(HTTPStatus.OK, result)
        except KeyError as exc:
            self._error(HTTPStatus.NOT_FOUND, str(exc).strip("'"))
        except ValueError as exc:
            self._error(HTTPStatus.BAD_REQUEST, str(exc))
        except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as exc:
            self._error(HTTPStatus.BAD_REQUEST, f"Invalid request body: {exc}")
        except Exception:
            LOG.exception("Unexpected POST failure: %s", self.path)
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "Unexpected local prototype error.")

    def _preview_import(self, body: dict[str, Any]) -> None:
        encoded = body.get("workbook_base64")
        if not isinstance(encoded, str):
            raise ValueError("workbook_base64 must be provided.")
        if len(encoded) > (MAX_WORKBOOK_BYTES * 4 // 3) + 8:
            raise ValueError("Workbook exceeds the 5 MB local prototype limit.")
        try:
            content = base64.b64decode(encoded, validate=True)
        except binascii.Error as exc:
            raise ValueError("Workbook data is not valid base64.") from exc
        filename = str(body.get("filename") or "uploaded.xlsx")
        if not filename.casefold().endswith(".xlsx"):
            raise ValueError("Only .xlsx workbooks are accepted.")
        existing_ids = {
            row["candidate_id"] for row in self.server.store.list_cases(limit=1000)
        }
        preview = parse_workbook(content, filename, existing_ids)
        token = uuid.uuid4().hex
        with self.server.pending_lock:
            now = time.monotonic()
            self.server.pending_imports = {
                key: value
                for key, value in self.server.pending_imports.items()
                if value[0] > now
            }
            self.server.pending_imports[token] = (now + 600, preview)
        self._json(
            HTTPStatus.OK,
            {
                "preview_token": token,
                "source_file": preview.source_name,
                "sha256": preview.digest,
                "accepted": len(preview.accepted),
                "rejected": len(preview.rejected),
                "rows": sorted(
                    [
                        {
                            "source_row": row["source_row"],
                            "candidate_id": row["candidate_id"],
                            "disposition": "Accepted",
                            "issues": [],
                        }
                        for row in preview.accepted
                    ]
                    + [
                        {
                            "source_row": row["source_row"],
                            "candidate_id": row["candidate_id"],
                            "disposition": "Rejected",
                            "issues": row["issues"],
                        }
                        for row in preview.rejected
                    ],
                    key=lambda row: row["source_row"],
                ),
                "warnings": preview.warnings,
            },
        )

    def _commit_import(self, body: dict[str, Any]) -> None:
        token = str(body.get("preview_token") or "")
        with self.server.pending_lock:
            pending = self.server.pending_imports.pop(token, None)
        if pending is None or pending[0] <= time.monotonic():
            raise ValueError("Import preview expired or was already used. Preview the workbook again.")
        preview = pending[1]
        if not preview.accepted:
            raise ValueError("Preview has no valid rows to import.")
        count = self.server.store.import_cases(
            preview.accepted,
            preview.source_name,
            preview.digest,
            len(preview.rejected),
            body.get("actor", ""),
        )
        self._json(HTTPStatus.CREATED, {"imported": count, "source_file": preview.source_name})

    def _read_json(self) -> dict[str, Any]:
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise ValueError("Content-Length is required.")
        try:
            length = int(raw_length)
        except ValueError as exc:
            raise ValueError("Content-Length is invalid.") from exc
        if length < 0 or length > MAX_JSON_BYTES:
            raise ValueError("Request exceeds the local prototype size limit.")
        raw = self.rfile.read(length)
        if self.headers.get_content_type() != "application/json":
            raise ValueError("Content-Type must be application/json.")
        decoded = json.loads(raw.decode("utf-8"))
        if not isinstance(decoded, dict):
            raise ValueError("JSON request body must be an object.")
        return decoded

    def _file(self, path: Path) -> None:
        if not path.is_file() or not path.resolve().is_relative_to(WEB_DIR.resolve()):
            self._error(HTTPStatus.NOT_FOUND, "File was not found.")
            return
        content = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _json(self, status: HTTPStatus, value: Any) -> None:
        content = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _error(self, status: HTTPStatus, message: str) -> None:
        self._json(status, {"error": message})


def build_server(host: str, port: int, data_dir: Path, source_dir: Path) -> PrototypeServer:
    if host not in {"127.0.0.1", "0.0.0.0"}:
        raise ValueError("This prototype binds only to 127.0.0.1 or the container interface.")
    store = Store(data_dir / "prototype.sqlite3", source_dir)
    return PrototypeServer((host, port), store)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the synthetic Proper Warm prototype.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("APP_PORT", "8765")))
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(os.environ.get("DATA_DIR", PACKAGE_DIR.parent / ".data")),
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path(
            os.environ.get(
                "SOURCE_DIR",
                PACKAGE_DIR.parents[1] / "docs" / "reference" / "research" / "retrofit-synthetic-data",
            )
        ),
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    internal_ingress = os.environ.get("APP_INTERNAL_INGRESS", "").casefold() == "true"
    host = "0.0.0.0" if internal_ingress else "127.0.0.1"
    server = build_server(host, args.port, args.data_dir.resolve(), args.source_dir.resolve())
    if not internal_ingress:
        LOG.warning("Local synthetic prototype listening on http://%s:%s. Do not enter real or personal data.", host, args.port)
    else:
        LOG.warning("Container listener enabled on port %s; use only behind internal ingress and never expose publicly.", args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOG.info("Stopping local prototype.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
