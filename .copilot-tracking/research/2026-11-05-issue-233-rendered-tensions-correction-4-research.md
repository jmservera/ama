---
title: "Research: issue 233 tensions correction 4"
description: Duplicate region name Tab-reach checker defect
author: Copilot
ms.date: 2026-11-05
ms.topic: reference
---

Disposition: executed (light, read of the helper at head 18f38e8d). Independent review found a Medium checker logic defect: `check_regions_and_keys` tracks Tab reach by `aria-label` strings and compares with `set(labels)`. Two distinct regions with the same name, where only one is focused, are accepted as "every table region" after one Tab. Duplicate accessible names are legitimate and the application is not at fault; this is a checker identity defect, not a production accessibility failure. Fix direction: track the scoped region DOM index of the focused element instead of labels.

Boundaries: checker and its tests only; the 18f38e8d receipt and 194-PASS run are genuine but historical for any new head. Correction 3 chronology deviation (artifacts written after the fix) stands; this correction writes Research and Plan before any code edit. No whole-issue, C4, C5, WCAG, AT or human acceptance is claimed.
