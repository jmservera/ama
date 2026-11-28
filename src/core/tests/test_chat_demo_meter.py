import logging
import unittest
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

from zava_forward.core import ai_registry, chat_demo_meter

DEMO_ENV = {
    ai_registry.DEMO_SWITCH: ai_registry.DEMO_ACTIVATION["switch_value"],
    ai_registry.DEMO_PROFILE: ai_registry.DEMO_PROFILE_VALUE,
}
OVERRIDE_ENV = {
    "ZF_DEMO_AI_SUSPENSION_OVERRIDE": "owner-directed-2026-11-23",
    "ZF_DEPLOYMENT_PROFILE": "demo",
}
NOON = datetime(2031, 5, 4, 12, 34, 56, tzinfo=UTC)


class FakeLedger:
    def __init__(self, fail: bool = False) -> None:
        self.prices: list[dict[str, Any]] = []
        self.authorities: list[dict[str, Any]] = []
        self.fail = fail

    def price(self, **kwargs: Any) -> str:
        self.prices.append(kwargs)
        return "price-" + str(kwargs["version"])

    def authorize(self, **kwargs: Any) -> None:
        if self.fail:
            raise ValueError("refused")
        self.authorities.append(kwargs)


class FakeAi:
    fast = "fast-model"
    model_version = "v1"

    def __init__(self, ledger: FakeLedger | None) -> None:
        self.consumption = ledger
        self.synthetic_price_capabilities = frozenset({"other"})

    def configuration(self, model: str, temperature: int, max_tokens: int) -> str:
        return f"{model}|{temperature}|{max_tokens}|abcdefghijklmnop"


def store(ledger: FakeLedger | None) -> Any:
    return SimpleNamespace(ai=FakeAi(ledger))


class ChatDemoMeterTests(unittest.TestCase):
    def test_no_switch_records_nothing_and_clears_the_capability(self) -> None:
        ledger = FakeLedger()
        target = store(ledger)
        target.ai.synthetic_price_capabilities = frozenset({chat_demo_meter.TASK})
        self.assertFalse(chat_demo_meter.ensure(target, 600, {}, NOON))
        self.assertEqual((ledger.prices, ledger.authorities), ([], []))
        self.assertEqual(target.ai.synthetic_price_capabilities, frozenset())

    def test_wrong_profile_or_switch_value_is_denied(self) -> None:
        for env in (
            {**DEMO_ENV, ai_registry.DEMO_PROFILE: "production"},
            {**DEMO_ENV, ai_registry.DEMO_SWITCH: "approved"},
        ):
            ledger = FakeLedger()
            self.assertFalse(chat_demo_meter.ensure(store(ledger), 600, env, NOON))
            self.assertEqual(ledger.authorities, [])

    def test_switch_seeds_one_bounded_synthetic_authority_for_the_hour(self) -> None:
        ledger = FakeLedger()
        target = store(ledger)
        self.assertTrue(chat_demo_meter.ensure(target, 600, DEMO_ENV, NOON))
        (price,), (authority,) = ledger.prices, ledger.authorities
        self.assertTrue(price["synthetic"])
        self.assertEqual(price["start"], "2031-05-04T12:00:00+00:00")
        self.assertEqual(price["end"], "2031-05-04T13:00:00+00:00")
        self.assertEqual((authority["start"], authority["end"]), (price["start"], price["end"]))
        self.assertEqual(authority["capability"], chat_demo_meter.TASK)
        self.assertEqual(authority["max_calls"], 1)
        (budget,) = authority["budgets"]
        self.assertEqual((budget["calls"], budget["tokens"], budget["amount"]), (20, 100000, "1"))
        self.assertIn(chat_demo_meter.TASK, target.ai.synthetic_price_capabilities)
        self.assertIn("other", target.ai.synthetic_price_capabilities)

    def test_same_hour_is_idempotent_and_a_new_hour_seeds_again(self) -> None:
        ledger = FakeLedger()
        target = store(ledger)
        for moment in (NOON, NOON.replace(minute=59), NOON.replace(hour=13)):
            self.assertTrue(chat_demo_meter.ensure(target, 600, DEMO_ENV, moment))
        self.assertEqual(len(ledger.authorities), 2)
        self.assertEqual(ledger.authorities[0]["end"], ledger.authorities[1]["start"])

    def test_a_different_token_limit_is_a_new_configuration(self) -> None:
        ledger = FakeLedger()
        target = store(ledger)
        chat_demo_meter.ensure(target, 600, DEMO_ENV, NOON)
        chat_demo_meter.ensure(target, 800, DEMO_ENV, NOON)
        self.assertEqual(len(ledger.authorities), 2)

    def test_ledger_refusal_is_logged_and_not_cached(self) -> None:
        ledger = FakeLedger(fail=True)
        target = store(ledger)
        with self.assertLogs(chat_demo_meter.__name__, logging.WARNING):
            self.assertFalse(chat_demo_meter.ensure(target, 600, DEMO_ENV, NOON))
        ledger.fail = False
        self.assertTrue(chat_demo_meter.ensure(target, 600, DEMO_ENV, NOON))
        self.assertEqual(len(ledger.authorities), 1)

    def test_a_store_without_a_ledger_is_not_seeded(self) -> None:
        self.assertFalse(chat_demo_meter.ensure(store(None), 600, DEMO_ENV, NOON))

    def test_quality_meter_follows_the_owner_override_only(self) -> None:
        ledger = FakeLedger()
        target = store(ledger)
        self.assertFalse(chat_demo_meter.ensure_quality(target, 600, DEMO_ENV, NOON))
        self.assertEqual(ledger.authorities, [])
        self.assertTrue(chat_demo_meter.ensure_quality(target, 600, OVERRIDE_ENV, NOON))
        (authority,) = ledger.authorities
        self.assertEqual(authority["capability"], chat_demo_meter.QUALITY_TASK)
        self.assertEqual(
            target.ai.synthetic_price_capabilities,
            frozenset({"other", chat_demo_meter.QUALITY_TASK}),
        )


if __name__ == "__main__":
    unittest.main()
