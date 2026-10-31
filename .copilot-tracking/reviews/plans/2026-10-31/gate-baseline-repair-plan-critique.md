<!-- markdownlint-disable-file -->
# RPI Plan Critique: gate-baseline-repair

## Metadata

* Task ID: a81da11b-4af4-4c2c-bd8a-ca8a765c6fd4
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/gate-baseline-repair-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/gate-baseline-repair-phase-details.md
* Critique execution status: Complete
* Execution count: one final-candidate critique; no additional critique requested.

## Inputs and Criterion Boundary

* Caller direction: ordered full RPI; repair the inherited complete main gate;
  bind nine strict B023 references without behavior changes or suppressions;
  diagnose the exact chat-panel Chromium case; small defects only; no duplicate
  #572 wiring; failing-group/API/Ruff validation; clean committed complete
  exact-head gate, normal push and main PR using Refs #572.
* Primary inputs: the plan and phase-details paths above, plus
  .copilot-tracking/research/2026-10-31/gate-baseline-repair-research.md,
  particularly Q1-Q4 and C1-C7.
* Referenced constraints: src/README.md local RPI gate and
  docs/reference/method/tracking-retention-policy.md. Project context was read
  in docs/case_study_48_original.md, docs/case_study_48_addendum.md,
  docs/reference/README.md and docs/reference/memory.md; memory is not evidence.
* Decisions considered: default binding retains mutable list identity;
  isolate only the two adversarial fixture command transcripts; retain the
  parser and production selector; do not outer-lock the self-locking runner.
* Dependencies and acceptance considered: P01 before P02; original critique
  and Review; two Python targets plus API README; zero added/removed test
  methods; pinned tooling, synthetic data, real Chromium, owned SQL and scans;
  fresh external complete receipt, current-main verification and independent
  exact-head assessment before publication.
* Boundary: assess implementation credibility and publication sequencing
  against supplied evidence, not re-execute the baseline, independently prove
  runtime behavior, inspect private data, or perform additional research.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI and original evidence | Covered | Dated Research, Plan, critique, changes and one original Review are explicitly owned. |
| Q1 / C1-C2 / P01-T01 | Covered | Full baseline failure and nine strict closures are identified; isolated lint and formatter are required. |
| Q2 / C7 / P01-T01 | Covered | Defaults preserve live list identity and per-iteration scalar/snapshot binding; callback identity survives unroute. |
| Q3 / C3 / C6 / P01-T03 | Covered | Unchanged exact Chromium selector passed in supplied research; real rerun with zero skips is required, without wiring changes. |
| Q4 / C4-C5 / P01-T02 | Covered | Capture is limited to two Runner.command fixture calls; transcript, receipt and integration rejection assertions remain. |
| P01-T02 / test ownership and budget | Covered | Existing test strengthened; zero added methods/removals; no production parser or allowance changes. |
| P01-T03 / focused and full validation | Covered | Tooling regression, three browser checks, exact chat, API unittest/Ruff/format/mypy and complete final gate. |
| P02-T01 / original Review disposition | Partial | PC-001: findings are routed to later work without an explicit publication-blocking disposition rule. |
| P02-T02 / generated cleanup | Partial | PC-002: identifying own generated files is not the retention policy's archive/restore-backed authorization. |
| P02-T02 / exact-head publication | Covered | Commit original evidence, self-locking jobs-3 complete gate, fetch/verify, independent exact-head assessment, normal push and main PR. |
| Scope, dependencies and non-goals | Covered | Synthetic-only, pinned prerequisites, no runtime/workflow/protection changes or duplicate #572 work; missing prerequisites block publication. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 1; Medium 1; Low 0.
* Rationale: The two root-cause repairs and test budget are credible.
  Publication must explicitly stop for unresolved material Review findings,
  and cleanup must not bypass the referenced retention contract. Both are
  direct corrections within existing caller direction, not design decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Make material Review findings publication-blocking

* Related IDs: P02-T01, P02-T02; independent Review acceptance criterion.
* Evidence: .copilot-tracking/plans/2026-10-31/gate-baseline-repair-plan.md,
  P02-T01 says "No repeated Review; findings route to later work."
  .copilot-tracking/details/2026-10-31/gate-baseline-repair-phase-details.md,
  P02-T01 preserves findings but does not define the eligible outcome for
  entering P02-T02. The final exact-head assessment is required but its
  blocking result and finding-disposition responsibility are not explicit.
* Concern: A completed original Review is not necessarily a successful Review.
  As written, a material defect could be deferred while the candidate still
  proceeds through a passing local gate and publication.
* Impact: Automated validation does not establish that an independently found
  behavior regression or weakened evidence boundary has been resolved.
* Smallest useful change: Explicitly prohibit publication with unresolved
  material Review findings or an adverse independent exact-head assessment.
  Assign in-scope corrections to Implement and record their disposition in
  changes without editing the original Review or rerunning the original
  Review stage. If resolution needs divergent scope, stop and return the
  blocker rather than silently defer it. Corrections require a new committed
  candidate and full gate; the already-planned final independent exact-head
  assessment must confirm the candidate is eligible for publication.
* Action owner: Planning parent defines the gate; implementation parent owns
  correction/disposition; final independent assessor owns exact-head findings.
* Exact resolving evidence: Revised P02-T01/P02-T02 in both planning artifacts
  explicitly bind publication to no unresolved material findings and a
  non-blocking exact-head assessment. Later changes must map each original
  finding to resolving source/validation or an explicit publication blocker;
  final assessment must identify the assessed HEAD and current base.
* Decision route: Direct planner correction. No user response is required;
  existing caller direction does not authorize publishing unresolved defects.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Replace ownership-only cleanup with the retention contract

* Related IDs: P02-T02; clean-input gate and original-evidence preservation.
* Evidence: .copilot-tracking/details/2026-10-31/gate-baseline-repair-phase-details.md,
  P02-T02 permits removing own generated ignored metadata/cache files after
  identifying exact paths. docs/reference/method/tracking-retention-policy.md,
  Explicit Cleanup Contract, requires an approved finite path manifest,
  full snapshot preservation, archive readback and selected-member restore
  verification before pruning. The plan references this policy but does not
  apply those requirements to its cleanup instruction.
* Concern: File ownership and classification as generated do not by themselves
  satisfy the required reversible cleanup authorization.
* Impact: An implementer could discard ignored candidate inputs to achieve a
  clean gate without the required preservation and restoration evidence.
* Smallest useful change: Prefer preventing checkout output by using external
  caches and bytecode controls already planned. If cleanup remains necessary,
  explicitly require the finite approved selection and archive/restore-backed
  verification before deletion; otherwise stop the gate as blocked. Do not
  extend cleanup to the existing untracked RPI artifacts, foreign outputs,
  historical records or adverse evidence.
* Action owner: Planning parent corrects P02-T02; implementation parent applies
  the retention contract and records any cleanup evidence.
* Exact resolving evidence: Revised P02-T02 names the no-deletion default and
  required policy-backed cleanup preconditions. Any actual deletion has its
  finite authorization, archive identity/readback, restored matching bytes,
  protected-input checks and removal journal recorded before the final gate.
  If no cleanup is needed, record that no files were deleted and demonstrate
  clean candidate inputs instead.
* Decision route: Direct planner correction. No new user decision is required
  to specify the existing policy; absent authorization for a necessary finite
  selection, execution must block rather than invent permission.

## Strengths and Residual Risk

* The plan repairs observed causes rather than the presumed chat runtime
  defect: supplied C6 reports one real Chromium execution, zero skips.
* Fixture-only stdout isolation keeps real skip detection fail-closed and
  retains adversarial receipt/rejection coverage without adding test methods.
* Strict lint, real browser journeys and the complete gate provide distinct
  evidence for closure semantics, execution and publication readiness.
* The caller's wait direction is preserved through the runner's own timeout;
  an outer flock is rejected rather than bypassing serialization.
* Further latent baseline failures are explicitly acknowledged. They remain
  bounded diagnosis work, not permission for suppressions or scope expansion.
* Read-only workspace inspection found branch fix/gate-baseline-b023 at
  a75bbdffa51ae34b1fcf779250f1f553d566ee93, while local origin/main is now
  e64c6e6c9da407682de59b926944424f94f50671. The research baseline is historical,
  not a current-main success. Apply the existing current-base reconciliation
  and fresh-gate rule before publication; this observation does not authorize
  rebasing, force-pushing or moving existing untracked work.

## Questions or Blocking Evidence Gaps

* No decision-critical research gap prevents assessment of this plan.
* No user question is needed for either correction.
* Actual future Review disposition, exact-head assessment and complete receipt
  are execution prerequisites, not evidence already established by this critique.

## Limitations

* Original external receipt/log references were considered as supplied
  research pointers, not opened or independently verified. No operations were
  performed on their historical /tmp locations.
* No heavy validation, source implementation, plan/research editing or agent
  delegation occurred. Only the caller-specified critique artifact was written.
* This is one complete assessment of the supplied boundary, not a runtime,
  security, accessibility, hosted-check or human-approval certification.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct the P02 Review/publication eligibility rule and
  cleanup preconditions in the plan and details, recording both dispositions
  without another critique pass, then continue the confirmed automatic RPI loop.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/gate-baseline-repair-plan.md](../../../plans/2026-10-31/gate-baseline-repair-plan.md) | Final-candidate plan assessed, unchanged. |
| [.copilot-tracking/details/2026-10-31/gate-baseline-repair-phase-details.md](../../../details/2026-10-31/gate-baseline-repair-phase-details.md) | Phase details assessed, unchanged. |
| [.copilot-tracking/research/2026-10-31/gate-baseline-repair-research.md](../../../research/2026-10-31/gate-baseline-repair-research.md) | Supplied research and historical evidence pointers. |
| [.copilot-tracking/reviews/plans/2026-10-31/gate-baseline-repair-plan-critique.md](gate-baseline-repair-plan-critique.md) | This original single critique and complete PC finding set. |

## Next Steps

Planning parent directly resolves PC-001 and PC-002, preserves this original
Revise verdict, and finalizes without another critique. Continue Implement
only after the material dispositions are recorded. No user action is required;
no implementation or peer stage is invoked by this critique.
