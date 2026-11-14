"""Tie-break, policy-version stamping and read-only archive verification (Refs #79).

Regression evidence only. Cases carry no UPRN in this model, so the fixed tie-break is the case id;
the shared home address below stands in for a shared property.
"""

import copy
import itertools
import os
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from dataset import case
from zava_forward.core import ranking
from zava_forward.core import ranking_publication as rp

AS_OF = "2026-10-09"
PUBLISHED_ON = "2026-10-10"


def tied_cases() -> list[dict[str, Any]]:
    cases = []
    for cid in ("ZF-C", "ZF-A", "ZF-D", "ZF-B"):
        c = case(cid)
        c["home"]["address"] = "1 Shared Road"
        cases.append(c)
    return cases


def second_policy() -> dict[str, Any]:
    p: dict[str, Any] = copy.deepcopy(ranking.POLICY_V1)
    p.update(version="2.0.0", effective_date="2026-12-01")
    p["content_hash"] = ranking.policy_hash(p)
    return p


def tree(folder: Path) -> dict[str, tuple[bytes, int]]:
    return {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in sorted(folder.iterdir())}


class TieBreakTests(unittest.TestCase):
    def test_equal_keys_order_by_case_id_for_every_input_order(self) -> None:
        want = ["ZF-A", "ZF-B", "ZF-C", "ZF-D"]
        golden = ranking.canonical(ranking.snapshot(tied_cases(), ranking.POLICY_V1, AS_OF))
        for perm in itertools.permutations(tied_cases()):
            cases = list(perm)
            ranked = ranking.rank(cases, ranking.POLICY_V1)
            self.assertEqual([e["id"] for e in ranked], want)
            self.assertEqual([e["rank"] for e in ranked], [1, 2, 3, 4])
            snap = ranking.snapshot(cases, ranking.POLICY_V1, AS_OF)
            self.assertEqual(ranking.canonical(snap), golden)

    def test_tied_rows_are_decided_by_case_id(self) -> None:
        snap = ranking.snapshot(tied_cases(), ranking.POLICY_V1, AS_OF)
        self.assertEqual(
            [e["deciding_rule"] for e in snap["entries"]],
            [None, "case_id", "case_id", "case_id"],
        )

    def test_sql_key_order_matches_rank_for_ties(self) -> None:
        cases = tied_cases()
        by_key = sorted(cases, key=lambda c: ranking.sql_key(c, ranking.POLICY_V1))
        ranked = ranking.rank(cases, ranking.POLICY_V1)
        self.assertEqual([c["id"] for c in by_key], [e["id"] for e in ranked])

    def test_ranking_does_not_mutate_its_input(self) -> None:
        cases = tied_cases()
        before = copy.deepcopy(cases)
        ranking.rank(cases, ranking.POLICY_V1)
        ranking.snapshot(cases, ranking.POLICY_V1, AS_OF)
        self.assertEqual(cases, before)


class PolicyVersionStampTests(unittest.TestCase):
    def test_entries_and_snapshot_carry_the_policy_that_ranked_them(self) -> None:
        v2 = second_policy()
        for policy in (ranking.POLICY_V1, v2):
            ranked = ranking.rank(tied_cases(), policy)
            self.assertEqual({e["policy_version"] for e in ranked}, {policy["version"]})
            snap = ranking.snapshot(tied_cases(), policy, AS_OF)
            self.assertEqual(
                (snap["policy_id"], snap["policy_version"], snap["policy_hash"]),
                (policy["policy_id"], policy["version"], policy["content_hash"]),
            )
        self.assertNotEqual(
            ranking.snapshot(tied_cases(), v2, AS_OF)["snapshot_hash"],
            ranking.snapshot(tied_cases(), ranking.POLICY_V1, AS_OF)["snapshot_hash"],
        )

    def test_a_newer_policy_leaves_the_v1_result_byte_identical(self) -> None:
        before = ranking.canonical(ranking.snapshot(tied_cases(), ranking.POLICY_V1, AS_OF))
        ranking.snapshot(tied_cases(), second_policy(), AS_OF)
        after = ranking.canonical(ranking.snapshot(tied_cases(), ranking.POLICY_V1, AS_OF))
        self.assertEqual(before, after)


class ReadOnlyArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.archive = self.root / "ranking-archive"
        snap = ranking.snapshot(tied_cases(), ranking.POLICY_V1, AS_OF)
        self.assertTrue(rp.publish(snap, self.archive, PUBLISHED_ON)["written"])

    def verify(self, registry: Mapping[str, Any] | None = None) -> dict[str, Any]:
        before = tree(self.archive)
        out = rp.verify(self.archive, registry)
        self.assertEqual(tree(self.archive), before)
        return out

    def test_verify_confirms_the_stamped_version_without_writing(self) -> None:
        for _ in range(2):
            out = self.verify()
            self.assertEqual((out["count"], out["problems"], out["latest"]), (1, [], PUBLISHED_ON))

    def test_registry_without_the_stamped_version_is_a_problem_not_a_write(self) -> None:
        out = self.verify({"2.0.0": second_policy()})
        self.assertEqual(out["count"], 1)
        self.assertEqual(len(out["problems"]), 1)
        self.assertIn("policy version or hash is not in the policy registry", out["problems"][0])

    def test_registry_with_a_different_hash_is_a_problem_not_a_write(self) -> None:
        forged = copy.deepcopy(ranking.POLICY_V1)
        forged["content_hash"] = "0" * 64
        out = self.verify({ranking.POLICY_V1["version"]: forged})
        self.assertEqual(len(out["problems"]), 1)

    def test_absent_archive_reads_empty_and_is_not_created(self) -> None:
        missing = self.root / "never-published"
        out = rp.verify(missing)
        self.assertEqual((out["count"], out["problems"], out["latest"]), (0, [], None))
        self.assertFalse(os.path.exists(missing))


if __name__ == "__main__":
    unittest.main()
