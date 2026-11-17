---
title: Issue 1845 withdrawn-sensor canary repair plan
description: Test-only plan replacing a substring canary search with a digit-bounded decimal match plus constructed-metadata regressions
ms.date: 2026-11-17
ms.topic: reference
---

## Context

* Research: [issue1845-withdrawn-canary-research.md](../../research/2026-11-17/issue1845-withdrawn-canary-research.md)
* Details: [issue1845-withdrawn-canary-phase-details.md](../../details/2026-11-17/issue1845-withdrawn-canary-phase-details.md)
* Base `main` f1df574bba2b94cd83bb2a783079ec94cd584c90, branch
  `test/withdrawn-sensor-canary-1845`. Eventual PR target `main`; this launch
  does not push or open a PR.
* Validation tier: FULL (conservative, privacy-regression guard). A focused
  downgrade is only a proposal for coordinator assessment.

## Objective

Make `Http.test_withdrawal_withholds_uncited_derived_text_and_edited_output`
distinguish withdrawn original and edited text from incidental numeric
metadata, with no loss of disclosure coverage.

## Revision note

The first draft used a digit-bounded regex over serialized JSON. The
[plan critique](../../reviews/plans/2026-11-17/issue1845-withdrawn-canary-plan-critique.md)
(verdict Revise) found it could miss `23.70`; the matcher and the
failing-before design below are the revised versions.

## Phases

* [ ] Phase 1: add the matcher helper and use it in the existing test.
  * Add a module-level `exposes(body, value)` that walks the parsed
    projection: string values and keys keep the substring check; numeric
    leaves match by numeric value, so an epoch timestamp no longer collides.
  * Replace the four-projection `assertNotIn` loop on serialized text with
    `assertFalse(exposes(body, derived), name)`; keep projections, canaries
    and names unchanged.
  * Convert the two pre-withdrawal `assertIn` positive controls to
    `assertTrue(exposes(...))`.
* [ ] Phase 2: add constructed-metadata regressions (new `unittest.TestCase`).
  * Clean colliding timestamps are accepted, with the old substring semantics
    shown to collide.
  * Original text, edited text, a key, `23.70` and a bare numeric reading are
    detected, also when the colliding timestamps sit in the same body.
  * Known limit: a numeric leaf exactly equal to the canary counts as
    exposure (conservative).
* [ ] Phase 3: prove failing-before and passing-after without the clock.
  * Failing-before: in a scratch copy with the old substring assertion,
    inject clean colliding timestamps into each projection and show the
    integration test fails; with the fix it passes. Then inject each
    canary (original and edited) into each projection one at a time and show
    the fixed test fails on that named projection.
  * Passing-after: targeted selectors with zero unexpected skips.
* [ ] Phase 4: static checks and receipts as listed in the details.

## Out of scope

Production code, authorization, providers, permissions, gates, #1641, browser,
SQL, Docker, scanner, image or full gate runs, the immutable 1837 receipt.

## Success criteria

* Corrected regression accepts constructed clean timestamp metadata containing
  `23.7` and `24.9` and still fails on actual original or edited text in each
  applicable projection.
* No privacy assertion deleted or weakened; no skip, xfail, retry,
  exception suppression or blanket metadata stripping.
* `git diff` touches only `src/api/tests/test_quality_sensors.py` plus
  original dated RPI artifacts.
