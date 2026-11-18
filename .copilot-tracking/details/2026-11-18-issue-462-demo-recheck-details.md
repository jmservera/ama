---
title: Plan details for #462 synthetic showcase demo recheck
ms.date: 2026-11-18
---

## Phase 1: Azure facts

* Commands: `az containerapp show`, `az containerapp revision list`, `az role assignment list` for `id-resident-demo`, Cost Management query for resource group `ama` (ActualCost, 2026-10-01 to 2026-11-18, grouped by service).
* Output: `.copilot-tracking/evidence/2026-11-18-resident-showcase-recheck/azure-app.json, azure-roles.json, azure-resident-resources.json and the cost files`. No secret values; Key Vault secret names only.

## Phase 2: browser script

* Script `.copilot-tracking/evidence/2026-11-18-resident-showcase-recheck/live_recheck.py`, run with the Python Playwright package.
* Credentials from `~/.ama-resident-test-user` (line 1 email, line 2 password); the script never prints them and fails if either appears in any recorded string.
* Retained results: `live-checks.json` (status codes, header names, key names, counts) and desktop screenshots; the filled form is masked.
* Rate-limit check is done last, after the sign-in journeys, so it cannot block them; it consumes the per-source in-memory budget only.

## Phase 3: documentation

* New note under `docs/reference/research/`; index row in `docs/reference/README.md`; append-only entry in `docs/reference/log.md`.

## Success criteria

* Each unticked criterion carries Proven, Partly proven or Unproven with the retained file that supports it.
