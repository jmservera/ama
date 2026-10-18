<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 87 appointment commitment controls

## Metadata

* Continuation execution: F8/P01-T02 and P03 complete; existing source changes
  remain authorized and preserved. Parent owns the one original Review.

* Task ID: 87; slug: issue-87-appointment-controls; date: 2026-10-18.
* Plan: .copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md.
* Evidence: matching research artifact and its current-code lane; initial source
  and base 99056cae7bc679d2ace3e42c75f28577cfce8887.
* Current source candidate: 22c98267. Final implementation validation ran on that
  exact source tree immediately before the commit, not on inherited base behavior.
* Current status: Implement complete, P01-P03; F8 explicit record-only supplied
  human closure and final changed-source local/SQL/browser/image gates evidenced.
* Original Review: Complete / Not accepted, RV-001 through RV-007. Execution
  completion is not correctness acceptance. No second Review or closure claimed.
* Human live policy/authority approvals remain unavailable, not fabricated.

## Phase Index

| Phase | Intent | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Domain commitments and investigation | Complete; source-authorized human closure/reset recorded | P01-T01, P01-T02 |
| P02 | API and existing workbench | Complete; separate confirmed manual home-case closure | P02-T01 |
| P03 | Validation and handoff evidence | Complete; final local/SQL/browser/image receipts reconciled | P03-T01, P03-T02 |

## Current implementation evidence

All P01-P03 markers are checked. Final changed-source evidence: core323 (264
passed, 59 existing skips), API/web85 (84 passed, 1 existing skip), actual owned
SQL61 (61 passed, no skips), configured core/API lint/format/mypy and JS syntax,
actual local Chromium and rebuilt installed-wheel hardened responsive image.
The changes record owns exact commands, failure corrections and cleanup evidence.

F8 reuses the existing appointment-control operation and current manager/contract
authority. The supplied human same-case closure requires source/version/reason,
explicit confirmation and a full-case optimistic version; actor/time and
controlled-event history are server-recorded. Existing case `closed` and the
outcome boundary commit atomically; prior events/config/consumed IDs and human
investigation remain, as do outstanding updates/remedies and other case fields.
Existing reopening semantics are unchanged. Final actual SQL tests execute
competing closure/event writes in both winning orders, rollback, committed
acknowledgement/retry and replay after authorized reopening. The manual browser
checks refusal without checkbox, cancel/accept confirmation and retained update.
The later original Review completed on source22c98267 and found two High/five
Medium defects. Its source-grounded counterexamples supersede any inferred
acceptance from these positive execution receipts. Corrections route separately
under the matching correction-routing receipt; no source correction or second
Review occurs in this completed original loop.

<!-- rpi:phase id=P01 -->
## P01: Domain commitments and human investigation

Context: research C5-C7 shows narrow current procurement/SQL seams but no explicit
appointment agreement. Preserve all capacity guards and measure consent.
Likely targets: core procurement, resident authority, Store advance, SQL dependency
validation and event/audit helpers only as required. No new scheduler.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Appointment records, authority and guarded readers

Implement an explicit appointment offer tied to actual order/home/package/measure
scope/date/period. Use separate resident-confirmation source/channel/time and
authorized staff-confirmation provenance, plus current #90 committed capacity.
Appointment-specific representative authority must enumerate permitted appointment
scope/home/person/validity and not reinterpret existing works/attendance authority.

Derive current state server-side on reads and consequential writes. Unknown legacy
Booked cannot satisfy Appointed, completion or advance. Retain its historical
record without invented confirmations. Date/option/bundle/scope changes cannot
reuse affected resident agreement. Capacity-only changes invalidate affected
capacity evidence, not unrelated resident decisions; authority revocation applies
only to dependent confirmations. Preserve unrelated work orders/measures/updates.

Offer captures household constraints, options, pause/deferral, necessary provider
instructions and named existing resident-update owner contract. No diagnosing
free-text in provider view. Bundles require explicit resident agreement and
scope-bound competence source, never capacity inference. Urgent hazard service
remains independent even if routine works gates refuse.

Validate direct/domain/API writers and advance/completion against missing each
confirmation, wrong home/order/scope/period, expired/revoked representative,
changed capacity and source, sibling isolation, legacy Booked and household
pause. Completion evidence: tests and exact change receipt, no live approval.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Outcome and human-investigation lifecycle

Depends P01-T01. Source semantics C2-C4 authorize default five, strict >, confirmed
verified resident no-access during the same underlying home case only; no generic
No access inference or substitution of a threshold-created investigation case.
Record each event reference, actor, cause owner, verification source and appointment
commitment snapshot. Configuration is explicit/versioned and defaults provisional,
not operational approval. Deduplicate retries independently of configuration
version and reject changed payload reuse.

Use existing underlying home case identity and explicit active/closed evidence,
not a work order, appointment or threshold-created investigation task. Since no
closure writer exists, add the minimal record-only supplied human closure action
required by C2-C4 using existing current staff/manager authorization, optimistic
version, exact home-case identity, explicit human evidence source/reason and
actor/time. Atomically record closure/count boundary and preserve consumed IDs.
Never infer closure from task/order/remedy state. This records a supplied human
decision, not agent approval of readiness, technical acceptance, legal/financial
settlement or operational policy. Preserve outstanding #88 updates/remedies and
#102 event/audit contracts. Unverified source/lifecycle evidence stays fail-closed.

| Underlying case state / action | Count effect |
| --- | --- |
| Existing active case, no investigation yet | Eligible events 1-5 accumulate; sixth creates one owned human task at default five. |
| Investigation task disposition, order/appointment completion, pause, update or remedy closure | No reset and no implicit case closure. |
| Explicit authorized human closure of that same underlying case | Reset active count only; retain events, configuration, closure provenance and consumed IDs. |
| Reopen or retry after closure | Reopen alone does not reset; old event IDs never count again. Only new verified events in an evidenced active case may accumulate. |
| Closed/inactive or unknown lifecycle | No eligible count; no inferred reopening or approval. |

The supplied closure is an explicit manual choice with confirmation, separate
from investigation disposition, labelled underlying home-case closure. No general
closure workflow, new threshold/approval chain, backdating or fabricated evidence.
Existing reopening semantics remain unchanged.

Investigation records human checks of confirmation, notice, attendance, adjustment/
accessibility arrangements, contact history and relevant circumstances as evidence
or explicit Unknown, plus corrective action and next resident update. No diagnosis
or automated cause classification. Repeated evaluation never duplicates tasks.
Provider no-show/cancellation/reschedule/unknown/unconfirmed events never qualify.

Record preference-breach and abortive-visit facts independently with cause/owner.
One visit may carry both facts; event-reference dedup prevents duplicate counts.
Project separate cause/owner totals and reporting threshold Unknown; no invented
meeting workflow or consequence and no implied resident no-access.

Preserve resident update/remedy records and active response/chase contracts.
Reuse current optimistic concurrency and commit-time dependency revalidation.
Audit failure before commit rolls back; post-COMMIT response failure reports
committed truth and idempotent retry cannot duplicate outcome/task/confirmation.

Validate counts 4/5/6, changed config, strict boundaries, duplicate/conflicting
refs, inactive/reset/history, exclusions, provider isolation and unchanged hazard
response. Add actual SQL stale/racing writer and commit-boundary coverage,
including concurrent underlying-case closure versus event and replay after closure.
Test preference breach without no-access, provider-caused abortive visit, overlap,
duplicate retry and reload with authorized cause/owner projection and no spurious
resident eligible increment.

<!-- rpi:phase id=P02 -->
## P02: Authorized API and existing workbench

Depends P01. Current source C8 identifies server routes and ops.js. Before editing
load web-design-guidelines and redesign-existing-projects, fetch complete current
rules, read Fluent2/WCAG/plain-language standards. No public-page aesthetics.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Routes, projections and controls

Extend existing authorized procurement surface, rejecting provider/unknown/
revoked actors for staff actions. Protect direct HTTP from forged status, actor
or source claims. Keep provider view to assigned scope and necessary instructions.
Add native labelled controls for offer/household options/pause/manual confirmation,
explicit representative authority, owned outcomes and investigation disposition
(never implied underlying case closure/reset). Show separate preference-breach/
abortive cause/owner counts and Unknown reporting threshold.
Display derived Offer/Unknown/Committed plus missing/stale evidence in words.
Keep safe contact and human approval boundaries visible; never send messages.

Actual local Playwright must exercise keyboard flow, missing confirmations,
unknown and denied paths, valid commitment, manual route and responsive
320/390/1280 layouts/reduced motion with no overflow. Source review uses refreshed
web rules with file:line findings. This is engineering, not WCAG certification.

<!-- rpi:phase id=P03 -->
## P03: Validation, documentation and handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: Local and durable validation

Depends P01/P02. Use existing venv if available; install src distributions only
when imports/dependencies are missing; no uv or PYTHONPATH=mvp. Read project
configured ruff/format/mypy targets rather than inventing a repository build.
Run focused core/API procurement and new appointment semantics, affected resident/
hazard/finance/quality/event guards and JS syntax. Record exact commands and
counts, existing skips, failures fixed and residual baseline issues honestly.
Explicitly include plan AC8 semantic coverage for preference-breach/abortive facts.

Then run an actual uniquely named task-owned loopback MSSQL instance, reuse
existing environment contract and temporary fixture databases. Prove competing
confirmation/outcome writers, source/authority/scope invalidation and audit/recovery/
post-COMMIT behavior. Inspect resource ownership first; stop/remove only exact
owned container after use and do not leave idle memory-heavy SQL resources.

Build API Dockerfile with src context. Run exact owned image as configured nonroot
user using read-only filesystem, no-new-privileges, dropped capabilities and
explicit temporary writable data/state, no cloud credentials or real private data.
Verify responsive actual application and installed source boundary. Local browser
must use synthetic stock and prohibit external contacts.

No correctness pass if required SQL/browser/image gates are unexecuted or failed;
source limitations cannot be hidden by broad catch/defaults.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Documentation, reconciliation and Review handoff

Depends P03-T01. Update directly related component READMEs and existing resident
journey synthesis, knowledge index and append-only log; no memory edit or new
policy. Distinguish source-backed exercise rule from operational unknowns.

Maintain plan checkboxes and this status table from actual completed evidence.
Changes record must capture source/base context, actual commands/results,
amendments/divergences, AC mapping, touched files, human limitations and resources
stopped. No invented results. Do not perform original Review or self-accept.

Parent then refreshes web rules and dispatches exactly one independent original
Review over the actual full diff. Freeze that artifact and its verdict. Defects
route to distinct correction receipt, never edit the original verdict or run a
second Review. Normal push/PR only if correctness gate passes; branch main
advancement is a blocker for integration without explicit authorization.
