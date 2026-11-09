<!-- markdownlint-disable-file -->
# Plan Critique: chat-schema-sql-selector-1298

* Critique run: single final-candidate critique, 2026-11-09
* Execution status: Complete
* Verdict: Revise (planner-direct corrections only; no user decision needed)
* Severity summary: High 0, Medium 3, Low 4

## Inputs and Criterion Boundary

* Plan, phase details, research and session state for task slug chat-schema-sql-selector-1298.
* Code read: tools/rpi-checks.py (lines 183-212, 721-763, 1381-1383, 1595-1603, 1650), tools/test_rpi_checks.py (lines 513-760), src/core mssqlstore.py, chatthreads.py, sqlstore.py, tests/sensor_consumer_fixture.py, src/README.md lines 175-200.
* Caller requirements were treated as authoritative: demo-targeted tier, Refs #1298 only, source bounded to the two tool files, no exhaustive or transitive claim, fresh attempt, correction budget 0 of 5.
* Not assessed: live SQL behavior, hosted CI, the old branch contents.

## Coverage Assessment

The core claim is verified. `changed_groups` (tools/rpi-checks.py:754-760) selects `mssql` only by the keywords store, schema, sql, assistants, the core+sensor rule, or `path in SENSOR_MSSQL_DIRECT_DEPENDENCIES`. `chatthreads.py` matches none, so the omission is real. `mssqlstore.py:20` imports `MEMORY_ADDED`, `MSSQL_DDL`, `MSSQL_INDEX` from `.chatthreads`. They are used at lines 51-54 (TABLES), 254 (memory column migration) and 294 (index creation). The fixture constructs `MssqlStore` when `ZF_SENSOR_MSSQL=1` (sensor_consumer_fixture.py:72-83). The ten pinned sensor tests, the `SENSOR_MSSQL_DISCOVERY_SKIPS` tuple (202-204, 1650) and `required_sql_tests`/`required_sql_count` (1595-1603) match the research. `SENSOR_MSSQL_DIRECT_DEPENDENCIES` is referenced only at rpi-checks.py:759, in test_rpi_checks.py:608 and in src/README.md:191, so adding one member has no hidden consumer. The base `9f9aacc8b` equals the current HEAD. `chat_panel.py` and `chat_privacy.py` exist under src/core and match no keyword, so the negative controls are valid.

## Findings

### PC-001 (Medium): validation plan does not state that the installed tool versions differ from the pins

* Related: P03-T01, NFR typing and formatting.
* Evidence: the gate pins `ruff==0.17.1` and `mypy==2.4.0` (tools/rpi-checks.py:1381, 2184). The environment has ruff 0.17.3 and mypy 2.4.1. The tooling group runs `lint(python, RUFF_GROUPS[-1])` (line 1382), which includes lint as well as format, plus `mypy --strict` on the two tool files. The plan names only the "Ruff format check" and "pinned versions when installed".
* Impact: a pass with unpinned versions could be reported as pinned-tool evidence.
* Smallest change: P03-T01 should run the Ruff lint check and the format check for the `RUFF_GROUPS[-1]` files, and strict mypy for `TYPE_GROUPS[2]`. It should record the installed versions and label the results "unpinned local versions, not equivalent to the pinned gate". A version-pinned virtual environment inside the worktree-owned scratch area is acceptable only if the owner's no-global-install rule allows it; otherwise rely on hosted CI for the pinned result.
* Resolving evidence: the changes record lists the versions, commands, exits and the equivalence caveat.
* Owner: planner. Direct correction.

### PC-002 (Medium): the exact-set pin edit is hand-maintained, so it adds a second unlinked source of truth

* Related: P02-T01, test ownership lock.
* Evidence: test_rpi_checks.py:604-609 derives `missed` from the AST of suite imports. It then adds the hand-written `indoor_projection.py`, and the assertion is exact equality with `SENSOR_MSSQL_DIRECT_DEPENDENCIES`. `chatthreads.py` is not a suite import (the fixture imports `mssqlstore`, which has the keyword `store`), so after the source edit the existing test fails unless the expectation gains it. The plan correctly schedules that edit, but only as a literal added to the set union. The new test separately parses `mssqlstore.py`. Nothing connects the two.
* Impact: a future removal of the `.chatthreads` import from `mssqlstore.py` would leave the pin and the set both holding a stale entry and the tests green.
* Smallest change: in P01-T01/P02-T01, have the new test derive the `.chatthreads` file from the `ImportFrom` nodes of `mssqlstore.py` (`level == 1`, module `chatthreads`) and assert that `chatthreads.py` is in `SENSOR_MSSQL_DIRECT_DEPENDENCIES`. Keep the exact-set expectation as `missed | {indoor_projection, chatthreads}`, or reference the derived path. The extra-pin edit stays one line. Also assert the path is not selected by any keyword, so set membership is what is proven necessary.
* Resolving evidence: after the edit, the module passes. Temporarily dropping the set member, or the `mssqlstore` import, makes the new test fail.
* Owner: planner. Direct correction.

### PC-003 (Medium): the "fourteen sibling modules" claim understates the sqlstore import surface

* Related: Executive Summary "What You May Not Know", research C14, Follow-Up Items.
* Evidence: sqlstore.py has 13 top-level relative imports (lines 29, 31-35) plus the absolute `zava_forward.core.ai` (line 30), so 14 is a top-level count. It also has many function-local relative imports (lines 224-237, 673-735, among others). `mssqlstore.py` also executes many of those paths at runtime.
* Impact: the issue requires recording the remaining transitive limitation honestly, and "fourteen" reads like a complete list.
* Smallest change: reword to "at least fourteen top-level imports (one absolute) plus function-local imports; not enumerated". Keep it in the research, plan, changes and review records.
* Resolving evidence: corrected wording in all four records.
* Owner: planner. Direct correction.

### PC-004 (Low): receipt-expectation coverage for issue acceptance criterion 3 should be explicit

* Related: P01-T01, research C11.
* Evidence: the receipt rejection tests (test_rpi_checks.py:643-760) are path-independent, and the plan leaves them unchanged. The loop edit at 513-541 asserts the flagged sensor command, the flag env and the count for the new path. That is sound and sufficient.
* Smallest change: state in the changes record that missing, substituted, skipped and failed evidence rejection is path-independent and already covered. Cite the exact test names (`test_sensor_mssql_execution_evidence_rejects_missing_substituted_skipped_or_failed`, `test_sensor_mssql_receipt_rejects_tampered_or_incomplete_evidence`). Correct the research C11 cite to 643-760 (700-760 omits the first test).
* Owner: planner. Direct correction.

### PC-005 (Low): the reproduction assertion boundary in P01 is ambiguous

* Related: P01-T01 validation expectations.
* Evidence: the planned AST assertions on `mssqlstore.py` and the fixture pass before the fix. Only the selection assertions and the loop subtest fail. The phrase "references the aliases in MssqlStore-side code" is loose: `CHAT_DDL` is used in module-level `TABLES`, and `CHAT_MEMORY_ADDED` and `CHAT_INDEX` in methods.
* Smallest change: name the usage sites to assert (`TABLES` entries, `CHAT_MEMORY_ADDED` loop, `CHAT_INDEX` index list) and record that the failing run is expected to fail on the selection assertions with the `mssql` not-in-groups message. Run `unittest -k chat_schema` and record that the loop subtest also fails.
* Owner: planner. Direct correction.

### PC-006 (Low): README text at src/README.md:183-192 stays accurate but should be recorded as checked

* Related: research C15, Non-Goals "README rewrite".
* Evidence: the text says local `--changed` selects `mssql` for core paths containing `sensor` and for "the listed `SENSOR_MSSQL_DIRECT_DEPENDENCIES`". It does not enumerate members or claim exhaustiveness, so it stays correct after the change and needs no edit within the two-file bound.
* Smallest change: state in the changes record that the README was re-read after the edit and found still accurate. Note the optional owner follow-up of mentioning the not-exhaustive boundary.
* Owner: planner. Direct correction.

### PC-007 (Low): the fail-closed review should list what was deliberately not changed

* Related: Non-Goals, NFR.
* Evidence: nothing in the planned change loosens any control. Selection matching stays exact-string, and rename or move cases are out of scope. `skipped_groups` text at rpi-checks.py:680 ("core sensor or SQL dependency path") stays valid. No further fail-closed gap was found within the bound. One accepted residual: other `sqlstore.py` imports and the function-local imports are not selected.
* Smallest change: have the review record that residual and the SQL-not-run rationale. A selection-only change does not alter the SQL command, so no SQL run is needed. The review must still say that real sensor SQL execution at this head is unproven by this attempt.
* Owner: planner and implementer. Direct.

## Checks of Specific Questions

1. Evidence cites: accurate. Corrections are PC-003 (count meaning) and PC-004 (cite range). Lines 250-256/292-295 contain the cited uses at 254 and 294.
2. Test edits: the loop entry and the new selection assertions fail before and pass after. The exact-set test passes before and needs the paired edit in P02. The module is not left red between P01 and P02 beyond the intended failing new test.
3. Exact-set pin: sound if paired with a derived check (PC-002).
4. README: still accurate (PC-006).
5. Validation: SQL-not-needed rationale is adequate for a selection-only change. Tool versions need the caveat (PC-001).
6. Fail-closed gaps: none new within bound (PC-007).

## Limitations

* No tests were executed; findings come from reading the code and plan.
* `git status` shows the plan artifacts untracked; the plan says they are committed before source edits.

## Relevant Artifacts

| Path | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-11-09/chat-schema-sql-selector-1298-plan.md](.copilot-tracking/plans/2026-11-09/chat-schema-sql-selector-1298-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-11-09/chat-schema-sql-selector-1298-phase-details.md](.copilot-tracking/details/2026-11-09/chat-schema-sql-selector-1298-phase-details.md) | Phase details |
| [.copilot-tracking/research/2026-11-09/chat-schema-sql-selector-1298-research.md](.copilot-tracking/research/2026-11-09/chat-schema-sql-selector-1298-research.md) | Research evidence |
| [.copilot-tracking/rpi-sessions/2026-11-09/chat-schema-sql-selector-1298-state.json](.copilot-tracking/rpi-sessions/2026-11-09/chat-schema-sql-selector-1298-state.json) | Session state |

## Next Steps

No user response is required. The planning parent revises the plan and details for PC-001 to PC-007 directly, records dispositions in the plan, then continues to implementation without another critique.
