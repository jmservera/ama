---
title: "Plan: issue 1362 inherited one correction"
description: One bounded exact-field correction of the Technical queue Current design version assertion
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

Tier: FOCUSED owner demo (checker and its existing unit module only). Not the full or `--changed` gate. Research: `.copilot-tracking/research/2026-11-10-issue-1362-inherited-one-research.md`. Details: `.copilot-tracking/details/2026-11-10-issue-1362-inherited-one-details.md`. Critique: `.copilot-tracking/plans/2026-11-10-issue-1362-inherited-one-critique.md`.

## Objective

Replace the whole-panel substring test of the design version in `check_technical` with an assertion on the one visible, non-blank `dd` that directly follows the one `dt` whose full text is `Current design version`, equal to `str(technical["design_version"])`. The wrong, Unknown, empty, `10`, missing-label and duplicate-label cases must fail even when other panel text contains the digit.

## Authority

ONE inherited #233 to #1362 correction (Root, 2026-11-10; minimum unused balance >= 1 proven, exact balance UNKNOWN). Not a fresh C1 or five, no reset. After this correction the conservative proven remaining minimum is zero; no further automatic correction or self-retry. A refusal or failure stops the task with evidence preserved.

## Phases

* [ ] Phase 1: current-main baseline before the edit. Own pinned environment (`/tmp/ama-1362-env`, Playwright 1.64.0, ruff 0.17.1, mypy 2.4.0, proving version and import origin). Unit module, the full Atlas browser check, and the D1 mutation diagnostic (control and mask) against the unchanged checker, each under `flock -n /tmp/ama-rpi-heavy.lock`. STOP if the false positives are absent or materially different.
* [ ] Phase 2: checker edit. Add `check_design_version` and `DESIGN_VERSION_FIELDS`; remove only the design version value from the substring loop; keep every other assertion.
* [ ] Phase 3: regressions in `tests/test_atlas_tensions_checker.py`: the helper accepts the exact value and rejects wrong, Unknown, `10`, empty, missing label, duplicate label and an invisible field. RED on the unchanged checker (the helper does not exist), GREEN after.
* [ ] Phase 4: candidate verification. Unit module, role conformance, atlas trace test, the full Atlas browser check, the D1 diagnostic control and mask (all negatives must now fail at the new assertion, baseline case 1 passes), Ruff lint and format, strict mypy.
* [ ] Phase 5: changes record with the debit, single Review, local commit, freeze handoff.

## Finite run budget (predeclared, no retry until green)

Baseline: 1 full check, 2 diagnostics. Candidate: 1 full check, 2 diagnostics. Unit, Ruff and mypy runs are cheap and may repeat only for syntax or format fixes before the first candidate browser run; every first error is preserved. A busy heavy lock means HOLD, not queue or bypass.

## Limits

Engineering check on one synthetic home. No assistive technology, WCAG, usability, production, live or whole #233, #149 or #1362 acceptance. The D1 Playwright 1.64.1 and harness-leak records stay adverse history. No push, PR, GitHub, merge, board or nested agents. The old read-only worktree and its records are untouched.
