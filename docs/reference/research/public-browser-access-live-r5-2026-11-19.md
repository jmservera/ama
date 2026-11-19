---
title: Public Browser Access on the Deployed Demo, Pass Five (Issue 344)
description: Fifth pass for issue 344 recording that no remaining criterion can be built or proven for the demo without infrastructure or SQL scope
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

Refs #344. This pass follows the [first](public-browser-access-live-demo-2026-11-18.md), [second](public-browser-access-live-rerun-2026-11-18.md), [third](public-browser-access-live-r3-2026-11-18.md) and [fourth](public-browser-access-live-r4-2026-11-19.md) notes. It used read-only Azure CLI only; no resource was created, no credential was read, nothing needs deleting.

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Public landing; Entra sign-in; anonymous API 401, not a redirect | Partly proven, browser-style clause unproven | Easy Auth `RedirectToLoginPage`; `Return401` needs a Bicep change (full tier) |
| 2 | Public edge follows #143 | Already ticked | External Container Apps environment |
| 3 | `/healthz` public; anonymous API 401 | Proven for non-browser clients | Same redirect caveat |
| 4 | SQL private, no policy bypass | Proven earlier, not re-run | No new evidence this pass |
| 5 | Parity, gaps filed | Unproven | `/api/time/status` 500 cause unknown: the path uses the SQL store and first-use DDL in `timecapture.py`; live console log holds no error line and no Log Analytics workspace is configured, so a fix would be SQL scope |
| 6 | Browser sign-in smoke recorded | Already ticked | Earlier passes |

## Outcome

Every remaining criterion is infrastructure, SQL or needs a human or owner decision. No source change was made. The owner ticks checkboxes.
