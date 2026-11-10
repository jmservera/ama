---
title: Quality sensor demo 1288 C5 research
ms.date: 2026-11-08
---

Recorded 2026-11-08T21:59Z, before any C5 product or test edit. Start head `b938ed73`, tree `d011e210`. Refs #1288, #107. Owner authority: final of three extra bounded cycles after C1 and C2, this issue only; consent, safety, human review, spend and live-model gates are not waived. Tier: FULL (SQL consent/control, security-sensitive projection), later and separately admitted. This cycle uses light SQLite and static checks on synthetic data only.

## Source read

* Independent C4 review `review-1288-b938-functional/functional-findings.json`: request_changes, 6 High, 2 Medium. Read completely.
* Code read at head: `sensor_view._controls`, `assistants._serviced/_due/_enqueue/claim/execute/_view/review_flag/build_request`, `sensor_view.capture_source/view`.

## Findings confirmed against source

* C5-1 High: `_controls` checks marker count, control count and the home's index digest. The marker is written at reconcile; nothing invalidates it when a control body changes. Changing only B1's `home_id` to A leaves marker, counts and A's digest valid, so A reads `granted` although B1 (declined) now names A. Confirmed by reading; red test planned.
* C5-2 High: `_due` returns true for an existing exact task id, `_enqueue` returns the old terminal `stale` row, and `claim` only takes pending or leased. Exact A-B-A therefore yields no runnable work. Applies to every capability.
* C5-3 High: `_serviced` skips every zero-attempt stale task, so each same-bucket arrival before claim stales the task and the next scan creates another. No dispatch, no allowance use, unbounded rows.
* C5-4 High: after a returned proactive result, the next reading changes the exact signature; `_view` marks it stale and `review_flag` becomes `not-current`. The coarse schedule refuses a replacement, so the flag is gone for up to six hours.
* C5-5 High: claim revalidates the snapshot, then `execute` runs a separate pre-dispatch transaction that checks suspension, admission, epoch and release only. Withdrawal committed after claim is not seen; `build_request` sends the claimed readings.
* C5-6 High: `_serviced` selects and decodes every historical task body for the case and capability on every scan and forecast; `assistant_tasks` has no case index.
* C5-7 Medium: the model request carries no as-of time and no freshness state; only `view()` computes staleness.
* C5-8 Medium: the future probe stops one day after the request, so a reading two days ahead is reported as absent with `future_dated_excluded` false. The consumer policy allows 31 days of skew.

## Design decisions (evidence-driven, smallest coherent)

* C5-1: SQL triggers on `sensor_consumer_control` (insert, update, delete) delete the index marker, so any control change outside `configure`/reconcile fails consent closed until `migrate()` rebuilds it. The marker carries `v: 2`; the reader also requires the guard triggers to exist. A C4-format marker or a store without triggers therefore fails closed until migrated. `configure` and reconcile rewrite the marker after their control writes. No request-time fleet scan.
* C5-2/3/6: a compact `assistant_schedule` row per (capability, case): scope (release and epoch digest), coarse signature, task id, time. `_due` reads that row and the exact-id task by primary key only. A queued proactive task whose capture moved within the same coarse schedule is refreshed in place at claim (event recorded), so churn never creates a second task. A never-dispatched stale task is requeued when its exact evidence is current again (any capability, scan or manual).
* C5-4: a returned proactive finding stays a `review-suggested` flag when the only difference to the current capture is newer sensor evidence in the same coarse schedule; the flag states the captured as-of and that newer readings exist. Acceptance still requires current evidence.
* C5-5: the consent hold is re-checked in the pre-dispatch transaction and again immediately before the provider call (inside the dispatch thread). Residual: a withdrawal committed after the last check and before bytes leave is ordered after dispatch and is projected as withheld.
* C5-7: the claim stores `dispatch.as_of`; `build_request` adds `request_as_of` and a freshness state (`fresh`, `stale`, `unknown`) to the sensors source. It never enters the signature, so unchanged evidence keeps its identity. The flag carries the same fields.
* C5-8: the future probe has no upper bound (one indexed row).

## Boundaries

No web edit planned. No SQL Server, Docker or browser (the heavy lock is not ours). #184 is unmerged and not integrated. Mock providers only; none is live AI.
