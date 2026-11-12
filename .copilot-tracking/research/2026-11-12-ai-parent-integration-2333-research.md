---
title: Research for #104 AI parent integration (Refs 104 107 157 216)
ms.date: 2026-11-12
---

* Task: ai-parent-integration-2333. Worktree `issue-104-parent-integration-2333`, branch `feat/demo-104-parent-integration-2333`, parent head `4459dadb4c751fcb4e1cc93d369ff844f2cbc9b7` (contains merged PR 1488 for #157 and PR 1489 for #107; merge base with main `43b2187b9`).
* Research disposition: reused. Mandatory reads: case study original and addendum (headings and relevant sections), `docs/reference/README.md`, `memory.md`, `src/api/README.md` test commands, the cutover evidence pack tail. Prior evidence: `rpi-104-integration-2220-result.json` (children are independent siblings, no path overlap), `rpi-107-current-parent-validation-2320-result.json` (canonical 60 release tests, 3 changed tests, 1 memory test on installed distributions; 7 MSSQL skips; original source-PYTHONPATH caveat in the 107 assessment) and the reviewed 216 candidate `e4aac8b72802f583f19eabf88e14742f68f4f653` (one own commit after `eac1206c6`, which is already in main; test-only plus its original RPI).
* Not duplicated: the prospective broad matrix and baseline inventory owned by `parent-base-preflight-2300`.
* Fresh main: `origin/main` `8e6e554570f4075ff41ea130e29511455f57df2d`. Dry-run `git merge-tree` of parent with main is clean. Main delta over the parent base touches `src/core` `form_export.py` and its test (not AI assistant, release, memory or citation code) plus docs and tracking.
* Candidate 216 touches only `src/api/tests/test_regulatory_chat_api.py` and its own dated RPI files; no ancestry beyond `eac1206c6`.
* Planning Readiness: Ready.
* Limits kept: no push, PR or merge; no MSSQL, provider, model, cloud or private data; no approval, tick or closing reference; #107 and #157 and #216 acceptance criteria stay unmet or human/live-owned.
