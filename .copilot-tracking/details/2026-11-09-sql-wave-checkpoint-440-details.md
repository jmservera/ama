---
title: SQL feature-recovery wave checkpoint 440 details
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109
---

## Phase 1: environment and import origins

* Create `OWN=$(mktemp -d /tmp/i440sw-XXXXXX)` and a venv at `$OWN/venv`; logs at `$OWN/logs`. Move logs to the sibling external directory `/home/azureuser/source/ama-demo-wt/logs-440-sqlwave/` before handoff; the repository never contains logs.
* `pip install -e src/core -e src/agents -e src/api` in the venv. Never `uv`, never private data.
* Print each package's namespace `__path__` (the `zava_forward` packages have no `__init__.py`, so `__file__` is `None`) and the concrete module origins `zava_forward.core.sqlstore`, `zava_forward.core.mssqlstore`, `zava_forward.api.server` and an agents module, plus the SQL driver origin if installed. The `zava_forward.*` origins must be under this worktree; the driver origin is expected under the venv and is recorded as such, not asserted under the worktree.

## Phase 2: targeted tests

* Commands as in the plan, each `cmd > log 2>&1; echo $? > exit`. Preserve first failures.
* Environment: no `ZF_TEST_MSSQL`, no `ZF_SQL_TASK_MANIFEST`, no Azure variables, `ZF_DATA` pointing at an owned temp path only if a test needs it.

## Phase 3: documentation edit

* Append `## SQL feature-recovery wave current-main checkpoint (2026-11-09, Refs #440)` after the last section of the pack; #1292 and #81 appear in the text as traceability references only. Subsections: Identities, Source equivalence, Requirement trace, SQL-wave behavior read from source, Evidence by class, Current observations, Findings and owners, Exclusions, Recommendation and resume conditions.
* Add one paragraph to `docs/reference/README.md` next to the previous checkpoint entry; append one entry at the end of `docs/reference/log.md`.

## Phase 4: validation

* `git diff --stat`, `git diff --numstat`, added lines ASCII and em dash grep, anchor check via the slug of the new heading, `git diff origin/main -- docs/reference/log.md | grep '^-' ` must show no removed lines, `git diff --name-only origin/main` allowlist.

## Phase 5: review and handoff

* One original Review in `.copilot-tracking/reviews/`, commit with the repository-local noreply identity resolved by `gh api user`, handoff `handoff-440-sql-wave-checkpoint.md` in the coordinator files directory.
