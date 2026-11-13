# Critique: #435 held-out batch live adapter plan (1953)

Executed once by `rubber-duck` (independent). Verdict: Revise. The reviewer could not write this file; the coordinator transcribed the findings and applied the dispositions below. Not repeated.

| ID | Finding | Disposition |
| --- | --- | --- |
| P1 | Byte-length prompt bound omits chat framing overhead | Accepted as residual: `_usage` rejects any post-call prompt count above `max_prompt_tokens`, charges the worst case and stops the batch, so accounting stays bounded. Documented in README |
| P2 | Rates and deployment identity are not verified pre-spend | Out of scope: rates, resource and model are owner-supplied in the authorization. Adapter checks response model against `--model` and fails closed. Documented as an owner pre-run check |
| P3 | `max_tokens` and API version `2024-10-21` unverified | Accepted: GA 2024-10-21 supports `max_tokens` for non-reasoning models such as gpt-4.1-nano. README says to confirm before the run |
| P4 | Cap resets across runs (no durable ledger) | Deferred follow-up (out of scope, runner-wide, pre-existing). README states one live run per authorization |
| P5 | Missing cached-token detail can undercharge | Adopted: adapter requires an integer `prompt_tokens_details.cached_tokens`, else unmeasured (fail closed) |
| P6 | Frozen ids do not bind proposal content | Deferred follow-up (pre-existing runner gate, out of scope); owner must supply the frozen proposals |
| P7 | Credential exception chains may leak in tracebacks | Adopted: `raise ... from None`, tests render tracebacks and captured output for the token |
