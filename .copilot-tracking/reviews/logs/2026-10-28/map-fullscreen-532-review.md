---
title: Map fullscreen issue 532 original Review
description: One independent post-implementation assessment and routing record
ms.date: 2026-10-28
---

## Opening Review State

Task 532 / map-fullscreen-532. Assess the full issue-specific implementation
at `9b9e467ab5b3d08621173e1cceff6e35c786b2d5`, compared with its original
supplied parent base `6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c`.
This is the single original post-implementation RPI Review, not the later
full-gate publication exact-head assessment.

Evidence set:

* `.copilot-tracking/research/2026-10-28/map-fullscreen-532-research.md`
* `.copilot-tracking/plans/2026-10-28/map-fullscreen-532-plan.md`
* `.copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md`
* `.copilot-tracking/plans/2026-10-28/map-fullscreen-532-critique.md`
* `.copilot-tracking/changes/2026-10-28/map-fullscreen-532-changes.md`

Acceptance basis: issue #532, user instructions, plan FR1-FR6/AC1-AC6, critique
dispositions and final attempt 6 evidence. P01/P02 are complete; P03 original
Review and local closeout commits are lifecycle work, not pending source fixes.

Read-only boundary: only this Review record may be written. No source, plan,
details, research, critique, changes or deployment edits. No heavy runs, az,
secrets, `.env`, private data, remote writes or nested reviews.

Initial publication blockers: required full runner invokes prohibited az;
remote stacked-parent ancestry has diverged from supplied base. Neither prevents
reviewing the local issue-only candidate. Human AT/staff acceptance and retained
axe contrast incompletes remain explicitly unaccepted. Refresh web rules before
reviewing the changed web files.

## Scope and Evidence

* Review date: 2026-10-28. Execution count: one independent original Review.
* Implementation: 9b9e467ab5b3d08621173e1cceff6e35c786b2d5.
* Original supplied base: 6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c.
* HEAD matched the supplied implementation. The comparison used these two
  immutable commits, not current main or the changed remote parent.
* Source/test/document boundary: src/api/src/zava_forward/api/web/app.js,
  src/api/src/zava_forward/api/web/style.css,
  src/api/checks/map_fullscreen_browser_check.py,
  src/api/checks/design_system_browser_check.py,
  src/api/tests/test_map_fullscreen.py and src/api/README.md.
* Compared the five canonical artifacts listed above, the issue #532 body
  retrieved with `gh issue view 532 --json title,body`, and the six-file diff.
  Repository context included docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md,
  docs/reference/memory.md and the three project UX standards listed below.
  Memory is context, not acceptance evidence.
* Refreshed Web Interface Guidelines successfully from
  https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  on 2026-10-28, after activating rpi-review and web-design-guidelines.
* The pre-existing dirty session-state file and this untracked opening Review
  were observed, not moved, staged or otherwise changed by this reviewer.

## Execution Status

* Execution status: Complete.
* All supplied requirements, FR1-FR6, AC1-AC6, P01-P03 markers, critique
  dispositions, implementation-time refinements, validation and follow-up
  boundaries were compared. One bounded read-only Node probe established RV-001.
* Complete describes this Review, not implementation acceptance, completion of
  every lifecycle task, full-gate execution or publication readiness.
* External raw evidence under /tmp was not read: this reviewer's filesystem
  policy prohibits operations there. Final browser/test results below are
  attributed to the canonical changes record and explicit caller evidence.
  This limitation does not establish a restriction in the implementing
  parent's execution context and does not invalidate its required shared lock.

## Plan-to-Change Reconciliation

| Current plan scope | Changes and implementation evidence | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01; FR1-FR3; AC1-AC2 | Same Leaflet instance moves into a named native dialog; left sidebar hosts the summary; embedded card overlays the map; native Open home link uses permitted map fields | Reconciled | Required architecture and summary-first behavior present; no framework or payload expansion |
| P01-T02; FR4-FR5; AC3 | Close icon, map click, Escape ordering, marker-ID restoration, same-ID selection, abort/session disposal and explicit no-animation paths | Reconciled | Core lifecycle supported; custom keyboard refinement introduces RV-001 |
| P02-T01; AC4-AC5 | Six static contracts, one 350-line focused browser script, two summary-first link activations in existing browser checks | Reconciled | File/contract budget met; zero removals; modifier-shortcut regression is not covered |
| P02-T02 | API README describes controls, withheld fields, manual paths and evidence limits | Reconciled | Directly related documentation; no briefing or #531 helper edits |
| P02-T03 | Final attempt 6 supersedes historical attempts after tooltip ARIA correction | Reconciled | Recorded focused checks passed; raw artifacts unavailable to this reviewer; no full-gate claim |
| P03-T01 | Guidelines refreshed and this existing canonical record completed once | Reconciled by this Review | Plan and changes correctly described Review as pending when committed; they are not rewritten in this read-only stage |
| P03-T02 | Source/artifact candidate exists; final Review/evidence closeout remains parent-owned | Lifecycle work remains | No reviewer commit, identity configuration or remote write; not an unfinished feature claim |
| P03-T03 and Follow-Up Items | Prohibited az prerequisite and diverged stacked parent prevent publication | Reconciled | Prerequisite assessment is complete; full gate and publication remain unmet, RV-002 |

## Completed Work Assessment

| Acceptance boundary | Evidence and assessment |
| --- | --- |
| Issue full-screen toggle and narrow left panel; FR1/AC1 | app.js:1401-1437 relocates/restores the same box and invalidates map size without animation. style.css:208-216 supplies near-viewport geometry, left grid panel, scrolling and safe areas. Recorded desktop and 320/390px checks support the layout |
| Home click/Enter/Space summary in both modes; FR2-FR3/AC2 | app.js:1335-1343 retains explicit marker activation; app.js:1359-1391 builds text nodes, status words/symbol and native encoded case link. The existing browser expectations intentionally add Open home activation rather than immediate navigation |
| Embedded top-right close, map click and Escape; FR4/AC3 | app.js:1374-1377 names the close action; app.js:1405-1411 closes the summary before native dialog cancellation; app.js:1483 handles map-background dismissal. Recorded browser assertions cover close position, marker focus and second-Escape toggle return |
| Selection/redraw/failure/route/session behavior; FR5 | app.js:1365-1373, 1438-1447, 1494-1506 and 1514-1541 recover by current marker ID or map region, preserve summary focus, remove stale cards and dispose map/dialog. login invokes disposal. Behavioral checks cover representative redraw, filter, failure and route navigation, not every session/AT combination |
| Manual equivalent; FR6/AC4 | Native map-area case links remain. Expanded Overview list navigation collapses first; Coordinator shortcut collapses then focuses Selected records. Browser assertions exercise both exits |
| Non-colour, reduced motion and keyboard; AC4 | Existing shapes/codes and words are reused; movement paths disable animation and focus autopan. Recorded forced-colour and reduced-motion checks passed. Browser/platform modified shortcuts are an uncovered defect, RV-001 |
| Validation; AC5 | 39 focused units, targeted mypy, new-file strict Ruff/format, Node syntax, focused browser and complete existing design/workbench browser are recorded passed in final attempt 6. Nine axe states report zero violations and no unresolved ARIA references; contrast incompletes remain |
| Independent critique and original Review; AC6 | Original Complete / Revise critique preserved; PC-001 rejected with caller-specific rationale, PC-002-PC-004 applied. This is the single original Review; it does not substitute for later publication exact-head assessment |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change, trigger and reconciliation | Assessment |
| --- | --- | --- |
| P01-T01/T02; PC-002 | Summary heading receives focus, expanded entry targets exit toggle, missing markers fall back to the in-surface named map region; plan and details explicitly match source | Within requested focus intent; no unresolved user product decision |
| P02-T03, attempts 1-2 | Browser-chrome traversal was distinguished from focusable background controls; a retained Leaflet class was replaced with observation of actual animation | Corrected test observations, not fabricated application fixes; original failures retained |
| P01-T02/P02-T01, attempts 4-5 | Inspection found keyboard animation, drag inertia/focus autopan and preventScroll hiding the summary heading; details describe explicit no-animation keyboard paths and normal focus scrolling | Rationale and behavioral assertions reconciled; newly introduced modifier handling is defective, RV-001 |
| P01-T02/P02-T03, attempt 6 | Retained axe evidence exposed dangling tooltip aria-describedby references; redundant tooltip removed, named marker and summary retained, static guard added | Tightly coupled accessibility correction; final validation and fingerprints correspond to corrected source |
| P03/Follow-Up Items | Installed-but-prohibited az and moving parent ancestry are explicitly recorded; coordinator resume sequence separates original Review from exact-head publication assessment | Descriptive delivery-state amendment, not authorization to rebase, bypass or publish |

These updates preserve the confirmed native-stack product direction. No material
architecture or product-scope divergence needs a new planning/critique cycle.
RV-001 is an implementation defect within that direction, not a missing product
decision.

## Critique and Material Revision Assessment

* PC-001 [High], rejected: the original finding extrapolated the critique
  worker's /tmp restriction to its caller. The explicit caller requirement is
  the shared /tmp/ama-rpi-heavy.lock with nonblocking admission bounded to
  40 minutes. Plan, details and changes retain that requirement; final attempt
  6 is recorded admitted within budget after contention. This Review's own
  filesystem limitation is not evidence against that disposition.
* PC-002 [Medium], applied: deterministic summary/dialog entry, stable-ID
  restoration, connected fallback and background-redraw focus preservation are
  present in current plan, details, source and behavioral assertions.
* PC-003 [Medium], applied to delivery instructions: details require runtime
  `gh api user` id/login-derived repository-local noreply attribution, not a
  fixed identity. This Review does not certify future closeout commits or
  reconfigure identity.
* PC-004 [Medium], applied: coordinator owns authorized reconciliation, final
  committed candidate/evidence, permitted complete gate, fresh external receipt,
  current-main verification, independent exact-head publication assessment and
  only then push/stacked PR. Original Review is preserved distinctly.
* The original critique remains Complete / Revise; dispositions do not
  retroactively replace it with a passing critique. No unresolved significant
  product choice, early resumption after an unaccepted decision, or missing
  material-revision planning evidence was found.

## Web Guideline Assessment

Applied the freshly fetched rules to the changed native app feature, not the
unrelated legacy application. Project sentence-case/plain-ASCII content and
owner-selected Fluent 2 standards take precedence over generic title-case and
curly-punctuation advice. Forms, new images/media, hydration, new asset origins,
destructive actions and locale formatting are not introduced by this slice.
Transient map presentation is not treated as an unapproved routing/framework
redesign requirement.

### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:1470 - RV-001 [Medium]:
custom map key handler consumes Ctrl/Meta +/- browser zoom and Alt+Arrow
navigation shortcuts; preserve modified browser/assistive-technology commands.

Otherwise no additional material changed-feature finding: native actions/links,
named icon, hidden decorative symbol, live map status, modal semantics, explicit
focus recovery and safe text construction are present. Leaflet-generated marker
controls retain the existing accessible naming/keyboard integration rather than
introducing a new click-only div.

### src/api/src/zava_forward/api/web/style.css

Pass by bounded inspection, subject to RV-003 human validation: shared visible
focus styling remains, new card actions have hover feedback, text wraps, grid
children can shrink, card/sidebar overscroll is contained, modal layout uses safe
areas, and no new motion/transition-all or zoom-disabling rule is added.
Recorded small-width browser results are supporting evidence, not independently
inspected screenshots in this Review.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate feature acceptance | Owner / next action | Route |
| --- | --- | --- | --- |
| Human AT, manual contrast and staff usability | Automation cannot establish human acceptance; nine axe states retain contrast incompletes | Accessibility owner and representative staff test the map/card workflows and record decisions | RV-003, distinct follow-up; no invented acceptance |
| Full exact-head gate and hosted checks | Separate mandatory publication evidence; required az is prohibited here | Coordinator clears the command authorization/prerequisite boundary and performs the complete sequence | RV-002, blocked publication follow-up |
| Diverged parent ancestry | Original-base implementation Review cannot authorize history reconciliation | Coordinator obtains authorization and reconciles the intended stack before a fresh candidate gate | RV-002, same publication follow-up |
| Full Fluent implementation adoption | Existing project-wide issue #150 remains open; this issue forbids a framework swap | Existing design-system adoption owner retains the wider implementation/acceptance decision | Existing distinct work; not a new #532 defect |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Custom map keys consume browser zoom and navigation shortcuts

* Classification: implementation defect; acceptance-blocking for this candidate.
* Related scope: P01-T02, P02-T01; AC4 keyboard accessibility and preservation of
  existing browser behavior.
* Evidence: src/api/src/zava_forward/api/web/app.js:1467-1476 disables Leaflet
  keyboard handling and replaces it with a handler whose only guards are
  defaultPrevented and a Leaflet-control target. It handles +/-/= and arrows
  without checking ctrlKey, metaKey or altKey, then calls preventDefault.
* Verification: a read-only Node probe extracted this exact new handler body,
  supplied a stub map and modifier-bearing events, and observed all three:
  Ctrl+= -> setZoom(11) and prevented=true; Meta+- -> setZoom(9) and
  prevented=true; Alt+ArrowLeft -> panBy([-80,0]) and prevented=true.
  This proves handler consumption; no real-browser shortcut/OS behavior was
  independently rerun.
* Impact: while the map or a marker has focus, standard page-zoom or browser
  navigation commands are captured as map commands. In the native modal the
  surrounding application is intentionally inert, making preservation of
  browser accessibility controls particularly important.
* Coverage gap: src/api/checks/map_fullscreen_browser_check.py:195-231 verifies
  reduced-motion button zoom and unmodified Arrow panning, not modified keys;
  the six static unit contracts do not catch this.
* Destination: later rpi-implement invocation, scoped to this defect.
* Smallest useful next action: ignore Ctrl/Meta/Alt-modified map commands without
  preventing their defaults, retain unmodified arrows and +/- including the
  Shift-generated plus key, and add assertions that modified commands neither
  move/zoom the map nor become defaultPrevented. Retain the current motion tests.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Publication remains blocked by prohibited gate commands and diverged ancestry

* Classification: residual delivery work and publication blocker, not a source
  defect or a failure of this original-base Review.
* Related scope: P03-T03 and plan Follow-Up Items.
* Evidence: canonical changes record, Review and Publication Boundary and
  Prepared Stacked PR Handoff. It records /usr/bin/az installed, required
  tools/rpi-checks.py preflight/infra invoking az, and no complete gate/receipt.
  It records remote parent 73e365e618d8cf701a12434e4cd0c2f2affb07f1 diverged
  from original supplied base 6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c while
  PR #529 remained open. These are supplied recorded observations, not a fresh
  remote-lifecycle certification by this reviewer.
* Impact: focused checks and this Review cannot authorize push or PR creation;
  reconciliation changes the candidate/base and invalidates prior gate evidence.
* Destination: distinct coordinator publication follow-up, not rpi-implement,
  rpi-plan product revision, or rpi-research.
* Smallest useful next action: obtain authorization for stack reconciliation
  and required commands; after resolving RV-001 and committing final source and
  dated original evidence, run the fresh complete local gate with a new external
  receipt. Fetch main and verify that receipt against current origin/main
  immediately before independent exact-head publication assessment and push.
  Preserve invalidation on later source/base/input/tool/image changes. Only then
  create the stacked PR targeting feat/case-journey-ux-526, declaring #529 and
  using Refs #532 only. No skip, cloud fallback or protection change.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Automated results leave manual accessibility and usability acceptance open

* Classification: non-blocking residual work for the bounded automated slice;
  not evidence that a specific contrast or AT defect exists.
* Related scope: AC4-AC5; plan Follow-Up Items.
* Evidence: changes record Final Validation (Attempt 6), API README:96-103,
  docs/reference/research/ux/wcag-conformance-baseline.md and
  docs/reference/research/ux/design-system.md. Nine reported axe states retain
  only color-contrast incomplete rules; human AT/staff acceptance is expressly
  unperformed, and native Fluent-token styling is not full Fluent adoption.
* Impact: zero automated violations cannot support a WCAG conformance, manual
  contrast, screen-reader usability, staff acceptance or complete Fluent
  implementation-adoption claim.
* Destination: distinct accessibility/staff-validation follow-up owned by the
  accessibility owner and representative staff; existing #150 owns broader
  Fluent adoption.
* Smallest useful next action: assess retained contrast incompletes and exercise
  both map modes with the project baseline's browser/AT, text-resize/zoom and
  human task checks. Record actual tools, people, dates, results and exceptions.
  Keep any later discovered defects separate from this residual evidence limit.

## Defects and Routed Findings

* Source defects: RV-001 only. No Critical or High finding.
* Severity summary across all entries: 0 Critical, 0 High, 2 Medium, 1 Low.

| Finding | Destination | Owner / smallest next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent scopes modifier guards and regression assertions | Existing-direction implementation defect |
| RV-002 | Distinct publication follow-up | Coordinator clears authorization/ancestry prerequisites and performs fresh full exact-head sequence | Residual delivery blocker, not a product defect |
| RV-003 | Distinct human accessibility/staff follow-up | Accessibility owner and staff assess incompletes and real workflows | Evidence limit explicitly outside automated acceptance |

No finding needs rpi-plan or rpi-research. A later implementation invocation
does not require another original RPI Review; the independent exact-head
publication assessment remains a separate mandatory gate.

## Validation Evidence

| Check | Status | Evidence and limit |
| --- | --- | --- |
| Exact commit/base diff, six files | Passed by reviewer inspection | Supplied original base used; no current-parent substitution |
| SHA-256 fingerprints of app.js, style.css, new browser script and new unit module | Passed independently | All four exactly match final-attempt-6 fingerprints in canonical changes |
| Six-file diff whitespace check | Passed independently | git diff --check against supplied base/head exited 0 |
| Isolated new keyboard-handler modifier probe | Failed behavior; probe completed | Three modified commands were consumed, establishing RV-001; no source writes or browser launch |
| 39 focused unit tests, no skips | Recorded passed; not rerun | Final attempt 6, 2.309s; expected rule-fixture log messages retained |
| Targeted mypy, two files | Recorded passed; not rerun | Final attempt 6 |
| New-file strict Ruff E/F/I/B/UP and format, 100 columns | Recorded passed; not rerun | Final attempt 6 |
| Node syntax | Recorded passed; not rerun as suite | Final attempt 6 |
| New map browser plus complete existing design/workbench browser | Recorded passed; not rerun | Final attempt 6; Chromium 156.0.8078.4; no uncaught JS errors reported |
| axe 4.10.3, nine states | Recorded zero violations and unresolved ARIA references | Pinned digest 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb; color-contrast incompletes remain, RV-003 |
| Shared heavy-run lock | Recorded admitted within 40-minute budget | Nonblocking flock -n on /tmp/ama-rpi-heavy.lock after contention; no heavy runs by reviewer |
| Raw external logs, JSON and screenshots | Unavailable to this reviewer | /tmp operations prohibited in this context; no invented access or visual inspection |
| Fresh web guideline retrieval and changed-web inspection | Completed | Current source fetched successfully; grouped findings above |
| Human AT/staff/manual contrast | Not performed | RV-003; no acceptance claim |
| Complete tools/rpi-checks.py --all, external receipt verification, independent publication exact-head assessment | Blocked / not performed | Prohibited az and unresolved stack reconciliation; RV-002 |
| Hosted checks, push, stacked PR publication | Not performed | Not authorized by this Review and not claimed complete |

## Blockers and Remaining Work

* Acceptance blocker: RV-001 needs a bounded keyboard-handler correction and
  regression evidence before this implementation candidate is accepted.
* Publication blockers: RV-002 remains independently applicable even after that
  correction. Any correction/reconciliation requires fresh candidate-bound gate
  evidence; final attempt 6 is historical for a subsequently changed candidate.
* Lifecycle work: parent owns final original Review/evidence persistence and
  P03-T02 closeout. This Review only writes its one canonical record.
* Human follow-up: RV-003 remains distinct from source defects.
* No source fixes, plan edits, second Review, nested agents, heavy tests, az,
  private data, secrets, .env, commit, push or history rewrite were performed.

## Outcome

* Outcome: Not accepted.
* Rationale: this Review completed the full supplied comparison and found one
  material keyboard regression, RV-001, despite substantial conformant feature
  behavior and recorded passing targeted checks. The passing suite does not
  cover the consumed modifier shortcuts. Publication and human acceptance remain
  separate residual work, not additional alleged source defects.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent handles RV-001 within the accepted native-map design |
| Decision gap or invalid assumption | None | No product/planning decision needed |
| Material research gap | None | Evidence supports the bounded verdict; external raw-access limitation disclosed |
| Residual publication work | Distinct coordinator follow-up | RV-002 authorization, ancestry, complete gate, receipt/current-main verification and independent exact-head assessment |
| Residual human acceptance | Distinct accessibility/staff follow-up | RV-003 manual checks; existing #150 retains wider Fluent adoption |

Execution is Complete; outcome is Not accepted. Return this single original
Review to the active parent for continuation. It does not approve publication.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/map-fullscreen-532-research.md](.copilot-tracking/research/2026-10-28/map-fullscreen-532-research.md) | Canonical research and pattern evidence |
| [.copilot-tracking/plans/2026-10-28/map-fullscreen-532-plan.md](.copilot-tracking/plans/2026-10-28/map-fullscreen-532-plan.md) | FR/AC, Pxx markers and follow-up boundary |
| [.copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md](.copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md) | Current-state phase details |
| [.copilot-tracking/plans/2026-10-28/map-fullscreen-532-critique.md](.copilot-tracking/plans/2026-10-28/map-fullscreen-532-critique.md) | Preserved original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-28/map-fullscreen-532-changes.md](.copilot-tracking/changes/2026-10-28/map-fullscreen-532-changes.md) | Amendments, final validation and publication handoff |
| [.copilot-tracking/reviews/logs/2026-10-28/map-fullscreen-532-review.md](.copilot-tracking/reviews/logs/2026-10-28/map-fullscreen-532-review.md) | This single completed original Review |
| [docs/reference/research/ux/design-system.md](docs/reference/research/ux/design-system.md) | Fluent 2 standard and adoption limits |
| [docs/reference/research/ux/wcag-conformance-baseline.md](docs/reference/research/ux/wcag-conformance-baseline.md) | Accessibility target and human evidence limits |
| [docs/reference/research/ux/content-standard.md](docs/reference/research/ux/content-standard.md) | Project plain-language standard |
| [src/api/README.md](src/api/README.md) | Controls, reproducible focused check and acceptance limits |

## Next Steps

The active parent should route RV-001 to a bounded rpi-implement continuation,
preserve this original Review outcome, and keep RV-002/RV-003 with their distinct
owners. No second original Review is requested. Coordinator publication remains
blocked pending authorized stack reconciliation and the full exact-head
publication sequence. This reviewer stops without fixes or remote actions.
