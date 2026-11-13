# Details: 435 C1 call-site inventory (2058)

## Phase 1

Create `/tmp/venv-435inv-2058` with `python3 -m venv`; `pip install -e src/core -e src/agents -e "src/api[dev]" mypy ruff`. From `src/api` run `PYTHONPATH=../core/tests:../agents/tests:tests /tmp/venv-435inv-2058/bin/python -m unittest test_ai_call_site_inventory -v`. Expect one failure listing `agents/src/zava_forward/agents/heldout_aoai.py`.

## Phase 2

Edit `src/api/tests/test_ai_call_site_inventory.py`: append to `INVENTORY` after the resident demo entries:

`"agents/src/zava_forward/agents/heldout_aoai.py": ("own-accounting", "<note>")`

Note content: opt-in adapter for the held-out batch runner; worst-case tokens and cost reserved and closed per call by `heldout_batch.run_batch` under a finite owner authorization (USD cap, call cap); no core consumption ledger, price register or authority is wired, so it stays own-accounting until the owner approves host wiring; nothing is dispatched at construction, and the CLI runner needs explicit flags for a live call. State that the accounting applies to runner-mediated calls only; a direct call to the returned provider bypasses the runner (critique N1). Keep the existing dict style and ruff line length.

## Phase 3

* `src/api`: unittest `test_ai_call_site_inventory test_cutover_audit` with `PYTHONPATH=../core/tests:../agents/tests:tests`.
* `src/agents`: unittest `test_heldout_batch` (and `test_heldout_aoai`) with `PYTHONPATH=../core/tests:tests`.
* Repo root: `ruff check src/agents src/api`, `ruff format --check src/agents src/api`.
* `cd src/agents && mypy`, `cd src/api && mypy`.

## Phase 4

`rm -rf /tmp/venv-435inv-2058` only. Resolve identity via `gh api user`, set repo-local `user.email`, commit with `Refs #435`, `Refs #432` and the Copilot co-author trailer. No push, no GitHub edits.
