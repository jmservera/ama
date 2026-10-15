"""Copy audit: banned internal terms absent from visible web copy, labels and blocked messages follow the content standard."""
import re
import unittest
from pathlib import Path

from zavaforward_mvp.store import Store

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "mvp" / "web"
DOC = (ROOT / "docs" / "reference" / "research" / "ux" / "content-standard.md").read_text()
BANNED = re.compile(r"\b(gates?|holds?|provenance|traces?)\b", re.I)
# Code identifiers and one stored value that are not shown as wording to a person.
ALLOWED = ("c.gate", "p.provenance", "earlier.provenance", "i.hold", "Keep on hold")


def visible_lines(path):
    for n, line in enumerate(path.read_text().splitlines(), 1):
        for ok in ALLOWED:
            line = line.replace(ok, "")
        yield n, line


class CopyAudit(unittest.TestCase):
    def test_no_internal_terms_in_web_copy(self):
        for f in ("app.js", "assistants.js", "panels.js", "ops.js", "index.html", "welcome.html"):
            for n, line in visible_lines(WEB / f):
                self.assertIsNone(BANNED.search(line), f"{f}:{n}: {line.strip()[:100]}")

    def test_ai_label_is_exact_and_never_implies_approval(self):
        self.assertEqual(Store.REC_LABEL, "AI suggestion, not approved")
        for f in (ROOT / "mvp" / "zavaforward_mvp").glob("*.py"):
            self.assertNotIn("human-approved", f.read_text().replace("human-approved by", ""), f.name)
        js = (WEB / "app.js").read_text()
        self.assertIn("This is not an approval, consent or safety decision", js)

    def test_blocked_reasons_have_reason_owner_and_next_action(self):
        c = {"decision": {"status": "Asked"}, "funding_ok": False, "owner": "Sam Officer",
             "hazards": [{"released": False, "owner": "Hazard Lead"}]}
        reasons = Store.gate_reasons(c)
        self.assertEqual(len(reasons), 3)
        for r in reasons:
            self.assertIn("Owner:", r)
            self.assertIn("Next action:", r)

    def test_standard_documents_glossary_and_review(self):
        for text in ("## Glossary", "## Copy audit of the core flow", "AI suggestion, not approved", "named human", "Reason", "Owner", "Next action"):
            self.assertIn(text, DOC)


if __name__ == "__main__":
    unittest.main()
