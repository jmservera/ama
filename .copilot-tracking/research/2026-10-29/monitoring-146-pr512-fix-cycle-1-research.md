<!-- markdownlint-disable-file -->

# Task Research: monitoring-146-pr512-fix-cycle-1

Date: 2026-10-29
Researcher: RPI Agent / rpi-research
Status: Complete

## Research Brief

* Topic: Refs #146, PR #512, fix cycle 1; absent-table workbook fallback.
* Purpose/audience: Give the implementation and reviewer a bounded correction and regression contract.
* Scope: Two KQL queries in infra/monitoring-workbook.json and their existing Python shape test.
* Non-goals: Azure operations, deployment, issue closure, unrelated monitoring gaps, latest.json edits, push.
* Criteria: Bare AppRequests/AppAvailabilityResults union operands; typed empty fallback; projection after union; regression rejects old shape; existing infra/monitoring tests, valid JSON and changed-Python Ruff checks.
* Requested outputs: Dated Research, Plan, Implement and Review evidence and local commit with required trailer.
* Output mode: convergence.

## Research Parameters

* Questions: Which test owns this contract? Does moving projection preserve downstream schemas and insufficient/null behavior?
* Internal candidates: infra/monitoring-workbook.json, infra/tests, monitoring runbooks, prior #146 evidence.
* External candidates: None; supplied finding defines the correction, and no service execution is authorized.
* Posture: focused (default for named source and supplied failure).
* Evidence root: .copilot-tracking/.
* Edits during research: Evidence/state only.
* Completion basis: In-scope evidence coverage with no material unresolved implementation question.

## Extension Registry and Provenance

* Selected: Repository instructions (all files), RPI research protocol, branch/commit safeguards.
* Selected later: rpi-plan, rpi-implement, rpi-review for explicitly requested full loop.
* Skipped: Web-design skills; this is KQL and source-shape Python, not web UI.
* Research specialists: Inline investigation; single tightly coupled trace needs no delegation.

## User Participation and Research Decisions

User explicitly requested the complete loop, initial pull/rebase, Refs only, no Azure, local commit/no push. No interactive clarification is needed or available. Full-loop execution is automatic for this bounded task; no child task will begin without selection.

## Direction Controls

* Preserve the existing active feat/monitoring-146 branch and PR #512.
* Preserve existing evidence and latest.json; no source changes during Research.
* Validate source behavior without claiming Azure/Kusto execution.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Where are both affected query sources and their regression test? | straightforward | answered |
| Q2 | Which invariants and validation commands cover the correction? | straightforward | answered |

## Prior Knowledge Gate

The supplied finding is a hypothesis to verify against source. Initial git pull --rebase succeeded with "Already up to date"; worktree was clean, branch feat/monitoring-146 matches open PR #512 targeting main. Prior #146 artifacts exist and will remain unchanged.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspected the workbook, infra test inventory, component commands and prior evidence inline. Both sources have the reported parenthesized projected operand (C1). The tracked Python tests contain no workbook/query-shape regression (C2).
Reflection: Add a focused unittest in the existing infra test directory rather than modify unrelated secret or Bicep policy tests.

#### Wave 2: Deeper

Prioritized schema and downstream behavior. Requests need datetime/string/int/bool/real fields; availability needs the same except DurationMs (C1). The aggregation and null-metric expressions follow the samples binding and can remain byte-identical.
Reflection: Assert the exact typed datatable, bare table operand and post-union projection as the initial statement for each panel; preserve the rest of each query.

#### Wave 3: Contrarian

Challenged a weaker test that merely checks isfuzzy=true or the presence of a datatable: both already exist in the defective form, so that assertion would miss the failure. No tracked existing workbook test was found using rg and git grep; add one rather than claim an update (C2). Keep schema/query/permission failures Blocked as documented (C3). No live Azure binding proof is claimed.
Reflection: A red-before-green source-shape test proves rejection of the old form without a cloud query or pretending to execute KQL.

#### Parent Synthesis and Disposition

* Accepted C1/C2: Change both union sources, add a dedicated parameterized-by-subTest workbook regression, and demonstrate failure against the unchanged source before the fix.
* Accepted C3: Retain all data-quality, sampling, time-window, null and status logic, with source-only validation language.
* Rejected: Test only keyword presence; it passes on the defect.
* Deferred: Live Kusto/portal execution and historical operational findings; explicitly outside caller authorization.

#### Cycle Re-entry Evaluation

No additional cycle needed: both questions answered, exact source shape and regression oracle identified; additional discovery would not change the bounded correction.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Both union operands currently project inside a parenthesized table expression. | infra/monitoring-workbook.json:41,55 | High |
| C2 | No tracked workbook/query-shape test exists; infra tests are unittest-based, with policy compilation performed offline. | infra/tests/test_bicep_policy.py:1,94; infra/tests/test_governance.py:1 | High |
| C3 | Workbook explicitly distinguishes absent/empty samples from schema/access/query failures; existing monitoring delivery is source-only. | infra/monitoring-workbook.json:32; infra/README.md:44 | High |
| C4 | Prior local monitoring validation uses policy, IoT, container, governance and secret tests; full publication gate is separate. | .copilot-tracking/changes/2026-10-29/monitoring-146-rebase-changes.md:100 | High |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Implication |
| --- | --- | --- | --- |
| Q1 | Correct the two initial samples bindings and add infra/tests/test_monitoring_workbook.py. | C1, C2 | No unrelated test refactor needed. |
| Q2 | Exact source-shape prefix plus red/green execution; existing infra group, JSON, isolated Ruff check/format. | C1-C4 | Local validation suffices for requested source correction, not operational acceptance. |

## Alternatives and Decision State

Selected: Bare table union operand alongside the existing typed datatable, with project applied after the union. This directly follows the owner-selected correction and preserves downstream logic (C1).
Rejected: Nested project inside a fuzzy source; binding can fail before source resolution, as reported by the supplied Copilot finding.

## Open Questions, Risks, and Residual Uncertainty

No Azure execution will be performed; local string checks cannot prove live Kusto binding.

## Planning Readiness

Ready. Research disposition: executed. Hand off C1-C4 to Plan; no implementation blockers.

## Current Decisions and Potential Next Research

No further in-scope research. Named-human approval, live verification and all historical operational findings remain open, not resolved here.

## Artifact Self-check

Brief, extensions, three ordered inline waves, provenance, decisions and limits recorded. No source was changed during Research.

## Sources

No external sources used.
