---
title: Issue 121 r6 research
date: 2026-11-04
---

Task: issue 121, branch feat/issue-121-r6 (the requested name feat/agent-chat-skills-530 was not the checked-out branch). Disposition: reused r1 research plus a fresh merged-PR check. Planning Readiness: Ready.

## Prior delivery

* #919 (Refs #121) delivered the pure core module `data_protection` (register, dispatch gate, task limits, rights clock). No other merged PR delivers #121; #281, #353, #506 and #673 are chat, regulatory or SQL-parameter scope.
* The module is not reachable from the API.

## Acceptance criteria status

* All four issue criteria unmet (they need named DPO and Legal owners). RAI processing criteria unmet except the constructed-fixture one, already checked.
* Blocked on humans: lawful basis, Article 17(3), retention period, transfer approval. Rights log persistence is SQL (complete gate, coordinator).

## Slice 2 chosen

Read-only `GET /api/data-protection` for staff so the missing-approval register is visible. No SQL, deployment or security-control change; focused tier. Wiring `model_dispatch` into assistant execution is deferred (it changes the live dispatch path and needs its own critique and gate).
