---
title: Case journey sixth correction changes
description: Execution, validation and sibling audit for PR 529
ms.date: 2026-10-28
---

Task 526-pr529-round6-20261028; full plan P01/P02. Research Ready.
Sole critique Complete / Revise, PC-002/003 applied; PC-001 rejected because its
unsupported /tmp prohibition conflicts with explicit user lock direction.
No second critique. Implementation begins at P01-T01.

Boundary: clean matching branch/open PR, pull --ff-only first completed;
intake HEAD 91caef1c413764aacea2da492368a72bb4366c6f.
No az/Azure, secrets/.env, private data, push or thread mutation. Refs #526.
Heavy admission uses exactly /tmp/ama-rpi-heavy.lock, flock -n, <=2400 seconds.
Complete publication gate is deferred, not passed, because it invokes az.

## P01 implementation

Shared snapshots retain semantic key and owning session. Success independently
compares original, current, recovery and cache values, retires only exact
dispatch-time values, removes consumed recovery and preserves later edits.
Capture preserves recovered checkbox semantics; restoration reads authoritative
session cache so delayed saved arrays cannot resurrect consumed drafts.
Case refresh uses keyed pending exclusion and distinguishes rejection,
uncertainty and committed mutation with failed redraw. Stale-session failures
cannot publish to a different case. Quality measure choice is navigation state,
retained separately without a phantom dirty field; evidence remains bound to
measure/version. Save evidence stays busy while switching measures is allowed.

Proposal local Reason validation precedes separate JSON parsing; malformed JSON
owns invalidity, description and focus. Correction clears stale associations.
API/reload errors are status feedback, never false Reason errors. Shared
ID/revision pending/consumed ownership covers case cards and the sessionless
queue. Consumed revisions cannot retry after reload failure; authoritative
refresh can recover uncertain transport outcomes.

Sibling corrections: aiNotes no longer marks valid Reason invalid on request
failure; local errors clear on correction/retry and uncertain reviews remain
unavailable until history checking. Quality remediation validates missing
evidence before dispatch, associates error/focus and clears it on correction;
an async failure cannot invalidate a later changed field. Manual actForm buttons
exclude duplicate pending requests and retain check-history disabling.
Recorded-change/resident forms reject reentrant pending submits; challenge
field invalidity clears on correction without changing committed/uncertain
outcome safeguards. No approval/consent authority changes.

Four new unit methods (within maximum four) exercise 20 representation/type/
later-value combinations, sessionless/case proposal errors and pending/reload
outcomes, quality error routing and manual-action pending siblings. Existing
shipped-code unit oracles were extended for keys/session and request status.
Two bounded existing-browser helpers add quality switch/cache/later/refusal/
reload and case/queue review JSON/pending/recovery matrices. API README updated.
No tools edits, dependencies, removals or generated source.

## P02 initial validation and preserved failures

External evidence root:
/home/azureuser/.copilot/session-state/ec604a8f-07fa-4225-8a37-eb9e234f5e87/files/.
round6-units-01 admitted lock 2026-10-28T23:46:08Z. Initial 19-test run had one
new fixture failure: its constructed live control omitted the checklist binding
that shipped controls carry, so a later draft could not meet the checklist-kind
restore assertion. Corrected the fixture; original tests.log retained.

round6-validation-02 admitted 2026-10-28T23:46:59Z: 19 focused tests pass;
API Ruff at 100 columns passes, format 52 files passes, mypy 99 source files
passes. Journey stopped at the first new pending assertion because the CSS
loading indicator intentionally contributes "(loading)" to the accessible
button name. Replaced exact-name pending locators with stable control identity/
loading-aware accessible names. Original journey.log retained; no browser pass
claimed from that attempt. Later source changes require final reruns.

System python lacked dev modules; existing worktree .venv has installed API,
Ruff 0.17.1/mypy 2.4.0/Playwright. No installation or PYTHONPATH source workaround.
Pinned public axe 4.10.3 fetched to external evidence root; SHA256
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
No secret or private dataset read.

round6-validation-03 admitted 2026-10-28T23:54:44Z. Quality success, later
whitespace, other-measure and cache-only scenarios passed their actual
dirty/unload/no-resurrection checks. The refusal wait was a strict locator
failure because both local and global status announced the same error.
Keep local feedback when connected, use global status only for detached
closures, and scope the browser error oracle. Original log retained.

round6-units-final admitted 2026-10-28T23:54:40Z, passed 43 focused/related
tests, API Ruff/format and mypy. Later final audit changes require another
final verification; these results are not silently attributed to later bytes.
The source audit also retained original File identity through recovery,
compared all aliasing file controls before clearing any selection, retired
consumed form-level unsaved markers and preserved later form edits. Quality
record actions retain check-history disabling after uncertain/committed-redraw
failures, not just Save evidence.

## P02 sibling audit matrix

PR web boundary verified with git diff --name-only origin/main; exactly the
eight files below. Current Web Interface Guidelines fetched again before this
post-fix read. Native semantics, focus, async status, labels, unsaved warnings,
loading state, content overflow, reduced motion and responsive CSS inspected
within this behavioral diff. Repository ASCII/content choices override generic
curly typography; unrelated pre-existing presentation is not redesigned.

| File | Error routing and aria-invalid | Pending and recovery controls |
| --- | --- | --- |
| app.js | aiNotes missing Reason is local; request failures now status-only; native recorded-change validity remains local; generic mutation/reload errors distinguished; list/map/login/account/document/generation errors retain their own alert/status channels without false field invalidity | shared keyed/session snapshots, all original/current/recovery/cache counterparts, file aliases and checkbox semantics, form markers, delayed restore, pending cache, tab/leave/unload, complete document/resident/chat nodes and funding identity inspected; recorded-change reentry excluded; current-session guard prevents stale feedback |
| assistants.js | missing Reason and JSON parse separately associated/focused; correction/retry clears stale invalidity; review/load/history/invoke failures status-only | shared pending/consumed revision state covers case and queue refresh; latest authoritative cache restoration; verification never consumes JSON; consumed revisions stay blocked on reload failure; unknown transport requires authoritative refresh; editor remains copyable/editable |
| ops.js | remediation evidence validated before dispatch, error association and correction clearing added; async failure no longer infers invalidity from later input; existing package/appointment native error associations and correction handlers inspected | quality Save and record actions busy/exclusion/check-history; measure navigation independent from draft dirtiness; version-bound checklist/recovery and delayed loader inspected; stale session cannot toggle another case; capacity/appointment separate draft/context/retry paths preserved |
| panels.js | challenge stale invalidity clears on correction; local first-invalid focus/reset retained; HTTP/uncertain/committed messages remain distinct | finance/grant/technical actForm pending guard added; resident native form reentry excluded; all their submitted fields use shared semantic reconciliation; challenge forms remain deliberately excluded from generic capture and retain complete context, later edits, reset and history pagination |
| chat.js | ordinary/regulatory question, source admission, source refresh, doubt and inbox errors use their separate status channels, no inferred field invalidity | both raw snapshot success paths, pending guards, retained node identity and later/whitespace/failure behavior inspected; regulatory admission remains disabled on failure; source/doubt controls retain existing explicit retry semantics |
| case-workspace.js | no field validation/submission handlers; summary statuses remain polite/atomic and deduplicated | retained panels, roving tabs, query-preserving native journey links, observer disposal and tab-only exemption unchanged |
| index.html | workspace status remains outside hidden tabs; native main/skip/account semantics retained | required script ordering unchanged; no submission/recovery state owner in markup |
| style.css | field-error presentation, focus visibility and non-colour error/status retained | busy naming, hidden panels, overflow/reflow, forced-colour and reduced-motion behavior preserved; no lifecycle state owner in CSS |

### Guideline read result

src/api/src/zava_forward/api/web/assistants.js:20 - pass: local error ownership,
association/correction and focus; valid fields unflagged on request failure.
src/api/src/zava_forward/api/web/app.js:808 - pass: exact semantic cleanup,
authoritative recovery and preserved later values/form markers.
src/api/src/zava_forward/api/web/ops.js:33 - pass: remediation error ownership;
quality pending controls keep copy/edit and measure navigation available.
src/api/src/zava_forward/api/web/panels.js:15 - pass: pending exclusion and
local correction clearing without weakening committed/uncertain safeguards.
No new in-scope guideline defect found by the bounded source read.
Actual screen-reader speech, real staff usability and deployment acceptance
remain unperformed, not certified by code inspection or axe.

## Final candidate validation

Source stopped changing before 2026-10-29T00:03:59Z admission of
round6-validation-04. Journey passes 231 assertions, 38 pinned axe scans with
zero violations, no page errors, Chromium 156.0.8078.4 and real
chrome.tabs.setZoom=2 (innerWidth<=640). This includes all six new quality
pending/switch/later/cache/refusal/reload outcomes and actual unload callbacks.
Result: round6-validation-04/journey/results.json under the external root;
SHA256 79be0afa1f705756f0ede4b8ed97d4e0cf7b7a52a4cea6cae2564abb003cfac1.
The result shape intentionally retains 38 scans; new lifecycle assertions are
preserved in journey.log rather than fabricated extra scan states.

The assistants part of attempt 04 stopped at a new wait that dereferenced a
temporarily absent article during replacement. Replaced that wait with a scoped
Playwright attribute expectation, and opened later-value recovery before axe.
No production or journey source changed. Original assistants.log retained.

round6-final-checks admitted 2026-10-29T00:05:33Z after all production/unit edits:
21 requested test_case_journey/test_workspace_scripts tests pass; 22 directly
related accessibility/design/content tests pass. API Ruff at 100 columns,
owning format (52 files) and mypy (99 source files) pass. All four modified
JavaScript files parse; git diff --check passes. No tools file touched, so tools
tests are not required. New Python additions remain <=100 columns.
Assistants attempts 05/06 exposed harness-only assertions: a rebuilt queue
correctly collapses its editor, and the reload-failure heading wait matched the
ordinary queue heading by substring before replacement completed. Pending
assertions now include hidden controls and error-heading matching is exact with
an explicit old-card removal wait. Both failed logs remain external. Production
source did not change.

round6-assistants-07 admitted 2026-10-29T00:14:11Z and passes 141 checks,
32 axe scans, zero violations/page errors, Chromium 155.0.8059.39.
Result: round6-assistants-07/assistants/results.json; SHA256
c29a4206f85d8b75fc606c9fcf2128c315e3208ee1543e51bb2573071caf243e.
Log SHA256 f9b9cb904c60ba396560f81d0a403e68f6270ffa0e98b641cb620e562b8bfb5f.
Expected aborted assistance requests logged fixture-server BrokenPipe errors;
the completed browser suite reports no page errors. Both suites retain axe
color-contrast incomplete results requiring manual assessment, not a clean
conformance claim.

Final owning Ruff check covers src/tests and both changed checks at 100 columns,
passes; production/tests format check passes 51 files. An exploratory direct
format check of the browser harness failed its existing whole-file formatting;
the established format gate does not include checks. The earlier 52-file figure
included an additional selected file and is not the final owning-gate count.
No broad reformat was made. git diff --check passes.
Final API diff SHA256 against intake:
142e451dc07f5602412e88ee3aa025d27d0bfef53c9f40bba02e6dcd84bf64f4.
P02-T01 complete. Sole independent implementation Review is next; not yet run.

## Sole Review and local retention disposition

Review execution Complete; outcome Not accepted. Original report:
.copilot-tracking/reviews/logs/2026-10-28/case-journey-526-round6-review.md.
Both primary corrections have passing evidence. RV-001 (Medium) identifies an
existing requested sibling: document upload dispatch occurs before shared
refresh, so transport uncertainty re-enables unchanged submit and permits a
duplicate upload. The independent shipped-handler reproduction produced two
requests without history checking. This qualifies the earlier matrix:
recorded-change reentry is excluded while pending, but upload uncertainty is
not protected by the shared refresh wrapper. Do not interpret that matrix as
complete sibling acceptance.

No post-Review source fix or second Review was performed. Route RV-001 to later
rpi-implement with the report's bounded fix and regression; preserve this
Complete / Not accepted outcome. Task execution closes with an open finding,
not with conformant acceptance. P02-T02 means Review and local retention were
performed, not that the finding or human/publication gates passed.

Local-only commit includes the eight API files and all seven dated original
RPI artifacts. Authenticated account id/login 8036360/jmservera determines the
repository-local privacy-safe author/committer address. Refs #526 and required
Copilot trailer retained. No PR text or thread mutation, push, az/Azure or full
gate receipt. Coordinator must address RV-001 before current-base/exact-head
publication assessment, then handle publication and both original threads.
Manual contrast, screen-reader/staff and hosted acceptance remain separate.
