---
title: Chromium skip gate final-candidate plan critique
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 572
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/gate-chromium-skip-572-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/gate-chromium-skip-572-phase-details.md
* Critique execution status: Complete
* Inspected HEAD: 4cb5964f7acce89668a37b5a56c3e125e26f6d21
* Inspected branch: fix/gate-chromium-skip-572, tracking origin/main
* Source disposition: no implementation changes; supplied untracked planning evidence left unchanged.

## Inputs and Criterion Boundary

* Caller requirements: one independent final-candidate critique, no delegation, no implementation, no heavy/full checks, no Azure, secrets or push; write only this artifact.
* Implementation boundary: exact enumeration of `opt-in local Chromium` and `Chromium is installed by the later browser-check step`, preserving unknown-skip rejection and the existing narrower chat test/group restriction. Safe opt-in execution is authorised as an alternative, not required instead of enumeration.
* Supplied research: .copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md, questions Q1-Q3 and evidence C1-C7.
* Dependencies: merged chat required browser execution is already present; P01 follows research and this critique, P01-T02 follows P01-T01, and P02 follows P01.
* Acceptance: bounded parser/receipt regressions, isolated Ruff and strict mypy, unit discovery under flock, unchanged pinned workflows, related src/README.md wording, dated original evidence, one independent implementation review and a local commit using Refs #572.
* Test budget: tools/test_rpi_checks.py is the canonical owner, no removals, at most two additional methods and no generated targets. Existing browser suites and workflow hashes must remain unchanged.
* Execution constraints also prohibit file operations in /tmp or /var/tmp and require newly created scratch files to be project-relative. The planned validation must respect these constraints without weakening shared serialization.
* Whole-issue acceptance is outside this assessment's delivery boundary. Actual Chromium execution, the asset test's later execution and fresh complete browser/MSSQL gate evidence remain unproven. They are not prerequisites to this explicitly local-only critique or bounded fix.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1, P01-T01: exact reasons and fail-closed scope | Covered | tools/rpi-checks.py:63-94,1021-1051; details explicitly require a separate chat identity/group predicate after enumeration. |
| Q2, C2, C5: already merged chat execution | Covered | tools/rpi-checks.py:695-709,1592-1608 and src/api/tests/test_chat_panel.py:563 establish install-before-dispatch, exact selector, opt-in flag and integration mode. No duplicate scheduling is needed. |
| Q3, C4: bounded enumeration versus opt-in discovery | Covered | src/api/tests/test_browser_asset_urls.py:51-58 launches Chromium and skips only its missing executable; installing/enabling browser discovery would change stage prerequisites. Enumeration is within caller authority. |
| C3, P01-T02: parser/receipt regressions and ownership | Covered | tools/test_rpi_checks.py:89-179 provides preserved chat negative cases and the receipt pattern; the proposed two asset methods cover exact counts, mutations, integration refusal and receipt recomputation. |
| P01-T02: related documentation | Covered | src/README.md:169-186 is the relevant contract. Planned recognition-versus-execution wording must distinguish reason-based asset discovery from exact-identity chat discovery. |
| C6, P02-T01: targeted commands | Partial | .github/workflows/src-ci.yml:243-249 matches the requested unit/Ruff/mypy selectors, but the planned lock and default test scratch violate execution constraints; PC-001. |
| P02-T01: immutable workflows and hashes | Covered | Plan excludes workflows and WORKFLOW_HASHES edits and requires an unchanged-hash check. |
| P02-T01: review, evidence and local commit | Covered | Details require one independent Review before local commit, original dated evidence, no push; plan specifies Refs #572 and explicitly denies publication readiness. Repository account/email and commit-trailer instructions remain applicable. |
| Broader #572 browser/full-gate acceptance | Explicitly outside bounded delivery | Plan, details, research and caller retain the missing actual-browser/full-gate evidence. Do not convert static dispatch or synthetic receipts into execution evidence. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 0 Medium, 0 Low.
* Rationale: the recognition design and regression budget are credible, and no browser-stage expansion is required. One executable validation-procedure conflict must be corrected before the parent treats P02 as runnable. This is a direct procedural correction, not a significant or divergent user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation uses a prohibited lock location and uncontrolled default scratch

* Related IDs: P02-T01; plan Dependencies; targeted validation and execution constraints.
* Evidence: the plan names /tmp/ama-rpi-heavy.lock; phase details P02-T01 explicitly prescribe `flock -w 600 /tmp/ama-rpi-heavy.lock` and external session-workspace logs. The supplied execution constraints prohibit /tmp file operations and require newly created files to be project-relative. tools/test_rpi_checks.py:192-193 creates each fixture with tempfile.TemporaryDirectory without a directory override; the planned unit command supplies no project-local TMPDIR. tools/rpi-checks.py:2273-2275 uses the same global lock pathname. tools/test_rpi_checks.py:434-447 mocks that lock's open into fixture-owned storage and asserts that all callers share its identity.
* Concern: the current P02 procedure cannot be executed as written in this environment. Fixing only the shell lock leaves default fixture creation targeting a system temporary location. Conversely, silently replacing the global lock with an unrelated worktree-private lock loses the intended shared serialization.
* Impact: requested validation would violate execution constraints or be represented as completed without authorised execution. This is a validation-planning blocker, not evidence that the proposed parser change is incorrect.
* Smallest useful change: revise only the P02 operational instructions and their dependency wording. Specify a permitted project-relative scratch/log location, explicitly set TMPDIR to its resolved project-local path before launching Python so existing fixtures remain unchanged, and identify a permitted flock lock shared by every competing participant for these bounded runs. Preserve the gate's existing production lock and its unit assertions; do not edit unrelated locking code or add fixture methods. If no compliant shared lock arrangement is available, mark the requested validation blocked and retain that limitation instead of running the prohibited command or substituting a private lock.
* Action owner: planning parent, coordinating the permitted shared validation lock with the caller/coordinator.
* Exact resolving evidence: revised P02-T01 and plan dependency instructions naming the permitted scratch/log directory and shared lock, showing explicit TMPDIR setup and the unchanged four requested validation commands under flock, plus coordinator confirmation that competing runs use that same lock. If unavailable, revised evidence must explicitly record the lock-dependent validation as blocked, with no passing-check or completed-delivery claim. Subsequent actual targeted result logs resolve execution status; no full gate or Azure evidence is requested.
* Decision route: direct planner correction. The source/test contract and caller's bounded scope need no significant or divergent change; no user response is required for this critique.

## Strengths and Residual Risk

* The details correctly anticipate the principal implementation hazard: putting the chat reason into EXPECTED_SKIP_REASONS must not bypass its separately enforced exact test/group restriction.
* Existing chat parser, dispatch and receipt negative cases are retained rather than replaced. The mixed asset pass/skip fixture allows receipt verification to demonstrate positive execution separately from a recognised skip.
* Both Chromium reasons remain forbidden for required integration commands. Existing SQL_NOT_APPLICABLE is the only integration exception; no broad browser exception is proposed.
* Enumeration is explicitly caller-authorised. Requiring real browser execution instead would diverge from the accepted bounded option and is not a critique correction.
* The asset reason is accepted by exact reason in general discovery, not newly restricted to one test ID. That is the proposed and authorised boundary; the guide must not imply it has the chat exception's narrower identity scope.
* The asset test is not a required later browser selector in the inspected inventory. A recognised discovery skip therefore does not establish later execution. This is an explicitly retained acceptance gap, not grounds to add browser execution to this task.
* No full gate, workflow changes, publication, issue closure or new dependency is authorised. Passing targeted checks and a local Refs #572 commit would not establish whole-issue acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved parser design question or significant/divergent decision.
* The permitted shared-lock/scratch arrangement needed for P02 is not supplied; the planning parent must correct that procedure or record blocked validation.
* Broader issue acceptance gaps are retained, not reopened as required work in this bounded task.

## Limitations

* Assessment used supplied planning/research evidence and focused reads of relevant gate, parser, tests, README and pinned workflow commands. Repository context documents were read as required, not treated as gate execution evidence.
* The issue's broader acceptance is represented by caller context and supplied research; no additional remote issue or open-ended research was performed.
* No unit, Ruff, mypy, browser, SQL, scanner or full-gate command was executed. Static source inspection does not prove post-change results.
* No code, plans, details, research, state, workflow or implementation-review record was changed. This is one complete finding set for the supplied boundary, not an iterative re-critique.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: reconcile the P02 shared-lock and scratch/log procedure with execution constraints and record the finding's disposition, then continue the existing bounded plan without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/gate-chromium-skip-572-plan.md](.copilot-tracking/plans/2026-10-31/gate-chromium-skip-572-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/gate-chromium-skip-572-phase-details.md](.copilot-tracking/details/2026-10-31/gate-chromium-skip-572-phase-details.md) | Assessed implementation and validation steps |
| [.copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md](.copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md) | Supplied C1-C7 evidence and retained acceptance gaps |
| [.copilot-tracking/reviews/plans/2026-10-31/gate-chromium-skip-572-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/gate-chromium-skip-572-plan-critique.md) | Complete critique and PC-001 resolving evidence |

## Next Steps

No user action is required. Return Revise to the active planning parent for the direct PC-001 procedure correction and disposition. Stop after this single critique; do not implement, run checks, invoke a peer stage or request a prohibited full gate.
