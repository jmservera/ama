---
title: Issue 142 research, Key Vault secret lifecycle
ms.date: 2026-11-17
---

## Scope and tier

Issue #142, evidence only, no rotation, no Azure action. Tier FOCUSED (offline tooling and docs; no SQL, deployment or infrastructure change). Base `eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4`. Disposition: executed.

## Issue state

* C1 owner, interval, expiry alert: unmet (owner placeholder to confirm, deployed alert unverified).
* C2 no-downtime Entra rotation tested: unmet (offline ordering model only).
* C3 scheduled, recorded access review: unmet (generator exists, no executed review).
* C4 diagnostic logs: ticked, unchanged.
* Out of scope: #1818, #1641 (core mssqlstore, chat grounding).

## Existing evidence

* `infra/secret-inventory.json`: four secrets with owner, rotation interval and expiry window.
* `infra/scripts/secret_lifecycle.py`: `check`, `review`, `review-status`, `rotation-plan`, `rotation-simulate`.
* `infra/modules/keyvault.bicep`: RBAC, soft delete, purge protection, diagnostics, expiry and denied-access alerts.
* Baseline measurement: `python3 -m unittest tests.test_secret_lifecycle tests.test_keyvault_secret_governance` from `infra/`: 28 tests, OK.

## Measured defect

`secret_lifecycle.py check` only inspects secrets named in the inventory. A vault secret with no inventory entry (no owner, interval or expiry alert) is silently accepted.

Reproduction with a listing of the four inventoried secrets plus `stray-unowned-secret`, `--now 2026-11-17T00:00:00Z`:

```text
(no output)
exit=0
```

This weakens C1 ("each secret has an owner"): the live check cannot detect an uninventoried secret. Names only are read; no values.

## Planning readiness

Ready. Smallest fix: add an `uninventoried` finding to `check_secrets` plus a regression test. The live criteria C1 to C3 stay unmet.
