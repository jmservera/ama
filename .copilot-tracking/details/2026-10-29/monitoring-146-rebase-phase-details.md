---
title: Monitoring 146 rebase phase details
description: Task-level resolution and validation contracts
ms.date: 2026-10-29
---

Task ID: pr-512-rebase-2026-10-29.
Evidence: .copilot-tracking/research/2026-10-29/monitoring-146-rebase-research.md.
Initial direction: bounded existing-branch reconciliation, no publication.

<!-- P01 -->
## P01: Rebase and reconcile

<!-- P01-T01 -->
### P01-T01: Resolve actual conflicts

Run `git rebase origin/main` with noninteractive editor; on conflicts read
stage 2 (upstream) and stage 3 (replayed topic). Preserve all upstream sections
and add the monitoring index block and full original monitoring log entry.
Keep one latest date if frontmatter conflicts. Stage only resolved paths and
continue until both original commits are replayed. Own new untracked RPI
artifacts are not pre-existing owner changes and must not be stashed.

<!-- P01-T02 -->
### P01-T02: Verify semantics

Compare original head and rebased source delta; verify upstream rubric directory
and scenario manifest equality. Check both upstream and original log entry
sequences survive, and both index link blocks. Confirm original RPI evidence
unchanged. Verify upstream model/endpoint output wiring coexists with disabled
monitoring and PT26H ledger range. No legacy runtime paths added.

<!-- P02 -->
## P02: Validate

<!-- P02-T01 -->
### P02-T01: Python quality and focused regression

From each of src/core and src/api, use `/tmp/mv/bin/ruff check .`,
`/tmp/mv/bin/ruff format --check .`, and `/tmp/mv/bin/mypy`.
Set `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests`
as applicable for focused unittest modules. Always run
`test_scenario_manifest`; run dependency-rule modules independently per owner.
No full API discovery is needed for infrastructure/docs-only changes; any
expansion must first satisfy `flock -n /tmp/ama-rpi-heavy.lock true`, and hold
the same lock throughout a heavy run. Do not read private datasets.
Use session-owned external caches/logs where practical. Existing tests retain
their normal temporary-fixture lifecycle; no parent constraint prohibits /tmp.
Do not delete unrelated or historical files.

<!-- P02-T02 -->
### P02-T02: Infrastructure integration

Use `/tmp/mv/bin/python` with `PYTHONPATH=infra/tests` for
`test_bicep_policy test_iothub_module test_container_contract test_governance
test_secret_lifecycle`; add the existing model/deploy tests if the merge
surface warrants it. Run offline `az bicep build --file infra/main.bicep
--stdout`, never ARM deployment/what-if. Preserve exact commands, counts,
failures, corrections and skip reasons. Missing prerequisites are concrete
blockers, not permission for Azure/cloud fallback.

<!-- P03 -->
## P03: Review and commit

<!-- P03-T01 -->
### P03-T01: Independent Review

Reconcile all task markers and evidence, then delegate one bounded independent
Review with research/plan/details/critique/changes and exact fetched base plus
rebased implementation boundary. Worker writes only its review artifact.
Route findings to later follow-ups; do not loop into another implementation
or Review in this task. Human/operational review boxes remain untouched.
Classify every finding: original operational/publication residuals may remain
follow-ups, but unresolved new correctness or required-check failures mean
local candidate Not accepted/Blocked. Committing evidence is not acceptance.

<!-- P03-T02 -->
### P03-T02: Local handoff

Use authenticated account privacy-safe email already configured locally.
Commit explicit task-owned paths with Conventional Commit subject and Copilot
trailer. No push, force push, PR update, merge or Azure operation.
After final commit confirm clean status, ancestry and local-vs-remote divergence.
External final gate/hosted CI and any main movement remain coordinator duties.
This is not a full publication-gate receipt.
Successful local handoff requires no unresolved in-scope correctness or
required-check blockers; otherwise report an explicitly blocked/evidence-only
handoff with the exact original Review outcome.

## Current Implementation Reconciliation

P01-T01/P01-T02 complete: two commits rebased onto the recorded base,
README/log conflict contributions preserved exactly. The README keeps one
latest date. Main-owned rubric/scenario content is unchanged. Upstream models
and monitoring source coexist; original seven RPI artifacts are byte-preserved.

P02-T01/P02-T02 complete: both projects pass Ruff/format/mypy; 10 core and 11 API
focused tests pass, plus 91 focused infrastructure tests and offline Bicep
compilation. No skips, new tests, runtime edits, package changes or full API
discovery. Exact commands and external evidence digests are in the changes
artifact. P03-T01 now complete: one independent Review Complete / Conformant,
zero new findings. P03-T02 remains local evidence commit and confirmation.
No new implementation or repeat Review follows this outcome.
