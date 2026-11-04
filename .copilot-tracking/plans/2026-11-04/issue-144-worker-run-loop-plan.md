# Plan: issue 144 worker run loop (2026-11-04)

Research: [research](../../research/2026-11-04-issue-144-worker-run-loop-research.md). Details: [details](../../details/2026-11-04/issue-144-worker-run-loop-details.md).

## Stack

* [x] Slice 1 (this PR): `worker.serve` loop, SIGTERM/SIGINT handler, fail-closed `serve` command, tests, status row.
* [ ] Slice 2: Azure Queue adapter for `TaskQueue` (new dependency pin, image and supply-chain checks; complete gate).
* [ ] Slice 3: API post-back endpoint and `ResultSink` with fence and release re-validation (security-sensitive; complete gate).
* [ ] Slice 4: orchestrator real job entrypoint; hosted load run and restore proof (needs owner Azure access).

## Validation (focused tier)

Unit tests, ruff, mypy `--cache-dir=/tmp/mypy-530`. No Bicep or deployment change; gate not run.

## Critique (single pass)

Verdict: proceed. Applied: `serve` must refuse rather than idle, so the unchanged agents app never appears healthy while processing nothing; the version print stays the default command.
