---
title: "RPI Plan Critique: IoT PR 557 main refresh"
description: Independent final-candidate assessment of the bounded local rebase plan
ms.date: 2026-10-29
---

## Metadata

* Task ID: pr-557-main-refresh-2026-10-29
* Task slug: iot-pr557-main-refresh
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/iot-pr557-main-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/iot-pr557-main-refresh-phase-details.md
* Research: .copilot-tracking/research/2026-10-29/iot-pr557-main-refresh-research.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* The caller requests the complete Research, Plan, Implement and Review loop
  for existing branch feat/iot-hub-live-140 and PR #557. This assessment is
  only its independent plan critique, not another implementation or review.
* Starting HEAD is 7bd71d37866671899ef11fa653d9eace9687069b; the supplied fetched
  main is 8ee1b77f8983ddf39216da07ae60c63ef66431d6. Assess preservation of both
  workstreams through the explicitly authorized rebase, including additive
  documentation and append-only evidence.
* Main owns the exact rubric directory and scenario manifest. IoT activation,
  receiver restrictions, finite budgets and compiled infrastructure assertions
  must survive. Canonical source remains under src/ and tests remain external.
* Assess requested core/API static, formatting, typing and focused unit checks,
  sibling source/test import paths, offline infrastructure validation and
  nonblocking shared-lock admission boundaries. A full API suite is conditional,
  not mandatory; the candidate explicitly elects not to run it.
* Assess the local Conventional Commit, privacy-safe author/committer,
  Copilot trailer, preserved original critique/Review outcomes, no Azure
  changes, no push and no issue-closing language.
* Decisions and dependencies considered: C1-C8, Q1-Q3, all acceptance criteria,
  P01-T01 through P03-T01, the locked test ownership/removal/addition budget and
  main-authoritative generated targets.
* Evidence considered: the three supplied artifacts; their cited validation
  contracts in src/README.md and .github/workflows/src-ci.yml; cited
  src/core/tests/test_scenario_manifest.py,
  src/core/src/zava_forward/core/synthetic/scenario_manifest.py and
  infra/tests/test_iothub_module.py. Repository startup context was read
  without extending this assessment into legal, product or live research.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Complete four-stage RPI; original outcomes | Covered | Research is supplied, planning requires this one critique, and P03 requires one independent original Review and committed evidence. The three execution phases are implementation work packages, not a replacement for the four RPI stages. |
| C3-C4; P01-T01; ancestry acceptance | Covered | Recorded original/main identities, per-conflict three-way reconciliation, no blanket side selection, range-diff and completed-rebase checks preserve the intended history boundary. |
| C4; additive index/log/infra documentation | Covered | Both additions survive; only duplicated metadata introduced by reconciliation is removed and main's canonical metadata is retained. |
| C6; generated targets and pinned inputs | Covered | Exact main rubric/manifest identity is required after rebase and at closeout. The selected manifest test invokes hash validation of all four fixed public inputs. |
| C1; source/test layout | Covered | Current src/ distributions and external test roots are explicit; no legacy-source migration or private-data access is authorized. |
| C5; runtime and compiled infrastructure contracts | Covered | Publisher-only activation, routed-only receiver, finite controls, actual hub scope/SKU/unit/name/parameter assertions and their existing tests are preservation requirements. |
| C2, C7; P02-T01; static/type/unit acceptance | Covered | Core/API project Ruff, format and mypy checks, named sensor/transport/dependency/manifest modules, sibling import paths and offline infrastructure selectors cover the changed contracts. |
| C2; shared validation admission | Covered | Details correctly distinguish a successful brief probe from ownership of the lock. No full API discovery or heavy SQL/browser/integration work is planned. |
| Test ownership and change budget | Covered | infra/tests, src/core/tests and src/api/tests own tests. No removals; zero additions for reconciliation. A coupled defect needs an explicit plan amendment before a new regression. |
| C8; acceptance and publication boundaries | Covered | Targeted local evidence does not establish a complete gate, live acceptance or hosted CI. Historical adverse outcomes remain intact; publication and fresh exact-head gating remain outside this task. |
| P03-T01; commit and Review acceptance | Covered | Reviewer receives original/main/rebased identities and actual results; original outcome is retained. Local identity/trailer/cleanliness checks and a no-push handoff are explicit. |
| Non-goals, dependencies and risk handling | Covered | No Azure changes, new cloud resources, unrelated cleanup, unowned work removal, new dependency absent failure, or protection changes. Task-coupled failures require correction or an explicit blocker. |

## Verdict

* Verdict: Pass
* Rationale: The plan is credible for the specifically authorized bounded
  maintenance work. Preservation requirements have observable completion
  checks, validation is proportionate to the reconciled contracts, and the
  local handoff is explicitly separated from publication and live acceptance.
  No substantive change to the plan is required by the supplied evidence.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC findings were identified across the supplied boundary.
There are no withheld findings, required planner corrections or unresolved
significant/divergent user decisions. No artificial PC identifier is assigned
to an accepted limitation.

## Strengths and Residual Risk

* The rebase is explicitly authorized despite rewriting local topic history;
  that authority does not extend to pushing or remote operations.
* Restoration of main-owned generated files is paired with inspection of the
  entire replayed diff before skipping an empty commit, reducing accidental
  loss of unrelated topic intent.
* Source-first sibling import paths address shared editable-install ambiguity.
  The manifest test checks pinned bytes rather than relying solely on intake
  comparisons.
* The full-suite omission is an explicit bounded selection, not evidence that
  the initial lock probe grants continuing heavy-work ownership.
* Exact conflicts and actual check outcomes remain implementation-time
  unknowns. The plan requires range-diff, generated identities and actual
  command/exit/skip records rather than assuming success.
* A material post-implementation Review finding prevents a successful
  maintenance outcome. Retaining it as a blocker without launching a second
  review/fix loop respects the bounded task; it does not resolve that finding.
* Historical live and full-gate blockers remain open. Their deferral is
  supported by the caller's no-publication/no-live-acceptance boundary, not
  newly accepted or waived by this critique.

## Questions or Blocking Evidence Gaps

None decision-critical for this plan assessment. No user response is required.

## Limitations

* This critique did not run fetch, rebase, validation, commit, Azure or remote
  mutation commands, and did not verify implementation outcomes.
* Intake observations in C1-C8 are supplied research evidence, not fresh
  execution results. Implementation must establish the plan's completion
  criteria against the recorded main and the actual rebased candidate.
* The initial worktree inspection found only the task's untracked
  plan/details/research/state artifacts on the expected branch. These are
  consistent with the details' distinction between clean intake and newly
  generated task evidence; no pre-existing work was altered.
* A passing plan critique is not post-implementation Review, a local complete
  gate receipt, exact-head publication approval or live acceptance.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this original Pass disposition, finalize the
  plan and continue with P01-T01 under the already confirmed RPI loop.
* Disposition requirements: Preserve this critique unchanged; record its
  Complete / Pass outcome in the parent-owned plan/state. No finding closure
  evidence, plan correction or second critique is required.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/iot-pr557-main-refresh-plan.md](.copilot-tracking/plans/2026-10-29/iot-pr557-main-refresh-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/iot-pr557-main-refresh-phase-details.md](.copilot-tracking/details/2026-10-29/iot-pr557-main-refresh-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-29/iot-pr557-main-refresh-research.md](.copilot-tracking/research/2026-10-29/iot-pr557-main-refresh-research.md) | Supplied C1-C8 evidence |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-pr557-main-refresh-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-pr557-main-refresh-plan-critique.md) | Original independent critique |

## Next Steps

The active planning parent may finalize and continue to Implement within the
confirmed loop. No user action is required. This critique stops here; it does
not invoke another phase or authorize publication.
