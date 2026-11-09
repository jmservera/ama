---
title: Plan critique - #1297 correction C1
date: 2026-11-09
---

## Inputs and Boundary

* Plan: .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c1-plan.md
* Details: .copilot-tracking/details/2026-11-09/sensor-mssql-gate-1297-c1-phase-details.md
* Research: .copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c1-research.md
* Code read: tools/rpi-checks.py changed_groups, SKIP_REASONS, skipped_groups, dependencies (lines ~640-800). tools/test_rpi_checks.py, the matrix and check_skips were not supplied or read.
* Execution: Complete for supplied boundary. No SQL, docker or gates run.

## Coverage Assessment

The core fix is credible. The source confirms that `mssql` is added only for requirement or pyproject paths, or for paths containing store, schema, sql or assistants. A `"sensor" in path.lower()` condition for `project == "core"` inside the `src/<project>` branch closes the gap. The `mssql` dependency closure to project-api is already handled by `dependencies`. The alternatives analysis is sound (A over B, C and D).

## Findings

### PC-001 (Medium): The recorded skip reason becomes inaccurate

* Related: P01-T01, plan Scope (out: receipt format).
* Evidence: `SKIP_REASONS["mssql"]` reads "no store, schema, SQL or SQL dependency path changed". `skipped_groups` writes it into the selection and receipt. After the change a skipped `mssql` also means no core sensor path changed, so the recorded reason understates the rule.
* Impact: Misleading audit evidence for reviewers. Any test or receipt check that pins the string needs the update too.
* Smallest change: Add "sensor" to the reason text in P01-T01. Search for tests and verifiers that pin the string and adjust them. The receipt schema is unchanged, so this stays within scope.
* Owner: Planner. Resolving evidence: the updated T01 and a test assertion on the skipped reason. Direct correction.

### PC-002 (Medium): The receipt-selection acceptance criterion has no concrete mechanism

* Related: Acceptance criterion 2, P01-T02.
* Evidence: The details say "selection ... includes the sensor command with expected count and flag via the matrix". They do not name the matrix function, the `check_skips` interaction or the command ID, and they never state that these were read. The research verified only `changed_groups`.
* Impact: The test could degrade to a group-list assertion that does not prove the flagged command is selected. The "at most two methods" cap may not fit the stated cases.
* Smallest change: In T02, name the function and the command ID used for the assertion (expected_count 8, flagged). Cite where it was read. Specify the sensor-only `changed_groups` assertion, the negative-path assertion and the command-list assertion. Allow a table-driven `subTest`, which fits within two methods.
* Owner: Planner. Resolving evidence: the named function and command ID in T02, confirmed by a read of the matrix code. Direct correction.

### PC-003 (Low): The over-selection residual risk is not bounded

* Related: Research residual risk, C4, C6, alternative D.
* Evidence: C4 lists the suite's import closure but not every module. It names `dataset` as a possible non-sensor import and offers no check that the flagged command's imports are all matched by "sensor", store or sql. C6 asserts that api sensor modules are not imported but cites no evidence.
* Impact: A change to a non-sensor-named module imported by the suite (for example `dataset`) would still pass `--changed` while the skips are accepted. The gap persists for that class of path.
* Smallest change: Add a T02 or review step that checks the flagged command's import closure against the rule by static grep. Do not run the suite. Record the outcome, or record the accepted residual risk explicitly in the plan's Critique Disposition. Also confirm that api sensor modules are out of the core suite (C6).
* Owner: Planner. Resolving evidence: a recorded import-closure listing or an explicit risk acceptance. Direct. No user decision, because the user's direction already says "minimal fail-closed".

### PC-004 (Low): Evidence pointers depend on /tmp and an external path

* Related: Research Brief.
* Evidence: The research cites /tmp/rpi-g1297-full-1108.log and /mnt/ama-gates/... as preserved evidence. These are historical and volatile.
* Impact: The pointers cannot be re-verified later. They are not needed by P01.
* Smallest change: Label them non-load-bearing, or note the retention location. The plan already treats the receipt as historical.
* Owner: Planner. Direct.

## Verdict

Revise (minor). There are no blocking findings. The approach is sound. PC-001 and PC-002 should be folded into P01-T01 and P01-T02 before implementation. This is a planner-owned revision and needs no user decision.

* Severity counts: Medium 2, Low 2, High 0.
* Highest impact: PC-002. Owner: planner. Next action: specify the matrix assertion in T02.
* User response: not required.

## Artifacts

| Path | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c1-plan.md](.copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c1-plan.md) | Plan |
| [.copilot-tracking/details/2026-11-09/sensor-mssql-gate-1297-c1-phase-details.md](.copilot-tracking/details/2026-11-09/sensor-mssql-gate-1297-c1-phase-details.md) | Phase details |
| [.copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c1-research.md](.copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c1-research.md) | Research |

## Next Steps

Return to the planning parent. It should revise P01-T01 and P01-T02 per PC-001 to PC-003 and record the disposition, without another critique. No user action is required.
