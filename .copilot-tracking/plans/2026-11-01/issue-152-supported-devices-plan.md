---
title: Issue 152 supported devices plan
description: Single-phase plan for the owner-decision proposal slice
ms.date: 2026-11-01
---

## Phases

* [x] Phase 1: write the proposal document and index/log entries.
* [x] Phase 2: add `supported_devices` (status `proposed`, owner decision pending) to the manifest and resolve the `unknowns` wording.
* [x] Phase 3: add tests in `src/api/tests/test_workbench.py`; run unittest, ruff, ruff format, mypy.

## Critique (single pass, 2026-11-01)

Verdict: proceed. Risks addressed directly: the proposal must not claim a decision
or conformance; widths in the manifest must stay a superset of the existing
`widths` list so the browser check is unchanged; `Closes` must not be used.

## Success

Tests pass, no behaviour change in the web app, issue stays open with AC 1 and
AC 5 named as unmet.
