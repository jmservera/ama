---
title: Issue 1231 r10 plan (normal local merge of the named parent)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 about 20:45Z, before any merge. It follows the r10 research. Governing design for the helper stays the original R1 to R8 records.

## Start identity

Branch `fix/ranking-archive-concurrent-writer-metadata`, head `29d1669e6ddf09a8566861228c6584d30fba8b51`, tree `c3c16145dfc4223112b2dd90c1a147da9f8af092`. Preserved prealignment ref `backup/issue-1231-29d1669-pre-r10-align` at that head. Parent `feat/ranking-publication-runner-79` `d654634fcbe5c82a362e9a3d948d09d0c2993d6d`. Main `56eec736906774ef56d8c9a66ed7f3f9c1e520c6`.

## Scope

* Phase 1: commit these prospective records (research, plan, details, critique, state) first.
* Phase 2: `git merge --no-ff --no-commit feat/ranking-publication-runner-79`, check no conflict, check the staged tree equals the predicted tree `5d21b1d44de…`, then commit with a Conventional message and the Copilot trailer. On any conflict, abort the merge and stop; do not reconcile source intent.
* Phase 3: prove ancestry (`43080ab42`, `d654634fc`, `56eec7369`, `29d1669e6` all ancestors), prove `src`, `infra`, `tools` and workflow trees identical to `29d1669e6`, and compare the eight child-corrected source and test blobs.
* Phase 4: lightweight checks only, in my own scratch under `/mnt/ama-gates/restart-1106-1231-align/`: ranking publication, runner and wiring unit tests with import-origin proof, Ruff check and format on the manifest-pinned scope, mypy for core, `git diff --check`, JSON validity of state files, relative-link check of new records. Missing tools are restored with pip into my own external venv only after an actual failure.
* Phase 5: Changes, separate author Review, final state; commit; verify ignored-inclusive clean.

## Out of scope

No new behavior, no FULL, SQL, browser, image, scanner or lock queue, no push or PR, no parent ref move, no deletion, no edit of memory, original case study, knowledge index or log, or older RPI records.

## Follow-up items

* Fresh FULL on the merged head with the stack `1231 -> 79 -> 73`, admitted separately by the coordinator.
* Independent exact-head assessment and human approvals.
