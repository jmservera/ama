<!-- markdownlint-disable-file -->
# Phase Details: Chat focus review follow-up

Task 550-focus-fixes; 2026-10-29. Plan:
.copilot-tracking/plans/2026-10-29/chat-widget-550-focus-fixes-plan.md.

<!-- rpi:phase id=P01 -->
## P01: Focus correction and regressions

<!-- rpi:task id=P01-T01 -->
### P01-T01

Shared create installs a named document focusin handler. For visible active popup,
outside targets except launcher cause hide(false). Do not prevent Tab, refocus,
abort, clear draft/history or reset busy. Dispose removes the same listener.
Keep launcher exception so click toggle remains correct and visible-background
completion can be tested independently. Remove async ui.focusInput after skills
and send finally. Keep explicit invalid-submit focus and synchronous busy handoff
from Send before disabling. Access-loss routing may focus app only when removal
would otherwise lose popup-owned focus; external focus must remain unchanged.
Remove CSS max-height:35rem override: default dynamic height/bottom already
reserves launcher space. At 1280x500 assert launcher hit point and single-click
toggle for both apps. Shared error explicitly aria-live=polite/aria-atomic=true;
retain existing role=alert selectors and inline visibility.
Implementation refinement: shared disposal no longer temporarily hides the
launcher; employee reset owns final visibility based on current admission.
Browser denial tests exposed that even a synchronous hide/show blurs a
deliberately focused surviving launcher. Root removal/listener cleanup and
access/session visibility remain unchanged.

<!-- rpi:task id=P01-T02 -->
### P01-T02

Node VM behavioral tests execute actual shared factory and employee adapter:
outside focus hides without return; launcher/internal focus does not; dispose
unregisters listener; retained state/busy; held setup/thread/ask success/error
cannot focus internal input after deliberate internal/external/launcher focus.
Use bounded subprocess timeout, no new dependencies. Include polarity proof
against git-show baseline copies in external storage, no source checkout.

Actual apps: resident signed-out 320x800 RV-001 reproduction checks exact
Sign in focus, hidden popup and elementFromPoint focused-control visibility.
Shared Tab/Shift+Tab tests prove unobscured target and retained draft/history.
Controlled async tests cover visible launcher/internal focus as well as an
external textarea (which hides popup); assert current completion updates
thread/status without focus/reopen, error keeps draft, success clears only
unchanged draft. Setup tests hold each skills/status dependency; thread and ask
success/rejection tested independent of abort/disposal. Keep existing obsolete
fencing, exact loading, consent, keyboard, layout and axe coverage.
Denial tests cover 403/404 at setup/thread/ask with internal/external/launcher
focus; only popup-owned focus recovers to app on disposal. Existing employee
checker retains actual 401 session tests. Its post-setup input-focus assertion
migrates to unchanged heading focus; both audience checks run mandatorily.

<!-- rpi:phase id=P02 -->
## P02: Validation, evidence and independent Review

<!-- rpi:task id=P02-T01 -->
### P02-T01

Use owner-specified /tmp/mv commands from src/api with
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Browser uses existing constructed loopback fixtures, pinned axe and browser.
No live data/model/Azure; no package installation unless missing prerequisite
failure. README states outside-focus hiding and no async refocus.
Parent runtime is existing /tmp/mv (executables verified); external evidence
uses the provided parent session files directory. Critique worker's /tmp
restriction does not apply to parent; no tools/runtime substitution required.

<!-- rpi:task id=P02-T02 -->
### P02-T02

One independent review for selected follow-up only, no second original Review.
Write new review, preserve adverse original, append closure evidence to original
review and changes. Original plan remains historical; add follow-up pointer.
Commit after review and identity resolution, no push. Publication/human checks
remain explicitly unperformed. New findings route to later work, not correction
or re-review in this task.

## Completion

P01/P02 and all task markers complete. One independent follow-up Review:
.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-focus-fixes-review.md,
Complete / Conformant, no new findings. Both original findings resolved;
dated resolution append preserves original adverse Review. No source changes
after assessment. Owner-authorized local commit contains final evidence/state;
its metadata is the closeout receipt. No push, az or rubric edit.
