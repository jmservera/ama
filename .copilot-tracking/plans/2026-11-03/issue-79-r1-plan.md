---
title: Issue 79 plan, slice 1
ms.date: 2026-11-03
---

* [x] Phase 1: add `ranking_publication.py` (publish, verify, overdue, SCHEDULE); no clock, no delete.
* [x] Phase 2: unit tests; ruff and mypy; ranking regression tests.
* [x] Phase 3: README note, log entry, evidence.

Details: [details](../../details/2026-11-03/issue-79-r1-details.md). Tier: focused (pure module, no SQL, infra, deployment or security change).

Critique (single pass, self-run): no policy change, so the unsigned policy cannot be mistaken for signed; retention left unset; publication is idempotent so a scheduler retry is safe. Applied directly; no significant issue.
