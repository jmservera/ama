---
title: Issue 151 live round 2 changes
ms.date: 2026-11-18
---

## Changes

* Added `docs/reference/research/issue-151-live-wcag-axe-evidence-r2-2026-11-18.md`.
* Added index row in `docs/reference/README.md` and log entry in `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-151-live-r2/` (script, summaries, 16 raw axe gz files, screenshots, adverse run 1, trap probe).
* Added `-r2` research, plan, details, critique, changes, review and state artifacts. Original `issue-151-live-*` artifacts are unchanged.
* No `src/` change. Tier FOCUSED. No Azure resource created or changed; nothing to delete.

## Per-criterion result (issue #151, demo scope)

| # | Criterion | Ticked in issue | Result for the demo |
| --- | --- | --- | --- |
| 1 | Target level and scope decided and recorded | Yes | Not re-tested |
| 2 | Audit covers eight dimensions | Yes | Not re-tested |
| 3 | Automated checks run in CI against key screens | Yes | Proven live: 16 screens, 0 axe violations (WCAG 2.0 to 2.2 A and AA tags), raw output retained. Hosted CI not read |
| 4 | Manual screen-reader and keyboard checks for each role workflow | No | UNPROVEN, stays unticked. Keyboard and 320 px reflow automated only, for one employee role and the resident app. Screen reader is person-run, production-only (#1907). Seven other role workflows not signed in |
| 5 | Accessible equivalents for map, charts, tables | Yes | Not re-tested |
| 6 | Accessibility statement draft without conformance claim | Yes | Not re-tested; no claim added |

## Validation

* Credential scan: literal match of every value in the three credential files against all retained evidence (gz decompressed): 0 hits.
* Link, diff and staging checks are recorded in the review.
* Not run: `src` tests, mypy, ruff (no code changed); `rpi-checks.py` (not applicable to FOCUSED docs tier here).

## Unretained or limited results

* Contrast sampling, Tab-walk and reflow results are retained only as summary counts; passes and inapplicable axe results were not retained; Azure revision and digest not re-read.
* Witness note: `research-open` (seq 2) was recorded while the mandated state file had been overwritten in error; it was restored from git and later boundaries use `issue-151-live-r2-state.json`.
