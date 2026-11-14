---
title: Issue 74 Criterion 2 plan
ms.date: 2026-11-14
---

## Plan

* [x] Add API payload separation test and `app.js` render-source region test to `src/api/tests/test_home_case_api.py`.
* [x] Add `check_regions_apart` two-way leakage, sub-heading and non-nesting checks (ZF-2 and ZF-3) to `src/api/checks/home_case_browser_check.py`.
* [x] Manifest invariant: inspected; `home_case_browser_check.py` is not tracked, no SHA change; run manifest and needs-inventory tests.
* [x] Run the browser check under the canonical non-queued heavy lock.
* [x] Focused validation: unit tests, ruff check and format, mypy.
* [x] Clean caches and commit locally without pushing.

## Validation tier

Focused (small test and check change, no gate-tool, workflow, dependency, infrastructure, SQL or security-control change). Basis: only a unit test file and a local-only browser check changed. Critique: single-pass self-critique found no conflict with the owner's direction; no divergence.
