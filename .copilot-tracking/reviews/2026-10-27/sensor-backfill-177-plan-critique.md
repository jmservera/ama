---
title: Sensor backfill final-candidate plan critique
ms.date: 2026-10-27
---

## Metadata

* Task ID: #177 / sensor-backfill-177
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/sensor-backfill-177-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate critique.

## Inputs and Criterion Boundary

* Caller requests the full ordered RPI loop with separate #178, #179, #180,
  #181 and #183 children from feat/sensor-backfill-177. All child PRs target
  that parent; only the parent targets main. No merging is authorized.
* Research: .copilot-tracking/research/2026-10-27/sensor-backfill-177-research.md.
  The supplied plan and details are assessed together, including their
  requirements, phase ordering, acceptance, dependencies and test boundary.
* Owner climate reuse approval remains unresolved. Active #425 is an
  alternative, not approved or merged input. #183 must stop at the actual
  #110 identity incompatibility rather than create a bypass.
* Eligible delivery is partial exercise components and evidence on unmerged
  children. The parent is draft coordination only. Its single documentation-
  scoped gate cannot validate child source.
* Validation authority is focused child tests only; no private data, secrets,
  .env, uv, Azure or Docker. The execution environment also forbids file
  operations in temporary directories, including /tmp.
* Supporting reads were limited to supplied evidence pointers and mandatory
  repository context: src/README.md, the cited generator, provenance, stock
  and consumer contracts, and the existing gate implementation. No additional
  climate research, GitHub retrieval or agent delegation was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #178; research W1/W3/W4; P01-T01 | Covered | Owner decision remains open; no silent #425 import; evidence-only child is appropriate. |
| P01-T01/P01-T02; all child branches | Partial | Common-parent commitment and checklist execution order disagree: PC-004. |
| #179; research Cycle 1 Wave 2; P02-T01 | Partial | Legacy equation/RNG preservation is planned, but extracted dependency provenance and numerical input domain are incomplete: PC-001/PC-005. |
| #180; P02-T02 | Covered for partial scope | Explicit synthetic dated measures, inclusive completion boundary, identity matching and no-history neutrality; no fabricated actual retrofit history. |
| #181; P02-T03 | Covered for partial scope | Per-ID/seed distributions, explicit synthetic monitoring and no inferred declined/unknown profiles; no demographic attribution. |
| #183; research C6/W2; P02-T04 | Covered | Actual consumer incompatibility is a stop, not permission to change identities or validation. |
| Test ownership and removals | Covered | Core owns semantics; no removals; at most the three named new test modules. Corrections below fit that boundary. |
| P02-T05; child publication | Covered for draft scope | Focused tests and child draft PRs, not whole-package gates or completed-issue claims. |
| P03-T01/P03-T02; independent Review | Partial | Review exists, but disposition of implementation defects is not severity-gated: PC-006. |
| P03-T03; cleanup and gate | Partial | Quiet dry-run conceals deletion selection; current runner requires prohibited writes; partial verification needs its explicit scope: PC-002/PC-003/PC-007. |
| Acceptance and dependency stops | Covered within stated limits | Whole-child, two-year grounded history, integration, scientific and parent acceptance remain unsupported and must remain unclaimed. |

## Verdict

* Verdict: Revise
* Severity counts: 0 Critical, 3 High, 4 Medium, 0 Low.
* Rationale: The partial-delivery strategy and dependency stops are credible.
  Seven concrete corrections are needed before execution. The current gate
  mechanism is blocked under the execution constraints; this does not forbid
  the independently testable exercise components or justify substituting a
  different ingestion/source path. No second critique is requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Equation extraction omits the generator dependency fingerprint

* Related IDs: #179, P02-T01, research Cycle 1 Wave 2.
* Evidence: .copilot-tracking/research/2026-10-27/sensor-backfill-177-research.md:93-95
  explicitly requires source fingerprint and manifest binding.
  .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md:23-29
  extracts the active legacy equation but specifies no provenance update.
  src/core/src/zava_forward/core/synthetic/sensor_backfill.py:190-193
  enumerates dependency files without the proposed helper;
  src/core/src/zava_forward/core/synthetic/provenance.py:17-27 hashes only
  those named files, not transitive imports or the Git tree.
* Concern: Once the wrapper delegates to a new module, changing that module
  can change generated readings without changing the recorded source revision.
* Impact: Deterministic output provenance would no longer identify all code
  needed to reproduce a snapshot, despite unchanged legacy values initially.
* Smallest useful change: Add the extracted helper to revision_sources and
  document the intentional provenance revision change. Bind the versioned
  projection contract to existing metadata without introducing integration
  of the other children.
* Action owner: Planning parent; implementation owner of child #179.
* Exact resolving evidence: Revised P02-T01 explicitly includes dependency
  fingerprint/manifest work. Within test_indoor_projection.py or an existing
  backfill test module, verify helper inclusion, fingerprint sensitivity to
  helper bytes, and generated manifest use of that revision, alongside the
  existing legacy equation/RNG comparisons.
* Decision route: Direct planner correction; no new user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The quiet cleanup preview cannot support deletion authorization

* Related IDs: P03-T03; preservation of original evidence and existing work.
* Evidence: .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md:66-67
  says to inspect git clean -ndxq before git clean -fdxq. In this worktree the
  read-only git clean -ndxq produced no output; git clean -ndx listed the
  untracked plan, details, research and RPI state files. No deletion was run.
* Concern: -q suppresses the very candidate list the plan requires the
  executor to inspect. The subsequent repository-wide -fdxq includes ignored
  and untracked inputs, not just task-owned scratch.
* Impact: An empty-looking preview could authorize irreversible deletion of
  original RPI evidence or unrelated work.
* Smallest useful change: Use a visible dry-run without -q, require an
  exact reviewed selection, and stop if any candidate is not authorized
  task-owned scratch. Preserve/commit original evidence first and honor the
  archive/restore-backed retention policy where applicable. Do not execute
  a whole-worktree clean merely because the preview is empty or quiet.
* Action owner: Planning parent; parent publication executor.
* Exact resolving evidence: Revised P03-T03 names git clean -ndx and a
  pre-deletion inventory/authorization check matching the actual removal
  scope; no original evidence or unrelated input appears in that scope.
* Decision route: Direct planner correction. Unknown ownership blocks cleanup;
  it does not authorize disposal or require a broader source decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: The planned gate necessarily writes to a forbidden path

* Related IDs: P03-T03; one documentation-only parent gate; environment boundary.
* Evidence: .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md:68-70
  explicitly requests acquiring /tmp/ama-rpi-heavy.lock.
  tools/rpi-checks.py:2175-2178 opens that hardcoded path with
  O_CREAT | O_RDWR, including for --lock-timeout 0. The execution constraints
  prohibit file operations in /tmp and other temporary directories.
* Concern: Zero lock wait changes waiting behavior, not the forbidden write.
  Documentation-only selection does not bypass the lock.
* Impact: The planned gate cannot be executed compliantly in this environment.
  Attempting it anyway would violate the boundary before validating the parent.
* Smallest useful change: Explicitly record the gate as blocked by the
  current runner/environment incompatibility and stop before its forbidden
  write. Retain the single documentation-scoped gate requirement; do not
  relocate/bypass the shared lock, modify the runner, or substitute child
  gates, Docker or cloud work within this task.
* Action owner: Planning parent to record the stop; runner/environment owner
  for any separately authorized resolution.
* Exact resolving evidence: Revised P03-T03 distinguishes a compliant
  preflight block from an executed failed gate and claims no receipt.
  Eventual execution requires evidence of a compatible authorized environment
  and an unchanged approved gate contract before the single invocation.
* Decision route: Direct planner correction to acknowledge the blocker.
  No new user choice is needed to continue the eligible partial component work.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The first child precedes the foundation all children must inherit

* Related IDs: P01-T01, P01-T02; #178 branch ancestry.
* Evidence: .copilot-tracking/plans/2026-10-27/sensor-backfill-177-plan.md:77-78
  creates the #178 child before committing the parent foundation.
  .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md:16-18
  instead requires all five children to fork that common commit.
* Concern: Following the checklist literally creates a #178 branch without
  the final shared RPI evidence, then requires forbidden/unplanned ancestry
  repair or leaves inconsistent review bases.
* Impact: The declared common base and independent child-diff review would
  not describe the actual branch graph.
* Smallest useful change: Commit the parent foundation before creating any
  child, including evidence-only #178. Make that dependency explicit in both
  artifacts. Keep all children as siblings targeting the parent.
* Action owner: Planning parent.
* Exact resolving evidence: Corrected task order/dependency and, at execution,
  a recorded foundation SHA that is the fork point for all five children.
  No merge, cherry-pick, rebase or history rewrite is needed.
* Decision route: Direct planner correction; caller already fixes the topology.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Finite outdoor temperature is not a safe equation input domain

* Related IDs: #179, P02-T01; explicit validation and bounds.
* Evidence: .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md:25-28
  specifies finite outdoor inputs and 0-to-100 RH, without a temperature
  interval. src/core/src/zava_forward/core/synthetic/sensor_backfill.py:73-74
  evaluates exp(17.62 * t / (243.12 + t)); _indoor uses that function on
  outdoor temperature at lines 103-104.
* Concern: A finite value of -243.12 passes the stated finiteness criterion
  but divides by zero; values near the singularity can also overflow.
* Impact: The new validated API can emit incidental arithmetic exceptions
  instead of its promised explicit domain errors.
* Smallest useful change: Specify a supported exercise temperature interval
  excluding singular/unstable inputs, finite positive construction factors
  with bounded support, and explicit rejection behavior. Apply new input
  validation without silently changing supported legacy equation/RNG behavior.
* Action owner: Planning parent; implementation owner of child #179.
* Exact resolving evidence: P02-T01 records supported intervals and rejection
  behavior; test_indoor_projection.py covers accepted endpoints, just-outside
  values, NaN/infinity, the finite singular value, and supported legacy cases.
* Decision route: Direct planner correction for an exercise contract, not
  approval of historical or physically calibrated model validity.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Implementation Review findings have no severity-based disposition

* Related IDs: P03-T01, P03-T02; ordered RPI and acceptance reporting.
* Evidence: .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md:58-61
  says to route findings to later work without a repair-and-repeat Review loop.
  Lines 63-64 then record child SHAs/checks, without specifying which findings
  block component completion or how a changed child is distinguished from
  the independently reviewed head.
* Concern: The blanket later-work instruction treats an implementation defect
  like an accepted external dependency. Even a failed component Review could
  be reported as completed bounded delivery.
* Impact: A parent documentation gate and passing unit tests could obscure
  known child defects or imply review of a later, different child head.
* Smallest useful change: Preserve the original single Review and explicitly
  disposition every finding. Unresolved substantive defects leave the affected
  component blocked/unaccepted; drafts may remain transparent coordination
  evidence only. If a repair is authorized, record focused retest evidence
  and distinguish the repaired SHA from the original reviewed SHA; do not
  claim independent review coverage that did not occur.
* Action owner: Planning parent and implementation Review coordinator.
* Exact resolving evidence: P03 describes a per-finding severity/disposition,
  child SHA, original Review outcome and completion eligibility ledger;
  deferral never converts an adverse finding to a pass.
* Decision route: Direct planner correction; no repeated plan critique or
  automatic second implementation Review is requested.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Partial receipt verification lacks its mandatory scope argument

* Related IDs: P03-T03; parent-only gate evidence.
* Evidence: .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md:70-72
  requests --changed and subsequent receipt verification without naming
  --required-scope partial. tools/rpi-checks.py:2158-2166 and :2203 default
  verification to full scope and reject a partial receipt.
  src/README.md:76-94 documents the required partial-scope verification.
* Concern: A default verification command rejects the intended changed-path
  receipt even if its selected checks pass. "If produced" is also insufficient:
  a failed receipt is adverse evidence, not a verifiable passing receipt.
* Impact: The executor may misclassify expected scope rejection as a code
  failure, skip verification, or expand the gate beyond caller authorization.
* Smallest useful change: Specify verification with --required-scope partial
  and the exact fetched origin/main SHA, only for a successful receipt.
  Bind it to the unchanged committed parent candidate. If main, HEAD or
  bound inputs move, stop as stale/blocked rather than spending another gate
  invocation or upgrading to --all under the one-invocation constraint.
* Action owner: Planning parent; parent publication executor.
* Exact resolving evidence: Revised P03-T03 contains the explicit partial
  verification command and success/failure/staleness branches. If PC-003
  remains unresolved, record Not run rather than fabricate verification.
* Decision route: Direct planner correction; no new user decision.

## Strengths and Residual Risk

* The plan correctly avoids needless #178 source implementation and #183 writer
  implementation where owner/dependency decisions genuinely forbid acceptance.
  Public licensing language and an existing unmerged branch are not substitutes
  for approval.
* #179/#180/#181 can deliver small synthetic primitives without a paired
  historical climate source, actual retrofit dates or ingestion compatibility.
  Their outputs remain exercise components, not completed original stories.
* The actual stock sensor identity is SENS-SYN- plus a 64-character lowercase
  hex digest: src/core/src/zava_forward/core/synthetic/sensor_stock.py:87.
  The consumer uses uppercase identities and observation limits of 20/40/12
  characters: src/core/src/zava_forward/core/sensor_consumer.py:20,
  :374-380. Evidence-only #183 is therefore justified; expanding legacy DDL
  would not resolve admission.
* Independent unmerged children are not integrated behavior. The caller has
  explicitly selected that limitation and a draft parent, not authorized
  merges or copied child code.
* All recommended tests fit the locked three-module limit or existing modules.
  No test removal, full child gate, new dependency or extra module is required.

## Questions or Blocking Evidence Gaps

* Existing owner climate/source reuse and consumer identity decisions remain
  open for #178/#183. The planning parent should retain the single blocker
  comment per affected issue, not reopen settled topology or import #425.
* The present gate mechanism is blocked by PC-003. The eligible exercise work
  need not wait for those external decisions or that publication blocker.
* No fresh user response is necessary to make the direct plan corrections.
  No owner approval, private dataset, paired source or integrated acceptance
  is inferred from this critique.

## Limitations

* This is one plan credibility assessment, not an implementation review or
  acceptance test. No executable component tests or gate were run.
* Original issue bodies and remote lifecycle were not independently fetched;
  issue acceptance and #425 status are assessed from the supplied research
  and caller direction. Whole-issue acceptance is not independently established.
* Initial status was feat/sensor-backfill-177, tracking origin/main, with the
  research, plan, details and RPI state untracked. Those inputs were preserved.
* Only this critique artifact was intentionally written. Plan, phase details,
  research, source and existing review records were not edited.

## Recommended Next Action

* Highest-impact finding: PC-001, loss of transitive model provenance.
* Action owner: Planning parent.
* Smallest next action: Add the extracted dependency/manifest regression
  obligation to #179, then directly disposition all seven findings, including
  the explicit gate block. Preserve this original critique.
* User response required: No for these corrections. Existing source/identity
  decisions remain necessary only for their affected blocked scope.

| [.copilot-tracking/research/2026-10-27/sensor-backfill-177-research.md](.copilot-tracking/research/2026-10-27/sensor-backfill-177-research.md) | Supplied dependency and source evidence |
| [.copilot-tracking/plans/2026-10-27/sensor-backfill-177-plan.md](.copilot-tracking/plans/2026-10-27/sensor-backfill-177-plan.md) | Final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md](.copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md) | Implementation and publication details assessed |
| [.copilot-tracking/reviews/2026-10-27/sensor-backfill-177-plan-critique.md](.copilot-tracking/reviews/2026-10-27/sensor-backfill-177-plan-critique.md) | Complete original final-candidate critique |

## Next Steps

The active planning parent should revise and record dispositions directly,
without another critique pass. Proceed only to eligible bounded child work
after disposition; retain blocked acceptance and gate status, unmerged child
drafts and draft parent coordination. No user action is required for the
planner-owned corrections. Do not merge.
