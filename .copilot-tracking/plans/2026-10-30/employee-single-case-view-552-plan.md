---
title: Employee single case view plan
ms.date: 2026-10-30
---

## Task Metadata

* Task ID: 552
* Task slug: employee-single-case-view-552
* Planning status: Ready; single critique dispositions complete
* Details: .copilot-tracking/details/2026-10-30/employee-single-case-view-552-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/employee-single-case-view-552-plan-critique.md

## Executive Summary

The requested UI already shipped through merged PR #554 and is present in the
requested baseline. Preserve that implementation; strengthen its focused
browser check with pinned axe scans and narrow-width attached-tab scrolling.
Fresh independently inspected evidence supports all six local criteria;
required API/browser checks pass and one Review is Complete / Residual work.
Persist locally; the required complete gate remains unexecuted and blocked.
No push, live sign-in, Azure or deployment.

### What You May Not Know

Original Review left independent rendered evidence inspection open. Its outcome
remains immutable. Current work produces fresh evidence rather than claiming
the old review passed. Fluent library adoption and full WCAG/AT acceptance are
not established by local engineering checks.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order for exactly Refs #552.
* Use the supplied topic branch/base; source in src, tests outside packages,
  pip only, native semantics, Fluent foundations, non-colour states, reduced
  motion and plain language.
* Run full API unittest discovery, Ruff check/format and mypy; exercise the
  local UI with Playwright/axe at desktop and narrow widths.
* Lock heavy gates; no cloud, deploy, live sign-in, credential files, secrets
  or pushes. Commit locally with the requested Copilot trailer.

## Goals

Provide current reproducible evidence for delivered compact case UI without
unnecessary runtime changes or unrelated refactoring.

## Scope and Non-Goals

Included: src/api/checks/case_view_ux_browser_check.py, its API README instructions,
dated RPI artifacts, local synthetic verification. Runtime fixes only if an
exact-criterion defect is established before Review.
Excluded: unrelated UX, frameworks, backend authority, new dependencies,
full Fluent adoption, live/user acceptance, issue mutation and remote writes.

## Functional Requirements

Retain all existing check behavior and baseline mode. Require a hash-verified
axe input for normal verification, scan compact journey and open disclosure
states across 1280/390/320px, retain full axe findings/incomplete results.
Verify tabs and panels share a surface, tabs lie outside scrolling ancestors
within that surface, panel scroll changes without moving tabs, at all widths.

## Non-Functional Requirements

No page overflow at 320/390/1280px; existing step ceilings <=132px desktop and
<=116px narrow. Preserve keyboard/touch, 200% text and reduced motion checks.
Reject all observed axe violations in the focused states, retain incomplete
items as manual-review limitations. Keep browser evidence external.

## Acceptance Criteria

1. Six loaded exact presentation icons with visible text labels.
2. Existing compact geometry meets ceilings; compare original historical
   baseline honestly rather than inventing a current before/after redesign.
3. One-line summary, full reasons/owners/actions reachable by keyboard/touch,
   dismissal and focus return, enlarged text.
4. Attached tabs outside inner scrolling region, panel actually scrolls under
   stationary tabs at desktop and both narrow widths.
5. Preserve source Fluent/WCAG/content baselines; local axe and regression
   evidence, without asserting full conformance.
6. Current desktop/narrow JSON and screenshot evidence inspected in Review.

## Sources

Research .copilot-tracking/research/2026-10-30/employee-single-case-view-552-research.md,
C1-C7/W1-W2. PR #554 already merged; original Partial Review is preserved.

## Test Ownership and Locked Budget

Canonical owner: existing API checks/case_view_ux_browser_check.py. Reuse
checks.case_journey_browser_check.scan and canonical AXE_SHA256, enforce all
violations after each scan. No new scanner library, fixture app or generated
source target. Exact test removals: none. Maximum new unit methods: zero;
semantic new browser assertions augment the existing real-server script.
Existing regression coverage retains safe rendering, exact icon bytes,
package data, workspace and accessibility/content contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Strengthen focused verification

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add scoped axe and responsive attached-tab checks

Depends on final critique dispositions. Keep baseline capture optional-axe;
require pinned axe for a normal run. Serialize results on failure. Update README.
Implemented in the existing dedicated browser check and README; no runtime
changes, dependencies, new unit methods or test removals.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate, independently review and persist

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute API and browser checks

Depends on P01. Use flock -w 600 for API/browser heavy checks, existing /tmp/mv
tools, exact user PYTHONPATH and full discovery. Run Ruff check, format check,
mypy. Review raw JSON and desktop/narrow PNGs; retain limitations explicitly.
Concrete external output: session files/case-552-browser under
/home/azureuser/.copilot/session-state/efa3c0ae-28bb-4df9-acfd-bd663c72eec3/.
This is not under /tmp and is explicitly provided to the reviewer.
Complete: 1379 tests (320 skips), Ruff check/format, mypy; fresh Playwright
run passed after one shared-lock timeout, nine axe states zero violations,
three preserved incomplete contrast records for clipped Resident targets.
Parent inspected raw JSON and desktop/narrow/popover PNGs.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: One Review, local commit and complete local gate attempt

Depends on P02-T01. Independent reviewer may read external generated evidence
as well as tracked files, writes only its new Review. Route findings to later
work, no repeated Review. Configure privacy-safe GitHub identity; local commit
with trailer. Fetch main, run full gate externally (runner self-locks; use its
600-second timeout, never nested flock). No Azure operations; if full gate
requires prohibited Azure CLI execution, record blocked instead of running
that prohibited command. No push. Final receipt remains external; do not make
another commit after successful final gate.
Current disposition: independent Review Complete / Residual work, no introduced
defect. Local persistence is the enclosing commit. This task/phase remains
unchecked specifically because complete-gate execution is unmet, not because
Review or the scoped implementation needs repeating. RV-001 preserves the
publication blocker; RV-002/RV-003 are distinct later work.

## Dependencies

Existing /tmp/mv source dependencies, Playwright/Chromium, pinned axe. Complete
gate requires additional local tools and its offline az/bicep invocation may
conflict with the user's no-Azure boundary; preserve that limitation explicitly.

## Critique Disposition

Single critique executed Complete / Revise; original outcome preserved.

| Finding | Disposition | Evidence and consequence |
| --- | --- | --- |
| PC-001 | Parent restriction premise rejected; reviewer evidence concern resolved directly | The parent has no /tmp prohibition; user explicitly requires /tmp/ama-rpi-heavy.lock, existing /tmp/mv tools were successfully inspected. Do not import a worker-only boundary or weaken the required shared lock. Keep these paths for parent execution. Generate fresh JSON/PNGs in the concrete external session path above, readable without /tmp. Full gate remains blocked independently by its mandatory az invocation, established in tools/rpi-checks.py preflight/infrastructure. No second critique. |

## Follow-Up Items

* RV-001: coordinator resolves no-Azure/full-gate conflict before publication.
* RV-002: accessibility owner assesses clipped Resident heading/Notes contrast
  with visible targets, alongside existing human/AT/cross-browser acceptance.
* RV-003: API/design-system owner assesses inherited form metadata/motion debt
  in later maintenance; no source fix in this one-pass task.
* Full Fluent adoption belongs to #150, not this bounded issue.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-30/employee-single-case-view-552-changes.md.
One Review complete; no further source changes or repeated Review. Scoped work
is ready for local persistence only; P02/P02-T02 full-gate portion is blocked.
Coordinator owns publication decisions and later separately selected follow-ups.
