---
title: Redeploy chat changes from main 398e846fd, changes and live results
ms.date: 2026-11-01
---

## Deployment

| App | Before | After | Health |
| --- | --- | --- | --- |
| ca-resident-demo | `--0000006` | `--0000007` (helper, 4 resident-owned what-if changes, none elsewhere) | `/healthz` 200 |
| ca-cutover-test-demo-api | `--0000007` | `--0000008` | `/healthz` 200, Healthy |
| ca-cutover-test-api | `--0000001` | `--0000002` (+ five `CHAT_*`) | Healthy, 1 replica (internal; no public probe) |
| ca-cutover-test-agents | `--z34vcua` | `--0000001` | Healthy |

* Sanitized before and after diff: only image and revision changed, plus the five `CHAT_*` additions on `ca-cutover-test-api`; resident and demo API `CHAT_*` values unchanged; secrets, identity, ingress and scale unchanged; min replicas 0 on all four; eight jobs Manual.
* Registry window: IP-only, exports on, restored; full `az acr show` before and after identical (`ACR_RESTORE_EQUAL True`).
* No rollback was needed. Own local images removed by exact tag. A `docker image prune -f` of dangling images was also run, which can include dangling layers not built here (disk only, no tagged image affected).

## Live results (2026-11-01 UTC)

| Check | Result | Evidence |
| --- | --- | --- |
| Resident sign-in | PASS | `redeploy-chat-2026-11-01/live-results-resident.json` |
| Resident "How is my case going?" | PASS | Grounded, "Summary by rules - AI is not enabled", pause status shown, no generic refusal |
| Resident "Can I unpause it?" | PASS | Grounded on the pause, explains a person must lift it |
| Resident "What docs are missing?" | PASS | Grounded, lists documents D1 and D2 with limits |
| Resident sensors view | PASS (loads) | Card renders; "No synthetic sensor readings are available for your home" (0 gauges, stored sensor tables hold 0 rows per the 2026-10-31 evidence) |
| Employee sign-in | PASS | `live-results-employee.json` |
| Employee chat window size | PASS | 512x720 in a 1280x900 viewport, contained |
| Employee chat stays open | PASS | Still open after two asks |
| Employee chat grounded on the case | FAIL | Replies "The assistant is not available right now", Sources (0); bug #749 |
| Employee chat storage | PASS (API), reply wording not saved/stored | `/api/chat/status` storage_approved true, retention 30 days; thread POST 200, asks 200, 4 persisted turns; no "storage not approved" notice. The reply text never says saved or stored |
| Employee capacity and work orders | PASS | Packages and work orders 200; pagers "Showing work orders 1 to 20 of 601. Page 1 of 31"; no stuck "Loading workspace data" |

Notes:

* The script's own "grounded" regex missed the wording "not available", so the raw `employee_chat_grounded_and_stays_open` entry says pass; the correct verdict is FAIL as above (screenshot `screenshots/employee-chat.png`). The raw `employee_chat_storage_works` and `employee_chat_storage_api_evidence` entries are fail only because they look for the word saved and because an unrelated `GET /api/chat/regulatory/status` returned 403 for this role (not investigated).
* `live-results-employee-run3-initial.json` is the earlier run of the same checks; three employee sign-ins were used in total, two earlier runs aborted on selector bugs in the check script (tabs, summary), not on the app.

## Issues

* #749 bug: stored employee chat is not grounded when AI is off.
