---
title: Issue 108 live plan 2026-11-24
description: Plan and single critique
ms.date: 2026-11-24
---

Refs #108. Tier: FULL classification because `src/agents/tests` changes (test only, no runtime code); `rpi-checks.py --all` not run (coordinator owns gates). Local checks: `tests.test_ai_eval`, mypy and ruff in `src/agents`.

1. Add `serving_region_record.json` under the 2026-11-24 evidence folder: uksouth only, two live deployments, `quota_headroom` confirmed with the two usage rows.
2. Repoint the serving-record tests at the new record; add a test that headroom rows are consistent with deployed capacity and that the record gates to `confirmed`.
3. Research note with per-criterion table; index row and log entry; keep the 2026-11-19 record as history.
4. Leave held-out, human, effort/cost and call-authorisation criteria unproven with reasons.

Critique (executed once, verdict accepted): risk that "confirmed" overclaims. Mitigation: the record states headroom means subscription quota rows for these two SKUs only, not a live call, accuracy or benefit; the issue criterion needs names, versions and quotas only. Production region remains owned by other issues.
