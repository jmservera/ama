---
title: Issue 432 resident host output link changes
ms.date: 2026-11-13
---

* `ledger_meter.py`: returned calls link an ineligible, content-free output record (`last_output` exposes the reference); new `AdvisorLedger`.
* `aoai.py`: whole admitted pre-transport interval and transport close the reservation on any exception; `configured_advisor(ledger=...)` builds `advisor_meters`.
* `assistant.py`: token and transport failures of any type close the reservation.
* Tests: 3 new in each of two classes of `test_resident_ledger_meter.py`.
* Validation (venv `/tmp/venv-432rh-1921`): api inventory 6, api consumption 38, core consumption 43, api `test_resident_*` 272 OK (9 skipped), ruff and mypy core and api clean. `__main__` host wiring unchanged: no owner-approved ledger or authority.
* Residual: the output reference is not yet joined to a delivery or review path; host wiring in `__main__` remains open.
