import contextlib
import copy
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import dataset
from zava_forward.core import factory, seed_merge
from zava_forward.core.sqlstore import SeedMergeError, SqlStore


def clone(case: dict[str, Any], n: int) -> dict[str, Any]:
    c = copy.deepcopy(case)
    c["id"] = f"ZF-SEED-{n}"
    return c


class SeedMergeBase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name) / "base.json"
        base.write_text(json.dumps(dataset.DATA))
        self.db = os.path.join(self.tmp.name, "live.sqlite")
        self.store = SqlStore(str(base), self.db)
        self.addCleanup(self.store.db.close)
        self.store.audit("seed", "proof", "ZF-1", "existing")
        self.store.save()
        self.seed = Path(self.tmp.name) / "seed.json"
        self.write_seed()

    def write_seed(self, **extra: Any) -> None:
        data: dict[str, Any] = copy.deepcopy(dataset.DATA)
        data["cases"] = list(data["cases"]) + [clone(data["cases"][0], n) for n in range(1, 4)]
        data["procurement"] = {"packages": [{"id": "PKG-SYNTHETIC"}], "work_orders": []}
        data.update(extra)
        self.seed.write_text(json.dumps(data))

    def full_rows(self) -> list[Any]:
        return self.store.db.execute(
            "SELECT * FROM cases WHERE id NOT LIKE 'ZF-SEED-%' ORDER BY id"
        ).fetchall()

    def state(self) -> dict[str, Any]:
        db = self.store.db
        return dict(
            cases=db.execute("SELECT id, body, seq, rowversion FROM cases ORDER BY id").fetchall(),
            audit=db.execute(
                "SELECT at, who, action, case_id, detail, prev, hash FROM audit ORDER BY seq"
            ).fetchall(),
            head=tuple(db.execute("SELECT count, hash FROM audit_head").fetchone()),
            meta=dict(db.execute("SELECT key, value FROM meta").fetchall()),
            staff=db.execute("SELECT email, body FROM staff ORDER BY email").fetchall(),
            recs=db.execute("SELECT id, body FROM recommendations ORDER BY id").fetchall(),
        )


class SeedMergeTests(SeedMergeBase):
    def test_dry_run_default_writes_nothing(self) -> None:
        before = self.state()
        report = self.store.merge_seed(self.seed)
        self.assertEqual((report["to_insert"], report["applied"]), (3, False))
        self.assertEqual(self.state(), before)

    def test_apply_inserts_only_and_preserves_existing(self) -> None:
        before = self.state()
        self.existing_full = self.full_rows()
        report = self.store.merge_seed(self.seed, apply=True, expect_added=3)
        after = self.state()
        self.assertTrue(report["applied"])
        self.assertEqual(len(after["cases"]), len(before["cases"]) + 3)
        for row in before["cases"]:
            self.assertIn(row, after["cases"])
        self.assertEqual(self.full_rows(), self.existing_full)
        self.assertEqual(after["audit"][: len(before["audit"])], before["audit"])
        self.assertEqual(len(after["audit"]), len(before["audit"]) + 1)
        self.assertEqual(after["audit"][-1][2], "seed_merge")
        self.assertEqual(after["recs"], before["recs"])
        self.assertEqual(after["staff"], before["staff"])
        self.assertEqual(after["meta"]["as_of"], before["meta"]["as_of"])
        self.assertEqual(int(after["meta"]["seq"]), int(before["meta"]["seq"]) + 1)
        self.assertIn("procurement", after["meta"])
        self.assertTrue(self.store.verify_audit())
        self.assertEqual(self.store.ledger_head()[0], len(after["audit"]))

    def test_other_replica_sees_new_cases(self) -> None:
        replica = SqlStore(str(self.seed), self.db)
        self.addCleanup(replica.db.close)
        replica._sync()
        self.store.merge_seed(self.seed, apply=True)
        replica._sync()
        self.assertIn("ZF-SEED-1", replica.cases)

    def test_second_apply_is_a_noop_without_audit(self) -> None:
        self.store.merge_seed(self.seed, apply=True)
        once = self.state()
        report = self.store.merge_seed(self.seed, apply=True, expect_added=0)
        self.assertEqual(
            (report["to_insert"], report["identical"] > 0, report["applied"]), (0, True, False)
        )
        self.assertEqual(self.state(), once)

    def test_identical_case_compares_semantically(self) -> None:
        data = json.loads(self.seed.read_text())
        data["cases"][0] = json.loads(json.dumps(data["cases"][0], sort_keys=True))
        self.seed.write_text(json.dumps(data, indent=2))
        self.assertEqual(self.store.merge_seed(self.seed)["conflicts"], 0)

    def test_seed_case_without_default_fields_matches_stored_case(self) -> None:
        data = json.loads(self.seed.read_text())
        for key in ("documents", "funding"):
            data["cases"][0].pop(key, None)
        self.seed.write_text(json.dumps(data))
        report = self.store.merge_seed(self.seed)
        self.assertEqual(
            (report["conflicts"], report["identical"]), (0, len(dataset.DATA["cases"]))
        )

    def test_collision_aborts_everything(self) -> None:
        data = json.loads(self.seed.read_text())
        data["cases"][0]["resident"]["name"] = "Changed Synthetic"
        self.seed.write_text(json.dumps(data))
        before = self.state()
        with self.assertRaises(SeedMergeError) as caught:
            self.store.merge_seed(self.seed, apply=True)
        self.assertEqual(caught.exception.report["conflicts"], 1)
        self.assertEqual(self.state(), before)

    def test_differing_document_aborts_but_continuity_is_preserved(self) -> None:
        self.store.merge_seed(self.seed, apply=True)
        data = json.loads(self.seed.read_text())
        data["procurement"] = {"packages": [], "work_orders": []}
        self.seed.write_text(json.dumps(data))
        before = self.state()
        with self.assertRaises(SeedMergeError):
            self.store.merge_seed(self.seed, apply=True)
        self.assertEqual(self.state(), before)
        data = json.loads(self.seed.read_text())
        data["procurement"] = {"packages": [{"id": "PKG-SYNTHETIC"}], "work_orders": []}
        data["continuity"] = {"different": True}
        self.store.db.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('continuity', '{\"kept\": 1}')"
        )
        self.seed.write_text(json.dumps(data))
        report = self.store.merge_seed(self.seed)
        self.assertEqual((report["docs_preserved"], report["conflicts"]), (["continuity"], 0))

    def test_expected_count_mismatch_refuses_before_writing(self) -> None:
        before = self.state()
        with self.assertRaises(SeedMergeError):
            self.store.merge_seed(self.seed, apply=True, expect_added=4)
        self.assertEqual(self.state(), before)

    def test_failure_after_inserts_rolls_back_all(self) -> None:
        before = self.state()
        with patch.object(SqlStore, "_append_audit", side_effect=RuntimeError("injected")):
            with self.assertRaises(RuntimeError):
                self.store.merge_seed(self.seed, apply=True)
        self.assertEqual(self.state(), before)
        self.assertEqual(self.store.merge_seed(self.seed, apply=True)["to_insert"], 3)

    def test_stale_audit_head_blocks_merge(self) -> None:
        self.store.db.execute("UPDATE audit_head SET count = count + 1")
        before = self.state()
        with self.assertRaises(SeedMergeError):
            self.store.merge_seed(self.seed, apply=True)
        self.assertEqual(self.state(), before)

    def test_corrupted_prior_audit_entry_blocks_merge(self) -> None:
        self.store.db.execute("DROP TRIGGER audit_no_update")
        self.store.db.execute(
            "UPDATE audit SET detail = 'tampered' WHERE seq = (SELECT MIN(seq) FROM audit)"
        )
        with self.assertRaises(SeedMergeError):
            self.store.merge_seed(self.seed, apply=True)
        self.assertEqual(len(self.state()["cases"]), len(dataset.DATA["cases"]))

    def test_staff_never_inserted(self) -> None:
        data = json.loads(self.seed.read_text())
        data["staff"].append(dict(data["staff"][0], email="seed.extra@example.invalid"))
        self.seed.write_text(json.dumps(data))
        before = self.state()["staff"]
        self.store.merge_seed(self.seed, apply=True)
        self.assertEqual(self.state()["staff"], before)


class SeedMergeCliTests(SeedMergeBase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        env = dict(ZF_STORE="sqlite", ZF_SQLITE=self.db, ZF_STATE=self.tmp.name)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = seed_merge.main(["--seed", str(self.seed), *args], env=env)
        return code, out.getvalue(), err.getvalue()

    def test_cli_dry_run_then_apply_and_privacy(self) -> None:
        code, out, _ = self.run_cli()
        self.assertEqual((code, json.loads(out)["applied"]), (0, False))
        code, out, _ = self.run_cli("--apply", "--expect-added", "3")
        self.assertEqual((code, json.loads(out)["applied"]), (0, True))
        text = json.dumps(dataset.DATA["cases"][0]["resident"]["name"])
        self.assertNotIn(text.strip('"'), out)
        self.assertNotIn("address", out)

    def test_cli_mismatch_and_conflict_exit_nonzero_without_rows(self) -> None:
        code, out, _ = self.run_cli("--apply", "--expect-added", "9")
        self.assertEqual(code, 3)
        self.assertNotIn(dataset.DATA["cases"][0]["resident"]["name"], out)
        self.assertEqual(self.run_cli("--apply", "--expect-added", "3")[0], 0)

    def test_cli_outputs_carry_no_case_content_on_any_path(self) -> None:
        data = json.loads(self.seed.read_text())
        data["cases"][0]["resident"]["name"] = "Zzyzx Qwerty"
        self.seed.write_text(json.dumps(data))
        private = (
            "Zzyzx",
            "Qwerty",
            dataset.DATA["cases"][0]["home"]["address"],
            dataset.DATA["cases"][0]["resident"]["name"],
        )
        for args in ((), ("--apply",), ("--apply", "--expect-added", "9")):
            code, out, err = self.run_cli(*args)
            self.assertEqual(code, 3)
            for text in private:
                self.assertNotIn(text, out + err)
        self.assertEqual(len(self.state()["cases"]), len(dataset.DATA["cases"]))

    def test_cli_refuses_an_empty_target_without_seeding_it(self) -> None:
        env = dict(
            ZF_STORE="sqlite",
            ZF_SQLITE=os.path.join(self.tmp.name, "empty.sqlite"),
            ZF_STATE=self.tmp.name,
        )
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(seed_merge.main(["--seed", str(self.seed), "--apply"], env=env), 2)
        import sqlite3

        raw = sqlite3.connect(os.path.join(self.tmp.name, "empty.sqlite"))
        self.addCleanup(raw.close)
        self.assertEqual(
            [raw.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("cases", "staff")],
            [0, 0],
        )

    def populated_default_dir(self) -> Path:
        """A data directory whose default database (no ZF_SQLITE/ZF_STATE) is the populated one."""
        d = Path(self.tmp.name) / "default"
        d.mkdir()
        self.store.db.close()
        os.replace(self.db, d / "zavaforward.sqlite")
        for ext in ("-wal", "-shm"):
            if os.path.exists(self.db + ext):
                os.replace(self.db + ext, str(d / "zavaforward.sqlite") + ext)
        self.store = SqlStore(str(self.seed), str(d / "zavaforward.sqlite"))
        self.addCleanup(self.store.db.close)
        self.db = str(d / "zavaforward.sqlite")
        return d

    def count(self, path: str) -> int:
        import sqlite3

        raw = sqlite3.connect(path)
        try:
            return int(raw.execute("SELECT COUNT(*) FROM cases").fetchone()[0])
        finally:
            raw.close()

    def run_env(self, env: dict[str, str], *args: str) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            return seed_merge.main(["--seed", str(self.seed), *args], env=env), out.getvalue()

    def test_default_path_merges_the_original_database_not_a_temporary_one(self) -> None:
        d = self.populated_default_dir()
        before = self.count(self.db)
        kept = Path(self.tmp.name) / "retained-temp"
        kept.mkdir()

        class Retained:
            def __init__(self) -> None:
                pass

            def __enter__(self) -> str:
                return str(kept)

            def __exit__(self, *a: object) -> None:
                return None

        with patch.object(tempfile, "TemporaryDirectory", Retained):
            code, out = self.run_env(
                dict(ZF_STORE="sqlite", ZF_DATA=str(d)), "--apply", "--expect-added", "3"
            )
        self.assertEqual((code, json.loads(out)["applied"]), (0, True))
        self.assertEqual(self.count(self.db), before + 3)
        self.assertEqual(list(kept.glob("*.sqlite")), [])

    def test_state_only_and_explicit_sqlite_paths_are_unchanged(self) -> None:
        state = Path(self.tmp.name) / "st"
        state.mkdir()
        self.store.db.close()
        os.replace(self.db, state / "zavaforward.sqlite")
        code, out = self.run_env(
            dict(ZF_STORE="sqlite", ZF_STATE=str(state), ZF_DATA=str(self.seed)), "--apply"
        )
        self.assertEqual(code, 0)
        self.assertEqual(
            self.count(str(state / "zavaforward.sqlite")), len(dataset.DATA["cases"]) + 3
        )
        other = Path(self.tmp.name) / "other-state"
        other.mkdir()
        code, out = self.run_env(
            dict(
                ZF_STORE="sqlite", ZF_SQLITE=str(state / "zavaforward.sqlite"), ZF_STATE=str(other)
            )
        )
        self.assertEqual((code, json.loads(out)["to_insert"]), (0, 0))

    def test_sqlite_path_matches_previous_resolution_and_mssql_gets_no_sqlite_setting(self) -> None:
        self.assertEqual(
            factory.sqlite_path(dict(ZF_SQLITE="/x/a.sqlite", ZF_STATE="/s")), "/x/a.sqlite"
        )
        self.assertEqual(
            factory.sqlite_path(dict(ZF_STATE="/s", ZF_DATA="/d/z.json")), "/s/zavaforward.sqlite"
        )
        self.assertEqual(factory.sqlite_path(dict(ZF_DATA="/d/z.json")), "/d/zavaforward.sqlite")
        seen = {}

        def fake(env: dict[str, str]) -> None:
            seen.update(env)
            raise SystemExit(9)

        with patch.object(seed_merge, "open_store", fake), self.assertRaises(SystemExit):
            self.run_env(dict(ZF_STORE="mssql", ZF_SQL_AUTH="msi", ZF_DATA="/real/seed.json"))
        self.assertNotIn("ZF_SQLITE", seen)
        self.assertEqual(seen["ZF_SQL_AUTH"], "msi")

    def test_cli_requires_sql_store(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(
                seed_merge.main(["--seed", str(self.seed)], env=dict(ZF_STORE="json")), 2
            )


if __name__ == "__main__":
    unittest.main()
