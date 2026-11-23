# Issue 2188 wall-time research (2026-11-23, second pass)

Planning Readiness: Ready. Research disposition: executed.

## Findings

* The issue's only unproven criterion is "wall time measured before and after on the same tree". Earlier passes (see `docs/reference/research/issue-2188-live-image-concurrency-2026-11-23.md`) proved the other six at unit level.
* Receipt command rows carry `started` and `finished`, but the receipt has no total wall time or per-group duration, so a before/after comparison needs hand arithmetic over timestamps.
* `--all` must not be run by this worker, so the before/after pair itself cannot be recorded here.
* Code-satisfiable slice: record `wall_seconds` (earliest start to latest finish, retries included) in the receipt and per-row `elapsed_seconds`, with a unit test. Receipt validation ignores unknown top-level keys and the command-identity check compares only named keys, so the addition does not change verify semantics.

## Scope

Tier: focused (tooling-only, receipt gains additive fields; no permission, image, package, secret or verify semantics change). Synthetic demo, no Azure access needed.
