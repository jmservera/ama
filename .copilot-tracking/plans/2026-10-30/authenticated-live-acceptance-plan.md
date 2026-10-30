<!-- markdownlint-disable-file -->
# RPI Plan: Authenticated live acceptance

## Task Metadata

* Task ID: authenticated-live-acceptance-2026-10-30
* Task slug: authenticated-live-acceptance
* Plan date: 2026-10-30
* Planning status: Ready; original critique Revise, direct dispositions complete
* Phase details: .copilot-tracking/details/2026-10-30/authenticated-live-acceptance-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/authenticated-live-acceptance-plan-critique.md

## Executive Summary

Executed both actual sites using the supplied test identity. The 19-row matrix
records one source-test-coverage criterion proven and eighteen unmet/blocked.
Only the resident public shell was reachable. No product fixes/access changes.
Independent Review executed Complete, outcome Not accepted. Original evidence
committed locally as 2e07c2ad; complete gate attempted and blocked by topic/main
lineage. No push. RV-003 blocks reuse of the runner until a
separate safety correction; no fix or second Review belongs to this task.

### What You May Not Know

Employee Entra authentication, roster binding and resident showcase enrolment
are separate. The documented roster initializer edits private SQL mappings and
restarts services; it is excluded. A denied journey is evidence of an unmet
acceptance gate, not permission to repair private data. Source/local synthetic
checks cannot substitute for observed live behavior.

### Unresolved Decisions or Blockers

Employee flow selects passkey and offers no password alternative; resident
login returns 401. Employee roster binding and deployment parity are unknown.
Actual full WCAG/Fluent adoption is not presumed from shell geometry.

## Sources

* .copilot-tracking/research/2026-10-30/authenticated-live-acceptance-research.md:
  completed focused research, C1-C8 and W1-W4.
* GitHub issue bodies #550, #551, #552 retrieved 2026-10-30: exact 19 criteria.
* src/api/checks/chat_widget_browser_check.py, map_fullscreen_browser_check.py,
  case_view_ux_browser_check.py: existing selector and measurement prior art.

## User Decisions and Requirements

* Run research, plan, implement and one independent Review with dated artifacts.
* Test employee https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io
  and resident https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io.
* Use the supplied AadiK test identity. Read ~/.ama-test-user only inside
  automation; never print, log, screenshot or commit its contents.
* MFA is excluded by Conditional Access; do not modify that policy.
* Missing roster binding must be reported; no private-data or role edits.
* Commit locally using Refs #550, Refs #551, Refs #552 only; do not push.
* Do not delete Azure resources or broaden acceptance into remediation.

## Goals

Obtain reproducible, secret-safe actual live evidence, with no inferred passes
for blocked, partial or unmeasured compound criteria.

## Scope and Non-Goals

In scope: sign-in, read-only authorized UI/API observations, bottom-right chat,
keyboard sending and selector, labels/sources/consent, expanded-map filters,
case icons/density/disclosure/tabs and 1280/390/320 CSS px observations.
Non-goals: product changes, deployments, roster/private-dataset reads or writes,
role changes, operational approvals, remote publication and issue closure.

## Functional Requirements

* Reach each site using its actual supported sign-in flow, without synthetic
  cookies or stored credential artifacts. Record denied authentication separately
  from a missing roster binding or empty queue.
* For #550 exercise both launchers, persistent multi-turn scrolling, pinned
  composer, Enter/Shift+Enter/send, employee skills, disabled controls and reasons,
  actual AI/rules labels and collapsed sources, consent before requests, rat
  fallback and actual loading/errors. Same-origin asset hashes support shared
  provenance but do not prove deployed backend or full source revision parity.
* For #551 compare expanded selection, marker/population changes and restored
  header state; keyboard and textual selection; narrow geometry; cite existing
  browser test coverage without claiming a local fixture run as live proof.
* For #552 inspect labeled presentation icons and byte provenance where
  accessible, step heights, actual blocker summary plus keyboard/touch disclosure,
  and tablist/panel ancestry and scrolling. Without a trusted deployed before
  baseline, absolute density is evidence, not proof of comparative improvement.

## Non-Functional Requirements

* Chromium actual browser version and UTC timestamps recorded.
* Screenshots only after checking no password input or auth-provider page is
  present; mask identity/account and home/case private details or crop solely
  public widget chrome. Prefer sanitized structured geometry to private captures.
* No Playwright tracing, HAR, raw network/console dumps, storage-state exports,
  authentication URL queries, tokens, cookies, identity IDs or private records.
* Catch expected probe failures into explicit safe evidence classifications;
  never print exception strings that may embed credentials or URLs.
* Missing auth is not proof of missing binding. Use authorized /api/me only to
  derive a binding boolean, never retain identity payloads.
* Use an owned external ephemeral browser directory, mode 0700, with tracing,
  video, HAR and downloads disabled. Close contexts/browser in finally; retain
  no profiles, crash reports, storage exports or raw responses in evidence.
  Existing /tmp/mv runtime is permitted: no actual caller temporary-path ban
  exists. Browser ephemeral profile cleanup is not historical evidence deletion.
* Loading 200ms threshold requires a measured observation, not a slow response
  alone; do not fabricate network replies. Optional browser-local request delay
  or abort must be labeled fault injection, never a natural backend failure.
* No native screen reader is available; DOM semantics alone cannot establish
  actual announcements. Report that limitation.
* Start a sanitized resident request-class observer before navigation; record
  assistant request ordering against record-use consent, not payloads. Normal
  portal session/view reads are separate from assistant data use. Server-only
  data-use ordering remains unproven unless applicable evidence resolves it.
* Compare actual styles with reduced motion emulated and reset; explicitly
  record error behavior observed naturally or by labeled browser-only abort,
  otherwise not observed. Record map aria-pressed plus visible Selected text.
* For 552-05 map native semantics, focus, non-colour states, reflow, token and
  motion observations to baseline scope. Unchecked contrast/zoom/AT and
  incomplete Fluent adoption prevent a blanket pass.
* For 550-01 split each live launcher/popup from shared-component use. Matching
  asset hashes or appearance alone are insufficient; require served call-site
  provenance showing both instantiate the shared implementation, or mark unmet.

## Acceptance Criteria

* AC-01: every exact issue criterion is present, with proven or unmet outcome,
  evidence IDs, partial observations and missing proof.
* AC-02: actual supplied-identity sign-in attempted safely on both sites.
* AC-03: authorized feature checks executed where access permits; inaccessible
  journeys clearly classified, without permission escalation.
* AC-04: dated original RPI evidence and one independent post-implementation
  Review retained, then a local Refs-only commit. No push.

## Test Ownership and Change Budget

* Owner: primary acceptance executor; no production test removals or edits.
* Exact removals: none. Maximum additions: one reusable acceptance script plus
  dated structured evidence/screenshots and canonical RPI artifacts.
* Canonical targets: tracking script and acceptance matrix/changes artifact.
* Generated targets: sanitized JSON and narrowly cropped/masked PNGs under
  .copilot-tracking/changes/2026-10-30/authenticated-live-acceptance/.
* Semantic proof: live observed behavior. Regression provenance: existing source
  browser checks, explicitly not rerun or live acceptance unless executed.
* Validation: Python syntax, evidence completeness/link/diff checks, independent
  Review. After local candidate commit, attempt complete local RPI gate in a new
  external directory; report prerequisites/failures honestly. No publication.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Execute actual access and feature acceptance

Dependencies: finalized plan critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Secret-safe login and authorized access classification

Record per-site outcome, binding evidence where authorized and safe captures.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Exercise accessible chat, expanded map and case view

Depends on P01-T01 per surface. Preserve blocked criteria rather than bypassing.

<!-- rpi:phase id=P02 -->
### [x] P02: Reconcile evidence, independent Review and local commit

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Complete all 19 criterion decisions and evidence hygiene

Record observed, partial, blocked and not-run distinctions.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Independent Review and local persistence

One independent Review; do not fix routed findings or repeat Review. Resolve
authenticated GitHub account and local noreply email before commit. Commit
original evidence with Refs only. Attempt complete local gate externally.

## Dependencies

* Existing /tmp/mv Python Playwright, Chromium and outbound HTTPS.
* Supplied local secret file and actual deployed access/enrolment.
* Independent critique and Review; neither grants human acceptance.

## Critique Disposition

Original one-pass critique verdict: Revise. No second critique.

| Finding | Disposition | Exact resolving evidence |
| --- | --- | --- |
| PC-001 | Partly rejected / partly applied | No temporary-path prohibition exists in parent/user instructions; preserve /tmp/mv. Non-Functional Requirements now require owned ephemeral profile containment and cleanup; implementation must record booleans. |
| PC-002 | Applied directly | Added reduced-motion comparison, explicit error/no-error disposition, map Selected text and scoped baseline mapping/unmet rules. |
| PC-003 | Applied directly | Added before-navigation sanitized observer, assistant versus portal boundary and backend visibility limitation. |
| PC-004 | Applied directly | Added served call-site proof requirement; matching assets/appearance alone cannot pass shared use. |

## Follow-Up Items

* RV-003: later tracking-runner implementation must isolate public capture in a
  fresh unauthenticated context and fail closed before text/images. Highest
  priority before reuse; current 401/public crops were safe. No repair here.
* Employee supported password sign-in is blocked by observed passkey route;
  owner/identity operator must validate access, then binding can be inspected.
* Resident test credentials returned 401; resident operator must confirm intended
  showcase enrolment. No private-data edits authorized.
* RV-001/002: later evidence research/execution must collect blocked authenticated
  criteria with exact script/runtime and uniquely hashed per-run outputs.
  No remediation, retroactive provenance edits or issue closure inferred.
* Full gate lineage blocker: candidate does not descend from current main
  63422cdf9fd477dd8892a27ac8b11487bc3a2429. No unauthorized integration/rebase;
  any later publication needs owner-directed integration and fresh exact-head
  gate/assessment. Metadata closeout is a second local commit because the first
  original-evidence candidate had to exist before the gate attempt.

## Handoff

P01/P02 complete as an honest bounded investigation and local evidence
persistence. Live/product acceptance blocked; 1 source-coverage criterion proven,
18 unmet. One independent Review executed Complete, outcome Not accepted;
original findings remain routed, not repaired. Gate attempted, no valid receipt.
Implementation owns .copilot-tracking/changes/2026-10-30/authenticated-live-acceptance-changes.md.
