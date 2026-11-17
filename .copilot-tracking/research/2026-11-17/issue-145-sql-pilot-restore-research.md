---
title: Issue 145 research, Azure SQL pilot tier and restore proof
ms.date: 2026-11-17
---

Task: issue-145. Mode: automatic, FOCUSED tier, documentation only, no live Azure actions.
Research disposition: executed. Planning Readiness: Ready.

## Measured baseline

* Base `origin/main` eb51af5c9. Delivered by PR #673 (`f2dbfcdd4`): `infra/modules/sql.bicep` tier,
  auto-pause, vCores, backup redundancy and retention parameters; `infra/main.pilot.example.bicepparam`;
  `infra/sql-recovery-runbook.md`; `infra/tests/test_sql_tier.py`.
* Reproduction: `python3 -m unittest infra.tests.test_sql_tier` ran 6 tests, OK (4.7 s). Bicep and `az` are installed; nothing was deployed.
* Issue ticks: C1 (parameters) and C3 (objectives undecided with owners) are ticked. C2 (actual PITR plus ledger result) and C4 (retention matches #121) are open.
* #121 is still OPEN, so C4 cannot be proven. The RAI restore criteria all need authorised disposable Azure infrastructure, a DPO and independent witnesses, none of which exist in this task.

## Findings

* No defect found in the delivered parameters or runbook; nothing to fix with a regression test.
* Open gaps are evidence gaps, not code gaps: no restore performed, RTO and RPO undecided, retention decision absent.
* Runbook omits one pilot caveat: when `zoneRedundant` is false the derived backup redundancy is `Local`, so the PITR copy has no zone or region resilience. This is a decision input for the owner, not an approved value.

## Scope and tier

The change is a documentation note in an infrastructure runbook. No Bicep, SQL, security control or deployment semantics change, so FOCUSED applies. Any later Bicep or live restore change moves to the FULL tier.
