---
title: Issue 154 changes
ms.date: 2026-11-01
---

* Added `src/core/tests/test_resident_journey_design.py` (8 tests, passing).
* Validation: ruff check, ruff format --check and mypy clean on the file; `python3 -m unittest discover -s tests -p test_resident_journey_design.py` OK.
* Divergence: none from the plan.

## Review feedback round (PR 664)

* Test now has 9 tests: J4/J5 content assertions, whitespace-normalised accessibility check, and all seven validation script rows must keep a populated result (Not run or recorded outcome).
* Added `docs/reference/research/ux/customer-journeys/residents.md` to the `src-ci.yml` pull-request path filter so documentation-only edits run the check.
* Validation: unittest 9 OK; ruff check and format clean.
