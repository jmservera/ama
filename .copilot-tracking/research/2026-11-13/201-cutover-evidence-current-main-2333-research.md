<!-- markdownlint-disable-file -->
# Research: Issue #201 cut-over evidence at current main (2333)

* Task: `201-cutover-evidence-current-main-2333`; branch `docs/demo-201-cutover-evidence-pack-2333`; base `origin/main` `3033dc9c21e57c7f86eca3882fffaf7e9a025033`.
* Research disposition: `executed` (focused read of the named sources and live issue).
* Planning Readiness: `Ready`.

## Sources read

* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md` (context only; memory is not evidence).
* `docs/architecture/cutover-evidence-pack.md` (8339 lines; latest sections end with the 2026-11-13 owner sign-offs and the demo feature-wave stabilization checkpoint).
* `docs/architecture/mvp-to-src-parity-matrix.md` (the task named `migration-parity-matrix.md`; that path does not exist, this is the actual file).
* `gh issue view 201 --comments` (live, OPEN, read 2026-11-13).
* `tools/rename-zava-tests.py` (324 lines, 25 tests), `.github/workflows/src-ci.yml` (lint runs `ruff check . && ruff format --check .` per project with `ruff==0.17.1`).

## Findings

* Issue #201 criteria: ticked are Layout ADR, `prototype/` retired, parity matrix complete, rubric tracks `src/`, docs/index/log, archive tag. Unticked: tests migrated with equal or greater coverage in CI; CI/Docker/Bicep repointed with a deployed healthy `src/` build; dependent epics with no old-path work; private `mvp/data/` backup; owner sign-off in the issue.
* The pack records the 2026-11-13 owner sign-offs (prototype mapping, `v0.21.0` archive retirement, workflow check set) and states live deployed parity and the private-data backup stay pending the live redeploy. The Azure demo sync is unperformed.
* The latest recorded merged-wave checkpoint pins `34b11967b`. No section pins current main `3033dc9c2` or reruns the local cut-over criteria on it.
* `git ls-files mvp prototype` is empty at `3033dc9c2`; no tracked path or import uses `mvp`, `prototype` or `zavaforward_mvp`.

## Gaps and conflicts

* The task named `migration-parity-matrix.md`; the real file is `mvp-to-src-parity-matrix.md`. No content conflict.
* Open PRs #1575 and #1576 touch `docs/reference/log.md` and the WCAG baseline; this task must not edit them (so no log entry is appended here).

## Recommendation

Append one dated current-main checkpoint to the pack that separates proven local criteria from the live Azure and owner gates, with no tick, closure or sign-off claim.
