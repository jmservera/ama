---
title: "RPI Plan Critique: PR #504 main rebase"
description: One final-candidate assessment of preservation and checkout-local validation
ms.date: 2026-10-29
---

## Metadata

* Task ID: pr-504-rebase-2026-10-29
* Task slug: rai-release-218-rebase
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/rai-release-218-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/rai-release-218-rebase-phase-details.md
* Critique execution status: Complete
* Assessment count: exactly one final-candidate critique

## Inputs and Criterion Boundary

* Caller requirements: complete the bounded local RPI rebase of draft PR #504;
  preserve both workstreams and both index/log entries; retain main rubric and
  scenario manifest; validate changed scenario pins; use src-only production
  and existing external tests; no new tests for pure integration, test removals,
  generated deliverables, Azure operations, dependency installation or push.
* Supplied candidate inputs: the plan and phase details above, plus
  .copilot-tracking/research/2026-10-29/rai-release-218-rebase-research.md.
* Supplied evidence pointers read: src/core/pyproject.toml,
  src/api/pyproject.toml, .github/workflows/src-ci.yml (validation steps), and
  .copilot-tracking/changes/2026-10-27/rai-release-218-changes.md
  (including its original integration/publication account).
* Standing context read: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory was not treated as evidence.
* Decisions assessed: pinned base
  5653547507f3056f09a726a18516237728da5e5b; original head e9b5604d;
  source/evidence commit 63e9074a; existing shared environment with wrong-checkout
  editable imports; one independent Review; local commit with authenticated
  noreply identity and exact requested co-author trailer.
* Acceptance/dependency boundary: preservation and ancestry after P01, scoped
  static/behavioral evidence after P02, then independent Review and a clean,
  committed no-push handoff after P03. A full API discovery run is unnecessary;
  omitting it respects the caller's lock condition without acquiring a lock.
* Read-only status inspection showed feat/rai-release-218 with untracked dated
  plan/details/research/session artifacts and no reported tracked modifications.
  Their presence is not permission to move, discard or stage unrelated inputs.
* This assesses candidate readiness, not actual rebase success, current remote
  state, fresh test results, hosted approval or full-gate publication readiness.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller rebase direction; C3; P01-T01 | Partial | Default replay does not account concretely for unique merge-commit content; PC-001 |
| Both index/log entries and original evidence; P01-T01 | Partial | Intent is explicit, but merge-only preservation needs an executable comparison; PC-001 |
| Pinned main and ancestry; P01-T01 | Partial | Mutable origin/main is the replay target despite an exact pinned base; PC-002 |
| Main rubric/manifest; C5-C6; P01/P02 | Covered | Main byte-identity checks, dynamic cache-key preservation and test_scenario_manifest are required |
| Local import precedence; C7; P02-T01 | Partial | Runtime assertions are useful, but PYTHONPATH does not establish mypy resolution; PC-003 |
| Existing release/oversight/ranking/quality/dependency tests; P02-T01 | Covered | Named core/API modules; exact commands/counts/skips required; no broad API discovery |
| Source/test ownership and zero new tests/removals | Covered | Locked targets and explicit amendment requirement for a discovered semantic defect |
| One independent Review and original outcome; P03-T01 | Covered | Separate reviewer artifact; original outcomes and residual findings retained |
| Identity/trailer, no push/Azure/closing keywords; P03-T01 | Covered | Explicit local-only commit and handoff requirements |
| Publication/human approval; C2/W1; P03 | Covered | Scoped validation does not imply full receipt, hosted checks or actual RAI acceptance |

## Verdict

* Verdict: Revise
* Severity counts: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: scope and local-only claims are credible, but the replay procedure
  can omit merge-only evidence, the operational target is not pinned, and the
  static-check import guarantee is not established by the proposed mechanism.
  These are planner-owned corrections, not reasons to revisit user direction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Default rebase can omit the integration merge's unique content

* Related IDs: C3, P01-T01; original-evidence and both-intents acceptance criteria.
* Evidence: the plan says to "Replay the two branch commits" with
  `git rebase origin/main`. The phase details require preserving unique
  e9b5604d publication annotations and allow skipping only a proven-empty replay.
  The original changes artifact's "Publication and Main Integration" section
  explicitly describes merging main 09099ecd, a manual index reconciliation,
  and subsequent integration metadata. Supplied research identifies e9b5604d
  as the integration commit.
* Concern: ordinary rebase omits merge commits rather than stopping on each
  merge as an empty replay. Its unique tree changes or annotations therefore
  need not appear for the proposed empty-commit safeguard to inspect.
  Comparing only three production modules and main-owned files does not detect
  missing publication annotations or a lost index entry.
* Impact: a clean, passing source integration can silently lose original
  evidence or documentation intent while claiming that both commits survived.
* Smallest useful change: make P01 explicitly inspect and record the original
  commit topology and identify merge-only evidence/resolution content before
  replay. Define how that content is retained or deliberately reapplied during
  the authorized rebase; do not assume default replay preserves it. Record
  before/after checks for original evidence and both index/log entries as well
  as the existing production/main-file checks. No extra feature or test is needed.
* Action owner: planning parent; implementer executes the amended safeguards.
* Exact resolving evidence: amended P01 plan/details naming the merge-content
  handling and comparison procedure; implementation evidence showing original
  commit parents, identified unique merge content, preservation of original
  dated evidence including publication annotations, both index/log entries,
  retained upstream content and no unresolved entries. A skipped merge or empty
  replay must have explicit content-equivalence evidence.
* Decision route: direct planner correction. The user already authorized rebase
  and preservation; no new user decision or remote history operation is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The replay command uses a mutable ref instead of the pinned base

* Related IDs: pinned-base decision, P01-T01; ancestry acceptance criterion.
* Evidence: the plan pins
  5653547507f3056f09a726a18516237728da5e5b and says later main advancement
  must be reported rather than silently rewritten. P01 nevertheless specifies
  `git rebase origin/main` without an immediate equality precondition.
* Concern: origin/main can move after Research, including through another
  process sharing repository refs. Successful ancestry to the older pinned SHA
  alone cannot prove that replay used exactly the reviewed target.
* Impact: implementation and test evidence may describe a different integration
  base from the one actually used.
* Smallest useful change: resolve and record origin/main immediately before
  replay, compare it with the pinned SHA, and rebase against the literal reviewed
  SHA. Report any movement and keep the task's pinned-base boundary explicit;
  do not silently substitute a new base.
* Action owner: planning parent.
* Exact resolving evidence: amended P01 command/preconditions with the full SHA
  and an explicit ref-movement disposition; implementation log recording
  pre-replay HEAD, resolved origin/main, actual target and final pinned-base
  ancestry.
* Decision route: direct planner correction. The supplied pinned-base decision
  already resolves the target; no user response is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: PYTHONPATH and runtime probes do not prove mypy import provenance

* Related IDs: C7, P02-T01; checkout-local validation requirement.
* Evidence: phase details say to prefix the runtime paths "for mypy too when it
  follows imports." src/core/pyproject.toml sets mypy_path to src/tests;
  src/api/pyproject.toml includes local core paths but not agents paths. API
  configuration also intentionally skips following many core/agents modules.
  Research C7 establishes that editable installations target another worktree.
* Concern: Python runtime import precedence and mypy source discovery are
  different mechanisms. Setting PYTHONPATH and checking module __file__ proves
  the runtime probe, not the paths or exclusions used by mypy. Existing local
  mypy_path entries are useful but do not establish the proposed blanket
  guarantee for sibling imports.
* Impact: a successful type-check can be overreported as checking checkout-local
  sibling code, or a followed sibling can still come from the shared environment.
* Smallest useful change: distinguish runtime PYTHONPATH assertions from mypy
  resolution. Specify checkout-local MYPYPATH or an equivalent supported mypy
  configuration for followed sibling modules, retaining existing strictness and
  intentional exclusions. Record enough resolution evidence to identify local
  followed paths and describe intentionally skipped imports accurately.
* Action owner: planning parent.
* Exact resolving evidence: amended P02 commands showing separate runtime and
  mypy path controls; implementation records runtime module origins, mypy
  invocation/configuration and resolution evidence for relevant followed sibling
  imports. Record configured exclusions as exclusions, not checked coverage.
* Decision route: direct planner correction; no dependency installation, shared
  editable mutation, source rewrite or user decision is necessary.

## Strengths and Residual Risk

* Main scenario pins and dynamic briefing-cache assertions are explicit
  preservation targets, not candidates for blanket branch-file selection.
* Existing selector coverage, zero new tests and no test removals fit pure
  integration; failures can justify a bounded explicit amendment.
* Historical adverse Review outcomes and human/manifest approval gaps remain
  intact. No hosted, SQL, browser, image or full-publication success is inferred.
* The no-full-API selection is a valid narrower choice than the caller's
  conditional permission and needs no heavy-lock probe.
* A later coordinator must separately satisfy applicable publication gates.
  These scoped checks are not a receipt or authorization to push.

## Questions or Blocking Evidence Gaps

* No unresolved user decision. PC-001 requires bounded pre-replay topology and
  unique-content inspection during implementation, not open-ended research.
* All three findings are available from the supplied boundary and are returned
  together. Do not schedule another critique after planner disposition.

## Limitations

* No rebase, install, test suite, lock acquisition, Azure operation, commit,
  push, delegation or plan/state/source edit was performed.
* Commit topology was assessed from the supplied research and original
  integration narrative, not independently reconstructed in this critique.
* No fresh remote check or test execution was performed; supplied claims are
  planning evidence, not new implementation receipts.
* Only this caller-specified critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: revise P01 with merge-only-content preservation and
  exact-base safeguards, correct P02's mypy provenance procedure, and record
  dispositions for PC-001 through PC-003 before implementation.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/rai-release-218-rebase-plan.md](.copilot-tracking/plans/2026-10-29/rai-release-218-rebase-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-29/rai-release-218-rebase-phase-details.md](.copilot-tracking/details/2026-10-29/rai-release-218-rebase-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-29/rai-release-218-rebase-research.md](.copilot-tracking/research/2026-10-29/rai-release-218-rebase-research.md) | Supplied evidence synthesis |
| [.copilot-tracking/reviews/plans/2026-10-29/rai-release-218-rebase-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/rai-release-218-rebase-plan-critique.md) | Complete one-pass critique |

## Next Steps

The active planning parent should apply and record the three planner-owned
corrections, finalize without another critique, and continue the authorized loop
only after disposition. No user action is required. This critique stops here.
