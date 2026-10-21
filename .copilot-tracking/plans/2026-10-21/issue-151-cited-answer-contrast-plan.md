<!-- markdownlint-disable-file -->
# RPI Plan: issue-151-cited-answer-contrast

## Task Metadata

* Task ID and slug: issue-151-cited-answer-contrast
* Date: 2026-10-21; branch `fix/regulatory-contrast-151`; base 993a7b88c03f5240f1e7a4c7c7afa7c064281622
* Parent: #151 (stays open; this is a bounded continuation, refs only)
* Research: .copilot-tracking/research/2026-10-21/issue-151-cited-answer-contrast-research.md (disposition executed, Ready)
* Details: .copilot-tracking/details/2026-10-21/issue-151-cited-answer-contrast-phase-details.md
* Critique: .copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-critique.md
* Changes record: .copilot-tracking/changes/2026-10-21/issue-151-cited-answer-contrast-changes.md

## Executive Summary

The hosted cited-answer axe failure is a timing defect: when a button leaves the disabled state, its background fades from #eceff1 to brand over 150 ms while its white text changes instantly, so axe can sample a mid-fade colour (#45838e is the 26 percent blend). The plan removes the background fade from buttons, adds a unit regression and a browser-check state that scans the cited-answer button mid-fade, and reuses four exact certifi requirement files from a named commit. It does not alter axe, its rules or coverage.

### User Decisions and Requirements Highlights

* Determine root cause, no assumed colour, no retry to green; no masking of transitional states.
* Preserve Fluent 2 tokens, native semantics, keyboard, focus, reduced motion and human approval boundaries.
* No whole-app or conformance claim; wholly partial work, Refs #151 only.

### What You May Not Know

* The failure reproduces only when a transition is in flight; the baseline run passes locally, so the regression freezes the transition to be deterministic.
* The text colour is not transitioned, which is what makes every fade pass through low contrast.

### Unresolved Decisions or Blockers

None. `.alt` hover pairing was dropped after critique PC-004.

## User Decisions and Requirements

* Reproduce the failing rendering state and fix the underlying contrast/timing defect (caller prompt).
* Do not disable axe, rules or coverage, and do not mask real transitional states (caller prompt).
* Preserve Fluent 2, native semantics, keyboard/focus/reduced-motion and human approval boundaries (caller prompt).
* Run the existing targeted regulatory browser check plus a focused regression that fails without the fix (caller prompt).
* Reuse exactly four requirements files from commit a3257c71f4963d98a88c501d040b3d07eada4392 (certifi 2026.10.19, GHSA-6q48-6c7w-9gw2); no other pin, ignore or security-control change, no copied tracking (caller prompt).
* src only; no `mvp/` feature code; no private datasets; no push, PR, merge or amend (caller prompt).

## Goals

* Eliminate the intermediate low-contrast button state, with a regression that fails on the old CSS.

## Scope and Non-Goals

### In Scope

* style.css button transition rule; regulatory_ux_check.py and its unit test; api README check description; four requirements files.

### Non-Goals

* Token changes, other screens, conformance or screen-reader claims. The complete local RPI gate (`tools/rpi-checks.py --all`) and its external receipt are deferred to the coordinator before publication; they are not run here and this task does not claim them. The mid-fade scan covers the cited-answer submit button only; ask, refresh and doubt buttons share the mechanism through the CSS fix but are not separately scanned.

## Functional Requirements

* FR-1: `button` and `.btn` must not animate `background-color` (no intermediate colour with instant text change).
* FR-2: The browser check scans the cited-answer submit button with its transitions frozen mid-fade and fails on any axe violation.

## Non-Functional Requirements

* NFR-1: Axe tags, rules, selectors and scan coverage are unchanged; added states only.
* NFR-2: `--motion` token and reduced-motion override unchanged; border-color transition kept.
* NFR-3: Python style matches repo ruff/mypy settings.

## Acceptance Criteria

* AC-1: With the fix reverted, the new unit test and the new browser states at 35 and 50 percent fail (`color-contrast` on the cited-answer submit button; computed background not equal to brand), and the helper records that a paused `background-color` animation existed. With the fix, the same states pass and no `background-color` animation exists.
* AC-2: With the fix, the unit test, the full `regulatory_ux_check.py --axe` run (axe 4.10.3, SHA-256 matched by the check) and the CI-mirroring commands (isolated ruff select E,F,I,B,UP line-length 100, format check, mypy, unit discovery) pass.
* AC-3: The four requirements files equal the named commit's versions; `git diff --stat` shows no other dependency file.
* AC-4: Review records exact commands, results, and unperformed checks.

## Implementation Context Record

* Focused environment: /tmp/ama-221-pr419-venv interpreter with PYTHONPATH pointing at this worktree's src (verified module path), axe at /tmp/ama-220-axe.min.js (SHA-256 verified by the check), PYTHONDONTWRITEBYTECODE=1.
* Author email: 8036360+jmservera@users.noreply.github.com (repo-local, verified).

## Sources

* Research artifact C1 to C8, W1; src/api/README.md local engineering checks; docs/reference/research/ux/design-system.md motion row.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Regression first (fails on old CSS)

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add unit regression for the button transition list

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add mid-fade browser scan state to the check and confirm it fails on current CSS

<!-- rpi:phase id=P02 -->
### [x] P02: Fix

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Remove background-color from the button transition

<!-- rpi:phase id=P03 -->
### [x] P03: Dependency reuse, docs and validation

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Restore the four requirements files from the named commit

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Update README check description; run focused validation and web-design-guidelines review

## Dependencies

* P02 after P01 (red before green). P03-T02 after P02.

## Critique Disposition

Critique: .copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-critique.md, verdict Revise, run once.

| Finding | Disposition |
| --- | --- |
| PC-001 vacuous mid-fade state | Accepted, applied: AC-1 names fractions 35 and 50 percent; helper asserts computed background equals brand after the freeze and records whether a paused background-color animation existed; red run recorded before the fix |
| PC-002 bypassable regex | Accepted, applied: P01-T01 specifies forbidden properties (`background-color`, `background`, `all`, in `transition` or `transition-property`), path from the package location and a non-empty match assertion |
| PC-003 side effects, sibling coverage | Accepted, applied: helper restores focus and disabled state and cancels animations; scope states submit button only |
| PC-004 `.alt` hover claim | Accepted: cascade (style.css:33 and :34 equal specificity, later wins) means `.alt` keeps the surface background; follow-up dropped; research note corrected; computed hover value checked in implementation |
| PC-005 validation not CI-mirroring | Accepted, applied: AC-2 and the changes record list the CI commands and axe SHA; environment is a recorded unrecorded local prerequisite |
| PC-006 gate and commit sequencing | Accepted, applied: gate deferred to coordinator; red output captured before the fix; commits only after green |

## Follow-Up Items

None. (The earlier `.alt` hover item was dropped under PC-004.)

## Handoff

Parent continues automatically to implementation after the single critique is dispositioned.
