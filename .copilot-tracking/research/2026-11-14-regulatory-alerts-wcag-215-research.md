# Research: regulatory alerts and home chat WCAG 2.2 AA (Issue #215 AC3)

Date: 2026-11-14. Branch: `feat/ux-215-regulatory-alerts-wcag-1840`, stacked on `origin/feat/demo-164-chat-grounding-provenance-0900`. Research disposition: executed. Planning Readiness: Ready.

## Scope

AC3: no colour-only status, keyboard operable, plain-language mode for regulatory alerts and home chat. `role-screens.js` is out of scope and untouched. `src/agents` holds no alert or chat panel rendering (checked by search); rendering is in `src/api/src/zava_forward/api/web/chat.js` and `style.css`.

## Findings

* Already present: `regulatory-state` border plus glyph classes per state (`style.css`), `Status:` and `Lookup status:` text headings, native `details`/`button`/`input`, Escape on the lookup disclosure, refresh focus return, live regions, plain-language checkbox with announced state (`regulatoryPlainMode`), `plain-explanation` copy per outcome.
* Existing static tests: `test_regulatory_a11y_cues.py`, `test_home_chat_regulatory_keyboard_provenance.py`, `test_alert_chat_role_wcag_plain_matrix.py`, `test_chat_panel_accessibility.py` (aliased by `test_alert_chat_*`).
* Gap 1: alert heading printed the raw `alert.result`. An unrecognised or missing value rendered text such as `Status: undefined` while the class fell back to `unknown`, so text and shape cue disagreed.
* Gap 2: alerts had no per-alert plain-language summary (home chat answers have `plain_summary`). The plain mode only toggled generic meaning copy.
* Gap 3: alert articles had no accessible name tying them to their status heading.

## Limits

Static source checks only. No screen reader, assistive technology or staff comprehension evidence; no conformance claim.
