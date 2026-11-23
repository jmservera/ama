# Research: issue 2202 readings coverage measurement (2026-11-23)

Refs #2202. Disposition: executed. Planning Readiness: Ready.

## Prior work read

* finalproof changes (2026-11-22): unproven or partial criteria are consent checkbox on the latest resident revision, half of homes with readings, map gauges, rollback note.
* Earlier workers only produced docs and probes. The "half of homes" check is done by eye from `/api/map` sensor states (fresh 59, consent-withheld 22, no-readings 19, not-loaded 343 of 443).

## New angle

No repository code measures reading coverage from the map snapshot, so the criterion has no reproducible definition (denominator unstated). Add `tools/demo_readings_coverage.py` with a pure function and a unit test, then run it on live `/api/map`.

## Owner-only or out of scope

Generative AI answers (SUS-1, budget expiry), rollback exercise (would change production), person-run assistive tests.
