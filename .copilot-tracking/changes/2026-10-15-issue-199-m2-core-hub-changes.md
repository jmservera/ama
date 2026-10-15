# Changes: M2 core hub move (refs #199)

## Summary

Moved the core hub from `mvp/zavaforward_mvp` to `src/core/src/zava_forward/core` with `git mv` (no shim or copy left): store, sqlstore, mssqlstore, factory, ledger, continuity, chatthreads, doc_controls, documents, controls, finance, grants, governance, signoffs, resident_decisions, workflows, quality, procurement, insights, projection, ranking, ai_tasks, assistant_release, ai_registry, assistants, and `policies/ranking-v1.json`. Tests moved: test_chatthreads, test_documents, test_finance_signoffs, test_generated_dataset, test_governance, test_quality_procurement, test_sqlreads, test_sqlstore and `release_support.py` to `src/core/tests`; `test_content_standard` to `src/api/tests`. New `src/core/tests/dataset.py` holds fixtures split from `test_mvp.py`.

## Divergences

* `ai_registry` and `assistants` went to `core`, not `agents` (A1; the dependency rule forbids `core` importing `agents`). R1 rebuilds dispatch later.
* `test_continuity`, `test_document_controls`, `test_ranking_policy`, `test_mssqlstore` stay in `mvp/tests` (they use `test_mvp` or the server); they move with M5.
* `factory` default data path is now relative to the current folder.

## Other edits

* `mvp/`, `infra/`, `support/` imports rewritten; `mvp/Dockerfile` and `Dockerfile.dockerignore` no longer copy `policies/`; CI `PYTHONPATH` updated, check names unchanged; `src/core` and `src/api` `pyproject.toml` exemptions and package data; READMEs, matrix, reference index and log updated. No dependency change, so hashed requirements were not regenerated.

## Validation (venv `/tmp/m2venv`, pip only, Python 3.12.3)

| Command | Result |
| --- | --- |
| Baseline on `main`: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` | Ran 702, OK (skipped=92) |
| `cd mvp && PYTHONPATH=.:../src/core/tests python3 -m unittest discover -s tests` | Ran 551, OK (skipped=92) |
| `src/core`: unittest discover -s tests | Ran 167, OK |
| `src/api`, `src/agents`, `src/orchestrator`, `src/importer`: unittest | 8, 8, 4, 4 OK |
| Total | 742 equals baseline 742 (702 plus 40 already in `src` (core 20, agents 8, api 4, orchestrator 4, importer 4)); equal or greater |
| `ruff check .`, `ruff format --check .`, `mypy` in each src project | all clean |
| `pip wheel --no-deps --no-build-isolation src/core` | wheel contains `zava_forward/core/policies/ranking-v1.json` |
| `python3 tools/rename-zava-tests.py` | 7 errors, all `ModuleNotFoundError` for `pptx` or `PIL` (not installed here); unrelated to M2 |
| `git diff -M --stat` | renames detected, 61 changed files |
| Docker image build, SQL Server `mssql` job | not run locally (docker socket permission denied, no SQL Server); rely on CI |
