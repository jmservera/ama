---
title: Issue 129 research, journey learning-test bundles (2026-11-17)
description: Measure of doc versus module drift for the five learning-test bundles
ms.date: 2026-11-17
---

## Scope

Issue #129, evidence-only docs and tests, FOCUSED tier, base `eb51af5c9`. No #1818/#1641 scope.

## Disposition

Research executed. Planning Readiness: Ready.

## Measured findings

* Delivered on main: protocol doc, `learning_test_bundles.py` (scorer, run validation, stop-first report, bounded constructed-input CLI from #1374), core tests, and `src/api/tests/test_learning_test_bundle_scenarios.py`.
* Bundle table in `docs/reference/research/ux/journey-learning-test-bundles.md` agrees by hand with `BUNDLES` (atlas IDs, comparator, requirements, stop rule, target-zero measures). No test enforces that agreement, so the protocol and the scorer can drift silently.
* The protocol's "Next slices" section lists only slices two and three; it omits the CLI slice and the cross-layer scenario tests, and its `ms.date` is 2026-11-04.
* Criteria 1 and 3 remain unmet: they need live participants, the Atlas owner and the DPO. Nothing here closes them.

## Chosen smallest fix

1. A regression test parsing the protocol bundle table and comparing it to `BUNDLES`.
2. A doc update recording the CLI and scenario slices, keeping all unmet criteria unmet.
