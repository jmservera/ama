<!-- markdownlint-disable-file -->
# #184 stage B1 start/stop retry enforcement: plan (2026-11-12)

Research: [research](../../research/2026-11-12/issue-184-start-stop-b1-1112-research.md). Details: [details](../../details/2026-11-12/issue-184-start-stop-b1-1112-details.md). Prospective: written before any source edit.

## Objective

Before every actual send attempt, including retries and after pacing or backoff delays, re-read and revalidate the run control; stop, expiry, invalid or unreadable control, or a home no longer in the cohort prevents that and later sends. Defaults without the optional gate are unchanged.

## Phases

* [x] 1. Failing-first tests in `test_live_simulator.py` and `test_live_control.py` (raw failing output retained).
* [x] 2. `live_simulator.py`: optional `attempt_gate` on `send_slot` and `run`, module function `attempt_permitted`, wired in `main` only when a control file is set.
* [x] 3. Targeted tests, ruff, mypy on changed files.
* [x] 4. Changes record, one Review (author, not independent), state record, scoped commit with privacy-safe identity.

## Constraints

No schema, SQL, Bicep, permission, guard, worker, UI, cadence, identity or new service change. No remote cancellation claim. No attempt cap (not admitted). One critique and one Review only.

## Critique

Executed once, read-only and self-run (not independent) before implementation; see [critique](./issue-184-start-stop-b1-1112-critique.md).
