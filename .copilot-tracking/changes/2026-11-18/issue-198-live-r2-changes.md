---
title: Issue 198 live r2 changes
date: 2026-11-18
task_slug: issue-198-live-r2
---

# Changes

Tier: FOCUSED (docs and evidence only; no src, workflow or registry edit). Refs #198; nothing ticked.

## Files

* Added `docs/reference/research/issue-198-rubric-live-r2-2026-11-18.md` and its `issue-198-rubric-live-r2-2026-11-18/` raw-output folder.
* Edited `docs/reference/README.md` (index row) and `docs/reference/log.md` (appended entry).
* Added RPI artifacts under `.copilot-tracking/` (research, plan, details, critique, changes, review) and updated the session state.

## Per-criterion table

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Baseline total and solution-code criteria | Proven | 47 baseline (#292), now 79; `latest.txt` |
| 2 | src test and Dockerfile coverage, own registry PR | Proven | #292; 297 tests, 3 pyproject, 6 Dockerfiles in `solution-code-count.txt` |
| 3 | Per-migration-PR total, dip cause, recovery | Unproven, cannot be proven for the demo | PR bodies hold counts not totals; D1 scores main only |
| 4 | Cut-over registry PR removes mvp and prototype globs; old-registry scoring first | Globs absent (proven); ordering unproven and unprovable | `registry.txt`; removal spread over #292, #295, #851 |
| 5 | README updated; failures reassessed | Proven with caveat | #705; failures now 10 in `test_safe_output_runtime.py` |
| 6 | Lock file recompiled if workflow Markdown changes | Proven | #748; no workflow edit here |
| 7 | Before and after comparison | Proven | #880: 47 to 79 |

Unmet: criteria 3 and 4 (owner waiver or rewording needed).

## Validation

| Check | Result |
| --- | --- |
| `python3 -m pytest -q test_prepare.py` (`.github/rubric/scripts`) | 76 passed |
| `python3 -m pytest -q test_safe_output_runtime.py` | 10 failed, 7 passed, 7 skipped; adverse, pre-existing, recorded as follow-up, not fixed |
| `prepare.py context` run | rc 0; counts retained |
| Markdown link check of the research note | all links resolve |
| mypy, ruff, accessibility and content tests | not applicable: no Python or web file changed |
| `rpi-checks.py --all` | not run (FULL tier not triggered) |
| Hosted CI | not observed; nothing pushed |
