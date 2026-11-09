---
title: Issue 80 r15 research, ancestor alignment to advanced main
description: Prospective research for a normal local merge of current origin/main into the issue 80 topic after main and the parent integration branch advanced
ms.date: 2026-11-06
---

* Task: excel-transition-80-r15-main-alignment, parent r14. Intake HEAD 2e05558e6cd7cc92e194bba2024b6d1463269a40, tree 902a7f970abfd1d55cbe70758331c9f96edce316, branch feat/checklist-list-export-80. Ignored-inclusive status is empty at intake.
* Disposition: executed (read-only). Planning Readiness: Ready.

## Facts observed after a fresh `git fetch origin`

* origin/main is 56eec736906774ef56d8c9a66ed7f3f9c1e520c6 (PR 1236, source 1204 agent and tracking only). The previous FULL receipt r69 was verified against bb3a3b03; it is genuine historical evidence and is not current-base evidence now.
* The parent integration branch feat/case-workbench-integration-73 (local and origin) is 56eec736906774ef56d8c9a66ed7f3f9c1e520c6, fast-forwarded and empty, so the old parent pin ead177ef is no longer the branch tip. The tip is not an ancestor of the topic HEAD yet (`merge-base --is-ancestor` exit 1); merging origin/main will make it one.
* Merge base of HEAD and origin/main is bb3a3b03. `git diff HEAD...origin/main` has 226 files. Outside `.copilot-tracking/` there is one file: `.github/agents/ama-backlog-delivery-coordinator.agent.md`. The topic's own non-tracking changes (src/api, src/core files and tests) share no path with it.
* `git merge-tree --write-tree` of HEAD and origin/main completes without conflict (tree 954c9f0dbb8a58060cc92c877c3aed18e972e7be). No source-intent conflict exists.

## Scope

* Only an ancestor alignment: a normal local `--no-ff` merge commit of the freshly resolved origin/main into this topic. No rebase, no history rewrite, no source, test, infra, tool, runtime or topic behavior change, and no refactoring. The incoming main file `.github/agents/ama-backlog-delivery-coordinator.agent.md` changes coordinator admission, liveness and approval instructions; the merge brings that merged-main content in unchanged, so it is not policy-neutral, and it activates nothing for the export feature. r68 failure, the r14 docstring correction and r69 receipts stay unchanged.
* Proof targets after the merge: first parent is the old head, second parent is origin/main, the parent branch tip and old head are ancestors, and every non-tracking path differs from the old head only by the merged main file, with source, test, infra, tool and workflow blobs equal to either the old head or main.

## Limits

* Light checks only: provenance equality, existing export regressions, configured Ruff, format and mypy, own-source imports, link and diff checks, in an owned external environment under `/mnt/ama-gates/restart-1106-80-align/`. No FULL, SQL, browser, image, stress or scan run; no receipt substitute. Prior FULL is not carried to the new head; a new coordinator-admitted FULL and independent exact-head assessment stay pending. Every-list export, owner thresholds and human, privacy, legal, operational and Azure acceptance stay unproven.
