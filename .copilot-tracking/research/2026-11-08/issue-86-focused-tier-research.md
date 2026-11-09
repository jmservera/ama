---
title: Issue 86 focused-tier validation research
description: Research for the owner's local validation boundary change and the interrupted FULL g86-main0f-r1
ms.date: 2026-11-08
---

Scope: issue #86 only, `Refs #86`, local only. No source edit, no publication, no tick. Observations, not acceptance.

## Owner boundary change

The owner asked to run local FULL "just when it makes sense": Main-bound PRs that modify executable code or Bicep, including an integrated parent. The coordinator reads this as: stacked children and docs-only work use relevant focused checks; the #86 to #81 child PR is FOCUSED; the later #81 to Main integration keeps FULL. Complete RPI, independent exact-head review, hosted checks, source currency and human approvals are not waived. This is the coordinator's interpretation, not a repository policy change; `src/README.md` still states the older rule and is not edited here.

## Interrupted FULL g86-main0f-r1 (immutable)

* Head `40ec31e2cc2f06013ac6bfcafea8fe7e0310a326`, tree `6ba42de3393a67fd51b72c18c943680e9cca8f53`, base `0f05e9aae70768def8d1d9c300215f9ee2f11638`, jobs 1, no shards. Receipt `/home/azureuser/.local/share/ama/gates/g86-main0f-r1/receipt.json`, sha256 `dfa60d46311ee5bf1ab351aca2f4a20cb5e3160b4742fc302327abdbcfe6dea9` (matches `receipt.sha256`); console `../g86-main0f-r1.console` sha256 `227e290ce462ebb5408d44ab4ec56cb150aab4ffc0808c9d3cd72b05fdba156c`. No `.exit` file exists.
* Status failed, failure "Interrupted by signal 15" at 08:05, in `mssql` (`0176-mssql.log`, `failed (-15)`). The console ends mid-test in `MssqlProcurementApi.test_contractors_own_orders_only_and_all_writes_denied`. The native CLI log reported a 600 second background-wait timeout; the launcher now sets a 7200 second bound.
* Executed groups: preflight, five projects, namespace, static, infra, migration, browser (11). Not executed: image-api, image-agents, image-orchestrator, image-importer, logo-0600. `mssql` interrupted after 164 `ok` lines and zero failures in its log (one skip line to be classified).
* Same-head results: project-core 2492 tests OK, 243 skipped; project-api 1999 tests OK, 354 skipped. Tracebacks in logs are synthetic failure-injection output inside passing tests.
* This is NOT a passing FULL and NOT a product assertion failure. It stays unreclassified.

## Actual change surfaces to cover

* Published parent `c5edb320` to candidate: `git diff --name-only c5edb320 HEAD -- src tools infra .github` lists 46 paths (core appointments, complaints_route, projection, quality, ranking_publication(+runner), resident_decisions, store; API server and web, chat, checks, many tests; tools rpi-checks and backlog-sync; rubric JSON).
* Local parent `e888a499` to candidate: rubric, `assistant_process_worker.py`, `test_assistant_release.py`, core README, `complaints_route.py`, `resident_decisions.py`, `store.py`, `test_resident_decisions.py`.
* Main `0f05` to candidate: inherited #1226, #1228, #1229 gates, procurement, quality, store, appointments and tests plus the child.

## Maintained coverage and gap

* `SQL_SELECTORS` (mssql group): `test_mssqlstore`, `test_lawstore.MssqlStoreTests`, five `test_assistants.Mssql*`, `test_assistant_release.MssqlUnleasedRevocation`, `test_resident_aoai_sql.AccountingSqlTests`, run from `src/api` against an owned container with `ZF_TEST_MSSQL=1`.
* Core resident-decision SQL class `MssqlResidentControls` is gated by `ZF_RESIDENT_MSSQL=1` and is not in `SQL_SELECTORS`; it covers the complaints and decisions store this slice changed.
* The maintained runner has no way to run the `mssql` group alone on this head: `--changed` selects projects, browser and images from the base diff, and `--resume` also reruns the four images and logo. Gap named; the smallest route is a manual run of the maintained selectors, mirroring the runner's owned-container steps (label, 3g, 2 cpus, loopback port, `rpi_disposable`), under the canonical lock. It is a focused manual record, not a runner receipt.
* The shared lock is `fcntl.flock` on `/tmp/ama-rpi-heavy.lock` (non-blocking in the runner).

## Resources observed now

Physical lock holder gone, `docker ps` empty, root 25 GiB free, `/mnt` 4.2 GiB, RAM available about 8 GiB, 4 CPUs shared. Rechecked before use.

## Open and unchanged

#1238 policy, original Medium findings, adverse browser outcome, per-store registry and point-in-time guard limits, no real receiver, no cross-process or multiuser proof, no model, legal, resident or AT approval.
