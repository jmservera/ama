<!-- markdownlint-disable-file -->
# RPI Phase Details: Align Coordinator Correction-Cycle Default and Local-Before-PR Publication Rule (Issue #1296)

## Metadata

* Task ID: issue-1296
* Task slug: delivery-1296-correction-cycles
* Related plan: .copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, .github/copilot-instructions.md

## Phase Index

| Phase ID | Name                                                                               | Status | Detail sections |
|----------|------------------------------------------------------------------------------------|--------|-----------------|
| P01      | Reconcile correction-cycle budget, D5 two-cycle threshold, and dated E1-E5 grant   | ready  | P01, P01-T01    |
| P02      | Codify 2026-11-15 local-before-PR CI-economy rule and step 5-6 publication flow    | ready  | P02, P02-T01    |
| P03      | Run focused mechanical validation and stage clean local commit readiness           | ready  | P03, P03-T01    |

## Test and Validation Ownership Lock

* Canonical target modified: `.github/agents/ama-backlog-delivery-coordinator.agent.md`
* Generated targets modified: `none`
* Test file removals: `none`
* Maximum new test files added: `0` (instruction-only change under `Focused` validation tier)
* Semantic vs regression coverage:
  * Semantic coverage: Five-boundary behavioral trace matrix verified against exact section/rule text in `rpi-review` (`five-total-cycle` allowance C1-C5, `early-stop` at C0-C4, `exhausted-limit` human blocker after C5, `authorized-extra-cycle` `E1-E5` from `2026-11-09` grant on `#1288` after historical `C8` with exhaustion after `E5`, and `D5 two-cycle non-blocking` follow-up boundary vs blocking safety/privacy/accessibility defects, plus unified pre-PR + post-PR cycle accounting under the `2026-11-15` CI-economy rule), explicitly qualified as static/trace verification rather than native live `tmux` execution.
  * Regression/mechanical coverage: `git diff --check`, YAML frontmatter parse (`name`, `description`), relative Markdown link and same-file heading-anchor verification, plain-ASCII (`ord(c) <= 127`) and repository Markdown style verification (`*` bullets, no em/en dashes, no new bolded-prefix list items), and diff verification that `#1783` (`ad005cd5f`) unrelated operational controls remain untouched.

<!-- rpi:phase id=P01 -->
## P01: Reconcile correction-cycle budget, D5 two-cycle threshold, and dated E1-E5 grant

### Context

Research findings `C1`, `C4`, `C5`, `W1`, and `W2` show that commit `ad005cd5f` (`#1783`) partially updated `Human blockers` and step 6 to mention five total review-correction cycles, but introduced three discrepancies against Issue `#1296`: it replaced D5's `"after two correction cycles"` with `"after the correction cycles"`, misdated the five-cycle default as `2026-11-11` instead of `2026-11-09`, and added an unqualified `"authorizing at least three scoped diagnostic RPI cycles"` parenthetical while omitting early stop, no-reset, gate non-waiver, and the dated `2026-11-09` `E1-E5` grant (`#1288#issuecomment-6735179415`).

### Intent

Add a canonical single-source `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` section immediately after `## Human blockers` and update the `Human blockers` bullet to reference it cleanly while restoring D5's exact two-cycle wording.

### Boundaries

* Included: `## Human blockers` blocking-finding bullet and the new `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` section in `.github/agents/ama-backlog-delivery-coordinator.agent.md`.
* Excluded: Other `Human blockers` bullets, `Liveness and stop decision`, `Recurring schedules`, and `Cleanup contract`.

### Likely Targets

* `.github/agents/ama-backlog-delivery-coordinator.agent.md`: Update `Human blockers` blocking-review bullet and insert `## Correction-cycle budget (owner, 2026-11-09, issue #1296)`.

### Dependencies

* None.

### Validation Expectations

* Heading slug `#correction-cycle-budget-owner-2026-11-09-issue-1296` matches internal links; all text uses plain ASCII (`E1-E5` / `E1 to E5`), `*` bullets, and unbolded prefixes.

### Completion Evidence

* Updated `Human blockers` and `Correction-cycle budget` text present in `.github/agents/ama-backlog-delivery-coordinator.agent.md` covering every clause of `#1296` AC 1, AC 2, AC 3, and AC 4.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add canonical Correction-cycle budget section and reconcile Human blockers

#### Context

 `.github/agents/ama-backlog-delivery-coordinator.agent.md` already uses single-source sections for cross-cutting rules (`Admission rule (single source; other sections cross-reference it)` and `Receipt refresh rule (single source)`). Placing all cycle-accounting rules in `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` keeps `Human blockers`, step 5, and step 6 concise and consistent.

#### Intent

Specify in `Human blockers` and `## Correction-cycle budget (owner, 2026-11-09, issue #1296)`:
1. `Human blockers` bullet: a blocking review finding (including a safety, privacy or accessibility defect) still open after the issue's correction-cycle budget is exhausted (up to five total review-correction cycles by default, or after an explicit dated issue-specific owner extension granted beyond an exhausted budget; see `[Correction-cycle budget](#correction-cycle-budget-owner-2026-11-09-issue-1296)`), a check that keeps failing for a reason the loop cannot fix, or a conflict whose intent cannot be reconciled. Non-blocking Copilot threads raised after two correction cycles are not blockers; they become follow-up issues (step 6, owner decision D5, `2026-11-01`, separate from the blocking-correction budget).
2. `Correction-cycle budget` single-source bullets (unbolded `* Label:` style):
   * `Cycle:` defines one review-correction cycle as a correction brief launched to the issue's loop after a recorded blocking finding from pre-publication independent exact-head review or post-publication PR review, producing a frozen local correction with its own dated research, plan, changes, and review artifacts. Pre-publication local review-correction cycles and post-publication PR review-correction cycles count against the same per-issue budget. A launch/tool failure that produces no worker commits or artifacts consumes nothing (retry once under step 5); first-pass critique/review inside a single RPI run is not a cycle; the one-time step 5 recovery for missing RPI artifacts is process recovery only and cannot modify defect scope or bypass the budget; bounded read-only or unchanged-tree diagnostics (confirming whether a failure is an infrastructure or fixture environment issue without modifying the candidate commit or tracked worktree files) never delay early stop, do not reset or enlarge the source-correction cap, and never authorize a sixth file-modifying fix.
   * `Default:` up to five total review-correction cycles per issue (`owner, 2026-11-09`, superseding the former two-cycle and four-cycle limits). Five is a maximum, not a target: a blocking finding can receive correction through cycle five (`C1` to `C5`) without further owner approval, and correction stops earlier as soon as no blocking finding remains (`0` cycles is valid when the initial candidate passes).
   * `Ledger:` record per issue the consumed count, each cycle's blocking finding and outcome, any dated extension authority with its URL, and the remaining budget in session SQL, the blocker ledger, and issue comments; state these before and inside every correction brief.
   * `No reset:` used cycles stay consumed. The five-cycle default never resets, restarts, or adds to already-consumed cycles and is never interpreted as additional authorization beyond five total cycles.
   * `Exhaustion:` an unresolved blocking finding after five total cycles (or after an authorized finite extension is spent) becomes a human blocker for that issue and its dependants. Launch no further source correction; comment once on the issue with the remaining finding, who can decide, and what it unblocks, update the blocker ledger, and set the board status. Only a new explicit, dated, issue-specific owner authorization adds cycles.
   * `Dated extension grant (owner, 2026-11-09, "add 5 additional cycles to exhausted issues"):` grants up to five new correction cycles, numbered `E1` to `E5` (`E1-E5`), solely to issues that were already exhausted when the grant was made on `2026-11-09` (for example Quality lane `#1288` resuming from its completed `C8` fixture recovery with extension `E1-E5`, recorded at `<https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415>`). Previous consumed cycles remain historical and are not erased or recounted against `E1-E5`; correction still stops early once resolved; exhausting `E5` with an open blocking finding becomes a human blocker requiring new owner authority; and the grant never resets counters or grants endless or automatic extensions to issues that subsequently exhaust the standing five-cycle default.
   * `No bypass and retained gates:` no blocking finding (including High-severity, correctness, safety, privacy, or accessibility defects or failing required checks), resident-consent boundary, named human/legal/compliance approval, validation-tier requirement, original adverse RPI/gate evidence, or independent exact-head review gate is waived during or at exhaustion of correction cycles. Every correction commit invalidates prior validation and independent exact-head assessment on the superseded HEAD. Owner decision D5 (`2026-11-01`, step 6) applies solely to new non-blocking Copilot threads after two correction cycles and never downgrades a blocking defect.

#### Boundaries

* Included: `Human blockers` bullet and `Correction-cycle budget` section.
* Excluded: Step 5/6 and `CI economy` edits (handled in `P02-T01`).

#### Likely Targets

* `.github/agents/ama-backlog-delivery-coordinator.agent.md`

#### Dependencies

* None.

#### Validation Expectations

* Exact match against `#1296` AC 1, AC 2, AC 3, and AC 4; plain ASCII and `*` list formatting.

#### Completion Evidence

* Clean diff in `.github/agents/ama-backlog-delivery-coordinator.agent.md` with working internal anchor `#correction-cycle-budget-owner-2026-11-09-issue-1296`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Codify 2026-11-15 local-before-PR CI-economy rule and step 5-6 publication flow

### Context

Research findings `C2`, `C3`, and `C5` show that while step 5 forbids workers from pushing, `CI economy and PR backlog cap` does not yet state the `2026-11-15` local-before-PR rule, and step 6 phrases `hve-core-all:code-review-*` under `"For the published PR"` while carrying `ad005cd5f`'s drifted D5/date text.

### Intent

Update `## CI economy and PR backlog cap`, step 5, and step 6 so issue loops keep WIP commits local in their worktree and defer `git push` and `gh pr create` (or PR updates) until the full local RPI loop (`research`, `plan`, `implement`, `review`), any local review-correction fixes (within the single per-issue five-cycle budget), selected-tier local validation, and pre-publication independent exact-head review complete on a clean frozen candidate, while preserving D5 (`2026-11-01`) after two correction cycles.

### Boundaries

* Included: `## CI economy and PR backlog cap` heading/bullets, step 5 brief/local-candidate rules, and step 6 independent review and correction-cycle prose in `.github/agents/ama-backlog-delivery-coordinator.agent.md`.
* Excluded: Launcher script (`gemini-4-carbon`, `/mnt/tmp`, `< /dev/null`), `src-ci.yml` parity commands, step 7 automerge gate, and step 8 rebase rules.

### Likely Targets

* `.github/agents/ama-backlog-delivery-coordinator.agent.md`

### Dependencies

* P01 (defines `#correction-cycle-budget-owner-2026-11-09-issue-1296` linked from steps 5-6 and `CI economy`).

### Validation Expectations

* Explicit statement in `CI economy and PR backlog cap`, step 5, and step 6 that WIP commits stay local in the worktree and no push or PR creation occurs until local RPI (`research`, `plan`, `implement`, `review`), any local review-correction fixes, and selected-tier local validation complete on a clean frozen candidate; D5 two-cycle threshold restored in step 6.

### Completion Evidence

* Clean diff in `CI economy and PR backlog cap`, step 5, and step 6 preserving all `#1783` controls.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update CI economy and PR backlog cap, step 5, and step 6

#### Context

Every premature branch push or early PR creation triggers `Source projects CI` (and `Capstone Rubric Scorer` when targeting `main`). Completing RPI, local independent exact-head review, any local review-correction cycles, and selected-tier local validation in the worktree before pushing/opening the PR eliminates avoidable hosted Actions runs on WIP commits.

#### Intent

Apply four coordinated edits in `.github/agents/ama-backlog-delivery-coordinator.agent.md`:
1. In `## CI economy and PR backlog cap (owner rules, 2026-11-03; updated 2026-11-15)`:
   * Clarify on the `code-review-*` bullet that the worker loop commits its own `rpi-review` artifact under `{worktree}/.copilot-tracking/reviews/` while coordinator-dispatched `code-review-*` pre-publication verdicts and precomputed diffs write to an external coordinator review directory outside `{worktree}` so `{worktree}` stays clean at exact `HEAD` (`PC-002`).
   * Add a dedicated bullet stating that issue loops keep WIP commits local in their worktree and do not push or open a pull request until the local RPI loop (`research`, `plan`, `implement`, `review`), any local review-correction fixes (counted within the issue's `[Correction-cycle budget](#correction-cycle-budget-owner-2026-11-09-issue-1296)`), selected-tier local validation, and pre-publication independent exact-head review in step 6 have completed on a clean frozen candidate, avoiding repeated GitHub Actions runs on WIP pushes (`owner rule, 2026-11-15`).
2. In step 5 (`Run one RPI loop per issue`, brief and publication rules):
   * Specify that a correction brief records the issue's consumed cycles, any dated extension authority (`E1-E5`), remaining budget, blocking finding, selected validation tier, and separate independent exact-head review requirement per `[Correction-cycle budget](#correction-cycle-budget-owner-2026-11-09-issue-1296)`.
   * Reinforce in the brief/publication paragraph that the issue loop keeps all WIP commits and any local review-correction fixes local in its worktree and never pushes or opens/updates a PR: `git push` and `gh pr create` wait until the full local RPI loop (`research`, `plan`, `implement`, `review`), any local review-correction fixes, selected-tier local validation, and step 6 independent exact-head review finish on a clean frozen candidate.
3. In step 5's closing `Verify RPI use before review` block:
   * Update the pre-review artifact check so pre-publication verification inspects the local worktree candidate diff against its target base (`git -C {worktree} diff --name-only {base-sha}...HEAD | grep .copilot-tracking`, using `gh pr diff {n} --name-only | grep .copilot-tracking` once a PR is open and in step 7), and change `"A PR without them"` to `"A candidate or open PR without them"` (`PC-001`).
4. In step 6 (`Review each candidate independently before publishing`):
   * Clarify that before pushing or opening a PR, the coordinator runs independent exact-head assessment (including `hve-core-all:code-review-*` against a precomputed diff of the frozen local candidate vs its target base written to an external coordinator directory outside `{worktree}`, without rerunning or replacing the loop's original RPI Review or dirtying `{worktree}`) while WIP and correction commits remain local in the worktree (`PC-002`). If pre-publication review finds a blocking issue, route local review-correction fixes in the worktree and rerun selected-tier local validation and exact-head review before the first push and `gh pr create`.
   * Once published, also review the open PRs of a wave together for contradictions and handle any post-publication review findings as local worktree commits pushed only after refreshed selected-tier local validation and exact-head assessment, sharing the same single per-issue `[Correction-cycle budget](#correction-cycle-budget-owner-2026-11-09-issue-1296)` (up to five total review-correction cycles per issue by default, `2026-11-09`, stopping earlier once resolved, preserving spent history and any dated finite extension such as `E1-E5`, and becoming a human blocker when exhausted with a blocking finding still open).
   * Restore exact D5 wording: `"After two correction cycles, new non-blocking Copilot threads become follow-up issues and do not hold the PR; a blocking safety, privacy or accessibility defect (or any other blocking finding) still stops publication and the PR (owner decision D5, 2026-11-01, separate from the five-cycle blocking-correction default, 2026-11-09)."`

#### Boundaries

* Included: `CI economy and PR backlog cap`, step 5, and step 6 in `.github/agents/ama-backlog-delivery-coordinator.agent.md`.
* Excluded: Steps 1-4 and steps 7-10.

#### Likely Targets

* `.github/agents/ama-backlog-delivery-coordinator.agent.md`

#### Dependencies

* P01-T01.

#### Validation Expectations

* All cross-references resolve; no duplicate or conflicting cycle numbers remain anywhere in `.github/agents/ama-backlog-delivery-coordinator.agent.md`.

#### Completion Evidence

* Updated `CI economy`, step 5, and step 6 sections in `.github/agents/ama-backlog-delivery-coordinator.agent.md`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Run focused mechanical validation and stage clean local commit readiness

### Context

Under `.github/copilot-instructions.md` (`C7`, `C8`) and Issue `#1296` (`W1`), this instruction-only edit takes the `Focused` validation tier (`git diff --check` plus mechanical frontmatter, link/anchor, and Markdown/ASCII checks).

### Intent

Prove mechanical cleanliness and zero regressions on `.github/agents/ama-backlog-delivery-coordinator.agent.md` and reconcile all RPI tracking records prior to independent `rpi-review` and local git commit.

### Boundaries

* Included: Read-only mechanical validation commands on `.github/agents/ama-backlog-delivery-coordinator.agent.md` and `.copilot-tracking/` artifacts; reconciliation of plan, phase-details, changes, and state files.
* Excluded: Heavy full-gate runner (`tools/rpi-checks.py --all`) and remote git push.

### Likely Targets

* `.github/agents/ama-backlog-delivery-coordinator.agent.md` (read-only verification)
* `.copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md`
* `.copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md`
* `.copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md`

### Dependencies

* P01, P02.

### Validation Expectations

* `git diff --check` returns exit code `0` with empty output.
* Python mechanical check confirms valid YAML frontmatter, resolved relative file links and same-file `#anchor` fragments, `ord(c) <= 127` ASCII-only content, `*` list markers, zero em/en dashes, zero new bolded-prefix list items, and intact `#1783` lines.

### Completion Evidence

* Recorded command outputs and exit codes in `.copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute focused validation checks, record five-boundary HVE static/trace matrix, and reconcile tracking records

#### Context

Ensures all implementation gates in `rpi-implement` pass cleanly and supplies HVE-qualified source identity and five-boundary static/trace evidence in `changes.md` (`PC-004`) before transitioning to the single `rpi-review` pass and final unpushed local commit.

#### Intent

Run `git diff --check` and a deterministic Python validation snippet verifying frontmatter, links/anchors, ASCII/Markdown style, and `#1783` preservation; record in `.copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md` both the mechanical check results and the HVE-qualified five-boundary static/trace verification table (including target file SHA-256 source identity, post-edit `path:line` citations, execution status, verdict, `static/trace` fidelity, and explicit non-execution qualification for live `tmux` coordinator runs); then tick completed `P01`-`P03` markers and reconcile the changes record so post-`rpi-review` closeout commits cleanly with repository-local `gh api user` `{id}+{login}@users.noreply.github.com` and the Copilot trailer without pushing.

#### Boundaries

* Included: Local command verification and tracking-artifact reconciliation.
* Excluded: Remote push or PR creation.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md`
* `.copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.md`
* `.copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-phase-details.md`

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* Exit code `0` across all focused checks.

#### Completion Evidence

* Reconciled plan markers (`[x]`), phase details statuses (`completed`), and complete changes record.

#### Unresolved Items

* None.
