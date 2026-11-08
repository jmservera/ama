---
title: Issue 80 r11 research, browser harness hygiene and cleanup preservation
description: Prospective research for a harness correction and a preservation proof, no deletion
ms.date: 2026-11-06
---

* Task: excel-transition-80-r11-harness-hygiene, parent r10 execution. Intake HEAD 1fa335435290b40e2cdd49630adfd312065a424e, tree 44ae1a770232ed8e6985692c01e59e5c72f3acc2, main bb3a3b03, parent ead177ef unchanged.
* Disposition: executed (read-only). Planning Readiness: Ready.
* Worktree state at intake is NOT clean: ignored status lists exactly three `__pycache__` directories (agents, api, core under `src/*/src/zava_forward/`) and an empty repo-root `.venv` (ignored by `.gitignore` line 2) exists. Tracked status is empty.

## Cause (source evidence)

* `src/api/checks/design_system_browser_check.py` `main()` line 234 does `(ROOT / ".venv").mkdir(exist_ok=True)` and line 235 puts the scratch tempdir under `ROOT / ".venv"`. The scratch is deleted on exit but the parent `.venv` stays. This is the source of the empty `.venv`.
* Same file: the child server environment is built from only `PATH`, `HOME`, `LANG` (about line 244), plus `PYTHONPATH` of the worktree `src/{core,agents,api}/src`. `PYTHONDONTWRITEBYTECODE` is dropped, so the child server `python -m zava_forward.api.server` writes `__pycache__` beside the worktree sources. This is the source of the three ignored directories. The r10 parent process used `-B`, so it wrote none.
* `main` is shared by many checks (`case_journey_browser_check`, chat, employee and others), and already has an `env_overrides` keyword, but no scratch-location control.
* The child `PYTHONPATH` points at this worktree's sources by design; that import path is honest. The r10 parent environment used system Python plus PYTHONPATH rather than pip-installed distributions of this candidate (global editable installs point at another checkout). That is an environment-evidence problem for the later admitted run, not a source bug.

## Smallest correction

* In the shared harness only: pass `PYTHONDONTWRITEBYTECODE` and `PYTHONPYCACHEPREFIX` through to the child when the caller has set them, and honour an optional `ZF_BROWSER_SCRATCH` directory (external) for the scratch parent instead of `ROOT/.venv`. Default behaviour with neither set is unchanged, so every other check keeps its present behaviour. Two small pure helpers make the boundary testable without starting a server or browser.
* Not chosen: fake interpreter, sitecustomize, deleting caches in the harness, editing `.gitignore`, changing the schema check's assertions.

## Cleanup preservation findings

* `tools/tracking_retention.py` `approved_paths()` is hardwired to the seven finite PR 438 preview groups and `build`/`prune` operate on that manifest; it cannot select these exact generated paths. It is reused only as policy guidance. Policy sections used: Explicit Cleanup Contract (finite per-run manifest, full tracking snapshot archive outside the checkout with symlinks opaque, member types/sizes/SHA-256, full readback, restore to a new empty external location, protected-byte comparison, no age or glob rule).
* Inventory at intake: agents `__pycache__` 5 members, api 5, core 61, `.venv` 0 members. Directory mtimes 13:37:40 to 13:37:46 on 2026-11-06 coincide with the r10 run, and the r9 final status had 0 ignored entries and the r10 handoff recorded the appearance; that is the provenance, not age.

## Limits

* No deletion is authorised. No browser rerun, server, SQL, lock or install. The harness correction cannot be proven by a browser run here; only unit checks of the helpers.
