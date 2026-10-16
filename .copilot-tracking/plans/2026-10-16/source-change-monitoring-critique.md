---
title: Source change monitoring final-candidate critique
description: One bounded assessment of the issue 213 offline implementation plan
ms.date: 2026-10-16
---

## Metadata

* Task ID: 213 / source-change-monitoring.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/source-change-monitoring-plan.md.
* Phase details: .copilot-tracking/details/2026-10-16/source-change-monitoring-phase-details.md.
* Critique execution status: Complete.
* Assessment count: Exactly one final-candidate critique; no delegated assessment.

## Inputs and Criterion Boundary

* Caller requirements: bounded offline src-only executable slice; differences
  trigger review of affected cards, journeys, tests and communications;
  discovery stays unverified until provenance/completeness review; approved
  cards remain immutable; human approval and regression precede effective-date
  activation; rollback and per-source High/Medium/Low cadence are required.
  Juan Manuel Servera is the sole exercise Legal/Compliance/DPO owner.
* Primary evidence: the supplied plan, phase details and
  .copilot-tracking/research/2026-10-16/source-change-monitoring-research.md.
* Source evidence: src/core/src/zava_forward/core/lawstore.py,
  src/core/src/zava_forward/core/rulecards.py and
  src/core/src/zava_forward/core/rule_engine.py. A targeted inspection of
  src/core/tests/test_rulecards.py established existing lifecycle and local
  temporary-fixture conventions, not test execution results.
* Repository context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md (exercise baseline),
  docs/reference/README.md and docs/reference/memory.md.
* Decisions/dependencies assessed: P01 precedes P02, which precedes P03;
  existing HEAD is 0f9ba37 on feat/src-regulatory-change-review-213. The
  supplied planning inputs are already untracked; they were not moved,
  committed or edited.
* Criterion boundary: implementation credibility and locally demonstrable
  safety, not live source currentness, production/legal acceptance, hosted
  scheduling, scraping, network tests, notification delivery or source
  publication. No private data, environment files, editor settings or
  .copilot-tracking/github-issues were read. No additional agents were used.
* The plan references six issue acceptance criteria but does not reproduce
  their wording. This critique assesses the supplied requirements and the
  plan's acceptance claims, not an independently retrieved issue checklist.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Offline/src-only scope; research C1-C3; P01-T01/T02 | Covered | Separate candidate storage, local JSON inputs, bounded job and no approval command are appropriate. |
| Difference/impact review; research C2; P01-T01 | Partial | Impact fields and unknowns are required, but exact source-to-card matching and candidate/version-specific review identity need definition: PC-005. |
| Provenance/completeness; research C5; P01-T01, P02-T01 | Partial | Candidate isolation is explicit; passing evaluate alone does not prove runtime citation eligibility: PC-003. |
| Immutable approved cards; P01-T01, P02-T01 | Covered | Append-only card versions, observations and events preserve the existing design. |
| Human owner and exercise-only evidence; P02-T01/T02 | Partial | Named owner and independent author/owner are explicit; new approval/result records need their own simulated labels: PC-007. |
| Activation authority/date gates; research C4; P02-T01/T02 | Partial | Direct activate is addressed, but release and alternate versions can escape target-only gating: PC-001. |
| Approval/regression freshness; P02-T01/T02 | Partial | Exact cards and immutable test plans are good foundations; the evidence identity/invalidation contract is incomplete: PC-002. |
| Rollback; P02-T01/T02 | Partial | Exact prior active cards and atomicity are required, but intervening transitions and rollback validity are unresolved: PC-004. |
| Per-source cadence; research C6; P01-T01/T02 | Covered | Research specifies High/Medium/Low, explicit positive day intervals and retained rationale; no guessed legal interval or hosted timer is needed. |
| Portability, isolation, concurrency; P01-T01, P02-T02 | Partial | Portable adapters and SQL contracts are retained; freshness/rollback tests must exercise independent connections as specified in PC-002/004. |
| Validation and handoff; P03-T01/T02 | Partial | Honest partial-acceptance audit and retained evidence are sound; forbidden temporary paths require correction: PC-006. |
| Dependencies and missed concerns | Covered | Phase ordering is coherent; the findings below cover the discoverable safety and execution gaps within the supplied boundary. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 4 High, 3 Medium, 0 Low.
* Rationale: the offline architecture is credible, but the plan does not yet
  close every route to active state or specify sufficient evidence freshness,
  runtime eligibility and rollback preconditions. These are bounded planner
  corrections, not reasons to demand excluded live work or new user decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Target-only activation gating leaves other reactivation routes unspecified

* Related IDs: research C4; P02-T01; P02-T02.
* Evidence: plan lines 60-61 gate direct activation for "monitored target
  cards"; phase details lines 30-32 name only existing activate.
  src/core/src/zava_forward/core/rulecards.py RuleCardStore.release appends
  active directly from held, independently of activate. activate can also
  supersede a held version. Neither path currently consults monitoring.
* Concern: guarding only the approved replacement tuple allows a held monitored
  version to become active through release, or a different approved version
  of the same affected card to evade target registration. This is a planning
  gap in the gate boundary, not a claim that the future implementation
  already contains that bug.
* Impact: owner identity alone could resume an affected control without the
  required assessment, current regression evidence or effective-date checks.
* Smallest useful change: enumerate every supported transition to active,
  including release and rollback. Gate by monitored card/source and applicable
  unresolved review state, not just replacement membership. Explicitly
  distinguish valid no-change hold release from replacement activation;
  give rollback its separately constrained authorization path. Keep unrelated
  unmonitored lifecycle behavior unchanged.
* Action owner: planning parent for P02-T01/T02; implementing developer executes.
* Exact resolving evidence: revised phase details name these paths and require
  negative tests for held release before evidence/date readiness, an alternate
  version of a monitored card, and supersession of a held card. Assertions
  inspect unchanged lifecycle events on denial plus valid owner-controlled
  no-change/replacement paths.
* Decision route: direct planner correction; no user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Latest test outcome is not a sufficient freshness contract

* Related IDs: P01-T01; P02-T01; P02-T02.
* Evidence: plan lines 55-59 require exact approved cards and configured test
  coverage. Phase details lines 27-31 require an immutable regression plan and
  recheck "candidate baseline, latest test outcome" but do not define the
  result's complete identity or invalidation dependencies.
  RuleCardStore.assess_review in src/core/src/zava_forward/core/rulecards.py
  resolves the latest card version when assessing an existing review;
  its stored assessment is not independently bound to that card version.
* Concern: a result can be latest and passing yet belong to another candidate,
  configuration revision, assessment, test plan, fixture inputs or evaluation
  contract. A newly discovered material difference or changed impact/test map
  can also leave an old approval apparently usable. The existing assessment
  API does not supply these bindings automatically.
* Impact: stale or cross-candidate approval/test evidence could authorize a
  release that was never actually reviewed and regressed as a whole.
* Smallest useful change: define a persisted release-evidence identity binding
  source/candidate ID, baseline version/hash, relevant configuration revision,
  exact impacted/target card versions, assessment/approval event IDs, immutable
  regression plan and fixture digest, evaluator version and evaluation clock.
  Define which new observations or revisions invalidate approval/results,
  versus harmless duplicate observations. Activation atomically checks that
  exact identity and its complete required result set; failed reruns of that
  identity cannot fall back to an earlier pass.
* Action owner: planning parent for P01-T01 and P02-T01/T02.
* Exact resolving evidence: phase details contain the identity and
  invalidation rules; table-driven tests reject cross-candidate evidence,
  changed configuration/assessment/fixtures, failed rerun after pass and
  intervening material observations. Include restart persistence and
  independent-connection interleaving, not only a shared adapter RLock.
  SQL Server contract evidence must identify the locking/conflict mechanism
  supporting the atomic check/write; a live SQL Server test is not required.
* Decision route: direct planner correction; no user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Evaluator regression can pass for a card the runtime cannot execute

* Related IDs: research C5 and Contrarian; P02-T01; P02-T02.
* Evidence: phase details lines 27-29 select existing evaluate.
  src/core/src/zava_forward/core/rule_engine.py evaluate accepts kind, spec,
  facts and time without inspecting cards or citations. RuleEngine._citations
  and run additionally require exact current, reviewed, complete provisions,
  eligible card lifecycle and dates. The plan excludes verified source
  publication and keeps candidates outside reg_version/provision/index.
* Concern: a replacement citing candidate-only, missing, partial, stale or
  unreviewed provisions can pass direct evaluator fixtures yet produce
  unknown at runtime. The plan does not say whether such a card is rejected
  for activation or how the positive offline fixture demonstrates eligibility
  without publishing unverified content.
* Impact: a successful release demonstration could claim an executable
  controlled rule when it only proved a pure function's behavior.
* Smallest useful change: keep evaluate for deterministic cases, but require
  a separate runtime-equivalent citation/specification/temporal eligibility
  preflight. State that unavailable verified provisions block the executable
  activation path. Use clearly synthetic, exercise-only reviewed source
  fixtures already in the law store for the positive path; do not promote
  monitor candidates or weaken production citation checks.
* Action owner: planning parent for P02-T01/T02.
* Exact resolving evidence: phase details distinguish evaluator regression
  from eligibility. Negative tests cover candidate-only/missing, partial,
  unreviewed and superseded citations. A positive synthetic test demonstrates
  the released card is actually evaluated through RuleEngine.run, not merely
  through evaluate. Search/source/provision results and index contents remain
  unchanged after detection, approval, regression, activation and rollback.
* Decision route: direct planner correction; no user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Exact rollback targets do not define safe rollback after intervening changes

* Related IDs: P02-T01; P02-T02.
* Evidence: plan lines 62-63 require exact captured prior active cards, not
  held cards. Phase details lines 30-32 mention prior active/held rechecks
  and owner-only rollback but do not specify rollback preconditions.
  In src/core/src/zava_forward/core/rulecards.py activate retires prior
  active/held versions, retire and hold add later states, and is_active
  also enforces effective/retirement dates.
* Concern: restoring the right historical version can still undo a later
  human hold, retirement, newer release or another rollback. A captured prior
  version may have expired or lost valid current citations by rollback time.
  Initial activation with no prior active card has no defined reverse state.
* Impact: rollback could resurrect an ineligible control or overwrite a
  subsequent owner decision, despite preserving immutable history.
* Smallest useful change: capture the complete per-card preactivation state
  under the activation transaction. Define rollback as an all-or-nothing
  compare-and-append against that release's unchanged active lifecycle heads;
  reject intervening owner transitions and repeated/stale rollback. Restore
  only eligible captured active versions, reject held/expired/ineligible
  restoration, and define no-prior-card rollback as removal of the new
  active state without inventing an old active version. Retain reasons,
  exercise labels and all original events.
* Action owner: planning parent for P02-T01/T02.
* Exact resolving evidence: phase details state capture timing,
  compare-and-append preconditions and no-baseline behavior. Tests cover
  hold/retire/newer release after activation, repeated rollback, expired or
  source-ineligible prior version, no prior active card, and injected failure
  during a multi-card rollback. Independent-connection interference must
  either serialize or fail cleanly with no partial lifecycle changes.
* Decision route: direct planner correction; no user decision required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Reused review discovery does not guarantee exact source and version impact

* Related IDs: research C2; P01-T01; P02-T01.
* Evidence: plan lines 50-57 require affected card versions and full
  impacted-card coverage while honestly acknowledging unknown impact.
  Phase details lines 9-14 require extending review impact.
  RuleCardStore._source_changed in
  src/core/src/zava_forward/core/rulecards.py selects card IDs with
  provisions LIKE '%source_id%', across every historical card version, and
  records only the date-selected active version. Its source_version field
  describes a law-store version, not an isolated monitor candidate.
* Concern: merely extending this payload can produce substring false matches,
  conflate historical and current impacts, or make two unpromoted candidates
  indistinguishable to assessment. No matched card can also mean an unknown
  mapping, not proof of no impact.
* Impact: the release gate's "full coverage" can describe the wrong set, while
  journeys/tests/communications appear reviewed without a stable candidate
  and card-version basis.
* Smallest useful change: define exact source matching using explicit
  configuration and parsed canonical provision references, preserve the
  particular impacted card versions/states, and bind review records to
  candidate/configuration identity without fabricating published law versions.
  Freeze the bounded impact inventory used for approval, with a disposition
  for every entry, including explicit no_change when appropriate. Preserve
  unknown/unmapped impacts separately; completeness is relative to the
  declared configuration, never a claim of complete legal impact analysis.
* Action owner: planning parent for P01-T01 and P02-T01/T02.
* Exact resolving evidence: revised details and tests distinguish similarly
  named sources, historical versus active/approved versions, two candidates
  against the same baseline and no-match/unknown impact. Stored reviews expose
  exact candidate/card bindings plus requirements, journeys, tests and
  communications, and incomplete configured dispositions block approval.
* Decision route: direct planner correction; no user decision required.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Planned interpreter and fixture paths violate the no-temporary-directory constraint

* Related IDs: P01-T02; P03-T01.
* Evidence: plan line 28 and phase details lines 44-45 prescribe
  /tmp/zf164 and /tmp/zf164/bin/python. Phase details line 19 specifies
  temporary source fixtures without directing their root. Existing
  src/core/tests/test_rulecards.py uses tempfile.TemporaryDirectory.
  The current execution constraint forbids file operations in /tmp,
  /var/tmp or other temporary directories.
* Concern: the advertised validation recipe cannot be followed as written;
  default tempfile behavior can also write outside the permitted project
  tree even if the interpreter is changed.
* Impact: implementation validation can violate an explicit environment
  restriction before testing the feature.
* Smallest useful change: replace the forbidden environment path with a
  project-local environment or an available installed interpreter. Specify
  project-relative fixture/scratch roots, explicit fixture directory
  arguments and test-process temporary-root configuration as needed so
  existing affected suites stay inside the project. Clean owned scratch
  outputs without touching existing work. Keep tests outside packages and
  executable changes inside src/.
* Action owner: planning parent for P01-T02 and P03-T01.
* Exact resolving evidence: plan and details contain no executable recipe
  using forbidden directories and provide concrete project-relative
  interpreter/fixture/test-root commands. Validation evidence records the
  actual paths and affected test commands used.
* Decision route: direct planner correction required by current constraints;
  no user decision required.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Exercise labels must travel with the new approval and evidence records

* Related IDs: P01-T01; P02-T01/T02; P03-T01.
* Evidence: research lines 66-68 correctly state all fixture approvals remain
  simulated. Plan lines 21-22 disclaim real approval, but its persistence
  requirements do not carry that distinction onto new monitor assessments,
  release approvals and regression results. Existing card lifecycle events
  have simulated and exercise labels; existing assess_review records do not
  automatically inherit the lifecycle event's simulated field.
* Concern: a standalone monitor approval/result naming Juan Manuel Servera
  can look like actual human provenance/compliance approval when read apart
  from the research document. Synthetic reviewed-source fixtures introduced
  for PC-003 present the same risk.
* Impact: persistent evidence can misrepresent simulated approval as the
  named owner's real legal, compliance or DPO acceptance.
* Smallest useful change: explicitly require exercise/simulated classification
  and a visible disclaimer in every new approval-bearing record, fixture,
  returned release/evidence representation and README example. Preserve Juan
  Manuel Servera as the sole exercise owner and a distinct synthetic author;
  do not invent additional real approvers or real review timestamps.
* Action owner: planning parent for P01/P02 data contracts and P03 documentation.
* Exact resolving evidence: phase details specify the classification fields
  and display text; persistence/restart and output tests assert simulated
  labels on approval, regression, activation and rollback evidence. Synthetic
  reviewed-source fixtures explicitly identify themselves as exercise-only.
* Decision route: direct planner correction implementing the explicit user
  requirement; no user decision required.

## Strengths and Residual Risk

* Candidate storage outside law versions/provisions/index correctly avoids
  changing latest-source retrieval simply because discovery occurred.
* Append-only persistence, immutable replacement cards, explicit owner review,
  bounded rule kinds and non-executable regression plans fit the existing core.
* Explicit source configuration is preferable to interpreting prose cadence;
  High/Medium/Low does not itself invent a legal review deadline.
* Offline/local fixture operation and the orchestrator's lack of approval
  commands preserve the human boundary without demanding a new API.
* Source publication, live adapters, hosted scheduling, staff messaging,
  complete impact inventory and operational/legal acceptance remain explicitly
  excluded. They are honest follow-ups, not findings against this slice.
* Trusted in-process identity is a declared limitation. This critique does
  not require HTTP authentication, tenant integration or a new authority role.
* The 30-method limit can be retained using table-driven subtests; it must not
  be treated as permission to omit the negative-state cases above.

## Questions or Blocking Evidence Gaps

* No unresolved user choice blocks these planner corrections.
* The verbatim six issue criteria were not supplied. P03 must retain its
  criterion-by-criterion delivered/partial/deferred audit using authoritative
  context available to the planning parent; this critique makes no separate
  all-six acceptance claim and does not request prohibited file access.

## Limitations

* This is one static plan critique, not implementation review, test execution,
  security certification or legal/currentness verification.
* Existing code identifies concrete integration hazards. Findings describe
  missing plan contracts, not unobserved defects in future code.
* SQL Server portability can be assessed here only through adapter contracts;
  no live service or network test was performed or requested.
* Only this critique artifact was written. Plan, details, research, code and
  existing state artifacts remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001, because held release can reach active state
  outside a gate attached only to activate or approved target tuples.
* Action owner: planning parent.
* Smallest next action: revise P02-T01/T02 to enumerate and gate every
  monitored transition to active, then resolve PC-002 through PC-007 in the
  same plan/detail reconciliation.
* User response required: No.
* Handoff: return this complete finding set to the planning parent for direct
  correction and finalization without another critique. Do not implement,
  commit, push, open a PR or invoke another stage from this critique task.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/source-change-monitoring-plan.md](.copilot-tracking/plans/2026-10-16/source-change-monitoring-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-16/source-change-monitoring-phase-details.md](.copilot-tracking/details/2026-10-16/source-change-monitoring-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-16/source-change-monitoring-research.md](.copilot-tracking/research/2026-10-16/source-change-monitoring-research.md) | Supplied bounded research |
| [.copilot-tracking/plans/2026-10-16/source-change-monitoring-critique.md](.copilot-tracking/plans/2026-10-16/source-change-monitoring-critique.md) | Complete one-pass critique |

## Next Steps

The active planning parent should resolve PC-001 through PC-007 directly,
update its disposition and finalize without a second critique. No user action
is required. This critique stops here; it starts no implementation or live work.
