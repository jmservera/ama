---
title: Issue 86 integration of local parent 6cae8cb changes
description: Changes record for one normal merge (Refs #86)
ms.date: 2026-11-07
---

* Start `72544ed7` (ref `backup/issue-86-pre-6cae-72544ed`); planning commit `4af9c626…`; one normal merge `9d6d6346011864ba759c1fd1bc930a6ee41e6d97`, tree `8a4ae438…`, parents `4af9c626…` and `6cae8cbe…`. No rebase, force, push or retarget; PR 1243 target unchanged. `origin/main` `a1d26534…` is contained in the parent.
* Incoming delta: 18 paths (16 additions, 2 modifications, all mode 100644); non-tracking `tools/backlog-sync.py` and `tools/test_backlog_sync.py`. All paths changed since `720d9e49` equal the parent's blobs; five complaint paths equal pre-merge blobs.
* Checks on git-archive snapshot `/mnt/ama-gates/g86-parent6cae-preparation-1107` (origin in snapshot): `tests.test_resident_decisions` exit 0, 308 tests, 110 skipped; strict mypy 267 files exit 0; ruff check and format exit 0; `test_backlog_sync` exit 0, 17 tests. Earlier API setup failure (exit 1) and retry (46 pass) remain historical; API test not re-run as the API is unchanged.
* No behaviour change. SQL/Azure skipped, not claimed. 1238 follow-up untouched.

Pending: new parent integration FULL on exact head and main, independent assessment, hosted checks, human approvals, real receiver acknowledgement.
