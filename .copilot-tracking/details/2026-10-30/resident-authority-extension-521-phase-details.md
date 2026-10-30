<!-- markdownlint-disable-file -->
# RPI Phase Details: Resident authority extension

## Metadata

* Task ID: 521
* Slug: resident-authority-extension-521
* Date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/resident-authority-extension-521-plan.md
* Research: .copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md

## Phase Index

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Validate and reconcile | Executed, residual infra static debt |
| P02 | Review and final gate | Review Complete / Residual work; final gate base-drift blocker |

## Validation Isolation Contract

Every setup/check uses env -i with only explicit PATH (external venv plus known
tool directories), HOME, TMPDIR, XDG_CACHE_HOME, AZURE_CONFIG_DIR, ZF_DATA,
PYTHONDONTWRITEBYTECODE=1 and tool cache paths under the owned external validation
directory. Do not copy or print ambient ZF/SQL/Azure/token variables or credential
files. No SQL/browser opt-ins in ordinary discovery. Pip uses existing manifests
and only its explicitly named public dependency index, never inherited pip config.
The requested PYTHONPATH is added explicitly for each command.

Only the separate owned SQL fixture may add its ephemeral synthetic local settings.
No actual resident/account credential is generated, accessed or stored.
Inspect current lock ownership before admission. Caller-specific flock -w 600
overrides generic nonqueued guidance; native runner must not be double-wrapped.

<!-- rpi:phase id=P01 -->
## P01: Validate and reconcile

Context: C1-C7 support authored implementation but historical runtime evidence
was blocked. Do not equate static inspection with SQL execution.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Restore tools and run bounded checks

External environment: /tmp/ama-521-validation-20261030. Existing missing-import
failure permits pip installation of src/core, src/agents, src/api dev dependencies.
Use non-editable installs to avoid generated package metadata in the worktree;
explicit source paths in requested tests remain current source.

Run under flock -w 600 /tmp/ama-rpi-heavy.lock:

* From src/api: PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
  python3 -m unittest discover -s tests -q.
* API: ruff check ., ruff format --check ., mypy.
* Core resident showcase and rendering tests; core Ruff/mypy.
* Infra resident secret/deploy tests with fake CLI, not actual Azure; focused
  infra lint/types following existing runner configuration.

Completion: exact exits/counts/skips recorded externally and in changes. Any
existing failure is isolated, not silently fixed outside scope. SQL integration
uses only runner-owned disposable local SQL, never inherited connection strings.

Correction after critique: the standard runner does NOT select the core resident
SQL class. Run it separately under the same lock with a newly owned labelled SQL
Server Developer container and random loopback port. A session-owned external
Python harness generates only ephemeral synthetic DB authentication in memory,
passes it through environment (not arguments/logs/files), records container ID,
ownership label and endpoint, checks those identities before connecting, waits
for an actual query, and invokes:
PYTHONPATH=src/core/src:src/core/tests python -m unittest -v
test_resident_showcase_sql.SqlBoundaryTests
with explicit ZF_TEST_MSSQL=1 and only its owned 127.0.0.1 endpoint.
Assert zero skips and all legacy/reapply/rollback/rights methods pass.
Use finally to remove only that exact owned labelled container. If Docker/driver/
memory admission is unavailable, record blocked SQL; no foreign fixture reuse.
This supplemental result is separate from the unchanged full receipt.

Changed infra static selectors: infra/scripts/resident_showcase_sql.py,
infra/tests/test_resident_demo_deploy.py and infra/tests/test_resident_demo_secrets.py.
Run ruff check --isolated --line-length 100, ruff format --isolated
--line-length 100 --check and mypy --follow-imports=silent on these paths.
Do not introduce lint/type ignores to hide historical untyped renderer debt;
report baseline findings and fix only new/coupled failures.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Correct coupled gaps and reconcile

Targets: changed source/infra/tests/docs from rebased commit only, unless a direct
consumer defect requires tightly coupled repair. No web target identified.
Preserve original historical evidence and append-only log. New source changes,
if any, need targeted regression first, then owning-package lint/type checks.
Do not modify tests merely to hide baseline failures.

Completion: truthful changes record, all task markers and evidence reconciled.
Rotation plan in infra/README.md remains a source-only operational proposal.

<!-- rpi:phase id=P02 -->
## P02: Review and final gate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Independent Review

Fresh reviewer assesses the complete current diff, plan, critique dispositions,
changes and issue criteria. Explicitly assess rotation/SQL renewal plan and
preserved min0/synthetic/scope/narrow-rights guards. Write only:
.copilot-tracking/reviews/logs/2026-10-30/resident-authority-extension-521-review.md.
No implementation or second Review after findings.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit and complete gate

Commit source and dated evidence after Review. Runner's native shared flock is
the lock owner; no nested flock wrapper. Permit only offline Bicep tooling using
the runner's isolated Azure configuration. No Azure resource API or deployment.
Fresh external receipt path: /tmp/ama-521-final-20261030 (must not already exist).
Run full gate after commit and current-main fetch, then verify exact-head receipt
if passing. Preserve failed receipts externally. Later commits invalidate it.
No push or PR. Final report distinguishes locally proven, partial and unproven
acceptance including required owner approval and live application.
After a passing gate, fetch and compare origin/main with the reviewed base before
verification. A fresh read-only assessor evaluates exact HEAD/base/receipt with
external output only. Drift invalidates the gate and blocks publication assessment;
do not repeat original Review or silently rebase.

## Initial Readiness

No unresolved implementation design choice. Local environment restoration and
required integration execution remain prerequisites, not evidence already earned.

## Current Execution Reconciliation

P01-T01 complete as execution: core 78/27 skipped, infra 32/0 skipped, API
1380/320 skipped and separately owned real-SQL 27/0 skipped all passed. API/core
Ruff check/format/mypy passed. Targeted infra findings reproduce on main and remain
failed, not waived. Initial missing-Node harness error and wrong-CWD retry are
preserved in changes; corrected final API run passed. No source defect emerged.
P01-T02 complete: only current operations/index/log evidence updated; no test,
runtime, resource, role, network or approval change in this continuation.
All owned pip build metadata/caches were removed from the candidate.

Origin/main moved from a02984e8 to 4b37c2c9 during execution. Per PC-006,
P02-T02's full gate/verification/exact-head assessment is blocked by base drift.
Commit original current Review and evidence; invoke the unchanged gate to record
its refusal, without silent rebase, private inputs, fallback or push.

P02-T01 executed once: Complete / Residual work, no new source defect. Review
technically assessed rotation/renewal as coherent; actual owner operational
approval and exact procedure/application remain pending. RV-001/002/003 route
publication/current-base, owner/live/funding and pre-existing infra debt separately.
P02-T02 is not complete and no full-plan or publication acceptance is claimed.
