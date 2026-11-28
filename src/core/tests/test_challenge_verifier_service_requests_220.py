"""Issue #220 verifier tests for the service-request growth path and residual guard branches.

``resident_decisions`` calls ``assert_no_adverse_challenge_effects`` with
``allowed_case_keys=("service_requests",)`` when a dispute or service request is opened or its
response is reopened. These cases prove that path permits only a new request and refuses any
dropped, replaced or closed unrelated request, and that nested adverse keys, non-challenge case
fields and corrupted hazard lists are refused, so a challenge cannot retaliate, infer refusal or
delay a hazard response.
"""

from __future__ import annotations

import copy
import unittest
from collections.abc import Callable
from typing import Any

from zava_forward.core.challenges import (
    ChallengeSafeguardError,
    assert_no_adverse_challenge_effects,
)

Case = dict[str, Any]
SERVICE_KEYS = ("service_requests",)


def _before() -> Case:
    return {
        "id": "ZF-220-SR",
        "score": 80,
        "service_requests": [
            {"id": "SR-1", "status": "Open"},
            {"id": "SR-2", "status": "Closed"},
        ],
        "hazards": [
            {
                "id": "HZ-1",
                "released": False,
                "aware_at": "2026-11-15T08:00:00Z",
                "hold": {"status": "Active"},
            }
        ],
    }


def _guard(before: Case, after: Case, **kwargs: Any) -> None:
    assert_no_adverse_challenge_effects(before, after, allowed_case_keys=SERVICE_KEYS, **kwargs)


class ServiceRequestGrowthPathTests(unittest.TestCase):
    def test_new_request_is_allowed_but_only_when_service_requests_are_permitted(self) -> None:
        before = _before()
        after = copy.deepcopy(before)
        after["service_requests"].append({"id": "SR-3", "status": "Open"})
        _guard(before, after)
        with self.assertRaisesRegex(ChallengeSafeguardError, "service_requests"):
            assert_no_adverse_challenge_effects(before, after)

    def test_already_closed_request_may_stay_closed(self) -> None:
        before = _before()
        after = copy.deepcopy(before)
        after["service_requests"][1]["status"] = " closed "
        _guard(before, after)

    def test_dropped_replaced_or_closed_unrelated_request_is_refused(self) -> None:
        def dropped(case: Case) -> None:
            case["service_requests"].pop()

        def not_a_list(case: Case) -> None:
            case["service_requests"] = None

        def replaced(case: Case) -> None:
            case["service_requests"][0] = {"id": "SR-9", "status": "Open"}

        def closed(case: Case) -> None:
            case["service_requests"][0]["status"] = "Cancelled"

        expected: list[tuple[str, Callable[[Case], None], str]] = [
            ("dropped", dropped, "dropped an existing service request"),
            ("not_a_list", not_a_list, "dropped an existing service request"),
            ("replaced", replaced, "removed existing service request 'SR-1'"),
            ("closed", closed, "closed unrelated service request 'SR-1'"),
        ]
        for label, mutate, message in expected:
            with self.subTest(label):
                after = _before()
                mutate(after)
                with self.assertRaisesRegex(ChallengeSafeguardError, message):
                    _guard(_before(), after)


class ResidualGuardBranchTests(unittest.TestCase):
    def test_nested_adverse_key_inside_a_permitted_key_is_refused(self) -> None:
        before = _before()
        after = copy.deepcopy(before)
        after["service_requests"].append(
            {"id": "SR-3", "status": "Open", "detail": [{"Hazard-Pause": True}]}
        )
        with self.assertRaisesRegex(ChallengeSafeguardError, "Case service_requests"):
            _guard(before, after)

    def test_top_level_adverse_field_added_or_altered_is_refused(self) -> None:
        before = _before()
        added = copy.deepcopy(before)
        added["Retaliation Flag"] = False
        with self.assertRaisesRegex(ChallengeSafeguardError, "added forbidden"):
            _guard(before, added)

        flagged = _before()
        flagged["refusal"] = False
        altered = copy.deepcopy(flagged)
        altered["refusal"] = True
        with self.assertRaisesRegex(ChallengeSafeguardError, "introduced or altered"):
            _guard(flagged, altered)

    def test_unrelated_case_field_change_is_refused(self) -> None:
        before = _before()
        after = copy.deepcopy(before)
        after["notes"] = "added during a challenge"
        with self.assertRaisesRegex(ChallengeSafeguardError, "non-challenge case field 'notes'"):
            _guard(before, after)

    def test_corrupted_hazard_list_is_refused_when_routing_a_new_hazard(self) -> None:
        for label, hazards in (("none", None), ("tuple", ())):
            with self.subTest(label):
                before = _before()
                after = copy.deepcopy(before)
                after["hazards"] = hazards
                with self.assertRaisesRegex(ChallengeSafeguardError, "removed or corrupted"):
                    _guard(before, after, allow_new_independent_hazard=True)


if __name__ == "__main__":
    unittest.main()
