# Changes: M4 core features (refs #199)

Plan: [plan](../plans/2026-10-15-issue-199-m4-core-features-plan.md).

## Moves (git mv, 9 renames)

* `mvp/zavaforward_mvp/{chat_privacy,chat_isolation,recovery}.py` to `src/core/src/zava_forward/core/`.
* `mvp/zavaforward_mvp/ai_eval.py` to `src/agents/src/zava_forward/agents/`; `mvp/evals/ai_priority_golden.json` to `src/agents/evals/`.
* `mvp/tests/test_{chat_privacy,chat_memory,recovery}.py` to `src/core/tests/`; `mvp/tests/test_ai_eval.py` to `src/agents/tests/`.

## Edits

* Imports: `server.py`, `test_ai_tasks.py` and `test_chat_isolation.py` import `zava_forward.core` and `zava_forward.agents`; moved tests use `dataset.DATA` instead of `test_mvp.DATA`; `chat_isolation` imports `zava_forward.core.chat_privacy`.
* `ai_eval`: golden path from `src/agents/evals/`, override `ZF_AI_GOLDEN`; run line updated.
* Registry and tests: `registry.json` paths, `EVAL_DIRS` in `test_eval_registry` and `test_synthetic_provenance`; provenance register, data dictionary, needs inventory, chat memory DPIA.
* Tooling: ruff and mypy exemptions in `core` and `agents` (plus E731 for `ai_eval`); `mvp-ci` and `mvp-validation` install `src/agents`, trigger on `src/agents/**`, compile `src/agents/src`; `mvp/Dockerfile` builds the agents wheel and copies the golden file with `ZF_AI_GOLDEN`; dockerignore allows them.
* Docs: parity matrix statuses and totals, `mvp/README.md`, `infra/README.md`, `src/README.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* Divergence: `test_chat_isolation` stays in `mvp/tests` until M5 (depends on `test_role_matrix`).

## Validation

| Command | Result |
| --- | --- |
| `cd mvp && PYTHONPATH=.:../src/core/tests:../src/agents/tests python3 -m unittest discover -s tests -q` | Ran 443, OK (skipped=92); baseline 505 |
| `cd src/core && python3 -m unittest discover -s tests -q` | Ran 252, OK; baseline 196 |
| `cd src/agents && ...` | Ran 31, OK; baseline 25 |
| `cd src/api`, `src/importer`, `src/orchestrator` | 8, 9, 4 OK; unchanged |
| Total | 747, equal to the 747 baseline; skips 92 as before |
| `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/agents` | all pass |
| `pip wheel --no-deps --no-build-isolation src/core src/agents` | both wheels build |
| `ZF_AI_GOLDEN=... python -m zava_forward.agents.ai_eval` | runs the golden scenarios |
| `python tools/rename-zava-tests.py` | 7 errors, `PIL` and `pptx` not installed; identical on unmodified `main`, unrelated |
| `docker build -f mvp/Dockerfile .` | not run: docker socket permission denied; CI image job |
| SQL Server `mssql` job | not run locally; CI |

Hashed requirements: no dependency change, so pip-compile was not needed and no pin was touched. SQL portability: no `INSERT OR REPLACE/IGNORE`, `AUTOINCREMENT` or `PRAGMA` added; `recovery` keeps `sqlite3` for the local backup copy only.
