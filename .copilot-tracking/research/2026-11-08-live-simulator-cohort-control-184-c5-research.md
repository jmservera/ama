---
title: "#184 C5 research: readers must enforce the 14-day control maximum"
ms.date: 2026-11-08
---

Prospective record, committed before any source or test edit. Owner authorized one bounded receiver correction cycle for this gap only.

## Start identity

* HEAD 10c550a8cbd4beb54a758d69b4dd03faa4e56b06, tree 725fe08069d2bbf94088a83840155f0c392d289c, tracked tree clean. Product and infra source equal the f28e278d candidate.
* Preserved and unchanged: C4 research, plan, tests, changes, review, the full-tier amendment and the independent f28 review (approve_with_comments: one Medium control-contract defect, one carried Low gap).

## Demonstrated defect

* Coordinator probe 184-10c-expiry-probe.out: a synthetic 365-day control gives reader decision SEND while the start CLI refuses it with CONTROL_WINDOW_INVALID. No live system was involved.
* Cause in src/api/src/zava_forward/api/live_control.py: the 14-day maximum (MAX_WINDOW) is enforced only by `check_window`, called from the start CLI. `decide(control, now)` checks only expiry and `enabled`. The simulator gate (live_simulator.py, gate) and the receiver (`window_seconds` and `_watch` in live_receiver.py) all use `decide`, so a hand-edited or otherwise written file bypasses the finite-window rule, including on refresh and watch.

## Correction contract

* `decide` also refuses an unexpired control whose expiry is beyond now + 14 days, with a new non-SEND outcome INVALID. Callers already treat any non-SEND result as no send and as a receiver stop, so no caller changes are required.
* Already-expired controls stay EXPIRED. Disabled controls stay STOPPED. Exactly 14 days stays valid. Order: expired first, then over-window, then enabled.
* Owner, cohort, approval, stop, refresh and human authorization rules are unchanged.

## Gaps kept open

* Low: restricted-grant live_receiver.main and rejected data-quality SQL coverage is unrelated; not closed here.
* Whole-issue criteria remain unmet. No live, model, accessibility or human acceptance claim.

## Tier

The branch diff includes infra Bicep and SQL source, so the mandatory FULL local gate and external receipt remain pending after this edit. Earlier f28 SQL 70/0 skip and unit 139/2 skip results become historical. This session starts no SQL Server, Docker, browser or heavy gate.

Planning readiness: Ready. Disposition: executed (read-only inspection).
