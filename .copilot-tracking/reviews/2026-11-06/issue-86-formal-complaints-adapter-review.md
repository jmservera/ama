---
title: Issue 86 formal-complaints adapter author review (2026-11-06)
ms.date: 2026-11-06
---

Scope: issue86 only. Author Review of source commit `30b5ccb0a` (single pass, not repeated). This is NOT an independent exact-head assessment; one is still required.

Execution: executed by the author against the diff, plan supplement and critique dispositions. Outcome: conformant for the admitted slice with open items routed below; no human review boxes are ticked.

## Checked

* Default unconfigured and no network code: confirmed (`receiver_from_env` accepts only `unconfigured`).
* Local request preserved; local recording distinct from receipt: tests compare the request without `formal_route` before and after.
* Failure state and request/receipt identity preserved: Failed, Pending and Acknowledged keep `request_id`, `route_key` and `request_version`.
* Independent-review safeguards: named reviewer only, independence re-asserted, no manager bypass.
* Resident access under holds: asserted; the action never consults holds.
* SQL replay cannot double-send: handlers hold no side effects and the receiver is called outside them.
* All 7 critique findings have a recorded disposition; none silently dropped.

## Open findings routed to later work (not fixed here)

1. Free text in `summary` and `desired_outcome` is sent unscreened to a receiver; needs DPO/Legal decision before any real receiver (later Research).
2. Receiver-side dedupe on `route_key` is unverified; a lost outcome save leaves Pending that needs a human check (later Plan with a real receiver contract).
3. No concurrent two-process proof for two reservations (only the single-store Pending guard is tested); heavy SQL service tests belong to the coordinated full gate.
4. No web control or resident-facing surface; `panels.js` text remains accurate. Any UI needs the web-design-guidelines load and Fluent 2 / WCAG review.
5. `followup_view` does not show a Not sent default (removed to keep the legacy exact-shape contract); a read view is a later optional change.
6. Operational criterion 4 (reach independent review and the formal route without detriment) is unproven; remains unticked.

## Gates still pending

Full local receipt gate (`tools/rpi-checks.py --all`, handoff to the coordinator after issue1231r9 releases heavy capacity), independent exact-head review, hosted CI, human approvals. Future PR uses `Refs #86`, never a closing keyword.
