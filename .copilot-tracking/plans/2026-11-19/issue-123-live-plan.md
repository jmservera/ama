# Issue 123 live plan (2026-11-19)

* Phase 1: add `GoldenFileError` and a `load_golden(path)` helper in `src/agents/src/zava_forward/agents/ai_eval.py`; `run_eval` uses it.
* Phase 2: add focused tests in `src/agents/tests/test_ai_eval.py` (missing file names `ZF_AI_GOLDEN`; present file still loads).
* Phase 3: run `test_ai_eval`, mypy in `src/agents`, ruff check; record per-criterion table in the changes file.
* Non-goals: moving the golden file, D1, D3, other eval modules, issue filing.
* Tier: FOCUSED local tests; src change noted as FULL-tier before publication, no `--all` run (heavy lock).
