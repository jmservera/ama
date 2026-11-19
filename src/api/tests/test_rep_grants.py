"""Representative grants file for the deployable resident showcase (#154 C3, live demo)."""

import json
import tempfile
import threading
import unittest
from datetime import timedelta
from pathlib import Path
from typing import Any

from zava_forward.core import resident_showcase as rs

from test_resident_demo_api import FAKE_PASSWORD, HOST, KEY, NOW, Client, Clock, make_row
from zava_forward.api.resident_demo import app as demo
from zava_forward.api.resident_demo.rep_grants import load_grants


def grant_item(**over: Any) -> dict[str, Any]:
    item: dict[str, Any] = {
        "case_id": "SYN-REP-01",
        "email": "rep.info@example.com",
        "representative_ref": "REP-INFO-1",
        "measure": "Loft insulation",
        "tasks": ["Receive information"],
        "valid_from": (NOW - timedelta(hours=1)).isoformat(),
        "expires_at": (NOW + timedelta(minutes=15)).isoformat(),
    }
    item.update(over)
    return item


class RepGrantsFile(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, data: Any) -> str:
        path = Path(self.tmp.name) / "grants.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return str(path)

    def test_absent_setting_adds_no_grants(self) -> None:
        self.assertEqual(load_grants(None), ())
        self.assertEqual(load_grants(""), ())

    def test_valid_file_loads_task_limited_grant_with_recorded_expiry(self) -> None:
        (grant,) = load_grants(self.write([grant_item()]))
        self.assertEqual(grant.tasks, ("Receive information",))
        self.assertEqual(grant.expires_at, NOW + timedelta(minutes=15))
        self.assertFalse(grant.revoked)

    def test_unsafe_files_fail_closed_without_echoing_values(self) -> None:
        bad: list[Any] = [
            [grant_item(expires_at=None)],
            [grant_item(expires_at="2026-10-25T12:15:00+01:00")],
            [grant_item(expires_at=(NOW - timedelta(hours=2)).isoformat())],
            [grant_item(expires_at="2099-01-01T00:00:00+00:00")],
            [grant_item(extra="x")],
            [grant_item(tasks="Receive information")],
            [grant_item(representative_ref="Unknown")],
            [grant_item(revoked="no")],
            {"not": "a list"},
        ]
        for data in bad:
            with self.subTest(data=str(data)[:60]):
                with self.assertRaises(rs.ShowcaseConfigError) as ctx:
                    load_grants(self.write(data))
                self.assertNotIn("example.com", str(ctx.exception))
        for path in ("relative.json", str(Path(self.tmp.name) / "missing.json")):
            with self.assertRaises(rs.ShowcaseConfigError):
                load_grants(path)

    def test_loaded_grant_gives_a_live_task_limited_view_that_expires(self) -> None:
        clock = Clock()
        row = make_row(
            "SYN-REP-01",
            "resident.01@example.com",
            address="10 Private Resident Walk",
            measures=("Loft insulation", "Cavity wall"),
        )

        class Reader:
            def list_rows(self) -> list[rs.ShowcaseRow]:
                return [row]

            def fetch_case(self, case_id: str) -> rs.ShowcaseRow | None:
                return row if case_id == row.case_id else None

        app = demo.ResidentDemo(
            Reader(),
            rs.build_identity_map([row], NOW),
            rs.PasswordVerifier(rs.make_verifier(FAKE_PASSWORD, n=2**14)),
            rs.SessionCodec(KEY, NOW + timedelta(hours=6), clock),
            rs.LoginLimiter(clock=clock),
            (HOST,),
            NOW + timedelta(hours=6),
            "127.0.0.1",
            0,
            clock,
            representative_grants=load_grants(self.write([grant_item()])),
        )
        server = demo.serve(app)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        rep = Client(app.port)
        self.assertEqual(rep.login("rep.info@example.com"), 200)
        code, view, _ = rep.call("GET", "/demo/view")
        self.assertEqual(code, 200)
        self.assertTrue(view["active"])
        self.assertEqual([m["measure"] for m in view["measures"]], ["Loft insulation"])
        text = json.dumps(view)
        self.assertNotIn("Cavity wall", text)
        self.assertNotIn("10 Private Resident Walk", text)
        clock.now += 16 * 60
        code, view, _ = rep.call("GET", "/demo/view")
        self.assertFalse(view.get("active", False))


if __name__ == "__main__":
    unittest.main()
