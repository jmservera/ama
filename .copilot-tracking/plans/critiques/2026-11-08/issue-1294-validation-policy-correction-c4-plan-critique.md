<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-1294-validation-policy-correction-c4

## Metadata

* Task ID: issue-1294-validation-policy-correction-c4
* Critique date: 2026-11-08
* Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c4-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: disposition all eight C3 readiness findings F1-F8; focused tier, docs-only; no workflow or source change; append-only log; preserve retained evidence; independent static review before behavior; at most two behavior attempts; no fifth cycle; no fabricated Pass.
* Research and evidence considered: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c4-research.md; .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-5/checks/ (selector-probe.txt, loader-probe-runner.txt, loader-probe-unset.txt, loader-probe-exits.txt); .github/workflows/src-ci.yml; tools/ci-affected.py; tools/rpi-checks.py (verify and resume paths, spot-read); src/README.md (lines 105-125, 284-300); the independent findings file readiness-findings.json (session files, 8 findings).
* Decisions, dependencies, and acceptance criteria considered: plan FR1-FR7, AC1-AC5, P01-P04 and the phase-details task text.
* Assessment boundary: static read of the plan against supplied evidence. No README edit, behavior run or hosted result exists yet, so only plan credibility is assessed, not the corrected wording.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| F1 / FR7 / P02 | Partial | Independent static stage planned, but it can be made stale by later edits and its proxy status is not labelled non-canonical (PC-001, PC-002) |
| F2 / FR1 / P01-T01(a,b) | Partial | Selector and workflow evidence supports most claims; project job also depends on image-paths; candidate selection claim rests on a synthetic probe (PC-005) |
| F3 / FR2 / P01-T01(c) | Partial | Full/partial split planned; relaxation conditions and resume non-relaxation not stated (PC-004) |
| F4 / FR5 / P04-T01 | Partial | Probe outputs retained; probe command or script is not (PC-006) |
| F5 / FR3 / P01-T01(d) | Covered | Core path exists (research C5); selector shows core selects all, namespace, mssql |
| F6 / FR4 / P01-T01(e) | Partial | Fresh BASE_SHA is wrong for a resume command (PC-003) |
| F7, F8 / FR6 / P04-T02 | Partial | Provenance corrections depend on report 5 and the final changes record; log outcome entry repeats the F8 boundary issue (PC-007) |
| Whitespace note / AC4 | Covered | Source-document check and raw-patch check kept separate |
| Tier classification (focused, docs-only) | Partial | Planned but no recorded basis or hosted-coverage statement (PC-008) |
| Behavior loop cap and terminal rule | Covered with residual risk | Two attempts, Revise reported as Revise; interacts with PC-001 |

## Verdict

* Verdict: Revise
* Rationale: All eight findings are correctly confirmed and dispositioned, and scope and caps respect the owner constraints. The plan still leaves the High F1 gap reproducible (static evidence can go stale after a behavior-driven edit batch) and plans one README command (focused resume with a fresh base) that the runner would reject. Both are direct planner corrections; no user decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Static assessment can be invalidated by the behavior-attempt edit batch

* Related IDs: F1, FR7, P02-T01, P03-T01
* Evidence: phase details P03-T01 ("confirmed contract defects are applied in one batch and attempt 2 runs") and P02-T01 ("A static Pass or closed Revise precedes behavior").
* Concern: If attempt 1 is Revise and the README or instructions are edited, the static review no longer matches the final source. That reproduces the original F1 defect (static evidence not on the final state). P02 only requires static before behavior, not on the final tree. A closure that is still Revise has no defined outcome either.
* Impact: The final candidate could carry a stale static record while the plan reports F1 resolved.
* Smallest useful change: Add to P03-T01 that any source edit after the static stage requires a targeted static closure limited to the edited hunks and original finding IDs before attempt 2, and that the final static record states the exact sha256 and blob IDs it covers, which must equal the committed targets. Define a still-Revise closure as reported Revise with the blocker, not Pass.
* Action owner: planning parent
* Exact resolving evidence: updated P02/P03 text; at implementation, a static log whose covered hashes equal the committed blob IDs for every target.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Proxy static reviewer is not labelled as non-canonical

* Related IDs: F1, FR7, AC3, P02-T01
* Evidence: P02-T01 ("generic Medium-proxy"); research Wave 3 (host `task` offers no model binding); findings file F1 suggested fix (obtain the required independent HVE static assessment, or record a real deferral).
* Concern: The plan says proxy honesty in prose but AC3 only requires "executor, verdict, status, scope". A general-purpose subagent applying the static template may be recorded as satisfying the coordinator's canonical-evidence rule (agent.md:699-706).
* Impact: Risk of a fabricated or overstated Pass, which the caller forbids.
* Smallest useful change: Add to AC3 and P02-T01 that the record carries the label "proxy independent static assessment, not canonical host-bound HVE stage", names the executor agent type, states the rubric used, and keeps human acceptance of proxy evidence in Follow-Up (already present). If the subagent cannot be dispatched, record a real deferral and block behavior only per the retained requirement, never a Pass.
* Action owner: planning parent
* Exact resolving evidence: static review log header with the label and profile limits.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Focused resume example must reuse the original base

* Related IDs: F6, FR4, P01-T01(e)
* Evidence: tools/rpi-checks.py lines 2774-2776 (resume validates with relax_base=False against the supplied base) and 3227 (`--exact-base`); src/README.md lines 123-125 (resume only at the exact same clean commit, base and tool identity).
* Concern: FR4 sets BASE_SHA from freshly fetched origin/main in the focused block, then shows resume "separately". A resume after main has moved with a freshly computed base fails or contradicts the guide.
* Impact: The corrected example would be self-contained but still wrong for the resume case, a new contract defect after F6 is "fixed".
* Smallest useful change: In the resume command, state the base is the recorded base of the failed receipt (read from the receipt identity), not a fresh origin/main; keep fetch and BASE_SHA only for the fresh run.
* Action owner: planning parent
* Exact resolving evidence: README focused block where resume takes the failed receipt's recorded base, checked against rpi-checks.py lines 2774-2776.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Partial-receipt relaxation rule is under-specified

* Related IDs: F3, FR2, P01-T01(c)
* Evidence: src/README.md lines 288-297 (relaxation conditions, `--exact-base`, full receipts never relaxed); rpi-checks.py 2985 (relaxation only for partial scope).
* Concern: FR2 says "BASE RELAXED may keep the receipt valid" without the conditions: fast-forward move only, moved paths docs/tracking/markdown outside src or disjoint from the selected groups, not touching workflows, gate matrix, changed paths or dependents. A shortened sentence can over-promise, producing the reverse of F3. The "rerun on any later commit, correction or rebase" clause for partial receipts must stay.
* Impact: Readers could keep a stale partial receipt after a dependent-project move.
* Smallest useful change: Make the line 493-499 edit a cross-reference to the lines 288-297 rule (verify prints BASE RELAXED, else rerun) instead of restating it; keep full-tier exact-base wording unchanged.
* Action owner: planning parent
* Exact resolving evidence: edited README lines reading as a pointer to the existing rule, with no conflicting restatement, plus the stale-phrase grep in P04-T01.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Hosted-selection claims need two exact corrections and an actual-candidate probe

* Related IDs: F2, FR1, AC1, P01-T01(a,b)
* Evidence: src-ci.yml lines 36-57 (the `project` job runs only if `image-paths` succeeds, and per-step `if: matrix.run`); lines 281-290 (src-no-working-data unconditional); selector-probe.txt (synthetic inputs "readme+log", "readme+tracking" only); ci-affected.py DOC_SUFFIXES (.md and .mdx, at any depth under a project).
* Concern: (1) FR1 omits that project steps also depend on image-paths. (2) The claim "this candidate's own paths select all projects" is inferred from synthetic path sets, not from the candidate's real `git diff --name-only` list. (3) "src/<project>/*.md" understates inert paths (any depth, .mdx).
* Impact: Small inaccuracy risk in the very section F2 criticises.
* Smallest useful change: Run the selector against the actual candidate file list after the final commit (or the working-tree diff) and retain the output; word the inert rule as "markdown directly in src/ or under a project directory"; keep "unobserved hosted result".
* Action owner: planning parent
* Exact resolving evidence: a retained selector-probe output for the actual changed-file list; README wording matching ci-affected.py lines 77-80.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Strict loader probe is not reproducible from retained evidence

* Related IDs: F4, FR5, AC2
* Evidence: .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-5/checks/ holds four output files and no probe command or script text.
* Concern: AC2 relies on outputs only; the exact invocation, cwd, PYTHONPATH values and HEAD are not recorded, so the finding F4 closure cannot be re-run.
* Impact: Weakens independent exact-head review of the very evidence F4 asked for.
* Smallest useful change: Save the probe command text and environment (cwd src/api, runner PYTHONPATH value, PYTHONDONTWRITEBYTECODE=1, HEAD sha) as a new file in sandbox 5 checks, leaving existing files unchanged. Also state the strict probe proves import and name resolution only, not a browser run.
* Action owner: planning parent
* Exact resolving evidence: new sandbox 5 checks file with command and environment; AC2 cites it.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Provenance corrections and the outcome log entry risk repeating the F8 boundary error

* Related IDs: F7, F8, FR6, P01-T02, P04-T02
* Evidence: P01-T02 appends an outcome entry "after the verdict"; P03-T01 says no guide edit after the last attempt but does not bind the log; findings F8 (the C3 outcome entry was appended after grading, then summarised as not simulated).
* Concern: (1) F7 and F8 corrections live in the C4 changes record and report 5, which is created or finalised at the end; if behavior ends Blocked or the report is unwritten, the corrections have no home. (2) The log is a behavior target, and an outcome entry appended after grading again leaves a log state that was never simulated.
* Impact: Same class of overstated source boundary the reviewer already flagged.
* Smallest useful change: Place the F7 and F8 corrections in the correction entry appended in P01-T02 and the C4 changes record, independent of the behavior report. State in report 5 and the changes record that the outcome entry and tracking records were appended after grading and not simulated. Keep identities captured before dispatch and after grading as planned.
* Action owner: planning parent
* Exact resolving evidence: log correction entry citing C3 changes line 37, sandbox 4 pre-run-status.txt, and report 4 lines 13 and 19; report 5 boundary sentence naming the unsimulated entries; append-only diff showing only additions.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Low]: Tier classification and hosted-coverage statement are not recorded

* Related IDs: AC5, repository validation policy (focused tier)
* Evidence: plan Executive Summary says "Focused tier"; repository instructions require recording the classification and its basis, stating what ran and what did not, and treating absent hosted workflows as not a success.
* Concern: No recorded basis (documentation-only; no workflow, tool, dependency, Dockerfile, SQL or security-control change; src/README.md edit does trigger the Source CI path filter), and no statement that hosted CI was not observed and local-only coverage is the loader probe and selector probe.
* Impact: Reviewers cannot confirm the focused tier was justified rather than assumed.
* Smallest useful change: Add one AC line and a changes-record section naming the tier, basis, planned checks, what ran locally, and that hosted Source CI is unobserved; confirm instruction files stay unchanged unless static review finds a defect (then reclassify).
* Action owner: planning parent
* Exact resolving evidence: classification section in the C4 changes record.
* Decision route: direct planner correction

## Strengths and Residual Risk

* All eight findings and the whitespace note have a disposition backed by retained probe output or file/line evidence; the F4 strict probe differentiates success (exit 0, zero loader errors) from three import failures (exit 1).
* Counter-arguments (narrow, do not delete, the inert claim; full-tier exact base retained) are sound and match the selector and runner behavior.
* Scope respects no workflow/source change, append-only log, retained evidence and the two-attempt cap with no fifth cycle.
* Residual risk (to be accepted by the planning parent): the static and behavior stages are proxy, not host-bound; a second Revise is reported as Revise; hosted CI is unobserved; human acceptance remains pending.

## Questions or Blocking Evidence Gaps

* None. No user decision is required; every finding has a direct planner correction.

## Limitations

* The corrected README, static review and behavior report do not exist, so wording and stage outcomes are not assessed.
* tools/rpi-checks.py was spot-read at the verify, resume and relaxation sites only. Findings JSON was read in full for findings 1-8; changed-file list and out-of-scope notes were not reconciled line by line.
* No hosted CI results were available.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Revise the plan and phase details to add PC-001 to PC-008 corrections, record the Critique Disposition, then proceed to P01 without another critique.
* User response required: no

## Next Steps

* The planning parent revises directly and finalizes without another critique. No user action is required.
