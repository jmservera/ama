---
title: In-VNet staff initialization phase details
description: Task-level evidence and completion expectations for Refs #360
ms.date: 2026-10-16
---

Task: 360-run-in-azure.

## P04: Rebase-only continuation (2026-10-17)

P04-T01 preserves the complete origin/main tree for #176 and #175 while
retaining #360 source, image/dockerignore/timeout corrections and both hashed
requirements workflow installs. Use GIT_EDITOR=true and resolve only clear
combined intent. Record every conflicted file and actual disposition.
P04-T02 uses a new pip-only venv with no system site packages and the existing
source/hashed runtime/PyYAML dependencies. Execute targeted test_staff_azure
and test_pipeline, full infra with REQUIRE_AZ_BICEP=1, and the exact ten-file
Ruff/format plus three mypy commands recorded in changes. No uv, Docker
bypass, image builds, Azure service calls or private input.
P04-T03 reviews resolutions read-only once, leaves original live blockers
open, then records evidence before the single force-with-lease publication.
Authenticated id/login was resolved and local privacy-safe email configured
before commits. No amending outside rebase; no issue closure or merge.

P04-T01/T02 completion: rebase onto c9ba95f succeeded, only index/log conflicts;
combined entries and exact upstream recovery retention verified. Fresh pip
venv passed 21 staff, 28 pipeline and 307 full infra tests with zero skips,
exact ten-file Ruff/format, three mypy commands, local Bicep build/lint and
git diff --check. Source/workflows match d050003; upstream source matches main.
P04-T03 is ready for one resolution-focused Review then publication.

P04-T03 local Review now Complete, outcome Residual work; no source defect.
Only the parent-owned single lease push/PR update remains at evidence commit
time. Final response and PR readback own the exact published SHA; no further
tracking-only closeout push is planned. Session remains manual/stopped.

## P01

### P01-T01

Use existing initializer SQL position/identity checks, transaction and audit.
Factor Graph retrieval from preparation, passing validated person objects from
operator login. Worker imports existing initializer without invoking its CLI.
Connection uses inherited mssql-python and SQL-admin MSI. Candidate results,
summaries and failure status must be encrypted with a secret-held random key.
Never print tracebacks or plaintext SQL/roster data.

### P01-T02

Use existing Azure private body helper with management-plane job create/start,
execution-status and authenticated environment-log capture, stop/delete cleanup.
Validate API and init job
share one ama environment, exactly the expected init identity and private SQL
administrator. Reuse only source image/registry, safe resource limits and explicit
SQL env. Roster goes into secretRef, never command args. Failures print exact
private-host fallback. Read-only SQL checks disclose transient control-plane work;
dry-run never runs jobs. No new identity/network or storage permission.
The standalone API-only custom role in infra/staff-initializer-rbac.bicep
grants the existing MI app/revision/replica reads and revision restart only;
deployment is not run. The worker verifies SQL then uses its own MI to execute
the canonical restart/replica convergence helper. Source image/assets must be
built and pinned separately, never repaired by embedding untracked source.

## P02

### P02-T01

Fake az owns complete job lifecycle and records arguments, private ARM body files,
encrypted output and cleanup. Assert directory calls never originate in worker;
local and explicit/blocked paths remain covered. Reuse canonical initializer tests
to verify immutable bindings, role/supplier coverage and preserved history.
Docs must distinguish operator-owned Graph work from job-owned SQL/restart.

### P02-T02

Run existing infra suites and targeted Ruff/mypy, local synthetic app smoke without
private data; no Azure build/validation. Review once after implementation and
record criteria as proved locally or unmet live. Privacy-safe commit and PR with
Refs #360; no issue checkbox edits or merge.

## P03: Correction cycle 1 (2026-10-17)

Planning opening: research is complete and Ready; no unresolved implementation
choice. Preserve existing task identity, phase history and deployment blockers.

### P03-T01

Before each full infra discovery in mvp-validation.yml and src-ci.yml run
`pip install --require-hashes -r src/api/requirements.txt`. Retain the existing
pinned PyYAML installation and workflow/check names. Extend
infra_test_dependency_errors to require that command before discovery. Add
positive and removal/unhashed/late-install mutation coverage, maximum two
test methods. No runtime changes or manifest churn.

### P03-T02

New clean venv: /tmp/ama-360-correction1-YRmaea, Python 3.12.3,
include-system-site-packages false. Baseline command mirrors MVP source
`--no-deps` and PyYAML installation; 21 staff tests fail (14 failures/four
errors) exactly as CI before correction dependencies are installed.
After installing the workflow's hashed lock, run full infra discovery with
REQUIRE_AZ_BICEP=1, then existing src namespace Ruff/format and mypy commands.
Run named BuildContextTests and decoded-result timeout regression; execute
in-memory negative controls for each new staff context allow rule and timeout
acceptance guard. Mutation test failure is the required success signal.
Keep full commands/results in the existing changes and review artifacts.

### P03-T03

Read-only one-cycle Review assesses workflow order, real crypto paths,
unchanged prior corrections and full clean-venv evidence. Reconcile plan,
details, changes, review and state. Resolve GitHub id/login and configure
local noreply for author/committer. Commit with Refs #360 and Copilot trailer,
push only feat/run-in-azure-360 and update existing PR #370. Never merge,
force-push or claim local evidence establishes live acceptance. RV-001 through
RV-003 remain separate authorized follow-ups. Stop after publication.

P03 completion receipt: source head 6976ae9649de291409c771986b818b83e0ebc8ae
was committed, pushed and reported in updated PR #370. Full infra discovery
rerun there: 307 tests, no skips, 66.039 seconds. All P03 tasks complete;
remaining receipt is tracking-only and does not alter assessed source.
No live acceptance or continuing automatic session.
