---
title: "Plan: #432 resident adapter ledger join"
ms.date: 2026-11-04
---

Details: [details](../details/2026-11-04-issue-432-resident-ledger-join-details.md)

* [x] 1. Add optional `record_call(outcome, counts, returned_model)` to `AzureTopicProvider`, called for success, timeout, other transport failure and unreadable or oversized replies; failures in the hook never change the resident outcome.
* [x] 2. Add `resident_demo/ledger_meter.py` (`LedgerTopicMeter`): `reserve`, `token` (dispatch recheck after credential) and `close` over the core `Consumption` ledger with capability `resident-topic`, case type `resident-chat`, configuration and prompt versions.
* [x] 3. Behavioural tests in `src/api/tests/test_resident_ledger_meter.py`; update the inventory description.
* [x] 4. Focused tests, ruff, mypy (cache /tmp/mypy-432, tests included).
* [ ] 5. Commit, push, PR with Refs #432.

## Critique (single pass)

* Risk: a held meter could block residents. Applied: any hold or failure raises the existing unavailable error, so the resident keeps the workflow-only path; nothing new is shown to residents.
* Risk: unclosed reservations after pre-network failures. Accepted: the ledger treats them as unknown liability after 40 seconds, matching the adapter rule never to refund automatically.
* Risk: claiming more than proven. Applied: aoai.py remains un-joined, criterion 1 stays unticked.
