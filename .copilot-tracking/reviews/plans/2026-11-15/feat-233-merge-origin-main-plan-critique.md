<!-- markdownlint-disable-file -->
# RPI Plan Critique: Reconcile feat/demo-233-same-home-tensions-0825 with origin/main

## Metadata

* Task ID: pr-1639-feat-233-merge-origin-main
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Reconcile parent integration branch feat/demo-233-same-home-tensions-0825 (PR #1639, HEAD a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0) with fetched origin/main (45cd2bd00a593d28208f5b99053d854ababb5484) in one continuous non-pausing RPI run across rpi-plan-critique, rpi-implement, and rpi-review; resolve all 10 conflicts preserving both origin/main (#1664, #1665, #1666, #1667, #1672) and #1639 (#233 and child issues) without dropping methods, routes, or fields; validate at the Focused tier (ruff, mypy, and src/core + src/api unit tests without running tools/rpi-checks.py); write .copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md in rpi-implement and .copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md in rpi-review; commit the clean frozen candidate locally with Refs #233, repository-local privacy-safe user.email, zero .copilot-tracking/ strings in the commit message, and the Copilot Co-authored-by trailer; do not push to remote.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md, .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md, .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md, docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/content-standard.md.
* Decisions, dependencies, and acceptance criteria considered: Confirmed additive 3-way merge strategy across all 10 conflicted files; preservation of WCAG 2.2 AA static counters (9 aria-invalid sites, 14 regex-counted tables) and plain-language BLOCKED_WORDS rules; test ownership lock (zero test removals, at most 2 focused additions in test_job_pack.py if needed); web-design-guidelines fetch before web edits and refresh before review; single two-parent local merge commit without git commit --amend and without git push.
* Assessment boundary: Read-only assessment bounded strictly to the supplied plan, phase details, research log (C1-C16), caller requirements, and cited documentation. Live git merge execution, source code diffs outside C1-C16, and test execution belong to rpi-implement and rpi-review and were not mutated or independently researched outside supplied inputs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 (Sync PR #1639 HEAD a1d0be5f6 with origin/main 45cd2bd00) | Covered | C1 verifies live origin/main SHA 45cd2bd00a593d28208f5b99053d854ababb5484 and exact 10-file conflict set |
| Caller Req 2 (Continuous automatic RPI run without pausing) | Covered | Implementation Context Record and User Decisions record automatic continuation through rpi-implement and rpi-review |
| Caller Req 3 (Critique artifact at .copilot-tracking/reviews/plans/2026-11-15/feat-233-merge-origin-main-plan-critique.md) | Covered | Matched in Plan Task Metadata and Implementation Context Record |
| Caller Req 4 (Clean 10-file merge, zero dropped methods/routes/fields, changes artifact, focused tests without tools/rpi-checks.py) | Partial | Overall merge architecture and test lock are sound, but PC-001 identifies dual-contract field/guard omissions across staff_intake.py, staff-intake.js, and app.js, and PC-004 identifies missing worktree-local PYTHONPATH/MYPYPATH isolation for src/api |
| Caller Req 5 (Review artifact at .copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md and local merge commit hygiene) | Partial | PC-002 identifies a review output path mismatch (.copilot-tracking/reviews/logs/2026-11-15/... vs required .copilot-tracking/reviews/2026-11-15/...), and PC-003 identifies stage-boundary inversion in P03-T02 plus unscoped .copilot-tracking/ staging and commit-hygiene gaps |
| Research C1, C4, C5, C6, C9, C10, C15, C16 | Covered | Branch SHAs, test_role_endpoint_inventory.py, READMEs, job_pack.py, store.py, test_job_pack.py, scenario-manifest.json digests, and local tool binaries are accurately mapped |
| Research C2, C3, C7, C8, C11, C12, C13, C14 | Partial | Mapped across P01-T02 and P02-T01, except for view() omitting escalation_destination(), _view_escalation dropping HEAD fields, ambiguous _quality_staff() predicate, and unguarded JS property reads (PC-001) |
| P01 / P01-T01 | Covered | Starts git merge --no-commit origin/main and verifies the 10-file unmerged index list |
| P01-T02 | Partial | Reconciles job_pack.py, staff_intake.py, projection.py, and test_job_pack.py, but has dual-contract specification gaps in view(), _view_escalation(), escalate(), and dual-list deduplication (PC-001) |
| P01-T03 | Covered | Combines accountable_owner fallback with gates.BOOKING_RULES["safety"] in store.py and reconciles src/core/README.md |
| P02 / P02-T01 | Partial | Enforces web-design-guidelines, WCAG counters, and BLOCKED_WORDS, but reads data.escalation.owner_status and work.hazard_clocks.map(...) without null-safe guards when cross-branch fixtures omit one side's key (PC-001) and omits worktree PYTHONPATH for targeted src/api tests (PC-004) |
| P02-T02 | Covered | Unions POST_ENDPOINTS in test_role_endpoint_inventory.py and reconciles src/api/README.md |
| P03 / P03-T01 | Partial | Covers scenario-manifest.json check, unit tests, mypy, and ruff, but omits worktree-local PYTHONPATH/MYPYPATH for src/api (PC-004) and relies on git diff --check HEAD during an uncommitted merge (PC-003) |
| P03-T02 | Partial | Mixes rpi-implement completion with rpi-review execution and final git commit, references the wrong review output directory (PC-002), and uses blanket .copilot-tracking/ staging without author/committer verification or negated-closing-keyword guard (PC-003) |

## Verdict

* Verdict: Revise
* Rationale: The additive 3-way merge strategy grounded in research C1-C16 is well-evidenced, but three High-severity and one Medium-severity planner-owned gaps require direct plan/detail revision before rpi-implement runs: (1) cross-branch field and guard omissions between staff_intake.py, staff-intake.js, and app.js (PC-001), (2) a conflicting review output path against Caller Requirement 5 (PC-002), (3) stage-boundary inversion between rpi-implement (P03-T02) and rpi-review for frozen-candidate staging and single-commit creation (PC-003), and (4) missing worktree-local PYTHONPATH/MYPYPATH isolation for src/api validation (PC-004). None require user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Incomplete dual-contract specification across staff_intake.py, staff-intake.js, and app.js risks runtime TypeError and regression failures

* Related IDs: Caller Req 4, C2, C3, C7, C8, C12, P01-T02, P02-T01
* Evidence: .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md (Functional Requirements lines 68-71), .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md (P01-T02 lines 115-124, P02-T01 lines 249-253), .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md (C2, C3, C7, C8, C12)
* Concern: Four cross-module contract details between HEAD (#1682/#1725/#1692) and origin/main (#1665/#1666) are inconsistent or underspecified across P01-T02 and P02-T01:
  1. P02-T01 requires staff-intake.js to read data.escalation.owner_status and pass data.escalation (checking escalation?.owner_assigned) to intakeEscalate, yet Plan Functional Requirement 1 and P01-T02 omit "escalation": escalation_destination() from staff_intake.view() (specifying only escalation_options, boundaries, and escalations), do not state whether view() also exposes field_escalations if HEAD callers read it, and leave data.escalation.owner_status unguarded when HEAD Node-VM fixtures omit data.escalation.
  2. P01-T02 projects view() escalations through origin/main's _view_escalation(e, user) without specifying that _view_escalation must preserve HEAD's acts_as_contract_instruction, is_contract_instruction, contract_notice, raised_by_email, and raised_at fields; without them, P02-T01's intakeNotInstruction check (acts_as_contract_instruction === false && contract_instruction === false) evaluates false and renders "Unknown - check with the contract manager" instead of "No - not a contract instruction". Dual-writing to c["escalations"] and c["field_escalations"] also needs distinct dict copies (dict(rec)) and a fallback deduplication key when legacy/fixture records lack id (and projection.hold_notes should recognize escalation_kind as well as kind).
  3. P01-T02's directory rule ("when store._quality_staff() is non-empty and explicit or configured owner matches staff roles - verifies the resolved owner['name'] holds owner['role'] in store._quality_staff()") is ambiguous under ProcurementApiFixture (where DATA["staff"] is non-empty for both test_fieldwork_variation_owner_guard.py and test_staff_intake_api.py) and does not specify escalate()'s combined return payload shape (preserving out["escalation"] alongside any HEAD top-level keys).
  4. P02-T01 specifies bare work.hazard_clocks.map(...) in app.js workSummary(work) alongside (work.safeguarding_clocks || []).map(...), risking a TypeError if #1665 fixtures omit hazard_clocks.
* Impact: Implementing P01-T02 and P02-T01 literally as written can throw TypeError on data.escalation.owner_status or work.hazard_clocks.map, render fail-closed "Unknown" rows in StaffIntakeEscalationScreen, collapse id-less fixture escalations during deduplication, or reject valid #1666 configured/synthetic owners in test_staff_intake_api.py.
* Smallest useful change: Update Plan Functional Requirement 1, P01-T02, and P02-T01 to: (a) include "escalation": escalation_destination() (and preserve field_escalations compatibility if present on HEAD) in staff_intake.view() plus null-safe data.escalation?.owner_status in staff-intake.js; (b) require _view_escalation(e, user) to preserve acts_as_contract_instruction, is_contract_instruction, contract_notice, raised_by_email, and raised_at alongside #1666 fields, append separate dict copies to c["escalations"] and c["field_escalations"], deduplicate by id with a composite fallback tuple (work_order_id, kind or escalation_kind, routed_at or raised_at, summary) when id is absent, and match ("kind" in c or "escalation_kind" in c) in projection.hold_notes; (c) define the exact _quality_staff() mismatch predicate against both branches' tests (for example, reject when owner["name"] is a directory member whose directory roles do not include owner["role"], or when an unconfigured staff-role claim fails directory membership as required by HEAD without rejecting #1666 env-configured/external owners) and explicitly preserve both branches' escalate() return keys; and (d) guard (work.hazard_clocks || []).map(...) in app.js.
* Action owner: planning_parent
* Exact resolving evidence: Revised Plan Functional Requirement 1 and Phase Details P01-T02 and P02-T01 explicitly specifying view() keys (including escalation), _view_escalation preserved fields, distinct-copy dual persistence + fallback deduplication, exact _quality_staff() predicate + escalate() return keys, and null-safe JS expressions for data.escalation and work.hazard_clocks.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Review output artifact path contradicts Caller Requirement 5

* Related IDs: Caller Req 5, Acceptance Criteria, P03, P03-T02
* Evidence: .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md (What You May Not Know line 29, Acceptance Criteria line 105, P03-T02 line 198), .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md (P03 Likely Targets line 330, P03-T02 Context line 378)
* Concern: Caller Requirement 5 explicitly directs rpi-review to write .copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md, whereas the plan and phase details consistently specify .copilot-tracking/reviews/logs/2026-11-15/feat-233-merge-origin-main-review.md.
* Impact: Downstream execution following P03-T02 and Acceptance Criteria will either write the review artifact to the wrong subdirectory (violating Caller Requirement 5) or fail to stage the caller-required artifact into the single merge commit.
* Smallest useful change: Replace .copilot-tracking/reviews/logs/2026-11-15/feat-233-merge-origin-main-review.md (and the reviews/logs directory reference in Acceptance Criteria) with .copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md across the plan and phase details.
* Action owner: planning_parent
* Exact resolving evidence: Zero references to .copilot-tracking/reviews/logs/2026-11-15/feat-233-merge-origin-main-review.md in the plan and phase details, with all review artifact pointers matching .copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: P03-T02 inverts the rpi-implement and rpi-review boundary for frozen-candidate staging, commit timing, and commit hygiene

* Related IDs: Caller Req 4, Caller Req 5, Non-Goals, NFR1, P03-T01, P03-T02
* Evidence: .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md (Non-Goals line 64, NFR1 line 78, P03-T01 line 191, P03-T02 lines 194-200), .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md (P03-T02 lines 374-407), .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md (Prior Knowledge Gate line 93)
* Concern: P03-T02 is an implementation checklist item executed during rpi-implement, yet its title, expected result, and completion evidence require completing rpi-review and creating the final local git commit ("ahead 1 of origin/feat/demo-233-same-home-tensions-0825"). Because rpi-implement completes before rpi-review starts and Non-Goal 4 forbids git commit --amend, rpi-implement cannot commit during P03-T02 without omitting the post-implementation review artifact from the single merge commit. In addition, three staging and commit-hygiene details need tightening: (a) P03-T02 says "staging .copilot-tracking/ artifacts" generically rather than scoping git add to this task's feat-233-merge-origin-main-* tracking files (even though prior untracked or unrelated .copilot-tracking/ files may exist in the worktree); (b) NFR1 and P03-T01 rely on git diff --check HEAD while MERGE_HEAD is active instead of checking staged index hygiene (git diff --cached --check) plus explicit conflict-marker scanning across resolved files; and (c) P03-T02 sets git config --local user.email without verifying both GIT_AUTHOR_IDENT and GIT_COMMITTER_IDENT (in case environment variables override config) or explicitly prohibiting even negated closing keywords alongside Refs #233 in the custom git commit -m message.
* Impact: Can cause premature merge commit creation before rpi-review (forcing either a prohibited --amend or a dirty/second commit), accidental staging of unrelated .copilot-tracking/ files, or commit-message/committer-identity policy drift.
* Smallest useful change: Scope P03-T02 strictly to rpi-implement closeout: configure repository-local privacy-safe user.email (and local user.name if unset) and verify git var GIT_AUTHOR_IDENT and git var GIT_COMMITTER_IDENT both use {id}+{login}@users.noreply.github.com; run git diff --cached --check and explicit conflict-marker regex scanning; write .copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md; and stage only the resolved merge files plus this task's feat-233-merge-origin-main-* .copilot-tracking/ files so MERGE_HEAD remains staged and clean as the frozen candidate for rpi-review. Move the review write (.copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md), final staging of the review/session files, and single git commit -m execution (with Refs #233, zero closing keywords even negated, zero .copilot-tracking/ path strings in the message, and the Copilot trailer, without pushing) to the rpi-review handoff and post-review acceptance check per Caller Requirement 5.
* Action owner: planning_parent
* Exact resolving evidence: Revised P03-T01, P03-T02, Functional Requirement 4, NFR1, and Handoff sections separating rpi-implement frozen-candidate staging from rpi-review commit finalization, scoping git add to task-specific .copilot-tracking/ paths, checking git diff --cached --check and GIT_AUTHOR_IDENT/GIT_COMMITTER_IDENT, and banning negated closing keywords.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: src/api validation tasks omit worktree-local PYTHONPATH and MYPYPATH isolation

* Related IDs: Caller Req 4, C16, NFR2, P02, P03-T01
* Evidence: .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md (P01 line 55, P02 lines 226-227, P03-T01 lines 350-372), .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md (Prior Knowledge Gate line 94, C16)
* Concern: P01 pins PYTHONPATH=src:tests for src/core, whereas P02 and P03-T01 omit explicit PYTHONPATH and MYPYPATH values for src/api unittest discovery and mypy. Because execution runs inside git worktree /home/azureuser/source/ama-demo-wt/feat-233-same-home-tensions-0825 in a shared environment, omitting src and ../core/src on PYTHONPATH/MYPYPATH allows Python or mypy to import zava_forward.core or zava_forward.api from an editable site-packages install pointing at another checkout, while running pip install -e would mutate shared user site-packages across worktrees.
* Impact: Focused src/api tests and mypy could silently validate stale code from another worktree rather than the reconciled 10-file merge tree, masking cross-package type or runtime regressions.
* Smallest useful change: Specify explicit worktree-local commands in P02 and P03-T01 for src/api unit tests (PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests /usr/bin/python3 -m unittest discover -s tests -q) and mypy (MYPYPATH=src:../core/src:../agents/src /home/azureuser/.local/bin/mypy src tests), alongside explicit ruff check and ruff format --check commands, without mutating shared editable installs.
* Action owner: planning_parent
* Exact resolving evidence: Explicit worktree-local PYTHONPATH, MYPYPATH, and ruff command invocations recorded in Phase Details P02 and P03-T01.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strong three-way evidence baseline: Research C1-C16 verifies the live origin/main SHA (45cd2bd00a593d28208f5b99053d854ababb5484), enumerates all 10 conflicted files, checks adjacent auto-merged modules (server.py, governance.py, taskqueues.py, workflows.py), and confirms zero changes to the 4 scenario_manifest.py tracked source files.
* Explicit test ownership and UX guardrails: NFR2 and NFR3 lock modified targets to the 10 conflicting files, prohibit test method removals across test_job_pack.py and test_role_endpoint_inventory.py, preserve WCAG 2.2 AA static counters (9 aria-invalid sites, 14 regex-counted tables) and content-standard BLOCKED_WORDS rules, and schedule web-design-guidelines retrieval before web edits and before rpi-review.
* Accepted residual risk: Opt-in Playwright/axe browser checks, full tools/rpi-checks.py gate execution, human assistive-technology/walkthrough sign-offs (#151, #155), and pushing PR #1639 to origin are intentionally excluded from this focused local reconciliation run by explicit caller direction.

## Questions or Blocking Evidence Gaps

* None. All four findings are direct planner corrections resolvable from the supplied caller requirements and research log without additional user input or blocking research.

## Limitations

* This critique is read-only and evaluated only the supplied plan, phase details, research log (C1-C16), caller instructions, and cited project documents; it did not execute git merge or inspect unmerged source hunks outside the supplied research evidence.
* Cross-branch interactions in non-conflicting test files (such as test_generator_determinism_matrix.py, test_safeguarding_clock_a11y.py, test_safeguarding_detail_boundary.py, test_staff_intake_api.py, and test_gates.py) rely on full src/core and src/api unittest discovery during P03-T01 for runtime confirmation.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md and .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md to resolve PC-001 through PC-004, finalize planning status without a second critique pass, and advance immediately to rpi-implement and rpi-review.
* User response required: no
