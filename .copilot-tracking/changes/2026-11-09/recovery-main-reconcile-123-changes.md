<!-- markdownlint-disable-file -->
# Changes: recovery main reconciliation (#123), 2026-11-09

Plan: [plan](../../plans/2026-11-09/recovery-main-reconcile-123-plan.md). Refs #123, #128, #440.

* Planning commit `3b3334fab` preceded the merge.
* Ordinary merge `18cc67ece` of `origin/main` `b46a9ad9a9619db535368d1b2cbbddec8110e122` into seed `cfd1bca86`. Auto-merged `docs/reference/README.md`, `docs/reference/log.md` and `docs/architecture/cutover-evidence-pack.md` with no conflicts. Merged log has 0 removed lines against both parents; README and pack removals versus the topic are main-side edits only (`ms.date`, wording).
* `paired_equity.py` and `test_paired_equity.py` are unchanged by the merge. No source edit, no threshold or policy change; `fairness_evidence=False` and `activation_allowed=False` preserved.

## Validation (owner-selected demo-targeted tier; no `rpi-checks --all`)

From `src/core`, `PYTHONDONTWRITEBYTECODE=1`, current-source imports (`PYTHONPATH=src:tests`):

* `python3 -m unittest tests.test_paired_equity tests.test_cohort_eval tests.test_household_conditions tests.test_retrofit_effects tests.test_monitoring_coverage tests.test_rule_engine tests.test_chat_privacy`: 146 tests, OK, 0 skips.
* `ruff check src tests`: pass. `ruff format --check src tests`: 215 files formatted. `mypy`: no issues in 269 files.
* `git diff --check origin/main...HEAD`: clean.
* Tool versions were ruff 0.17.3 and mypy 2.4.1 against pins 0.17.1 and 2.4.0; recorded deviation.
* Not run: API, SQL, browser, hosted CI, complete gate. No mssql tests were selected.
