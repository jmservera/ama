---
title: Regulatory UX optional browser dependency changes
description: Implementation and validation evidence for the CI repair
ms.date: 2026-10-16
---

Refs #215. Full plan scope: P01-P03.

## Main merge

Merged origin/main in cc31736 before implementing the repair. Kept both
append-only log histories. Chat conflict resolution preserves main's privacy
warning, retention metadata and textarea association alongside the branch's
accessible live-log/list, controls and visible unavailable-chat fallback.
No authorization or legal approval boundary changed.

## Baseline

Created `/tmp/v215c` using python3 venv and installed only editable core,
agents and API distributions with pip. Full API discovery failed:
558 tests, 110 skipped, one import error for test_regulatory_ux_check;
`ModuleNotFoundError: No module named 'playwright'` at the eager check import.
This reproduces the reported failure with no browser dependencies installed.

## P01 / P01-T01

Implemented type-only Page annotations and local browser imports, including
expect in run as required by PC-001. Added one subprocess import-blocking
regression. All four harness tests pass with Playwright confirmed absent.
No pure test removal or skip.

## P02 / P02-T01

Full API discovery passes without Playwright: 561 tests, 110 opt-in skips,
190.482 seconds. Module absence explicitly verified before execution.
Installed API dev extra only after missing Ruff/mypy/Playwright tool failures.
Full API discovery then passes with Playwright 1.64.0: 561 tests, 110 skips,
188.282 seconds. Four harness tests also pass with Playwright installed.
API Ruff/format and isolated regulatory-check lint/format pass. Strict mypy:
no issues in 47 source files. No new typing exemptions.
Merged core regulatory/chat/privacy/rule-card regressions: 56 tests pass.

Both source CI browser commands pass against actual synthetic loopback apps,
including running/responsive server probes. Chromium 156.0.8078.4.
Pinned axe 4.10.3 hash verification passes. Regulatory output:
17 states, 142 measured targets, minimum width/height 24px, zero detected axe
violations, eight contrast-incomplete states; staff comprehension Not run.
Source workflow is unchanged and continues to invoke the real browser harness.
Full JSON is local at `/tmp/v215c-regulatory-ux-results.json`; no application
content was shared with the download host.

## P03 / P03-T01

Updated API/source READMEs, reference index and appended knowledge-base log.
Verified both original log histories are subsequences of the merged log:
every line retained in order. Existing issue criterion audit remains accurate.
Pending one final review and publication; no issue body edits or checkbox ticks.

## Remaining acceptance boundaries

Full WCAG/manual assessment, staff comprehension, paired chat value and
real accountable owners/sources remain unmet. No actual legal, consent,
safety or financial approval is represented by these synthetic checks.
