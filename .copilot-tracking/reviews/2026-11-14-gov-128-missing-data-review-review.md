# Review: #128 AC2 and AC3

## Cycle 1 Review

Execution: Complete (self-review once). Outcome: Conformant for the Cycle 1 functional scope; hosted `src-core` `mypy` later caught one strict test-typing error (`[arg-type]`).

* Routing is deterministic, order-independent, never lowers rank and never drops a case.
* Aggregate reporting blocks on any identifier field, so individual staff surveillance cannot be reported.

## Cycle 2 Review (`src-core` `mypy` Correction, PR #1735)

* Execution: Complete (single post-implementation review pass over Cycle 2 diff and artifacts).
* Outcome: Conformant (for the Cycle 2 `mypy` correction scope; independent exact-head review, hosted CI after coordinator push, and human approval remain required).
* Assessed boundary:
  * `.copilot-tracking/research/2026-11-14-gov-128-missing-data-review-research.md`
  * `.copilot-tracking/plans/2026-11-14-gov-128-missing-data-review-plan.instructions.md`
  * `.copilot-tracking/changes/2026-11-14-gov-128-missing-data-review-changes.md`
  * `src/core/tests/test_journey_register.py`
  * `src/core/src/zava_forward/core/journey_register.py` (unchanged in Cycle 2; contract verified)
* Findings:
  * Resolved defect: `src/core/tests/test_journey_register.py` (`test_usability_rejects_small_cells_extra_keys_and_bad_values`) previously left `obs` unannotated, causing mypy invariance join to infer `bad: list[object]` at `jr.aggregate_usability(bad, 5)`. Annotating `obs: list[dict[str, Any]]` resolves `[arg-type]` cleanly without `cast` or widening `aggregate_usability`'s `Sequence[Mapping[str, Any]]` signature.
  * `RV-001` (Residual / Follow-up, Low, destination: `rpi-plan`): Wire named human reviewer and missing-data review routing into live API/queue endpoints (`Refs #128`).
  * `RV-002` (Residual / Human governance gate, Medium, destination: `rpi-research` / human decision): Obtain owner-approved minimum cell threshold (`min_cell >= 5`) and agreed AC3 user-research protocol (OD-09, OD-25) before claiming usability evidence (`Refs #128`).
* Validation verified in `src/core`:
  * `python3 -m mypy` -> `Success: no issues found in 307 source files`
  * `python3 -m ruff check .` -> `All checks passed!`
  * `python3 -m ruff format --check .` -> `254 files already formatted`
  * `python3 -m unittest tests/test_journey_register.py -v` -> `Ran 11 tests ... OK` (plus 40 related tests in `test_paired_equity.py`, `test_journey_acceptance.py`, and `test_journey_trace.py` OK)
  * Not run here: hosted CI (awaits coordinator `git push` on PR #1735) and full external RPI gate (focused tier applies to this test-annotation correction). Issue link stays `Refs #128`.
