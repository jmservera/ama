"""Independent XLSX fixtures and durable, role-scoped coordination data oracles."""
import base64
from copy import deepcopy
import hashlib
from http.server import ThreadingHTTPServer
import io
import json
from pathlib import Path
import shutil
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request
import uuid
from xml.sax.saxutils import escape
import zipfile

from properwarm_mvp.exercise import MAX_WORKBOOK_BYTES, read_case_updates
from properwarm_mvp.factory import open_store
from properwarm_mvp.server import App, get_kind, make_handler

HOME = "EX-HOME-001"
SIBLING = "EX-HOME-002"
HEADERS = ["case_id", "coordination_note", "task_due_date"]
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def workbook(rows, *, headers=None, shared=False, formula=False, dtd=False, extra=None):
    """Generate OOXML bytes independently of the production parser."""
    headers = HEADERS if headers is None else headers
    strings = []
    physical = []
    for number, values in enumerate([headers, *rows], 1):
        cells = []
        for index, value in enumerate(values):
            ref = f"{chr(65 + index)}{number}"
            if formula and number == 2 and index == 1:
                cells.append(f'<c r="{ref}"><f>1+1</f><v>2</v></c>')
            elif shared:
                strings.append(str(value))
                cells.append(f'<c r="{ref}" t="s"><v>{len(strings) - 1}</v></c>')
            else:
                cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>')
        physical.append(f'<row r="{number}">{"".join(cells)}</row>')
    raw = io.BytesIO()
    with zipfile.ZipFile(raw, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("xl/workbook.xml",
                         f'<workbook xmlns="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                         '<sheets><sheet name="Case updates" sheetId="1" r:id="rId7"/></sheets></workbook>')
        archive.writestr("xl/_rels/workbook.xml.rels",
                         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                         '<Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet7.xml"/>'
                         '</Relationships>')
        declaration = '<!DOCTYPE worksheet [<!ENTITY x "unsafe">]>' if dtd else ""
        archive.writestr("xl/worksheets/sheet7.xml",
                         f'{declaration}<worksheet xmlns="{NS}"><sheetData>{"".join(physical)}</sheetData></worksheet>')
        if shared:
            archive.writestr("xl/sharedStrings.xml",
                             f'<sst xmlns="{NS}">\n' + "".join(f'<si><t>{escape(value)}</t></si>\n' for value in strings) + "</sst>")
        for name, value in (extra or {}).items():
            archive.writestr(name, value)
    return raw.getvalue()


class ExerciseDataTests(unittest.TestCase):
    def setUp(self):
        self.root = Path.cwd() / ".exercise-test-state" / uuid.uuid4().hex
        self.env = patch.dict("os.environ", {"PW_EXERCISE": "1", "PW_STATE": str(self.root),
                                            "PW_STORE": "sqlite", "PW_DOC_STORE": "local",
                                            "PW_AI": "off"}, clear=True)
        self.env.start()
        self.store = open_store()
        self.users = {u["code"]: u for u in self.store.staff.values()}
        self.pm = self.users["EX-PM-01"]
        self.contractor = self.users["EX-CON-01"]

    def tearDown(self):
        self.store.db.close()
        self.env.stop()
        shutil.rmtree(self.root)
        try:
            self.root.parent.rmdir()
        except OSError:
            pass

    def preview(self, ids=None, changes=None):
        return self.store.exercise_data_action(self.pm, dict(
            action="bulk-preview", reason="Explicit exercise coordination",
            case_ids=[HOME, SIBLING] if ids is None else ids,
            changes={"coordination_note": "Call the team, not a resident consent."} if changes is None else changes))

    def import_preview(self, raw, fields=None):
        return self.store.exercise_data_action(self.pm, dict(
            action="import-preview", reason="Supplied workbook checked",
            filename="updates.xlsx", fields=["coordination_note", "task_due_date"] if fields is None else fields), raw)

    def commit(self, preview, user=None):
        return self.store.exercise_data_action(user or self.pm, dict(
            action="commit", token=preview["token"], input_hash=preview["input_hash"],
            expected_fingerprints={str(row["row"]): row["expected_fingerprint"] for row in preview["rows"]}))

    def test_workbook_namespace_shared_strings_mapping_and_immutable_lineage(self):
        raw = workbook([[HOME, "Call team & confirm task", "2026-10-20"]], shared=True)
        before_hash = hashlib.sha256(raw).hexdigest()
        preview = self.import_preview(raw)
        row = preview["rows"][0]
        self.assertEqual(row["row"], 2)
        self.assertEqual(row["case_id"], HOME)
        self.assertEqual(row["changes"]["coordination_note"], "Call team & confirm task")
        self.assertEqual(row["status"], "ready")
        self.assertEqual(preview["lineage"]["source_sha256"], before_hash)
        self.assertEqual(preview["lineage"]["mapping"], dict(zip("ABC", HEADERS)))
        self.assertTrue(preview["lineage"]["source_unchanged"])
        sibling = deepcopy(self.store._case(SIBLING))
        stock = deepcopy(self.store._case(HOME)["home"])
        owner = self.store._case(HOME)["owner_code"]
        self.assertNotIn("coordination_note", self.store._case(HOME)["exercise"])
        self.store.db.close()
        self.store = open_store()
        result = self.commit(preview)
        self.assertEqual((result["committed"], result["errors"]), (1, 0))
        self.assertEqual(self.store._case(HOME)["exercise"]["task_due_date"], "2026-10-20")
        self.assertEqual(self.store._case(HOME)["home"], stock)
        self.assertEqual(self.store._case(HOME)["owner_code"], owner)
        self.assertEqual(self.store._case(SIBLING), sibling)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), before_hash)
        history = self.store._case(HOME)["exercise"]["data_history"]
        self.assertEqual(history[0]["lineage"]["source_sha256"], before_hash)
        self.assertEqual(history[0]["actor"], self.pm["email"])
        self.assertIsNone(history[0]["before"]["coordination_note"])
        self.assertEqual(self.commit(preview), result)
        self.assertEqual(len(self.store._case(HOME)["exercise"]["data_history"]), 1)
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_duplicate_unknown_controlled_formula_rows_have_explicit_outcomes(self):
        raw = workbook([[HOME, "note", "2026-10-20"], [HOME, "different", "2026-10-21"],
                        ["NO-HOME", "unknown", "2026-10-20"], [SIBLING, "valid", "2026-10-20"]])
        preview = self.import_preview(raw)
        self.assertEqual([r["status"] for r in preview["rows"]], ["error", "error", "error", "ready"])
        result = self.commit(preview)
        self.assertEqual((result["committed"], result["errors"]), (1, 3))
        self.assertNotIn("coordination_note", self.store._case(HOME)["exercise"])
        self.assertEqual(self.store._case(SIBLING)["exercise"]["coordination_note"], "valid")
        preview = self.import_preview(workbook([[HOME, "note", "2026-10-20"]], formula=True))
        self.assertIn("formulas unsupported", " ".join(preview["rows"][0]["errors"]))
        self.assertEqual(self.commit(preview)["committed"], 0)
        for controlled in ("owner_email", "owner_code", "funding_ok", "declaration", "signature",
                           "safety_release", "decision", "claim_amount", "payment", "quality_acceptance"):
            with self.subTest(controlled=controlled):
                preview = self.import_preview(workbook([[HOME, "note", "2026-10-20", "true"]],
                                                      headers=[*HEADERS, controlled]))
                self.assertTrue(preview["rows"][0]["errors"])
                self.assertEqual(self.commit(preview)["committed"], 0)

    def test_stale_preview_reports_each_case_and_forged_inputs_are_rejected(self):
        preview = self.preview()
        with self.store.lock:
            self.store._case(HOME)["exercise"]["unknowns"].append("Current case changed")
            self.store.save()
        result = self.commit(preview)
        self.assertEqual((result["committed"], result["errors"]), (1, 1))
        self.assertIn("Stale case", result["outcomes"][0]["errors"][0])
        self.assertNotIn("coordination_note", self.store._case(HOME)["exercise"])
        self.assertEqual(self.store._case(SIBLING)["exercise"]["coordination_note"],
                         preview["rows"][1]["changes"]["coordination_note"])
        forged = deepcopy(preview)
        forged["input_hash"] = "client-generated"
        with self.assertRaises(ValueError):
            self.commit(forged)
        forged = deepcopy(preview)
        forged["rows"][0]["expected_fingerprint"] = "client-generated"
        with self.assertRaises(ValueError):
            self.commit(forged)
        with self.assertRaises(PermissionError):
            self.commit(preview, self.users["EX-PM-02"])

    def test_server_owned_authority_and_no_controlled_bulk_fields(self):
        for code in ("EX-CON-01", "EX-RC-01", "EX-RLO-01", "EX-GEO-01", "EX-QI-01", "EX-BSL-01"):
            with self.subTest(code=code), self.assertRaises(PermissionError):
                self.store.exercise_data_action(self.users[code], dict(action="bulk-preview"))
        forged = dict(self.contractor, role="Retrofit Programme Manager")
        with self.assertRaises(PermissionError):
            self.store.exercise_data_action(forged, dict(action="bulk-preview"))
        before_owner = self.store._case(HOME)["owner_code"]
        for changes in ({"owner_email": self.pm["email"]}, {"funding_ok": True},
                        {"consent": True}, {"claim_amount": "7500 GBP"}, {"task_due_date": "45234"},
                        {"task_due_date": "2026-02-30"}, {"coordination_note": "x" * 301},
                        {"coordination_note": ""}, {}):
            with self.subTest(changes=changes):
                preview = self.preview([HOME], changes)
                self.assertEqual(preview["rows"][0]["status"], "error")
                self.assertEqual(self.commit(preview)["committed"], 0)
        self.assertEqual(self.store._case(HOME)["owner_code"], before_owner)
        self.assertFalse(self.store._case(HOME)["funding_ok"])
        with self.assertRaises(ValueError):
            self.preview([HOME] * 26)
        with self.assertRaises(ValueError):
            self.preview([])
        preview = self.preview([HOME, HOME])
        self.assertTrue(all(row["errors"] for row in preview["rows"]))
        preview = self.preview(["unknown", None])
        self.assertIsNone(preview["token"])
        self.assertTrue(all(row["errors"] for row in preview["rows"]))

    def test_workbook_bounds_entities_mapping_and_wrong_case_identity(self):
        cases = [
            b"not a zip", b"x" * (MAX_WORKBOOK_BYTES + 1),
            workbook([[HOME, "note", "2026-10-20"]], dtd=True),
            workbook([[HOME, "note", "2026-10-20"]], headers=["home", "coordination_note", "task_due_date"]),
            workbook([[HOME, "note", "2026-10-20"]], headers=["case_id", "case_id", "task_due_date"]),
            workbook([[HOME, "note", "2026-10-20"]] * 501),
            workbook([[HOME, "note", "2026-10-20"]], extra={f"extra{i}": "x" for i in range(18)}),
            workbook([[HOME, "note", "2026-10-20"]], extra={"large": b"x" * (20 * 1024 * 1024)}),
            workbook([[HOME, "note", "2026-10-20"]], extra={"evil.xml": "<!ENTITY x 'bad'><root/>"}),
        ]
        for raw in cases:
            with self.subTest(size=len(raw)), self.assertRaises(ValueError):
                read_case_updates(raw)
        preview = self.import_preview(workbook([["EX-BUILDING-001", "note", "2026-10-20"]]))
        self.assertEqual(preview["rows"][0]["status"], "error")
        self.assertIsNone(preview["token"])
        with self.assertRaises(ValueError):
            self.import_preview(workbook([[HOME, "note", "2026-10-20"]]), fields=[])
        with self.assertRaises(ValueError):
            self.import_preview(workbook([[HOME, "note", "2026-10-20"]]), fields=["owner_email"])

    def test_cohort_and_full_role_projected_history_exports(self):
        with self.store.lock:
            c = self.store._case(HOME)
            c["contacts"] = [dict(at=f"2026-10-{i % 10 + 1:02d}", note=f"history-{i}",
                                  by=self.pm["name"], purpose="Update", outcome="Recorded", channel="Phone")
                             for i in range(45)]
            c["exercise"]["source_history"] = [dict(id="old-source", version="1", raw_text="old allowed source")]
            c["exercise"]["evidence"][0]["raw_text"] = "FINANCE-RAW-MARKER"
            c["finance"] = {"confidential": "FINANCE-MARKER"}
            self.store._case(SIBLING)["contractor"]["name"] = "Another contractor"
            self.store.save()
        self.commit(self.preview([HOME]))
        data = self.store.exercise_data_export(self.pm)
        self.assertEqual(data["metadata"]["count"], 18)
        self.assertEqual(data["metadata"]["as_of"], "2026-10-10")
        story = next(row for row in data["cases"] if row["case"]["id"] == HOME)
        self.assertEqual(len(story["events"]["contacts"]), 45)
        self.assertEqual(story["reviews"]["source_history"][0]["version"], "1")
        self.assertEqual(len(story["events"]["data_changes"]), 1)
        self.assertNotIn("data_previews", story["case"]["exercise"])
        self.assertTrue(story["sources"])
        self.assertEqual(self.store.exercise_data_export(self.pm, "forecast")["metadata"]["count"], 16)
        contractor = self.store.exercise_data_export(self.contractor)
        self.assertEqual(contractor["metadata"]["count"], 17)
        self.assertNotIn(SIBLING, [row["case"]["id"] for row in contractor["cases"]])
        encoded = json.dumps(contractor)
        for secret in ("FINANCE-MARKER", "FINANCE-RAW-MARKER", "old allowed source", "data_history",
                       "history-44", "coordination_note", "source_candidates", "Fictional Resident"):
            self.assertNotIn(secret, encoded)
        for row in contractor["cases"]:
            self.assertEqual(row["sources"], [])
            self.assertEqual(row["decisions"], [])
            self.assertEqual(row["evidence_references"], [])
        self.assertTrue(self.store.verify_ledger()["intact"])
        forged = dict(self.contractor, contractor="Another contractor")
        self.assertEqual(self.store.exercise_data_export(forged)["metadata"]["count"], 17)
        with self.assertRaises(ValueError):
            self.store.exercise_data_export(self.pm, "silent-default")

    def test_http_xlsx_commit_and_contractor_get_post_boundary(self):
        app = App(self.store, "data-test-password")
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_port}"

        def request(path, payload=None, cookie=None):
            headers = {"Content-Type": "application/json"}
            if cookie:
                headers["Cookie"] = cookie
            req = urllib.request.Request(url + path, headers=headers,
                                         data=json.dumps(payload).encode() if payload is not None else None)
            return urllib.request.urlopen(req, timeout=5)

        def login(user):
            with request("/api/login", {"email": user["email"], "password": "data-test-password"}) as response:
                return response.headers["Set-Cookie"].split(";")[0]

        try:
            with request("/healthz") as response:
                self.assertEqual(response.status, 200)
            self.assertEqual(get_kind("/api/exercise/data"), "exercise")
            cookie = login(self.pm)
            raw = workbook([[HOME, "HTTP explicit note", "2026-10-23"]])
            with request("/api/exercise/data", dict(action="import-preview", reason="Manual HTTP review",
                         filename="updates.xlsx", workbook_base64=base64.b64encode(raw).decode(),
                         fields=["coordination_note", "task_due_date"]), cookie) as response:
                preview = json.load(response)
            with request("/api/exercise/data", dict(action="commit", token=preview["token"],
                         input_hash=preview["input_hash"],
                         expected_fingerprints={str(row["row"]): row["expected_fingerprint"] for row in preview["rows"]}),
                         cookie) as response:
                self.assertEqual(json.load(response)["committed"], 1)
            with request("/api/exercise/data?population=story", cookie=cookie) as response:
                self.assertEqual(json.load(response)["metadata"]["count"], 2)
                self.assertIn("exercise-data.json", response.headers["Content-Disposition"])
            contractor_cookie = login(self.contractor)
            with request("/api/exercise/data", cookie=contractor_cookie) as response:
                self.assertNotIn("HTTP explicit note", json.dumps(json.load(response)))
            with self.assertRaises(urllib.error.HTTPError) as caught:
                request("/api/exercise/data", {"action": "bulk-preview"}, contractor_cookie)
            self.assertEqual(caught.exception.code, 403)
            with self.assertRaises(urllib.error.HTTPError) as caught:
                request("/api/exercise/data", dict(action="import-preview", reason="manual",
                        filename="bad.xlsx", workbook_base64="!bad!", fields=["coordination_note"]), cookie)
            self.assertEqual(caught.exception.code, 400)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
