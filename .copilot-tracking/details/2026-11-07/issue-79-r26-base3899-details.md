---
title: Issue 79 r26 details
ms.date: 2026-11-07
---

* Commands: `git rebase origin/main`; `git diff --stat preserve/issue-79-pre-base3899 HEAD` limited to expected incoming paths; `git diff origin/main HEAD --name-only` equals the topic-owned set of bb7 versus 23b.
* Tests use `/tmp/zf79venv/bin/python` after printing the `__file__` of `zava_forward.core.ranking_publication` and `zava_forward.api`, with `PYTHONDONTWRITEBYTECODE=1` and scratch `/mnt/ama-gates/g79-base3899-1107`.
* No FULL, browser, SQL, Docker or scanner. Exception register tests run only as existing unit fixtures.
