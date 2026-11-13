# Research: held-out token measurement and cost-cap runner (#432 AC3, #435 AC4)

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* `chat_heldout.py` scores scripted harness only; no model calls, no cost ceiling.
* `heldout_freeze.check_freeze(manifest)` returns `outcome` `frozen`/`insufficient`, `held_out_cases`, `manifest_digest`. Reuse as the freeze gate.
* `dispatch.AgentWorker.provider_call(system, prompt, max_tokens, timeout)` never raises; envelope has `usage` (`prompt_tokens`, `completion_tokens`, `total_tokens`, optional `cached_tokens`), `outcome` (`returned`), `text`.
* `core.chat_panel.valid_usage` validates usage dicts (core is untyped for mypy; agents does not import it in new code to keep the dependency small; validation is local).
* Conventions: ruff line length 100, mypy strict, unittest, tests import fixtures from `tests/` (`heldout_freeze_fixture.manifest`).

## Design decisions

* Money uses `Decimal`; hard cap `Decimal("5.00")`.
* Authorization validated before any call; worst-case next-call cost = max_prompt_tokens * input_rate + max_completion_tokens * output_rate (cached rate never lowers the worst case).
* Live path requires `--execute-live` and an injected provider; CLI offers dry-run only plus a refusal for live without a configured provider.
* Evidence label differs: `measured held-out batch` versus `dry-run simulation - not measured evidence`.

## Boundary

Owned files: `heldout_batch.py`, `tests/test_heldout_batch.py`, README if needed. No live calls are made in this task.
