---
title: Issue 79 r27 details
ms.date: 2026-11-07
---

* Commands: `git fetch origin main`; `git merge --no-ff origin/main`; `git diff --raw <planning-head> HEAD` must list only the score JSON and the new RPI files; `git rev-parse HEAD:.github/rubric/scores/latest.json origin/main:.github/rubric/scores/latest.json`; `python3 -m json.tool`.
