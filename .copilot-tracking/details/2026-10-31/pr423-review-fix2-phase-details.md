---
title: PR 423 review fix2 phase details
description: Evidence and completion boundaries for the preservation-first repair
ms.date: 2026-10-31
---

Task ID: pr423-review-fix2. Candidate plan:
.copilot-tracking/plans/2026-10-31/pr423-review-fix2-plan.md.

<!-- rpi:phase id=P01 -->
## P01: Integration and correction

<!-- rpi:task id=P01-T01 -->
### P01-T01: Merge and preserve

Start head 7eba611664c12d09270c5765575a57d1aea1a936, fetched main
ec2d784255c3377ab39e5d2d1b5140e76c8e7f36. Use merge --no-commit,
not rebase. Read-only merge-tree finds only latest.json conflict; select main's
blob. Preserve both log append ranges even if conflict state changes.
Verify no unintended deletion and imported main source remains byte-identical.
Do not alter unrelated main UI behavior.

Completion evidence: merge has only latest.json conflict, resolved to main.
Both parent logs pass ordered-subsequence preservation; branch log unchanged.
All imported main src/tracking files are byte-identical; no deletion.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Exact allocation and page regressions

Research C1-C4: range/all-page checks and regressions already exist. Keep
download offset=0,length=MAX_BLOB+1; replace readall with explicit
read(MAX_BLOB+1). Fake read accepts an explicit size, enforces size, tracks
actual returned bytes; forbid unbounded readall in regressions.
Test replacement after listing and within/outside bounds, verify job cleanup.
Strengthen exact requested page counterexample to test write_result performs
no upload. Keep exact/head/unicode/page-count controls and all-pages check.
No speculative replacement of correct split_pages logic.

Completion evidence: explicit read bound and two new tests implemented; full
74-test transport suite passes. Existing all-page/head/exact counterexample
controls retained and no-upload check strengthened.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Current runbook and provenance

Research C5-C8: active examples already correct. Add explicit default=false
prerequisite and clarify disabled incremental deployment is not grant cleanup;
manual IAM retirement requires approval. Historical includeResultRelay
commands remain unchanged, but surrounding text is past-tense and warns that
the current template no longer accepts that parameter.
Qualify old changes record for this new integration: run9 and f30d9583/
b4d467ca are historical, not current VERIFIED provenance. No successful
receipt exists for integrated candidate. Do not edit PR body remotely.

Completion evidence: current prerequisites/default-off grant/IAM cleanup and
historical parameter wording clarified; old changes record qualified for
ec2d7842 integration. PR body untouched.

<!-- rpi:phase id=P02 -->
## P02: Validation, Review and local delivery

<!-- rpi:task id=P02-T01 -->
### P02-T01: Offline validation

Baseline command already failed with missing zava_forward. Use pip to install
needed distributions into task-owned external venv, no source-path workaround.
Run unittest discover -s infra/tests -p test_staff_azure.py -q; then related
identity/RBAC/Bicep policy and infra suite if practical. Bicep 0.48.1 is available;
compile relevant templates to external paths, no Azure command.
All heavy commands take the shared flock with 600-second wait. Preserve actual
results including prerequisite failures. Focused Ruff/format/mypy if available.
No full receipt claim; complete gate is required before later publication.

Completion evidence: missing core namespace restored with pip for core/dev,
agents and API externally; first broad run lacked yaml (478 tests succeeded,
one import error). Restored workflow-pinned PyYAML 6.0.3. Full infra suite:
507 tests, OK, zero skips. Ruff check/format and mypy passed for changed Python;
staff-initializer-rbac and storage direct Bicep builds succeeded. Compiled
policy tests ran offline with REQUIRE_AZ_BICEP=1. No Azure operation.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Independent Review and commit

Invoke one fresh independent Review worker on exact staged candidate, plan,
details, research and test evidence. Write one dated Review artifact and keep
findings/outcome intact; no re-review loop. Route later work explicitly.
Commit local merge/corrections/evidence using authenticated account's
8036360+jmservera@users.noreply.github.com for author/committer and exact
requested Copilot trailer. Verify parents, branch, clean tracked status and
remote unchanged. No push. A final receipt for this commit is not proven.

Completion evidence: one independent Review Complete / Residual work, zero
scoped source defects, original assessed boundary preserved. Local merge commit
3ad8afc909d5fb120e4d75c8a15dd2085aefda7f has parents 7eba6116 and ec2d7842.
Author/committer privacy-safe address and exact Copilot trailer verified.
Owner PR head remains 7eba6116; no push or PR body edit. P02-T02 complete.
The following local evidence commit does not change source or establish a
full-gate receipt, independent exact-final-head approval or live acceptance.
