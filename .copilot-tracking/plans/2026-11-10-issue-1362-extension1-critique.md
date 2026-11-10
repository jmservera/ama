---
title: "Critique: issue 1362 extension E1 visible associated version"
description: One-pass final-candidate critique of the E1 plan
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

Executed once by the author against the final plan and details. Verdict: APPROVE with direct applications.

## Findings

* Ancestor visibility: `opacityProperty` and `visibilityProperty` account for ancestors, so a hidden section is also rejected. Applied: ancestor case added to the real-DOM test.
* `contentVisibilityAuto`: enabling it would reintroduce the 320px blank-value failure fixed in the inherited correction. Applied: stays off, stated in the details.
* Skip risk: an opt-in test can be skipped silently. Applied: the test runs with the flag set for this task and the handoff reports the default run as skipped, with counts. No skip is used to claim a pass.
* Positive and desktop/mobile: only a served-fixture run proves the unchanged positive at both widths. Applied: the full Atlas browser run and the D3 pair are in Phase 4.
* A test double returning `visible=False` was rejected as sufficient (reviewer note); retained only as the D1 unit control.
* Scenario manifest: no dependency found, so no manifest edit. Conflicts with confirmed decisions: none. No user decision needed.
