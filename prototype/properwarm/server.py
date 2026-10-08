"""Minimal HTTP API. Identity comes from the platform (Container Apps Entra auth injects X-MS-CLIENT-PRINCIPAL)."""
from __future__ import annotations

import base64
import json
import logging
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .domain import Rejected, Store

STORE = Store()
STORE.add_case("C-001")
log = logging.getLogger("properwarm")


def principal(headers) -> tuple[str, str]:
    raw = headers.get("X-MS-CLIENT-PRINCIPAL")
    if not raw:
        raise Rejected("unauthenticated", "no verified principal")
    claims = json.loads(base64.b64decode(raw))
    roles = [c["val"] for c in claims.get("claims", []) if c.get("typ") in ("roles", "role")]
    if len(roles) != 1:
        raise Rejected("unknown_role", "exactly one app role is required")
    return claims.get("userId", "unknown"), roles[0]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/healthz", "/readyz"):
            return self._send(200, {"status": "ok", "audit_valid": STORE.verify_audit()})
        self._send(404, {"error": "not_found"})

    def do_POST(self):
        try:
            actor, role = principal(self.headers)
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0)) or 0) or b"{}")
            parts = self.path.strip("/").split("/")
            if parts[0] == "proposals" and len(parts) == 1:
                p = STORE.submit_proposal(actor, role, body)
                return self._send(201, {"proposal_id": p.proposal_id, "status": p.status})
            if parts[0] == "proposals" and len(parts) == 3 and parts[2] in ("accept", "reject"):
                p = STORE.decide_proposal(actor, role, parts[1], parts[2] == "accept")
                return self._send(200, {"proposal_id": p.proposal_id, "status": p.status})
            if parts[0] == "cases" and len(parts) == 3 and parts[2] == "transitions":
                c = STORE.transition(actor, role, parts[1], body.get("to_stage", ""), int(body.get("expected_version", 0)),
                                     self.headers.get("Idempotency-Key", ""), body.get("approver"))
                return self._send(200, {"case_id": c.case_id, "stage": c.stage, "version": c.version})
            self._send(404, {"error": "not_found"})
        except Rejected as exc:
            code = 401 if exc.code == "unauthenticated" else 403 if "forbidden" in exc.code else 409 if "conflict" in exc.code else 422
            log.warning(json.dumps({"severity_text": "WARN", "body": exc.code, "attributes": {"role": locals().get("role")}}))
            self._send(code, {"error": exc.code, "message": str(exc)})
        except (ValueError, KeyError):
            self._send(400, {"error": "bad_request"})


def main() -> None:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()


if __name__ == "__main__":
    main()
