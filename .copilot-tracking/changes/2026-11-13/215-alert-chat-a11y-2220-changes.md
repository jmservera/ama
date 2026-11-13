---
title: Issue 215 alert and chat WCAG cue changes
description: Changes record for criterion 3 software and markup gaps
ms.date: 2026-11-13
---

## Related plan

[.copilot-tracking/plans/2026-11-13/215-alert-chat-a11y-2220-plan.instructions.md](../../plans/2026-11-13/215-alert-chat-a11y-2220-plan.instructions.md)

## Changes

* `src/api/src/zava_forward/api/web/chat.js`: state classes on alert headings, chat outcome headings, the no-source item, sent doubt button and unknown-coverage status; plain explanations for chat outcomes, no-source and doubt route; Escape closes the lookup disclosure and focuses its summary.
* `src/api/src/zava_forward/api/web/style.css`: glyph (empty alternative) and border-shape rules per state; list-item display for plain explanations in lists.
* `src/api/tests/test_regulatory_a11y_cues.py` (new): static checks.
* `src/api/checks/regulatory_ux_check.py`: `assert_state_cue` and Escape assertions.
* `src/api/README.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md`: dated, bounded evidence notes.

## Amendments and divergences

* Plan details said unrecognised states fall back to unknown; implemented with an allow-list set.
* No divergence from scope: no queue screens, `infra/` or ranking files touched.

## Validation (focused tier, `/tmp/venv-215-2220`, pip)

| Check | Result |
| --- | --- |
| `src/api` 14 modules (193 tests: chat, alerts, a11y baseline, content standard, design system, cues, ux check) | OK, 1 skipped |
| `src/core` `test_regulatory_chat`, `test_regulatory_privacy` (43 tests) | OK |
| Browser check `checks.regulatory_ux_check --axe` (pinned axe 4.10.3, hash verified) | PASS, 21 states, keyboard, reflow, new cue and Escape assertions |
| `ruff check` (src/api) and `ruff format --check` on new files | clean |
| `mypy` (src/api) | no issues in 240 files |

Not run: full `tools/rpi-checks.py` gate (not required for the focused tier), screen reader and assistive technology tests, hosted CI.
