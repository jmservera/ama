# Issue 2203 details (2026-11-22)

## Phase 2
* Add `_read_connection()` next to `_transaction()` in src/core/src/zava_forward/core/assistants.py: an autocommit connection from `store.assistant_connection()`, closed in `finally`, no application lock.
* `forecast()` uses it with `rel.read_only()`. No other caller changes.
* Test in src/core/tests (existing assistants test module): while `forecast` is running, another connection takes `BEGIN IMMEDIATE` with a zero busy timeout; it must succeed.

## Phase 3
* Runbook `Live Demo Status` becomes 2026-11-22; rows updated from the live note; stale-cohort and Hardening rows rewritten; forecast hazard added to the AI scope row and cautions.
* Keep the `### The five homes` table and header unchanged (parsed by test_generated_dataset).

## Acceptance mapping
* Criteria 1 to 4 are answered in the changes record table.
