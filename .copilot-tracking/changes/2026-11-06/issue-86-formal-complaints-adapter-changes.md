---
title: Issue 86 formal-complaints adapter changes (2026-11-06)
ms.date: 2026-11-06
---

Scope: issue86 only. Source commit `30b5ccb0a`. Plan, supplement, details and critique are in `.copilot-tracking/{plans,details,challenges}/2026-11-06/issue-86-formal-complaints-adapter-*`.

## Files

* `src/core/src/zava_forward/core/complaints_route.py` (new): `UnconfiguredReceiver`, `receiver_from_env` (only `unconfigured`), `build_envelope` (exact allow-list), `parse_acknowledgement`, fixed reason texts.
* `src/core/src/zava_forward/core/resident_decisions.py`: `service_forward` action; `_forward` orchestration (reserve, send outside lock, record outcome); handlers `_res_service_forward` and `_res_service_forward_outcome`; retention clears `resident_request_ref` and `requested_by`.
* `src/core/tests/test_resident_decisions.py`: 7 shared JSON/SQLite tests plus a configuration test and `SyntheticReceiver`.
* `src/core/README.md`: boundary section.

## Divergences and amendments

* Plan supplement design (two-phase) was implemented, not the original single-step handler.
* Plan item "followup_view exposes formal_route defaults" was tried and removed: it broke the existing exact-shape legacy test `test_mixed_closure_clocks_survive_unrelated_transitions_and_restart` (2 failures, JSON and SQLite). Retained as adverse result. `formal_route` now appears on a request only after an attempt.
* `service_forward` is not in `FOLLOWUP_ACTIONS` because it is orchestrated; it is in `RESIDENT_ACTIONS`, so the API dispatch works unchanged and `ResidentCommittedError` maps to the existing 409.
* No web change: `panels.js` text stays truthful.

## Validation tier and commands

Tier FULL selected (receipt persistence and access boundary). Not run: the complete gate, SQL/browser services, Docker, scanners, heavy installs (issue1231r9 owns heavy execution). Environment note: `zava-forward-core` is editable-installed from the primary checkout, so every run used `PYTHONPATH` pointing at this worktree's `src` and import identity was printed (resolved under this worktree). Scratch: `/mnt/ama-gates/restart-1106-86-complaints`. `PYTHONDONTWRITEBYTECODE=1`.

| Command (from `src/core`, `PYTHONPATH=src:tests`) | Result |
| --- | --- |
| `python3 -m unittest -k forward -k ComplaintsRoute test_resident_decisions` before source | exit 1, 13 errors (RED, expected) |
| same after source | exit 0, 25 tests, 8 skipped |
| `python3 -m unittest test_resident_decisions test_resident_preview test_perspective_walkthroughs` with the followup_view default | exit 1, 2 failures (retained, see above) |
| same after removing it | exit 0, 321 tests, 101 skipped (Azure/Mssql, no service) |
| `src/api`: `PYTHONPATH=tests:src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest test_resident_api` | exit 0, 20 tests, 1 skipped |
| `ruff check` on the three Python files | one failure (6 E501) then fixed; final pass |

Tests prove: default unconfigured; Failed (raise and malformed) with no receipt, stable `route_key`, unchanged local request; Acknowledged receipt stored separately, exact envelope keys, second send refused, single receiver call under SQL validation replay; denied roles, stale version, missing reference, wrong route; named-reviewer and independence safeguards (non-reviewer manager refused); access under authority and tenure holds without leaking private references; outcome-save failure leaves Pending and blocks silent resend; retention clearing.

## Not implemented

Real receiver and destination, appointment, UI control, delivery SLA, envelope free-text screening, receiver-side dedupe verification, concurrent two-process proof, and the operational criterion that residents reach the route without detriment.
