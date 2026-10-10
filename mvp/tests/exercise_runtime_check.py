"""Measured local HTTP samples and SQLite backup drill, not scale/RPO acceptance."""
from __future__ import annotations

import argparse
from http.cookiejar import CookieJar
from http.server import ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import sqlite3
import threading
import time
import urllib.request
from unittest.mock import patch

from properwarm_mvp.factory import open_store
from properwarm_mvp.server import App, make_handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    state = args.state.resolve()
    if state.exists():
        raise SystemExit("Use a new explicit state directory; existing data is never removed.")
    results = {}
    with patch.dict(os.environ, {"PW_EXERCISE": "1", "PW_STATE": str(state), "PW_STORE": "sqlite",
                                  "PW_DOC_STORE": "local", "PW_AI": "off", "PW_PASSWORD": "fictional-local-only"}, clear=True):
        store = open_store()
        app = App(store, password="fictional-local-only")
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))

        def request(path, body=None):
            data = json.dumps(body).encode() if body is not None else None
            req = urllib.request.Request(base + path, data=data, headers={"Content-Type": "application/json"})
            with client.open(req, timeout=10) as response:
                return json.load(response)

        try:
            request("/api/login", {"email": "ex-pso-01@example.test", "password": "fictional-local-only"})
            operations = {
                "list": ("/api/cases?view=all&limit=50", None, 1),
                "detail": ("/api/cases/EX-HOME-001/exercise", None, 1),
                "dashboard": ("/api/exercise", None, 3),
                "write": ("/api/cases/EX-HOME-001/exercise",
                          {"action": "resident-update", "channel": "Phone", "evidence": "Fictional sampled coordination",
                           "next_update": "Named case team checks next weekday"}, 2),
            }
            for name, (path, body, threshold) in operations.items():
                request(path, body)
                samples = []
                for _ in range(200):
                    started = time.perf_counter()
                    request(path, body)
                    samples.append(time.perf_counter() - started)
                p95 = sorted(samples)[math.ceil(.95 * len(samples)) - 1]
                results[name] = {"samples": len(samples), "warm_http_p95_seconds": p95,
                                 "threshold_seconds": threshold, "result": "Pass" if p95 <= threshold else "Fail"}
            before = json.loads(json.dumps(store._case("EX-HOME-001")))
            with sqlite3.connect(state / "backup.sqlite") as target:
                store.db.backup(target)
            start = time.perf_counter()
            store.db.close()
            reopened = open_store()
            try:
                same = reopened._case("EX-HOME-001") == before
                integrity = reopened.db.execute("PRAGMA integrity_check").fetchone()[0]
                rows = reopened.db.execute("SELECT body FROM cases WHERE id='EX-HOME-001'").fetchone()[0]
            finally:
                reopened.db.close()
            results["clean-restart"] = {"seconds": time.perf_counter() - start,
                                        "exact_case_retained": same, "integrity": integrity,
                                        "result": "Pass" if same and integrity == "ok" else "Fail"}
            with sqlite3.connect(state / "backup.sqlite") as source, sqlite3.connect(state / "restored.sqlite") as target:
                source.backup(target)
                restored = target.execute("SELECT body FROM cases WHERE id='EX-HOME-001'").fetchone()[0]
                audit_same = source.execute("SELECT count,hash FROM audit_head").fetchall() == target.execute(
                    "SELECT count,hash FROM audit_head").fetchall()
                results["backup-restore"] = {"exact_stored_case": restored == rows, "exact_audit_head": audit_same,
                                             "result": "Pass" if restored == rows and audit_same else "Fail"}
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "kind": "local-http-and-clean-backup-engineering",
        "population": "18 fictional homes; one HTTP session, one writer; 201 updates on story home",
        "core_30_minute_workload": "Not run", "scale_30_minute_workload": "Not run",
        "crash_and_response_loss": "Not run", "rpo_and_reconciliation": "Not run",
        "results": results,
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results))
    return int(any(value["result"] == "Fail" for value in results.values()))


if __name__ == "__main__":
    raise SystemExit(main())
