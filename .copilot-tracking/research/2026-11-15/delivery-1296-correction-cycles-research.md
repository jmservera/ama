<!-- markdownlint-disable-file -->

# Task Research: delivery-1296-correction-cycles

| Field              | Value                                                                                  |
|--------------------|----------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                             |
| Researcher / agent | rpi-research (via RPI Agent)                                                           |
| Status             | Complete                                                                               |
| Artifact path      | .copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md      |

## Research Brief

* What to research: Every place in `.github/agents/ama-backlog-delivery-coordinator.agent.md` and adjacent instruction/governance files touching review-correction cycle limits, early stop on resolution, exhausted-cycle human blockers, the owner's dated 2026-11-09 five-additional-cycle grant (`E1-E5` for exhausted issues such as `#1288` resuming from `C8`), owner decision D5 (`2026-11-01` two-cycle non-blocking Copilot follow-up boundary), and the owner's `2026-11-15` CI-economy rule deferring push/PR creation until the local RPI loop, local review-correction fixes, and selected-tier local validation finish on a clean frozen candidate.
* Why it matters: Reconciles residual or drifted correction-cycle dates/wording, prevents ambiguous counter resets or endless extensions, preserves safety/privacy/accessibility/consent/tier/exact-head gates and D5, and codifies local-before-PR publication to conserve hosted GitHub Actions capacity.
* Audience or intended use: RPI planning, surgical edits to `.github/agents/ama-backlog-delivery-coordinator.agent.md`, boundary verification in `rpi-review`, and parent integration on `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Scope: `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `.github/copilot-instructions.md` (read-only alignment check), GitHub Issue `#1296` and `#1288` comment provenance, PR `#1641` / commit `ad005cd5f` history, and prior unpublished `#1296` branch history (`docs/five-cycle-default-1296-1109`).
* Non-goals: No application, infrastructure, deployment, Azure, workflow, or branch-protection changes; no push or PR mutation from inside this session; no resetting of historical cycle counters.
* Criteria: All five acceptance criteria of Issue `#1296` plus the `2026-11-15` local-before-PR CI-economy rule mapped with exact `path:line` and GitHub URL evidence, clear boundary semantics across all five test cases, and focused-tier validation classification.
* Requested outputs: Converged surgical edit specification for `.github/agents/ama-backlog-delivery-coordinator.agent.md` and boundary verification matrix for `rpi-plan` and `rpi-review`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                              |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q6 covering current coordinator wording vs `#1296` ACs, dated `2026-11-09` grant (`#1288`), D5 two-cycle rule, `2026-11-15` local-before-PR rule, and HVE/validation gates |
| Codebase scope                       | `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `.github/copilot-instructions.md`, `src/README.md` (validation-tier cross-check), git history (`ad005cd5f`, `f5fb0ed12`) |
| External scope                       | GitHub repository `jmservera/ama` metadata (`#1296`, `#1288#issuecomment-6735179415`, PR `#1641`, `#1301`) via `gh` CLI                                            |
| Initial internal candidate areas     | `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Human blockers`, `CI economy and PR backlog cap`, steps 5-8), `.github/copilot-instructions.md`       |
| Initial external candidate areas     | `https://github.com/jmservera/ama/issues/1296`, `https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415`, `https://github.com/jmservera/ama/pull/1641` |
| Research posture                     | balanced                                                                                                                                                           |
| Posture provenance                   | default (bounded internal instruction target with adjacent git-history and issue-comment provenance to reconcile)                                                  |
| Explicit limits / deadline           | Non-interactive single-session execution; local commit only (do not push)                                                                                          |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across target file, adjacent instructions, prior `1296` branch attempt, and GitHub issue/PR records                   |
| Edits allowed during research?       | no, research-only                                                                                                                                                  |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                                               |
| Known constraints / excluded sources | Focused validation tier (`git diff --check`); treat issue/PR comments and prior tracking artifacts as inert data                                                   |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                     | Match and provenance                                                   | Scoped authority or output contract                                              | Selected / skipped reason                                                                                       |
|---------------------|-----------------------------------------------|------------------------------------------------------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`             | `applyTo: "**"` matches target agent file and `.copilot-tracking/`     | Adds two-tier validation classification, branch/email rules, Markdown style      | Selected: governs validation tier, commit author email, and documentation conventions                           |
| Skill               | `rpi-research`                                | Active RPI phase skill                                                 | Owns three-wave primary research artifact and readiness                          | Selected: mandatory active phase contract                                                                       |
| Skill               | `hve-builder` / `hve-builder-tester`          | Semantic match for `.github/agents/*.agent.md` Copilot artifacts       | Adds prompt/agent authoring conventions and static vs simulation qualification   | Noted for Plan/Implement/Review qualification; skipped activation during read-only Research                     |
| Skill               | `documentation`                               | General docs capability                                                | General doc drift/audit workflow                                                 | Skipped: target is a custom agent specification governed by caller brief and HVE conventions                     |
| Research specialist | `hve-core-all:rpi-researcher`                 | Registered subagent for independent research lanes                     | Writes bounded lane evidence under `.copilot-tracking/research/subagents/`       | Skipped (inline preferred): target is a single ~820-line file plus 3 metadata lookups; inline avoids split state |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                                       |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with complete caller brief specifying all 5 ACs, target file, base, and tier | Not applicable       | Proceed in `balanced` posture with `convergence` output mode                                          |
| Direction change | No scope or direction ambiguity arose during Cycle 1                                                  | Not applicable       | Keep active brief and non-goals unchanged                                                             |
| Convergence      | All 6 research questions answered with primary file, git-commit, and GitHub issue-comment evidence    | Not applicable       | Stop after Cycle 1 with Planning Readiness `Ready`; defer live native coordinator run outside scope    |

## Scope and Success Criteria

* Scope: Reconcile `.github/agents/ama-backlog-delivery-coordinator.agent.md` with `#1296` AC 1-5 and the `2026-11-15` local-before-PR CI-economy rule without altering application code, workflows, or repository protections.
* Assumptions:
  * Commit `ad005cd5f` (`#1783`) partially updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` after `#1296` was filed, introducing partial `2026-11-11` five-cycle text that must be checked line-by-line against `#1296`'s exact `2026-11-09` default, early-stop wording, `E1-E5` grant rules, D5 two-cycle boundary, and `2026-11-15` local-before-PR rule.
  * The checked-out worktree branch `docs/1296-correction-cycles-1125` (currently at `697b00c0a`, matching `origin/feat/demo-164-chat-grounding-provenance-0900`) is the active worktree branch created by the caller and should be reused in place without branch deletion.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and a converged recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Reconcile `Human blockers` and step 6 `Review each candidate independently before publishing` with the `2026-11-09` default of up to five total review-correction cycles per issue, explicit early-stop when resolved, human blocker after five total cycles absent issue-specific owner authorization, no counter reset, and non-waiver of gates (`#1296` AC 1 & AC 2).
  * Record the dated `2026-11-09` grant (`"add 5 additional cycles to exhausted issues"`, e.g. Quality lane `#1288` resuming from `C8` with extension `E1-E5` per `https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415`) with historical cycle preservation and non-renewal (`#1296` AC 4).
  * Preserve owner decision D5 (`2026-11-01`): new non-blocking Copilot threads raised after two correction cycles become follow-up issues and do not hold the PR, whereas blocking safety, privacy, or accessibility defects still stop the PR (`#1296` AC 3).
  * Codify in `## CI economy and PR backlog cap` and steps 5-6 the owner's `2026-11-15` CI-economy rule keeping WIP commits local in the worktree and deferring push/PR creation until local RPI (`research`, `plan`, `implement`, `review`), any local review-correction fixes, and selected-tier local validation complete on a clean frozen candidate.
  * Verify all five boundaries in the RPI review artifact with explicit static/simulation vs native execution qualification (`#1296` AC 4 & AC 5).
* Inferred research questions:
  * Did commit `ad005cd5f` (`#1783`) inadvertently alter D5's "after two correction cycles" wording to "after the correction cycles" / "After the allowed correction cycles", and did it misdate the five-cycle default as `2026-11-11` instead of `2026-11-09` or inject unrequested "at least three scoped diagnostic RPI cycles" language that interacts with `#1296`?
  * What did the earlier `2026-11-09` candidate (`f5fb0ed12` on `docs/five-cycle-default-1296-1109`) change, and what caused the 3 mismatches / 1 conditional in its High-profile simulation?
* Caller constraints and non-goals: Research-only during this phase; focused validation (`git diff --check`) during Implement/Review; commit locally with Copilot trailer; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                                              | Source / checkpoint | Effect on active brief, evidence, or revalidation                                            |
|----------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|---------------------|----------------------------------------------------------------------------------------------|
| add                                                      | Codify `2026-11-15` CI-economy rule deferring PR creation/push until local RPI, local review-correction fixes, and validation pass | Caller brief        | Included in Q4 and target sections (`CI economy and PR backlog cap`, steps 5-6)              |
| narrow                                                   | Focused validation (`git diff --check`) for instruction-only edit; do not push from inside session                                 | Caller brief        | Constrains validation plan and forbids `git push` / `gh pr create` inside this worker run    |
| exclude                                                  | No application, deployment, Azure, or branch-protection changes                                                                    | Issue `#1296`       | Restricts implementation strictly to `.github/agents/ama-backlog-delivery-coordinator.agent.md` and `.copilot-tracking/` |

## Research Questions

|  # | Sub-question                                                                                                                                          | Type            | Priority | Status   |
|---:|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Where does `.github/agents/ama-backlog-delivery-coordinator.agent.md` currently specify review-correction cycles, early stop, and human blockers?     | depth           | H        | answered |
| Q2 | How did recent history (`#1301`, `#1783` / `ad005cd5f`, and prior `#1296` branch `f5fb0ed12`) modify correction-cycle and D5 wording?                 | depth           | H        | answered |
| Q3 | What exact provenance and rules govern the `2026-11-09` `"add 5 additional cycles to exhausted issues"` grant (`#1288#issuecomment-6735179415`)?      | straightforward | H        | answered |
| Q4 | Where and how do `CI economy and PR backlog cap` and steps 5-6 currently describe local commits, local review-correction fixes, and PR publication?   | depth           | H        | answered |
| Q5 | Does any current wording dilute D5 (`2026-11-01` two-cycle non-blocking threshold) or conflict with `#1296`'s five-cycle maximum / early-stop rule?   | depth           | H        | answered |
| Q6 | What validation-tier classification and HVE static/simulation boundary qualification are required for `#1296` AC 4 & AC 5?                            | straightforward | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: Issue `#1296` body and comments (`2026-11-09`), `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/memory.md`, `docs/reference/README.md`, and `.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-*` from `#1783`.
* Reused (verified) findings: `#1301` (`#1294`) is already merged on `main` (`9814cf6b2`) and present in `HEAD` (`697b00c0a`); `HEAD` equals `origin/feat/demo-164-chat-grounding-provenance-0900` (PR `#1641`).
* Superseded / stale: Issue `#1296`'s opening note ("The coordinator profile still contains conflicting two-cycle limits...") predates `#1783` (`ad005cd5f`), which partially edited lines 51-59 and 821-829 earlier on `2026-11-15` while unintentionally dropping D5's explicit two-cycle threshold, misdating the five-cycle default as `2026-11-11`, and omitting `#1296` AC 1/2/4 details and the `2026-11-15` local-before-PR rule.

## Research Cycle Log

### Cycle 1

* Active direction controls: `add` (`2026-11-15` local-before-PR CI-economy rule), `narrow` (focused validation `git diff --check`; no push), `exclude` (no app/Azure/workflow/protection edits)
* Active research posture and completion basis: `balanced`; scope coverage across target file, adjacent `.github/` files, git commit history, and GitHub issue/PR records with adequate primary evidence
* Explicit limits or deadline effect: Inline single-session execution; no external web search required because all authoritative records live in local git history and `jmservera/ama` GitHub metadata

#### Wave 1: Wider

* Plan and independent lanes: Sweep `.github/` for all references to review-correction cycles, `D5`, `exhausted`, `1288`, `CI economy`, and PR publication boundaries; inspect git history of `.github/agents/ama-backlog-delivery-coordinator.agent.md` and fetch GitHub metadata for `#1296`, `#1288#issuecomment-6735179415`, and PR `#1641`.
* Worker evidence relationships or inline fallback: Inline investigation (single target file plus 3 metadata queries) mapped Q1-Q4 to `.github/agents/ama-backlog-delivery-coordinator.agent.md` lines 51-59, 372-404, 600-794, and 795-830 (`C1`-`C6`) and GitHub records (`W1`-`W3`).
* Reflection: Confirmed `#1301` (`9814cf6b2`) is already in ancestry, PR `#1641` is open on `feat/demo-164-chat-grounding-provenance-0900` (`W3`), and commit `ad005cd5f` (`#1783`) introduced partial five-cycle wording that altered D5 and misdated the `2026-11-09` default. Prioritized line-by-line diff inspection of `ad005cd5f` and the `2026-11-09` unpublished `#1296` candidate (`52e44a70c` / `f5fb0ed12`) for Wave 2.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Q2, Q3, Q5, and Q6 -- inspect the exact `Correction-cycle budget` structure from `52e44a70c`, the simulation report from `f5fb0ed12`, the exact wording of `#1288#issuecomment-6735179415`, and the mechanical style checks from `#1783` (`coordinator-instructions-validation-1.md`).
* Plan and independent lanes: Compare `9814cf6b2..52e44a70c` and `ad005cd5f` diffs on `.github/agents/ama-backlog-delivery-coordinator.agent.md`, read `issue-1296-five-cycle-default-behavior-report-5.md` from `f5fb0ed12`, and check `.github/copilot-instructions.md` validation-tier and Markdown style rules (`C7`, `C8`).
* Worker evidence relationships or inline fallback: Inline inspection confirmed:
  * `W2` (`#1288#issuecomment-6735179415`, `2026-11-09T08:03:44Z`) grants up to five additional scoped correction cycles to currently exhausted issues, keeping `#1288`'s `C7` exhaustion and `C8` fixture-validation recovery historical, counting newly authorized cycles (`E1-E5`) explicitly from the frozen candidate, stopping earlier when resolved, and waiving no review, SQL/browser validation, consent, human quality, release, cost, or live-AI/Azure gates.
  * `52e44a70c` used a dedicated single-source section `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` referenced from `Human blockers`, step 5, and step 6, and `f5fb0ed12` confirmed zero design/source defects in that structure while highlighting the importance of explicit blocker/board actions, exact artifact directories in briefs, and plain ASCII style (`ord(c) <= 127`, `*` bullets, no bolded-prefix list items, ASCII `E1-E5` / `E1 to E5` rather than Unicode en-dashes).
* Reflection: Need Contrarian Wave 3 to test whether `ad005cd5f`'s diagnostic-cycle parenthetical or pre-PR local correction loops create loopholes in the five-total-cycle cap or D5.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries:
  1. Challenge whether retaining `ad005cd5f`'s parenthetical `"and authorizing at least three scoped diagnostic RPI cycles with validation before stopping solely because of the cycle limit"` could allow an agent to run 3 extra source-modifying cycles after cycle 5 (total 8) or refuse early stop before cycle 3.
  2. Challenge whether moving independent exact-head review and review-correction fixes BEFORE `git push` / `gh pr create` (`2026-11-15` CI-economy rule) creates a split-counter loophole (e.g., 5 local pre-PR cycles + 5 post-PR cycles = 10 cycles).
  3. Challenge whether scattering rules across `Human blockers`, `CI economy`, step 5, and step 6 without a single-source budget definition causes drift.
* Plan and independent lanes: Cross-check `#1783` authoring notes (`.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-author-1.md`), `#1288` comment history (unchanged-source diagnostics vs productive corrections), and step 5/6 publication flow in `.github/agents/ama-backlog-delivery-coordinator.agent.md`.
* Worker evidence relationships or inline fallback: Inline contrarian test established three critical safeguards:
  1. `ad005cd5f`'s phrasing (`"authorizing at least three scoped diagnostic RPI cycles..."`) weakens `#1296` AC 1 & AC 2 if left unqualified, because five total review-correction cycles is a **maximum** (early stop at 0-4 is required when clean, and unresolved blocking findings after 5 total cycles become a human blocker absent explicit owner extension). Qualifying that bounded unchanged-source diagnostics do not modify product source, do not reset or enlarge the five-total productive correction cap, and never block early stop resolves the conflict cleanly.
  2. Unifying pre-publication local independent-review corrections and any post-publication PR-review corrections under **one** per-issue `Correction-cycle budget` (default up to five total cycles per issue) closes any split-counter loophole while ensuring WIP commits and local review-correction fixes finish locally before pushing/opening a PR.
  3. Centralizing the budget rules in `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` and cross-referencing it from `Human blockers`, `CI economy and PR backlog cap`, step 5, and step 6 eliminates duplicate-rule drift while keeping D5 (`2026-11-01` two-cycle non-blocking Copilot follow-up rule) explicitly separate.
* Reflection: All contrarian challenges resolved with high-confidence primary evidence; no unresolved questions remain.

#### Parent Synthesis and Disposition

| Material / claim                                                                                                              | Evidence IDs   | Parent disposition | Evidence-based rationale                                                                                              | Primary-artifact treatment                      |
|-------------------------------------------------------------------------------------------------------------------------------|----------------|--------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| Add single-source `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` covering 5-total max, early stop, ledger, no-reset, exhaustion, `E1-E5` grant (`#1288` from `C8`), no-bypass, and retained gates | `C1, C5, W1, W2` | accepted           | Directly satisfies `#1296` AC 1, AC 2, and AC 4 without duplicating prose across four sections                        | Selected recommendation & Decision D-1296-1     |
| Restore explicit `"after two correction cycles"` in `Human blockers` and step 6 for owner decision D5 (`2026-11-01`) and fix `2026-11-11` date drift to `2026-11-09` | `C1, C5, C6, W1` | accepted           | `ad005cd5f` inadvertently replaced `"after two correction cycles"` with `"after the [allowed] correction cycles"`     | Selected recommendation & Decision D-1296-2     |
| Qualify bounded unchanged-source diagnostics so they never mandate unnecessary cycles or permit source-modifying fixes past cycle 5 | `C1, C5, W1, W2` | accepted           | Prevents misreading `#1783`'s parenthetical as overriding `#1296` AC 1 early-stop or AC 2 five-cycle exhaustion       | Selected recommendation & Decision D-1296-3     |
| Codify `2026-11-15` local-before-PR CI-economy rule in `CI economy and PR backlog cap`, step 5, and step 6, counting pre-PR and post-PR review-correction cycles against the single per-issue five-cycle budget | `C2, C3, C4, C5` | accepted           | Satisfies caller requirement 4 (`2026-11-15` rule) while closing any pre-PR + post-PR double-budget loophole          | Selected recommendation & Decision D-1296-4     |
| Run native live multi-worktree `tmux` coordinator execution during this documentation-only RPI session                        | `C5, C7, W1`     | rejected           | Unsafe and unauthorized in shared environment; `#1296` AC 4 explicitly accepts qualified static/simulation testing    | Recorded as boundary qualification in Plan/Review |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Balanced-posture scope coverage complete; every sub-question `Q1`-`Q6` is answered with verified `path:line` and GitHub URL provenance, and contrarian challenges were resolved without uncovering missing external sources.
* Revised brief or revalidation required: none
* Readiness effect: `Ready` for `rpi-plan`

## Evidence Log

* Delegation: `inline: single target instruction file (.github/agents/ama-backlog-delivery-coordinator.agent.md) plus local git history and three GitHub issue/PR metadata reads; inline execution kept full line-level context cohesive`

### Codebase Evidence

| ID | Claim / finding                                                                                                                                                                                                 | Location (`path:line`)                                                    | Tool | Confidence | Notes                                                                                     |
|----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|------|------------|-------------------------------------------------------------------------------------------|
| C1 | `Human blockers` currently states five total review-correction cycles with an unqualified `"at least three scoped diagnostic RPI cycles"` parenthetical, drops `"two"` from D5 (`"after the correction cycles"`), and misdates the default as `2026-11-11` | `.github/agents/ama-backlog-delivery-coordinator.agent.md:51-59`          | view | high       | Introduced by commit `ad005cd5f` (`#1783`); omits early-stop, no-reset, and `E1-E5` grant |
| C2 | `CI economy and PR backlog cap` instructs `"Push less. Batch fixes into one push..."` and local `src-ci.yml` parity checks, but does not yet explicitly state the `2026-11-15` rule keeping WIP commits and local review-correction fixes local before PR creation | `.github/agents/ama-backlog-delivery-coordinator.agent.md:372-404`        | view | high       | Target location for requirement 4 (`2026-11-15` owner CI-economy rule)                    |
| C3 | Step 5 (`Run one RPI loop per issue`) forbids the worker to push or open/update a PR and requires returning a clean frozen local candidate after RPI and selected-tier validation, but does not yet state correction-brief budget fields or keeping local review-correction fixes unpublished before PR creation | `.github/agents/ama-backlog-delivery-coordinator.agent.md:676-727`        | view | high       | Lines 602-615 and 676-727 govern brief generation and local worker outputs                |
| C4 | Step 5 RPI artifact recovery (`lines 791-794`) sends a PR missing `.copilot-tracking/` phases/artifacts back once to produce a frozen local correction; must remain distinct from defect review-correction cycles | `.github/agents/ama-backlog-delivery-coordinator.agent.md:791-794`        | view | high       | Process-artifact recovery cannot be used to bypass the 5-cycle blocking-defect cap        |
| C5 | Step 6 (`Review each candidate independently before publishing`) frames `hve-core-all:code-review-*` under `"For the published PR"`, uses `"After the allowed correction cycles"` instead of `"After two correction cycles"` for D5, misdates the five-cycle default as `2026-11-11`, and omits early-stop, no-reset, and the `2026-11-09` `E1-E5` grant | `.github/agents/ama-backlog-delivery-coordinator.agent.md:795-830`        | view | high       | Primary reconciliation site for `#1296` AC 1-4 and `2026-11-15` local-before-PR review    |
| C6 | Commit `ad005cd5f` (`#1783`, `2026-11-15`) applied general chronicle updates (`gemini-4-carbon`, `/mnt/tmp`, adaptive schedule, `src-ci.yml` parity) that must be preserved intact while reconciling its partial five-cycle edit with `#1296` | `.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-author-1.md:10-38` | view | high | Preserves `#1783` improvements without regression                                         |
| C7 | Repository validation policy classifies documentation/instruction-only edits that do not alter workflows, gate tools, dependencies, permissions, or security controls under the `Focused` tier; mechanical checks verify YAML frontmatter, relative links, plain ASCII (`ord(c) <= 127`), `*` bullets, and `git diff --check` | `.github/copilot-instructions.md:83-105`                                  | view | high       | Cross-checked with `.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-validation-1.md:21-31` |
| C8 | Markdown style conventions require preserving target heading/table style, `*` unordered lists, fenced code block language tags, plain ASCII punctuation (no Unicode en/em dashes), and no bolded-prefix list items | `.github/copilot-instructions.md:364-376`                                 | view | high       | Use ASCII `E1-E5` or `E1 to E5` rather than Unicode en-dash in `.agent.md`                |

### External Evidence

| ID | Claim / finding                                                                                                                                                                                                 | Source (title)                                                    | URL                                                                | Retrieved  | Version/date         | Confidence |
|----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|--------------------------------------------------------------------|------------|----------------------|------------|
| W1 | Issue `#1296` defines five acceptance criteria: (1) reconcile blocking-review/correction wording with `2026-11-09` five-total-cycle default and early stop when resolved; (2) unresolved blocking finding after 5 total cycles is a human blocker absent issue-specific owner authority, no counter reset, no gate waivers; (3) preserve D5 (`2026-11-01`) two-cycle non-blocking follow-up rule; (4) test all five boundaries (qualifying simulation vs native execution) and record the dated `2026-11-09` five-additional-cycle grant (`#1288` resuming from `C8` with `E1-E5`); (5) deliver dated RPI artifacts, independent review, and focused checks after `#1301` | GitHub Issue `#1296`: `docs(delivery): align correction-cycle default with owner authorization` | https://github.com/jmservera/ama/issues/1296                       | 2026-11-15 | 2026-11-09 (OPEN)    | high       |
| W2 | Owner authorization comment on `#1288` (`2026-11-09T08:03:44Z`) grants up to five additional scoped correction cycles to currently exhausted issues, resolving `#1288`'s `C7` exhaustion while keeping `C8` fixture recovery and earlier adverse findings historical, counting explicitly from the frozen candidate, stopping earlier when resolved, and retaining independent review, SQL/browser validation, consent, human quality, release, cost, and live-AI/Azure gates | GitHub Issue `#1288` comment `6735179415` by `jmservera`          | https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415 | 2026-11-15 | 2026-11-09T08:03:44Z | high       |
| W3 | Parent integration PR `#1641` (`feat(chat): label answer origin and answer case-unblock questions from rules`) is `OPEN` on branch `feat/demo-164-chat-grounding-provenance-0900` targeting `main`, and current worktree `HEAD` (`697b00c0a`) matches `origin/feat/demo-164-chat-grounding-provenance-0900` | GitHub Pull Request `#1641`                                       | https://github.com/jmservera/ama/pull/1641                         | 2026-11-15 | 2026-11-15 (OPEN)    | high       |

### Contradictions / Conflicts

* Date and D5 threshold drift between `#1783` (`C1`, `C5`) and Issue `#1296` (`W1`, `W2`): Commit `ad005cd5f` (`#1783`) dated the five-cycle default as `2026-11-11` and rewrote D5 as `"after the [allowed] correction cycles"`, whereas primary owner authorization in Issue `#1296` (`W1`) and `#1288#issuecomment-6735179415` (`W2`) establishes `2026-11-09` as the authorization date and explicitly requires preserving D5's **two-cycle** non-blocking threshold (`2026-11-01`). Resolved by primary-source precedence (`W1`, `W2` and explicit caller brief): restore `2026-11-09` for the five-cycle default and `E1-E5` grant, and restore `"after two correction cycles"` for D5.
* Diagnostic cycles vs five-cycle maximum (`C1`, `C5` vs `W1`): `ad005cd5f` added `"authorizing at least three scoped diagnostic RPI cycles with validation before stopping solely because of the cycle limit"`; resolved by distinguishing read-only/unchanged-source diagnostics from productive source-modifying review-correction cycles so early stop (cycles 0-4) and hard exhaustion after cycle 5 (`W1` AC 1 & AC 2) hold strictly without contradiction.

## Findings Mapped to Questions and Evidence

| Question | Finding                                                                                                                                                                                                 | Evidence IDs     | Confidence | Decision or readiness implication                                                                                  |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|------------|--------------------------------------------------------------------------------------------------------------------|
| Q1       | Blocking-finding cycles and human blockers are currently mentioned in `Human blockers` (`lines 51-59`) and step 6 (`lines 821-829`), without a canonical single-source budget section or early-stop text | `C1, C5`         | high       | Add `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` after `Human blockers` and link `Human blockers`, step 5, and step 6 to it |
| Q2       | `#1301` (`9814cf6b2`) is already merged; `#1783` (`ad005cd5f`) added partial five-cycle prose with date/D5 drift while also adding `gemini-4-carbon`, `/mnt/tmp`, cadence, and `src-ci.yml` parity rules that must stay intact | `C1, C5, C6`     | high       | Reconcile only the correction-cycle, D5, and local-before-PR passages while preserving all unrelated `#1783` edits  |
| Q3       | The `2026-11-09` grant (`#1288#issuecomment-6735179415`) awards up to five new cycles (`E1-E5`) only to issues exhausted when granted (e.g., `#1288` after historical `C8`), preserves prior cycles as historical, stops early when resolved, requires new owner authority if `E5` is exhausted, and does not auto-extend issues that later exhaust the 5-cycle default | `W1, W2`         | high       | Codify exact `E1-E5` eligibility, historical accounting, non-renewal, and `#1288` provenance link in `Correction-cycle budget` |
| Q4       | `CI economy and PR backlog cap` (`lines 372-404`), step 5 (`lines 676-727`), and step 6 (`lines 795-830`) forbid workers from pushing, but step 6 still frames `code-review-*` under `"For the published PR"` rather than requiring WIP commits, local RPI, local review-correction fixes, and selected-tier validation to finish locally before opening a PR | `C2, C3, C5`     | high       | Update `CI economy and PR backlog cap` and steps 5-6 to mandate local-before-PR completion (`2026-11-15` rule) under the single per-issue cycle budget |
| Q5       | `ad005cd5f` inadvertently altered D5 from `"after two correction cycles"` to `"after the [allowed] correction cycles"`, which would delay non-blocking Copilot thread deferral from cycle 2 to cycle 5 | `C1, C5, W1`     | high       | Restore explicit `"after two correction cycles"` in both `Human blockers` and step 6 while keeping blocking safety/privacy/accessibility defects blocking at all cycles |
| Q6       | Focused validation applies (`git diff --check`, YAML frontmatter check, relative Markdown link check, ASCII/style check); boundary verification in `rpi-review` must test all five boundaries via structured static/trace table and explicitly qualify static/simulation review vs unexecuted live `tmux` native runs | `C7, C8, W1`     | high       | Record Focused validation tier rationale and five-boundary verification matrix in Plan and Review artifacts        |

## Key Discoveries

* Commit `ad005cd5f` (`#1783`, earlier on `2026-11-15`) partially touched `Human blockers` and step 6, inadvertently replacing D5's `"after two correction cycles"` with `"after the [allowed] correction cycles"` and recording `2026-11-11` instead of `2026-11-09` (`C1`, `C5`, `W1`).
* Pre-publication local review-correction cycles (`2026-11-15` CI-economy rule) and post-publication PR review-correction cycles must share one per-issue `Correction-cycle budget` so deferring PR creation saves GitHub Actions runs without silently doubling the five-cycle ceiling (`C2`, `C3`, `C5`, `W1`).
* Repository Markdown rules enforced by `#1783`'s mechanical validator require plain ASCII (`ord(c) <= 127`, ASCII hyphens `E1-E5`, no em/en dashes), `*` bullets, and unbolded list-item prefixes (`C7`, `C8`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Introduce a concise, canonical `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` section immediately after `## Human blockers` in `.github/agents/ama-backlog-delivery-coordinator.agent.md`, reconcile `Human blockers` and step 6 to link to it while restoring D5's exact two-cycle threshold (`2026-11-01`), and update `## CI economy and PR backlog cap` plus steps 5-6 to codify the `2026-11-15` local-before-PR publication rule (keeping WIP commits, full local RPI, any local review-correction fixes within the single five-cycle budget, selected-tier local validation, and pre-publication independent exact-head review local in the worktree before pushing or opening a PR).
* Rationale: Single-source definition eliminates wording drift across `Human blockers`, `CI economy`, step 5, and step 6; preserves all `#1783` operational improvements (`C6`); closes both the diagnostic-cycle overreach and pre-PR/post-PR split-budget loopholes; and satisfies every criterion of `#1296` (`W1`, `W2`) plus the `2026-11-15` CI-economy directive.
* Evidence refs: `C1, C2, C3, C4, C5, C6, C7, C8, W1, W2, W3`
* Implementation impact: Single production instruction file `.github/agents/ama-backlog-delivery-coordinator.agent.md` plus dated RPI artifacts under `.copilot-tracking/`.
* Confidence: high: all authoritative issue comments, commit diffs, and target sections were inspected directly.

File tree:

```text
.github/agents/ama-backlog-delivery-coordinator.agent.md (modified)
.copilot-tracking/rpi-sessions/2026-11-15/delivery-1296-correction-cycles-state.json (created)
.copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md (created)
.copilot-tracking/plans/2026-11-15/delivery-1296-correction-cycles-plan.instructions.md (planned)
.copilot-tracking/details/2026-11-15/delivery-1296-correction-cycles-details.md (planned)
.copilot-tracking/changes/2026-11-15/delivery-1296-correction-cycles-changes.md (planned)
.copilot-tracking/reviews/2026-11-15/delivery-1296-correction-cycles-review.md (planned)
```

### Alternative: Inline repetition across Human blockers and Step 6 without a dedicated section

* Approach: Paste the full five-cycle default, early-stop, no-reset, gate non-waiver, `E1-E5` `#1288` grant rules, and D5 distinction inline inside both `Human blockers` and step 6.
* Trade-offs: Fewer headings, but duplicates ~35 lines of dense policy rules across two distant places (`line 52` and `line 822`), inviting future drift like `ad005cd5f`.
* Evidence refs: `C1, C5, C6`
* Rejection rationale: Violates the file's own single-source pattern (used by `Admission rule (single source; other sections cross-reference it)` at line 99 and `Receipt refresh rule (single source)` at line 866).

### Alternative: Separate cycle budgets for pre-PR local review and post-PR review

* Approach: Allow up to five local pre-publication correction cycles before `gh pr create` and a fresh five correction cycles after PR creation.
* Trade-offs: Gives more autonomous retries after publication, but permits up to ten total correction cycles per issue without owner approval.
* Evidence refs: `C2, C5, W1`
* Rejection rationale: Directly violates `#1296` AC 1 & AC 2 ("up to five total review-correction cycles per issue" and "Do not reset used cycles").

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Branch naming note -- the active worktree `/home/azureuser/source/ama-demo-wt/docs-1296-correction-cycles` was checked out by the caller on branch `docs/1296-correction-cycles-1125` at `697b00c0a` (`origin/feat/demo-164-chat-grounding-provenance-0900`), while the brief header parenthetically wrote `docs/delivery-1296-correction-cycles`. Following `.github/copilot-instructions.md` ("Known active branch... Reuse it by default... does not authorize... deleting a branch"), keep commits on the worktree's active checked-out branch `docs/1296-correction-cycles-1125` so caller HEAD inspection succeeds cleanly, and record both names in the changes/review handoff.
* Follow-up: Live native coordinator behavior under `tmux` is never exercised by documentation-only edits; static/trace boundary verification in `rpi-review` must state that qualification explicitly per `#1296` AC 4.
* Residual uncertainty: none affecting planning or implementation.

## Current Decisions

| Decision                                                                                                              | Status    | Owner / source          | Rationale                                                                                                       | Evidence IDs     | Implications                                                                                      |
|-----------------------------------------------------------------------------------------------------------------------|-----------|-------------------------|-----------------------------------------------------------------------------------------------------------------|------------------|---------------------------------------------------------------------------------------------------|
| D-1296-1: Reconcile coordinator correction-cycle policy via single-source `## Correction-cycle budget (owner, 2026-11-09, issue #1296)` | confirmed | owner (`#1296`, `#1288`) | Centralizes 5-total max, early stop, ledger, no-reset, exhaustion blocker, `E1-E5` grant, and retained gates   | `C1, C5, W1, W2` | Referenced from `Human blockers`, `CI economy`, step 5, and step 6                                |
| D-1296-2: Preserve owner decision D5 (`2026-11-01`) with explicit `"after two correction cycles"` threshold           | confirmed | owner (`#1296` AC 3)    | Repairs `ad005cd5f` wording drift while keeping blocking safety/privacy/accessibility findings blocking         | `C1, C5, W1`     | Restores two-cycle non-blocking follow-up rule in `Human blockers` and step 6                     |
| D-1296-3: Distinguish bounded unchanged-source diagnostics from source-modifying review-correction cycles              | confirmed | evidence (`C1, W1, W2`) | Prevents diagnostic wording from overriding early stop or authorizing a 6th source-correction cycle             | `C1, C5, W1, W2` | Keeps `#1783` diagnostic intent compatible with `#1296` AC 1 & AC 2                               |
| D-1296-4: Defer push and PR creation until local RPI, local review-correction fixes, and selected-tier validation pass | confirmed | owner (`2026-11-15`)    | Prevents repeated hosted GitHub Actions runs on WIP pushes while counting local fixes in the 5-cycle budget     | `C2, C3, C5`     | Updates `CI economy and PR backlog cap`, step 5, and step 6                                       |
| D-1296-5: Classify validation as `Focused` tier (`git diff --check`, frontmatter/link/ASCII style verification)        | confirmed | caller & instructions   | Instruction-only change touching no workflow, gate runner, dependency, Dockerfile, SQL, or runtime code         | `C7, C8, W1`     | No heavy local gate receipt required; coordinator/hosted checks run upon eventual publication      |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none     | none                               | none  | none   | none           |

## Potential Next Research

| Priority | Research item                                                                 | Expected value                                                   | Trigger                                                       | Selected? | Related questions / evidence |
|----------|-------------------------------------------------------------------------------|------------------------------------------------------------------|---------------------------------------------------------------|-----------|------------------------------|
| L        | Post-merge observation of PR-push count reduction under `2026-11-15` CI rule  | Operational telemetry on hosted Actions runner savings           | After future delivery wave runs under updated coordinator     | deferred  | `Q4; C2, C5`                 |

## Planning Readiness

* Status: Ready
* Decision state: Converged single-source `Correction-cycle budget` + D5 two-cycle restoration + `2026-11-15` local-before-PR publication rule selected (`D-1296-1` through `D-1296-5`).
* Evidence basis: `C1, C2, C3, C4, C5, C6, C7, C8, W1, W2, W3`
* Preconditions met: `#1301` (`#1294`) is already merged in ancestry; worktree is clean at `697b00c0a` (`origin/feat/demo-164-chat-grounding-provenance-0900`); all target line ranges and acceptance criteria are verified.
* Blockers: none
* Smallest action to change readiness: none (`Ready`)

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Cycle 1: Wave 1 (Wider), Wave 2 (Deeper), and Wave 3 (Contrarian) completed in order                                           |
| Lane evidence or inline fallback | Inline execution across single target agent file, local git commit history, and GitHub issue/PR metadata (`jmservera/ama`)     |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (`C1`-`C8`, `W1`-`W3`)                                                                                                   |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `Plan` (`rpi-plan`)                                                   |

## Advisory Next Step

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (`C1`-`C8`, `W1`-`W3`)                                                                                                   |
| Output mode and planning support | `convergence`; yes -- converged edit specification and five-boundary verification design ready for planning                    |
| Acting owner                     | confirmed automatic RPI Agent                                                                                                  |
| Required gates or confirmations  | Research waves complete (`passed`), Planning Readiness `Ready` (`passed`), pre-transition state write to `Plan` (`passed`)     |
| Continuation result              | automatic continuation to `rpi-plan`                                                                                           |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/delivery-1296-correction-cycles-research.md                                              |
| Notes for planning or re-entry   | Preserve all `#1783` (`ad005cd5f`) operational rules, enforce ASCII-only punctuation (`E1-E5`), and cover all 5 test boundaries |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All target passages, git ancestry commits, and GitHub issue authorizations are verified from primary records; further search would be redundant.

## Sources

* W1 - GitHub Issue #1296: docs(delivery): align correction-cycle default with owner authorization - https://github.com/jmservera/ama/issues/1296 (retrieved 2026-11-15, created 2026-11-09)
* W2 - GitHub Issue #1288 owner authorization comment 6735179415 - https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415 (retrieved 2026-11-15, 2026-11-09T08:03:44Z)
* W3 - GitHub Pull Request #1641: feat(chat): label answer origin and answer case-unblock questions from rules - https://github.com/jmservera/ama/pull/1641 (retrieved 2026-11-15, OPEN)

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry and Provenance, User Participation and Research Decisions, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions and Evidence, Key Discoveries, Alternatives and Decision State, Open Questions/Risks/Residual Uncertainty, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
