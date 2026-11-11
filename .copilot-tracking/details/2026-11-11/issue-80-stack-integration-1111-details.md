---
title: Issue 80 stack integration details
description: Commands and boundaries for the integration validation
ms.date: 2026-11-11
---

## Execution boundary

* Scratch worktree `/tmp/ama-80-stack-scratch-1111` (detached `adbca56e` plus uncommitted merge of `origin/main`), venv `/tmp/ama-80-stack-venv-1111`. Assert import origins resolve under the scratch tree and `ZF_DATA` is an owned temp file; never the default dataset.
* From `src/api`: `PYTHONPATH=../core/tests:../agents/tests:tests` only; direct exits to evidence files, no pipes.
* Browser tests use the nonqueued `flock -n /tmp/ama-rpi-heavy.lock`; busy means stop and report.
* Source hash carry: sha256 of `checks/capacity_browser_check.py`, `web/ops.js`, `web/app.js` and capacity-relevant web files compared with the C4 validation hashes (`attempt2-pre-hashes.txt`). `app.js` differs, so no hash carry is claimed; the whole run is executed once instead (critique PC-001).
* Own RPI changes only are committed in the parent branch; the scratch merge is never committed or pushed and is removed after evidence is kept.
