<!-- markdownlint-disable-file -->
# RPI Plan Critique: Per-user agent chat and memory

## Metadata

* Task ID: 157
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/agent-chat-157-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/agent-chat-157-phase-details.md
* Critique execution status: Complete
* Candidate branch: feat/agent-chat-157
* Assessment count: One independent final-candidate assessment.

## Inputs and Criterion Boundary

* Caller requirements: ordered full RPI loop, one PR on the supplied branch,
  reuse existing assistants/provider/store, local targeted tests only, no Azure,
  secrets, private datasets, uv or full --all gate. At most one locked --changed
  gate is permitted; the parent selected targeted checks instead.
* Supplied evidence: the plan, phase details and
  .copilot-tracking/research/2026-10-27/agent-chat-157-research.md, including
  C1-C7, W1-W3 and their recorded decision boundaries.
* Context read: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory is context, not approval evidence.
* Bounded source inspection: existing chat panel/isolation/privacy, agents
  adapter/provider worker/evaluator, AI admission implementation, API turn
  routes, chat UI and existing adapter/API panel tests.
* Decisions preserved: parent #157 and children #162/#159/#164/#163 remain
  Refs. Privacy/access/threshold/screen-reader/held-out evidence and #440
  remain unproven. No requirements, live activation or human approval inferred.
* Locked test boundary: existing test ownership, zero removals, at most
  20 additional methods and the conditional single browser test file remain
  unchanged. Findings request coverage within that allocation.
* Assessment boundary: credibility of the bounded offline implementation plan,
  not live approval, semantic accuracy, actual model effectiveness, legal
  compliance or accessibility conformance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1, W1, W2; human decisions and issue acceptance | Covered | Open decisions and #440 remain blockers; all five issues remain Refs. |
| C2, C7; P01-T01 admission and per-invocation receipts | Partial | Dispatch admission is planned; completion release recheck and receipt survival need explicit acceptance coverage, PC-001/PC-002. |
| C3; P01-T01 prompt bounds and source completeness | Covered | Complete source JSON, user-only bounded history, oversize fallback and final prompt ceiling are explicit. |
| C4; P01-T01 route unification and compatibility | Covered | Both HTTP turn paths use the panel; legacy reply/label/model/withheld compatibility is retained. |
| C5, W3; P02-T01 warning and UI | Covered | Server warning, described question field, fail-closed loading and accurate refusals are explicit; rendered checks remain conditional, not acceptance. |
| C6; P02-T01 evaluator | Partial | Scripted/actual calls and runtime/human acceptance are distinguished; exceptional completion accounting needs PC-002. |
| P03-T01 local validation | Partial | Targeted checks fit caller direction; executable scratch/interpreter instructions conflict with the environment, PC-003. |
| P03-T01 independent Review and PR | Partial | One Review and Refs-only PR are planned; automatic later-work routing needs severity-based disposition, PC-004. |
| Locked test ownership/removals/addition ceiling | Covered | No change requested; incorporate negative cases into existing methods/subtests where appropriate. |

## Verdict

* Verdict: Revise
* Severity summary: 1 High, 3 Medium, 0 Low, 0 Critical.
* Rationale: the bounded engineering scope is credible, but completion-time
  admission, exceptional-turn accounting and two execution/disposition
  instructions need direct corrections before implementation handoff.
  None requires a new owner decision or another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Completion checks omit release and continuity revocation

* Related IDs: C7, P01-T01, admission requirement and post-call acceptance.
* Evidence: phase details require admission before dispatch and post-call
  user/thread/case/source checks, but not a post-call release/continuity check.
  src/core/src/zava_forward/core/ai.py, Ai.run, already rechecks the gate and
  selected release after its provider returns. The new ChatModel path uses
  AgentWorker.provider_call rather than Ai.run.
* Concern: staff permissions and case sources can remain unchanged while
  the task is suspended or its release is revoked during inference.
  The specified completion checks would not necessarily discard that result.
* Impact: a result can escape the existing release boundary despite correct
  pre-dispatch admission.
* Smallest useful change: explicitly require the adapter to recheck the
  server-owned admission boundary after provider completion and discard text
  on denial or a changed selected release, where that release boundary exists.
  Do not register or approve the conversational task to make this work.
* Action owner: Planning parent, then P01 implementer.
* Exact resolving evidence: revised P01 details and an existing-file synthetic
  regression that admits dispatch, revokes/suspends admission inside the
  provider callback, and proves one call, no returned/stored model answer,
  workflow-only handling and retained non-content consumption metadata.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Completed-turn receipts do not specify incurred-call accounting on rejection

* Related IDs: C2, C6, P01-T01, P02-T01, consumption-report acceptance.
* Evidence: P01 says to store an event "per completed turn" and return it for
  reporting, while also requiring re-reading the current user/thread/case
  after the callback. Current ChatPanel.ask and API handling allow
  permission/not-found failures; chat_eval.Run.ask converts exceptions to an
  error with no reply. P02 accumulates panel receipts.
* Concern: a provider call can consume tokens and then lose its reply/receipt
  because permission, thread or case revalidation fails. A successful-response
  receipt alone cannot account for this attempted turn. The same issue applies
  to provider failures with validated usage.
* Impact: durable and evaluation totals can undercount actual calls/cost or
  misrepresent missing usage on the precise negative cases being added.
* Smallest useful change: define exactly-once metadata recording for every
  invoked provider attempt, including failures and completion rejection,
  independently of successful assistant-message persistence or HTTP reply.
  Define how the evaluator obtains that receipt without disclosing content or
  restoring access. Denied-before-dispatch cases must record zero actual calls.
* Action owner: Planning parent, then P01/P02 implementer.
* Exact resolving evidence: revised receipt lifecycle and synthetic subcases
  for post-call role removal, thread/case disappearance and provider failure;
  assert durable/report call totals, validated usage or explicit Unknown,
  no duplicate event and no stored/released provider content after rejection.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Validation instructions rely on a forbidden external temporary path

* Related IDs: P03-T01, local-only validation and environment constraints.
* Evidence: phase details name an installed /tmp/ama-chat157-venv as the
  validation environment. src/agents/src/zava_forward/agents/chat_eval.py,
  run_eval, uses tempfile.TemporaryDirectory() without an explicit parent.
  The active environment prohibits all /tmp/temporary-directory file
  operations and requires created scratch files under the working directory.
* Concern: following the phase literally reads the forbidden interpreter
  location, and default evaluator scratch can write outside the permitted
  project location.
* Impact: the proposed validation cannot be executed as written within the
  task constraints; a historical installation is not an execution exception.
* Smallest useful change: replace the interpreter guidance with an allowed
  project-local environment strategy, and explicitly configure the test and
  evaluator scratch root under the project before any tempfile initialization.
  Reuse permitted installed dependencies when available; restore only after
  a missing-dependency failure. Preserve evidence and clean only exact newly
  owned scratch outputs.
* Action owner: Planning parent, then P03 implementer.
* Exact resolving evidence: corrected P03 command/environment instructions
  and recorded targeted test/evaluator commands that use a project-local
  scratch root, synthetic inputs and no forbidden-path operations.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Review findings are unconditionally routed to later work

* Related IDs: P03-T01, ordered RPI loop and one-PR completion.
* Evidence: phase details say to preserve independent Review findings and
  "route them as later work, no repeat Review" without a severity or
  publication disposition rule.
* Concern: this instruction treats new implementation defects and already
  accepted human blockers alike. It could defer a correctness regression or
  a violated acceptance criterion solely to avoid another Review.
* Impact: completion/publication may proceed despite a known defect introduced
  by this candidate; one Review does not imply acceptance.
* Smallest useful change: distinguish preserved external/human residuals from
  implementation-blocking findings. Correct in-scope blocking defects on the
  same branch, record their disposition and targeted validation, preserve the
  original Review verdict, and do not claim independent acceptance of an
  unreviewed corrected head. If that prevents the required publication outcome,
  report the blocker rather than silently deferring it or repeating Review.
* Action owner: Planning parent, then P03 implementer.
* Exact resolving evidence: revised Review closeout/publication rule;
  eventual changes/Review/PR records identify each finding's disposition,
  original reviewed head and any later unreviewed correction boundary.
* Decision route: Direct planner correction; no user decision required.

## Strengths and Residual Risk

* Reuses existing runtime, provider envelope, evaluator and metadata ledger.
* Preserves source completeness, default-deny dispatch, proposal-only behavior,
  role/source revalidation and the canonical warning.
* Explicitly preserves the known semantic grounding failure, disabled
  enablement and the distinction between scripted runtime acceptance and
  independently labelled human acceptance.
* Owner-approved role budgets, privacy/access decisions, held-out/serving-model
  evidence, named screen-reader exercise and #440 remain external blockers,
  not defects this critique asks the planner to manufacture away.
* Targeted checks, not a full gate or newly authorized changed-gate run,
  remain the selected validation boundary.

## Questions or Blocking Evidence Gaps

* No new user choice is needed for the four direct corrections.
* Live and whole-issue approval evidence remains unavailable by design;
  the plan correctly does not make it an offline engineering prerequisite.

## Limitations

* No tests, model calls, cloud operations, private-data reads or new research
  were performed. Supplied issue/ADR/requirements summaries were assessed as
  recorded evidence, not freshly authenticated approval records.
* This is a plan critique, not an implementation, UI-conformance or final
  exact-head acceptance review. Only this critique artifact was written.
* Existing untracked parent artifacts were left untouched. Branch inspection
  found feat/agent-chat-157 and no PR for that head.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: disposition PC-001 through PC-004 directly in the
  candidate plan/details, preserving the locked test allocation, then finalize
  and continue P01 without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/agent-chat-157-plan.md](.copilot-tracking/plans/2026-10-27/agent-chat-157-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/agent-chat-157-phase-details.md](.copilot-tracking/details/2026-10-27/agent-chat-157-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-27/agent-chat-157-research.md](.copilot-tracking/research/2026-10-27/agent-chat-157-research.md) | Supplied bounded research evidence |
| [.copilot-tracking/reviews/plans/2026-10-27/agent-chat-157-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/agent-chat-157-plan-critique.md) | This single independent assessment |

## Next Steps

The active planning parent should resolve the four direct findings, finalize
the candidate and continue the ordered RPI loop. No second critique, additional
agent dispatch or user response is requested.
