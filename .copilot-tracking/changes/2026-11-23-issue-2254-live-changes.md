# Changes: issue 2254 run 4 (2026-11-23)

Tier: focused. No `src` change, so FULL tier and rpi-checks --all do not apply. Validation: `python3 -m unittest tests.test_sqlreads` in src/core, 18 OK; the 2254 test fails (3 != 4) with the fix temporarily reverted and passes restored; live Playwright and API probe.

Files
* docs/reference/research/issue-2254-live-r4-2026-11-23.md and issue-2254-live-2026-11-23/ (probe, result JSON, two screenshots, two test outputs).
* docs/reference/README.md index line; docs/reference/log.md entry.
* .copilot-tracking research, critique, plan, details, changes, review and state files for 2026-11-23.

Criteria (the issue has no ticked list; criteria are its stated expectations)
| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce the 23 vs 22 defect on the code | Proven | test fails 3 != 4 with the repair reverted; test-before-fix-reverted.txt |
| Fix the defect with a regression test | Proven (already on main, a6c0910c97) | test passes, 18 module tests OK; test-with-fix.txt |
| One definition across tile, map and list | Proven | live tile 23, 23 map markers, list "23 cases", API 23, same case ids; probe-after.json, screenshots |
| Live demo shows equal counts after fix | Proven for revision 0000055 on 2026-11-23 | probe-after.json |
| Original stale live row explained | Unproven | SQL public access is disabled; cause inferred from code and test |
| Deployed image contains the fix commit | Unproven | image digest names no commit; inferred from equal counts |
