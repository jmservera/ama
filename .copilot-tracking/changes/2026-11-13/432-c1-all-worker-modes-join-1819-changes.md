---
title: Issue 432 per-call join across all worker modes changes
ms.date: 2026-11-13
---

Test-only change in `src/api/tests/test_ai_consumption_api.py`; Refs #432.

* `call_join` takes exact `configuration`, `prompt`, `root`, `attempt` (plus exact model, case type, retry) and `output=None` for calls with no output (asserts none under the root).
* Definition: a call joins through its reserved row and its settlement by meter id; a returned or revoked call also joins to exactly one output under its root; a failed or fenced call has attempt + root on its reservation, a settlement, and no output.
* Worker test applies it to returned, revoked, stale-fence and provider-failure with independent expected values and worker canaries (asserted present in the prompt).
* New `test_worker_retry_joins_every_attempt_to_one_root_and_its_output`: fence/attempts 1 then 2 after lease expiry, retry 0 and 1, report calls +2, retries +1, unjoined outputs unchanged.
* Chat path: root captured independently from the call context; assistant thread and legacy draft use exact values; legacy adds system-prompt canary.
* Resident-demo `ledger_meter.py`: out of Criterion 6 scope; `test_ai_call_site_inventory.py` classifies it own-accounting/counts-only and no host wires meters.

Validation in `/tmp/venv-432m-1819`: core 44 and api 38 `test_ai_consumption*` tests OK; ruff check/format and mypy clean (core 299 files, api 237 files).
