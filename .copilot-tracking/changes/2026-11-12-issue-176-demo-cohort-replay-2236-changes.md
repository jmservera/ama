---
title: Changes, issue 176 five-home demo cohort replay regression
ms.date: 2026-11-12
---

* Added `runbook_five_homes` and two tests to `src/core/tests/test_generated_dataset.py`: a malformed-table parser guard and `test_runbook_five_home_cohort_is_reproduced_by_seed_and_as_of`.
* Added a provenance bullet to `docs/capstone/demo/runbook.md`, a section and `ms.date` bump to `docs/reference/research/retrofit-synthetic-data/README.md`, and a `docs/reference/log.md` entry.
* No generator, builder, manifest, `dataset.py` or other scenario recipe source changed; no index change (no file added).

## Amendments and divergences

* Critique corrections applied before implementation (unique ids, defensive parsing, 6,000-row register wording). No divergence from the plan.

## Validation (focused tier; synthetic inputs only)

* Isolated virtualenv, `pip install -e src/core` from this worktree and pinned `ruff==0.17.1`; no `PYTHONPATH` to source packages.
* From `src/core`: `python -m unittest tests.test_generated_dataset tests.test_scenario_manifest tests.test_determinism_audit` ran 40 tests, OK.
* Negative controls (temporary scripts, deleted): wrong id, wrong stage, wrong type and duplicate id in the runbook copy each fail the new test. Seed 20260902 moves all five homes; as-of 2026-12-01 does not.
* `ruff check tests/test_generated_dataset.py` passes. The file is excluded from `ruff format` by project configuration.
* Not run: blanket gate, full suite, hosted CI, mypy over the whole project, any cloud, provider, model or private-data path.
