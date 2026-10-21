<!-- markdownlint-disable-file -->
# Review: issue-151-cited-answer-contrast

## Scope and Evidence

* Reviewed implementation commit 55f3f33307d6efa62adf7058220283198e65717a on `fix/regulatory-contrast-151` (base 993a7b88c03f5240f1e7a4c7c7afa7c064281622), date 2026-10-21.
* Artifacts: .copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-plan.md, .copilot-tracking/details/2026-10-21/issue-151-cited-answer-contrast-phase-details.md, .copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-critique.md, .copilot-tracking/changes/2026-10-21/issue-151-cited-answer-contrast-changes.md, .copilot-tracking/research/2026-10-21/issue-151-cited-answer-contrast-research.md.
* Code reviewed by reading the committed diff directly (no review subagents; the boundary is small).
* web-design-guidelines source refetched 2026-10-21; the refresh returned only its first 1500 characters in this pass (partial); the full rule set was read in the implementation pass moments earlier. Changed web file: style.css only. Rules applied: Animation (list properties, no `transition: all`, honour reduced motion), Focus States, Hover states. No violation found.

## Opening Review State

Review began after the implementation commit with a clean tracked tree.

## Execution Status

Complete for the supplied boundary. Not performed: complete local RPI gate, hosted CI, manual screen-reader/keyboard test, whole-app review.

## Plan-to-Change Reconciliation

All plan markers P01 to P03 and their tasks are checked and match the changes record. The red-before-green sequence and the requirements-files reuse are evidenced. Plan follow-up items: none.

## Completed Work Assessment

* P01-T01 unit regression: present, scoped to rules naming `button` or `.btn`; fails on the original CSS (recorded).
* P01-T02 mid-fade states: present; fails on the original CSS through the helper's colour assertion; passes on fixed CSS (19 states).
* P02-T01 fix: `button,.btn` transitions border-color only; `.item,.tile` unchanged; reduced-motion token unchanged.
* P03-T01: four files, certifi-only diff (verified at implementation).
* P03-T02: README paragraph added, no conformance claim.

## Implementation-Time Plan and Detail Update Assessment

One disclosed divergence: AC-1 expected the red browser state to show an axe `color-contrast` violation; the committed helper asserts the computed colour before axe, so the red failure is that assertion. The axe violation on the same state was observed through an uncommitted probe. The divergence is recorded in the changes record and does not weaken coverage.

## Critique and Material Revision Assessment

Critique ran once (Revise); all six findings were applied directly; no user decision was required and no second critique ran. Applied items are visible: fractions, non-empty parse guard, deferral of the gate, `.alt` follow-up dropped after observation.

## Plan Follow-Up Assessment

None open.

## Findings

### RV-001 [Low]: Unused JavaScript variable left in the helper

* Evidence: src/api/checks/regulatory_ux_check.py line 109 declares `const field = document.querySelector('#regulatory-question');` in `scan_mid_fade` and never uses it. An attempted removal during implementation did not take effect, and the changes record does not mention it.
* Impact: dead code only; behaviour is correct.
* Destination: distinct follow-up for `rpi-implement` (one-line removal).

### RV-002 [Low]: Unit guard only inspects rules naming `button` or `.btn` directly

* Evidence: src/api/tests/test_regulatory_ux_check.py `test_button_background_is_not_animated`; a future selector such as `button.alt` with a background transition would not be caught. The browser mid-fade state still covers the lookup button.
* Impact: partial protection of the class.
* Destination: residual work, optional.

### RV-003 [Medium]: Hosted timing and complete gates not exercised

* Evidence: changes record "Not performed"; the natural hosted failure was not reproduced locally, only the frozen state (research caveat).
* Impact: hosted stability is unconfirmed until the coordinator's gate and hosted run.
* Destination: residual work for the coordinator (complete local gate, hosted src-api job); not a code defect.

### RV-004 [Low]: Local validation environment is not reproducible from the record

* Evidence: validation used an existing venv whose editable installs point at another worktree, overridden by PYTHONPATH (path resolution verified).
* Impact: results are valid for this tree but rely on a local prerequisite.
* Destination: residual work, covered by the coordinator's gate.

## Defects

None material. RV-001 is a trivial cleanup.

## Routed Findings

* RV-001 to a later `rpi-implement` (optional).
* RV-002 residual work.
* RV-003 and RV-004 to the coordinator's complete gate.

## Residual Work

Original #151 criteria remain unmet except as noted: no target level decision, audit, whole-app CI coverage, manual screen-reader record, accessible equivalents or statement are delivered or claimed here.

## Blockers and Remaining Work

No blockers for this task. Remaining: complete local gate, independent exact-head assessment, hosted checks, partial PR with Refs #151.

## Validation Evidence

See the changes record Validation table: regulatory browser check 19 states PASS (axe 4.10.3, SHA-256 verified), design-system browser check PASS, unit module 5 OK, related unit modules 94 OK, ruff/format/mypy pass, red runs on unfixed CSS fail as recorded.

## Outcome

Outcome: Residual work (no material defects; a low-severity cleanup and unexercised hosted/gate validation are routed).

## Closeout Routing Record

Review executed once. Next: coordinator runs the complete gate and independent assessment; optional later `rpi-implement` for RV-001.
