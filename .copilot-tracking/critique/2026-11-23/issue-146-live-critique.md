---
title: Issue 146 live critique (2026-11-23)
ms.date: 2026-11-23
---

Verdict: proceed. Executed once.

* Risk: workbook JSON edit is infra, not src; focused tier, no permission, secret or control change. Disposition: accepted.
* Risk: deploying the fixed workbook is a production change; owner forbids. Disposition: source fix only, verify fixed query live read-only.
* Risk: throwaway storage must not leak; delete and prove with az resource list. Disposition: in plan.
* Do not tick any box; no named owners, no firing drill, no Portal render, no AI-backed availability data. Disposition: recorded as unproven.
