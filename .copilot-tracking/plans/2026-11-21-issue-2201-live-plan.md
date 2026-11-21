---
title: Issue 2201 plan and critique
ms.date: 2026-11-21
---

## Plan

* Add keyword `bounded_window` (default False) to `HubReceiver.run`. When True: reaching the window deadline or event cap returns the receipts (normal end); an event refused by `decode()` is skipped, never stored or counted as a receipt, and tallied by reason code on `receiver.rejected`. SQL, receive-link and cleanup failures stay fatal. Default behaviour is unchanged for existing callers and tests.
* `live_receiver.run_window` passes `bounded_window=True`; `main` prints `receipts=N rejected=M` plus reason counts to stdout/stderr (codes only, no payload) so a future log shows the cause.
* Regression tests: a window that ends on the deadline returns normally; a foreign-device event is skipped and the following valid event is stored; SQL failure stays fatal. Update the two fake receivers' `run` signature.
* README note; research note under docs/reference/research; knowledge-base log entry.
* Tier: FULL (src change) but the coordinator owns the full gate; run targeted tests, mypy and ruff only. No push, no Azure writes; deployment and three scheduled successes are unproven for the demo.

## Critique (executed once)

* Risk: skipping refused events could hide a spoof attempt. Disposition accepted: events are never ingested, are counted by code and reported; strict mode remains the default and for non-window callers.
* Risk: ending on the deadline could mask an idle hub. Disposition accepted: receipts count is printed; idle is not a fault for a polling job.
* Verdict: proceed.
