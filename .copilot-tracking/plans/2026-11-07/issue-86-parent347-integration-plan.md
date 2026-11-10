---
title: Issue 86 integration of local parent 34729c4 plan
description: Plan for one normal merge and light checks (Refs #86)
ms.date: 2026-11-07
---

Tier: FULL eventually; none admitted here, no services or lock. Steps: commit records; re-verify; one `git merge --no-ff 34729c4`; prove two parents, each incoming path's blob/mode, child-owned blobs and prior log/RPI bytes unchanged; run from a whole git archive: `tools/test_rpi_checks.py`, `src/api` `tests.test_assistant_release`, core `tests.test_resident_decisions` (historical 308/110 reused only if core blobs equal, re-run cheaply anyway), canonical ruff/mypy for core; record .out/.err/.exit. New parent integration FULL and independent assessment follow; no receipt survives.
