<!-- markdownlint-disable-file -->
# RPI Changes: employee-case-workspace

Date: 2026-10-27. Declared scope: full plan P01/P02.
Plan: .copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md.
Details: .copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md.
Single critique preserved with direct PC-001/002 dispositions; PC-003 rejected
as a worker-only filesystem restriction, not a parent constraint.

## P01-T01: Script recovery

Implemented route-specific readiness/error recovery in app.js using safe typeof
checks. Required missing file paths produce Reload workspace (document reload),
generic API failures retain Try again (route-only). No partial quality screen.
Current source and installed serving ops bytes already match; not a deployed
missing-wire fix. Three Chromium scenarios pass, including unrelated missing
specialist module not blocking ordinary case/queue.

## P01-T02: Assignment scope and AI settings

Implemented wording-only briefing change and component runbook update. No change
to ownership query, role mapping, release/incident control or AI activation.
Read-only model management follow-through found the existing employee Foundry
OpenAI endpoint, but zero deployments. README now explicitly says env alone
cannot restore inference: actual authorized employee models/releases are needed,
and resident resource/budget is not a fallback. This is a directly relevant
configuration clarification, not source or deployment expansion.

## P02-T01: Validation

Initial targeted checks: 90 unittest cases passed; three real-server Chromium
scenarios passed (Chromium 156.0.8078.4). Six added unittest method definitions
(task mixin repeats three on JSON/SQLite); zero removals. Node syntax, diff
whitespace and changed-file Ruff passed. First mypy run caught missing generic
dict type in new browser fixture; corrected to dict[str, Any] without exemptions.
Full discovery: 1130 tests in 411.838s, OK (314 explicit opt-in skips).
No failing tests. Isolated pip environment restored after missing
zava_forward dependency. Existing real-server harness uses constructed fixtures.
No full gate per owner; no deployment, secret or private data access.

Final changed-file Ruff/mypy passed for browser module and core Store; Node
syntax and git diff whitespace passed. Existing workbench Chromium check passed
all eight implemented roles and shared navigation/queue checks without pageerrors.
Negative control served pre-change app.js from git with ops.js HTTP 404:
actual alert was exactly "qualityPanel is not defined"; Try again retained
that error and ops request count stayed 1. Final source passes named recovery
and re-fetch assertions. This proves the failure class and ineffective retry,
not the upstream cause of the owner's deployed failed script execution.

## Reconciliation and Review Handoff

P01/P02 and all task markers complete, matching details and evidence. Six added
unittest method definitions, no removals, one three-scenario browser module
within locked bounds. No significant implementation divergence or second critique.
Validation logs are external session artifacts; commands and outcomes are above.
No required human acceptance checkbox is marked complete. Original exact live
failure/current owner mapping, authorized model deployments/releases and later
redeploy remain follow-up-only. Ready for one independent source Review.

## Blockers and Remaining Work

Exact original live authenticated asset failure and current owner mapping are
unobserved. These remain owner/operator follow-ups, not source acceptance.
