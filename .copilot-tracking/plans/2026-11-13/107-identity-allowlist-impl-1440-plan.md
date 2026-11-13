# Plan: #107 identity-field sanitisation (1440)

* [ ] P1 RED tests in `src/core/tests/test_ai_consumption_safety.py`: `shape_result` and `bounded_model`/`Consumption.complete_in` with `sk-SENTINEL0123456789`, newline, `Bearer x`, spaces, subclass, non-str, lengths 120/121/512/513; accepted literals byte-preserved.
* [ ] P2 Add `safe_identity` and route `bounded_model` through it in `ai_consumption.py`.
* [ ] P3 `shape_result`: sanitise provider/deployment (truncate 120 first) and model; `_settle_meter` passes the sanitised model.
* [ ] P4 Run core consumption/assistant suites, `src/api/tests/test_assistants.py`, agents tests, ruff check/format, mypy.

Details: [details](../../details/2026-11-13/107-identity-allowlist-impl-1440-details.md)
