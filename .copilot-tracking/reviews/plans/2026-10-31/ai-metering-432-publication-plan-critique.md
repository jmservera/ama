<!-- markdownlint-disable-file -->
# RPI Plan Critique: AI metering publication remainder

## Metadata

* Task ID: 432-publication; slug ai-metering-432-publication.
* Critique date: 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md
* Critique execution status: Complete.
* Assessed workspace HEAD: 1c912b29f0bf1f88b1b42570de2e25f02167064c.
* Observed local origin/main: a75bbdffa51ae34b1fcf779250f1f553d566ee93.
* Execution boundary: one independent child critique; no implementation, Git mutation, heavy validation, private data access or delegation.

## Inputs and Criterion Boundary

* Caller direction: continue the remaining full RPI loop on feat/ai-metering-432; non-rewriting main merge with main rubric on conflict; requested outer flock with a 1,800-second wait; optional validated inherited descriptor; pip only; no secrets; normal push and main PR.
* Authorised exception: known main B023/test_chat_panel failures may be documented and publication may proceed if fix/gate-baseline-b023 has not landed. This is not a passing gate or permission to disregard unrelated failures.
* Supplied research: .copilot-tracking/research/2026-10-31/ai-metering-432-publication-research.md, Q1-Q3, C1-C5/W1.
* Direct evidence: tools/rpi-checks.py heavy_lock/main, Runner.command/run/schedule; tools/test_rpi_checks.py existing ownership, interruption and identity patterns; src/README.md complete-gate and publication contracts.
* Preservation evidence: .copilot-tracking/changes/2026-10-31/ai-metering-432-review-findings-changes.md; .copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-review-findings-state.json; .copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-review.md.
* Project intake: docs/case_study_48_original.md, opening/current framing in docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. No consequential legal, business or financial conclusion is assessed.
* Acceptance boundary: descriptor/path identity and fail-closed admission; continuous exclusion and closure ownership; at most five added runner-test methods with no removals or parent-metering test changes; committed clean exact candidate; honest full-gate/exception evidence; one child independent Review; authorised publication with Refs #432 and retained human/hosted gates.
* Read-only status showed four untracked child planning/research/state artifacts, not a presently gate-ready clean candidate. P01-T02's planned evidence commit addresses this; no existing work was moved or modified.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C2/C5; P01-T01 inherited-lock composition | Covered | Validated duplicate/nonblocking flock is compatible with the actual independent-open deadlock and the caller-owned outer exclusive descriptor. |
| P01-T01 invalid/wrong/symlink/contended FD | Covered | Explicit regular-file lstat/fstat identity checks and contention rejection; require real descriptor semantics rather than mocked flock success. |
| P01-T01 normal/exception closure and subprocess ownership | Partial | Caller preservation is specified; duplicate disposal, original inheritable FD isolation and main/verify wiring need resolving tests, PC-003. |
| P01-T01 test cap/regression/static scope | Covered | Maximum five new methods, no removals, existing runner suite and related static checks; no parent-module expansion is needed. |
| P01-T02 ancestry, identity and original evidence | Covered | Fetch/merge, privacy-safe identity, trailer, clean committed evidence and immutable parent adverse outcomes are explicit. |
| C3; P02-T01 exact gate/Review/publication ordering | Partial | Post-Review evidence commits followed only by another gate cannot provide an independently assessed final HEAD, PC-001. |
| Q3; P02-T01 known baseline exception | Partial | Authorisation is explicit, but failure classification and blocked downstream coverage need an exact evidence contract, PC-002. |
| P02-T01 continuous outer admission | Covered | Queued outer flock is expressly authorised and outranks the older nonqueued instruction; no unlock/reacquire or foreign-owner interruption is proposed. |
| C4/W1; source-only and whole-issue acceptance | Covered | Refs #432, original adverse Review and RV-006 operational/presentation gaps remain distinct. |
| Publication/hosted/human boundaries | Covered with correction | Normal push/main PR and retained approvals are credible once PC-001/PC-002 are disposed. |

## Verdict

* Verdict: Revise.
* Severity summary: two High, one Medium; zero Critical or Low.
* Rationale: the minimal inherited-descriptor implementation direction is credible and authorised. The final Review ordering, exception evidence and decisive ownership tests need direct parent-owned corrections before implementation/publication. None requires reopening the user's selected direction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Post-Review commits leave the publication HEAD without its required exact-head assessment

* Related IDs: C3/C4; P01-T02; P02-T01; acceptance criteria for one child Review and exact candidate publication.
* Evidence: the phase details permit final committed review/evidence followed by a fresh gate, prohibit repeating the child Review, and correctly prohibit claiming assessment of future commits. The plan separately requires immediate verification before exact-head assessment and push. src/README.md:208-220 requires current-base, exact-head independent assessment; a new gate proves checks, not an independent assessment of a later commit.
* Concern: the permitted post-Review commit path changes HEAD even if it changes only tracking evidence. The plan does not supply a sequence that both preserves the sole Review's exact-head boundary and publishes that independently assessed candidate.
* Impact: a passing final receipt could be published alongside a Review of a different HEAD. Honest historical labels do not fulfil the final exact-head assessment requirement.
* Smallest useful change: freeze all required in-tree implementation and evidence before the final gate and the sole child exact-head Review. Specify where subsequently produced Review/receipt evidence remains externally owned so it does not dirty or change that candidate before immediate verification and normal push. If archival commits are required, route them as later work rather than silently treating them as independently reviewed. Specify a stop/routing condition for any source/base/identity change after the sole Review.
* Action owner: planning parent / automatic RPI Agent.
* Parent-compatible disposition: accept as a direct sequencing correction; retain both the original parent adverse Review and the child's original assessed HEAD/verdict without another critique or replacement Review.
* Exact resolving evidence: revised P01-T02/P02-T01 state an executable single-Review ordering and external evidence locations; implementation closeout records one final HEAD/base, matching receipt identity and child Review assessed identity, a clean candidate and immediate pre-push verification at freshly fetched main. Any baseline-exception route names the same candidate identities without claiming receipt verification.
* Decision route: direct planner correction. No unresolved significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Baseline-exception evidence must distinguish a failed full selection from actual complete execution

* Related IDs: Q3/C3; P02-T01; known B023/test_chat_panel exception; full SQL/browser/images/scanner acceptance.
* Evidence: tools/rpi-checks.py:1920-1958 propagates failed prerequisites to blocked groups. project-api precedes browser and mssql in the shared-API chain. Runner.run can stop before scheduling on setup/preflight failures at tools/rpi-checks.py:2016-2041. Its receipt scope is derived from selection, while completed/executed groups are separately recorded at tools/rpi-checks.py:2076-2111. Phase details say to retain a known baseline failure and proceed, but do not define how to classify all other failures and nonexecution.
* Concern: a receipt marked scope full can still omit required integration execution. A known API failure can block browser/SQL transitively; unrelated scanner, prerequisite or cleanup failures can coexist. Naming B023 or test_chat_panel alone neither proves baseline provenance nor establishes that every remaining failure is covered by the exception.
* Impact: the PR may overstate full-gate coverage or use the narrow exception to conceal independent blockers. Conversely, treating every transitively blocked group as an unrelated failure would improperly negate the user's explicit permission to proceed.
* Smallest useful change: require a per-group/per-command exception matrix: exact candidate/base/tool identities, logs/exits/test IDs or diagnostic locations, completed versus failed versus not-executed groups, and causal prerequisite links. Distinguish directly allowed baseline failures and their explicitly disclosed downstream nonexecution from independent failures, unexpected skips, cleanup/ownership or identity defects, which still block. Refetch before final publication as well as on failure; record evidence of the fix's actual main ancestry, not merely an open/absent branch or PR name. Merge a landed fix and rerun at the new candidate.
* Action owner: planning parent / automatic RPI Agent.
* Parent-compatible disposition: accept as an evidence/classification correction, preserving the authorised baseline exception and the runner's fail-closed receipt semantics. Do not add a skip, fabricated success or unrelated baseline fix.
* Exact resolving evidence: revised P02-T01 contains the classification and freshness rules; the final external receipt/log matrix identifies every required group's actual status, all failure roots and any causal blocked descendants. The PR cites that matrix and the current-main fix check, states known exceptions and omitted integration coverage explicitly, and either cites passing immediate verification or expressly states failed/unverified evidence.
* Decision route: direct planner correction. The known-failure publication choice is already authorised; no new user decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The five-method test budget needs explicit duplicate, subprocess and entry-point lifecycle assertions

* Related IDs: C5; P01-T01; non-functional child-subprocess ownership and continuous Runner.run/verify exclusion.
* Evidence: phase details specify caller-FD survival and os.dup's non-inheritable default, but do not name proof of duplicate closure or original-FD exclusion from child processes. The real util-linux inherited descriptor is intentionally inheritable. tools/rpi-checks.py:1239-1247 currently uses Popen's default close_fds behavior; tools/test_rpi_checks.py:491-505 tests only the standalone redirected-open path. main holds the helper around both run and verify at tools/rpi-checks.py:2346-2365.
* Concern: helper-only tests can pass while CLI wiring fails to forward the supplied FD, verification occurs outside the context, an error leaks a duplicate, or a spawned child retains the original inheritable FD despite the duplicate being close-on-exec.
* Impact: the requested full command can still deadlock or the shared lock can outlive its authorised owner; merely checking the caller remains open cannot detect these defects.
* Smallest useful change: allocate explicit assertions within at most five new methods: actual util-linux composition; wrong/closed/negative/nonregular/symlink/contended cases; normal/exception and pre-yield cleanup of the runner-owned duplicate with caller validity preserved; descendant FD exclusion and independent-open acquisition after the outer owner exits; lightweight main forwarding plus run/automatic-verify lock lifetime. Parameterize related cases and patch heavy work only, not the descriptor/flock semantics being established.
* Action owner: planning parent, then implementation owner.
* Parent-compatible disposition: accept as a bounded test-evidence refinement, retaining every existing method and parent-metering module unchanged. No heavy gate or real shared-lock contention is needed for these tests.
* Exact resolving evidence: revised P01-T01 names those assertions and a maximum-five-method allocation; passing runner tests show duplicate fstat failure after closure, caller fstat success across normal/exception exits, bounded outer-process termination, child inability to access inherited lock handles, refusal during run/verify and acquisition after caller release. The diff confirms at most five added methods and zero removals.
* Decision route: direct planner correction. No user response required.

## Strengths and Residual Risk

* The optional CLI descriptor is a narrow, explicit composition interface, not an environment bypass or receipt-trust relaxation. Default self-locking behavior is retained.
* The caller expressly authorised queueing on the existing shared lock. The older nonqueued README/parent-state direction is historical and must not be used to demand another routine approval or reject the selected path.
* Wrong-file/nonregular/symlink/contended inputs, duplicate-only closure and no unlock/reacquire are correctly selected controls; the findings tighten their proof and ownership preconditions.
* The supported caller uses a pre-held exclusive outer descriptor. Nonblocking flock proves or acquires exclusive ownership, not historical acquisition provenance; README wording should not claim otherwise. The caller retains responsibility for releasing its original descriptor. This observation does not add an unsupported requirement to reject an otherwise matching unlocked descriptor.
* Original source-only adverse Review and later correction observations remain immutable. Refs #432 is correct because OD-51, applicable numerical prices, billing attribution, held-out benefits, resident/historical joins and actual pitch delivery remain unproven.
* Local tests and receipts do not replace independent assessment, human approval, hosted checks, resident consent, professional judgement or spending authority.
* The baseline exception is explicitly accepted adverse evidence. Neither its authorisation nor an all-selected receipt establishes complete execution or operational acceptance.

## Questions or Blocking Evidence Gaps

* No user question is required. All three findings are compatible parent-owned corrections within the confirmed scope.
* No fresh upstream lifecycle check or full-gate result was obtained in this critique. The planning parent must perform the already-planned current-main checks and candidate validation.
* The supplied probe proves outer-FD composition, not the unimplemented main/verification/duplicate-cleanup test coverage identified in PC-003.

## Limitations

* This is plan credibility assessment, not implementation Review or runtime validation. No tests, gate groups, foreign lock probe or subprocess experiment ran.
* Research's historical probe and upstream observations are treated as supplied evidence, not independently repeated current observations. No private dataset, credentials, paid model call or external GitHub state was accessed.
* Only the child critique artifact was written. Plan/details/research/state, original parent Review and correction artifacts, source and Git state remain unmodified.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent / automatic RPI Agent.
* Smallest next action: reconcile all three findings directly into the child plan/details and record compatible dispositions; freeze the single-Review publication sequence before P01 implementation.
* User response required: no.
* Critique execution is Complete; verdict remains Revise. This is the one complete finding set for the supplied boundary, not an invitation to another critique pass.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md](.copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md) | Assessed child plan, unchanged. |
| [.copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md](.copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md) | Assessed phase details, unchanged. |
| [.copilot-tracking/research/2026-10-31/ai-metering-432-publication-research.md](.copilot-tracking/research/2026-10-31/ai-metering-432-publication-research.md) | Supplied research, unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-publication-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-publication-plan-critique.md) | This single independent critique. |
| [.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-review.md](.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-review.md) | Preserved original adverse parent Review. |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Actual lock, execution and receipt contracts. |
| [tools/test_rpi_checks.py](tools/test_rpi_checks.py) | Existing isolated ownership/regression patterns. |
| [src/README.md](src/README.md) | Current exact-candidate gate/publication policy. |

## Next Steps

No user action is required. The active planning parent should apply PC-001 through PC-003 dispositions directly, finalize the child plan without another critique, then continue the already-authorised loop only after its gates pass or the precisely evidenced baseline exception applies. This reviewer stops after the single critique.
