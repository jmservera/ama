---
title: Issue 86 recorder identity final-candidate plan critique
ms.date: 2026-10-18
---

## Metadata

* Task ID: 86 / issue-86-recorder-identity.
* Critique date: 2026-10-18.
* Plan: .copilot-tracking/plans/2026-10-18/issue-86-recorder-identity-plan.md.
* Phase details: .copilot-tracking/details/2026-10-18/issue-86-recorder-identity-phase-details.md.
* Critique execution status: Complete.
* Branch: fix/review-recorder-identity-86.
* Verified HEAD and supplied exact base: 6c1e376ff1241316272df22a5a3a6853aae9f87b.
* Execution: exactly one independent final-candidate plan critique; no implementation, code security audit, second critique or original Review performed.

## Inputs and Criterion Boundary

* Assessed the complete supplied plan, phase details, research C1-C10, reproducible synthetic probe and saved failing-first results in .copilot-tracking/research/2026-10-18/.
* Applied the caller's confirmed requirements: stable code OR oid detects changed-email recorder at opening and redress reassignment; server-derived new snapshots; exact historical decision binding; no client identity override, current-email-owner backfill or legacy reconstruction; explicit Unknown with narrow review-assignment refusal only.
* Assessed preservation of existing role restrictions, unrelated consent/service access, isolation, hazards and remedies, atomic case/successful-audit refusal, JSON/SQLite restart, authenticated HTTP, role projection/export and mandatory actual task-owned loopback MSSQL validation for changed persisted bodies.
* Applied the locked test boundary: no removals or weakened existing assertions; at most eight core and two API new methods in existing test_resident_decisions.py and test_resident_api.py, using inherited/subtest matrices.
* Assessed P01-P03, AC1-AC7, sequencing, dependencies, acceptance gates, evidence freezing, immutable original assessments, bounded correction cycles and publication handoff. The current critique does not authorize those later actions.
* Read mandatory project context and directly relevant resident implementation, registered actor helper, SQL writer replay, projections, model facts/export paths, resident tests, API route and component validation configuration. No open-ended research, external service access, private datasets, support material, environment files, Azure/IAM/Graph, inference, spending or web changes.
* Formal complaints integration, historical erasure, contact identity and human acceptance remain unmet. Issue #86 stays open; this work grants no #130/#76 authorization.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1-AC2; C1-C2; P01-T01 | Covered | Shared normalized email/code/oid comparisons, code-only and oid-only changed-email denials on both assignment paths, and distinct-reviewer positive controls are explicit. |
| AC3; C3-C4; P01-T01/T02 | Covered | Registered actor resolution, detached server snapshot, decision recorder-role restriction, transactional operation and SQL replay are specified. AC3 makes current-registry-race refusal mandatory despite the detail's conditional wording about adding a test. |
| AC4; C6-C7; P01 | Covered | Unknown, no current-owner backfill, no historical rewrite, and continued unrelated consent/service/complaint and service-owner operations are explicit. |
| AC5; C6; P01-T01/T02 | Partial | Bound new requests survive payload deletion, but legacy fallback does not explicitly prevent reuse of a deleted decision's measure/version ordinal. PC-001. |
| AC6; C5/C8; P01-T02/P02-T01 | Covered | Actual authenticated local HTTP, unauthorized role/export canaries and existing resident/hazard/quality/remedy regressions are required. Projection exclusion is explicit; existing facts/export code uses selected fields rather than serializing new snapshots. |
| AC7; C4/C9; P02-T01 | Covered | Actual task-owned loopback MSSQL is mandatory, including inherited resident controls; JSON bodies do not justify skipping it. Quality commands, errors/skips, exact evidence and cleanup are specified. |
| C10; P01-T02 | Covered | All eight supplied adverse JSON/SQLite probes record successful assignments and changed case/audit, with expected assertion failure. Probe retention is required, not used to replace semantic tests. |
| Test and scope locks; P01-P02 | Covered | Existing test files, eight/two method ceiling, inheritance/subtests, no removals/generated targets, narrow dependent documentation and no unrelated redesign are explicit. |
| P03-T01; dependencies and publication | Covered | One immutable original Review, exact candidate, separately receipted corrections, normal branch publication, no unilateral integration and coordinator exact-head review are specified. |
| Outstanding original issue acceptance and dependent gates | Covered | No closure or claims of formal complaints, erasure, contact or human acceptance; no dependent authorization. |

## Verdict

* Verdict: Revise.
* Severity summary: Critical 0; High 1; Medium 0; Low 0.
* The bounded approach is otherwise credible. One directly coupled historical-binding edge must be made explicit before implementation. This is a planning correction, not a request for retention redesign or additional policy authorization.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Prevent legacy review fallback from binding a reused decision version after retention deletion

* Related IDs: AC4-AC5, C6, P01-T01, P01-T02, P02-T01.
* Evidence:
  * .copilot-tracking/plans/2026-10-18/issue-86-recorder-identity-plan.md:72-78 permits legacy requests to resolve an actual historical snapshot from their recorded measure/version.
  * .copilot-tracking/details/2026-10-18/issue-86-recorder-identity-phase-details.md:35-39 specifies exact integer/version-field matching and retained bound snapshots, but not how an unbound legacy request distinguishes the original decision from a reused ordinal.
  * src/core/src/zava_forward/core/resident_decisions.py:375-399 deletes measure_decisions while retaining service_requests.
  * src/core/src/zava_forward/core/resident_decisions.py:478-493 assigns new decision versions using len(versions) + 1. src/core/tests/test_resident_decisions.py:159-195 demonstrates deletion followed by fresh scope/answer and a new one-entry decision history.
  * src/core/src/zava_forward/core/resident_decisions.py:528-540 retains review_measure, review_decision_version and the legacy reviewed_actor label on review requests.
* Concern: Measure plus integer version, including a matching version field, is not necessarily a unique historical decision across payload deletion. A preserved legacy request with no bound reviewed_identity may refer to old measure M/version 1. After deletion and new recording, M/version 1 can exist again with a genuine new server snapshot. Using that snapshot as the old request's historical identity establishes independence against the wrong recorder. The plan does not expressly exclude this fallback or include this collision in its test matrix.
* Impact: An original recorder whose email changed could receive redress responsibility on the old review because the replacement decision was recorded by someone else. A valid new snapshot does not cure missing evidence about the original contested decision. This would violate exact historical binding and Unknown fail-closed requirements while apparently passing ordinary newer-version and payload-removal tests.
* Smallest useful change: State in the plan and P01 details that legacy fallback may never accept an ordinal match alone when original decision provenance is absent or cannot be established, including deleted-and-recreated histories. Leave that request Unknown and refuse only its dependent independent-redress assignment. Conservatively retaining Unknown for an unbound legacy request is sufficient; do not add a migration, global versioning scheme, current-owner lookup, retention change or historical backfill. Preserve the positive path for a new request with its own bound snapshot after deletion.
* Action owner: Planning parent for plan/details/acceptance matrix; parent implementer for the corresponding bounded guard and regression evidence.
* Exact resolving evidence:
  1. Revised AC5/P01-T01 expressly distinguishes a retained bound snapshot from an unbound legacy pointer to a recycled measure/version and requires Unknown on unprovable original binding.
  2. P01-T02 includes a synthetic inherited/subtest scenario, within the eight/two method caps: retain a legacy review lacking reviewed_identity; remove the original resident payload through the existing deletion path; record a new decision with the same measure/version but a different recorder; restart; attempt redress reassignment to the changed-email original recorder. It must refuse with case and successful audit unchanged, remain Unknown without rewriting legacy evidence, and not copy the replacement snapshot into the old request.
  3. Positive controls retain a genuinely bound new review's original identity across deletion/recreation and allow unrelated supplied consent/service actions and permitted service-owner reassignment.
  4. P02 requires executed JSON/SQLite restart and actual task-owned loopback MSSQL evidence for that matrix; authenticated HTTP exercises the refusal/positive boundary using the existing API test allowance. No new test module or larger method allowance is needed.
* Decision route: Direct planner correction. Current user direction already requires exact historical binding, no invented legacy evidence and narrow fail-closed behavior; no significant or divergent user decision is needed.
* Evidence classification: Confirmed source behavior establishes deletion/version reuse. The incorrect future fallback is a plan ambiguity and foreseeable implementation risk, not a claim that an unimplemented candidate has already exhibited it.

## Strengths and Residual Risk

* Existing resident workflows are reused rather than replaced. Decision writes explicitly retain recorder-role restrictions when entering the broader transactional follow-up boundary.
* The plan rejects today's email owner as historical proof, ignores client identity claims, and binds new requests independently of payload retention.
* Code-only and oid-only matrices, genuine distinct reviewers, malformed legacy evidence, durable refusal atomicity, real HTTP and actual SQL Server are appropriately bounded acceptance gates.
* The saved probe establishes the original email-change failure on the exact base; it does not establish that the planned fix or broader acceptance has passed.
* Human/formal acceptance and historical erasure remain explicitly open. Their exclusion is caller-directed, not waived or solved by this critique.

## Questions or Blocking Evidence Gaps

* No unresolved user choice or decision-critical research gap prevents this assessment. PC-001 can be resolved directly within the existing scope and test budget.
* Actual MSSQL and post-change validation remain implementation-phase obligations. Research reports driver import and image availability, not completed SQL Server parity.

## Limitations

* This is a plan credibility assessment, not an implementation review, security audit or acceptance certificate. No application tests, probe, HTTP server, SQL container or quality checks were executed by this critique.
* Direct source reads were limited to assessing supplied requirements and research claims. No external issue retrieval or additional discovery was required.
* The plan, details, research, saved probe/results, source, tests and session state were not edited. Existing untracked planning inputs were left in place. Only this critique artifact was created.
* The original assessment is this artifact; subsequent dispositions must not replace or revise its verdict or finding text.

## Input Fingerprints

SHA-256 fingerprints of the assessed supplied artifacts:

| Workspace-relative path | SHA-256 |
| --- | --- |
| .copilot-tracking/plans/2026-10-18/issue-86-recorder-identity-plan.md | 1ec8c30658f033b7e3c020c0564a51c2066b38ef68ab7aaa4bfc906f5ece5df2 |
| .copilot-tracking/details/2026-10-18/issue-86-recorder-identity-phase-details.md | 7e51708a4b35e8ec06742d04bba6bb53b27fe55c890a879e7e8f96dd507ad334 |
| .copilot-tracking/research/2026-10-18/issue-86-recorder-identity-research.md | bac84bab8cae3a189da43a6e7cea9d5cc32968d6a371eb05ce166e4a7e9f03d4 |
| .copilot-tracking/research/2026-10-18/issue-86-recorder-identity-probe.py | 6e039ee617f2ed3e65ea85907ed5ab2f54b1cb291a83d42a1e089c5babb5f257 |
| .copilot-tracking/research/2026-10-18/issue-86-recorder-identity-before.txt | ce534bab00d9f712dae81066bab663735ee7e4ee9eaaf4557d8268c139fc1cf6 |

## Recommended Next Action

* Highest-impact finding: PC-001, High.
* Action owner: Planning parent.
* Smallest next action: Make original-versus-reused decision binding explicit in AC5 and P01, and include the collision in the existing inherited/subtest matrix.
* User response required: No.
* Complete actionable finding set for this supplied boundary: PC-001 only. No additional findings are withheld for a later pass.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue-86-recorder-identity-plan.md](.copilot-tracking/plans/2026-10-18/issue-86-recorder-identity-plan.md) | Assessed final-candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-18/issue-86-recorder-identity-phase-details.md](.copilot-tracking/details/2026-10-18/issue-86-recorder-identity-phase-details.md) | Assessed phase details, unchanged. |
| [.copilot-tracking/research/2026-10-18/issue-86-recorder-identity-research.md](.copilot-tracking/research/2026-10-18/issue-86-recorder-identity-research.md) | Supplied C1-C10 evidence and scope decisions. |
| [.copilot-tracking/research/2026-10-18/issue-86-recorder-identity-probe.py](.copilot-tracking/research/2026-10-18/issue-86-recorder-identity-probe.py) | Supplied synthetic probe, not rerun or changed. |
| [.copilot-tracking/research/2026-10-18/issue-86-recorder-identity-before.txt](.copilot-tracking/research/2026-10-18/issue-86-recorder-identity-before.txt) | Original failing-first results, unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-86-recorder-identity-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-86-recorder-identity-plan-critique.md) | This original Complete / Revise assessment. |

## Next Steps

The active planning parent should directly disposition PC-001 and finalize the corrected plan without another critique. No user action is required. Preserve this original assessment unchanged. This critique stops here: no implementation or original Review is authorized or performed by this invocation.
