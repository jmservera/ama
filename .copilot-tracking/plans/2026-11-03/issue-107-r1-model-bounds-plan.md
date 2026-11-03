<!-- markdownlint-disable-file -->
# Issue 107 R1 model bounds: plan

Details: [details](../../details/2026-11-03-issue-107-r1-model-bounds-details.md). Branch feat/issue-107-r1, target main.

## Phases

* [x] Phase 1: add `model_bounds()` and constants in `core/assistants.py`; expose `model_bounds` in the registry view for every assistant (not in `REGISTRY`, so hashes and proposal identity are unchanged).
* [x] Phase 2: tests: API tests for stated bounds, attempt ceiling and claims stopping at the bound for all five; worker test of one depth-1 call per task per capability.
* [x] Phase 3: document in `src/agents/README.md`; keep unmet criteria stated.
* [x] Phase 4: focused validation (unittest, ruff, mypy), commit, push, PR with `Refs #107`.

## Out of scope

Gate, benchmarks, full suites, prices or budgets, release approvers, serving attestation, forecasts, attribution.
