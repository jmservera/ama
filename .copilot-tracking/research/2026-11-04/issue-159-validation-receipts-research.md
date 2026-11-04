<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refused receipts research
description: Delivered work on #159 and the remaining receipt gap for validation-refused unstored asks
ms.date: 2026-11-04
---

## Disposition

* Research executed (focused). Planning Readiness: Ready.

## Prior delivery checked

* Merged: #305, #307, #503, #556 (criteria 1 to 5), #661, #840, #1003 (refusal receipts for permission, role-gate, unstored and regulatory refusals), #927 (limits and consumption in the panel).
* Stored `ChatPanel.ask` already records a receipt in `finally`, including on ValueError (outcome `rejected`).

## Gap found

* `ChatPanel.ask_unstored` (src/core/src/zava_forward/core/chat_panel.py) raised ValueError (bad skill, empty or over-long question) and ChatNotFound (missing or unpermitted case) before writing any `chat.turn.unstored` receipt.
* Still not receipted: 401 with no actor (no identity to attribute) and route-level key validation in `server.py`.

## Unmet criteria

* Criterion 6: named human screen-reader test and announcement check (human tester needed).
* Tokenomics criterion: advanced, not proven (401 and route-validation paths; cost Unknown, BRD OD-51 open).
