<!-- markdownlint-disable-file -->
# Details: #74 home and building evidence integration (issue-74-evidence-integration-0424)

Date 2026-11-13. Plan: [plan](../../plans/2026-11-13/issue-74-evidence-integration-0424-plan.md).

## Phase 2 section content (docs/architecture/cutover-evidence-pack.md, appended at the end)

Heading: `## Issue 74 home and building separation evidence integration (2026-11-13, Refs #74 #440)`. Subsections: identities; instruments kept separate (table); exact commands and results; chronology and preserved failures; cleanup and isolation; original critiques and adverse items; limits and what is not claimed; artifact links (relative, to `.copilot-tracking/...`).

## Facts to state (each re-read from artifacts or raw outputs)

* Pin and tree; frozen heads; tracking-only difference.
* Units: two commands, cwd, Ran 8 / Ran 6, OK, zero skips, 8 + 6 named tests, editable installs of this checkout, Python 3.12.3, first missing-package failure and bad API selector preserved.
* Home browser: command `home_case_browser_check`, 24 PASS = 1 server + 23 browser and axe, exit 0, zero skips, axe 4.10.3 COMPLETE, ZF-2 and ZF-3 only, zero JS errors, zero post-sign-in writes, lock 04:09:42Z to 04:10:11Z, MemAvailable 4.95 GiB, Chromium 156.0.8078.4, `run2.log` identical to `run-final.log`, run 1 failure preserved, retrospective plan file.
* Building observation: one route, case-home ZF-2 then `Open full building context` to `#/building/SYN-B1`, API 200, six distinct sections, markers, linked ZF-2 and ZF-3, home-only sentinels present on home and absent from building main, sibling sentinels absent already on home so prove nothing, zero controls, zero non-safe or foreign requests, zero JS errors, lock 04:17:28Z to 04:17:32Z, MemAvailable 4.87 GiB, own process group 0 remaining, `observe.py` unexecuted draft.

## Validation

Link review of every added relative link by path existence; `git diff --check` on staged and untracked content before commit; ASCII-only added lines; scope check of staged, unstaged and untracked files before commit and again of the committed diff `git diff --stat <pin>..HEAD` afterwards scope equals 26 imported tracking files, this task's seven tracking files, pack, index, log.
