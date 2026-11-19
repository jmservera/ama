---
title: Research, issue 344 live (20261119T152819Z)
ms.date: 2026-11-19
---

Refs #344. Opening note. Four live passes already exist (docs/reference/research/public-browser-access-live-*.md).
Open criteria: 1 (browser-style anonymous API gets 302, needs Bicep or auth-flow change: infra), 3, 4, 5 (parity; `/api/time/status` 500 cause unknown).
Candidate buildable item: diagnose `/api/time/status` 500 (src/api/src/zava_forward/api/timecapture.py `status`, reads via SQL store).
Disposition: executing; findings follow below.

## Findings

* Criterion 1 and 3 browser-style 302: Easy Auth action `RedirectToLoginPage`; `Return401` exists only via opt-in `entraBearerOnly` in `infra/modules/containerapps.bicep`. Infrastructure and deployment: FULL tier, out of scope.
* Criterion 5 `/api/time/status` 500: `TimeCapture.status` calls `request()`/`activation()` which open the shared SQL store connection and run `CREATE TABLE`/`ALTER` DDL on first use (`_ensure`). The likely cause is the app identity lacking DDL rights or a SQL-side error, which is SQL/security scope. Live console log (read-only `az containerapp logs show`, new replica 0000033) holds no error line, the environment has no Log Analytics workspace configured, and reproducing needs a signed-in call whose traceback is not logged. Cause stays unproven.
* Criterion 4: SQL disabled/private proven in earlier passes; not re-run (no new evidence).
* No buildable, demo-provable code item remains: every open criterion is infrastructure, SQL, or needs a defect diagnosis in SQL scope. Tier FOCUSED (docs only); no src change.

Planning Readiness: Ready (documentation-only outcome).
