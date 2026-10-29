---
title: Loading and briefing correction research
description: Focused evidence for four review corrections on PR 538
ms.date: 2026-10-29
---

## Research Brief

Correct the four supplied review findings on branch
`feat/loading-briefing-hax-531`, PR #538, Refs #531. Audience: implementer
and independent reviewers. Output mode: convergence preparing planning.
Scope: draft-review focus, search feedback, async busy restoration and
sentence citation separation, each with regression coverage.
Non-goals: redesign, Azure, pushing, merging or closing the issue.

## Research Parameters

Focused posture selected from named code targets and supplied failure cases.
Use current worktree source with the issue-526-journey venv. Full suites
require nonblocking `/tmp/ama-rpi-heavy.lock`; contention limits validation
to targeted tests. No interaction is needed for the explicit bounded brief.
Resolved evidence root: `.copilot-tracking/research/2026-10-29/`.

## Extension Registry and Provenance

* Repository instructions: preserve existing topic branch, privacy-safe
  identity, source layout and original RPI evidence.
* RPI skills: selected for phase evidence, critique and independent Review.
* Web interface guidelines: selected for changed web behavior.
* Design overhaul skills: skipped; this is a behavioral correction, not redesign.
* Research specialists: skipped; the four small connected traces fit direct reads.

## Research Cycle Log

### Cycle 1: Wider

The existing parent state is completed with historical Review Not accepted.
This correction is a new bounded child, not a rewrite of that outcome.
Existing `test_loading_feedback`, loading/briefing browser and API task tests
cover the shared helper and briefing. Core owns the parser but lacks a direct
parser test. Reflection: reuse the existing harness and add one core test file.

### Cycle 1: Deeper

Verified all four reported paths against current source (C1-C4).
`actForm` sets busy synchronously and clears it in `finally` (C5).
The list sequence guard prevents an older response replacing a later response
(C2). Reflection: use non-control feedback for editable search, not a new
disable option or another sequence mechanism.

### Cycle 1: Contrarian

Stale/unverified drafts deliberately disable accept/edit but retain rejection;
removing those safeguards would be wrong (C1). The helper must retain
duplicate suppression and action-owned permanent refusal (C3).
Citation relocation must retain newlines and multiple adjacent references,
not merely pass the two-sentence example (C4). Reflection: explicit opener
focus, null-control regional feedback, pre-handler busy capture and one
separator after relocated punctuation are the smallest complete changes.
Another cycle is not needed: the bounded paths and counter-cases are covered.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/web/app.js:428 | Cancel always focuses chooseEdit, even for rejection of unavailable drafts |
| C2 | src/api/src/zava_forward/api/web/app.js:677,705 | Sequence-guarded list reads are passed the editable search as a disabling control |
| C3 | src/api/src/zava_forward/api/web/async-action.js:32-49 | Busy attribute is read after invoking task |
| C4 | src/core/src/zava_forward/core/ai_tasks.py:135-158 | Citation relocation consumes horizontal separator before the next sentence |
| C5 | src/api/src/zava_forward/api/web/panels.js:33-50 | actForm synchronously sets busy, clears it in finally |
| C6 | src/api/tests/test_loading_feedback.py:1; src/api/checks/loading_briefing_browser_check.py:66 | Existing controlled helper clock and real Chromium/axe regression owners |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-29 | Native semantics, focus and polite async feedback guide these changes; no conformance inference |

## Findings Mapped to Questions and Evidence

All four questions are answered by C1-C5. Existing coverage C6 can assert real
keyboard cancellation and overlapping search, while a direct core test checks
exact statement/citation association independently of stores.

The requested `/home/azureuser/source/ama-wt/issue-526-journey/.venv`
does not exist. Current worktree `.venv` is only a harness scratch location,
not an interpreter. Existing `/tmp/ama-531-venv/bin/python` is Python 3.12.3;
verify its dependencies and use source-first PYTHONPATH without modifying
another worktree or installing into a shared environment.

## Alternatives and Decision State

Select the four surgical corrections described above. Reject enabling stale
edit, disabling editable search, global helper API changes and parser rewrites:
they weaken safeguards or add unnecessary scope. No manifest recipe changes
are needed: extend the loading check, not `workbench_browser_check.py`.
No new legal/regulatory or company claims are made.

## Planning Readiness

Ready. Research disposition: executed, complete. Evidence paths, constraints,
alternatives and residual environment uncertainty recorded. Self-check:
three waves completed inline, all four findings grounded, no source changes.
Parent continues to Plan under the explicit full-loop request.
