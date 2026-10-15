# Research: retire prototype/ (#202 step 1)

Disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #202 step 1 and owner decisions 2026-10-14/15 (prototype may retire before mvp/; mvp/ untouched).
* ADR 0006 phase 3 and parity matrix P1 rows: all 10 tracked `prototype/` files mapped (1 archive, 9 retire). `git ls-files prototype` returned 10 files, all listed.
* `.github/workflows/prototype-validation.yml` only validates `prototype/`; it self-skips when absent.
* `.github/rubric/artifacts.json`: only live reference is `prototype/deploy/**/*.bicep` in `infrastructure` (dead; no such dir).
* Live references found by grep: rubric README, rubric `test_prepare.py` fixtures (8 stale prototype cases already failing), capstone README, ADR 0006, parity matrix, coordinator agent, reference index. `tools/rename-zava*` mentions are dated historical records (left exact).
* Required checks: branch protection and rulesets API returns 403 (plan limit), so the required status could not be verified. Reported as owner blocker.

## Baseline (before change)

* mvp suite: 719 tests, OK (skipped=92).
* `tools/rename-zava-tests.py`: 25 tests, 7 pre-existing errors (pptx tests).
* rubric scripts: 19 pre-existing failures.
