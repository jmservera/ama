# Changes: #128 AC2 and AC3

## Cycle 1: Missing-Data Human Routing and Aggregate-Only Usability

* `src/core/src/zava_forward/core/journey_register.py`: reviewer assignment, `unassigned` and `dropped` counts, stricter incomplete-appointment detection, `aggregate_usability`.
* `src/core/tests/test_journey_register.py`: tests covering reviewer routing, aggregate usability, small-cell suppression, identifier rejection, extra keys, non-finite/bad values, and appointment-history normalisation.
* Validation: `python3 -m ruff check` pass; `ruff format --line-length 100 --check` pass; focused unittest cases pass (journey_register, paired_equity, journey_acceptance, journey_trace).
* Not run: full local RPI gate, hosted CI. Not pushed. `role-screens.js` unchanged.

## Cycle 2: `src-core` Strict `mypy` Fix (PR #1735)

* `src/core/tests/test_journey_register.py`: annotated `obs: list[dict[str, Any]]` in `test_usability_rejects_small_cells_extra_keys_and_bad_values` so unpacked observation lists mixed with invalid-value dicts satisfy `Sequence[Mapping[str, Any]]` under strict `mypy` (`[arg-type]`) without widening production types.
* Validation (from `src/core`):
  * `python3 -m mypy`: pass (0 errors across 307 source files).
  * `python3 -m ruff check .`: pass (0 errors).
  * `python3 -m ruff format --check .`: pass (0 formatting diffs).
  * `python3 -m unittest tests/test_journey_register.py -v` (in isolated worktree venv resolving `src/core/src` ahead of the shared host install, and with `PYTHONPATH=src`): pass (11 tests OK).
* Validation tier: focused tier (test-only strict type annotation fix inside `src/core/tests/test_journey_register.py`; no infrastructure, SQL, workflow, dependency, or security-control boundary modified). Not pushed (`git push` is coordinator-gated).
