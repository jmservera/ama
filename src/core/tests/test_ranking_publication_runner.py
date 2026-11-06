"""Local ranking publication runner: schedule, publish and verify (Refs #79).

Synthetic fixtures only. The shipped ranking policy is an unsigned draft and stays one; the signed
copies below exist only inside tests and are patched into a temporary registry.
"""

import contextlib
import copy
import errno
import io
import json
import os
import tempfile
import unittest
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import case
from test_ranking_publication import DEADLINE, gated
from zava_forward.core import ranking
from zava_forward.core import ranking_publication as rp
from zava_forward.core import ranking_publication_runner as runner
from zava_forward.core.store import Store

TODAY = "2026-11-05"
AS_OF = "2026-11-05"


def open_cases() -> list[dict[str, Any]]:
    a, b = case("ZF-A"), case("ZF-B")
    b["days_in_stage"] = 50
    return [a, b]


def signed_registry() -> dict[str, Any]:
    pol = copy.deepcopy(ranking.POLICY_V1)
    pol["owner"] = "Dana Example"
    pol["signoff"] = dict(
        signed_by="Dana Example",
        signed_on="2026-11-05",
        rule_order_hash=ranking.rule_order_hash(pol),
    )
    pol["content_hash"] = ranking.policy_hash(pol)
    return {pol["version"]: pol}


class RunnerBase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.archive = self.root / "archive"
        self.signed = signed_registry()

    def go(self, op: str, **kw: Any) -> dict[str, Any]:
        kw.setdefault("registry", self.signed)
        return runner.run(op, self.archive, kw.pop("today", TODAY), **kw)

    def codes(self, res: dict[str, Any]) -> list[str]:
        return [r["code"] for r in res["refusals"]]

    def cli(self, *args: str) -> tuple[int, dict[str, Any]]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = runner.main(list(args))
        return code, json.loads(out.getvalue())

    @contextlib.contextmanager
    def registry_patched(self) -> Iterator[None]:
        version = ranking.POLICY_V1["version"]
        pol = self.signed[version]
        with patch.dict(ranking.POLICIES, {version: pol}), patch.object(ranking, "CURRENT", pol):
            yield

    def cases_file(self) -> Path:
        path = self.root / "cases.json"
        path.write_text(json.dumps({"as_of": AS_OF, "cases": open_cases()}))
        return path


class PublishTests(RunnerBase):
    def test_signed_policy_publishes_once_and_repeat_is_idempotent(self) -> None:
        first = self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.assertEqual((first["status"], first["written"]), ("published", True))
        again = self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.assertEqual((again["status"], again["written"]), ("already_published", False))
        self.assertEqual((again["path"], again["run_key"]), (first["path"], first["run_key"]))
        self.assertEqual(len(list(self.archive.iterdir())), 1)
        self.assertEqual(self.go("verify")["status"], "ok")

    def test_same_inputs_give_the_same_run_key_and_snapshot_in_any_case_order(self) -> None:
        a = self.go("publish", cases=open_cases(), as_of=AS_OF, exercise=True)
        b = self.go("publish", cases=list(reversed(open_cases())), as_of=AS_OF, exercise=True)
        self.assertEqual((a["run_key"], a["snapshot_hash"]), (b["run_key"], b["snapshot_hash"]))
        later = self.go(
            "publish", cases=open_cases(), as_of=AS_OF, exercise=True, today="2026-11-06"
        )
        self.assertNotEqual(a["run_key"], later["run_key"])

    def test_draft_policy_fails_closed_with_approval_reason_and_writes_nothing(self) -> None:
        res = runner.run("publish", self.archive, TODAY, cases=open_cases(), as_of=AS_OF)
        self.assertEqual((res["status"], self.codes(res)), ("refused", ["approval_missing"]))
        self.assertEqual(res["refusals"][0]["message"], "No named policy owner.")
        self.assertFalse(res["policy"]["signed"])
        self.assertFalse(self.archive.exists())
        self.assertEqual(ranking.CURRENT["owner"], "to be named")
        self.assertFalse(ranking.is_signed(ranking.CURRENT))

    def test_owner_without_recorded_signoff_is_refused(self) -> None:
        reg = copy.deepcopy(self.signed)
        pol = reg[ranking.POLICY_V1["version"]]
        del pol["signoff"]
        pol["content_hash"] = ranking.policy_hash(pol)
        res = self.go("publish", cases=open_cases(), as_of=AS_OF, registry=reg)
        self.assertEqual(self.codes(res), ["approval_missing"])
        self.assertIn("No recorded sign-off", res["refusals"][0]["message"])

    def test_exercise_runs_unsigned_policy_but_never_writes_or_approves(self) -> None:
        res = runner.run(
            "publish", self.archive, TODAY, cases=open_cases(), as_of=AS_OF, exercise=True
        )
        self.assertEqual((res["status"], res["written"], res["refusals"]), ("exercise", False, []))
        self.assertFalse(res["policy"]["signed"])
        self.assertIn("proposed", res["schedule"]["status"])
        self.assertFalse(self.archive.exists())

    def test_missing_unusable_or_undated_source_fails_closed(self) -> None:
        self.assertEqual(self.codes(self.go("publish", as_of=AS_OF)), ["source_missing"])
        self.assertEqual(self.codes(self.go("publish", cases=open_cases())), ["source_missing"])
        broken = open_cases()
        del broken[0]["days_in_stage"]
        self.assertEqual(
            self.codes(self.go("publish", cases=broken, as_of=AS_OF)), ["source_invalid"]
        )
        self.assertFalse(self.archive.exists())

    def test_future_source_is_refused_and_stale_source_is_published_with_a_warning(self) -> None:
        future = self.go("publish", cases=open_cases(), as_of="2026-11-06")
        self.assertEqual(self.codes(future), ["source_future"])
        self.assertFalse(self.archive.exists())
        stale = self.go("publish", cases=open_cases(), as_of="2026-11-04")
        self.assertEqual((stale["status"], stale["source_current"]), ("published", False))
        self.assertEqual([w["code"] for w in stale["warnings"]], ["source_not_current"])
        self.assertEqual(self.go("publish", cases=open_cases(), as_of=AS_OF)["warnings"], [])

    def test_missing_capacity_fails_closed_without_partial_file(self) -> None:
        res = self.go("publish", cases=open_cases(), as_of=AS_OF, free_bytes=lambda _p: 10)
        self.assertEqual(self.codes(res), ["capacity_missing"])
        self.assertFalse(self.archive.exists())

    def test_damaged_archive_blocks_publish_and_is_not_overwritten(self) -> None:
        self.go("publish", cases=open_cases(), as_of=AS_OF)
        path = next(self.archive.iterdir())
        rec = json.loads(path.read_text())
        rec["snapshot"]["entries"].reverse()
        path.write_text(json.dumps(rec))
        damaged = path.read_text()
        res = self.go("publish", cases=open_cases(), as_of="2026-11-06", today="2026-11-06")
        self.assertEqual(self.codes(res), ["archive_unverified"])
        self.assertEqual(path.read_text(), damaged)
        self.assertEqual(self.go("verify")["status"], "problem")

    def test_bad_date_unknown_operation_and_unknown_policy_are_refused(self) -> None:
        self.assertEqual(self.codes(self.go("publish", today="05/11/2026")), ["bad_date"])
        self.assertEqual(self.codes(self.go("purge")), ["unknown_operation"])
        res = self.go("publish", cases=open_cases(), as_of=AS_OF, policy_version="9.9.9")
        self.assertEqual(self.codes(res), ["policy_unknown"])


class ConcurrentPublishTests(RunnerBase):
    def test_same_snapshot_on_two_dates_publishes_once_and_reports_the_retained_date(self) -> None:
        def publish(today: str) -> dict[str, Any]:
            return self.go("publish", today=today, cases=open_cases(), as_of=AS_OF)

        with gated("A", "B") as gate:
            gate.start("A", lambda: publish("2026-11-05"))
            self.assertTrue(gate.arrived["A"].wait(DEADLINE))
            gate.start("B", lambda: publish("2026-11-06"))
            self.assertTrue(gate.arrived["B"].wait(DEADLINE))
            gate.release("A")
            gate.release("B")
            gate.join()
        a, b = gate.results["A"], gate.results["B"]
        self.assertIsInstance(b, dict)
        self.assertEqual(
            (a["status"], a["written"], a["published_on"]), ("published", True, "2026-11-05")
        )
        self.assertEqual(
            (b["status"], b["written"], b["published_on"]),
            ("already_published", False, "2026-11-05"),
        )
        self.assertEqual(self.codes(b), [])
        (record,) = self.archive.iterdir()
        self.assertEqual(json.loads(record.read_text())["published_on"], "2026-11-05")
        self.assertEqual(rp.verify(self.archive, self.signed)["problems"], [])

    def test_filesystem_without_hard_links_is_a_refusal_and_writes_no_record(self) -> None:
        with patch.object(os, "link", side_effect=OSError(errno.EPERM, "hard links unsupported")):
            res = self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.assertEqual(self.codes(res), ["publish_failed"])
        self.assertNotIn("written", res)
        self.assertEqual(list(self.archive.iterdir()), [])
        again = self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.assertEqual((again["status"], again["written"]), ("published", True))


class ScheduleAndVerifyTests(RunnerBase):
    def test_schedule_reports_window_due_and_next_window_without_writing(self) -> None:
        res = self.go("schedule")
        self.assertEqual(
            (res["status"], res["due"], res["window"]),
            ("due", True, {"start": TODAY, "end": "2026-11-06"}),
        )
        self.assertEqual(res["next_window_start"], TODAY)
        self.assertFalse(self.archive.exists())
        self.go("publish", cases=open_cases(), as_of=AS_OF)
        done = self.go("schedule")
        self.assertEqual(
            (done["status"], done["due"], done["next_window_start"]),
            ("current", False, "2026-11-06"),
        )
        self.assertTrue(self.go("schedule", today="2026-11-06")["due"])

    def test_schedule_with_draft_policy_is_blocked_and_proposed_not_approved(self) -> None:
        res = runner.run("schedule", self.archive, TODAY)
        self.assertEqual((res["status"], self.codes(res)), ("blocked", ["approval_missing"]))
        self.assertTrue(res["schedule"]["status"].startswith("proposed, not"))
        self.assertEqual(res["schedule"]["owner"], "to be named")
        self.assertIn("not set", res["schedule"]["retention"])
        self.assertIn("Legal", res["retention_note"])

    def test_verify_flags_missing_and_stale_publication_as_problem(self) -> None:
        self.assertEqual(self.go("verify")["status"], "problem")
        self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.assertEqual(self.go("verify")["status"], "ok")
        stale = self.go("verify", today="2026-11-07")
        self.assertEqual(
            (stale["status"], stale["overdue"], stale["problems"]), ("problem", True, [])
        )


class MalformedArchivedDateTests(RunnerBase):
    def damage(self, value: Any) -> Path:
        self.go("publish", cases=open_cases(), as_of=AS_OF)
        (path,) = self.archive.iterdir()
        rec = json.loads(path.read_text())
        rec["published_on"] = value
        path.write_text(json.dumps(rec))
        return path

    def test_impossible_calendar_date_is_reported_by_all_operations_without_crashing(self) -> None:
        path = self.damage("2026-11-31")
        before = path.read_bytes()
        problem = f"{path.name}: publication date is not a valid calendar date."
        ver = self.go("verify")
        self.assertEqual(
            (ver["status"], ver["latest"], ver["problems"]), ("problem", None, [problem])
        )
        sched = self.go("schedule")
        self.assertEqual(
            (sched["due"], sched["latest"], sched["next_window_start"], sched["problems"]),
            (True, None, TODAY, [problem]),
        )
        pub = self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.assertEqual((pub["status"], self.codes(pub)), ("refused", ["archive_unverified"]))
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(len(list(self.archive.iterdir())), 1)

    def test_malformed_metadata_types_never_look_current_or_crash(self) -> None:
        self.damage("2026-11-05")
        odd = ("2026-11-05\n", "\u0662\u0660\u0662\u0666-\u0661\u0661-\u0660\u0665")
        for value in (None, 20261105, ["2026-11-05"], "20261105", "", *odd):
            with self.subTest(value=value):
                (path,) = self.archive.iterdir()
                rec = json.loads(path.read_text())
                rec["published_on"] = value
                path.write_text(json.dumps(rec))
                for op in ("verify", "schedule"):
                    res = self.go(op)
                    self.assertEqual(len(res["problems"]), 1)
                    self.assertIsNone(res["latest"])
                self.assertEqual(self.go("verify")["status"], "problem")

    def test_valid_archived_date_still_schedules_next_window(self) -> None:
        self.go("publish", cases=open_cases(), as_of=AS_OF)
        done = self.go("schedule")
        self.assertEqual((done["status"], done["next_window_start"]), ("current", "2026-11-06"))


class CliAndStoreTests(RunnerBase):
    def test_cli_exit_codes_and_explicit_inputs(self) -> None:
        arch = ["--archive", str(self.archive), "--today", TODAY]
        code, res = self.cli("publish", *arch, "--cases", str(self.cases_file()))
        self.assertEqual(
            (code, res["status"], res["refusals"][0]["code"]), (2, "refused", "approval_missing")
        )
        code, res = self.cli("publish", *arch, "--cases", str(self.cases_file()), "--exercise")
        self.assertEqual((code, res["status"]), (0, "exercise"))
        code, res = self.cli(
            "publish", *arch, "--cases", str(self.root / "absent.json"), "--exercise"
        )
        self.assertEqual((code, res["refusals"][0]["code"]), (2, "source_missing"))
        self.assertFalse(self.archive.exists())

    def test_cli_publish_verify_round_trip_with_signed_policy(self) -> None:
        arch = ["--archive", str(self.archive), "--today", TODAY]
        with self.registry_patched():
            self.assertEqual(self.cli("verify", *arch)[0], 1)
            code, res = self.cli("publish", *arch, "--cases", str(self.cases_file()))
            self.assertEqual((code, res["status"], res["as_of"]), (0, "published", AS_OF))
            self.assertEqual(
                self.cli("publish", *arch, "--cases", str(self.cases_file()))[1]["status"],
                "already_published",
            )
            self.assertEqual(self.cli("verify", *arch)[0], 0)

    def test_publishes_from_persisted_store_and_store_status_reads_it_back(self) -> None:
        data = Path(self.tmp.name) / "zavaforward.json"
        data.write_text(json.dumps({"as_of": AS_OF, "staff": [], "cases": open_cases()}))
        store = Store(str(data))
        store.save()
        cases, as_of = runner.load_cases(store.live_path)
        self.assertEqual((len(cases), as_of), (2, AS_OF))
        manager = {"email": "pam@example.test", "role": "Retrofit Programme Manager"}
        with self.registry_patched():
            res = runner.run("publish", store._ranking_archive(), TODAY, cases=cases, as_of=as_of)
            self.assertEqual(res["status"], "published")
            status = store.ranking_publication_status(manager)
            self.assertEqual((status["count"], status["problems"]), (1, []))
            self.assertEqual(store.publish_ranking_snapshot(manager)["written"], False)
        self.assertEqual(rp.verify(store._ranking_archive(), self.signed)["count"], 1)

    def test_runner_has_no_clock_environment_default_data_or_delete(self) -> None:
        src = Path(runner.__file__).read_text()
        for word in (
            "datetime.now",
            "date.today",
            "import time",
            "os.environ",
            "ZF_DATA",
            "os.remove",
            "unlink",
            "rmtree",
            "Store(",
            "import random",
        ):
            self.assertNotIn(word, src)


class AssessmentFindingTests(RunnerBase):
    def damaged_extra(self, archive: Path) -> None:
        archive.mkdir(exist_ok=True)
        (archive / "ranking-garbage.json").write_text("not json")

    def test_malformed_closed_flags_refuse_the_whole_source(self) -> None:
        path = self.root / "bad.json"
        bad_values: list[Any] = ["false", None, 1, 0, "", []]
        for bad in bad_values:
            with self.subTest(closed=bad):
                cases = open_cases()
                cases[0]["closed"] = bad
                path.write_text(json.dumps({"as_of": AS_OF, "cases": cases}))
                with self.assertRaises(TypeError):
                    runner.load_cases(path)
                arch = ["--archive", str(self.archive), "--today", TODAY, "--cases", str(path)]
                with self.registry_patched():
                    code, res = self.cli("publish", *arch)
                self.assertEqual((code, self.codes(res)), (2, ["source_missing"]))
                self.assertFalse(self.archive.exists())
        path.write_text(json.dumps({"as_of": AS_OF, "cases": ["x"]}))
        with self.assertRaises(TypeError):
            runner.load_cases(path)
        mixed = open_cases() + [dict(open_cases()[0], closed=True)]
        path.write_text(json.dumps({"as_of": AS_OF, "cases": mixed}))
        self.assertEqual(len(runner.load_cases(path)[0]), 2)

    def test_schedule_is_a_problem_when_the_archive_does_not_verify(self) -> None:
        self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.damaged_extra(self.archive)
        mixed = self.go("schedule")
        self.assertEqual(
            (mixed["status"], mixed["due"], mixed["latest"], len(mixed["problems"])),
            ("problem", False, TODAY, 1),
        )
        arch = ["--archive", str(self.archive), "--today", TODAY]
        with self.registry_patched():
            self.assertEqual(self.cli("schedule", *arch)[0], 1)
        only_bad = self.root / "only-bad"
        self.damaged_extra(only_bad)
        res = runner.run("schedule", only_bad, TODAY, registry=self.signed)
        self.assertEqual((res["status"], res["due"], res["latest"]), ("problem", True, None))
        draft = runner.run("schedule", self.archive, TODAY)
        self.assertEqual((draft["status"], self.codes(draft)), ("problem", ["approval_missing"]))

    def test_verified_identical_retry_needs_no_new_capacity(self) -> None:
        first = self.go("publish", cases=open_cases(), as_of=AS_OF)
        path = Path(first["path"])
        before = path.read_bytes()
        again = self.go(
            "publish", cases=open_cases(), as_of=AS_OF, today="2026-11-06", free_bytes=lambda _p: 0
        )
        self.assertEqual((again["status"], again["written"]), ("already_published", False))
        self.assertEqual((again["published_on"], path.read_bytes()), (TODAY, before))
        fresh = self.go("publish", cases=open_cases()[:1], as_of=AS_OF, free_bytes=lambda _p: 0)
        self.assertEqual(self.codes(fresh), ["capacity_missing"])
        self.assertEqual(len(list(self.archive.iterdir())), 1)

    def test_latest_representable_date_is_refused_without_a_traceback(self) -> None:
        for op in ("schedule", "publish", "verify"):
            with self.subTest(op=op):
                res = self.go(op, today="9999-12-31", cases=open_cases(), as_of="9999-12-31")
                self.assertEqual((res["status"], self.codes(res)), ("refused", ["bad_date"]))
        code, res = self.cli("schedule", "--archive", str(self.archive), "--today", "9999-12-31")
        self.assertEqual((code, self.codes(res)), (2, ["bad_date"]))
        self.assertFalse(self.archive.exists())

    def test_archived_latest_without_a_next_day_is_a_problem_not_a_crash(self) -> None:
        first = self.go("publish", cases=open_cases(), as_of=AS_OF)
        path = Path(first["path"])
        rec = json.loads(path.read_text())
        rec["published_on"] = "9999-12-31"
        path.write_text(json.dumps(rec))
        before = path.read_bytes()
        sched = self.go("schedule")
        self.assertEqual(
            (sched["status"], sched["latest"], sched["next_window_start"]),
            ("problem", "9999-12-31", None),
        )
        self.assertEqual(len(sched["problems"]), 1)
        pub = self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.assertEqual((pub["status"], self.codes(pub)), ("refused", ["archive_unverified"]))
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(len(list(self.archive.iterdir())), 1)
        self.assertEqual(self.go("verify")["latest"], "9999-12-31")


class StorageAndDuplicateFindingTests(RunnerBase):
    def unreadable(self) -> Any:
        self.archive.mkdir()
        return patch("os.listdir", side_effect=PermissionError(13, "Permission denied"))

    def test_unreadable_archive_is_a_problem_never_empty_or_healthy(self) -> None:
        with self.unreadable():
            ver = self.go("verify")
            sched = self.go("schedule")
            pub = self.go("publish", cases=open_cases(), as_of=AS_OF)
        self.assertEqual((ver["status"], ver["latest"], len(ver["problems"])), ("problem", None, 1))
        self.assertIn("PermissionError", ver["problems"][0])
        self.assertEqual(
            (sched["status"], sched["due"], sched["next_window_start"]), ("problem", None, None)
        )
        self.assertEqual((pub["status"], self.codes(pub)), ("refused", ["archive_unreadable"]))
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_unreadable_archive_exits_nonzero_through_main(self) -> None:
        cases = self.cases_file()
        base = ("--archive", str(self.archive), "--today", TODAY)
        with self.registry_patched(), self.unreadable():
            self.assertEqual(self.cli("verify", *base)[0], 1)
            self.assertEqual(self.cli("schedule", *base)[0], 1)
            code, res = self.cli("publish", *base, "--cases", str(cases))
        self.assertEqual((code, self.codes(res)), (2, ["archive_unreadable"]))
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_capacity_probe_failure_is_a_refusal_not_a_traceback(self) -> None:
        def broken(_p: Any) -> int:
            raise OSError(5, "Input/output error")

        res = self.go("publish", cases=open_cases(), as_of=AS_OF, free_bytes=broken)
        self.assertEqual((res["status"], self.codes(res)), ("refused", ["capacity_missing"]))
        self.assertIn("OSError", res["refusals"][0]["message"])
        cases = self.cases_file()
        self.archive.mkdir(exist_ok=True)
        with self.registry_patched(), patch("shutil.disk_usage", side_effect=OSError(5, "I/O")):
            code, out = self.cli(
                "publish", "--archive", str(self.archive), "--today", TODAY, "--cases", str(cases)
            )
        self.assertEqual((code, self.codes(out)), (2, ["capacity_missing"]))
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_duplicate_case_identity_is_source_invalid_before_ranking(self) -> None:
        dup = open_cases() + open_cases()[:1]
        res = self.go("publish", cases=dup, as_of=AS_OF)
        self.assertEqual((res["status"], self.codes(res)), ("refused", ["source_invalid"]))
        path = self.root / "dup.json"
        path.write_text(json.dumps({"as_of": AS_OF, "cases": dup}))
        with self.registry_patched():
            code, out = self.cli(
                "publish", "--archive", str(self.archive), "--today", TODAY, "--cases", str(path)
            )
        self.assertEqual((code, self.codes(out)), (2, ["source_invalid"]))
        self.assertFalse(self.archive.exists())


if __name__ == "__main__":
    unittest.main()
