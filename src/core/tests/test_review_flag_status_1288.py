"""Quality review flag status precedence (issue 1288).

Local engineering evidence: a constructed task and a pure call of `review_flag`, with no store and
no model provider. It proves which states may be an autonomous flag, not real model behaviour.
"""

import unittest
from collections.abc import Callable
from typing import Any

from zava_forward.core import assistants, sensor_view

READING: dict[str, Any] = dict(
    sensor_id="sensor-1",
    reading_id="r-1",
    observed_at="2026-11-28T07:00:00Z",
    temperature_c=19.5,
    humidity_pct=64.0,
)
KEY = sensor_view.key_of(READING)
review_flag: Callable[..., dict[str, Any] | None] = assistants.review_flag


def task(
    *,
    state: str = "ready",
    trigger: str = "proactive",
    cites: tuple[str, ...] = (KEY,),
    sensors: dict[str, Any] | None = None,
    source: str = "ai",
    outcome: str = "returned",
    capability: str = "quality-evidence",
    output: bool = True,
) -> dict[str, Any]:
    return dict(
        capability=capability,
        state=state,
        envelope=dict(
            source=source,
            outcome=outcome,
            provider="mock",
            deployment="d",
            model="m",
            task_version="v1",
        ),
        output=dict(findings=[dict(citations=list(cites))]) if output else None,
        dispatch=dict(trigger=trigger),
        snapshot=dict(sources=dict(sensors=dict(readings=[READING], **(sensors or {})))),
        release="rel-1",
        created_at=1_795_000_000,
    )


class ReviewFlagStatus(unittest.TestCase):
    def status(self, **kwargs: Any) -> dict[str, Any]:
        flag = review_flag(task(**kwargs))
        assert flag is not None
        return flag

    def test_only_a_returned_model_quality_output_can_be_a_flag(self) -> None:
        for kwargs in (
            dict(source="rules"),
            dict(outcome="unavailable"),
            dict(capability="other"),
            dict(output=False),
        ):
            with self.subTest(kwargs=kwargs):
                self.assertIsNone(review_flag(task(**kwargs)))

    def test_a_current_proactive_cited_finding_is_the_one_autonomous_flag(self) -> None:
        flag = self.status()
        self.assertEqual(flag["status"], "review-suggested")
        self.assertEqual(
            (flag["level"], flag["autonomous"], flag["unapproved"]), ("L4", True, True)
        )
        self.assertEqual(flag["sensor_cited_ids"], [KEY])
        self.assertEqual(flag["readings"][0]["reading_id"], "r-1")
        self.assertEqual(flag["model"]["release"], "rel-1")

    def test_every_other_state_is_named_and_never_autonomous(self) -> None:
        conflict = dict(conflicting_readings=[dict(citation_key=KEY)])
        impossible = dict(implausible_readings=[dict(sensor_id="sensor-1", citation_key=KEY)])
        cases: list[tuple[str, dict[str, Any]]] = [
            ("manual-proposal", dict(trigger="requested")),
            ("uncited", dict(cites=("doc:1",))),
            ("not-current", dict(state="stale")),
            ("conflicting-readings", dict(sensors=conflict)),
            ("implausible-readings", dict(sensors=impossible)),
            ("conflicting-readings", dict(sensors=dict(conflict, **impossible))),
            ("rejected", dict(state="rejected", sensors=conflict)),
            ("reviewed", dict(state="accepted", sensors=impossible)),
        ]
        for expected, kwargs in cases:
            with self.subTest(expected=expected, kwargs=kwargs):
                flag = self.status(**kwargs)
                self.assertEqual(flag["status"], expected)
                self.assertIs(flag["autonomous"], False)
                self.assertIsNone(flag["level"])
                self.assertIs(flag["unapproved"], True)

    def test_a_task_that_is_no_longer_actionable_is_not_current(self) -> None:
        flag = review_flag(task(), actionable=False)
        assert flag is not None
        self.assertEqual(flag["status"], "not-current")
        self.assertIs(flag["autonomous"], False)

    def test_withheld_consent_hides_readings_and_findings(self) -> None:
        flag = review_flag(task(), withheld=True)
        assert flag is not None
        self.assertEqual(flag["status"], "withheld")
        self.assertIs(flag["autonomous"], False)
        self.assertNotIn("readings", flag)
        self.assertNotIn("cited_ids", flag)


if __name__ == "__main__":
    unittest.main()
