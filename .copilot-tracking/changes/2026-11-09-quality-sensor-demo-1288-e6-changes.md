---
title: Quality sensor demo 1288 E6 changes
ms.date: 2026-11-09
---

Refs #1288 only. E6 of the owner grant E6-E10 (comment 6747867150). E1-E5 and C1-C8 records are unchanged.

## Order of commits (local only)

| Commit | Content |
| --- | --- |
| 774c12c56, e39768fae | E6 research, plan, details, independent critique and amendments, before any merge or source edit |
| bd12db5e8 | ordinary merge of origin/main 5c3b8b4be (tree 1720bd5c663015ed14f5f10a33c3c96cfb3eb934), no rebase or force |
| f1f939d78 | Medium: three simulation routes added to test_role_endpoint_inventory, with a per-role refusal test |
| b9efd6eaa | failing-first two-process fence regressions (logs-1288-e6/failing-first-fence.log) |
| 5827ebede | High fix: transport-owning send fence; Core 61 and API 571 strict-mypy errors fixed by annotation |
| 5f44dc4e1 | original review finding fixed: the send-refused event is now committed before the withdrawal is raised |

## High: expired-ticket physical dispatch race

* `ai_transport.py` (new): a fenced HTTP and HTTPS connection. The fence runs before connect and again before the first request byte, with a margin check and a total-deadline timer that closes the socket. The opener has no proxy, redirect or retry handler.
* `assistants.Assistants.fence_send`: one BEGIN IMMEDIATE (SERIALIZABLE on SQL Server) transaction that re-applies the operator authority, suspension, release and allowance-expiry conditions and requires a live `reserved` or `sending` attempt. It restamps the lease to cover the bounded send. A refusal commits a `send-refused` event and raises `DispatchWithdrawn`.
* `ai.Ai._request`: runs the fence before the financial reservation, so a late caller creates no reservation, credential or socket. `send_fence_supported` is true only for this transport.
* `simulation_lane.Lane.request`: refuses with `dispatch-fence-unavailable` before admission when the client cannot fence, and wraps the evidence call in the ticket fence. The ordinary assistant `execute` path installs the same fence.
* Deployment boundary: every dispatcher must share one assistant authority store and one database clock domain.

## Typing and inventory

* Core `sensor_view.py` and `sensor_consumer.py`, API `test_quality_sensors.py` and `test_quality_sensors_c7.py`, and `two_process_worker.py` are annotated. No ignore, cast, stub or config change.
* `test_ai_call_site_inventory` names the send call `open_request` because the call is now the plain or fenced opener; the order assertion is unchanged.

## Validation evidence

Logs are under the coordinator files directory `logs-1288-e6/` and `sql-1288-e6-run/`.

| Check | Result |
| --- | --- |
| API mypy, pinned strict profile from src/api | Success, 210 files |
| Core mypy, pinned strict profile from src/core | Success, 279 files |
| ruff check on changed API files and core files | pass, except two E501 in `sensor_consumer.py` that exist at HEAD |
| Impacted API suites (16 modules) and core suites (6 modules) | all exit 0; lane 28 OK, sensors 187 OK (92 skipped), c7 45 OK (7 skipped), e1 78 OK (29 skipped), e2 62 OK (31 skipped), inventory 23 OK |
| Disposable SQL Server 2022, one non-queued flock -n admission, clean head 5827ebede | API 605 tests OK (1 SQLite-only skip), Core 53 OK, container removed |
| After the review fix (5f44dc4e1): lane 28, assistants 120 (58 skipped), release 54 (4 skipped), consumption API 17, call-site 6, inventory 23, c7 45, core consumption 42 | all OK |

## Limits

* The SQL admission ran before the review fix 5f44dc4e1. The fix only moves a raise after the transaction commits; its SQL Server run is not repeated (one finite admission).
* An OS freeze between the last in-process fence return and the kernel write, or one outlasting the restamped window, cannot be excluded in user space. No provider-side fence token exists.
* The total-deadline timer has no dedicated test.
* No provider is admitted or activated, and no live, model or cloud call was made.
