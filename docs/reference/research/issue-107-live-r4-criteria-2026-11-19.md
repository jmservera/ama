---
title: Five assistants first unmet criterion, actual SQL coverage (Refs #107)
description: Per-criterion proven or unproven record for issue 107 after adding actual SQL Server coverage of the material-mismatch and allowance race tests
ms.date: 2026-11-19
---

Refs #107. Scope is the synthetic demo, desktop only, FOCUSED tier (test-only change), under the owner decisions of 2026-11-18. No Azure resource was created or changed; the only resource created was a local throwaway SQL Server 2022 container (`zf107-sql`, bound to 127.0.0.1), deleted afterwards.

## Finding

The first unticked criterion is independent SQL connection/worker and race tests for material mismatches, revocation and restart. Before this change `src/api/tests/test_assistant_restart_non_replenishment.py` ran only revocation on actual SQL Server (`MssqlRevocationAndSuspension`); the allowance and material-mismatch classes ran on SQLite alone, and no test combined a material mismatch with an old image.

Added in that file:

* `MssqlAllowance` and `MssqlMaterialMismatch`, skipped unless `ZF_TEST_MSSQL=1`, run the existing allowance and ten-variation mismatch tests on actual SQL.
* `test_old_image_after_a_material_mismatch_cannot_reactivate_or_refill`: after each of ten material mismatches revokes the release, an old-image worker with a larger allowance cannot reactivate it, cannot invoke or execute, and leaves the allowance row, provider call count and controlled-domain records unchanged.

## Validation

| Check | Result |
| --- | --- |
| `python3 -m unittest test_assistant_restart_non_replenishment -q` (SQLite, from `src/api`) | 30 tests OK, 15 skipped (Mssql classes) |
| Same with `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, port 14337, container `mcr.microsoft.com/mssql/server:2022-latest` | 30 tests OK, 0 skipped |
| `ruff format --isolated --line-length 100 --check` and `ruff check` on the file | pass |
| `python3 -m mypy` in `src/api` | 7 errors, all `opentelemetry.sdk` stubs missing in this environment (`src/core/tests/telemetry_support.py`), none in the changed file; unchanged by this change |

## Per-criterion table

| Criterion | Proven for the demo? | Basis |
| --- | --- | --- |
| Independent SQL worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish allowances | Proven on a disposable actual SQL Server 2022; not on Azure SQL | Table above. Old images are modelled as fresh workers over the same database with a larger configured allowance, not a pulled older container image (the ACR is private, see the [third pass](./issue-107-live-r3-assistants-evidence-2026-11-18.md)). |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven | No approved release exists and creating one needs a named approver and residual-risk holder (OQ-017); real AI use is not authorised here. |

Nothing was ticked on the issue. Independent exact-head review and hosted CI remain outstanding.
