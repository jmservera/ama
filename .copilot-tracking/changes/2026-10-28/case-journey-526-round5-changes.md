---
title: Case journey round five changes
description: Execution and validation evidence for the three-thread correction
ms.date: 2026-10-28
---

## Invocation

Task 526-pr529-round5-20261028; full plan P01/P02. Research executed Ready.
Single critique Complete / Revise, PC-001 applied directly before implementation:
retain chat panel state across same-case redraw and test pending completion.
Original critique unchanged. Automatic Implement begins at P01-T01.

## Boundaries

Existing branch and open PR verified; fetch and pull --ff-only completed,
including bot HEAD 1d36e8b3. Refs #526 retained. No az/Azure, secrets, .env,
private datasets, remote replies/resolution or push without complete gate.
Heavy checks use shared flock -n with absolute <=2400-second retry deadline.
Only original dated RPI evidence and authorized local source are committed.

## Implementation and Validation

P01 source and regression batch implemented. Shared raw snapshot cleanup clears
only successful unchanged questions. The complete session chat node retains
both pending handlers/threads and conversation across redraw. Save edited
proposal now has the exact Accept/Edit predicate. Count announcements use an
atomic polite text span inside the semantic dd, with availability and navigation
outside the live region and equality guards for counts and tab labels.

Three new executable shipped-function unit methods cover both chat handlers,
every proposal readiness predicate/verifier state, and live text write counts.
17 focused journey/workspace tests pass. API Ruff at 100 columns passes and
owning format check passes (48 files); mypy passes 95 source files. JS parse
passes for all four modified web scripts. No tools files touched.

### Preserved initial browser failures

External root:
/home/azureuser/.copilot/session-state/16a6e9f1-7878-4a36-8169-280cadd8346c/files/.
Attempt round5-validation-01 admitted shared flock at 23:08:50Z; first unchanged
chat success/redraw/dirty/unload passed. Later scenario failed because goto
changed only the hash and clicking the already-open retained details closed it.
Corrected the test to use unique document query URLs per scenario.
Attempt round5-validation-02 admitted 23:09:27Z; all five ordinary chat scenarios
passed. Regulatory button correctly remained disabled because the base journey
fixture has no regulatory admission. Added an explicitly constructed admission
response for the lifecycle test only; no production readiness bypass.
Both original logs retained unchanged; neither attempt is reported passed.

The initial explicit format check over excluded legacy browser files reported
pre-existing assistant formatting plus one new test formatting change; only the
owning test was formatted. The repository excludes checks/*.py from formatting;
owning Ruff/format/mypy run passes. New Python additions remain <=100 columns.

## Sibling Audit Matrix

PR web boundary against origin/main: app.js, assistants.js, case-workspace.js,
chat.js, ops.js, panels.js, index.html and style.css. Refreshed current Web
Interface Guidelines before the changed-web read. This is a bounded lifecycle
audit, not a whole-app conformance or no-future-defect guarantee.

| Surface | Dirty-state paths | Live/status paths | Readiness/disabled paths |
| --- | --- | --- | --- |
| app.js | input marker, raw snapshots, refresh, capture/restore/pending cache, route and unload guards, record-bound recovery/discard, resident/document/funding generation and aiNotes review inspected; external manual wording intentionally remains separately unsaved after AI review | review/error statuses, retained document results and ai-review-change dispatch inspected | draft stale/invalid guards, completed review disabling and pending review exclusion retained; chat panel now session-retained |
| chat.js | both handlers corrected; success, raw later edits, whitespace, create/answer failure and redraw pending paths regressed | distinct log additions and concise status messages retained; regulatory results/doubt/admission failures remain explicit | pending submit guards added to both forms; source-admission failure still disables regulatory lookup; doubt aria-disabled retry semantics retained |
| assistants.js | existing immutable note/editor/verification cleanup and revision recovery inspected; verify intentionally does not consume JSON edits | load/error/deadline/history statuses retained, late panels cannot populate a different case | all three acceptance controls now use identical ready/own-verification predicates; Reject remains available; text never disabled |
| case-workspace.js | mounted tabs and query-preserving native links do not consume drafts | dedicated polite atomic count text, stable navigation node and equality guards; loading, count, zero and unavailable wording inspected | tab active/hidden/roving focus and summary jumps retained; observer disposal preserved |
| ops.js | quality mutation snapshots, measure/version checklist restore and later evidence recovery inspected | quality errors and checklist load failures explicitly announced | busy action restoration and human quality role/state controls retained; no approval rule changed |
| panels.js | finance/grant/technical actForm submitted controls, resident immutable body/snapshot, challenge complete-form preservation/reset/pagination inspected | local field feedback and history pagination statuses retained | uncertain committed resident/challenge results intentionally stay disabled pending history check; failure-before-dispatch can retry |
| index.html, style.css | persistent workspace status and native main retained | no hidden ancestor for summary; no newly live parent wrapping count/navigation | native control focus, hidden panels, overflow and reduced-motion styles unchanged |

### Guideline read result

src/api/src/zava_forward/api/web/app.js:708 - pass: session retains pending chat controls.
src/api/src/zava_forward/api/web/chat.js:12 - pass: exact successful cleanup; failed/newer edits retained.
src/api/src/zava_forward/api/web/assistants.js:55 - pass: submission matches readiness and verifier gates.
src/api/src/zava_forward/api/web/case-workspace.js:67 - pass: one atomic polite count text, no repeated equal updates.
No new in-scope guideline defect found. Existing repository ASCII/content rules
override generic curly punctuation preferences. Real screen-reader speech and
staff usability are not executed or certified by this read or axe.

## Completed Journey Evidence

Attempt round5-validation-03 admitted shared flock at 23:10:02Z.
Journey completed: 206 PASS assertions, 38 pinned axe 4.10.3 scans, zero
violations and no page errors, actual Chromium 200% zoom and narrow reflow.
Both chats passed all five unchanged/later/whitespace/answer-failure/thread-
failure cases across real call-save redraws, including retained node identity,
pending resubmit exclusion, cached dirty and actual beforeunload callback.
Hidden AI tab count/loading/unavailable and duplicate-event nonmutation passed.
Result: round5-validation-03/journey/results.json under the external root;
SHA256 79be0afa1f705756f0ede4b8ed97d4e0cf7b7a52a4cea6cae2564abb003cfac1.

The assistants segment of attempt 03 failed in the new interception fixture:
Playwright supplied Request as the handler's second argument, replacing the
intended default override dict. Corrected the callback signature to accept
Request explicitly and wait for actual replacement after the preceding
same-revision refresh. Original failure retained; no production fix changed.
Attempt 04 runs assistants only under fresh bounded shared admission; the
completed journey source is unchanged. Additional related chat/accessibility/
design/content contracts passed 43 tests; expected missing-law-store fixture
diagnostics are explicit, not swallowed or a live-law success claim.

## Final Validation and Pre-Review Reconciliation

Attempt round5-validation-04 admitted shared flock at 23:11:37Z, exit 0.
Assistants: 58 checks, 10 pinned axe 4.10.3 scans, zero violations/page errors,
Chromium 155.0.8059.39. All nine unavailable same-revision editor variants keep
JSON selectable and all acceptance controls disabled; ready own verification
reenables all three. Existing real proposal verify/accept/revision/overlap/manual
scenarios pass. Result SHA256
a2b3fc5677db545f58bdfd1490181cf7397deb438cfea62cbf1557cc6addc745;
round5-validation-04/assistants/results.json under the external root.
Both attempts release shared lock immediately on process exit; no foreign
process/output touched. No full discovery or tools suite claimed or required.

Final focused 17 tests rerun after strengthening the unit's editor identity
assertion; owning API Ruff/format and mypy (95 source files) pass; all four
changed JS scripts parse. New Python additions <=100; git diff --check passes.
Source/test/guide diff (eight paths under src/api) against intake 1d36e8b3:
SHA256 d6c2431f7ac4088036a6354b074e68d83f48658d429409bd604ddeffb89357c5.
No production changes after the successful journey run; later assistants edits
only correct its interception fixture and await actual refresh settlement.

Plan/details: P01 and P02-T01 checked. Sole remaining P02-T02 owns one independent
Review and local commit bookkeeping. Research Ready and original critique
Revise/PC-001 applied are reconciled; no unresolved local implementation or
validation blocker. Required full publication gate remains unavailable:
tools/rpi-checks.py TOOLS includes az and the full recipe runs az bicep
version/build/lint. These commands are prohibited, so the complete gate was not
invoked, no receipt invented and no push is eligible. Coordinator owns that
external gate and subsequent PR replies/resolution. Screen-reader/manual/staff/
hosted approval remain distinct, unmet acceptance boundaries.

## Sole Independent Review and Later Routed Implementation

Review executed Complete / Defects found, one Low RV-001 test-ordering defect,
no substantive introduced production defect. The original Review is preserved
unchanged at .copilot-tracking/reviews/logs/2026-10-28/case-journey-526-round5-review.md,
including its original assessed diff identity. It independently passed all
60 focused/related tests and verified the source and browser evidence hashes.
No second critique or Review.

RV-001 was routed to a later bounded rpi-implement invocation, recorded at
.copilot-tracking/changes/2026-10-28/case-journey-526-round5-rv001-changes.md.
It moves the outage assertion after fresh document/Overview readiness and
observes the injected 503. Final journey rerun passes 207 assertions/38 zero-
violation scans/real zoom. Original Review outcome remains Defects found, not
silently upgraded to Conformant by this later implementation.

Final source/test/guide diff hash:
bb3f69ae883e67ff2acdc045f19ce34d74739be90dffc53526f2569ffd4c97d9.
All required local checks pass; no known in-scope source or regression defect
remains from the supplied threads or the one routed finding. This is not a
promise that automated review can find nothing else or human acceptance.
Local source/evidence commit is next. Publication is deferred to coordinator.

## Local Commit and Final Handoff

Source and all dated original evidence committed as
6f836a68459dbafee5a6c3382b1d62366c8fcd67. Authenticated account privacy-safe
author/committer address and required Copilot trailer verified; commit uses
Refs #526. Worktree clean immediately after source commit. The containing
documentation-only handoff commit reconciles final plan markers/details/state;
no later source, test, tool or evidence-result changes.

Automatic task completed, session running at Follow-up with publication blocked.
Coordinator owns current-base/final-HEAD complete gate, receipt verification,
independent exact-head assessment, permitted push and three thread replies/
resolutions. Latest fetched main 9bfed51863b05a25e9939d82504c576524688e14.
No prior receipt is reusable. No az/Azure/private-data access, push, PR-body
change, remote thread mutation or source-history rewrite performed. Human
screen-reader/staff acceptance and hosted approval remain separate outstanding
boundaries, not replaced by zero automated violations.
