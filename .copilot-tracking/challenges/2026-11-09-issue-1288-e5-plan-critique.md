---
title: Plan critique - issue 1288 E5
---

# Plan critique, issue 1288 E5 (one pass, executed by a rubber-duck subagent; not independent)

Scope: research, plan and details drafted before any source edit. Verdict: eight findings, all compatible with confirmed owner direction; all applied directly, none rejected, no user decision needed.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Plan kept 600 output tokens and 20 s although authority may permit less. | Applied: `Admission.bounds()` gives `min(600, limits.output_tokens)` and `limits.timeout`; the body is composed and sealed with them; reduced-limit test. |
| 2 | Blocking | A call stalled before dispatch can outlive its durable lease. | Applied in part: the lease is `limits.lease` (at least timeout + 5 s) and the call starts immediately after admission; the process-local physical slot is held to return. A meter stall longer than the lease is disclosed as a residual limit, as for ordinary tasks. |
| 3 | Blocking | Reservation before local slot acquisition needs compensation. | Applied: the physical slot is acquired first (non-blocking), then the one transaction; no compensation exists. An ambiguous commit keeps the reservation as liability, never replayed. |
| 4 | Blocking | Settlement must be one-time and slot ownership explicit. | Applied: `begin_call` returns a ticket whose `end` is idempotent under a lock; the SQL settle selects only an attempt still `reserved`; the slot is released once. Duplicate and concurrent end test. |
| 5 | Blocking | Stored readings are triples; `key_of` needs a mapping. | Applied: keys rebuilt from the fixture sensor id and reading id; historic-row test. |
| 6 | Non-blocking | `finally` must cover mint and context setup. | Applied: admission is released in `finally` around mint, context and call; pre-dispatch failures settle like ordinary pre-dispatch holds (reservation kept as liability, conservative, as in `execute`). Mint-failure test. |
| 7 | Non-blocking | Unavailable SQL while admitting. | Applied: `begin_call` fails closed with a manual-route reason on `store.dberror`, slot released; `simulation_act` authorizes first as before. Test. |
| 8 | Non-blocking | SQL Server coverage of the new paths. | Applied: the new tests run inside the API suite on the owned SQL Server backend in the single non-queued heavy admission; identifiers fit (`id` VARCHAR(100), `task_id` VARCHAR(64) via a 64-hex reference). |
