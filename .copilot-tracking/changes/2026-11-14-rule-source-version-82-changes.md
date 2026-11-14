---
title: Changes - rule provenance tests (#82)
ms.date: 2026-11-14
---

* `src/core/tests/test_gates.py`: added `RuleProvenanceExposureTests` (3 tests).
* No production code changes. Existing tests cover AC1 (deterministic gate outcomes with reason), AC2 (unknown never passes) and AC3 (safety release by named role and different person).
* Validation: results recorded in the review.

## Cycle 1 of 5 (Refs #82)

* `gates.py`: added registered, honestly unreviewed `TRANSITION_RULES` (technical, building, stock, capture, pause) and `RuleGatedPermissionError`, `GateResultError`, `GateResultPermissionError` that keep `GateResult.rule`.
* `store.py`, `signoffs.py`, `governance.py`: pre-transition refusals now attach a `GateRule`; `GateError.rules` holds rule records and `GateError(reasons)` still works.
* `store.py`, `workflows.py`, `grants.py`: booking, quality, hazard release and grant submission refusals keep `GateResult.rule` and text unchanged.
* `api/server.py`: 409 gains additive `rules`, 403 gains additive `rule`; existing fields unchanged.
* Tests: `TransitionRuleAttachmentTests` added; `test_gates` registry assertion extended.
* Validation: focused core tests (309, one assertion updated), api impacted tests (632 OK), `ruff check`, `ruff format --check`, `mypy` clean in core and api. No full discover run.
