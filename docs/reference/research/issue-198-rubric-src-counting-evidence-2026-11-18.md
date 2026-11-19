---
title: Issue 198 rubric src counting and mvp stop, state and remaining criteria
description: Fresh local evidence for #198 acceptance criteria, with the two criteria that cannot be proven for the demo
ms.date: 2026-11-18
---

Scope: the synthetic demo, desktop only. Docs and evidence only; no `src/` change, so the focused tier applies.
No Azure resource was needed or created. Retrieval date for all GitHub data: 2026-11-18.

## Current state on main (branch base 68aed5946)

| Fact | Evidence |
| --- | --- |
| Registry has no `mvp/` or `prototype/` glob | `grep -n '"mvp\|prototype' .github/rubric/artifacts.json .github/rubric/rubric.json` returns nothing; `git ls-files` matches 0 paths under `mvp/` or `prototype/` |
| `solution-code` includes `src/**/*` and excludes vendor, data, egg-info, build | `.github/rubric/artifacts.json` lines 28-36 |
| Dropped by #292 (src excludes, 2026-10-15), #295 (prototype glob, 2026-10-15), #851 (dead mvp excludes, 2026-11-03) | `gh pr view` merge dates and bodies |
| `rubric_version` is 2, unchanged | `.github/rubric/scores/latest.json` |
| Latest recorded score 79/100, Pass with Merit, floors met | `latest.json` (commit 20f0b166f, run 44255173449: push, main, success, 8 of 8 jobs successful) |
| Solution-code criteria A1 5, A3 5, A4 5, A5 5, A6 5, A7 5, B6 4 | `latest.json`; the 47 baseline was A1 4, A3 5, A4 5, A5 3, A6 3, A7 4, B6 4 (#292 body) |
| `prepare.py context` counts src tests, pyproject and Dockerfiles | Local run, base `HEAD~1`, event `workflow_dispatch` (raw output not retained): `solution-code` file_count 949 (the list is capped at 500; within it 297 test files, 3 pyproject.toml, 6 Dockerfiles, 0 `mvp` paths, 0 vendor or data paths). Raw `git ls-files src` excluding vendor, data, build and egg-info gives 934 files |
| Rubric script tests | `python3 -m pytest -q test_prepare.py` in `.github/rubric/scripts`: 76 passed (raw output not retained) |

## Per-criterion status

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Baseline total and solution-code criteria recorded | Proven (ticked) | 47/100 at commit fa730d6 (the #292 body; the issue body names `9261c5c`, a discrepancy not resolved here) and scores in #292 body; re-confirmed above |
| 2 | src test and Dockerfile coverage in own registry PR | Proven (ticked) | #292 merged; `src/**/*` already covers tests, pyproject and Dockerfiles (local count above) |
| 3 | Each dual-window migration PR records total, dip cause, recovery expectation | Unproven, cannot be proven | See below |
| 4 | Cut-over registry PR removes mvp globs and `prototype/deploy`; deletion PR scored by old registry first | Unproven, cannot be proven | See below |
| 5 | README rubric section updated; 19 failures reassessed | Proven (ticked) | #705; README lines 82-90, 591-615 |
| 6 | Recompile lock file if workflow Markdown changes | Proven (ticked) | #748 changed `rubric-score.md` and `rubric-score.lock.yml` together |
| 7 | Before and after comparison with recovery expectation | Proven (ticked) | #880 records 47, 77, 77 in `docs/architecture/cutover-evidence-pack.md` |

## Why criteria 3 and 4 cannot be proven

Criterion 3. The migration PRs #295, #300 and #302 (all merged 2026-10-15) did record a source-file or test-count baseline
(747 before and after for #300 and #302) and #295 stated "no dip is expected", but none recorded the rubric total against 47 with a
cause and recovery expectation. Owner decision D1 (2026-11-01, #748) later moved score recording to main only, not per PR, so the
per-PR clause is now contradicted by current policy as well as being unrecoverable after merge. A PR body cannot be written
retroactively, and the rubric workflow scores main only, so no per-PR rubric total exists.

Criterion 4. The registry edits were distributed: #292 (excludes), #295 (prototype glob, with the prototype deletion in the same PR),
#851 (dead mvp excludes). No dedicated cut-over registry PR followed an old-registry-scored deletion PR, and the sequence
is a past ordering. Current absence of the globs is proven; the ordering is not.

Fresh live Azure, sign-in or browser proof has no bearing on either criterion, so none was gathered. The relevant demo-level
outcome (no dip, 47 to 79) is proven by criteria 1, 5 and 7.

## Owner decision needed

Waive or reword criteria 3 and 4 as historically unsatisfiable (suggested wording: "current registry has no `mvp/` or
`prototype/` globs and the before and after score shows no dip", already proven), then close #198 citing #292, #295, #705, #748, #851
and #880. Until then #198 stays open at 5 of 7. This note does not tick any box.

## Source evidence

* `gh issue view 198` body and comments (closure audits 2026-10-31, 2026-11-02, 2026-11-05, 2026-11-15).
* `gh pr view` for #292, #295, #300, #302, #705, #748, #851, #880.
* `.github/rubric/artifacts.json`, `scores/latest.json`, `README.md`.

## Evidence limits

* The `prepare.py context` output (file_count 949, 297 test files, 3 pyproject.toml, 6 Dockerfiles, 0 `mvp` paths) and the pytest result (76 passed) were not saved; they are unrecorded local runs and cannot be re-checked from this diff.
* The baseline commit is `fa730d6` in the #292 body and `9261c5c` in the issue body; the contradiction is open.
* Rows resting on GitHub pull request bodies and `latest.json` are traceable to those sources.
