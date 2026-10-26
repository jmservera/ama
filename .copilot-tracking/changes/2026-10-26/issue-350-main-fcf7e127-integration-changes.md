<!-- markdownlint-disable-file -->
---
title: Issue 350 main fcf7e127 integration changes
description: Changes record
ms.date: 2026-10-26
---

Order: integration note committed first, `origin/main` pinned at `fcf7e12735c9e4e69f83df9d643ec8e28a981409`, normal `--no-ff` merge `e5b3d64a63c37852863de86e4f87c47711c7932f`, cheap checks, this record. No conflict; 76 paths from main only; rubric and `log.md` identical to main. Checker, its tests and `src` unchanged. No independent review was run this stage (not requested); the earlier reviews are unchanged and the previous integration review does not cover this merge.

Checks: `unittest tools.test_check_demo_feedback` 88 OK (topic-bound venv); ruff check E,F,I,B,UP py312 line-length 100 passes; ruff format check passes. No gate, Docker, browser, push, PR edit or live action. Cleanup: no images, containers or caches were created; protected SQL, preview and rehearsal services untouched. The shared runner fix (PR 437) is now in the base, so the dependency in the earlier gate plan is satisfied; the gate still needs admission while the 444 gate holds the lock and 462 is next. Original 350 acceptance criteria remain unmet where unproved.
