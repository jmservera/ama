---
title: Issue 215 run 2 changes
ms.date: 2026-11-18
---

Tier: FOCUSED. No `src/` change; `rpi-checks.py --all` not run. The research note was drafted during the proof phase, before `implement-start` was called; no source file was edited at any point.

## Files

* Added `docs/reference/research/issue-215-live-populated-states-evidence-2026-11-18.md`.
* Updated `docs/reference/README.md` (index) and `docs/reference/log.md` (append).
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-215-live/` (scripts, JSON, five screenshots, axe SHA-256).
* RPI artifacts `*-r2-*`, new `issue-215-live-r2-state.json` and preserved `issue-215-live-state-run1.json`; the main `issue-215-live-state.json` is unchanged. The duplicate `mocked-alert-states.png` (identical to the live coverage-unknown panel image) was removed, so `prove.py` line 77 names a file that is no longer retained.

## Per-criterion result

| # | Criterion | Proven or unproven for the demo |
| --- | --- | --- |
| 1 | Patterns per role | Already ticked; not re-tested (one role available) |
| 2 | Alert states noticed, source, status, safe action, owner, clock | Already ticked; client rendering proven with mocked data only; real alerts unprovable (law store not loaded) |
| 3a | No colour-only status | Proven for three mocked states (text, marker, border style) |
| 3b | Keyboard operable | Proven for reachable controls |
| 3c | Plain-language mode | Proven show and hide (mocked); announced state absent in deployed build |
| 3 | WCAG 2.2 AA overall | Unproven; automation is not conformance; left unticked |
| 4 | Doubt route and no-source states | Already ticked; observed live and mocked |
| 5 | Staff comprehension tested | Unproven; needs real staff, cannot be simulated |

## Validation

* Literal scan of all text evidence for each credential value: no matches.
* Screenshots viewed; no account name or secret.
* Documentation link and diff review. Azure: nothing created or changed, nothing to delete.
