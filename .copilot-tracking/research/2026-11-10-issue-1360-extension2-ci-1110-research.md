---
title: Issue 1360 extension 2 CI regression research
ms.date: 2026-11-10
task_id: 1360-extension2-ci-1110
---

## Scope

Owner approved five additional corrections on 2026-11-10; E1 is spent; Root admits one new E2 (three left after). No reset or auto-renewal. Head under work: `29d94d10` (source `c7d570c8`), merged with main `6f5e5007a` (Atlas checker/tests/RPI only, no conflict). Planning Readiness: Ready. Raw hosted logs `ci1426-core-failed-2350.log` and `ci1426-mssql-failed-2350.log` are original adverse evidence and stay unchanged. E1 approval and the missing raw red are not rewritten.

## Reproduced red (local, own venv, `/tmp/e2/red-core-selectors.log`)

Four selectors at the merged head: 2 errors and 6 failures, matching hosted Core (6 fail, 2 error) and MSSQL (4 fail, 2 error):

* `test_hazard_referral.SqlHazardReferral.test_failed_writes_preserve_prior_pending_audit_and_original_error` (postcommit_sync_failure x2)
* `test_quality_procurement.SqlFlows.test_quality_sql_postcommit_refresh` (4 subtests)
* `test_resident_decisions.SqlResidentDecisions.test_followup_postcommit_sync_fault_is_truthful_and_not_replayed`
* `test_resident_decisions.SqlResidentDecisions.test_response_reassignment_faults_preserve_history_and_exactly_once_outcome`

## Root cause

E1 widened the shared `SqlStore.save` post-commit handler from `except RuntimeError` to `except (RuntimeError, OSError, ValueError)`. `save` is the common commit path of every SQL write. Callers that previously received the original `OSError`/`ValueError` from a post-commit refresh now receive a `CommittedReloadError` whose `__cause__` is that error. Their established contracts (original error type and chaining, hazard failed-write handling, quality and resident post-commit assertions that the cause is the injected OSError) changed. The importer needs the committed truth only on its own path, `SqlStore._persist_import_refusals`, the only importer caller of `save`.

## Chosen approach

Restore the shared contract (`except RuntimeError` only, original behaviour). Make the wider translation opt-in for the import-refusal persist path through a thread-local marker set only inside `_persist_import_refusals` and cleared in a `finally`. Other callers, including their error chaining, refund, rollback and manual-recovery contracts, are untouched. The E1 core test that called `save()` directly with OSError/ValueError is moved to the import-refusal path and gains a control that a plain `save()` keeps the original error. No new field, API, role or provider; no assertion weakening; no broad catch.

## Not changed

Importer CLI, transfer semantics, permissions, consent, state; JSON store; unrelated formatting.
