<!-- markdownlint-disable-file -->
# RPI Plan Critique: Align Coordinator Correction-Cycle Default and Local-Before-PR Publication Rule (Issue #1296)

## Metadata

* Task ID: issue-1296
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Reconcile `.github/agents/ama-backlog-delivery-coordinator.agent.md` for Issue `#1296` targeting parent integration branch `feat/demo-164-chat-grounding-provenance-0900` (PR `#1641`) across five caller requirements: (1) `2026-11-09` five-total-cycle blocking-finding default with early stop when resolved, human-blocker classification after cycle five absent issue-specific owner authorization, no counter reset, and zero gate waivers (`#1296` AC 1 and AC 2); (2) dated `2026-11-09` five-additional-cycle grant (`E1-E5` for issues already exhausted when granted, citing Quality lane `#1288` resuming from historical `C8` per `https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415`) with historical counter preservation and non-renewal (`#1296` AC 4); (3) preservation of owner decision D5 (`2026-11-01`) turning new non-blocking Copilot threads after two correction cycles into follow-up issues while blocking safety, privacy, or accessibility defects continue to block (`#1296` AC 3); (4) `2026-11-15` owner CI-economy rule in `CI economy and PR backlog cap` and steps 5-6 keeping WIP commits local in the worktree and deferring push and PR creation until local RPI (`research`, `plan`, `implement`, `review`), any local review-correction fixes, and selected-tier local validation finish on a clean frozen candidate; and (5) five-boundary verification qualified for static/simulation vs native execution, `Focused` validation (`git diff --check`), and a local unpushed commit with the Copilot trailer (`#1296` AC 4 and AC 5).
* Research and evidence considered: .copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md, .copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md, .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, .github/copilot-instructions.md
* Decisions, dependencies, and acceptance criteria considered: Research decisions `D-1296-1` through `D-1296-5`; merged ancestry prerequisites `#1301` (`9814cf6b2`) and `#1783` (`ad005cd5f`); functional and non-functional requirements `FR-01` through `FR-05` and `NFR-01` through `NFR-02`; plan acceptance criteria `AC-01` through `AC-06`; and phases/tasks `P01`/`P01-T01`, `P02`/`P02-T01`, and `P03`/`P03-T01`.
* Assessment boundary: Evaluates internal consistency, line-level coverage of `.github/agents/ama-backlog-delivery-coordinator.agent.md`, conformance with `.github/copilot-instructions.md`, and sufficiency of planned validation and commit handoff from the supplied repository artifacts and research provenance (`C1`-`C8`, `W1`-`W3`). Cannot observe live `tmux` multi-worktree coordinator execution or run hosted GitHub Actions checks on an unpushed local candidate.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-01 / AC-01 / AC-02 (`#1296` AC 1-2; `C1, C4, C5, W1`) | Partial | Single-source `Correction-cycle budget` covers 5-total maximum, early stop (`0` valid), no-reset, exhaustion, and retained gates, but `P01-T01` leaves `"five plus..."` extension math in `Human blockers` and `"without editing candidate source"` diagnostic wording open to misinterpretation (`PC-003`). |
| FR-02 / AC-04 (`#1296` AC 4; `W1, W2`) | Partial | `Correction-cycle budget` accurately records the `2026-11-09` `E1-E5` grant and `#1288` `C8` provenance URL, but `Human blockers` parenthetical `"five plus a dated issue-specific owner extension"` conflicts with `#1288` having 8 historical pre-grant cycles (`PC-003`). |
| FR-03 / AC-03 (`#1296` AC 3; `C1, C5, W1`) | Covered | Restores explicit `"after two correction cycles"` threshold for D5 (`2026-11-01`) in both `Human blockers` and step 6 while preserving blocking safety, privacy, and accessibility gates across all cycles. |
| FR-04 / AC-05 (`2026-11-15` rule; `C2, C3, C4, C5`) | Partial | Updates `CI economy`, step 5 brief prose, and step 6 review flow, but misses step 5's end-of-step `Verify RPI use before review` block (`gh pr diff {n}` before PR creation, `PC-001`) and pre-publication `code-review-*` output placement relative to the clean frozen worktree (`PC-002`). |
| FR-05 / AC-06 (`#1296` AC 4-5; `C7, W1`) | Partial | Names five-boundary verification and local unpushed commit in requirements/ACs, but `P03-T01` schedules only mechanical checks without recording HVE-qualified five-boundary trace evidence or post-review noreply local commit steps (`PC-004`). |
| NFR-01 / NFR-02 (`C6, C7, C8`) | Covered | Enforces YAML frontmatter parse, relative link/anchor checks, `ord(c) <= 127` ASCII conformance, `*` list bullets, no bolded-prefix list items (`P01-T01` prose emphasis `**after two correction cycles**` must be emitted unbolded if placed at a list prefix), `git diff --check`, and verbatim `#1783` operational rule preservation. |
| P01 / P01-T01 | Partial | Strong single-source design matching existing coordinator conventions, subject to tightening extension arithmetic and unchanged-tree diagnostic scope (`PC-003`). |
| P02 / P02-T01 | Partial | Unifies pre-PR and post-PR review-correction cycles under one 5-cycle budget, but omits step 5 lines 769-794 (`gh pr diff {n}`) and external review output path protection (`PC-001`, `PC-002`). |
| P03 / P03-T01 | Partial | Mechanical validation checks are well-specified, but task execution omits producing the five-boundary HVE static/trace verification record and explicit local commit handoff (`PC-004`). |

## Verdict

* Verdict: Revise
* Rationale: The single-source `Correction-cycle budget` architecture, D5 two-cycle restoration, and unified pre-PR/post-PR five-cycle accounting are well-grounded in primary evidence (`C1`-`C8`, `W1`-`W3`), but four planner-owned gaps (`PC-001` High; `PC-002` through `PC-004` Medium) would leave an unexecutable `gh pr diff {n}` pre-review check in step 5 before any PR exists, risk dirtying the clean frozen candidate worktree during pre-publication `code-review-*` runs, leave `#1288` (`C8` + `E1-E5`) extension math and non-`src/` diagnostic edits slightly ambiguous in `P01-T01`, and omit implementation-stage five-boundary HVE evidence and noreply-commit sequencing in `P03-T01`.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Step 5 pre-review RPI check still mandates `gh pr diff {n}` before a PR is opened

* Related IDs: FR-04, AC-05, C3, C4, P02, P02-T01
* Evidence: .github/agents/ama-backlog-delivery-coordinator.agent.md lines 769-794; .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md (P02-T01)
* Concern: `P02-T01` updates `CI economy and PR backlog cap`, the mid-step-5 brief rules, and step 6 so that `git push` and `gh pr create` wait until local RPI, selected-tier validation, pre-publication independent exact-head review, and any local review-correction fixes complete. However, `P02-T01` leaves the closing verification block of step 5 (`.github/agents/ama-backlog-delivery-coordinator.agent.md` lines 769-794) untouched, where it still instructs: `"Verify RPI use before review: the PR diff must contain that issue's research, plan, changes and review artifacts (gh pr diff {n} --name-only | grep .copilot-tracking)..."` and `"A PR without them goes back to its loop once..."`.
* Impact: Before pre-publication review in step 6 and the deferred first push, an unpublished local candidate has no pull request `{n}`. Leaving `gh pr diff {n}` as the step 5 pre-review check creates a direct contradiction inside step 5 and causes literal pre-review verification to fail or prematurely open a PR.
* Smallest useful change: Expand `P02-T01` in both the plan and phase details to also update `.github/agents/ama-backlog-delivery-coordinator.agent.md` lines 769-794 so pre-publication RPI artifact verification inspects the local worktree candidate diff against its target base (`git -C {worktree} diff --name-only {base-sha}...HEAD | grep .copilot-tracking`, using `gh pr diff {n} --name-only | grep .copilot-tracking` once published and in step 7), and change `"A PR without them"` to `"A candidate or open PR without them"`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `P02` / `P02-T01` in `.copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md` explicitly scoping `.github/agents/ama-backlog-delivery-coordinator.agent.md` lines 769-794 to use local `git -C {worktree} diff --name-only {base-sha}...HEAD` before PR creation.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Pre-publication `code-review-*` output path can dirty the clean frozen candidate worktree or invalidate exact-HEAD receipts

* Related IDs: FR-04, AC-05, C2, C5, P02, P02-T01
* Evidence: .github/agents/ama-backlog-delivery-coordinator.agent.md lines 381-382, 500-505, 616-640, 798-820; .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md (P02-T01)
* Concern: `CI economy and PR backlog cap` (lines 381-382) currently states `"The local code-review-* verdict, recorded in .copilot-tracking/reviews/, is the review gate"`, while step 6 (lines 798-803) requires a clean frozen candidate worktree with zero dirty/untracked/ignored inputs and a verified exact-HEAD receipt before push. When `P02-T01` moves coordinator-dispatched `hve-core-all:code-review-*` runs before the first push and `gh pr create`, writing coordinator precomputed diffs or `code-review-*` findings into `{worktree}/.copilot-tracking/reviews/` after the worker committed `HEAD` and ran validation either leaves untracked files in `{worktree}` (breaking clean-worktree and Full-tier `--verify-receipt` checks) or forces an extra commit (invalidating exact-HEAD validation, Full-tier receipts, and `rpi_phase_witness.py` `commit-complete`).
* Impact: Without separating the worker's committed `rpi-review` artifact inside `{worktree}/.copilot-tracking/reviews/` from the coordinator's external pre-publication `code-review-*` output path, pre-publication review on a clean candidate invalidates the candidate's own exact-HEAD validation state.
* Smallest useful change: Specify in `P02-T01` (`CI economy` and step 6) that while the issue loop commits its own `rpi-review` artifact under `{worktree}/.copilot-tracking/reviews/` before freezing and validating `HEAD`, the coordinator writes precomputed diffs and independent `code-review-*` review outputs outside `{worktree}` (such as an external coordinator review/evidence directory, matching `rpi_phase_witness.py` and external gate receipts) so `{worktree}` stays clean at the validated exact `HEAD` unless a blocking finding initiates a correction cycle.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `P02-T01` specification in `.copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md` (and `P02` summary in the plan) keeping coordinator pre-publication `code-review-*` outputs external to `{worktree}` so clean-tree and exact-HEAD invariants hold.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `Human blockers` extension formula and `Cycle` diagnostic-edit wording in `P01-T01` leave `#1288` (`C8` + `E1-E5`) and non-`src/` edits ambiguous

* Related IDs: FR-01, FR-02, AC-01, AC-02, AC-04, C1, W1, W2, P01, P01-T01
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md (P01-T01); .copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md (W1, W2)
* Concern: `P01-T01` contains two narrow policy ambiguities: (1) item 1 (`Human blockers`) summarizes an extended budget as `"five total review-correction cycles by default, or five plus a dated issue-specific owner extension"`, which literally evaluates to `5 + 5 = 10` total cycles and contradicts the primary `#1296` AC 4 example where Quality lane `#1288` already had 8 historical cycles (`C1`-`C8`) before receiving five new cycles (`E1`-`E5` per `#1288#issuecomment-6735179415`); and (2) item 2 (`Cycle:`) defines non-consuming diagnostics as `"without editing candidate source"`, which could be read as excluding only `src/` package code while permitting uncounted commits to tests, fixtures, browser checks, or docs past cycle five (even though `#1288`'s `C8` fixture recovery counted as `C8`).
* Impact: A coordinator following `Human blockers` literally could cut off an `E1-E5` grant early when pre-grant history exceeded five cycles, or allow file-modifying test/fixture/doc commits after cycle five under the `"without editing candidate source"` exception.
* Smallest useful change: In `P01-T01`, revise `Human blockers` to say `"up to five total review-correction cycles by default, or after an explicit dated issue-specific owner extension granted beyond an exhausted budget"` (removing `"five plus"` and omitting Markdown `**...**` emphasis when copied into `.agent.md`), and revise `Cycle:` to qualify non-consuming diagnostics as read-only or unchanged-tree checks `"without modifying the candidate commit or tracked worktree files"` and never delaying early stop.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `P01-T01` wording in `.copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md` reconciling `Human blockers` with historical `C8` + `E1-E5` accounting and anchoring non-consuming diagnostics to an unchanged candidate commit/worktree tree.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `P03-T01` omits implementation-stage five-boundary HVE qualification evidence and local noreply-commit sequencing

* Related IDs: FR-05, AC-06, NFR-01, C7, W1, P03, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md (FR-05, AC-06, P03-T01, Handoff); .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md (Test and Validation Ownership Lock, P03-T01); .github/agents/ama-backlog-delivery-coordinator.agent.md lines 803-813; .github/copilot-instructions.md lines 196-205
* Concern: `FR-05`, `AC-06`, and `.github/agents/ama-backlog-delivery-coordinator.agent.md` step 6 (lines 803-813, requiring behavior-bearing `.agent.md` changes to carry static and behavior evidence with exact source identity, execution status, verdict, fidelity, and executor/profile limits) require structured verification of all five `#1296` boundaries (plus unified pre-PR and post-PR cycle accounting) qualified as static/trace evaluation vs unexecuted live `tmux` native runs, followed by a clean unpushed local commit with the Copilot trailer. However, `P03-T01` schedules only mechanical `git diff --check` and Python frontmatter/link/ASCII checks during implementation, leaving primary boundary-verification evidence unrecorded in `.copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md` prior to read-only `rpi-review`, and leaves the post-`rpi-review` local commit steps (`gh api user` `{id}+{login}@users.noreply.github.com` repository-local `user.email`, staging `.agent.md` plus all dated `.copilot-tracking/` artifacts including the final review artifact, Copilot trailer, and zero `git push`) unspecified in `P03` / `Handoff`.
* Impact: If `rpi-implement` executes `P03-T01` literally, `rpi-review` receives a changes record with no primary five-boundary trace or HVE source-identity/fidelity metadata to verify against `FR-05` / `AC-06`, and post-review commit execution risks omitting the repository-mandated `gh api user` noreply author configuration or committing before the review artifact exists.
* Smallest useful change: Expand `P03-T01` (and `Handoff` in the plan) so implementation records in `.copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md` both the mechanical check outputs and the HVE-qualified five-boundary static/trace verification table (including target file SHA-256 source identity, post-edit `path:line` citations, execution status, verdict, `static/trace` fidelity, and live-`tmux` non-execution limits for `rpi-review` to verify independently), and state the post-`rpi-review` local commit protocol (`gh api user` local `user.email`, staging target + all dated `.copilot-tracking/` artifacts including `review.md`, Copilot trailer, clean `git status --short` and `git diff --check`, no `git push`).
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `P03` / `P03-T01` and `Handoff` in `.copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md` specifying the HVE-qualified five-boundary trace matrix in the changes record and the post-`rpi-review` noreply local commit steps.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Single-source design strength: Introducing `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` matches `.github/agents/ama-backlog-delivery-coordinator.agent.md`'s established single-source pattern (`Admission rule` at line 99 and `Receipt refresh rule` at line 866) and prevents future drift across `Human blockers`, `CI economy`, step 5, and step 6.
* Loop-closure strength: Unifying pre-publication local independent-review corrections and post-publication PR-review corrections under one per-issue five-cycle ceiling prevents the `2026-11-15` CI-economy rule from creating a hidden ten-cycle loophole.
* Historical non-regression strength: Explicitly guarding `#1783` (`ad005cd5f`) operational controls (`gemini-4-carbon`, `/mnt/tmp`, `< /dev/null`, adaptive cadence, `src-ci.yml` parity) in `NFR-02` and `P03-T01` protects concurrent coordinator improvements while fixing `ad005cd5f`'s `2026-11-11` date and D5 wording drift.
* Residual risk (explicitly accepted by caller scope): Live multi-worktree `tmux` native coordinator execution is not run in this documentation-only session; residual runtime risk is mitigated by explicit static/trace fidelity qualification (`#1296` AC 4) and observation on subsequent coordinator waves.

## Questions or Blocking Evidence Gaps

* None. All four findings (`PC-001` through `PC-004`) are fully resolved by existing owner authorizations (`#1296`, `#1288#issuecomment-6735179415`, D5 `2026-11-01`, CI-economy rule `2026-11-15`) and `.github/copilot-instructions.md` without requiring user input or further research.

## Limitations

* Critique is strictly read-only over repository sources and supplied planning/research artifacts; external GitHub records (`W1`-`W3`) were assessed via the verified excerpts in `.copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md`.
* Hosted CI (`Source projects CI`) and live `tmux` coordinator behavior are outside local pre-push plan-critique observability.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent (`rpi-plan`)
* Smallest next action: Apply direct planner revisions for `PC-001` through `PC-004` in `.copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md`, record critique dispositions, and finalize the plan without another critique pass.
* User response required: no
