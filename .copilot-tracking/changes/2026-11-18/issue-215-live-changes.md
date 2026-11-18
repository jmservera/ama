---
title: Issue 215 live proof changes record
description: Files changed and per-criterion proven or unproven table for issue 215
ms.date: 2026-11-18
---

## Changes

* Added `docs/reference/research/issue-215-live-alert-chat-ux-evidence-2026-11-18.md`.
* Added index entry in `docs/reference/README.md` and log entry in `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-215-live/` (three scripts, redacted JSON, six screenshots).
* No `src/` change. Azure was read-only: nothing created, so nothing to delete.

## Per-criterion table

| Criterion | Proven for the demo? | Basis |
| --- | --- | --- |
| Patterns defined per role (ticked) | Not re-tested | Already ticked |
| Each alert states noticed, source, status, safe action, owner, clock (ticked) | Not provable live | Demo law store not loaded; zero alert cards render |
| WCAG 2.2 AA: no colour-only status | Partly proven | Unknown state has marker and word; other states unreachable |
| WCAG 2.2 AA: keyboard operable | Proven for reachable controls | Tab, Space, Enter, Escape and focus return; axe 0 violations |
| WCAG 2.2 AA: plain-language mode | Partly proven | Toggle works by keyboard but shows no visible effect and no announced state on the deployed image |
| WCAG 2.2 AA overall | Unproven | Automation is not conformance; assistive-technology testing waived for the demo |
| Doubt route and no-source states (ticked) | Observed | Unknown state and doubt owner text seen |
| Comprehension tested with staff | Cannot be proven for the demo | Needs real staff participants; kit stays "Not run" |

## Validation

Focused tier. Documentation link and diff review, redaction review of screenshots, literal credential scan of text evidence (no match). No unit tests or mypy/ruff apply (no source or Python under `src/` or `infra/` changed). `rpi-checks.py --all` not run.
