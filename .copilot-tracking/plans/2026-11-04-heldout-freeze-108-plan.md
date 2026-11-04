# Plan: issue 108 held-out freeze check (2026-11-04)

Research: [research](../research/2026-11-04-heldout-freeze-108-research.md). Details: [details](../details/2026-11-04-heldout-freeze-108-details.md).

* [x] Phase 1: add `heldout_freeze.check_freeze` with gap list and digest.
* [x] Phase 2: behavioural tests, README section.
* [x] Phase 3: focused validation (unit, ruff, mypy); no gate, benchmark or full suite.

Critique (single pass, direct): keep pure and offline; do not tick any criterion; approval binds to a digest that excludes the approval field; leakage needs explicit lists, even empty. All applied.

Stacked later slices: report integration; five-assistant coverage matrix.
