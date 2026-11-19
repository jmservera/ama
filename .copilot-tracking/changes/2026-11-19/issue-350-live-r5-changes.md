---
title: Issue 350 r5 changes
description: Changes record with per-criterion proven/unproven table
ms.date: 2026-11-19
---

Changed: `docs/reference/research/issue-350-live-2026-11-19.md` (14:12 UTC recheck appended), `docs/reference/log.md`. No source changes; tier FOCUSED (documentation diff review; no tests apply). Divergence: the documentation edits were made before the changes file existed, so the `implement-start` witness is late; no src was touched.

Live evidence: anonymous native curl 401 versus browser UA 302 on `/api/me`, `/api/cases`, `/app`, `/cases.html`; `/healthz` 200; Easy Auth `RedirectToLoginPage`. Nothing created in Azure, nothing to delete. No credentials used or printed.

| # | Criterion | Proven for demo? | Basis |
| --- | --- | --- | --- |
| 1 | Anonymous API 401 in browser mode, page redirect kept | Unproven, failing | 302 from Easy Auth at 14:12 UTC; needs FULL-tier edge change, outside demo authorisation |
| 2 | All parity rows and 16 assets | Unproven | Not attempted; earlier partial proof in deployed-parity-live-2026-11-18.md |
| 3 | Continuing baseline | Unproven | Earlier read showed 980 cases; restore authority not recorded |
| 4 | Model deployment, five assistants | Unproven | Earlier partial proof; release authority human-owned |
| 5 | Map provider | Unproven | OSM demo tiles only; licensed provider is an owner decision |
| 6 | Delegated photo tokens | Unproven | Needs consent and token store |
| 7 | Law store | Unproven | SQL/Blob path, FULL tier |
| 8 | Ledger, document, digest durability | Unproven | Earlier partial evidence; not re-run |
| 9 | Time capture gated | Unproven | Earlier 500 on `/api/time/status`; not re-run |
| 10 | Per-role results record | Unproven | One staff role only; depends on 2 to 9 |
