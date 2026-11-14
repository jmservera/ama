"""Ranking read endpoints stamp the policy version and never mutate the archive (Refs #79)."""

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core import ranking, ranking_publication

from test_role_matrix import QualityMatrix

PM = "pam"


def archive_state(folder: str) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(Path(folder).glob("*"))}


class RankingReadRegression(QualityMatrix):
    test_quality_http_controls = None  # type: ignore[assignment]  # inherited fixture test is not part of this slice

    def archive(self) -> str:
        path: str = self.store._ranking_archive()
        return path

    def test_snapshot_read_is_stamped_and_byte_stable(self) -> None:
        code, first = self.call(PM, "/api/ranking/snapshot")
        self.assertEqual(code, 200)
        self.assertEqual(
            (first["policy_version"], first["policy_hash"]),
            (ranking.CURRENT["version"], ranking.CURRENT["content_hash"]),
        )
        ids = [e["id"] for e in first["entries"]]
        open_cases = [c for c in self.store.cases.values() if not c["closed"]]
        want = [e["id"] for e in ranking.rank(open_cases, ranking.CURRENT)]
        self.assertEqual(ids, want)
        _, second = self.call(PM, "/api/ranking/snapshot")
        self.assertEqual(ranking.canonical(first), ranking.canonical(second))
        _, pinned = self.call(PM, "/api/ranking/snapshot?policy=" + ranking.POLICY_V1["version"])
        self.assertEqual(pinned["policy_version"], ranking.POLICY_V1["version"])

    def test_unknown_policy_version_is_refused_without_a_write(self) -> None:
        code, _ = self.call(PM, "/api/ranking/snapshot?policy=9.9.9")
        self.assertEqual(code, 400)
        self.assertFalse(Path(self.archive()).exists())

    def test_publication_status_reads_change_nothing(self) -> None:
        code, published = self.call(PM, "/api/ranking/publish", {})
        self.assertEqual((code, published["written"]), (200, True))
        files = archive_state(self.archive())
        cases = copy.deepcopy(self.store.cases)
        audit = list(self.store.audit_entries())
        self.assertEqual(len(files), 1)
        for _ in range(3):
            code, status = self.call(PM, "/api/ranking/publication")
            self.assertEqual((code, status["count"], status["problems"]), (200, 1, []))
        self.assertEqual(archive_state(self.archive()), files)
        self.assertEqual(self.store.cases, cases)
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_archived_record_keeps_the_stamped_version(self) -> None:
        self.call(PM, "/api/ranking/publish", {})
        (name,) = archive_state(self.archive())
        record = json.loads((Path(self.archive()) / name).read_text(encoding="utf-8"))
        self.assertEqual(record["snapshot"]["policy_version"], ranking.CURRENT["version"])
        self.assertEqual(record["snapshot"]["policy_hash"], ranking.CURRENT["content_hash"])
        before = archive_state(self.archive())
        stripped: dict[str, Any] = {}
        problems: list[str] = ranking_publication.verify(self.archive(), stripped)["problems"]
        self.assertEqual(len(problems), 1)
        self.assertEqual(archive_state(self.archive()), before)


if __name__ == "__main__":
    unittest.main()
