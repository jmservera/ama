<!-- markdownlint-disable-file -->
---
title: Issue 350 local feedback rehearsal plan critique
description: One independent pre-implementation critique with direct dispositions
ms.date: 2026-10-24
---

Execution: complete, independent `rubber-duck` agent, read-only, before implementation. Verdict: Revise. Executed once; not repeated.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | `/api/cases/<id>/ai` needs `{"task": "message"\|"summary"}`; with no `AI_ENDPOINT` both AI routes return 200 template/manual results (`source: template`, `model: null`), not a failure | Accepted. Details amended: assert template fallback and no model call |
| PC-002 | Blocking | `ZF_DATA`, `ZF_STATE` and full env contract not stated | Accepted. Details amended with one environment contract |
| PC-003 | Non-blocking | Contractor staff share `Test Ltd` with every base case so cannot prove denial | Accepted. A second-contractor staff member and case are added to the external fixture only |
| PC-004 | Non-blocking | Anyone holding the shared password can choose any staff email, so role selection is not identity proof | Accepted as a stated limitation in the hand-off; loopback-only |

No conflict with confirmed owner decisions. Confirmed by the critic: `MssqlStore` seeds an empty database from the JSON fixture; the database itself must be created first.
