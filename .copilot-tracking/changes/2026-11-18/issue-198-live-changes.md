---
title: Issue 198 live changes
date: 2026-11-18
---

Tier: FOCUSED (docs and evidence only; no `src/`, SQL, infra or security change). Branch test/rubric-src-counting-live-20261118T1129Z.
Divergence recorded: the docs were drafted before this file and the `implement-start` witness call; no source code was touched.

## Files

* `docs/reference/research/issue-198-rubric-src-counting-evidence-2026-11-18.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Baseline and solution-code criteria recorded | Proven (#292; reconfirmed) |
| 2 | src test and Dockerfile coverage registry PR | Proven (#292; local `prepare.py context` run) |
| 3 | Per-migration-PR total, dip cause, recovery | Unproven: historical, unrecoverable; contradicted by D1 (main-only scoring) |
| 4 | Dedicated cut-over registry PR after old-registry deletion scoring | Unproven: ordering is historical; end state (no globs) proven |
| 5 | README updated, 19 failures reassessed | Proven (#705) |
| 6 | Lock file recompiled with workflow Markdown | Proven (#748) |
| 7 | Before and after comparison and recovery | Proven (#880; 47, 77, 77; now 79) |

## Validation

* `python3 .github/rubric/scripts/prepare.py --base-ref HEAD~1 --event workflow_dispatch --out .copilot-tracking/evidence/2026-11-18/issue-198-live/prepare-out context`: ran locally (the original run wrote outside the repository); solution-code file_count 949, no mvp paths; raw output not retained.
* `python3 -m pytest -q test_prepare.py` (in `.github/rubric/scripts`): 76 passed (raw output not retained).
* Not run: rpi-checks (not required at focused tier, never `--all`), mypy/ruff (no Python changed), Azure/browser (not relevant).
* Hosted CI: not observed (no push permitted).

Unmet: criteria 3 and 4, pending owner waiver or rewording.
