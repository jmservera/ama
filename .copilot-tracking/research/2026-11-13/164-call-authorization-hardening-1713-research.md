# Research: issue #164 criterion 7, call authorization hardening

Disposition: executed. Planning Readiness: Ready.

## Findings

* `call_authorization` in `src/agents/src/zava_forward/agents/chat_eval.py` accepts `max_budget=inf` and `NaN`
  (only `<= 0` is checked; `NaN <= 0` is false), compares `expires_at` as a raw string (`"zzz"` is
  "unexpired"), and never checks spend against the budget.
* It is called only from `enablement_decision` with `auth=None` to print `blocked`. No execution path
  gates a model call: `Run` always uses the `Scripted` provider.
* Existing test `test_actual_calls_are_blocked_without_finite_unexpired_authorisation` uses date-only
  expiry and `now`; these become invalid under strict UTC timestamps and must be updated.
* `regulatory_gates.py` already parses expiry with `datetime.fromisoformat` and requires an aware value.

## Approach

* Strict `_parse_utc` (ISO-8601, timezone present, offset zero).
* `math.isfinite` on budget; new `projected_spend` and `used_spend` arguments checked against `max_budget`.
* `AuthorizedModel` wrapper: checks `call_authorization` before every dispatch, fail-closed with
  `ModelUnavailable`, and meters used calls, tokens and spend. `Run` accepts an optional actual `provider`
  and wraps it; scripted calls stay ungated.
