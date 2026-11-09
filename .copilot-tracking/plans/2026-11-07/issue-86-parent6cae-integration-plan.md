---
title: Issue 86 integration of local parent 6cae8cb plan
description: Plan for one normal merge and light checks (Refs #86)
ms.date: 2026-11-07
---

Tier: FULL eventually, none admitted here. Steps: commit records; re-verify; one `git merge --no-ff 6cae8cb`; prove two parents, incoming delta blobs/modes, child-owned blobs unchanged; run from a git-archive snapshot `tests.test_resident_decisions` (expect 308/110), core strict mypy, ruff, and `tools/test_backlog_sync.py` as incoming-source check; write changes and one author Review; freeze. New parent integration FULL and independent assessment follow; no receipt survives the merge.
