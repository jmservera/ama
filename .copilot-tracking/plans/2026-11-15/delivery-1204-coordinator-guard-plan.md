<!-- markdownlint-disable-file -->
# RPI Plan: Prevent Unsupported Idle Ticks and Stale Coordinator Handoffs (Issue #1204)

## Task Metadata

* Task ID: issue-1204
* Task slug: delivery-1204-coordinator-guard
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-plan-critique.md

## Executive Summary

This plan updates the AMA Backlog Delivery Coordinator instructions in .github/agents/ama-backlog-delivery-coordinator.agent.md and adds an offline deterministic validator in tools/check-coordinator-handoff.py paired with focused unit tests in tools/test_check_coordinator_handoff.py for Issue #1204. Together, these changes ensure scheduled coordinator checks cannot claim "nothing changed" or pause on an unverified blocker while open issues remain unclassified in the current run, require an explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, or `ready to start`) before any idle or waiting summary, require handoff and checkpoint notes to refresh open-issue counts, open-PR counts, active session status, and exact SHAs from live commands at write time, and mechanically flag violations in coordinator artifacts.

### User Decisions and Requirements Highlights

* Update .github/agents/ama-backlog-delivery-coordinator.agent.md so scheduled checks cannot claim "nothing changed" or pause on an unverified blocker while open issues remain unclassified in the current run, keeping independent lanes progressing.
* Require an explicit Markdown issue-state classification table using the five canonical categories (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before any idle or waiting summary.
* Require handoff and checkpoint notes to refresh open-issue counts, open-PR counts, and active session status from live commands at the time of writing rather than copying earlier counts, session lists, or SHAs.
* Deliver tools/check-coordinator-handoff.py and tools/test_check_coordinator_handoff.py (using `unittest`), run focused validation (`unittest`, `ruff check`, and `ruff format --isolated --line-length 100 --check`) without running tools/rpi-checks.py, commit locally on `fix/delivery-1204-coordinator-guard` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641), and leave a clean frozen HEAD without pushing.

### What You May Not Know

* Tools outside the named trigger list in .github/workflows/src-ci.yml do not run automatically in hosted Source projects CI, making local execution of tools/test_check_coordinator_handoff.py and tools/check-coordinator-handoff.py essential focused-tier evidence.
* Every issue-classification table row already includes the issue's own `#N` identifier in the first column; the validator must require blocker/dependency links in non-issue columns and reject bare self-only `#<self>` tokens on both `human-blocked` and `dependency-blocked` rows unless paired with an `https?://` URL, Markdown `[label](target)` link, `#issuecomment-` anchor, or distinct `#<other>` issue/PR reference.
* Open PRs awaiting hosted GitHub Actions CI or queued auto-merge with zero live `tmux` sessions, as well as still-open stacked child issues merged into an unmerged parent topic branch, map cleanly to `dependency-blocked` with a concrete PR/check link (`merged` is reserved for issues closed by delivery on `main`), and multi-role `rpi-{number}-{role}` runs allow multiple active `tmux` sessions to map to one `active session` issue row (`active_session_rows <= declared_active_sessions`).
* Existing adoption tests in tools/test_rpi_phase_witness.py assert exact `tools/rpi_phase_witness.py record launch`, `tools/rpi_phase_witness.py verify`, and `--evidence-dir` strings in .github/agents/ama-backlog-delivery-coordinator.agent.md, which must remain untouched.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) writing dated artifacts under .copilot-tracking/ (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/2026-11-15/`, and `reviews/logs/2026-11-15/`) for Issue #1204 (caller prompt).
* Work in worktree `/home/azureuser/source/ama-demo-wt/feat-1204-coordinator-guard` on branch `fix/delivery-1204-coordinator-guard` targeting parent base `feat/demo-164-chat-grounding-provenance-0900` (PR #1641) (caller prompt).
* Update the delivery coordinator instructions so scheduled checks cannot claim "nothing changed" or pause on an unverified blocker while open issues remain unclassified in the current run (Issue #1204 AC 1; caller prompt).
* Require an explicit issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, or `ready to start`) before any idle or waiting summary (Issue #1204 AC 2; caller prompt).
* Require handoff and checkpoint notes to refresh open-issue counts, open-PR counts, and active session status from live commands at the time of writing (Issue #1204 AC 3; caller prompt).
* Create tools/check-coordinator-handoff.py and tools/test_check_coordinator_handoff.py (using `unittest`) validating coordinator handoff/status Markdown and .github/agents/ama-backlog-delivery-coordinator.agent.md for the five required issue-state classification categories (`merged`, `active session`, `human-blocked`, `dependency-blocked`, `ready to start`), rejecting unsupported idle/waiting summaries when unclassified open issues exist, and flagging stale count/SHA handoff blocks (Issue #1204 AC 4; caller prompt).
* Apply Focused validation tier: run `python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`, and `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`; do NOT run tools/rpi-checks.py (caller prompt).
* Commit all changes and .copilot-tracking/ RPI artifacts locally on `fix/delivery-1204-coordinator-guard` with repository-local noreply author/committer email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; do NOT push or open a PR (caller prompt; .github/copilot-instructions.md).

## Goals

* Eliminate unsupported coordinator idle/waiting claims and unverified-blocker pauses across connected sections of .github/agents/ama-backlog-delivery-coordinator.agent.md (`G-01`).
* Establish a single canonical five-category issue-state classification table contract (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) and live-command count/session/SHA refresh contract for coordinator check, handoff, and checkpoint outputs (`G-02`).
* Provide a deterministic, zero-network CLI and library validator (tools/check-coordinator-handoff.py) with focused `unittest` coverage (tools/test_check_coordinator_handoff.py) proving acceptance criteria 1 through 4 (`G-03`).

## Scope and Non-Goals

### In Scope

* Coordinated instruction updates in .github/agents/ama-backlog-delivery-coordinator.agent.md across `## Liveness and stop decision`, `## Recurring schedules`, `## Stabilization checkpoints`, `## Workflow` step 5 scheduled-check summary, and `## Final report`.
* Creation of tools/check-coordinator-handoff.py using Python 3.12 standard library only.
* Creation of tools/test_check_coordinator_handoff.py using `unittest`.
* Focused validation (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`, existing `tools/test_rpi_phase_witness.py` regression check, and AMA Markdown/frontmatter/link/ASCII checks) and HVE-aligned static/trace qualification in the review artifacts.
* Dated RPI tracking artifacts under .copilot-tracking/ and a clean frozen local commit on `fix/delivery-1204-coordinator-guard`.

### Non-Goals

* Application, database, API, UI, or infrastructure changes under `src/` or `infra/`.
* Workflow trigger edits under `.github/workflows/`, branch-protection changes, or live schedule mutations.
* Running `python3 tools/rpi-checks.py`.
* Pushing to `origin` or creating/updating a GitHub pull request from inside this worker session.

## Functional Requirements

* `FR-01` (Anti-idle and unverified-blocker guard): .github/agents/ama-backlog-delivery-coordinator.agent.md must forbid scheduled checks and turns from claiming `"nothing changed"`, reporting idle/waiting, or pausing on an unverified blocker while any open issue remains unclassified in the current run; an asserted or carried-over blocker without current-run verification and a concrete link is inspection work, not a pause ground.
  * Observable acceptance criteria: `AC-01`, `AC-04`
* `FR-02` (Explicit five-category issue-state classification table): .github/agents/ama-backlog-delivery-coordinator.agent.md must require an explicit Markdown issue-state classification table assigning every issue to `merged` (closed on `main`), `active session` (open issue with >=1 live `tmux` `rpi-*` session), `human-blocked` (with concrete issue/comment/ADR/decision link), `dependency-blocked` (with concrete blocking issue/PR/check link, including still-open stacked children awaiting parent PR merge to `main` and open PRs awaiting hosted CI or queued auto-merge when no `tmux` session is active), or `ready to start` (actionable work eligible now) **before** any `"what changed"`, `"what is waiting"`, idle, waiting, `"nothing changed"`, pause, or handoff summary, reconciling internal `running`/`ready`/`unknown` investigation rules cleanly.
  * Observable acceptance criteria: `AC-02`, `AC-04`
* `FR-03` (Live-command refresh for handoffs and checkpoints): .github/agents/ama-backlog-delivery-coordinator.agent.md must require handoff notes, end-of-check status notes, stabilization checkpoints, and final/wave handoff reports to refresh open-issue counts (`gh issue list --state open --limit 500`), open-PR counts (`gh pr list --state open --limit 200`), active session status (`tmux list-sessions`), and exact `HEAD` / `origin/main` / stacked `target/base` SHAs (`git rev-parse`) from live commands run at write time using a canonical metadata + table schema, forbidding copied counts, stale `/tmp` brief references, or unrefreshed SHA blocks.
  * Observable acceptance criteria: `AC-03`, `AC-04`
* `FR-04` (Coordinator instruction and handoff Markdown validator): tools/check-coordinator-handoff.py must validate (a) .github/agents/ama-backlog-delivery-coordinator.agent.md for valid frontmatter, resolved relative links, all five required classification categories, blocker-link requirements, anti-idle/unclassified-open-issue rules, and live-refresh handoff rules, and (b) coordinator handoff/status/checkpoint Markdown documents (scoped per dated checkpoint/handoff section when multiple dated sections appear) for valid five-category classification tables, non-bare-self blocker links on both `human-blocked` and `dependency-blocked` rows, table-before-summary ordering, rejection of idle/waiting/`"nothing changed"`/unverified-blocker pause summaries when open issues are unclassified or `ready to start` (honoring explicit `M/N` session caps and active `open_prs > 15` PR drains on waiting summaries), and detection of stale count/SHA handoff blocks (missing live metrics/provenance, carry-forward/stale markers, `observed_at` vs `written_at` timestamp skew, internal count contradictions including multi-role-safe `active_session_rows` vs `Active sessions` invariants, placeholder or per-key conflicting SHAs separating `HEAD SHA` vs `Origin/main SHA` vs `Target/base SHA`, and optional `--expect-*` mismatches).
  * Observable acceptance criteria: `AC-04`, `AC-05`
* `FR-05` (Focused unit test suite): tools/test_check_coordinator_handoff.py must test tools/check-coordinator-handoff.py offline with `unittest`, covering the live repository agent file, valid active and valid fully-classified waiting handoffs, missing/mutated agent rules, invalid/unknown categories, missing or self-only links on `human-blocked` and `dependency-blocked`, unsupported idle/waiting/`"nothing changed"` summaries (missing table, table after summary, unclassified open-issue count/list gap, `ready to start` row during idle/`"nothing changed"`, unverified blocker pause), stale count/SHA/timestamp/carry-forward blocks, fenced-code/negation non-false-positives, and CLI exit codes.
  * Observable acceptance criteria: `AC-04`, `AC-05`

## Non-Functional Requirements

* `NFR-01` (Offline determinism, Python 3.12 typing, and Ruff compliance): tools/check-coordinator-handoff.py and tools/test_check_coordinator_handoff.py must use only the Python 3.12 standard library, perform zero network calls during default/unit-test runs, avoid retired path literals flagged by tools/check-legacy-references.py, and pass `ruff check` (including `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100`) and `ruff format --isolated --line-length 100 --check` with zero diagnostics.
  * Objective threshold or evaluation condition: Exit code `0` across `unittest` and both `ruff` commands in under 5 seconds offline.
  * Operating condition or verification approach, if needed: Direct CLI execution in the worktree without network or GitHub credentials.
  * Observable acceptance criteria: `AC-05`
* `NFR-02` (AMA Markdown style and coordinator contract preservation): Edits to .github/agents/ama-backlog-delivery-coordinator.agent.md must preserve YAML frontmatter (`name`, `description`), all existing resolved relative links, plain ASCII (`ord(c) <= 127`), `*` unordered list markers without bolded prefixes, zero em/en dashes, language-tagged fenced blocks, `#1296` correction-cycle rules, `2026-11-15` CI-economy rules, and `tools/rpi_phase_witness.py` commands asserted by tools/test_rpi_phase_witness.py.
  * Objective threshold or evaluation condition: Zero whitespace/ASCII/frontmatter/link violations and exit code `0` on `python3 -m unittest tools/test_rpi_phase_witness.py -q`.
  * Operating condition or verification approach, if needed: Mechanical Python audit plus `git --no-pager diff --check` and `test_rpi_phase_witness.py`.
  * Observable acceptance criteria: `AC-01`, `AC-02`, `AC-03`, `AC-06`

## Acceptance Criteria

* `AC-01`: .github/agents/ama-backlog-delivery-coordinator.agent.md explicitly forbids scheduled checks and turns from claiming `"nothing changed"` or pausing on an unverified blocker while open issues remain unclassified in the current run (`FR-01`, `NFR-02`).
* `AC-02`: .github/agents/ama-backlog-delivery-coordinator.agent.md requires an explicit Markdown issue-state classification table with categories `merged`, `active session`, `human-blocked` (with link), `dependency-blocked` (with link), or `ready to start` before any idle or waiting summary (`FR-02`, `NFR-02`).
* `AC-03`: .github/agents/ama-backlog-delivery-coordinator.agent.md requires handoff and checkpoint notes to refresh open-issue counts, open-PR counts, active session status, and exact SHAs from live commands at the time of writing (`FR-03`, `NFR-02`).
* `AC-04`: tools/check-coordinator-handoff.py validates both .github/agents/ama-backlog-delivery-coordinator.agent.md and coordinator handoff/status Markdown artifacts for required classification categories + links, rejects unsupported idle/waiting summaries when unclassified open issues or `ready to start` work exist, and flags stale count/SHA handoff blocks (`FR-04`).
* `AC-05`: `python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`, and `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` all pass with exit code `0` (`FR-04`, `FR-05`, `NFR-01`).
* `AC-06`: All changes and dated .copilot-tracking/ RPI artifacts (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/2026-11-15/`, and `reviews/logs/2026-11-15/`) pass mechanical/link/ASCII and `test_rpi_phase_witness.py` checks and are committed locally on `fix/delivery-1204-coordinator-guard` with the Copilot trailer and clean `git status --short` (`NFR-02`).

## Test Ownership and Validation Lock

* Canonical implementation targets: .github/agents/ama-backlog-delivery-coordinator.agent.md, tools/check-coordinator-handoff.py, tools/test_check_coordinator_handoff.py (generated targets: `none`).
* Applicable test ownership: tools/test_check_coordinator_handoff.py owns unit and CLI behavior tests for tools/check-coordinator-handoff.py and live contract verification of .github/agents/ama-backlog-delivery-coordinator.agent.md; tools/test_rpi_phase_witness.py owns existing phase-witness adoption regression coverage.
* Exact test removals: `none`.
* Maximum test additions: At most 16 focused `test_*` methods in tools/test_check_coordinator_handoff.py, using `self.subTest(...)` grouping per contract family to cover all positive and negative semantic cases cleanly without redundant constant checks.
* Semantic-versus-regression coverage: Semantic tests prove five-category table parsing, non-self blocker link enforcement, table-before-summary ordering, unclassified open-issue and `ready to start` anti-idle rejection, unverified-blocker pause rejection, stale count/SHA/timestamp/carry-forward detection, fenced/negated prose immunity, and CLI exit behavior; regression tests prove the live repository .github/agents/ama-backlog-delivery-coordinator.agent.md passes both `check_agent_instructions` and tools/test_rpi_phase_witness.py.
* Planned validation commands:
  * `python3 tools/check-coordinator-handoff.py`
  * `python3 -m unittest tools/test_check_coordinator_handoff.py -q`
  * `python3 -m unittest tools/test_rpi_phase_witness.py -q`
  * `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`
  * `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`
  * `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`
  * `git --no-pager diff --check`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md                                              |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-plan-critique.md with Revise disposition (all `PC-001`..`PC-004` resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md                                                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for `rpi-implement`                                                                                             |
| Continuation context             | Confirmed automatic RPI Agent parent continues automatically to `rpi-implement`                                                    |

## Sources

* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Primary codebase research (`C1`-`C9`) and converged design decisions (`D-1204-1` through `D-1204-4`).
* .github/agents/ama-backlog-delivery-coordinator.agent.md: Target coordinator agent instruction specification.
* .github/copilot-instructions.md: Repository validation tiers (`D4` / `#1294`), AMA Markdown style, and branch/commit conventions.
* tools/check-legacy-references.py and tools/test_check_legacy_references.py: Repository conventions for standalone Markdown/repo checkers and `importlib`-loaded `unittest` suites.
* tools/test_rpi_phase_witness.py: Existing coordinator instruction adoption regression test.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Coordinator Instruction Guardrails for Issue Classification and Live Handoffs

* Intent: Update .github/agents/ama-backlog-delivery-coordinator.agent.md across all connected liveness, scheduled-check, checkpoint, and report sections to satisfy `FR-01`, `FR-02`, `FR-03`, and `NFR-02`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add Canonical Issue-State Classification Table and Live Handoff Refresh Rules

* Requirement and evidence: `FR-01`, `FR-02`, `FR-03`, `NFR-02`; research `C1`-`C4`, `C6`, `C7`, `C9`.
* Expected result: .github/agents/ama-backlog-delivery-coordinator.agent.md forbids claiming `"nothing changed"` or pausing on an unverified blocker while open issues remain unclassified in the current run, requires an explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before any idle or waiting summary, requires handoff and checkpoint notes to refresh open-issue counts, open-PR counts, active session status, and exact SHAs from live commands at write time, references `python3 tools/check-coordinator-handoff.py`, and preserves AMA Markdown style plus existing `#1296`, `#1783`, and `rpi_phase_witness.py` invariants.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Deterministic Coordinator Handoff and Instruction Validator

* Intent: Create tools/check-coordinator-handoff.py to enforce the coordinator agent contract and validate coordinator handoff/status/checkpoint Markdown artifacts offline (`FR-04`, `NFR-01`).
* Dependencies: `P01`.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement tools/check-coordinator-handoff.py CLI and Validation Engine

* Requirement and evidence: `FR-04`, `NFR-01`; research `C1`-`C5`, `C7`, `C8`.
* Expected result: tools/check-coordinator-handoff.py validates .github/agents/ama-backlog-delivery-coordinator.agent.md by default and validates supplied coordinator handoff/status/checkpoint Markdown documents via `--handoff` (or `--stdin`), checking the five canonical classification categories, non-self links on `human-blocked` and `dependency-blocked` rows, table-before-summary ordering, unclassified open-issue and `ready to start` anti-idle guards, unverified-blocker pause rejection, and stale count/SHA/timestamp/carry-forward handoff blocks, with exit codes `0` (pass) and `1` (violations).
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Unit Tests, Ruff Lint/Format, and Mechanical Verification

* Intent: Create tools/test_check_coordinator_handoff.py and execute all required focused unit, Ruff, regression, and mechanical/HVE checks (`FR-05`, `NFR-01`, `NFR-02`).
* Dependencies: `P01`, `P02`.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Implement tools/test_check_coordinator_handoff.py and Run Focused Validation

* Requirement and evidence: `FR-05`, `NFR-01`, `NFR-02`, `AC-01` through `AC-06`; research `C5`-`C9`.
* Expected result: tools/test_check_coordinator_handoff.py passes `python3 -m unittest tools/test_check_coordinator_handoff.py -q` (at most 16 focused test methods), Ruff lint and isolated 100-char format checks pass with exit `0`, tools/test_rpi_phase_witness.py and `python3 tools/check-coordinator-handoff.py` pass with exit `0`, and mechanical/HVE static-trace evidence is recorded for review and clean local commit closeout.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md

## Dependencies

* Parent target branch `feat/demo-164-chat-grounding-provenance-0900` (`f74e1bf1fd7d3e62048a69ade51a126704ebc556`, PR #1641): Current worktree `fix/delivery-1204-coordinator-guard` is already branched cleanly from that exact SHA.
* Python 3.12 and `ruff` (`0.17.3`): Verified present in the local environment.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` (High: five-category membership for hosted-CI/stacked-child states, multi-role `tmux` sessions, and cap/PR-drain waiting checks) | resolved | Defined exhaustive five-category membership (`merged` closed on `main`; `dependency-blocked` with PR/check link for open PRs awaiting hosted CI/auto-merge with 0 sessions and still-open parent-merged stacked children), relaxed session consistency to multi-role-safe `active_session_rows <= declared_active_sessions` (forbidding `0` declared with `>0` rows or `>0` declared with `0` rows absent explicit non-issue sessions), and honored declared `M/N` session caps plus active `open_prs > 15` PR drains on waiting summaries in `FR-02`, `FR-04`, `P01-T01`, `P02-T01`, and `P03-T01`. |
| `PC-002` (High: step 5 summary ordering, canonical handoff/checkpoint field schema, stacked SHA keys, and `--limit` on `gh` list commands) | resolved | Reordered step 5 `Cover, in this order:` to lead with the live-refreshed counts/sessions/SHAs snapshot (`gh issue list --state open --limit 500`, `gh pr list --state open --limit 200`, `tmux list-sessions`, `git rev-parse`) and the five-category classification table using a canonical fenced Markdown schema, separated `HEAD SHA` vs `Origin/main SHA` vs `Target/base SHA` keys, and scoped snapshot checks per dated section in `FR-03`, `FR-04`, `P01-T01`, and `P02-T01`. |
| `PC-003` (Medium: bare same-issue `#<self>` link bypass on `human-blocked` rows) | resolved | Updated `What You May Not Know`, `FR-04`, `P02-T01`, and `P03-T01` to reject bare same-issue `#<self>` tokens on both `human-blocked` and `dependency-blocked` rows unless paired with an `https?://` URL, Markdown `[label](target)` link, `#issuecomment-` anchor, or distinct `#<other>` reference. |
| `PC-004` (Medium: mandatory step 6 HVE static/behavior qualification artifact fields and `subTest` grouping within `<= 16` test methods) | resolved | Made .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md an unconditional `P03`/`P03-T01` deliverable recording all five step 6 attributes (`exact source identity`, `execution status`, `verdict`, `fidelity`, `executor or profile limits`) and specified `self.subTest(...)` grouping per contract family within `<= 16` `test_*` methods. |

## Follow-Up Items

* Consider wiring `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR if the owner selects full-gate integration (outside immediate Issue #1204 focused scope; owner: backlog triage).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-changes.md
* Ready phase or task: All planned phases (`P01`, `P02`, `P03`) complete; ready for `rpi-review`
* Remaining provisional question or blocker: None
