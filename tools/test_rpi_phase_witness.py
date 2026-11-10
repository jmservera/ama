"""Focused tests for the local RPI phase witness, run in isolated temporary repos."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("rpi_phase_witness.py")
SPEC = importlib.util.spec_from_file_location("rpi_phase_witness", SCRIPT)
witness = importlib.util.module_from_spec(SPEC)
sys.modules["rpi_phase_witness"] = witness
SPEC.loader.exec_module(witness)

STATE = ".copilot-tracking/rpi-sessions/s.json"
PATHS = {
    "research": ".copilot-tracking/research/r.md",
    "plan": ".copilot-tracking/plans/p.md",
    "details": ".copilot-tracking/details/d.md",
    "critique": ".copilot-tracking/plans/c.md",
    "changes": ".copilot-tracking/changes/ch.md",
    "review": ".copilot-tracking/reviews/rv.md",
}


def run_git(repo: Path, *args: str) -> str:
    return subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            *args,
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


class WitnessCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="rpi-witness-test-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        run_git(self.repo, "init", "-q")
        (self.repo / "src.txt").write_text("one\n")
        run_git(self.repo, "add", "src.txt")
        run_git(self.repo, "commit", "-qm", "init")
        self.state = {"artifact_paths": {key: None for key in PATHS}}
        self.write_state()

    def write_state(self) -> None:
        (self.repo / STATE).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / STATE).write_text(json.dumps(self.state))

    def persist(self, *keys: str) -> None:
        for key in keys:
            path = self.repo / PATHS[key]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{key} record\n")
            self.state["artifact_paths"][key] = PATHS[key]
        self.write_state()

    def record(self, event: str, *extra: str) -> tuple[int, dict]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = witness.main(
                [
                    "record",
                    event,
                    "--repo",
                    str(self.repo),
                    "--issue",
                    "1300",
                    "--state",
                    STATE,
                    *extra,
                ]
            )
        return code, json.loads(out.getvalue())

    def verify(self) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = witness.main(["verify", "--repo", str(self.repo), "--issue", "1300"])
        return code, out.getvalue()

    def log(self) -> Path:
        return witness.log_paths(self.repo, "1300")[0]

    def observe_launch(self) -> None:
        brief = Path(self.tmp.name) / "brief.md"
        brief.write_text("synthetic brief\n")
        self.assertEqual(self.record("launch", "--brief", str(brief))[0], 0)

    def commit_all(self) -> tuple[int, dict]:
        run_git(self.repo, "add", "-A", ".")
        run_git(self.repo, "commit", "-qm", "work")
        head = run_git(self.repo, "rev-parse", "HEAD")
        return self.record("commit-complete", "--claim-commit", head)

    def launched_run(self) -> None:
        self.observe_launch()
        self.full_run()

    def full_run(self) -> None:
        self.persist("research")
        self.assertEqual(self.record("research-open")[0], 0)
        self.persist("plan", "details", "critique")
        self.assertEqual(self.record("plan-done")[0], 0)
        self.persist("changes")
        self.assertEqual(self.record("implement-start")[0], 0)
        (self.repo / "src.txt").write_text("two\n")
        self.assertEqual(self.record("implement-done")[0], 0)
        self.persist("review")
        self.assertEqual(self.record("review-done")[0], 0)


class ObservationTests(WitnessCase):
    def test_clock_is_the_tool_clock_and_caller_time_is_rejected(self) -> None:
        self.persist("research")
        before = datetime.now(UTC)
        _, result = self.record("research-open")
        stamp = datetime.fromisoformat(result["utc"])
        self.assertTrue(before <= stamp <= datetime.now(UTC))
        for option in ("--utc", "--time", "--started-at"):
            with (
                self.assertRaises(SystemExit) as raised,
                contextlib.redirect_stderr(io.StringIO()),
            ):
                witness.main(
                    [
                        "record",
                        "research-open",
                        "--repo",
                        str(self.repo),
                        "--issue",
                        "1300",
                        option,
                        "2020-01-01T00:00:00Z",
                    ]
                )
            self.assertEqual(raised.exception.code, 64)

    def test_missing_artifact_is_refused_and_kept(self) -> None:
        code, result = self.record("research-open")
        self.assertEqual(code, 2)
        self.assertIn("research", result["reasons"][0])
        self.persist("research")
        self.assertEqual(self.record("research-open")[0], 0)
        records, _ = witness.read_log(self.log())
        self.assertEqual([r["outcome"] for r in records], ["refused", "ok"])
        self.assertEqual(self.verify()[0], 1)

    def test_missing_state_and_empty_artifact_are_refused(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = witness.main(
                ["record", "research-open", "--repo", str(self.repo), "--issue", "1300"]
            )
        self.assertEqual(code, 2)
        self.persist("research")
        (self.repo / PATHS["research"]).write_text("")
        self.assertEqual(self.record("research-open")[0], 2)

    def test_out_of_order_is_recorded_and_qualified(self) -> None:
        self.persist("research", "plan", "details", "critique", "changes")
        code, result = self.record("implement-start")
        self.assertEqual(code, 0)
        self.assertIn("missing observed predecessor", result["qualifications"][0])
        code, text = self.verify()
        self.assertEqual(code, 1)
        self.assertIn("QUALIFIED", text)

    def test_dirty_source_at_implement_start_is_qualified(self) -> None:
        self.persist("changes")
        (self.repo / "src.txt").write_text("edited early\n")
        _, result = self.record("implement-start")
        self.assertTrue(any("already dirty" in q for q in result["qualifications"]))
        records, _ = witness.read_log(self.log())
        self.assertIn("src.txt", records[0]["git"]["dirty_source"])

    def test_clean_run_verifies_and_artifact_evolution_is_only_a_note(self) -> None:
        self.launched_run()
        (self.repo / PATHS["plan"]).write_text("plan record, later checklist tick\n")
        code, text = self.verify()
        self.assertIn("note:", text)
        records, _ = witness.read_log(self.log())
        self.assertEqual(code, 1)  # no observed commit-complete yet
        self.assertEqual(sum("QUALIFIED" in line for line in text.splitlines()), 1)
        self.assertEqual(len(records), 6)

    def test_guarded_review_revision_is_qualified(self) -> None:
        self.full_run()
        (self.repo / PATHS["review"]).write_text("rewritten review\n")
        self.assertIn("review artifact changed after observation", self.verify()[1])

    def test_stale_review_source(self) -> None:
        self.full_run()
        (self.repo / "src.txt").write_text("three\n")
        self.assertIn("review source is stale", self.verify()[1])


class CommitTests(WitnessCase):
    def test_commit_marker_without_commit_is_refused(self) -> None:
        self.full_run()
        head = run_git(self.repo, "rev-parse", "HEAD")
        code, result = self.record("commit-complete", "--claim-commit", head)
        self.assertEqual(code, 2)
        self.assertTrue(result["reasons"])

    def test_commit_with_reviewed_content_is_accepted_and_not_stale(self) -> None:
        self.launched_run()
        self.assertEqual(self.commit_all()[0], 0)
        code, text = self.verify()
        self.assertEqual(code, 0, text)
        self.assertNotIn("stale", text)

    def test_complete_run_without_launch_is_qualified(self) -> None:
        self.full_run()
        self.assertEqual(self.commit_all()[0], 0)
        records, _ = witness.read_log(self.log())
        self.assertTrue(
            any("launch" in q for q in records[0]["qualifications"]), records[0]
        )
        code, text = self.verify()
        self.assertEqual(code, 1)
        self.assertIn("no successful observation of launch", text)

    def test_clean_source_commit_before_implement_start_is_qualified(self) -> None:
        self.observe_launch()
        self.persist("research")
        self.assertEqual(self.record("research-open")[0], 0)
        (self.repo / "src.txt").write_text("early commit\n")
        run_git(self.repo, "add", "src.txt")
        run_git(self.repo, "commit", "-qm", "early")
        self.persist("plan", "details", "critique", "changes")
        self.assertEqual(self.record("plan-done")[0], 0)
        _, opening = self.record("implement-start")
        self.assertTrue(any("src.txt" in q for q in opening["qualifications"]), opening)
        self.assertEqual(self.verify()[0], 1)

    def test_tracking_only_commit_and_unrelated_head_are_handled(self) -> None:
        self.observe_launch()
        self.persist("research")
        self.assertEqual(self.record("research-open")[0], 0)
        run_git(self.repo, "add", "-A", ".")
        run_git(self.repo, "commit", "-qm", "records only")
        self.persist("plan", "details", "critique", "changes")
        self.assertEqual(self.record("plan-done")[0], 0)
        _, opening = self.record("implement-start")
        self.assertEqual(opening["qualifications"], [])
        # A first HEAD that is not an ancestor cannot be compared.
        records, _ = witness.read_log(self.log())
        records[0]["git"]["head"] = "0" * 40
        self.assertIn(
            "unable to compare",
            witness.early_source_changes(self.repo, records, "HEAD")[0],
        )

    def test_wrong_claim_and_unrelated_commit_are_refused(self) -> None:
        self.full_run()
        self.assertEqual(
            self.record("commit-complete", "--claim-commit", "0" * 40)[0], 2
        )
        (self.repo / "other.txt").write_text("unrelated\n")
        run_git(self.repo, "add", "other.txt")
        run_git(self.repo, "commit", "-qm", "unrelated")
        head = run_git(self.repo, "rev-parse", "HEAD")
        self.assertEqual(self.record("commit-complete", "--claim-commit", head)[0], 2)


class LogTests(WitnessCase):
    def test_torn_tail_is_kept_and_next_record_chains(self) -> None:
        self.persist("research")
        self.record("research-open")
        with self.log().open("ab") as handle:
            handle.write(b'{"seq": 2, "event": "pla')
        self.assertEqual(self.record("research-open")[0], 0)
        records, problems = witness.read_log(self.log())
        self.assertEqual(len(records), 2)
        self.assertEqual(len(problems), 1)
        self.assertIn(b'"pla\n', self.log().read_bytes())
        self.assertIn("torn", self.verify()[1])

    def test_edited_record_breaks_chain(self) -> None:
        self.persist("research")
        self.record("research-open")
        self.record("research-open")
        text = (
            self.log()
            .read_text()
            .replace('"refused"', '"ok"')
            .replace(self.repo.name, self.repo.name + "x", 1)
        )
        self.log().write_text(text)
        self.assertIn("hash mismatch", self.verify()[1])

    def test_concurrent_writers_keep_a_valid_chain(self) -> None:
        self.persist("research")
        command = [
            sys.executable,
            str(SCRIPT),
            "record",
            "research-open",
            "--repo",
            str(self.repo),
            "--issue",
            "1300",
            "--state",
            STATE,
        ]
        writers = [
            subprocess.Popen(command, stdout=subprocess.DEVNULL) for _ in range(8)
        ]
        self.assertEqual([writer.wait() for writer in writers], [0] * 8)
        records, problems = witness.read_log(self.log())
        self.assertEqual(problems, [])
        self.assertEqual([r["seq"] for r in records], list(range(1, 9)))

    def test_backward_clock_is_qualified(self) -> None:
        self.persist("research")
        self.record("research-open")
        lines = self.log().read_text().splitlines()
        record = json.loads(lines[0])
        record["utc"] = "2999-01-01T00:00:00.000000+00:00"
        record["record_hash"] = witness.record_hash(record)
        self.log().write_text(
            json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
        )
        _, result = self.record("research-open")
        self.assertIn(
            "clock earlier than the previous record", result["qualifications"]
        )
        self.assertIn("clock earlier", self.verify()[1])


class IsolationTests(WitnessCase):
    def test_state_and_artifact_paths_cannot_escape_tracking(self) -> None:
        outside = Path(self.tmp.name) / "outside.md"
        outside.write_text("x\n")
        self.state["artifact_paths"]["research"] = "../outside.md"
        self.write_state()
        self.assertEqual(self.record("research-open")[0], 2)
        link = self.repo / PATHS["research"]
        link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(outside, link)
        self.state["artifact_paths"]["research"] = PATHS["research"]
        self.write_state()
        self.assertEqual(self.record("research-open")[0], 2)

    def test_verify_does_not_read_a_substituted_external_artifact(self) -> None:
        self.full_run()
        review = self.repo / PATHS["review"]
        dummy = Path(self.tmp.name) / "owned-dummy.md"
        dummy.write_text("review record\n")
        review.unlink()
        review.symlink_to(dummy)
        real = witness.sha256_file

        def guarded(path: Path) -> str:
            if Path(path).resolve() == dummy.resolve():
                raise AssertionError("read outside")
            return real(path)

        with mock.patch.object(witness, "sha256_file", side_effect=guarded):
            code, text = self.verify()
        self.assertEqual(code, 1)
        self.assertIn("escapes the tracking root", text)

    def test_replaced_tracking_root_is_refused_before_any_open(self) -> None:
        self.full_run()
        outside = Path(self.tmp.name) / "outside-tracking"
        (self.repo / witness.TRACKING).rename(outside)
        (self.repo / witness.TRACKING).symlink_to(outside)
        before = (outside / "phase-witness/issue-1300/events.jsonl").read_bytes()
        with mock.patch.object(
            witness, "sha256_file", side_effect=AssertionError("read outside")
        ):
            code, text = self.verify()
            self.assertEqual(code, 1)
            self.assertIn("not read", text)
            code, result = self.record(
                "research-open"
            )  # state resolves outside tracking, so refused
        self.assertEqual(code, 2, result)
        after = (outside / "phase-witness/issue-1300/events.jsonl").read_bytes()
        self.assertEqual(before, after)

    def test_log_and_lock_symlink_targets_are_not_opened(self) -> None:
        self.persist("research")
        log, lock = witness.log_paths(self.repo, "1300")
        log.parent.mkdir(parents=True)
        target = Path(self.tmp.name) / "outside.log"
        target.write_text("untouched\n")
        log.symlink_to(target)
        self.assertEqual(self.record("research-open")[0], 2)
        log.unlink()
        lock.symlink_to(target)
        self.assertEqual(self.record("research-open")[0], 2)
        self.assertEqual(target.read_text(), "untouched\n")

    def test_launch_requires_a_brief_and_captures_no_environment(self) -> None:
        self.assertEqual(self.record("launch")[0], 2)
        brief = Path(self.tmp.name) / "brief.md"
        brief.write_text("brief\n")
        os.environ["RPI_WITNESS_SECRET"] = "do-not-record"
        self.addCleanup(os.environ.pop, "RPI_WITNESS_SECRET")
        code, _ = self.record(
            "launch",
            "--brief",
            str(brief),
            "--actor",
            "coordinator",
            "--claim-model",
            "claude-sonnet-5.5",
            "--session",
            "rpi-1300",
        )
        self.assertEqual(code, 0)
        text = self.log().read_text()
        self.assertNotIn("do-not-record", text)
        records, _ = witness.read_log(self.log())
        self.assertEqual(records[-1]["asserted"]["model"], "claude-sonnet-5.5")
        self.assertEqual(records[-1]["brief"]["sha256"], witness.sha256_file(brief))


class AdoptionTests(unittest.TestCase):
    def test_coordinator_step_five_invokes_the_helper(self) -> None:
        text = (
            Path(__file__)
            .parents[1]
            .joinpath(".github/agents/ama-backlog-delivery-coordinator.agent.md")
            .read_text()
        )
        for needle in (
            "tools/rpi_phase_witness.py record launch",
            "tools/rpi_phase_witness.py verify",
        ):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
