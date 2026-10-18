<!-- markdownlint-disable-file -->
# RPI Plan: Issue 87 appointment commitment controls

## Task Metadata

* Task ID: 87; slug: issue-87-appointment-controls; parent: 81.
* Plan date: 2026-10-18.
* Base/initial source: 99056cae7bc679d2ace3e42c75f28577cfce8887.
* Current source candidate: 22c98267, committed after final implementation checks;
  subsequent lifecycle-only commits do not change the assessed source.
* Branch: feat/appointment-commitment-controls-87; target: main.
* Lifecycle status: Research/Plan/Implement/one original Review executed.
  P01-P03 execution complete; original Review Complete / Not accepted.
  One critique Complete/Revise, both findings dispositioned.
* Details: .copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-18/issue-87-appointment-controls-plan-critique.md.

## Executive Summary

Extend current controlled work orders with explicit appointment offers, separate
recorded human confirmations and a server-derived commitment. Historical Booked
entries remain unverified. Preserve committed-capacity/consent/authority controls
and record household options, necessary adjustments and a named update owner.
Missed access creates only an owned human investigation after the sixth eligible
event under provisional default five, with auditable configuration and closure.
This describes implemented intent, not accepted correctness: the original Review
found RV-001 through RV-007 (two High, five Medium). Completed markers and positive
validation receipts do not establish a conformant or live-ready result.

### What You May Not Know

Existing capacity commits one home/work order per package period, not a crew or
weekly visit slot. This change must not allocate extra capacity or infer competence.
Works consent is not appointment agreement. Provider failures do not count against
residents. A positive synthetic result is not live scheduling or policy approval.
The coordinator delegates source implementation and preserves exactly one original
Review; defects require a separate correction receipt, not a second Review.

### Unresolved Decisions or Blockers

Correctness acceptance and normal push/PR are blocked by seven original-Review
defects: response serialization truth, role-sensitive privacy, configuration
lowering, bundle evidence validation, withdrawn-order status, readable selected
date/period and manual draft protection. F8 closure direction was supported.
Final SQL/browser/image checks ran but did not cover these counterexamples.
Corrections route separately; original verdict stays unchanged.

## User Decisions and Requirements

* Execute Research -> Plan plus one critique -> Implement -> one original Review;
  commit actual dated artifacts, normal push/PR if correctness gate passes.
* Meet issue #87 AC exactly; use FR-048/FR-031/AC-062/AC-065 and
  BRD FR-046/RULE-006/007/AC-088; parent #81, dependency #90/#384 is merged.
* Keep #88/#85/#91/#102/#101/#117 existing contracts and do not import #92/#389.
* No bundled delay to urgent safety; no real sending, booking, instruction,
  allocation, private datasets, spend or invented legal/financial approval.
* Appointment-specific representative authority is explicit and bounded; works
  decisions remain separate. Confirmation binds actual home/scope/order/period/
  current committed capacity; client status cannot confer commitment.
* Count only confirmed verified resident no-access in active case; strict greater
  than configurable default five; deduplicate retries/events/config versions.
  Human closure alone resets active counter while preserving event history.
* Preserve current quota/delegation/coverage/period/source checks and selective
  invalidation. Household provider view contains necessary instructions, not
  diagnoses; reuse #88 update/remedy ownership without silent clearing.
* Validate local-first, actual owned loopback MSSQL concurrency/recovery, source
  Docker/nonroot hardened run, actual local browser/keyboard/reflow/denials.
* One adverse Review is immutable; route corrections separately. No force push,
  rebase, main push or merge. Main advancement needs coordinator authorization.

## Goals

* Make offers and verified commitments unambiguous at every writer/reader.
* Keep resident choice, capacity and safety decisions independent and auditable.
* Deliver accessible existing-workbench controls and honest engineering evidence.

## Scope and Non-Goals

In scope: src domain/persistence dependencies, direct/API writers and readers,
existing operation UI, synthetic tests, component READMEs, existing resident journey
synthesis/index and append-only knowledge log, dated RPI artifacts.

Non-goals: schedule optimization, crew/visit allocation, automated communication,
new consultation policy, operational ratification, legal interpretation, real
contacts, diagnoses, company facts, other issues or framework/visual redesign.

## Functional Requirements

* F1: explicit offer captures date/period, actual scope, options offered, household
  constraints/necessary adjustments, deferral/pause and named update owner. Preserve
  history and resident-service commitments; provider projection is minimal.
* F2: record resident or explicit bounded appointment-representative confirmation
  with human/source/channel/time provenance separately from authorized staff and
  committed contractor capacity evidence. Non-digital route is supported. Derive
  commitment on server; no client status assertion or legacy Booked may bypass it.
* F3: bind each confirmation to its dependencies; scope/date/capacity/authority
  changes invalidate only affected confirmations. Preserve unrelated decisions and
  evidence. Recheck current capacity, quota, delegation, coverage, time and source.
* F4: bundle requires explicit resident bundle agreement and scoped competence
  evidence, never inferred. Urgent hazard intake/response remains independent.
* F5: outcome causes distinguish verified resident no-access, provider failure,
  cancellation/reschedule and unknown. Count only actually confirmed appointments
  while the same underlying home case is active, including before any investigation
  exists. Event reference retries are idempotent;
  conflicting reuse is rejected. Repeated configuration versions cannot recount.
* F6: versioned configurable nonnegative integral threshold defaults provisionally
  to five; count > threshold creates only one owned human investigation per active
  case, referencing counted events and configuration. Human investigation records
  checks of confirmation, notice, attendance, adjustments/accessibility, contact
  history and relevant circumstances as evidence or explicit Unknown, corrective
  action and next update. Only explicit authorized human closure of that same
  underlying home case resets active count, not investigation task disposition,
  appointment/order completion, pause or remedy/update closure. Reopening alone
  does not reset or permit replay of consumed events. No sanction/refusal/delay.
* F7: breach/abortive counts retain cause/owner; reporting threshold stays Unknown
  until supplied. Explicit preference-breach and abortive-visit facts may overlap
  on one visit but deduplicate independently by event reference. Neither implies
  resident no-access. No new threshold or reporting policy is invented.
* F8: add the missing narrowly authorized record-only human home-case closure
  operation with explicit supplied source, reason, actor, case identity and
  optimistic version. Atomically record the human decision, existing underlying
  `closed` state and active-count boundary; preserve outcome/configuration/consumed
  IDs. No task/order/remedy transition may invoke it implicitly. It does not
  declare technical/financial/legal closure, accepted handover, fulfilled resident
  updates or operational permission.

## Non-Functional Requirements

* Domain and direct HTTP enforce authorization/validation, including unknown actors
  and provider denials; direct work-order completion/advance cannot bypass checks.
* Optimistic concurrency and SQL transaction-time dependency revalidation prevent
  stale appointment confirmation/advance and lost/duplicated outcomes or tasks.
* Pending audit failure cannot leave a committed unrecorded decision; after COMMIT
  recovery/response errors report truthful committed outcomes, no duplicate retry.
* Preserve installed-src package boundary and existing test/check names; no mvp.
* Fluent 2, WCAG baseline, plain language, native controls, visible non-colour
  state, manual paths and reduced motion. Fresh web rules before editing and Review.
* Test data is public tiny fixture/generated stock only; no live integrations.

## Acceptance Criteria

1. Missing any confirmation leaves an Offer/Unknown, never commitment; representative
   appointment authority must be explicit. Valid tri-party evidence permits the
   current scoped commitment; legacy Booked cannot appoint/complete/advance.
2. Bundles need agreement/competence; urgent safety intake/response does not wait
   on bundle, appointment, investigation, pause or no-access counter.
3. Household constraints, offered options, deferral/pause and named update owner
   persist/reload and display; provider sees only necessary instructions; unrelated
   resident measures/remedies/updates retain state.
4. Counts four/five do not investigate and sixth eligible event does under default
   five; configuration changes work without duplicate counting. Provider/cancel/
   reschedule/unknown/unconfirmed/inactive events are excluded. Named human closure
   closure of that same underlying home case resets active count only, history
   remains; task disposition never resets. No automatic consequence.
5. Direct domain/API bypass, stale scope/capacity/authority, representative expiry,
   retry/dedup, audit failure, concurrent writers and post-COMMIT outcomes are tested.
6. Actual local browser demonstrates offer versus commitment/Unknown, denials,
   keyboard/manual route and 320/390/1280 reflow; not a WCAG certification.
7. Actual loopback MSSQL and source-context/nonroot hardened image run succeed,
   or gaps remain explicitly unmet and correctness acceptance is withheld.
8. Preference breach without no-access, provider-caused abortive visit and overlap
   retain separate cause/owner counts across retry/reload and authorized projection.
   Reporting threshold stays Unknown; resident count remains unchanged unless its
   independent confirmed/verified definition holds.

## Implementation Context Record

* Research: .copilot-tracking/research/2026-10-18/issue-87-appointment-controls-research.md.
* Details and critique: paths in Task Metadata.
* Changes evidence: .copilot-tracking/changes/2026-10-18/issue-87-appointment-controls-changes.md.
* Original Review: .copilot-tracking/reviews/logs/2026-10-18/issue-87-appointment-controls-review.md.
* State: .copilot-tracking/rpi-sessions/2026-10-18/issue-87-appointment-controls-state.json.
* Continuation: authorized full bounded automatic loop; no extra issue work.

## Sources

Research C1-C10 and W1-W3, including delegated current-code lane. Existing
capacity/quality procurement tests, resident decisions, SQL revalidation and
operations UI are canonical seams, not evidence of already passing #87.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Scoped domain commitments and human investigation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement appointment records, authority and guarded readers

Separate appointment-specific authority, capture offers/confirmations/household
state, dependency-derived status and current capacity/resident/safety gates at all
work-order/advance surfaces. Details P01-T01.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement outcomes, versioned threshold and human lifecycle

Cause-aware idempotent event history, owned investigation, human closure/reset and
truthful durable writer behavior. Details P01-T02.

<!-- rpi:phase id=P02 -->
### [x] P02: API and existing workbench

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Wire authorized routes, projections and accessible controls

Load relevant skills/rules first; show server-derived states, constraints/options/
pause/owner and human actions. No automatic sends. Details P02-T01.

<!-- rpi:phase id=P03 -->
### [x] P03: Evidence, compatibility and handoff

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute local regression, actual SQL, browser and container gates

Targeted semantics plus retained neighbor regressions, configured formatting/
lint/mypy/JS checks, owned SQL races/recovery, hardened installed-source image and
actual local UI. Details P03-T01.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Reconcile documentation and artifacts for one Review

Update existing synthesis/index/log and component guides. Record exact commands,
counts/skips/failures, source/base, current limitations and AC evidence. Details
P03-T02. One independent original Review follows implementation; no self-pass.

## Dependencies

* #90/#384 merged committed capacity is retained; #88 commitments, #85 hazard,
  #91 quality, #102 events, #101 coordinator and #117 rescans already in base.
* P01-T02 uses P01-T01 provenance; P02-T01 uses P01 APIs; P03 uses P01/P02.
* Current web source must be retrieved before web edits, refreshed before Review.

## Test Ownership and Change Budget

* Canonical behavior tests belong in existing core procurement/resident and API
  procurement suites or one appointment-focused module per component when clearer.
* Exact removals: none. Update old positive Booked fixtures to supply explicit
  agreement; do not remove retained capacity/authority/consent assertions.
* Maximum additions: two focused test modules (one core, one API), one dedicated
  browser check if existing check cannot be cleanly extended. No generated fixture
  dumps, snapshots or package-internal tests. No arbitrary test-count target.
* Semantic coverage: each AC boundary, exclusion and dependency matrix above;
  regression coverage: existing #90 and affected resident/hazard/finance/quality/
  event gates. Use installed packages, tests outside packages.
* Generated validation assets stay out of source; compact exact receipts enter
  changes. Never present inherited historical receipts as freshly executed.

## Critique Disposition

One final-candidate critique Complete, verdict Revise, frozen at the declared path.

| Finding | Owner and disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High | Parent resolved directly | F5/F6, AC4/5 and details P01-T02 state table bind actual same underlying case, count before investigation, prohibit implied resets, include human checks and SQL closure/event/replay coverage. Research interpretation corrected. |
| PC-002 Medium | Parent resolved directly | F7, AC8 and details P01-T02/P02-T01/P03-T01 explicitly record/project separate breach/abortive facts, cause/owner, overlap and retry/reload assertions; reporting threshold Unknown. |

No significant divergent user decision remains. No second critique is authorized.

## Follow-Up Items

* RV-001 through RV-007 route to a distinct later implementation receipt,
  .copilot-tracking/changes/2026-10-18/issue-87-appointment-controls-correction-routing.md.
  They are outside completed P01-P03 execution, not accepted closure or new active
  tasks inside this original loop. Coordinator owns delegation/final-head judgment.
* Live policy/authority/real evidence and existing UX acceptance remain human-owned.

## Handoff

P01-P03 implementation is complete. F8 records only supplied human same-home-case
closure, with current authority, explicit evidence, optimistic version, atomic
count boundary and preserved histories/updates/remedies. Final changed-source
evidence: core323 (59 skips), API/web85 (1 skip), actual owned MSSQL61 (0 skips),
configured static checks, actual manual closure/browser confirmation/reflow and
rebuilt hardened installed-wheel image including HTTP human closure. Exact
commands, results and stopped resources are in the changes record. Parent owns
the original independent Review result: Complete / Not accepted on source
22c98267ae6da365d6a2d9fceed7113c8f4578ea. Separate correction routing is recorded;
no second Review, self-Pass or remote delivery is authorized by passing tests.
