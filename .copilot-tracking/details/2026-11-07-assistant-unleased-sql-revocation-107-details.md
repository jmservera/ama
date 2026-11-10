---
title: Details for unleased SQL revocation coverage (#107)
description: Test steps, selectors and the future nonqueued SQL admission plan
ms.date: 2026-11-07
---

Plan: [plan](../plans/2026-11-07-assistant-unleased-sql-revocation-107-plan.md).

## Test `test_independent_worker_revocation_denial_is_durable_for_an_unleased_task`

1. Invoke a CAP proposal and a control proposal for another assistant; assert the CAP row is pending, unowned, unleased, attempts 0 and passes the claim precondition.
2. Positive control: an independent worker executes the control proposal; it returns True with exactly one provider call.
3. Revoke the CAP release through a separate connection and service.
4. A further independent worker executes the CAP proposal: returns False, provider calls stay at one, the row is disabled with attempts 0 and no owner (so not a lease rejection), the reason starts with "Release admission denied", and exactly one `disabled` event carries it; allowance use is unchanged.
5. A reopened worker repeats: denial and release status `revoked` persist, no new event, no provider call.

## Classes

`UnleasedRevocation` (mixin), `SqliteUnleasedRevocation(UnleasedRevocation, Base)` (proxy), `MssqlUnleasedRevocation(MssqlFixture, UnleasedRevocation, Base)` gated on `ZF_TEST_MSSQL=1`.

## Proposed SQL selector for the one future nonqueued shared-lock admission

From `src/api` with own-source pip packages, `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=localhost` and the local disposable service: `python -m unittest test_assistant_release.MssqlUnleasedRevocation -v`. Then the complete FULL runner on the frozen head against freshly fetched main (`--all --base <current main> --out <new external dir>`, stdin /dev/null, fresh images, actual disposable SQL), read from the current tools and README at run time. Main may move (1252 pending): a normal merge of the admitted main is needed before FULL; no gratuitous rebase.
