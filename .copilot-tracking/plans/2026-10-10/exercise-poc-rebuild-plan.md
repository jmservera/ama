---
title: RPI Plan - Proper Warm Exercise PoC Rebuild
description: Connected exercise implementation against the accepted PRD
ms.date: 2026-10-10
---

## Task Metadata

* Task ID: exercise-poc-rebuild-2026-10-10
* Task slug: exercise-poc-rebuild
* Planning status: Local and owner-authorized Azure deployment implemented; full acceptance incomplete
* Phase details: .copilot-tracking/details/2026-10-10/exercise-poc-rebuild-phase-details.md
* Critique target: .copilot-tracking/reviews/plans/2026-10-10/exercise-poc-rebuild-plan-critique.md

## Executive Summary

Owner-directed restart: this is the next iteration of the existing Proper
Warm MVP within the whole AMA exercise, not a separate 18-case application.
Reuse the recovered 60,000-home register and 980-case programme baseline,
preserving existing history and provenance. Retain small fixtures as tests.
Real bounded AI must be enabled and demonstrated; GPT-4.1-mini summary
success is observed, Decision 1 authentication remains unresolved.
Earlier completed small-fixture markers and workload evidence do not accept
the generated-data deployment. P07 owns the corrected delivery boundary.

Rebuild the demonstration as a connected fictional-home journey, reusing the
existing Python workbench, durable SQL store and independently checked domain
controls. Add versioned assisted forms and a dedicated Decision 1 adapter,
separate application/claim/cash evidence, and make the approved exercise
assumptions visible in the UX and evidence report.

### What You May Not Know

The existing app already implements substantial resident, technical, quality,
procurement and finance controls; a wholesale rewrite would discard useful
coverage. Its current funding shortcut and template-based AI path do not
satisfy the new form and actual-inference requirements.
Exercise startup isolates the fictional seed and SQLite/local or
MSSQL/Blob storage. A shared inference guard will keep both scoring
and generation disabled until separately authorized. Legacy hazard release
does not represent authoritative external safety clearance.

The AMA Foundry account currently deploys only gpt-4.1-mini and gpt-4.1.
Read-only catalog metadata advertises Decision 1 version 1 GlobalStandard
eligibility, not a deployment or price quote.
Decision 1 activation and billable authorization remain blocked, not simulated
success. Neither local tests nor a working adapter satisfies live AI acceptance.

## Sources

* docs/prds/proper-warm-retrofit-programme-demonstrator.md: v0.12.0 accepted exercise baseline.
* docs/case_study_48_addendum.md: EXA-001 through EXA-016 and quantitative targets.
* .copilot-tracking/research/2026-10-10/system-one-decision-models-research.md: provider API evidence.
* mvp/README.md and mvp/properwarm_mvp/: existing reusable controls, storage and transport.
* .github/workflows/mvp-ci.yml: existing unit/API/SQL/image validation gates.

## User Decisions and Requirements

* The exercise is the whole AMA programme. Restart the existing MVP iteration
  using the same generated 60,000-home stock, not the isolated 18-case seed.
* Latest owner direction removes the prior USD450 budget constraint for this
  rebuild. Keep cost/usage telemetry and source/authority/token-bound controls;
  do not treat budget removal as permission for live resident or financial action.
* Synthetic state is disposable and can be regenerated/reloaded; use the
  existing snapshot first for comparability, not as an irreplaceable-data gate.
* Reuse and preserve the 980-case existing snapshot and retained SQL history;
  do not regenerate dates/identities or invent completed workflows for stock.
* Every new prototype, PoC and MVP must demonstrate real enabled bounded AI
  and realistic customer UX, with sources, uncertainty and human authority.

* Merge accepted PRD #57 and rebuild the PoC end to end.
* Apply System One where useful, especially extraction/selection and filling of retrofit subsidy forms; scoring never grants decision authority.
* Use grounded, explicitly fictional company assumptions, not invented company validation or further broad research.
* Keep the USD 450/month cap and four-week plan; real Foundry scoring and generation remain required.
* Demonstrate one connected home, source conflict/correction, resident choice, delivery, QA/handover and financial reconciliation with tribunal-defensible evidence.
* Owner now authorizes real Azure SQL, app and asset deployment. Use existing
  AMA resources and a separate fictional database/document container; preserve
  existing retrofit data. Subsequent owner direction explicitly requires
  actual AI enabled and demonstrated, with the USD450 cap retained.
* Activate bounded Decision1 proposals and GPT-4.1-mini drafting after
  deployment/access/pricing checks, with SQL-backed reservations surviving
  app restarts. Preserve source lineage, human approval and manual continuity.

## Goals

* Restore generated-data lineage and full-stock visibility alongside the
  existing programme, with an honest stock/programme/analytical denominator.

* Complete the accepted exercise journey with traceable human decisions.
* Provide safe optional assistance with manual continuity and exact source lineage.
* Publish reproducible checks and honest unmet acceptance gates.

## Scope and Non-Goals

Owner correction supersedes the private-generator exclusion in earlier
planning prose: privately reuse the existing generated geography and MVP
snapshot, preserving their privacy and provenance. Historical small-fixture
implementation is regression-only evidence, not the deployment baseline.

Non-production local and owner-authorized Azure implementation, wholly fictional fixtures, browser
workbench, existing durable stores, provider adapters and evidence generation
are in scope. No real resident data, external sending/submission/payment,
unrestricted spend, fake legal/professional approval or
production readiness claims are in scope.

The owner-authorized deployment adds Azure MSSQL/Blob exercise startup,
managed-identity access, immutable image/static assets, a separate low-cost
fictional database and evidence container, and HTTPS app deployment on the
existing Container Apps environment. Validate actual write/read/restart and
document bytes without migrating existing retrofit databases or activating AI.

## Functional Requirements

Retain FR-001 through FR-035 controls and cover their connected exercise path.
Implement FR-036 through FR-044 task registry, scoring envelopes, versioned
forms, candidate lineage, per-field human review, deterministic validation,
pack export and exact dependent invalidation. Preserve FR-045/046 measure
scope/choice isolation and strengthen where source inspection reveals gaps.

## Non-Functional Requirements

Use SQLite transactional durability locally and Azure SQL/Blob durability
for the deployed exercise. Enforce
service-side permission checks and no-self-approval, not UI-only restrictions.
Preserve existing tests and map the PRD performance, recovery, accessibility
and evaluation thresholds to executed evidence or explicit Not run/Blocked.
Never infer live model success from fake transports or agent labels.

## Acceptance Criteria

* Verify exactly 60,000 existing stock IDs and the 980-case programme baseline,
  with fingerprints, source dates and retained audit/history. No silent reseed.
* Full-stock browse/filter/count and programme workflows share explicit
  linkage or visible unknowns; no fabricated case history or consent.
* Real AI produces a useful source-bound output on generated programme data;
  failed Decision calls remain visible and cannot be labelled success.

* Same-home lifecycle can be exercised locally with separate identities, independent QA and separate finance events.
* Conflicting EPC candidates remain visible; manual correction and source changes preserve history and invalidate exactly dependent reviews.
* Form export reproduces field values, attachments, versions and review manifest; export never establishes submission, award, claim or cash.
* Model proposals cannot change source records, ranking, resident choice, safety or controlled approvals.
* Existing unit/API/SQL coverage passes; new tests use independent exact oracles.
* Browser journey, durability and declared runtime checks are recorded; live inference and human evaluation remain blocked unless actually authorized and executed.

## Implementation Context Record

PR #57 merged as 5a6ec60f885a3e207b6984a725870a48e0d4cf99 after current-head
validation and the rubric status passed. The unpublished rebuild branch now
starts at that merged main commit, with no duplicated squash ancestry.
The existing full MVP unittest suite passes before application changes.
Local implementation and engineering checks have run. Direct owner rebuild instruction authorizes implementation
after the planning gate; an automatic RPI session was not confirmed.
The bounded validation planner found no cohort forecast or compliant public
fixture; existing private-geography data is excluded. Existing offline AI and
browser smoke checks remain regression tests, not full acceptance evidence.
The connected fictional home reaches independent handover and financial
closure in tests. Later owner-directed implementation fixes financial
staleness/readiness/cumulative cash/rejected retry and adds explicit
handoff/update/hazard and shared liability contracts. Latest regression runs
370 tests, OK, with 26 live SQL skips; focused tests include 30 Decision and
20 connected workbench tests. Fresh browser run passes 25 finite checks,
including actual doubled body text, CSS zoom reflow, targets and palette contrast.
The image again passes non-root/read-only health startup. Separate exact
500-row/25-case Store probe passes. Two 1800-second workloads pass with no
failures, >=200 samples/op and p95 below thresholds: five-session core and
twenty-session 60000-home/600000-trace scale, both two writers. They schedule
five interactions/s (writes use two HTTP requests); separate Store import is
not the prescribed concurrent mixed core HTTP import.
P05/P06 remain unchecked because complete
role/workflow fixtures, exact prescribed workload/recovery/accessibility and
actual inference/human acceptance are unfinished. The complete inventory is
.copilot-tracking/changes/2026-10-10/exercise-poc-rebuild-acceptance.md.

Renewed owner continuation adds independently projected building/home/sibling
navigation and actual differing consent/design browser fixture. Eleven
controlled profile tasks safely refuse unsupported award recording;
resident commitment and sent/received/accepted/completed handoff journey
execute in the browser. Final headed Chrome run passes 53 finite checks,
including true native 400% zoom. Background batch interruption/retry and
document-byte restore with detected missing-event launch block pass.
Latest regression 374 tests, OK, 26 live SQL skips. All eleven profiles/six
templates/eight protected batch denials have focused permission evidence.
Exact five-HTTP-request/s scale and strict mixed core 500-row/25-case HTTP
workloads pass separately. Independent full seed/database/trace/document/audit
comparisons pass. Remaining initial cold-start/complete permissions and
scheduled recovery/human/live boundaries are not inferred from those results.
P05/P06 remain open for complete matrix and mandatory human/live gates.

Renewed owner continuation resumes P05-T01 with exact two-measure
resident scope/design/representative and accessible-service/redress fixtures.
Runtime writes remain within existing resident/technical APIs and their
authority boundaries. Preserve independent choices, historical answers and
service-versus-retrofit controls; fix only coupled defects exposed by these
fixtures. Validate focused tests before regression and publish on the same
unmerged topic branch. Live model and human evaluation gates remain blocked.

Exact resident/service fixtures now pass. Coupled fixes minimize contact
references without mutating stored decision history and repair shared nested
DOM child rendering. Full regression 377 tests, 26 live SQL skips; headed
browser 57 checks including actual complaint refusal/independent closure and
native zoom. Fresh 18-home cold startup measured separately; scale/cloud
startup remains unmeasured. P05/P06 stay open for remaining complete workflow,
return, permission, recovery, screen-reader and actual-model/human evidence.

Current P05-T01 continuation adds explicit return scopes: named technical
sign-offs and same-home form fields requiring re-review. Blank scope remains
a routing-only return, not guessed invalidation or approval. Use existing
sign-off return and form input-version dependency helpers; preserve sources,
resident choices, sibling and historical external receipts. Test exact
invalidation, atomic invalid-scope refusal and return-stage/version matrix.

Executed: all 36 earlier-stage dispositions, ten atomic invalid-scope shapes,
exact sign-off/form/financial ancestry scope, preserved source/choice/sibling/
cash and need-based form-scope projection. Real return browser/history passes.
Latest full regression 380 tests/26 live SQL skips, headed native-browser
60 checks. FR-010/AC-012 complete constructed disposition evidence; full
quality/procurement/milestone return invalidation remains an open P05 boundary.

Current P05-T01 continuation adds explicit same-home milestone re-review
scope. A stale milestone must block subsequent invoice acceptance/payment
status and financial closure, even after a historical accepted disposition.
Retain prior milestones, invoices and external-payment references; renew only
through existing independent evidence controls. Test exact stale-ref refusal
and unaffected milestone/invoice history, with no inferred payment execution.

This continuation is implemented: E27 paid/unpaid journeys and E28 native
browser scope refusal pass; 382-test regression and read-only container startup
pass. P05/P05-T01 stay unchecked: quality/procurement dependencies and the full
milestone-version matrix remain incomplete. P06 remains blocked on live/human
prerequisites; original Review is not rerun or regraded.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Establish reusable exercise and acceptance contracts

Dependencies: merge PRD and finish source assessment.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Freeze fictional fixture, journey and capability map

Assess current implementation versus the accepted PRD and define honest
implemented/unavailable boundaries before parallel implementation.

<!-- rpi:phase id=P02 -->
### [x] P02: Implement versioned source-bound forms

Dependencies: P01. Own forms domain and focused form tests; no provider, server
or UI writes.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add schema, candidate, review, validation and pack contracts

Implement approved synthetic funding/non-funding templates, exact dependency
invalidation, independent field review and export fidelity.

<!-- rpi:phase id=P03 -->
### [x] P03: Implement dedicated scoring and inference evidence

Dependencies: P01. Own provider/registry modules and focused provider tests;
no forms, server or UI writes.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add Decision 1 transport and validated proposal envelopes

Actual provider contract, explicit disabled/unavailable states, permitted
candidate IDs, finite normalized probabilities, abstention and identity/usage.

<!-- rpi:phase id=P04 -->
### [x] P04: Build fictional fixtures and deterministic forecast

Dependencies: P01. Own new exercise.py, forecast.py, test_exercise_forecast.py,
exercise manifest and independent forecast-oracle fixtures only.

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Freeze independent cohort and journey fixtures

Implement wholly fictional lead/sibling, 16-home cohort, six frozen scenarios,
separate install/QA capacity pools and scale-shaped generation. Include
as-of, versions, denominator, unknowns, coverage and exact independent oracles.
Describe eleven profile paths and nine workflows explicitly; do not grant
additional privileges simply to implement a perspective.

<!-- rpi:phase id=P05 -->
### [ ] P05: Connect journey, finance, browser and evidence

Dependencies: P02, P03 and P04.

<!-- rpi:task id=P05-T01 -->
#### [ ] P05-T01: Integrate local durable journey and usable workbench

Wire service authorization, same-home forms, application/claim records,
fictional fixture, forecast and UX with clear owner/blocker/next action.

<!-- rpi:phase id=P06 -->
### [ ] P06: Validate and publish

Dependencies: P05.

<!-- rpi:task id=P06-T01 -->
#### [ ] P06-T01: Execute acceptance evidence and publish implementation PR

Run integrated tests and local browser/runtime checks, reconcile requirements
and unresolved gates, one independent post-implementation review, publish.
Include the required five-session/two-writer workload, declared import/bulk
limits, 200 samples per reported interaction, 30-minute runs and the separate
60,000-home/600,000-event scale workload in the acceptance inventory. Perform
the feasible local checks; preserve Not run for unexecuted shapes/thresholds
instead of substituting existing timing tests. Preserve the exact restore,
restart, accessibility, 120-family AI and paired-effort acceptance gates.
Browser scripts cover eleven perspectives and nine workflows with service
rights unchanged, 320/390/1280px, keyboard/focus/status and chart tables;
record checks separately from screen-reader/human evidence. Stakeholder
aggregates below ten require complementary suppression, not exposure through
another total.

<!-- rpi:phase id=P07 -->
### [ ] P07: Restart the existing generated-data MVP iteration

Dependencies: existing P02/P03 domain controls; owner scope correction.
This is a later implementation amendment, not a repeat critique or Review.

<!-- rpi:task id=P07-T01 -->
#### [x] P07-T01: Recover and integrate generated stock and programme lineage

Recover 60,000 stock rows and the 980-case baseline without changing IDs,
dates or private source bytes. Verify retained SQL history and documents.
Provide durable full-stock storage, paging/filtering and explicit case linkage;
missing/ambiguous linkage remains unknown. Keep the 18-case seed as tests.
Executed: copied the retained Azure programme to properwarm-programme,
imported exactly 60,000 original stock rows and enriched 980 cases without
changing their prior fields/history. Original four-entry audit head retained
and verified. Source SHA-256s recorded; no private data committed.

<!-- rpi:task id=P07-T02 -->
#### [x] P07-T02: Demonstrate real AI and customer workflows on generated data

Reuse enhanced forms and source review controls on generated cases without
inventing approvals or source evidence. Resolve Decision provider access or
record the exact blocker while demonstrating successful bounded generation.
Validate useful matched/abstaining outputs, permissions and spending guards.
Executed generated-case EPC candidate proposal: real Decision1, validated,
source-bound and Not reviewed; actual citation-verified generative summary.
Optional confidence validation and explicit cap override retain task controls.
Actual browser source-provenance inspection passes. Calibration/paired value
remain separate incomplete PRD acceptance gates, not this smoke boundary.

<!-- rpi:task id=P07-T03 -->
#### [ ] P07-T03: Deploy and publish the corrected continuing MVP

Replace the app only after generated-data startup and regression pass;
verify stock/case counts, source fingerprints, live AI, SQL/Blob persistence,
browser UX and the exact deployment digest. Publish on existing draft PR #58.
Keep earlier Review Not accepted and remaining human/full-PRD gates explicit.

## Validation Ownership and Change Budget

* Primary owns integration/end-to-end/API/browser/runtime and result mapping.
* P02 owns semantic form tests; P03 owns provider shape/abstention/permissions tests; P04 owns exact independent forecast/fixture tests.
* Exact test removals: none. Existing regression expectations may change only for tightly coupled explicit behavior shifts, retaining or strengthening equivalent controls.
* Maximum additions: six test modules, four domain modules plus one provider registry, three independent fixture/manifest JSON files, one browser module and two local acceptance scripts; reuse existing modules otherwise. Changes/plan/review evidence are not runtime files.
* Canonical runtime targets: mvp/properwarm_mvp, mvp/web and exercise fixture contracts. Generated state and browser/test outputs stay in scratch/session paths, never private data in commits.
* Semantics: independent expected field/stale sets, forecast arrays and lifecycle trace; regression: all existing unit/API/SQL checks and image CI.
* Evidence: record exact commands, versions, conditions and observed results; no unexecuted acceptance claim.

## Dependencies

* PR #57 current-head CI and merge precede implementation.
* Actual Decision 1 deployment, processing/cost verification and authorized billable calls block live AI acceptance only.
* Human-adjudicated evaluation labels and real UX participants cannot be manufactured.

## Critique Disposition

One critique executed with Revise verdict. All five planner-owned corrections
below are incorporated; no second critique or invented clean regrade.

| Finding | Disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 | Resolved by plan amendment; primary owns implementation | P05: shared pre-transport authorization guard for all registered scoring/generative tasks; default no calls, injected denied-call matrix |
| PC-002 | Resolved by plan amendment; primary owns implementation | P05: exercise denies local hazard classification/closure/release, records supplied external authority/version/evidence references only; legacy API isolated |
| PC-003 | Resolved by plan amendment; primary owns implementation | P05: existing ai.py/ai_tasks.py retain response identity/usage/version/latency and explicit failed-provider vs available-template provenance |
| PC-004 | Resolved by plan amendment; P02 owns implementation | P02: actual deterministic text/CSV extraction from independent bytes, source hash/locator/parser, unsupported scan manual handling |
| PC-005 | Resolved by plan amendment; primary owns implementation | P05: explicit isolated fixture startup, compatible existing DB check, local evidence backend, inherited private seed/external backend rejection |

## Follow-Up Items

* None.

## Handoff

Changes target: .copilot-tracking/changes/2026-10-10/exercise-poc-rebuild-changes.md.
Local implementation handoff ready: P01 through P06, under the owner's direct
rebuild request. Full acceptance remains blocked by actual platform and human
evaluation prerequisites.
