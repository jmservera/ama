---
title: Role workbench IA 152 review
description: One post-implementation RPI assessment of the shared API workbench slice
ms.date: 2026-10-15
---

## Review Metadata

Task `152`, slug `role-workbench-ia-152`. Execution: Complete.
Outcome: Defects found. Boundary: shared API navigation, responsive layout and
recovery, not role-specific screens or full issue/product acceptance.

Current disposition: RV-001 fixed in the explicitly requested follow-up on
PR #317. The delayed-briefing regression failed against the original app.js
and passes with the fix. This updates finding disposition, not the historical
Review outcome or its one-pass execution. RV-002 to RV-004 remain open; device
support and full AC-034/043 acceptance are still unchecked.

## Compared Artifacts

* `.copilot-tracking/research/2026-10-15/role-workbench-ia-152-research.md`
* `.copilot-tracking/plans/2026-10-15/role-workbench-ia-152-plan.md`
* `.copilot-tracking/details/2026-10-15/role-workbench-ia-152-phase-details.md`
* `.copilot-tracking/reviews/2026-10-15/role-workbench-ia-152-plan-critique.md`
* `.copilot-tracking/changes/2026-10-15/role-workbench-ia-152-changes.md`
* Issue #152 body/comments, ADR 0006, parity matrix, PRD SA-001/002/003/007,
  AC-034/043 and UX-07 boundary.

## Reconciliation

P01/P02 source/evidence tasks checked; publication explicitly remains the
parent post-Review action. One critique executed; six direct dispositions.
Owner device and complete journey criteria remain unchecked. No open
implementation failure reported; all five suites, lint/types, final targeted
regressions and both real local browser checks have results.

## Opening Review State

Interpreted goal: compare complete shared-IA plan to actual source and evidence,
not accept the full issue. All five task artifacts and independent critique
were available. First comparison: production diff, followed by new module/
manifest/tests and validation semantics. Read-only source boundary; this one
record is the only Review-owned write. No initial evidence blocker.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 server navigation | workbench.py, `/api/me`, test_workbench, eight browser identities | Existing permission rules reused; no rights added |
| P01-T02 context/layout | app.js, shell, CSS and coupled catch paths | Mine/all/reset/status/safety implemented; delayed briefing defect found below |
| P02-T01 fixtures/browser | workbench-manifest.json, both browser checks | Independent IDs/routes and explicit partial/deferred declarations; no full journey claim |
| P02-T02 validation | changes command table | 931 tests/97 SQL skips, all project lint/types and final 34 targeted regressions pass; both browser suites pass |
| P02-T03 documentation | API guide, UX synthesis, index/log | Updated; publication belongs to parent after this Review |

## Implementation-Time Update and Critique Assessment

PC-001 readiness gate is applicable: an introduced defect found during this
Review means no conformant/ready claim. PC-002 independent manifest, PC-004
local scratch and PC-006 CI integration are implemented. PC-003 route lifetime
is substantially implemented, but missed the cached briefing lifecycle.
PC-005 provides measured queue/case widths, enlarged text and keyboard/reset/
status checks, not human conformance.

Root venv ignore, CSSOM text enlargement, preserving table-scroll behavior,
and cancellation in map/Finance/time/proposal views are justified local
amendments preserving user intent. They do not justify the briefing gap.
No significant owner decision was invented; no extra critique ran.

## Findings

### RV-001 [Medium]: Cancelled cached briefing remains permanently loading

* Related scope: P01-T02, PC-003 and preserved AI assistance.
* Evidence: app.js `briefingBox` is retained across routes; `aiBox` starts a
  request using the current route controller, then removes its box on failure.
  `listView` reuses any non-null cached box without restarting its request.
* Reproduction: real local API, same synthetic fixture and isolated launcher.
  Hold `/api/briefing` at login, wait for My cases, navigate All cases then
  My cases before releasing the response. Observed one briefing request total,
  one Today's briefing heading and one "Reading your cases..." placeholder
  after return. Releasing the obsolete response does not restart assistance.
* Impact: switching queues during initial assistance can strand the AI briefing
  in a false loading state. Ordinary case work, proposals and manual controls
  remain available, but preserved-assistance recovery is not complete.
* Destination: later `rpi-implement`, highest priority distinct follow-up.
* Smallest next action: reset or scope the cached briefing when its request is
  cancelled; show an explicit current failure/retry instead of cached loading.
  Add this exact delayed-briefing scenario to the existing browser check.
* Original disposition: open, blocks ready/conformant shared-slice claim.
  Repair was routed to a distinct later invocation, not performed inside Review.
* Current disposition: fixed by the user-requested PR #317 follow-up. `aiBox`
  captures each request's route signal and synchronously clears only its own
  cached panel on abort while pending. Completion removes the abort listener,
  preserving successful cached briefings. Non-abort failures expose an alert
  and retry; old cancelled responses cannot replace the new panel.
* Regression: existing CI design-system entry point invokes the extended
  workbench check. Hold the initial response through My cases -> All cases ->
  My cases; assert three requests, fulfill the current one, then release old
  responses. Assert recovered content, no stale/loading content, one panel and
  no additional calls when navigating with a completed cache. Also assert
  explicit failure/retry preserves workflow-only mode. The exact request-count
  assertion fails before the production fix and passes afterward.
* Follow-up validation: requested absolute-PYTHONPATH API suite passes,
  498 run / 400 passed / 98 skipped; both browser suites pass in Chromium
  156.0.8078.4; `/tmp/zf164/bin/mypy .` passes (40 files), ruff lint/format and
  isolated browser-harness lint/format pass, as does app.js syntax.
  No second Review or independent human acceptance is claimed.

### RV-002 [Medium]: Supported devices and field/mobile use remain undecided

* Evidence: #152 first checkbox, research W1 and API guide. Engineering widths
  are not an owner-approved browser/device matrix.
* Impact: no supported-device or complete issue acceptance claim is justified.
* Destination: distinct owner decision through `rpi-plan`.
* Smallest next action: approve browser/device/field-use scope, then map
  engineering checks to that decision. This is not an implementation defect.

### RV-003 [Medium]: Full AC-034/043 and originating-row recovery are partial

* Evidence: manifest declares eleven perspectives/nine workflows as partial
  or deferred; only eight current auth roles exist. UX-07 explicitly lacks
  row selection, scroll, prior pagination and originating-row focus recovery.
* Impact: successful layout/reset checks do not satisfy full cross-profile
  journey acceptance. The issue's last criterion stays unchecked.
* Destination: distinct journey/recovery follow-up coordinated with #225 to
  #233; use `rpi-plan` to select one bounded profile/recovery scope.
* Smallest next action: agree required manifest defaults/endpoints and
  selection/focus semantics; implement/test only that authorized follow-up.

### RV-004 [Medium]: Real-platform and human acceptance evidence unavailable

* Evidence: all browser calls use sanitized synthetic local data; 97 SQL tests
  skipped; Docker socket denied. No actual provider, SQL Server, Azure or
  screen-reader/human acceptance result was produced.
* Impact: mandatory actual-AI/SQL/Azure exercise and human accessibility
  acceptance cannot be inferred from this local build or generic CI status.
* Destination: distinct authorized validation/evidence task, `rpi-research`
  first to verify environment, budget, authority and human-test prerequisites.
* Smallest next action: obtain approved prerequisites and record executed
  non-skipped evidence; do not activate release authority or deploy by inference.

## Validation Evidence and Review Commands

* Five src suites: core 325, agents 70, API 480, orchestrator 17, importer 39;
  931 total with 97 expected SQL Server skips. Baseline core ResourceWarnings
  did not fail tests.
* All five project ruff/format/mypy pass; new browser files pass isolated
  lint/format without migration exemptions. All first-party JS syntax passes.
* Final targeted navigation/design/accessibility/role regression: 34 pass.
* Both complete browser suites pass in Chromium 156.0.8078.4, covering the
  cases listed in changes. The additional Review scenario found RV-001; it
  was not covered by those passing suites.
* `git --no-pager diff -- ...` reviewed production state/IA, shell/CSS,
  launcher and coupled root-view cancellation; large combined output was
  reread as two bounded app.js and remaining-file commands.
* `python3 -` checked relative file targets in the three changed guides and
  parsed state with duplicate-key rejection: pass, no missing file target.
* `cd src/api && ../../.venv/bin/python -` ran the RV-001 Playwright heredoc
  using `main(inspect, synthetic_data)`: server healthy; one held briefing,
  still one request and loading placeholder after queue return. No source
  writes; server/browser/temp fixture cleaned in finally/context managers.

## Blockers, Residual Work and Outcome

The original Review performed no source change or second Review. Its RV-001
readiness blocker has since been fixed and regression-tested by the authorized
follow-up above. RV-002 to RV-004 remain known owner/evidence/residual boundaries,
not waived acceptance criteria. No high/critical finding was identified.

Historical execution: Complete. Outcome: Defects found. RV-001 is now fixed;
this does not accept full issue/product readiness or close residual findings.
Keep the draft Refs #152 PR and unchecked criteria, never Closes or a
conformant/human-acceptance claim.

## Closeout Routing

| Finding | Destination | Owner / next action |
| --- | --- | --- |
| RV-001 | Fixed in authorized follow-up | Cancelled cache invalidated; regression fails before fix and passes after |
| RV-002 | Owner decision / rpi-plan | Supported browser/device/field-use scope |
| RV-003 | Distinct journey/recovery plan | Full profile/workflow and row-focus evidence |
| RV-004 | Authorized validation / rpi-research | Live platform and human-test prerequisites |
