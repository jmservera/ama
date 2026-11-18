# Research: #1259 unusable ranking archive paths (live demo lane)

Date: 2026-11-18. Disposition: executed. Planning Readiness: Ready.

* Source fix and regressions are already on main at `cd687abad` (#1328); `ranking_publication._names` classifies non-directory, dangling and stat failure as `OSError`, and the runner `_verify` turns it into the unreadable problem.
* Unticked: AC4 (failing-first evidence, literal) and AC5 (FULL receipt, exact-head assessment, hosted checks).
* Azure is irrelevant (filesystem logic); no live action taken.
* Output: docs/reference/research/2026-11-18-ranking-archive-unusable-1259-failing-first.md.
