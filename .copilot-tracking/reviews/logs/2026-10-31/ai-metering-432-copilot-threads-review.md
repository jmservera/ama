---
title: AI metering Copilot threads Review
description: One independent post-implementation source Review for PR 602
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Opening Review State

Task 432-copilot-threads / ai-metering-432-copilot-threads, 2026-10-31.
Review scope: completed P01-T01..T03 and P02-T01 before publication.
Five W1-W5 threads, C1-C7 research, ready plan/details, one preserved critique
with PC-001..004 applied, implementation changes and component validation
form the reviewed boundary. Publication P02-T03 remains pending.

All dated artifacts use the stable ai-metering-432-copilot-threads slug under
.copilot-tracking/research, plans, details, changes and reviews.
Core 1638 tests / 206 opt-in skips; API 1443 / 320 opt-in skips; each component
Ruff/check-format/mypy pass. No full-local-gate receipt, CI result, human/
Finance approval or whole-issue acceptance is implied.

Review is read-only except this one record. Compare source/test/doc diff against
the five requirements, transaction/cohort/as-of invariants and critique
dispositions. Initial blockers: none. Execution and outcome pending independent
reviewer assessment.

## Scope and Evidence

* Task ID: 432-copilot-threads / ai-metering-432-copilot-threads.
* Review date: 2026-10-31.
* Assessment count: Exactly one independent post-implementation RPI Review,
  performed directly with no nested agents, source corrections or second Review.
* Scope: Completed P01-T01, P01-T02, P01-T03 and P02-T01, not the entire
  publication phase, issue #432, operational readiness or human acceptance.
* Branch: feat/ai-metering-432; PR #602 is OPEN against main.
* Assessed snapshot: Uncommitted working-tree diff from HEAD
  736f20d82b64b383f13a8a6cb6291c8a7c743d35. Thirteen tracked files changed,
  634 insertions / 31 deletions; five matching research/planning/changes inputs
  are untracked. No candidate implementation commit or publication is assessed.
* Tracked diff fingerprint: SHA-256 of `git diff --binary` is
  d53b870b619d2149e7cc6a224b547e56d442249a5035fccd58217d51ffe00447,
  unchanged before and after focused reviewer validation. This is a snapshot
  identifier, not a signed gate receipt or exact-head publication assessment.
* Acceptance basis: The five actual PR comment bodies, W1-W5 / C1-C7 research,
  current plan/details, PC-001..004 dispositions and implementation/validation
  evidence. Read-only gh GraphQL inspection confirmed comments 4431875217,
  4431875235, 4431875253, 4431875268 and 4431875281 remain unresolved.
* Authoritative task artifacts:
  .copilot-tracking/research/2026-10-31/ai-metering-432-copilot-threads-research.md;
  .copilot-tracking/plans/2026-10-31/ai-metering-432-copilot-threads-plan.md;
  .copilot-tracking/details/2026-10-31/ai-metering-432-copilot-threads-phase-details.md;
  .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-copilot-threads-plan-critique.md;
  .copilot-tracking/changes/2026-10-31/ai-metering-432-copilot-threads-changes.md.
* Read boundary: Actual source/test/documentation diff plus surrounding
  consumption, AI request, assistant authorization/revision/transaction,
  completion and legacy repair paths. Required case-study documents, reference
  index/memory and housing-association primer supplied context, not financial
  or legal-currentness evidence.
* Write boundary: Only this canonical record. Existing source, task artifacts,
  original adverse reviews, private data and remote PR state were not edited.
  Focused constructed tests used project-local, self-cleaning fixtures and
  loopback HTTP; no paid provider, schema migration, UI or deployment action.

### Task-artifact fingerprints

| Input | SHA-256 |
| --- | --- |
| Research | 1b58b7de25c6a277ba1bc094997c1ea268707aa7fc02d6f8542090600852b49f |
| Plan | 48c3799b2ee00d59b4baebda3985583e3db1a66f754ead0a31086705e2699861 |
| Details | 0d59da465e7b5932d43c684135f3682d0a70634ae551f6e1cb782af52599c7be |
| Critique | d58bbce773f012e3b0281633642efacea9e5bab46fb0c6fe86954cd575c8c351 |
| Changes | 4cc05ef6f9911366f96d2e62b144f6810a456b872a220a9f166b95ec4fdd5fd7 |

## Execution Status

* Execution status: Complete.
* Review execution evidence: All four supplied completed task markers, all five
  threads, current critique dispositions, actual diff, surrounding invariants,
  related documentation and validation were compared. Focused reviewer tests
  passed. This does not mark unperformed P02-T03 complete or mutate the plan.
* Implementation execution boundary: P01 and P02-T01 Complete; P02-T02 receives
  this one result; P02-T03 remains pending.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 / W1-W2 | CURRENT preservation and shared report_period | Reconciled | Matches actual source and composed document/HTTP tests. |
| P01-T02 / W3 | Root-associated orphan rejection | Reconciled | Reject-only intent before authoritative legacy save; immutable original-link recovery remains separate. |
| P01-T02 / W4-W5 | Atomic ineligible repair and sticky unresolved withdrawal | Reconciled | One metering snapshot precedes normal writes; DispatchHeld fallback is metering-only and rejects only. |
| P01-T03 | Tests and related documentation | Reconciled | Exactly four core and four API methods added; zero removed/renamed methods. Existing fault matrix and HTTP test retained/extended. |
| P02-T01 | Focused/full suites and configured static checks | Reconciled | Changes record reports final component runs; reviewer independently ran only focused checks. |
| P02-T02 / P02-T03 | Independent Review then publication | Reconciled | Opening/plan/handoff correctly marked pending before this Review; publication and unresolved remote threads still pending. |
| Follow-Up Items | Historical/resident joins, OD-51/Finance and held-out evidence | Reconciled, open | Explicitly outside active completion/acceptance scope; routed separately below. |

## Completed Work Assessment

| Related marker / thread | Source and tests | Assessment |
| --- | --- | --- |
| P01-T01 / W1 | src/core/src/zava_forward/core/ai.py:207-217; src/api/tests/test_ai_consumption_api.py:test_document_calls_preserve_shared_call_and_depth_limits | Conformant. look_at creates a document context only without CURRENT. _request replaces actual configuration but preserves root/attempt/capability/prompt/depth/retry. The real loopback provider sees one shared-root call, the next attempt is held, depth two is held, and a standalone call receives a separate root. CURRENT is restored on success and held paths. |
| P01-T01 / W2 | src/core/src/zava_forward/core/ai_consumption.py:77-81; src/api/src/zava_forward/api/server.py:516-537; existing test_manager_report_local_http_and_bad_period | Conformant. All three timestamps require explicit timezone; start must precede exclusive end and as_of must be at/after end. Validation runs before SQL availability branching. Actual HTTP SQL, JSON and unavailable-schema cases return 400 for malformed/naive/reversed/too-early/blank/repeated/unknown inputs and retain Unknown unavailable reporting for valid periods. |
| P01-T02 / W3 | src/core/src/zava_forward/core/ai_consumption.py:681-719, 742-792, 908-923; src/core/src/zava_forward/core/ai_tasks.py:375-377; src/core/src/zava_forward/core/store.py:941-943; core orphan test and existing API SQL/JSON legacy/priority matrix | Conformant. Both callers supply original root. Only unlinked reject creates review-orphan plus intent; accept/edit remain denied. Domain rejection and financial disposition persist without inventing a legacy output. Pending intent and missing orphan linkage are unioned per output in the original call cohort; completed reject remains incomplete until matching original output repair. Wrong-root repair fails; repair/replay does not reapply edits, save or audit. Legacy domain and consumption stores are explicitly not cross-store atomic. |
| P01-T02 / W4 | src/core/src/zava_forward/core/ai_consumption.py:723-792; src/core/src/zava_forward/core/assistants.py:1060-1085; test_failed_metered_provider_pending_task_can_be_rejected_without_redispatch and core immutable-output test | Conformant. A real loopback provider 500 leaves a metered pending task without output. Authorized rejection creates one eligible=False output and reject disposition in the authoritative transaction; task becomes rejected, revision advances once, domain state stays unchanged and execute cannot redispatch. Existing output eligibility/root/output is never rewritten; original-root conflicts fail. |
| P01-T02 / W5 | src/core/src/zava_forward/core/assistants.py:1060-1085; src/core/src/zava_forward/core/ai_consumption.py:800-818, 888-923, 941; capacity, sticky/cohort and exact-boundary tests | Conformant. Only DispatchHeld from metering permits reject fallback. It appends a closed root/output/action/time/reason/authoritative-task-revision marker and persists unresolved task/history metadata with withdrawal. Read recovery/restart/later ordinary reviews never clear it. In-cohort markers at/before as_of suppress stale acceptance, dominate equal-time acceptance and count distinct unresolved outputs once; pre-withdrawal and unrelated cohorts are preserved. Billing/TCA/quality-qualified ratios remain Unknown while reconciliation is unresolved. |
| P01-T03 | src/core/README.md; src/api/README.md; docs/reference/resources/ai-tokenomics.md; docs/reference/README.md; docs/reference/log.md | Conformant. Documentation distinguishes rejection from acceptance, legacy recovery from assistant atomicity, immutable eligibility from latest review, and source controls from financial/human acceptance. Index updated and log append-only; no case-study or memory changes. |
| P02-T01 | Changes Validation; two existing canonical test modules | Conformant for recorded engineering scope. Focused 30 core / 13 API pass independently; supplied final full/static results are accurately qualified, not rerun or represented as reviewer-observed full runs. |

### Cross-cutting invariants

* One-snapshot staging: Consumption.review reads once, checks matching original
  association and pending intent, and selects disposition before appending any
  normal output/review events. It does not call output and rescan after insert.
  At exactly the existing-record scan limit it writes both normal events, not a
  leaked output plus fallback marker. Above the limit it writes only fallback
  financial metadata alongside authoritative withdrawal. The production scan
  limit is unchanged; eventual over-limit reads still hold, not truncate.
* SQL atomicity: Assistants.transaction uses BEGIN IMMEDIATE locally,
  SERIALIZABLE for MSSQL, commits only on success and rolls back escaping
  failures. Metering writes now precede task update/history in that transaction.
  Output, disposition and fallback insertion failures are covered by existing
  new tests. Additional reviewer probes prove task-update and human-history
  failures roll back both normal and held metering, task state/revision and
  human history. No arbitrary SQL error is swallowed.
* Authorization/revision: _view authorizes current staff capability/case scope
  before changes; exact task revision is checked before either metering path.
  Unauthorized/stale rejection writes nothing. Existing source verification,
  epoch/release/state/output validation for acceptance is unchanged. Additional
  probes on a valid verified ready task prove accept/edit-accept propagate
  DispatchHeld and commit nothing; reject fallback cannot widen acceptance.
* Event/schema compatibility: Existing ai-consumption-v1 event field sets are
  unchanged. review-orphan and review-unresolved are new closed event kinds
  stored in the existing append-only table; no DDL or mutable repair is added.
  Constructed old-shape events and new kinds coexist in passing tests.
  No mixed-version deployed-reader compatibility or live rollout is claimed.
* As-of/cohort/deduplication: Reviews choose highest financial revision at/before
  cutoff. Unresolved markers use their own cutoff/root cohort rather than a
  guessed financial revision or random event ordering. The union of pending,
  orphan and unresolved output IDs prevents double-counting; repeated reject
  markers remain sticky. Call-time roots and exclusive bounds remain unchanged.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Trigger / decision | Reconciliation and assessment |
| --- | --- | --- | --- |
| P01-T02 / PC-001 | Added immutable original-root orphan association | Critique identified missing cohort attribution for reviews without output | Plan Critique Disposition, details and changes match code; direct clarification preserves reject-only user direction and existing v1 field shapes. |
| P01-T02 / PC-002 | Staged normal link/review before writes; metering-only hold catch | Critique identified partial insertion on a second bounded scan | One-snapshot code, exact-capacity and fault regressions satisfy disposition; no relaxed limit or arbitrary exception catch. |
| P01-T02 / PC-003 | Defined closed sticky unresolved marker and cohort/as-of precedence | Critique identified guessed-revision, equal-time and stale-economic hazards | Source, tests, details and documentation reconciled; no clearing operation or additional financial authority introduced. |
| P01-T03 / PC-004 | Allocated four API/four core additions; extended existing matrix/HTTP test | Critique identified negative-test and eight-method-budget risk | Actual diff meets cap with no removals/renames; named tests and assertions cover all four critique contracts. |
| P02-T01 | Pip editable setup, lint corrections and final fixture refinement | Observed missing imports and initial configured lint failures, recorded in changes | Final full results reported after refinements and independent focused results now pass; no material scope/intent divergence. |

## Critique and Material Revision Assessment

* The original critique remains Complete / Revise with 3 High and 1 Medium
  findings. This Review does not rewrite it or earlier adverse reviews.
* PC-001..004 are recorded as applied in the current plan. Independent source/
  test comparison supports each disposition, including original-root recovery,
  one-snapshot atomicity, temporal/cohort stickiness and bounded negative tests.
* Current plan/details readiness is Ready after compatible direct dispositions.
  The refinements resolve implementation contracts within confirmed direction;
  no significant/divergent decision or fresh user approval is needed.
* The preserved sequence is critique, reconciled plan/details, implementation,
  final validation, then this independent Review. No evidence of premature
  dependent-work resumption or unrecorded material revision was found.
* The changes record's no-divergence claim is supported for this snapshot.
  No second critique or Review is requested, and review conclusions are not
  substituted for hosted approval or original planning outcomes.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Historical and independent resident financial joins | Explicitly excluded broader attribution project, not one of W1-W5 | Digital/metering owner to commission a distinct attribution work item | Open, RV-002; not a new active P01 task or a source defect. |
| OD-51, Finance authority, applicable prices/actual billing and authorized held-out measurements | Synthetic source correction cannot establish external evidence or human authority; paid calls prohibited here | Finance and named approval owners to supply/approve evidence before any separately authorized measurement | Open, RV-001; distinct follow-up, not whole-issue acceptance or permission to spend. |

## Findings

No implementation defect, significant decision gap or material missing evidence
was found in the supplied completed-source boundary. The following complete
finding set records known non-blocking residual work, not newly introduced bugs
or failures of the five source corrections.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Financial and human acceptance evidence remains unestablished

* Related scope: Plan Follow-Up Items; external financial/quality acceptance,
  outside completed P01/P02-T01.
* Evidence: Changes Review Readiness and Remaining Work;
  docs/reference/resources/ai-tokenomics.md source-only engineering/gap matrix;
  Consumption.report coverage_gaps and synthetic constructed price/billing/
  quality inputs. No actual applicable price/bill reconciliation, OD-51
  authority or authorized held-out measurement is supplied.
* Impact: Engineering passes cannot demonstrate real cost per accepted output,
  approved quality floors, live financial reconciliation or human acceptance.
  Treating this result as whole #432 delivery would overstate evidence.
* Destination: Distinct financial-validation follow-up owned by Finance and
  named human approval owners, not current rpi-implement.
* Smallest useful next action: Obtain applicable price/billing, OD-51 and
  quality/measurement approval evidence; commission a separately authorized
  held-out exercise only after permission and safeguards exist. Record missing
  inputs as Unknown meanwhile. No paid execution or approval is authorized here.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Complete historical and resident attribution remains outside this ledger cohort

* Related scope: Plan Follow-Up Items; coverage beyond the five PR threads.
* Evidence: Plan Scope and Non-Goals / Follow-Up Items; changes remaining work;
  src/core/src/zava_forward/core/ai_consumption.py report coverage_gaps;
  docs/reference/resources/ai-tokenomics.md qualification of separate resident
  reservations without financial cohort joins.
* Impact: A repaired current orphan join or recorded-ledger-only result does
  not establish exhaustive historical/resident per-call/outcome accounting.
  Current acceptance and cost denominators cannot be generalized to those paths.
* Destination: Distinct historical/resident-attribution follow-up owned by the
  Digital/metering owner; not added to this source-correction plan.
* Smallest useful next action: Scope and assign a separate evidence/engineering
  work item defining historical/resident join provenance and completeness
  criteria, without accessing private datasets or claiming these joins exist.

## Defects

* None found within completed P01-T01..T03/P02-T01.
* No current rpi-implement, rpi-plan or rpi-research defect/evidence handoff is
  needed. RV-001/RV-002 remain explicitly outside active accepted scope.

## Routed Findings

| Finding | Destination | Owner / next action | Reason for route |
| --- | --- | --- | --- |
| RV-001, Medium | Distinct financial-validation follow-up | Finance / named human approval owners: supply evidence and separately authorize measurement | Known external/human residual, not a source defect. |
| RV-002, Medium | Distinct historical/resident-attribution follow-up | Digital/metering owner: assign separate provenance/completeness work item | Explicitly excluded broader attribution scope. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* RV-001 and RV-002 remain open and do not invalidate conformance of this
  bounded source result. No whole-issue closure is recommended.
* Publication is remaining original P02-T03 work, not a new finding or added
  implementation task. Thread replies/resolution must use actual evidence.

## Blockers and Remaining Work

* Review blockers: None.
* Remaining active work: Parent records the one P02-T02 result without changing
  its original verdict, then performs P02-T03 privacy-safe commit, non-force
  push, five evidence-backed replies/resolutions and remote verification.
* Hosted CI/check results and human merge decision were not assessed. All five
  threads remain unresolved at this prepublication snapshot. The owner explicitly
  selected CI; no complete-local-gate wait or receipt is required by this Review.
* No receipt is fabricated, protection changed, hosted/human acceptance claimed,
  or prior adverse evidence erased. A future commit/base/source change is not
  automatically covered by this precommit snapshot verdict.

## Validation Evidence

Reviewer commands used
/home/azureuser/.copilot/session-state/0368cebe-6336-46a8-b819-d330fc26490a/files/venv/bin/python.
Tests use editable installed components and constructed data only.

| Command / evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Core unittest discover('tests', pattern='test_ai_consumption.py') with tempfile.tempdir patched to project cwd | Existing canonical core module | Passed, reviewer observed | 30 tests, 5.152s, no skips; no source-test edits. |
| API `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_ai_consumption_api -q` | Existing canonical API module | Passed, reviewer observed | 13 tests, 14.940s, no skips; actual loopback HTTP and SQL/JSON constructed fixtures. |
| In-memory reviewer fault probes using existing ConsumptionApi fixtures | Normal/held withdrawal rollback and valid acceptance | Passed, reviewer observed | Four combinations: task-update or human-history SQL failure after normal/held staged metering; all task/detail/ledger state unchanged. Valid verified ready accept/edit-accept during hold both raise DispatchHeld and write nothing. No files/test methods added. |
| `git diff --check` | Tracked candidate diff | Passed, reviewer observed | No whitespace errors. |
| Diff-added/removed test method inspection | Two canonical test modules | Passed, reviewer observed | Exactly eight additions, zero removals/renames. |
| Core `python -m unittest discover -s tests -q` | Complete component suite | Passed, supplied changes evidence | 1638 tests, 478.208s, 206 existing opt-in skips; not rerun by reviewer. |
| API `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` | Complete component suite | Passed, supplied changes evidence | 1443 tests, 666.362s, 320 existing opt-in skips; not rerun by reviewer. |
| Each component `python -m ruff check .`; `python -m ruff format --check .`; `python -m mypy` | Configured component checks | Passed, supplied changes evidence | Core 117 formatted files / 170 typed sources; API 66 / 124. Not rerun; configured exclusions do not imply universal typing/format coverage. |
| Markdown / link and actual diff review | Related README/synthesis/index/log changes | Passed, bounded reviewer inspection | New text reconciled to source; changed existing targets retained; no repository-wide documentation build exists. |
| Complete local RPI gate | Whole publication receipt | Skipped, explicitly user-selected CI direction | No local-gate receipt or simulated status claimed. |
| Hosted CI / exact committed remote candidate / five resolved threads | P02-T03 and hosted gates | Pending, unassessed | Source candidate is precommit; remote threads remain unresolved. |
| Opt-in live SQL/browser/scanner/large-data tests; actual Azure/provider/Finance/human acceptance | External/full acceptance | Skipped or unavailable | Existing skips retained; no live services, paid calls, private data, deployment or human authority exercised. |

## Outcome

* Outcome: Conformant.
* Outcome rationale: All five source corrections and four critique dispositions
  are supported by actual source/test/doc inspection and focused negative
  execution. No acceptance bypass, eligibility mutation, partial-write fallback,
  authorization/revision regression or stale unresolved economics was found.
* Scope qualification: Conformant only for completed P01-T01..T03/P02-T01 at the
  recorded precommit boundary. Publication and broader financial/human/history/
  resident acceptance remain pending; this is not whole #432 completion.
* Severity summary: 0 Critical / 0 High / 2 Medium known non-blocking residual
  findings / 0 Low; zero implementation defects.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No bounded-source correction required. |
| Decision gap or invalid assumption | None | Critique refinements preserve confirmed direction. |
| Material evidence gap within assessed source boundary | None | Supplied artifacts plus focused tests support the bounded verdict. |
| Non-blocking residual work | Distinct financial-validation and historical/resident-attribution follow-ups | Finance/human approval owners for RV-001; Digital/metering owner for RV-002. |
| Original remaining publication work | P02-T03, parent continuation | Preserve this result, commit/push non-force, reply/resolve five threads and verify remote/CI without merge or issue-closure claims. |

* Execution status: Complete.
* Outcome: Conformant for the bounded precommit source tasks.
* Validation coverage: Independently observed 43 focused tests, four SQL
  rollback combinations and held accept/edit denial; supplied full/static
  results qualified above.
* Blockers: None for this Review; external/human acceptance remains unavailable.

## Compared Artifact Links

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/ai-metering-432-copilot-threads-research.md](.copilot-tracking/research/2026-10-31/ai-metering-432-copilot-threads-research.md) | W1-W5 and C1-C7. |
| [.copilot-tracking/plans/2026-10-31/ai-metering-432-copilot-threads-plan.md](.copilot-tracking/plans/2026-10-31/ai-metering-432-copilot-threads-plan.md) | Current scope, completion and dispositions. |
| [.copilot-tracking/details/2026-10-31/ai-metering-432-copilot-threads-phase-details.md](.copilot-tracking/details/2026-10-31/ai-metering-432-copilot-threads-phase-details.md) | Transaction/report/test contracts. |
| [.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-copilot-threads-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-copilot-threads-plan-critique.md) | Original Complete / Revise preserved. |
| [.copilot-tracking/changes/2026-10-31/ai-metering-432-copilot-threads-changes.md](.copilot-tracking/changes/2026-10-31/ai-metering-432-copilot-threads-changes.md) | Implementation and supplied validation. |
| [.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-copilot-threads-review.md](.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-copilot-threads-review.md) | This sole Review. |
| [src/core/src/zava_forward/core/ai.py](src/core/src/zava_forward/core/ai.py) | Document/current request trace. |
| [src/core/src/zava_forward/core/ai_consumption.py](src/core/src/zava_forward/core/ai_consumption.py) | Immutable ledger and report trace. |
| [src/core/src/zava_forward/core/ai_tasks.py](src/core/src/zava_forward/core/ai_tasks.py) | Legacy review trace. |
| [src/core/src/zava_forward/core/store.py](src/core/src/zava_forward/core/store.py) | Priority review and repair trace. |
| [src/core/src/zava_forward/core/assistants.py](src/core/src/zava_forward/core/assistants.py) | Authoritative assistant transaction trace. |
| [src/api/src/zava_forward/api/server.py](src/api/src/zava_forward/api/server.py) | Pre-availability API validation. |
| [src/core/tests/test_ai_consumption.py](src/core/tests/test_ai_consumption.py) | Core constructed regressions. |
| [src/api/tests/test_ai_consumption_api.py](src/api/tests/test_ai_consumption_api.py) | Composed HTTP/SQL/JSON regressions. |
| [src/core/README.md](src/core/README.md) | Ledger/review contract. |
| [src/api/README.md](src/api/README.md) | Reporting contract. |
| [docs/reference/resources/ai-tokenomics.md](docs/reference/resources/ai-tokenomics.md) | Source result and financial evidence gaps. |
| [docs/reference/README.md](docs/reference/README.md) | Knowledge-base index. |
| [docs/reference/log.md](docs/reference/log.md) | Append-only documentation record. |
| [docs/case_study_48_original.md](docs/case_study_48_original.md) | Unchanged original context. |
| [docs/case_study_48_addendum.md](docs/case_study_48_addendum.md) | Qualified project/human authority context. |
| [docs/reference/memory.md](docs/reference/memory.md) | Owner context, not evidence. |
| [docs/reference/research/sector/housing-association-primer.md](docs/reference/research/sector/housing-association-primer.md) | Sector context, not company evidence. |

## Next Steps

Parent continues original P02-T03 using this one Review result; no further
Review or source correction is requested. Retain Refs #432 and preserve original
adverse outcomes. Publish only with the owner-selected CI path and honest remote/
hosted status; leave merge to the owner. Assign RV-001/RV-002 as distinct future
work without widening this accepted source scope or claiming whole-issue closure.
