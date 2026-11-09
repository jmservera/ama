"""Empty own-queue explanations never claim scenario coverage without a bound declaration.

Runs the real helper functions from app.js in Node. Constructed synthetic values only; this is
partial AC-034/043 evidence and proves neither browser behaviour nor a runtime producer.
"""

import json
import re
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
vm.runInContext(cut("trustedCoverage") + "\n" + cut("queueEmptyExplanation"), context);
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

    def test_no_match_is_a_search_result_even_with_a_valid_declaration(self) -> None:
        for coverage in (None, DECLARATION):
            out = explain(filtered=True, coverage=coverage)
            assert out is not None
            self.assertEqual(out["state"], "no-match")
            self.assertTrue(out["text"].startswith("No cases match these filters."))
            self.assertIn("not a statement about scenario coverage", out["text"])
            self.assertNotIn("fixture", out["text"])

    def test_valid_bound_declaration_is_a_declared_gap_with_provenance(self) -> None:
        out = explain(coverage=DECLARATION)
        assert out is not None
        self.assertEqual(out["state"], "declared-unrepresented")
        for part in ("152-ia-v1", "dataset declaration", "2026-10-16", "declared gap"):
            self.assertIn(part, out["text"])
        self.assertNotIn("complete", out["text"])

    def test_missing_stale_mismatched_or_malformed_declarations_stay_unknown(self) -> None:
        variants: dict[str, Any] = {
            "stale as_of": {**DECLARATION, "as_of": "2026-10-01"},
            "stale policy": {**DECLARATION, "policy_version": "ranking-0"},
            "contract mismatch": {**DECLARATION, "contract": "work-queues-0"},
            "other role": {**DECLARATION, "perspective": "Retrofit Programme Manager"},
            "represented": {**DECLARATION, "status": "represented"},
            "blank fixture": {**DECLARATION, "fixture_version": " "},
            "no source": {k: v for k, v in DECLARATION.items() if k != "source"},
            "no as_of": {k: v for k, v in DECLARATION.items() if k != "as_of"},
            "numeric policy": {**DECLARATION, "policy_version": 1},
            "list": [DECLARATION],
            "string": "unrepresented",
        }
        for name, coverage in variants.items():
            with self.subTest(name):
                out = explain(coverage=coverage)
                assert out is not None
                self.assertEqual(out["state"], UNKNOWN)
        for name in ("asOf", "policyVersion", "version", "role"):
            with self.subTest(f"page value {name} missing"):
                out = explain(coverage=DECLARATION, ctx={**CTX, name: ""})
                assert out is not None
                self.assertEqual(out["state"], UNKNOWN)
        out = explain(coverage=DECLARATION, ctx={k: v for k, v in CTX.items() if k != "asOf"})
        assert out is not None
        self.assertEqual(out["state"], UNKNOWN)

    def test_all_cases_scope_never_uses_coverage_wording(self) -> None:
        out = explain(view="all", coverage=DECLARATION)
        assert out is not None
        self.assertEqual(out["state"], "empty-all")
        self.assertEqual(out["text"], "No permitted open cases are available.")

    def test_no_server_produces_a_coverage_declaration_yet(self) -> None:
        self.assertNotIn("coverage", taskqueues.contract(ranking.CURRENT))

    def test_list_view_passes_the_page_and_session_values_to_the_helper(self) -> None:
        source = APP.read_text()
        self.assertTrue(re.search(r"asOf = d\.as_of;", source))
        for token in (
            "coverage: me.work_queues.coverage",
            "role: me.user.role",
            "version: me.work_queues.version",
            "policyVersion: policy",
            "rowsLength: rows.length",
        ):
            self.assertIn(token, source)


if __name__ == "__main__":
    unittest.main()
