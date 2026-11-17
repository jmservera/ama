---
title: Issue 216 changes
date: 2026-11-17
---

# Changes

Started. Planned: test in `src/agents/tests/test_regulatory_answers.py`, one README sentence in `src/agents/README.md`.

Done. Added `test_adversarial_variants_refuse_and_controls_answer` (`src/agents/tests/test_regulatory_answers.py`) and a README
note in `src/agents/README.md`. No production, frozen-case or core change.
Validation (PYTHONPATH = worktree agents/core src + tests): `unittest test_regulatory_answers test_regulatory_gates test_eval_registry`
35 tests OK; `ruff format --isolated --line-length 100 --check` on the test file clean; `mypy .` in src/agents no issues (58 files).
Not run: rpi-checks --all, core/api suites, SQL/browser (not touched; heavy lock held). Without the PYTHONPATH the stale installed agents copy
fails 2 tests (environment, preserved as adverse evidence).
