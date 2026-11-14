import copy
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core import perspective_walkthroughs as pw
from zava_forward.core import profile_journey_contract as pjc

ROOT = Path(__file__).resolve().parents[3]


def good() -> dict[str, Any]:
    step = dict(
        record_ids=["EX-HOME-646"],
        state_text="Unknown: eligibility needs an owner",
        keyboard_operable=True,
        announcement="Eligibility unknown, owner shown",
    )
    return dict(
        perspective="asset-investment",
        steps={e: dict(step) for e in pjc.ELEMENTS} | {"handoff": dict(step, owner="Asset lead")},
    )


class ProfileJourneyContractTests(unittest.TestCase):
    def test_complete_record_is_never_accepted(self) -> None:
        rec = pjc.validate(good())
        self.assertEqual(rec["blockers"], [])
        self.assertFalse(rec["accepted"])
        self.assertIn("not user validation", rec["notice"])

    def test_each_contract_failure_is_a_blocker(self) -> None:
        w = copy.deepcopy(good())
        del w["steps"]["recovery"]
        w["steps"]["entry"]["record_ids"] = [" "]
        w["steps"]["evidence"]["state_text"] = "green"
        w["steps"]["safe_endpoint"]["keyboard_operable"] = False
        w["steps"]["handoff"]["announcement"] = ""
        w["steps"]["handoff"]["owner"] = ""
        self.assertEqual(
            set(pjc.validate(w)["blockers"]),
            {
                "asset-investment.recovery:missing",
                "asset-investment.entry:no_linked_records",
                "asset-investment.evidence:state_not_textual",
                "asset-investment.safe_endpoint:not_keyboard_operable",
                "asset-investment.handoff:no_status_announcement",
                "asset-investment.handoff:no_accountable_owner",
            },
        )

    def test_gaps_cover_all_perspectives_and_match_register(self) -> None:
        g = pjc.gaps(ROOT)
        self.assertEqual(set(g), set(pw.register()))
        self.assertEqual(g["provider-contractor"]["unmet"], ["handoff"])
        self.assertIn("evidence", g["finance-grants"]["not_probed"])


if __name__ == "__main__":
    unittest.main()
