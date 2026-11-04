# Plan: gate workflow matrix drift (2026-11-04)

* Re-pin `src-ci.yml` in `WORKFLOW_HASHES` (keep the check strict; no relaxation).
* Add a regression test classifying every real src-ci.yml job/step and checking the pin.
* Run tools unit tests, ruff, mypy --strict, focused gate. Focused tier only.
* Critique: executed once, verdict compatible; no weakening of the drift check.
