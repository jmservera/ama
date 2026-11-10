---
title: Issue 109 actual remote parent and main adoption details
ms.date: 2026-11-10
task_id: 109-actual-parent-main-1110
---

## Phase details

* Phase 1 Research: done, executed, Ready.
* Phase 2 Plan: plan, details, one critique, prospective changes declaration.
* Phase 3 Implement: pin recheck, `implement-start`, single ordinary two-extra-parent merge without commit, invariants, selected checks, actuals, `implement-done`.
* Phase 4 Review: one self-review (not independent), `review-done`, single commit with noreply author and committer and Copilot trailer, literal 40-hex HEAD, `commit-complete`, `verify` exit read directly.

## Pins

HEAD `20addb9ae1d7c652ecf1882401e54523fee97ba0`; squash `bd2a6494464b451572fc3dc7c8d53c549e0f9dad`; main `64c3f9191a2ffa97ef2dc07245422333ad4d6585` (tree `8fbdaec7d138e360e9e460ad714742cb78b4d621`); reviewed child `6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2` (content equal to the squash). Dry runs: HEAD+squash tree `ce82f2f6...` (equals HEAD tree), HEAD+main tree `d45426bd28850d893622b48df1a2649a13135992`.

## Selection rationale

Changed inputs from PR #1400 are Core aftercare modules, `projection.py`, `sqlstore.py`, API `server.py`, `workbench.py`, front-end `app.js`, `index.html`, `aftercare.js`, scenario and workbench manifests and two scoped pyproject exemptions. The selected tests cover the sensor-review consumers of the shared files (draft, analysis, store, manifest), the new aftercare Core and API tests that exercise shared files, route inventory, accessibility baseline and workbench as consumers of `server.py` and `index.html`, both configured type checks, the sensor browser (served UI) and the SQL draft selector (changed SQL store).

## Heavy admission

One `flock -n /tmp/ama-rpi-heavy.lock` attempt per heavy check (browser, MSSQL); on BUSY record the holder from the lock file or process list and stop that check, no wait, queue, spin or kill.
