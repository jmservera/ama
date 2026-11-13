"""Failing-first tests for the scheduled ranking publication job (Refs #79, criterion 4).

The transport is the in-memory Blob mock (ranking_blob_fixture), not an emulator or an account.
The signed policy copy exists only inside the tests; the shipped policy stays an unsigned draft.
"""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from dataset import case as dataset_case
from ranking_blob_fixture import SAS, URL, FakeBlobContainer
from zava_forward.core import ranking
from zava_forward.core import ranking_archive_blob as rab
from zava_forward.core import ranking_publication as rp
from zava_forward.core.store import Store

from zava_forward.orchestrator import ranking_publish as job

DAY1, DAY2 = "2026-11-05", "2026-11-06"
SELECTOR_ENV = {
    "ZF_RANKING_ARCHIVE": "azure-blob",
    "ZF_BLOB_ACCOUNT_URL": URL,
    "ZF_RANKING_BLOB_CONTAINER": "ranking-archive",
    "ZF_BLOB_SAS": SAS,
}


def case(cid: str, days: int, closed: bool) -> dict[str, Any]:
    c: dict[str, Any] = dataset_case(cid)
    c.update(days_in_stage=days, closed=closed)
    return c


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


class JobBase(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "zavaforward.json"
        path.write_text(
            json.dumps(
                {
                    "as_of": DAY1,
                    "staff": [],
                    "cases": [
                        case("ZF-A", 3, False),
                        case("ZF-B", 50, False),
                        case("ZF-C", 9, True),
                    ],
                }
            )
        )
        self.store = Store(str(path))
        self.fake = FakeBlobContainer()
        self.archive = rab.BlobRankingArchive(
            URL, "ranking-archive", sas=SAS, transport=self.fake, env={}
        )
        self.lines: list[str] = []

    def go(self, today: str = DAY1, **kw: Any) -> int:
        kw.setdefault("registry", signed_registry())
        return job.main(
            ["--today", today],
            env=SELECTOR_ENV,
            store=self.store,
            archive=self.archive,
            out=self.lines.append,
            **kw,
        )

    def text(self) -> str:
        return "\n".join(self.lines)


class ScheduledPublicationTests(JobBase):
    def test_publishes_open_cases_to_blob_once_and_repeat_keeps_the_retained_bytes(self) -> None:
        self.assertEqual(self.go(), 0)
        self.assertIn("RANKING_PUBLISH_OK status=published", self.text())
        (name,) = self.fake.blobs
        first = self.fake.blobs[name]
        record = json.loads(first)
        self.assertEqual(record["published_on"], DAY1)
        self.assertEqual(sorted(e["id"] for e in record["snapshot"]["entries"]), ["ZF-A", "ZF-B"])
        self.lines.clear()
        self.assertEqual(self.go(), 0)
        self.assertIn("RANKING_PUBLISH_OK status=already_published", self.text())
        self.assertEqual(self.fake.blobs, {name: first})

    def test_next_day_with_unchanged_data_keeps_record_and_raises_stale_source_alert(self) -> None:
        self.assertEqual(self.go(DAY1), 0)
        (name,) = self.fake.blobs
        first = self.fake.blobs[name]
        self.lines.clear()
        self.assertEqual(self.go(DAY2), 1)
        self.assertIn("RANKING_PUBLISH_ALERT", self.text())
        self.assertIn("not current", self.text())
        self.assertEqual(self.fake.blobs, {name: first})

    def test_shipped_unsigned_draft_policy_publishes_nothing_and_stays_unsigned(self) -> None:
        code = job.main(
            ["--today", DAY1],
            env=SELECTOR_ENV,
            store=self.store,
            archive=self.archive,
            out=self.lines.append,
        )
        self.assertEqual(code, 1)
        self.assertIn("RANKING_PUBLISH_BLOCKED", self.text())
        self.assertIn("approval_missing", self.text())
        self.assertEqual(self.fake.blobs, {})
        self.assertFalse(ranking.is_signed(ranking.CURRENT))

    def test_blob_is_never_replaced_by_a_folder_and_missing_configuration_is_refused(self) -> None:
        code = job.main(["--today", DAY1], env={}, store=self.store, out=self.lines.append)
        self.assertEqual(code, 2)
        self.assertIn("ZF_RANKING_ARCHIVE=azure-blob", self.text())
        self.assertNotIn("RANKING_PUBLISH_OK", self.text())

    def test_blob_selected_without_account_or_container_is_refused_not_folder_fallback(
        self,
    ) -> None:
        env = {"ZF_RANKING_ARCHIVE": "azure-blob"}
        code = job.main(["--today", DAY1], env=env, store=self.store, out=self.lines.append)
        self.assertEqual(code, 2)
        self.assertEqual(self.fake.blobs, {})

    def test_bad_date_is_refused_and_writes_nothing(self) -> None:
        self.assertEqual(self.go("not-a-date"), 1)
        self.assertEqual(self.fake.blobs, {})

    def test_failure_reports_the_exception_type_only(self) -> None:
        self.fake.put_faults.append("unreachable")
        self.assertEqual(self.go(), 1)
        self.assertIn("RANKING_PUBLISH_ALERT", self.text())
        for secret in ("SENTINEL-SAS-SECRET", "acct.blob.core.windows.net"):
            self.assertNotIn(secret, self.text())
        self.assertEqual(self.fake.blobs, {})
        self.lines.clear()
        self.assertEqual(self.go(), 0)
        self.assertEqual(len(self.fake.blobs), 1)

    def test_non_boolean_closed_flag_refuses_the_whole_source(self) -> None:
        self.store.cases["ZF-A"]["closed"] = "no"
        self.assertEqual(self.go(), 1)
        self.assertIn("RANKING_PUBLISH_ALERT", self.text())
        self.assertEqual(self.fake.blobs, {})

    def test_sql_backed_store_selected_by_zf_store_publishes_open_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "zavaforward.json"
            data.write_text(
                json.dumps(
                    {
                        "as_of": DAY1,
                        "staff": [],
                        "cases": [case("ZF-A", 3, False), case("ZF-C", 9, True)],
                    }
                )
            )
            env = {
                **SELECTOR_ENV,
                "ZF_STORE": "sqlite",
                "ZF_DATA": str(data),
                "ZF_STATE": tmp,
                "ZF_AS_OF": DAY1,
            }
            code = job.main(
                ["--today", DAY1],
                env=env,
                archive=self.archive,
                registry=signed_registry(),
                out=self.lines.append,
            )
        self.assertEqual(code, 0)
        self.assertIn("RANKING_PUBLISH_OK status=published", self.text())
        (name,) = self.fake.blobs
        record = json.loads(self.fake.blobs[name])
        self.assertEqual([e["id"] for e in record["snapshot"]["entries"]], ["ZF-A"])

    def test_published_record_verifies_against_the_signed_registry(self) -> None:
        reg = signed_registry()
        self.go(registry=reg)
        self.assertEqual(rp.verify(self.archive, reg)["problems"], [])

    def test_source_has_no_exercise_or_signoff_bypass(self) -> None:
        src = Path(job.__file__).read_text()
        for word in ("exercise=True", "signoff", "os.remove", "unlink", "DELETE"):
            self.assertNotIn(word, src)


if __name__ == "__main__":
    unittest.main()
