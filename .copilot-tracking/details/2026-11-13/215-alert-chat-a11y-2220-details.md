<!-- markdownlint-disable-file -->
# Implementation Details: Issue 215 alert and chat WCAG cues

## Phase 1

### Step 1.1: state classes (`chat.js`)

* Alert `h3` gets `class: "regulatory-state state-<slug>"` where slug is the result with spaces as hyphens (`breach-risk`, `attention`, `unknown`, `clear`, `not-applicable`); unrecognised results use `state-unknown`.
* Chat turn `h3` gets `state-answer`, `state-refused` or `state-conflict` (unrecognised: `state-unknown`).
* No-source list item gets `state-no-source`; the doubt button and its receipt text get `state-sent` once sent; unavailable and unknown-coverage notices get `state-unknown` on the status element and clear it on success.

### Step 1.2: CSS (`style.css`)

* `.regulatory-state:before` generated glyph with empty alternative text (decorative), distinct glyph per state, plus distinct left border style (solid, double, dashed, dotted) so shape differs without colour.
* Keep ASCII-safe escapes; no new fixed-position rules, no `outline:none`, no `transition: all`.

## Phase 2

### Step 2.1: plain explanations

* Per-outcome text: answer (sources found, not a decision), refused (no supported lookup, ask owner), conflict (sources disagree, owner compares).
* No-source: nothing held, open question, ask named owner.
* Doubt: sending asks a person to check; it approves nothing.
* Unknown coverage: not clear, use human route.
* Wording uses the content-standard glossary; no gate, hold, provenance, trace, envelope or snapshot.

### Step 2.2: Escape

* Keydown on the `details` root: when open and key is Escape, prevent default, set `open=false`, focus the summary. Native Enter/Space on summary unchanged.

## Phase 3

* New `src/api/tests/test_regulatory_a11y_cues.py`: static checks on `chat.js` and `style.css` (state classes, glyph rules have empty alternative and non-colour border rule, Escape handler restores summary focus, every plain-language explanation avoids banned terms, `aria-invalid` not added).
* Extend `regulatory_ux_check.py` with Escape and state-cue assertions.
* Update README criterion audit and WCAG baseline with dated engineering evidence and residuals.
