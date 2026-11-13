# Research: #107 AI telemetry raw-content exclusion (107-ai-telemetry-1045)

Research disposition: executed (targeted source reading; prior readiness `3c42b381e` and `bdecadacf` only grep-read the tests). Planning Readiness: Ready.

## Findings (source-read, this worktree at 3b0514317)

* `ai_consumption.py`: `Consumption._read` rejects any record whose key set differs from `EVENT_FIELDS[kind]` (`meter-evidence-invalid`), so free text cannot be added to an event without failing closed.
* `usage()` returns only `prompt_tokens`, `completion_tokens`, `total_tokens`, `cached_tokens` (ints) and drops other keys. `bounded_model()` and `reference()` bound or hash the model. `CallContext.metadata()` requires opaque ids and closed `[a-z][a-z0-9-]` capability and case-type identifiers.
* `complete_in` writes `tokens`, `charge`, `outcome`, `returned_model=reference(model)`. `output()` stores `reference(output)` only, never proposal text.
* `capability_usage()` (report `by_capability`) emits counts, token totals and `tokens_per_accepted_proposal` per capability only.
* `assistants.py`: `issue_permit` builds `CallContext` from `reference(tid)`, `reference(attempt)`, `reference(prompt_version)`; `_settle_meter` passes usage and model only; `complete` publishes `publish_output(meter_root, task id, ...)`.
* `chat_panel.py`: `_ask` builds `CallContext(root, root, TASK, "retrofit-case", reference(TASK), reference(system))`; the receipt holds counts, `valid_usage` tokens, outcome, limits, `meter_id`, `meter_root`; chat output id is `chat:{tid}:{seq}` with `eligible=False`. Limit-fallback returns `LIMIT_REACHED` with `model_calls=0`.
* Tests: `test_ai_consumption.py` has `test_metadata_canaries_and_historical_output_not_exported` and `test_report_attributes_usage_per_assistant_and_accepted_proposal`; `test_chat_panel.py` covers receipt shapes and limits. Neither feeds sentinel strings through all five assistants.

## Open question

Whether any sentinel raw-content string reaches a usage envelope, ledger event or chat receipt. Resolved only by executing a deterministic probe after critique.

## Boundaries

Offline only; no `.env`, private data, cloud or model calls; no `src/` or `docs/` edits (tracking-only commit).
