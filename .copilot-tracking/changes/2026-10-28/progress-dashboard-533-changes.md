---
title: Progress dashboard and closed cases changes
ms.date: 2026-10-28
---

Task #533, progress-dashboard-533. Full RPI loop executed for local delivery;
independent Review Complete / Defects found. Source acceptance remains open.
Plan/details and original Complete / Revise critique retained. PC-002..006
applied; PC-001 rejected because its worker-only restriction conflicts with
the user's explicit shared /tmp lock.

## P01: Server read models

Implemented progress.py with synthetic admission, observed episode replay,
UTC date cohorts, current recorded workflow/team/stalled/overdue measures and
explicitly synthetic briefing reviews. GET endpoints use existing staff/manager
permissions. No source dataset reads or modifications.
Focused semantic tests cover JSON and SQLite, exact metric values, unknowns,
provenance exclusions, roles, combined filters and paging.

## P02: Native employee surfaces

Implemented progress.js/progress.css, recoverable script registry, staff
navigation and hash routes. Every chart has an equal-value table; archive
filters/page survive reload/history and filter changes reset paging. Safety
marker retained. Added README contract and real-browser regression.

## P03: Validation and review

Default Python lacked namespace packages, so installed
existing core/agents/api[dev] distributions into owned /tmp/ama-533-venv.
Chromium installation command succeeded. No dependency manifest changes.

Focused unit regressions: 31 passed (targeted-unit-3.log). First two attempts
exposed a fixture writer that did not touch its SQL case; fixed harness to
use _case and canonical stage_since, not production logic.
Browser attempt 1 found 320px grid min-content overflow; added min-width:0.
Attempt 2 encountered CSP-blocked inline axe injection; changed check to
existing DevTools evaluation pattern, preserving production CSP.
Attempt 3 passed all six API/chart/table comparisons, URL filters, page
boundaries, refresh/history, empty state, retry, late-response cancellation,
keyboard focus, 320/390/1280 reflow and axe (zero violations on both pages).
Pinned axe SHA256:
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
Original logs retained externally in /tmp/ama-533-evidence.
Full API discovery passed: 1192 tests, 316 inherited skips, 423.365 seconds
(api-suite-final.log). Skips cover opt-in local SQL Server suites, existing
opt-in Chromium workflows, and JSON's non-applicable SQL COMMIT boundary.
No new test is skipped. This is not SQL Server or full-gate evidence.
The first full run failed missing endpoint inventory entries and an old
mid-edit renderer harness; added both new endpoints to the existing all-role
inventory and preserved its canaries. Original failure remains in api-suite.log.

Final focused run after the last two backend safeguards (explicit
is_synthetic=false overrides historical labels; missing archive stage displays
Unknown without a summary KeyError): 50 tests passed, 9.346 seconds
(targeted-final-2.log). Browser-final-3 passed on Chromium 156.0.8078.4 with the
same pinned axe 4.10.3: zero violations on both pages. Dashboard has one
color-contrast incomplete rule for clipped/offscreen bar text; retained for
manual review, not claimed as a conformance pass. Closed archive has zero
incomplete rules. API/chart/table parity checks use actual endpoint values.

Earlier browser-final failure was a harness readiness race (old heading could
be present before the hash refresh completed); replaced an immediate count
with Playwright's retrying six-chart assertion. Browser-final-2 and final-3
passed. Invalid date ranges retain editable filters and recover through submit;
failed reads remain distinct from empty data.

Package Ruff passed with line limit 100 (new Python files checked for actual
line lengths); strict mypy passed all 98 configured files. New Python formatter,
node --check for app.js/progress.js and git diff --check passed.
No source changes to briefing, map or case-workspace modules.

## Amendments and Divergences

Updated tightly coupled regression contracts: workbench navigation manifest,
capacity navigation browser expectations, and existing closed safety test to
exercise the new renderer while preserving all safety/name/status assertions.
No tests removed. Added scoped mypy allowance for untyped migrated Store/server
calls, consistent with existing HTTP harnesses. No runtime dependency changed.

Final source guardrails and relevant reruns are complete. P01/P02 and P03-T01
complete. P03-T02 is complete with the original independent Review and the
local implementation/evidence commit containing this record.

## Independent Review and Follow-Up Handoff

Exactly one Review executed, separately from critique:
.copilot-tracking/reviews/logs/2026-10-28/progress-dashboard-533-review.md.
Execution Complete; outcome Defects found (Medium 1, Low 1). Original outcome
and all conclusions preserved. No source fixes or repeated Review after it.
Frozen src/api diff SHA256:
e79f806638643586483ebd0649dd5634eb19905b5584a0ce20d9cbb115723991.

Ranked next work:

1. Later rpi-implement: RV-001 associates range errors with invalid date fields
   and focuses the first relevant invalid input; RV-002 adds loading aria-busy.
   Small bounded changes within the accepted native-UI direction.
2. Coordinator: reconcile the updated stacked parent and run the complete
   exact-head publication gate with permitted prerequisites. Any source/base
   or commit change requires new gate evidence. No publication in this task.
3. Owner/accessibility participants: existing screen-reader/text-resize/user
   acceptance, including reported contrast incomplete; retain #150 Fluent
   adoption as distinct existing work. Automation is not acceptance.

Denied browser roles were not exercised in the new browser harness; focused
HTTP tests and the existing all-role inventory own that coverage. The reviewer
inspected source/tests and ran lightweight numerical/syntax probes; raw external
suite/browser logs were not opened by that reviewer and remain attributed
execution evidence, not independently certified results.

Task status completed means the requested RPI loop executed and evidence is
preserved, not that review findings or release gates passed. Automatic session
remains running in Follow-up awaiting selection; no child work auto-selected.
Supported choices include the ranked work above, Stop automatic session and
Switch to manual mode. State:
.copilot-tracking/rpi-sessions/2026-10-28/progress-dashboard-533-state.json.

## Publication

No Azure or az permitted. Full exact-head gate remains mandatory before push.
If blocked, commit locally for coordinator; do not create an unbacked PR.

Publication blocked: tools/rpi-checks.py:62,601,1365 requires az and
az bicep version/build/lint. The user prohibits az/Azure, so the complete gate
was not invoked and no full receipt exists. Do not equate focused checks or
general-discovery skips with full gate approval.

Fetched main and parent during preparation. Parent PR #529 remains OPEN at
73e365e618d8cf701a12434e4cd0c2f2affb07f1. Starting worktree HEAD
6d2c2dc4 has 12 commits ahead/12 behind the updated parent; cherry comparison
shows the case-workspace commits patch-equivalent, while the parent gained
resident work (#525). No history was rewritten or unrelated resident code
integrated. Coordinator must reconcile changed parent ancestry before
publication and rerun the exact-head gate. Current origin/main merge base:
1dde6a908c20358dbb3067dcdd674e5ad0bd246d.

Prepared PR title: feat(employee): add progress dashboard and paged closed cases.
Base: feat/case-journey-ux-526.
Body must state: "Depends on #529 (feat/case-journey-ux-526, unmerged).
Refs #533." No closing keyword.
