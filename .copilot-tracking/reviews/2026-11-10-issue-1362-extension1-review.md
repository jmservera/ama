---
title: "Review: issue 1362 extension E1 visible associated version"
description: One author Review of the checker-only visibility fix
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

Executed once by the author after implementation. Assessed boundary: the two-file checker and unit-test change. This is not the independent exact-head review, which the same independent reviewer must still perform before publication.

## Outcome

Conformant on local evidence, no open finding.

* The reviewer's Medium is closed on this candidate: real-DOM controls (unit and served fixture, 1280 and 320) reject `visibility:hidden` and `opacity:0` on the label, the value and an ancestor; the unchanged positive passes at both widths; all D1 negatives still reject; the full Atlas browser check passes (370 PASS).
* Scope: no app, CSS, fixture, role or manifest change; `contentVisibilityAuto` not enabled; no fallback, skip-as-pass, broad exception handling or timeout change.
* Residual and disclosed: the real-DOM unit class is opt-in (3 skipped by default); only the opt-in and browser runs exercise it. The checker uses `checkVisibility` options, so `display:none`, `content-visibility` hidden and off-screen clipping remain governed by the previous rules. Declared deviations are in the changes record. The earlier D1 run-count deviation and adverse Playwright 1.64.1 and harness-leak records are preserved.
* No conformance, human, hosted CI, AT, WCAG, usability or production approval is claimed.

## Routing

No later work from this Review. Independent exact-head review by the same reviewer, then Root publication decisions.
