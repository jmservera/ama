---
title: Issue 215 audit details
description: Phase details for the issue 215 accessibility evidence audit
ms.date: 2026-11-13
---

## Phase 1

From `src/api`: `PYTHONPATH=tests:../core/tests:../agents/tests /tmp/venv-215-1953/bin/python -m unittest test_regulatory_ux_check test_accessibility_baseline test_content_standard -v`. Record Ran N, OK/skips.

## Phase 2

Download `https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js` to `/tmp/ama-215-1953-out/`; run the check with `--out` in the same external directory. Summarise per-state axe violations and incomplete from the JSON.

## Phase 3

Changes record at `.copilot-tracking/changes/2026-11-13/215-regulatory-ux-a11y-audit-1953-changes.md`. Do not tick issue criteria; do not edit GitHub.

## Phase 4

code-review agent on the diff; commit with trailer; clean status.
