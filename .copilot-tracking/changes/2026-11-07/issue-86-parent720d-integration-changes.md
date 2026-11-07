---
title: Issue 86 integration of local parent 720d9e4 changes
description: Changes record for one normal merge (Refs #86)
ms.date: 2026-11-07
---

* Start `608248ee` (ref `backup/issue-86-pre-720d-608248ee`); planning commit `e6ed8035…`; one normal merge `297e17923d29478d7b77d8a35a7d8f3553567d41`, tree `9ab5e589…`, parents `e6ed8035…` and `720d9e49…`. No rebase, force, push or retarget; PR 1243 target unchanged. `origin/main` `3950602754…`, contained in the parent.
* Incoming delta from the first parent: 27 paths. Every changed path between old parent `ae549635` and `720d9e4` equals the parent's blob (no mismatch); the five corrected complaint paths equal their pre-merge blobs; no mode changes. Non-tracking incoming: `.github/rubric/scores/latest.json`, `src/api/tests/test_assistant_release.py`.
* Checks on a git-archive snapshot (`/mnt/ama-gates/g86-parent720d-preparation-1107`, origin in snapshot): `tests.test_resident_decisions` exit 0, 308 tests, 110 skipped; strict mypy 267 files exit 0; ruff check and format exit 0; API `tests.test_assistant_release` exit 0, 46 tests. A first API attempt exited 1 (missing test-dir on `PYTHONPATH`, my setup error, `api.out` retained); the retry used the right paths (`api2.out`).
* No behaviour change. SQL/Azure variants skipped, not claimed. Issue 1238 follow-up untouched.

Pending: FULL (new parent integration FULL after child merge), independent exact-head review, hosted checks, human approvals, real receiver acknowledgement. Main may move (1252).
