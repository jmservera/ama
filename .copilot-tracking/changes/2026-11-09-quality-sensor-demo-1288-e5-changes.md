---
title: Changes - quality sensor demo, issue 1288 E5
---

# Changes, issue 1288 E5 (final additional cycle; 1 High, 2 Medium E4 findings)

Start `25434bb03`. Source commit `c8afa77bb`. Refs #1288 only.

## F1 High: finite operator authority

* `assistants.py`: `claim` and `complete` now share `_reserve` and `_settle`. New `Assistants.begin_call` takes the physical active-call slot without waiting, then in one transaction applies the disabled, expiry, release, input bound and durable reserve checks. New `CallTicket.end` settles once and always frees the physical slot.
* `simulation_lane.py`: `Admission` and `Ticket`; `Lane.request` admits before minting a seal, so declines happen before meter, token and socket.
* `server.py`: `App.simulation_admission` wires the existing authority.

## F2 Medium: supplied versus cited readings

* `last_proposal` adds `cited`; `readings` stays the supplied set. `ops.js` states "given N, cited M", handles zero cited and empty findings.

## F3 Medium: optional key and store failures

* `_read_key` and `Lane.open`/`__init__` translate OSError and sqlite3 errors to explicit `Unavailable` codes and close partial stores. Tested through real `App` construction.

## Validation (SQLite and owned SQL Server 2022 CU27)

* Failing-first lane: 23 tests, 9 failures and 8 errors on unchanged source (a few errors were test bugs fixed afterwards). Green: 23 OK. Browser failing-first exit 1 at the new cited-count check.
* Impacted API modules green. Core 53 OK. Browser and axe: 29 checks passed.
* Owned SQL, one non-queued admission on committed head `96da7bae0`: API 577 OK, 1 SQLite-only skip, exit 0; core 53 OK, exit 0; container removed.
* mypy: 0 errors in changed files. Ruff clean on the two new E4 files.

## Limits and disclosures

* Pre-existing, not E5: `test_role_endpoint_inventory` lacks the three E4 simulation routes (fails on clean HEAD too).
* A pre-dispatch stall longer than the lease can free the durable slot; the suspension and withdrawal race is not atomic.
* No live, Azure, model or actual provider/admission activation; the finite LIVE step is unperformed. SQL 1292 fix (PR 1308) is not in main, so no shared integration.
