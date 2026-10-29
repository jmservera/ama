---
title: Case journey 526 open threads changes
description: Execution evidence for the further five-thread correction
ms.date: 2026-10-28
---

## Invocation and Current State

Task 526-pr529-open-threads-20261028; full plan P01/P02.
Research executed Ready. One critique executed, original Revise preserved;
PC-001 rejected as unsupported worker-only filesystem constraint conflicting
with explicit user lock direction; PC-002 applied to acceptance/handoff.
No further critique. Starting dependency-ready P01-T01.

## Boundaries

No Azure/az, secrets, .env, private data, workflow changes or approval changes.
Use actual shared /tmp/ama-rpi-heavy.lock, nonblocking retries <=2400 seconds.
Publication requires the full exact-head gate, so no remote write is eligible
when the prohibited az prerequisite prevents that gate. Local commit authorized.

## Execution and Validation

P01 source correction and focused regressions complete; P02 validation in progress.

* P01-T01 shared hasUnsavedChanges reconciles live controls through the existing
  rememberCaseFields cache, then checks DOM and pendingFields. Both guards use it;
  tab-only selection remains ahead of warnings. VM globals and pending-only,
  cancellation, clean-cache and actual unload-callback checks added.
* P01-T02 aiNotes snapshots dispatched fields, prevents duplicate review, clears
  only unchanged submitted controls and retains newer read-only dirty values in
  a record-labelled recovery fieldset. Completed buttons remain disabled. The
  document displays dispatch-time replacement. Unit cases cover text-only,
  reason-only, both, unchanged and failure; delayed browser review covers actual DOM.
* P01-T03 journey href synchronization replaces only tab, including after
  challenge history replaceState. Native anchors, six step mappings and tab focus
  behavior unchanged. Unit tests preserve encoded/repeated parameters; real DOM
  browser assertions page history and check no confirmation/redraw.
* Gate verifier and fixture require exactly 38 scans; negative mutations cover
  37, 39 and serious violations. No workflow or WORKFLOW_HASHES pin changed.

### Sibling inspection and immediately relevant amendment

Re-read aiNotes callers, assistantProposal, mutation refresh, case-field recovery
and challenge pagination. Assistant dispatch cleanup already compares immutable
snapshots; verification does not consume JSON edits. Resident/funding external
drafts remain editable and dirty; later reasons use record-labelled generic
recovery on redraw. Found tightly coupled draft replacement paths in document
Read with AI and resident AI/template replacement that could remove dirty nodes
without warning. Added explicit discard confirmation and cached-key cleanup for
those replacements; rejected replacement preserves values and completed record.
This is an intent-preserving P01-T02 amendment, not unrelated redesign.

### Initial checks and preserved nonpassing commands

Focused workspace/journey: 13 tests passed before the final query test addition.
API Ruff check and format: passed, 48 files; mypy: passed, 95 source files.
Tooling unit suite: 31 tests passed, with its expected interruption-probe output.
Initial format-check requested two test-file formatting changes; applied existing
Ruff formatter. A root-config Ruff invocation over tools surfaced nine pre-existing
rules outside the changed lines (EXE001/ISC004/FURB162/PLW1510/RUF007/SIM117).
Do not silently fix unrelated baseline or claim that invocation passed. Use the
runner's owning lint selection for tooling and retain its actual outcome.

Owning tooling command `ruff check --isolated --select E,F,I,B,UP
--target-version py312 --line-length 100 tools/rpi-checks.py
tools/test_rpi_checks.py`, isolated format check and tooling mypy all passed.
Final focused API suite: 14 tests passed. Final API mypy: 95 source files passed.
All added Python lines independently checked <=100. Five actual tracked workflow
hashes match the unchanged WORKFLOW_HASHES pins.

### Heavy validation admission

External evidence root:
/home/azureuser/.copilot/session-state/e7894362-b3b0-4580-89f4-7ed23a4bf20b/files/open-threads-validation/.
Owned shell 10 uses the actual shared lock FD 9, `flock -n`, absolute SECONDS+2400
deadline and min(15, remaining) sleeps. It waited for a foreign holder without
touching its process/resources/output, then admitted at 2026-10-28T22:34:19Z.
Temporary test/Chromium data is routed to this run's owned external scratch.
Full API discovery and journey-01 are in progress. No duplicate heavy run started.
During admission/early API execution, final sibling error paths were tightened to
append an explicit alert rather than remove dirty replacement drafts on failure;
final focused regressions are repeated before review. No success-shaped fallback.

API discovery completed: exit 0, 1168 tests in 423.616 seconds, 316 explicit opt-in
skips. These skips are not SQL/browser/live acceptance. Final focused units again
passed 14 cases after the sibling error-path correction.

Journey-01 passed the new pagination, delayed review/recovery, dirty replacement
confirmation and all 38 axe assertions, but exited 1 when the separate real-zoom
Chromium profile failed to launch: process_singleton_posix.cc reported
"Socket path too long" under the session-directory TMPDIR. Keep its original log
and screenshots; do not claim a completed browser pass. Retry the unchanged
harness with a short, uniquely owned external TMPDIR, under a fresh bounded lock
admission. This is validation-environment correction, not a source workaround.

### Completed validation and exact implementation boundary

Journey-02 admitted 2026-10-28T22:42:15Z with TMPDIR
/tmp/ama529-e789-nmFe7o. Same shared flock/deadline recipe, unchanged harness.
Exit 0: 153 PASS assertions, Chromium 156.0.8078.4, pinned axe 4.10.3,
exactly 38 scans, zero violations, zero page errors, actual
chrome.tabs.setZoom=2; innerWidth<=640. Result SHA256:
79be0afa1f705756f0ede4b8ed97d4e0cf7b7a52a4cea6cae2564abb003cfac1.
Existing assistants browser suite also passed 30 checks under the same owned
lock, including overlapping proposal loaders, revision-bound recovery and manual
paths. Neither uses billable providers or private data. Lock released on exit.

Source/test/guide diff against intake HEAD
454fc49f4f8c5d7e4119ead247725990b2fa5c0c:
SHA256 211caf8060ab3beeb50294bb8fbcc1c8197f869bb0dc2450e2b3de0c2559747e.
Nine files, no workflow changes. Full API run passed while final sibling
error-notification code was tightened; final focused 14 tests and JS parse were
rerun afterward, and the complete journey/assistants retry used the final source.
API Ruff/format and mypy pass; isolated 100-column tooling Ruff/format and tooling
mypy pass. Diff whitespace check passed. Five workflow pins match actual bytes.

### Web rule and sibling-read boundary

Guidelines fetched in full before edits and refreshed before the changed-web
read. Re-read shared dirty guards, aiNotes, capture/restore, resident/document
replacement including error paths, assistantProposal and in-place history
pagination. No new in-scope guideline finding identified in the changed code:
native anchors, control labels, async status/errors, copyable readonly text,
explicit discard and existing focus/reduced-motion semantics retained.
Repository ASCII/content standards take precedence over generic typography.
This is not whole-app WCAG, screen-reader or staff acceptance.

## Pre-Review Reconciliation

P01 and P02-T01 complete in plan/details. P02-T02 remains solely for one
independent Review and authorized local commit/handoff. Required local checks
passed; original browser environment failure and critique Revise retained.
Full publication gate was not executed: required az commands are explicitly
prohibited. Remote reply/resolution and publication remain blocked, not passed.
Review-ready implementation boundary is the nine-file diff hash above; no
unresolved implementation decision or failed mandatory local check remains.

## Sole Independent Review and Delivery Boundary

Review executed Complete; Outcome Conformant for the assessed local nine-file
implementation, no substantive findings. Original record:
.copilot-tracking/reviews/logs/2026-10-28/case-journey-526-open-threads-review.md.
Reviewer independently verified exact diff hash, pinned result identity,
38-scan contract, five workflow pins, 14 focused units and owning lint/parse.
It preserves the original critique and browser failure. No second Review.
The 37 retained incomplete color-contrast rule results require manual checking;
zero automated violations do not establish WCAG/manual/staff acceptance.

Fresh remote inspection: PR #529 OPEN at 454fc49f, matching topic; no remote-only
bot commit, so no fast-forward pull was required. Current fetched main:
1dde6a908c20358dbb3067dcdd674e5ad0bd246d.
GraphQL false-only listing still returns the exact five research thread IDs.
PR body retains `Refs #526`. No PR body change or remote mutation attempted.

Publication blocked only at required full-gate eligibility: tools/rpi-checks.py
TOOLS includes az and the full recipe runs az bicep version/build/lint. User
forbids these, so no fabricated gate receipt, bypass, Azure call or push attempt.
User-authorized local commit follows with authenticated
8036360+jmservera@users.noreply.github.com for both author and committer and the
required Copilot trailer. Remote replies/resolution remain deferred until the
coordinator publishes the actual corrected code. No claim that remote threads
are fixed before their source is present on the PR.

## Verified Local Commit and Final Routing

Source, regressions and all seven dated RPI artifacts committed in
2af0c7f6b4d6155b63004d01e83dee9a60c14840,
`fix(web): preserve pending case edits and journey navigation`.
Author/committer privacy-safe identities, `Refs #526` and exact Copilot trailer
verified from the resulting commit. Worktree clean immediately afterward.
P01/P02 and all local tasks complete. This later documentation-only handoff
persists final plan/details/state; it changes no assessed source or test byte.

Task execution: full RPI loop complete, sole Review Complete / Conformant for
local code. Automatic session remains running at Follow-up with publication
blocked. No second critique, Review, Azure, push, remote reply or thread
resolution occurred. No fresh full-gate or hosted/human approval is implied.

Ranked current follow-up: coordinator runs the complete permitted exact-head gate
against freshly fetched main, verifies the external receipt immediately before
publication, obtains the required independent exact-head assessment, pushes this
topic normally, then replies to and resolves the five verified review thread IDs
from the research artifact. Keep `Refs #526`. No unrelated code work is invented.
