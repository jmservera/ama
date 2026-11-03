<!-- markdownlint-disable-file -->
---
title: Issue 159 panel limits and per-turn consumption visibility research
description: Evidence for the next slice of the workbench conversation panel after PRs 305, 307, 503, 556, 661 and 840
ms.date: 2026-11-03
---

## Task Metadata

* Task slug: issue-159-r1-limits-ui. Branch feat/issue-159-r1, target main. Mode: automatic. Research disposition: executed (prior-delivery check plus source reading). Planning Readiness: Ready.

## Prior delivery (merged PRs)

* #305: case panel, cited and labelled answers, abstention, per-turn role and case re-check, proposal-only route, workflow-only fallback (criteria 1 to 5).
* #307, #503, #556, #650: grounding and evaluation, isolated turns, shared widget, break-glass audit.
* #661 and #840: `chat.turn` receipts for turns refused by the user/thread checks and by the route-level role gate.
* Already in code: `ChatPanel._receipt` records model calls, tokens, provider outcome, outcome and cost "Unknown"; `LIMIT_REACHED` falls back to workflow-only when system plus prompt exceed `MAX_INPUT_CHARS`; `GET /api/chat/status` returns `limits` (1 call per turn, 0 retries, 600 output tokens, context and history character caps, "engineering caps, not spend authorization"); `/ask` replies carry `consumption`.

## Remaining gap found

* `src/api/src/zava_forward/api/web/chat.js` ignores `admission.limits` and `answer.consumption`. The tokenomics criterion asks that the thread context has a stated bound and that each turn's calls, tokens and outcome are recorded; staff cannot see the bound or the per-turn consumption in the panel.

## Selected slice

Show the stated bounds in the panel intro and a one-line per-turn consumption note (calls, tokens or Unknown, outcome, cost Unknown) on each assistant message. Front-end only; no permission, schema, storage or API change.

## Out of scope and unmet

* Criterion 6 needs a named human screen-reader run; code cannot satisfy it.
* Tokenomics criterion stays open: receipts are still missing for unauthenticated 401, `unstored-ask` and regulatory-thread asks; prices, budgets and targets are unset (BRD OD-51 open), so cost stays Unknown.

## Validation tier

Focused. No security, infrastructure, SQL or deployment change; gate not run.
