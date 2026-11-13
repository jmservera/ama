# Recovery research and plan: chat-clean-validation-891-0901 (2026-11-13, prospective)

Original records at e01ae7796 are preserved unchanged. Source pin 347962dace stays. Historical-pin byte-identical replay is impossible (store.py, server.py, ai_eval.py, test_assistants.py differ from 8c735ae).

## Preflight evidence (read-only, before any environment change, 09:07 UTC)

* Venv `/tmp/v891-0901` `zava_forward.agents.ai_eval.__file__` = site-packages copy. `ai_eval.py:40`: `GOLDEN = Path(ZF_AI_GOLDEN or Path(__file__).resolve().parents[3]/"evals"/"ai_priority_golden.json")`; `ZF_AI_GOLDEN` unset.
* Resolved `GOLDEN` = `/tmp/v891-0901/lib/python3.12/evals/ai_priority_golden.json`, exists: False. The repo fixture `src/agents/evals/ai_priority_golden.json` exists.
* Supported: the non-editable install causes the FileNotFoundError path. Not yet shown: that the editable install fixes it and that no other error remains.

## Plan (admitted work only)

1. `/tmp/v891-0901/bin/pip install --no-deps -e src/core -e src/agents -e src/api` (README form; no new dependencies, venv only).
2. Probe resolved `GOLDEN` and module origins (expect worktree `src/...`); stop if not.
3. One run from `src/api`: `env -u ZF_DATA PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_ai_consumption_api -v`, output to a new file, real exit captured. No rerun.
4. One independent recovery Review; commit new files only.
Excluded: source/test/fixture edits, other suites, external services, push, cleanup.
