<!-- markdownlint-disable-file -->
---
title: Case view review fixes 552 plan
description: Bounded selector and API wheel packaging corrections for PR 554
ms.date: 2026-10-29
---

## Task Metadata

* Task ID: 552-pr554-review-fixes.
* Task slug: case-view-review-fixes-552.
* Plan date: 2026-10-29.
* Status: bounded full loop complete and implementation committed locally;
  original critique Revise and Review Conformant with justified divergence preserved.
* Details: .copilot-tracking/details/2026-10-29/case-view-review-fixes-552-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-29/case-view-review-fixes-552-plan-critique.md.

## Executive Summary

Count only the six top-level summary terms and explicitly ship the six journey
icons in the API wheel. Both pre-fix failures are reproduced. Add one lightweight
manifest regression beside the existing icon provenance test and verify real
wheel contents, not just source files.

### What You May Not Know

The source browser can load icons that are absent from the container's installed
wheel. The existing icon test verifies presentation provenance, not packaging.
Local results do not replace publication, hosted or human acceptance gates.
The prior task's RV-001 and Partial Review remain historical and unchanged.

No unresolved implementation decision or planning blocker. PC-001 identifies a
review-worker evidence-access limitation, not a parent execution failure:
parent already successfully built a wheel and ran a browser with /tmp output.
Keep external generated outputs and record reviewable result extracts in the
tracked changes artifact instead of relocating generated files into the repo.

## User Decisions and Requirements

* Fix `.case-summary dt` to `.case-summary > dl > div > dt`.
* Add `web/journey-icons/*.png` to API package data and verify built/installed assets.
* Pull the rubric commit first; retain PR #554 / branch feat/case-view-ux-552.
* Execute all four RPI phases with dated artifacts and commit locally with the
  specified Copilot trailer. Do not push, use az or hand-edit rubric scores.
* Use /tmp/mv and supplied PYTHONPATH; run focused API tests, ruff check,
  ruff format --check, node --check and relevant local Playwright checks.

## Goals

Restore the truthful summary regression and container asset distribution without
changing UI behavior or authority boundaries.

## Scope and Non-Goals

Targets: API browser assertion, package manifest, existing journey tests and API
README. No production JavaScript/CSS, Dockerfile, dependency, generated PNG,
rubric, cloud, branch-lineage or unrelated changes.

## Functional Requirements

* Summary assertion counts exactly six outer terms even with blocker details.
* All six expected PNG paths and exact source bytes exist inside the built wheel.
* Existing source icon provenance and journey behavior remain unchanged.

## Non-Functional Requirements

* No new runtime/dev dependency or framework.
* Synthetic-only owned loopback browser execution and external generated evidence.
* Preserve original critique and one Review outcome; no repeat review loop.

## Acceptance Criteria

* AC1: actual ZF-1 journey check passes the corrected six-term assertion.
* AC2: fresh wheel contains assessment, contractor, funding, quality, resident
  and survey PNGs at `zava_forward/api/web/journey-icons/`, byte-exact to source.
* AC3: focused tests, ruff lint/format and both relevant JS syntax checks pass.
* AC4: complete available journey and compact-view browser checks are attempted
  with honest failures/blockers and desktop/narrow evidence recorded.
* AC5: independent critique, implementation reconciliation and one independent
  Review recorded; local Conventional Commit has privacy-safe identity and trailer.

## Sources

Research: .copilot-tracking/research/2026-10-29/case-view-review-fixes-552-research.md,
C1-C8, disposition executed, Planning Readiness Ready. No further research needed.

## Test Ownership and Change Budget

* Canonical targets: browser assertion and API setuptools package-data.
* Tests: existing test_case_journey owns icon semantics/provenance; existing
  case_journey_browser_check owns actual six-term DOM coverage.
* Exact removals: none. Maximum additions: one manifest regression in
  test_case_journey.py. Keep existing semantic tests; no new test file.
* Generated targets: none tracked. Wheel/browser outputs remain external.
* Evidence: real pre-fix failure, full post-fix relevant checks, and direct wheel
  ZIP path/byte inspection. Manifest test is preventive, not proof of wheel contents.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and validate both findings

Dependencies: completed research and independently critiqued final plan.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Apply selector, packaging and documentation corrections

Change the exact selector and nested asset glob. Add the single allowed
manifest test using stdlib tomllib/Path.match and update the existing API guide.
Path.match preserves pathname-segment matching; unlike fnmatch, `web/*` does
not incorrectly match a nested icon. The new regression failed for all six
icons before the manifest fix.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate actual output and local browser behavior

Run five focused API modules, lint/format, JS syntax, fresh wheel ZIP inspection,
case_journey_browser_check with pinned axe and case_view_ux_browser_check.
Record actual command outcomes and retain failures.
Completed: 55 tests, lint, repository-exclusion-aware format, both JS checks,
six wheel members/bytes, full journey and compact browsers. Direct explicit
formatting of the already-excluded legacy browser file exposes pre-existing
format debt (baseline also exit 1), retained rather than reformatted.

<!-- rpi:phase id=P02 -->
### [x] P02: Review and persist locally

Depends on P01 and reconciled original implementation evidence.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute one independent Review and commit locally

Give the reviewer read access to changes/evidence and write access only to its
review artifact. Route findings to later work, never loop Review. Resolve GitHub
identity and configure repository-local privacy-safe author/committer email.
Commit implementation and dated original evidence with Conventional Commit
and requested trailer; verify commit and clean worktree. No push.
Completed: one independent Review Complete / Conformant with justified
divergence, no new findings; implementation/original evidence commit 5a3edfe6.
Both identity addresses and Copilot trailer verified; worktree clean afterward.

## Dependencies

Working /tmp/mv, local Chromium/Playwright, hash-verified axe and pip wheel are
available. Required checks use synthetic data, no SQL/cloud prerequisites.
Full publication gate is not run or waived: publication is explicitly prohibited.

## Critique Disposition

One independent critique executed, original verdict Revise preserved at
.copilot-tracking/reviews/plans/2026-10-29/case-view-review-fixes-552-plan-critique.md.

| Finding | Disposition | Evidence and consequence |
| --- | --- | --- |
| PC-001 | Parent-execution premise rejected; reviewer-access concern addressed directly | Parent baseline wheel and browser commands already succeeded using /tmp outputs (research C2-C3). Do not import a worker-specific restriction into parent authority or move generated output contrary to external-evidence plan. Keep external paths, include exact wheel/member/byte checks and compact browser result extracts in tracked changes, and give reviewer those records and raw outputs if accessible. Any unavailable independent raw inspection must remain explicit, not relabelled accepted. No second critique. |

## Follow-Up Items

* Inherited RV-001: prior issue-wide rendered-evidence acceptance remains outside
  this two-finding task; preserve original outcome and route separately.

## Handoff

Implementation record:
.copilot-tracking/changes/2026-10-29/case-view-review-fixes-552-changes.md.
Complete: P01/P02 and all tasks. Implementation and original evidence persisted
locally as 5a3edfe6; final closeout records completion separately without
changing assessed source or repeating Review. No push/publication authorized.
