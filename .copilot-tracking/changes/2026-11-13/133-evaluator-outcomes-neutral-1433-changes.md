---
title: Issue 133 evaluator outcomes and neutral text changes
ms.date: 2026-11-13
---

## Changes

* `src/core/src/zava_forward/core/aftercare.py`: `neutral_text` also rejects paraphrased savings, causation and blame patterns; clauses stating uncertainty are not scanned by those patterns.
* `src/api/src/zava_forward/api/web/aftercare.js`: evaluator table gains an Outcomes column (counts per home from `row.concerns[].outcome`; unlabelled values show Unknown; no concerns shows No concerns raised).
* `src/core/tests/test_aftercare.py`, `src/api/tests/test_aftercare_screen.py`: RED-first tests, then green; static scan of all `aftercare.js` string literals through `neutral_text` and the banned-term check.

## Validation

* Core `test_aftercare*` 111 tests OK (15 skipped), `test_scenario_manifest` OK; api `test_aftercare*`, `test_content_standard`, `test_scenario_manifest` OK.
* `ruff check` and `ruff format --check` clean in core and api; core `mypy` clean. api `mypy` reports only environment-missing playwright imports; `aftercare_browser_check.py` untouched.
* No divergences from the plan beyond the critique amendments.
