# Changes: regulatory alerts and home chat WCAG 2.2 AA (Issue #215 AC3)

Date: 2026-11-14. Plan: [plan](../plans/2026-11-14-regulatory-alerts-wcag-215-plan.md).

| File | Change |
| --- | --- |
| `src/api/src/zava_forward/api/web/chat.js` | `regulatoryStateLabel`; per-alert plain-language summary; alert `aria-labelledby` |
| `src/api/tests/test_regulatory_a11y_cues.py` | new test for known-word label, summary and article name; updated heading assertion |
| `src/api/tests/test_alert_chat_role_wcag_plain_matrix.py` | heading assertion follows the label helper |

No divergence from plan. `src/agents` and `role-screens.js` unchanged.

Validation: `ruff check` and `ruff format --line-length 100 --check` on `src/api` pass; `src/agents` unchanged. Focused tests (a11y cues, keyboard provenance, role/plain matrix, chat panel a11y, origin badge) pass: 80 tests. Wider run (accessibility baseline, regulatory UX check, chat panel, design system, a11y cues, matrix): 109 tests OK, 1 skipped. Tier: focused (web-only static change, no gate, infra or security control). Not run: complete local gate, hosted CI, browser or assistive-technology checks.
