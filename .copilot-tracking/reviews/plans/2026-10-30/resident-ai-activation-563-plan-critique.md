---
title: Resident AI activation 563 plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: 563 / resident-ai-activation-563.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/resident-ai-activation-563-phase-details.md.
* Critique execution status: Complete.
* Assessment: exactly one final-candidate pass; no cloud actions or source edits.

## Inputs and Criterion Boundary

* Caller requirements: resident ca-resident-demo only; USD20 ceiling;
  exclusive 2026-11-01 pilot expiry; redeploy authority through November15;
  exact private backup before mutation; prefer account-only managed-identity
  access; min0; every job Manual; no new networking, groups or broad RBAC;
  at most two sign-ins and no credential disclosure; local commit only,
  Refs #563, no push.
* Supplied research:
  .copilot-tracking/research/2026-10-30/resident-ai-activation-563-research.md,
  including C1-C8, selected alternative and residual uncertainty.
* Decisions and dependencies: private SQL preflight failed with 47073 because
  the public network interface is disabled. Existing narrow role/model are
  reported correct. P01-T01 precedes anonymous checks; reconciliation precedes
  Review, local persistence and the external full local gate.
* Acceptance boundary: AC1-AC5 are safe-stop deliverables, explicitly not
  activation acceptance. Assess whether the proposed backup, read-only
  configuration checks, anonymous health/denial checks and honest handoff
  fulfill the conditional stop request without expanding authority.
* Repository context: original case study, resident-service section of the
  addendum, reference-index opening and owner memory were read for scope and
  consent context. They are not new live operational evidence.
* No fresh source, Azure, SQL, HTTP, identity, model or gate verification was
  performed. Research evidence is assessed as supplied, not independently
  reproduced. No additional research was conducted.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Resident-only scope; existing account-only MI role/model | Covered | Research C2/C7 and plan scope prohibit identity grants or unrelated activation. |
| USD20 and exclusive November1 boundary | Covered for safe stop | No activation or paid inference; source-pinned limits are not claimed as verified live SQL controls. November15 redeploy authority does not extend AI authority. |
| Exact private backup; FR1 / AC1 / P01-T01 | Covered | Exact app/revision/auth/jobs responses, protected directory/files, timestamps and hashes; failure blocks further operation. Secret values are not requested or changed. |
| min0; Manual jobs; no networking/groups/broad RBAC; FR2 / AC2 | Covered | Before/after configuration comparison; no job execution, SQL mutation, role creation or networking changes. |
| Anonymous health/denial; FR3 / AC3 / P01-T02 | Covered | Bounded cold-start retries, synthetic no-record-use POST, expected 401/403; explicit failure is permitted and cannot become model-readiness proof. |
| Sign-in/credential limits | Covered | Zero sign-ins, no cookies, credentials, screenshots or model calls on the selected path. |
| C5/C6/C8; FR4 / AC4; P02-T01 | Covered | Unreachable accounting state remains Unknown. An initializer's historical omission is not proof that the deployed migration is absent. |
| Conditional activation and rollback | Covered as future work only | Private proof precedes any later activation; missing migration requires separate approval; fresh backup and valid authority remain necessary. No rollback is claimed necessary for this unchanged candidate. |
| Test ownership and locked boundary | Covered | Source/test removals: none. Source/test additions: zero. Configuration equality and anonymous behavior do not replace authenticated actual-model acceptance. |
| AC5 / P02-T02; independent Review dispositions | Partial | PC-001: unconditional deferral of Review findings can leave defects in the safe-stop deliverable unresolved. |
| Local commit, Refs #563, no push; external full gate | Covered | Local-only persistence, privacy-safe identity and trailer; unavailable prerequisites remain blockers, not fabricated passes or permission to publish. |

## Verdict

* Verdict: Revise.
* The selected no-activation alternative safely and honestly fulfills the
  conditional stop request in principle. SQL proof is a prerequisite, not a
  reason to open networking, execute a job or assume a missing migration.
  One direct planner correction is required in Review disposition handling;
  no significant or divergent user decision is necessary.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Distinguish blocking Review defects from deferred activation work

* Related IDs: AC5; P02-T02; Test Ownership and Locked Boundary.
* Evidence:
  .copilot-tracking/details/2026-10-30/resident-ai-activation-563-phase-details.md,
  P02-T02 says, "Route findings to later work without a repeated Review,"
  then proceeds to local commit and the full gate.
  .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-plan.md
  requires independent post-implementation Review and honest evidence.
* Concern: The blanket deferral does not distinguish an accepted inability to
  activate from a defect in the current safe-stop candidate. A Review finding
  about exposed configuration, an unsupported denial/success claim or a
  configuration mismatch cannot safely be treated merely as future activation
  work.
* Impact: The executor could persist misleading or unsafe evidence while
  implying that the safe-stop deliverable passed independent Review. A local
  gate does not resolve or override a substantive Review finding.
* Smallest useful change: Amend P02-T02 to preserve the original Review and
  disposition every finding. Correct in-scope, directly resolvable evidence
  defects before treating the candidate as complete; defer only explicitly
  identified future activation work or accepted residual limitations. If a
  material finding cannot be resolved within scope or needs unavailable
  independent validation, record the candidate as Blocked/not accepted rather
  than implying a passing Review. Keep the one-Review/no-repeat boundary and
  distinguish any subsequent correction validation from that original Review.
* Action owner: Planning parent; operations executor records implementation
  dispositions.
* Exact resolving evidence: Revised P02-T02 explicitly contains the
  fix/defer/block rule above. During execution, the preserved original Review
  and dated changes evidence map each finding to its correction and actual
  validation, accepted future-work disposition or unresolved blocker; no
  corrected candidate inherits an unsupported independent-Review pass.
* Decision route: Direct planner correction. Existing user direction already
  requires safe stopping and honest reporting; no significant/divergent user
  decision or additional critique pass is required.

## Strengths and Residual Risk

* Missing private SQL proof is correctly separated from known absence of a
  migration. The existing account role/model do not need replacement.
* No activation, paid request, sign-in, SQL/job/network mutation or new
  resource is admitted by the selected implementation path.
* Exact private configuration capture and unchanged-configuration evidence
  preserve reversibility without fetching secret values.
* Unperformed consent, grounded-answer, model fallback and authenticated unset
  checks remain explicitly unperformed; #563 remains unmet/open.
* Private SQL state, permissions, remaining budget and rate allowance remain
  unknown. That uncertainty is deliberately contained by not activating.
* Failed anonymous checks or unavailable full-gate prerequisites must be
  recorded as actual failures/blockers, never reclassified as success.

## Questions or Blocking Evidence Gaps

* No user question is required for the selected safe stop.
* Live activation remains blocked on an authorized private SQL receipt and
  valid activation authority. This does not block assessing the stop plan and
  does not authorize migration or alternate access.

## Limitations

* This is a plan credibility assessment, not live verification, operational
  acceptance, a fresh legal assessment or a completed local gate.
* The read-only status inspection showed the supplied research/plan/details
  and session state already untracked on ops/resident-ai-activation-563.
  Those existing files were neither modified nor staged.
* Only this critique artifact was written. No plan, details, research, state,
  application source or cloud configuration was changed.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: Planning parent.
* Smallest next action: Directly correct P02-T02's Review disposition rule,
  record this critique's disposition, then finalize the safe-stop plan without
  another critique. Execution may continue only within its unchanged
  no-activation boundary.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-ai-activation-563-research.md](.copilot-tracking/research/2026-10-30/resident-ai-activation-563-research.md) | Supplied evidence and SQL uncertainty. |
| [.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-plan.md](.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-plan.md) | Safe-stop final candidate assessed. |
| [.copilot-tracking/details/2026-10-30/resident-ai-activation-563-phase-details.md](.copilot-tracking/details/2026-10-30/resident-ai-activation-563-phase-details.md) | Executor tasks; PC-001 correction target. |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-plan-critique.md) | Original single-pass critique. |

## Next Steps

Planning parent: resolve PC-001 directly and preserve this original Revise
outcome; do not request another critique. No user action is required.
