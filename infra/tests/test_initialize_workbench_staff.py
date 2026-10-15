import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("staff_initializer", ROOT / "infra/scripts/initialize-workbench-staff.py")
INIT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(INIT)
from zava_forward.core import ledger

ONE = "11111111-1111-4111-8111-111111111111"
TWO = "22222222-2222-4222-8222-222222222222"
ROLE = {"id": "role-1", "value": "Demo.Coordinator", "isEnabled": True, "allowedMemberTypes": ["User"]}
MAP = {"Demo.Coordinator": "Retrofit Coordinator", "Demo.Manager": "Retrofit Programme Manager"}
ROSTER = [{"code": "RC-01", "oid": ONE, "name": "Tenant Coordinator",
           "email": "coordinator@example.invalid", "role": "Retrofit Coordinator"}]


class FakeDirectory:
    def __init__(self, assignments=(), groups=()):
        self.assignments = list(assignments)
        self.groups = [{"id": g} for g in groups]
        self.writes = []
        self.reads = []

    def pages(self, path):
        self.reads.append(path)
        return self.groups if "/memberOf/" in path else self.assignments

    def request(self, path, *, body=None):
        self.writes.append(body)
        self.assignments.append(dict(body))
        return body


def grant(principal=ONE, role="role-1"):
    return {"principalId": principal, "appRoleId": role, "resourceId": "app"}


class StaffInitializationTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:", isolation_level=None)
        self.addCleanup(self.db.close)
        self.db.executescript("""
            CREATE TABLE staff (email TEXT PRIMARY KEY,body TEXT);
            CREATE TABLE cases (id TEXT PRIMARY KEY,rowversion INT,seq INT,body TEXT);
            CREATE TABLE meta (key TEXT PRIMARY KEY,value TEXT);
            CREATE TABLE audit (at TEXT,who TEXT,action TEXT,case_id TEXT,detail TEXT,prev TEXT,hash TEXT);
            CREATE TABLE audit_head (id INT PRIMARY KEY,count INT,hash TEXT);
            INSERT INTO meta VALUES ('seq','1');
        """)
        self.db.execute("INSERT INTO audit_head VALUES (1,0,?)", (ledger.GENESIS,))
        self.old = dict(ROSTER[0], name="Generated Coordinator", email="generated@example.invalid")
        self.old.pop("oid")
        self.case = {"id": "case-1", "owner_code": "RC-01", "owner": "Generated Coordinator",
                     "contractor": {"name": "Example Supplier"},
                     "approval": {"by": "Historic Actor"}, "resident": {"name": "Fixture Resident"}}
        self.db.execute("INSERT INTO staff VALUES (?,?)", (self.old["email"], json.dumps(self.old)))
        self.db.execute("INSERT INTO cases VALUES ('case-1',1,1,?)", (json.dumps(self.case),))

    def snapshot(self):
        return {t: self.db.execute(f"SELECT * FROM {t}").fetchall()
                for t in ("staff", "cases", "meta", "audit", "audit_head")}

    def test_private_roster_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "roster.json"
            path.write_text(json.dumps([{"code": "RC-01", "userId": ONE}]))
            path.chmod(0o600)
            self.assertEqual(INIT.read_roster(path)[0]["userId"], ONE)
            for data in ([], [{"code": "RC-01", "userId": "invalid"}],
                         [{"code": "RC-01", "userId": ONE}, {"code": "RC-02", "userId": ONE}]):
                with self.subTest(data=data):
                    path.write_text(json.dumps(data))
                    with self.assertRaises(ValueError):
                        INIT.read_roster(path)
            path.chmod(0o644)
            with self.assertRaises(ValueError):
                INIT.read_roster(path)

    def test_resource_and_disabled_accounts_refused(self):
        user = {"id": ONE, "displayName": "Example Member", "userPrincipalName": "person@example.invalid",
                "accountEnabled": True, "userType": "Member"}
        self.assertEqual(INIT.person(user)["oid"], ONE)
        for changes in ({"accountEnabled": False}, {"userType": "Guest"},
                        {"displayName": "Example ConfRm"}, {"userPrincipalName": "wksp-office@example.invalid"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                INIT.person(dict(user, **changes))
        self.db.execute("ALTER TABLE cases ADD COLUMN contractor TEXT")
        self.db.execute("UPDATE cases SET contractor='Example Supplier'")
        directory = INIT.Directory(Path("/private"))
        wanted = [{"code": "RC-01", "userId": ONE}]
        with patch.object(directory, "request", return_value=user):
            prepared = INIT.prepare_roster(self.db, wanted, directory)
            self.assertEqual(prepared[0]["code"], "RC-01")
            self.assertEqual(prepared[0]["role"], self.old["role"])
            with self.assertRaises(ValueError):
                INIT.prepare_roster(self.db, [], directory)
            with self.assertRaises(ValueError):
                INIT.prepare_roster(self.db, wanted + [{"code": "CT-01", "userId": TWO,
                                                       "role": "Contractor", "contractor": "Unknown Supplier"}], directory)
            self.db.execute("UPDATE staff SET body=?", (json.dumps(dict(self.old, oid=TWO)),))
            with self.assertRaises(ValueError):
                INIT.prepare_roster(self.db, wanted, directory)

    def test_runtime_overlay_and_distinct_mapped_roles(self):
        roles = [ROLE, dict(ROLE, id="alias", value="Demo.Alias")]
        mapping = dict(MAP, **{"Demo.Coordinator": "Retrofit Programme Manager",
                              "Demo.Alias": "Retrofit Programme Manager"})
        assignments = [grant(), grant("group", "alias"), grant(role="00000000-0000-0000-0000-000000000000"),
                       dict(grant(role="alias"), resourceId="another-app")]
        self.assertEqual(INIT.effective_roles(assignments, ONE, {"group"}, "app", roles, mapping),
                         {"Retrofit Programme Manager"})

    def test_matching_group_role_no_new_grant_default_access_preserved(self):
        directory = FakeDirectory([grant("group"), grant(role="00000000-0000-0000-0000-000000000000")], ["group"])
        self.assertEqual(INIT.reconcile_roles(directory, "app", [ROLE], MAP, ROSTER, apply=True), 0)
        self.assertEqual(directory.writes, [])
        self.assertEqual(len(directory.assignments), 2)
        self.assertTrue(any("/memberOf/" in path for path in directory.reads))
        self.assertFalse(any("transitiveMemberOf" in path for path in directory.reads))
        nested_only = FakeDirectory([grant("parent-group")], ["direct-group"])
        self.assertEqual(INIT.reconcile_roles(nested_only, "app", [ROLE], MAP, ROSTER, apply=True), 1)
        self.assertEqual(len(nested_only.writes), 1)

    def test_conflicting_group_role_refused_before_writes(self):
        roles = [ROLE, dict(ROLE, id="manager", value="Demo.Manager")]
        directory = FakeDirectory([grant(), grant("group", "manager")], ["group"])
        with self.assertRaises(ValueError):
            INIT.reconcile_roles(directory, "app", roles, MAP, ROSTER, apply=True)
        self.assertEqual(directory.writes, [])

    def test_role_addition_check_and_repeat_idempotency(self):
        directory = FakeDirectory()
        self.assertEqual(INIT.reconcile_roles(directory, "app", [ROLE], MAP, ROSTER, apply=False), 1)
        self.assertEqual(directory.writes, [])
        self.assertEqual(INIT.reconcile_roles(directory, "app", [ROLE], MAP, ROSTER, apply=True), 1)
        self.assertEqual(INIT.reconcile_roles(directory, "app", [ROLE], MAP, ROSTER, apply=True), 0)
        self.assertEqual(len(directory.writes), 1)

    def test_collection_completeness_and_fixed_host(self):
        directory = INIT.Directory(Path("/private"))
        with patch.object(directory, "request", side_effect=[{"value": [grant()], "@odata.nextLink": "next"}, {"value": []}]):
            self.assertEqual(directory.pages("first"), [grant()])
        with patch.object(directory, "request", return_value={}), self.assertRaises(ValueError):
            directory.pages("first")
        with self.assertRaises(ValueError):
            directory.request("https://untrusted.example/v1.0/users")
        with patch.object(directory, "request", side_effect=RuntimeError("unreadable")):
            with self.assertRaises(RuntimeError):
                INIT.reconcile_roles(directory, "app", [ROLE], MAP, ROSTER, apply=True)

    def test_sql_identity_labels_history_and_versions(self):
        before = self.snapshot()
        INIT.install_roster(self.db, ROSTER, apply=True)
        after = self.snapshot()
        case = json.loads(after["cases"][0][3])
        self.assertEqual(case, dict(self.case, owner="Tenant Coordinator"))
        self.assertEqual(after["cases"][0][1:3], (2, 2))
        self.assertEqual(after["meta"], [("seq", "2")])
        self.assertEqual(before["audit"], after["audit"][:-1])
        entry = after["audit"][0]
        self.assertEqual(entry[6], ledger.make_entry(entry[1], entry[2], entry[3], entry[4], entry[5], entry[0])["hash"])
        self.assertNotIn(ONE, entry[4])
        self.assertNotIn("coordinator@example.invalid", entry[4])

    def test_sql_check_and_matching_noop_are_readonly(self):
        before = self.snapshot()
        self.assertEqual(INIT.install_roster(self.db, ROSTER, apply=False)["staff_changes"], 1)
        self.assertEqual(before, self.snapshot())
        INIT.install_roster(self.db, ROSTER, apply=True)
        after = self.snapshot()
        self.assertEqual(INIT.install_roster(self.db, ROSTER, apply=True), {"staff_changes": 0, "owner_labels": 0})
        self.assertEqual(after, self.snapshot())

    def test_protected_identity_coverage_and_atomic_failure(self):
        bound = dict(self.old, oid=TWO)
        self.db.execute("UPDATE staff SET body=?", (json.dumps(bound),))
        before = self.snapshot()
        with self.assertRaises(ValueError):
            INIT.install_roster(self.db, ROSTER, apply=True)
        self.assertEqual(before, self.snapshot())
        self.db.execute("UPDATE staff SET body=?", (json.dumps(self.old),))
        self.db.executescript("CREATE TRIGGER refuse_audit BEFORE INSERT ON audit BEGIN SELECT RAISE(ABORT,'injected'); END;")
        before = self.snapshot()
        with self.assertRaises(sqlite3.IntegrityError):
            INIT.install_roster(self.db, ROSTER, apply=True)
        self.assertEqual(before, self.snapshot())
        with self.assertRaises(ValueError):
            INIT.install_roster(self.db, [], apply=True)

    def test_email_key_swap_and_unrelated_profile_preserved(self):
        other = dict(self.old, code="RC-02", email="second@example.invalid")
        self.db.execute("INSERT INTO staff VALUES (?,?)", (other["email"], json.dumps(other)))
        swapped = [dict(ROSTER[0], email=other["email"]),
                   dict(other, email=self.old["email"], name="Other Tenant Member", oid=TWO)]
        INIT.install_roster(self.db, swapped, apply=True)
        self.assertEqual({r[0] for r in self.db.execute("SELECT email FROM staff")}, {other["email"], self.old["email"]})

    def test_restart_failure_then_noop_retry_replaces_serving_replicas(self):
        INIT.install_roster(self.db, ROSTER, apply=True)
        after = self.snapshot()
        revision = [{"name": "revision-1"}]
        traffic = [{"revisionName": "revision-1", "weight": 100}]
        old = [{"name": "old-replica"}]
        fresh = [{"name": "new-replica", "properties": {"containers": [{"ready": True}]}}]
        with patch.object(INIT, "azure", side_effect=[revision, traffic, "revision-1", old, RuntimeError("restart failed")]):
            with self.assertRaises(RuntimeError):
                INIT.restart_api("group", "app")
        self.assertEqual(INIT.install_roster(self.db, ROSTER, apply=True)["staff_changes"], 0)
        with patch.object(INIT, "azure", side_effect=[revision, traffic, "revision-1", old, None, fresh]) as azure:
            INIT.restart_api("group", "app")
            self.assertTrue(any("restart" in call.args[0] for call in azure.call_args_list))
        self.assertEqual(after, self.snapshot())


if __name__ == "__main__":
    unittest.main()
