<!-- markdownlint-disable-file -->
# RPI Changes: Align Backlog Delivery Coordinator Correction-Cycle Default, Dated Extension Grant, D5 Boundary, and Local-Before-PR CI-Economy Rule (Issue #1296)

## Metadata

* Task ID: issue-1296
* Related plan: .copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (P01, P02, P03)
* Completed scope markers: P01, P01-T01, P02, P02-T01, P03, P03-T01
* All remaining active-plan markers: none
* Status basis: All planned edits to `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`SHA-256: dda5f87a9438d3a1a951c7aec516b8aaefed78ca52c890dbcc0b0a1091045803`), focused mechanical validation (`git diff --check`, frontmatter, relative links/anchors, plain ASCII, Markdown style, and `#1783` diff hunk boundary), and HVE-qualified five-boundary static/trace verification completed cleanly.

## Execution Summary

Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` on active worktree branch `docs/1296-correction-cycles-1125` (checked out in `/home/azureuser/source/ama-demo-wt/docs-1296-correction-cycles` at `feat/demo-164-chat-grounding-provenance-0900` base `697b00c0a`; caller prose parenthetically mentioned `docs/delivery-1296-correction-cycles`, preserved active worktree branch without rewriting refs) to deliver Issue `#1296` and the owner's `2026-11-15` CI-economy publication rule while keeping every operational control from `#1783` (`ad005cd5f`) intact.

## Completed Work

### Canonical Correction-Cycle Budget Section and Human-Blocker Alignment

* Related phase or task: P01 (`P01-T01`)
* Files: `.github/agents/ama-backlog-delivery-coordinator.agent.md`
* What changed and why: Added `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` (`Cycle`, `Default`, `Ledger`, `Exhausted`, `Dated grant`, `Retained gates`) as the single cross-referenced policy source and reconciled `## Human blockers` so blocking findings escalate to `human-blocked` only when the issue's budget is exhausted (`up to five total review-correction cycles by default, or after an explicit dated issue-specific owner extension granted beyond an exhausted budget`, matching `#1288` historical `C1-C8` + `E1-E5`), restored owner decision D5 (`2026-11-01`) to `"after two correction cycles"`, corrected the `2026-11-09` authorization date, and bounded unchanged-tree diagnostics so they cannot modify the candidate commit or tracked worktree files, delay early stop, or authorize a sixth file-modifying fix.
* Completion evidence: Diff hunks in `## Human blockers` and `## Correction-cycle budget (owner, 2026-11-09, issue #1296)`.
* Validation: Passed (`git diff --check` exit `0`; Python mechanical and anchor check `PASS`).

### Local-Before-PR CI-Economy Rule and Step 5-6 Pre-Publication Flow

* Related phase or task: P02 (`P02-T01`)
* Files: `.github/agents/ama-backlog-delivery-coordinator.agent.md`
* What changed and why: Updated `## CI economy and PR backlog cap (owner rules, 2026-11-03; updated 2026-11-15)`, step 5 (`Run one RPI loop per issue`, including correction-brief ledger fields and the closing `Verify RPI use before review` block), and step 6 (`Review each candidate independently before publishing`) so WIP commits and local review-correction commits remain local in `{worktree}` until the full local RPI loop (`research`, `plan`, `implement`, `review`), any local review-correction fixes (within the single per-issue `Correction-cycle budget`), selected-tier local validation, local candidate `.copilot-tracking` diff verification (`git -C {worktree} diff --name-only {base-sha}...HEAD | grep .copilot-tracking`), and pre-publication `hve-core-all:code-review-*` exact-head review (writing coordinator review outputs to an external directory outside `{worktree}` so `{worktree}` stays clean at exact `HEAD`) all pass on a clean frozen candidate before the first `git push` and `gh pr create`; preserved D5's `"After two correction cycles"` threshold in step 6.
* Completion evidence: Diff hunks in `CI economy and PR backlog cap`, step 5, and step 6.
* Validation: Passed (`git diff --check` exit `0`; Python mechanical and anchor check `PASS`).

### Focused Mechanical Validation and HVE-Qualified Five-Boundary Static/Trace Verification

* Related phase or task: P03 (`P03-T01`)
* Files: `.copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md`, `.copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md`
* What changed and why: Executed `git diff --check` and deterministic Python verification of YAML frontmatter, relative Markdown links, internal anchor `#correction-cycle-budget-owner-2026-11-09-issue-1296`, `ord(c) <= 127` plain ASCII conformance, `*` unordered list bullets without bolded prefixes, and `#1783` diff-boundary preservation; compiled the HVE-qualified static/trace boundary evidence record below for independent `rpi-review` assessment.
* Completion evidence: Target `.github/agents/ama-backlog-delivery-coordinator.agent.md` `SHA-256: dda5f87a9438d3a1a951c7aec516b8aaefed78ca52c890dbcc0b0a1091045803` (`1047` lines) and the static/trace matrix below.
* Validation: Passed (Focused validation tier per `.github/copilot-instructions.md` and `#1294`).

### HVE-Qualified Static and Scenario-Trace Boundary Record

* Target artifact: `.github/agents/ama-backlog-delivery-coordinator.agent.md`
* Exact source identity: `SHA-256 dda5f87a9438d3a1a951c7aec516b8aaefed78ca52c890dbcc0b0a1091045803` (unstaged working-tree candidate against base `697b00c0a9e649696f18cce8dc6e51c72d02617a`)
* Execution status: Executed (Focused mechanical checks + deterministic clause/scenario static trace)
* Fidelity and executor/profile limits: `static/trace` fidelity only. Live native coordinator execution (spawning multi-session `tmux` workers, driving GitHub PR state, or issuing live issue comments) was intentionally not executed in this documentation-only Focused-tier session; static/trace evidence verifies policy consistency and decision determinism across sections and claims no native runtime execution acceptance.

| Boundary scenario | Requirement | Canonical clause pointers in `.github/agents/ama-backlog-delivery-coordinator.agent.md` | Static/trace outcome | Verdict |
|---|---|---|---|---|
| 1. Five-total-cycle default (`C1-C5`, unified across pre-PR and post-PR review) | `#1296` AC 1; `2026-11-15` CI-economy rule | `Human blockers`, `Correction-cycle budget` (`Cycle`, `Default`, `Ledger`), `CI economy and PR backlog cap`, step 5 brief rules, step 6 | Blocking findings from pre-publication local exact-head review or post-publication PR review draw from one per-issue `C1-C5` maximum (`2026-11-09`) without extra owner approval; e.g. `2` local pre-PR fixes leave at most `3` post-PR fixes (`2 + 3 = 5`). | Pass (`static/trace`) |
| 2. Early-stop boundary (`0` cycles or `C1-C4` resolution) | `#1296` AC 1 | `Correction-cycle budget` (`Cycle`, `Default`), step 6 | Five is a cap, not a target: `0` cycles publishes immediately when initial exact-head review passes, and correction stops immediately at `C1-C4` once no blocking finding remains open; read-only diagnostics never delay early stop. | Pass (`static/trace`) |
| 3. Exhausted-limit human-blocker, no-reset, diagnostic bound, and non-waiver | `#1296` AC 2 | `Human blockers`, `Correction-cycle budget` (`Cycle`, `Ledger`, `Exhausted`, `Retained gates`), step 6 | Open blocking finding after `C5` (absent explicit dated issue-specific extension) stops correction launches, comments once with the consumed ledger, and marks `human-blocked`; counters never reset across retries/rebases/restarts; unchanged-tree diagnostics cannot modify candidate commits/files or authorize a sixth fix; all safety, privacy, accessibility, resident-consent, human-approval, validation-tier, and exact-head review gates remain active. | Pass (`static/trace`) |
| 4. Dated `2026-11-09` five-additional-cycle grant (`E1-E5` beyond historical exhaustion) | `#1296` AC 4 | `Human blockers`, `Correction-cycle budget` (`Ledger`, `Exhausted`, `Dated grant`), step 5, step 6 | Records the `2026-11-09` `"add 5 additional cycles to exhausted issues"` grant (`E1-E5`) for issues already exhausted when granted (citing `#1288` preserving `C1-C8` and resuming under `E1-E5` per `#1288#issuecomment-6735179415`); stops early if resolved at `E1-E4`, returns to `human-blocked` if open after `E5`, and denies automatic `E1-E5` inheritance to later `C1-C5` exhaustions. | Pass (`static/trace`) |
| 5. Owner decision D5 (`2026-11-01`) two-cycle non-blocking Copilot follow-up boundary + local-before-PR publication gate | `#1296` AC 3; `2026-11-15` CI-economy rule | `Human blockers`, `Correction-cycle budget` (`Retained gates`), `CI economy and PR backlog cap`, step 5 (`Verify RPI use before review`), step 6 | After `C2`, new non-blocking Copilot threads become follow-up issues and do not hold publication/PR, whereas blocking safety, privacy, accessibility, or functional defects still block and consume `C3-C5`/`E1-E5`; WIP commits, local RPI (`git -C {worktree} diff ...`), local correction fixes, selected-tier validation, and external-output pre-publication `code-review-*` complete before first `git push` and `gh pr create`. | Pass (`static/trace`) |

## Implementation-Time Plan and Detail Updates

None; implementation executed `P01-T01`, `P02-T01`, and `P03-T01` directly as finalized after critique disposition.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|---|---|---|---|
| `git diff --check` | `.github/agents/ama-backlog-delivery-coordinator.agent.md` and `.copilot-tracking/` | Passed | Exited `0` with zero whitespace or conflict-marker issues |
| Focused frontmatter, relative-link/anchor, ASCII, Markdown style, and `#1783` diff-hunk boundary check | `.github/agents/ama-backlog-delivery-coordinator.agent.md` | Passed | `ALL_MECHANICAL_CHECKS=PASS`; YAML frontmatter (`name`, `description`) valid; `#correction-cycle-budget-owner-2026-11-09-issue-1296` and `../../src/README.md#local-rpi-gate` resolve; 100% `ord(c) <= 127` ASCII; zero `-` or bolded-prefix bullets; `git diff` touches only the 6 planned hunks and leaves `#1783` operational rules verbatim |
| HVE-qualified five-boundary static/trace verification | `#1296` AC 1-5 and `2026-11-15` pre-PR/post-PR budget unity | Passed | All 5 boundaries pass at `static/trace` fidelity (`SHA-256: dda5f87a9438d3a1a951c7aec516b8aaefed78ca52c890dbcc0b0a1091045803`), explicitly qualified against unexecuted live `tmux` coordinator runs |
| Complete heavy local RPI gate (`tools/rpi-checks.py --all`) | Repository source/SQL/browser/container suites | Skipped | Documentation/agent-instruction-only edit classified under Focused validation tier per `.github/copilot-instructions.md` (D4 / `#1294`); touches zero `src/`, `infra/`, workflow, dependency, SQL, or deployment paths |

## Pre-Review Reconciliation

* Plan markers and phase details: current (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` checked `[x]` in `.copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md` and aligned with phase details)
* Completed-work evidence and handoff prose: current (descriptive completed-work entries, diff verification, and HVE-qualified five-boundary trace matrix recorded)
* Validation, blockers, remaining work, and follow-up items: current (Focused checks passed, zero blockers, zero remaining active plan markers, follow-up mirrored from plan)
* Review readiness: Ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none within `rpi-implement` (`P01`-`P03` complete; `rpi-review` and post-review local commit execute next in the automatic RPI loop).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md, `## Follow-Up Items`
* Observe PR-push frequency across subsequent coordinator delivery waves under the `2026-11-15` local-before-PR CI-economy rule (outside immediate documentation scope; owned by future coordinator wave telemetry).

## Return-to-Caller State

* Implementation execution status: Complete (Full plan: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Declared scope and markers: Full plan (`P01`, `P02`, `P03`); completed: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining active-plan markers: none
* Validation coverage: Focused tier passed (`git diff --check`, YAML frontmatter, relative links + anchors, `ord(c) <= 127` ASCII, `*` list style, `#1783` diff-hunk non-regression, and HVE-qualified `static/trace` five-boundary verification)
* Blockers: none
* Current plan and detail updates: none during implementation
* Planning and critique state: Ready (`PC-001` through `PC-004` resolved in plan `## Critique Disposition`)
* Follow-up items: Observe PR-push frequency across subsequent coordinator delivery waves under the `2026-11-15` local-before-PR CI-economy rule
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
