<!-- markdownlint-disable-file -->
---
title: Independent plan critique - resident survey publication correction1
description: Single final-candidate assessment of validation and publication controls
ms.date: 2026-10-31
---

## Metadata

* Task ID: 571-correction1.
* Task slug: resident-survey-check-571-correction1.
* Critique date: 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction1-plan.md.
* Phase details: .copilot-tracking/details/2026-10-31/resident-survey-check-571-correction1-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate critique.
* Write boundary: this critique only. Original and correction inputs remain unchanged.

## Inputs and Criterion Boundary

* Caller requirements: preserve the authorized latest-main merge, main rubric,
  both log histories and unchanged workflow hashes; use pip only; execute the
  requested API/Ruff/light checks without a lock and standalone resident browser
  with the same global lock, 1800-second admission and one admission retry.
  The full runner owns its lock internally and must use --lock-timeout 1800,
  never an outer flock.
* Publication requirements: commit dated original correction Review evidence,
  run the full current-main exact-head gate, verify its external receipt and
  obtain independent exact-head assessment before non-forced branch publication
  and a main PR. Hosted and owner approval remain separate.
* Scope lock: zero new or removed tests, zero source/assertion changes, only
  correction artifacts. No Azure, private data, secrets, force push, nested
  agents, tests, git mutation or further Review during this critique.
* Research: the complete supplied correction research, C1-C7, Q1-Q3, alternatives,
  provenance, readiness and risks. Relevant original research, original changes
  and original Review were inspected as immutable historical evidence.
* Decisions: original RV-001 permission is settled by current owner direction;
  original RV-002 human/AT/live limits remain open. Neither is re-decided here.
* Acceptance boundary: the caller identifies three issue criteria: root cause,
  local check/prompt agreement and acceptance not weakened. A closing keyword
  requires independently reviewed proof of all three; otherwise use Refs #571
  and name unproven criteria. These criteria do not require pretending that
  synthetic checks establish human, AT, live or actual-model acceptance.
* Supporting sources inspected: src/README.md local-gate contract;
  tools/rpi-checks.py locking, verification and external-output admission;
  src/api/checks/resident_assistant_browser_check.py positive and fresh-refusal
  assertions; src/api/README.md correction explanation and acceptance limits.
  Required project framing, knowledge-base index and owner memory were read;
  memory is context, not evidence.
* Read-only local identities: HEAD
  e2e815e22432441887597e5ab7e97bcb4282ca0f; origin/main
  a75bbdffa51ae34b1fcf779250f1f553d566ee93.
  The current main-to-candidate committed diff retains the seven browser-check
  lines and five guide lines plus original artifacts. Inspected workflow,
  runner and knowledge-log diffs against main are empty. No fetch was performed.
* Boundary: assess planning credibility and supplied provenance, not certify
  forthcoming executions, a fresh receipt, an exact-head approval or PR closure.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| G1; FR1; AC1; C1-C2; Q1 | Covered | Authorized merge identities and preservation checks; no source correction or workflow-hash update proposed. |
| G2; FR2; AC2; C3-C4; Q2 | Covered | Fresh API discovery, API Ruff check/format and full synthetic resident browser retain positives and fresh obsolete-input refusals. |
| NFR1; coverage lock | Covered | Task-owned pip environment, no shared editable mutation, no added/removed tests or source assertions. |
| NFR2; C5; P01-T01 | Covered | Light checks unlocked; standalone browser shares global lock with one admission retry; no retry of an executed failing test. |
| FR3; AC4; C5-C6; P02-T02 | Partial | Correct full-runner native locking and committed exact-head order, but publication eligibility lacks an explicit finding/assessment disposition guard; PC-001. |
| NFR3; AC2; AC5; Q3 | Covered | Failures, skips and axe incompletes retained; conditional closure and human/AT/live/model boundaries explicit. |
| NFR4; P02-T02 | Covered | Authenticated privacy-safe author/committer, local configuration and required trailer retained. |
| P01-T01 | Covered | Verify main invariants and run existing requested checks; no foreign-output reuse. |
| P01-T02 | Covered | Reconcile actual commands, hashes, base/head, adverse attempts, canonical changes/state and remaining work before Review. |
| AC3; P02-T01 | Partial | Exactly one independent correction Review is sequenced correctly; disposition and fail-closed continuation need PC-001. |
| P02 dependencies | Covered | P01-T02 follows validation; correction Review follows reconciliation; publication follows Review. |
| G3; C7; original RV-001/RV-002 | Covered | Original correction and negative regression distinguished; owner-settled ancestry issue not reopened; residual acceptance not erased. |
| Drift, prerequisites and retention risks | Covered | Fresh-main verification, immutable adverse attempts, fresh external outputs, no cloud/partial fallback and no broad cleanup. |

## Verdict

* Verdict: Revise.
* Rationale: the scoped correction is credible and technically coherent.
  One direct planning correction is needed to make independent Review and
  exact-head assessment substantive publication gates rather than merely
  sequenced activities. No new user decision, source change, test addition
  or second critique is needed.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Publication must explicitly depend on resolved Review findings and an approving exact-head assessment

* Related IDs: FR3, AC3-AC4, P02-T01, P02-T02, coverage lock.
* Evidence: .copilot-tracking/details/2026-10-31/resident-survey-check-571-correction1-phase-details.md
  P02-T01 says to record the Review outcome and route residual work.
  P02-T02 depends on that task's completion and explicitly requires a passing
  full receipt, but proceeds from receipt verification to independent exact-head
  assessment and push without stating the required assessment result or the
  disposition of any correction-Review blockers.
  .copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction1-plan.md
  AC3-AC4 and P02 checklist likewise require execution and ordering, not an
  explicit no-publication guard for unresolved findings.
* Concern: a Complete Review can report a defect or unresolved blocker, as the
  immutable original Review demonstrates with its separate Complete /
  Residual work statuses. Finishing Review, or simply obtaining an exact-head
  assessment, is not itself approval. The frozen source/test boundary also
  leaves no authorized in-task source repair or repeat-Review loop if a new
  source defect is found.
* Impact: automatic continuation could satisfy task dependencies and publish
  after adverse independent evidence despite a passing automated receipt.
  Conversely, improvising a source correction or another Review would violate
  the current correction's authorized boundary.
* Smallest useful change: add a fail-closed continuation rule to P02-T01/P02-T02
  and AC3-AC4. Before publication, record each correction-Review finding's
  disposition and distinguish accepted non-blocking residual limits from
  unresolved blockers. Require an explicit approving independent exact-head
  assessment bound to the committed HEAD, fetched main and verified full
  receipt identity. An adverse, missing or stale assessment, unresolved
  blocker, or required source/test change stops publication. Compatible
  artifact-only dispositions occur before the final commit/gate; any later
  commit or input change requires a fresh full gate and verification.
  Preserve the single correction Review and immutable original outcomes.
* Action owner: planning parent, for the direct plan/details correction and
  disposition contract; delivery parent, for enforcing the stop; independent
  exact-head assessor, for the explicit bound assessment result.
* Exact resolving evidence: amended P02-T01/P02-T02 and AC3-AC4 state those
  conditions and the stop route within the frozen coverage boundary. At
  execution, committed correction Review/dispositions show no unresolved
  publication blocker; external assessment records an approving result for
  the exact candidate/base and verified full receipt, before push.
  No fabricated approval or post-gate evidence commit resolves this finding.
* Decision route: direct planner correction. Current owner direction already
  establishes the independent gate and source/test lock; no significant or
  divergent user decision is needed. If future evidence requires prohibited
  source changes, report the blocker rather than expanding this task.

## Strengths and Residual Risk

* Native runner locking is supported by the inspected implementation; no outer
  flock, changed global lock, weaker tier or workflow edit is recommended.
* Existing positive document facts and negative fresh-turn refusal assertions
  remain intact. The plan does not reinterpret synthetic success as semantic,
  human, assistive-technology or live approval.
* Latest-main merge authorization settles original RV-001 prospectively without
  rewriting its historical finding or the original ancestry-rejection evidence.
* Original RV-002 remains a separately owned acceptance limit, not an introduced
  correction defect or an automatic reason to declare all three issue criteria
  failed. Closure still requires their actual reviewed evidence.
* Current main can advance during validation; external receipt verification must
  fail closed on changed base/head/tools/images or dirty inputs. Hosted checks
  and the owner merge decision remain outstanding after any eligible PR.

## Questions or Blocking Evidence Gaps

* No decision-critical user question is required for this plan correction.
* Fresh validation, correction Review, receipt and exact-head assessment are
  intentionally future evidence, not missing historical successes to invent.

## Limitations

* No tests, installation, browser run, git mutation, nested delegation or further
  Review occurred. Only this critique artifact was written.
* External temporary-directory evidence and environments were not opened.
  Historical execution results and environment readiness are supplied
  provenance, not independent re-execution or filesystem certification.
* No live issue fetch, legal-currentness assessment, private-data inspection,
  model call or cloud operation occurred. Issue-criterion wording is assessed
  from the caller and supplied research, not independently refreshed issue state.
* The critique is complete for the supplied candidate boundary; it does not
  approve an as-yet uncommitted final candidate or a future publication.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly add the Review-disposition and approving
  exact-head publication guard, record this critique's disposition, then
  continue the authorized phases without another critique.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction1-plan.md](.copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction1-plan.md) | Candidate plan and acceptance criteria |
| [.copilot-tracking/details/2026-10-31/resident-survey-check-571-correction1-phase-details.md](.copilot-tracking/details/2026-10-31/resident-survey-check-571-correction1-phase-details.md) | Validation and publication sequence |
| [.copilot-tracking/research/2026-10-31/resident-survey-check-571-correction1-research.md](.copilot-tracking/research/2026-10-31/resident-survey-check-571-correction1-research.md) | Supplied correction evidence and decisions |
| [.copilot-tracking/changes/2026-10-31/resident-survey-check-571-changes.md](.copilot-tracking/changes/2026-10-31/resident-survey-check-571-changes.md) | Immutable original execution and failed-gate history |
| [.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-review.md](.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-review.md) | Immutable original Review and residual limits |
| [.copilot-tracking/reviews/plans/2026-10-31/resident-survey-check-571-correction1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/resident-survey-check-571-correction1-plan-critique.md) | This single complete finding set |

## Next Steps

Planning parent directly resolves PC-001 and finalizes the plan without a second
critique. Continue the single authorized correction Review and gated publication
only under the explicit eligibility conditions. No user action is required.
