---
title: Issue 153 wording defect fix and per-criterion result, 2026-11-18
description: Source fix for the Finance limit wording and the handoff owner wording recorded in the live re-checks, with local test evidence and a proven and unproven result for each acceptance criterion
ms.date: 2026-11-18
ms.topic: reference
---

Refs #153. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 apply: DPO and Legal approval,
Azure billing reconciliation and person-run assistive-technology testing are not needed for the demo. This run changed
source, so it is a FULL-tier candidate; the full gate was not run (owner instruction) and nothing was pushed or
deployed. No Azure resource was created, so nothing needed deleting.

## Defects fixed

| Id | Before (live revision `0000032`, from the [fourth re-check](content-recheck-153-live-r4-2026-11-18.md)) | After (source) |
| --- | --- | --- |
| R1, N3 | Finance: "Pause for human decision. Held. No person-approved envelope or tolerances are recorded." | "Pause for human decision. Paused. No person-approved investment limit or tolerances are recorded." Stored status `Held` is unchanged; `panels.js` maps it for display and replaces "envelope" in the reason and finding labels |
| R2, N1, N2 | Handoff lists, handoff tab, waiting table: "Unassigned" for chase owner, proposed receiver and resident update owner | "No one named yet. Next action: ask the case lead to name one" (`app.js`); the waiting sentence says "a receiver not yet named" |

Not changed (residual): N4 to N6, the Source line F1, generic error bodies R5 to R7, the safety-clock "unassigned"
flag, `exceptionRoleLabel` and one other owner fallback in `app.js`.

## Evidence

* `src/core`: `test_exposure_limits.py`, `test_issue_99_acceptance.py` and the finance tests pass (33 and 91 tests).
* `src/api`: finance, handoff, content-standard and accessibility-baseline modules, 166 tests, OK (13 opt-in browser
  cases skipped). New cases: Held shown as Paused with no "envelope" (`test_finance_exposure_screen.py`), no
  "Unassigned" in the waiting table (`test_handoff_waiting_view.py`), exact core reason (`test_exposure_limits.py`).
* `python3 -m mypy` clean in `src/core` (396 files) and `src/api` (347 files); `ruff format --isolated
  --line-length 100 --check` and `ruff check` clean on the changed Python files.
* The live demo still serves revision `0000032` without this change (no production change was authorised), so the
  fix is proven by rendering the shipped JavaScript in Node, not by a new live screenshot. The test, mypy, ruff and Node rendering results above are observed; raw output not retained. Independent review re-ran `test_exposure_limits` (21 tests) and nine related api modules (89 tests, 11 skipped), all OK.

## Per-criterion result

| Criterion | Issue state | Result | Evidence |
| --- | --- | --- | --- |
| Content standard and glossary exist | Ticked | Proven | `ux/content-standard.md` present |
| Copy audit removes gate, hold, provenance, trace from the core flow | Ticked | Proven in source for Finance (Held, envelope); live demo proves it only after redeploy | Tests above; R1 |
| Error and blocked messages state reason, owner, next action | Ticked | Partly proven: handoff owner text now gives a next action; generic API bodies (R5 to R7) still give a reason only | Tests above; fourth re-check |
| AI suggestion text says "AI suggestion, not approved" | Ticked | Proven live in the [second audit](content-audit-live-153-2026-11-18.md) (P2, P5); not re-run | Second audit |
| Resident wording reviewed by a named human | Unticked | Unproven. A review record needs a named person, role, date, exact text and outcome; none exists and an automated run cannot supply one | Fourth re-check, record search |
