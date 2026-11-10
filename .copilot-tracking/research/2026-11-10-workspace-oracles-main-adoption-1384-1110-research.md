---
title: Issue 1384 main adoption research
description: Research for adopting current origin/main into the held 1384 candidate before final validation
ms.date: 2026-11-10
ms.topic: reference
---

## Scope

Completion of the original held initial scope (integration and validation) for issue 1384 after dependency #1388 was delivered. Not a new oracle correction. Original frozen candidate `3f1fa4810a79b8689aaa8d8e167aa6470b262420` stays in ancestry; original research, plan, critique, changes, review and red evidence are preserved unchanged.

## Research Disposition

* Disposition: executed (fresh fetch and merge simulation). Planning Readiness: Ready.

## Evidence

* `git fetch origin main` observed `origin/main` = `111847191d1fde5e8ea18c30c999e99f33721aff` (PR 1390 merge). Branch HEAD `3f1fa48` was clean on `fix/demo-workspace-retry-oracles-1384-1110`; merge-base with main is `caaf989148aff21ed8ecb5b71eb0be75b29c16de`; main is 7 commits ahead.
* Main changed `src/api/checks/workspace_scripts_browser_check.py` (+11 -1): `from time import monotonic`, `ROUTE_DELIVERY_DEADLINE_S = 5.0`, and a bounded 10 ms poll before the exact `assert len(pending) == 1` in `delayed_companion`. This is the #1388 fix for the race diagnosed in `handoff-1384-delayed-diagnostic-1314.md` (route delivery after DOM insertion).
* Our candidate changed the same file in two other places (import of `functools.partial`, constants `TERMINAL` and `REVISIT`, `exhaustion`, `exhaustion_controls`). The candidate did not touch `delayed_companion`.
* `git merge-tree --write-tree HEAD origin/main` reports exactly one conflicted file, that file, with two purely additive hunks: the import block (`partial` versus `monotonic`) and the constants block (`TERMINAL`/`REVISIT` versus `ROUTE_DELIVERY_DEADLINE_S`). Both sides' lines are wanted; no semantic interpretation is needed. All other merge content is non-overlapping.
* Main also changed `app.js` (+9), `panels.js`, `style.css`, other checkers and tests. `app.js` changes do not touch `SCRIPT_RETRY_DELAYS` or `workspaceScript*` (grep of the diff: 0 matches), so the derived oracle contract is unchanged; the unit test that runs the real loader in a Node VM will confirm this on the merged tree.
* Our other touched files (`employee_workspace_browser_check.py`, `script_retry.py`, `tests/test_workspace_scripts.py`) are unchanged on main.
* Manifest assessment: `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` binds `src/api/checks/workbench_browser_check.py` as the `recipe` source. Main already updated that hash for its own change to that file (`9a975543...`). This task does not modify that file or `workbench-manifest.json`, so no manifest update is needed; the merged file must equal main's version, which will be verified by sha256.

## Unknowns preserved

* The original baseline `sign_out` empty failure (`04-after-workspace_scripts.*`) remains UNKNOWN. Later greens do not explain it. The route-delivery diagnosis is not retried.
* Whether whole `workspace_scripts_browser_check` is green on the merged tree is not known until it is run once.

## Planning Readiness

Ready. One plan: ordinary `--no-ff` merge of `origin/main` after `implement-start`, resolve the two additive hunks keeping both, no other source edit, validate once with the original whole commands.
