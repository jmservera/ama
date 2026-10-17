---
title: Coordinator lifecycle funnel issue101 original Review
description: Single original review, execution separate from outcome and independent acceptance
ms.date: 2026-10-17
---

## Scope and Evidence

Task101 / coordinator-lifecycle-funnel-101; date2026-10-17.
Initial source/base ebc8dab87ae9bd6a33380b85e86f38be5ed9f213 on the designated
feat/coordinator-lifecycle-funnel-101 branch, current implementation uncommitted.
Review scope: full bounded read-only coordinator task, not general repository
audit or independent customer/coordinator acceptance.

* Research: .copilot-tracking/research/2026-10-17/coordinator-lifecycle-funnel-101-research.md
* Plan: .copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-plan.md
* Details: .copilot-tracking/details/2026-10-17/coordinator-lifecycle-funnel-101-phase-details.md
* Critique: .copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/coordinator-lifecycle-funnel-101-changes.md
* State: .copilot-tracking/rpi-sessions/2026-10-17/coordinator-lifecycle-funnel-101-state.json

## Opening Review State

Goal: compare implemented filtering/denominators/observed funnel/record-map
membership and authorization with exact issue101, FR-020/021 and PR-005, the
accepted plan and PC001-003 dispositions.
Evidence readiness: P01/P02/P03-T01/T02 reconciled complete; actual local core/API,
browser, SQL and image receipts exist. P03-T03 Review and T04 delivery pending.
First comparison: authorization/event membership correctness and changed existing
workbench behavior. Fresh full Web Interface Guidelines source retrieved on
2026-10-17 before Review; owner Fluent/plain-language/native semantics govern
conflicting generic style suggestions. Read-only boundary: this one review record
and workflow state only. No source/artifact correction in Review.
Initial blockers: none preventing review; human/coordinator/WCAG acceptance not
established and not inferred from local checks.

## Execution Status

Execution: Complete. This is the only original Review; there is no repeat,
closure review or rewritten adverse outcome. Full bounded implementation and
artifact comparisons completed. One independent bounded backend lens contributed
evidence; the parent assessed changed web files, refreshed web rules, documentation
and lifecycle reconciliation. This is not independent coordinator acceptance.

## Plan-to-Change Reconciliation

| Current plan scope | Changes record | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01/T02 | Read-only Contract | Implemented with defect | RV-001 denies a legitimate registered identity |
| P02-T01/T02 | Existing Workbench | Reconciled | Native existing-map mode, independent selectors, current/unknown explanations, actual Chromium receipt |
| P03-T01/T02 | Commands and actual results | Reconciled | Focused results separate from earlier coupled regressions; SQL and final image actually executed |
| P03-T03 | Before Original Review | Complete by this record | Original Complete / Defects found retained |
| P03-T04 | Delivery pending | Blocked for publication | PC-003 mandatory correctness gate applies; no corrected-delivery claim |

## Completed Work Assessment

| Related marker | Files | Change and reason | Evidence and validation | Assessment |
| --- | --- | --- | --- | --- |
| P01 | core/coordinator.py, projection.py, API server.py and tests | Reuse Store filters, progress events and closed fields, no new writers | Core26, API18, SQL6 and bounded lens | RV-001 remains |
| P02 | API web/app.js and style.css | Existing map/list/table controls with exact cohort versus metric state | Actual keyboard/filter/exit-A/detail/back/cluster/unknown/denial browser receipt | Bounded engineering evidence; not human/WCAG acceptance |
| P02 | Core/API guides, programme synthesis, KB index/log | Explain denominator, event coverage and unsupported outcomes | Relative links and diff examined | Existing synthesis reused;117 overlap declared |
| P03 | Changes, plan/details/state | Preserve dated actual versus historical checks and cleanup | Explicit pass/skip/rerun and image/source hash receipts | No full-suite or invented closure claim |

## Implementation-Time Plan and Detail Update Assessment

| Area | Change and trigger | Reconciliation | Planning state | Assessment |
| --- | --- | --- | --- | --- |
| P01/P02 | PC-001 independent current-stage and metric-stage selectors | Plan/details/source/browser evidence agree | Single critique Complete / Revise, direct correction accepted | Reconciled |
| P01/P02 | PC-002 forced cluster fixture | Production cap unchanged; test geography corrected instead of altering clustering | Accepted before implementation | Reconciled |
| P03 | PC-003 correctness gate | Unresolved RV-001 now blocks publication/completed delivery | Accepted before implementation | Gate must remain active |
| P01 | Closed scalar record helper and accurate excluded-record stop flags | Directly coupled field minimization/semantics; final focused tests and image rerun | No material architecture/scope divergence | Justified |

## Critique and Material Revision Assessment

Exactly one final-candidate critique executed, original Revise retained.
All PC-001/002/003 advice is compatible with confirmed user scope and was applied.
No dependent writer work resumed, no Store/provenance writer change, no117
runtime path or other worktree inspected. No material change requires a new
critique. RV-001 is a post-implementation defect, not justification to repeat
critique or Review.

## Plan Follow-Up Assessment

| Item | Why outside immediate scope | Next action | Route |
| --- | --- | --- | --- |
| Authoritative lifecycle exclusion/initial-entry capture | No such general current writer; task explicitly read-only | Separate evidence/requirements and approved capture design | Later Research/Plan, never invent actuals |
| Human/coordinator/WCAG acceptance | Engineering and browser checks cannot establish it | Named coordinator/human review of intended task and accessibility | Separate acceptance; unchecked |
| Production-scale aggregation/rendering | Tiny actual browser fixture is not a scale benchmark | Bound realistic grouping/event volumes before scale acceptance | Separate measured performance work, no pass inferred |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Mixed-case registered email falsely denies authorized staff

* Related scope: P01-T01/T02, FR1 and server-authorized access.
* Evidence: src/core/src/zava_forward/core/coordinator.py:160 performs a verbatim
  staff lookup; Store indexes staff by lowercase email at
  src/core/src/zava_forward/core/store.py:59. Authentication at
  src/api/src/zava_forward/api/auth.py:66-87 returns the stored record with its
  original email casing. The bounded backend lens reproduced with fictional
  Pam's stored email changed only to `Pam@Example.Test`, on both JSON and SQLite.
  Normal authentication succeeded; existing GET /api/cases?view=all&limit=2
  returned200, but GET /api/coordinator?view=all&as_of=2026-10-10T12:00:00Z
  returned403 claiming changed access. Signing in again does not fix it.
* Impact: an otherwise legitimate registered staff member cannot use the new
  reporting surface. No privilege escalation or field disclosure is claimed.
* Destination: later rpi-implement correction, not another Review.
* Smallest useful next action: normalize only the lookup key consistently with
  Store/authentication; retain current email/code/role verification and fail-closed
  behavior. Add mixed-case JSON/SQLite HTTP and direct-reader regressions.
* Disposition: open mandatory correctness defect; blocks completed delivery and
  push under PC-003. No source correction or closure assessment in this Review.

## Web Interface Guidelines Findings

### src/api/src/zava_forward/api/web/app.js

No additional mandatory web defect identified in changed lines. Native labelled
inputs, semantic tables/captions, count links, explicit unknowns, live status,
abort guards, inherited visible focus and button-based map-list focus are present.
Keyboard map actions and non-colour signals are reused. Current and metric-stage
state remain distinct. Empty/error/manual paths remain available.

src/api/src/zava_forward/api/web/app.js:1053 - map summary interpolates raw numbers
rather than the coordinator's Intl.NumberFormat helper; low-priority locale/copy
consistency residual, not a denominator correctness failure.

### src/api/src/zava_forward/api/web/style.css

No new scoped-rule finding. Existing Fluent tokens, responsive min-width handling
and tabular numeric columns retained; no new animation or outline suppression.
No screen-reader, full WCAG, production-scale or human-understanding pass inferred.
Machine UTC evidence timestamps intentionally remain explicit ISO; repository
ASCII/sentence-case/plain-language guidance overrides generic curly punctuation
and Title Case suggestions. Images/media/dark-mode/hydration rules add no new
changed-surface requirement here. Large group-table performance remains unmeasured,
not silently treated as accepted.

## Defects

RV-001 is open. Normalize lookup and add targeted regressions in later
rpi-implement; do not weaken authorization or alter Store writers.

## Routed Findings

| Finding | Destination | Next action | Reason |
| --- | --- | --- | --- |
| RV-001 Medium | rpi-implement | Normalize identity lookup, mixed-case regression coverage | Existing legitimate access diverges; mandatory correctness gate |
| Web locale residual Low | Distinct UI cleanup | Reuse number formatter for map status | Non-blocking presentation consistency |

Later implementation of the routed finding does not require another Review.

## Residual Work

Lifecycle exclusions/conversion remain explicit Unknown, not fabricated feature
completion. Human/coordinator/WCAG approval remains unchecked. Production-scale
performance and optional locale cleanup are not completed by tiny browser tests.

## Blockers and Remaining Work

RV-001 blocks completed/corrected delivery and publication (P03-T04). The
one-pass lifecycle routes it to later selected implementation; this task does not
silently transition back to Implement or repeat Review. Commit the original
artifacts and actual implementation locally for persistence; do not push/open a
ready or draft PR while the accepted publication gate remains blocked.

## Validation Evidence

| Command / evidence | Scope | Status | Actual result |
| --- | --- | --- | --- |
| Core coupled unittest selectors in changes | Queue/progress/read/sensor regressions | Passed with skips |154 run,135 pass,19 skips |
| API coupled selectors with ZF_COORDINATOR_BROWSER=1 | HTTP/role/UI contracts plus actual Chromium | Passed with skips |97 run,78 pass,19 skips |
| Final core coordinator discovery | JSON/SQLite semantics | Passed |26 run/pass |
| Final test_coordinator_api with browser enabled | HTTP plus actual Chromium | Passed with skips |18 run,11 pass,7 skips |
| MssqlCoordinatorApi with ZF_COORDINATOR_MSSQL=1 | Actual disposable loopback SQL Server | Passed with skip |6 run,5 pass,1 browser-only skip |
| Ruff/format/mypy, node --check, diff --check | Configured project gates | Passed | Exact commands in changes, no full-suite claim |
| Docker build/check-container/installed-source HTTP | Final source-context image | Passed | c4238ecd132048bdd01ce5bbe5f0c71c31e9a9727ba9bab2507d656b34f2f08c, nonroot/read-only/NoNewPrivs/zero caps and installed hashes |
| Bounded backend lens unittest/repros | New semantics/HTTP, malformed histories, UTC and ledger failure | Passed with skips; additional defect reproduced |44 run,36 pass,8 skips;63 malformed variants plus mixed-case repro on JSON/SQLite |

All test data fictional/public fixture material. Owned SQL/image containers and
debug app/browser were stopped; shared117 SQL resource was not touched.
Existing passing suites omit the newly exposed mixed-case regression; they do
not contradict or close RV-001.

## Outcome

Outcome: **Defects found**. Execution Complete, with one mandatory Medium
correctness finding and one Low web presentation residual. No conformant or
independent coordinator acceptance verdict. The feature's main count/drill
engineering evidence exists, but an authorized-identity counterexample prevents
completed delivery. Do not rewrite this adverse verdict after a later correction.

## Closeout Routing Record

| Finding class | Destination | Next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement | RV-001 minimal lookup normalization and regression |
| Decision gap | None in buildable read-only scope | No new writer/approval authority assumed |
| Material evidence gap | Separate acceptance/performance work | Human/coordinator/WCAG and scale remain unproven |
| Non-blocking residual | Distinct UI cleanup | Map status locale consistency |

Execution: Complete. Outcome: Defects found. Validation: bounded local engineering
receipts above, no full-suite/human acceptance. Blocker: RV-001 publication gate.
