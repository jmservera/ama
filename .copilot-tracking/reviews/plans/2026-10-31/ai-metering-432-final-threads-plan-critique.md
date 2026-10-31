---
title: AI metering final threads independent plan critique
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-432-pr-602-final-threads
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-final-threads-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md
* Research: .copilot-tracking/research/2026-10-31/ai-metering-432-final-threads-research.md
* Critique execution status: Complete
* Candidate source HEAD: 3d4a8d324b5324c2cabd1e037bde3dcbf6ba7f6f
* Independence: one assessment of the supplied final candidate; no nested agents, implementation changes, or repeated critique.

## Inputs and Criterion Boundary

* Caller requirements: correct the three named PR #602 threads, Refs #432;
  preserve bounded mismatch evidence through worker shaping, return complete
  reports despite backend holds, and deliver consistent persistent manual
  fallbacks at the real 9,999 -> 10,001 threshold.
* Confirmed decisions: automatic RPI correction, privacy-safe commit and
  ordinary push, three thread replies/resolutions, CI instead of the full local
  gate, no force push or PR merge. These decisions are not reopened here.
* Locked tests: src/api/tests/test_ai_consumption_api.py only, at most four
  additional methods plus fixture controls/helpers, no removals.
* Supplied evidence: the three RPI input artifacts and their C1-C7 source
  pointers; relevant provider, assistant shaping/completion, worker transport,
  report handler, financial ledger, draft, priority, chat, SQL transaction,
  continuity-publication, and existing composed-test contracts.
* The three supplied discussion URLs were read through authenticated GitHub
  GraphQL. All three remain unresolved; PR HEAD matches candidate source HEAD.
  Their concerns match the research summaries.
* Acceptance boundary: FR1-FR4, AC1-AC5, P01-T01 through P02-T03. This critique
  assesses implementation credibility, test feasibility, and publication
  sequencing, not delivered functionality or live authority.
* Project context: original case study, addendum, knowledge-base index and
  owner's memory were consulted for the existing human/manual boundaries.
  No private dataset, paid provider, deployment, or external research was used.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1, AC1, C1-C2, P01-T01 | Partial | Specific mismatch handling is credible, but the durable model field and worker shaping bound are not specified; PC-002. |
| FR2, AC2, C3, P01-T02 | Covered | Validate parameters before reading the ledger; catch only DispatchHeld around the SQL consumption read and retain ordinary report sections. |
| FR3, AC3, C4-C5, P01-T03 | Covered for legacy/priority | Publication-only helper, preserved comparison output, manual shown fields and a second durable save address the named failures without loosening output(). |
| FR3-FR4, AC3, C6, P01-T03 | Partial for chat | Predicted sequence plus expected_version does not make separate financial/message commits atomic; PC-001. |
| FR4, C7 | Covered with required fault cases | Missing output joins already make reporting incomplete; tests must also prevent a phantom chat join after save/conflict failure. |
| AC4, P02-T01-P02-T02 | Partial | Four methods can cover the boundary using subtests/helpers; add PC-001 fault/interleaving cases and PC-002 bound cases within that cap. |
| AC5, P02-T02 | Partial | Original independent Review is preserved, but unconditional deferral of open findings can leave this task's acceptance unmet; PC-004. |
| AC5, P02-T03 | Partial | Owner-selected CI gate is recorded, but push/reply/resolve sequence lacks a required successful exact-head CI checkpoint; PC-003. |
| Non-functional requirements and non-goals | Covered | Strict immutable attribution, no schema/admission-limit change, no paid call, no source closure of remaining #432 live gaps. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 3 Medium, 0 Low.
* Rationale: the plan addresses all three review concerns and can fit the
  locked test budget, but chat pre-linking creates a new attribution correctness
  risk. Worker model preservation and final publication dispositions require
  explicit resolving steps before implementation/publication.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Chat pre-linking can commit attribution to an unsaved or different message

* Related IDs: FR3-FR4, AC3-AC4, C6-C7, P01-T03, P02-T01.
* Evidence:
  * .copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md, P01-T03, selects financial linking before final chat message save using a predicted sequence under Store.lock.
  * src/core/src/zava_forward/core/chat_panel.py:403-412 currently obtains the actual saved message sequence before output linking.
  * src/core/src/zava_forward/core/chatthreads.py:184-195 gives SQL message writes their own transaction; :317-342 checks ownership, active status and expected_version before insertion.
  * src/core/src/zava_forward/core/sqlstore.py:103-149 implements a process-local re-entrant lock; :241-245 supplies a separate assistant connection.
  * src/core/src/zava_forward/core/assistants.py:425-441 commits the financial transaction independently.
  * src/core/src/zava_forward/core/ai_consumption.py:608-652 makes the output join immutable; :875-936 considers a root joined without checking for a persisted chat message.
* Concern: expected_version detects a later writer, but only after the
  predicted financial join has committed. A second Store/process can advance,
  archive or delete the thread despite this Store's lock. The message write
  can also fail for a persistence reason. Propagating the conflict/error leaves
  the financial join behind. A subsequent writer can occupy the predicted
  sequence, causing that immutable join to identify another message; even
  without that writer, reporting can mistake an undelivered result for a
  joined output. Ineligible chat joins prevent proposal acceptance, not this
  completeness error.
* Impact: the correction could satisfy the capacity happy path while
  weakening original immutable attribution and truthful incomplete/Unknown
  reporting. This is a introduced design risk, not a request to expand chat
  permissions or add a public message-edit API.
* Smallest useful change: replace unconditional separately committed pre-linking
  with finalization tied to the actual message being saved. A small private
  finalization hook can use the existing SQL message transaction and pass that
  same connection to output(..., db=...), deciding fallback on DispatchHeld
  before committing the final message. Avoid nested financial transactions.
  For MemoryRepo/JSON, a simpler alternative is to save first, use its actual
  sequence, and on a publication hold replace only that just-created message
  with FALLBACK under the existing Store lock and persist again. That needs
  targeted internal finalization, not a public edit API or schema. Keep
  non-hold errors propagating. Do not treat a read-only preflight as eliminating
  a later ledger race. Specify the selected backend-safe approach explicitly.
* Action owner: planning parent, then implementation parent.
* Exact resolving evidence:
  * Revised P01-T03 states transaction/lock boundaries and how a failed
    message write cannot leave a join attributed to a later occupant.
  * Within the fourth permitted test method, SQL/JSON subtests inject
    publication RuntimeError and message/save failure; errors propagate and
    no financial join can identify an unsaved or different message.
  * A deterministic second SQL Store/connection advances the same thread
    between sequence observation and finalization. Conflict propagation or
    actual-sequence finalization is demonstrated, with no wrong immutable join.
  * Existing successful chat metering assertions still link the actual
    persisted assistant sequence with eligible=False.
  * Real-capacity chat subtests persist FALLBACK, empty evidence, workflow-only
    model, unresolved/Unknown receipt, exactly one provider request, and a
    missing join that remains incomplete when read capacity is restored.
* Decision route: direct planner correction. The owner has already selected
  consistent delivery, immutable attribution and no public message-edit API;
  none requires this particular predictive design. No user response needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The bounded mismatch field is not defined through worker result shaping

* Related IDs: FR1, AC1, C1-C2, P01-T01, P02-T01.
* Evidence:
  * .copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md, P01-T01, bounds the exception and receipt returned_model to <=512 but does not specify the shaped field or update shape_result().
  * src/core/src/zava_forward/core/ai.py:96-118 retains returned_model in the receipt but evidence initially has model=None.
  * src/core/src/zava_forward/core/assistants.py:322-338 copies model, not returned_model, and truncates all selected string fields to 120 characters.
  * src/agents/src/zava_forward/agents/dispatch.py:226-244 calls shape_result() before ResultMessage serialization.
  * src/core/src/zava_forward/core/assistants.py:891-903 uses envelope.model for the returned-model evidence in serving_attestation.
* Concern: bounding the exception/receipt alone does not define which model
  survives the worker allowlist. Putting the value only in returned_model
  drops it; putting it in model preserves only its first 120 characters.
  A closed model-mismatch outcome can still survive, but the proposed <=512
  evidence contract is not implemented by the existing shaping contract.
* Impact: direct-provider tests can pass while worker completion loses the
  actual bounded returned model. Long but permitted model evidence cannot be
  traced faithfully to the attestation.
* Smallest useful change: explicitly map the mismatch exception's safe model
  to an allowlisted durable field, preferably the existing model field, and
  give model its own consistent <=512 bound through shape_result(). Keep
  provider/deployment and other metadata bounds unchanged. Normalize
  oversized/non-string returned model values to None rather than copying
  arbitrary objects. Handle the closed mismatch outcome even with None,
  withholding text/output and suspending the task's released record.
* Action owner: planning parent, then implementation parent.
* Exact resolving evidence:
  * Revised P01-T01 names the durable field and the model-specific shaping
    rule, plus the model-mismatch completion branch.
  * One added mismatch test method uses fixture controls/subtests for a
    different short string, a 121-512-character string, an oversized string,
    and a non-string. A valid <=512 string survives exactly; invalid values
    are None in shaped/serialized/task/audit evidence.
  * The real loopback -> AgentWorker.handle -> ResultMessage JSON roundtrip ->
    Assistants.complete path retains settled usage, no raw provider text or
    proposal output, mismatch attestation, quarantined state, suspended release,
    and no request on a subsequent execute/claim attempt.
  * Existing ordinary provider-failure test still produces retryable pending
    rather than mismatch quarantine.
* Decision route: direct planner correction; no divergent user decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Thread resolution is not conditioned on the selected exact-head CI gate

* Related IDs: AC4-AC5, P02-T02-P02-T03, owner-selected publication decision.
* Evidence: P02-T03 specifies commit, ordinary push, reply and resolve in
  sequence, then says to report pending/failing hosted checks accurately.
  The plan's user decisions instead select CI as the publication gate.
* Concern: accurate disclosure of pending/failing checks is not a passing
  gate. The current phase permits resolving all three threads before required
  CI on the final pushed candidate succeeds.
* Impact: source completion could be declared for a candidate whose required
  validation is still pending or fails, despite the explicitly selected gate.
* Smallest useful change: insert an explicit checkpoint after the ordinary
  push and before final thread resolution: await required CI for that exact
  PR head, correct relevant failures with ordinary further commits, and verify
  the new head's checks again. A preliminary reply may say validation is
  pending, but resolution must wait for the required successful checks.
  Do not reinstate the full local gate or infer hosted/human/live approval.
* Action owner: planning parent and publication parent.
* Exact resolving evidence: P02-T03 names the wait/verify step; closeout
  evidence records final commit SHA, required check names, successful
  conclusions and run URLs, a matching PR head, and the subsequent three
  precise thread replies/resolutions. Pending/failed gates leave resolution
  incomplete with the blocker accurately recorded.
* Decision route: direct application of the owner's CI-gate decision;
  no user response needed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Unconditional deferral of Review findings conflicts with automatic acceptance correction

* Related IDs: FR1-FR4, AC1-AC5, P02-T02-P02-T03.
* Evidence: P02-T02 instructs the parent to preserve one independent Review's
  original outcome and "route open findings to later work without repeating
  Review." The caller authorizes automatic full RPI correction; AC1-AC4 still
  require the scoped behavior and validations.
* Concern: retaining the original Review outcome is correct, but the deferral
  instruction does not distinguish new out-of-scope work from a finding that
  disproves a current acceptance criterion. It permits publication/resolution
  with an uncorrected scoped correctness defect.
* Impact: passing tests/CI would not resolve an independent Review's evidenced
  violation of the three thread contracts.
* Smallest useful change: preserve the single original Review verbatim and
  correct actionable in-scope findings automatically, recording a separate
  disposition with exact corrective commit and resolving tests. Revalidate
  the final candidate and its CI. Defer only genuinely out-of-scope items or
  explicitly accepted residual risks; do not manufacture a passing Review or
  run another critique/Review. If a remaining criterion cannot be resolved,
  record a blocked closeout and leave its thread unresolved.
* Action owner: planning parent, then implementation/publication parent.
* Exact resolving evidence: revised P02-T02 distinguishes in-scope correction
  from deferral; the eventual changes/closeout artifact maps every original
  Review finding to an evidenced correction, accepted residual risk, or
  genuine out-of-scope follow-up, with no unresolved finding that invalidates
  the claimed thread resolution. Original Review status remains unchanged.
* Decision route: direct application of existing automatic correction
  authority. A future genuinely divergent scope decision must be reported,
  but none is required to resolve this planning finding.

## Strengths and Residual Risk

* Separate parameter validation and narrow DispatchHeld handling correctly
  retain evaluation/live/registry without swallowing arbitrary backend errors.
* Preserving strict output() and adding only publication-specific handling
  protects original immutable joins and financial admission/settlement bounds.
* Legacy and priority fallback plans preserve the original AI comparison
  instead of relabelling AI content as manual output.
* Exactly four added test methods are feasible: mismatch subtests, HTTP report
  hold/invalid-input subtests, six backend/publication capacity subtests, and
  publication/message-failure/interleaving subtests. Fixture helpers remain in
  the same external test file; no removal is needed.
* Capacity fixtures must count actual financial records after authority and
  ensure matching model/valid bounded usage so reservation and completion add
  exactly two events. Recovery should preserve ledger evidence, for example
  through a test-only enlarged read bound, rather than deleting history.
* Existing tests already cover worker failure/revocation/fence, successful chat
  attribution, legacy/priority unexpected output errors, and review repairs.
  Retain these contracts and run the related suites.
* Source-only synthetic evidence does not satisfy actual Azure price/billing,
  live approval, resident/historical joins, or the remaining #432 gaps.
  Refs #432, rather than issue closure, remains appropriate.

## Questions or Blocking Evidence Gaps

* No decision-critical research gap prevents this assessment.
* No current user response is required. All four findings are direct planner
  corrections inside supplied authority and scope.

## Limitations

* This is a plan critique against the existing source and test contracts, not
  an implementation Review. No tests, static checks or CI were executed here.
* No new implementation exists in the supplied candidate, so the resolving
  evidence listed above is required future evidence, not a claimed result.
* Local SQL transaction contracts were inspected; deployed Azure SQL behavior,
  live concurrency and provider attestation were not validated.
* The worktree initially contained the parent's untracked plan/details/research
  and state artifacts. They were left untouched. This critique writes only its
  caller-specified output.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: replace separately committed predicted chat pre-linking
  with backend-safe actual-message finalization, then apply PC-002 through
  PC-004 directly and finalize the plan without another critique.
* User response required: no.

| [.copilot-tracking/plans/2026-10-31/ai-metering-432-final-threads-plan.md](.copilot-tracking/plans/2026-10-31/ai-metering-432-final-threads-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md](.copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md) | Assessed implementation and publication details |
| [.copilot-tracking/research/2026-10-31/ai-metering-432-final-threads-research.md](.copilot-tracking/research/2026-10-31/ai-metering-432-final-threads-research.md) | Supplied focused research and thread pointers |
| [.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-final-threads-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-final-threads-plan-critique.md) | Complete single independent critique |

## Next Steps

The active planning parent applies PC-001 through PC-004 directly, preserves this
original Revise outcome, and finalizes without repeating critique. Continue the
authorized implementation, single independent Review, ordinary commit/push and
exact-head CI gate; resolve only evidenced threads after that gate. No user
action is required. This critique invocation stops here.
