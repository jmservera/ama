"""Guard that owner-facing docs make no unqualified production claim (issue #113)."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIM = re.compile(
    r"production[- ](ready|grade)|ready for production|approved for production"
    r"|production[- ]approved",
    re.IGNORECASE,
)
QUALIFIER = re.compile(
    r"\b(not|no|never|without|nor|neither|until|before|unless|non|cannot|isn't|aren't)\b",
    re.IGNORECASE,
)


def unqualified_claims(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if CLAIM.search(line) and not QUALIFIER.search(line)
    ]


def guarded_documents() -> list[Path]:
    paths = [ROOT / "README.md", ROOT / "infra" / "README.md"]
    for pattern in ("docs/adrs/*.md", "docs/brds/*.md", "docs/prds/*.md", "src/*/README.md"):
        paths.extend(sorted(ROOT.glob(pattern)))
    return [path for path in paths if path.is_file()]


class ProductionClaimGuardTest(unittest.TestCase):
    def test_documents_make_no_unqualified_production_claim(self) -> None:
        found = {
            str(doc.relative_to(ROOT)): hits
            for doc in guarded_documents()
            if (hits := unqualified_claims(doc.read_text(encoding="utf-8")))
        }
        self.assertEqual({}, found)

    def test_detector_flags_claim_and_accepts_negation(self) -> None:
        self.assertTrue(unqualified_claims("The platform is production-ready."))
        self.assertEqual([], unqualified_claims("This is not production-ready."))
        self.assertEqual([], unqualified_claims("No production approval is claimed."))


if __name__ == "__main__":
    unittest.main()
