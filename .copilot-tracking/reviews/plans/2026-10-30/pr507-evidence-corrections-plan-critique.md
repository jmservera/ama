---
title: PR 507 evidence corrections final-candidate plan critique
description: One independent bounded assessment of the correction plan and phase details
ms.date: 2026-10-30
---

## Metadata

* Task ID: pr507-evidence-corrections
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/pr507-evidence-corrections-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/pr507-evidence-corrections-phase-details.md
* Critique execution status: Complete
* Execution count: One independent final-candidate critique; no nested agents.

## Inputs and Criterion Boundary

* Caller requirements: Correct the two supplied PR #507 comments on feat/rubric-src-198; separate discarded fixture/guide work and historical results from the integrated documentation-only 355 passed / 18 failed / 7 skipped candidate; distinguish original and integrated frozen references; prepare an owner-applied replacement description with Refs #198 and no closing-keyword references; use a genuinely registered B6 recovery route and a proposed later PR.
* Lifecycle requirements: Research, Plan, Implement and independent Review, followed by a local Conventional Commit with authenticated privacy-safe identity and the required Copilot trailer. No push, remote metadata update, score edit, test additions/removals, full API suite or heavy publication gate.
* Supplied evidence: .copilot-tracking/research/2026-10-30/pr507-evidence-corrections-research.md, C1-C8/W1; docs/architecture/cutover-evidence-pack.md:2110-2270; .github/rubric/artifacts.json; the original 2026-10-27 Review and latest 2026-10-30 synchronization changes/Review referenced by research.
* Relevant implementation context inspected: .github/rubric/scripts/test_prepare.py:263-348; .github/rubric/scripts/prepare.py:250-310; .github/rubric/scripts/gate.py:181-198. Required project framing/index/memory and the customer primer were consulted for context, not as proof of rubric outcomes.
* Decisions and dependencies: Preserve old tracking bytes and log prefix; change only the three documentation files and task-owned dated evidence; preserve inherited adverse results and historical acceptance gaps; defer B6 content improvements, remote application and publication.
* Assessment boundary: Plan credibility and evidence consistency only. No implementation, suite execution, dependency installation, commit, fetch, external-body creation or remote write. The active instruction prohibiting all file operations in temporary directories applies to future execution as well as this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C2; P01-T01; both supplied comments | Covered | Correct existing downstream prose, fixture claims and both acceptance rows rather than adding only another disclaimer. |
| C5/C6/C7; original versus integrated boundary | Covered | Distinct historical hashes/bases, adverse integrated results and a separate corrected-candidate freeze are required. Independent read-only hash verification supports the supplied integrated reference. |
| C3/C4; B6 recovery | Covered | src/README.md belongs to solution-code and informs B6; the rubric guide is not registered. Proposed later PR is named without inventing a number, changed evidence or score increase. |
| Replacement description and owner application | Partial | Content and no-remote-write boundaries are sound; the required output location conflicts with the active filesystem restriction, PC-001. |
| C8; P02-T01; zero test changes | Partial | Existing focused selectors, actual prepare/matcher, links/anchors, protected bytes and whitespace are appropriate. Validation storage and fixture destinations need correction, PC-001. |
| P02-T02; independent Review and local persistence | Covered | Separate source/body hashes, one independent Review, authenticated local identity, trailer and clean-status verification; no same-task Review loop or publication claim. |
| Full four-stage RPI and exclusions | Covered | Research, this critique-backed Plan, implementation tasks and independent Review are explicit. Two implementation phases do not omit an RPI stage. |
| Scope preservation and adverse evidence | Covered | No source/fixture/guide/registry/score edits; old evidence and append-only history retained. Inherited failures, skips and RV-001 remain separate follow-ups. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 1; Medium 0; Low 0.
* Rationale: The substantive documentation correction, frozen-reference model and bounded validation strategy are credible. One execution-contract conflict must be resolved in the plan before implementation can fulfill its acceptance criteria without violating the active filesystem restriction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned external output and validation storage violate the active filesystem boundary

* Related IDs: User Decisions and Requirements; Acceptance Criteria; Dependencies; P01-T01; P02-T01; P02-T02.
* Evidence: The plan requires creating /tmp/pr507-body.md and using temporary external test storage. The phase details require creating that body, an isolated external --target dependency installation and external validation logs. The caller also requests /tmp/mv. Active higher-priority execution instructions prohibit file operations in /tmp, /var/tmp or temporary directories and require created intermediate/scratch files to be project-relative. Existing focused tests use pytest tmp_path, as shown in .github/rubric/scripts/test_prepare.py:263-348, so merely relocating the body would not resolve the entire execution conflict.
* Concern: The plan declares no blockers while making a forbidden destination an acceptance requirement and leaving dependency, fixture, cache and log destinations outside a compliant execution contract. Installing pytest externally or running default temporary-directory fixtures could violate that contract even without editing production inputs.
* Impact: Implementation cannot honestly satisfy the plan as written. Silent substitution would also leave the body existence criterion, validation provenance and final clean-worktree claim inconsistent.
* Smallest useful change: Revise the plan and phase details to disclose that the literal requested temporary paths cannot be used under the active instruction. Define compliant project-relative, task-owned non-temporary output/validation locations and explicit runner, pytest fixture, dependency, cache and log placement. If the requested interpreter cannot be used compliantly, record that limitation and the permitted alternative rather than claiming the requested invocation ran. Preserve zero test-source changes, the three-document source boundary and no remote writes. State how generated files are excluded from staging and retained or handled under the existing retention policy without deleting original evidence. Carry the replacement-body location deviation into the changes record and final owner handoff.
* Action owner: Planning parent.
* Exact resolving evidence: Revised plan and details contain no instruction to create or operate on forbidden temporary paths; they name the actual permitted replacement-body location and complete validation-output/fixture environment. Acceptance and dependency sections agree with those paths. Subsequent implementation evidence records the exact compliant commands and actual body location, and the independent Review checks their scope and provenance without claiming /tmp/pr507-body.md was created or /tmp/mv was used if they were not.
* Decision route: Direct planner correction required by an existing higher-priority constraint, not a significant or divergent user decision. No user confirmation can authorize bypassing that restriction. If no compliant execution route is available, mark the affected implementation acceptance blocked and report it honestly.

## Strengths and Residual Risk

* The supplied integrated hash was independently reproduced from the current three-document diff against ffd8f35e63b24905b9aeb937dbf2a7fe9968747f: 8059b4aa91f469ff735c33c620bd23cc1b529d108a5737a08d862b53f0061883. Current starting HEAD resolves to 254d2274693c8190f827067c3732e03d102a563d.
* The latest synchronization Review assessed HEAD 86ce8f660d846a57da03ddd973ab513dd482465f plus its worktree edits. The later persistence commits retain the same three-document hash. A link to the immutable starting commit can therefore identify that historical integrated content, but must not be described as a fresh exact-head Review.
* The original de87d9e063b59ca93f178241776d82c2ac447d68efc02ba9780373fb17a75962 hash covered seven existing files against 09099ecd1a66ee9d37ad993707d1f2eda07cdfd4, not the integrated three-document path set. Retain the respective domains when presenting both boundaries.
* The plan already avoids hash self-reference: public documentation identifies immutable pre-correction history, acknowledges the correction changes that delta, and places the new corrected three-document hash and body hash in task evidence before Review. Tracking bookkeeping does not enter the three-document hash.
* Read-only protected-path comparison against the integrated base returned no src, infra, tools or .github delta. The plan preserves this boundary and never treats prepare should_score=false as a fresh score.
* The registered src README proposal and actual matcher/prepare checks address B6 without changing scored evidence now. Existing focused tests and migration regressions, links/anchors, whitespace and protected-byte checks are proportionate; no additional suite, test source change or heavy gate is requested by this critique.
* The inherited 18 failures, seven missing-runtime skips, historical #198 gaps, previous RV-001 audit locator and publication requirements remain explicit residual work, not new same-task repairs or acceptance waivers.

## Questions or Blocking Evidence Gaps

* No unresolved user decision or decision-critical research gap. PC-001 requires planner-owned reconciliation of an instruction conflict before execution, not further open-ended research.

## Limitations

* W1's PR metadata and exact comment retrieval were assessed through supplied research; no new GitHub request or remote-state certification was performed.
* Historical suite counts were assessed through supplied changes/Review evidence, not rerun or independently certified from external raw logs.
* No filesystem operation on the requested external body or environment was performed. Their current existence, contents and usability are not certified.
* This is the complete actionable finding set for the supplied boundary. No cosmetic changes, second critique or implementation work are requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Reconcile output and validation locations with the active filesystem restriction in the plan/details and record the disposition, then finalize planning without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/pr507-evidence-corrections-plan.md](.copilot-tracking/plans/2026-10-30/pr507-evidence-corrections-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/pr507-evidence-corrections-phase-details.md](.copilot-tracking/details/2026-10-30/pr507-evidence-corrections-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-30/pr507-evidence-corrections-research.md](.copilot-tracking/research/2026-10-30/pr507-evidence-corrections-research.md) | Supplied evidence and scope decisions |
| [.copilot-tracking/reviews/plans/2026-10-30/pr507-evidence-corrections-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/pr507-evidence-corrections-plan-critique.md) | Sole independent critique and complete finding set |

## Next Steps

Return Complete / Revise to the active planning parent. Parent resolves PC-001 directly, records the execution-location deviation and finalizes without another critique. No user action is required. Stop here; no implementation, source revision or peer stage is invoked.
