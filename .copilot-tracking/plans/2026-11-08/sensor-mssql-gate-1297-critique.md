<!-- markdownlint-disable-file -->
# RPI Plan Critique: bind sensor MSSQL skips to required SQL execution (issue #1297)

## Metadata

* Task ID: issue-1297 / sensor-mssql-gate-1297
* Critique date: 2026-11-08
* Plan: .copilot-tracking/plans/2026-11-08/sensor-mssql-gate-1297-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/sensor-mssql-gate-1297-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: fail-closed exact discovery exception (group, test IDs, reason); explicit sensor MSSQL dispatch with ZF_SENSOR_MSSQL=1 in the SQL group; zero skips; evidence the named test test_reopened_store_reproduces_signal_without_writes passed; runner and receipt regression tests; existing suites preserved; no workflow edits; no heavy workloads; #184 DEFAULT_TESTS untouched. Test ownership lock: removals none, additions at most about 6 focused methods in tools/test_rpi_checks.py, validation = tools unit tests, ruff, strict mypy.
* Research and evidence considered: .copilot-tracking/research/2026-11-08/sensor-mssql-gate-1297-research.md; tools/rpi-checks.py (check_skips, required_sql_tests, required_checks, Runner.sql, Runner.command, verify_commands, SQL_CHAT_REQUIRED_TESTS, _required_tests_passed); tools/test_rpi_checks.py (sql_chat_log, receipt fixtures near lines 1676-1830).
* Decisions, dependencies, and acceptance criteria considered: plan FR1-FR4, AC1-AC5, P01-P03, follow-ups.
* Assessment boundary: read-only static review. No SQL, no test execution, no source test files of the sensor module were re-read. Research claims C1-C7 were spot-checked against current source and hold.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Exact discovery exception (FR1, P01-T02, AC1) | Partial | Scoping is right; ID format and the check_skips condition rewrite are under-specified (PC-001, PC-002) |
| Explicit dispatch with flag (FR2, P01-T04) | Covered | Mirrors SQL_SELECTORS command in both Runner.sql and required_checks; verify_commands compares env |
| Zero skips and named test passed (FR3, AC3) | Partial | Mechanism exists (expected_count, required_tests); no check that pinned IDs exist in the real module (PC-003) |
| Runner and receipt regression tests (P02, AC2) | Partial | Existing fixtures break and are not planned for edit (PC-004); test budget not itemised (PC-005) |
| Existing suites preserved (FR4) | Covered | Selector command argv/env unchanged |
| No workflows, no heavy workload, #184 untouched | Covered | Non-goals and AC5 |
| Validation (P03, AC4) | Partial | No pre-implementation proof that the module collects from src/api (PC-006); lint/type commands not tied to repo definitions (PC-007) |

## Verdict

* Verdict: Revise
* Rationale: The design is sound and fail-closed, but the plan omits mandatory edits to existing receipt fixtures that the new matrix command will break, leaves the test-ID format and check_skips restructuring ambiguous, and has no guard against a mistyped pinned ID permanently failing the gate. All are direct planner corrections; none needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Pinned test IDs must be full unittest IDs, not method names

* Related IDs: FR1, FR3, P01-T01, C8
* Evidence: tools/rpi-checks.py SQL_CHAT_REQUIRED_TESTS uses `_sql_tests(module, klass, *names)` producing `name (module.Class.name)`; check_skips regex matches `^(.+?) \.\.\. skipped '...'$` and _required_tests_passed matches `startswith(f"{name} ... ")`. P01-T01 lists bare method names.
* Concern: Bare names will not match the verbose header or discovery skip line, so the exception and the ok-once check would both fail (or, if prefix-matched loosely, be non-exact).
* Impact: Gate either permanently rejects or weakens exactness.
* Smallest useful change: State that the tuple is built with `_sql_tests("test_sensor_analysis_mssql", "MssqlRetainedAnalysisTests", ...)` and that discovery pairs are `(id, reason)` built from it; note the discovery skip ID uses the same class path in project-core (C8 confirms).
* Action owner: planning parent
* Exact resolving evidence: P01-T01 text names the helper and class; a unit test asserts a discovery skip line in C8 form is accepted.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: check_skips rewrite must keep the reason out of the global allowlist without a bypass path

* Related IDs: FR1, P01-T02, C1, C2
* Evidence: check_skips currently raises when `s["reason"] not in EXPECTED_SKIP_REASONS` before any scoped logic; the CHAT_PANEL pattern works only because that reason is in the allowlist and then narrowed.
* Concern: P01-T02 says the reason is not added to the allowlist but does not specify the new condition. A naive "accept if pair in set" placed before the allowlist test must not skip the integration branch, and the allowlist-then-narrow alternative would make the reason acceptable in every group.
* Impact: Risk of a reason-only allowlist (the rejected Alternative A) or of accidentally weakening the integration=True path.
* Smallest useful change: Specify the exact predicate: a skip is accepted iff (reason in EXPECTED_SKIP_REASONS and existing scoping) or (group == "project-core" and not integration and (test, reason) in the pair set); integration=True still accepts only SQL_NOT_APPLICABLE. Require each rejection case in AC1 (other group, integration, altered ID, altered reason) to be asserted.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 states the predicate; the exception test fails if the pair set is replaced by reason-only matching.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: No guard that pinned IDs correspond to real tests

* Related IDs: FR3, AC3, P02
* Evidence: existing test_required_actual_sql_chat_tests_exist_and_are_selected (tools/test_rpi_checks.py ~415-426) checks pinned chat IDs against source; the plan adds no analogue.
* Concern: A typo or rename (including test_reopened_store_reproduces_signal_without_writes) makes the gate unpassable, or the named-test evidence vacuous, without any unit test noticing.
* Impact: AC3 ("named test in the required set") is satisfied only by constant membership, not by reality.
* Smallest useful change: Add one test that loads the pinned IDs against the module source (same approach as the chat analogue, no SQL) and asserts the set equals the eight methods of MssqlRetainedAnalysisTests, including the named test. This test intentionally fails when #184 adds two inherited tests; record that in follow-ups.
* Action owner: planning parent
* Exact resolving evidence: test present in P02 list and passing on main base.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Existing receipt fixtures will break and their update is not planned

* Related IDs: FR2, FR4, P02-T03, ownership lock (removals none)
* Evidence: tools/test_rpi_checks.py ~1684-1692 generates logs with `if gate.required_sql_tests(check["argv"]): text = sql_chat_log()`, which would feed the chat log to the sensor argv; ~1795 asserts `len(suites) == 10`; ~1806 picks the first mssql suite row; ~1829 restores sql_chat_log.
* Concern: Adding a suite command in required_checks makes the full-receipt verification fixtures fail (wrong log, count 11), contradicting "existing tests still pass" (AC4). Plan lists only new tests.
* Impact: P03 fails on first run, or the implementer deletes or loosens assertions, violating the lock.
* Smallest useful change: Add a P02 task: modify (not remove) the fixture to select the log by argv (chat log for SQL_SELECTORS tail, a pinned eight-ok log for the sensor argv), update the suite count to 11, and keep the mutation loop pinned to the selector row. Declare these as modifications within the lock, and add a sensor_mssql_log helper beside sql_chat_log.
* Action owner: planning parent (record), implementer (edit)
* Exact resolving evidence: plan lists the fixture edits; the full-receipt verify tests pass unchanged in intent with count 11.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Test additions are not itemised against the six-method budget

* Related IDs: P02-T01..T03, ownership lock
* Evidence: P02 details enumerate about twenty cases across three task bullets.
* Concern: Without a method-level mapping, scope either exceeds the cap or cases are dropped silently.
* Impact: Lock breach or uncovered caller requirements (runtime command() path, receipt tamper).
* Smallest useful change: Fix six methods, each using subTest: (1) discovery exception exact and rejections; (2) matrix order, argv, env flag, selector env lacks flag; (3) runtime and receipt log mutations (missing, duplicate, failed, skipped, extra count nine, substituted ID, named test absent) via check_skips with the sensor argv's required_tests and count; (4) verify_commands rejects flag removed, selector substituted, cwd changed, command missing; (5) pinned IDs equal real module methods (PC-003); (6) Runner.sql dispatch ordering using the existing fake-command pattern near line 2217. Merge or drop rather than exceed six.
* Action owner: planning parent
* Exact resolving evidence: phase details list six named methods mapped to AC1-AC3.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Import and collection feasibility from src/api is asserted, not shown

* Related IDs: FR2, C6, C8
* Evidence: C8 ran from src/core; the gate runs from src/api with test_paths("api", True). SQL execution cannot happen here.
* Concern: If the module or its fixture imports something absent from the api PYTHONPATH or venv, the first coordinator run fails late and expensively.
* Impact: Wasted heavy run; weak confidence in FR2.
* Smallest useful change: Add a no-SQL P03 step: from src/api with the gate's PYTHONPATH (api, core, agents tests) run `python -m unittest -v test_sensor_analysis_mssql` and require Ran 8 with eight skips carrying the exact reason and eight unique IDs matching the pinned tuple. Resource-light and consistent with "no heavy workload".
* Action owner: planning parent (plan), implementer (run)
* Exact resolving evidence: recorded output in the changes record showing the eight pairs equal the pinned set.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Validation commands should come from the repository's own definitions

* Related IDs: P03-T01, AC4
* Evidence: plan states "ruff --isolated line length 100, mypy --strict ... per TYPE_GROUPS"; tools/rpi-checks.py defines RUFF_GROUPS and TYPE_GROUPS (strict entry for tools/rpi-checks.py and tools/test_rpi_checks.py). Repository guidance also requires `python3 tools/rpi-checks.py --changed` as the focused tier.
* Concern: Hand-typed flags may diverge; the focused tier is not mentioned, nor is it stated that the complete gate is deferred (D4: SQL-sensitive change).
* Impact: Possible false pass or missed gate step.
* Smallest useful change: Take ruff and mypy invocations from RUFF_GROUPS and TYPE_GROUPS; add `--changed` as a final local check if it needs no Docker or SQL, otherwise record it as deferred with the full gate to the coordinator.
* Action owner: planning parent
* Exact resolving evidence: P03-T01 cites the definitions; changes record states what ran and what was deferred.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Low]: Other groups that might collect the sensor module, and receipt compatibility, are unchecked

* Related IDs: FR1, C7
* Evidence: C7 covers project-core discovery only; the exception is deliberately group-scoped, so any other group that collects the module would now fail closed.
* Concern: A project-api or image-group discovery that imports test_sensor_analysis_mssql would newly fail. Also, receipts produced before this change will fail verification by design.
* Impact: Unexpected red gate; confusion over stale receipts.
* Smallest useful change: Have the implementer confirm by search that only project-core discovery collects the module, and note in the plan that earlier receipts are intentionally invalid.
* Action owner: implementer
* Exact resolving evidence: one-line result recorded in the changes record.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Fail-closed design confirmed: separate command keeps the existing selector argv and env (FR4), avoids discovery-derived expectations, and reuses expected_count plus required_tests in both command() and verify_commands.
* Accepted residuals (already stated): #184 raises the inherited set to ten and will intentionally fail the pinned set until extended; DEFAULT_TESTS conflict is out of scope; real SQL execution is deferred to the coordinator.
* The sensor setUp drops sensor tables on the shared disposable database; running it last in the group (as planned) is adequate.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Static review only; no tests or SQL run. Sensor test sources were not re-read beyond research citations. The research notes a prior process deviation (pre-skill source exploration, bash-written Findings); not assessed further.

## Recommended Next Action

* Highest-impact finding: PC-004
* Action owner: planning parent
* Smallest next action: revise phase details to add fixture-edit task, full-ID format, check_skips predicate and six-method test map, then finalize without another critique
* User response required: no

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-11-08/sensor-mssql-gate-1297-plan.md](.copilot-tracking/plans/2026-11-08/sensor-mssql-gate-1297-plan.md) | Plan critiqued |
| [.copilot-tracking/details/2026-11-08/sensor-mssql-gate-1297-phase-details.md](.copilot-tracking/details/2026-11-08/sensor-mssql-gate-1297-phase-details.md) | Phase details critiqued |
| [.copilot-tracking/research/2026-11-08/sensor-mssql-gate-1297-research.md](.copilot-tracking/research/2026-11-08/sensor-mssql-gate-1297-research.md) | Research evidence |

## Next Steps

No user action required. The planning parent applies PC-001 to PC-008 directly and finalizes.
