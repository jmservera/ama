<!-- markdownlint-disable-file -->
---
title: Issue 159 panel limits and consumption visibility plan
description: One-slice plan for showing stated limits and per-turn consumption in the workbench chat panel
ms.date: 2026-11-03
---

## Plan

* [x] Phase 1: render `admission.limits` in the panel intro and a consumption note on each reply in `chat.js`.
* [x] Phase 2: add a Node-executed test in `test_chat_widget_focus.py`; run focused tests, ruff and mypy.
* [x] Phase 3: record changes and review; open PR with Refs #159.

## Critique (executed once)

* Verdict: Approve. Front-end display only, no new permission or data path. Text is plain language, uses `textContent` via `h`, so server values cannot inject markup. The notes are rendered only when the server supplies the values.
* Stacked slices: next is receipts for the remaining refusal paths (unstored-ask, regulatory asks), then the human screen-reader run.
