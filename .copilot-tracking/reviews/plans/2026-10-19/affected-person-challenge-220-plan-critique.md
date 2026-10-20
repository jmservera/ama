---
title: Original Independent Plan Critique - Affected-Person Challenge 220
description: Evidence-grounded final-candidate critique of the bounded retained-priority challenge plan
ms.date: 2026-10-19
ms.topic: reference
---

## Metadata

* Task ID: jmservera/ama#220
* Critique date: 2026-10-19
* Plan: .copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md
* Phase details: .copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md
* Research: .copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md
* Reviewed source HEAD/base: eeb6c3aba5d07244ae3cc0e53d839617fd928e3b
* Branch: feat/affected-person-challenge-220, tracking origin/main.
* Critique execution status: Complete.
* Original verdict: Revise.
* Severity summary: 0 Critical, 3 High, 4 Medium, 0 Low.
* Original-record rule: this is the one original independent final-candidate critique. Preserve it unchanged, including adverse findings. Planner disposition belongs in the plan/details, not in this artifact. No repeat critique is requested.

## Inputs and Criterion Boundary

The assessment covers the supplied research, complete plan and phase details,
caller requirements, and their identified actual source/test/gate seams. The
original case study, relevant addendum exercise/RAI sections, KB index and owner
memory were read. PRD FR-052, FR-043 and AC-071 were checked directly. Memory
was context, not authority.

The accepted scope is a useful retained-priority vertical slice in the existing
staff workbench. Supplied digital evidence may be staff recorded; a new resident
portal, authentication scheme, assistant graph or operational policy is neither
required nor recommended. Both digital and non-digital examples must work through
real stores and HTTP without real inference. Historical human decisions and
server recorder identity, including #406, remain evidence rather than mutable
approvals manufactured by this feature.

The assessment criteria are:

* R1: supplied digital and staff-recorded non-digital challenges, permitted
  explanation, named human owner, manual route, next update and resolution.
* R2: exact proposal, captured source and actual policy-version binding, with
  retained human decision and honest Unknown historical source provenance.
* R3: only exact dependent priority proposals/reviews become stale after supplied
  human correction; explanation alone does not invalidate; historical evidence
  is not rewritten.
* R4: current identity/owner authority, optimistic version, atomic SQL checks,
  rollback and truthful committed acknowledgement.
* R5: no inferred consent/refusal, sanction, retaliation, unrelated closure,
  ranking mutation or delayed/changed hazard handling.
* R6: native Fluent-styled labelled UI, protected drafts, keyboard/error focus,
  cancellable correction and actual Chromium/reflow evidence.
* R7: existing test ownership, no removed tests, at most 12 core and 6 HTTP
  additions and one browser script; immutable original Review and full frozen
  17-group gate after commit, without publication or later commits.

Actual sources examined include resident_decisions.py, store.py, sqlstore.py,
mssqlstore.py, projection.py, continuity.py, ai_tasks.py, ranking.py, controls.py,
change_provenance.py and export_fields.py under src/core/src/zava_forward/core;
server.py and web/panels.js plus relevant web/app.js under
src/api/src/zava_forward/api; the existing resident test owners, SQL-store and
SQL Server harnesses, public dataset, provenance browser harness; src/README.md
and tools/rpi-checks.py.

This is a plan assessment, not an implementation Review, legal determination,
accessibility acceptance or executed gate. No new external research, cloud
operation, private data access, real AI, code change or test execution occurred.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| R1; FR1-FR3; A1-A2; C1/C9 | Covered | Staff-recorded digital and non-digital evidence, explanation, owner, manual route, date and supplied human resolution are explicitly required. No portal expansion is necessary. |
| R2; FR1-FR2; C3-C4; P02-T01 | Partial | Old source Unknown and separate decision token are sound. Source capture must bind the actual initial snapshot, not a later current-case read: PC-002. |
| R3; FR3-FR4; A3; P02-T01/P02-T02 | Partial | Exact typed dependencies and preserved disposition are sound; terminal correction semantics and non-vacuous scope oracles need PC-003/PC-005. |
| R4; A5; C2; P02-T01/P02-T02 | Partial | Existing resident replay covers challenge writes. The reverse priority-acceptance race is not covered: PC-001. |
| FR5; A2/A6; C5; P02-T02 | Partial | Required dual entitlement is correct, but existing projection reuse has a concrete bypass trap needing explicit placement and denial proof: PC-004. |
| R5; A4; P01-T01 | Covered in intent | Before/after decision, remedy, closure, hazard and deterministic-ranking equality is appropriate; preserve active manual/hazard-path proof when implementing PC-005. |
| R6; A6; C5/C7; P02-T02/P03-T01 | Covered in intent | Actual Chromium and native controls are planned. app.js:445-450 rebuilds the case after other writes, so local draft preservation must cover this path, not just navigation. |
| R7; P01-T01/P03-T01; C7/C8 | Partial | Canonical modules and addition bounds are locked, but current SQL Server gate selectors do not execute the new resident contracts: PC-006. |
| R7; P04-T01 | Partial | Commit-before-gate, immutable original Review, fixed base and no later commit are correct. The specified execution paths require PC-007's explicit environment handoff/blocker. |
| Q1-Q3; C1-C9 | Covered for bounded assessment | Supplied source pointers support this scope; source-specific traps above are actionable without another research cycle. |

## Verdict

* Verdict: Revise.
* Rationale: the bounded direction is useful and supported. However, writer-time
  stale-acceptance enforcement and initial source-snapshot binding are not yet
  implementation-ready contracts. Correction finality, privacy placement and
  the acceptance evidence need explicit revision. P04 also needs an eligible
  execution route rather than an assumption that its supplied paths are usable.
* Execution status is Complete separately from the adverse verdict. These are
  plan findings, not assertions that an unimplemented candidate already has
  seven defects. No significant or divergent product decision is required:
  current user direction resolves scope, authority and prohibited behavior.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Fence priority accept/edit against concurrently committed corrections

* Related IDs: R3-R4, FR4, A3/A5, P02-T02, C2/C3.
* Evidence: phase details:55-58 require current transaction target reads when
  replaying the challenge write. In contrast, store.py:851-891 accepts/edits a
  retained priority using an in-memory recommendation. sqlstore.py:554-618
  checks modified recommendation rowversions, but does not automatically
  validate unchanged case rows used as read dependencies. The continuity fence
  in continuity.py:101-118 concerns continuity state and AI publications, not
  case-held challenge corrections; workflow-only priority has no such fence.
* Concern: checking staleness before save is insufficient. Writer A can observe
  an actionable proposal, writer B can commit a dependent correction to a case,
  and writer A can then accept/edit the unchanged recommendation row. B did not
  alter that row, so its optimistic version alone cannot prevent acceptance.
  Correcting the returned projection afterward does not satisfy server refusal.
* Impact: a stale proposal acquires a fresh human disposition after its
  correction committed, violating the core reliance boundary.
* Smallest useful change: specify writer-transaction validation of all exact
  challenge dependencies for priority accept/edit, including workflow-only
  records and policy corrections recorded on another case. Reuse the existing
  writer machinery; do not add a graph or rewrite historical recommendations.
  Keep reject and ordinary manual/hazard actions available.
* Action owner: planning parent, P02-T02 and P01-T01.
* Exact resolving evidence: revised details name the accept/edit writer seam.
  Within the existing test budget, actual two-store tests commit a correction
  between initial read and save, then show accept and edit refuse without
  persisting a disposition/audit acceptance. Reopen confirms the correction
  survives. Independent unrelated-dependency and reject/manual controls succeed.
* Decision route: direct planner correction; no user response.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Stamp the snapshot actually used to generate the recommendation

* Related IDs: R2, FR1-FR2, A2-A3, P02-T01, C3-C4.
* Evidence: store.py:774-788 assembles facts, source labels and template items
  under the initial lock, then runs generation outside it at :790-802 and
  publishes at :803-822. ai_tasks.py:188-193 computes source hashes by rereading
  the current case with the caller's reason entitlement. source_labels at
  ai_tasks.py:48-82 is a role-filtered display/citation snapshot, not a versioned
  raw document/row manifest. Details:44-50 say actual captured per-case hash but
  do not identify the capture boundary.
* Concern: calling the existing current-hash helper during publication can stamp
  source B onto a recommendation generated from source A. Also, describing that
  helper's output simply as a universal source version obscures its
  audience-dependent, citation-label scope.
* Impact: challenges can invalidate the wrong version and leave the actual
  generation dependency unchallengeable, despite apparently exact hashes.
* Smallest useful change: capture/hash the initial source-label snapshot beside
  the generation inputs, carry it unchanged into publication, and document that
  precise projected-snapshot contract. Preserve the existing hash algorithm or
  an explicitly compatible small helper; do not reconstruct old records or
  invent document-version authority.
* Action owner: planning parent, P02-T01 and P01-T01.
* Exact resolving evidence: revised details fix capture timing and scope.
  A controlled concurrent public-fixture change during actual workflow-only
  generation proves the retained hash still describes the original input;
  later generation captures the new input. Tests distinguish same-case hashes,
  different-case identical hashes and historical missing hashes. Missing source
  remains Unknown and cannot become a fabricated source target.
* Decision route: direct planner correction; no user response.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Define terminal resolution and durable correction effects

* Related IDs: R1/R3, FR3-FR4, A3/A5, P02-T01/P02-T02.
* Evidence: plan FR3 distinguishes two resolution outcomes; details:52-58
  require owner, expected version and evidence. Neither artifact says whether a
  resolved challenge can be resolved again or whether its original request,
  target/decision capture and resolution event remain immutable.
* Concern: expected version prevents an outdated write, not a subsequent
  authorized overwrite. If a current-version second resolve can replace
  `Correction recorded` with `Explanation recorded`, a derived matcher based on
  the latest outcome could silently restore reliance. Multiple causes composing
  does not by itself prevent this single-record reversal.
* Impact: supplied correction evidence and stale state can disappear without any
  source correction or separately approved restart.
* Smallest useful change: define Open-to-one-terminal-resolution behavior and
  preserve immutable opening/binding and resolution evidence. Reject a second
  resolution, or make later notes append-only without undoing correction effects.
  No new reopening, reversal or redress policy is needed for this slice.
* Action owner: planning parent, P02-T01.
* Exact resolving evidence: explicit transition rule plus real-store/HTTP
  current-version repeat-resolution denial; reopened original evidence and
  exact stale sets remain unchanged. An explanation-only resolution never
  invalidates, while independent correction causes remain effective.
* Decision route: direct planner correction; no user response.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Make the new field's dual-entitlement projection explicit

* Related IDs: FR5, A2/A6, R1/R4, P02-T02, C5.
* Evidence: store.py:366-368 deep-copies the complete case. In projection.py,
  redact_staff_detail at :155-190 removes selected known fields rather than
  arbitrary new fields. It captures RESIDENT_FIELDS for resident-view roles and
  restores them after hold_notes. RESIDENT_FIELDS at
  resident_decisions.py:34-35 does not currently contain challenges.
  hold_notes does not establish a general allow-list for new request,
  explanation, route and reference field names.
* Concern: merely adding the collection to the case and reusing existing
  resident-field handling does not implement FR5. Leaving it outside the
  existing removal list leaks to other staff; putting it into RESIDENT_FIELDS
  alone restores raw content for resident-view actors without reason rights.
  The current contractor allow-list does not prove either staff-denial case.
* Impact: sensitive challenge narrative or supplied references can escape the
  required resident-view AND reason boundary.
* Smallest useful change: specify explicit removal of both challenge collection
  and catalog unless both entitlements hold, without changing existing resident
  decision projection or #406. Keep general audit details free of challenge
  narrative/reference canaries, or apply an equally explicit existing audience
  boundary there. Authorized evidence export must agree on stale flags without
  leaking restricted challenge content through another read path.
* Action owner: planning parent, P02-T02 and P01-T01.
* Exact resolving evidence: explicit projection placement; actual HTTP GET and
  write-response canary denials for a resident-view role lacking reason rights,
  a reason-enabled role lacking resident-view rights, and a contractor.
  Positive authorized detail/UI evidence is required too. Check any newly
  populated audit/export fields, not just the challenge panel's visibility.
* Decision route: direct planner correction; no user response.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Lock a non-vacuous dependency and historical-review oracle

* Related IDs: R2-R3/R5, A1-A4, P01-T01, P03-T01.
* Evidence: details:29-35 require independent ID sets but say actual human
  reviews are created through resolve_priority "where possible." Details:64-68
  define proposal-, case/hash- and policy-version matching. The public fixture
  and store.py:772-891 support actual workflow-only generation and acceptance;
  no missing real-model dependency prevents creating retained human reviews.
* Concern: the proposed proof does not yet require a nonempty actual reviewed
  dependent set. Nor does it explicitly disambiguate a same-policy proposal on
  another case, which is dependent, from the same source hash on another case,
  which is not. Identical generated content must not make separate proposal IDs
  the same proposal. An empty review set or an overbroad per-case oracle could
  pass superficially exact comparisons.
* Impact: the defining selective-invalidation behavior could remain unproven
  while the bounded acceptance is reported complete.
* Smallest useful change: add a compact explicit fixture/expected-ID manifest:
  separate proposal IDs even for identical content; same case/hash matches only
  that source dependency; same policy version matches across applicable cases;
  different policy versions and non-priority contracts remain unaffected.
  Require nonempty accepted/edited human-review examples made by actual calls,
  an explanation-only control and multiple correction causes.
* Action owner: planning parent, P01-T01.
* Exact resolving evidence: revised acceptance matrix and reserved cases within
  the 12-core/6-HTTP/one-browser bounds; exact nonempty expected proposal/review
  ID equality after reopen; original recommendation/disposition bytes unchanged;
  protected-state equality and successful independent manual/hazard actions.
  Failing-first output must fail the intended missing feature, not fixture setup.
* Decision route: direct planner correction; no user response.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Distinguish issue-specific SQLite proof from the general SQL Server gate

* Related IDs: R4/R7, A5, P01-T01/P03-T01/P04-T01, C7-C8.
* Evidence: test_resident_decisions.py:2412 onward gates inherited
  MssqlResidentControls on ZF_RESIDENT_MSSQL. tools/rpi-checks.py:28-36 lists
  SQL_SELECTORS, none of which select this class or test_resident_api;
  src/api/tests/test_mssqlstore.py does not import the resident owner modules.
  The runner's SQL phase at :1330-1362 uses those fixed selectors and removes
  its container. Extra tests at :1530-1543 run afterward with tests_env only,
  without that SQL endpoint or the resident opt-in.
* Concern: a full 17-group pass does not demonstrate these new challenge cases
  on SQL Server. Saying optional extra selectors can supplement SQL coverage
  is not a runnable mechanism in this runner. This does not invalidate actual
  JSON/SQLite transaction tests or the existing general SQL Server gate.
* Impact: validation can overclaim store coverage, or select an opt-in test that
  skips/fails after its intended owned endpoint is gone.
* Smallest useful change: explicitly label issue-specific store evidence
  JSON/SQLite and the 17-group SQL Server evidence general regression only.
  Remove any assumption that the shown extra-test recipe supplies the resident
  SQL environment. If additional native-SQL challenge acceptance is retained as
  required, name an actually supported owned-local execution mechanism before
  claiming readiness; do not change the runner/matrix, target a cloud database
  or treat skipped tests as proof.
* Action owner: planning parent for evidence scoping; gate coordinator only if
  additional owned-local execution is required.
* Exact resolving evidence: revised validation table naming backend, selector,
  opt-in, endpoint lifecycle and expected non-skipped cases, or an explicit
  native-SQL issue-specific coverage limitation. Existing required 17 groups
  and original adverse evidence remain unchanged.
* Decision route: direct planner correction for honest bounded evidence.
  A runner/matrix expansion would be a significant scope change, not an implied
  recommendation or authorization.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Separate the frozen-gate obligation from an unusable execution recipe

* Related IDs: R7, P03-T01/P04-T01, C8.
* Evidence: details:98-99 prescribe the system-temporary heavy lock and :120
  hard-code a previous issue's system-temporary tool directory.
  tools/rpi-checks.py:1675-1680 creates/opens the hard-coded lock; :1711-1716
  requires a newly created external output directory. Those file operations
  cannot be performed in the restricted file-operation context of this task.
* Concern: the P04 gate is a real execution dependency, not merely a command to
  copy. Changing TMPDIR or moving the receipt alone cannot relocate the runner's
  hard-coded shared lock. Silently bypassing serialization, changing the runner,
  or substituting the prior issue's receipt would violate the agreed gate.
* Impact: a correct implementation could be falsely reported fully validated,
  or forbidden file operations attempted to satisfy the plan.
* Smallest useful change: retain the unchanged full gate and exact-head receipt
  requirement, but explicitly mark local gate execution blocked in an
  incompatible executor and hand it to the coordinator's eligible execution
  context. Replace the assumed borrowed PATH with verified tool prerequisites.
  No code or runner change is authorized by this finding.
* Action owner: planning parent to state the blocker; coordinator to provide an
  eligible execution context within existing authority.
* Exact resolving evidence: revised P04 preconditions and blocker/handoff state;
  later, an actual new external 17-group receipt and successful verification
  bound to the frozen candidate/base, with no subsequent commit. If no eligible
  context is available, retain Blocked/Not run for that gate and do not publish.
* Decision route: planner-owned execution correction, not a divergent product
  decision. No user response is needed to preserve an honest blocked state;
  restrictions must not be overridden to obtain a pass.

## Strengths and Residual Risk

* The retained-priority slice is supported by existing policy, actual workflow
  generation and human-disposition contracts. Rejecting a new cross-assistant
  graph is appropriate, not a missing feature for this agreed iteration.
* Capturing hashes only for new records, keeping historical source Unknown, and
  freezing target plus human-decision tokens avoid invented provenance.
* Existing resident _operation and server.py:963-978 provide valuable rollback,
  current staff replay and truthful committed-outcome handling. Reuse should
  preserve them, not replace the recorder identity contract.
* Native forms, local draft protection and real Chromium are credible choices.
  The unrelated-refresh rebuild in app.js:445-450 must actually be exercised;
  navigation/beforeunload handling alone cannot establish draft safety.
* The no-retaliation/no-delay boundary is rightly expressed through unchanged
  ranking/state and manual/hazard availability, not a purported operational
  fairness or legal acceptance.
* Whole-system AC-071, other assistant/form integrations, qualified human/legal/
  RAI acceptance, resident comprehension and live-platform acceptance remain
  explicitly unmet. They are not reasons to expand this slice.

## Questions or Blocking Evidence Gaps

* No unresolved product-policy question requires a user answer. PC-001 through
  PC-006 can be resolved by the planning parent using current direction.
* PC-007 is an execution prerequisite for P04, not permission to weaken the
  gate. The source contract is inspectable; actual gate availability/pass is
  not established by this critique.

## Limitations

* No implementation exists in the supplied candidate. Findings concern
  readiness, not independently reproduced implementation failures.
* Initial status showed the four supplied research/planning/session tracking
  files untracked over the specified base. They were left untouched; no branch,
  commit, PR or remote state was changed.
* The live issue was not reread. Its requirements and scope were supplied by the
  caller and research; no claim of a new live dependency/currentness check is
  made.
* This critique did not execute Chromium, component tests, SQL containers or the
  full gate. Those remain implementation/validation obligations.
* Research, plan and details input SHA-256 values at assessment:
  * Research: 7a4dc049ba4de04cd6cf9d2ccc06656d7dd36526e3e1304d1c370339a9f0778a
  * Plan: 081f92397fd75502a789bb43b492809ef73a4289029a78bc926b1c7eb37a6447
  * Details: dc8709ea513d537596f76aecf9b3dcc6631df23f1fb7b9a04245f691061ae625

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: amend P02-T02 to require writer-time dependent-correction
  validation for accept/edit, reserve the two-store race proof in P01, then
  disposition the remaining complete finding set in the plan/details.
* User response required: no. No significant/divergent product choice is
  outstanding. Preserve this original critique without a repeat pass.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md | Supplied bounded research and evidence pointers |
| .copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md | Reviewed final-candidate plan, unchanged |
| .copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md | Reviewed phase details, unchanged |
| .copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md | This immutable original independent critique |

## Next Steps

Return Revise to the active planning parent for direct disposition and plan
finalization without another critique. After those revisions, the parent may
continue the authorized ordered implementation and one original Review. P04
must remain blocked until its execution prerequisites are genuinely available.
No user action or new RPI invocation is required. This critique stops here.
