---
title: Issue 80 capacity C4 instrumented validation, plan
description: Plan for one observed whole capacity browser run on unchanged source 2cc34027
ms.date: 2026-11-10
---

## Objective

Execute ONE whole `capacity_browser_check --axe` on unchanged HEAD `2cc34027` under an external passive observer, record the actual result and the first failure if any. No source change, no repeat, no C5.

## Phases

* [ ] Phase 1: pre-run integrity (clean tree, HEAD/tree pin, checker and web file hashes, venv import origins, host load, heavy lock not held by this author).
* [ ] Phase 2: one execution of `observer.py` with direct Python exit capture to a file; raw stdout/stderr log and incremental event log preserved.
* [ ] Phase 3: post-run reading: milestones reached, exit, first failure, served-vs-owned hashes, ZF_DATA, delayed-401 iterations and empty-capacity assertion actually reached or not.
* [ ] Phase 4: native review after the execution, handoff, commit of own tracking records only.

## Success and stop rules

* Pass requires direct Python exit 0 AND milestones showing both delayed-401 iterations (packages, workorders) and the empty-capacity zero-anchor scenario executed with no skips. Anything else is reported exactly as observed.
* Lock busy, missing dependency or observer import failure: stop, preserve the adverse result, no install, no retry. Failure of the checker: keep primary exception and exit, no second run.
* Carried same-source evidence (Ruff, format, Node, API11, static60 from the C4 commit) is labelled carried, not re-run.
