<!-- markdownlint-disable-file -->
---
title: Issue 159 role-gate denied-turn receipt plan
description: Record a consumption receipt when the route-level role gate refuses a conversation turn
ms.date: 2026-11-03
---

## Task Metadata

* Task slug: issue-159-role-gate-receipts. Research: .copilot-tracking/research/2026-11-03/issue-159-role-gate-receipts-research.md
* Phase details: .copilot-tracking/details/2026-11-03/issue-159-role-gate-receipts-details.md
* Critique: executed once on the final candidate. Verdict Approve. Compatible findings applied directly: limit to `messages` and `ask` (other chat routes are not turns), skip the 401 path (no actor), reuse `record_rejected`, assert the question text is absent from the receipt.

## Phases

* [x] Phase 1: call `app.panel.record_rejected` from the POST role gate for `/api/chat/threads/<tid>/messages|ask`.
* [x] Phase 2: API tests outside the package: contractor refused on both routes yields one receipt each, no model call, no question text; other chat routes record none.
* [x] Phase 3: ruff check, ruff format --check, mypy with `--cache-dir=/tmp/mypy-159`, focused unittest.
* [x] Phase 4: commit, push, PR with `Refs #159` naming unmet criteria.

## Acceptance for this slice

* A turn refused by the role gate yields exactly one `chat.turn` receipt: outcome `access-rejected`, `model_calls` 0, `tokens` null, cost Unknown.
* No stored message, no model call, no change to the 403 response, no change to who is permitted.

## Unmet after this slice

* Criterion 6: named human screen-reader test and announcement check.
* Tokenomics criterion: not proven for every refusal path (see research); left unticked.
