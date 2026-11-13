"""Copy audit: banned internal terms absent from visible web copy, labels and blocked messages follow the content standard."""

import json
import re
import subprocess
import unittest
from pathlib import Path

from zava_forward.core.store import Store

ROOT = Path(__file__).resolve().parents[3]
WEB = ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web"
DOC = (ROOT / "docs" / "reference" / "research" / "ux" / "content-standard.md").read_text()
BANNED = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b", re.I)
AUDITED_FILES = (
    "app.js",
    "assistants.js",
    "panels.js",
    "ops.js",
    "chat.js",
    "timecapture.js",
    "role-screens.js",
    "simulator-control.js",
    "staff-intake.js",
    "law.js",
    "law.html",
    "index.html",
    "welcome.html",
    "aftercare.js",
    "case-workspace.js",
    "chat-widget.js",
    "async-action.js",
    "progress.js",
    "workspace-shell.js",
)
# Exact identifiers, raw technical JSON key and legacy stored finance value only.
ALLOWED = (
    "c.gate",
    "p.provenance",
    "earlier.provenance",
    "v.provenance",
    "i.hold",
    "x.hold",
    "h.hold",
    "inv.hold",
    "Keep on hold",
    'category("holds",',
    'shared("holds",',
    "envelope: p.envelope",
    "p.snapshot",
)


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

    def test_every_served_script_and_page_is_audited(self):
        served = {p.name for p in (*WEB.glob("*.js"), *WEB.glob("*.html"))}
        self.assertEqual(sorted(served - set(AUDITED_FILES)), [])
        self.assertEqual(sorted(set(AUDITED_FILES) - served), [])

    def test_all_standard_vocabulary_families_are_guarded(self):
        for word in (
            "gate",
            "gates",
            "hold",
            "holds",
            "provenance",
            "trace",
            "traces",
            "snapshot",
            "snapshots",
            "envelope",
            "envelopes",
        ):
            with self.subTest(word=word):
                self.assertTrue(list(copy_violations(f'h("p", {{}}, "{word.upper()}");')))

    def test_identifier_exceptions_do_not_hide_adjacent_bad_copy(self):
        for identifier in (
            "c.gate",
            "p.provenance",
            "earlier.provenance",
            "v.provenance",
            "i.hold",
            "x.hold",
            "envelope: p.envelope",
            "p.snapshot",
        ):
            with self.subTest(identifier=identifier):
                self.assertEqual(list(copy_violations(identifier)), [])
                self.assertTrue(
                    list(copy_violations(f'{identifier}; h("dt", {{}}, "Check snapshot");'))
                )
        # Dynamic quotations, facts and user/model text are not application-owned literals.
        for expression in ("source.quote", "fact.text", "answer.reply", "turn.content"):
            self.assertEqual(list(copy_violations(f'h("blockquote", {{}}, {expression});')), [])

    def test_proposal_card_keeps_technical_evidence_in_one_labelled_disclosure(self):
        js = (WEB / "assistants.js").read_text()
        disclosure = js[
            js.index('h("details", { "data-proposal-technical"') : js.index('h("fieldset"')
        ]
        for text in (
            "Suggestion details (technical, for audit and support)",
            "JSON.stringify(p.snapshot, null, 2)",
            "history,",
            "moreHistory",
        ):
            self.assertIn(text, disclosure)
        self.assertNotIn("Edited evidence proposal JSON", js)
        for text in (
            "AI suggestion, not approved",
            "Accept proposal only",
            "Nothing is sent, booked, paid",
        ):
            self.assertNotIn(text, disclosure)

    def test_chat_safety_and_copy_contract(self):
        js = (WEB / "chat.js").read_text()
        for text in (
            "AI suggestion, not approved",
            "only an authorised human can make a restart decision for stopped retrofit work",
            "This panel cannot acknowledge, decide compliance or restart stopped retrofit work.",
            "Check recorded at",
            "These are historical records; ask again for a fresh lookup.",
            "Use the existing human emergency or hazard service now.",
            "Evidence is missing or cannot be relied on. Do not treat this as clear.",
            "Licensed PAS 2035 text and contract incorporation are unverified.",
            "it can only request a proposal that someone else reviews",
        ):
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
        for f in (
            *(ROOT / "src" / "api" / "src" / "zava_forward" / "api").glob("*.py"),
            *(ROOT / "src" / "core" / "src" / "zava_forward" / "core").glob("*.py"),
        ):
            self.assertNotIn(
                "human-approved", f.read_text().replace("human-approved by", ""), f.name
            )
        js = (WEB / "app.js").read_text()
        self.assertIn("This is not an approval, consent or safety decision", js)

    def test_blocked_reasons_have_reason_owner_and_next_action(self):
        c = {
            "decision": {"status": "Asked"},
            "funding_ok": False,
            "owner": "Sam Officer",
            "hazards": [{"released": False, "owner": "Hazard Lead"}],
        }
        reasons = Store.gate_reasons(c)
        self.assertEqual(len(reasons), 3)
        for r in reasons:
            self.assertIn("Owner:", r)
            self.assertIn("Next action:", r)

    def test_saved_check_errors_state_reason_owner_and_next_action(self):
        js = (WEB / "role-screens.js").read_text()
        block = re.search(r"const HELD_CHECK_ERRORS = \{(.*?)\n\};", js, re.S).group(1)
        entries = re.findall(r'^\s*(\d{3}): "(.*)",?$', block, re.M)
        self.assertEqual([s for s, _ in entries], ["400", "403", "404", "409", "502"])
        for status, text in entries:
            reason = text.split("Owner:")[0].split("Next action:")[0].strip()
            self.assertGreater(len(reason), 20, status)
            self.assertRegex(text, r"Owner: [^.]+\.", status)
            self.assertIn("Next action:", text, status)
            self.assertLess(text.index("Owner:"), text.index("Next action:"), status)
            self.assertIsNone(BANNED.search(text), status)

    def test_unreadable_saved_file_message_states_reason_owner_and_next_action(self):
        js = (WEB / "role-screens.js").read_text()
        text = re.search(r'const HELD_CHECK_UNREADABLE = "(.*)";', js).group(1)
        self.assertGreater(len(text.split("Owner:")[0].strip()), 20)
        self.assertRegex(text, r"Owner: [^.]+\.")
        self.assertLess(text.index("Owner:"), text.index("Next action:"))
        self.assertIsNone(BANNED.search(text))

    def test_chat_aftercare_and_shared_failure_messages_state_reason_owner_and_next_action(self):
        def ordered(text, label):
            self.assertIn("Owner:", text, label)
            self.assertIn("Next action:", text, label)
            self.assertLess(text.index("Owner:"), text.index("Next action:"), label)

        for name in ("chat.js", "aftercare.js", "async-action.js", "progress.js"):
            js = (WEB / name).read_text()
            literals = (
                lit
                for line in js.splitlines()
                if line.count("`") % 2 == 0
                for lit in re.findall(r"`[^`]*\.message[^`]*`", line)
            )
            for literal in literals:
                if "Owner:" in literal or "error.message ||" in literal:
                    continue
                if name == "chat.js" and "${feature}" in literal:
                    continue
                with self.subTest(name=name, literal=literal):
                    ordered(literal, literal)
        aftercare = (WEB / "aftercare.js").read_text()
        for const in ("AC_UNCONFIRMED", "AC_EARLIER"):
            literal = re.search(rf'const {const} = "(.*)";', aftercare).group(1)
            ordered(literal, const)
        chat = (WEB / "chat.js").read_text()
        for text in (
            "Chat could not load. Owner: application support. Next action:",
            "is not available for your role. Owner: your team manager. Next action:",
            "is not available right now: ${error.message} Owner: application support. Next action:",
        ):
            self.assertIn(text, chat)
        self.assertIn("Your role cannot do this. Owner:", aftercare)
        self.assertIn("cannot record one. Owner:", aftercare)
        self.assertIn(
            "Next action: change the filters or try again.", (WEB / "progress.js").read_text()
        )

    OWNED_FILES = {
        "ops.js": "opsOwned",
        "assistants.js": "assistantOwned",
        "simulator-control.js": "simControlOwned",
        "staff-intake.js": "intakeOwned",
        "panels.js": "panelOwned",
    }
    BLOCKED_WORDS = re.compile(
        r"cannot|could not|not available|unavailable|failed|not valid|switched off"
        r"|does not include|refused|not writable",
        re.I,
    )
    # Literals that describe a state or a label, not an error or blocked notice, or that feed an owned message.
    NOT_NOTICES = (
        "Resident not available",
        "Sending is permitted until the expiry time. This screen cannot see",
        "Review due date (authority unavailable",
        "AI assistance unavailable. Work continues manually.",
        "These are synthetic exercise rules.",
        "A challenge never means consent, refusal or a sanction.",
        "The existing limits apply:",
    )

    def literals(self, name):
        js = (WEB / name).read_text()
        for line in js.splitlines():
            for lit in re.findall(r'"(?:[^"\\]|\\.)*"|`[^`]*`', line):
                yield line, lit

    def test_remaining_error_and_blocked_notices_state_owner_then_next_action(self):
        for name, helper in self.OWNED_FILES.items():
            js = (WEB / name).read_text()
            self.assertIn(f"const {helper} = (message, owner, next, status) =>", js, name)
            self.assertNotIn("Something went wrong", js, name)
            for line, lit in self.literals(name):
                if not self.BLOCKED_WORDS.search(lit) or lit in (
                    '"unavailable"',
                    '"Unavailable"',
                    '"Not valid"',
                ):
                    continue
                if any(skip in lit for skip in self.NOT_NOTICES) or f"{helper}(" in line:
                    continue
                with self.subTest(name=name, literal=lit[:80]):
                    self.assertIn("Owner:", lit)
                    self.assertIn("Next action:", lit)
                    self.assertLess(lit.index("Owner:"), lit.index("Next action:"))
                    self.assertIsNone(BANNED.search(lit))

    def test_dynamic_error_messages_always_go_through_the_owner_helper(self):
        sink = re.compile(
            r"\b(?:e|error|d\.error)\.message\b|\bvalidationMessage\b|\.(?:blocker|not_ready_reason)\b"
        )
        for name, helper in self.OWNED_FILES.items():
            for n, line in enumerate((WEB / name).read_text().splitlines(), 1):
                if not sink.search(line) or line.lstrip().startswith("const " + helper):
                    continue
                if (
                    re.search(
                        r"\.message\s*=\s*`|const (reason|detail)\b|e\.generic|error\.message \|\||\.message,",
                        line,
                    )
                    and "Owned(" not in line
                ):
                    continue
                with self.subTest(file=name, line=n):
                    self.assertTrue(helper + "(" in line or "Owner:" in line, line.strip()[:160])

    def test_owner_helpers_keep_complete_messages_and_complete_partial_ones(self):
        for name, helper in self.OWNED_FILES.items():
            js = (WEB / name).read_text()
            fn = re.search(rf"const {helper} = .*?\n}};", js, re.S).group(0)
            script = (
                fn
                + f"""
const full = "It failed. Owner: app support. Next action: retry.";
const out = [
  {helper}(full, "X", "Y"),
  {helper}("It failed", "X", "Y"),
  {helper}("It failed. Owner: someone.", "X", "Y"),
  {helper}("Next action: retry. Owner: someone.", "X", "Y"),
  {helper}(undefined, "X", "Y"),
  {helper}("Ask the contract manager.", "X", "Y", 403),
  {helper}("Server fault", "X", "Y", 500),
];
console.log(JSON.stringify(out));
"""
            )
            result = subprocess.run(
                ["node", "-e", script], text=True, capture_output=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            got = json.loads(result.stdout)
            self.assertEqual(got[0], "It failed. Owner: app support. Next action: retry.", name)
            for text in got[1:4]:
                self.assertRegex(text, r"Owner: [^.]+\. Next action: ", name)
            self.assertEqual(got[1], "It failed. Owner: X. Next action: Y", name)
            self.assertIn("Owner: X. Next action: Y", got[4], name)
            self.assertIn(
                "Owner: your team manager. Next action: follow the advice above", got[5], name
            )
            self.assertNotIn("Owner: X", got[5], name)
            self.assertEqual(got[6], "Server fault. Owner: X. Next action: Y", name)

    def test_standard_documents_glossary_and_review(self):
        for text in (
            "## Glossary",
            "## Copy audit of the core flow",
            "AI suggestion, not approved",
            "named human",
            "Reason",
            "Owner",
            "Next action",
        ):
            self.assertIn(text, DOC)

    def test_resident_draft_and_representative_copy_boundaries(self):
        js = (WEB / "app.js").read_text()
        self.assertIn("Draft a message for review", js)
        self.assertNotIn('"Write to the resident"', js)
        self.assertIn(
            "Draft only. Nothing is sent here. A named human must review the exact wording before any resident use.",
            js,
        )
        self.assertIn(
            "Reviewing a draft is not approval of works, resident consent or a safety decision.", js
        )
        panels = (WEB / "panels.js").read_text()
        self.assertIn("Review due date (authority unavailable from this date)", panels)
        self.assertNotIn("authority held from this date", panels)

    def test_proposal_review_copy_is_not_decision_approval(self):
        js = (WEB / "assistants.js").read_text()
        self.assertIn("AI suggestion, not approved", js)
        self.assertIn(
            "Accepting or editing this proposal records a draft review. This is not an approval, consent or safety decision.",
            js,
        )
        self.assertIn("Requested using:", js)
        self.assertNotIn("Invocation:", js)
        self.assertIn("Accept proposal only", js)
        self.assertIn('onclick: () => act("edit-accept") }, "Save edited proposal"', js)
        self.assertIn(
            "as a draft by a person. This is not an approval, consent or safety decision.", js
        )
        self.assertIn("Confidence: not provided. Confidence is not accuracy.", js)

    def test_generic_error_and_ranking_error_state_reason_owner_next_action(self):
        js = (WEB / "app.js").read_text()
        self.assertNotIn("Something went wrong", js)
        self.assertIn("e.generic = !data.error", js)
        self.assertIn("check the recorded history before repeating a change", js)
        self.assertIn("body === undefined ? GENERIC_READ_ERROR : GENERIC_CHANGE_ERROR", js)
        self.assertIn("refresh to try again", js)
        self.assertNotIn("This did not complete", js)
        self.assertIn(
            "Owner: application support. Next action: try All sources", (WEB / "law.js").read_text()
        )
        with self.assertRaises(PermissionError) as ctx:
            Store.ranking_snapshot(object(), {"role": "Resident"})
        for part in ("Only a manager", "Owner:", "Next action:"):
            self.assertIn(part, str(ctx.exception))
        self.assertNotIn("snapshot", str(ctx.exception).lower())

    def test_role_screen_law_and_server_notices_state_reason_owner_then_next_action(self):
        role = (WEB / "role-screens.js").read_text()
        law = (WEB / "law.js").read_text()
        server = (ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "server.py").read_text()
        notices = [
            (role, "This screen is not installed for your signed-in role. Your access has not changed."),
            (role, "That page could not be loaded. The rows shown are unchanged."),
            (role, "is not installed for your role. Your access has not changed."),
            (role, "Unknown. The queue could not be read for your role."),
            (role, "This file is incomplete or was changed after download."),
            (law, "Required law viewer file did not load: /async-action.js."),
            (server, "The service hit an unexpected error."),
        ]
        for source, start in notices:
            with self.subTest(notice=start):
                self.assertEqual(source.count(start), 1)
                text = source[source.index(start):].split('"')[0].split("`")[0]
                self.assertRegex(text, r"Owner: [^.]+\. Next action: ")
        self.assertIn("/Owner:/.test(e.message) ? e.message :", law)

    def test_role_screens_use_phase_check_wording(self):
        js = (WEB / "role-screens.js").read_text()
        self.assertIn("Benefits and phase check", js)
        self.assertTrue(
            list(copy_violations(js.replace("phase check evidence", "gate evidence", 1)))
        )

    def test_finance_decision_sources_contain_display_mapping(self):
        panels = (WEB / "panels.js").read_text()
        self.assertIn('{ value: "Keep on hold", label: "Keep payment paused" }', panels)
        self.assertIn("Finance decision: ${financeDecisionLabel(i.disposition)}", panels)
        self.assertIn(
            "screenFinanceDecision(inv.disposition)", (WEB / "role-screens.js").read_text()
        )

    def test_finance_and_ai_review_refusals_use_plain_wording(self):
        core = ROOT / "src" / "core" / "src" / "zava_forward" / "core"
        pattern = re.compile(r'raise (?:ValueError|PermissionError)\((f?"[^"\n]*")')
        for name in ("finance.py", "ai_tasks.py"):
            for literal in pattern.findall((core / name).read_text()):
                with self.subTest(name=name, literal=literal):
                    self.assertFalse(re.search(r"\bon hold\b|\bthe hold\b", literal), literal)
        text = (core / "finance.py").read_text()
        self.assertIn("A different Finance user must restart payment first", text)

    def test_safety_restart_refusals_use_plain_wording(self):
        core = ROOT / "src" / "core" / "src" / "zava_forward" / "core"
        pattern = re.compile(r'raise (?:ValueError|PermissionError)\(\s*((?:f?"[^"\n]*"\s*)+)')
        for name in ("workflows.py", "hazard.py"):
            for literal in pattern.findall((core / name).read_text()):
                with self.subTest(name=name, literal=literal):
                    self.assertFalse(
                        re.search(
                            r"retrofit hold|hold release|release (?:a|the|this)\b[^\"]*hold",
                            literal,
                        ),
                        literal,
                    )

    def test_consultation_and_restart_gate_refusals_use_plain_wording(self):
        core = ROOT / "src" / "core" / "src" / "zava_forward" / "core"
        for name in ("procurement.py", "gates.py"):
            text = (core / name).read_text()
            for literal in re.findall(r'"[^"\n]*"', text):
                with self.subTest(name=name, literal=literal):
                    self.assertFalse(
                        re.search(r"(?:release|releases|released) (?:this|the) hold", literal),
                        literal,
                    )
        self.assertIn(
            "Next action: ask Legal to verify the decision.", (core / "procurement.py").read_text()
        )

    def test_document_control_refusals_use_plain_wording(self):
        text = (
            ROOT / "src" / "core" / "src" / "zava_forward" / "core" / "doc_controls.py"
        ).read_text()
        self.assertNotIn("A legal hold blocks deletion on this case.", text)
        self.assertNotIn("is not past its retention trigger", text)
        self.assertIn(
            "A legal hold is in place on this case (its documents must be kept for a legal reason)",
            text,
        )
        self.assertIn("This document is not due for deletion, so nothing was deleted.", text)

    def test_time_capture_copy_is_guarded(self):
        self.assertIn("timecapture.js", AUDITED_FILES)
        js = (WEB / "timecapture.js").read_text()
        corrected = "have the same role as the requester"
        self.assertIn(corrected, js)
        self.assertTrue(
            list(copy_violations(js.replace(corrected, "hold the same role as the requester")))
        )


if __name__ == "__main__":
    unittest.main()
