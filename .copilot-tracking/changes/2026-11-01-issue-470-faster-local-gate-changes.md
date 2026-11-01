# Changes: issue 470 faster local gate (2026-11-01)

Plan: [plan](../plans/2026-11-01-issue-470-faster-local-gate-plan.md)

## Changes

* Added research, plan, changes and review artifacts only. No source or test change.

## Validation (focused tier)

* `python3 -m unittest tools.test_rpi_checks -k changed -k partial -k resume`: 8 tests OK.
* `mypy tools/rpi-checks.py`: no issues.
* `ruff check` and `ruff format --check` on `tools/rpi-checks.py` and `tools/test_rpi_checks.py` report pre-existing findings (16 errors, 2 files to reformat) when run with the root configuration. Those files are untouched by this PR; the findings are not caused by it and were not fixed here. No CI evidence is claimed: `.github/workflows/src-ci.yml` excludes tracking-only changes, so it does not run for this PR; Ruff validation remains unavailable as passing evidence.

## Divergence

Criterion 4 (measured full-run before/after) was not measured: the owner excluded the heavy local gate for this run. No timing is claimed.

## Unmet publication prerequisite

`.github/copilot-instructions.md` requires the complete local gate (`tools/rpi-checks.py --all`) and a verified external receipt before publication, including documentation-only candidates. That gate was not run (heavy gate not authorised for this run) and no receipt exists. Publication is therefore not gate-complete; the owner must authorise the gate and receipt verification before merge.
