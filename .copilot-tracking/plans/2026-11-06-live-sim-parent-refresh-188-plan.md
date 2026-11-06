---
title: Plan for #188 parent 184 refresh and wrapper r12
ms.date: 2026-11-06
---

* Step 1: ordinary no-ff merge of pinned 2dc125f97 into this child only. Resolve `src/core/README.md` by keeping both additions; stop and report if the intent is ambiguous. No rebase, force, amend, parent ref or worktree movement.
* Step 2: light checks with explicit i188 `PYTHONPATH` (api, core, agents source and tests; never mvp), bytecode off, external caches: sensor consistency, live consumer and ingestion modules; the parent's device identity and provision tests; Ruff check and format (no cache); mypy for affected core and API with external cache directories. Missing dependency is a blocker, no install.
* Step 3: Changes, dedicated author Review (once), session state; commit with the gh-api-user privacy-safe identity, Conventional Commit and Copilot trailer; freeze ignored-clean; no tracked edits afterwards.
* Step 4, only after the freeze: new external `/tmp/188-sql-readiness-r12`, created from r8 functions and the r11 repin, pinned to the actual final head and tree, with new absent evidence paths and a parent 184 vs pinned 2dc125f9 guard next to the main guard at each fetch check. Compile() only, exact diff and hash. Not executed.
* Gates pending: owned SQL run, FULL, independent exact-head review, hosted checks, parent and main acceptance. Human review checkbox left unchecked.
