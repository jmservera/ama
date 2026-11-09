<!-- markdownlint-disable-file -->
# RPI Plan Critique: #1297 correction C3

## Metadata

* Task ID: issue-1297-c3
* Critique date: 2026-11-09
* Plan: .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-09/sensor-mssql-gate-1297-c3-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context: add direct shared dependencies of the sensor MSSQL suite to the mssql selection, with an AST regression; no closure claim.
* Evidence: plan, details, research C3 file; tools/rpi-checks.py (SENSOR_MSSQL constants ~184-215, changed_groups 711-766, moved_path_blocker/receipt use ~355-415); tools/test_rpi_checks.py (~418-545); import statements of the three suite files.
* Boundary: static reading only. No gates, SQL, docker or edits. Closure counts (67/128) were not re-derived.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Research C1 (dataset.py and synthetic/__init__.py are the misses) | Covered | Confirmed. fixture imports `dataset` (line 9) and `zava_forward.core.synthetic` submodules (line 12); store test line 12 does the same. Every other first-party direct import path contains "sensor", "sql" or "store", so the existing keywords select it. zava_forward/core has no __init__.py (namespace package), so no further miss there. |
| Research C1 "15 of 17" | Partial | I count 13 unique direct first-party modules/files including the three suite files, plus the function-level `mssqlstore` import (fixture line 62). The 17 is not reproducible from the supplied text. The two misses are right, but the count is unverified. |
| Research C3 (receipt verification recomputes via changed_groups) | Covered | changed_groups is called in moved_path_blocker (line 363) and the pr_groups check (line 415). |
| P01-T01 constant plus exact-match selection | Covered | Placement in the `src/<project>` branch works for both paths. The `mssql` group depends on `project-api` (dependencies), so no extra wiring is needed. |
| P01-T02 AST regression | Partial | See PC-001 to PC-003. |
| Acceptance: C1 tests still pass | Covered | The sensor-path test at test_rpi_checks.py ~513 is unaffected. |

## Verdict

* Verdict: Revise
* Rationale: The fix is sound and minimal. The regression test, which is the only drift protection, is under-specified in ways that would let it pass vacuously or fail brittly. All findings are direct planner corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: AST resolver rules are unspecified and the import form matters

* Related IDs: P01-T02, Research C1
* Evidence: sensor_consumer_fixture.py line 62 has a function-level `from zava_forward.core.mssqlstore import ...`. `from zava_forward.core.synthetic import sensor_backfill, sensor_faults` and `from zava_forward.core import sensor_analysis` import a module name from a package. test_sensor_analysis_mssql.py line 7 imports the sibling suite file `test_sensor_analysis_store`.
* Concern: A top-level-only `ast.Import`/`ImportFrom` scan would miss the mssqlstore import. A naive resolver would treat `from pkg import name` as `pkg` only (hiding sensor_backfill/faults and the package `__init__`) or try to resolve non-module names such as CONTROL and POLICY. Bare imports (`dataset`, `test_sensor_analysis_store`) must resolve against src/core/tests, and `zava_forward.core.*` against src/core/src.
* Impact: The test could pass without ever exercising synthetic/__init__.py, or could error on non-module names.
* Smallest useful change: In P01-T02 specify the resolver. Use `ast.walk` for nested imports. For `from pkg import n`, add `pkg/__init__.py` (or `pkg.py`) and `pkg/n.py` only when the file exists. Resolve bare names in src/core/tests first. Skip stdlib and third-party names.
* Action owner: planning parent
* Exact resolving evidence: Phase details name these resolution rules, and the test asserts the resolved set contains dataset.py, synthetic/__init__.py, mssqlstore.py and sensor_backfill.py.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: "At least includes both constants" does not guard drift

* Related IDs: P01-T02, Acceptance 1
* Evidence: plan says each resolved path must select mssql and the set must include both constants. The constants are defined in the same change.
* Concern: Each resolved path selects mssql today, so the assertion passes if the constants hold extra entries. A new direct import added to the suite is caught only if it is not selected, which is the intended case. But nothing stops stale or extra constant entries.
* Impact: The constant can rot silently, which weakens the "future drift fails" claim.
* Smallest useful change: Assert that the subset of resolved dependencies selected only because of the constant equals `set(SENSOR_MSSQL_DIRECT_DEPENDENCIES)`. This can be computed by checking whether the path selects mssql without the constant, for example by testing the keyword rule in isolation or by checking the constant membership. Equality is the minimum acceptable check.
* Action owner: planning parent
* Exact resolving evidence: The test contains an equality assertion between the keyword-missed resolved set and the constant, and it fails when either side changes.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Negative cases must be named and keyword-free

* Related IDs: P01-T02 test 2, Functional Requirements
* Evidence: Keywords "store", "schema", "sql", "assistants" and "sensor" match anywhere in the lowercase path. Candidate paths that are clean: src/core/tests/building_fixture.py, src/core/src/zava_forward/core/synthetic/climate_history.py. Do not use sensor_*.py siblings or anything containing "store".
* Concern: "A sibling synthetic module not imported directly" is ambiguous. Most siblings are `sensor_*.py` and would select mssql through the existing keyword, making the negative assertion false. The plan also lists core timeline.py without checking that it is clean.
* Impact: Implementer error or a flaky test.
* Smallest useful change: Name concrete paths (building_fixture.py, climate_history.py, timeline.py after a keyword check) in the details. Assert `"mssql" not in changed_groups(...)` and `project-core` is in the result. Also assert a path in `src/api` such as an unrelated api test does not select mssql.
* Action owner: planning parent
* Exact resolving evidence: Phase details list exact negative paths, each confirmed to contain none of the five keywords.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Research counts are unreproducible

* Related IDs: Research C1, C2
* Evidence: My count of direct first-party modules is 13 unique (including the three suite files), not 17. The 67/128 closure figure was not derived in the supplied inputs.
* Concern: The facts that drive the policy option B (cost of closure-wide selection) rest on unverified numbers.
* Impact: Low for C3 itself. It matters if the owner weighs B.
* Smallest useful change: Either correct or caveat the counts ("by AST script, not reproduced here"), or drop them from the owner follow-up text.
* Action owner: planning parent
* Exact resolving evidence: Research counts reconciled with the AST test's output, or marked as unverified.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Scope is minimal. Closure selection is explicitly deferred as an owner policy (alternative B) with no overclaim, which is consistent with the user's direction.
* Check_skips, the matrix and the receipt format are untouched. Receipt verification inherits the rule through changed_groups.
* Residual, accepted in the plan: transitive modules such as workflows.py, ai.py and ledger.py do not select mssql.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Static read only. Count claims and the 15/17 breakdown were not re-run. Test behaviour was not executed.

## Recommended Next Action

* Highest-impact finding: PC-001 (with PC-003, which share the same test-spec correction)
* Action owner: planning parent
* Smallest next action: Revise P01-T02 to specify the resolver, the equality assertion and the named clean negative paths. No user response is required.
