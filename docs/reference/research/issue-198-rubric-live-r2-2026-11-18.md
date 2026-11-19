---
title: Issue 198 rubric src counting and mvp stop, live r2 audit with retained raw output
description: Second 2026-11-18 audit of the rubric registry and workflow against #198, with raw outputs kept and a new finding on stale mvp references
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Audit and evidence only; no workflow, registry or `src/` edit, so the focused tier applies.
No Azure resource was needed or created, and no sign-in credential was read. This note extends
[the earlier 2026-11-18 note](issue-198-rubric-src-counting-evidence-2026-11-18.md), whose raw outputs were not retained.
Raw outputs are in [issue-198-rubric-live-r2-2026-11-18/](issue-198-rubric-live-r2-2026-11-18/). Base commit a39ae2339.

## Retained evidence

| Check | Command (run at repository root unless stated) | Result | File |
| --- | --- | --- | --- |
| Registry has no mvp or prototype glob | `grep -n -E 'mvp\|prototype' .github/rubric/artifacts.json .github/rubric/rubric.json .github/workflows/rubric-score.md` | no match; `git ls-files mvp prototype` gives 0; neither directory exists | [registry.txt](issue-198-rubric-live-r2-2026-11-18/registry.txt) |
| `solution-code` globs | same file | include `src/**/*` plus the retrofit generator; exclude vendor, `src/**/data/**`, build, egg-info, caches | [registry.txt](issue-198-rubric-live-r2-2026-11-18/registry.txt) |
| src counting in `prepare.py context` | `python3 .github/rubric/scripts/prepare.py --root . --base-ref HEAD~1 --event workflow_dispatch --out <tmp> context` | `solution-code` file_count 949; of the 500 listed paths 297 are tests, 3 `pyproject.toml`, 6 Dockerfiles, 0 mvp or prototype, 0 vendor or data; baseline total 79 | [solution-code-count.txt](issue-198-rubric-live-r2-2026-11-18/solution-code-count.txt), [prepare-context.log](issue-198-rubric-live-r2-2026-11-18/prepare-context.log) |
| Rubric script tests | `python3 -m pytest -q test_prepare.py` and `test_safe_output_runtime.py` in `.github/rubric/scripts` | `test_prepare.py` 76 passed; `test_safe_output_runtime.py` 10 failed, 7 passed, 7 skipped | [pytest.txt](issue-198-rubric-live-r2-2026-11-18/pytest.txt) |
| Score state | `.github/rubric/scores/latest.json` | total 79, `rubric_version` 2, A1 5, A3 5, A4 5, A5 5, A6 5, A7 5, B6 4 | [latest.txt](issue-198-rubric-live-r2-2026-11-18/latest.txt) |
| Delivery PRs | `gh pr view` for #292, #295, #300, #302, #705, #748, #851, #880 | all merged 2026-10-15 to 2026-11-03 | [prs.txt](issue-198-rubric-live-r2-2026-11-18/prs.txt) |
| Workflow files | `ls .github/workflows` | `mvp-ci.yml` and `mvp-validation.yml` still exist | [workflows.txt](issue-198-rubric-live-r2-2026-11-18/workflows.txt) |

## New finding: stale mvp references outside the registry

The 10 failures in `test_safe_output_runtime.py` are all `test_tracking_only_changes_do_not_trigger_workflows`.
Two kinds of cause appear in the output:

* `KeyError: 'push'` or `'pull_request'`: the test reads `config["on"][event]` for every workflow file, and some workflows do not declare both triggers (`src-ci.yml` declares only `pull_request` and `workflow_dispatch`).
* One `assert any(...)` failure: the test uses the retired path `mvp/zavaforward_mvp/app.py` as its sample source file, so a trigger list that no longer names `mvp/` cannot match it.

The earlier README reassessment (#705) counted 19 and then 17 failures; the current count is 10 in a different test. This does not change the registry criteria, but it shows the mvp stop is not complete in the test fixture, and the two `mvp-*.yml` workflows remain. Neither is in the #198 acceptance criteria and neither was edited here. Both are recorded as follow-ups.

## Per-criterion status

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Baseline total and solution-code criteria recorded | Proven (ticked) | 47/100 baseline in #292; current 79 and per-criterion scores in `latest.txt`. The baseline commit is `fa730d6` in the #292 body and `9261c5c` in the issue body; unresolved |
| 2 | src test and Dockerfile coverage in its own registry PR | Proven (ticked) | #292 merged; `src/**/*` counts 297 tests, 3 `pyproject.toml`, 6 Dockerfiles in the retained run |
| 3 | Each dual-window migration PR records total, dip cause, recovery expectation | Unproven, cannot be proven for the demo | Merged PR bodies (#295, #300, #302) record file or test counts, not the rubric total against 47. D1 (#748) moved score recording to main only, so no per-PR total exists or can be created after merge |
| 4 | Cut-over registry PR removes mvp globs and `prototype/deploy`; deletion PR scored by the old registry first | Unproven (ordering), cannot be proven for the demo | Globs are absent now (`registry.txt`). They were removed across #292, #295 and #851, not in one cut-over PR after an old-registry-scored deletion PR |
| 5 | README rubric section updated; pre-existing failures reassessed | Proven (ticked), with caveat | #705; README lines 591-623. The failure count has since changed to 10 (see the new finding) |
| 6 | Recompile lock file if workflow Markdown changes | Proven (ticked) | #748 changed `rubric-score.md` and `rubric-score.lock.yml` together; no workflow edit in this run |
| 7 | Before and after comparison with recovery expectation | Proven (ticked) | #880 in `docs/architecture/cutover-evidence-pack.md`: 47 to 79 |

Live Azure, browser and sign-in proof have no bearing on any criterion, so none was gathered.

## Owner decision needed

Waive or reword criteria 3 and 4 as historically unsatisfiable (suggested: "current registry has no `mvp/` or `prototype/` globs and the before and after score shows no dip"), then close #198. This note ticks no box.

## Follow-ups (not in #198)

* Replace the `mvp/` sample path and the both-triggers assumption in `test_tracking_only_changes_do_not_trigger_workflows`.
* Decide whether `mvp-ci.yml` and `mvp-validation.yml` should be retired now that `mvp/` is gone.

## Evidence limits

* Counts rest on a local `prepare.py` run on one base ref; the listed file set is capped at 500 of 949.
* GitHub data retrieved 2026-11-18 and reflects PR state at that time.
* Not checked: hosted CI for this commit, and whether the PR bodies were edited after merge.
