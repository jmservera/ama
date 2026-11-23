---
title: Issue 2133 manual screen-reader and keyboard checks, demo classification
description: Per-criterion classification for the remaining WCAG baseline criterion of #2133
ms.date: 2026-11-23
---

Refs #2133. Synthetic demo, desktop only. No source change.

## Criterion table

| Criterion | Status | Evidence and reason |
| --- | --- | --- |
| Manual screen-reader and keyboard checks are recorded for each role workflow | Unproven, owner-gated | The record needs a named person operating NVDA with Firefox or VoiceOver with Safari for each of the eight role workflows. The owner decision of 2026-11-18 excludes person-run assistive-technology testing for the demonstrator. The host has no screen reader (see the baseline section "Map list alternative screen-reader check"). |

## What exists instead

* Automated keyboard and DOM checks, for example `src/api/tests/test_assistant_panel_a11y_159.py` and the role-screen browser checks under `src/api/checks/`. They are engineering evidence, not assistive-technology output, and they do not fill any row of the manual check record.
* The eight rows in [the manual check record](ux/wcag-conformance-baseline.md) stay `Not run`.

## Disposition

The criterion stays unticked on #2133. It needs a named tester before a production release; no conformance is claimed.
