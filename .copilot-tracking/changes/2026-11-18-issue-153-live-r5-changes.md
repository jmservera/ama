---
title: Issue 153 live r5 changes
ms.date: 2026-11-18
---

Refs #153. Plan: [plan](../plans/2026-11-18-issue-153-live-r5-plan.md). Tier FULL (src change); the complete gate was
not run (owner instruction); nothing pushed or deployed.

## Files

* `src/core/src/zava_forward/core/exposure_limits.py`: reason says "investment limit", not "envelope".
* `src/api/src/zava_forward/api/web/panels.js`: Finance panel shows `Held` as "Paused" and rewrites "envelope".
* `src/api/src/zava_forward/api/web/app.js`: "Unassigned" owner fallbacks replaced with "No one named yet. Next action: ask the case lead to name one" (7 sites).
* Tests: `test_exposure_limits.py`, `test_finance_exposure_screen.py`, `test_handoff_waiting_view.py`.
* Docs: `wording-defects-fix-153-live-r5-2026-11-18.md`, index and log entries.

## Divergence record

* A first draft overwrote the previous run's tracked artifacts and edited source before this file existed; both were
  reverted (`git checkout`) and the `r5` suffix used. The witness refused `implement-start` once (changes path missing
  from the state file), then accepted.
* A shared JS constant broke 4 tests that slice `app.js` at other markers; the text was inlined (correction cycle 1).

## Validation

| Command | Result |
| --- | --- |
| `src/core` unittest `test_exposure_limits`, `test_issue_99_acceptance`; finance pattern | OK (33; 91) |
| `src/api` handoff, finance, content, accessibility modules (166 tests) | OK, 13 skipped |
| `python3 -m mypy` in `src/core` and `src/api` | Success |
| `ruff format --isolated --line-length 100 --check`, `ruff check` on changed Python | Clean |
| Full `src/core` discover run | Started; output tail was timing lines only, no pass/fail summary captured, so not claimed |
| `rpi-checks.py --all` | Not run (owner instruction) |

## Per-criterion table

| Criterion | Result |
| --- | --- |
| Content standard and glossary exist | Proven |
| Copy audit removes gate, hold, provenance, trace | Proven in source for Finance; live only after redeploy |
| Errors state reason, owner, next action | Partly proven; generic API bodies still reason-only |
| AI suggestion, not approved | Proven live (second audit), not re-run |
| Resident wording reviewed by a named human | Unproven; needs a named person's recorded review |
