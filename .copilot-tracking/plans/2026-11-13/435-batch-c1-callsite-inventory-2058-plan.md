# Plan: classify heldout_aoai.py in the call-site inventory (435 C1, 2058)

Research: [research](../../research/2026-11-13/435-batch-c1-callsite-inventory-2058-research.md). Details: [details](../../details/2026-11-13/435-batch-c1-callsite-inventory-2058-details.md). Refs #435, #432. Focused tier: test-only classification, no source, workflow, dependency or gate change.

## Phases

* [ ] Phase 1: reproduce the failure in a scratch venv (`/tmp/venv-435inv-2058`, pip only).
* [ ] Phase 2: add the `own-accounting` `INVENTORY` entry for `agents/src/zava_forward/agents/heldout_aoai.py`.
* [ ] Phase 3: run the focused validation (inventory, cutover audit, heldout batch tests, ruff, format, both mypy runs).
* [ ] Phase 4: remove only the scratch venv, commit locally with trailers, leave a clean tree.

## Decisions

* Status `own-accounting` (not `ledger`): the file has no `consumption.reserve` or `dispatch_check` call, so `ledger` would fail the admission invariant and overstate the join.
* No change to the adapter, the runner, the cutover pack or any workflow.
