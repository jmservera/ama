# Details: authority rotation guard

## Phase 1

`_pool(db)` returns the row for `Limits.pool`; otherwise `MIN(calls,tokens,expires)` and `MAX(used_calls,reserved_tokens)` across all rows, clamped by the current configuration; `None` when the table is empty. `_reserve` inserts the inherited values for a new digest. `disabled` uses the same view so refusal is reported before dispatch.

## Phase 2

Tests: rotated token after call exhaustion, after token exhaustion, and a rotated authority that spends only the remaining allowance once across independent connections. They failed against the unmodified source (3 failures) and pass with the change.

## Phase 3

Run with `PYTHONPATH=<worktree>/src/{core,agents,api}/src` plus the test directories.
