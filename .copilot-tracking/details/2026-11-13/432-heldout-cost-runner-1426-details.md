# Details: 432-heldout-cost-runner-1426

## API (`heldout_batch.py`)

* `HARD_CAP_USD = Decimal("5.00")`, `MAX_CALLS = 50`.
* `authorization_problems(auth, now=None) -> list[str]`: required string fields (`approved_by`, `authority_ref`, `model`), `expires_utc` ISO with tz and in future, `max_calls` int 1..50, `max_total_tokens` int > 0, `max_budget_usd` Decimal-parsable in (0, 5.00], `currency == "USD"`, rates non-negative Decimals (input/output required > 0, cached optional), plus `max_prompt_tokens` / `max_completion_tokens` positive ints (needed for worst-case).
* `worst_case_usd(auth)` = max_prompt * input_rate/1e6 + max_completion * output_rate/1e6.
* `run_batch(auth, manifest, proposals, call, *, mode, now=None)`: `mode` is `dry-run` or `live`. Refuses (outcome `refused`, zero calls) on authorization problems, `check_freeze != frozen`, empty proposals. Loops proposals; before each call stops with `stop_reason` in {`max_calls`,`max_total_tokens`,`budget`,`proposals-exhausted`}; a pre-call check also tests `tokens + max_prompt + max_completion > max_total_tokens` is not used; tokens check is `tokens >= max_total_tokens`. A failed envelope (no valid usage) stops the batch (`stop_reason` `unmeasured-call`) and charges the worst case, so cap cannot be bypassed.
* Cost of a call = (prompt - cached) * input + cached * (cached_rate or input) + completion * output, all per 1M.
* `dry_run_call(proposals)`: deterministic estimator (chars/4) returning envelope with usage; zero network.
* `spread(values)`: count, min, p50 (median), mean, p90 (nearest-rank), max.
* `render_markdown(report)`; `main(argv)` CLI: `--authorization`, `--manifest`, `--proposals`, `--dry-run` / `--execute-live`, `--json-out`. Exactly one mode flag required; `--execute-live` with no configured provider exits 2 with refusal (no provider is wired in this task).
* Evidence label: `measured held-out batch` only in live mode with at least one measured call; else `dry-run simulation - not measured evidence`.
* Report includes `source`, `spend_authority_ref`, token totals input/cached/output, `accrued_usd` string, calls, stop reason, per-proposal rows, no proposal text.

## Tests

Refusals (each field, expired, cap 5.01, max_calls 51, USD, unfrozen manifest, empty proposals) with call spy at 0; stop before dispatch on budget/calls/tokens; accrued never exceeds cap; dry-run zero provider calls and label; live label; unmeasured call stop; spread arithmetic; determinism; CLI refuses live without provider and dry-run runs.

## Critique dispositions (all applied directly; verdict Revise, one pass)

* PC-001: each proposal carries `prompt` text; before dispatch require `ceil(len(system+prompt)/4)` estimate <= `max_prompt_tokens` else stop `prompt-too-large`; provider receives `max_tokens=max_completion_tokens`; envelope usage above the bounds is an `unmeasured-call` violation charged at worst case; runner performs no retries.
* PC-002: pre-call stop when `tokens + max_prompt + max_completion > max_total_tokens` (replaces `tokens >= max`).
* PC-003: worst-case input rate = max(input, cached when given); explicit zero cached rate is honoured (`None` means use input rate).
* PC-004: usage valid only when ints (not bool) >= 0, total == prompt + completion, cached <= prompt, prompt <= max_prompt, completion <= max_completion; otherwise unmeasured, stop, charge worst case.
* PC-005: proposal ids must be unique and each in `manifest["held_out"]["case_ids"]`; `authorization.model` must equal `manifest["versions"]["model"]`; live mode also requires `provider_model` equal to the authorized model; mismatches refuse with zero calls.
