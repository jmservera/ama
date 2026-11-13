"""Identity fields never carry free text or secret-shaped values (#107, #432)."""

from __future__ import annotations

import unittest
from typing import Any

from zava_forward.core import ai_consumption, assistants

TASK: dict[str, Any] = dict(
    capability="c", version="v", case_id="k", source_signature="s", snapshot={}
)
LIMITS = assistants.Limits({})
UNVERIFIED = "unverified-identity"
SECRETS = (
    "sk-SENTINEL0123456789",
    "abcsk-SENTINEL0123456789",
    "SK-SENTINEL0123456789",
    "line one\nsk-SENTINEL0123456789",
    "Bearer SENTINEL0123456789",
    "raw case text with spaces",
    " leading",
    "tab\tvalue",
)
ACCEPTED = (
    "trusted-proxy",
    "scripted",
    "local-test-double",
    "azure-openai",
    "password",
    "offline-extractive; zero model calls",
    "test",
    "capable",
    "d",
    "standard",
    "test-model",
    "offline-extractive",
    "none",
    "synthetic",
    "m1",
    "m-1",
    "m",
    "live",
    "other-model",
    "model-id",
    "unattested",
    "gpt-4o-2024-08-06",
    "task-fast",
    "risk-model",
    "gpt-4o-mask-v1",
)


def shaped(**fields: Any) -> dict[str, Any]:
    result = dict(
        outcome="returned",
        source="ai",
        usage=None,
        text=None,
        provider="p",
        deployment="d",
        model="m",
    )
    result.update(fields)
    return assistants.shape_result(TASK, result, LIMITS)[0]


class IdentityFields(unittest.TestCase):
    def test_secret_shaped_values_are_replaced_in_every_field(self) -> None:
        for field in ("provider", "deployment", "model"):
            for value in SECRETS:
                with self.subTest(field=field, value=value):
                    self.assertEqual(shaped(**{field: value})[field], UNVERIFIED)

    def test_accepted_values_are_preserved_byte_for_byte(self) -> None:
        for field in ("provider", "deployment", "model"):
            for value in ACCEPTED:
                with self.subTest(field=field, value=value):
                    self.assertEqual(shaped(**{field: value})[field], value)

    def test_type_and_length_edges(self) -> None:
        class Sub(str):
            pass

        for field in ("provider", "deployment", "model"):
            self.assertIsNone(shaped(**{field: Sub("m")})[field])
            self.assertIsNone(shaped(**{field: 7})[field])
            self.assertIsNone(shaped(**{field: None})[field])
        for field in ("provider", "deployment"):
            self.assertEqual(shaped(**{field: "a" * 120})[field], "a" * 120)
            self.assertEqual(shaped(**{field: "a" * 121})[field], "a" * 120)
        self.assertEqual(shaped(model="a" * 512)["model"], "a" * 512)
        self.assertIsNone(shaped(model="a" * 513)["model"])

    def test_bounded_model_is_the_shared_ledger_boundary(self) -> None:
        self.assertEqual(ai_consumption.bounded_model("sk-SENTINEL0123456789"), UNVERIFIED)
        self.assertEqual(ai_consumption.bounded_model("a\nb"), UNVERIFIED)
        self.assertEqual(ai_consumption.bounded_model("m-1"), "m-1")

    def test_post_back_envelope_is_sanitised(self) -> None:
        raw = dict(
            provider="sk-SENTINEL0123456789",
            deployment="a b",
            model="x\ny",
            outcome="returned",
            source="ai",
        )
        clean = assistants.sanitize_identity(raw)
        self.assertEqual(
            (clean["provider"], clean["deployment"], clean["model"]), (UNVERIFIED,) * 3
        )
        self.assertEqual(raw["provider"], "sk-SENTINEL0123456789")


if __name__ == "__main__":
    unittest.main()
