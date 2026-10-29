---
title: Agent chat 157 refresh plan critique
description: Independent final-candidate readiness and safety critique for PR 503 refresh
ms.date: 2026-10-29
---

## Metadata

* Task ID: pr-503-refresh-2026-10-29
* Task slug: agent-chat-157-refresh
* Plan: .copilot-tracking/plans/2026-10-29/agent-chat-157-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/agent-chat-157-refresh-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller direction: rebase PR #503, feat/agent-chat-157, onto origin/main, preserving both sides; retain main rubric and manifest copies; use /tmp/mv for relevant validation; no full API discovery without the shared heavy lock; no Azure operations or push; Conventional Commit with Copilot trailer; exact commands/results in changes.
* Research considered: .copilot-tracking/research/2026-10-29/agent-chat-157-refresh-research.md, including Q1-Q3, C1-C4, W1-W2 and its stated limitations.
* Plan and details considered: all requirements, acceptance criteria, P01-P03, dependencies, change budget, critique disposition and handoff.
* Standing context read: docs/case_study_48_original.md, the introductory addendum context, docs/reference/README.md and docs/reference/memory.md. These do not independently verify branch or runtime state.
* Assessment boundary: planning credibility and execution safety from supplied evidence and governing instructions. This is not a source review, ancestry verification, test execution, hosted-check assessment or feature acceptance.
* The supplied research reports prior clean-worktree and PR lifecycle observations. Those are reported evidence, not fresh verification by this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C3, P01-T01: history and semantic integration | Partial | Intent and rebase-side semantics are explicit; execution-time branch/base safeguards need PC-002. |
| Main-owned rubric and manifest; C4 | Partial | Main ownership is explicit, but the acceptance exception permits a contrary manifest edit; PC-001. |
| Append-only/index and original adverse evidence | Covered | Both contributions and historical Review findings must survive; no deletion authorized. |
| C1, Q2, P02-T01: relevant validation | Partial | Component tools and coverage families are named, but selectors, source precedence and browser execution remain underspecified; PC-003. |
| Heavy-lock and filesystem safety; P02-T01 | Partial | Focused testing avoids full discovery, but contingency and log paths conflict with current filesystem restrictions; PC-004. |
| Conventional Commit and authenticated identity | Covered | Plan requires authenticated numeric-id noreply email and required trailer; details require local configuration. |
| Changes evidence | Covered | Exact commands, outcomes, failures, fixes and limitations are required; PC-003 makes the planned commands reproducible. |
| No push, Azure operations or acceptance inference | Covered | Explicit non-goals and separate publication/hosted evidence boundary. |
| C2, W1-W2, P03-T01: independent Review and publication | Covered | One independent Review, original adverse evidence, separate evidence commit and no implied exact-head approval after later commits. |
| Test ownership and change budget | Covered | Existing sibling tests, no legacy implementation, at most two directly coupled added methods. |

## Verdict

* Verdict: Revise
* Rationale: Four substantive, planner-owned corrections are needed before execution. The user's confirmed choices already resolve the direction; none requires a new user decision. Research is sufficient to identify the planning corrections, although actual conflicts and test availability remain execution-time observations.
* Severity summary: 2 High, 2 Medium, 0 Critical, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Manifest acceptance permits overriding the user's main-copy decision

* Related IDs: main-owned rubric/manifest requirement, C4, P01-T01, Acceptance Criteria.
* Evidence: .copilot-tracking/plans/2026-10-29/agent-chat-157-refresh-plan.md, Acceptance Criteria, allows a "narrowly documented derived hash correction" as an exception to byte equality. The same plan's User Decisions and the caller require origin/main's manifest; the research direction selects main copies.
* Concern: The exception authorizes changing a caller-selected snapshot if reconciled public source changes a frozen hash. A failing manifest test demonstrates incompatibility, not permission to change that snapshot.
* Impact: Execution could silently depart from the selected main state and alter the frozen-source evidence boundary merely to satisfy validation.
* Smallest useful change: Remove the derived-hash exception. Require exact main rubric and manifest bytes from the captured rebase target. If a pinned-source mismatch occurs, record its exact failure and stop that acceptance item as blocked; do not edit the manifest under this authorization.
* Action owner: Planning parent.
* Exact resolving evidence: Revised acceptance criterion and P01/P02 details prohibit snapshot exceptions, name the captured target as the comparison source and require unchanged-snapshot failure evidence in .copilot-tracking/changes/2026-10-29/agent-chat-157-refresh-changes.md if incompatibility occurs.
* Decision route: Direct planner correction. A future request to change the snapshot would be a separate divergent user decision, not a decision needed to correct this plan.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Rebase lacks an explicit fresh preflight and immutable execution target

* Related IDs: Q1, C3, P01-T01, branch/base dependency and ancestor acceptance.
* Evidence: Research records an earlier clean branch and main SHA 5653547507f3056f09a726a18516237728da5e5b. The plan says "captured main SHA"; phase details instead direct git rebase origin/main and retrieve snapshots from origin/main, without a fresh preflight/capture step.
* Concern: Prior intake observations do not protect against intervening worktree or branch changes. Mutable origin/main could also diverge from the target described in evidence or change between rebase and snapshot retrieval.
* Impact: A destructive history operation could start with unrelated inputs, or a candidate could combine snapshots and ancestry from different main states.
* Smallest useful change: Before mutation, require fresh branch/worktree/rebase-state inspection, confirm the expected active PR workstream, fetch main as authorized and capture pre-rebase HEAD plus fetched main SHA. Rebase, retrieve snapshots and assess ancestry/diffs against that same immutable SHA. Stop rather than stash, reset, discard or move unexpected work.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 gains a mandatory preflight/capture dependency and stop rules. Changes evidence must later contain exact commands/results, pre-rebase HEAD, fetched main SHA, rebase result, snapshot comparison and ancestor/unmerged-path results against that SHA.
* Decision route: Direct planner correction; caller already authorized the rebase. Unexpected dirty or divergent state is a future stop condition, not permission to resolve it autonomously.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Validation is not yet a reproducible command and coverage contract

* Related IDs: Q2, C1, C4, P02-T01, focused-test acceptance and source precedence.
* Evidence: Phase details defer selectors to "actual module names", describe sibling PYTHONPATH entries "as applicable", and request "exact existing browser checks" without naming the entry point. The plan alternately says selected browser regressions and browser checks "if overlap requires it"; research already identifies chat.js and regulatory browser-check overlap.
* Concern: The implementer must still determine which tests actually cover both intents and whether imports resolve to this worktree rather than installed editable copies. The browser check has no stable inclusion rule or missing-prerequisite outcome.
* Impact: Apparently green checks may exercise stale code, omit the changed browser contract or vary by implementer, undermining the stated compatibility evidence.
* Smallest useful change: Resolve exact existing selectors and browser entry point before validation; document working directory, /tmp/mv executable and ordered worktree source/test paths. Map selectors to preserved employee-chat, admission, privacy/isolation, role, model/eval and manifest behavior. Define when browser checks are mandatory and record unavailable prerequisites as a limitation or blocked criterion, never a pass. If web files change, include the required applicable web-guideline retrieval/review without expanding into redesign.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T01 contains a concrete command/coverage table or a mandatory bounded selector-resolution step that produces that table before execution, plus import-origin confirmation and explicit browser applicability. The changes artifact later records the resolved commands, results, skips and unavailable checks.
* Decision route: Direct planner correction. No new test framework, full API suite or feature acceptance is requested.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Scratch and heavy-lock contingency conflict with execution restrictions

* Related IDs: P02-T01, /tmp/mv tooling, heavy-lock requirement and filesystem safety.
* Evidence: Phase details allow logs in "session files or explicit external scratch" and prescribe flock -n /tmp/ama-rpi-heavy.lock true before a possible full suite. Governing execution restrictions prohibit file operations in temporary directories and require new files relative to the project. The caller requires the existing /tmp/mv toolchain, not temporary output writes.
* Concern: Executing an existing /tmp/mv binary is distinct from creating lock/log/cache files under /tmp. The proposed lock command can create a prohibited file and releases any acquired lock immediately; although the following sentence requires holding the same lock, no executable single critical-section command is supplied.
* Impact: A fallback may violate filesystem restrictions or supply misleading lock evidence. Broad scratch guidance can also produce prohibited output locations.
* Smallest useful change: Retain the caller-selected existing /tmp/mv tools, but direct new logs/cache/scratch to explicit project-relative paths and prevent implicit temporary output where applicable. Keep this plan focused-only. If full API discovery becomes necessary, stop and report that the mandated shared-lock path conflicts with current write restrictions; do not run it, relocate the shared lock or treat a probe as lock coverage.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02-T01 removes the executable /tmp lock contingency and external-scratch permission, names permitted project-relative output locations and explicitly blocks full discovery until a compatible authorized locking procedure exists. Changes evidence later identifies focused selectors and confirms no full API discovery occurred.
* Decision route: Direct planner correction for the present focused plan. A future full-suite requirement may need instruction-level resolution; it is not required for this bounded refresh.

## Strengths and Residual Risk

* The plan correctly rejects whole-file runtime preference and explains rebase ours/theirs semantics.
* It preserves original RV-001 through RV-005, immutable adverse outcomes and both documentation contributions rather than converting refresh work into acceptance remediation.
* No push, Azure change, issue closure or fresh hosted success is authorized.
* The plan distinguishes a local candidate, publication receipt and hosted acceptance. A missing complete local gate still blocks publication; focused green checks cannot replace it.
* A later evidence commit changes HEAD. The explicit warning that earlier Review does not approve that later exact head is sound and must remain in handoff.
* Actual semantic conflicts, browser prerequisites and frozen-source compatibility remain unverified. These are execution observations, not facts established by this critique.

## Questions or Blocking Evidence Gaps

* No user response is needed to resolve PC-001 through PC-004.
* A frozen-source mismatch, unexpected dirty state or mandatory full-suite dependency must be reported with evidence if encountered; this critique does not preauthorize resolving those future blockers by changing scope.

## Limitations

* No Git commands, checks, tests, source inspection beyond the supplied planning evidence, remote operations or mutations were performed.
* Research observations and historical check outcomes were assessed as supplied; no claim of current mergeability or runtime correctness is made.
* Only this critique artifact was written. Plan, phase details, research, changes and original review records remain untouched.
* This is the complete actionable finding set for the supplied boundary. No second critique or delegated reassessment is requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Remove the manifest exception, then incorporate PC-002 through PC-004 directly into the plan/details and record disposition.
* User response required: No.
* Return execution Complete and verdict Revise to the active parent; do not start implementation from this unrevised candidate.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/research/2026-10-29/agent-chat-157-refresh-research.md | Supplied focused research and reported branch/check observations. |
| .copilot-tracking/plans/2026-10-29/agent-chat-157-refresh-plan.md | Final-candidate plan assessed once. |
| .copilot-tracking/details/2026-10-29/agent-chat-157-refresh-phase-details.md | Execution details requiring the identified corrections. |
| .copilot-tracking/reviews/plans/2026-10-29/agent-chat-157-refresh-plan-critique.md | This complete independent critique. |

## Next Steps

The active planning parent should apply the four direct corrections, record their disposition and finalize without another critique. No user action is required. This reviewer stops here; no implementation, checks, Git mutations or peer stage is invoked.
