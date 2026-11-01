---
title: Issue 212 upgrade regrouping review
description: Single review of the PR 630 upgrade-safety amendment
ms.date: 2026-11-01
---

* Execution: executed once by the implementing agent; independent human/hosted review still required.
* Boundary: `rule_engine.py` ENGINE_VERSION bump and read-time regrouping; one regression test.
* Outcome: no open material findings; follow-up: human re-approval of source-monitor approvals bound to engine version 2.
* Changes: [issue-212-home-grouping-changes.md](../../changes/2026-11-01/issue-212-home-grouping-changes.md)
* Amendment boundary: `_homes()`, `_publish()` cooldown and `alerts()` regrouping for the three later PR threads; executed once by the implementing agent; no open material findings; independent human/hosted review still required.
* Second amendment boundary: `_publish()` windowed query and `_current_home` for two further PR threads; executed once by the implementing agent; no open material findings; independent human/hosted review still required.
