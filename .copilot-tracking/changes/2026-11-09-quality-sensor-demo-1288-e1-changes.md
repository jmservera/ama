---
title: Quality sensor demo 1288 E1 changes
ms.date: 2026-11-09
---

Recorded 2026-11-09. Parent: frozen C8 `1251c1dcbe97a50039cf134a9d54ed90164ec846`. Refs #1288, #107. No closing claim. Local candidate only; nothing pushed. E1 is the first of up to five additional owner-authorised cycles (E1 used, 4 remain). Owner grant: issue #1288 comment 6735179415.

## Source

* `src/core/src/zava_forward/core/sensor_consumer.py` (F2): the control guard trigger is gate-aware on SQLite and SQL Server. Any INSERT, UPDATE or DELETE of a control for a home with a live `assistant_dispatch_gate` row (database clock), or with an invalid JSON body while any gate is live, is rejected (`RAISE(ABORT)` or `ROLLBACK` plus `THROW 50002`). Older stored triggers are replaced in place; trigger names are unchanged. `_replace_controls` now writes only the controls that differ.
* `src/core/src/zava_forward/core/ai.py`, `ai_consumption.py` (F1): `Deadline` send-by object; `bounded_send` sends in 16 KiB chunks and checks the gate and caps the socket timeout before every send, restoring the timeout afterwards.
* `src/core/src/zava_forward/core/assistants.py`:
  * F1: `Assistants(transport=)`, `_carrier`, `_provider_honours_gate`, `_provider_sends_nothing`; a provider that neither honours the gate nor declares `sends_no_bytes` is held to the manual route before dispatch when readings are captured.
  * F3: a manual quality request for a different capture no longer rewrites the serviced proactive slot (`_serviced_proactive_slot`); `claim`, `_paused` and `_replaceable` act only on the slot owner's task.
  * F4: `_adopt` is paged (5 rows by up to 20 pages, deterministic `id` tiebreak) and writes an explicit `incomplete-history` marker on cap exhaustion, retried later and reported by `scan()["incomplete_history"]`. New schedule columns `seen` and `paused_at` are added by `_upgrade` on both backends.
  * F5: the quiet interval is measured from the last observed change (`seen`), with `COALESCE_QUIET=300` and `COALESCE_MAX=1800`; `forecast()` does not mutate.
  * F6: `review_flag` compares cited readings only against an authoritative `ok` or `no-readings` capture; otherwise the comparison is unknown and no reading is called missing.
* `src/api/src/zava_forward/api/server.py` (F1, production defect): the provider is wired as a `fenced()` function over `store.ai`, which raises `DispatchWithdrawn("unfenced-provider")` if a gate is active and the object does not honour it; `transport=lambda: store.ai` reaches the real client.
* `src/core/README.md`, `DispatchGate` docstring: E1 behaviour and residual limits.
* `src/api/pyproject.toml`: the two new modules join the existing mypy `ignore_errors` override list used by sibling test and check modules.

## Tests and checks

* `src/api/tests/test_quality_sensors_e1.py` (new): F1 to F6 regressions plus `Mssql*` variants gated on `ZF_TEST_MSSQL=1`.
* `src/api/tests/test_quality_sensors_c7.py`: the coalescing recovery test scans at +400 and +800 (E1/F5).
* `src/api/tests/test_assistants.py`: the mock `Provider` declares `sends_no_bytes`.
* `src/api/checks/quality_sensors_browser_check.py` (new, AC7): Chromium check on a constructed fixture with a mock provider.

## Divergences from the plan

* No `assistants.js` change: the UI already treats `changed_since_capture == null` as unknown.
* The non-bytes fail-closed branch is defensive and untested (urllib never passes non-bytes to `send`).
* Two Fence tests passed vacuously on unchanged source and were tightened before the fix.

## Not changed

C1 to C7 product code beyond the paths above; the C8 fixture fix; no real model, credential, cloud or private dataset; no sibling #1292 or #184 import.
