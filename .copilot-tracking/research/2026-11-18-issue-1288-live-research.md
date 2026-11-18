# Research: issue 1288 live demo verification (2026-11-18)

Refs #1288. Demo, desktop only, docs and evidence only (no src change, FOCUSED tier). Research disposition: executed. Planning Readiness: Ready.

## Findings

* Criteria 1, 2 and 9 are already ticked. Open: 3 to 8.
* Source: quality-evidence capability in `src/core/.../assistants.py` (categories include `sensor`; one proposal per six-hour bucket of latest reading); read model `GET /api/cases/{id}/sensors` (`retained-reading-view-v2`); focused tests `src/api/tests/test_quality_sensor*.py`, browser check `src/api/checks/quality_sensors_browser_check.py` (local MOCK provider).
* Live demo (revision `ca-cutover-test-demo-api--0000031`, image sha256:5368f4e4...c17e5fb): signed in as Retrofit Programme Manager, only ZF-2025-0031 is in scope (11 other cases 403). `/sensors` returns 12 retained readings with IDs, units, UTC times, `freshness: stale`, no retrofit context; the case Quality tab shows the same values.
* Live release gate: `release.missing` for the approved record (OQ-017 not appointed, per #107 note); `POST /api/assistants/quality-evidence/invoke` returns 202 with `envelope: null`, `release: null`, no provider call.
* No simulator job exists in resource group ama (jobs: init, verify, ledger-verify, import, orchestrator, smoke, mi-http, public-audit); latest retained reading is 2026-11-18T07:40Z from earlier live run.

## Disposition by criterion (to plan)

* 3, 5, 6, 7: local engineering proof from focused tests and browser check (labelled local, mock provider) plus live read side.
* 4, 8: cannot be proven for the demo: needs approved release record (no appointed approver), a model-attributed returned flag, and an admitted simulator run. Creating either is out of scope.
