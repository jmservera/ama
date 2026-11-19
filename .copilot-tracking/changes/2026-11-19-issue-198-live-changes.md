# Issue 198 live changes (2026-11-19)

* `.github/rubric/scripts/test_safe_output_runtime.py`: `test_tracking_only_changes_do_not_trigger_workflows` now skips events a workflow does not declare and uses a `src/` sample path instead of the retired `mvp/` path. Fixes the 10 failures recorded in `docs/reference/research/issue-198-rubric-live-r2-2026-11-18.md`.
* No src, workflow, SQL, security or infra change. Tier: focused. Live Azure, browser and sign-in proof not applicable to any criterion; none gathered.

## Validation

* `python3 -m pytest -q test_safe_output_runtime.py test_prepare.py` in `.github/rubric/scripts`: before, 10 failed 7 passed 7 skipped (safe-output file); after, 84 passed, 16 skipped, 0 failed.
* `ruff format --isolated --line-length 100 --check` on that file: fails on pre-existing long lines throughout the file (not in src-ci scope, not reformatted to keep the diff surgical). mypy per `src/<project>`: not applicable.

## Per-criterion status

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Baseline recorded | Proven (ticked) | #292; `docs/reference/research/issue-198-rubric-live-r2-2026-11-18.md` |
| 2 | src test and Dockerfile coverage | Proven (ticked) | #292; 297 tests, 3 pyproject, 6 Dockerfiles counted |
| 3 | Per-PR totals in dual window | Unproven; cannot be proven for the demo | Merged PR bodies record counts, not totals; D1 (#748) moved scoring to main |
| 4 | Cut-over registry PR ordering | Unproven (ordering); end state proven | No mvp or prototype glob in `artifacts.json` (grep, 2026-11-19: none); removed across #292, #295, #851 |
| 5 | README and failures reassessed | Proven (ticked); stale count fixed in test | 0 failures in `test_safe_output_runtime.py` now |
| 6 | Lock recompiled | Proven (ticked) | #748 |
| 7 | Before and after comparison | Proven (ticked) | #880: 47 to 79 |

Owner decision still needed: waive or reword criteria 3 and 4. Remaining follow-up: retire `mvp-ci.yml` and `mvp-validation.yml` (separate workflow classification).
