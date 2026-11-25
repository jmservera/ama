---
title: "Issue 2164 deployed code proof, revision 69 (2026-11-25)"
description: Read-only check that the demo API revision 0000069 carries the assistants roster-scope fix, with a per-criterion table.
ms.date: 2026-11-25
---

Scope: synthetic demo, desktop only. Read-only `az containerapp exec` into `ca-cutover-test-demo-api` (resource group `ama`) running `grep -c`, plus local unit tests. No credential was read or printed, and no roster row, Azure resource or source file was created or changed. Refs #2164.

## Evidence

* Active revision `ca-cutover-test-demo-api--0000069`, created 2026-11-25T14:18:52Z, 100% traffic.
* `grep -c -e re-read -e oid` on the replica's `zava_forward/core/assistants.py` returned 4 and on `sensor_review_draft.py` returned 1. These are the markers of the bound-row re-read in `Assistants.authorize` and the oid gate in the sensor draft; they are presence evidence only.
* HEAD `1154ce6058`: core `tests.test_assistants_identity` and `tests.test_sensor_review_draft` ran 73 tests, OK (23 skipped, SQL Server variants). api `tests.test_assistants` and `tests.test_entra_authoritative` ran 192 tests, OK (65 skipped).
* Code reading of `Assistants.authorize` found no defect: view-only is refused, a bound row is re-read on matching oid and tenant, and revocation, malformed scope, `case_ids` and `areas` are enforced.
* A live behavioural proof needs a roster-bound Entra principal with a restricted `case_ids` list, which means editing live roster data and an interactive sign-in. The owner decisions of 2026-11-18 exclude production changes, so it was not attempted.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Decide whether bound Entra staff inherit roster scope | Proven | Fix on HEAD and markers in the deployed module |
| Test `view_only` with an eligible role | Proven | api and core tests pass |
| Test scope bypass | Proven | api and core tests pass |
| Deployed API carries the assistants and sensor draft fixes | Proven (presence) | Marker greps on revision 69 |
| Live behaviour with a restricted roster row | Unproven | Needs a live roster edit and a bound Entra sign-in; excluded for the demo |
