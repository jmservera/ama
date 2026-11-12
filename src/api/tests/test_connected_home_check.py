"""Regression tests for the pure rules of the connected same-home check (Refs #134)."""

from __future__ import annotations

import copy
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

import dataset
from checks import connected_home_browser_check as walk

SCREENS = Path(walk.__file__).resolve().parents[1] / "src/zava_forward/api/web/role-screens.js"


def screen_block(source: str, screen: str) -> str:
    blocks = source.split("registerRoleScreen({")
    block = next(b for b in blocks if f'id: "{screen}"' in b[:60])
    return block.split("function hazardScreen")[0]


def panel_span(block: str, source: str, title: str) -> str:
    """The renderer text of the panel with this title, to the next panel or function end."""
    if f'screenPanel("{title}"' not in block:
        block = source
    source = block
    start = source.index(f'screenPanel("{title}"')
    rest = source[start + 1 :]
    stops = [m.start() for m in re.finditer(r"screenPanel\(|screenWithheld\(|\n\}\)?;?\n", rest)]
    return source[start : start + 1 + (min(stops) if stops else len(rest))]


def observed_from(expected: list[walk.Expect], home: str) -> dict[str, Any]:
    """A page observation holding exactly the markers a screen must show for the home."""
    panels: dict[str, dict[str, Any]] = {}
    links: list[str] = []
    for want in expected:
        panel = panels.setdefault(
            want.panel, {"title": want.panel, "text": "", "rows": [], "fields": []}
        )
        if want.row:
            panel["rows"].append(list(want.row))
        if want.field:
            panel["fields"].append(list(want.field))
        panel["text"] += want.text + "\n"
        links += want.links
    menu = [walk.screen_href("asset-board", home), walk.screen_href("programme-queue", home)]
    return {
        "heading": f"Selected home {home}",
        "panels": list(panels.values()),
        "links": links,
        "handoff": f"#/case/{home}",
        "menu": menu,
    }


class ConnectedHomeCheck(unittest.TestCase):
    data: dict[str, Any]
    expected: dict[str, tuple[walk.Expect, ...]]
    own: dict[str, tuple[walk.Expect, ...]]
    leaks: list[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = walk.journey_snapshot()
        cls.expected = walk.home_expectations(cls.data)
        cls.own = walk.sibling_expectations(cls.data)
        cls.leaks = walk.leak_markers(cls.data)

    def test_real_journey_snapshot_is_usable_and_empty_or_seed_only_is_not(self) -> None:
        self.assertEqual(walk.snapshot_failures(self.data), [])
        self.assertTrue(walk.snapshot_failures({}))
        self.assertTrue(walk.snapshot_failures(copy.deepcopy(dataset.DATA)))
        partial = copy.deepcopy(self.data)
        partial["cases"] = [
            {**c, "quality": []} if c["id"] == walk.HOME_ID else c for c in partial["cases"]
        ]
        self.assertTrue(walk.snapshot_failures(partial))
        home_quality = walk.case_of(self.data, walk.HOME_ID)["quality"]
        indistinct = copy.deepcopy(self.data)
        indistinct["cases"] = [
            {**c, "quality": home_quality} if c["id"] == walk.SIBLING_ID else c
            for c in indistinct["cases"]
        ]
        self.assertTrue(walk.snapshot_failures(indistinct))

    def test_every_screen_needs_its_markers_and_names_the_missing_one(self) -> None:
        for screen, expected in self.expected.items():
            with self.subTest(screen=screen):
                self.assertEqual(
                    walk.home_failures(
                        screen, observed_from(list(expected), "ZF-1"), self.expected
                    ),
                    [],
                )
                for index, dropped in enumerate(expected):
                    rest = [w for i, w in enumerate(expected) if i != index]
                    seen = observed_from(rest, "ZF-1")
                    self.assertTrue(walk.home_failures(screen, seen, self.expected), dropped)

    def test_wrong_home_heading_handoff_and_menu_are_rejected(self) -> None:
        screen = "technical-queue"
        good = observed_from(list(self.expected[screen]), "ZF-1")
        changes: tuple[dict[str, Any], ...] = (
            {"heading": "Selected home ZF-2"},
            {"handoff": "#/case/ZF-2"},
            {"menu": [walk.screen_href("asset-board", "ZF-1"), "#/screens?screen=programme-queue"]},
            {"menu": []},
        )
        for change in changes:
            with self.subTest(change=change):
                self.assertTrue(walk.home_failures(screen, {**good, **change}, self.expected))

    def test_sibling_must_show_own_data_without_home_records(self) -> None:
        self.assertTrue(self.leaks)
        for screen, expected in self.own.items():
            with self.subTest(screen=screen):
                seen = observed_from(list(expected), "ZF-2")
                self.assertEqual(walk.sibling_failures(screen, seen, self.own, self.leaks), [])
                leaked = copy.deepcopy(seen)
                leaked["panels"][0]["text"] += self.leaks[0]
                self.assertTrue(walk.sibling_failures(screen, leaked, self.own, self.leaks))
                self.assertTrue(
                    walk.sibling_failures(screen, {**seen, "panels": []}, self.own, self.leaks)
                )

    def test_leak_in_actual_record_panel_is_rejected_without_a_positive_panel(self) -> None:
        # Record panels the positive sibling expectations do not name must still be scanned.
        for screen, titles in walk.RECORD_PANELS.items():
            named = {w.panel for w in self.own[screen]}
            for title in [t for t in titles if t not in named]:
                with self.subTest(screen=screen, panel=title):
                    seen = observed_from(list(self.own[screen]), "ZF-2")
                    clean = walk.sibling_failures(screen, seen, self.own, self.leaks)
                    self.assertEqual(clean, [])
                    seen["panels"].append(
                        {"title": title, "text": self.leaks[0], "rows": [], "fields": []}
                    )
                    self.assertTrue(walk.sibling_failures(screen, seen, self.own, self.leaks))
        seen = observed_from(list(self.own["quality-queue"]), "ZF-2")
        seen["panels"].append(
            {"title": "Loft insulation: Handed over", "text": "x", "rows": [], "fields": []}
        )
        self.assertTrue(walk.sibling_failures("quality-queue", seen, self.own, self.leaks))

    def test_literal_home_data_destinations_each_reject_a_home_record(self) -> None:
        # Titles are listed here from the renderers, not taken from walk.RECORD_PANELS.
        destinations = {
            "asset-board": ("Stock conflict comparison", "Eligibility"),
            "programme-queue": ("Connected view for ZF-2",),
            "technical-queue": (
                "Technical readiness",
                "Source facts",
                "Design version",
                "Separate sign-offs",
                "Returns and routing",
                "Missing references",
            ),
            "resident-choice": (
                "Choice for each measure",
                "Paused or withdrawn by the resident",
                "Linked update commitment",
                "Service requests and access needs (separate from choice)",
            ),
            "quality-queue": (
                "Handover readiness",
                "Quality evidence",
                "Loft insulation: Handed over",
            ),
            "finance-invoices": ("Invoice line comparison",),
        }
        for screen, titles in destinations.items():
            for title in titles:
                with self.subTest(screen=screen, panel=title):
                    seen = observed_from(list(self.own[screen]), "ZF-2")
                    self.assertEqual(walk.sibling_failures(screen, seen, self.own, self.leaks), [])
                    seen["panels"].append(
                        {"title": title, "text": self.leaks[0], "rows": [], "fields": []}
                    )
                    self.assertTrue(walk.sibling_failures(screen, seen, self.own, self.leaks))

    def test_technical_readiness_with_home_source_conflict_is_rejected(self) -> None:
        home = walk.case_of(self.data, walk.HOME_ID)["stock_reconciliation"][0]
        text = f"Source conflict {home['id']} ({home['field']}) is unresolved."
        seen = observed_from(list(self.own["technical-queue"]), "ZF-2")
        seen["panels"].append({"title": "Technical readiness", "text": "Missing items are listed."})
        self.assertEqual(walk.sibling_failures("technical-queue", seen, self.own, self.leaks), [])
        seen["panels"][-1]["text"] = text
        failures = walk.sibling_failures("technical-queue", seen, self.own, self.leaks)
        self.assertTrue([f for f in failures if "leaked" in f], failures)
        sibling = walk.case_of(self.data, walk.SIBLING_ID)
        self.assertNotIn(home["id"], str(sibling))

    def test_inventory_covers_every_panel_the_six_renderers_declare(self) -> None:
        source = SCREENS.read_text(encoding="utf-8")
        for screen, record in walk.RECORD_PANELS.items():
            titles = set(re.findall(r'screenPanel\(\s*"([^"]+)"', screen_block(source, screen)))
            if screen == "finance-invoices":
                titles.add("Invoice line comparison")
            audited = set(record) | set(walk.EXCLUDED[screen])
            with self.subTest(screen=screen):
                self.assertEqual(titles - audited, set())
                self.assertEqual(set(record) & set(walk.EXCLUDED[screen]), set())
                self.assertTrue(set(record) <= titles | {"Quality evidence"})

    def test_every_exclusion_rests_on_its_source_anchor_and_reads_no_home_field(self) -> None:
        source = SCREENS.read_text(encoding="utf-8")
        for screen, excluded in walk.EXCLUDED.items():
            for title, why in excluded.items():
                with self.subTest(screen=screen, panel=title):
                    self.assertIn(why.kind, ("portfolio-call", "constant", "home-id-only"))
                    block = screen_block(source, screen)
                    self.assertTrue(why.why)
                    self.assertTrue(why.anchor in block or why.anchor in source, why.anchor)
                    span = panel_span(block, source, title)
                    # Aliases of the selected home's record in the renderers' render(c) bodies.
                    fields = set(re.findall(r"\bc\??\.(\w+)", span))
                    aliases = r"\b(queries|reasons|states|requests)\b\s*[.\[)]"
                    self.assertFalse(re.search(aliases, span), span)
                    self.assertEqual(fields - {"id"}, set(), span)
                    if why.kind == "home-id-only":
                        self.assertIn("c.id", span)
                    else:
                        self.assertNotIn("c.id", span)

    def test_importing_the_check_keeps_api_tests_first_for_discovery(self) -> None:
        # A fresh process discovers this module, then the duplicate-named dependency-rule test.
        api = SCREENS.parents[4]
        script = (
            "import sys, unittest\n"
            "loader = unittest.TestLoader()\n"
            "loader.discover('tests', pattern='test_connected_home_check.py')\n"
            "suite = loader.discover('tests', pattern='test_dependency_rule.py')\n"
            "import test_dependency_rule as rule\n"
            "print('RECEIPT', rule.__file__, sys.path[0])\n"
            "print('FAILED', [t.id() for t in suite._tests if 'Failed' in type(t).__name__])\n"
        )
        run = subprocess.run(
            [sys.executable, "-c", script], cwd=api, env=os.environ, capture_output=True, text=True
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        receipt = next(x for x in run.stdout.splitlines() if x.startswith("RECEIPT")).split()
        self.assertEqual(Path(receipt[1]).resolve(), api / "tests/test_dependency_rule.py")
        self.assertIn("FAILED []", run.stdout)

    def test_portfolio_panels_with_other_homes_data_are_not_rejected(self) -> None:
        seen = observed_from(list(self.own["asset-board"]), "ZF-2")
        for title in (
            "Stock conflict queue across homes (portfolio scope, not this home)",
            "Portfolio scope",
        ):
            seen["panels"].append({"title": title, "text": self.leaks[0], "rows": [], "fields": []})
        self.assertEqual(walk.sibling_failures("asset-board", seen, self.own, self.leaks), [])

    def test_generic_values_are_not_used_as_home_markers(self) -> None:
        sibling = str(walk.case_of(self.data, walk.SIBLING_ID))
        self.assertFalse([m for m in self.leaks if m in sibling])

    def test_declared_screens_and_required_labels_exist_in_the_page_source(self) -> None:
        source = SCREENS.read_text(encoding="utf-8")
        for screen in self.expected:
            self.assertRegex(source, rf"[\"']{re.escape(screen)}[\"']")
        for label in (
            "Evidence boundary",
            "Connected view for",
            "Invoice line comparison",
            "Choice for each measure",
        ):
            self.assertIn(label, source)


if __name__ == "__main__":
    unittest.main()
