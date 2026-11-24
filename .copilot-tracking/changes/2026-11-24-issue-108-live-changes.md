---
title: Issue 108 live changes 2026-11-24
description: Changes record with per-criterion proven/unproven table
ms.date: 2026-11-24
---

Refs #108. Tier: FULL classification (test-only change under `src/agents`); local checks run: `tests.test_ai_eval` 27 OK, `python3 -m mypy` clean, `ruff check` clean. `rpi-checks.py --all` not run; hosted CI not observed. No Azure resource created.

## Files

* `docs/reference/research/issue-108-live-20261124-2026-11-24.md` and folder (raw Azure outputs, new `serving_region_record.json`)
* `src/agents/tests/test_ai_eval.py` (records repointed; gate test now asserts `confirmed`, capacity/usage consistency and the partial fallback)
* `src/agents/README.md`, `docs/reference/README.md`, `docs/reference/log.md`

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Model names, versions, quotas in chosen region | PROVEN for the demo (uksouth): deployments, versions, capacity, usage rows 10/5000 and 10/16000. Tick proposed for the owner; not ticked here |
| 2 | Frozen independent held-out split | Unproven: no independent labeller |
| 3 | Humans detect seeded errors | Unproven: needs people |
| 4 | Effort and cost comparison | Unproven: no measured effort, no Finance |
| 5 | Hashes, seed, denominators, protocol, outcomes | Unproven: no reviewer protocol or outcome |
| 6 | Call authorisation, payload, attestation | Unproven: production authority |
| 7 | Real AI/SQL/Azure proof (CON-009/AC-057) | Unproven: restart check drill-like |
