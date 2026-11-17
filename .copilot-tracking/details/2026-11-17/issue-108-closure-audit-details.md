---
title: Issue 108 closure audit details
ms.date: 2026-11-17
---

Test derives the not-exercised task ids from `ai_eval.run_eval()["evidence"]["task_coverage"]` and requires each in the audit page, plus the phrases "Refs #108", "not on main" and the origin SHA. Rationale: the doc cannot drift from the harness's own coverage report.
