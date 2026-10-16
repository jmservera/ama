import unittest
from pathlib import Path

from zava_forward.core.synthetic import cutover_audit as audit

ROOT = Path(__file__).resolve().parents[3]


class CutoverAuditTests(unittest.TestCase):
    def test_api_runtime_golden_is_the_only_eval_context_exception(self) -> None:
        lines = (ROOT / "src/.dockerignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("**/evals", lines)
        self.assertEqual(
            [line for line in lines if line.startswith("!agents/evals")],
            ["!agents/evals", "!agents/evals/ai_priority_golden.json"],
        )
        self.assertLess(lines.index("!agents/evals"), lines.index("agents/evals/*"))
        self.assertLess(
            lines.index("agents/evals/*"), lines.index("!agents/evals/ai_priority_golden.json")
        )

    def test_real_matrix_has_no_missing_destinations(self) -> None:
        import subprocess

        tracked = set(
            subprocess.check_output(["git", "-C", str(ROOT), "ls-files"], text=True).splitlines()
        )
        rows = audit.parity((ROOT / audit.MATRIX).read_text(encoding="utf-8"), tracked)
        self.assertGreater(len(rows), 100)
        self.assertFalse([row for row in rows if row[-1].startswith("MISSING:")])

    def test_missing_destination_mutation_is_detected(self) -> None:
        text = "| `mvp/web/app.js` | migrate | `api/web/app.js` | M5 | proof |"
        target = "src/api/src/zava_forward/api/web/app.js"
        self.assertEqual(audit.parity(text, {target})[0][-1], "destination-present")
        self.assertEqual(audit.parity(text, set())[0][-1], f"MISSING:{target}")

    def test_sandbox_pattern_rows_are_not_silently_omitted(self) -> None:
        text = "| `mvp/.assistant-test-*/seed.json` | 225 | retire | none | S1 |"
        row = audit.parity(text, {"mvp/.assistant-test-example/seed.json"})[0]
        self.assertEqual(row[1], "retire")
        self.assertEqual(row[-1], "still-tracked")
        self.assertEqual(audit.parity(text, set())[0][-1], "absent-before-this-pack")

    def test_actual_targets_override_stale_proposals(self) -> None:
        text = "| `mvp/tests/release_support.py` | migrate | `api-tests/release_support.py` |"
        row = audit.parity(text, {"src/core/tests/release_support.py"})[0]
        self.assertEqual(row[-1], "destination-present")
        self.assertEqual(row[-2], "src/core/tests/release_support.py")

    def test_exclusions_happen_before_read(self) -> None:
        excluded = [
            ".env",
            ".env.local",
            ".vscode/settings.json",
            "properwarm.json",
            "mvp/data/properwarm.json",
            ".copilot-tracking/github-issues/201.md",
            "support/cohort.md",
            "../outside.md",
            "/outside.md",
            audit.REFERENCES,
        ]
        opened: list[str] = []

        def read(name: str) -> str:
            opened.append(name)
            self.assertEqual(name, "README.md")
            return "mvp/ and mvp-ci.yml"

        rows = audit.inventory([*excluded, "README.md"], read)
        self.assertEqual(opened, ["README.md"])
        self.assertEqual(len(rows), 2)

    def test_reference_mutation_fails_shared_oracle(self) -> None:
        original = audit.tsv(
            ("path", "line", "token", "classification"),
            audit.inventory(["README.md"], lambda _: "src/"),
        )
        changed = audit.tsv(
            ("path", "line", "token", "classification"),
            audit.inventory(["README.md"], lambda _: "mvp/"),
        )
        audit.check_expected(original, original, "references")
        with self.assertRaisesRegex(ValueError, "Stale references"):
            audit.check_expected(original, changed, "references")

    def test_deterministic_and_distinct_old_workflow_tokens(self) -> None:
        def read(_: str) -> str:
            return "mvp-ci.yml mvp-validation.yml prototype/ mvp/ mvp/"

        rows = audit.inventory(["b.md", "a.md", "b.md"], read)
        self.assertEqual(len(rows), 8)
        self.assertEqual(rows, audit.inventory(["a.md", "b.md"], read))

    def test_unknown_empty_and_duplicate_rows_fail_explicitly(self) -> None:
        row = "| `mvp/x.py` | migrate | `unknown/x.py` |"
        with self.assertRaisesRegex(ValueError, "Unresolved matrix target"):
            audit.parity(row, set())
        with self.assertRaisesRegex(ValueError, "No historical matrix rows"):
            audit.parity("", set())
        row = "| `prototype/x.py` | retire | none |"
        with self.assertRaisesRegex(ValueError, "Duplicate matrix row"):
            audit.parity(row + "\n" + row, set())


if __name__ == "__main__":
    unittest.main()
