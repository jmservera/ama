---
title: Issue 432 resident demo ledger join details
description: Phase details for F1 and F2
ms.date: 2026-11-13
---

## P1

Helper `call_join(test, reserved, completed, capability)`: same `id`, `root`, `attempt`, `configuration`, `prompt`; `completed["tokens"]` equals the provider usage; `held` false on success. Canary resident question text (`SYN-RESIDENT-QUESTION-CANARY`, name, phone) must not appear in the JSON of all ledger records (reserved, completed, alert) or in logged output. Cover question kind success, transport failure (join holds, outcome timeout) and topic provider.

## P2

In `ConsumptionApi`, send `look_at("PRIVATE-DOCUMENT-NAME.txt", b"PRIVATE-DOCUMENT-BODY", "text/plain")` under a call context; assert the reserved record carries context fields, the completed record has the response usage and `returned`, the receipt `meter_id` matches, and no canary appears in records.

## P3

Inventory notes name the missing host wiring and owner decision. New test: parse all `src/*/src` files; `advisor_meters` or `LedgerTopicMeter` referenced only by `ledger_meter.py` (so wiring forces reclassification here).

## Critique amendments

* Join on reservation id; context on reserved, usage and outcome on completed.
* `configured_advisor(..., meters=None)` seam plus test; close reservations on credential/expiry exits in `aoai.py` and `assistant.py`.
* Canary reaches transport first; check ledger records and logs.
* Replace name-scan guard with seam behaviour test.

## Non-goals

No host wiring, no price or authority supply, no GitHub edits, no push.
