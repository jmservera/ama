---
title: Resident chat 520 phase details
description: Evidence, dependencies and completion expectations
ms.date: 2026-10-28
---

Task ID 520, resident-chat-520. Plan owns requirements and dispositions.
The plan's Critique Disposition applies to all tasks below and supersedes
earlier narrower wording: all personal requests require use_record true;
Europe/London filtering/display, UTC instants and first-three ordering;
operator-assisted CLI cancellation; visible no-live-contact callback receipts;
200% text and 400%-equivalent reflow; post-gate independent exact-head
assessment before push. PC-001..006 are accepted direct corrections.
Implementation reconciliation: P01/P02 and P03-T01/T02 complete. P03-T03
documentation is written and independent Review is next. P03-T04 has not run.
See the changes record for exact local commands/counts and external browser
evidence. Remaining acceptance is not silently satisfied by automated checks.
Original Review is now recorded: execution Partial, outcome Residual work,
one Low RV-001 evidence-summary inconsistency. P03-T03 is complete with that
original outcome, not a conformant assessment. P03-T04 remains pending; raw
external evidence must be accessible to the separate exact-head assessor.

<!-- phase: P01 -->
## P01 - Backend and agenda

<!-- task: P01-T01 -->
### P01-T01 - Persistent synthetic callback agenda

Research C4/C5: showcase is read-only and existing works agreements cannot be
silently reused as a scheduler. Add an explicit local SQLite adapter with
operator-seeded synthetic officer callback slots, no automatic fake bookings.
Use transactions/unique constraints for races, resident hashes for ownership,
expiring proposals and fresh admission checks before mutation. Retry returns
the same booking; cancel only own booking. Startup opens only an explicit
ZF_DEMO_AGENDA_PATH, otherwise reports unavailable. Local fixture seeds a
task-owned temporary database; never open normal working data.

<!-- task: P01-T02 -->
### P01-T02 - Bounded host chat routing

Depends on P01-T01 for appointments context. Research C1..C3: retain existing
topic endpoint/provider/Azure advisor. Additional bounded question request
requires explicit record-use boolean. Host recognizes supported categories,
rejects selectors and uncertain actions; model never receives free text.
Use own projected home/case only, callback agenda only, unknown works consent.
Regulatory evidence C8 is explanatory only with complete local metadata;
currentness was not verified. Safety always gives immediate human help and
states that nothing was sent. No automatic safety case or false receipt.

<!-- phase: P02 -->
## P02 - Resident app

<!-- task: P02-T01 -->
### P02-T01 - Shared accessible chat

Depends on P01-T02. Mount once outside hidden personal content, not once per
render. Native launcher with SVG chat symbol and visible Chat label; nonmodal
dialog, close/Escape return focus, heading focus on open only. Preserve current
question/select IDs where feasible for compatibility. Avoid trapping Tab;
prevent overlay covering focused background controls by closing when focus
moves outside. Reset all transcript/consent/proposals on session changes;
ignore delayed callbacks belonging to an old mount/session generation.

<!-- task: P02-T02 -->
### P02-T02 - Appointments

Depends on P01-T01/P02-T01. Independent manual appointment section plus chat
route to the same controls. Explicit date/time filters and data-use consent.
Render at most three stored slots. Selection does not book; unchecked separate
confirmation control plus labelled Book action does. Cancel needs explicit
confirmation or undo. Human route always visible, even with no configured agenda.
All dates use Intl; messages distinguish requested/proposed/booked/unavailable.

<!-- phase: P03 -->
## P03 - Validation and publication

<!-- task: P03-T01 -->
### P03-T01 - Regression coverage

Depends on P01/P02. Max two new modules, no test removals. Cover persistent
reopen, first three/date/session preferences, expiry, no-availability, duplicate
confirm, cross-owner/cancel, parallel booking race, failures, reauthorization,
source metadata/legal refusal and untrusted text. Existing provider regressions
must remain passing. Extend existing browser harness for actual HTTP, launcher,
manual booking, focus and delayed previous-session responses.

<!-- task: P03-T02 -->
### P03-T02 - Local evidence

Depends on P03-T01. Use installed pip distributions, constructed fixtures.
Run focused tests then API discovery, ruff/types and Node. For heavy commands,
nonblocking shared flock; if busy do not queue/poll. Browser installs only after
actual missing prerequisite. Pin axe digest using existing helper. Exercise
320/390/1280, reduced motion, keyboard and error/session states; retain external
screenshots/JSON. Never mistake axe for AT/resident acceptance.

<!-- task: P03-T03 -->
### P03-T03 - Documentation and original Review

Depends on P03-T02. Update API README with actual local setup, API schemas,
synthetic-only callback semantics and limitations. Changes evidence records
commands/outcomes. Fresh independent Review once, preserve original outcome
and route findings to later work rather than re-review this task.

<!-- task: P03-T04 -->
### P03-T04 - Publication

Depends on P03-T03. Authenticate gh identity, repo-local noreply, conventional
commit/trailer. Fetch main, complete `tools/rpi-checks.py --all --lock-timeout 0`
with new external output, verify exact receipt against current origin/main
immediately before push/independent exact-head assessment. Any failed gate
blocks publication; never deploy or bypass. One push, PR Refs #520 only.
