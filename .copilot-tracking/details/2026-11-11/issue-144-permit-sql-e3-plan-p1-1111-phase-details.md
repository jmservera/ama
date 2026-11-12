---
title: Issue 144 permit SQL E3 plan P1 phase details
description: Phase gates, receipts, failure classification and pause or resume conditions for the corrected real-MSSQL permit validation recipe
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e3-plan-p1-1111
---

## Phase gates

* Phase A, this launch (done): Research and Plan correction of the frozen plan. Artifacts only. No execution of any kind.
* Gate G1: independent prospective clearance of this corrected plan by the same independent reviewer (Root forwards the actual P1 delta). Blocking findings must be resolved first; unresolved REQUEST_CHANGES means no Implement.
* Gate G2: Root's explicit admission of Implement and execution, including the conditional pip admission (X2) and the heavy-resource run (X6 to X10). Neither gate is claimed here.
* Phase B (future, same E3, only after G1 and G2): create the single `src/api/tests/test_permit_sql.py`; author external scripts under `X/scripts`; run X0 to X10 in order; classify results; write dated changes and review records; commit the test and records.
* Phase C (future): authored review labelled authored; independent exact-head assessment is Root's.

## Order and stop rules for Phase B

1. X0, then X1 (expected failing probe preserved), then X2 only on the failed probe.
2. X3 static must pass on the new module before any SQL starts. A static failure is a test-authoring defect inside the same E3 only if Root admitted Implement; otherwise stop.
3. X4 and X5 (no heavy lock) before X6.
4. X6 admission; busy lock, memory, disk, image or port failure: UNADMITTED, stop, report SQL as unobserved, no substitute and no queue.
5. X8, then X9. Each producer exit is its own file. No retry-until-green; a rerun only with Root's explicit admission and a new unique name.

## Failure classification (never conflated)

* Source defect: a fixed-source (V) assertion fails in a case whose every R5 witness is valid. Record evidence on existing #144 and stop for Root; no source fix, no new issue, no further cycle.
* Invalid setup: R1 assertion, scratch identity, holder SPID or `@@TRANCOUNT` change, missing or wrong DMV witness (lock granularity, permission), headroom miss, coordination overrun, container readiness, resource error. Reported INVALID; no defect claim.
* Expected mutant failure: a failing set equal to the R2 row, `AssertionError` with the expected label. Any other mutant result is INCONCLUSIVE and blocks success.
* Environment or tool failure: pip, wheelhouse, docker, driver timeout. Reported as blocked or unobserved.

## Receipts per run (unique names, outside `scratch/`)

Driver stdout and stderr and exit per producer; first-failure full trace; wheel and file sha256 and `pip freeze`; source snapshot manifest (`git ls-files` list, tree hash, test file sha256); mutant diffs and hashes; origin probe output per process; allowlisted docker receipt; SQL Server version; sqlguard manifest hash (never the password); DMV witness records (holder and claimant SPID, database id, wait type, wait resource, statement offsets, applock granted) and database clock records (`L0`, observation, release, reservation read, `issued_at`); framework `Ran`/`OK` lines; database readback before container removal; cleanup readback; credential-token scan result; sha256 manifest.

## Pause and resume

Paused after this plan correction. Resume only on Root's explicit admission naming G1 clearance and G2 scope. The independent reviewer's original report and the authored proceed critique of the parent plan remain unchanged adverse history; this correction does not backfill phase witnesses and no canonical phase-witness chain was requested for this launch (recorded, not regraded).
