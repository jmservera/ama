"""Audit the delivery order of the children of Epic #208 against ADR 0005.

Refs #208, Refs #440. Read-only over repository evidence; it never calls GitHub, never
ticks a criterion and never states that a duty is met. Closure dates are observations
recorded on 2026-11-19, not live assertions.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADR = ROOT / "docs/adrs/0005-regulatory-compliance-assistant.md"
CORE = ROOT / "src/core/src/zava_forward/core"

# ADR 0005 "Phasing" step for each child (step 5, broadening, has no child yet).
ADR_PHASE = {210: 1, 211: 2, 212: 2, 214: 3, 213: 4}

# "Depends on" lines of the child issue bodies, observed 2026-11-19.
DEPENDS_ON = {
    209: [],
    210: [209],
    211: [210, 209],
    212: [211],
    213: [210, 211],
    214: [210, 211],
    215: [212],
    216: [212, 214],
    217: [209],
}

# Closure date (ISO) observed on 2026-11-19; open children are absent.
CLOSED_ON = {
    209: "2026-10-16",
    210: "2026-10-15",
    211: "2026-10-27",
    212: "2026-11-04",
    213: "2026-10-27",
    214: "2026-10-31",
    217: "2026-11-18",
}

# Implementing module per phase, so the audit fails if code and phase drift apart.
MODULE = {
    210: CORE / "lawstore.py",
    211: CORE / "rulecards.py",
    212: CORE / "rule_engine.py",
    213: CORE / "source_monitor.py",
    214: CORE / "regulatory_chat.py",
}


def adr_phasing() -> list[str]:
    text = ADR.read_text(encoding="utf-8")
    section = text.split("## Phasing", 1)[1].split("\n## ", 1)[0]
    return re.findall(r"^\d+\.\s+(.*?)(?=^\d+\.|\Z)", section, re.DOTALL | re.MULTILINE)


def deviations() -> set[tuple[int, int]]:
    """Pairs (later_phase, earlier_phase) where the later ADR phase closed first."""
    found = set()
    for a, pa in ADR_PHASE.items():
        for b, pb in ADR_PHASE.items():
            if pa > pb and CLOSED_ON[a] < CLOSED_ON[b]:
                found.add((a, b))
    return found


class Epic208ChildOrder(unittest.TestCase):
    def test_adr_phase_order_matches_pinned_mapping(self) -> None:
        steps = [s.lower() for s in adr_phasing()]
        self.assertEqual(len(steps), 5)
        self.assertIn("law store", steps[0])
        self.assertIn("rule cards", steps[1])
        self.assertIn("chat", steps[2])
        self.assertIn("change monitoring", steps[3])
        self.assertIn("broaden", steps[4])

    def test_declared_dependencies_resolve_and_closure_order_is_recorded(self) -> None:
        early = set()
        for child, deps in DEPENDS_ON.items():
            for dep in deps:
                self.assertIn(dep, DEPENDS_ON)
                if child in CLOSED_ON and dep in CLOSED_ON and CLOSED_ON[child] < CLOSED_ON[dep]:
                    early.add((child, dep))
        # #210 closed one day before the decision #209 it depends on; kept as adverse evidence.
        self.assertEqual(early, {(210, 209)})

    def test_phase_and_dependency_order_agree(self) -> None:
        for child, deps in DEPENDS_ON.items():
            for dep in deps:
                if child in ADR_PHASE and dep in ADR_PHASE:
                    self.assertLessEqual(ADR_PHASE[dep], ADR_PHASE[child])

    def test_each_phase_has_an_implementing_module(self) -> None:
        for child, path in MODULE.items():
            self.assertTrue(path.is_file(), f"#{child}: {path} missing")

    def test_observed_order_deviation_is_recorded_not_hidden(self) -> None:
        # Change monitoring (phase 4) closed before the engine (2) and chat (3).
        self.assertEqual(deviations(), {(213, 212), (213, 214), (214, 212)})

    def test_open_children_block_epic_closure(self) -> None:
        open_children = {215, 216}
        self.assertTrue(open_children.isdisjoint(CLOSED_ON))
        self.assertTrue(open_children <= set(DEPENDS_ON))


if __name__ == "__main__":
    unittest.main()
