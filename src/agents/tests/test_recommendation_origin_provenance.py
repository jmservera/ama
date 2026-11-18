"""Issue #104: recommendation cards separate rule-based gates from generative narrative.

Offline and synthetic: the model is a scripted answer; nothing is approved or called.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core import ai_tasks
from zava_forward.core.store import Store

from zava_forward.agents import ai_eval

harness: Any = ai_eval  # the offline harness is untyped


def scenario(name: str) -> dict[str, Any]:
    golden = json.loads(Path(harness.GOLDEN).read_text())
    return next(s for s in golden["scenarios"] if s["name"].startswith(name))


class RecommendationOriginTests(unittest.TestCase):
    def card(self, sc: dict[str, Any], mode: str | None = None) -> dict[str, Any]:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = Path(tmp.name) / "eval.json"
        cases = [harness.build_case(c) for c in sc["cases"]]
        p.write_text(json.dumps(dict(staff=[harness.OWNER, harness.OTHER], cases=cases)))
        live = os.path.join(tmp.name, "live.json")
        store = Store(str(p), live, os.path.join(tmp.name, "audit.jsonl"))
        outs = [sc["model_output"]] if sc.get("model_output") is not None else None
        harness._scripted(store, outs)
        card: dict[str, Any] = store.ai_priority(harness.OWNER, sc["n"], mode=mode)
        return card

    def test_origin_of_maps_only_model_output_to_generative(self) -> None:
        self.assertEqual(ai_tasks.origin_of("ai"), "generative_model")
        for source in ("template", None, ""):
            self.assertEqual(ai_tasks.origin_of(source), "decision_rule")

    def test_model_card_labels_narrative_generative_and_order_rule_based(self) -> None:
        card = self.card(scenario("valid cited model output"))
        self.assertEqual(card["source"], "ai")
        self.assertEqual(card["origin"], "generative_model")
        self.assertEqual(card["ordering_origin"], "decision_rule")
        self.assertTrue(card["items"])
        self.assertEqual({i["reason_origin"] for i in card["items"]}, {"generative_model"})
        self.assertTrue(card["deterministic"])
        self.assertEqual({d["origin"] for d in card["deterministic"]}, {"decision_rule"})

    def test_fallback_and_workflow_only_cards_never_claim_generative(self) -> None:
        for sc, mode in (
            (scenario("template path"), None),
            (scenario("model invents a case id"), None),
            (scenario("valid cited model output"), "workflow"),
        ):
            with self.subTest(scenario=sc["name"], mode=mode):
                card = self.card(sc, mode)
                self.assertEqual(card["source"], "template")
                self.assertEqual(card["origin"], "decision_rule")
                self.assertEqual({i["reason_origin"] for i in card["items"]}, {"decision_rule"})


if __name__ == "__main__":
    unittest.main()
