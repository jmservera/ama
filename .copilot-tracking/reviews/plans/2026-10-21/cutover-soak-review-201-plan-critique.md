<!-- markdownlint-disable-file -->
# RPI Plan Critique: Cut-over soak evidence preparation for #201

## Metadata

* Task ID: 201-soak-review
* Critique date: 2026-10-21
* Plan: .copilot-tracking/plans/2026-10-21/cutover-soak-review-201-plan.md
* Phase details: .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: preparation-only plan for #201; 11-AC map; soak specification proposal; OPEN duration; pending owner decisions; reconcile in existing docs only; no Azure, tenant, private data, tag, deletion, issue/PR writes, AC ticking or sign-off; no budget headroom; avoid other workers' files (PRs 420-426; #423 lines 1-7 and 166-190).
* Research and evidence considered: .copilot-tracking/research/2026-10-21/cutover-soak-review-201-research.md; spot checks of docs/architecture/cutover-evidence-pack.md (lines 1695-1749), docs/adrs/0006-src-layout-and-cutover.md (lines 298, 361-369), .github/rubric/scores/latest.json, .github/workflows/src-ci.yml, docs/reference/log.md conventions, docs/reference/README.md:288, `gh issue view 201` (read-only), `git status`.
* Decisions, dependencies, and acceptance criteria considered: plan acceptance criteria, D1-D12, P01-P03 dependencies.
* Assessment boundary: no live re-verification of PR 420-426 files, run history or comments beyond the research record; no Azure or tenant checks.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| 11-AC map (P01-T01) | Partial | All 11 AC present and issue text matches `gh issue view 201`; status vocabulary and MET labels need tightening (PC-001, PC-002) |
| Stale-statement reconciliation (P01-T01) | Partial | Rubric 47 to 48 verified (latest.json: 48, A30/B13/C5/D0, `332101ed`, floors false); correction is placed before, not at, the stale text (PC-003) |
| Soak specification (P01-T02) | Covered with gaps | All required dimensions present; some proposed rules are presented as the "existing recovery baseline" without a cited source (PC-004) |
| Pending decisions (P01-T03) | Partial | D1-D12 omit several decisions already on the pack checklist (PC-005) |
| ADR/index/log (P02-T01) | Partial | Log type `update` is not in the log's stated type list (PC-006) |
| Validation and commit (P03) | Partial | Placement claim and final-candidate gate mismatches (PC-007, PC-008) |
| Out-of-scope guards | Covered | No Azure, tag, deletion, ticking or sign-off; #423 hunks avoided |

## Verdict

* Verdict: Revise
* Rationale: The plan is substantively sound and within scope, but several planner-correctable defects could produce an evidence pack that overstates status (MET labels), leaves contradictory stale text, or omits owner decisions the caller wants exact. None needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: MET labels for AC1 and AC2 conflict with "missing/stale/unverified stays UNMET"

* Related IDs: P01-T01, research AC table rows 1-2
* Evidence: research AC table ("MET for ADR acceptance; A1-A5 disposition open"; "MET for removal; mapping caveat open"); pack checklist item 2 leaves A1-A5 and service-role denial gap undispositioned; issue AC1/AC2 text.
* Concern: Rows carry compound statuses. A reader or later automation may take "MET" as the AC being satisfied while owner disposition is open.
* Impact: Risks an implied sign-off signal in a document whose purpose is to avoid one.
* Smallest useful change: Specify in P01-T01 a closed status vocabulary (EVIDENCED-SCOPED, PARTIAL, UNMET) or split each of AC1/AC2 into "evidenced element" and "open element (UNMET)"; state that no status is acceptance and ticking stays with the owner.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 intent defines the vocabulary and the 11 rows show no bare MET; plan acceptance criterion forbids "MET" without scope qualifier.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: PARTIAL rows (AC3, 6, 7, 8) hide the UNMET component

* Related IDs: P01-T01, AC3, AC6, AC7, AC8
* Evidence: research AC table; AC6 requires cause and recovery recorded before sign-off (issue text), which is currently not recorded.
* Concern: PARTIAL without naming the exact unmet sub-requirement lets stale or unverified parts read as progress. AC3 "owner agreement on retire rows not recorded", AC6 "candidate score and cause/recovery", AC7 "refresh at sign-off", AC8 "full link gate external" are the unmet parts.
* Impact: Weakens the caller rule that unverified stays UNMET.
* Smallest useful change: Add an explicit "UNMET component" column or text to each PARTIAL row, using the gap wording already in research.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 Intent lists the UNMET component per PARTIAL row; table check finds none without one.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Stale statements remain uncorrected in place

* Related IDs: P01 Intent/Boundaries, P01-T01
* Evidence: pack lines 1697-1710: "`gh pr list` returned `[]`" and "currently committed score snapshots point to `fa730d63` ... total 47 ... no valid post-migration numeric comparison"; latest.json now reports 48 at `332101ed`. The plan inserts the new section before "Other Cut-Over Gates" and forbids rewriting historical text.
* Concern: The stale sentences sit directly after the new section and still read as current ("currently committed"), so the pack contradicts itself and the checklist item 9 wording.
* Impact: Misleading evidence to the owner and later reviewers.
* Smallest useful change: Allow a single appended one-line "Superseded by the 2026-10-21 section" pointer after each stale paragraph (additive, outside #423 hunks), or state in the new section's first sentence which exact lines are superseded and that the older text is retained as history. Update P01 Boundaries and the "two places" completion evidence accordingly.
* Action owner: planning parent
* Exact resolving evidence: P01 Boundaries and Completion Evidence name the pointer lines; implemented diff shows additions only and no #423 overlap.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Unsourced rules presented as existing baseline or as spec content

* Related IDs: P01-T02
* Evidence: P01-T02 failure row ("per the existing recovery baseline"), CI row ("src-ci, mvp-ci, mvp-validation, infra-plan" required), rubric row (score "48 (A30 B13 C5 D0)"), environment row ("named non-production synthetic environment in `ama`"), reset triggers. The research cites no source for the recovery baseline or the required-workflow set; .github/workflows also holds src-deploy.yml and rubric-score.lock.yml.
* Concern: Reset triggers, required-check set and rollback wording read as established rules, though only duration/cadence/tolerance are labelled OPEN. The rubric row embeds a specific baseline that is an unverified comparison basis (research: comparability unverified).
* Impact: Invents controls and implies approvals; contradicts the "proposal, nothing decided" posture.
* Smallest useful change: Cite the pack section for the recovery baseline or drop the phrase; label every row "proposed" with an explicit "OPEN (owner)" on the reset-trigger list, required-workflow set (verify against .github/workflows and branch protection by read-only reference, noting protection is not verified) and rubric baseline.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 cites a file:line for each non-OPEN assertion; validation search shows every row labelled proposal.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: D1-D12 omit pending decisions already on the pack checklist

* Related IDs: P01-T03, plan Functional Requirements ("exact pending owner decisions")
* Evidence: pack checklist items at lines 1719-1749: retained `ama` resources and charges (remediation/retention or ID-scoped cleanup), approval of the post-cut-over rename plan, tenant registration/Graph/roster and authorized HTTP acceptance (#349/#350), go/no-go record. Research AC3 gap: owner agreement on retire rows not recorded.
* Concern: The new list is presented as the exact pending set but D1-D12 omits these; D7 only touches finance and the sign-in smoke.
* Impact: Owner may think the list is complete.
* Smallest useful change: Add decisions (retire-row agreement for AC3; retained `ama` resource/charge disposition; rename-plan approval; tenant/staff acceptance prerequisites #349/#350; final go/no-go) or add a crosswalk row stating D1-D12 are soak-specific and the existing checklist items remain the remaining decisions.
* Action owner: planning parent
* Exact resolving evidence: P01-T03 lists each checklist item mapped to a D-number or crosswalk; each has owner and smallest evidence.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Log entry type not in documented type list

* Related IDs: P02-T01
* Evidence: docs/reference/log.md Conventions list `ingest`, `query`, `restructure`, `memory`, `lint`; plan uses `update` (76 existing entries also use it).
* Concern: Convention drift; existing precedent exists, so risk is small.
* Impact: Searchability inconsistency.
* Smallest useful change: Use the documented `query` type (recent entries do) or note the precedent; list files touched and the raised contradiction (D1) in the entry as the convention requires.
* Action owner: planning parent
* Exact resolving evidence: P02-T01 states the type and the entry lists touched files and open contradiction.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Shared-file overlap and base-revision safeguards are incomplete

* Related IDs: P01, P02, P03, plan Dependencies
* Evidence: research W4 (all open PRs touch index/log); plan Dependencies only cites #423 for the pack; local HEAD equals origin/main `993a7b88` today; line numbers (1697, 1719, README:288, ADR 298/366) are cited from this base.
* Concern: Plan has no check immediately before editing and before commit that (a) origin/main is unchanged, (b) no merged PR moved the cited anchors, and (c) the index row 288 and log tail are not changing under other open PRs. It also does not say the README row is edited by a single-line change to minimize conflicts.
* Impact: Merge conflicts or edits on stale line anchors; log append-only could be broken by a rebase.
* Smallest useful change: Add to P01 and P03 a read-only `git fetch` plus anchor-by-heading check (not line numbers), a one-row-only README edit and log end-of-file append, and record the base SHA in the changes record.
* Action owner: planning parent
* Exact resolving evidence: P03-T01 validation lists fetch result, base SHA and heading-based anchor checks.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Local commit scope and final-gate handoff are ambiguous

* Related IDs: P03-T01, plan Acceptance Criteria ("clean including ignored and untracked"), repository RPI gate rules
* Evidence: `git status --short` shows .copilot-tracking/{details,plans,research,rpi-sessions}/2026-10-21 untracked, and .copilot-tracking is tracked in git with no ignore rule; plan says tracking is committed but also "no copied tracking" and defers the full gate to the coordinator; P03 plans two local commits with no amend.
* Concern: The plan neither states that its commits are not a final RPI candidate nor that the receipt/`rpi-checks.py` gate and independent assessment remain the coordinator's, with any later commit (including the Review commit) invalidating a receipt; it also does not say the critique file's path is the only critique write, nor whether rpi-sessions files are committed.
* Impact: Coordinator may treat the branch as gate-ready, or a prior gate run may be invalidated unnoticed.
* Smallest useful change: Add a Handoff statement: not publishable, no push/PR; list tracking paths to commit (plan, details, research, critique, changes, state) and rpi-sessions disposition; note that post-commit changes invalidate any receipt; keep original critique outcome unedited (Critique Disposition updated only in the plan).
* Action owner: planning parent
* Exact resolving evidence: Plan Handoff and P03-T01 enumerate committed tracking paths and gate ownership; final `git status --short --ignored` empty.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-009 -->
### PC-009 [Low]: Plan readiness statements are overconfident

* Related IDs: plan Handoff, Critique Disposition, research Planning Readiness
* Evidence: plan Handoff "Remaining provisional question or blocker: none"; research D1 contradiction unresolved and the budget cap overdrawn.
* Concern: "none" understates that D1-D12 are pending and that implementation text must keep every one pending; no stop rule if the owner posts a decision in #201 mid-implementation.
* Impact: Implementer might record an owner decision from a newly seen comment (inferred sign-off).
* Smallest useful change: Handoff: "none for preparation; D1-D12 remain pending and must not be recorded as decided; re-read #201 read-only before commit and report, not apply, any new owner comment."
* Action owner: planning parent
* Exact resolving evidence: Plan Handoff contains the statement.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strong scope discipline; owner-only items (backup attestation, tag, sign-off) remain owner-owned; #423 hunks avoided; duration kept OPEN; cost cap noted.
* Accepted residual risk: PR 420-426 file checks and run history rely on the research record dated 2026-10-21; no live re-check was performed here.
* The D1 contradiction (2026-10-15 "no minimum soak" vs open issue item and 2026-10-20 proposal request) is correctly surfaced for the owner and not resolved by the plan.

## Questions or Blocking Evidence Gaps

* None blocking. No user decision is required for any finding.

## Limitations

* Read-only; no live gh PR or run verification; only the listed files were spot-checked, not the whole pack.

## Artifacts

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-21/cutover-soak-review-201-plan.md](.copilot-tracking/plans/2026-10-21/cutover-soak-review-201-plan.md) | Plan critiqued |
| [.copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md](.copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md) | Phase details critiqued |
| [.copilot-tracking/research/2026-10-21/cutover-soak-review-201-research.md](.copilot-tracking/research/2026-10-21/cutover-soak-review-201-research.md) | Research evidence |

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: revise plan and details directly for PC-001 to PC-009, record dispositions in the plan's Critique Disposition, and finalize without another critique.
* User response required: no

## Next Steps

Return the verdict to the planning parent (rpi-plan); no user action is required.
