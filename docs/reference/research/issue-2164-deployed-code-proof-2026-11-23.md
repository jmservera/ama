---
title: "Issue 2164 deployed code proof (2026-11-23)"
description: Read-only check that the deployed demo API package carries the assistants roster-scope fix, with a per-criterion table.
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Read-only `az containerapp exec` into `ca-cutover-test-demo-api` (resource group `ama`) running `grep`, plus local unit tests. No credentials were read or printed, no roster row or Azure resource was created or changed, and no source changed. Refs #2164.

## Evidence

* Active revision `ca-cutover-test-demo-api--0000055`, created 2026-11-23T03:25:45Z, 100% traffic.
* `grep -c re-read /usr/local/lib/python3.12/site-packages/zava_forward/core/assistants.py` in the replica returned 1. That string is the comment added by 6a03928ccb (committed 2026-11-22T21:26:50Z) in the bound-row branch of `Assistants.authorize`, so the deployed package contains the fix. This closes the earlier "digest untraceable" gap with direct content evidence.
* `grep -c oid .../sensor_review_draft.py` returned 0, while HEAD has the oid check at line 168. The sensor draft gate fix (5dfa7312d5, committed 2026-11-23T10:20:28Z) post-dates the revision, so the deployed image lacks it. Sensor review drafts are default-off in the demo, so there is no demo exposure; the next image build will carry it.
* Local: `src/core` `tests.test_assistants_identity` and `tests.test_sensor_review_draft`: 73 tests OK (23 skipped, SQL Server variants). `src/api` `ReviewTests.test_bound_entra_staff_inherit_roster_scope_and_revocation` and `test_unbound_and_view_only_entra_principals`: 2 tests OK.
* A live behavioural proof needs a roster-bound Entra principal with a restricted `case_ids` list, which means editing live roster data. The owner decisions of 2026-11-18 exclude production changes, so it was not attempted.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Decide whether bound Entra staff inherit roster scope | Proven | Fix in 6a03928ccb on HEAD and present in the deployed assistants module |
| Test `view_only` with an eligible role | Proven | api and core tests pass |
| Test scope bypass | Proven | api and core tests pass |
| Deployed API carries the assistants fix | Proven | Marker grep in the live replica |
| Live behaviour with a restricted roster row | Unproven | Needs a live roster edit, excluded for the demo |
| Deployed API carries the sensor draft gate fix | Unproven (not deployed) | Revision predates 5dfa7312d5; feature default-off |
