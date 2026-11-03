import unittest
from typing import Any

from zava_forward.core import job_pack
from zava_forward.core.quality import checklist_for

ORDER = dict(
    id="WO-1",
    package="PKG-1",
    case_id="C-1",
    address="1 Test Road",
    postcode="TE1 1ST",
    measures="Loft insulation",
    needs_notice=True,
    named_contact="Sam Example",
    state="Appointed",
    version=2,
    scope="Loft top-up to 300mm",
    scope_version=3,
)
CASE = dict(
    technical=dict(design_version=4),
    resident=dict(reason="uses oxygen at night", health="asthma"),
    notes=["private note"],
)
ITEMS = checklist_for("Loft insulation")["items"]
NOTES = {label: f"  seen: {label}  " for label in ITEMS}
WORKER = dict(name="Kim Builder", email="kim@example.test")


def receipt(pack: dict[str, Any] | None = None, **over: Any) -> dict[str, Any]:
    pack = pack or job_pack.build_job_pack(ORDER, CASE)
    args: dict[str, Any] = dict(
        measure="Loft insulation",
        notes=NOTES,
        confirmed_by="Kim Builder",
        confirmed=True,
        capture_ref="ref-1",
        captured_at="2026-11-03T10:00:00Z",
        recorded_by=dict(name="Sam Example"),
    )
    args.update(over)
    return job_pack.worker_receipt(pack, **args)


class JobPackTests(unittest.TestCase):
    def test_pack_has_scope_design_contact_and_no_private_detail(self) -> None:
        pack = job_pack.build_job_pack(ORDER, CASE)
        self.assertEqual(pack["design_version"], 4)
        self.assertEqual(pack["named_contact"], "Sam Example")
        self.assertEqual(pack["access"], job_pack.ACCESS_NOTICE)
        self.assertTrue(pack["ready"])
        blob = str(pack).lower()
        for secret in ("oxygen", "asthma", "private note", "vulnerab"):
            self.assertNotIn(secret, blob)

    def test_pack_not_ready_without_design_scope_or_appointment(self) -> None:
        for order, case in (
            (ORDER, dict(technical={})),
            (dict(ORDER, measures="Unknown (resident scope confirmation needed)"), CASE),
            (dict(ORDER, state="Issued"), CASE),
        ):
            pack = job_pack.build_job_pack(order, case)
            self.assertFalse(pack["ready"])
            self.assertIn("do not start work", pack["not_ready_reason"])

    def test_pack_digest_changes_with_scope_or_design(self) -> None:
        base = job_pack.build_job_pack(ORDER, CASE)["pack_digest"]
        self.assertNotEqual(
            base, job_pack.build_job_pack(dict(ORDER, scope_version=4), CASE)["pack_digest"]
        )
        self.assertNotEqual(
            base,
            job_pack.build_job_pack(ORDER, dict(technical=dict(design_version=5)))["pack_digest"],
        )

    def test_receipt_keeps_original_notes_and_is_not_accepted(self) -> None:
        r = receipt()
        self.assertEqual(r["original_notes"], {label: NOTES[label] for label in ITEMS})
        self.assertEqual(r["checklist_version"], checklist_for("Loft insulation")["version"])
        self.assertFalse(r["accepted"])
        self.assertEqual(r["review_state"], job_pack.NOT_REVIEWED)

    def test_receipt_needs_confirmation_every_check_and_known_measure(self) -> None:
        with self.assertRaises(ValueError):
            receipt(confirmed=False)
        with self.assertRaises(ValueError):
            receipt(notes={ITEMS[0]: "only one"})
        with self.assertRaises(ValueError):
            receipt(measure="Heat pump")
        with self.assertRaises(ValueError):
            receipt(mode="fax")

    def test_acknowledgement_is_not_acceptance(self) -> None:
        r = job_pack.acknowledge_receipt(
            receipt(), dict(name="Sam Example"), "2026-11-03T11:00:00Z"
        )
        self.assertEqual(r["status"], job_pack.ACKNOWLEDGED)
        self.assertFalse(r["accepted"])
        self.assertEqual(r["review_state"], job_pack.NOT_REVIEWED)

    def test_no_self_approval(self) -> None:
        r = job_pack.acknowledge_receipt(receipt(), dict(name="Ann Ack", code="PS-1"), "t")
        for who in (dict(name="kim builder"), dict(name="Sam Example"), dict(code="ps-1")):
            self.assertIn("Independent review", job_pack.review_blocker(r, who) or "")
        self.assertIsNone(
            job_pack.review_blocker(r, dict(name="Quin Inspect", email="quin@example.test"))
        )
        self.assertIn("named", job_pack.review_blocker(r, {}) or "")

    def test_offline_merge_keeps_originals_and_flags_duplicates_and_stale(self) -> None:
        pack = job_pack.build_job_pack(ORDER, CASE)
        offline = receipt(pack, capture_ref="off-1", mode="offline")
        stale = receipt(
            job_pack.build_job_pack(dict(ORDER, scope_version=2), CASE),
            capture_ref="off-2",
            mode="offline",
        )
        out = job_pack.merge_offline(
            [receipt(pack)], [offline, offline, stale], pack["pack_digest"]
        )
        self.assertEqual([r["capture_ref"] for r in out["new"]], ["off-1"])
        self.assertEqual(len(out["duplicate"]), 1)
        self.assertEqual(out["held_for_review"][0]["capture_ref"], "off-2")
        self.assertEqual(out["new"][0]["original_notes"], offline["original_notes"])
        again = job_pack.merge_offline(out["new"], [offline], pack["pack_digest"])
        self.assertEqual(len(again["duplicate"]), 1)

    def test_provider_no_show_is_not_resident_refusal(self) -> None:
        for event in job_pack.NO_SHOW_EVENTS:
            out = job_pack.visit_recovery(event)
            self.assertIs(out["resident_refusal"], False)
            self.assertIn("No change", out["resident_effect"])
            self.assertNotIn("refus", (out["outcome"] + out["cause"]).lower())
        self.assertEqual(job_pack.visit_recovery("provider no-show")["outcome"], "Rebooking needed")
        with self.assertRaises(ValueError):
            job_pack.visit_recovery("resident refused")

    def test_escalation_reaches_named_owner_and_is_no_instruction(self) -> None:
        e = job_pack.escalation(
            "variation",
            "Extra 20m2 of loft",
            "Kim Builder",
            "WO-1",
            "Pam Lead",
            "Retrofit Programme Manager",
        )
        self.assertIs(e["contract_instruction"], False)
        self.assertEqual(e["owner"]["name"], "Pam Lead")
        self.assertIn("new version", e["note"])
        with self.assertRaises(ValueError):
            job_pack.escalation("variation", "x", "Kim", "WO-1", "", "Retrofit Programme Manager")
        with self.assertRaises(ValueError):
            job_pack.escalation("variation", "x", "Kim", "WO-1", "Kim", "Contractor")
        with self.assertRaises(ValueError):
            job_pack.escalation("order", "x", "Kim", "WO-1", "Pam", "Retrofit Programme Manager")


if __name__ == "__main__":
    unittest.main()
