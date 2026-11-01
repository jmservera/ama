# Plan: issue 167, per-record is_synthetic on the scale fixture

Research: `.copilot-tracking/research/2026-11-01-issue-167-scale-fixture-is-synthetic-research.md`

## Phases

* [ ] 1. `scale_fixture.py`: add `is_synthetic=True` to `homes()` and `events()`; bump `VERSION` to 1.3.0.
* [ ] 2. Tests: add per-record assertion over homes, households and events in `src/core/tests/test_synthetic_determinism.py`; re-pin homes/events goldens.
* [ ] 3. Docs: update the coverage-baseline paragraph in `docs/reference/research/retrofit-synthetic-data/README.md` and the `1.2.0` mention in `src/core/README.md`; append `docs/reference/log.md`.
* [ ] 4. Validate: core tests for synthetic modules plus agents/api users of `scale_fixture`; ruff check, ruff format --check, mypy on core.
* [ ] 5. Commit, push, PR.

## Critique (single pass, direct)

* Compatible: bump version because bytes change; do not hand-edit goldens blindly, recompute from generator.
* Risk: sensors.csv/readings goldens may shift if they hash home dicts; the tests will show it, re-pin only if justified.
* Closure: PR uses `Refs #167` because owner confirmation of the mapping/deferrals is not evidenced.
