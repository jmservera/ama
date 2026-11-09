"""Empty own-queue explanations never claim scenario coverage.

Runs the real helper function from app.js in Node. Constructed synthetic values only; this is
partial AC-034/043 evidence and proves neither browser behaviour nor a runtime producer. No
authoritative current fixture or provenance exists, so any coverage payload is ignored.
"""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core import ranking, taskqueues

API = Path(__file__).resolve().parents[1]
APP = API / "src/zava_forward/api/web/app.js"
MANIFEST = json.loads((API / "checks/workbench-manifest.json").read_text())

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(process.argv[1], "utf8");
const cut = (name) => {
  const start = source.indexOf("function " + name + "(");
  let depth = 0, i = source.indexOf(") {", start) + 2;
  for (let j = i; j < source.length; j++) {
    if (source[j] === "{") depth++;
    if (source[j] === "}" && --depth === 0) return source.slice(start, j + 1);
  }
};
const context = vm.createContext({});
vm.runInContext(cut("queueEmptyExplanation"), context);
const cases = JSON.parse(process.argv[2]);
console.log(JSON.stringify(cases.map((c) => vm.runInContext(
  "queueEmptyExplanation(" + JSON.stringify(c) + ")", context))));
"""

CTX = {
    "role": "Retrofit Coordinator",
    "version": "work-queues-1",
    "asOf": "2026-10-16",
    "policyVersion": "ranking-1",
}
DECLARATION = {
    "status": "unrepresented",
    "contract": "work-queues-1",
    "as_of": "2026-10-16",
    "policy_version": "ranking-1",
    "perspective": "Retrofit Coordinator",
    "fixture_version": "152-ia-v1",
    "source": "dataset declaration",
}
UNKNOWN = "coverage-unknown"


def explain(**overrides: Any) -> dict[str, Any] | None:
    case = {"view": "mine", "filtered": False, "rowsLength": 0, "coverage": None, "ctx": CTX}
    case.update(overrides)
    return explain_many([case])[0]


def explain_many(cases: list[dict[str, Any]]) -> list[dict[str, Any] | None]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(APP), json.dumps(cases)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: list[dict[str, Any] | None] = json.loads(result.stdout)
    return parsed


class EmptyQueueExplanation(unittest.TestCase):
    def test_empty_coordinator_default_without_declaration_is_unknown(self) -> None:
        coordinator = next(
            p for p in MANIFEST["profiles"] if p.get("identity") == "coordinator@example.test"
        )
        self.assertEqual(coordinator["default"]["ids"], [])
        out = explain()
        assert out is not None
        self.assertEqual(out["state"], UNKNOWN)
        self.assertTrue(
            out["text"].startswith(
                "No open cases are assigned to you. This does not mean the programme has no work."
            )
        )
        self.assertIn("unknown", out["text"])
        self.assertNotIn("unrepresented", out["text"])

    def test_populated_queue_such_as_programme_manager_zf5_has_no_explanation(self) -> None:
        manager = next(p for p in MANIFEST["profiles"] if p.get("identity") == "pam@example.test")
        self.assertEqual(manager["default"]["ids"], ["ZF-5"])
        for coverage in (None, DECLARATION):
            self.assertIsNone(explain(rowsLength=len(manager["default"]["ids"]), coverage=coverage))

    def test_no_match_is_a_search_result_even_when_a_coverage_payload_is_supplied(self) -> None:
        for coverage in (None, DECLARATION):
            out = explain(filtered=True, coverage=coverage)
            assert out is not None
            self.assertEqual(out["state"], "no-match")
            self.assertTrue(out["text"].startswith("No cases match these filters."))
            self.assertIn("not a statement about scenario coverage", out["text"])
            self.assertNotIn("fixture", out["text"])

    def test_unverified_provenance_never_becomes_a_declared_gap(self) -> None:
        payloads: dict[str, Any] = {
            "well formed": DECLARATION,
            "stale or unrelated fixture": {
                **DECLARATION,
                "fixture_version": "stale-or-unrelated-fixture",
                "source": "unverified declaration",
            },
            "malformed": [DECLARATION],
        }
        for name, coverage in payloads.items():
            with self.subTest(name):
                out = explain(coverage=coverage)
                assert out is not None
                self.assertEqual(out["state"], UNKNOWN)
                for part in ("fixture", "declared", "unrepresented", "unverified declaration"):
                    self.assertNotIn(part, out["text"])

    def test_all_cases_scope_never_uses_coverage_wording(self) -> None:
        out = explain(view="all", coverage=DECLARATION)
        assert out is not None
        self.assertEqual(out["state"], "empty-all")
        self.assertEqual(out["text"], "No permitted open cases are available.")

    def test_no_server_produces_a_coverage_declaration_yet(self) -> None:
        self.assertNotIn("coverage", taskqueues.contract(ranking.CURRENT))

    def test_list_view_passes_only_the_row_count_and_scope_to_the_helper(self) -> None:
        source = APP.read_text()
        self.assertIn("rowsLength: rows.length", source)
        for gone in ("trustedCoverage", "declared-unrepresented", "me.work_queues.coverage"):
            self.assertNotIn(gone, source)


if __name__ == "__main__":
    unittest.main()
