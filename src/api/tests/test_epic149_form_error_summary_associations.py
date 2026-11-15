"""Epic #149: form validation error associations, summary recovery anchors and plain copy.

Static engineering evidence over the workbench scripts in ``web/``. It is not WCAG conformance,
assistive-technology or browser-rendered acceptance, which stay with human testers. The counted
``setAttribute("aria-invalid", "true")`` baseline lives in ``test_accessibility_baseline.py`` and
this module only reads it.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
BASELINE_TEST = Path(__file__).with_name("test_accessibility_baseline.py")

# One row per counted site: (file, invalid line, describedby fragment, message element fragment).
SITES = (
    (
        "assistants.js",
        'field.setAttribute("aria-invalid", "true")',
        'field.setAttribute("aria-describedby", error.id)',
        "id: `proposal-error-${p.id}`",
    ),
    (
        "ops.js",
        'note.setAttribute("aria-invalid", "true")',
        'note.setAttribute("aria-describedby", message.id)',
        "id: `quality-feedback-${i}`",
    ),
    (
        "ops.js",
        'contractVersion[1].setAttribute("aria-invalid", "true")',
        'setAttribute("aria-describedby", "capacity-version-error")',
        'id: "capacity-version-error"',
    ),
    (
        "ops.js",
        'control.setAttribute("aria-invalid", "true")',
        '"aria-describedby": `${id}-error`',
        "id: `${id}-error`",
    ),
    (
        "progress.js",
        'input.setAttribute("aria-invalid", "true")',
        'input.setAttribute("aria-describedby", message.id)',
        "id: `${input.id}-error`",
    ),
    (
        "app.js",
        'why.setAttribute("aria-invalid", "true")',
        'why.setAttribute("aria-describedby", error.id)',
        "id: `ai-error-${d.record_id}`",
    ),
    (
        "panels.js",
        'input.setAttribute("aria-invalid", "true")',
        '"aria-describedby": status.id',
        "id: `${key}-feedback`",
    ),
    (
        "role-screens.js",
        'input.setAttribute("aria-invalid", "true")',
        '"aria-describedby": `${id}-error`',
        "id: `${id}-error`",
    ),
)
# Sites that rely on native validation or a later check rather than moving focus when they mark
# the field. Recorded gaps, shrink-only: a fix must remove the entry so the check then enforces it.
NO_FIELD_FOCUS = {
    ("ops.js", 'control.setAttribute("aria-invalid", "true")'),
    ("progress.js", 'input.setAttribute("aria-invalid", "true")'),
    ("role-screens.js", 'input.setAttribute("aria-invalid", "true")'),
}
# Message elements that take programmatic focus themselves, so recovery has a focus target.
FOCUSABLE_MESSAGE = {
    "ops.js": "tabindex: -1",
    "app.js": "error.tabIndex = -1",
    "panels.js": "tabindex: -1",
}
# Error copy shown for these sites; each states the fix in plain words.
RECOVERY_COPY = (
    ("assistants.js", "Enter a reason to edit or reject this proposal."),
    ("assistants.js", "Enter valid JSON for the edited evidence proposal."),
    ("ops.js", "Enter the remediation evidence before recording the fix."),
    ("ops.js", "Enter the contract or call-off version before creating the package."),
    ("app.js", "Enter a reason to edit or reject this draft."),
    ("panels.js", "before recording this challenge."),
)
RAW_ERROR = re.compile(
    r"traceback|\.stack\b|\[object|\bundefined\b|\bNaN\b|Uncaught|TypeError|ReferenceError|"
    r"SyntaxError|Exception:",
    re.I,
)


def source(name: str) -> str:
    return (WEB / name).read_text()


def window(text: str, needle: str, before: int = 8, after: int = 8) -> str:
    lines = text.splitlines()
    for number, line in enumerate(lines):
        if needle in line:
            return "\n".join(lines[max(number - before, 0) : number + after + 1])
    raise AssertionError(f"not found: {needle}")


class FormErrorAssociations(unittest.TestCase):
    def test_counted_baseline_is_unchanged_and_fully_mapped(self) -> None:
        # The baseline test pins eight setAttribute sites; this table must map exactly those.
        self.assertIn("self.assertEqual(sites, 8,", BASELINE_TEST.read_text())
        found = sum(
            line.count('setAttribute("aria-invalid", "true")')
            for path in sorted(WEB.glob("*.js"))
            for line in path.read_text().splitlines()
        )
        self.assertEqual(found, 8)
        self.assertEqual(len(SITES), found)
        for name, invalid, _, _ in SITES:
            self.assertIn(invalid, source(name), name)

    def test_each_invalid_site_names_an_existing_message_element(self) -> None:
        for name, invalid, describedby, message in SITES:
            text = source(name)
            with self.subTest(file=name, site=invalid):
                self.assertIn(describedby, text)
                self.assertIn(message, text)
                self.assertNotIn("aria-errormessage", describedby)

    def test_aria_errormessage_is_not_used_without_a_matching_id(self) -> None:
        # No script uses aria-errormessage today; a new use must point at an element with that id.
        for path in sorted(WEB.glob("*.js")) + sorted(WEB.glob("*.html")):
            text = path.read_text()
            for target in re.findall(r'aria-errormessage["\']?\s*[:=,]\s*["\']?([\w-]+)', text):
                self.assertRegex(
                    text, rf'id[=:]\s*["\']{re.escape(target)}["\']', f"{path.name}:{target}"
                )

    def test_marking_a_field_invalid_moves_focus_or_records_the_gap(self) -> None:
        for name, invalid, _, _ in SITES:
            key = (name, invalid)
            with self.subTest(file=name, site=invalid):
                around = window(source(name), invalid, 4, 4)
                if key in NO_FIELD_FOCUS:
                    self.assertNotRegex(
                        around, r"\.focus\(\)", "gap fixed: remove it from NO_FIELD_FOCUS"
                    )
                else:
                    self.assertRegex(around, r"\.focus\(\)")

    def test_focus_target_message_elements_are_programmatically_focusable(self) -> None:
        for name, marker in FOCUSABLE_MESSAGE.items():
            self.assertIn(marker, source(name), name)

    def test_aftercare_summary_exposes_anchors_to_each_field_outside_the_baseline(self) -> None:
        # aftercare.js sets aria-invalid through a spread attribute, so it is not a counted site.
        text = source("aftercare.js")
        self.assertNotIn('setAttribute("aria-invalid"', text)
        field = window(text, '"aria-invalid": error ? "true" : undefined', 8, 30)
        self.assertIn('"aria-describedby": error ? errId : undefined', field)
        self.assertIn("const errId = `${id}-error`;", text)
        self.assertIn('h("p", { id: errId, class: "field-error" }', field)
        summary = window(text, 'id: "ac-error-summary"', 1, 4)
        self.assertIn('tabindex: "-1"', summary)
        self.assertIn('role: "alert"', summary)
        self.assertIn('h("a", { href: `#ac-${name}` }, text)', summary)
        self.assertIn("const id = `ac-${spec.name}`;", text)
        self.assertIn(
            "acFocus(Object.keys(result.errors).length"
            ' ? document.getElementById("ac-error-summary")',
            text,
        )
        self.assertRegex(
            text,
            r"function acFocus\(node\) \{\s*if \(!node\) return;"
            r"\s*node\.tabIndex = -1;\s*node\.focus\(\);",
        )

    def test_error_copy_gives_recovery_guidance_not_raw_exceptions(self) -> None:
        for name, fragment in RECOVERY_COPY:
            with self.subTest(file=name, copy=fragment):
                text = source(name)
                self.assertIn(fragment, text)
                line = next(row for row in text.splitlines() if fragment in row)
                copy = line[line.index(fragment) :]
                self.assertNotRegex(copy[:200], RAW_ERROR)
        for name in ("ops.js",):
            self.assertIn(
                "Next action:", window(source(name), "Enter the contract or call-off version", 0, 0)
            )
        async_action = source("async-action.js")
        self.assertIn("Owner: application support. Next action:", async_action)
        self.assertIn("opsOwned(control.validationMessage,", source("ops.js"))

    def test_no_script_renders_stack_traces_to_people(self) -> None:
        for path in sorted(WEB.glob("*.js")):
            text = path.read_text()
            with self.subTest(file=path.name):
                self.assertNotRegex(text, r"\.stack\b|traceback", path.name)
                self.assertNotRegex(text, r"textContent\s*=\s*String\((?:err|error|e)\)")
                self.assertNotRegex(text, r"textContent\s*=\s*(?:err|error|e)\.toString\(\)")
                self.assertNotRegex(text, r"textContent\s*=\s*JSON\.stringify\((?:err|error|e)\b")


if __name__ == "__main__":
    unittest.main()
