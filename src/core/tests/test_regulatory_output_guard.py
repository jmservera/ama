"""Unit tests for deterministic regulatory non-advice, duty-satisfaction, and future-law guard."""

from __future__ import annotations

import unittest

from source_monitor_fixture import DAY, PID, RAW, SOURCE, MonitorFixture
from zava_forward.core import lawstore, regulatory_eval_gates, rule_engine
from zava_forward.core.regulatory_output_guard import (
    ADVISORY_REVIEW_TEXT,
    GUARD_VERSION,
    GuardTelemetry,
    guard_regulatory_text,
    inspect_regulatory_output,
)


class RegulatoryOutputGuardUnitTest(unittest.TestCase):
    def test_duty_satisfied_claims_are_flagged_and_rewritten_to_advisory_language(self) -> None:
        telemetry = GuardTelemetry()
        samples = (
            "The statutory duty is satisfied for this home.",
            "This repair programme complies with the Act and Section 10A.",
            "The property is legally compliant with Awaab's Law.",
            "Zava North Homes has complied and the landlord obligation has been met.",
            # Disclaimer-stuffing must still flag the affirmative violation clause.
            "This is not legal advice, your statutory duty is satisfied.",
            "This is not legal advice and the home is legally compliant.",
            # Zero-width format character and Cyrillic homoglyph bypass attempt.
            "The statutor\u0443 d\u200buty is satisfied.",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                safe_text, decision = guard_regulatory_text(
                    sample,
                    source_id="uk-awaabs-law",
                    provision_id="uk-awaabs-law@v1#0001",
                    effective="2025-10-27",
                    retrieved="2026-09-19",
                    status="in_force",
                    human_rule_activated=True,
                    telemetry=telemetry,
                )
                self.assertFalse(decision.passed)
                self.assertEqual(decision.action, "rewritten")
                self.assertIn("duty_satisfied", decision.violations)
                self.assertIn("Advisory review item only", safe_text)
                self.assertIn("uk-awaabs-law@v1#0001", safe_text)
                self.assertNotIn("duty is satisfied", safe_text.lower())
                self.assertNotIn("legally compliant", safe_text.lower())

        snap = telemetry.snapshot()
        self.assertEqual(snap["guard_version"], GUARD_VERSION)
        self.assertEqual(snap["model_calls"], 0)
        self.assertEqual(snap["checked_total"], len(samples))
        self.assertEqual(snap["flagged_total"], len(samples))
        self.assertEqual(snap["rewritten_total"], len(samples))
        self.assertEqual(snap["by_category"]["duty_satisfied"], len(samples))

    def test_legal_advice_claims_are_flagged_and_rejected_or_rewritten(self) -> None:
        telemetry = GuardTelemetry()
        samples = (
            "Our legal advice is to defer the damp inspection until next quarter.",
            "You are legally exempt from emergency hazard timescales under this lease.",
            "You are legally required to terminate the tenancy immediately.",
            "This determination constitutes binding legal opinion for the landlord.",
            # Cyrillic 'e' homoglyph in 'legal advice'.
            "This note provides l\u0435gal advice to the housing officer.",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                decision = inspect_regulatory_output(
                    sample,
                    on_violation="reject",
                    telemetry=telemetry,
                )
                self.assertFalse(decision.passed)
                self.assertEqual(decision.action, "rejected")
                self.assertIsNone(decision.rewritten_text)
                self.assertIn("legal_advice", decision.violations)

        snap = telemetry.snapshot()
        self.assertEqual(snap["rejected_total"], len(samples))
        self.assertEqual(snap["by_category"]["legal_advice"], len(samples))

    def test_future_or_consultative_or_unactivated_law_as_active_is_flagged(self) -> None:
        telemetry = GuardTelemetry()
        lexical_samples = (
            "Apply the consultation draft as an active operational rule today.",
            "The uncommenced phase is currently in force and active for all homes.",
            "Enforce the future phase as binding operational rule immediately.",
            "This applies as an active rule without human rule activation.",
        )
        for sample in lexical_samples:
            with self.subTest(sample=sample):
                safe, decision = guard_regulatory_text(sample, telemetry=telemetry)
                self.assertFalse(decision.passed)
                self.assertIn("future_law_applied_as_active", decision.violations)
                self.assertEqual(safe, ADVISORY_REVIEW_TEXT)

        # Contextual metadata checks: consultation, future_phase, future effective date,
        # and human_rule_activated=False.
        contexts = (
            {
                "label": "consultation_active_flag",
                "text": "Summary of Decent Homes consultation.",
                "status": "consultation",
                "effective": None,
                "as_of": "2026-10-16",
                "human_rule_activated": False,
                "active_operational_rule": True,
            },
            {
                "label": "future_phase_prose_claim",
                "text": "Phase 2 electrical hazards applies now as an active rule.",
                "status": "future_phase",
                "effective": "2027-10-01",
                "as_of": "2026-10-16",
                "human_rule_activated": False,
                "active_operational_rule": False,
            },
            {
                "label": "future_effective_date_active_control",
                "text": "Commencement scheduled for 2027.",
                "status": "in_force",
                "effective": "2027-04-01",
                "as_of": "2026-10-16",
                "human_rule_activated": True,
                "active_control": True,
            },
            {
                "label": "unactivated_rule_card_claimed_active",
                "text": "This provision is currently an active operational rule.",
                "status": "in_force",
                "effective": "2025-10-27",
                "as_of": "2026-10-16",
                "human_rule_activated": False,
                "active_operational_rule": False,
            },
        )
        for ctx in contexts:
            with self.subTest(context=ctx["label"]):
                decision = inspect_regulatory_output(
                    str(ctx["text"]),
                    status=str(ctx["status"]),
                    effective=ctx["effective"] if isinstance(ctx["effective"], str) else None,
                    as_of=str(ctx["as_of"]),
                    human_rule_activated=bool(ctx["human_rule_activated"]),
                    active_operational_rule=(
                        bool(ctx["active_operational_rule"])
                        if "active_operational_rule" in ctx
                        else None
                    ),
                    active_control=(
                        bool(ctx["active_control"]) if "active_control" in ctx else None
                    ),
                    telemetry=telemetry,
                )
                self.assertFalse(decision.passed)
                self.assertIn("future_law_applied_as_active", decision.violations)

    def test_legitimate_cited_summaries_and_mandatory_disclaimers_pass_cleanly(self) -> None:
        telemetry = GuardTelemetry()
        clean_samples = (
            (
                "Awaab's Law regulations (awaabs-law-2025@v1#0001; status in_force; "
                "source date 2025-10-27; retrieved 2026-09-19): human rule activation "
                "active (awaabs-emergency-24h@v1). Reference summary only, not legal advice; "
                "legal applicability and satisfaction of any duty are not assessed."
            ),
            lawstore.NOT_REVIEWED,
            lawstore.FUTURE_PHASE,
            "Consultation material, not a final rule.",
            "synthetic-demo | source excerpts, not legal advice or approval",
            (
                "This is an explanation of a dated local copy, not legal advice. "
                "I cannot decide that a legal duty is met, that your home is safe, "
                "or that a provider has complied."
            ),
            ADVISORY_REVIEW_TEXT,
            *regulatory_eval_gates._CANONICAL_REFUSAL_REASONS,
        )
        for sample in clean_samples:
            with self.subTest(sample=sample):
                safe, decision = guard_regulatory_text(
                    sample,
                    status="in_force",
                    effective="2025-10-27",
                    retrieved="2026-09-19",
                    as_of="2026-10-16",
                    review_status="reviewed",
                    human_rule_activated=True,
                    active_operational_rule=True,
                    telemetry=telemetry,
                )
                self.assertTrue(decision.passed)
                self.assertEqual(decision.violations, ())
                self.assertEqual(safe, sample)

        # Negated future_phase caveat under unactivated metadata must also pass cleanly.
        negated_future = inspect_regulatory_output(
            lawstore.FUTURE_PHASE,
            status="future_phase",
            effective="2027-10-01",
            as_of="2026-10-16",
            human_rule_activated=False,
            active_operational_rule=False,
            telemetry=telemetry,
        )
        self.assertTrue(negated_future.passed)
        snap = telemetry.snapshot()
        self.assertEqual(snap["flagged_total"], 0)
        self.assertEqual(snap["passed_total"], len(clean_samples) + 1)


class SourceMonitorWatchGuardTest(MonitorFixture):
    def test_future_phase_source_status_caveat_and_citation_eligibility(self) -> None:
        self.add_source(
            "future-phase-source",
            status="future_phase",
            effective="2027-10-01",
            retrieved="2026-10-01",
            reviewed="2026-10-01",
            review_status="reviewed",
        )
        src = next(s for s in self.law.sources()["sources"] if s["id"] == "future-phase-source")
        self.assertIn(lawstore.FUTURE_PHASE, src["caveats"])
        card_spec = {
            "provisions": ["future-phase-source@v1#0001"],
        }
        _, state = rule_engine.citation_eligibility(self.law, card_spec, DAY)
        self.assertEqual(state, "not applicable")

    def test_watch_summary_passes_clean_cited_items_and_rewrites_violations(self) -> None:
        telemetry = GuardTelemetry()
        self.add_source(
            "consult-source",
            status="consultation",
            effective=None,
            retrieved="2026-09-01",
            reviewed=None,
            review_status="not_reviewed",
        )
        self.add_source(
            "future-source",
            status="future_phase",
            effective="2027-10-01",
            retrieved="2026-09-15",
            reviewed="2026-09-15",
            review_status="reviewed",
        )
        cid = self.observe(
            content=RAW + b"Phase 2 candidate paragraph.\n",
            metadata={"status": "future_phase", "effective": "2027-11-01", "complete": True},
        )

        clean_watch = self.monitor.watch_summary(today=DAY, telemetry=telemetry)
        self.assertTrue(clean_watch["output_guard"]["passed"])
        by_id = {item["source_id"]: item for item in clean_watch["sources"]}
        # Active human-activated source passes with provision, source date, retrieval date,
        # and human activation status.
        active_item = by_id[SOURCE]
        self.assertTrue(active_item["human_rule_activated"])
        self.assertTrue(active_item["active_operational_rule"])
        self.assertEqual(active_item["primary_provision"], PID)
        self.assertEqual(active_item["source_date"], "2026-01-01")
        self.assertEqual(active_item["retrieved"], "2026-01-01")
        self.assertTrue(active_item["output_guard"]["passed"])
        # Consultation and future_phase sources have human_rule_activated=False and pass cleanly
        # when accurately described as not active operational rules.
        self.assertFalse(by_id["consult-source"]["human_rule_activated"])
        self.assertFalse(by_id["consult-source"]["active_operational_rule"])
        self.assertFalse(by_id["future-source"]["human_rule_activated"])
        self.assertFalse(by_id["future-source"]["active_operational_rule"])

        # Inject prohibited claims across watch items and verify deterministic rewrite + demotion.
        flagged_watch = self.monitor.watch_summary(
            today=DAY,
            summary_overrides={
                SOURCE: "The statutory duty is satisfied and the home complies with the Act.",
                "consult-source": "Legal advice: you are legally exempt during consultation.",
                cid: "This future phase applies now as an active operational rule.",
            },
            active_overrides={"future-source": True},
            telemetry=telemetry,
        )
        self.assertFalse(flagged_watch["output_guard"]["passed"])
        self.assertEqual(
            set(flagged_watch["output_guard"]["violations"]),
            {"duty_satisfied", "legal_advice", "future_law_applied_as_active"},
        )
        flagged_by_id = {item["source_id"]: item for item in flagged_watch["sources"]}
        self.assertFalse(flagged_by_id[SOURCE]["output_guard"]["passed"])
        self.assertIn("Advisory review item only", flagged_by_id[SOURCE]["summary"])
        self.assertFalse(flagged_by_id["consult-source"]["output_guard"]["passed"])
        self.assertIn("legal_advice", flagged_by_id["consult-source"]["output_guard"]["violations"])
        self.assertFalse(flagged_by_id["future-source"]["active_operational_rule"])
        self.assertIn(
            "future_law_applied_as_active",
            flagged_by_id["future-source"]["output_guard"]["violations"],
        )
        cand_entry = next(c for c in flagged_watch["changes"] if c["candidate_id"] == cid)
        self.assertFalse(cand_entry["active_operational_rule"])
        self.assertIn("Advisory review item only", cand_entry["summary"])
        snap = flagged_watch["output_guard"]["telemetry"]
        self.assertGreaterEqual(snap["by_category"]["duty_satisfied"], 1)
        self.assertGreaterEqual(snap["by_category"]["legal_advice"], 1)
        self.assertGreaterEqual(snap["by_category"]["future_law_applied_as_active"], 2)


class AssistantAndChatGuardWiringTest(unittest.TestCase):
    def test_assistants_validate_output_and_visibility_reject_non_advice_violations(self) -> None:
        from zava_forward.core import assistants

        telemetry = GuardTelemetry()
        snapshot = {"citations": {"case:ZF-1": "epc=D"}, "unknowns": ["survey date unverified"]}
        clean = assistants.validate_output(
            {
                "summary": "Dated case evidence lists EPC D pending human review.",
                "findings": [{"text": "Recorded EPC band is D.", "citations": ["case:ZF-1"]}],
                "unknowns": [],
            },
            snapshot,
            4000,
            guard_telemetry=telemetry,
        )
        self.assertIn("survey date unverified", clean["unknowns"])
        self.assertEqual(telemetry.snapshot()["passed_total"], 1)

        for bad_text, expected_cat in (
            ("The statutory duty is satisfied for this home.", "duty_satisfied"),
            ("Legal advice: you are legally required to waive consent.", "legal_advice"),
            (
                "Consultation phase 2 applies now as an active operational rule.",
                "future_law_applied_as_active",
            ),
        ):
            with self.subTest(bad_text=bad_text):
                with self.assertRaises(ValueError):
                    assistants.validate_output(
                        {
                            "summary": bad_text,
                            "findings": [
                                {"text": "Recorded EPC band is D.", "citations": ["case:ZF-1"]}
                            ],
                            "unknowns": [],
                        },
                        snapshot,
                        4000,
                        guard_telemetry=telemetry,
                    )
                self.assertTrue(
                    assistants._output_violates_visibility(
                        {"summary": bad_text, "findings": [], "unknowns": []},
                        (),
                    )
                )
                self.assertGreaterEqual(
                    telemetry.snapshot()["by_category"][expected_cat],
                    1,
                )
        self.assertEqual(telemetry.snapshot()["rejected_total"], 3)

    def test_chat_panel_and_regulatory_chat_enforce_single_gate_telemetry(self) -> None:
        import json
        import tempfile
        from typing import Any

        from regulatory_fixture import ENV, NOW, Fixture
        from zava_forward.core.chat_panel import WITHHELD, ChatPanel
        from zava_forward.core.regulatory_chat import RegulatoryChat

        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            self.addCleanup(fx.close)
            chat_telemetry = GuardTelemetry()

            def unsafe_model(_system: str, _prompt: str) -> str:
                return json.dumps(
                    {
                        "answer": "The statutory duty is satisfied for ZF-1.",
                        "citations": ["ZF-1/stage"],
                    }
                )

            fx.store.cases["ZF-1"]["ai_consent"] = {"status": "Given", "date": "2026-10-01"}
            panel = ChatPanel(fx.iso, model=unsafe_model, guard_telemetry=chat_telemetry)
            created = fx.store.chat_create_thread(fx.user, case_id="ZF-1")
            turn = panel.ask(
                fx.user, created["id"], "Summarise the recorded EPC details.", skill="general"
            )
            self.assertEqual(turn["kind"], "withheld")
            self.assertEqual(turn["reply"], WITHHELD)
            self.assertEqual(chat_telemetry.snapshot()["rejected_total"], 1)

            reg_telemetry = GuardTelemetry()

            def rogue_render(bundle: dict[str, Any]) -> dict[str, Any]:
                return {
                    "schema": "regulatory-chat-v1",
                    "kind": "answer",
                    "reply": "Legal advice: you are legally exempt under the uncommenced phase.",
                    "sections": {
                        "what_sources_say": [],
                        "recorded_home_facts": [],
                        "unknown_or_missing": ["The statutory duty is satisfied."],
                        "safe_next_action": "Proceed.",
                        "who_decides": "Agent.",
                    },
                    "citations": list(bundle["sources"]),
                    "cards": list(bundle["cards"]),
                    "as_of": bundle["as_of"],
                    "requires_human": False,
                    "workflow_only": True,
                }

            reg = RegulatoryChat(
                fx.iso,
                fx.law,
                rogue_render,
                lambda _q: "hazard-awareness-clock",
                lambda _q: None,
                env=ENV,
                clock=lambda: NOW,
                guard_telemetry=reg_telemetry,
            )
            reg_tid = reg.start(fx.user, "ZF-1")
            reg_reply = reg.ask(fx.user, reg_tid, "What do the hazard sources say?")
            self.assertEqual(reg_reply["kind"], "refused")
            self.assertTrue(reg_reply["requires_human"])
            self.assertEqual(reg_reply["citations"], [])
            self.assertFalse(reg_reply["output_guard"]["passed"])
            self.assertEqual(reg_reply["output_guard"]["action"], "rewritten")
            self.assertIn("legal_advice", reg_reply["output_guard"]["violations"])
            self.assertIn("duty_satisfied", reg_reply["output_guard"]["violations"])
            self.assertIn("Advisory review item only", reg_reply["reply"])
            # Single-gate telemetry: exactly 1 checked_total and 1 rewritten_total per turn.
            snap = reg_telemetry.snapshot()
            self.assertEqual(snap["checked_total"], 1)
            self.assertEqual(snap["rewritten_total"], 1)


if __name__ == "__main__":
    unittest.main()
