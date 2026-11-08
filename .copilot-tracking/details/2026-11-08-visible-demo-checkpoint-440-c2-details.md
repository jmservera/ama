---
title: Visible-demo integration checkpoint 440 C2 details
ms.date: 2026-11-08
---

## Phase 1

* `docs/architecture/cutover-evidence-pack.md` new section only: replace "calls `ChatModel` once per turn" with a conditional, at most once statement citing `chat_panel.py` 583-591; qualify the BRD and PRD trace row; add one provenance note.

## Phase 2

* Append one entry to `docs/reference/log.md`.

## Phase 3 and 4

* Validation commands as in the plan; records and state under `.copilot-tracking/`.
