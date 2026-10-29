---
title: Case journey round nine details
description: Raw presentation lifecycle and validation ownership
ms.date: 2026-10-29
---

Task 526-round9. Explicit original user direction selects this child correction;
round-eight original Review and source committed in 24d7ca9c. No new decision.

<!-- rpi:phase id=P01 -->
## P01

<!-- rpi:task id=P01-T01 -->
### P01-T01

One shared raw-form presentation helper binds session/form-key state to the
latest rendered form. Pending, message and history-required presentation survive
reconstruction. Outcome updates render to the current node, not only detached
original closures. Transport locks remain at api.

restoreChallengeDrafts must synchronize restored whole-form controls after
caseView accepts a causally current GET. Pending presentation stays disabled;
global history barrier remains authoritative. Never clear that barrier here.
Newly constructed resident forms bind the same state automatically.

Implemented: session.rawFormStates owns pending/message/history presentation.
Restoration rebinds the renderer to the retained whole form. Input/reset events
may clear ordinary validation feedback but cannot erase pending/history status.
Error focus targets the latest renderer. Successful writes with failed reload
retain explicit history instructions; no presentation path clears the barrier.
Preserve the distinct acknowledged-success rule: later edits in the actual
submitted challenge form remain guarded against repeating its already-recorded
action. Presentation retains that exact form identity, not a global pending
lock. Explicit confirmed draft discard clears this guard; a newly built form
with current tokens is not the acknowledged original. History recovery alone
does not authorize repeating an acknowledged action.

<!-- rpi:task id=P01-T02 -->
### P01-T02

Extend the existing shipped-code raw matrix through reconstruction with no
duplicate click, all structured/malformed outcomes, mounted feedback and retry
after recovery. Extend existing journey helper through normal retained challenge
refresh and fresh-handler reconstruction, with visible status, input retention,
dispatch counts and axe. Add a bounded restore unit only if existing matrix
cannot faithfully exercise retained DOM. No removals or new browser helper.

Implemented within existing owners: the raw unit matrix executes actual shipped
capture/restore and mounted feedback, successful/failed reloads and corrected
retries. Journey exercises resident, normal retained challenge and fresh rebuilt
challenge forms as well as fieldless advance. Pending feedback is asserted after
further typing, without another submit. Existing success assertions now expect
the intentional visible status rather than the old empty replacement status.
Retry count assertions wait for the pending transport to enter the browser
event loop before inspecting the intercepted requests.

<!-- rpi:phase id=P02 -->
## P02

<!-- rpi:task id=P02-T01 -->
### P02-T01

Shared worktree .venv; PYTHONPATH uses absolute worktree src/test roots.
Focused test_case_journey, test_workspace_scripts, related accessibility,
content/design, procurement/resident and timecapture tests; Ruff100, mypy99,
node syntax. Both browsers with existing pinned axe. flock -n on the caller's
/tmp/ama-rpi-heavy.lock, 15-second retries up to 40 minutes. New external output.
Full discovery passed on round eight; this narrow correction uses focused/
related suites rather than rerunning unrelated opt-in integrations.

Completed final attempt round9-validation-06: 27 focused and 117 related
tests pass (one related skip), Ruff100/mypy99, JavaScript syntax, unit formatting
and diff whitespace pass. Journey: 406 assertions/87 axe states; assistants:
206 checks/56 states. All five challenge browser modes pass, with 11 further
axe states. No reported axe violation or page error. Manual incomplete items
and whole-system/human acceptance remain unestablished. Commands, source/evidence
hashes and failed attempts are retained in the changes record.

<!-- rpi:task id=P02-T02 -->
### P02-T02

Fresh independent reviewer compares complete round-nine diff and coupled raw
handlers, plus prior pending-lock/queue regressions and source-bound evidence.
Writes only this child's dated Review. Retain all original adverse outcomes;
commit source and original evidence locally, no push. Publication remains gated.

Completed: sole original independent Review at
.copilot-tracking/reviews/logs/2026-10-29/case-journey-526-round9-review.md,
execution Complete / outcome Conformant, zero findings. Reviewed source hash
unchanged. This local commit retains implementation and all seven dated
original phase/state artifacts. State is automatic/Follow-up/completed with
session running, no child selected. Coordinator owns publication; manual
acceptance remains separate. Earlier original Not accepted outcomes unchanged.
