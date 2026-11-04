---
title: Changes, issue 153 consultation and restart check wording
ms.date: 2026-11-04
---

## Changed

* procurement.py, gates.py, test_content_standard.py, content standard, log.

## Validation (focused tier, venv in /tmp, no bytecode)

* Run: api test_content_standard and test_procurement_api (53 OK); core test_consultation_controls (45 OK, 16 skipped) and gates tests (10 OK); ruff check on core src and tests and the api test (pass); mypy --cache-dir=/tmp/mypy-153 on core as CI runs it (tests included, no issues, 254 files).
* api mypy as CI runs it: 42 import-not-found errors for optional packages (for example playwright) not installed here; no error in touched files.
* ruff format --check reports pre-existing reformatting in procurement.py, unchanged before this change; not applied.
* Not run: gate, benchmarks, full suites, browser or accessibility checks, human wording review.
