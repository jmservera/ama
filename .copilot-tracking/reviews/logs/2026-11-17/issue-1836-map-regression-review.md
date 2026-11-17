<!-- markdownlint-disable-file -->
# RPI Review: Map count and tile-fallback regression (issue 1836)

## Metadata

* Task ID: issue-1836-map-regression
* Review date: 2026-11-17
* Compared artifacts: research, plan, phase details, plan critique, changes record, state file (paths under .copilot-tracking/)
* Boundary: committed test-only change plus evidence at the local candidate head

## Execution and Outcome

* Review execution: Complete (single pass, read-only, no subagents)
* Outcome: Conformant with justified divergence

## Findings

### RV-001 (Low): unconditional pass line in the focused check

The line "exact zero count is independent of the tile fallback" calls `check(..., True)`. The real assertions are the preceding `expect` calls, which abort on failure, so no weakness in detection exists, but the constant PASS reads as an assertion. Destination: distinct follow-up (rpi-implement), tidy the label.

### RV-002 (Low): full src/api unit discovery not completed

Discovery exceeded 700 s and was stopped. Targeted map modules (32 tests), the new tests, ruff, strict mypy and the Core scenario_manifest and needs_inventory tests passed. Justified by the FOCUSED tier; hosted CI should cover the full suite. Destination: coordinator hosted CI.

### RV-003 (Info): default-font baseline failure is environmental

At 390x568 the container's system-ui fallback font gives a 0.17px overflow on main and on the candidate. Runs used a Liberation Sans fontconfig override and say so. No check was relaxed. Destination: follow-up (rpi-research) on sub-pixel sensitivity.

### RV-004 (Info): witness refusal

Witness seq 2 refused research-open because no research artifact existed; disclosed in state and research, fixed prospectively at seq 3. Destination: none.

## Requirement Check

* Old locator reproduced as a labelled intentional demonstration in both tile states: met.
* Exact "0 homes shown" with an unambiguous locator; fallback visible on abort, hidden on success: met.
* Fails if the old selector returns: met (mutation evidence for check and static guard; both reverted, hashes identical).
* No external map service or resident data: met (tile host fulfilled or aborted, all other requests aborted and recorded).
* Full harness with axe, no skips: met (332 PASS, 0 FAIL, 0 skip, with font qualification).
* Test-only, scenario recipe bytes untouched: met.

## Routing

* Defects: none.
* Decision gaps: none.
* Residual work: RV-001, RV-002 (hosted CI), follow-ups in the changes record. Independent exact-head review and hosted checks remain pending.
