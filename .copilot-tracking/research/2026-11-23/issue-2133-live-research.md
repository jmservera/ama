---
title: Issue 2133 research
date: 2026-11-23
---

# Issue 2133 research (Refs #2133)

Disposition: executed. Planning Readiness: Ready.

## Criterion inventory

Issue #2133 has one unticked criterion: "Manual screen-reader and keyboard checks are recorded for each role workflow".

## Evidence read

* `docs/reference/research/ux/wcag-conformance-baseline.md`, "Manual check record": eight role rows, all `Not run`; status line 2026-11-19 (#151, demo) says a screen-reader record needs a named person with NVDA or VoiceOver and the owner decision of 2026-11-18 excludes person-run assistive-technology testing for the demo.
* `src/api/checks/` and `src/api/tests/test_assistant_panel_a11y_159.py`: automated keyboard and DOM checks exist; they are not assistive-technology output.
* No screen reader is installed on the host (baseline section "Map list alternative screen-reader check").

## Classification

The criterion requires a person to operate a screen reader and keyboard per role and record the result. That is person-run assistive-technology testing, excluded for the demo by the owner decision of 2026-11-18. It is owner-gated and unproven. No code criterion exists that needs no approval, so no source change is made.
