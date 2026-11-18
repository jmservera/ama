<!-- markdownlint-disable-file -->
# RPI Phase Details: Prevent Unsupported Idle Ticks and Stale Coordinator Handoffs (Issue #1204)

## Metadata

* Task ID: issue-1204
* Task slug: delivery-1204-coordinator-guard
* Related plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, .github/copilot-instructions.md, tools/check-legacy-references.py, tools/test_check_legacy_references.py, tools/test_rpi_phase_witness.py

## Phase Index

| Phase ID | Name                                                                   | Status   | Detail sections |
|----------|------------------------------------------------------------------------|----------|-----------------|
| P01      | Coordinator Instruction Guardrails for Issue Classification and Live Handoffs | complete | P01, P01-T01    |
| P02      | Deterministic Coordinator Handoff and Instruction Validator            | complete | P02, P02-T01    |
| P03      | Focused Unit Tests, Ruff Lint/Format, and Mechanical Verification      | complete | P03, P03-T01    |

<!-- rpi:phase id=P01 -->
## P01: Coordinator Instruction Guardrails for Issue Classification and Live Handoffs

### Context

Research (`C1`-`C4`) showed that .github/agents/ama-backlog-delivery-coordinator.agent.md currently classifies items internally as `ready`, `running`, `dependency-blocked`, `human-blocked`, or `unknown`, but lacks three explicit prompt contracts required by Issue #1204:
1. Explicitly forbidding scheduled checks and turns from claiming `"nothing changed"` or pausing on an unverified blocker while open issues remain unclassified in the current run.
2. Requiring an explicit rendered Markdown issue-state classification table using the five canonical categories (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before any idle or waiting summary.
3. Requiring handoff notes and checkpoint notes to refresh open-issue counts, open-PR counts, active session status, and exact SHAs from live commands run at the time of writing rather than copying earlier counts or `/tmp` briefs.

### Intent

Update all connected liveness, schedule, checkpoint, step 5 check-summary, and final-report sections in .github/agents/ama-backlog-delivery-coordinator.agent.md so they enforce one consistent contract without regressing `#1296`, `#1783`, or `rpi_phase_witness.py` rules.

### Boundaries

* Included: Surgical edits to .github/agents/ama-backlog-delivery-coordinator.agent.md in `## Liveness and stop decision`, `## Recurring schedules`, `## Stabilization checkpoints`, `## Workflow` step 5 scheduled-check summary, and `## Final report`.
* Excluded: Changing YAML frontmatter keys (`name`, `description`), editing `.github/copilot-instructions.md`, modifying `Correction-cycle budget` (`#1296`), modifying `rpi_phase_witness.py` launch/verify lines, or changing application code.

### Likely Targets

* .github/agents/ama-backlog-delivery-coordinator.agent.md: Add `### Issue-state classification table and live handoff refresh` under `## Liveness and stop decision` and align `## Recurring schedules`, `## Stabilization checkpoints`, step 5 check-summary prose, and `## Final report`.

### Dependencies

* None.

### Validation Expectations

* `git --no-pager diff --check` exits `0`.
* YAML frontmatter parses with `name` and `description`, all relative Markdown links and section anchors resolve, all characters are plain ASCII (`ord(c) <= 127`), unordered lists use `*` without bolded prefixes, zero em/en dashes appear, and `python3 -m unittest tools/test_rpi_phase_witness.py -q` passes.

### Completion Evidence

* Clean diff in .github/agents/ama-backlog-delivery-coordinator.agent.md proving `AC-01`, `AC-02`, and `AC-03`, verified by `python3 tools/check-coordinator-handoff.py` in `P02`/`P03`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add Canonical Issue-State Classification Table and Live Handoff Refresh Rules

#### Context

Connected gates across .github/agents/ama-backlog-delivery-coordinator.agent.md must agree so a scheduled check or handoff writer sees the same rule in `Liveness and stop decision`, `Recurring schedules`, `Stabilization checkpoints`, step 5, and `Final report`.

#### Intent

Specify exact, mechanically checkable rules for the five-category classification table, unverified-blocker non-pause, and live-command refresh at write time.

#### Boundaries

* Included:
  * In `## Liveness and stop decision`: state explicitly that scheduled checks and turns must never claim `"nothing changed"`, emit an idle or waiting summary, or pause on an unverified blocker while any open issue remains unclassified in the current run (`gh issue list --state open --limit 500`); an asserted or cached blocker from an earlier tick or handoff without current-run verification and a concrete link is inspection work for this tick, never a pause condition. Add subsection `### Issue-state classification table and live handoff refresh` defining:
    * Mandatory Markdown issue-state classification table (`| Issue | State | Blocker or evidence link | Next action |`) rendered **before** any `"what changed"`, `"what is waiting"`, idle, waiting, `"nothing changed"`, pause, or handoff summary, classifying every issue into exactly one of the five canonical states:
      * `merged` — issues whose required delivery has merged to `main` and closed the issue on GitHub (never used for still-open stacked child issues merged only into an unmerged parent topic branch or open `status:partially-delivered` issues).
      * `active session` — open issues with at least one verified live `tmux` `rpi-*` worker session (internal `running`, including multi-role `rpi-{number}-{role}` sessions).
      * `human-blocked` — open issues blocked on an owner decision, credentials, legal/resident/executive approval, branch-protection gate, or exhausted `#1296` correction-cycle budget, carrying a concrete non-bare-self link (`https?://` URL, `#issuecomment-` anchor, Markdown document link, or distinct `#<other>` reference).
      * `dependency-blocked` — open issues blocked on a specific upstream active or human-blocked issue or PR, still-open stacked child issues merged into a parent topic branch awaiting that parent PR's merge to `main`, or open PRs awaiting hosted GitHub Actions CI or queued auto-merge when no `tmux` session is active, carrying a concrete link to the blocking issue, PR, or check run.
      * `ready to start` — actionable open issues eligible now (internal `ready`, including open `status:partially-delivered` issues with remaining actionable scope, completed unpublished candidates awaiting coordinator gate, or failing fixable PR checks).
      * Any `unknown` or `unassessed` open issue must be inspected and classified in the current run before emitting an idle or waiting summary, and any `ready to start` issue bars `"nothing changed"` or global idle summaries (and bars `waiting` summaries unless active `tmux` sessions have reached the declared session cap `M/N` or an active PR drain with `open_prs > 15` is recorded).
    * Live-command refresh rule and canonical fenced Markdown handoff/status schema requiring every handoff note, scheduled-check status note, stabilization checkpoint note, and wave/final report to refresh open-issue counts (`gh issue list --state open --limit 500`), open-PR counts (`gh pr list --state open --limit 200`), active session status (`tmux list-sessions`), and exact `HEAD SHA`, `Origin/main SHA`, and stacked `Target/base SHA` (`git rev-parse`) from live commands executed at the time of writing (`Observed UTC` and `Written UTC`), forbidding copied counts, stale `/tmp` brief references, or carried-over SHA blocks, and validating handoff/status Markdown with `python3 tools/check-coordinator-handoff.py --handoff <file>`.
  * In `## Recurring schedules`: cross-reference that scheduled delivery checks cannot claim `"nothing changed"` or pause on an unverified blocker while open issues remain unclassified in the current run and must render the explicit issue-state classification table before any idle or waiting summary.
  * In `## Stabilization checkpoints`: require checkpoint notes and handoffs to refresh open-issue counts, open-PR counts, active session status, and exact `HEAD SHA`, `Origin/main SHA`, and parent-topic `Target/base SHA` from live commands at the time of writing.
  * In `## Workflow` step 5 scheduled-check summary (`End every check with a status summary...`): reorder `Cover, in this order:` to lead with (1) the live-refreshed counts, active sessions, and SHAs snapshot from live commands at write time and (2) the explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) **before** covering what changed since the last check, what is running now, open PR checks, or any waiting, idle, or `"nothing changed"` summary, and forbid claiming `"nothing changed"` or pausing on an unverified blocker while any open issue remains unclassified in the current run.
  * In `## Final report`: require refreshing open-issue counts, open-PR counts, active session status, and pinned SHAs from live commands at write time in wave, handoff, and final reports.
* Excluded: Unrelated workflow steps or repository files.

#### Likely Targets

* .github/agents/ama-backlog-delivery-coordinator.agent.md: Five surgical hunks aligned to `FR-01` through `FR-03`.

#### Dependencies

* None.

#### Validation Expectations

* Verified mechanically by `python3 tools/check-coordinator-handoff.py` (`P02`), `python3 -m unittest tools/test_rpi_phase_witness.py -q`, and AMA Markdown style checks (`P03`).

#### Completion Evidence

* Updated .github/agents/ama-backlog-delivery-coordinator.agent.md passing all mechanical and contract assertions.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Deterministic Coordinator Handoff and Instruction Validator

### Context

Issue #1204 AC 4 requires creating tools/check-coordinator-handoff.py to validate both .github/agents/ama-backlog-delivery-coordinator.agent.md and coordinator handoff/status Markdown artifacts for required classification categories, unsupported idle/waiting summaries, and stale count/SHA handoff blocks (`C5`, `C7`, `C8`).

### Intent

Build a clean, modular, standard-library Python 3.12 CLI and importable validator module in tools/check-coordinator-handoff.py.

### Boundaries

* Included: Creating tools/check-coordinator-handoff.py with agent-instruction validation, handoff/status/checkpoint Markdown parsing and validation, CLI argument parsing, clear `path:line: <rule>: <detail>` diagnostics, and exit codes `0` (pass), `1` (violations), `2` (CLI/file error).
* Excluded: External third-party dependencies, automatic GitHub API network calls, or mutations to checked files.

### Likely Targets

* tools/check-coordinator-handoff.py: New standalone CLI and library module.

### Dependencies

* `P01`.

### Validation Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0` against the updated repository.
* `python3 -m ruff check tools/check-coordinator-handoff.py` and `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py` exit `0`.

### Completion Evidence

* Executable/importable tools/check-coordinator-handoff.py validating both the coordinator agent file and coordinator handoff/status Markdown inputs.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Implement tools/check-coordinator-handoff.py CLI and Validation Engine

#### Context

Contrarian research (`C1`, `C4`, `C5`) identified four subtle bypasses and false-positive modes to prevent:
1. Column-1 self-link bypass (`#1204` in the `Issue` column falsely satisfying `human-blocked` / `dependency-blocked` link checks).
2. Fenced code blocks (` ``` ` / `~~~`) and negated normative prose (`cannot claim "nothing changed"`, `must not pause`) causing false table or idle-claim triggers.
3. Offline detection of unclassified open issues (via `Open issues: <N>` vs non-merged table rows, explicit open-issue lists or `--open-issues`, `unknown`/`unclassified`/`unassessed` markers, or non-zero `unassessed` closure queues) and `ready to start` idle contradictions.
4. Offline detection of stale count/SHA handoff blocks (missing live metrics or live-command provenance, carry-forward/unrefreshed phrases or stale `/tmp/brief-` template reuse, `observed_at` older than `written_at` beyond `--max-age-minutes`, internal count mismatches between declared `Open issues` / `Open PRs` / `Active sessions` counts and parsed classification/PR/session entries, invalid/placeholder/conflicting SHAs, and optional `--expect-head`, `--expect-base`, `--expect-open-issues`, `--expect-open-prs`, `--expect-active-sessions`, `--check-git-head` CLI checks).

#### Intent

Implement well-factored, typed functions in tools/check-coordinator-handoff.py covering every requirement cleanly within ~320-380 lines of readable Python 3.12.

#### Boundaries

* Included:
  * Constants: `REQUIRED_CATEGORIES = ("merged", "active session", "human-blocked", "dependency-blocked", "ready to start")` and `LINK_REQUIRED_CATEGORIES = ("human-blocked", "dependency-blocked")`.
  * `check_agent_instructions(path: Path, root: Path | None = None) -> list[str]`:
    * Verify top-of-file YAML frontmatter defines non-empty `name` and `description`.
    * Verify all five `REQUIRED_CATEGORIES` appear in non-fenced instruction prose/tables.
    * Verify link requirement wording for `human-blocked` and `dependency-blocked`.
    * Verify scheduled-check anti-idle guard wording (`nothing changed`, `unverified blocker`, `unclassified`, and classification table before idle/waiting summary).
    * Verify live-refresh handoff/checkpoint requirement wording (`open-issue` / `gh issue list`, `open-PR` / `gh pr list`, `active session` / `tmux list-sessions`).
    * Verify relative Markdown links in the agent file resolve under `root`.
  * `check_handoff_text(path: str, text: str, *, expect_head: str | None = None, expect_base: str | None = None, expect_open_issues: int | None = None, expect_open_prs: int | None = None, expect_active_sessions: int | None = None, open_issues: set[int] | None = None, max_age_minutes: int = 30) -> list[str]`:
    * Fence-aware line iterator stripping ` ``` ` and `~~~` blocks while preserving 1-based line numbers.
    * Parse Markdown issue-state classification table(s) (tables whose headers include an issue column like `issue` and a classification column like `state`, `classification`, `category`, or `disposition` where cells match issue states, or under an `issue-state classification` heading):
      * Validate each row's category belongs to `REQUIRED_CATEGORIES`; flag `unknown`, `unclassified`, `unassessed`, empty, or non-canonical categories.
      * Flag duplicate issue numbers in the classification table.
      * Enforce concrete link presence in non-issue cells (`https?://`, Markdown `[label](target)`, explicit comment anchor `#<num>#issuecomment-...`, or distinct issue/PR reference `#<other>` / `owner/repo#<other>` where `other != row_issue`) on **both** `human-blocked` and `dependency-blocked` rows, rejecting bare same-issue `#<self>` tokens on either category when not paired with a URL, Markdown link, `#issuecomment-` anchor, or distinct `#<other>` target.
    * Scope snapshot validation per dated handoff/checkpoint section when multiple dated sections appear in one append-only document so distinct historical checkpoints do not false-conflict.
    * Detect non-negated idle, waiting, `"nothing changed"`, or pause summary lines (e.g., `"nothing changed"`, `"no changes since last"`, `"idle tick"`, `"status: idle"`, `"reporting idle"`, `"waiting on human"`, `"all remaining issues are human-blocked"`, `"pausing schedule"`, `"paused on blocker"`):
      * Require a valid issue-state classification table to exist **before** the first idle/waiting/pause summary line in the section.
      * Reject when unclassified open issues exist (any invalid/unknown row, prose/metadata reporting unclassified/unknown/unassessed open issues or non-zero unassessed closure items, declared `Open issues: N` exceeding classified non-merged issues, or any issue in `open_issues` / declared `Open issue list` missing from the table or marked `merged`).
      * Reject `"nothing changed"` or global idle/`"all blocked"` claims when any row is `ready to start`, and reject `waiting` claims when `ready to start` rows exist while active sessions are below the declared session cap (`M/N` if recorded, else default `8`) and no active PR drain (`open_prs > 15` with drain recorded, or `open_prs > 20`) is active.
      * Reject pausing/waiting on an unverified blocker (prose naming an unverified/assumed/cached blocker, or citing a blocked `#N` issue not classified as `human-blocked` or `dependency-blocked` with a valid link in the table).
    * Detect stale count and SHA handoff blocks:
      * Require refreshed live metrics (`open issues` count, `open PRs` count, `active sessions` count/status) and live-command provenance (`gh issue list` prefix accepting `--limit`/`--json`, `gh pr list` prefix accepting `--limit`/`--json`, `tmux list-sessions` or `tmux ls`) in handoff/checkpoint sections (or flag missing live refresh fields).
      * Flag carry-forward/unrefreshed markers (`copied from`, `carried over`, `cached from`, `from prior handoff`, `from previous tick`, `not refreshed`, `stale /tmp/brief`, reused `/tmp/brief-` template without timestamp).
      * Flag internal count mismatches: declared `Open issues` count vs classified non-merged open issue count (when the table covers the full open set or classified non-merged exceeds declared `Open issues`), multi-role-safe `Active sessions` consistency (`declared_active_sessions == 0 and active_session_rows > 0`, `active_session_rows > declared_active_sessions`, `declared_active_sessions > 0 and active_session_rows == 0` unless non-issue `tmux` sessions are explicitly listed, or mismatch against an explicit rendered `tmux` session list), and declared `Open PRs` count vs listed open-PR rows when an open-PR table is present, plus conflicting repeated metric declarations within the same dated snapshot section.
      * Flag stale/invalid SHAs: malformed/placeholder/all-zero SHAs (`TBD`, `unknown`, `<sha>`, `0000000`, `<7` hex chars) on top-level `HEAD SHA` / `Origin/main SHA` / `Target/base SHA` metadata fields, conflicting SHA values within the **same** normalized top-level SHA key (`head sha` vs `origin/main sha` vs `target/base sha`, without conflating `origin/main` against a stacked parent `target/base` SHA or per-PR table cells) in the same snapshot section, `Observed UTC` older than `Written UTC` by more than `max_age_minutes` (or observed after `Written UTC`), and mismatches against `expect_head`, `expect_base`, `expect_open_issues`, `expect_open_prs`, or `expect_active_sessions` when supplied.
  * `main(argv: list[str] | None = None) -> int`:
    * Supports `--root`, `--agent`, `--no-agent`, `--handoff` (zero or more Markdown files), `--stdin`, `--expect-head`, `--expect-base`, `--check-git-head`, `--expect-open-issues`, `--expect-open-prs`, `--expect-active-sessions`, `--open-issues`, and `--max-age-minutes`.
* Excluded: Retired path tokens or non-stdlib imports.

#### Likely Targets

* tools/check-coordinator-handoff.py: Full implementation.

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* Direct CLI run `python3 tools/check-coordinator-handoff.py` passes (`0 violation(s)`) and unit tests in `P03-T01` exercise every branch.

#### Completion Evidence

* Clean, Ruff-formatted tools/check-coordinator-handoff.py.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Unit Tests, Ruff Lint/Format, and Mechanical Verification

### Context

Issue #1204 requires focused `unittest` verification in tools/test_check_coordinator_handoff.py plus clean `ruff check` and `ruff format --isolated --line-length 100 --check`, without running tools/rpi-checks.py (`C5`, `C6`, `C7`, `C8`, `C9`).

### Intent

Prove every acceptance criterion (`AC-01` through `AC-06`) with deterministic unit tests, lint/format checks, phase-witness adoption regression check, and HVE-qualified static/trace review artifacts, then commit locally on `fix/delivery-1204-coordinator-guard`.

### Boundaries

* Included: Creating tools/test_check_coordinator_handoff.py (using `self.subTest(...)` grouping per contract family within `<= 16` `test_*` methods), running focused tests and Ruff commands, creating .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md as a required deliverable recording all five coordinator step 6 HVE static/behavior attributes (`exact source identity`, `execution status`, `verdict`, `fidelity`, and `executor or profile limits`) for the post-edit .github/agents/ama-backlog-delivery-coordinator.agent.md SHA-256, updating .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-changes.md, and running `rpi-review` to .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md.
* Excluded: Running `tools/rpi-checks.py`, pushing to remote, or creating a PR.

### Likely Targets

* tools/test_check_coordinator_handoff.py: Focused `unittest` test suite (at most 16 test methods).

### Dependencies

* `P01`, `P02`.

### Validation Expectations

* `python3 -m unittest tools/test_check_coordinator_handoff.py -q` exits `0`.
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`.
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`.
* `python3 -m unittest tools/test_rpi_phase_witness.py -q` and `python3 tools/check-coordinator-handoff.py` exit `0`.
* `git --no-pager diff --check` exits `0`.

### Completion Evidence

* Recorded command outputs and SHA-256 source identities in .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-changes.md and .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Implement tools/test_check_coordinator_handoff.py and Run Focused Validation

#### Context

Dynamic loading via `importlib.util.spec_from_file_location` must register `sys.modules[SPEC.name] = checker` before `SPEC.loader.exec_module(checker)` so Python 3.12 `@dataclass` introspection succeeds cleanly.

#### Intent

Author focused, high-signal unit tests covering both positive and negative paths across agent instructions and handoff/checkpoint Markdown validation.

#### Boundaries

* Included:
  * Group related positive and negative scenarios via `self.subTest(...)` per contract family so the suite stays within `<= 16` focused `test_*` methods while covering every semantic edge case:
  * Live agent contract test: repository .github/agents/ama-backlog-delivery-coordinator.agent.md passes `check_agent_instructions` with zero violations.
  * Agent negative tests (`subTest`s): missing required category (`ready to start`), missing anti-idle/unclassified rule, missing live-refresh command rule, broken relative Markdown link, or missing frontmatter field are each flagged.
  * Valid handoff tests (`subTest`s): (a) active delivery handoff with refreshed live counts/commands (`--limit`), distinct stacked `Origin/main SHA` vs `Target/base SHA`, multi-role `Active sessions: 2` across one `active session` row, and valid five-category classification table passes; (b) legitimate waiting/idle tick summary **preceded** by a complete classification table where all open issues are `active session`, `human-blocked` (with URL/`#issuecomment-` link), or `dependency-blocked` (including hosted-CI/auto-merge PR wait with `Active sessions: 0` and still-open parent-merged stacked child with PR link) passes, as does a waiting summary with `ready to start` rows when at the declared `M/N` session cap or active `open_prs > 15` PR drain; (c) multi-section dated checkpoint file with distinct SHAs per dated entry passes.
  * Classification and link negative tests (`subTest`s): unknown/invalid state (`unknown`, `blocked`), missing link on `human-blocked`, bare same-issue `#1288` self-reference on `human-blocked`, bare same-issue `#1204` self-reference on `dependency-blocked`, and duplicate issue row are flagged.
  * Unsupported idle/waiting negative tests (`subTest`s): `"nothing changed"` without table, classification table placed **after** the idle/waiting summary, `"nothing changed"` / idle summary when declared `Open issues` count or `--open-issues` exceeds classified open issues (or marks an open issue `merged`), `"nothing changed"` / idle when an issue is `ready to start` below cap/drain, and pausing on an unverified blocker are each flagged; negated rule prose and fenced code blocks do not false-trigger.
  * Stale handoff block negative tests (`subTest`s): missing live-command provenance or missing open-issue/open-PR/active-session counts, carry-forward wording (`copied from previous tick`), internal mismatch between `Active sessions: 0` and an `active session` row (or `active_session_rows > Active sessions` or `Open issues` mismatch), placeholder or same-key conflicting `HEAD SHA`, `Observed UTC` older than `Written UTC` beyond `--max-age-minutes`, and `--expect-head` / `--expect-open-issues` CLI mismatches are each flagged.
  * CLI integration test: `main()` returns `0` on valid agent + handoff file and `1` on invalid handoff file.
  * HVE assessment deliverable: write .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md recording exact SHA-256 of post-edit .github/agents/ama-backlog-delivery-coordinator.agent.md, execution status, verdict, fidelity (static + contained trace/validator simulation, qualified as non-native-host runtime), and executor/profile limits.
* Excluded: Redundant getter/constant assertions or network-dependent tests.

#### Likely Targets

* tools/test_check_coordinator_handoff.py: Complete `unittest` suite.

#### Dependencies

* `P01-T01`, `P02-T01`.

#### Validation Expectations

* All three caller-mandated validation commands plus strict Ruff (`E,F,I,B,UP`), `test_rpi_phase_witness.py`, and Markdown mechanical checks pass with exit `0`.

#### Completion Evidence

* Zero-failure test and lint output recorded in .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-changes.md.

#### Unresolved Items

* None.
