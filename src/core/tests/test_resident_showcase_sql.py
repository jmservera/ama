"""The showcase SQL boundary against a real SQL Server.

SQL tests are skipped unless ZF_TEST_MSSQL=1 and ZF_SQL_SERVER is loopback (a throwaway container
that may be wiped, never the pilot database). The password comes from ZF_SQL_PASSWORD in the
process environment of the run and is never stored. The renderer tests always run.
"""

import importlib.util
import json
import os
import unittest
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from zava_forward.core import resident_showcase as rs
from zava_forward.core import resident_showcase_sql as rsql

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "resident_showcase_sql_script", ROOT / "infra" / "scripts" / "resident_showcase_sql.py"
)
script = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
spec.loader.exec_module(script)  # type: ignore[union-attr]

ON = os.environ.get("ZF_TEST_MSSQL") == "1" and os.environ.get("ZF_SQL_SERVER") in (
    "127.0.0.1",
    "localhost",
)
USER = "zf_showcase_user"

if ON:
    import mssql_python


class FakeCursor:
    def __init__(
        self,
        principal: tuple[Any, ...] | None = None,
        members: int = 0,
        permissions: tuple[tuple[Any, ...], ...] = (),
        public: int = 0,
    ) -> None:
        self.public = public
        self.principal, self.members, self.permissions = principal, members, permissions
        self.rows: list[Any] = []
        self.sql: list[str] = []

    def execute(self, sql: str) -> None:
        self.sql.append(sql)
        if "sys.database_principals" in sql:
            self.rows = [self.principal] if self.principal else []
        elif "grantee_principal_id = 0" in sql:
            self.rows = [(self.public,)]
        elif "database_role_members" in sql:
            self.rows = [(self.members,)]
        else:
            self.rows = list(self.permissions)

    def fetchall(self) -> list[Any]:
        return self.rows


CLIENT = "11111111-2222-3333-4444-555555555555"
GOOD_USER = ("E", "EXTERNAL", uuid.UUID(CLIENT).bytes_le)
OK_PERMS = (
    ("G", "CONNECT", 0, None),
    ("G", "SELECT", 1, "resident_showcase.v_resident_case"),
    ("D", "SELECT", 1, "dbo.cases"),
)


class PrincipalVerificationTests(unittest.TestCase):
    def verify(self, **kw: Any) -> None:
        script.verify_principal(FakeCursor(**kw), "id-resident", CLIENT)

    def test_exact_identity_and_view_only_rights_pass(self) -> None:
        self.verify(principal=GOOD_USER, permissions=OK_PERMS)

    def test_name_only_reuse_is_refused(self) -> None:
        bad = (
            dict(principal=None),
            dict(principal=("E", "EXTERNAL", uuid.uuid4().bytes_le)),
            dict(principal=("S", "NONE", uuid.UUID(CLIENT).bytes_le)),
            dict(principal=("E", "EXTERNAL", None)),
            dict(principal=GOOD_USER, members=1),
            dict(principal=GOOD_USER, permissions=OK_PERMS, public=1),
            dict(principal=GOOD_USER, permissions=(("G", "SELECT", 1, "dbo.chat"),)),
            dict(principal=GOOD_USER, permissions=(("G", "SELECT", 0, None),)),
            dict(
                principal=GOOD_USER,
                permissions=(("W", "SELECT", 1, "resident_showcase.v_resident_case"),),
            ),
            dict(
                principal=GOOD_USER,
                permissions=(("G", "INSERT", 1, "resident_showcase.v_resident_case"),),
            ),
        )
        for case in bad:
            with self.assertRaises(script.PrincipalError, msg=str(case)):
                self.verify(**case)

    def test_apply_without_a_client_id_is_refused_before_connecting(self) -> None:
        self.assertEqual(script.main(["id-resident", "--apply", "srv", "db"]), 2)


class RenderTests(unittest.TestCase):
    def test_principal_substituted_and_validated(self) -> None:
        batches = script.render("id-cutover-test-resident-demo")
        text = "\n".join(batches)
        self.assertIn("[id-cutover-test-resident-demo]", text)
        self.assertNotIn("{{", text)
        for bad in ("", "a", "x]; DROP", "has space", "a" * 61, "semi;colon"):
            with self.assertRaises(ValueError):
                script.render(bad)

    def test_sql_text_has_no_role_membership_or_writes_for_principal(self) -> None:
        text = "\n".join(script.render(USER)).upper()
        for forbidden in (
            "ADD MEMBER",
            "DB_DATAREADER",
            "DB_DATAWRITER",
            "DB_DDLADMIN",
            "GRANT INSERT",
        ):
            self.assertNotIn(forbidden, text)
        self.assertEqual(text.count("GRANT "), 1)
        self.assertIn("GRANT SELECT ON OBJECT::RESIDENT_SHOWCASE.V_RESIDENT_CASE", text)

    def test_principal_statement_uses_client_id_sid(self) -> None:
        cid = str(uuid.UUID(int=1))
        statement = script.principal_statement(USER, cid)
        self.assertIn("TYPE = E", statement)
        self.assertIn("0x" + uuid.UUID(cid).bytes_le.hex(), statement)

    def test_reader_selects_only_the_view(self) -> None:
        for sql in (rsql.LIST_SQL, rsql.ONE_SQL):
            self.assertIn("[resident_showcase].[v_resident_case]", sql)
            self.assertNotIn("dbo.", sql)
            self.assertTrue(sql.startswith("SELECT "))

    def test_connection_string_modes(self) -> None:
        msi = rsql.connection_string(
            {"server": "s", "database": "d", "auth": "msi", "client_id": "c"}
        )
        self.assertIn("ActiveDirectoryMSI", msi)
        self.assertIn("UID=c", msi)
        with self.assertRaises(rs.ShowcaseConfigError):
            rsql.connection_string({"server": "s", "database": "d", "auth": "token"})


def _body(email: str, **extra: Any) -> str:
    body = {
        "resident": {"email": email},
        "home": {"address": "1 Test Road", "town": "Testville", "postcode": "TE1 1ST"},
        "measures": ["Loft insulation", "Cavity wall"],
    }
    body.update(extra)
    return json.dumps(body)


@unittest.skipUnless(ON, "opt-in loopback SQL Server")
class SqlBoundaryTests(unittest.TestCase):
    db: str
    base: dict[str, str]
    connect: Callable[[], Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.db = "show462_" + uuid.uuid4().hex[:8]
        base = {
            "server": os.environ["ZF_SQL_SERVER"],
            "port": os.environ.get("ZF_SQL_PORT", "1433"),
            "auth": "password",
            "user": os.environ.get("ZF_SQL_USER", "sa"),
            "password": os.environ["ZF_SQL_PASSWORD"],
            "trust_cert": "1",
        }
        cls.base = {**base, "database": cls.db}
        admin = rsql.connector({**base, "database": "master"})()
        admin.cursor().execute(f"CREATE DATABASE [{cls.db}] COLLATE Latin1_General_100_BIN2")
        admin.close()
        cls.connect = staticmethod(rsql.connector(cls.base))
        from zava_forward.core.mssqlstore import TABLES

        try:
            cls.q(TABLES["cases"])
            cls.q(f"CREATE USER [{USER}] WITHOUT LOGIN")
            for batch in script.render(USER):
                cls.q(batch)
        except BaseException:
            cls.tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls) -> None:
        conn = rsql.connector({**cls.base, "database": "master"})()
        cur = conn.cursor()
        cur.execute(f"ALTER DATABASE [{cls.db}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
        cur.execute(f"DROP DATABASE [{cls.db}]")
        conn.close()

    @classmethod
    def q(cls, sql: str, *params: Any) -> list[Any]:
        conn = cls.connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, params) if params else cur.execute(sql)
            return cur.fetchall() if cur.description else []
        finally:
            conn.close()

    def setUp(self) -> None:
        self.q("DELETE FROM resident_showcase.allowed_case")
        self.q("DELETE FROM cases")
        self.reader = rsql.ShowcaseReader(self.connect)

    def add_case(self, case_id: str, body: str, allow: bool = True, **kw: Any) -> None:
        self.q(
            "INSERT INTO cases (id, seq, stage, area, wave, owner_code, closed, hazard, postcode,"
            " address, body) VALUES (?, 1, ?, 'A', 'W', 'O', ?, 0, 'P', 'A', ?)",
            case_id,
            kw.get("stage", "Survey"),
            kw.get("closed", 0),
            body,
        )
        if allow:
            self.allow(case_id)

    def allow(
        self,
        case_id: str,
        provenance: str = "owner-approved local fixture",
        revoked: int = 0,
        start: str = "2026-10-01T00:00:00",
        end: str = "2026-11-01T00:00:00",
    ) -> None:
        self.q(
            "INSERT INTO resident_showcase.allowed_case (case_id, provenance, valid_from, valid_to,"
            " revoked) VALUES (?, ?, ?, ?, ?)",
            case_id,
            provenance,
            start,
            end,
            revoked,
        )

    def as_user(self, sql: str) -> list[Any]:
        conn = self.connect()
        try:
            cur = conn.cursor()
            cur.execute(f"EXECUTE AS USER = '{USER}'")
            cur.execute(sql)
            return cur.fetchall() if cur.description else []
        finally:
            conn.close()

    def test_empty_allowlist_shows_nothing(self) -> None:
        self.add_case("C-1", _body("a@example.com"), allow=False)
        self.assertEqual(self.reader.list_rows(), [])
        self.assertIsNone(self.reader.fetch_case("C-1"))

    def test_allowlisted_clean_row_is_shaped(self) -> None:
        self.add_case("C-1", _body("a@example.com"))
        [row] = self.reader.list_rows()
        self.assertEqual((row.case_id, row.email, row.email_count), ("C-1", "a@example.com", 1))
        self.assertEqual(row.measures, ("Loft insulation", "Cavity wall"))
        self.assertEqual(row.town, "Testville")
        self.assertIsNotNone(row.valid_to.tzinfo)
        self.assertIsNone(rs.exclusion(row, datetime(2026, 10, 25, tzinfo=UTC)))
        self.assertEqual(self.reader.fetch_case("C-1"), row)

    def test_string_measures_and_text_columns_are_bounded(self) -> None:
        body = json.loads(_body("a@example.com"))
        body["measures"] = "Loft insulation; Cavity wall"
        self.add_case("C-1", json.dumps(body))
        self.assertEqual(self.reader.list_rows()[0].measures, ("Loft insulation", "Cavity wall"))

    def test_duplicate_counts_include_non_allowlisted_cases_and_variants(self) -> None:
        self.add_case("C-1", _body("a@example.com"))
        self.add_case("C-2", _body(" A@EXAMPLE.COM "), allow=False)
        [row] = self.reader.list_rows()
        self.assertEqual(row.email_count, 2)
        self.assertEqual(rs.exclusion(row, datetime(2026, 10, 25, tzinfo=UTC)), "email_duplicate")

    def test_unicode_lookalike_does_not_collide_and_is_excluded(self) -> None:
        self.add_case("C-1", _body("a@example.com"))
        self.add_case("C-2", _body("ａ@example.com"))
        rows = {r.case_id: r for r in self.reader.list_rows()}
        self.assertEqual(rows["C-1"].email_count, 1)
        self.assertEqual(
            rs.exclusion(rows["C-2"], datetime(2026, 10, 25, tzinfo=UTC)), "email_form"
        )

    def test_malformed_missing_and_non_string_email_rows_are_not_shown(self) -> None:
        self.add_case("C-1", "not json at all")
        self.add_case("C-2", json.dumps({"resident": {}}))
        self.add_case("C-3", json.dumps({"resident": {"email": ["a@example.com"]}}))
        self.add_case("C-4", json.dumps({"resident": {"email": {"x": 1}}}))
        self.add_case("C-5", _body("ok@example.com"))
        self.assertEqual([r.case_id for r in self.reader.list_rows()], ["C-5"])

    def test_other_domain_row_is_shown_to_app_which_excludes_it(self) -> None:
        self.add_case("C-1", _body("a@example.org"))
        [row] = self.reader.list_rows()
        self.assertEqual(rs.exclusion(row, datetime(2026, 10, 25, tzinfo=UTC)), "email_form")

    def test_revoked_and_expired_rows_are_excluded_by_domain(self) -> None:
        self.add_case("C-1", _body("a@example.com"), allow=False)
        self.add_case("C-2", _body("b@example.com"), allow=False)
        self.allow("C-1", revoked=1)
        self.allow("C-2", end="2026-10-25T00:00:01")
        now = datetime(2026, 10, 25, 12, tzinfo=UTC)
        reasons = {r.case_id: rs.exclusion(r, now) for r in self.reader.list_rows()}
        self.assertEqual(reasons, {"C-1": "revoked", "C-2": "window"})

    def test_more_than_25_fails_closed(self) -> None:
        for i in range(26):
            self.add_case(f"C-{i:02d}", _body(f"u{i}@example.com"))
        with self.assertRaises(rs.ShowcaseConfigError):
            self.reader.list_rows()

    def test_table_checks_reject_blank_provenance_and_late_window(self) -> None:
        self.add_case("C-1", _body("a@example.com"), allow=False)
        with self.assertRaises(mssql_python.Error):
            self.allow("C-1", provenance="   ")
        with self.assertRaises(mssql_python.Error):
            self.allow("C-1", end="2026-11-01T00:00:01")

    def test_principal_reads_only_the_view(self) -> None:
        self.add_case("C-1", _body("a@example.com"))
        self.assertEqual(len(self.as_user(rsql.LIST_SQL)), 1)
        denied = (
            "SELECT TOP 1 id FROM dbo.cases",
            "SELECT TOP 1 case_id FROM resident_showcase.allowed_case",
            "INSERT INTO dbo.cases (id, seq, stage, area, wave, owner_code, closed, hazard,"
            " postcode, address, body) VALUES ('X', 1, 's', 'a', 'w', 'o', 0, 0, 'p', 'a', '{}')",
            "UPDATE dbo.cases SET stage = 'x'",
            "DELETE FROM dbo.cases",
            "INSERT INTO resident_showcase.allowed_case VALUES"
            " ('C-9', 'p', '2026-10-01', '2026-10-02', 0)",
            "UPDATE resident_showcase.allowed_case SET revoked = 0",
            "CREATE TABLE dbo.zf_should_fail (x INT)",
            "CREATE VIEW dbo.zf_should_fail AS SELECT 1 AS x",
            "ALTER TABLE dbo.cases ADD zf_x INT",
            "DROP VIEW resident_showcase.v_resident_case",
        )
        for sql in denied:
            with self.assertRaises(mssql_python.Error, msg=sql):
                self.as_user(sql)

    def test_principal_has_no_roles_and_single_effective_permission(self) -> None:
        roles = self.q(
            "SELECT COUNT(*) FROM sys.database_role_members m JOIN sys.database_principals u"
            " ON u.principal_id = m.member_principal_id WHERE u.name = ?",
            USER,
        )
        self.assertEqual(roles[0][0], 0)
        view = self.as_user(
            "SELECT permission_name FROM sys.fn_my_permissions("
            "'resident_showcase.v_resident_case', 'OBJECT')"
        )
        self.assertEqual({r[0] for r in view}, {"SELECT"})
        for target in ("dbo.cases", "resident_showcase.allowed_case"):
            perms = self.as_user(
                f"SELECT permission_name FROM sys.fn_my_permissions('{target}', 'OBJECT')"
            )
            self.assertEqual(perms, [], target)
        database = {
            r[0]
            for r in self.as_user(
                "SELECT permission_name FROM sys.fn_my_permissions(NULL, 'DATABASE')"
            )
        }
        public_defaults = {
            "CONNECT",
            "VIEW ANY COLUMN ENCRYPTION KEY DEFINITION",
            "VIEW ANY COLUMN MASTER KEY DEFINITION",
        }
        self.assertLessEqual(database, public_defaults)

    def test_apply_is_idempotent_and_keeps_data(self) -> None:
        self.add_case("C-1", _body("a@example.com"))
        for batch in script.render(USER):
            self.q(batch)
        self.assertEqual(len(self.reader.list_rows()), 1)


if __name__ == "__main__":
    unittest.main()
