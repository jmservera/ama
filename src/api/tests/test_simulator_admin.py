"""Administrator simulator run control (#189): authorization, guards, status, failed writes."""

import hashlib
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from datetime import UTC, datetime
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core import identity
from zava_forward.core.synthetic.sensor_stream import StreamError

from test_auth import ENV, OID_NEW, OID_SAM, TENANT, Base, principal
from zava_forward.api import auth, live_control, simulator_admin
from zava_forward.api.live_simulator import check_capacity as real_capacity
from zava_forward.api.server import App, make_handler

ADMIN = "ZavaForward.ApplicationAdmin"
STAFF = "ZavaForward.LiaisonOfficer"
CONTRACTOR = "ZavaForward.Contractor"
NOW = datetime(2026, 11, 9, 10, 0, tzinfo=UTC)
EXPIRES = "2026-11-10T10:00:00Z"
PATH = "/api/admin/simulator-control"
HOMES = [f"HOME-{i:03d}" for i in range(5)]
Provider: Any = auth.TrustedProxyProvider
Application: Any = App
handler: Any = make_handler


def start_body(**changes: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "owner": "demo owner",
        "approval_reference": "issue-184-comment-6652226413",
        "expires_at": EXPIRES,
        "homes": HOMES[:3],
        "expected_revision": "absent",
        "confirm": True,
    }
    return base | changes


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FakeStore:
    def __init__(self, fail: bool = False) -> None:
        self.entries: list[tuple[str, ...]] = []
        self.fail = fail

    def audit(self, *entry: str) -> None:
        if self.fail:
            raise OSError("audit down")
        self.entries.append(entry)


class AdminModuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = Path(self.tmp.name) / "control.json"
        self.env = {simulator_admin.ENV: str(self.file)}
        self.store = FakeStore()
        self.admin: dict[str, Any] = identity.principal(
            TENANT, OID_NEW, identity.ADMIN_ROLE_NAME, app_admin=True, view_only=False
        )
        self.read_only: dict[str, Any] = dict(self.admin, view_only=True)

    def call(
        self, method: str, path: str, body: Any = None, user: Any = None
    ) -> tuple[int, dict[str, Any]]:
        return simulator_admin.handle(
            self.store, self.admin if user is None else user, method, path, body, self.env, NOW
        )

    def start(self, **changes: Any) -> tuple[int, dict[str, Any]]:
        return self.call("POST", PATH + "/start", start_body(**changes))

    def test_only_a_verified_entra_application_admin_is_served(self) -> None:
        staff = identity.principal(TENANT, OID_SAM, "Resident Liaison Officer")
        contractor = identity.principal(TENANT, OID_SAM, "Contractor")
        forged = dict(self.admin, oid=OID_NEW.upper())
        legacy = {"role": "Application Administrator", "app_admin": True, "email": "a@example.test"}
        truthy = dict(self.admin, app_admin="yes")
        for label, user in (
            ("staff", staff),
            ("contractor", contractor),
            ("forged", forged),
            ("legacy", legacy),
            ("truthy", truthy),
            ("none", None),
        ):
            for method, path in (
                ("GET", PATH),
                ("POST", PATH + "/start"),
                ("POST", PATH + "/stop"),
                ("GET", PATH + "/other"),
            ):
                with self.subTest(label=label, method=method, path=path):
                    code, body = simulator_admin.handle(
                        self.store,
                        user,  # type: ignore[arg-type]
                        method,
                        path,
                        start_body(),
                        self.env,
                        NOW,
                    )
                    self.assertEqual((code, body["code"]), (403, "ADMIN_REQUIRED"))
                    self.assertFalse(self.file.exists())
                    self.assertNotIn("owner", body)

    def test_view_only_administrator_reads_status_but_cannot_start_or_stop(self) -> None:
        self.assertEqual(self.start()[0], 200)
        before = digest(self.file)
        revision = simulator_admin._snapshot(self.file)[0]
        self.assertEqual(revision, before)
        entries = len(self.store.entries)
        locks = sorted(Path(self.tmp.name).iterdir())
        for path, body in (
            (PATH + "/start", start_body(expected_revision=revision)),
            (PATH + "/stop", {"expected_revision": revision, "confirm": True}),
        ):
            for user in (self.read_only, dict(self.read_only, view_only="yes")):
                with self.subTest(path=path, view_only=user["view_only"]):
                    code, out = self.call("POST", path, body, user)
                    self.assertEqual((code, out["code"]), (403, "VIEW_ONLY"))
                    self.assertNotIn("owner", out)
                    self.assertEqual(digest(self.file), before)
                    self.assertEqual(len(self.store.entries), entries)
                    self.assertEqual(sorted(Path(self.tmp.name).iterdir()), locks)
        code, status = self.call("GET", PATH, user=self.read_only)
        self.assertEqual((code, status["state"], status["read_only"]), (200, "send", True))
        self.assertFalse(status["writable"])
        self.assertFalse(self.call("GET", PATH)[1]["read_only"])

    def test_unconfigured_and_missing_file_are_unavailable_and_refuse_writes(self) -> None:
        code, status = simulator_admin.handle(self.store, self.admin, "GET", PATH, None, {}, NOW)
        self.assertEqual(
            (code, status["availability"], status["state"]), (200, "not_configured", None)
        )
        self.assertFalse(status["budget_alert"]["live_verified"])
        self.assertIn("manual route", status["manual_route"].lower())
        for action in ("start", "stop"):
            code, body = simulator_admin.handle(
                self.store, self.admin, "POST", f"{PATH}/{action}", start_body(), {}, NOW
            )
            self.assertEqual((code, body["code"]), (503, "CONTROL_NOT_CONFIGURED"))
        code, status = self.call("GET", PATH)
        self.assertEqual(
            (status["availability"], status["revision"], status["state"]),
            ("unavailable", "absent", None),
        )
        self.assertEqual(
            self.call("POST", PATH + "/stop", {"expected_revision": "absent", "confirm": True})[1][
                "code"
            ],
            "NOTHING_TO_STOP",
        )

    def test_start_writes_the_existing_schema_and_status_is_truthful(self) -> None:
        code, body = self.start()
        self.assertEqual(
            (code, body["ok"], body["changed"], body["audit_recorded"]), (200, True, True, True)
        )
        control = live_control.load(self.file)
        self.assertEqual(
            (control.enabled, control.owner, len(control.homes)), (True, "demo owner", 3)
        )
        status = body["status"]
        self.assertEqual(
            (status["state"], status["activity"], status["cohort_size"]), ("send", "unverified", 3)
        )
        self.assertEqual(status["owner"]["status"], "declared_unverified")
        self.assertEqual(status["approval_reference"]["status"], "declared_unverified")
        self.assertEqual(
            status["budget_alert"],
            {
                "status": "not_recorded",
                "live_verified": False,
                "detail": simulator_admin.ALERT_DETAIL,
            },
        )
        self.assertNotIn("issue-184", json.dumps(status["budget_alert"]))
        self.assertEqual(status["capacity"]["messages_per_day"], 3 * 288)
        self.assertNotIn("HOME-000", json.dumps(status))
        self.assertEqual(self.store.entries[0][1:3], ("sim_control_start", "-"))
        self.assertNotIn("HOME-000", " ".join(self.store.entries[0]))

    def test_status_of_expired_stopped_and_oversized_expiry_controls(self) -> None:
        control = live_control.parse(
            {
                "version": live_control.VERSION,
                "enabled": True,
                "expires_at": "2026-11-09T09:00:00Z",
                "approval_reference": "ref",
                "owner": "owner",
                "homes": HOMES[:2],
            }
        )
        live_control.write(self.file, control)
        status = self.call("GET", PATH)[1]
        self.assertEqual(
            (status["state"], status["time_limit"]["remaining_seconds"]), ("expired", 0)
        )
        far = live_control.Control(
            True, datetime(2026, 12, 30, tzinfo=UTC), "ref", "owner", tuple(HOMES[:2])
        )
        live_control.write(self.file, far)
        self.assertEqual(self.call("GET", PATH)[1]["state"], "invalid")
        live_control.write(
            self.file,
            live_control.Control(
                False, datetime(2026, 11, 10, tzinfo=UTC), "ref", "owner", tuple(HOMES[:2])
            ),
        )
        self.assertEqual(self.call("GET", PATH)[1]["state"], "stopped")

    def test_invalid_and_unreadable_files_are_reported_not_hidden(self) -> None:
        self.file.write_text("not json", encoding="utf-8")
        status = self.call("GET", PATH)[1]
        self.assertEqual(
            (status["availability"], status["state"], status["owner"]), ("invalid", None, None)
        )
        self.assertEqual(status["revision"], digest(self.file))
        self.file.write_text(json.dumps({"version": "v0"}), encoding="utf-8")
        self.assertEqual(self.call("GET", PATH)[1]["availability"], "invalid")
        os.chmod(self.file, 0)
        try:
            readable = os.access(self.file, os.R_OK)
            status = self.call("GET", PATH)[1]
            if not readable:
                self.assertEqual(
                    (status["availability"], status["revision"]), ("unavailable", "unreadable")
                )
        finally:
            os.chmod(self.file, 0o600)

    def test_an_invalid_file_can_be_replaced_with_its_revision(self) -> None:
        self.file.write_text("not json", encoding="utf-8")
        self.assertEqual(self.start()[1]["code"], "STALE_CONTROL")
        code, body = self.start(expected_revision=digest(self.file))
        self.assertEqual((code, body["status"]["state"]), (200, "send"))

    def test_start_refuses_every_existing_guard_and_writes_nothing(self) -> None:
        cases: dict[str, tuple[dict[str, Any], str]] = {
            "owner placeholder": ({"owner": "tbd"}, "CONTROL_INVALID"),
            "owner template": ({"owner": "<name>"}, "CONTROL_INVALID"),
            "owner control character": ({"owner": "a\u202eb"}, "CONTROL_INVALID"),
            "owner too long": ({"owner": "x" * 161}, "CONTROL_INVALID"),
            "owner not text": ({"owner": 7}, "CONTROL_INVALID"),
            "approval blank": ({"approval_reference": " "}, "CONTROL_INVALID"),
            "no homes": ({"homes": []}, "CONTROL_INVALID"),
            "duplicate homes": ({"homes": [HOMES[0], HOMES[0]]}, "CONTROL_INVALID"),
            "too many homes": ({"homes": [f"HOME-{i:03d}" for i in range(101)]}, "CONTROL_INVALID"),
            "homes not list": ({"homes": "HOME-001"}, "CONTROL_INVALID"),
            "bad stamp": ({"expires_at": "2026-11-10"}, "CONTROL_INVALID"),
            "past expiry": ({"expires_at": "2026-11-09T09:00:00Z"}, "CONTROL_WINDOW_INVALID"),
            "beyond 14 days": ({"expires_at": "2026-11-24T10:00:01Z"}, "CONTROL_WINDOW_INVALID"),
            "no confirmation": ({"confirm": False}, "CONFIRMATION_REQUIRED"),
            "truthy confirmation": ({"confirm": "true"}, "CONFIRMATION_REQUIRED"),
            "unknown field": ({"enabled": False}, "BODY_INVALID"),
            "missing revision": ({"expected_revision": None}, "BODY_INVALID"),
        }
        for label, (change, code) in cases.items():
            with self.subTest(label):
                status, body = self.start(**change)
                self.assertEqual((status, body["code"]), (400, code))
                self.assertFalse(self.file.exists())
        self.assertEqual(self.call("POST", PATH + "/start", {})[1]["code"], "BODY_INVALID")
        self.assertEqual(self.store.entries, [])

    def test_start_reuses_the_existing_quota_check_and_cannot_bypass_it(self) -> None:
        with patch.object(
            simulator_admin,
            "check_capacity",
            side_effect=StreamError("B1_QUOTA_HEADROOM"),
        ):
            code, body = self.start()
        self.assertEqual((code, body["code"]), (400, "B1_QUOTA_HEADROOM"))
        self.assertFalse(self.file.exists())
        seen: list[int] = []

        def spy(n: int, limits: Any) -> Any:
            seen.append(n)
            return real_capacity(n, limits)

        with patch.object(
            simulator_admin,
            "check_capacity",
            side_effect=spy,
        ):
            self.assertEqual(self.start()[0], 200)
        self.assertTrue(seen and set(seen) == {3})

    def test_a_second_start_stale_and_replayed_requests_are_refused(self) -> None:
        self.assertEqual(self.start()[0], 200)
        before = self.file.read_bytes()
        code, body = self.start(homes=HOMES[:4], expected_revision=digest(self.file))
        self.assertEqual((code, body["code"]), (409, "ALREADY_RUNNING"))
        self.assertEqual(self.start()[1]["code"], "STALE_CONTROL")
        self.assertEqual(self.file.read_bytes(), before)
        self.assertEqual(len(self.store.entries), 1)

    def test_stop_is_confirmed_idempotent_and_keeps_the_record(self) -> None:
        self.start()
        revision = digest(self.file)
        self.assertEqual(
            self.call("POST", PATH + "/stop", {"expected_revision": revision, "confirm": False})[1][
                "code"
            ],
            "CONFIRMATION_REQUIRED",
        )
        self.assertEqual(
            self.call("POST", PATH + "/stop", {"expected_revision": "old", "confirm": True})[1][
                "code"
            ],
            "STALE_CONTROL",
        )
        self.assertTrue(live_control.load(self.file).enabled)
        code, body = self.call(
            "POST", PATH + "/stop", {"expected_revision": revision, "confirm": True}
        )
        self.assertEqual((code, body["changed"], body["status"]["state"]), (200, True, "stopped"))
        control = live_control.load(self.file)
        self.assertEqual(
            (control.enabled, control.owner, len(control.homes)), (False, "demo owner", 3)
        )
        code, again = self.call(
            "POST", PATH + "/stop", {"expected_revision": digest(self.file), "confirm": True}
        )
        self.assertEqual((code, again["changed"], again["audit_recorded"]), (200, False, None))
        self.assertEqual(
            [e[1] for e in self.store.entries], ["sim_control_start", "sim_control_stop"]
        )

    def test_stop_works_on_an_expired_enabled_control(self) -> None:
        live_control.write(
            self.file,
            live_control.Control(
                True, datetime(2026, 11, 9, 9, tzinfo=UTC), "ref", "owner", tuple(HOMES[:2])
            ),
        )
        code, body = self.call(
            "POST", PATH + "/stop", {"expected_revision": digest(self.file), "confirm": True}
        )
        self.assertEqual((code, body["status"]["state"]), (200, "expired"))
        self.assertFalse(live_control.load(self.file).enabled)

    def test_a_stopped_control_can_start_again_with_the_same_guards(self) -> None:
        self.start()
        self.call("POST", PATH + "/stop", {"expected_revision": digest(self.file), "confirm": True})
        code, body = self.start(
            expected_revision=digest(self.file), expires_at="2026-11-24T10:00:01Z"
        )
        self.assertEqual((code, body["code"]), (400, "CONTROL_WINDOW_INVALID"))
        code, body = self.start(expected_revision=digest(self.file), owner="second owner")
        self.assertEqual((code, body["status"]["owner"]["value"]), (200, "second owner"))

    def test_failed_write_is_surfaced_and_leaves_the_file_unchanged(self) -> None:
        self.start()
        before = self.file.read_bytes()
        stop = {"expected_revision": digest(self.file), "confirm": True}
        with patch.object(live_control, "write", side_effect=OSError("disk full: /secret/path")):
            code, body = self.call("POST", PATH + "/stop", stop)
        self.assertEqual((code, body["code"]), (503, "WRITE_FAILED"))
        self.assertNotIn("secret", json.dumps(body))
        self.assertEqual(self.file.read_bytes(), before)
        self.assertEqual(len(self.store.entries), 1)

    def test_a_write_that_cannot_be_read_back_is_reported_unverified(self) -> None:
        with patch.object(live_control, "write", lambda path, control: None):
            code, body = self.start()
        self.assertEqual((code, body["code"]), (503, "WRITE_NOT_VERIFIED"))
        self.assertEqual(self.store.entries, [])

    def test_missing_directory_and_a_held_lock_refuse_without_changes(self) -> None:
        missing = {simulator_admin.ENV: str(Path(self.tmp.name) / "none" / "control.json")}
        code, body = simulator_admin.handle(
            self.store, self.admin, "POST", PATH + "/start", start_body(), missing, NOW
        )
        self.assertEqual((code, body["code"]), (503, "CONTROL_UNAVAILABLE"))
        self.assertFalse(
            simulator_admin.handle(self.store, self.admin, "GET", PATH, None, missing, NOW)[1][
                "writable"
            ]
        )
        with live_control.locked(self.file):
            code, body = self.start()
            self.assertEqual((code, body["code"]), (409, "CONTROL_BUSY"))
            cli = live_control.main(["stop", "--file", str(self.file)], NOW)
            self.assertEqual(cli, 2)
        self.assertFalse(self.file.exists())

    def test_racing_starts_produce_exactly_one_success(self) -> None:
        results: list[int] = []
        barrier = threading.Barrier(6)

        def run(index: int) -> None:
            barrier.wait()
            code, _ = self.start(owner=f"owner {index}")
            results.append(code)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(6)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(results.count(200), 1, results)
        self.assertTrue(all(code in (200, 409) for code in results), results)
        self.assertEqual(len(self.store.entries), 1)

    def test_audit_failure_is_surfaced_not_hidden(self) -> None:
        self.store = FakeStore(fail=True)
        code, body = self.start()
        self.assertEqual((code, body["changed"], body["audit_recorded"]), (200, True, False))
        self.assertTrue(live_control.load(self.file).enabled)

    def test_cli_and_surface_share_the_same_file_and_guards(self) -> None:
        self.assertEqual(
            live_control.main(
                [
                    "start",
                    "--file",
                    str(self.file),
                    "--expires-at",
                    EXPIRES,
                    "--approval",
                    "ref",
                    "--owner",
                    "cli owner",
                    "--homes",
                    "HOME-001",
                ],
                NOW,
            ),
            0,
        )
        status = self.call("GET", PATH)[1]
        self.assertEqual((status["state"], status["owner"]["value"]), ("send", "cli owner"))
        self.assertEqual(
            self.start(expected_revision=status["revision"])[1]["code"], "ALREADY_RUNNING"
        )


class AdminHttpTests(Base):  # type: ignore[misc]
    def setUp(self) -> None:
        super().setUp()
        self.control_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.control_dir.cleanup)
        self.file = Path(self.control_dir.name) / "control.json"
        patcher = patch.dict(os.environ, {simulator_admin.ENV: str(self.file)})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), handler(Application(self.store, provider=Provider(self.store, ENV)))
        )
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.addCleanup(self.httpd.server_close)
        self.addCleanup(self.httpd.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        roles: tuple[str, ...] | None = (ADMIN,),
        csrf: bool = True,
        header: str | None = None,
        **kw: Any,
    ) -> tuple[int, Any]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if header is not None:
            headers["X-MS-CLIENT-PRINCIPAL"] = header
        elif roles is not None:
            headers["X-MS-CLIENT-PRINCIPAL"] = principal(roles=roles, **kw)
        if csrf:
            headers["X-ZF-CSRF"] = "1"
        data = None if body is None else json.dumps(body).encode()
        try:
            with urllib.request.urlopen(
                urllib.request.Request(self.base + path, data=data, headers=headers, method=method)
            ) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            raw = e.read()
            return e.code, (json.loads(raw) if raw else {})

    def test_boundary_matrix_refuses_without_disclosure_or_change(self) -> None:
        good = start_body()
        principals: dict[str, dict[str, Any]] = {
            "no principal": dict(roles=None),
            "malformed principal": dict(header="e30="),
            "garbage principal": dict(header="%%%"),
            "wrong tenant": dict(roles=(ADMIN,), tid="99999999-2222-3333-4444-555555555555"),
            "no object id": dict(roles=(ADMIN,), oid=None),
            "no tenant": dict(roles=(ADMIN,), tid=None),
            "bearer auth type admin": dict(roles=(ADMIN,), typ="saml"),
            "staff without admin": dict(roles=(STAFF,)),
            "contractor": dict(roles=(CONTRACTOR,)),
            "contractor with admin": dict(roles=(CONTRACTOR, ADMIN)),
            "unmapped role": dict(roles=("ZavaForward.Nope",)),
        }
        for label, kwargs in principals.items():
            for method, path, body in (
                ("GET", PATH, None),
                ("POST", PATH + "/start", good),
                ("POST", PATH + "/stop", {"expected_revision": "absent", "confirm": True}),
            ):
                with self.subTest(label=label, method=method, path=path):
                    code, out = self.request(method, path, body, **kwargs)
                    self.assertIn(code, (401, 403))
                    self.assertNotIn("revision", out)
                    self.assertNotIn("owner", out)
                    self.assertFalse(self.file.exists())

    def test_missing_csrf_header_is_refused_before_any_change(self) -> None:
        code, _ = self.request("POST", PATH + "/start", start_body(), csrf=False)
        self.assertEqual(code, 403)
        self.assertFalse(self.file.exists())

    def test_lookalike_paths_never_reach_the_control(self) -> None:
        for path in (
            PATH + "s",
            PATH + "-x",
            "/api/admin/simulator",
            PATH.replace("admin", "Admin"),
        ):
            with self.subTest(path=path):
                code, out = self.request("POST", path, start_body())
                self.assertIn(code, (403, 404))
                self.assertNotIn("revision", out)
        for path in (PATH + "/start/x", PATH + "/other"):
            self.assertEqual(self.request("POST", path, start_body(), roles=(ADMIN, STAFF))[0], 404)
            self.assertEqual(self.request("POST", path, start_body())[0], 403)
        self.assertEqual(self.request("GET", PATH + "/start")[0], 404)
        self.assertFalse(self.file.exists())

    def test_administrator_alone_reads_status_and_the_server_gate_denies_writes(self) -> None:
        status = self.request("GET", PATH, oid=OID_NEW)[1]
        self.assertEqual(
            (status["availability"], status["read_only"], status["writable"]),
            ("unavailable", True, False),
        )
        code, body = self.request("POST", PATH + "/start", start_body(), oid=OID_NEW)
        self.assertEqual(code, 403)
        self.assertIn("changes nothing", body["error"])
        self.assertNotIn("code", body)
        self.assertFalse(self.file.exists())
        for path in (
            "/api/cases",
            "/api/stats",
            "/api/finance/queue",
            "/api/audit",
            "/api/cases.csv",
        ):
            self.assertEqual(self.request("GET", path, oid=OID_NEW)[0], 403, path)
        for path in ("/api/time/enable", "/api/cases/ZF-1/notes"):
            self.assertEqual(self.request("POST", path, {}, oid=OID_NEW)[0], 403, path)
        me = self.request("GET", "/api/me", oid=OID_NEW)[1]
        self.assertTrue(
            all(d["access"] == "needs a role with this authority" for d in me["navigation"])
        )
        self.assertIn("Simulator control", [d["label"] for d in me["navigation"]])
        self.assertEqual((me["counts"], me["staff"]), ({}, []))
        staffed = self.request("GET", "/api/me", roles=(ADMIN, STAFF), oid=OID_NEW)[1]
        self.assertEqual(
            [d["access"] for d in staffed["navigation"] if d["href"] == "#/simulator"],
            ["available"],
        )

    def test_view_only_administrator_stop_and_start_are_denied_before_the_module(self) -> None:
        self.assertEqual(
            self.request("POST", PATH + "/start", start_body(), roles=(ADMIN, STAFF))[0], 200
        )
        before = digest(self.file)
        entries = len(list(self.store.audit_entries()))
        for path, body in (
            (PATH + "/start", start_body(expected_revision=before)),
            (PATH + "/stop", {"expected_revision": before, "confirm": True}),
        ):
            with self.subTest(path=path), patch.object(simulator_admin, "handle") as module:
                code, out = self.request("POST", path, body, oid=OID_NEW)
                self.assertEqual(code, 403)
                self.assertIn("changes nothing", out["error"])
                module.assert_not_called()
            self.assertEqual(digest(self.file), before)
            self.assertEqual(len(list(self.store.audit_entries())), entries)
        for path, body in (
            (PATH + "/start", start_body(expected_revision=before)),
            (PATH + "/stop", {"expected_revision": before, "confirm": True}),
        ):
            code, out = simulator_admin.handle(
                self.store, dict(self.admin_user(), view_only=True), "POST", path, body
            )
            self.assertEqual((code, out["code"]), (403, "VIEW_ONLY"))
        self.assertEqual(digest(self.file), before)

    def admin_user(self) -> dict[str, Any]:
        user: dict[str, Any] = identity.principal(
            TENANT, OID_NEW, identity.ADMIN_ROLE_NAME, app_admin=True, view_only=False
        )
        return user

    def test_admin_with_a_staff_role_is_served_and_the_staff_role_only_is_not(self) -> None:
        self.assertEqual(self.request("GET", PATH, roles=(ADMIN, STAFF))[0], 200)
        self.assertEqual(self.request("GET", PATH, roles=(STAFF,))[0], 403)
        self.assertEqual(
            self.request("POST", PATH + "/start", start_body(), roles=(STAFF,))[0], 403
        )
        self.assertFalse(self.file.exists())

    def test_start_stop_round_trip_over_http_with_audit(self) -> None:
        both = (ADMIN, STAFF)
        code, started = self.request("POST", PATH + "/start", start_body(), roles=both)
        self.assertEqual((code, started["changed"]), (200, True))
        revision = started["status"]["revision"]
        code, second = self.request(
            "POST", PATH + "/start", start_body(expected_revision=revision), roles=both
        )
        self.assertEqual((code, second["code"]), (409, "ALREADY_RUNNING"))
        code, stopped = self.request(
            "POST", PATH + "/stop", {"expected_revision": revision, "confirm": True}, roles=both
        )
        self.assertEqual((code, stopped["status"]["state"]), (200, "stopped"))
        actions = [e["action"] for e in self.store.audit_entries()]
        self.assertEqual(actions[-2:], ["sim_control_start", "sim_control_stop"])

    def test_password_provider_user_cannot_use_the_surface(self) -> None:
        provider = auth.PasswordProvider(self.store, "synthetic")
        user = provider.authenticate(
            {"Cookie": f"zf_session={provider.login('sam@example.test', 'synthetic')}"}
        )
        self.assertIsNotNone(user)
        self.assertEqual(simulator_admin.handle(self.store, user, "GET", PATH)[0], 403)


if __name__ == "__main__":
    unittest.main()
