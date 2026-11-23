# Changes: issue 2254 run 5 (2026-11-23)

Tier: focused. The change is a test only; no `src` production code changed, so the FULL tier and `rpi-checks.py --all` do not apply. Validation: `python3 -m unittest tests.test_sqlreads` in src/core with `PYTHONPATH=src:tests`, 19 tests OK; ruff check clean on the test file. Hosted CI for the exact head was not observed (no push).

Files
* src/core/tests/test_sqlreads.py: new `test_overcounted_safety_column_is_repaired_when_hazard_is_released_or_case_closed_issue_2254` (the over-count direction: stored hazard 1 while all hazards are released, or the case is closed).
* docs/reference/research/issue-2254-live-r5-2026-11-23.md plus evidence in issue-2254-live-2026-11-23/ (probe-r5.json, screens overview-r5.png and list-safety-r5.png, r5-test-with-fix.txt, r5-test-before-fix-reverted.txt).
* docs/reference/README.md index line and docs/reference/log.md entry.
* .copilot-tracking r5 research, critique, plan, details, changes, review and the state file.

Regression proof: with `"hazard"` temporarily removed from the column tuple in `SqlStore._repair_identity_columns`, both 2254 tests fail (the existing one 3 != 4); restored, both pass. The source file was restored with git checkout; no source diff remains.
Tier: FULL by classification (`src/core` changed). Local validation only: `tests.test_sqlreads` 19 OK, `ruff check` clean, `mypy` 3 pre-existing errors unchanged. `rpi-checks.py --all` was not run; the coordinator runs the gate.

Files
* src/core/src/zava_forward/core/sqlstore.py: repair also rebuilds `support`, `days`, `fstatus`.
* src/core/tests/test_sqlreads.py: new regression test; `insights` import.
* docs/reference/research/issue-2254-live-r5-2026-11-23.md and its evidence folder; docs/reference/README.md; docs/reference/log.md.
* .copilot-tracking r5 research, critique, plan, details, changes, review; state file.

Criteria (the issue has no ticked list; criteria are its stated expectations)
| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce the 23 vs 22 defect on the code | Proven | existing under-count test fails 3 != 4 with the repair reverted; r5-test-before-fix-reverted.txt |
| Regression test covers both drift directions | Proven (new) | over-count test fails reverted, passes with fix |
| One definition across tile, map and list | Proven | live revision 0000056: tile 23, 23 markers, list "23 cases", API 23, no id differences; probe-r5.json, screenshots |
| Live demo shows equal counts after the fix | Proven for revision 0000056 on 2026-11-23 | probe-r5.json |
| Original stale live row explained | Unproven | SQL public access is disabled and not changed; cause inferred from code and tests |
| Deployed image contains the fix commit | Unproven | image digest names no commit; inferred from equal counts |
| Reproduce the 23 vs 22 defect on the code | Proven (run 4) | docs/reference/research/issue-2254-live-r4-2026-11-23.md |
| Fix with a regression test | Proven (main a6c0910c97) | test_sqlreads, 19 OK |
| Same defect class for other list filters (new this run) | Proven on code | r5 test fails `0 != 21 : long` reverted, passes with change |
| One definition across tile, map and list, live | Proven for revision 0000055 (run 4); not re-probed this run | r4 probe-after.json |
| This run's change live on the demo | Unproven | not deployed; no push or deploy allowed here |
| Original stale live row explained | Unproven | SQL private; cause inferred from code |
| Deployed image contains the fix commit | Unproven | digest names no commit |
