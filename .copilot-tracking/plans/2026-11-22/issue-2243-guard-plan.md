---
title: Plan for issue 2243 diagnosable ledger refusal
ms.date: 2026-11-22
---

Tier: FULL classification applies because `src/` and `infra/sql` change; the coordinator runs gates and `rpi-checks.py --all` is not run here. Local checks: affected unit tests, mypy and ruff.

* [x] Phase 1: SQL procedure returns `accepted` plus `refusal` column (details phase 1).
* [x] Phase 2: `SqlAccounting.reserve` maps refusal to specific reasons; labels added (details phase 2).
* [x] Phase 3: tests (unit and opt-in SQL), research note with per-criterion table (details phase 3).
