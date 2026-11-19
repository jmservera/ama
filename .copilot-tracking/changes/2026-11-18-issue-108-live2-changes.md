---
title: Issue 108 live round 2 changes
description: Changes record with per-criterion proven or unproven table
ms.date: 2026-11-18
---

Files: `docs/reference/research/issue-108-harness-audit-live-r2-2026-11-18.md`, raw evidence folder beside it, `docs/reference/README.md` index row, `docs/reference/log.md` entry. No source, SQL or infra change. Tier FOCUSED. No amendments or divergences.

Validation: harness unittest 116 OK; GUID and e-mail scan of retained evidence clean; link and diff review done. mypy, ruff and rpi-checks not applicable (docs only).

| Criterion | Status |
| --- | --- |
| Critical misses fail the run | Proven (tests) |
| Model, prompt, latency, reviewer outcomes reported | Proven offline/scripted |
| Model names, versions, quotas in region | Partly: names, versions, capacity, rate limits proven; subscription quota unproven (usages route empty) |
| Benefit not claimed without calibration | Unchanged, proven |
| Held-out freeze, independent labels | Partly; independence unproven |
| Human detection of seeded errors | Unproven (needs people) |
| Effort and cost comparison, Finance | Unproven |
| Hashes, seed, serving version, protocol | Partly |
| Finite call authority, payload approval, attestation | Partly |
| Real AI/SQL/Azure proof (AC-057) | Partly; restart check not run |
| One-lever routing/caching live | Mechanism proven offline; no live lever |
