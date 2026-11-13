# Details: 164 call authorization hardening

## Step 1
* `_parse_utc(value)`: str only; `datetime.fromisoformat` (Z mapped to +00:00); reject naive and non-zero offsets; None on failure.
* Budget: bool/non-number/non-finite/<=0 rejected. `projected_spend`, `used_spend` default 0.0; must be finite and >= 0 (else reason); `used+projected > max_budget` blocks.
* Expiry: invalid `expires_at` -> "expires_at is not a UTC ISO-8601 timestamp"; invalid `now` -> blocked; `expires_at <= now` -> expired.

## Step 2
* `AuthorizedModel(provider, auth, *, now, tokens_per_call, spend_per_call)`; `__call__` computes
  `call_authorization(auth, 1, tokens_per_call, now=now(), used_*, projected_spend=spend_per_call)`;
  blocked -> `ModelUnavailable("call-not-authorised: ...", calls=0)` without calling provider. After dispatch it accrues usage.
  `now` is a callable returning the clock string so expiry is checked per call. Missing/None spend_per_call blocks.
* `Run.__init__(..., provider=None, authorization=None, clock=None)`; provider given -> wrapped. Scripted unchanged.

## Step 3-4
* Cases: inf, nan, bool, zzz, naive, non-UTC offset, budget exceeded (projected and accrued), wrapper blocks with no/missing auth and provider never invoked, allowed call dispatches, second call blocked once accrued budget exhausted, expiry mid-run.
