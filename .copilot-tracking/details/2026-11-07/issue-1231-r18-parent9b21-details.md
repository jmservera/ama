---
title: Issue 1231 r18 phase details
description: Prospective phase details for the r18 parent79 9b21a6a0 merge
ms.date: 2026-11-07
---

* Phase 1: `git branch backup/issue-1231-201f2-pre-r18-merge 201f2612e7277cd1b4a403c07905b60436de2223`; the planning head differs from 201f2612 only by the four r18 files.
* Phase 2: `git merge --no-ff -m "merge: align #1231 with parent79 9b21a6a0" 9b21a6a0d2bc0646076cd2da03f7fc4d088af06e` with Refs and Copilot trailer.
* Phase 3: compare `git diff --raw cf5f57a00 9b21a6a0` with `git diff --raw 201f2612 HEAD` excluding .copilot-tracking (and the planning/record commits); child ranking blobs equal 201f2612; zero deleted log lines.
* Phase 4: core and API selectors as in research; Ruff 0.17.1 from the preserved r7 venv; mypy cache in scratch; print module `__file__` for ranking_publication, runner, store, ranking and api server; capture each exit code directly to files.
