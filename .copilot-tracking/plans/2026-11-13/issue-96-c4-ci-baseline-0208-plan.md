---
title: Issue 96 C4 plan, accessibility baseline eighth invalid-field site
description: Prospective plan for one tests and record correction after the hosted 8 != 7 failure
ms.date: 2026-11-13
---

## Objective

Make the baseline audit truthfully cover the saved Held copy field, with no product change. Research: [research](../../research/2026-11-13/issue-96-c4-ci-baseline-0208-research.md). Details: [details](../../details/2026-11-13/issue-96-c4-ci-baseline-0208-details.md).

## Phases

* [x] Phase 1: research and failing-first reproduction of `8 != 7` on the exact candidate (done before this plan).
* [ ] Phase 2: independent critique once (read-only); apply compatible findings.
* [ ] Phase 3: edit `src/api/tests/test_accessibility_baseline.py` and `docs/reference/research/ux/wcag-conformance-baseline.md`; append `docs/reference/log.md`.
* [ ] Phase 4: validation: focused baseline module, RoleScreens and RoleScreenConformance (21 tests), ruff and mypy on the changed test file as configured.
* [ ] Phase 5: changes record, freeze commit, original Review once, result file, STOP.

## Constraints

* C4 of 5 against the current scoped 96 budget, one remaining afterwards. No retry, no C5, no 233 authority, no optional repair.
* No product JS, CSS, backend, tools, infra, manifests, workflows or browser recipes. No whole-suite or full-gate rerun; the hosted failure stays preserved.
* No immutable original RPI or earlier log edits; no push, PR or merge.
