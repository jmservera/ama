---
title: Issue 432 per-call join across all worker modes research
ms.date: 2026-11-13
---

Disposition: executed. Planning Readiness: Ready. Tier: Focused. Refs #432 (not Closes).

## Inputs

* Review `/home/azureuser/source/ama-demo-wt/review-432-join-1800/.copilot-tracking/reviews/2026-11-13/432-join-independent-review-1800-review.md` (REQUEST_CHANGES on `b7ed2ec0f`).
* `src/api/tests/test_ai_consumption_api.py`: `call_join` (:250) asserts configuration, prompt, root, attempt as 64-hex shape; used only for the returned assistant thread (:299) and the chat adapter (:1040). The worker test (:1057) has four modes without `call_join`.
* `src/agents/src/zava_forward/agents/dispatch.py:213`: `retry=max(0, task["fence"] - 1)`; root = `reference(task id)`, attempt = `reference(task id:fence)`, prompt = `reference(canonical([system, purpose, version]))`, configuration from the provider.
* `src/core/src/zava_forward/core/ai_consumption.py`: `output(root, ...)` rows join by `root`; report `retries` counts reserved rows with `retry > 0`.
* `src/api/tests/test_ai_call_site_inventory.py`: resident-demo `aoai.py` and `assistant.py` are `own-accounting` / `counts-only-sink`, ledger join only via `ledger_meter.py` when a host supplies meters, and none does.

## Findings

* Failed (`provider-failure`) and `stale-fence` worker calls publish no output by design (`test_permitted_failure_without_root_settles_the_meter_and_publishes_no_output`), and revoked publishes an ineligible output. So `call_join` (exactly one output) cannot apply to the first two.
* Definition proposed: a call joins to its reserved row (`root`, `attempt`, configuration, prompt, model, case type, retry), its `completed` settlement by the same meter id, and, when an output exists, one output row by `root`. A failed or fenced call joins to attempt + root settlement and has zero eligible output rows under its root.
* Real retry: fail attempt one (provider failure), expire the backoff, reclaim (fence 2, attempts 2), succeed. Expect two reserved rows under one root with `retry` 0 and 1, distinct attempts, and `report["retries"] >= 1`.
* Legacy `ai.py` draft path already asserts reserved/completed/output but not exact fields; resident-demo has no ledger wiring in any host (inventory test), documented out of Criterion 6 scope with that evidence.

## Plan Readiness

Test-only change in `src/api/tests/test_ai_consumption_api.py`; no `src/` change expected.
