# Plan: issue 229 data steward and digital operator screens (2026-11-01)

Task: issue-229-data-steward-screens. Research: ../research/2026-11-01-issue-229-data-steward-screens-research.md

## Phases

1. [x] Add `data-operator` screen to `role-screens.js` reusing the issue 226 helpers; no controls, no writes.
2. [x] Add `src/api/tests/test_data_operator_screen.py` (node VM, as for the asset-board test) covering both values with provenance, preserved unresolved eligibility, exception queue, event metadata and recovery caveat, no controls, empty state.
3. [x] Run unittest, ruff check, ruff format --check, mypy for `src/api`; commit, push, open PR.

## Critique (single pass, direct)

* Compatible: keep to read-only existing data; do not invent monitoring data; state Unknown with owner.
* Rejected: adding a new server role or integration endpoint (outside acceptance criteria, new authority).
