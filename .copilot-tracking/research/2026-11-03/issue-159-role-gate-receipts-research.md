<!-- markdownlint-disable-file -->
---
title: Issue 159 role-gate denied-turn receipt research
description: Evidence for the remaining engineering gap in the workbench conversation panel after PRs 305, 307, 503 and 661
ms.date: 2026-11-03
---

## Task Metadata

* Task slug: issue-159-role-gate-receipts. Branch feat/issue-159-r1, target main. Mode: automatic. Research disposition: executed (prior-delivery check plus source reading; follow-up 1 of the 2026-11-01 review).
* Planning Readiness: Ready.

## Prior delivery (merged PRs, checked on origin/main a 044b1fa6d)

* #305: case panel, cited and labelled answers, abstention, per-turn role and case re-check, proposal-only path, workflow-only fallback (criteria 1 to 5).
* #307, #503, #556, #650: chat grounding and evaluation, isolated turns, shared widget focus fixes, break-glass audit.
* #661: `chat.turn` receipt (`access-rejected`, 0 calls, unknown tokens) for turns refused by the current-user check and the thread resume check.
* Issue comment (2026-10-31 closure audit): criterion 6 and the tokenomics criterion remain unmet. The audit names denial before receipt construction as the tokenomics gap; #661 closed two of its paths.

## Remaining gap found

* `src/api/src/zava_forward/api/server.py` POST dispatch calls `projection.allowed(u, "post", "POST")` before `_chat`. A contractor (and any role without POST) is refused with 403 there, so a `/api/chat/threads/<tid>/messages` or `/ask` turn leaves no `chat.turn` receipt. #661 review routed this as follow-up 1.
* Receipt shape and `ChatPanel.record_rejected(user, tid)` already exist in `src/core/src/zava_forward/core/chat_panel.py`; no new field is needed.

## Selected slice

Record one `access-rejected` receipt for turn routes refused by the route-level role gate. Out of scope:

* Criterion 6 needs a named human screen-reader run (owner or accessibility tester). Code cannot satisfy it.
* Other refusal points (unauthenticated 401 has no actor, `unstored-ask`, regulatory-thread asks, `get_kind` GET projection) record no chat receipt. These are residual.
* Prices, budgets, targets (BRD OD-51 open); cost stays Unknown.

## Validation tier

Focused. The slice touches an authorization-adjacent audit write but changes no permission decision, infrastructure, SQL schema or deployment. It adds no new access; the gate is not run here and the coordinator decides on any gate.
