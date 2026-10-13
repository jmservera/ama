---
title: Five Assistant Runtime Validation Changes
ms.date: 2026-10-13
---

## Opening Implementation State

Declared scope: full bounded follow-up plan P01 to P03, not parent live rollout.
Owner explicitly requests implementation and autonomous completion after the
published Review. Reuse approved parent contracts/critique and implement its
RV-003/004 plus actual disposable-SQL coverage for RV-002. No new research,
architecture decision or repeated parent Review.

Source boundary: existing MVP runtime/UI/test file/browser check, SQL CI job
and directly related canonical docs. Validation: delayed-claim interleaving,
pending-request/manual browser writes, timeout/stale navigation, full unittest,
actual SQL Server suites and exact-source local container.

First execution: P01-T01 shutdown dispatch admission. Live rollout and finite
paid model allowance remain unapproved; continue all nonbillable work.

## P01: Runtime Fixes

Shutdown and provider-thread admission now share a short lock; SQL/complete/
inference stay outside it. Already stopped requests do not claim; delayed
claims cannot dispatch after stop, retain reservation liability and release
their local/shared active slots. Two deterministic regressions pass.

Case panels return immediately; registry/proposal GETs use a shared 10-second
abort deadline. Detached or different-route panels cannot consume late results.
Manual rendering/writes do not await assistance. Chromium proves pending
requests, a successful manual write, timeout fallback and stale navigation.

Validation: 46 assistant tests and both Node syntax checks passed. Chromium
19 checks passed. Missing browser package was restored only after import
failure, into session-only pip target; no repository dependency changed.
Pending intercepted request cleanup is made explicit in the same test.

## P02: Actual SQL Test Ownership

Immediately relevant validation refinement, not new scope: reuse test_assistants
fixtures via open_store; four conditional classes exercise the same contracts
on actual SQL Server with a dedicated local-only disposable database. Preserve
the existing general parity suite. CI runs both and checks assistant JS syntax.
No pilot SQL reset or real model invocation.

Actual local SQL validation passed 68 tests: 26 general store and 42 assistant
contract/review/durability/API tests, against SQL Server 2022 image digest
cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718.
Fresh generated private credentials established readiness; scoped container,
network and credentials were cleaned. Previous bootstrap failure is historical,
not an active blocker for disposable SQL coverage.

Full regression: 377 discovered, 309 passed, 68 conditional SQL skips.
Chromium rerun: 19 passed, no page errors or pending-route cleanup warnings.
Both JS syntax checks and Git whitespace check passed. Real models, human
acceptance, deployed SQL identity/permission and retained-data restart proof
remain distinct unexecuted gates.

## P03: Build and Publication

Corrected source ready for commit, exact-source local image and canonical
evidence updates. No PR merge or re-run of the completed parent Review.

Runtime source bf383c40369fa67db3d0cbbe7c9473c24ababbe8 published on #68.
Local image assistants-20261013-02 ID
d3e652cec1bdef8846270a75c124d55743bdb757231ffaeae585cc423e6b8786 carries
that exact runtime OCI revision. UID10001, no baked data, read-only root,
no capabilities, writable SQLite state, health and current UI/logo bytes pass.
Source CI 38457772710 passes test/image/mssql, including scan/SBOM and 68 SQL
tests. Added explicit first-assistant-table concurrent creation on retained
domain state; latest actual SQL run passes 69 (43 assistant + 26 general).
Latest full discovery passes: 379 discovered, 310 passed, 69 SQL skips.
Chromium 19 and JS syntax pass; runtime code unchanged by extra test coverage.

Actual serving image/revision still account-switch-20261013-01/--0000009,
read-only verified. Azure tool confirms existing app in ama/uksouth.
Specific retained-data rollout and USD 5 incremental QA approval requested;
owner unavailable, no affirmative permission inferred. No cloud writes,
provider calls, tenant changes or fabricated human verification.

PRD/ADR/MVP/operator/index/log learnings reconciled in place. Canonical validator
reports zero missing targets/fragment/frontmatter failures; six pages render
with expected headings/tables; original, memory and regulatory evidence remain
untouched. Prior failures and Review remain historical; disposable SQL success
is not live Azure/model acceptance. Final publication/reconciliation pending.
