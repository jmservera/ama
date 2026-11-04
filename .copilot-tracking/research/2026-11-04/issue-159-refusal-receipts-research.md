<!-- markdownlint-disable-file -->
---
title: Issue 159 unstored-ask and regulatory-capability refusal receipt research
description: Evidence for the remaining receipt gaps in the workbench conversation panel after PRs 305, 661, 840 and 927
ms.date: 2026-11-04
---

## Task Metadata

* Task slug: issue-159-refusal-receipts. Branch feat/agent-chat-skills-530, target main. Mode: automatic. Research disposition: executed (merged-PR check, issue comments, source reading).
* Planning Readiness: Ready.

## Prior delivery (merged PRs, origin/main 885687a17)

* #305, #307, #503, #556: criteria 1 to 5 (case panel, cited and labelled answers, abstention, per-turn permission re-check, proposal-only, workflow-only fallback).
* #661: `chat.turn` receipt for turns refused by the current-user check and thread resume check. #840: receipt for turns refused by the route-level role gate. #927: limits and per-turn consumption shown in the panel.
* Issue comments: criterion 6 (named screen-reader run) and the tokenomics criterion remain unticked.

## Remaining gaps found (read from `server.py` and `chat_panel.py`)

* `POST /api/chat/unstored-ask`: a role refused by the route gate, or a user refused by `current_user`, leaves no audit record (the success path writes `chat.turn.unstored`).
* `POST /api/chat/threads/<tid>/messages|ask` on a regulatory thread without the separately assigned RegulatoryChat capability returns 403 from `_regulatory_access` with no `chat.turn` receipt.
* Residual, out of scope: unauthenticated 401 (no actor), a regulatory-thread ask routed to the generic endpoint that fails validation (400, no model call), and `get_kind` GET projection.

## Selected slice

Record one `access-rejected` receipt (0 model calls, tokens unknown, no question text) for the two gaps above. No permission decision, response or storage schema changes.

## Out of scope

* Criterion 6 needs a named human screen-reader run; code cannot satisfy it.
* Prices, budgets, targets (BRD OD-51 open); cost stays Unknown.

## Validation tier

Focused. Audit-write only; no new access, infrastructure, SQL schema or deployment. Gate not run; coordinator decides.
