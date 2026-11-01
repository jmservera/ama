# Plan: issue 608 remaining criteria

* Scope: no source change; criteria 1 and 2 already delivered by #610 and re-verified. Criterion 3 cannot be delivered under the focused-validation constraint.
* Phase 1: re-run `python3 -m unittest tools.test_rpi_checks`, ruff check and ruff format --check on the touched tool files. mypy is not applicable (no project source touched).
* Phase 2: record research, plan, changes and review evidence under .copilot-tracking/*/2026-11-01/.
* Phase 3: open a PR using `Refs #608` naming criterion 3 as unmet.
* Critique (single pass): compatible. Avoid a closing keyword because criterion 3 is unproven; do not fabricate a gate receipt or skip browser/SQL.
