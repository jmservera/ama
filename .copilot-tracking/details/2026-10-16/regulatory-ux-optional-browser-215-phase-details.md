---
title: Regulatory UX optional browser dependency phase details
description: Task-specific implementation and completion expectations
ms.date: 2026-10-16
---

## P01 / P01-T01

Research C1-C6 establishes that all discovered regulatory harness tests are
pure but import the browser library eagerly. Import Page under TYPE_CHECKING;
import expect within each helper using it; import expect and sync_playwright inside run,
after axe verification and before fixture startup. Keep fixture imports intact.
Use a fresh subprocess with a meta-path blocker to reject all Playwright imports,
then import the check. A failure must include subprocess stderr.

## P02 / P02-T01

First reproduce the baseline in the exact requested runtime-only venv.
Retain proof of missing Playwright and test counts/skips. Re-run after changes,
then install the dev extra only after browser/tool dependency absence is
demonstrated. Run full API discovery again plus Ruff/format/mypy. Run relevant
core integration tests after main's merged changes. Install Chromium if absent.
Execute both existing browser harnesses against synthetic loopback data only,
using absolute fixture PYTHONPATH. Use the pinned axe URL/hash from source CI.
No need for Azure: this repairs test import boundaries, not a delivered app.

## P03 / P03-T01

Explain runtime-only discovery and separate browser execution in API/source
READMEs. Preserve existing log entries and append this repair's evidence.
Record exact verification, unmet issue criteria and one post-implementation
review. Reuse open PR #354, update its body without introducing closure syntax
or changing issue checkboxes, commit with authenticated privacy-safe identity
and required trailer, and push normally. Check remote head matches local.
