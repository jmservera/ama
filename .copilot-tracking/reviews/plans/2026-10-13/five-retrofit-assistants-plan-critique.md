---
title: Five Retrofit Assistants Final-Candidate Plan Critique
ms.date: 2026-10-13
---

## Metadata

* Task ID: five-retrofit-assistants-2026-10-13
* Critique date: 2026-10-13
* Plan: .copilot-tracking/plans/2026-10-13/five-retrofit-assistants-plan.md
* Phase details: .copilot-tracking/details/2026-10-13/five-retrofit-assistants-phase-details.md
* Critique execution status: Complete
* Assessment count: One bounded independent final-candidate critique.
* Output boundary: Only this critique artifact is written. The parent owns dispositions and implementation.

## Inputs and Criterion Boundary

* Confirmed direction: implement all five reactive/proactive assistants in the existing MVP, update PRD/ADR, resolve ordinary ambiguities autonomously and finish. Continue consolidated PR #68, existing services and generated stock/programme lineage; do not create another estate or autonomous authority.
* Candidate inputs: the plan and phase details above, and .copilot-tracking/research/2026-10-13/five-retrofit-assistants-research.md, including C1-C15 and its five-capability table.
* Requirements evidence: docs/prds/zava-forward-retrofit-programme-demonstrator.md, particularly FR-003/005/028/036/043/044, bounded orchestration, CON-009 and AC-054/057; docs/adrs/0002-pilot-readiness-architecture.md, Exercise Applicability and durable-store/projection decisions; docs/case_study_48_addendum.md, Subsequent Application Exercise Builds; docs/case_study_48_original.md.
* Implementation evidence: mvp/zavaforward_mvp/sqlstore.py:270-381; mvp/zavaforward_mvp/mssqlstore.py:1-190; mvp/zavaforward_mvp/ai_tasks.py:18-86 and 153-249; mvp/zavaforward_mvp/ai.py:1-110; mvp/zavaforward_mvp/projection.py:1-101; mvp/zavaforward_mvp/server.py:60-116.
* Operator evidence: infra/README.md:112-145, the dated existing exercise handover. Knowledge context: docs/reference/README.md, docs/reference/memory.md and docs/reference/research/sector/housing-association-primer.md.
* Dependency boundary: P01-T01 establishes the contracts used by P01-T02; P01-T03 validates the implemented contracts before delivery. The parent may overlap documentation and source work but must not publish before these dependencies and evidence gates are satisfied.
* Assessment boundary: plan credibility and concrete acceptance obligations, not implementation acceptance, exploitable-vulnerability assessment, fresh legal research or current Azure inventory. No source tests, image builds, provider calls or platform operations were executed.
* Direction reconciliation: research's earlier unanswered intake does not override the later explicit autonomous implementation direction. That procedural issue is resolved. Effective spending limits and safe changed-runtime evidence are still execution gates, not grounds to ask the same intake questions again.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner five-assistant/reactive/proactive direction; C1/C10 | Partial | Correct shared-runtime scope; each contract's executable trigger/source/reviewer/output acceptance needs a matrix, PC-008. |
| P01-T01; FR-036; ADR 0001/0002 | Covered | Preserves proposal status and distinguishes shared MVP realization from deferred worker topology. Contract detail follows PC-008. |
| P01-T02; C7/C14; durable claim/deduplication | Partial | SQL ownership is stated, but lease fencing, uncertain outcomes and attempt semantics are unspecified, PC-001. |
| P01-T02; bounded provider/scan costs | Partial | No effective limits, durable reservations or accounting behavior; inherited adapter discards usage, PC-002. |
| P01-T02; FR-003; C5/C11 | Partial | Role-owned review is correct; source-to-output audience compatibility and persisted-record projections are unresolved, PC-003. |
| P01-T02; FR-005/043; C10 | Partial | Current hash recheck is stated without transaction-time validation or complete dependency basis, PC-004. |
| P01-T02; existing SQL/AI/shared-runtime behavior | Partial | Existing global SQL writer lock and store caches require an explicit short-transaction/background lifecycle, PC-005. |
| P01-T03; existing SQL/data/service lineage | Partial | Persistent schema migration and rollback compatibility are not acceptance steps, PC-006. |
| P01-T03; CON-009/AC-057; C2/C15 | Partial | Correct real-platform requirement; concrete changed-image, identity, budget and non-destructive evidence procedure missing, PC-007. |
| Proposal-only; funding/rank/consent/safety/quality authority | Covered | Explicitly rejects old mutating funding path and domain approvals. PC-008 makes the unchanged-state checks concrete across all outcomes. |
| P01-T03; regression and publication boundary | Covered | Existing tests retained, new focused tests bounded, #68/no merge/no force-push and private-file preservation explicit. |
| Human/business/value acceptance | Covered | Not claimed; accessibility/role acceptance, calibration and benefit measurement remain separate. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 7 High, 1 Medium, 0 Low.
* Rationale: Scope and authority are credible, but the safety-critical runtime contract and changed-build evidence are still promises rather than a sufficiently specified implementation/validation path. Apply the bounded corrections below directly before implementing the affected paths. A second critique is not requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Recoverable leases need fenced completion and uncertain-outcome semantics

* Related IDs: P01-T02/P01-T03; durable deduplication requirement; C7/C14.
* Evidence: phase details say claims are atomic with bounded recoverable leases. sqlstore.py:300-353 persists recommendations transactionally; mssqlstore.py:50-51 serializes SQL writes. Neither cited primitive defines task leasing or fences late model results.
* Concern: A worker can exceed its lease, another worker can reclaim, and the first worker can later overwrite the new attempt's result. A crash after inference but before persistence can replay a billed call; a lost SQL acknowledgement can duplicate task creation/completion unless the task identity is recovered. Reactive and proactive deduplication also needs a stated relationship, not just stable trigger IDs.
* Impact: Duplicate proposals, overwritten results and uncontrolled retries can occur despite an atomic initial claim.
* Smallest useful change: Define a durable task state machine and database uniqueness key over assistant/version, case, permitted source signature and intended proposal identity. Record reactive/proactive provenance separately. Use owner plus monotonic attempt/fencing token, lease expiry and compare-and-set for renewal/completion. Define database-authoritative time, attempt limit/backoff, terminal/manual states and lookup-by-key recovery for uncertain commit. Do not claim exactly-once inference; conservatively account for possible billed calls before retry.
* Action owner: Planning parent for contract; implementation parent for store/runtime and tests.
* Exact resolving evidence: Revised P01-T02 contract and targeted tests using independent store connections for simultaneous enqueue/claim, expired-lease takeover, late first-worker completion rejected, restart before/after inference, lost completion acknowledgement, exhausted attempts and reactive/proactive collision. Verify one durable current proposal, no unauthorized terminal transition and bounded provider attempts on SQLite and the actual MSSQL adapter path.
* Decision route: Direct planner correction. Choosing a bounded at-least-once attempt design is compatible with owner direction; no separate infrastructure or user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Model-call counts do not bound shared provider liabilities

* Related IDs: P01-T02/P01-T03; bounded cost NFR; CON-009/AC-057.
* Evidence: plan promises input/output/scan/invocation bounds. ai.py:53-60 limits output to 700 tokens and returns only message content, dropping provider usage. PRD:100-122 and addendum:180-220 require effective per-build budget/authority, reservations and usage/cost telemetry; historical #58 override is not blanket authority.
* Concern: No enforced numeric/configured input bound, concurrency/rate ceiling, total-call allowance, retry budget or reservation settlement is specified. Independent replicas and repeated requests can each satisfy a per-task call cap yet exceed the shared allowance. A timeout can incur provider cost even if no output returns.
* Impact: Proactive scans can cause unbounded cumulative cost; accepted-build usage provenance cannot be obtained from the unchanged adapter.
* Smallest useful change: Record effective scoped authority and explicit conservative execution limits before enabling real inference. Define maximum evidence bytes/tokens, output tokens, scan size/frequency, active calls, attempts and shared time-window/run allowance. Reserve allowance durably before dispatch; deny before calling when exhausted, preserve unknown-cost timeout liabilities and reconcile actual usage without treating missing usage as zero. Extend the existing adapter's result envelope to retain available provider/model/deployment/usage provenance. Keep automatic scans disabled until limits are valid.
* Action owner: Planning/implementation parent; existing authorized operator records the effective allowance.
* Exact resolving evidence: Versioned effective configuration and authority reference, provider result provenance, and tests showing two connections competing for the last reservation cannot both dispatch, oversized inputs cause zero calls, retries/lease reclaim consume the same aggregate budget, timeout reserves remain accounted for, and exhaustion retains manual case access.
* Decision route: Direct correction for limits and fail-closed behavior. A genuinely missing spending authorization remains Blocked; only obtaining a new spending grant requires an authorized owner decision. Do not reopen routine autonomy intake or invent authorization.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Role-owned proposals need source-authority and audience compatibility end to end

* Related IDs: P01-T01/P01-T02; FR-003/036; C5/C11.
* Evidence: phase details prohibit actor impersonation and cross-role exposure. projection.py:18-29 and 83-91 distinguish reason and finance access. ai_tasks.py:38-74 constructs source labels from raw case fields; run_text_task at 201-206 checks reason visibility but is not a complete field-permission boundary. Existing review at 223-244 is requester-only.
* Concern: Selecting a registered reviewer role does not establish which fields a service invocation may read or whether every recipient may see the persisted prompt, citations or result. A proactive service principal could accidentally produce a richer proposal than its eventual reviewer is permitted to receive. Current task helpers must not be treated as universal projected evidence builders.
* Impact: Review queues, direct task lookup or reports can expose finance, resident adjustment, document or supplier-scoped information across roles.
* Smallest useful change: Define each assistant's source allowlist and service-purpose principal independently of a human requester. Ensure evidence is permitted for the intended recipient audience before inference. Gate enqueue, invocation, list/detail, review and any reports/exports separately; recheck current case/supplier scope and role on every read. Hide inaccessible source/output rather than reusing a richer stored answer for a poorer audience. Treat source text as data, not authority to extend permissions.
* Action owner: Planning parent for the registry matrix; implementation parent for projection and API tests.
* Exact resolving evidence: Per-assistant source/audience matrix plus captured adapter-input tests and list/detail/review/report denial tests for unknown role, non-reason staff, non-finance staff, another supplier, changed owner and revoked access. Assertions cover prompt, response text, citations, record metadata and errors, not only buttons.
* Decision route: Direct planner correction using retained role mappings. Broader company control-owner approval remains a separate pilot gate, not permission to expand exercise access.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Stale checks must be dependency-complete and atomic with review persistence

* Related IDs: P01-T02/P01-T03; FR-005/043; C10.
* Evidence: phase details require canonical hash before inference and source/permission recheck on review. PRD FR-043 requires exactly dependent invalidation, preserving unrelated decisions. SQL currently uses optimistic versions when saving recommendation records, but these are not dependency checks on a concurrently changed case/document/configuration.
* Concern: A current-source check followed by a later write permits a change between check and commit. Hashing every case field can also make unrelated edits stale, while hashing only selected values can miss document replacement, task/schema/rule version or reviewed source withdrawal. Editing a stale result must not bypass the accept prohibition.
* Impact: A reviewed proposal can be accepted against superseded evidence or unrelated changes can cause unnecessary review churn.
* Smallest useful change: Define canonical material dependency signatures with stable source IDs/versions, relevant document hashes and assistant/schema/rule configuration versions. Re-read and validate dependencies, current permission and pending proposal version inside the review transaction or equivalent compare-and-set. Treat stale/failed/unverified output as non-acceptable/non-edit-acceptable; preserve rejection/history and require a fresh proposal for successful review.
* Action owner: Planning/implementation parent.
* Exact resolving evidence: Tests race a dependency change and two reviewer decisions against acceptance; only one current authorized review commits. Include document replacement under the same name, changed registry/rule version, revoked role, unrelated field update, stale edit and failed/unverified acceptance. Dependent records stale, unrelated proposals unchanged, prior evidence retained.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Shared-runtime execution must not hold domain locks during inference

* Related IDs: P01-T02/P01-T03; manual-case access NFR; durable claims.
* Evidence: mssqlstore.py:50-51 takes an exclusive transaction-owned application lock with a 15-second wait; sqlstore.py:270-353 coordinates shared store/cache and persistence; ai.py:58 permits a 40-second provider request. Plan does not specify startup/shutdown, connection ownership or where scan/provider work occurs relative to these locks.
* Concern: A naive shared worker can hold the global writer/store lock while calling AI, reuse a connection concurrently, or start duplicate unbounded scan loops per replica. Disabled assistance does not ensure responsive manual access if work already running blocks ordinary reads/writes.
* Impact: Existing funding, consent, safety and quality users can suffer avoidable lock contention or blocked access even without any assistant domain mutation.
* Smallest useful change: Use short transactions to capture/reserve/claim and complete; invoke the provider outside domain/store/database locks. Specify bounded worker concurrency, connection ownership, non-overlapping scan scheduling, interruptible shutdown and recovery of in-flight leases. Database task identity handles replica duplicates. Do not add a separate estate merely to achieve this.
* Action owner: Implementation parent, with lifecycle constraints added by planning parent.
* Exact resolving evidence: A deliberately blocked provider call runs while ordinary case reads and authorized domain writes complete without waiting for it; two replicas do not create duplicate durable work; shutdown/restart recovers or expires claims; assistance-off prevents new calls/scans while case access remains responsive.
* Decision route: Direct correction within the shared-runtime decision. Separate infrastructure would be a divergent proposal, unsupported and unnecessary on supplied evidence.

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: Durable task schema needs a retained-data migration and compatible rollback

* Related IDs: P01-T02/P01-T03; existing dataset/service lineage; rollback NFR.
* Evidence: SQL schema is defined in sqlstore.py and separately translated/created in mssqlstore.py:28-46 and 189 onward. Plan requires durable storage and rollback but gives no persistent-schema rollout or old-image compatibility procedure.
* Concern: New task/lease/index state will outlive the new container image. An image rollback alone cannot undo an incompatible SQL change; multiple starting replicas may race schema initialization. A global store sequence/cache change may affect existing recommendations or retained audit history.
* Impact: The exercise can damage the retained programme or leave the last known-good image unable to serve it.
* Smallest useful change: Plan an additive, idempotent, transactional/versioned migration for SQLite and MSSQL, with startup concurrency controlled and migration privileges identified separately from ordinary runtime operation. Preserve existing records and stable codes; no reseed/reset. State whether the old image safely ignores new tables/fields and how assistance is disabled/traffic restored without deleting new evidence.
* Action owner: Implementation parent and existing authorized deployment operator.
* Exact resolving evidence: Migrate a populated retained-structure fixture, rerun migration, start competing connections, compare controlled records/audit lineage, and run the old-image compatibility or explicitly documented safe rollback path. SQL counts/content and old recommendations survive; the new claim schema/indexes exist in the actual MSSQL dialect.
* Decision route: Direct planner correction. Destructive migration or extra privilege grants would be divergent and must not be assumed; choose the compatible additive path.

<!-- rpi:critique id=PC-007 -->
### PC-007 [High]: Delivery gate needs a concrete changed-image and non-destructive platform evidence procedure

* Related IDs: P01-T03; CON-009/AC-057; C2/C15.
* Evidence: phase details call for a tagged image, deployment privilege/config checks and real SQL/model evidence. infra/README.md:112-139 identifies historical image account-switch-20261013-01 and revision ca-forward-test-api--0000009; it does not establish the new candidate's deployed behavior. AC-057 requires independent SQL before/after/restart, identity and provider usage evidence.
* Concern: A tag/build success or local non-root test can be substituted for the actual running digest, and an old model call/restart proof can be inadvertently reused. The candidate does not define what gets written for proof, how domain state is preserved, config comparison, rollback readiness or what happens when shared-runtime authorization/budget is missing.
* Impact: A nominally completed new version could fail the owner's mandatory real-platform baseline or perform unnecessary shared-environment mutations.
* Smallest useful change: Add ordered delivery gates: check current existing runtime and effective budget/authority; capture private pre-rollout config/identity/data fingerprints and rollback digest; build the exact source revision; verify non-root/readable assets/health; update only the intended existing image/config; verify serving digest/revision and unchanged SQL/AI/auth references. Execute a registered assistant proposal via the changed deployed API, independently inspect task/audit persistence in real SQL, restart the app non-destructively, read it again, and exercise failure/manual handling. Preserve 60,000 stock/980-case lineage and domain-state fingerprints. Record per-assistant mode evidence without claiming ten live billed calls are required by AC-057.
* Action owner: Planning/implementation parent and existing authorized deployment operator.
* Exact resolving evidence: A redacted acceptance manifest links source commit, image digest, serving revision, endpoint, configuration fingerprint, workload identity, executed assistant/source signature, provider/model/usage/outcome, SQL before/after/restart and failure/manual observations. Include build/non-root checks and unchanged domain/data comparisons. Missing live evidence is Blocked/Not run, with the build artifact distinguished from accepted deployed delivery.
* Decision route: Direct correction to operational proof. Latest direction resolves ordinary implementation/new-version choices; missing genuine platform authority or spending authorization is an execution blocker, not something inferred from possession of credentials. Obtain only the specific missing authority if required.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Five callable labels need executable eligibility, validity and unchanged-state evidence

* Related IDs: P01-T01/P01-T02/P01-T03; FR-028/036; AC-054; C1/C10/C12/C13.
* Evidence: research's capability table supplies useful trigger categories and human boundaries; candidate details map human roles but omit exact implemented predicates, authoritative source IDs/locators and malformed-output handling. ai_tasks.py:179-198 checks label citations, not whether a claim is entailed by its source; ai.py:64-92 can return a validated template after provider failure.
* Concern: An always-eligible scan, generic case summary under five names, or cited but unsupported inference could satisfy a loose reading of callable paths. Failure/template validation must not become AI success or a reviewable authoritative answer.
* Impact: The delivery may not demonstrate five distinct useful proactive/reactive capabilities, and tests may miss mutation on fallback/review paths.
* Smallest useful change: Include one compact executable contract/acceptance matrix for all five: stable assistant/version, relevant source schema and permitted IDs/locators, reactive permission, concrete proactive predicate and scan/due semantics, owner/reviewer, typed output limits/validation, citations/unknowns, disabled/failure/manual behavior and unchanged controlled-state assertions. Bound source text and reject instructions that request authority expansion. Citation checks prove provenance, not semantic truth; retain unverified status where verification is absent.
* Action owner: Planning parent for matrix; implementation parent for adapters/UI/tests.
* Exact resolving evidence: For each assistant, one eligible and one ineligible proactive scenario plus reactive, disabled, malformed/unsupported citation and manual/failure tests. Verify status/provenance in API/UI and compare before/after case, rank/order, consent, safety holds, funding, appointments/work orders and quality approvals across generation, retry and accept/edit/reject. Proposal/audit changes are permitted; controlled-domain changes are not.
* Decision route: Direct planner correction. Choose bounded exercise predicates from existing evidence; do not invent approved company rules, add estate integrations or request renewed five-assistant scope approval.

## Strengths and Residual Risk

* Reuses the existing SQL/AI/API/UI lineage instead of treating five capabilities as five physical applications.
* Correctly rejects requester impersonation and the old mutating funding draft path.
* Preserves independent quality, professional assessment, resident choice, Finance approval, deterministic ranking and safety control.
* Distinguishes real inference from templates, and technical delivery from measured value or human acceptance.
* Keeps unrelated presentation/private files untouched and publication on consolidated #68 without merging or rewriting history.
* Exactly-once external inference is not supported by the supplied provider evidence. Bounded duplicate billing must be an explicitly documented residual risk, not an invented guarantee.
* Company role-policy approval, calibrated task quality, accessibility participant acceptance and comparative benefit remain separate gates. This critique does not silently accept them.

## Questions or Blocking Evidence Gaps

* No routine user question is required. All eight findings have compatible direct corrections.
* Current effective spending allowance, deployment/migration privilege and changed-image SQL/provider evidence are not supplied. Establish them at the relevant execution gate; missing evidence blocks acceptance rather than the bounded plan critique.
* Only a genuinely absent authority grant, destructive migration, expanded access or new infrastructure would require a significant/divergent decision. None is necessary to implement the recommended compatible corrections.

## Limitations

* Internal source inspection only; no external research, current cloud assertions or native execution.
* Research pins its source evidence to 0af4a9b481008c0e00206c34532af8039c18b7a6. Inspected workspace artifacts are the supplied candidate/evidence, not proof of later deployed parity.
* Existing untracked material was observed and not altered. No branch change, remote write or private configuration inspection occurred.
* The critique evaluates the full supplied boundary once. Findings are missing contract/test obligations, not allegations that the future implementation already contains those bugs.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning/implementation parent.
* Smallest next action: Specify the fenced SQL task/attempt lifecycle and race/recovery acceptance cases, then incorporate PC-002 through PC-008 in the same disposition/revision before affected implementation.
* User response required: No, unless execution reveals genuinely missing scoped spending/platform authority.
* Do not commission another critique pass. Parent records dispositions and completes implementation and the planned post-implementation Review.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-13/five-retrofit-assistants-plan.md](.copilot-tracking/plans/2026-10-13/five-retrofit-assistants-plan.md) | Assessed final-candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-13/five-retrofit-assistants-phase-details.md](.copilot-tracking/details/2026-10-13/five-retrofit-assistants-phase-details.md) | Assessed implementation and delivery details, unchanged. |
| [.copilot-tracking/research/2026-10-13/five-retrofit-assistants-research.md](.copilot-tracking/research/2026-10-13/five-retrofit-assistants-research.md) | Supplied source analysis, unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-13/five-retrofit-assistants-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-13/five-retrofit-assistants-plan-critique.md) | One complete independent actionable finding set. |

## Next Steps

Active parent applies compatible corrections directly, records dispositions, and proceeds through implementation and evidence gates without another critique loop. No routine user action is required. This critique stops here.
