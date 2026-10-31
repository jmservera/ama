<!-- markdownlint-disable-file -->
---
title: Required gate harness correction phase details
description: Exact repair and validation targets for correction2
ms.date: 2026-10-31
---

## Metadata

Task `571-correction2`, same slug/date as plan. Parent correction1. Source start
`10401c5a`, main `a75bbdff`, same fix/resident-survey-check-571 branch.

<!-- rpi:phase id=P01 -->
## P01: Repair and validate

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fix only observed harness roots

In tools/test_rpi_checks.py existing exact chat-panel skip test, capture stdout
with existing unittest patch helper and io.StringIO around both Runner.command
fixture invocations, assert captured text retained. Real output/parser/skip
policy remains unchanged. In case_journey_browser_check.py bind pending/loads/
reads/held/snapshot/change per iteration in callbacks with keyword-only default
arguments after route; never consume Playwright's positional Request slot.
No route/scenario/assertion deletion. Run isolated formatter for directly
affected journey, preserve all semantic checks. Add short src/README gate note
explaining synthetic fixture isolation/iteration binding, no acceptance change.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate and reconcile

After P01-T01, run full existing tools/test_rpi_checks.py suite and exact isolated
Ruff E,F,I,B,UP/format for affected files (same runner argv), then complete actual
local checks.case_journey_browser_check with pinned axe, mandatory isolated
synthetic preview environment and import safety used by runner.
Use task-owned environment, no application/cloud inherited settings. Browser
flock -w1800 shared lock, one admission retry. Also fresh API discovery, API Ruff
check/format and complete resident Chromium/axe check. Light tests unlocked.
Keep logs/counts/hashes, no skipped integration passes; source and acceptance
remain unchanged. Reconcile changes/plan/details/state before Review.
Evaluate full verbose combined tooling transcript with unchanged
check_skips(group="static"), record tests/executed/skips and no leaked synthetic
chat-panel skip. One capture assertion requires both transcript occurrences.

<!-- rpi:phase id=P02 -->
## P02: Review and publish

<!-- rpi:task id=P02-T01 -->
### P02-T01: One child independent Review

After P01-T02, new child Review only; preserve both earlier Reviews/verdicts.
Assess exact harness diff and evidence, no source fixes or repeat Review.
Record material blockers separately from residual direct-acceptance boundaries.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit and full gate

After Review with no material blocker, commit original child evidence and fixes
with privacy-safe identity/trailer. Fresh clean detached candidate, current
main-descended full --all runner --lock-timeout1800, new external directory.
Failed correction1 receipt immutable; later commit requires fresh gate, no resume
of stale source. Verify receipt against freshly fetched main; independent
assessment must explicitly approve exact HEAD/base/receipt before push/PR.
Missing/adverse/stale checks/assessment or material findings block publication.
Pip only, no protection/skip/hash weakening, no cloud fallback, no force/merge.
Final authoritative receipt/status external/PR, not post-gate tracked commit.
Closes #571 only if assessed evidence still proves all three actual criteria;
otherwise Refs and named unmet criteria. Hosted/owner merge separate.

## Current Completion and Review Handoff

P01-T01/02 complete. Full tools discovery passed 37 tests (12.677s), unchanged
outer static parser tests=37/executed=37/skips=[]; both synthetic transcript
occurrences captured. Exact gate-cwd isolated harness Ruff/format and strict
tooling mypy passed. Fresh API 1430 tests (546.321s), 320 explicit opt-in skips,
API Ruff pass/65 formatted. Complete employee browser first admission passed:
87 axe scans, zero violations, 50 incomplete-rule occurrences, no page errors,
actual chrome.tabs.setZoom=2. Complete resident browser first admission passed:
32 scans, zero violations, 42 incomplete-rule occurrences in 31 states, no
errors/external requests; native resident zoom and human/AT Not run.
Source AST identical except keyword-only callback defaults. All original resident
source and acceptance limits unchanged; no policy/workflow/hash edit.
P02-T01 Review and P02-T02 committed full gate/publication pending.

P02-T01 now complete: one independent correction2 Review, Complete / Residual
work, bounded correction approved with no material defect. Six external execution
hashes independently match copied logs/reports. Low direct-acceptance limits
retained. P02-T02 pending final evidence commit and new full exact-head gate;
no successful receipt or publication yet. No repeat Review/source correction.
