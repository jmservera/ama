---
title: Issue 432 resident host wiring and output link research
ms.date: 2026-11-13
---

## Scope

Stacked on `edf4ccf14`. Closes residuals from the 1905 exact-head review: output linkage, unclosed reservation on non-`ValueError` exceptions, and caller-driven wiring of advisor meters in `configured_advisor`.

## Evidence

* `ledger_meter.py` `LedgerTopicMeter.reserve` creates a root reference and keeps only the reservation id; `close` calls `Consumption.complete` and never links an output.
* `Consumption.publish_output(root, output, eligible=...)` writes an immutable `output` record; holds are logged and returned, so it cannot break manual delivery. Output ids pass through `reference()` (bounded, opaque).
* `aoai.py` `_request`: `acquire()` catches only `ValueError`; `meter.token` guard can propagate other errors. Transport catches `Exception` (closed). Between `acquire()` and transport, other failures are not closed.
* `assistant.py` `select`: `self.token()` and `reserve` may raise non-`ValueError`; only `OSError` at transport is closed. Other exceptions leave the reservation open.
* `configured_advisor` accepts `meters` only; hosts must hand-build them.
* `__main__.py` supplies no ledger, price or authority, so production stays unmetered. No owner approval exists to change that, so it stays unchanged.

## Planning Readiness

Ready. Research disposition: executed.

## Decisions

* The output record is always `eligible=False` (nothing is accepted by a human), content-free (random reference), and written only after a close that follows an admitted reservation.
* No host wiring in `__main__`; only the supported API in `configured_advisor`.
