<!-- markdownlint-disable-file -->
# RPI Plan: Align Coordinator Correction-Cycle Default and Local-Before-PR Publication Rule (Issue #1296)

## Task Metadata

* Task ID: issue-1296
* Task slug: delivery-1296-correction-cycles
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/delivery-1296-correction-cycles-plan-critique.md

## Executive Summary

This plan updates `.github/agents/ama-backlog-delivery-coordinator.agent.md` to align the backlog coordinator's review-correction policy with the owner's **2026-11-09 five-total-cycle default** and **dated five-additional-cycle extension grant (`E1-E5`)**, restore owner decision **D5 (`2026-11-01`)** for non-blocking Copilot follow-up threads after two correction cycles, and codify the owner's **2026-11-15 CI-economy rule** deferring branch push and pull request creation until local RPI (`research`, `plan`, `implement`, `review`), any local review-correction fixes, and selected-tier local validation complete on a clean frozen candidate.

### User Decisions and Requirements Highlights

* Default blocking-finding correction budget is **up to five total review-correction cycles per issue** (`2026-11-09`), stopping early as soon as blocking findings are resolved and becoming a human blocker after cycle five unless an explicit issue-specific owner extension exists.
* Issues already exhausted when the owner issued the `2026-11-09` grant (`"add 5 additional cycles to exhausted issues"`, such as Quality lane `#1288` resuming from `C8` per `#1288#issuecomment-6735179415`) hold up to five new cycles (`E1-E5`) with prior cycles preserved as historical and no automatic renewal.
* Owner decision **D5 (`2026-11-01`)** remains unchanged: new non-blocking Copilot threads raised **after two correction cycles** become follow-up issues, while blocking safety, privacy, or accessibility defects continue to block publication and merge.
* Under the **2026-11-15 CI-economy rule**, WIP commits and local review-correction fixes stay local in the issue worktree until full local RPI, selected-tier local validation, and pre-publication independent exact-head review pass on a clean frozen candidate, avoiding repeated GitHub Actions runs.

### What You May Not Know

* Earlier on `2026-11-15`, commit `ad005cd5f` (`#1783`) applied general chronicle updates to `.github/agents/ama-backlog-delivery-coordinator.agent.md` and partially edited the correction-cycle sentences, inadvertently changing D5's `"after two correction cycles"` to `"after the [allowed] correction cycles"`, misdating the five-cycle default as `2026-11-11`, and adding an unqualified diagnostic-cycle clause. This plan preserves all unrelated `#1783` operational rules while repairing those exact passages.
* Pre-publication local review-correction cycles and post-publication PR review-correction cycles share one unified per-issue five-cycle budget so deferring PR creation saves hosted Actions runs without creating a ten-cycle loophole; coordinator pre-publication `code-review-*` outputs stay in an external coordinator directory outside `{worktree}` so the candidate's clean frozen `HEAD` is never dirtied (`PC-002`), and pre-publication RPI artifact checks inspect `git -C {worktree} diff --name-only {base-sha}...HEAD` before a PR exists (`PC-001`).
* Repository Markdown checks require plain ASCII (`ord(c) <= 127`, ASCII hyphens `E1-E5` rather than Unicode en-dashes), `*` unordered list markers, and unbolded list-item prefixes.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Reconcile `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Human blockers` and step 6 `Review each candidate independently before publishing`) with the owner's `2026-11-09` default of up to five total review-correction cycles per issue, stating clearly that a blocking finding can receive correction through cycle five without further approval and that correction stops earlier when the finding is resolved (Issue `#1296` AC 1).
* Specify that an unresolved blocking finding after five total cycles becomes a human blocker unless the owner has authorized an additional issue-specific cycle; do not reset used cycles or interpret the default as additional authorization, and waive no finding, safety, resident-consent, human-approval, validation-tier, or independent exact-head review gate (Issue `#1296` AC 2).
* Preserve owner decision D5 (`2026-11-01`): new non-blocking Copilot threads raised after two correction cycles become follow-up issues and do not hold the PR, whereas blocking safety, privacy, or accessibility defects still stop the PR (Issue `#1296` AC 3).
* Record the owner's dated `2026-11-09` grant (`"add 5 additional cycles to exhausted issues"`, e.g. Quality lane `#1288` resuming from `C8` with extension `E1-E5` per `https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415`): previous consumed cycles remain historical, up to five new correction cycles are available for issues exhausted when the grant was made, exhaustion of that extension requires new owner authority, and counters are never reset or endlessly extended for issues that subsequently exhaust the standing default (Issue `#1296` AC 4).
* Codify in `## CI economy and PR backlog cap` and steps 5-6 the owner's `2026-11-15` CI-economy rule that issue loops keep WIP commits local in their worktree and do not push or open a pull request until the local RPI loop (`research`, `plan`, `implement`, `review`), any local review-correction fixes, and selected-tier local validation have completed on a clean frozen candidate (Caller brief item 4).
* Document and verify the five-total-cycle, early-stop, exhausted-limit, authorized-extra-cycle (`E1-E5`), and D5 two-cycle non-blocking boundaries in the RPI review artifact with explicit static/simulation vs native execution qualification, validate with focused checks (`git diff --check`), commit locally with the Copilot trailer, and do not push from inside this session (Issue `#1296` AC 4 & AC 5; Caller brief item 5).

## Goals

* Establish one unambiguous, single-source correction-cycle budget contract in `.github/agents/ama-backlog-delivery-coordinator.agent.md` aligned with the `2026-11-09` default and `E1-E5` grant.
* Restore exact D5 (`2026-11-01`) two-cycle non-blocking thread handling while preserving strict blocking gates for safety, privacy, accessibility, correctness, consent, validation-tier, and independent exact-head review.
* Codify local-before-PR WIP, review-correction, and validation completion across `CI economy and PR backlog cap` and workflow steps 5-6 (`2026-11-15` rule).

## Scope and Non-Goals

### In Scope

* Surgical policy updates to `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Human blockers`, new `Correction-cycle budget` single-source section, `CI economy and PR backlog cap`, step 5, and step 6).
* Focused mechanical validation (`git diff --check`, YAML frontmatter parse, relative link check, plain-ASCII and Markdown style check) and five-boundary verification record in `.copilot-tracking/reviews/`.
* Clean local commit on the active worktree branch targeting `feat/demo-164-chat-grounding-provenance-0900` (PR `#1641`) without pushing.

### Non-Goals

* Modifying `.github/copilot-instructions.md`, `src/`, `infra/`, `tools/`, GitHub Actions workflows, or repository branch-protection settings.
* Running heavy full-gate services (`tools/rpi-checks.py --all`), live Azure operations, or live `tmux` multi-worktree coordinator dispatches.
* Pushing to `origin` or opening/updating a pull request from inside this worker session.

## Functional Requirements

* FR-01: Single-source correction-cycle budget and five-cycle default (`#1296` AC 1 & AC 2)
  * Observable acceptance criteria: `.github/agents/ama-backlog-delivery-coordinator.agent.md` defines `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` and links `Human blockers`, step 5, and step 6 to it, stating up to five total review-correction cycles per issue as a maximum, early stop as soon as no blocking finding remains (`0` cycles valid), human-blocker classification after five total cycles absent explicit issue-specific owner authority, no counter resets, qualification that unchanged-source diagnostics never authorize extra source-correction cycles, and retention of all safety, privacy, accessibility, resident-consent, human-approval, validation-tier, and independent exact-head review gates.
* FR-02: Dated five-additional-cycle extension grant (`#1296` AC 4)
  * Observable acceptance criteria: `## Correction-cycle budget` records the `2026-11-09` grant (`"add 5 additional cycles to exhausted issues"`), preserves pre-grant consumed cycles as historical, grants up to five new cycles (`E1` to `E5`) solely to issues exhausted when granted (citing `#1288` resuming from historical `C8` at `https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415`), stops early when resolved, treats exhaustion of `E5` as a human blocker requiring new owner authority, and forbids automatic extensions for issues that later exhaust the standing default.
* FR-03: Preservation of owner decision D5 (`#1296` AC 3)
  * Observable acceptance criteria: Both `Human blockers` and step 6 state explicitly that new non-blocking Copilot threads raised **after two correction cycles** become follow-up issues and do not hold the PR (`owner decision D5, 2026-11-01`), while blocking findings including safety, privacy, or accessibility defects still stop publication and merge.
* FR-04: Local-before-PR publication rule (`2026-11-15` CI-economy rule)
  * Observable acceptance criteria: `## CI economy and PR backlog cap`, step 5, and step 6 state explicitly that issue loops keep WIP commits local in their worktree and do not push or open a pull request until the local RPI loop (`research`, `plan`, `implement`, `review`), any local review-correction fixes (counted within the single per-issue five-total cycle budget), selected-tier local validation, and pre-publication independent exact-head assessment complete on a clean frozen candidate.
* FR-05: Five-boundary verification and focused local delivery (`#1296` AC 4 & AC 5)
  * Observable acceptance criteria: Dated research, plan, details, critique, changes, and review artifacts exist under `.copilot-tracking/`; the review artifact verifies the five-total-cycle, early-stop, exhausted-limit, authorized-extra-cycle (`E1-E5`), and D5 two-cycle non-blocking boundaries with explicit static/trace vs native execution qualification; `git diff --check` and mechanical checks pass; and all changes are committed locally with the Copilot trailer and unpushed.

## Non-Functional Requirements

* NFR-01: Repository Markdown, frontmatter, link, and ASCII conformance
  * Objective threshold or evaluation condition: YAML frontmatter keys (`name`, `description`) parse cleanly; 100% of relative Markdown links resolve; 100% of characters in `.github/agents/ama-backlog-delivery-coordinator.agent.md` are plain ASCII (`ord(c) <= 127`) with zero em/en dashes, `*` unordered list bullets, and zero new bolded-prefix list items; `git diff --check` exits `0`.
  * Operating condition or verification approach, if needed: Deterministic Python mechanical check plus `git diff --check` on the modified file.
  * Observable acceptance criteria: Zero whitespace, frontmatter, link, or ASCII/style violations.
* NFR-02: Zero regression of `#1783` (`ad005cd5f`) operational coordinator controls
  * Objective threshold or evaluation condition: Unrelated `#1783` rules (`gemini-4-carbon` worker model, `/mnt/tmp` and `< /dev/null` launcher hardening, eight-session stack concurrency wording, adaptive 10-30 minute delivery cadence, and local `src-ci.yml` parity checklist) remain verbatim in `git diff`.
  * Observable acceptance criteria: `git diff` touches only the intended sections (`Human blockers`, `Correction-cycle budget`, `CI economy and PR backlog cap`, step 5, and step 6).

## Acceptance Criteria

* AC-01: `Human blockers`, `Correction-cycle budget`, and step 6 reconcile blocking-finding corrections to the `2026-11-09` maximum of up to five total cycles per issue with explicit early stop when resolved (`#1296` AC 1).
* AC-02: Unresolved blocking findings after five total cycles become a human blocker absent explicit issue-specific owner authorization, without resetting used cycles, treating the default as extra budget, allowing unchanged-source diagnostics to authorize source fixes past cycle five, or waiving any safety, privacy, accessibility, resident-consent, human-approval, validation-tier, or independent exact-head review gate (`#1296` AC 2).
* AC-03: Owner decision D5 (`2026-11-01`) is preserved with its explicit two-cycle threshold for new non-blocking Copilot threads while blocking safety, privacy, and accessibility defects continue to block (`#1296` AC 3).
* AC-04: The dated `2026-11-09` five-additional-cycle grant (`E1-E5`, citing `#1288` resuming from `C8` at `#1288#issuecomment-6735179415`) is recorded with historical cycle preservation, fixed eligibility, early stop, and non-renewal (`#1296` AC 4).
* AC-05: `CI economy and PR backlog cap` and steps 5-6 explicitly require keeping WIP commits local in the worktree and deferring push/PR creation until local RPI (`research`, `plan`, `implement`, `review`), any local review-correction fixes within the single per-issue cycle budget, and selected-tier local validation complete on a clean frozen candidate (`2026-11-15` rule).
* AC-06: Focused mechanical checks (`git diff --check`, frontmatter, relative links, ASCII/Markdown style), five-boundary verification (qualified as static/trace verification vs native execution), dated `.copilot-tracking/` RPI artifacts, and a clean unpushed local commit with the Copilot trailer are complete (`#1296` AC 4 & AC 5).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md                                                               |
| Phase details                    | .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md                                                    |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/delivery-1296-correction-cycles-plan-critique.md with Revise disposition (PC-001 to PC-004 resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md                                                        |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete; implementation `P01`-`P03` complete and ready for `rpi-review`                                 |
| Continuation context             | Confirmed automatic RPI Agent automatic continuation to `Review`                                         |

## Sources

* .copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md: Synthesizes `C1`-`C8` and `W1`-`W3`, resolving `#1783` date/D5 drift and pre-PR/post-PR cycle-budget unification.
* .github/agents/ama-backlog-delivery-coordinator.agent.md: Canonical target artifact (`Human blockers`, `CI economy and PR backlog cap`, step 5, step 6).
* .github/copilot-instructions.md: Governs Focused validation tier (`git diff --check`), branch/email rules, and plain-ASCII Markdown style.
* https://github.com/jmservera/ama/issues/1296 and https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415: Primary owner authorization records (`2026-11-09`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reconcile correction-cycle budget, D5 two-cycle threshold, and dated E1-E5 grant

* Intent: Establish the canonical `Correction-cycle budget` section and align `Human blockers` and step 6 with `#1296` AC 1-4 while preserving `#1783` controls.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add canonical Correction-cycle budget section and reconcile Human blockers

* Requirement and evidence: FR-01, FR-02, FR-03; research `C1, C4, C6, C8, W1, W2`; critique `PC-003`
* Expected result: `Human blockers` references `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` (using extension-beyond-exhausted-budget wording compatible with `#1288` historical `C8` + `E1-E5`), restores `"after two correction cycles"` for D5 (`2026-11-01`), fixes the `2026-11-09` date, and the new section defines cycle consumption, five-total maximum with early stop (`0` valid), ledger tracking, no-reset, exhaustion human blocker, bounded read-only/unchanged-tree diagnostic limits (never modifying the candidate commit or tracked worktree files and never delaying early stop), the dated `2026-11-09` `E1-E5` grant (`#1288` from `C8`), no-bypass, and retained gates in plain ASCII Markdown.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Codify 2026-11-15 local-before-PR CI-economy rule and step 5-6 publication flow

* Intent: Ensure WIP commits, full local RPI, pre-publication RPI artifact checks on the local branch diff, any local review-correction fixes (within the single five-cycle budget), selected-tier validation, and external-output pre-publication independent exact-head review finish locally before `git push` or `gh pr create`, while preserving D5 in step 6.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update CI economy and PR backlog cap, step 5, and step 6

* Requirement and evidence: FR-01, FR-03, FR-04, NFR-02; research `C2, C3, C4, C5, C6, C8, W1`; critique `PC-001, PC-002`
* Expected result: `CI economy and PR backlog cap` (`2026-11-03; updated 2026-11-15`), step 5 (including brief rules and the closing `Verify RPI use before review` block using `git -C {worktree} diff --name-only {base-sha}...HEAD | grep .copilot-tracking` pre-publication and `gh pr diff {n}` post-publication), and step 6 explicitly keep WIP commits and local review-correction fixes local in the worktree until local RPI (`research`, `plan`, `implement`, `review`), selected-tier local validation, and pre-publication independent exact-head review (writing coordinator `code-review-*` outputs outside `{worktree}` so `{worktree}` stays clean at exact `HEAD`) pass on a clean frozen candidate; step 6 references `Correction-cycle budget` and restores `"After two correction cycles"` for D5 (`2026-11-01`).
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Run focused mechanical validation, record HVE-qualified five-boundary trace evidence, and stage clean local commit readiness

* Intent: Verify frontmatter, relative links, plain-ASCII Markdown rules, `git diff --check`, `#1783` non-regression, and SHA-256/line-anchored five-boundary static/trace evidence in `changes.md` before `rpi-review` and post-review noreply local commit.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute focused validation checks, record five-boundary HVE static/trace matrix, and reconcile tracking records

* Requirement and evidence: FR-05, NFR-01, NFR-02; research `C7, C8, W1`; critique `PC-004`
* Expected result: `git diff --check` exits `0`; Python check confirms valid YAML frontmatter, 100% resolved relative Markdown links and `#correction-cycle-budget-owner-2026-11-09-issue-1296` anchor, `ord(c) <= 127` ASCII conformance, `*` bullets, and untouched `#1783` operational passages; `changes.md` records target SHA-256 source identity and the HVE-qualified five-boundary static/trace verification table (`static/trace` fidelity vs unexecuted live `tmux` native runs) for independent verification in `rpi-review`; plan/details/changes records reconciled for `rpi-review` followed by local `gh api user` noreply commit with Copilot trailer and zero push.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md

## Dependencies

* Merged PR `#1301` (`#1294` validation policy) and `#1783` (`ad005cd5f` chronicle updates): Already present in worktree `HEAD` (`697b00c0a`, matching `origin/feat/demo-164-chat-grounding-provenance-0900` / PR `#1641`).
* Focused validation tools (`git`, `python3` with `yaml`): Available in local environment; no new test files (`0` additions, `none` removals) are added because `.github/agents/ama-backlog-delivery-coordinator.agent.md` is an instruction-only artifact validated mechanically and via structured five-boundary trace review.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [High]: Step 5 closing `Verify RPI use before review` block still used `gh pr diff {n}` before PR creation | resolved | Expanded `P02` / `P02-T01` to update step 5's closing verification block to check `git -C {worktree} diff --name-only {base-sha}...HEAD \| grep .copilot-tracking` pre-publication (`gh pr diff {n}` post-publication and in step 7) and `"A candidate or open PR without them"`. |
| Run 1 `PC-002` [Medium]: Pre-publication `code-review-*` outputs inside `{worktree}/.copilot-tracking/reviews/` would dirty `{worktree}` or invalidate exact-HEAD validation | resolved | Updated `P02-T01` (`CI economy` and step 6) so the worker commits its `rpi-review` artifact under `{worktree}/.copilot-tracking/reviews/` before freezing `HEAD`, while coordinator precomputed diffs and `code-review-*` verdicts write to an external coordinator review directory outside `{worktree}`. |
| Run 1 `PC-003` [Medium]: `Human blockers` `"five plus..."` formula conflicted with `#1288` (`C8` + `E1-E5`) and `"without editing candidate source"` left non-`src/` commits ambiguous | resolved | Updated `P01-T01` so `Human blockers` states `"up to five total review-correction cycles by default, or after an explicit dated issue-specific owner extension granted beyond an exhausted budget"` (plain unbolded text in `.agent.md`) and `Cycle:` anchors non-consuming diagnostics to `"without modifying the candidate commit or tracked worktree files"` and never delaying early stop. |
| Run 1 `PC-004` [Medium]: `P03-T01` omitted HVE-qualified five-boundary trace evidence in `changes.md` and post-`rpi-review` noreply local commit steps | resolved | Expanded `P03` / `P03-T01` and `Handoff` to record target SHA-256 source identity and the HVE-qualified five-boundary static/trace matrix in `changes.md` for `rpi-review` verification, followed by post-review `gh api user` `{id}+{login}@users.noreply.github.com` repository-local `user.email` configuration and clean unpushed local commit with Copilot trailer. |
| Residual risk (live `tmux` native coordinator execution) | accepted with risk | Explicit caller/issue boundary (`#1296` AC 4): documentation-only Focused-tier edit qualifies static/trace boundary verification and claims no live native `tmux` execution; mitigated by follow-up wave observation. |

## Follow-Up Items

* Observe PR-push frequency across subsequent coordinator delivery waves under the `2026-11-15` local-before-PR CI-economy rule (outside immediate documentation scope; owned by future coordinator wave telemetry).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md
* Ready phase or task: P01 (`P01-T01`), then P02 (`P02-T01`), then P03 (`P03-T01`); after `rpi-review` writes `.copilot-tracking/reviews/logs/2026-11-15/delivery-1296-correction-cycles-review.md`, resolve `gh api user` repository-local `{id}+{login}@users.noreply.github.com`, verify `git diff --check`, and create one clean local commit staging `.github/agents/ama-backlog-delivery-coordinator.agent.md` plus all dated `.copilot-tracking/` artifacts with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.
* Remaining provisional question or blocker: none
