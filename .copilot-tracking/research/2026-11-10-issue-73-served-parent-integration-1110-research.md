---
title: Issue 73 served parent integration of child 1357 with current main - research
ms.date: 2026-11-10
---

## Research opening (2026-11-10T05:26Z, written before substantive research)

* Task: parent #73 current-main integration of already-reviewed child #1357. Not a new feature.
* Worktree: issue-73-served-parent-1110, branch feat/demo-served-exceptions-73-1110.
* Starting parent head: b0af68a3e87faf535d8cdddc3357d4cfd32c7adf (clean).
* Fetched origin/main pin: 4244e84e763e6e01dd6012fcb9b650dae8d58e9d.
* Research disposition: executing. Planning Readiness: not yet determined.
* Opening checks only so far: git status, branch, head, clock, helper --help.
* Tier: owner DEMO TARGETED (not the full or --changed gate).
* Merge of main is deferred until after a genuine plan and the implement-start witness event.

## Findings (research executed 2026-11-10, after the research-open witness event)

* Read after opening: case original, memory, reference index head, src/README (commands, heavy-lock guidance), child handoffs 135 C4, C5 and C5 review record, core README slice 4, both CLI entry points. The addendum was grepped for #135/#1357 references (none); no addendum change is planned.
* Parent b0af68a3 is the merged child #1357 (merge-base with main a61bebe6). Main 4244e84e has three commits beyond it: #1355 (Core discovery-demo CLI in core `__main__.py`, new module and test, core README slice 4), a rubric score commit, and #1358 (witness tool and its tests, coordinator agent, tracking records).
* File overlap between parent changes (14 non-tracking files: Core exception_register, import_refusals, sqlstore, store; Importer __main__, exceptions, pyproject, README, test; API role-screens.js and two tests; docs/reference/log.md) and main changes: none. `git merge-tree` trial of main into the parent reports no conflict (tree 7567de89). Main did not touch docs/reference/log.md, so the log stays append-only with a new entry.
* Semantic interaction: the two CLIs live in different entry points (`python -m zava_forward.core discovery-demo` versus `python -m zava_forward.importer`), share no module and no argument parsing. Core `__main__` imports only version and, on the single `discovery-demo` argument, the demo module; the parent did not touch it. Core store, sqlstore, exception_register and import_refusals changes are not imported by discovery_assistant_demo (to be re-verified by tests after the merge).
* Optional-driver typing: Importer pyproject mypy override for `mssql_python` came from child C5 and is preserved. Must be proven with the driver absent (CI-shaped) and present.
* Environments: private venvs /tmp/issue73-1110-venv-full (core[sql,dev], agents, api[dev], importer[dev]) and /tmp/issue73-1110-venv-nosql (core[dev], importer[dev], driver absent), declared pins only (ruff 0.17.1, mypy 2.4.0, mssql-python 1.15.0, playwright 1.64.0). Python 3.12.3. Child venvs are bound to another worktree and are not reused.
* Heavy resources: /tmp/ama-rpi-heavy.lock had no holder at 05:26Z (lsof empty). MSSQL image mcr.microsoft.com/mssql/server:2022-latest sha256 cf8f0ab2 present locally; no containers running. Use own labelled container under the nonqueued lock, remove only it.
* Private data: synthetic fixtures only, explicit temporary ZF_DATA, never the owner default dataset.
* Corrections: parent correction balance unknown; child 135 C5/5 exhausted and not reset. A new source defect would be returned as evidence, not corrected here.
* Old child observations (C4 served browser, MSSQL) are references only and are not claimed for the merged head; they are re-run on the merged head.

## Planning Readiness

Ready. Research disposition: executed. No blocker. Tier: owner DEMO TARGETED.
