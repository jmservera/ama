import unittest

from properwarm.domain import Rejected, Store


def fresh():
    s = Store()
    s.add_case("C1")
    return s


class TransitionRules(unittest.TestCase):
    def test_agent_and_service_roles_cannot_transition(self):
        for role in ("agent", "orchestrator", "importer"):
            with self.assertRaises(Rejected) as ctx:
                fresh().transition("svc", role, "C1", "assessment", 1, "k")
            self.assertEqual(ctx.exception.code, "forbidden_role")

    def test_human_moves_ungated_stage_and_version_increments(self):
        s = fresh()
        c = s.transition("ann", "coordinator", "C1", "assessment", 1, "k1")
        self.assertEqual((c.stage, c.version), ("assessment", 2))

    def test_stage_skipping_rejected(self):
        with self.assertRaises(Rejected) as ctx:
            fresh().transition("ann", "coordinator", "C1", "installation", 1, "k")
        self.assertEqual(ctx.exception.code, "invalid_transition")

    def test_gated_stage_needs_second_human(self):
        s = fresh()
        s.transition("ann", "coordinator", "C1", "assessment", 1, "k1")
        for approver in (None, "ann"):
            with self.assertRaises(Rejected) as ctx:
                s.transition("ann", "assessor", "C1", "design_ready", 2, "k2", approver)
            self.assertEqual(ctx.exception.code, "approval_required")
        self.assertEqual(s.transition("ann", "assessor", "C1", "design_ready", 2, "k3", "bob").stage, "design_ready")

    def test_optimistic_concurrency(self):
        s = fresh()
        s.transition("ann", "coordinator", "C1", "assessment", 1, "k1")
        with self.assertRaises(Rejected) as ctx:
            s.transition("bob", "coordinator", "C1", "design_ready", 1, "k2", "ann")
        self.assertEqual(ctx.exception.code, "version_conflict")

    def test_idempotent_replay_does_not_double_apply(self):
        s = fresh()
        a = s.transition("ann", "coordinator", "C1", "assessment", 1, "same")
        b = s.transition("ann", "coordinator", "C1", "assessment", 1, "same")
        self.assertIs(a, b)
        self.assertEqual(s.cases["C1"].version, 2)
        self.assertEqual(len([r for r in s.audit if r["event"] == "case.transitioned"]), 1)


class ProposalRules(unittest.TestCase):
    good = {"task": "summarise", "case_id": "C1", "summary": "Survey incomplete", "citations": ["doc:survey-1"]}

    def test_agent_proposal_stored_but_state_unchanged(self):
        s = fresh()
        p = s.submit_proposal("agent-id", "agent", self.good)
        self.assertEqual(p.status, "pending")
        self.assertEqual(s.cases["C1"].stage, "new")

    def test_proposal_without_citation_or_with_transition_field_rejected(self):
        s = fresh()
        for bad, code in (({**self.good, "citations": []}, "missing_citation"),
                          ({**self.good, "to_stage": "closed"}, "forbidden_field"),
                          ({**self.good, "task": "approve_case"}, "invalid_task")):
            with self.assertRaises(Rejected) as ctx:
                s.submit_proposal("agent-id", "agent", bad)
            self.assertEqual(ctx.exception.code, code)

    def test_accepting_a_proposal_never_advances_the_case(self):
        s = fresh()
        p = s.submit_proposal("agent-id", "agent", self.good)
        s.decide_proposal("ann", "coordinator", p.proposal_id, True)
        self.assertEqual(s.cases["C1"].stage, "new")
        with self.assertRaises(Rejected):
            s.decide_proposal("agent-id", "agent", p.proposal_id, True)

    def test_only_agent_submits(self):
        with self.assertRaises(Rejected):
            fresh().submit_proposal("ann", "coordinator", self.good)


class AuditChain(unittest.TestCase):
    def test_tampering_is_detected(self):
        s = fresh()
        s.transition("ann", "coordinator", "C1", "assessment", 1, "k")
        self.assertTrue(s.verify_audit())
        s.audit[1]["actor"] = "mallory"
        self.assertFalse(s.verify_audit())


if __name__ == "__main__":
    unittest.main()
