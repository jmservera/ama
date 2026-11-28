"""Pure unit tests of the AC-070 gate and scripted panels (no Store, no model)."""

import unittest
from typing import Any

from zava_forward.agents import review_effectiveness as re_

LABELS = ["Extra support: Large print", "Contact: phone", "Contact: phone"]
SOURCE = "Extra support: Large print"
TASK = "demo-task"


def _proposal(
    defect: str = "mismatch", asserted: str = "Braille", confident: bool = True
) -> dict[str, Any]:
    return dict(
        id="P",
        defect=defect,
        confident=confident,
        claims=[dict(topic="Extra support", asserted=asserted, cite=SOURCE)],
    )


def _record(
    action: str = "edit",
    reason: str = f"mismatch: Extra support {re_.SOURCE_TAG}{SOURCE}]",
    text: str | None = "Extra support is Large print",
    status: str = "Reviewed",
    reviewer: str = "reviewer-a",
) -> dict[str, Any]:
    return dict(
        status=status,
        task=TASK,
        reviewer_action=action,
        reviewer_reason=reason,
        override_text=text,
        verified=True,
        review_evidence=dict(reviewer=reviewer, source_hashes=["h1"]),
    )


def _gate(
    prop: dict[str, Any],
    rec: dict[str, Any],
    authority: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    return re_.gate_satisfied(prop, rec, LABELS, re_._facts(LABELS), [], authority)


class GateUnitTests(unittest.TestCase):
    def test_defect_edited_with_source_and_effective_text_passes(self) -> None:
        self.assertTrue(_gate(_proposal(), _record())[0])

    def test_unreviewed_or_unattributed_record_never_passes(self) -> None:
        self.assertEqual(
            _gate(_proposal(), _record(status="Not reviewed"))[1], "no recorded human review"
        )
        rec = _record()
        rec["review_evidence"] = None
        self.assertFalse(_gate(_proposal(), rec)[0])

    def test_reason_naming_another_resolving_label_is_refused(self) -> None:
        rec = _record(reason=f"mismatch: Contact {re_.SOURCE_TAG}Contact: phone]")
        ok, why = _gate(_proposal(), rec)
        self.assertFalse(ok)
        self.assertIn("seeded discrepancy", why)

    def test_reason_without_a_source_tag_is_refused(self) -> None:
        ok, why = _gate(_proposal(), _record(reason="looks wrong"))
        self.assertFalse(ok)
        self.assertIn("resolves in the case", why)

    def test_correct_control_rejected_or_altered_is_refused(self) -> None:
        control = _proposal(defect="", asserted="Large print")
        self.assertEqual(
            _gate(control, _record(action="reject", text=None))[1], "correct control rejected"
        )
        altered = _record(action="edit", text="Extra support is Braille")
        self.assertFalse(_gate(control, altered)[0])
        self.assertTrue(_gate(control, _record(action="accept", reason="", text=None))[0])

    def test_authority_must_cover_reviewer_and_task(self) -> None:
        authority: dict[str, Any] = dict(
            authorised_reviewers=["reviewer-a"], task=TASK, required_evidence=["reviewer"]
        )
        self.assertTrue(_gate(_proposal(), _record(), authority)[0])
        self.assertIn(
            "no defined authority", _gate(_proposal(), _record(reviewer="x"), authority)[1]
        )
        wrong_task = dict(authority, task="other")
        self.assertIn("task", _gate(_proposal(), _record(), wrong_task)[1])

    def test_control_is_exempt_from_a_required_source_reason(self) -> None:
        authority: dict[str, Any] = dict(
            authorised_reviewers=["reviewer-a"], task=TASK, required_evidence=["source_reason"]
        )
        control = _proposal(defect="", asserted="Large print")
        accepted = _record(action="accept", reason="", text=None)
        self.assertTrue(_gate(control, accepted, authority)[0])
        self.assertIn("source_reason", _gate(_proposal(), _record(reason="x"), authority)[1])


class PanelAndLabelUnitTests(unittest.TestCase):
    def test_repeated_labels_become_detail_aliases_with_a_citable_origin(self) -> None:
        facts = re_._facts(LABELS)
        self.assertEqual(facts["Contact detail"], "phone")
        self.assertEqual(re_._origin("Contact detail detail"), "Contact")
        self.assertEqual(re_._origin("detail"), "detail")

    def test_automation_bias_trusts_confident_verified_output_only(self) -> None:
        facts = re_._facts(LABELS)
        rec = _record()
        self.assertEqual(re_.automation_bias(_proposal(), facts, rec, [])[0], "accept")
        hedged = re_.automation_bias(_proposal(confident=False), facts, rec, [])
        self.assertEqual(hedged[0], "edit")
        self.assertIn(SOURCE, hedged[1])

    def test_over_reject_cites_a_resolving_label_yet_rejects_everything(self) -> None:
        facts = re_._facts(LABELS)
        action, reason, text, _ = re_.over_reject(_proposal(), facts, _record(), [])
        self.assertEqual((action, text), ("reject", None))
        self.assertIn(f"{re_.SOURCE_TAG}Extra support: Large print]", reason)


if __name__ == "__main__":
    unittest.main()
