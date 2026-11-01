<!-- markdownlint-disable-file -->
---
title: Issue 159 denied-turn receipt plan
description: Record a consumption receipt for every conversation turn including permission-denied turns
ms.date: 2026-11-01
---

## Task Metadata

* Task slug: issue-159-denied-turn-receipts. Research: .copilot-tracking/research/2026-11-01/issue-159-denied-turn-receipts-research.md
* Phase details: inline below. Critique: single pass, Complete / Approve (scope tight, no conflicts with user decisions).

## Phases

* [x] Phase 1: `ChatPanel.record_rejected` and use in `ask` when `current_user` raises.
* [x] Phase 2: server `/messages` and `/ask` pre-check denial records a receipt.
* [x] Phase 3: tests outside the package (core and api); ruff check, format check, mypy; unittest.
* [x] Phase 4: commit, push, PR with `Refs #159` naming unmet criteria (C6 AT, tokenomics only if proven).

## Acceptance for this slice

* A denied turn yields exactly one `chat.turn` audit receipt with outcome `access-rejected`, `model_calls` 0, `tokens` null, cost Unknown.
* Denied turns store no message and call no model.
