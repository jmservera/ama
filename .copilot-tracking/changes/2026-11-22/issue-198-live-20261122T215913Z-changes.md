---
title: Issue 198 changes 20261122T215913Z
ms.date: 2026-11-22
---

Docs-only, focused tier (no src, workflow or registry change). Added the research note
docs/reference/research/issue-198-rubric-live-20261122T215913Z-2026-11-22.md, raw outputs in
docs/reference/research/issue-198-rubric-live-20261122T215913Z/, an index row and a log entry.
No Azure resource created, no credential read. Validation: `test_prepare.py` and `test_safe_output_runtime.py` 84 passed, 16 skipped.

## Per-criterion table

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Baseline and solution-code criteria recorded | Proven (ticked) | 47/100 baseline in #292; `latest.json` |
| 2 | `src/` test and Dockerfile coverage in its own registry PR | Proven (ticked) | #292 merged |
| 3 | Dual-window PRs record total, dip cause, recovery | Unproven | #295, #300, #302 carry test counts only; #748 moved scoring to main only, so it cannot be created retroactively |
| 4 | Cut-over registry PR removes `mvp/` and `prototype/deploy` globs | Partly proven | No such glob remains (registry.txt); #295 removed the prototype glob with a dip statement, #851 dropped dead mvp excludes; a single dedicated cut-over PR after an old-registry-scored deletion PR is unproven |
| 5 | README updated; failures reassessed | Proven (ticked) | #705; 0 failures now |
| 6 | Lock file recompiled if workflow changes | Proven (ticked) | #748 |
| 7 | Before and after comparison with recovery | Proven (ticked) | #880: 47 to 77; now 79 |
