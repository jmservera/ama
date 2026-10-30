---
title: Sensor ingestion consistency changes
ms.date: 2026-10-30
---

## Scope and Status

Task 188, full approved plan. Implementation complete; P01/P01-T01 and
P02/P02-T01/P02-T02 checked. Original Review and committed-candidate gate next.
Plan/details/research use sensor-ingestion-consistency-188 and 2026-10-30.
Original critique Revise retained; PC-001/003 applied, PC-002 rejected because
its worker-only path restriction is not a parent constraint and conflicts with
explicit caller direction. No second critique.

## P01: Shared Model and Statistical Contract

P01/P01-T01 implemented: existing sensor_stream now accepts optional composed
climate and dated measures, reuses full-origin projection and validates climate
coverage. Descriptor binds climate, composed/household/retrofit parameters and
dated-history hash. Default legacy output remains unchanged.
New typed sensor_consistency report checks complete grid/identity/units/schema
and point/mean-step/population-stddev limits per channel, default zero.
Five focused handover tests and twelve existing replay tests pass locally.
Initial lint issues fixed; initial mypy found two dynamic-kwargs test errors,
corrected with explicit typed channel arguments. Recheck pending.

## P02: SQL Evidence and Validation

Active P02. Missing packages observed and restored with pip in /tmp/ama-188-venv;
no dependency manifests changed. No cloud execution or credential files.
The first queued focused-test lock wait was stopped by this task before
execution; small unit tests ran as lightweight work. Foreign heavy lock
ownership was observed; no foreign process interrupted or output inspected.

### Focused SQL/Receiver and Static Evidence

The composed CSV prefix and SDK-decoded suffix query together for two homes,
24 readings at three/day. Reopened whole-window replay preserves exact values,
24 delivery outcomes, zero DQ and case/audit snapshots in SQLite.
The existing fake HubReceiver seam now uses the composed path and passes.
Initial fixture failure (cases.seq required) was corrected by cloning the
existing projected case columns; a misplaced snapshot assignment briefly caused
a syntax error and was corrected before the successful rerun.

Core Ruff check/format/mypy pass (167 files), API Ruff check/format/mypy pass
(117 typed files). Five new core report tests, twelve existing stream tests and
ten existing composed writer tests pass. Decimal point/mean/statistical
calculations include 0.1 and 0.5 inclusive boundaries, independent temperature/RH
channels and isolated point/mean/stddev failures.

Migration regressions initially failed seven missing pptx/PIL imports under
system Python. Installed the existing tools/rename-zava-requirements.txt into
the task venv using pip; rerun passes all 25 tests. The expected malformed-PPTX
diagnostic is a passing negative control.

### Heavy Validation Admission

Locked API discovery/static/owned-SQL batch is queued with the caller's
`flock -w 600 /tmp/ama-rpi-heavy.lock`. Logs are external under
/home/azureuser/.copilot/session-state/b669b987-2355-43d4-99ca-bf7c5c0215a9/files/validation-188.
This is not yet a pass or actual SQL Server evidence.

The batch subsequently acquired the shared lock. Requested API discovery,
from src/api with
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`
and task-venv `python3 -m unittest discover -s tests -q`, passed:
1,408 tests in 492.700 seconds, 318 reported opt-in skips (not executions).
Both owning projects' Ruff check, Ruff format --check and mypy then passed.
Task-owned SQL selector is still running; no Azure evidence is inferred.

The owned SQL helper then passed all 46 tests in 20.649 seconds, including
`test_sensor_consistency.SqlHandoverTests.test_composed_joint_query_statistics_and_reopened_window_replay`
with its asserted MssqlStore backend. SQL Server was responsive on a random
loopback port, and its exact owned container was removed. Actual local SQL
Server therefore proves joint per-home queries, all-zero declared handover
errors and exact 24-reading/24-delivery/zero-DQ reopened replay.

## Acceptance Evidence

| Issue criterion | Proven boundary | Not proven |
| --- | --- | --- |
| Live and backfill jointly queryable per home | Constructed CSV prefix plus SDK-decoded suffix, two home IDs, SQLite and actual local SQL Server, twelve rows/home | Actual authenticated Hub transport and Azure SQL |
| Statistical handover within tolerance | Per-channel zero C/RH point, reference-adjusted mean-step and population-stddev errors; independent drift/metadata/coverage/tolerance negative controls | Actual live handover or physical sensor statistical validity |
| Re-running a window idempotent | Reopened entire 24-observation window, all accepted replay receipts, unchanged readings/deliveries/DQ/cases/audit on SQLite and local SQL Server | Actual live Azure restart/recovery |

No whole-issue acceptance, hosted/human approval or live #110 delivery is claimed.

## Amendments and Divergences

Immediately relevant sequencing clarification: P02-T02 owns documentation,
validation and Review readiness; original Review, commit and complete gate are
subsequent lifecycle gates. This removes a circular completion condition without
waiving any check or changing user scope. Final focused rerun: 27 core tests
passed in 1.602s; changed-file lint/format and diff whitespace passed.
Actual Azure acceptance remains outside authorized local execution.

## Review Handoff

Ready for one independent original Review. Plan/details markers, completion
evidence, validation and live follow-up boundaries reconciled. No active
implementation task remains. Full committed-candidate gate remains required
after original Review and local commit, with external evidence, not a pass yet.

The independent original Review subsequently completed with outcome Residual
work and no implementation defects. RV-001 retains live evidence; RV-002 routes
the expected post-Review candidate/publication validation to the parent and
coordinator. Original Review and critique remain immutable evidence.

## Candidate Handoff

The four-phase local RPI loop is complete, not whole-issue acceptance.
The next lifecycle operation is a privacy-safe local commit, followed by
`python3 tools/rpi-checks.py --all --base a31048f15fa3120c58bacd22a375d86ae5ab7431
--out /home/azureuser/.copilot/session-state/b669b987-2355-43d4-99ca-bf7c5c0215a9/files/rpi-188-final`.
The runner owns the same shared heavy lock; do not nest a flock around it.
This committed handoff cannot self-certify its later gate. The authoritative
post-commit result/log/receipt stays external at that path. The coordinator must
inspect actual output, fetch current main and verify any passing receipt before
independent exact-head assessment and separately authorized publication.
No push, hosted approval, human acceptance or live authority is inferred.

Before sealing the candidate, preserve this run's generated ignored
bytecode/lint/type/editable-metadata caches in the external session directory
using an explicit per-file hash/size selection, archive readback and restored
copy verification before removing only those selected generated files.
Retain the archive, restore copies and journal; preserve every original RPI
artifact and all tracked/untracked source bytes. No historical tracking cleanup.

Commit-helper limitation: its referenced commit-message instruction file and
get_changed_files tool are unavailable in this host. Use the repository's
Conventional Commit convention and explicit caller trailer/privacy requirements;
inspect the staged delta with the available Git CLI rather than invent a tool
result. This does not waive final source/base/receipt verification.

Cache sealing completed: 262 selected generated files were archived, restored
and hash-verified before exact-file removal. Protected source/RPI hashes were
unchanged and no ignored candidate input remained. Selection, archive, restored
copies and prune journal are external under
/home/azureuser/.copilot/session-state/b669b987-2355-43d4-99ca-bf7c5c0215a9/files/owned-cache-preservation.
