---
title: Map fullscreen issue 532 changes and validation
description: Original implementation evidence, amendments and delivery boundary
ms.date: 2026-10-28
---

## Scope and Status

Full approved plan for task 532, `map-fullscreen-532`. All RPI phases executed;
original Review Complete / Not accepted. RV-001 remains an open implementation
defect; no acceptance or publication is claimed.
Plan and phase details:
`.copilot-tracking/plans/2026-10-28/map-fullscreen-532-plan.md` and
`.copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md`.
Original critique Complete / Revise is preserved with all dispositions.

## P01: Map interaction and lifecycle

P01-T01/T02 implemented in `app.js` and `style.css`: native expanded dialog,
same-map relocation, sidebar card and embedded overlay, named close icon,
summary focus entry, marker-ID focus recovery, route/session disposal and
non-animated map movement. Existing map fields only; coordinator omissions
remain. P02-T01/T02 add six unit contracts, a focused real-server browser check,
update legacy marker navigation expectations and document controls.

## P02: Validation and Documentation

Initial prerequisite probe: Python 3.12.3, Node 24.21.0; system Python import
failed with `ModuleNotFoundError: playwright` (exit 1). Created isolated
`/tmp/ama-532-venv` and installed editable src/core, src/agents, src/api[dev]
(exit 0), without accessing secrets, `.env`, private data or Azure.
First locked run acquired nonblocking shared flock immediately. The 39 focused
unit tests passed (2.334s); targeted mypy passed for both new Python files.
Expected pre-existing unit fixture logs report unavailable rule evaluation.
Node syntax and new-file Ruff (strict E/F/I/B/UP, 100 columns) passed after
formatting/import corrections.

Browser attempt 1: embedded card behavior, zero-violation axe, map click,
top-right close and expanded geometry passed. The check then timed out asking
for `:focus` immediately after backward Tab from the dialog's first control.
Chromium permits browser-chrome traversal at this boundary, so no page element
matches `:focus`. This is a test-observation error, not evidence that background
application controls become focusable. The corrected assertion permits that
native browser-chrome step and separately attempts to focus a background nav
link to establish actual modal isolation. Original external results retained
at `/tmp/ama-532-map-check-1`.

Browser attempt 2 passed keyboard containment, inert background, Escape ordering,
expanded axe and recreated-marker/action focus. It then failed a proxy assertion
that Leaflet's `leaflet-zoom-animated` utility class should not exist. Leaflet
retains that class independently of whether a zoom transition executes. Replaced
the proxy with observing the actual `leaflet-zoom-anim` transition state during a
real zoom-button action, plus computed reduced-motion token. Results retained at
`/tmp/ama-532-map-check-2`. No application defect was established by this failure.

Browser attempt 3 passed all focused checks and seven axe states with zero
violations, plus the complete existing design-system/workbench browser script.
Chromium 156.0.8078.4, no uncaught JavaScript errors. Axe retained 13 incomplete
rule evaluations across the seven states (not violations or human acceptance).
External reports/screenshots: `/tmp/ama-532-map-check-3`. Inspected the actual
embedded desktop, expanded desktop and 320px screenshots.

Post-validation inspection found two tightly coupled gaps before Review:
Leaflet's built-in keyboard panning could animate independently of disabled zoom,
and preventScroll on summary entry could leave its focused heading above a
scrolled sidebar. P01/P02 amended within approved intent: native nonanimated
arrow/+/- keyboard map controls, disabled drag inertia/focus autopan, ordinary
summary focus scrolling, and behavioral endpoint/scroll-visibility assertions.
Expanded direct home navigation is now explicitly exercised too. Attempt 4
passed the amended source and both browser scripts; attempt 5 also covered
embedded 320/390px cards and disabled focus autopan for clusters. The 39 focused
tests and targeted mypy passed again. These runs are historical after the
following tightly coupled accessibility correction.

Detailed inspection of attempt 5's retained axe incompletes found Leaflet's
closed tooltip left a marker's `aria-describedby` pointing at a removed tooltip.
The marker already has a title/accessible name containing the same name/status,
and the new summary provides its detail, so remove the redundant Leaflet tooltip
instead of accepting a dangling ARIA reference or modifying the vendor. A unit
guard prevents its reintroduction. Contrast incompletes still require human
assessment. Fresh final validation is required for this correction.

Attempt 6 has been launched with the same nonblocking flock retry, bounded to
40 minutes. Initial admission waited behind another shared heavy run;
the lock was acquired within the budget and all commands exited 0.
No heavy check executed without the lock. Source fingerprints for the final
batch:

| File | SHA-256 |
| --- | --- |
| app.js | de65ae5995085598d02ff30041ee0633400c51dc713fc1f4fa9c05af74340f55 |
| style.css | 2ab63b6619164f8de01fdbeacb2f3132adc0952096caee7163fae2d59c4f0c75 |
| map_fullscreen_browser_check.py | af4a35728f5d1ccc70ab52a99e0c15916f24650402e8c817fe915065f062b82c |
| test_map_fullscreen.py | a8600496502f08cc46ddee3001b6960d6a495b1a4268758e05a5f4f8b90bb767 |

### Final Validation (Attempt 6)

From `src/api`, with `/tmp/ama-532-venv/bin` tools:

| Command | Result |
| --- | --- |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_map_fullscreen test_design_system test_accessibility_baseline test_content_standard test_ui_support test_workspace_scripts -q` | 39 passed, 2.309s, no skips; expected unavailable-rule fixture logs |
| `mypy --follow-imports=silent tests/test_map_fullscreen.py checks/map_fullscreen_browser_check.py` | Passed, 2 source files |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.map_fullscreen_browser_check --axe /tmp/ama-532-axe-4.10.3.min.js --out /tmp/ama-532-map-check-6` | Passed, 9 axe states, zero violations, zero unresolved ARIA references |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.design_system_browser_check` | Passed both existing design-system and workbench browser flows |
| `ruff check --isolated --line-length 100 --select E,F,I,B,UP` on the two new Python files | Passed |
| `ruff format --check --isolated --line-length 100` on the two new Python files | Passed |
| `node --check src/api/src/zava_forward/api/web/app.js` from repository root | Passed |
| `git diff --check` | Passed |

Every heavy run uses `exec 9>/tmp/ama-rpi-heavy.lock` and `flock -n 9`;
failed admission sleeps 20 seconds and stops at 2400 seconds. Attempt 6's lock
was released when the command completed.

Evidence: `/tmp/ama-532-unit-6.log`, `/tmp/ama-532-browser-6.log`,
`/tmp/ama-532-design-browser-6.log`, plus screenshots, browser version/error
record and raw axe report under `/tmp/ama-532-map-check-6/`.
Chromium 156.0.8078.4; axe 4.10.3 SHA-256
`880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`.
All 9 states retain only color-contrast incomplete rules, primarily short marker
codes or layered map backgrounds. They are not passed manual contrast judgments.
No screen reader/human AT, staff usability or full WCAG acceptance is claimed.
The final desktop/320px expanded screenshots were inspected directly.

No source changes followed this validation before the original Review.

## Amendments and Divergences

No product or scope divergence. PC-001's worker-only filesystem restriction
does not apply to the caller; explicit shared-lock instruction takes precedence.
PC-002 through PC-004 were incorporated before source implementation.

## Review and Publication Boundary

Original Review executed once: Complete / Not accepted. Full gate invokes az, prohibited by this task.
Check prerequisites and preserve local candidate; no bypass or remote mutation.
Coordinator must complete exact-head/current-main receipt and independent
publication assessment before push/stacked PR. The executable is installed at
`/usr/bin/az`, but `tools/rpi-checks.py:1358` invokes `az bicep version` and its
infra group invokes az build/lint. The full gate was not executed: this is a
prohibited-command boundary, not a missing-tool claim.

A read-only fetch found the parent ref has diverged from the worktree's original
base `6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c`. At the check,
origin/main was `9bfed51863b05a25e9939d82504c576524688e14`,
origin/feat/case-journey-ux-526 was
`73e365e618d8cf701a12434e4cd0c2f2affb07f1`, and the common ancestor was
`1dde6a908c20358dbb3067dcdd674e5ad0bd246d`. PR #529 remained open.
No merge, rebase or history rewrite is authorized here. Preserve issue-only
local commits against the supplied original base; coordinator must reconcile
the current stack before publication and rerun affected checks/gate afterward.

## Prepared Stacked PR Handoff (Not Published)

Base: `feat/case-journey-ux-526`.
Title: `feat(web): expand map with accessible home summaries`.
Dependency: PR #529 is unmerged. This branch is stacked on that workstream.
No briefing code or #531 async helper is changed.

Proposed body:

```markdown
Refs #532

Depends on #529 (feat/case-journey-ux-526); this PR is stacked and targets that
branch, not main.

Adds a near-full-screen map with a narrow left information panel. Home markers
open a summary and native Open home link in both modes. Embedded cards have a
top-right close icon and map-click dismissal. Keyboard, Escape/focus return,
non-colour status, reduced motion and manual list navigation are retained.
Coordinator summaries preserve fields withheld by the existing map API.

Pattern references: repository Fluent 2 design system, WCAG/content standards,
Fluent React Card/Inline Drawer/Dialog stories, and current Web Interface
Guidelines. No framework swap or briefing changes.

Focused unit/browser/axe results and original RPI critique/Review are recorded
in the dated tracking artifacts. Automated results are not human AT acceptance.
```

Only the coordinator should publish after stack reconciliation, final gate,
receipt verification and independent exact-head assessment. Add the actual
verified publication evidence to this body; no unrun gate is a success.

## Original Review and Ranked Follow-Up Routing

Independent Review:
`.copilot-tracking/reviews/logs/2026-10-28/map-fullscreen-532-review.md`.
Assessed implementation commit `9b9e467ab5b3d08621173e1cceff6e35c786b2d5`.
Execution Complete; outcome **Not accepted**. Exactly one original Review ran;
its original findings and outcome remain unchanged.

1. RV-001 [Medium], implementation defect: new map keyboard handling consumes
   Ctrl/Meta +/- browser zoom and Alt+Arrow navigation. The reviewer established
   consumption in a bounded Node probe of the exact handler. Passing focused
   browser checks did not cover modifier commands. Route to later `rpi-implement`
   for modifier guards and assertions that those keys neither move/zoom the map
   nor prevent default. Preserve Shift-generated plus and motion checks.
   Ranked first because the change is small and directly restores browser
   accessibility behavior. No correction/closure verification ran in this task.
2. RV-002 [Medium], residual publication: coordinator reconciles the diverged
   stack under appropriate authority, commits the resulting candidate, and runs
   the complete permitted local gate with a fresh external receipt. Fetch main,
   verify immediately before independent exact-head publication assessment and
   push, then open the PR against `feat/case-journey-ux-526`, declaring dependency
   #529 and `Refs #532`. Ranked next because it gates all external delivery.
3. RV-003 [Low], residual human evidence: accessibility/staff owners assess
   contrast incompletes and both map modes with the baseline's AT/browser,
   resize/zoom and staff tasks. Ranked third because it needs human participation;
   automation and native token styling cannot supply that acceptance.

The reviewer could not access /tmp under its own filesystem policy and attributed
the raw check results to the supplied canonical evidence. The implementing parent
did inspect the external axe report and actual final screenshots. That reviewer
limitation neither fabricates independent visual inspection nor invalidates the
parent's explicitly required shared lock.

Implementation was committed locally with runtime GitHub-derived noreply identity
and the requested Conventional Commit/trailer. Final evidence is a separate local
closeout commit. No source was changed after the original Review, no second Review
ran, no az/Azure command ran, and no push or PR creation was attempted.
