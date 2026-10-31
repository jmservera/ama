---
title: Issue 531 publication harness correction plan
description: Repair actual required-gate execution blockers without weakening checks
ms.date: 2026-10-31
---

## Metadata and Executive Summary

Task 531 / employee-briefing-loading-531-publication-harness, automatic
publication correction child of employee-briefing-loading-531-capacity-correction.
Fix only the two actual harness failures, preserve original adverse receipts,
then obtain one Review and a fresh full exact-head gate before requested PR.

## User Decisions and Requirements

* Continue until validation runs and PR is published; pip only, no secrets/Azure.
* Main merge and non-force publication required; heavy waits 1800, retry once.
* No weakened gate or false issue closure; Refs #531, live/specialist unmet.

## Goals

Restore reliable required-gate execution without relaxing skip or lint contracts.

## Scope and Non-Goals

tools/test_rpi_checks.py synthetic fixture output and
src/api/checks/case_journey_browser_check.py callback capture only.
No production gate parser, workflows, hashes, UI/runtime/dependency edits.
No unrelated test deletion or skip addition. Formatting of the repaired
browser file is permitted only as required by its existing isolated gate.

## Functional Requirements

Fixture transcripts stay within fixture logs/capture; outer suite has real
unittest output only. Browser callbacks capture each iteration's state.

## Non-Functional Requirements

Type safety, original assertion coverage, isolated Ruff/format, external scratch,
preserved failures, clean committed exact-head full publication checks.

## Acceptance Criteria

* Full tools suite passes; real outer skip parser sees zero synthetic skips.
* Required isolated case-journey lint/format and relevant mypy pass.
* Actual local case-journey/axe check runs under shared lock.
* One original correction Review is committed before fresh full gate.
* Full receipt/current-base verification/exact-head assessment precede PR.

## Test Ownership and Budget

Parent owns source fixes/execution. Removals none; one new regression maximum
in tools/test_rpi_checks.py, no new browser scenarios. Retain every existing
assertion; source captures are semantic fixes, formatter is hygiene.
Generated logs/JSON/screenshots/receipt external only.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Repair and verify harness

* [x] P01-T01: Capture fixture output and bind browser callbacks.
* [x] P01-T02: Run exact tools/isolated lint/types and local browser/axe.
* [x] P01-T03: Reconcile evidence and obtain one original Review.

P01 complete; one original independent Review execution Complete / outcome
Conformant for the bounded harness correction. No defects; inherited issue
follow-ups remain separate. P02 publication remains.

<!-- rpi:phase id=P02 -->
### P02: Gated publication

* [ ] P02-T01: Commit all correction evidence/trailer; fresh full gate.
* [ ] P02-T02: Verify current receipt, independent exact-head assessment, push/PR.

## Critique Disposition

One final-candidate critique execution Complete / Pass, no findings.
Planning readiness Ready; no repeated critique.

## Follow-Up Items

Prior specialist note, live AC7 and manual contrast assessment remain open.

## Handoff

P01 complete after one critique/Review. Research/details/changes/Review use this same
slug/date. This distinct correction does not reopen the completed parent's Review.
Commit reconciled evidence, then run full exact-head gate; final publication
state/receipt remain external, not a later self-invalidating evidence commit.
