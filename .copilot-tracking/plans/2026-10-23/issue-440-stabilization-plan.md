<!-- markdownlint-disable-file -->
# RPI Plan: Issue 440 stabilization checkpoints

## Task Metadata

* Task ID: 440; parent: #123 (hierarchy only).
* Task slug: issue-440-stabilization.
* Plan date: 2026-10-23.
* Planning status: complete; owner resumed execution after independently verified #349 completion; actual lock recheck free.
* Phase details: .copilot-tracking/details/2026-10-23/issue-440-stabilization-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-23/issue-440-stabilization-plan-critique.md (executed once; original Revise preserved).

## Executive Summary

Improve the existing delivery coordinator with recurring, operational
stabilization checkpoints and execute the first bounded integrated checkpoint
against pinned main, not sibling/unmerged functionality. Preserve per-issue
RPI and exact-head receipts. Only affected epic closure/dependent expansion is
gated; independent lanes continue.

### User Decisions and Requirements Highlights

* Cap eight active issues per wave, never fill to eight for its own sake.
* Use focused failure loops before broader suites; final release gates remain.
* No source feature implementation, unrelated bug fixes or private data.

### What You May Not Know

* BRD0.19.0 and PRD0.18.0 are draft/candidate, not automatic approval of their
  changes. ADR0001 future worker isolation differs from ADR0002 shared API.
* Local trusted-principal tests do not satisfy real Entra sign-in or the
  already-open deployed #349/#350/#360 gaps.
* The supported current-main integration checkpoint needs a clean preliminary
  engineering commit and its own full local runner invocation. Its receipt is
  not publication evidence; later results/documentation commits require a new
  final gate after the original Review.

### Unresolved Decisions or Blockers

Owner resumed on 2026-10-23 after #349 completion. Fresh nonblocking lock probe
acquired/released successfully; fresh main is unchanged and an ancestor of HEAD.
Local checkpoint execution proceeds. P01/P02 and focused174/package2392
discoveries completed (468 skipped). Independent static and seven-scenario
simulation Pass; actual native host candidate discovery is Deferred. That
blocks P04 completion/publication, not independent P03 local runtime evidence.
Azure headroom stays Unknown and no cloud work is authorized.

P03 execution and reconciliation now complete with an actual failed native
receipt:16 groups passed, core filtered-query17383ms exceeds1500ms.
Three focused repeats pass106-108ms, cause unknown; they do not repair the
receipt. P04-T01 host discovery remains Deferred. Task blocked in Implement,
not eligible for original Review/final publication yet.

## User Decisions and Requirements

* Run real ordered Research, Plan/details/critique, Implement and independent Review in this isolated worktree, with genuine dated artifacts written during their phases.
* Modify the existing coordinator and narrowly necessary existing guidance/evidence, preserve frontmatter/capability surfaces and per-issue RPI/receipt safeguards.
* Trigger checkpoints before epic closure, after each completed wave and earlier on material architecture/requirements changes or significant regression; cap eight, with scoped blocking only.
* Pin main/source, covered merged PRs/issues and BRD/PRD/ADR identities; reconcile planned features, contracts and observed journeys.
* Record exact gaps, regressions, necessary evidence-based refactoring, bugs and continue/fix/pivot recommendation; owner alone approves pivots or requirements relaxation.
* Use smallest reproduction/unit/static, affected packages, relevant local HTTP/browser/SQL/Docker, then authorized Azure-only residuals; fixtures never establish live acceptance.
* Execute first checkpoint only on current-main functionality, retain consent/human-review/manual/AI-failure paths, and distinguish every evidence tier.
* Deduplicate code findings; fixes need separate issue/RPI/branch/PR, not this policy PR. Preserve #349/#350/#360 gaps and all existing unchecked epic criteria.
* HVE Builder Major improve requires independent static review, hve-builder-tester execution and host validation of final policy candidate.
* If #349 owns the lock, finish Research/Plan, record exact resume point and stop without polling or pushing.

## Goals

* Prevent child merges from substituting for integrated acceptance.
* Make stabilization bounded, repeatable, traceable and compatible with independent delivery.
* Produce actual first-checkpoint evidence without overstating product or live readiness.

## Scope and Non-Goals

### In Scope

Existing coordinator; src/README.md delivery ladder; dated checkpoint in existing
docs/architecture/cutover-evidence-pack.md; directly necessary KB index/log.
Tracking artifacts and temporary external owned execution evidence.

### Non-Goals

Application code changes, new architecture/service, whole-repository freezes,
private data/default dataset, Azure/Graph/Entra operations, paid calls, modifying
other sessions, tools/model configuration, automatic issue/epic acceptance.

## Functional Requirements

* F1: each trigger produces a pinned reconciliation record and explicit scoped recommendation.
* F2: checkpoint blockers apply to affected closure/dependent expansion only.
* F3: first checkpoint maps document-qualified requirements to existing tests and honest outcomes.
* F4: deduplicated findings identify severity/reproduction/smallest fix/test/dependency; no invented refactor.

## Non-Functional Requirements

* N1: preserve behavior/capabilities outside approved coordinator additions.
* N2: zero private/cloud data reads or cloud mutations; no competing heavy owner.
* N3: local evidence includes exact commands/exits/skips/limitations; full receipt only for frozen final head/current base.

## Acceptance Criteria

* A1: all checkpoint triggers, cap and scoped blocking have observable behavior scenarios.
* A2: pin source and document identities; qualify local/Azure/implemented-unverified/deferred/blocked/unknown explicitly.
* A3: test ladder preserves manual, resident and human authority; no live pass from mocks. Azure-only residual admission requires named residuals, passing relevant local checks, valid action-specific authority, complete all-in headroom, finite scope/budget/stop conditions and exact owned cleanup boundaries, all conjunctively.
* A4: actual first current-main checkpoint results persisted in existing evidence, distinct from policy candidate.
* A5: findings deduplicated and routed separately, or explicit no-confirmed-defect statement.
* A6: original critique/Review retained, independent HVE static/behavior/host gates and exact-head final receipt completed before publication.
* A7: no unchecked acceptance ticks or unrelated closures; PR uses Refs #440.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-10-23/issue-440-stabilization-plan.md |
| Phase details | .copilot-tracking/details/2026-10-23/issue-440-stabilization-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-10-23/issue-440-stabilization-plan-critique.md; original Revise retained, PC-001/002 resolved directly |
| Research | .copilot-tracking/research/2026-10-23/issue-440-stabilization-research.md; C1-C15, W1-W4 |
| Changes record | .copilot-tracking/changes/2026-10-23/issue-440-stabilization-changes.md |
| Readiness | Planning complete; PC-001/002 corrected; implementation active |
| Continuation | P01-P03 execution complete with failed native receipt; P04-T01 host Deferred; task blocked |

## Sources

* .copilot-tracking/research/2026-10-23/issue-440-stabilization-research.md: canonical research and document identities.
* .copilot-tracking/research/2026-10-23/issue-440-current-issue.json: complete current #440 body.
* .copilot-tracking/research/2026-10-23/issue-440-preflight.log: actual branch/base and lock observations.
* .copilot-tracking/research/2026-10-23/issue-440-open-issues.json: open-issue dedup inventory.
* src/README.md; .github/workflows/src-ci.yml; tools/rpi-checks.py: existing component/full-gate contracts.
* Activated hve-builder workflow contract: Major improve routing; later stage criteria must be loaded before execution.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Establish safe execution boundary

* Intent: preserve #349 execution and isolate current-main source from policy evidence.
* Dependencies: coordinator resume after heavy lock release.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Reconfirm source, lock and approved boundary

* Fresh fetch/status/branch/HEAD/main and actual lock-holder inspection. If busy, stop without enqueue/sleep.
* Pin checkpoint source and document blobs; list covered merged PRs/issues explicitly, not a product-wide pass.
* If main moved, reconcile plan/source identities before testing. Runner requires fresh main ancestry; if absent, stop with branch-reconciliation blocker, never silently rebase/amend/force.
* Detail section: P01-T01 in phase details.

<!-- rpi:phase id=P02 -->
### [x] P02: Improve existing checkpoint policy

* Intent: operational recurring checkpoints using existing agent/guidance only.
* Dependencies: P01; user-approved Major improve boundary.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Author coherent scoped policy addition

* HVE generic author stage, approved targets: .github/agents/ama-backlog-delivery-coordinator.agent.md and src/README.md.
* Add trigger/record/decision/ladder rules and link them at wave completion, early regression/drift detection, before epic closure and loop selection.
* Cap active wave eight without changing existing parallel/model/tool surfaces. Preserve per-issue RPI/merge/current-receipt safeguards.
* Restrict blockers to affected closure/dependent expansion, require owner approval for pivot/requirements relaxation/deliberate deferrals.
* Require all Azure residual preconditions in A3; incomplete authority/cost/local results block Azure-dependent work only. This run still authorizes zero Azure operations.
* Detail section: P02-T01.

<!-- rpi:phase id=P03 -->
### [x] P03: Execute pinned-main checkpoint and triage

* Intent: genuine bounded main evidence, separately labelled from candidate-policy validation.
* Dependencies: P01, installed source distributions. May execute independently of P02 source prose, but never on unmerged source functionality.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run focused local contracts and affected suites

* Execute existing tracked auth/session/manual/safety/consent/review/persistence selectors, then five existing package suites and structural/lint/type checks as relevant.
* Record all command exits, test counts/skips, source/tool/environment identities and limitations. No dataset defaults or paid model invocation.
* Use an external pinned-source archive/venv for focused checks to avoid editable-install artifacts in the policy worktree. After focused checks, make a clean preliminary engineering-checkpoint commit containing P02 policy plus genuine tracking evidence, not fabricated results.
* Prove application/test/build/workflow inputs equal pinned main; the only allowed preliminary diff is existing coordinator, src/README.md and own tracking artifacts. Then run existing --all with --lock-timeout 0 in a unique external directory for actual browser/SQL/Docker ownership.
* Persist actual broad results only after the preliminary run completes. P03 receipt is engineering-checkpoint evidence, never final-candidate publication eligibility; P05 repeats full gate after original Review and final commit.
* Detail section: P03-T01 and validation ownership table.
* Executed, not accepted: preliminary native gate16 groups pass/core benchmark
  failure; original failure and three passing focused retests retained.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Persist reconciliation and deduplicated findings

* Append dated evidence to docs/architecture/cutover-evidence-pack.md; update docs/reference/README.md and append-only docs/reference/log.md when filing the material KB pointer.
* Requirement/document IDs, scope/merged PRs, ADR contracts, actual journey results and classification per row; continue/fix/pivot with exact affected gate and independent lanes.
* Code bugs/refactors only if demonstrated, deduplicated against fresh open issues. Separate issue requires severity/reproduction/requirement/ADR/smallest fix/regression test/dependency; return numbers to coordinator.
* Detail section: P03-T02.
* Actual dated checkpoint/index/append-only log filed. No confirmed stable
  application defect/refactor or new bug issue; validation blockers explicit.

<!-- rpi:phase id=P04 -->
### [ ] P04: Validate final policy and independently Review

* Intent: distinct final-candidate policy and RPI evidence, no stage skip converted to pass.
* Dependencies: P02 and completed/explicitly qualified P03 evidence.

<!-- rpi:task id=P04-T01 -->
#### [ ] P04-T01: HVE final-candidate static, behavior and host validation

* Fresh independent generic static review under HVE catalog/rubric, without author rationale.
* Resolve original in-scope findings in one batch and targeted closure; then activate hve-builder-tester (not direct tester agent) against final candidate with seven named scenarios in details.
* Generic host validator checks actual agent at real path with existing host-supported validation/discovery and bounded metadata/reference integrity; unavailable required host execution is Deferred, not static-prose Pass.
* Detail section: P04-T01.

<!-- rpi:task id=P04-T02 -->
#### [ ] P04-T02: Run original independent RPI Review

* Activate rpi-review once after implementation reconciliation. Preserve original outcome, route findings to later selected work; no repeated Review or fabricated human approval.
* Detail section: P04-T02.

<!-- rpi:phase id=P05 -->
### [ ] P05: Freeze, full-gate and publish

* Intent: publish only genuinely eligible frozen final evidence.
* Dependencies: P04, no blockers, free heavy lock, publication authority.

<!-- rpi:task id=P05-T01 -->
#### [ ] P05-T01: Commit, gate, verify and hand off exact candidate

* Resolve gh api user and local privacy-safe author/committer email, commit implementation plus original dated evidence with Conventional Commit and requested Copilot trailer.
* Fresh main; stable candidate full native --all in new external directory using --lock-timeout 0, then official current-base --verify-receipt and independent exact-head assessment.
* Head/base/source/tool/image/input changes invalidate receipt; let an active gate finish before reconciliation, preserve all adverse receipts.
* Normal push and gh pr create to main only after requirements met; Refs #440, explicit evidence/limitations, no merge.
* Detail section: P05-T01.

## Locked Test and Artifact Ownership

* Application/test removals: none. Application/test additions in src/tools/workflows: maximum zero; this is policy/evidence work, not a code-fix PR.
* HVE semantic scenarios: seven required scenarios, distinct from source regression tests. Tester owns generated sandbox stimuli and grading evidence under its allocated tracking root; no new reusable source test framework.
* Canonical production targets: existing coordinator, src/README.md, cutover evidence pack, KB index/log only. Generated production targets: none. Original and memory: immutable.
* Tests: five component owners retain their existing suites. Native runner owns disposable SQL/browser/images/scanner/full receipt. No private/support generator, .env, cloud or foreign receipt inputs.
* Current-main source testing and candidate-policy testing have separate identities/outcome tables. Full final gate is only after stable committed candidate and original Review.
* Planned selectors retain their original intent; actual outcomes are recorded
  in changes/details and external logs. No unrun gate is counted passed.

## Dependencies

* #349 lock release: execution prerequisite, not parent hierarchy dependency.
* Final human/hosted approvals remain separate and cannot be fabricated by local checks.

## Critique Disposition

One fresh independent critique executed once, via worker activating
rpi-plan-critique. Original verdict **Revise** remains unchanged.

| Finding | Owner and disposition | Exact resolving evidence |
| --- | --- | --- |
| PC-001 High: executable clean checkpoint/source boundary | Planner; resolved directly, no owner decision | P01-T01 ancestry stop; P03-T01 external pinned archive, focused checks, clean preliminary commit and allowlisted source equality, supported --all/--lock-timeout 0, distinct receipt and external results; P05-T01 fresh final gate |
| PC-002 Medium: complete Azure admission predicate | Planner; resolved directly, no owner decision | A3, P02-T01 complete conjunctive admission and P04 existing cost scenario grading; present no-cloud boundary unchanged |

No second critique or later Review was run. These are direct plan corrections,
not runtime verification or a retroactively changed independent verdict.

## Follow-Up Items

* Diagnose measured native benchmark breach/repeatability, retain original
  failure and unchanged threshold; no confirmed source cause or speculative fix.
* Resolve safely contained native policy discovery; static/simulation Pass
  cannot replace unmet host evidence.
* Existing #349/#350/#360 live gaps and #432 Tokenomics remain outside this policy PR.

## Handoff

* Blocked Implement at P04-T01: P01-P03 executed, required host discovery unmet
  and native preliminary receipt failed. Exact resume facts in changes/state.
* Original Review/final receipt/PR remain not run, not fabricated.
* Original research/critique and adverse results remain preserved.
