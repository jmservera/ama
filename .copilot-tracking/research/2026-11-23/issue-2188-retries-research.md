# Issue 2188 timing-retries research (2026-11-23, third pass)

Planning Readiness: Ready. Research disposition: executed.

## Prior coverage

Earlier workers covered `--no-cache` removal, shard partition, shard-level retry with `receipt["retries"]`, tamper tests, image concurrency and `wall_seconds`. Gate-level before/after pair remains unproven (needs two full gates; `--all` forbidden here). Four-image timed build and live receipt are owner/coordinator work.

## New angle

`tools/rpi-gate-timing.py` (the before/after comparison tool, issue #1830) ignores `receipt["retries"]`. A retried shard silently inflates `span_seconds`, so an arm containing a retry looks identical to a clean arm; the "receipt records retries" criterion is not visible in the evidence that proves speed. `commands_of` reads only `commands`; `analyse` and `compare` emit no retry data.

## Slice

Report `retries` (count) and `retried_groups` in `analyse`; carry per-arm `retries` totals in `compare`; add a Retries column to the markdown table. Read-only analysis tool: no gate semantics, permissions, images or packages change. Tier FOCUSED. No `src/` change. Synthetic demo, no Azure or browser proof applicable to a local tool.
