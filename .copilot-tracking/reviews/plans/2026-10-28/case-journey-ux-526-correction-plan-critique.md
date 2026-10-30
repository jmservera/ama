---
title: Case journey correction final-candidate plan critique
description: Independent bounded assessment of seven PR 529 preservation fixes and publication feasibility
ms.date: 2026-10-28
---

## Metadata

* Task ID: 526-correction, PR #529
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/case-journey-ux-526-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/case-journey-ux-526-correction-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: correct the seven named preservation defects; preserve
  the stepper; no Azure/az, secrets or .env; normal push only. The full RPI loop
  is already user-authorized. This critique cannot implement or launch agents.
* Research: .copilot-tracking/research/2026-10-28/case-journey-ux-526-correction-research.md,
  C1-C6 and the seven recorded review thread identifiers.
* Inspected source: src/api/src/zava_forward/api/web/app.js,
  src/api/src/zava_forward/api/web/assistants.js,
  src/api/src/zava_forward/api/web/ops.js and
  src/api/src/zava_forward/api/web/panels.js at the affected functions.
* Inspected validation contracts: src/api/checks/case_journey_browser_check.py,
  src/api/checks/assistants_browser_check.py, src/README.md:61-158 and
  tools/rpi-checks.py at tool discovery, preflight, clean candidate identity,
  receipt verification and lock admission.
* Repository context: original case study, relevant addendum context, reference
  index and owner memory. Memory was not treated as evidence.
* Dependencies and acceptance: P01-T01 through P01-T04 precede P02 validation;
  original independent Review and committed evidence precede publication gate;
  publication depends on the applicable complete gate and exact-head checks.
  Existing test ownership, no-removal and maximum-addition locks are accepted.
* Live read-only branch evidence: PR #529 is OPEN, targets main and uses
  feat/case-journey-ux-526 at d3fbba5807d574136bc77307b4e95c2fec657654.
  The worktree contains untracked correction planning/research/state artifacts;
  the plan's clean-branch statement describes its earlier starting point, not
  the current gate-ready state. No branch or existing input was moved.
* Boundary: assess repair credibility, deterministic regression coverage and
  validation/publication feasibility. This is not implementation Review, a
  fresh UI/accessibility audit, legal validation or live deployment acceptance.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| PRRT_kwDOUU8JX86xUr6L; C1; P01-T01 | Covered | Retain complete document output and handlers, not the upload form or an entire stale panel; refresh regression specified. |
| PRRT_kwDOUU8JX86xUr6p; P01-T01 | Covered | Capture submitted replacement before await; display it read-only after successful Edit and assert recorded review state. |
| PRRT_kwDOUU8JX86xUr7A; C3; P01-T02 | Covered | Session-owned unresolved snapshots, live-value precedence, explicit discard and disconnected-loader exclusion; delayed overlap regression. |
| PRRT_kwDOUU8JX86xUr7q; C2; P01-T03 | Covered | Pre-mutation snapshots for upload/handoff/resident; pre-FileReader kind; unchanged-only cleanup and retained dirty edits; held-response and failure scenarios. |
| PRRT_kwDOUU8JX86xUr8F; C4; P01-T04 | Covered | Restore measure before asynchronous checklist construction, version/item identity and separate drafts for other identities; same-measure regression. |
| PRRT_kwDOUU8JX86xUr8k; P01-T04 | Covered | Funding record_id identity, manual initial identity, copyable older edits without review actions, subsequent refresh and discard scenarios. |
| PRRT_kwDOUU8JX86xUr9C; C5; P01-T02 | Covered | Verify cleans only submitted metadata, not unsent JSON; preserve old-revision recovery and test own verification. |
| Stepper, permissions and human boundaries | Covered | No journey algorithm/file changes; existing six-step, tab, keyboard, reflow, zoom and pinned axe assertions retained. |
| C6; P02-T01; test ownership/removal/addition locks | Partial | Two existing browser checks are credible canonical owners; no removals or new runner required. Heavy execution conflicts with current path constraints, PC-001. |
| P02-T02; original evidence retention | Partial | One independent Review and unchecked human acceptance are explicit; unresolved current-scope findings must block publication, PC-003. |
| P02-T03; no az/Azure; complete gate | Partial | Source confirms the gate itself invokes az, not merely an optional cloud lane. Current branch cannot be represented as publishable under this plan, PC-002. |
| P02-T03; exact-head normal publication | Partial | Identity/trailer, normal push and evidence-backed thread resolution are sound; pre-push receipt/base/head acceptance sequence is incomplete, PC-003. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 3 High, 0 Medium, 0 Low.
* Rationale: the seven repair designs are credible and appropriately bounded.
  Validation and publication are not executable as currently described under
  the supplied constraints. These are direct planning corrections; no new
  significant or divergent user decision is necessary.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Heavy-check lock admission uses a prohibited filesystem path

* Related IDs: P02-T01, P02-T03; plan User Decisions and Requirements.
* Evidence: plan:24-25 mandates /tmp/ama-rpi-heavy.lock. Phase details:50-52
  requires the locked browser checks. tools/rpi-checks.py:2243-2246 opens that
  same path with O_CREAT. Current execution constraints prohibit /tmp file
  operations and require created scratch files to be workspace-relative.
* Concern: the plan presents a mandatory validation operation that cannot be
  performed in this execution context. A different private lock would not
  coordinate with the repository's existing shared heavy-resource lock.
* Impact: heavy validation can neither be admitted as written nor safely
  bypassed. Reporting the browser or full publication gate as completed would
  lack permitted execution evidence.
* Smallest useful change: explicitly mark shared-lock-dependent validation
  blocked in this context, separate permitted lightweight checks, and state
  that no alternate lock, omitted admission or prohibited-path attempt is
  authorized. Only identify a runnable heavy-check path if an already permitted,
  equivalent shared-admission mechanism is evidenced; do not expand this
  correction into lock-tool changes.
* Action owner: planning parent.
* Exact resolving evidence: revised P02-T01/P02-T03 name the path/admission
  blocker and stop condition, keep the resource lock and bounded retry safety
  requirements intact, and do not claim blocked checks passed. Any claimed
  executable alternative must identify its permitted path and shared-lock
  equivalence before execution.
* Decision route: Direct planner correction. The current restriction is not an
  invitation to ask for a bypass or weaken shared-resource admission.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The required complete gate is already known to invoke prohibited az

* Related IDs: P02-T03; no az/Azure requirement; full publication prerequisite.
* Evidence: phase details:65-66 conditionally says to complete repository checks
  without az and record a blocker if they conflict. src/README.md:61-77
  describes the complete gate and its Azure CLI dependency.
  tools/rpi-checks.py:598-601 requires az bicep version in trusted preflight;
  :1365 executes it, and :1487-1488 executes az bicep build/lint.
  This task's repository instructions require the complete --all gate before
  publication, even though src/README.md also documents a focused tier.
* Concern: this is a confirmed contract conflict, not an unknown prerequisite
  to discover by launching the gate. Offline Bicep use still invokes az and
  violates the explicit command prohibition. The conditional wording leaves
  implementation to rediscover the conflict and leaves publication eligibility
  ambiguous.
* Impact: there is no supported complete-gate success path evidenced under the
  present constraints. A focused check, fabricated receipt or offline/cloud
  distinction cannot satisfy the required full gate.
* Smallest useful change: record the exact known incompatibility now; prohibit
  executing --all while its az commands remain required; make P02-T03 stop
  before push and thread resolution when the required gate is blocked.
  Retain permissible implementation and lightweight-check progress without
  calling it complete validation or publishable. Do not remove gate checks,
  choose a lesser tier or change tooling/protections within this correction.
* Action owner: planning parent.
* Exact resolving evidence: revised P02-T03 cites the concrete az preflight
  contract, records full-gate/publication status as Blocked under the current
  restrictions, and explicitly prevents push or thread resolution without
  valid required evidence. A future feasible path requires separately
  established compliant gate evidence, not an assumed exception.
* Decision route: Direct planner correction. Existing no-az direction resolves
  what may run; no new user response is required to record the blocker.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Publication lacks explicit fail-closed Review and exact-head receipt checks

* Related IDs: P02-T02, P02-T03; independent Review and publication acceptance.
* Evidence: phase details:56-59 preserves the original Review but routes new
  findings to later work; :63-68 proceeds from commit/fetch/checks to push and
  thread resolution without an explicit accepted-current-scope condition,
  current-main receipt verification or independent exact-head assessment.
  src/README.md:150-158 requires fetching main again and verifying immediately
  before independent exact-head review and push.
  tools/rpi-checks.py:152-175 binds clean HEAD/tree/current origin/main ancestry;
  :2121 onward validates receipt identities against the candidate.
* Concern: the plan does not distinguish deferrable out-of-scope Review
  observations from unresolved defects in the seven promised fixes. Nor does
  it bind the final push to the exact committed candidate and current-main
  receipt after possible bot commits or base movement. Verifying remote HEAD
  after push is not a substitute for these prerequisites.
* Impact: unresolved in-scope defects or a stale receipt could be published and
  threads resolved despite failure of the required acceptance boundary.
* Smallest useful change: make current-scope Review blockers and every failed
  or unavailable required check stop publication. Specify the sequence:
  preserve original Review; commit candidate and dated evidence; establish
  reviewed current-main ancestry; run the required complete gate if permitted;
  fetch main again; verify its external receipt against current origin/main
  and unchanged clean HEAD; obtain required independent exact-head assessment;
  then normal push and evidence-supported per-thread resolution. Any later
  commit/base/tool/image/input change invalidates the gate. Preserve the
  single original Review; do not request another plan critique or silently
  rerun Review to erase an adverse result.
* Action owner: planning parent, with final exact-head assessor responsible for
  its assessment evidence.
* Exact resolving evidence: revised P02-T02/P02-T03 name the stop conditions,
  --verify-receipt receipt/base binding, exact assessed HEAD and normal-push
  dependency; explicitly leave publication blocked under PC-001/PC-002.
  Deferred findings must be identified as outside the seven-fix acceptance
  boundary rather than unresolved required corrections.
* Decision route: Direct planner correction. The full loop and normal push
  are already authorized; authorization does not waive validation prerequisites.

## Strengths and Residual Risk

* Draft ownership, immutable dispatch boundaries and semantic identities address
  the actual defects instead of timing delays or blanket input disabling.
* Document-node-only retention avoids preserving entire stale case panels.
  Checklist and funding recovery remain evidence-bound rather than silently
  applying old edits to new records.
* The locked test scope permits focused scenarios without deleting existing
  assertions or introducing another runner/framework. No change to ownership
  or helper-addition limits is recommended.
* Synthetic browser/axe evidence is not human screen-reader, staff usability,
  live deployment or regulatory acceptance; the plan already preserves those
  boundaries.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents planner revision.
* No compliant heavy-lock/full-gate execution path is evidenced in this
  environment. Treat that as a validation/publication blocker, not evidence
  that the seven repair designs are invalid.

## Limitations

* No code, plan, research or phase-details edits; no agents launched; no
  implementation, browser tests, gate execution or mutation of PR threads.
* Review thread identities and defect descriptions were assessed from the
  supplied research. PR lifecycle/head were independently checked read-only;
  this critique does not attest later remote state or implementation success.
* Tool availability, package restoration and runtime outcomes were not tested.
  The az and lock incompatibilities are source-backed contract observations,
  not claimed failed test runs.
* This is the complete actionable finding set for the supplied boundary.
  No additional critique pass is requested.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: planning parent.
* Smallest next action: revise P02 validation/publication dispositions directly
  for PC-001 through PC-003, then continue only eligible authorized RPI work.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/case-journey-ux-526-correction-research.md](.copilot-tracking/research/2026-10-28/case-journey-ux-526-correction-research.md) | Supplied focused evidence |
| [.copilot-tracking/plans/2026-10-28/case-journey-ux-526-correction-plan.md](.copilot-tracking/plans/2026-10-28/case-journey-ux-526-correction-plan.md) | Assessed candidate, unchanged |
| [.copilot-tracking/details/2026-10-28/case-journey-ux-526-correction-phase-details.md](.copilot-tracking/details/2026-10-28/case-journey-ux-526-correction-phase-details.md) | Assessed task details, unchanged |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly,
preserve this original Revise verdict and continue the authorized loop only
within permitted execution boundaries. Keep publication and thread resolution
blocked until required validation and exact-head acceptance are supported.
No user action or second plan critique is required.
