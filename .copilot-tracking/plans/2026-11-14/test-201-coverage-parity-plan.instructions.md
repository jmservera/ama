---
title: Issue 201 coverage baseline parity plan
ms.date: 2026-11-14
---

Refs #201. Focused validation tier (non-gate tooling test only).

* [x] Phase 1: add `tools/test_src_coverage_baseline_parity.py` (wiring, count floors, threshold and disclosure guards). Details: [details](../../details/2026-11-14/test-201-coverage-parity-details.md).
* [x] Phase 2: run unittest, `ruff check`, `ruff format --check`.
* [x] Phase 3: critique once (self-critique recorded in details); no edit to `docs/architecture/cutover-evidence-pack.md`.

Critique (single pass): the test must not claim measured coverage; it asserts the disclosure instead. Applied directly.
