---
title: Issue 521 rollback-fixture diagnostic D1 plan
ms.date: 2026-11-11
task_id: 521-rollback-d1-1111
---

## Objective

Move the deliberately invalid row in `test_failed_migration_rolls_back_original_check_and_leaves_no_transaction` one second beyond the shared maximum (`rs.AUTHORITY_END + timedelta(seconds=1)`), prove RED then GREEN on an owned disposable SQL Server, and record dated evidence in the existing `infra/README.md` section. Test-fixture-only. Research: [research](../research/2026-11-11-rollback-fixture-521-d1-1111-research.md). Details: [details](../details/2026-11-11-rollback-fixture-521-d1-1111-details.md).

## Phases

* [x] Phase 1: critique (one independent, final candidate only), then apply compatible findings.
* [x] Phase 2: RED on real SQL (unchanged fixture, exact test), retain output.
* [x] Phase 3: fixture edit, GREEN on the changed test, then the whole `test_resident_showcase_sql` module on real SQL, plus `test_resident_showcase` (core), `infra/tests/test_resident_demo_deploy.py` and `test_resident_demo_secrets.py` source and fake-CLI selectors.
* [x] Phase 4: ruff check, ruff format --check (report inherited findings separately), mypy on changed Python.
* [x] Phase 5: README evidence, changes record, review, handoff, commit.

## Boundaries and stop rules

* Change only the test file fixture and the one README subsection. No product Python, SQL template, JSON, Bicep, helpers, caps, guards, permissions, live resources. No assertion weakening, fake success or mocks in place of the real SQL test.
* Focused validation only, no complete gate. Shared heavy lock by non-queued `flock -n`, one owned labelled container on a random loopback port from the cached image, cleanup of own container only. If a prerequisite is unavailable or the lock is busy: record a blocked validation, stop before publication, no blind retry, no pull or cloud fallback.
* If RED does not occur with the unchanged fixture, stop and record that finding (no correction claimed).
* No push, PR, criteria ticks or board change. D1 consumed; no automatic D2.
