# Research: issue #891 exact-source validation quality (2026-11-13)

* Task: `chat-clean-validation-891-0901`. Issue #891 Refs only; criterion 2 stays unmet; no ticks or closure.
* Source pin: `347962dace94171724cc8db4044c8d783335fecf` (worktree HEAD at start, branch `test/demo-chat-clean-validation-891-0901`). Earlier candidate: `8c735ae5710ba262ce9de8363ecd74848c2f1d85`.
* Research disposition: executed (git show of the candidate's own evidence, one diff, one run).

## Recovered selector (from candidate evidence, treated as data)

* The candidate research and review (`git show 8c735ae:.copilot-tracking/{research,reviews}/2026-11-12-chat-call-provenance-891-1112-*.md`) name one module: `tests.test_ai_consumption_api` run from `src/api`, "37 tests OK (68 s)". No other module or per-test selector is named.
* Current repository file: `src/api/tests/test_ai_consumption_api.py`. Safe derived selector: `python -m unittest test_ai_consumption_api -v` from `src/api` with the README test-helper path `PYTHONPATH=tests:../core/tests:../agents/tests` (helpers only, no package source).
* Recovered: the module and the count 37 (verified below as the current count). Not recoverable: any earlier subset or ID list beyond that module, and the author's own 37-test claim (the "previous author claim" is a different, still-unverified statement; this task does not verify it).

## Tested-code equality between pins

* `git diff 8c735ae 347962d` over `src/{core,agents,api}/{src,tests}` lists 32 files. Unchanged between pins: `test_ai_consumption_api.py`, `core/ai.py`, `core/ai_consumption.py`, `core/chat_panel.py`, `agents/chat.py`, and `core/tests/release_support.py` (the imported helper location).
* Changed and imported by the selected module: `core/store.py` (`Store` imported), `api/server.py` (`App`, `make_handler`), `api/tests/test_assistants.py` (imports `Base`, `proposal`; one test added). Also changed in the agents package: `agents/ai_eval.py` (loaded by the API report path). The selected module therefore does NOT run byte-identical dependencies to the earlier pin; only the five named tested files and the test file itself are equal.

## Environment

* Ambient `python3` resolves `zava_forward` to a different checkout (`/home/azureuser/source/ama/src/...`); not accepted as exact-source. An owned venv `/tmp/v891-0901` was created and `pip install --no-deps ./src/core ./src/agents ./src/api` (non-editable) was used. `PYTHONPATH` held only test-helper directories. No unrelated package was installed; no dependency was missing for the run.

## Limits

No model, external network, cloud, SQL service, browser, Docker, private data or `ZF_DATA` use (the tests themselves use loopback HTTP and local SQLite). No source edit, no full gate.
