---
title: "Task Research: 111-sensor-reproducibility-2142-c2"
description: "Cycle-2 CI fix for pinned sensor MSSQL test list in tools/rpi-checks.py and tools/test_rpi_checks.py (Refs #111, PR #1741)"
ms.date: 2026-11-14
---

| Field | Value |
| --- | --- |
| Date | 2026-11-14 |
| Researcher / agent | rpi-research (RPI Agent) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-c2-research.md |

## Research Brief

* What to research: Why hosted CI job `src-namespace` on PR #1741 (`feat/iot-111-sensor-reproducibility-2142`) failed `test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py`, how `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` governs both `project-core` discovery skips and `mssql` local-gate execution checks, and whether any secondary dependencies, test assertions, or CI selector rules are affected.
* Why it matters: Cycle 1 (`79b9cd1be`) added `RetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in `src/core/tests/test_sensor_analysis_store.py`. Because `MssqlRetainedAnalysisTests` in `src/core/tests/test_sensor_analysis_mssql.py` subclasses `RetainedAnalysisTests`, the new test automatically entered the live SQL sensor suite without being added to `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py`, breaking the `src-namespace` contract check and the local gate's skip/count pin.
* Audience or intended use: Cycle-2 planning, implementation, and review on `feat/iot-111-sensor-reproducibility-2142` (targeting `feat/demo-164-chat-grounding-provenance-0900`).
* Scope: `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `tools/ci-affected.py`, `tools/test_ci_affected.py`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_mssql.py`, and `.github/workflows/src-ci.yml`.
* Non-goals: Altering `src/core` production sensor logic delivered in Cycle 1, modifying GitHub Actions workflow YAML, running live Azure resources, or pushing to remote.
* Criteria: `test_pinned_sensor_mssql_tests_match_the_real_suite` and all tests in `tools/test_rpi_checks.py` and `tools/test_ci_affected.py` pass, `ruff` and `mypy --strict` pass on `tools/rpi-checks.py` and `tools/test_rpi_checks.py` matching `.github/workflows/src-ci.yml`, and MSSQL compatibility of the inherited test is verified by inspection.
* Requested outputs: Dated Cycle-2 primary research artifact with convergence recommendation for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | Q1-Q3 below |
| Codebase scope | `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `tools/ci-affected.py`, `tools/test_ci_affected.py`, `src/core/tests/test_sensor_analysis_*.py`, `.github/workflows/src-ci.yml`, `src/README.md` |
| External scope | none (bounded internal repository failure with exact CI traceback supplied) |
| Initial internal candidate areas | `tools/test_rpi_checks.py:461-487`, `tools/rpi-checks.py:184-216` |
| Initial external candidate areas | none |
| Research posture | focused |
| Posture provenance | default (bounded CI fix with named files and exact failure output) |
| Explicit limits / deadline | Commit cleanly on `feat/iot-111-sensor-reproducibility-2142`; do NOT push |
| Posture-specific completion basis | focused scope and materiality |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | Preserve Cycle-1 `src/core` behavior and Cycle-1 RPI artifacts; classify gate-tool edit impact accurately under repository two-tier validation rules |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` | `applyTo: "**"` matches `tools/` and `.copilot-tracking/` | Requires knowledge-base index check, validation-tier impact classification for gate-tool edits, privacy-safe Git author config, `Refs #111` discipline, and Markdown style | Selected: mandatory repository governance |
| Skill | `python-foundational` | Python unit testing and strict typing | Standard-library `unittest`, `ruff`, and `mypy --strict` conventions | Skipped: `src-ci.yml` and `tools/rpi-checks.py` already specify exact `ruff` and `mypy --strict` invocations |
| Research specialist | `hve-core-all:rpi-researcher` | General internal research worker | Delegated subagent lane artifact | Skipped: inline fallback used because all relevant files fit direct inspection in <=5 reads |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
| --- | --- | --- | --- |
| Intake | Non-interactive Cycle-2 invocation with exact CI failure, target files, validation commands, branch, and no-push rule | No interaction needed | Proceed in confirmed automatic child loop (`parent_task`: `111-sensor-reproducibility-2142`) with focused posture |
| Direction change | None; reproduced failure matches caller problem statement verbatim (`102/103` pass, 1 failure at `tools/test_rpi_checks.py:474`) | No interaction needed | Keep scope tightly focused on `SENSOR_MSSQL_REQUIRED_TESTS` and gate contract tests |
| Convergence | Single three-wave cycle answered Q1-Q3 with primary codebase and test-execution evidence | No interaction needed | Advance automatically to `rpi-plan` |

## Scope and Success Criteria

* Scope: Pinning `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in `tools/rpi-checks.py` (`SENSOR_MSSQL_REQUIRED_TESTS`) and strengthening or verifying `tools/test_rpi_checks.py` and `tools/test_ci_affected.py`.
* Assumptions: `MssqlRetainedAnalysisTests` intentionally inherits every `test_*` method on `RetainedAnalysisTests` so retained SQLite tests also execute against disposable SQL Server when `ZF_SENSOR_MSSQL=1`.
* Success criteria:
  * Every research question is answered with `C#` codebase evidence (`path:line`).
  * Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian are completed in order.
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Validation-tier classification for editing `tools/rpi-checks.py` is explicitly established from repository rules.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect `tools/test_rpi_checks.py` around line 474 and `tools/rpi-checks.py`; update pinned sensor MSSQL test list so `test_pinned_sensor_mssql_tests_match_the_real_suite` passes with `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only`; record Cycle-2 fix in `.copilot-tracking/`; run `test_rpi_checks.py`, `test_ci_affected.py`, `ruff`, and `mypy`; commit cleanly without pushing.
* Inferred research questions: Does `SENSOR_MSSQL_REQUIRED_TESTS` drive downstream skip tolerances, SQL test counts, or direct-dependency sets, and is the new inherited test SQL-compatible with `MssqlRetainedAnalysisTests` on SQL Server?
* Caller constraints and non-goals: Do not push; preserve Cycle-1 deliverables and commit cleanly on `feat/iot-111-sensor-reproducibility-2142`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
| --- | --- | --- | --- |
| narrow | Scope code fix to the pinned sensor MSSQL test contract in `tools/rpi-checks.py` (and `tools/test_rpi_checks.py` if needed) | Caller prompt | Keep `src/core` untouched unless contrarian SQL check finds an incompatibility |
| exclude | Do NOT push to remote | Caller prompt | Complete local validation and clean commit only; keep full live-SQL external gate as pre-merge follow-up |

## Research Questions

| # | Sub-question | Type (depth / breadth / straightforward) | Priority | Status |
| ---: | --- | --- | --- | --- |
| Q1 | How does `test_pinned_sensor_mssql_tests_match_the_real_suite` compute the expected sensor MSSQL test set, and where is the pinned tuple defined and consumed? | straightforward | H | answered |
| Q2 | What downstream effects does adding `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` to `SENSOR_MSSQL_REQUIRED_TESTS` have on `SENSOR_MSSQL_DISCOVERY_SKIPS`, `SENSOR_MSSQL_DIRECT_DEPENDENCIES`, `required_sql_count`, and `ci-affected.py`? | depth | H | answered |
| Q3 | Is the inherited `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` method compatible with `MssqlRetainedAnalysisTests` on SQL Server, or should it be excluded instead of pinned? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-14/111-sensor-reproducibility-2142-state.json`, `.copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-changes.md`, `.copilot-tracking/reviews/2026-11-14/111-sensor-reproducibility-2142-review.md`.
* Reused (verified) findings: Cycle 1 (`79b9cd1be`) added `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` to `RetainedAnalysisTests` in `src/core/tests/test_sensor_analysis_store.py` (`C3`).
* Superseded / stale: Cycle 1 validated `src/core` and `src/api` sensor tests directly without running `tools/test_rpi_checks.py`, leaving `SENSOR_MSSQL_REQUIRED_TESTS` at 10 entries instead of 11 (`C1`, `C2`).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to pinned sensor MSSQL contract in `tools/`; exclude `git push`
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: local validation only; no remote push

#### Wave 1: Wider

* Plan and independent lanes: Inline inspection of `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `tools/ci-affected.py`, `tools/test_ci_affected.py`, `.github/workflows/src-ci.yml`, and `src/README.md` to map every consumer of `SENSOR_MSSQL_REQUIRED_TESTS` and exact `src-namespace` CI commands.
* Worker evidence relationships or inline fallback: Inline fallback (`Q1` -> `C1`, `C2`, `C5`, `C6`, `C7`).
* Reflection: `src-namespace` executes `test_rpi_checks.py`, `test_ci_affected.py`, isolated `ruff check` + `ruff format --check` (`--select E,F,I,B,UP --target-version py312 --line-length 100`), and `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py`. Reproducing `test_rpi_checks.py` locally confirmed 102 passing tests and 1 failure (`test_pinned_sensor_mssql_tests_match_the_real_suite`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Trace every reference to `SENSOR_MSSQL_REQUIRED_TESTS`, `SENSOR_MSSQL_DISCOVERY_SKIPS`, `SENSOR_MSSQL_DIRECT_DEPENDENCIES`, and hardcoded indices/counts in `tools/rpi-checks.py` and `tools/test_rpi_checks.py`.
* Plan and independent lanes: Inline trace of lines 64-73, 184-216, 226-232, 755-765, 1284-1292, 1597-1607, 1648-1656, and 2578-2585 in `tools/rpi-checks.py`, plus lines 432-620 and 690-805 in `tools/test_rpi_checks.py`.
* Worker evidence relationships or inline fallback: Inline fallback (`Q2` -> `C1`, `C2`, `C5`).
* Reflection: `SENSOR_MSSQL_DISCOVERY_SKIPS`, `required_sql_tests`, and `required_sql_count` derive dynamically from `SENSOR_MSSQL_REQUIRED_TESTS`. Without the 11th test in `SENSOR_MSSQL_REQUIRED_TESTS`, both `project-core` discovery skip verification (which saw 34 skips instead of 33 when `ZF_SENSOR_MSSQL` is unset) and `mssql` suite count/name verification in `tools/rpi-checks.py` would fail with `GateError`. `test_direct_sensor_suite_dependencies_select_mssql` already passes because `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` imports only `test_sensor_consumer_live` (already imported by earlier methods and matched by `"sensor"`).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` actually works when inherited by `MssqlRetainedAnalysisTests` against SQL Server (or whether it contains SQLite-specific SQL/assumptions and should instead be moved to a non-inherited class), and check validation-tier impact of editing `tools/rpi-checks.py`.
* Plan and independent lanes: Line-by-line inspection of `RetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` (`src/core/tests/test_sensor_analysis_store.py:118-165`) against `MssqlRetainedAnalysisTests.setUp` (`src/core/tests/test_sensor_analysis_mssql.py:21-38`).
* Worker evidence relationships or inline fallback: Inline fallback (`Q3` -> `C3`, `C4`, `C7`).
* Reflection: Every SQL operation in `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` (`self.snapshot()`, `self.consumer.observed_series(...)`, `self.consumer.configure(...)`, `DELETE FROM sensor_reading`, `DELETE FROM sensor_delivery`, and `DROP TABLE sensor_consumer_control`) is identical to SQL operations already proven in sibling methods `test_unreadable_store_is_insufficient_with_no_priority_effect` and `test_weather_only_window_is_insufficient_with_explicit_reason`, and `MssqlRetainedAnalysisTests.setUp` registers `self.addCleanup(lambda: self.consumer.configure(POLICY, [CONTROL]))` specifically to recreate dropped tables on the shared disposable SQL database. Therefore, inheriting and pinning the test in `SENSOR_MSSQL_REQUIRED_TESTS` strengthens real-SQL gate coverage (strictening gate semantics) rather than weakening anything. Under repository rules, gate-tool and `sensor_analysis.py` changes belong to the Full SQL tier for PR merge/publication, while local Cycle-2 validation runs the targeted `tools/` unit, lint, and strict type checks without pushing.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
| --- | --- | --- | --- | --- |
| Add `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in alphabetical order to `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` and assert its presence in `tools/test_rpi_checks.py` | `C1`, `C2`, `C3`, `C4` | accepted | Restores exact parity between AST-discovered `RetainedAnalysisTests \| MssqlRetainedAnalysisTests` methods, `SENSOR_MSSQL_DISCOVERY_SKIPS`, and `required_sql_tests`/`required_sql_count` while requiring actual MSSQL execution of `reproduce_retained` in the SQL gate | Selected recommendation |
| Move `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` out of `RetainedAnalysisTests` so `MssqlRetainedAnalysisTests` does not inherit it | `C3`, `C4`, `C7` | rejected | Weakens actual SQL Server verification of `sensor_analysis_store.reproduce_retained` even though the test uses 100% MSSQL-compatible operations already exercised by sibling tests | Rejected alternative |
| Full external `tools/rpi-checks.py --all` receipt with live SQL Server (`ZF_SENSOR_MSSQL=1`) | `C7` | deferred | Caller explicitly forbade `git push`; remains tracked rank-1 follow-up prior to PR publication/merge | Open follow-up |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All three research questions are conclusively answered from primary code and local reproduction; `102/103` tests in `test_rpi_checks.py` already pass and the single failure is exact.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded 6-file internal investigation completed directly in <=5 reads with tight coupling between `tools/rpi-checks.py` and `tools/test_rpi_checks.py`.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | `SENSOR_MSSQL_REQUIRED_TESTS` pins 10 alphabetically ordered `MssqlRetainedAnalysisTests` test IDs and drives `SENSOR_MSSQL_DISCOVERY_SKIPS`, `required_sql_tests`, and `required_sql_count` | `tools/rpi-checks.py:187-205` | view / grep | high | Also consumed at `tools/rpi-checks.py:1598-1606` and `1652` |
| C2 | `test_pinned_sensor_mssql_tests_match_the_real_suite` parses `RetainedAnalysisTests` (`test_sensor_analysis_store.py`) and `MssqlRetainedAnalysisTests` (`test_sensor_analysis_mssql.py`) via `ast` and asserts exact set equality against `gate.SENSOR_MSSQL_REQUIRED_TESTS` | `tools/test_rpi_checks.py:461-487` | view / bash | high | Fails at line 474 with missing `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` |
| C3 | `RetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` uses `snapshot()`, `observed_series`, `configure`, `DELETE FROM sensor_reading`, `DELETE FROM sensor_delivery`, and `DROP TABLE sensor_consumer_control` | `src/core/tests/test_sensor_analysis_store.py:118-165` | view | high | Identical SQL statements to lines 80-81 and 106-107 |
| C4 | `MssqlRetainedAnalysisTests` subclasses `base.RetainedAnalysisTests` and registers `addCleanup(lambda: self.consumer.configure(POLICY, [CONTROL]))` to restore dropped tables on SQL Server | `src/core/tests/test_sensor_analysis_mssql.py:21-38` | view | high | Confirms full MSSQL compatibility for the inherited test |
| C5 | `tools/rpi-checks.py` includes `("tools/rpi-checks.py", "tools/test_rpi_checks.py")` in `RUFF_GROUPS` and `("--strict", "tools/rpi-checks.py", "tools/test_rpi_checks.py")` in `TYPE_GROUPS`, matching `src-namespace` in `.github/workflows/src-ci.yml` | `tools/rpi-checks.py:67-68` | view | high | Also `tools/rpi-checks.py:229` and `.github/workflows/src-ci.yml:258-267` |
| C6 | `tools/ci-affected.py` maps `tools/rpi-checks.py` and `tools/test_rpi_checks.py` to `NAMESPACE_ONLY` (`namespace=True`), while `src/core/*` changes on the branch select all 5 projects, `namespace=True`, and `mssql=True` | `tools/ci-affected.py:44-50` | view | high | Verified against `tools/test_ci_affected.py:63-67` |
| C7 | `src/README.md` documents that the local SQL group runs `test_sensor_analysis_mssql` with `ZF_SENSOR_MSSQL=1` verifying `SENSOR_MSSQL_REQUIRED_TESTS` with zero skips, while `project-core` tolerates only those declared discovery skips | `src/README.md:182-192` | view | high | Confirms gate-tool edit tightens/maintains Full SQL tier coverage |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
| --- | --- | --- | --- | --- |
| Q1 | `test_pinned_sensor_mssql_tests_match_the_real_suite` computes the union of `test_*` methods on `RetainedAnalysisTests` and `MssqlRetainedAnalysisTests` and compares them to `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py:187-200`. | `C1`, `C2` | high | Adding the missing method name in `SENSOR_MSSQL_REQUIRED_TESTS` directly resolves the CI failure. |
| Q2 | `SENSOR_MSSQL_DISCOVERY_SKIPS`, `required_sql_tests`, and `required_sql_count` derive automatically from `SENSOR_MSSQL_REQUIRED_TESTS`; `SENSOR_MSSQL_DIRECT_DEPENDENCIES` and `ci-affected.py` need no changes (`102/103` tests in `test_rpi_checks.py` already pass). | `C1`, `C2`, `C5`, `C6` | high | Updating `SENSOR_MSSQL_REQUIRED_TESTS` (and adding an explicit `assertIn` pin check in `test_rpi_checks.py`) fixes both CI and local gate skip/count accounting cleanly. |
| Q3 | `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` uses only SQL operations already exercised in `MssqlRetainedAnalysisTests` and restored by `setUp` cleanup, so running it in the MSSQL suite is safe and desirable. | `C3`, `C4`, `C7` | high | Keep inheritance intact and pin the 11th test in `SENSOR_MSSQL_REQUIRED_TESTS`. |

## Key Discoveries

* `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` is the single source of truth for both tolerated `project-core` discovery skips (`SENSOR_MSSQL_DISCOVERY_SKIPS`) and mandatory zero-skip `mssql` test execution (`required_sql_tests` and `required_sql_count`) (`C1`, `C7`).
* Adding `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` in alphabetical order after `"test_reopened_store_reproduces_signal_without_writes"` brings `SENSOR_MSSQL_REQUIRED_TESTS` from 10 to 11 tests, matching `RetainedAnalysisTests` (10 methods) + `MssqlRetainedAnalysisTests` (1 subclass-specific method) (`C1`, `C2`, `C3`, `C4`).
* Editing `tools/rpi-checks.py` and `tools/test_rpi_checks.py` changes a gate-tool file to tighten required SQL test coverage from 10 to 11 tests; combined with Cycle-1 `sensor_analysis.py` edits on this branch, the branch remains classified under the **Full SQL tier** prior to PR merge/publication (`C5`, `C7`).

### Configuration Examples (when applicable)

```python
SENSOR_MSSQL_REQUIRED_TESTS = _sql_tests(
    SENSOR_MSSQL_SELECTOR,
    "MssqlRetainedAnalysisTests",
    "test_any_declined_control_wins",
    "test_declined_unknown_and_unmapped_consent_fail_closed",
    "test_live_weather_rows_are_not_indoor_input",
    "test_matches_pure_derivation_over_retained_rows_and_is_reproducible",
    "test_read_only_and_no_task_without_approved_rule",
    "test_reopened_store_reproduces_signal_without_writes",
    "test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only",
    "test_stale_and_missing_readings_are_insufficient",
    "test_unmapped_or_invalid_home_is_insufficient",
    "test_unreadable_store_is_insufficient_with_no_priority_effect",
    "test_weather_only_window_is_insufficient_with_explicit_reason",
)
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Add `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` to `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` (preserving alphabetical order) and assert its explicit membership in `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py`.
* Rationale: Aligns the gate's pinned SQL contract and `project-core` discovery-skip allowlist with the inherited `MssqlRetainedAnalysisTests` suite, ensuring `reproduce_retained` is enforced on actual SQL Server as well as SQLite.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C7`
* Implementation impact: `tools/rpi-checks.py` and `tools/test_rpi_checks.py`
* Confidence: high: local reproduction already confirmed `102/103` tests in `test_rpi_checks.py` pass with this exact set difference as the sole failure.

File tree:

```text
tools/
  rpi-checks.py
  test_rpi_checks.py
```

### Alternative: Split `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` into a SQLite-only test class

* Approach: Move the Cycle-1 retained reproduction test into a separate `unittest.TestCase` subclass in `test_sensor_analysis_store.py` not inherited by `MssqlRetainedAnalysisTests`.
* Trade-offs: Avoids touching `tools/rpi-checks.py`, but exempts `sensor_analysis_store.reproduce_retained` from actual SQL Server verification under `ZF_SENSOR_MSSQL=1`.
* Evidence refs: `C3`, `C4`, `C7`
* Rejection rationale: Rejected because `reproduce_retained` is part of the SQL retained-reading adapter (`sensor_analysis_store.py`), is 100% MSSQL-compatible, and caller instructions explicitly require updating the pinned sensor MSSQL test list so the new test is included.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Branch `feat/iot-111-sensor-reproducibility-2142` modifies `sensor_analysis.py` and `tools/rpi-checks.py`, so the Full SQL local gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and verified external receipt) plus hosted CI on the new commit head remain required before PR merge.
* Follow-up: Analytics research phases R1-R3 remain open under Issue #111 criterion 3 (`Refs #111`).
* Residual uncertainty: none within the Cycle-2 `src-namespace` gate fix scope.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
| --- | --- | --- | --- | --- | --- |
| Pin `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in `SENSOR_MSSQL_REQUIRED_TESTS` and verify in `test_rpi_checks.py` | confirmed | user / `C1`, `C2`, `C3`, `C4` | Fixes `src-namespace` failure and enforces MSSQL execution of `reproduce_retained` in the Full SQL gate | `C1`, `C2`, `C3`, `C4` | Updates `tools/rpi-checks.py` and `tools/test_rpi_checks.py` |
| Classify branch validation tier as Full SQL tier (with focused local `tools/` verification in this no-push cycle) | confirmed | repository instructions / `C5`, `C7` | Gate-tool edit changes gate test-count semantics (10 -> 11 required SQL tests) alongside Cycle-1 `sensor_analysis.py` changes | `C5`, `C7` | Disclose completed `tools/` checks vs pre-merge Full SQL receipt |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
| --- | --- | --- | --- | --- |
| Pre-merge Full SQL receipt on exact post-commit head | Run `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <external-dir>` with disposable SQL Server (`ZF_SENSOR_MSSQL=1`) before final merge to `main` | Branch owner / coordinator | Required for Full SQL tier publication gate | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
| --- | --- | --- | --- | --- | --- |
| M | Issue #111 R1-R3 primary-standards sensor threshold research | Prerequisite for non-exercise threshold approval | Separate research workstream | deferred | Cycle-1 follow-up |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected (update `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` and pin assertion in `tools/test_rpi_checks.py`)
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`
* Preconditions met: Exact failure reproduced locally (`102/103` pass, 1 failure); MSSQL compatibility verified; `ruff` and `mypy` commands confirmed against `src-ci.yml`.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field | Record |
| --- | --- |
| Research execution status | Complete |
| Completed waves | Wider, Deeper, and Contrarian for Cycle 1 |
| Lane evidence or inline fallback | Inline fallback: 6 tightly coupled repository files inspected directly |
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C7`) |
| Blockers | none |
| Continuation owner and state | confirmed automatic RPI Agent with automatic continuation to `Plan` |

## Advisory Next Step

| Field | Record |
| --- | --- |
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C7`) |
| Output mode and planning support | convergence; yes, single evidence-backed fix selected |
| Acting owner | confirmed automatic RPI Agent |
| Required gates or confirmations | Research disposition recorded (passed); Planning Readiness `Ready` (passed); pre-transition state write (pending parent transition) |
| Continuation result | automatic continuation to `rpi-plan` |
| Primary evidence file | .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-c2-research.md |
| Notes for planning or re-entry | Single-phase surgical update to `tools/rpi-checks.py` and `tools/test_rpi_checks.py`, validated with `test_rpi_checks.py`, `test_ci_affected.py`, `ruff check`, `ruff format --check`, and `mypy --strict` |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Further research is immaterial because the exact AST set comparison, downstream consumers, and MSSQL compatibility are fully verified from primary code.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check
* Missing or limited sections: none
