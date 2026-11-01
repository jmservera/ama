# Plan: issue 466 resident gauges and assistant evidence slice, 2026-11-01

* Research: [research](../research/2026-11-01-issue-466-resident-sensor-gauges-research.md). Scope is tight to the acceptance criteria; no source change is justified.

## Phases

* [x] Phase 1: record current-main verification (tests, ruff, mypy) in a dated evidence trail.
* [x] Phase 2: append a knowledge-base log entry in `docs/reference/log.md` stating criteria status and that criterion 1 stays unmet.
* [x] Phase 3: commit, push and open a PR with `Refs #466` naming criterion 1 (no closing keyword).

## Critique (single pass)

* Execution: executed inline. Verdict: proceed.
* Disposition: adding new gauge or assistant code would exceed the criteria and risk the isolation guarantees; rejected. Not claiming closure: owner confirmation is a human approval gate.
* Validation tier: focused tests plus ruff and mypy for core and api; Policy conflict: `.github/copilot-instructions.md` requires the complete local gate even for documentation-only candidates while `src/README.md` permits focused checks. The complete local gate is not run and remains unresolved publication work for owner reconciliation; CI does not replace it.
