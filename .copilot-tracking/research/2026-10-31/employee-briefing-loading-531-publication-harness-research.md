---
title: Issue 531 publication harness correction evidence
description: Executed full-gate failures and bounded non-weakening corrections
ms.date: 2026-10-31
---

## Brief and Disposition

Task 531 / employee-briefing-loading-531-publication-harness is a necessary
publication correction under the user's continuous delivery instruction.
Parent employee-briefing-loading-531-capacity-correction finished its original
Review; do not repeat or alter that Review. Publication is still incomplete.
Research disposition reused; readiness Ready from exact failed gate evidence
and direct source trace. No new broad research or design decision is needed.

## Evidence

* External full-gate-1.log records an actual 1800-second lock timeout.
* External full-gate-2/receipt.json binds failed full execution to 99358b65,
  base a75bbdff. Lock acquired after 195 seconds, jobs admitted 1.
* full-gate-2/0068-static.log: tools/test_rpi_checks.py's fixture subprocesses
  print fabricated skip transcripts through Runner.command. The outer gate
  correctly rejects those lines, although all 37 fixture tests pass.
* full-gate-2/0073-browser.log: nine B023 loop-variable bindings in the existing
  case-journey harness fail the gate's isolated lint. No loading/briefing
  scenario failed; its previous executed results remain retained evidence.

## Recommendation and Boundaries

Capture only synthetic fixture stdout in the test; preserve the actual production
skip parser and every fail-closed assertion. Bind loop-specific callback state
with keyword-only defaults, not shared late-bound variables. Preserve all
scenario assertions and registrations. Apply the required isolated formatter
to this directly repaired harness if its gate requires it. No runtime, workflow,
WORKFLOW_HASHES, Azure, secret, dependency or gate-contract change.
Add one focused fixture-output regression. Full gate must rerun on a new
committed candidate; failed receipt cannot resume across source changes.

## Alternatives

Reject allowing synthetic skips in static, disabling B023, deleting scenarios,
changing hashes, partial/cloud receipts or publishing failed checks. These
would weaken the required contract. Prior Review stays immutable; a distinct
bounded harness correction owns one critique and one original Review.
