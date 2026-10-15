# Research: M4 core features (refs #199)

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue 199 comments, ADR 0006 (Accepted, move-not-copy), parity matrix rows marked M4 (`chat_privacy`, `chat_isolation`, `recovery`, `ai_eval`, `ai_priority_golden.json`, five tests), merged PRs 296, 297 (M1, M2) and 298 (M3, merged 2026-10-15; branch rebased on `main` `5546282`), `src/README.md`, `.github/copilot-instructions.md`, `docs/reference/README.md`.
* Baseline on `main`: `mvp` 505 (skipped 92), core 196, agents 25, api 8, importer 9, orchestrator 4. Total 747. Target: at least 747.
* Size: about 1,000 lines of Python, one JSON file and five tests, no import cycle. One pull request is safe, so no M4a/M4b split.

## Findings that shape the plan

* `chat_isolation` imports `chat_privacy` relatively, so it moves with it. `ai_eval` imports only `core` (`ai_tasks`, `store`), so it may live in `agents` under the dependency rule.
* `test_chat_isolation` extends `test_role_matrix` and the server harness (M5), so it stays in `mvp/tests` and imports the moved module (the M2 precedent).
* `test_chat_privacy`, `test_chat_memory` and `test_recovery` used `test_mvp.DATA`; the same data lives in `core/tests/dataset.py` (M2), so they move to `core/tests` and use it.
* `ai_eval.GOLDEN` was computed from the module path (`mvp/evals`). The golden file goes to `src/agents/evals/` (outside the package, ADR 0006), so the path is recomputed and overridable with `ZF_AI_GOLDEN`. The `mvp` image never copied the golden file, so `/api/ai/report` could not run in the image; the image now installs the `agents` wheel and copies the file.
* Path-sensitive strings: eval registry paths and `EVAL_DIRS` (registry and provenance tests), provenance register, data dictionary, needs inventory, chat memory DPIA, READMEs, CI paths and installs.
* `recovery` uses `sqlite3` only for the local backup copy; no `INSERT OR REPLACE/IGNORE`, `AUTOINCREMENT` or `PRAGMA` exists in the moved code.
* Docker is installed but the socket is permission denied, and no SQL Server is available locally; rely on CI.
* No dependency change, so no pip-compile run is needed and pins stay as they are.
