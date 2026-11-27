# Changes: issue 2245 live (2026-11-27)

Tier: FULL (src/core change; basis: source behaviour change on the chat answer path). Refs #2245 (no closing keyword: the lock-hold cause and the live effect of the fix are unproven). Local commit only; the complete gate (`rpi-checks.py --all`) is left to the coordinator.

## Files

* src/core/src/zava_forward/core/chat_panel.py: bounded retry (`SAVE_LOCK_RETRIES = 2`) of the assistant-message save on a SQL write-lock timeout.
* src/core/tests/test_chat_panel.py: `test_answer_save_retries_a_write_lock_timeout_after_the_model_answered` (fails without the change).
* docs/reference/research/issue-2245-live-20261127T024556Z.md and folder (probe scripts, JSON, screenshots); docs/reference/README.md and log.md entries.

## Validation

* `PYTHONPATH=src:tests python3 -m unittest test_chat_panel` in src/core: 64 tests OK; `-p "test_chat*.py"` discover: 208 tests OK.
* New test fails against the previous chat_panel.py.
* `ruff check`, `ruff format --isolated --line-length 100 --check` pass. `python3 -m mypy` reports 3 errors that also exist without the change (missing opentelemetry stubs, one unused ignore in synthetic/device_provision.py).
* Not run: full core/api suites, hosted CI (nothing pushed), complete local gate.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Thread creation does not 500 | Proven for this window (no 500; deliberate 503 under lock contention); 2026-11-22 cause unproven (telemetry denied) | probe-chat-result.json |
| Model-answerable question shows "Model calls: 1" | Proven live on revision 0000130 | screens/widget-model-call.png, probe-widget-result.json, AI_USAGE log line |
| No paid answer lost to a transient write-lock timeout | Defect reproduced live (ask 500 after AI_USAGE); source fix and test done; not deployed, live effect unproven | research note |
| Banner states plainly when answers are rule-based | Proven live; held wording by earlier notes and tests | probe JSON |
| Which skills and routes call the model, why none did | Proven from source, logs, probes | research note |
| Why the write lock is held over 15 s | Unproven: no SQL lock inspection or Log Analytics | n/a |
| Azure billing, DPO/Legal, assistive-technology testing | Out of scope by owner decision 2026-11-18 | n/a |
