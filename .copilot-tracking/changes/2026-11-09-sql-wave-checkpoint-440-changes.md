---
title: SQL feature-recovery wave checkpoint 440 changes
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109
---

## Order of work (genuine, prospective)

1. Research, plan, details, critique and state were written and committed first as `df45791be` (2026-11-09T15:39Z), before any local check or documentation edit.
2. P1 environment and import origins, then P2 targeted tests, then the documentation edit, then validation. Times are UTC from the shell clock.

## Documentation changes (append only)

* `docs/architecture/cutover-evidence-pack.md`: appended section `SQL feature-recovery wave current-main checkpoint (2026-11-09, Refs #440)` (+102, no deletion; `ms.date` already 2026-11-09).
* `docs/reference/README.md`: one index paragraph (+10). `docs/reference/log.md`: one appended entry (+5).
* No `src`, `infra`, `tools`, workflow, coordinator, BRD, PRD, ADR, memory or rubric change.

## Actual commands and outcomes

| Command (directory) | Exit | Result |
| --- | --- | --- |
| `git fetch origin main`; identities, equivalence diffs, hash comparisons | 0 | Equivalence commands empty or as recorded in the pack |
| `gh pr view 1308`, `gh run list/view`, `gh api .../status`, `gh issue view` | 0 | Reads only |
| venv plus `pip install -e src/core -e src/agents -e src/api` (owned `mktemp -d` dir) | 0 | Editable installs of this worktree; origins confirmed (`e15167d5`) |
| Core four-module unittest, first run (`src/core`) | 1 | 421 tests, 1 failure (SQLite concurrent opener, `database is locked`), 158 skipped; retained (`f3b54e83`) |
| Same failing test alone x3 | 0, 0, 0 | OK |
| Core four-module unittest serial rerun | 0 | 421 OK, 158 skipped (`3413ad0c`) |
| API six-module unittest (`src/api`) | 0 | 263 OK, 58 skipped (`8f630cfb`) |

* The first Core failure ran concurrently with the API selection (I launched both in one batch) on a host at load average 5.4; that overlap was an execution choice, not intended. Cause is unproven; not waived: it is recorded in the pack as F2 with the serial pass beside it.
* Logs are in `/home/azureuser/source/ama-demo-wt/logs-440-sqlwave/` (outside the repository). The owned scratch directory `/tmp/i440sw-TmmdQe` (venv, original logs) is removed at the end of the task; no shared path was written.
* No SQL admission, browser, Azure, model, job, `rpi-checks` or full gate run. No Docker image, cache or other session touched.

## Documentation validation

* `git diff --numstat`: 102/0, 10/0, 5/0 (no removed line). Added lines are ASCII with no em dash or bold marker. Table column counts consistent. New heading anchor resolves for the index and log links.

## Amendments and divergences

* Plan phase 3 said `ms.date` stays; confirmed no change was needed. No divergence from the plan. The PR-head rollup was corrected from "19 green" to 18 successful check runs plus one `rubric/score` status after critique PC-003.
* During the work `origin/main` advanced by a rubric-bot commit `ef28d4da` (only `latest.json`); recorded in the pack, no merge made.
