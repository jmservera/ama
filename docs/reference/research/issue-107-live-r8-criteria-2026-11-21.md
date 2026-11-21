---
title: Issue 107 eighth live pass, unticked criteria at head 0c497160e (2026-11-21)
description: Actual-SQL re-run at the current head and proven/unproven table for the two unticked issue 107 criteria in the synthetic demo
ms.date: 2026-11-21
---

Refs #107. Synthetic demo, desktop only. No Azure resource was created or changed. The only resource created was a local throwaway SQL Server 2022 container (`zf107-sql`, bound to 127.0.0.1, random password never printed), deleted afterwards and verified absent. No source change; no defect found.

## Evidence

Commands ran from `src/api` with `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests` at head `0c497160e`.

| Command | Result |
| --- | --- |
| `python3 -m unittest tests.test_assistant_restart_non_replenishment tests.test_assistant_release -q` (SQLite) | 95 tests, OK, 22 skipped (actual-SQL classes) |
| Same with `ZF_TEST_MSSQL=1` against the local SQL Server 2022 (password auth, trusted certificate) | 95 tests, OK, 0 skipped |
| `python3 -m unittest tests.test_assistants -q` with `ZF_TEST_MSSQL=1` (independent-connection races) | 139 tests, OK |
| `az containerapp show -n ca-cutover-test-demo-api -g ama` | revision `ca-cutover-test-demo-api--0000038`, image `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:bc5cb9ae...a937da` (digest only; not linked to a source commit or to an approved exercise release) |

## Per-criterion table

| Criterion | Result | Basis |
| --- | --- | --- |
| Independent SQL connection/worker and race tests for material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish allowances | Proven for the demo on a disposable actual SQL Server 2022 | Table above. Old images are modelled as fresh workers over the same database with a larger allowance, not a pulled older image. Azure SQL is not covered and is not needed for the demo. |
| A matching approved exercise record permits bounded proposals only; delivered-build real AI, SQL and Azure evidence (CON-009/AC-057) | Unproven | The deployed image is identified only by digest, with no version-linked approved release. An approved release needs a named approver and residual-risk holder (OQ-017), not appointed; real AI use is not authorised for this issue. Human step. |

Nothing was ticked on the issue. Independent exact-head review and hosted CI remain outstanding.
