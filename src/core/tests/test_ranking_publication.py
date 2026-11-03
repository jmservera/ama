"""Retained ranking snapshot publication (Refs #79)."""
import json
import tempfile
import unittest
from pathlib import Path

from dataset import case
from zava_forward.core import ranking
from zava_forward.core import ranking_publication as rp

AS_OF = "2026-10-09"


def snap():
    a, b = case("ZF-A"), case("ZF-B")
    b["days_in_stage"] = 50
    return ranking.snapshot([a, b], ranking.POLICY_V1, AS_OF)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name) / "archive"

    def test_publish_is_dated_idempotent_and_verifies(self):
        first = rp.publish(snap(), self.dir, "2026-10-10")
        self.assertTrue(first["written"])
        again = rp.publish(snap(), self.dir, "2026-10-11")
        self.assertFalse(again["written"])
        self.assertEqual((again["path"], again["published_on"]), (first["path"], "2026-10-10"))
        self.assertEqual(len(list(self.dir.iterdir())), 1)
        self.assertEqual(rp.verify(self.dir), dict(count=1, problems=[], latest="2026-10-10"))

    def test_edited_record_is_reported_and_not_overwritten(self):
        path = Path(rp.publish(snap(), self.dir, "2026-10-10")["path"])
        rec = json.loads(path.read_text())
        rec["snapshot"]["entries"].reverse()
        path.write_text(json.dumps(rec))
        want = [f"{path.name}: content does not match its snapshot hash."]
        self.assertEqual(rp.verify(self.dir)["problems"], want)
        self.assertFalse(rp.publish(snap(), self.dir, "2026-10-12")["written"])

    def test_unknown_policy_hash_and_unreadable_files_are_reported(self):
        s = snap()
        s["policy_hash"] = "0" * 64
        s["snapshot_hash"] = rp.snapshot_hash(s)
        rp.publish(s, self.dir, "2026-10-10")
        (self.dir / "ranking-bad.json").write_text("{")
        probs = rp.verify(self.dir)["problems"]
        self.assertEqual(len(probs), 2)
        self.assertTrue(any("policy registry" in p for p in probs))
        self.assertTrue(any("unreadable" in p for p in probs))

    def test_refuses_tampered_snapshot_and_bad_date(self):
        s = snap()
        s["total"] = 99
        with self.assertRaises(rp.PublicationError):
            rp.publish(s, self.dir, "2026-10-10")
        with self.assertRaises(rp.PublicationError):
            rp.publish(snap(), self.dir, "10/10/2026")
        self.assertFalse(self.dir.exists())

    def test_overdue_reports_missing_and_stale_publication(self):
        self.assertTrue(rp.overdue(self.dir, "2026-10-10"))
        rp.publish(snap(), self.dir, "2026-10-10")
        self.assertFalse(rp.overdue(self.dir, "2026-10-10"))
        self.assertTrue(rp.overdue(self.dir, "2026-10-11"))

    def test_schedule_states_what_is_not_decided(self):
        self.assertEqual(rp.SCHEDULE["owner"], "to be named")
        self.assertIn("not set", rp.SCHEDULE["retention"])

    def test_module_has_no_clock_and_no_delete(self):
        src = Path(rp.__file__).read_text()
        for word in ("datetime", "import time", "os.remove", "unlink", "rmtree"):
            self.assertNotIn(word, src)


if __name__ == "__main__":
    unittest.main()
