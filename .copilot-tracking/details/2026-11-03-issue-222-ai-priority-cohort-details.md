---
title: Issue 222 AI priority cohort details
ms.date: 2026-11-03
---

## Phase details

* Phase 1: groups of ten keep each pair together; ranks are rebuilt across groups from the AI items; `reason_codes` come from the deterministic ranking, so review burden stays the ranker's. Biased mode drops `sensor-1-b`, `source-2-b`, `history-3-b`.
* Phase 2: `ai_eval` is not changed (its cohort report lives only on the #956 stack); a later slice can surface this record there.
* Phase 3: `src/agents/README.md` note.
