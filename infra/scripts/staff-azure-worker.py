"""SQL-only staff worker. Never log private input or raw SDK/SQL exceptions."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

from staff_azure import ARM, MAX_INPUT, VERSION, encode_result
from staff_roster import staff_candidates

SPEC = importlib.util.spec_from_file_location(
    "workbench_staff", Path(__file__).with_name("initialize-workbench-staff.py")
)
assert SPEC and SPEC.loader
STAFF = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STAFF)


class Management:
    """Fixed-target ARM adapter for canonical restart verification, using only MI."""

    def __init__(self, target: str):
        from azure.identity import ManagedIdentityCredential

        self.target = target
        self.credential = ManagedIdentityCredential(client_id=os.environ["AZURE_CLIENT_ID"])

    def request(self, suffix: str = "", *, method: str = "GET") -> dict[str, Any]:
        token = self.credential.get_token(ARM + "/.default").token
        request = Request(
            ARM + self.target + suffix + "?api-version=" + VERSION,
            method=method,
            headers={"Authorization": "Bearer " + token},
            data=b"" if method == "POST" else None,
        )
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read() or "{}")

    def call(self, args: list[str]) -> Any:
        if args[:3] == ["containerapp", "revision", "list"]:
            return self.request("/revisions")["value"]
        if args[:2] == ["containerapp", "show"]:
            app = self.request()["properties"]
            query = args[args.index("--query") + 1]
            if query == "properties.configuration.ingress.traffic":
                return app["configuration"]["ingress"]["traffic"]
            if query == "properties.latestReadyRevisionName":
                return app["latestReadyRevisionName"]
        revision = quote(args[args.index("--revision") + 1], safe="")
        if args[:3] == ["containerapp", "replica", "list"]:
            return self.request("/revisions/" + revision + "/replicas")["value"]
        if args[:3] == ["containerapp", "revision", "restart"]:
            return self.request("/revisions/" + revision + "/restart", method="POST")
        raise ValueError("Unsupported management operation.")


def run_sql(request: dict[str, Any], db: Any, management: Any = None) -> dict[str, Any]:
    operation = request["operation"]
    payload = request["payload"]
    if operation == "candidates":
        rows = [
            json.loads(body) for _, body in db.execute("SELECT email, body FROM staff").fetchall()
        ]
        return {"candidates": staff_candidates(rows)}
    if operation not in {"check", "apply"}:
        raise ValueError("Unsupported operation.")
    wanted, people = payload["wanted"], payload["people"]
    if (
        not isinstance(wanted, list)
        or not wanted
        or len({row["code"] for row in wanted}) != len(wanted)
        or len({row["userId"] for row in wanted}) != len(wanted)
    ):
        raise ValueError("Invalid roster coverage.")
    roster = STAFF.prepare_sql_roster(db, wanted, people.__getitem__)
    summary = STAFF.install_roster(db, roster, apply=operation == "apply")
    verified = False
    if operation == "apply":
        # Reread after commit; do not trust only the commit's change counts.
        actual = STAFF.prepare_sql_roster(db, wanted, people.__getitem__)
        remaining = STAFF.install_roster(db, actual, apply=False)
        if any(remaining.values()) or actual != roster:
            raise ValueError("Post-commit SQL verification failed.")
        if management is None:
            management = Management(payload["target"])
        try:
            STAFF.restart_api("ama", payload["target"].rsplit("/", 1)[-1], call=management.call)
        finally:
            credential = getattr(management, "credential", None)
            if credential is not None:
                credential.close()
        verified = True
    return {
        "positions": len(roster),
        **summary,
        "sql_verified": operation == "apply" or not any(summary.values()),
        "restart_required": not verified,
    }


def main() -> int:
    request = None
    try:
        encoded = os.environ.pop("ZF_STAFF_REQUEST")
        request = json.loads(encoded)
        payload = json.dumps(request["payload"], sort_keys=True)
        if (
            type(request["version"]) is not int
            or request["version"] != 1
            or len(payload.encode()) > MAX_INPUT
            or hashlib.sha256(payload.encode()).hexdigest() != request["digest"]
            or request["payload"]["target"] != os.environ["ZF_STAFF_TARGET"]
            or os.environ["ZF_SQL_AUTH"] != "msi"
            or os.environ["ZF_SQL_CLIENT_ID"] != os.environ["AZURE_CLIENT_ID"]
        ):
            raise ValueError("Invalid private request.")
        from zava_forward.core.mssqlstore import _Conn, connection_string

        db = _Conn(connection_string())
        try:
            value = run_sql(request, db)
        finally:
            db.raw.close()
        result = {
            "version": 1,
            "run": request["run"],
            "operation": request["operation"],
            "ok": True,
            **value,
        }
        code = 0
    except Exception:
        # This executable is a privacy boundary: no raw SQL/SDK/identity exception.
        print("Staff job failed; private details were not logged.", flush=True)
        if request is None:
            return 1
        result = {
            "version": 1,
            "run": request.get("run"),
            "operation": request.get("operation"),
            "ok": False,
        }
        code = 1
    try:
        for line in encode_result(request, result):
            print(line, flush=True)
    except Exception:
        print("Staff job result unavailable; private details were not logged.", flush=True)
        return 1
    # The supported console-log endpoint needs a live replica. Give the operator
    # time to capture the encrypted response before requiring terminal success.
    time.sleep(60)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
