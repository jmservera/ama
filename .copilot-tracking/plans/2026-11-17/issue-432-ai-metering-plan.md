---
title: Issue 432 AI metering inventory plan
ms.date: 2026-11-17
---

## Objective

Refs #432. Record a current-main inventory of AI metering, correct the stale gap statements, name the
smallest next step, and add one small regression test. Docs plus test only; no Core store change.

## Phases

* [x] Phase 1: add a dated "Current-main metering inventory" section to
  `docs/reference/resources/ai-tokenomics.md`, mark the older Gaps rows as superseded where merged code covers them,
  index it in `docs/reference/README.md` and append to `docs/reference/log.md`.
* [x] Phase 2: add `src/core/tests/test_ai_metering_inventory.py`, which fails if a code symbol or test file named in
  the inventory no longer exists, and if the report stays `Unknown` cost with no price or billing evidence.
* [x] Phase 3: run the targeted tests, ruff format check and mypy for `src/core`; record in changes and review.

Details: `.copilot-tracking/details/2026-11-17/issue-432-ai-metering-details.md`.

## Critique (single pass, final candidate)

Plan is minimal and compatible with the scope. Risks: the doc must not claim criteria 5 or 8 proven; the test
must not depend on private data. Both applied directly. Verdict: proceed.
