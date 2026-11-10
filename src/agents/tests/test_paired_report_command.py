"""Command-level tests for the constructed paired-observation input of run_regulatory_gates.py.

The observations are caller-declared constructed data, not staff evidence.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from zava_forward.agents.paired_trial import evaluate_paired_trial

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "src/agents/evals/run_regulatory_gates.py"
PYTHONPATH = os.pathsep.join(str(REPO / "src" / name / "tests") for name in ("core", "agents"))
OPTION = "--constructed-paired-observations"
SCHEMA = "constructed-paired-observations-v1"
SECTION = "constructed_paired_observations"
ROLES = ("repairs", "housing", "grants")
UNKNOWN_COST_INPUTS = (
    "accepted_check_definition missing",
    "price_source missing",
    "allocation_basis missing",
    "usage missing",
    "authority missing",
    "price_source.id missing",
    "usage.model_calls missing",
)
# Any import of a provider, network or subprocess entry point is refused inside the command.
GUARDED_RUN = """
import runpy, socket, subprocess, sys

def refuse(*args, **kwargs):
    raise AssertionError("network or subprocess attempted")

socket.socket.connect = refuse
subprocess.Popen = refuse
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""


def observation(role: str, n: int, arm: str, **over: Any) -> dict[str, Any]:
    chat = arm == "chat"
    base: dict[str, Any] = dict(
        participant=f"{role}-{n}",
        task="t1",
        role=role,
        arm=arm,
        completed=chat,
        comprehension_correct=chat,
        accepted=True,
        hazard_missed=False,
        elapsed_seconds=60.0 if chat else 100.0,
        review_seconds=20.0,
    )
    base.update(over)
    return base


def favourable() -> list[dict[str, Any]]:
    return [
        observation(role, n, arm) for role in ROLES for n in range(2) for arm in ("cards", "chat")
    ]


def envelope(rows: Any, schema: str = SCHEMA) -> dict[str, Any]:
    return dict(schema=schema, observations=rows)


class Command(unittest.TestCase):
    tmp: Path
    default: subprocess.CompletedProcess[str]
    opted_in: subprocess.CompletedProcess[str]
    input_bytes: bytes
    record: Path

    @classmethod
    def setUpClass(cls) -> None:
        holder = tempfile.TemporaryDirectory()
        cls.addClassCleanup(holder.cleanup)
        cls.tmp = Path(holder.name)
        cls.input_bytes = json.dumps(envelope(favourable())).encode()
        path = cls.tmp / "favourable.json"
        path.write_bytes(cls.input_bytes)
        cls.record = cls.tmp / "recorded.json"
        cls.default = cls.run_command("--homes", "100")
        cls.opted_in = cls.run_command(
            "--homes", "100", OPTION, str(path), "--record", str(cls.record)
        )

    @classmethod
    def run_command(cls, *args: str, guarded: bool = False) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ, PYTHONPATH=PYTHONPATH, ZF_DATA=str(cls.tmp / "absent" / "zf.json"))
        argv = [sys.executable, *(["-c", GUARDED_RUN] if guarded else []), str(SCRIPT), *args]
        return subprocess.run(argv, capture_output=True, text=True, env=env, check=False)

    def submit(self, payload: bytes, *extra: str) -> subprocess.CompletedProcess[str]:
        path = self.tmp / "submitted.json"
        path.write_bytes(payload)
        return self.run_command("--homes", "100", OPTION, str(path), *extra)

    def section(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        done = self.submit(json.dumps(envelope(rows)).encode())
        self.assertEqual(done.returncode, 0, done.stderr)
        section: dict[str, Any] = json.loads(done.stdout)[SECTION]
        return section

    def refused(self, payload: bytes, fragment: str) -> None:
        done = self.submit(payload)
        self.assertEqual(done.returncode, 1, done.stderr)
        self.assertEqual(done.stdout, "")
        self.assertIn(fragment, done.stderr)

    def test_baseline_option_is_a_recognised_argument(self) -> None:
        self.assertEqual(self.opted_in.returncode, 0, self.opted_in.stderr)

    def test_supplied_observations_reach_the_real_scorer_and_the_emitted_report(self) -> None:
        section = json.loads(self.opted_in.stdout)[SECTION]
        direct = evaluate_paired_trial(
            favourable(), thresholds=None, cost_inputs=None, now=datetime(2026, 11, 10, tzinfo=UTC)
        )
        self.assertEqual(section["result"], json.loads(json.dumps(direct)))
        result = section["result"]
        self.assertEqual((result["status"], result["pairs"]), ("measured", 6))
        self.assertEqual(result["per_role"]["repairs"]["completion_gain"], 1.0)
        self.assertEqual(result["hazard_misses"]["status"], "no_misses_observed")

    def test_input_identity_and_qualification_are_reported(self) -> None:
        section = json.loads(self.opted_in.stdout)[SECTION]
        self.assertEqual(section["schema"], SCHEMA)
        self.assertEqual(
            section["input"],
            dict(
                sha256=hashlib.sha256(self.input_bytes).hexdigest(),
                bytes=len(self.input_bytes),
                observations=12,
            ),
        )
        text = section["qualification"]
        for phrase in (
            "caller-declared constructed",
            "unverified",
            "not a staff trial",
            "not human acceptance",
            "not owner-agreed",
        ):
            self.assertIn(phrase, text)

    def test_favourable_constructed_result_is_unknown_cost_and_cards_only(self) -> None:
        result = json.loads(self.opted_in.stdout)[SECTION]["result"]
        self.assertEqual(result["ship_recommendation"], "cards_only")
        self.assertEqual(result["threshold"]["status"], "unset_pending_owner_agreement")
        self.assertIsNone(result["threshold"]["value"])
        economics = result["economics"]
        self.assertEqual(economics["ai_cost_per_accepted_check"], "Unknown")
        for missing in UNKNOWN_COST_INPUTS:
            self.assertIn(missing, economics["missing_inputs"])
        self.assertIn("no owner-agreed thresholds recorded", result["reasons"])

    def test_existing_report_content_is_unchanged_and_not_merged(self) -> None:
        plain = json.loads(self.default.stdout)
        report = json.loads(self.opted_in.stdout)
        self.assertNotIn(SECTION, plain)
        del report[SECTION]
        self.assertEqual(report, plain)
        self.assertEqual(plain["comparison"]["status"], "not_evaluated")
        self.assertEqual(plain["not_evaluated"]["staff_comprehension"]["status"], "not_evaluated")

    def test_record_writes_only_the_explicit_destination_with_the_printed_report(self) -> None:
        self.assertEqual(self.record.read_text(), self.opted_in.stdout)
        self.assertEqual(self.default.returncode, 0)

    def test_empty_input_is_not_evaluated(self) -> None:
        result = self.section([])["result"]
        self.assertEqual((result["status"], result["pairs"]), ("not_evaluated", 0))
        self.assertEqual(result["ship_recommendation"], "cards_only")
        self.assertEqual(result["hazard_misses"]["status"], "not_evaluated")

    def test_partial_roles_leave_absent_roles_not_evaluated(self) -> None:
        rows = [observation("repairs", 0, arm) for arm in ("cards", "chat")]
        result = self.section(rows)["result"]
        self.assertEqual(result["pairs"], 1)
        self.assertEqual(result["per_role"]["housing"], dict(pairs=0, status="not_evaluated"))
        self.assertEqual(result["per_role"]["repairs"]["pairs"], 1)

    def test_unpaired_rows_are_reported_and_block_value(self) -> None:
        rows = [observation("housing", 0, "chat")]
        result = self.section(rows)["result"]
        self.assertEqual(result["unpaired"], ["housing-0/t1"])
        self.assertEqual(result["status"], "not_evaluated")
        self.assertIn(
            "invalid or unpaired observations excluded; trial must be repaired", result["reasons"]
        )

    def test_critical_chat_hazard_miss_is_reported(self) -> None:
        rows = favourable()
        rows[1]["hazard_missed"] = True
        result = self.section(rows)["result"]
        hazard = result["hazard_misses"]
        self.assertEqual(
            (hazard["status"], hazard["misses"], hazard["failure_severity"]),
            ("failed", 1, "critical"),
        )
        self.assertEqual(hazard["failed_case_ids"], ["repairs-0/t1"])
        self.assertIn("a chat hazard miss is critical", result["reasons"])

    def test_supplied_acceptance_is_only_counted_under_the_constructed_qualification(self) -> None:
        section = self.section(favourable())
        self.assertEqual(section["result"]["economics"]["accepted_checks"], 6)
        self.assertIn("not human acceptance", section["qualification"])

    def test_missing_unreadable_and_non_regular_inputs_are_refused(self) -> None:
        done = self.run_command(OPTION, str(self.tmp / "none.json"))
        self.assertEqual((done.returncode, done.stdout), (1, ""))
        self.assertIn("cannot read", done.stderr)
        done = self.run_command(OPTION, str(self.tmp))
        self.assertEqual((done.returncode, done.stdout), (1, ""))
        self.assertIn("regular file", done.stderr)

    def test_oversize_input_is_refused_by_size(self) -> None:
        self.refused(b" " * (256 * 1024 + 1), "larger than 262144 bytes")

    def test_malformed_and_non_finite_json_is_refused(self) -> None:
        self.refused(b"{", "not valid JSON")
        self.refused(b"\xff", "not valid UTF-8")
        self.refused(b'{"schema": "x"} trailing', "not valid JSON")
        self.refused(b"[" * 100_000, "too deeply nested")
        base = json.dumps(envelope([observation("repairs", 0, "cards")]))
        self.refused(base.replace("100.0", "NaN").encode(), "non-finite")
        self.refused(base.replace("100.0", "Infinity").encode(), "non-finite")
        self.refused(base.replace("100.0", "1e999").encode(), "elapsed_seconds exceeds")
        self.refused(base.replace("100.0", "1" + "0" * 400).encode(), "elapsed_seconds exceeds")
        self.refused(b'{"schema": "a", "schema": "b", "observations": []}', "duplicate key")

    def test_wrong_envelope_is_refused(self) -> None:
        self.refused(
            json.dumps(envelope([], "constructed-paired-observations-v2")).encode(), "schema"
        )
        self.refused(b"[]", "JSON object")
        self.refused(json.dumps(dict(schema=SCHEMA)).encode(), "exactly the keys")
        self.refused(
            json.dumps(dict(envelope([]), thresholds=dict(owner="x"))).encode(), "exactly the keys"
        )
        self.refused(json.dumps(envelope({"a": 1})).encode(), "observations must be a list")
        self.refused(json.dumps(envelope([1])).encode(), "observation 0 must be an object")
        too_many = [observation("repairs", n, "cards") for n in range(1001)]
        self.refused(json.dumps(envelope(too_many)).encode(), "more than 1000 observations")

    def test_wrong_observation_fields_are_refused_with_the_index(self) -> None:
        good = observation("repairs", 0, "cards")
        for bad, fragment in (
            ({**good, "price": 1}, "exactly the keys"),
            ({k: v for k, v in good.items() if k != "task"}, "exactly the keys"),
            ({**good, "role": "finance"}, "role not repairs, housing or grants"),
            ({**good, "arm": "both"}, "arm not cards or chat"),
            ({**good, "accepted": 1}, "accepted not recorded as true or false"),
            ({**good, "elapsed_seconds": True}, "elapsed_seconds"),
            ({**good, "review_seconds": -1}, "review_seconds"),
            ({**good, "participant": "Ada Lovelace"}, "participant must be a pseudonymous id"),
            ({**good, "participant": "ada@example.org"}, "participant must be a pseudonymous id"),
            ({**good, "task": "t" * 65}, "task must be a pseudonymous id"),
            ({**good, "participant": 7}, "participant must be a pseudonymous id"),
        ):
            with self.subTest(fragment=fragment):
                self.refused(json.dumps(envelope([good, bad])).encode(), "observation 1")
                self.refused(json.dumps(envelope([bad])).encode(), fragment)

    def test_refusal_happens_before_any_record_write(self) -> None:
        target = self.tmp / "must-not-exist.json"
        done = self.submit(b"{", "--record", str(target))
        self.assertEqual(done.returncode, 1)
        self.assertFalse(target.exists())

    def test_command_makes_no_network_or_subprocess_call_and_reads_no_data_store(self) -> None:
        path = self.tmp / "guarded.json"
        path.write_bytes(self.input_bytes)
        done = self.run_command("--homes", "100", OPTION, str(path), guarded=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        report = json.loads(done.stdout)
        self.assertEqual(report["evidence"]["provider"], "offline-extractive; zero model calls")
        self.assertEqual(report["comparison"]["economics"]["execution"]["model_calls"], 0)
        self.assertFalse((self.tmp / "absent").exists())


if __name__ == "__main__":
    unittest.main()
