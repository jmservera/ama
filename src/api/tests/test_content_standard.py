"""Copy audit: banned internal terms absent from visible web copy, labels and blocked messages follow the content standard."""
import re
import unittest
from pathlib import Path

from zava_forward.core.store import Store

ROOT = Path(__file__).resolve().parents[3]
WEB = ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web"
DOC = (ROOT / "docs" / "reference" / "research" / "ux" / "content-standard.md").read_text()
BANNED = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b", re.I)
AUDITED_FILES = ("app.js", "assistants.js", "panels.js", "ops.js", "chat.js", "timecapture.js", "role-screens.js", "law.js", "law.html", "index.html", "welcome.html")
# Exact identifiers, raw technical JSON key and legacy stored finance value only.
ALLOWED = ("c.gate", "p.provenance", "earlier.provenance", "i.hold", "x.hold", "Keep on hold", 'category("holds",', "envelope: p.envelope", "p.snapshot")


def copy_violations(text):
    """Conservative lexical guard, not a JS visibility parser or a dynamic-content audit."""
    for n, line in enumerate(text.splitlines(), 1):
        for ok in ALLOWED:
            line = line.replace(ok, "")
        if BANNED.search(line):
            yield n, line


class CopyAudit(unittest.TestCase):
    def test_no_internal_terms_in_web_copy(self):
        for f in AUDITED_FILES:
            self.assertEqual(list(copy_violations((WEB / f).read_text())), [], f)

    def test_all_standard_vocabulary_families_are_guarded(self):
        for word in ("gate", "gates", "hold", "holds", "provenance", "trace", "traces",
                     "snapshot", "snapshots", "envelope", "envelopes"):
            with self.subTest(word=word):
                self.assertTrue(list(copy_violations(f'h("p", {{}}, "{word.upper()}");')))

    def test_identifier_exceptions_do_not_hide_adjacent_bad_copy(self):
        for identifier in ("c.gate", "p.provenance", "earlier.provenance", "i.hold",
                           "x.hold", "envelope: p.envelope", "p.snapshot"):
            with self.subTest(identifier=identifier):
                self.assertEqual(list(copy_violations(identifier)), [])
                self.assertTrue(list(copy_violations(f'{identifier}; h("dt", {{}}, "Check snapshot");')))
        # Dynamic quotations, facts and user/model text are not application-owned literals.
        for expression in ("source.quote", "fact.text", "answer.reply", "turn.content"):
            self.assertEqual(list(copy_violations(f'h("blockquote", {{}}, {expression});')), [])

    def test_chat_safety_and_copy_contract(self):
        js = (WEB / "chat.js").read_text()
        for text in ("AI suggestion, not approved", "only an authorised human can make a restart decision for stopped retrofit work",
                     "This panel cannot acknowledge, decide compliance or restart stopped retrofit work.",
                     "Check recorded at", "These are historical records; ask again for a fresh lookup.",
                     "Use the existing human emergency or hazard service now.",
                     "Evidence is missing or cannot be relied on. Do not treat this as clear.",
                     "Licensed PAS 2035 text and contract incorporation are unverified.",
                     "it can only request a proposal that someone else reviews"):
            self.assertIn(text, js)

    def test_restored_bad_chat_labels_fail_the_actual_guard(self):
        js = (WEB / "chat.js").read_text()
        for corrected, original in (
            ("make a restart decision for stopped retrofit work", "decide a hold"),
            ("restart stopped retrofit work", "release a hold"),
            ("Check recorded at", "Check snapshot"),
            ("These are historical records", "Dates are historical snapshots"),
        ):
            with self.subTest(original=original):
                self.assertIn(corrected, js)
                mutated = js.replace(corrected, original, 1)
                self.assertTrue(list(copy_violations(mutated)), original)

    def test_ai_label_is_exact_and_never_implies_approval(self):
        self.assertEqual(Store.REC_LABEL, "AI suggestion, not approved")
        for f in (*(ROOT / "src" / "api" / "src" / "zava_forward" / "api").glob("*.py"), *(ROOT / "src" / "core" / "src" / "zava_forward" / "core").glob("*.py")):
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

    def test_resident_draft_and_representative_copy_boundaries(self):
        js = (WEB / "app.js").read_text()
        self.assertIn("Draft a message for review", js)
        self.assertNotIn('"Write to the resident"', js)
        self.assertIn("Draft only. Nothing is sent here. A named human must review the exact wording before any resident use.", js)
        self.assertIn("Reviewing a draft is not approval of works, resident consent or a safety decision.", js)
        panels = (WEB / "panels.js").read_text()
        self.assertIn("Review due date (authority unavailable from this date)", panels)
        self.assertNotIn("authority held from this date", panels)

    def test_proposal_review_copy_is_not_decision_approval(self):
        js = (WEB / "assistants.js").read_text()
        self.assertIn("AI suggestion, not approved", js)
        self.assertIn("Accepting or editing this proposal records a draft review. This is not an approval, consent or safety decision.", js)
        self.assertIn("Requested using:", js)
        self.assertNotIn("Invocation:", js)
        self.assertIn("Accept proposal only", js)
        self.assertIn('onclick: () => act("edit-accept") }, "Save edited proposal"', js)
        self.assertIn("as a draft by a person. This is not an approval, consent or safety decision.", js)
        self.assertIn("Confidence: not provided. Confidence is not accuracy.", js)

    def test_generic_error_and_ranking_error_state_reason_owner_next_action(self):
        js = (WEB / "app.js").read_text()
        self.assertNotIn("Something went wrong", js)
        self.assertIn("e.generic = !data.error", js)
        self.assertIn("check the recorded history before repeating a change", js)
        self.assertIn("Owner: application support. Next action: try All sources", (WEB / "law.js").read_text())
        with self.assertRaises(PermissionError) as ctx:
            Store.ranking_snapshot(object(), {"role": "Resident"})
        for part in ("Only a manager", "Owner:", "Next action:"):
            self.assertIn(part, str(ctx.exception))
        self.assertNotIn("snapshot", str(ctx.exception).lower())

    def test_role_screens_use_phase_check_wording(self):
        js = (WEB / "role-screens.js").read_text()
        self.assertIn("Benefits and phase check", js)
        self.assertTrue(list(copy_violations(js.replace("phase check evidence", "gate evidence", 1))))

    def test_time_capture_copy_is_guarded(self):
        self.assertIn("timecapture.js", AUDITED_FILES)
        js = (WEB / "timecapture.js").read_text()
        corrected = "have the same role as the requester"
        self.assertIn(corrected, js)
        self.assertTrue(list(copy_violations(js.replace(corrected, "hold the same role as the requester"))))


if __name__ == "__main__":
    unittest.main()
