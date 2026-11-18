---
title: Issue 215 live re-verification changes (run 3)
ms.date: 2026-11-18
---

Refs #215. Tier FOCUSED: docs and evidence only; no `src/` edit, so FULL is not triggered and `rpi-checks.py --all` was not run.

## Files

| File | Change |
| --- | --- |
| `docs/reference/research/issue-215-live-rerun3-evidence-2026-11-18.md` | New research note with observations and per-criterion table |
| `docs/reference/README.md`, `docs/reference/log.md` | Index row and log entry |
| `.copilot-tracking/evidence/2026-11-18/issue-215-live-r3/` | Scripts and redacted JSON (screenshots not retained) |
| `.copilot-tracking/rpi-sessions/2026-11-18/issue-215-live-state.json` | Overwritten from the earlier run (same mandated path); earlier content is in commit 1a79804d1 |

## Per-criterion status (unticked and related criteria)

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 3a | No colour-only status | Partly proven | Live unknown state has marker and word; three populated states proven with mocked data (run 2) |
| 3b | Keyboard operable | Proven for reachable controls | Tab, Space, Enter, Escape walks; home chat open and close with focus return re-confirmed |
| 3c | Plain-language mode | Partly proven | Show and hide proven with mocked data; no announced state in the deployed image |
| 3 | WCAG 2.2 AA overall | Unproven | Automation only; axe incomplete on contrast overlap; clipped helper line open; person-run testing waived |
| 5 | Comprehension with staff | Unproven, cannot be proven for the demo | No real staff; none may be simulated |
| 2 | Alert fields (ticked) | Not provable live | Law store not loaded; mocked data only |

## Notes

* Witness: the first `plan-done` call was refused (`missing persisted artifact evidence: plan, details, critique`) because I mistyped three artifact file names; I renamed them and the second call succeeded. The refusal remains in the witness log.
* Azure: read-only `az containerapp show`; nothing created, so nothing to delete.
