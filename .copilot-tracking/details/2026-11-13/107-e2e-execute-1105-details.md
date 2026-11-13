---
title: Issue 107 end-to-end execute probe details
description: Probe design details
ms.date: 2026-11-13
---

## Probe design

* Runs with cwd `src/api/tests`, imports `ConsumptionApi` (instantiated manually, `setUp()`, `doCleanups()`).
* Sentinels: `SENT-NOTE-<hex>`, `SENT-DOC-<hex>`, `SENT-CHAT-USER-<hex>`, `SENT-CHAT-REPLY-<hex>`; case note/document
  summary set through `fixture.case`; chat reply text via `response_text`.
* Assistants: every `REGISTRY` key. Each is authorised with `authority(cap)`, run with the PM role via
  `invoke` + `execute`; where invocation is refused for the role or case, record as skipped with reason (not silent).
* Accept: `service.review(pm, id, "verify", revision, note, source_verified=True)`.
* Attribution: per task, ledger `reserved` row `root == reference(task id)` and `configuration`, `prompt`
  match the envelope; `output` row eligible and reviewed; `report().accepted_proposals` equals accepted count.
* Chat: `chat_panel(store).ask(pm, thread, SENT-CHAT-USER...)` with `authority(TASK)`; assert `meter_root` set,
  `output.eligible` false, audit rows non-empty.
* Leak scan: dump every table of the SQLite file (text, blobs decoded) plus ledger records and report JSON;
  allow sentinels only in domain tables that legitimately hold the case (`cases`, `chat_*`, `assistant_tasks`
  body) and require zero in `assistant_events` ledger/telemetry rows, report output and envelopes' usage fields.
  Report per-table hit counts so the allowlist is visible.

## Critique amendments (C1 to C6, applied)

* C1: after `verify`, call `review(..., "accept", new_revision, ...)`; assert task state and a ledger `review` record.
* C2: any skipped or failed capability fails the probe; executed set and accepted set must equal `set(REGISTRY)`.
* C3: per capability join reserved, completed, output and review rows by meter id, root, attempt, output id; assert
  tokens (100/20/120, cached 10) and `by_capability` metrics; `accepted_proposals == len(REGISTRY)` and chat separate (not eligible).
* C4: seed a captured field (home address) with a sentinel and a provider response with a sentinel; assert each
  appears in the request or response seen by the fake provider before scanning; case notes and document summaries
  are excluded by `capture` and asserted absent from requests.
* C5: no table-wide allowlist. Scan ledger rows (`assistant_events` where `task_id='ai-consumption'`), audit receipts,
  `report()` JSON, and `envelope` JSON of every task and chat receipt. The only exempt locations are named
  domain-content fields (`cases.body`, task `output`, chat message text) and are listed with hit counts.
* C6: chat uses `store.ai = inner`, `chat_create_thread`, JSON answer with citations containing the sentinel reply;
  assert answer kind, `meter_root`, exact output join `chat:{thread}:{seq}`, `eligible` false, accepted count unchanged.
