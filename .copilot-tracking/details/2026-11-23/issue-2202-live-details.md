# Details: issue 2202 readings coverage tool

## Phase 1
* `coverage(snapshots)`: merge items by id across snapshots, preferring a loaded state over `not-loaded`. Return total, per state counts, `with_readings` (fresh, stale, offline), `recent` (fresh), `unmeasured` (not-loaded, unavailable, restricted, not-connected) and shares of all homes.
* `meets(result, share=0.5)`: True only when the lower bound `with_readings/total` reaches the share (unmeasured homes are never assumed to have readings).
* Tests: dedupe and prefer loaded; lower bound rule; empty input.

## Phase 2
Live tiles via Playwright session cookie, 8x8 bbox grid over the map extent, `sensors=1`.
