"""Epic #113: no production claim without measured load, recovery and DPO or Legal approvals."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLAIM = re.compile(
    r"production[- ](ready|grade|resilien\w*|certified)|ready for production|"
    r"production[- ]approved",
    re.IGNORECASE,
)
QUALIFIER = re.compile(
    r"\b(no|not|never|without|until|before|pending|requires?|required|cannot|n't)\b",
    re.IGNORECASE,
)
SUFFIXES = {".py", ".js", ".html", ".md", ".bicep"}
SKIP_PARTS = {"tests", "node_modules", "__pycache__", ".mypy_cache", ".ruff_cache", "checks"}


def unqualified_claims(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if CLAIM.search(line) and not QUALIFIER.search(line)
    ]


def shipped_files() -> list[Path]:
    roots = [p / "src" for p in sorted((ROOT / "src").iterdir()) if (p / "src").is_dir()]
    roots.append(ROOT / "infra")
    return [
        f
        for base in roots
        for f in base.rglob("*")
        if f.is_file() and f.suffix in SUFFIXES and not SKIP_PARTS & set(f.relative_to(ROOT).parts)
    ]


class NoUnqualifiedProductionClaimTest(unittest.TestCase):
    def test_scanner_flags_positive_and_accepts_negated_claims(self) -> None:
        self.assertEqual(
            unqualified_claims("The demo is production-ready."),
            ["The demo is production-ready."],
        )
        self.assertEqual(unqualified_claims("Owner-approved demo only, no production claim."), [])
        self.assertEqual(
            unqualified_claims("Not production ready until DPO and Legal approve."), []
        )

    def test_shipped_source_makes_no_unqualified_production_claim(self) -> None:
        files = shipped_files()
        self.assertGreater(len(files), 50)
        offenders = {
            str(f.relative_to(ROOT)): hits
            for f in files
            if (hits := unqualified_claims(f.read_text(encoding="utf-8", errors="ignore")))
        }
        self.assertEqual(offenders, {})


if __name__ == "__main__":
    unittest.main()
