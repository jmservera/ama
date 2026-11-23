# Changes: issue 2254 run 5 (2026-11-23)

Tier: focused. The change is a test only; no `src` production code changed, so the FULL tier and `rpi-checks.py --all` do not apply. Validation: `python3 -m unittest tests.test_sqlreads` in src/core with `PYTHONPATH=src:tests`, 19 tests OK; ruff check clean on the test file. Hosted CI for the exact head was not observed (no push).

Files
* src/core/tests/test_sqlreads.py: new `test_overcounted_safety_column_is_repaired_when_hazard_is_released_or_case_closed_issue_2254` (the over-count direction: stored hazard 1 while all hazards are released, or the case is closed).
* docs/reference/research/issue-2254-live-r5-2026-11-23.md plus evidence in issue-2254-live-2026-11-23/ (probe-r5.json, screens overview-r5.png and list-safety-r5.png, r5-test-with-fix.txt, r5-test-before-fix-reverted.txt).
* docs/reference/README.md index line and docs/reference/log.md entry.
* .copilot-tracking r5 research, critique, plan, details, changes, review and the state file.

Regression proof: with `"hazard"` temporarily removed from the column tuple in `SqlStore._repair_identity_columns`, both 2254 tests fail (the existing one 3 != 4); restored, both pass. The source file was restored with git checkout; no source diff remains.

Criteria (the issue has no ticked list; criteria are its stated expectations)
| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce the 23 vs 22 defect on the code | Proven | existing under-count test fails 3 != 4 with the repair reverted; r5-test-before-fix-reverted.txt |
| Regression test covers both drift directions | Proven (new) | over-count test fails reverted, passes with fix |
| One definition across tile, map and list | Proven | live revision 0000056: tile 23, 23 markers, list "23 cases", API 23, no id differences; probe-r5.json, screenshots |
| Live demo shows equal counts after the fix | Proven for revision 0000056 on 2026-11-23 | probe-r5.json |
| Original stale live row explained | Unproven | SQL public access is disabled and not changed; cause inferred from code and tests |
| Deployed image contains the fix commit | Unproven | image digest names no commit; inferred from equal counts |
