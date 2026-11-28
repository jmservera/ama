"""Retained prompt text keeps the recommend-only bound for every AI task (Refs #104)."""

from __future__ import annotations

import re
import unittest
from unittest import mock

from zava_forward.core import ai_prompts

FACT_BOUND_TASKS = ("message", "summary", "briefing", "priority", "funding_draft", "read_document")
NOT_SENT_TASKS = ("message", "summary")


def system(task: str) -> str:
    return ai_prompts.PROMPTS[task][0]


class PromptBounds(unittest.TestCase):
    def test_every_registered_task_is_covered_by_this_suite(self) -> None:
        self.assertEqual(sorted(ai_prompts.PROMPTS), sorted(FACT_BOUND_TASKS))

    def test_every_task_restricts_the_model_to_supplied_facts(self) -> None:
        for task in FACT_BOUND_TASKS:
            text = system(task).lower()
            self.assertTrue(
                "use only the facts" in text or "do not guess" in text,
                f"{task} must bind the model to the facts given",
            )

    def test_every_task_forbids_inventing_content(self) -> None:
        for task in FACT_BOUND_TASKS:
            text = system(task).lower()
            self.assertRegex(text, r"never invent|do not invent|no invented|do not guess", task)

    def test_text_tasks_never_claim_anything_was_sent(self) -> None:
        for task in NOT_SENT_TASKS:
            self.assertIn("never say anything has been sent", system(task).lower(), task)

    def test_no_prompt_instructs_the_model_to_decide_approve_or_act(self) -> None:
        acting = re.compile(
            r"\b(you (will|must) )?(approve|execute|send|decide|book|submit)\b", re.I
        )
        for task in FACT_BOUND_TASKS:
            for sentence in re.split(r"(?<=[.!?])\s+", system(task)):
                if not acting.search(sentence):
                    continue
                self.assertRegex(
                    sentence,
                    r"(?i)never|do not|a person decides|not been sent",
                    f"{task}: {sentence!r}",
                )

    def test_priority_prompt_keeps_the_human_decision_and_safety_rules(self) -> None:
        text = system("priority")
        self.assertIn("only recommend; a person decides", text)
        self.assertIn("only the case ids", text)
        self.assertIn("open safety issue", text)
        self.assertIn("cites", text)


class PromptVersion(unittest.TestCase):
    def test_version_is_deterministic_short_hex_and_distinct_per_task(self) -> None:
        versions = {task: ai_prompts.version(task) for task in ai_prompts.PROMPTS}
        for task, value in versions.items():
            self.assertRegex(value, r"^[0-9a-f]{16}$", task)
            self.assertEqual(ai_prompts.version(task), value)
        self.assertEqual(len(set(versions.values())), len(versions))

    def test_any_change_to_prompt_or_citation_text_changes_that_version(self) -> None:
        original = ai_prompts.version("priority")
        system_text, user_text = ai_prompts.PROMPTS["priority"]
        for edited in ((system_text + " ", user_text), (system_text, user_text + " ")):
            with mock.patch.dict(ai_prompts.PROMPTS, {"priority": edited}):
                self.assertNotEqual(ai_prompts.version("priority"), original)
        with mock.patch.object(ai_prompts, "CITATION_RULE", ai_prompts.CITATION_RULE + ("x",)):
            self.assertNotEqual(ai_prompts.version("priority"), original)
        self.assertEqual(ai_prompts.version("priority"), original)


if __name__ == "__main__":
    unittest.main()
