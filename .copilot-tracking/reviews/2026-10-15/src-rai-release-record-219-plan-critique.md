---
title: RPI Plan Critique - task-bound RAI release records
description: Single final-candidate credibility assessment for issue 219
ms.date: 2026-10-15
---

## Metadata

* Task ID: 219
* Critique date: 2026-10-15
* Branch: feat/src-rai-release-record-219
* Plan: .copilot-tracking/plans/2026-10-15/src-rai-release-record-219-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/src-rai-release-record-219-phase-details.md
* Critique execution status: Complete
* Critique count: one final-candidate assessment; no delegated or additional review.

## Inputs and Criterion Boundary

* Caller requirements: versioned RAI records for registered task activations;
  reuse core assistant_release and ai_registry; no new mvp code, core-to-workload
  import, or agents SQL/blob clients; portable new SQL; local suites, ruff, mypy
  and a synthetic local app run; honest unavailable owner/live evidence;
  implementation artifacts committed and a main-targeting PR with Refs #219.
* Assessed the complete supplied plan, phase details and research artifact,
  including C1-C7, W1, all functional/non-functional requirements, acceptance
  criteria, P01-T01 through P02-T02, dependencies, decisions and residual risks.
* Checked canonical issue #219 body and owner migration comment read-only with
  gh. Its five criteria are unchanged; #105 is the registry dependency and
  #290 is the migration prerequisite. The current branch has no open PR.
* Read project context in docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md, with focused release-position and OQ-017 sections.
* Implementation evidence: src/core/src/zava_forward/core/assistant_release.py,
  ai_registry.py, ai_tasks.py, ai.py, assistants.py, sqlstore.py and store.py;
  src/core/tests/release_support.py; src/core/pyproject.toml; src/README.md;
  docs/adrs/0006-src-layout-and-cutover.md;
  docs/architecture/mvp-to-src-parity-matrix.md.
  File basenames above share the explicitly stated core source directory.
* Test ownership, no removals, and maximum additions are locked. Every resolving
  test below belongs in existing owning tests or within the already allowed
  three new test modules. No finding authorizes a changed budget, golden
  evaluation content, dependency boundary, or production authorization bypass.
* This is a plan assessment, not implementation acceptance, a vulnerability
  review, a legal-currentness check or live authorization. Tests and app
  execution are future implementation deliverables, not critique results.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Issue #219 / FR-051 / AC-069: required record content and fail-closed dispatch | Partial | Required fields and malformed/expired controls are planned; runtime legacy prompt binding needs PC-002. |
| Issue #219: visible, persisted denial and manual route | Covered | Plan Functional Requirements and P01-T02 explicitly require persisted denials; local assertion remains implementation work. |
| Issue #219: matching exercise record permits only bounded proposals | Covered | Exercise/actual distinction, no fabricated approvers and unreviewed outputs are explicit. |
| Issue #219: material-change invalidation | Partial | Exact record identity is planned, but cross-endpoint rollback and retained reliance paths need PC-001 and PC-003. |
| Issue #219 / OQ-017: named authority or explicit gap | Covered | Unavailable holders, qualified review and real evidence remain open; no user choice is needed to preserve denial. |
| Research C1-C2: migration and dependencies | Covered | Reuse of the migrated core cluster agrees with ADR 0006 and parity mapping; no additional migration or mvp implementation is needed. |
| Research C3-C6 / P01-T01: shared contract and selection | Partial | Existing release storage is the right extension point; actual legacy prompt dependencies need PC-002. |
| P01-T02: activation/completion/reliance and supersession | Partial | PC-001, PC-003 and PC-004 identify missing lifecycle cases and resolving evidence. |
| Non-functional requirements / P02-T01: strict tooling | Partial | Project commands retain migrated-module exclusions; PC-005 requires evidence for the new contract logic itself. |
| P02-T01: all five suites, dependency rules, synthetic App/HTTP run, Docker attempt | Covered | Commands, cwd, results and limitations must be recorded; no synthetic result may be called live AI. |
| P02-T02: documentation, reference index/log, artifacts, PR and review | Covered | Privacy-safe commit, topic push, main PR with Refs #219 and no merge are explicit. |
| Locked test ownership, removals and additions | Covered | Findings can be resolved within the existing budget; none requests new ownership or removals. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 3 High, 2 Medium, 0 Low.
* Rationale: reuse, isolation and evidence boundaries are credible, but the
  candidate does not yet reconcile its supersession rule with rollback,
  actual legacy dispatch inputs with their release binding, or all retained
  reliance surfaces with invalidation. Renewed activation and strict-check
  evidence also need explicit completion criteria. These are direct planner
  corrections, not reasons to seek fictional owner approval or another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Tuple-scoped supersession can revive an older release after an endpoint or deployment rollback

* Related IDs: issue #219 material-change criterion; Research Wave 3;
  P01-T01; P01-T02; plan Functional Requirements.
* Evidence: the plan says "Supersede prior records for the same
  task/endpoint/deployment." Research Wave 3 explicitly rejects a historical
  record reviving after rollback. In
  src/core/src/zava_forward/core/assistant_release.py:55-76, admission searches
  every active record and accepts any matching record.
* Concern: release A for task T at endpoint/deployment X remains active when
  release B for T at Y supersedes only Y records. Restoring X can match A without
  renewed approval. Binding individual proposals to their selected release does
  not prevent this new activation from selecting the still-active historical A.
* Impact: material endpoint/model routing changes can silently restore obsolete
  use, impact or evidence approval, contrary to the stated rollback protection.
* Smallest useful change: define the release succession scope and a non-revival
  invariant. Supersede the previous task authorization across endpoint/deployment
  changes, or explicitly bind routing scopes to a current authorization generation
  that cannot be restored merely by changing configuration. Use the existing
  transaction and record body/status, preserving historical events.
* Action owner: planning parent, P01-T01/P01-T02.
* Exact resolving evidence: revised succession rule plus an owning core test:
  approve T/X, approve T/Y, restore runtime X, assert denial and zero provider
  calls until a new explicit X approval; B supersedes dependent A proposals,
  unrelated tasks remain unaffected, and old records/events remain inspectable.
* Decision route: direct planner correction. Existing direction already rejects
  historical-record revival; no owner decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Legacy release bindings do not represent the prompts actually dispatched

* Related IDs: issue #219 prompt-version mismatch criterion; Research C5;
  P01-T01; P01-T02.
* Evidence: src/core/src/zava_forward/core/ai_registry.py:57-71 constructs
  prompt_version from LEGACY_PROMPT, task and registry purpose.
  Actual system/instruction text is independently constructed in
  src/core/src/zava_forward/core/store.py:538-558 and :608-616,
  src/core/src/zava_forward/core/ai.py:131-140, and the other retained
  text-task call sites. src/core/src/zava_forward/core/ai_tasks.py:25 declares
  a separate PROMPT_VERSION used in persisted envelopes.
  P01-T01 proposes hashing the registered task use/impact/evaluation contract,
  but does not reconcile these actual prompt dependencies and version sources.
* Concern: changing a resident-message, briefing, priority or document-reading
  instruction need not change the current release binding. Merely centralizing
  the existing selector or hashing the registry entry preserves that mismatch.
  The persisted output can also report a different prompt version from the one
  used to authorize it.
* Impact: a material prompt change can still obtain a provider call using
  obsolete approved evidence, violating a primary no-call criterion.
* Smallest useful change: specify one canonical versioned prompt contract for
  each retained task, shared by request construction, release matching and
  persisted output metadata. Bind the actual static instructions and applicable
  schema/policy dependencies, not per-case prompt data or a purpose-only hash.
* Action owner: planning parent, P01-T01/P01-T02.
* Exact resolving evidence: revised binding ownership and core tests that change
  an actual dispatched prompt contract while retaining the registry purpose,
  assert zero calls with the old release, and show matching release/output
  prompt versions after renewed approval. Include the strong-model priority and
  document-reading routes, not just the generic text-task fixture.
* Decision route: direct planner correction; no new functionality or user
  decision is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Generic legacy gating does not cover the separate retained reliance surfaces

* Related IDs: issue #219 material-change criterion; P01-T02; plan
  "recheck it before completion/reliance" requirement.
* Evidence: src/core/src/zava_forward/core/ai.py:108-128 rechecks a string-valued
  gate before/after generic inference but retains no invocation-specific release
  context. src/core/src/zava_forward/core/store.py:543-548 returns cached
  briefings based only on store.version; :623-635 constructs priority records
  separately from ai_tasks.finish; :663-697 resolves those priority records
  without a release check. src/core/src/zava_forward/core/ai_tasks.py:258-303
  handles other reviews separately. P01-T02 names assistant review checkpoints
  and legacy output identity, but its completion criteria do not enumerate
  these legacy read/review paths.
* Concern: changing only SqlStore.release_block and ai_tasks.envelope does not
  update priority records or their separate review function, invalidate a
  cached briefing, or ensure that the post-call gate checks the exact record
  selected before the call. Release updates use their own SQL connection, so
  they cannot be assumed to invalidate the Store version cache.
* Impact: a superseded/revoked proposal can remain visible as usable or be
  accepted; a replacement matching release can mask an in-flight record change.
* Smallest useful change: enumerate the retained lifecycle in P01-T02:
  per-invocation selected release context through Ai.run/look_at and persistence;
  ordinary text/document records and distinct priority records; cached reads,
  current views, and both review functions. Require current exact-record
  validation before reliance while retaining history and manual/templates.
* Action owner: planning parent, P01-T02.
* Exact resolving evidence: core tests revoke/supersede after generation, then
  read cached briefing and attempt ordinary and priority accept/edit: obsolete
  AI content is not actionable and acceptance is denied. A provider test double
  replaces the release during a call and proves the old call is quarantined
  even when the replacement otherwise matches. Outputs retain the exact
  selected ID/version/digest without shared mutable per-call context.
* Decision route: direct planner correction. The plan already requires
  completion/reliance checks; this makes their actual retained surfaces explicit.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Release renewal has no defined fresh activation identity

* Related IDs: P01-T02; exact-record binding and history-preservation requirements.
* Evidence: src/core/src/zava_forward/core/assistants.py:569-596 derives the task
  ID from capability, VERSION, case, source signature and proposal_identity,
  with no selected release. Existing rows are reused; only disabled rows with
  remaining attempts are reset. The plan binds claims to release identity and
  invalidates proposals on supersession, but does not say how unchanged
  source is activated again under a newly approved release.
* Concern: a ready, accepted or quarantined A-bound task can remain the
  deterministic target after release B approval. Invalidating A without
  changing identity or defining a new activation attempt can either strand
  legitimate renewed work or tempt an implementation to overwrite A's binding.
* Impact: renewed approval need not restore bounded generation, or it can erase
  the evidential relationship between the historical output and its release.
* Smallest useful change: define a release-aware proposal/activation identity or
  an append-only activation generation. Repeated requests under the same
  release stay idempotent; renewed approval can create fresh work without
  changing the old proposal's binding, review or usage accounting.
* Action owner: planning parent, P01-T02.
* Exact resolving evidence: core test generates under A, supersedes with B
  without altering source/case, reinvokes reactively and proactively, and proves
  fresh B-bound work is dispatchable, same-B requests deduplicate, and A's
  record/output/events remain unchanged and non-actionable.
* Decision route: direct planner correction; preserve the existing schema
  boundary and locked module/test addition budget.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Per-project tool success does not prove strict checking of new logic in exempt modules

* Related IDs: Non-Functional Requirements; P01-T01; P02-T01.
* Evidence: src/core/pyproject.toml:41-63 excludes assistant_release,
  assistants, ai_registry, ai_tasks, ai, store and sqlstore from formatting,
  suppresses selected lint rules and sets ignore_errors=true for their mypy
  modules. P01-T01 makes a typed helper optional. P02-T01 specifies project
  ruff/mypy runs, whereas the plan promises strict ruff/mypy for new contract
  logic without broadening existing exemptions.
* Concern: implementing all new contract logic in those existing modules can
  produce green project commands while never strictly checking that logic.
* Impact: recorded tooling evidence can overstate compliance with the plan's
  explicit strictness requirement.
* Smallest useful change: make the unexempt typed contract helper the owner of
  new validation/selection logic within the permitted two-module allowance, or
  specify an equivalent narrow strict-check mechanism. Keep exempt integration
  glue and existing migration debt honestly distinguished; do not require a
  repository-wide cleanup or loosen existing settings.
* Action owner: planning parent, P01-T01/P02-T01.
* Exact resolving evidence: phase details name the strictly checked file(s)
  and exact commands/configuration. Implementation evidence records successful
  format/lint and strict mypy checks that actually include those files, alongside
  all existing per-project checks, and identifies any unchanged exempt glue.
* Decision route: direct planner correction; no changed test ownership,
  removals or addition budget is requested.

## Strengths and Residual Risk

* The existing SQL-owned record, shared registry, transactions and append-only
  events are appropriate foundations. No parallel governance service, new
  schema or workload-to-core dependency reversal is needed.
* Exercise approval is not live approval. Unknown holders, non-representative
  constructed evaluations, returned-model checks rather than serving
  attestation, and unavailable Azure/SQL Server evidence are correctly
  distinguished from engineering completion.
* Local provider test doubles can demonstrate control semantics and zero-call
  denials, not model value, fairness, human oversight or legal compliance.
* The Docker attempt is an honest tooling result, not an image or deployment
  success claim. New portable SQL must still be reviewed as SQL Server-bound;
  local SQLite execution cannot establish live SQL Server compatibility.
* The requirement to leave unsupported human/live criteria open is accepted
  caller direction, not an implementation blocker or a new owner question.

## Questions or Blocking Evidence Gaps

* No decision-critical owner question blocks the direct corrections above.
* Actual release/risk/suspension/restart holders and competent-review evidence
  remain unavailable under OQ-017. Explicitly record that gap; do not promote the
  existing hard-coded denial owner label into validated authority.

## Limitations

* Read-only inspection of supplied materials and directly relevant code only;
  no tests, lint, type checking, HTTP run, Docker build, deployment or provider
  calls were performed for this critique.
* Existing untracked plan/research/state inputs were preserved. No source,
  plan, phase-details, research or session-state file was edited.
* No .env, private data, issue mirrors or private runtime fixtures were read.
  No nested agent, second review, commit or push was performed.
* Findings assess missing plan guarantees and concrete current extension
  hazards, not the correctness of an implementation that does not yet exist.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: correct the succession scope/non-revival invariant in
  P01-T01/P01-T02, then disposition PC-002 through PC-005 in the same plan
  revision before implementation.
* User response required: no. All findings are direct corrections within
  existing caller decisions.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/src-rai-release-record-219-plan.md](.copilot-tracking/plans/2026-10-15/src-rai-release-record-219-plan.md) | Assessed final-candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-15/src-rai-release-record-219-phase-details.md](.copilot-tracking/details/2026-10-15/src-rai-release-record-219-phase-details.md) | Assessed phase details, unchanged |
| [.copilot-tracking/research/2026-10-15/src-rai-release-record-219-research.md](.copilot-tracking/research/2026-10-15/src-rai-release-record-219-research.md) | Supplied research, unchanged |
| [.copilot-tracking/reviews/2026-10-15/src-rai-release-record-219-plan-critique.md](.copilot-tracking/reviews/2026-10-15/src-rai-release-record-219-plan-critique.md) | This single critique and complete finding set |

## Next Steps

Return Revise to the active planning parent. The parent should directly
disposition PC-001 through PC-005, finalize the plan without another critique,
and continue only after its implementation eligibility gate is satisfied.
No user action is required. This critique stops after writing this artifact.
