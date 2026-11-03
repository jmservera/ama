<!-- markdownlint-disable-file -->
---
title: Issue 159 panel limits and consumption visibility details
description: Phase details for the limits and consumption display
ms.date: 2026-11-03
---

## Phase 1

* `limitsNote(limits)` builds the intro paragraph `chat-limits`: calls per question, retries, context and history characters, that earlier assistant replies are not sent back, that caps are engineering caps and not spend authorization, and that an over-cap question gets workflow-only help.
* `usageNote(receipt)` returns "Model calls: n. Tokens: total or Unknown. Outcome: x. Cost: Unknown." and an empty string without a receipt.
* Both read server values only; no number is hard-coded in the panel.

## Phase 2

* New test `test_panel_states_limits_and_per_turn_consumption` runs the real `chat-widget.js` and `chat.js` under Node, checks the intro text and both a counted turn and a zero-call fallback turn.
* Confirmed the test fails without the `chat.js` change.
