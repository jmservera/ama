<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resident sensors

## Metadata

* Task ID: 468; parent issue: 466.
* Critique date: 2026-10-27.
* Plan: .copilot-tracking/plans/2026-10-27/resident-sensors-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md
* Critique execution status: Complete.
* Assessment: one independent final-candidate critique; no implementation or further agents.

## Inputs and Criterion Boundary

* Caller requirements: own-home generated synthetic temperature/humidity gauges and accessible history; existing resident principal/view isolation; source-only SQL view edits, never SQL execution; no private datasets, .env, secrets, verifier file, Azure, deployment, MAX_MAPPINGS or header changes.
* Publication decisions: parent feat/resident-interactive, Refs only, no force push or merge. Affected tests, changed-Python Ruff/mypy and local Playwright replace the full two-hour gate for this task.
* Supplied research: .copilot-tracking/research/2026-10-27/resident-sensors-research.md, especially C1-C7/W1 and its absent-table and historical-data limitations.
* Source evidence: infra/sql/resident-showcase.sql; infra/scripts/resident_showcase_sql.py; src/core/src/zava_forward/core/resident_showcase.py; src/core/src/zava_forward/core/resident_showcase_sql.py; src/core/src/zava_forward/core/synthetic/sensor_backfill.py; src/core/src/zava_forward/core/synthetic/sensor_stock.py; src/core/src/zava_forward/core/synthetic/sensor_faults.py; support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py.
* Existing validation and presentation evidence: src/core/tests/test_resident_showcase_sql.py; src/core/tests/test_resident_showcase.py; src/api/tests/test_resident_demo_api.py; src/api/src/zava_forward/api/resident_demo/app.py; src/api/src/zava_forward/api/resident_demo/web/demo.js; docs/reference/research/ux/wcag-conformance-baseline.md.
* Repository context: original/addendum, knowledge-base index/memory and housing-association primer. Memory is context, not evidence. Issue #468 title/body were inspected read-only.
* Assessment boundary: P01-P03, their dependency ordering, requirements, acceptance criteria, bounded test budget, source feasibility and prohibited-operation safeguards. This assessment does not establish SQL compilation, deployed permissions, populated history, browser behaviour or accessibility conformance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C3; generated stock and provenance | Partial | Generator and stock anchor exist; exact register/reading ownership and provenance predicates need PC-001. |
| C4-C5; signed-session authority | Covered | Existing fixed case query and fresh authorisation support the proposed extension without browser-selected IDs or new grants. |
| C7; optional source SQL projection; P01-T01 | Partial | Conditional dynamic view creation is feasible, but its source contract must preserve exact home ownership and explicit nullable measurements. PC-001/PC-002. |
| Latest recorded values, bounded history, UTC | Partial | Forty-eight stored rows and chronological output are specified; numeric validity versus malformed-row denial is unresolved. PC-002. |
| Empty, missing, invalid, out-of-range and fault states | Partial | Required in acceptance criteria but not mapped consistently to parser and UI outcomes. PC-002. |
| Native meters, separate SVGs and equivalent table; P02-T01 | Covered with correction | Suitable static patterns, labels, units and keyboard disclosure; fault-state behaviour depends on PC-002. |
| Own-home and forged/revoked-session regressions | Partial | Correct test categories; add adversarial register/reading mismatch cases under PC-001. |
| Local unit discovery, Ruff/mypy, Playwright; P03-T01 | Partial | Scope is appropriate, but ambient SQL opt-ins can violate the no-execution boundary. PC-003. |
| No private data, secrets, deployments or unrelated edits | Covered with correction | Source-generated fixtures and constructed reader are suitable; make test-process isolation explicit under PC-003. |
| Stacked branch, Refs only, independent Review, no full gate | Covered | Explicit caller decisions are preserved; no recommendation to expand authority or validation scope. |

## Verdict

* Verdict: Revise.
* Rationale: the architecture is credible and does not require an operational SQL step. Three directly correctable planning gaps affect the core ownership invariant, required unavailable-value behaviour and the prohibition on SQL execution. None requires a divergent user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify the complete exact-match ownership and synthetic-provenance invariant

* Related IDs: C1-C5/C7, P01-T01, own-home isolation acceptance criteria.
* Evidence: .copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md:20-31 says readings are joined through the register and case stock ID, but does not state all required equalities. src/core/src/zava_forward/core/synthetic/sensor_backfill.py:47-53 stores home_id and source_type independently in both tables, without a foreign key enforcing agreement. src/core/src/zava_forward/core/synthetic/sensor_stock.py permits case-sensitive synthetic IDs without imposing a common SQL collation. infra/sql/resident-showcase.sql already uses binary collation for its existing identity comparisons.
* Concern: joining a register row to the case home and readings only by sensor_id does not itself prove the reading's own home_id agrees. The plan's internal home validation is useful, but it does not explicitly identify which source identity survives projection or require independently matching register and reading identities. Database-default comparison can also collapse distinct case-sensitive stock IDs. A SYNTHETIC reading alone does not establish a synthetic register row.
* Impact: inconsistent or case-colliding stored identities can select another home's values or attach synthetic provenance to the wrong register association. A well-formed two-resident fixture would not expose this.
* Smallest useful change: state that sensor_id links the tables, both register.home_id and reading.home_id must match the case's home.stock_id using an explicit case-sensitive/binary comparison, both source_type values must be SYNTHETIC, and the reading's original home identity is retained internally for exact Python validation. Define fail-closed behaviour for mismatches without exposing IDs. Add source-query assertions and adversarial mocked rows for mismatched register/reading homes, case-distinct homes and non-synthetic provenance.
* Action owner: planning parent, correcting P01-T01.
* Exact resolving evidence: revised phase details state the invariant and named negative cases; implementation Review can trace each predicate and internal validation to corresponding source-text/domain/API assertions, with zero foreign values or internal identifiers in resident output.
* Decision route: direct planner correction. Strict own-home synthetic isolation is already required; no user response is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Resolve malformed-envelope denial versus unavailable-measurement presentation

* Related IDs: C1, P01-T01, P02-T01, missing/invalid/fault acceptance criteria.
* Evidence: .copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md:27-28 requires finite values and says malformed projection denies; lines 42-45 require unavailable-value presentation and plot gaps. src/core/src/zava_forward/core/synthetic/sensor_backfill.py:41 defines synthetic exercise bounds, lines 50-53 allow nullable numeric measurements and injected_fault, and lines 117-127 emit OUTLIER/STUCK labels. src/core/src/zava_forward/core/resident_showcase.py:119-162 currently treats malformed rows as denied.
* Concern: the plan does not distinguish an invalid measurement that must remain visible as an explicit unavailable/fault state from an invalid ownership/JSON envelope that must deny. Rejecting every null, out-of-range or fault-labelled value makes the required sensor states unreachable; accepting them as ordinary finite values misrepresents faults. The nullable SQL-to-JSON representation is also unspecified: default FOR JSON omission of null properties can turn a legitimate missing measurement into a malformed strict row.
* Impact: one missing channel can remove the whole resident page, or faulty data can appear as a normal gauge/line point. The latest-value acceptance criterion can also be defeated by silently substituting an older valid value for a faulty latest observation.
* Smallest useful change: add a compact outcome contract for structural/ownership/provenance failure versus null measurement, non-finite/out-of-range value, recognised fault and unknown fault. Preserve authorised timestamps and per-channel unavailable reasons where appropriate; deny untrusted envelopes. Specify explicit JSON null preservation or an equally strict optional-field contract. Reuse generator bounds only as fictional validation limits, not health thresholds; define non-evaluative meter min/max without safe/unsafe colouring. Latest means the latest stored observation, including its unavailable state, not an undisclosed fallback. Add browser cases for a valid sibling channel, latest STUCK/OUTLIER, missing value and singleton history, checking matching table text and plot gaps.
* Action owner: planning parent, correcting P01-T01/P02-T01 and their acceptance/test notes.
* Exact resolving evidence: one explicit state/outcome table in phase details, agreed JSON nullable shape, and named domain/browser assertions showing unavailable latest readings do not become zero, normal meters or silently older readings; structural ownership failures remain denied.
* Decision route: direct planner correction. Existing caller requirements already require explicit fault/missing states and no safety judgement.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Force integration opt-ins off before full test discovery

* Related IDs: P03-T01, no SQL execution requirement.
* Evidence: .copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md:61 calls for core/API unit discovery without process-environment safeguards. src/core/tests/test_resident_showcase_sql.py:28-31 enables integration tests when ZF_TEST_MSSQL=1 and ZF_SQL_SERVER is loopback. Its SqlBoundaryTests setup/teardown at lines 177-228 creates and drops a database and executes the rendered DDL.
* Concern: discovery is not guaranteed to be SQL-free solely because the new tests use fake cursors. Inherited integration opt-ins can run existing SQL-writing tests, contrary to the task's explicit prohibition.
* Impact: the validation step can execute SQL and mutate a local database even though the implementation remains source-only.
* Smallest useful change: require a controlled test subprocess environment that explicitly sets ZF_TEST_MSSQL=0 and disables other integration/deployment opt-ins relevant to the selected suites before imports/discovery. Do not inspect or print existing credential values or load .env. Keep browser startup on the constructed reader, not the production SQL-configured entry point. Record opt-in SQL tests as intentionally unrun, separately from passed source/mocked tests.
* Action owner: planning parent, correcting P03-T01.
* Exact resolving evidence: phase details include the explicit no-SQL discovery invocation/process policy; changes evidence records that policy and expected integration skips, with only constructed-reader loopback HTTP/browser execution.
* Decision route: direct planner correction. No permission for SQL execution is needed or sought.

## Strengths and Residual Risk

* The existing same-owner view chain can expose stored history without granting the resident principal direct sensor-table rights. Conditional dynamic CREATE OR ALTER VIEW can avoid binding absent tables; both branch outputs must retain an identical typed column contract. This is feasible source work, not an instruction to apply it.
* The plan correctly avoids equating a case ID with a stock home ID, generating readings during requests, inventing live measurements or expanding principal authority.
* Separate static unit-labelled charts, native meters only for valid readings, and a native details/table alternative are an appropriate implementation direction. Keyboard checks do not imply that a non-interactive meter must become a tab stop.
* Existing ownership/session machinery can remain intact. No header edit, mapping-cap change, new chart dependency or operational safety threshold is needed.
* SQL compilation, optional-table branch execution and ownership-chain behaviour remain unverified operational dependencies because SQL execution is explicitly excluded. Source/mocked tests must not be reported as SQL integration evidence.
* Historical synthetic labels and explicit recorded timestamps address the distinction between requested current gauges and non-live stored observations.
* Human screen-reader acceptance remains separate from focused engineering checks, as the plan already records.

## Questions or Blocking Evidence Gaps

* None requiring a user decision. The supplied sources support direct correction of all findings.
* Do not broaden this task to fault-packet evaluator truth or all generator schema variants. The supplied baseline SQL schema contains injected_fault; any unsupported optional schema must be documented rather than treated as populated live evidence.

## Limitations

* No implementation, tests, SQL commands, browser session, deployment, private dataset, verifier file, secret or .env was accessed or executed for this critique.
* Current Web Interface Guidelines were considered through supplied W1, not independently re-fetched. This is a plan critique, not a fresh UI rules audit.
* Source-only review cannot prove dynamic T-SQL compilation or populated deployment behaviour. The caller's no-SQL constraint takes precedence; this limitation is not a request for cloud or database access.
* The worktree already contained the parent-created untracked planning/research/session artifacts. They were not changed. Only this critique artifact was added.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: add the exact register/reading/case ownership invariant and negative cases, then directly resolve PC-002/PC-003 in the same plan/detail revision.
* User response required: no.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/resident-sensors-plan.md](.copilot-tracking/plans/2026-10-27/resident-sensors-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md](.copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md) | Assessed implementation and verification details |
| [.copilot-tracking/research/2026-10-27/resident-sensors-research.md](.copilot-tracking/research/2026-10-27/resident-sensors-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/reviews/plans/2026-10-27/resident-sensors-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/resident-sensors-plan-critique.md) | Complete independent critique |

## Next Steps

The active planning parent should disposition PC-001 through PC-003 directly,
revise the plan/details and finalize without another critique. Preserve this
original outcome, then continue the confirmed native RPI loop with implementation
and its independent Review. No user action is required.
