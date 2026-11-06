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

    def test_malformed_archived_publication_date_is_a_problem_and_not_latest(self):
        good = Path(rp.publish(snap(), self.dir, "2026-10-10")["path"])
        s2 = snap()
        s2["as_of"] = "2026-10-08"
        s2["snapshot_hash"] = rp.snapshot_hash(s2)
        bad = Path(rp.publish(s2, self.dir, "2026-10-11")["path"])
        odd = ("2026-10-11\n", "\u0662\u0660\u0662\u0666-\u0661\u0660-\u0661\u0661")
        for value in ("2026-11-31", "20261011", "", None, 20261011, ["2026-10-11"], *odd):
            with self.subTest(value=value):
                rec = json.loads(bad.read_text())
                rec["published_on"] = value
                bad.write_text(json.dumps(rec))
                res = rp.verify(self.dir)
                self.assertEqual(
                    res["problems"], [f"{bad.name}: publication date is not a valid calendar date."]
                )
                self.assertEqual((res["count"], res["latest"]), (2, "2026-10-10"))
        self.assertTrue(good.exists())

    def test_only_malformed_dates_leave_no_trusted_latest(self):
        path = Path(rp.publish(snap(), self.dir, "2026-10-10")["path"])
        rec = json.loads(path.read_text())
        rec["published_on"] = "2026-11-31"
        path.write_text(json.dumps(rec))
        self.assertIsNone(rp.verify(self.dir)["latest"])
        self.assertTrue(rp.overdue(self.dir, "2026-10-10"))

    def test_publish_refuses_impossible_calendar_date_before_writing(self):
        odd = ("2026-10-10\n", "\u0662\u0660\u0662\u0666-\u0661\u0660-\u0661\u0660")
        for value in ("2026-11-31", "2026-02-29", "2026-13-01", "0000-01-01", *odd):
            with self.subTest(value=value), self.assertRaises(rp.PublicationError):
                rp.publish(snap(), self.dir, value)
        self.assertFalse(self.dir.exists())

    def test_schedule_states_what_is_not_decided(self):
        self.assertEqual(rp.SCHEDULE["owner"], "to be named")
        self.assertIn("not set", rp.SCHEDULE["retention"])

    def test_module_has_no_clock_and_no_delete(self):
        src = Path(rp.__file__).read_text()
        for word in ("datetime", "import time", "os.remove", "unlink", "rmtree"):
            self.assertNotIn(word, src)


if __name__ == "__main__":
    unittest.main()


class SignoffTests(unittest.TestCase):
    def signed(self):
        p = json.loads(json.dumps(ranking.POLICY_V1))
        p["owner"] = "Dana Example"
        p["signoff"] = dict(
            signed_by="Dana Example",
            signed_on="2026-11-05",
            rule_order_hash=ranking.rule_order_hash(p),
        )
        return p

    def test_draft_policy_is_not_signed_and_says_why(self):
        self.assertFalse(ranking.is_signed(ranking.POLICY_V1))
        self.assertEqual(ranking.signoff_problems(ranking.POLICY_V1), ["No named policy owner."])

    def test_named_owner_without_record_is_not_signed(self):
        p = self.signed()
        del p["signoff"]
        self.assertEqual(ranking.signoff_problems(p), ["No recorded sign-off of the rule order."])

    def test_complete_signoff_is_signed(self):
        self.assertTrue(ranking.is_signed(self.signed()))

    def test_signoff_by_someone_else_or_undated_is_refused(self):
        p = self.signed()
        p["signoff"].update(signed_by="Someone Else", signed_on="soon")
        self.assertEqual(len(ranking.signoff_problems(p)), 2)

    def test_changing_rule_order_voids_signoff(self):
        p = self.signed()
        p["rules"] = list(reversed(p["rules"]))
        self.assertEqual(ranking.signoff_problems(p), ["Sign-off does not match this rule order."])
        q = self.signed()
        q["stage_order"] = list(reversed(q["stage_order"]))
        self.assertFalse(ranking.is_signed(q))

    def test_status_reports_unsigned_reasons_without_changing_ranking(self):
        before = ranking.canonical(ranking.rank([case("ZF-A")]))
        self.assertFalse(ranking.is_signed(ranking.CURRENT))
        self.assertEqual(ranking.canonical(ranking.rank([case("ZF-A")])), before)
