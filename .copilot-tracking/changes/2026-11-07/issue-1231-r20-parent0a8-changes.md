---
title: Issue 1231 r20 changes, merge of parent79 0a8ecd50
description: Implementation record for the normal local merge of parent79 0a8ecd50 into the child
ms.date: 2026-11-07
---

* Planning commit 0378ce2027b26b2c876a2e013e2ae2a9d7a54981 preceded the merge. Backup ref `backup/issue-1231-120bb-pre-r20-merge` preserves 120bbcce.
* One normal `--no-ff` merge of 0a8ecd50f608964066ce07ae5c13c8f299b8daf7: commit 7aa173838ec4cbecbce7c854572df34ef8d8b96f, tree a9779eca68665aac8839beb217a6fe113d70fd2b, parents 0378ce20 and 0a8ecd50. No conflict; no source, test or log edit by this iteration.
* Proof: incoming raw/mode/blob delta outside .copilot-tracking (docs/reference/log.md, src/api/tests/test_assistant_release.py, tools/rpi-checks.py, tools/test_rpi_checks.py) equals the child's delta (diff empty). The only src path changed is the received src/api/tests/test_assistant_release.py; child ranking source, tests and README blobs are unchanged. log.md has 0 deleted lines.
* Checks (PYTHONDONTWRITEBYTECODE=1, own-source origins, per-command .out/.err/.exit in /mnt/ama-gates/g1231-parent0a8-preparation-1107): core 70 OK; API wiring 18 OK; test_assistant_release 48 OK with 1 skipped (opt-in SQL class, not SQL acceptance); test_rpi_checks 86 OK; test_backlog_sync 17 OK; Ruff check and format on src/core and src/api exit 0 (331 files); mypy 268 files exit 0; diff check exit 0.
* Adverse, preserved: a wider Ruff run including tools/ exited 1 (111 errors; format 16 files would be reformatted). That scope is outside the canonical src/core and src/api scope; the received tools files' format diagnostic is the known main baseline and was not reformatted. Wide outputs kept as ruff-wide/fmt-wide files.
* Not done: FULL, SQL, browser, Docker, scanners, lock wait, push, PR update, ticks, parent/main mutation. All earlier receipts are invalid for this head.
