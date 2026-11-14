"""Issue #217: AI features are registered completely and unregistered ones fail closed."""

import unittest
from typing import Any
from unittest import mock

from zava_forward.core import ai_registry as untyped_registry
from zava_forward.core.ai import Ai as UntypedAi

ai_registry: Any = untyped_registry
Ai: Any = UntypedAi


class RegisterCompleteness(unittest.TestCase):
    def test_every_feature_carries_the_required_fields(self) -> None:
        tasks = ai_registry.tasks()
        self.assertTrue(tasks)
        for task_id, entry in tasks.items():
            with self.subTest(task=task_id):
                self.assertEqual(ai_registry.missing_fields(entry), [])
                self.assertTrue(entry["owner"].strip())
                self.assertTrue(ai_registry.is_registered(task_id))

    def test_incomplete_entry_is_reported(self) -> None:
        entry = dict(ai_registry.tasks()["summary"], owner="", limits=[])
        self.assertEqual(ai_registry.missing_fields(entry), ["limits", "owner"])
        with mock.patch.object(ai_registry, "get", return_value=entry):
            self.assertFalse(ai_registry.is_registered("summary"))
            with self.assertRaises(ai_registry.UnregisteredFeature):
                ai_registry.require_registered("summary")


class UnregisteredFailsClosed(unittest.TestCase):
    def test_unknown_or_malformed_names_are_not_registered(self) -> None:
        for name in ("not-a-feature", "", None, 7):
            with self.subTest(name=name):
                self.assertFalse(ai_registry.is_registered(name))
                with self.assertRaises(ai_registry.UnregisteredFeature):
                    ai_registry.require_registered(name)

    def test_run_of_unregistered_feature_makes_no_model_call(self) -> None:
        ai = Ai()
        ai.endpoint = "https://provider.invalid"
        with (
            mock.patch("urllib.request.urlopen") as sent,
            mock.patch.object(Ai, "_chat") as chat,
        ):
            out = ai.run("not-a-feature", "sys", "user", "TEMPLATE")
        sent.assert_not_called()
        chat.assert_not_called()
        self.assertEqual(
            (out["source"], out["text"], out["registered"]), ("template", "TEMPLATE", False)
        )
        self.assertIn("not registered", out["reason"])


if __name__ == "__main__":
    unittest.main()
