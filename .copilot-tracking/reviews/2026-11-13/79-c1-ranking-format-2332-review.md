# Review: C1 ranking publication review fixes (#79)

Review executed once. Tier: Focused (test and formatting only; no workflow, dependency, deployment, SQL schema or security-control change). Venv: pip `/tmp/venv-79-c1` (ruff 0.17.5, mypy), removed afterwards. Boundary: working tree on top of 7fe6e08e6.

## Findings addressed
1. Blocking CI format failure: fixed by `ruff format`; `--check` now passes.
2. SQL-backed store path: new test uses a real SQLite `SqlStore` selected via `ZF_STORE=sqlite`. MSSQL itself remains unproven offline (inherits `SqlStore`); recorded, not claimed.
3. Details artifact: added `.copilot-tracking/plans/2026-11-13/details/79-c1-ranking-format-2332-details.md`.

## Commands run and output
* `ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py`: `1 file already formatted`
* `ruff check --isolated --line-length 100 infra/tests/test_bicep_policy.py`: 1 error, `RUF100` unused `noqa: S307` at line 168. Same error on `origin/main`'s copy (ruff 0.17.5 default set differs from CI); not from this change.
* CI selection `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py`: `All checks passed!`
* `python3 -m unittest infra/tests/test_bicep_policy.py`: `Ran 62 tests ... OK` (re-run on both new and stashed base). One earlier run reported `errors=1` with output not retained, and it did not reproduce in two further runs; treat as an unexplained transient.
* `src/orchestrator` `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q`: `Ran 126 tests ... OK` (125 plus the new one). Without that PYTHONPATH, 4 modules fail to import (`dataset`, fixtures); that is an environment gap, not a regression.
* `src/orchestrator` `ruff check . --exclude build`: `All checks passed!`; `ruff format --check src tests`: `14 files already formatted`; `mypy`: `Success: no issues found in 18 source files`.
* `src/core` `python3 -m unittest tests.test_scenario_manifest tests.test_needs_inventory`: `Ran 19 tests ... OK`.

## Not run
Hosted CI, the complete local gate, `az bicep build` (no template change), MSSQL integration.

## Outcome
Conformant for the three review findings. #79 criteria 3 and 4 remain open (`Refs #79`); human and hosted approvals still required.
