<!-- markdownlint-disable-file -->
# RPI Phase Details: Proper Warm Architecture and PoC

## Metadata

* Task ID: 4aaf9ee3-da69-4ebb-812a-edccc5637af7
* Task slug: retrofit-application-poc
* Related plan: .copilot-tracking/plans/2026-10-07/retrofit-application-poc-plan.md
* Evidence: research C3-C10/W1-W3 and independent contract lane.

## Phase Index

| ID | Name | Status |
| --- | --- | --- |
| P01 | Domain API | Complete; 39 tests and five simulator fixtures pass |
| P02 | UI | Complete; real browser interaction and mobile reflow pass |
| P03 | Architecture/container documentation | Complete; created resources inventoried |
| P04 | Validation/publication/review | Complete; PR24 published, historical Review found RV-001 |
| P05 | Owner-directed RV-001 implementation | Complete; regression and actual rebuilt container pass; no repeat Review |

## P05: Accepted Quality Replacement

After handed_over, recording new accepted quality evidence invalidates separate
handover acceptance and returns the current stage to quality_accepted. Historical
evidence/events, current invoice, resident-update ownership and unrelated facts
survive. New independent handover evidence and explicit advance are required.
Test completed count 1 -> 0 -> 1 and original-intent replay without duplicate
events. Rebuild the owned container without resetting its existing volume.

<!-- rpi:phase id=P01 -->
## P01: Controlled Domain API

One process with SQLite prepared statements, explicit domain commands and
HTTP/static boundary. No external consequence. No generic record-patch endpoint.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Persistent Cases, Commands, Audit and Assistant

* Targets: apps/proper-warm/src/{seed,domain,store,assistant,server}.mjs; tests; package.json.
* Dependencies: research/critique gate.
* Schema: cases(id, version, JSON), events(case ID, sequence, actor, action, timestamp, payload), idempotency(case/key, actor, request hash, stored response). Transaction wraps validation, mutation, audit and saved response. Same key/different intent conflicts.
* Seed at least nine constructed cases: EX-HOME-104 technical gap, 208 resident, 317 capacity, 422 quality, 531 hazard hold, 646 conflict, 752 finance, 863 handoff and 900 complete journey. Do not claim pack import or actual company records.
* Identity: x-demo-role allowlist is only local impersonation simulation. Provide roles programme_manager, data_owner, assessor, coordinator, resident_officer, contract_manager, safety_officer, quality_reviewer, finance, viewer, contractor. Role gates use fixed mapping; never body-supplied owner authority.
* Actions: resolve_conflict, submit_assessment, approve_design, record_decision, commit_capacity, record_installation, record_quality, match_invoice, record_grant, send_handoff, receive_handoff, accept_handoff, return_handoff, set_update, record_appointment, acknowledge_referral, advance.
* Lifecycle: candidate -> assessed -> designed -> resident_ready -> scheduled -> installed -> quality_accepted -> handed_over. A workflow "advance" checks stage-specific and continuing safety/resident/evidence requirements; no arbitrary stage assignment.
* Human synthetic decisions require reason and source reference. Update commitments and receiving/chase owner must remain visible. Declined/withdrawn discretionary decisions block release; shared building does not share consent.
* Immutable linked hazard holds in PoC; acknowledge_referral records exercise receipt only, never clears hold/clocks.
* Grant ledger separate opportunity/awarded/claimed/received values with ordered evidence and no external submission/payment.
* Assistant returns {mode:"simulator",status:"draft",citations:[...],findings:[...],draft:string,prohibitedActions:[...]}; only reads approved case fields. Disabled/failure mode returns explicit error with manual owner, no generated claim of completion. No live model mandatory.
* API: GET /health, /metrics, /api/config, /api/cases, /api/cases/:id, /api/portfolio, /api/export; POST /api/cases/:id/commands and /api/cases/:id/assistant.
* GET list supports workflow/query filters, returns {cases,scope,asOf}; detail returns case fields plus events and allowedActions for selected role. Config returns roles, workflow IDs/names, lifecycle, synthetic banner. Portfolio uses same filters.
* POST command: {action,expectedVersion,idempotencyKey,payload}. Response {case,replayed}. Errors {error:{code,message,details,owner},requestId}; use 400/403/404/409/422/503 correctly. Assistant uses {mode:"draft"|"disabled"|"failure"} for reproducible failure demonstration.
* Validate: domain gates, roles, duplicate intents, stale versions, rollback, no-access 5/6 strict threshold, quote handling, hazard untouched, handoff continuity, file-backed restart, HTTP origin/body limit and assistant evaluations. Tests use isolated temporary DBs.
* Unresolved: production identity and approved authority matrix outside PoC.

#### Frozen Synthetic Authority and Payload Contract (PC-001/004)

Each payload accepts exactly the listed fields plus `reason` and `source`
(both nonempty strings); unknown fields rejected. Server owns version, owner,
tasks, audit timestamps and stages. Evidence references are constructed source
identifiers, never URLs fetched or files read. Every mutating authority is
exercise-only. `advance` is programme_manager only and never grants approval.

| Action | Role | Additional payload |
| --- | --- | --- |
| resolve_conflict | data_owner | value:string |
| submit_assessment | assessor | evidenceId:string |
| approve_assessment | coordinator | evidenceId:string |
| approve_design | coordinator | designVersion:positive integer |
| record_decision | resident_officer | decision:accepted/declined/withdrawn, measure:string, designVersion:integer |
| approve_package | finance | budgetApproved:boolean, fundingConfirmed:boolean, contractApproved:boolean |
| commit_capacity | contract_manager | slots:positive integer, packageVersion:integer |
| release_work | programme_manager | packageVersion:integer |
| record_installation | contractor | evidenceId:string, designVersion:integer |
| record_quality | quality_reviewer | outcome:accepted/returned, evidenceId:string, designVersion:integer |
| accept_handover | quality_reviewer | evidenceId:string |
| match_invoice | finance | matched:boolean |
| record_grant | finance | state:opportunity/awarded/claimed/received, amount:nonnegative number |
| send_handoff | current owner role | destination:role |
| receive_handoff | destination role | handoffId:string |
| accept_handoff | destination role | handoffId:string |
| return_handoff | destination role | handoffId:string |
| set_update | resident_officer | dueAt:ISO timestamp |
| record_appointment | resident_officer | appointmentId:string, confirmed:boolean, verified:boolean, outcome:resident_no_access/provider_no_show/cancelled/rescheduled/kept |
| acknowledge_referral | safety_officer | referralId:string |
| return_case | coordinator/quality_reviewer | target:assessed/installed |
| advance | programme_manager | none |

Role gate failure is 403 FORBIDDEN; invalid payload 400 INVALID_PAYLOAD; stale
version/replay-intent mismatch 409 VERSION_CONFLICT/IDEMPOTENCY_CONFLICT;
failed domain predicate 422 GATE_BLOCKED with owner and exact blockers.
`allowedActions` represents role authority, not satisfied domain predicates;
therefore the UI can demonstrate a visible rejected action.

| Edge | Required current predicates (in addition to no safety hold) | Gate owner |
| --- | --- | --- |
| candidate -> assessed | conflict resolved, assessment submitted AND separately approved | data_owner/coordinator |
| assessed -> designed | approved design version | coordinator |
| designed -> resident_ready | accepted measure decision against current design | resident_officer |
| resident_ready -> scheduled | current design/decision, approved budget/funding/contract, committed package-version capacity and explicit release | finance/contract_manager/programme_manager |
| scheduled -> installed | continuing release/decision validity, provider installation evidence current design | contractor |
| installed -> quality_accepted | independent current-design quality acceptance, no returned defect | quality_reviewer |
| quality_accepted -> handed_over | separate handover acceptance, invoice matched, resident-update commitment exists | quality_reviewer/finance/resident_officer |

Unknown never passes. Demo measure is one per home; all gates are applicable
to this constructed scheme (there is no silent not-applicable bypass).
Grant ledger is optional to handover; `claimed` means simulated submitted
amount only, NOT accepted, claimable or paid. PRD claimable/accepted/rejected
and multi-measure states explicitly deferred.

#### Validity and Recovery Contract (PC-002)

* Reject assessment/design replacement once dependent stage progressed:
  coordinator `return_case(target=assessed)` must first preserve history,
  clear design, decision, capacity, release, installation, quality and handover;
  retain assessment, Finance package approval, invoice/history and update owner.
* Withdrawal/decline at any stage is always recorded, revokes release and
  dependent acceptance, moves already-progressed case back to designed with
  explicit reassessment task. No resident choice can be rejected merely because
  work was scheduled; retain history and previous observations.
* Quality returned moves quality_accepted/handed_over back to installed,
  invalidates handover and creates reinspection task; reinspection requires
  new evidence. `return_case(target=installed)` is quality_reviewer only.
* Design-version checks on decision, install and quality prevent v1 approval
  covering v2. Unaffected evidence versions and resident-update commitment stay.
* No automated hazard hold release, no generic record patch, no case closure
  or no-access reset in this PoC.

#### Transaction and Replay Algorithm (PC-003/005)

* Validate envelope/role/action first; compute stable canonical hash of actor,
  case ID, action, expectedVersion and recursively key-sorted payload.
* Lookup case/key BEFORE new-command version check. Same actor/hash returns
  original committed response with replayed=true; other actor/intent conflicts.
* Stored snapshot may be older than latest case. UI retains request/key across
  ambiguous transport failure, retries same intent, then GETs current case.
* Fresh write: BEGIN IMMEDIATE, version check, domain mutation, case write,
  event insert, replay insert, COMMIT. Exception ROLLBACK, 503 STORE_UNAVAILABLE,
  no successful shape; structured log exposes failure without body/secrets.
* Seed-on-empty and schema/fixture marker in one transaction. Existing
  incompatible/unreadable store fails startup, never reseeds/resets.
* Inject failure after case write and before replay insert in isolated tests;
  reopen file, reconcile unchanged version/events/replay, then safe retry.
* `/health` probes database readiness and returns non-200 on unavailable
  store; process liveness alone is not a claim of writable readiness.

#### Cases and Config Shared Shapes (PC-004)

* Selected role header is x-demo-role for every API read/write; absent defaults
  viewer for reads only; commands require a role. Synthetic reads/export are
  intentionally unrestricted across roles, explicitly not field-level privacy.
* `case`: {id,homeId,buildingId,schemeId,workflow,stage,version,owner,
  blockers:[{code,message,owner}],evidence:[{id,kind,version,source}],
  facts:object,handoff:object|null,residentUpdate:object,tasks:array,
  appointments:array,allowedActions:string[],events:array}.
* Config: {roles:string[],workflows:[{id,label}],lifecycle:string[],
  commands:[{action,label,roles,fields:[{key,type,options?,default?}]}],banner}.
* Command response {case,replayed}; errors {error:{code,message,owner,details},
  requestId}. Draft {mode,status,citations,findings,draft,prohibitedActions}.
* Filters: workflow exact configured ID or empty/all; q case-insensitive substring
  over id/homeId/buildingId/owner; metrics use identical filters. Invalid workflow
  yields INVALID_FILTER, not default all. Case detail does not inherit list filter.
* Handoff IDs are generated by server. Only destination can receive/accept/return;
  acceptance requires received, return requires sent or received, all require
  matching active ID. Current owner changes only on accept, NOT send/receipt;
  resident-update owner does not transfer. Do not permit payload owner injection.

#### Scenario, Rule and Assistant Oracles (PC-006/007/008)

* Manifest version poc-1 includes all nine workflow IDs and exact safe endpoints/
  tests. EX-HOME-208 and 317 share building/package but have independent consent
  and hold/evidence state; no propagated approvals.
* No-access rule `exercise-no-access-v1`, threshold configuration default 5,
  immutable for process lifetime; active case never closed/reset by app.
  appointmentId unique per case even with another idempotency key. Only confirmed
  AND verified resident_no_access counts. First count >threshold creates one
  persistent resident_officer investigation task; higher counts do not duplicate.
  Consent remains unchanged; hazard referral remains available and unchanged.
* Assistant modes draft/disabled/failure. Draft source IDs validated against
  actual current case evidence. Unsupported citations fail explicitly.
  Disabled/failure creates a durable deduplicated manual-review task/event
  without advancing stage, approvals or external consequences.
* Evaluation fixtures include complete/gapped/conflicted/held cases and hostile
  source text. Assertions: citations resolve (100%), prohibited commands never
  generated/executed (0 violations), fields obey closed schema, no approval
  mutation, one owned fallback task, source/notes treated as inert text.
  Scores are simulator contract checks only, not model-quality comparisons.

<!-- rpi:phase id=P02 -->
## P02: Connected Workbench

<!-- rpi:task id=P02-T01 -->
### P02-T01: Accessible Workbench

* Targets public/index.html, styles.css, app.js only; no dependencies/CDNs/remote fonts.
* API contract above; command form chooses allowed action and posts version/idempotency. Expose source/reason and structured action payload fields or well-labelled JSON editor for advanced commands. Avoid optimistic successful UI until server commits.
* Aesthetic: restrained civic/industrial workbench, dark ink navigation, warm paper content, Clawpilot accent/theme variables and ochre exceptions; local serif title and readable native font fallbacks. Accessible contrast and reduced motion.
* Controls: role simulation labelled separately from workflow view; nine workflow filters/search/reset; denominator-aware cards; selected home details, lifecycle, owner/blockers, resident updates, evidence, handoffs, audit, assistant and actions.
* Metric clicks drill into exact contributing cohort; no fabricated throughput/value.
* Error visible with owner and recovery; keyboard/live regions; responsive stacking.
* Completion: integration/browser validation after backend exists, not merely screenshot.

<!-- rpi:phase id=P03 -->
## P03: Architecture and Container Runtime

<!-- rpi:task id=P03-T01 -->
### P03-T01: Architecture, Runtime and Inventory

* Targets Dockerfile/compose.yaml/.dockerignore/README and docs/architecture.
* Compose project proper-warm-poc: one app, Node 24 pinned image, loopback 127.0.0.1:3410, named data volume, non-root image, healthcheck; no broad mounts or privileged mode.
* Mermaid format selected by automatic parent for readable documentation; architecture preference records selection.
* Diagram separates actual local resources from proposed Azure: Entra, ACA domain API, SQL store, evidence authority Blob/SharePoint, managed identity, optional durable worker/Service Bus, Foundry bounded adapter and telemetry. Optional services justified, not mandatory service count.
* Describe protocol contracts, threat model, RBAC, failure/recovery, scale-out migration, RPO/RTO proposed/not met, cost formula and rollback.
* Resource ledger: exact actual names/port/image digest and inventory/status/cleanup. Explicitly none for Azure/M365. No secrets/account IDs in docs.
* Full rubric challenge: 20 rows evidence/limits, no fabricated live presentation or stakeholder score. Floors cannot be established; architecture remains PoC draft not capstone-ready.
* Update root/index/log links; original/addendum/memory unchanged unless materially necessary (not currently needed).
* PC-009: before creation inspect Compose project labels, container/network/volume
  names and port availability. Use session-scoped project `proper-warm-4aaf9ee3`
  if generic proper-warm-poc collides; never adopt/delete foreign resources.
  Record created/reused/planned separately. Tests use ignored app `.test-data`
  files, not operating-system temp directories; clean only known test files.
  Verify non-root named-volume write and restart consistency. No credentials
  in inventory; image digest and generated ignored data location included.

<!-- rpi:phase id=P04 -->
## P04: Verify, Publish and Review

<!-- rpi:task id=P04-T01 -->
### P04-T01: Semantic and Runtime Validation

* Dependencies P01/P02/P03.
* Run Node test suite, offline evaluation, Docker build, Compose up and health.
* Exercise happy journey and negative holds via isolated test DB/API; verify named-volume persistence with a synthetic case command and restart.
* Browser inspect filters, workflow views, command/draft/error/export and mobile sizing. Save screenshots to session files, not production sources.
* Measure 100 sequential case-list requests, p95 target <=250ms local only.
* Keep user-requested demonstrator container available; stop temporary helper processes.
* Completion gates: no failures in changed-code tests; disclose unsupported full-PRD surfaces.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Publication and Review Handoff

* Commit using authenticated GitHub noreply email and required trailers, push feature branch, use dedicated create_pull_request tool against main.
* Complete implementation with a reconciled Review handoff, not by requiring
  Review to complete its own predecessor. The automatic RPI parent then executes
  rpi-review once against plan/change evidence.
* Subsequent Review routes findings to later selected work, never reopens
  Implement/Review in this task, and offers the running-session follow-up checkpoint.
