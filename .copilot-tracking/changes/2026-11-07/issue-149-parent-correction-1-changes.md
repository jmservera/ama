---
title: Issue 149 parent correction 1 changes
ms.date: 2026-11-07
---

## Changes

Base main b284d0d3; baseline e2704c2b. Source commits 9c85d4c4 and 47161a52 (checker and tests only, `src/api`).

* `checks/data_operator_ai_state.py`: added `FAILED_AI_KIND`, `failed_ai_rows` (select by Kind cell) and `says_failure_outcome`.
* `checks/data_operator_browser_check.py`: failed rows are now selected by the Kind cell in the Items region, each synthetic ID must appear exactly once, and every failed row must state its failure outcome.
* `tests/test_data_operator_ai_state.py`: two regression tests (extra fallback row accepted; third failed row with a wrong or missing sentence rejected; rendered Kind cell equals the label).

No product HTML, CSS, JS, server, auth, store, model, SQL or deletion change.

## Validation (focused, light; installed distributions byte-identical to the candidate, 211 files, 0 differing)

* Red before the fix: `/tmp/zf149-correction1-red-1107/red.log` (counterexample accepted).
* Green, archive `/tmp/zf149-correction1-1107`: 74 API tests OK; 19 core tests OK (needs inventory, scenario manifest); ruff check exit 0; ruff format 119 files formatted (the `checks/*.py` files are configured exclusions, so the checker is not claimed formatted); mypy strict 193 files, no issues. One first-run failure of the new rendered-cell test (wrong column assumption) was fixed in 47161a52; log retained as `unittest-api.log`.

## Pending

Corrected maintained browser check (atlas and data operator with required axe 4.10.3) on the final source awaits coordinator admission. Earlier e2704c2b browser results are historical. Independent review, human, AT and whole-issue acceptance pending. Refs #149 only.
