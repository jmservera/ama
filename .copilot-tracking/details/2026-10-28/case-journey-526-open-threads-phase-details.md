---
title: Case journey 526 open threads phase details
description: Bounded implementation and validation expectations
ms.date: 2026-10-28
---

## Metadata

Task ID: 526-pr529-open-threads-20261028.
Plan: .copilot-tracking/plans/2026-10-28/case-journey-526-open-threads-plan.md.
Research: .copilot-tracking/research/2026-10-28/case-journey-526-open-threads-research.md.

<!-- rpi:phase id=P01 -->
## P01: Corrections

Context: five exact unresolved review threads, C1-C7. Boundary: existing case
workspace and tests, no visual redesign or server approval change.
P01 complete: source and focused checks recorded in changes; P02 full requested
validation completed, including a preserved first browser environment failure and
successful unchanged-source retry. P01-T02 amendment adds confirmation before replacing
dirty document/resident outputs, preserving the existing explicit discard boundary.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Dirty guard and isolated harness

Place a shared dirty predicate within the route harness's extracted source.
Reconcile cached fields against live controls before checking pending count and
DOM flags; avoid false warnings from already submitted clean controls.
Both route and beforeunload call it; tab-only fast path remains first.
VM globals include caseSession, funding cache, URLSearchParams and guard stubs.
Regress pending-only leave cancellation, unloading and clean reconciliation.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Review race and siblings

Capture reason/text before request; only clear fields actually submitted and
unchanged. Retain newer values as read-only recovery explicitly labelled with
record identity. Completed review buttons cannot issue another review. The
document paragraph and audit status show dispatch-time submitted values.
Ensure recovery survives ordinary refresh and remains included in leave warning.
Exercise delayed success text/reason changes, unchanged success and failure.
Inspect aiNotes callers, assistantProposal, refresh, draft replacement and recovery
cache cleanup for the same dispatch-time/hidden-control patterns; fix coupled
instances, record out-of-scope findings without speculative redesign.

<!-- rpi:task id=P01-T03 -->
### P01-T03: URLs and receipt

Build step hrefs from current URLSearchParams with only tab replaced. Expose a
small controller sync hook and call it after challenge in-place replaceState.
Retain native anchor semantics, current focus behavior and step states.
Regress page parameters after actual pagination with dirty drafts and click a
journey link without confirmation, redraw or value loss; back/forward still work.
38 scans exact; receipt fixture and negative tests change together. Workflow hash
pins remain unchanged and checked against actual tracked bytes.

<!-- rpi:phase id=P02 -->
## P02: Validation and evidence

Dependency: P01. Existing .venv, synthetic fixture server and external axe source
only. Generated reports stay in a unique external session directory.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Commands and expected evidence

From src/api use installed .venv distributions and
PYTHONPATH=tests:../core/tests:../agents/tests. First test_workspace_scripts and
test_case_journey, then unittest discovery. Run tools/test_rpi_checks.py.
Run journey browser with hash-pinned axe; retain 38 scans and keyboard/zoom checks.
Ruff with line limit 100 and JS parse checks. Heavy command wrapper uses flock -n
on /tmp/ama-rpi-heavy.lock, 15-second retries with an absolute 2400-second deadline,
never a blocking flock. Preserve each attempt's separate log and actual outcomes.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review, commit and gated publication

Fresh independent reviewer activates rpi-review, scoped to this diff and evidence.
Record execution, outcome, remaining findings and no human approval inference.
Fetch main; no full gate invocation that would call prohibited az. If blocked,
commit locally using authenticated noreply identity and required trailer, retain
Refs #526 and report remote replies/resolution deferred until coordinator push.
Do not repeat Review or rewrite historical failures; route findings as later work.
Unresolved in-scope findings or failed mandatory checks yield Not accepted/Blocked,
not accepted delivery. A local checkpoint commit does not erase those findings.
PC-001's worker-only filesystem restriction is not a parent constraint; retain the
user-specified actual shared /tmp lock, never an uncoordinated substitute.
P02-T01 complete: API 1168 tests/316 opt-in skips, focused 14, tooling 31,
journey 153 assertions/38 zero-violation scans/real 200% zoom, assistants 30.
P02-T02 complete: sole Review Complete / Conformant for local code, no substantive
findings; authorized source/evidence commit
2af0c7f6b4d6155b63004d01e83dee9a60c14840 verified. Remote publication remains
blocked independently by the prohibited full-gate az prerequisite.
