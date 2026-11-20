---
title: Issue 2061 demo single-environment Bicep profile, evidence (2026-11-20)
description: Per-criterion proven and unproven status for the demoSingleEnvironment Bicep profile, with what-if, role inventory and the limits of the current login
ms.date: 2026-11-20
---

Refs #2061. Demo only (synthetic, desktop). Owner decision option A (2026-11-20).
No Azure resource was created, changed or deleted and nothing was deployed; only
read-only Azure CLI calls and `what-if` ran. No credential was read or printed.
Decision record: [ADR 0008](../../adrs/0008-single-external-demo-environment.md).
Runbook: [infra runbook](../../../infra/demo-single-environment-runbook.md).
Earlier inventory: [2026-11-19 note](./issue-2061-live-single-environment-2026-11-19.md).

## What changed

* `infra/main.bicep`: parameter `demoSingleEnvironment` (default false) and guard
  `singleEnvironmentRequiresDirectDemo`.
* `infra/modules/identity.bicep`: conditional `id-<prefix>-internal`; the
  `internal` key falls back to the API identity when off.
* `infra/modules/containerapps.bicep`: ledger-verify and rank-publish jobs use
  the internal identity; output `publicIngressApps` lists the API only.
* `infra/role-assignments.json` and `infra/scripts/create-sql-users.py`: internal
  roles and SQL grants.

## Per-criterion status

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| 1 | ADR | Proven (Proposed) | ADR 0008 updated; owner approval of delete list and Entra changes is not recorded |
| 2 | Bicep and what-if | Proven | `az bicep build` passes; what-if on group `ama` returned 0 Delete (103 Deploy, 33 Ignore, 28 Create, 16 Unsupported). Parameters were reconstructed, so the Create of an Event Hubs namespace is drift noise, not a plan |
| 3 | Delete list | Partly proven | Environment, DNS zone, link, subnet and NSG named; the load balancer and public IP ids sit in `ME_cae-cutover-test_ama_uksouth`, which this login cannot read |
| 4 | Entra table and sign-in | Unproven | `az ad app list` is denied (insufficient privileges), so URIs cannot be compared; no deploy, so no sign-in on the new layout. Option A keeps registration `0dbb6baf...` unchanged |
| 5 | Identities, role inventory, negative test | Partly proven | Role inventory before is in the evidence folder and the runbook; after-state is asserted by `test_identity_rbac`. The negative access test needs a deploy |
| 6 | End-to-end demo | Unproven | Needs a deploy, which was not authorised for this run. Baseline: demo API `/api/me` returns 401 unauthenticated |
| 7 | Production build and gate receipt | Partly proven | Production profile builds and its infra tests pass; the full gate was not run (`rpi-checks.py --all` forbidden for this run), so no receipt |
| 8 | Rollback | Proven as written | Runbook rollback section; the guarded default-off parameter makes it a redeploy. Not exercised |

## Evidence

* `.copilot-tracking/evidence/2026-11-20/issue-2061-live/roles-before.txt`:
  role assignments of six identities (subscription id redacted).
* `.copilot-tracking/evidence/2026-11-20/issue-2061-live/whatif-summary.txt`:
  what-if change list.
* Infra suite: `python3 -m unittest discover -s infra/tests -q`, result recorded in
  the changes record.
