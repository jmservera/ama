<!-- markdownlint-disable-file -->
---
title: Issue 349 current-main continuation plan critique
description: One independent final-candidate assessment of the local reconciliation plan
ms.date: 2026-10-23
---

## Metadata

* Task ID: 349-current-main-20261023, continuing issue349 and parent 349-correction3.
* Critique date: 2026-10-23.
* Plan: .copilot-tracking/plans/2026-10-23/issue349-tenant-readiness-preflight-current-main-plan.md.
* Phase details: .copilot-tracking/details/2026-10-23/issue349-tenant-readiness-preflight-current-main-phase-details.md.
* Critique execution status: Complete.
* Execution count: Exactly one final-candidate critique; rpi-plan-critique activated.

## Inputs and Criterion Boundary

* Caller requirements: Local-only reconciliation in the supplied worktree;
  preserve original correction3 and all original RPI evidence; checkpoint new
  phase evidence; integrate remote ancestry by rebase before rebasing onto fresh
  main; omit only two archived generated-score commits; preserve checker,
  tests, main documents, full KB log and active scores byte-for-byte.
* Initial local: 3eebcc3922188f5ddd614bfa5d4583b082f4e1c5.
* Supplied main: 140d8f494482c78e84d15f3d46b9223d3c487af0.
* Supplied remote topic: 6c284d4547de7c52a360b2ec2406ea2078a98f16.
* Supplied old base: b4d467cad84535ed106cffa1ae9aa303db7bfed2.
* Research: .copilot-tracking/research/2026-10-23/issue349-tenant-readiness-preflight-current-main-research.md,
  including C1-C6 and the accepted separation of historical score provenance
  from main's active score.
* Supporting evidence: Read-only Git history, both score-commit file summaries,
  main's changed-file inventory, src/README.md local gate contract, relevant
  tools/rpi-checks.py selectors and installation behavior, and original
  correction3 plan/dispositions and Review.
* Decisions and dependencies: Parent owns the unchanged 35-test suite, zero
  additions/removals, exactly two historical patch targets, fresh pip-installed
  distributions, focused checks and one independent Review before the final
  committed candidate and sole complete gate. Stop on failure; finish a running
  gate if main moves, report stale, and do not retry or publish.
* Boundary: Assess credibility and requirement coverage of this plan, not
  implementation success, gate availability, fresh remote currentness, source
  correctness certification, tenant readiness or publication approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C3, P01-T01/P01-T02: lineage and generated evidence | Covered | Git inventory confirms five human checker commits and two score-only commits; exactly two inert patches and explicit score omissions preserve both known intents. |
| C4/C6: original correction3 history and dispositions | Covered | Byte comparisons cover original topic RPI and source/tests; original rejected worker-local restrictions and Conformant bounded Review remain historical. |
| Main documents, log and active rubric preservation | Covered | Main changed-file inventory is bounded; plan requires whole-file/blob equality, not timestamp precedence or blanket conflict resolution. |
| P02-T01: fresh installed distribution provenance | Partial | PC-001: conditional installation permits an existing non-receipt environment instead of requiring a new installation context. |
| P02-T02: test ownership, budget and focused checks | Covered | Parent owns all 35 retained tests; bytecode-disabled unittest, pinned isolated no-cache Ruff lint/format, strict mypy, external cache and invariant comparisons are specified. |
| P02-T02/P03-T01/P03-T02: failure progression | Partial | PC-002: ordering is explicit but a failed check or adverse Review is not explicitly a terminal continuation state. |
| P03: one independent Review and committed evidence | Covered with PC-002 | Review record is the worker's only writable artifact; final evidence is committed before the gate and original outcomes remain immutable. |
| C5, P04-T01: full gate and exact-head receipt | Covered | One complete --all invocation, all integration groups, new unique external output, ownership checks, official verification, receipt hash and external final outcomes are specified across plan/details. |
| Main movement, no retry and stop-before-push | Covered | Gate finishes if main moves, then verification reports stale; no second gate or remote mutation is authorized. |
| Live/private/paid/UI constraints and October headroom | Covered | Live acceptance remains blocked; no new authority is inferred, and October headroom stays Unknown. |

## Verdict

* Verdict: Revise.
* Rationale: The reconciliation strategy is credible and supported by supplied
  Git evidence. Two bounded operational requirements need explicit correction
  before implementation: mandatory fresh distribution provenance and fail-stop
  progression. Neither requires a product decision, new research, altered
  source/tests or another critique.
* Severity summary: Critical 0; High 0; Medium 2; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Require a fresh installation context, not merely existing distribution metadata

* Related IDs: C5; P02-T01; P02-T02.
* Evidence: The caller requires fresh pip-installed distributions, not an old
  receipt venv. Plan lines 128-132 say to establish installation in a new
  environment "if missing"; phase details lines 50-53 first check installed
  metadata and install only "If missing." These instructions do not require
  that successful metadata comes from a newly created environment associated
  with this reconciled checkout.
* Concern: An already populated non-receipt environment can satisfy the
  conditional without establishing the requested fresh installation or its
  source provenance. Avoiding old receipt environments alone does not close
  that path.
* Impact: Focused validation can be reported complete without meeting the
  caller's installation prerequisite. The later gate's own fresh installs do
  not retrospectively establish the focused validation environment.
* Smallest useful change: In both P02-T01 descriptions, require a new isolated
  non-receipt environment for this continuation. Check for missing
  distributions inside that new environment, then pip-install the existing
  five distributions with the component commands before focused execution.
  Bind focused test/tool invocations to that environment and record its
  interpreter, source checkout and installed distribution metadata. Preserve
  dependency pins and all old receipt environments.
* Action owner: Planning parent, then implementation parent for execution.
* Exact resolving evidence: Both P02-T01 descriptions require the new context
  unconditionally; the subsequent changes record identifies the fresh
  environment/interpreter, successful pip commands, five distribution source
  locations and focused commands using that context. No validation is required
  during this critique.
* Decision route: Direct planner correction implementing the confirmed caller
  requirement; no significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make successful checks and a non-blocking Review explicit gate eligibility conditions

* Related IDs: P02-T02; P03-T01; P03-T02; P04-T01.
* Evidence: The caller says to stop on failure. Plan lines 139-143 list checks,
  lines 151-154 say to route any Review finding once, and lines 159-163
  instruct the parent to reconcile the outcome and seal. Phase details lines
  58-64 and 72-84 likewise describe execution and reconciliation without an
  explicit failure stop. Dependencies establish ordering, but Review execution
  Complete can coexist with an adverse outcome, as the original history also
  distinguishes execution from verdict.
* Concern: The transition to sealing and the sole gate does not explicitly
  require successful focused checks, byte invariants and a Review with no
  unresolved blocking findings. "Reconciles Review outcome" is not itself a
  pass condition and could be read as permission to continue after recording
  an adverse result.
* Impact: The parent can consume the one authorized full gate despite an
  already-known failed preservation/check condition or unresolved Review
  blocker, contrary to fail-stop direction. Automatic corrective source/test
  edits would also exceed this preservation-only continuation.
* Smallest useful change: Add one shared progression rule to plan and details:
  any failed required command, byte/range invariant or unresolved blocking
  Review finding stops dependent work; preserve actual evidence and report the
  blocker, without automatic remediation, another Review or gate retry.
  P03-T02/P04-T01 are eligible only after all preceding required checks pass
  and the one Review has no unresolved blocker. Keep acknowledged
  coordinator/hosted/live residuals distinct from blockers, and retain the
  explicit exception to let an already running gate finish if main moves.
* Action owner: Planning parent, then implementation parent at each transition.
* Exact resolving evidence: Plan/details name the fail-stop rule and positive
  seal/gate eligibility conditions. The eventual changes/Review evidence
  records actual required check and invariant results and the Review outcome;
  a failed prerequisite instead produces a stopped handoff with no dependent
  seal/gate execution. Do not predict any result in advance.
* Decision route: Direct planner correction under the caller's existing
  stop-on-failure direction; no new user response required.

## Strengths and Residual Risk

* Rebase sequencing retains remote ancestry before dropping only the two
  expressly authorized score commits. Exact historical patches and main's
  active latest.json are treated as different kinds of evidence.
* Preservation comparisons cover checker/tests, every original topic RPI
  artifact, all main-only changes, the complete KB log and both active rubric
  files. No source behavior change or score regeneration is justified.
* All 35 existing tests remain parent-owned and unchanged. This worker's
  filesystem restrictions do not create parent defects, require fixture
  changes or override the explicitly required external gate location.
* Main may advance and host prerequisites may fail. The supplied plan accepts
  reporting stale/failure rather than authorizing retries or publication.
* Coordinator assessment, hosted checks and actual human/tenant acceptance
  remain separate; no local result establishes them or October budget headroom.

## Questions or Blocking Evidence Gaps

* No decision-critical research gap or unresolved user choice was identified.
* Gate prerequisite availability and actual results are future execution
  evidence, not claims this critique can establish.

## Limitations

* Only supplied inputs and bounded read-only Git/source context were assessed.
  No fetch, live call, test, lint, build, gate, receipt verification, history
  rewrite, commit or source/evidence edit was performed.
* The worktree contains the parent's untracked continuation artifacts. They
  were read, not moved, staged, committed or modified.
* This artifact is the only file written. No second critique is requested.

## Recommended Next Action

* Highest-impact finding: PC-002, explicit fail-stop and gate eligibility.
* Action owner: Planning parent.
* Smallest next action: Correct both P02-T01 descriptions for PC-001 and add
  the shared progression rule for PC-002; record dispositions without
  overwriting this original Revise outcome.
* User response required: No.

| [.copilot-tracking/research/2026-10-23/issue349-tenant-readiness-preflight-current-main-research.md](.copilot-tracking/research/2026-10-23/issue349-tenant-readiness-preflight-current-main-research.md) | Supplied C1-C6 evidence and scope |
| [.copilot-tracking/plans/2026-10-23/issue349-tenant-readiness-preflight-current-main-plan.md](.copilot-tracking/plans/2026-10-23/issue349-tenant-readiness-preflight-current-main-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-23/issue349-tenant-readiness-preflight-current-main-phase-details.md](.copilot-tracking/details/2026-10-23/issue349-tenant-readiness-preflight-current-main-phase-details.md) | Assessed execution details |
| [.copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md](.copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md) | Preserved original dispositions |
| [.copilot-tracking/reviews/logs/2026-10-22/issue349-tenant-readiness-preflight-correction3-review.md](.copilot-tracking/reviews/logs/2026-10-22/issue349-tenant-readiness-preflight-correction3-review.md) | Original bounded Review and residuals |
| [src/README.md](src/README.md) | Installation and complete local gate contract |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Existing fresh-environment and infra discovery behavior |
| [.copilot-tracking/reviews/plans/2026-10-23/issue349-tenant-readiness-preflight-current-main-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-23/issue349-tenant-readiness-preflight-current-main-plan-critique.md) | This single complete critique |

## Next Steps

The active planning parent disposes PC-001 and PC-002 directly and finalizes the
plan without another critique. No user action is required. This worker stops;
implementation, the one Review and the sole gate remain parent-owned and
subject to the stated prerequisites and stop conditions.
