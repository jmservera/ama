# Changes: issue 167, per-record is_synthetic on the scale fixture

Plan: `.copilot-tracking/plans/2026-11-01-issue-167-scale-fixture-is-synthetic-plan.md`

* `src/core/.../synthetic/scale_fixture.py`: `is_synthetic=True` on homes and events; VERSION 1.3.0.
* `src/core/tests/test_synthetic_determinism.py`: new per-record test; homes/events goldens re-pinned (households and sensor goldens unchanged).
* Version label 1.3.0 in `src/agents/evals/registry.json`, `cohort_manifest_draft.json`, `src/api/checks/progress_browser_check.py`, `src/api/README.md`, `src/core/README.md`.
* Docs: retrofit-synthetic-data README coverage section and `docs/reference/log.md`.

## Validation (focused tier)

* core: synthetic determinism, provenance, sensor backfill/plausibility, coverage, needs-inventory tests: 53 OK. ruff check and mypy clean.
* agents full unit suite: 123 OK. api progress dashboard tests: 45 OK.
* `ruff format --check`: scale_fixture.py and progress_browser_check.py were already unformatted at baseline; not reformatted (unrelated).
* Local gate skipped by owner direction; CI is the evidence.

## Divergences

None.
