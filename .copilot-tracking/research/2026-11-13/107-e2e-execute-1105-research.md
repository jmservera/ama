---
title: Issue 107 end-to-end execute probe research
description: Research for the offline Assistants.execute and ChatPanel metering probe
ms.date: 2026-11-13
---

## Scope

Refs #107, #159, #432. Close the Wave-1 review gap: end-to-end Assistants.execute,
human acceptance, SqlStore rows and tariff-enabled ChatPanel, with leak scan.

## Evidence (read at 3b05143179f8)

* `src/core/src/zava_forward/core/assistants.py`: `REGISTRY` (line 37) lists the registered assistants;
  `Assistants.execute(tid)` (line 1758) claims a task, builds the request, dispatches under
  `ai_consumption.call_context` and completes with a shaped envelope (`shape_result`, line 441, keeps
  `meter_id`, `meter_root`, `configuration`, `prompt_hash`). Review actions (line ~1899) settle the ledger
  through `consumption.publish_output` / review records.
* `src/api/tests/test_assistants.py`: `Base` builds a SQLite `SqlStore` in a temp dir with `Assistants`,
  `run_ready(cap)` (invoke, execute, assert ready) and `verify(p)` (human accept).
* `src/api/tests/test_ai_consumption_api.py`: `ConsumptionApi.authority(cap)` registers a synthetic price and
  authority; a loopback fake HTTP provider returns a valid proposal with a usage envelope;
  `chat_panel(store)` builds `ChatPanel`; `records()` reads ledger rows; `consumption.report(start,end,as_of)`
  gives `accepted_proposals` and cost fields. Existing tests assert pieces, none scan every SQLite row for
  raw-content sentinels across all registered assistants.
* Wave-1 gap: pure `shape_result` and `Consumption` only; no all-assistant end-to-end sentinel sweep and no
  tariff-enabled chat leak scan.

## Planning Readiness

Ready. Disposition: executed. Approach: reuse existing test fixtures from a standalone probe script;
no `src/` or `docs/` edits. Loopback 127.0.0.1 HTTP stub is the existing offline pattern (no external network).
