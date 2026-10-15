# Details: M4 core features (refs #199)

| Phase | Files | Success |
| --- | --- | --- |
| 2 | `chat_privacy`, `chat_isolation`, `recovery` to `src/core/src/zava_forward/core`; `ai_eval` to `src/agents/src/zava_forward/agents`; `ai_priority_golden.json` to `src/agents/evals`; `test_chat_privacy`, `test_chat_memory`, `test_recovery` to `src/core/tests`; `test_ai_eval` to `src/agents/tests` | Git shows renames; nothing left in `mvp/` |
| 3 | `server.py`, `test_ai_tasks.py`, `test_chat_isolation.py`, moved tests, `registry.json`, `test_eval_registry.py`, `test_synthetic_provenance.py`, provenance pack, DPIA, READMEs | No `zavaforward_mvp.<moved>` or `mvp/evals` reference remains |
| 4 | `src/core/pyproject.toml`, `src/agents/pyproject.toml`, `mvp-ci.yml`, `mvp-validation.yml`, `mvp/Dockerfile`, `mvp/Dockerfile.dockerignore` | ruff and mypy pass; check names unchanged |
| 6 | parity matrix, `docs/reference/README.md`, `docs/reference/log.md` | Statuses and totals recorded |
