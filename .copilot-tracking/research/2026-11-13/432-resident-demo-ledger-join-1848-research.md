---
title: Issue 432 resident demo and read-document ledger join research
description: Evidence for closure review findings F1 and F2
ms.date: 2026-11-13
---

## Scope

Closure review findings F1 (resident demo advisor ledger join) and F2 (`read-document` text call join assertion), from `review-432-c1-1836` review. Tier: Focused. Research disposition: executed.

## Evidence

* `src/api/src/zava_forward/api/resident_demo/ledger_meter.py` provides `LedgerTopicMeter` and `advisor_meters` (capabilities `resident-guidance`, `resident-question`, `resident-topic`). `aoai.AzureAdvisor` and `assistant.AzureTopicProvider` already accept the meter, refuse unmetered kinds when a ledger is configured, and close with counts, returned model and outcome only.
* `tests/test_resident_ledger_meter.py` already proves admission, held and failure paths for the adapters, but no test asserts the reserved-to-completed join (same id, root, attempt, capability, configuration, prompt, counts) for the question kind carrying resident text, and the content-free check is a single substring.
* No host calls `advisor_meters`: `resident_demo/__main__.py` calls `configured_advisor(os.environ, connector)` with no ledger. The ledger (`Consumption`) is built on the assistants service store (`core/assistants.py`) or the demo port; the resident showcase host reads a synthetic SQL view and holds no ledger port, price or spending authority. The module docstring states the adapter supplies no price or authority and does not enable itself.
* `tests/test_ai_call_site_inventory.py` classifies `aoai.py` as `own-accounting` and `assistant.py` as `counts-only-sink`. The status check keys on `consumption.reserve` calls in source, so only `core/ai.py` is `ledger`.
* `tests/test_ai_consumption_api.py::test_document_calls_preserve_shared_call_and_depth_limits` covers `read-document` text limits and context, with no joined-record assertion for completed counts and no content canary; image calls stop before HTTP.

## Determination

* Adapter join is implemented and can record without resident data (ledger records hold references, counts, outcome, never text). Host wiring cannot be done cleanly without an owner-supplied ledger store, price and authority, so the inventory classification is not upgraded; wiring remains an owner decision on #432. The inventory note is tightened and a drift guard added so a future host wiring forces reclassification.
* Add join and content-free canary tests for the resident advisor (question and guidance) and topic provider, and for `read-document` text calls.

## Planning Readiness

Ready.
