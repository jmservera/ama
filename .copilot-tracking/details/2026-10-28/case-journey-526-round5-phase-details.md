---
title: Case journey round five phase details
description: Task-level implementation and validation contracts
ms.date: 2026-10-28
---

Task `526-pr529-round5-20261028`. Research C1-C8 and W1-W2 are complete.
No unresolved implementation decision. Sole critique Revise preserved; PC-001
applied directly. Plan Ready.

<!-- rpi:phase id=P01 -->
## P01: State corrections

<!-- rpi:task id=P01-T01 -->
### [x] P01-T01: Chat cleanup

Reuse snapshotCaseFields/caseFieldUnchanged in both question handlers. A small
shared chat helper can clear only a matching snapshot after success. Keep raw
text for exact equality; request payload remains trimmed. Failure retains text.
Return on already-disabled send controls. Unit executes shipped chat functions
with deferred promises for unchanged/later/whitespace/failure/thread-failure
states. Browser holds each actual ask, exercises both forms, dirty/unload guards,
and preserves unrelated fields. No changes to advisory authority.
Retain the complete chat panel in caseSession (like retained draft/document
nodes), so both handlers and pending state survive ordinary same-case redraw.
Unit/browser subcases assert retained node identity and pending exclusion after
an unrelated call-save refresh, with matching cleanup and later/failure retention.

<!-- rpi:task id=P01-T02 -->
### [x] P01-T02: Proposal readiness

Save edited proposal gets identical disabled predicate. Retain textarea,
revision-bound restore and Reject. Unit renders actual assistantProposal across
each readiness and verifier state. Browser intercepts same-revision refresh,
restores edited JSON/reason, proves disabled controls and no edit-accept request,
then removes fixture override so existing successful review tests still run.

<!-- rpi:task id=P01-T03 -->
### [x] P01-T03: Count announcements and siblings

Keep semantic dd and navigation button; introduce atomic polite text span for
count wording only. Keep availability detail outside live text. Compare text
before assignment and do not replace unchanged tab labels. Unit executes
enhance/counts using a minimal DOM contract and measures actual writes.
Browser validates hidden AI tab, delayed multi-page count and unavailable
transitions; preserve the existing 38-scan count. Inspect all dirty cleanup,
asynchronous status and readiness/disabled paths in PR-changed web files,
recording both fixes and intentional behaviors rather than a blanket guarantee.

<!-- rpi:phase id=P02 -->
## P02: Evidence and delivery

<!-- rpi:task id=P02-T01 -->
### [x] P02-T01: Validation

From src/api use installed project distributions, PYTHONPATH tests plus sibling
core/agents tests: unittest test_case_journey test_workspace_scripts -q.
Use existing environment Ruff with --line-length 100, format and mypy.
Journey harness uses pinned axe 4.10.3 and external --out. Assistant harness gains
opt-in --axe/--out, checksum validation and scans of actual restored editor states.
Heavy checks share one flock -n admission with absolute <=2400-second retry
deadline; never inspect foreign output or interrupt its owner. No az invocation.
Completed: focused 17, related 43, final journey 207/38 axe scans, assistants 58/10 axe
scans; zero browser violations/page errors; real zoom passed. Static checks pass.
Original nonpassing harness attempts retained in changes record.

<!-- rpi:task id=P02-T02 -->
### [ ] P02-T02: Single Review and local commit

Refresh guidelines, reconcile plan/details/changes/state and exact source diff.
Fresh independent worker activates rpi-review, writes only the canonical review,
checks findings and evidence; no implementation or second Review. Preserve adverse
outcomes and route new findings as later work, not a conformant claim.
Commit implementation and all dated original artifacts with authenticated local
privacy-safe identity and required trailer. Record gate blocker; coordinator
owns exact-head publication and remote thread replies/resolution.
Sole Review executed Complete / Defects found with Low RV-001, preserved
unchanged. Later bounded test-only implementation and final journey rerun are
recorded separately; original Review is not repeated or upgraded. Local commit
is the remaining bookkeeping action.
