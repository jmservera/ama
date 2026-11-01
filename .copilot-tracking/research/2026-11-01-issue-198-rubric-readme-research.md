# Issue 198 research: remaining slice (2026-11-01)

Disposition: executed. Planning Readiness: Ready.

## Evidence
* Merged PRs: #292 (src excludes, tests, rubric_version unchanged; criteria 1-2 ticked), #507 (src cut-over verification and migration evidence correction), #613 (closure audit batch 2, issue left open).
* Open PRs referencing #198: none.
* Registry on main: `.github/rubric/artifacts.json` has no `mvp/` include globs and no `prototype/deploy` glob; only `mvp/data/**` and `mvp/web/vendor/**` defensive excludes remain. `src/**/*` is in `solution-code`.
* Latest score: `.github/rubric/scores/latest.json` total 77 (A34 B23 C11 D9), rubric_version 2, commit 051f6a3.
* Rubric suite run today: 17 failed, 358 passed, 7 skipped. 7 failures hard-code the 66-point seed (test_gate 6, test_prepare 1); 10 are tracking-only trigger tests for infra-plan, mvp-ci, mvp-validation, src-ci and src-deploy workflows. README states 19 (line 87) and 21 (line 346).

## Findings
* Criteria 3, 4, 7 are historical sequencing/contemporaneous-recording clauses; closure audit and #507 confirm they cannot be proven retroactively. They stay unticked.
* Criterion 6 is conditional and not activated (no workflow Markdown change); lock recompile not applicable.
* Remaining deliverable: criterion 5 README rubric section (stale MVP/Prototype text, stale failure counts).
