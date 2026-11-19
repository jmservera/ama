---
title: Issue 350 live changes (2026-11-19)
description: Changes record with per-criterion proven/unproven table
ms.date: 2026-11-19
---

Changed: `docs/reference/research/issue-350-live-2026-11-19.md` (recheck section appended). No source changes; tier FOCUSED (documentation diff review; no tests apply).

| # | Criterion | Proven for demo? | Basis |
| --- | --- | --- | --- |
| 1 | Anonymous API 401 in browser mode, page redirect kept | Unproven, failing | Live 10:49 UTC: browser UA gets 302; Easy Auth edge, infra FULL tier |
| 2 | All parity rows and 16 assets | Unproven | Not attempted; depends on #349; see deployed-parity-live-r3-2026-11-18.md |
| 3 | Continuing baseline | Unproven | Data restore, not source work |
| 4 | Model deployment, five assistants | Unproven | Deployment configuration; no real-AI action here |
| 5 | Map provider | Unproven | Needs provider choice |
| 6 | Delegated photo tokens | Unproven | Needs consent and token store |
| 7 | Law store | Unproven | SQL/Blob path, FULL tier |
| 8 | Ledger, document, digest durability | Partly evidenced earlier | sql-ledger-live-r2 and digest notes; not re-run |
| 9 | Time capture gated | Unproven | Earlier live run reproduced a 500 on /api/time/status (r3 follow-up) |
| 10 | Per-role results record | Unproven | Depends on 2 to 9 |
