"""Per-task data contracts: declared for every AI task, enforced before a prompt (#2311)."""

import string
import unittest

from zava_forward.core import ai_prompts, ai_registry, task_contracts


class TaskContractTests(unittest.TestCase):
    def test_every_registered_task_declares_a_complete_contract(self) -> None:
        tasks = ai_registry.tasks()  # type: ignore[no-untyped-call]
        self.assertEqual(set(task_contracts.CONTRACTS), set(tasks))
        for task_id in tasks:
            contract = ai_registry.data_contract(task_id)  # type: ignore[no-untyped-call]
            self.assertIsNotNone(contract, task_id)
            for key in ("purpose", "audience", "fields", "prohibited_content", "minimum_necessary"):
                self.assertTrue(contract[key], f"{task_id}.{key}")
            for spec in contract["fields"].values():
                self.assertIn(spec["type"], ("str", "int"))
                self.assertGreater(spec["max_length"], 0)

    def test_every_retained_prompt_field_is_declared(self) -> None:
        for task_id, (system, user) in ai_prompts.PROMPTS.items():
            declared = set(task_contracts.CONTRACTS[task_id]["fields"])
            used = {
                name
                for text in (system, user)
                for _, name, _, _ in string.Formatter().parse(text)
                if name
            }
            self.assertLessEqual(used, declared, task_id)

    def test_undeclared_field_is_refused(self) -> None:
        with self.assertRaisesRegex(task_contracts.ContractRefusal, "not declared"):
            ai_prompts.render("briefing", facts="Stage: Survey", resident_notes="x")

    def test_prohibited_content_is_refused_without_echo(self) -> None:
        with self.assertRaises(task_contracts.ContractRefusal) as caught:
            ai_prompts.render("briefing", facts="Call the resident on 07700 900123")
        self.assertIn("telephone number", str(caught.exception))
        self.assertNotIn("900123", str(caught.exception))
        for text in ("jo@example.org", "AB 12 34 56 C", "sort code 12-34-56"):
            with self.assertRaises(task_contracts.ContractRefusal):
                ai_prompts.render("briefing", facts=text)

    def test_type_and_length_are_enforced(self) -> None:
        with self.assertRaises(task_contracts.ContractRefusal):
            ai_prompts.render("briefing", facts="x" * 30001)
        with self.assertRaises(task_contracts.ContractRefusal):
            ai_prompts.render("priority", n="3", facts="Stage: Survey")

    def test_user_permission_alone_does_not_satisfy_the_contract(self) -> None:
        with self.assertRaises(task_contracts.ContractRefusal):
            task_contracts.enforce(
                "briefing", dict(facts="Email jo@example.org"), user_permission=True
            )
        with self.assertRaises(task_contracts.ContractRefusal):
            task_contracts.enforce("briefing", dict(facts="ok", extra="x"), user_permission=True)

    def test_declared_clean_build_still_renders(self) -> None:
        system, prompt = ai_prompts.render("priority", n=3, facts="CASE-1: Stage: Survey booked")
        self.assertIn("top 3", prompt)
        self.assertTrue(system)

    def test_contract_does_not_claim_approval(self) -> None:
        for contract in task_contracts.CONTRACTS.values():
            self.assertIn("not claimed", contract["approval_claim"])
            self.assertIn("#121", contract["approval_claim"])


if __name__ == "__main__":
    unittest.main()
