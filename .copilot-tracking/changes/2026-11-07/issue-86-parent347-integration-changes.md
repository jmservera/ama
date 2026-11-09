---
title: Issue 86 integration of local parent 34729c4 changes
description: Changes record for one normal merge (Refs #86)
ms.date: 2026-11-07
---

* Start `ed5bddf4` (ref `backup/issue-86-pre-347-ed5bddf`); planning commit `24f5c0cfe92805a60e95a5b7937b0f9905636aaf`; one normal merge `9845e2e1af77e50b6ef8d903ce276605330e65f0`, tree `add82bce…`, parents `24f5c0cf…` and `34729c4f…`. No rebase, force, push or retarget. `origin/main` `23b26a7f…` is contained in the parent.
* Incoming delta: 24 paths (20 additions, 4 modifications, all mode 100644). Non-tracking: `.github/rubric/scores/latest.json`, `src/api/tests/test_assistant_release.py`, `tools/rpi-checks.py`, `tools/test_rpi_checks.py`. Every path changed since `6cae8cbe` matches the parent's blob and mode; `docs/` and `src/core` are byte-unchanged versus the first parent, so child-owned complaint source and prior log prefix are preserved; prior RPI files removed or changed: none.
* Checks on a whole git archive in `/mnt/ama-gates/g86-parent347-preparation-1107` (each with .out/.err/.exit): core `test_resident_decisions` exit 0, 308 tests, 110 skipped; strict mypy exit 0; ruff check and format exit 0; API `test_assistant_release` exit 0, 48 tests, 1 skipped; `test_rpi_checks` exit 0, 86 tests. No first-run failures this time. Earlier stopped a0ec attempt is historical (no write).
* No behaviour change. SQL/Azure skipped, not claimed. 1238 untouched.

Pending: NEW parent integration FULL on exact head and main, independent assessment, hosted checks, human approvals, real receiver acknowledgement.
