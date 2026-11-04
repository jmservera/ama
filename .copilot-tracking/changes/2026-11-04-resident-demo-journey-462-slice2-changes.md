---
title: Changes for #462 slice 2
ms.date: 2026-11-04
---

* Banner: shorter wording, same boundaries (synthetic, shared sign-in is not proof, not for decisions, Legal and Data Protection Officer review outstanding).
* Sign-in page: signed-out lede ("Sign in to see how your home improvement is going..."); intro says "Enter"; empty-field errors name the field and set `aria-invalid`.
* History: times in UK time (en-GB), "UK time" labels, no "UTC" text; `datetime` attributes remain exact UTC; chart axis labels larger and no longer clipped at 320px.
* Sign-out: shorter failure message that keeps the 30 minute fact.
* Tests: three static unit tests; one browser-check assertion.
* Validation run: `tests.test_resident_demo_api` (45 tests OK), `checks/resident_sensors_browser_check.py` (all PASS), ruff, mypy. Not run: `resident_demo_browser_check.py` (needs a SQL server), assistant browser checks, full suites, gate, deployment.
* Amendments or divergences: none.
* Amendment after independent review: the SQL-backed `resident_demo_browser_check.py` asserted the old banner and sign-out failure wording; updated both assertions (not executed, needs SQL).
