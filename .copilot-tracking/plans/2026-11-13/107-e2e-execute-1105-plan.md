---
title: Issue 107 end-to-end execute probe plan
description: Plan for the offline end-to-end attribution and leak probe
ms.date: 2026-11-13
---

## Plan

* [ ] P1 Critique this plan independently before any venv, install, run or merge.
* [ ] P2 Create `/tmp/venv-107e2e-1105` (system site packages), editable `--no-deps` install of core, agents, api; verify `__file__` inside worktree.
* [ ] P3 Run probe: for each REGISTRY assistant, authorise, seed sentinels, invoke, execute, human verify; chat turn with active meter_root; scan.
* [ ] P4 Record script, output, sha256, true exit in changes file; remove venv.
* [ ] P5 Independent code-review, review file, commit with trailer.

Details: [details](107-e2e-execute-1105-details.md). Success: per-assistant and per-accepted-proposal
attribution exact, `accepted_proposals` equals verified count, chat output not eligible, ledger and audit lists
non-empty, zero sentinel hits in all SQLite rows and report JSON.
