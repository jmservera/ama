---
title: Changes issue 2237 live2
ms.date: 2026-11-23
---

Tier: focused (no src change; documentation and evidence only). Added docs/reference/research/issue-2237-live-reproof-2026-11-23.md and its evidence folder; index and log updated. No Azure change; no throwaway resources.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history, not on demand | 11 logged 500s; deterministic local test; live lock not forced (no drills) |
| Cause in demo container logs | Proven | Log Analytics, cause note; holder unidentified |
| Fix with regression test | Proven | #2290 on main, tests present, deployed on 0000055 (container grep, 14 live 503 log lines) |
| Re-prove 200 live | Proven | 56 of 56 requests 200 at 14:30 UTC, Programme Manager |

Nothing ticked on the issue.
