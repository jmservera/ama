<!-- markdownlint-disable-file -->

# Task Research: delivery-1204-coordinator-guard

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (RPI Agent automatic loop)                                             |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md   |

## Research Brief

* What to research: Current coordinator liveness, idle-tick, and handoff/checkpoint rules in `.github/agents/ama-backlog-delivery-coordinator.agent.md`, existing coordinator handoff/status artifact patterns in the repository, and deterministic checker/test conventions under `tools/` to design the instruction updates plus `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` for Issue #1204.
* Why it matters: Prevent scheduled coordinator checks from claiming "nothing changed" or pausing on unverified blockers while open issues remain unclassified, enforce an explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before any idle or waiting summary, require live-command refreshes of open-issue counts, open-PR counts, and active session status at handoff/checkpoint write time, and add an offline deterministic validator with focused unit tests.
* Audience or intended use: `rpi-plan`, `rpi-implement`, `rpi-review`, and coordinator exact-head verification for Issue #1204 on branch `fix/delivery-1204-coordinator-guard` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Scope: `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and dated `.copilot-tracking/` RPI and HVE-aligned review artifacts.
* Non-goals: No application edits under `src/`, no cloud deployment, no repository protection or workflow trigger edits, no execution of `tools/rpi-checks.py`, and no `git push` or `gh pr create`.
* Criteria: Prove all four caller acceptance criteria with exact coordinator instruction rules, offline deterministic validation in `tools/check-coordinator-handoff.py`, focused `unittest` coverage in `tools/test_check_coordinator_handoff.py`, clean `ruff check` and `ruff format --isolated --line-length 100 --check`, and repository Markdown style conformance.
* Requested outputs: Synthesized `convergence` recommendation with exact file/section edits, parser/validator schema and CLI contract, edge-case rules, and test matrix ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                      |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How should `.github/agents/ama-backlog-delivery-coordinator.agent.md` and `tools/check-coordinator-handoff.py` enforce live issue-state classification tables, block unsupported idle/waiting summaries, and detect stale handoff count/SHA blocks? |
| Codebase scope                   | `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/*.py`, `pyproject.toml`, `docs/architecture/cutover-evidence-pack.md`, `.copilot-tracking/` |
| External scope                   | none                                                                                                                                       |
| Initial internal candidate areas | `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-legacy-references.py`, `tools/backlog-sync.py`, `.copilot-tracking/` |
| Initial external candidate areas | none                                                                                                                                       |
| Research posture                 | focused                                                                                                                                    |
| Posture provenance               | caller-specified (bounded internal task with named files, acceptance criteria, and focused validation commands)                             |
| Explicit limits / deadline       | Focused validation tier; do NOT run `tools/rpi-checks.py`; do NOT push or open a PR                                                        |
| Posture-specific completion basis| focused scope and materiality: all four acceptance criteria, instruction sections, checker heuristics, and test cases grounded in codebase evidence |
| Edits allowed during research?   | no, research-only                                                                                                                          |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                       |
| Known constraints / excluded sources | Plain ASCII Markdown, `*` unordered lists, no em dashes or bolded-prefix list items in new Markdown; standard-library Python 3.12 + `unittest` |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                   | Match and provenance                                             | Scoped authority or output contract                                         | Selected / skipped reason                                                                 |
|---------------------|---------------------------------------------|------------------------------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`           | `applyTo: "**"` matches all repository and tracking paths        | Adds AMA Markdown style, validation tier rules, and git/commit conventions  | Selected automatically by glob match                                                      |
| Skill               | `hve-builder` / `hve-builder-tester`        | Prompt-engineering artifact authoring/review/testing domain      | Adds frontmatter, static quality, and behavior-scenario criteria for agents | Recorded for Plan/Implement/Review scope; kept read-only during `rpi-research`            |
| Skill               | `python-foundational`                       | Python CLI and `unittest` conventions                            | Standard-library CLI and test structure                                     | Skipped activation in Research; direct `tools/*.py` codebase conventions are authoritative |
| Research specialist | `hve-core-all:rpi-researcher`               | General internal research worker registered in host              | Bounded read-only lane artifact                                             | Skipped dispatch; tightly coupled single-file/tools investigation handled inline per Flow 5.4 |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered | Resulting decision or selected further research                                          |
|------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------------|
| Intake           | Non-interactive automatic session with complete file targets, acceptance criteria, branch/base, and validation commands.   | N/A (non-interactive)| Proceed directly with `focused` posture in `convergence` mode.                           |
| Direction change | No scope or direction ambiguity encountered during Cycle 1.                                                               | N/A (non-interactive)| Keep active brief, target files, and focused validation boundary unchanged.              |
| Convergence      | All 5 research questions answered with exact `path:line` evidence across coordinator instructions and `tools/*.py`.       | N/A (non-interactive)| Stop after Cycle 1 with Planning Readiness `Ready`; proceed to `rpi-plan`.               |

## Scope and Success Criteria

* Scope:Coordinator agent instructions (`.github/agents/ama-backlog-delivery-coordinator.agent.md`) and new standalone checker + unit tests (`tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`).
* Assumptions:
  * Existing coordinator instructions already contain partial `#1204` wording from 2026-11-05 (`ready`, `running`, `dependency-blocked`, `human-blocked`, `unknown`) that must be reconciled cleanly with the explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) and live refresh rules required by Issue #1204's current acceptance criteria without breaking existing coordinator rules.
  * `pyproject.toml` or root Ruff configuration defines lint rules applied when `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` runs.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one convergence recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * AC1: Update delivery coordinator instructions so scheduled checks cannot claim "nothing changed" or pause on an unverified blocker while open issues remain unclassified in the current run.
  * AC2: Require an explicit issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, or `ready to start`) before any idle or waiting summary.
  * AC3: Require handoff and checkpoint notes to refresh open-issue counts, open-PR counts, and active session status from live commands at the time of writing.
  * AC4: Create `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` (`unittest`) validating coordinator handoff/status Markdown and `.github/agents/ama-backlog-delivery-coordinator.agent.md` for required issue-state classification categories (`merged`, `active session`, `human-blocked`, `dependency-blocked`, `ready to start`), rejecting unsupported idle/waiting summaries when unclassified open issues exist, and flagging stale count/SHA handoff blocks.
* Inferred research questions: Q1-Q5 below.
* Caller constraints and non-goals: Focused tier only; do not run `tools/rpi-checks.py`; do not push or open PR; target base `feat/demo-164-chat-grounding-provenance-0900`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                      | Source / checkpoint | Effect on active brief, evidence, or revalidation                          |
|----------------------------------------------------------|------------------------------------------------------------------------------------------------------------|---------------------|----------------------------------------------------------------------------|
| narrow                                                   | Focused validation only (`unittest` + `ruff check` + `ruff format --isolated --line-length 100 --check`)   | Caller intake       | Excludes `tools/rpi-checks.py` execution; verify exact root `ruff` config  |
| exclude                                                  | No `git push` or `gh pr create`; leave clean frozen HEAD on `fix/delivery-1204-coordinator-guard`          | Caller intake       | Constrains Implement/Review closeout to local commits only                 |

## Research Questions

|  # | Sub-question                                                                                                                                          | Type            | Priority | Status |
|---:|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|--------|
| Q1 | Where in `.github/agents/ama-backlog-delivery-coordinator.agent.md` are scheduled-check summaries, idle/stop rules, and handoff/checkpoint notes specified, and what gaps remain against AC1-AC3? | depth           | H        | answered |
| Q2 | What real coordinator handoff, status, and checkpoint Markdown structures exist in the repository (if any), and what stale count/SHA or unsupported idle patterns occur in practice? | breadth         | H        | answered |
| Q3 | What CLI, exit-code, Markdown-parsing, and Ruff/Python conventions do `tools/check-*.py` and `pyproject.toml` enforce?                                | straightforward | H        | answered |
| Q4 | How should `tools/check-coordinator-handoff.py` validate both `.github/agents/ama-backlog-delivery-coordinator.agent.md` and coordinator handoff/status Markdown without false positives or trivial bypasses? | depth           | H        | answered |
| Q5 | Does editing `.github/agents/ama-backlog-delivery-coordinator.agent.md` interact with any existing tests, HVE checks, or target-branch (`feat/demo-164-chat-grounding-provenance-0900`) diffs? | breadth         | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * GitHub Issue `#1204` (`fix(delivery): prevent unsupported idle ticks and stale coordinator handoffs`), `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `.github/copilot-instructions.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `.copilot-tracking/reviews/2026-11-13-demo-permanent-refill-1204-0914-closure.md`, `.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-static-review-1.md`, `.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-validation-1.md`, and `.copilot-tracking/reviews/logs/2026-11-15/delivery-1296-correction-cycles-review.md`.
* Reused (verified) findings:
  * Branch `fix/delivery-1204-coordinator-guard` is checked out at `f74e1bf1fd7d3e62048a69ade51a126704ebc556`, matching `origin/feat/demo-164-chat-grounding-provenance-0900` (PR #1641), with a clean working tree (`C8`).
  * Repository Markdown style rules on `.github/agents/ama-backlog-delivery-coordinator.agent.md` require valid YAML frontmatter (`name`, `description`), resolved relative links, plain ASCII (`ord(c) <= 127`), `*` unordered lists without bolded prefixes, zero em/en dashes, and language-tagged fenced blocks (`C6`, `C7`).
* Superseded / stale:
  * Earlier 2026-11-05 `#1204` prose in `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Liveness and stop decision`, lines 128-235) introduced internal liveness states (`ready`, `running`, `dependency-blocked`, `human-blocked`, `unknown`) but never required an explicit rendered five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before idle/waiting summaries, never explicitly barred pausing on unverified blockers while open issues remain unclassified in the current run in scheduled-check reporting, never mandated live-command refreshes of open-issue counts, open-PR counts, and active session status at handoff/checkpoint write time, and lacked a deterministic validator under `tools/` (`C1`, `C2`, `C3`, `C4`).

## Research Cycle Log

### Cycle 1

* Active direction controls: `narrow` (Focused validation tier without `tools/rpi-checks.py`), `exclude` (no push or PR creation; local frozen commit only)
* Active research posture and completion basis: `focused`; all four caller acceptance criteria, coordinator sections, validator checks, and unit test edge cases grounded in primary repository evidence
* Explicit limits or deadline effect: Single-session non-interactive execution; offline standard-library validator and unit tests only

#### Wave 1: Wider

* Plan and independent lanes: Inspect `.github/agents/ama-backlog-delivery-coordinator.agent.md` end-to-end (lines 1-1048), enumerate `tools/*.py` checkers and tests, check `.github/workflows/src-ci.yml` path triggers, grep repository references to `ama-backlog-delivery-coordinator`, and inspect recent `2026-11-15` delivery/HVE artifacts.
* Worker evidence relationships or inline fallback: Inline investigation mapped coordinator rules across `Liveness and stop decision` (`C1`), `Recurring schedules` (`C2`), `Stabilization checkpoints` (`C3`), step 5 scheduled-check summaries and `Final report` (`C4`), `tools/check-legacy-references.py` and `tools/backlog-sync.py` conventions (`C5`), HVE/Markdown rules (`C6`, `C7`), and existing `tools/test_rpi_*.py` adoption assertions (`C9`).
* Reflection: Confirmed `tools/check-coordinator-handoff.py` is outside `src-ci.yml` trigger paths (`C8`), making focused local execution essential. Identified exact gaps between internal liveness states (`ready`, `running`, `unknown`) and the required five-category rendered issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Q1, Q3, Q4, and Q5 -- reconcile the five canonical table categories cleanly with internal coordinator liveness states, verify `tools/test_rpi_phase_witness.py` invariants (`C9`), check Ruff settings (`E,F,I,B,UP`, `py312`, line length `100` in `src/core/pyproject.toml` plus bare root `ruff check`), and specify deterministic Markdown parsing for `tools/check-coordinator-handoff.py`.
* Plan and independent lanes: Read `Liveness and stop decision` (lines 128-265), `Stabilization checkpoints` (lines 475-545), step 5 check summary rules (lines 825-865), `Boundaries` / `Final report` (lines 1025-1048), `tools/test_rpi_checks.py` (lines 2381-2396), `tools/test_rpi_phase_witness.py` (lines 610-627), and `src/core/pyproject.toml` (lines 25-35).
* Worker evidence relationships or inline fallback: Inline inspection confirmed:
  * `tools/test_rpi_phase_witness.py:611-624` asserts that `.github/agents/ama-backlog-delivery-coordinator.agent.md` retains `"tools/rpi_phase_witness.py record launch"`, `"tools/rpi_phase_witness.py verify"`, and `"--evidence-dir"` (`C9`).
  * Mapping internal liveness labels to the rendered classification table is clean and lossless: `merged` (delivered/merged in run or backlog), `active session` (verified live `tmux` `rpi-*` session, internal `running`), `human-blocked` with concrete issue/comment/gate link, `dependency-blocked` with concrete blocking issue/PR link, and `ready to start` (actionable work, internal `ready`); any `unknown` / `unassessed` / unclassified open issue must be inspected and resolved before emitting any idle, waiting, `"nothing changed"`, or pause summary (`C1`, `C4`).
  * Handoff and checkpoint notes must refresh open-issue counts (`gh issue list --state open`), open-PR counts (`gh pr list --state open`), active session status (`tmux list-sessions`), and exact `HEAD` / base SHAs (`git rev-parse`) at write time (`C3`, `C4`).
* Reflection: Clear specification obtained for both the agent instruction edits and the checker CLI/library functions. Proceed to Wave 3 contrarian testing to eliminate bypasses and false positives.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge naive regex/table checks in `tools/check-coordinator-handoff.py` and potential runtime/import pitfalls in `tools/test_check_coordinator_handoff.py`.
* Plan and independent lanes:
  1. Test self-link false pass on `human-blocked` / `dependency-blocked` rows where column 1 already contains the row's own `#1204` issue number.
  2. Test normative negation sentences (e.g. `"Scheduled checks cannot claim 'nothing changed'"`) vs actual coordinator idle/waiting claims, and fenced code blocks containing illustrative snippets.
  3. Test dynamic `importlib.util.spec_from_file_location` loading with `@dataclass` on Python 3.12 (`sys.modules[SPEC.name] = mod` required before `exec_module`) and `check-legacy-references.py` retired-path tokens (`C5`).
  4. Test how stale count/SHA handoff blocks manifest offline without live GitHub network access (carry-forward wording, missing live-command provenance, timestamp skew where snapshot/observed timestamp precedes handoff write timestamp beyond threshold, conflicting counts/SHAs across header vs classification/PR/session tables, placeholder/short SHAs, and optional CLI `--expect-*` / `--check-git-head` overrides).
* Worker evidence relationships or inline fallback: Inline contrarian analysis resolved all four risks:
  1. Require the blocker/dependency link in non-issue columns (state, blocker, link, or evidence cells), and for `dependency-blocked` reject rows whose only `#N` reference equals the row's own issue `#N` without a distinct issue/PR/URL reference.
  2. Strip fenced code blocks before table/claim scanning and ignore sentences gated by normative/prohibitive markers (`cannot`, `must not`, `never`, `do not`, `forbid`, `permitted only when`, `reject`) when scanning prose for idle/waiting claims.
  3. Register `sys.modules[SPEC.name]` before `exec_module` and avoid any retired path strings (`C5`).
  4. Combine offline structural/internal staleness checks (carry-forward phrases, missing live-command refresh fields, count mismatches between handoff summary and classification/session/PR rows, conflicting or placeholder SHAs, and `observed_at` vs `written_at` staleness skew) with optional explicit `--expect-head`, `--expect-base`, `--expect-open-issues`, `--expect-open-prs`, `--expect-active-sessions`, and `--open-issues` flags.
* Reflection: Contrarian checks materially strengthened link validation, prose negation handling, and offline stale-handoff detection without adding external dependencies.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|----------------------------|
| Add explicit five-category issue-state classification table rule (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) and anti-idle / unverified-blocker guard to `Liveness and stop decision`, `Recurring schedules`, and step 5 check summary | `C1`, `C2`, `C4` | accepted | Directly satisfies AC1 and AC2 while keeping connected coordinator gates aligned | Selected recommendation (`P01`) |
| Require live-command refreshes of open-issue counts, open-PR counts, active session status, and exact SHAs at write time across handoff notes, `Stabilization checkpoints`, step 5 check summaries, and `Final report` | `C3`, `C4`, `C6` | accepted | Directly satisfies AC3 across every handoff and checkpoint surface | Selected recommendation (`P01`) |
| Implement standalone standard-library `tools/check-coordinator-handoff.py` validating both `.github/agents/ama-backlog-delivery-coordinator.agent.md` and coordinator handoff/status Markdown artifacts, paired with `unittest` suite `tools/test_check_coordinator_handoff.py` | `C5`, `C7`, `C8`, `C9` | accepted | Directly satisfies AC4 with fast deterministic offline tests and Ruff conformance | Selected recommendation (`P02`, `P03`) |
| Require live `gh` network calls inside `tools/check-coordinator-handoff.py` default runs | `C5`, `C8` | rejected | Offline unit tests and pre-commit checks must stay deterministic, fast, and credential-free | Rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: `focused` scope fully covered; every research question Q1-Q5 is answered with primary codebase evidence and contrarian edge cases are resolved.
* Revised brief or revalidation required: none
* Readiness effect: `Ready` for `rpi-plan`

## Evidence Log

* Delegation: inline: bounded single-agent instruction file plus standalone `tools/` checker and `unittest` suite (`focused` posture; zero independent external uncertainties)

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `Liveness and stop decision` classifies items internally as `ready`, `running`, `dependency-blocked`, `human-blocked`, or `unknown` (`134-147`) and gates `"Nothing changed"` (`218-235`), but does not require a rendered five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) or explicitly forbid pausing on an unverified blocker while open issues remain unclassified in the current run. | `.github/agents/ama-backlog-delivery-coordinator.agent.md:128` | view | high | Lines 128-235 inspected |
| C2 | `Recurring schedules` defines the 10-30 minute delivery check and hourly cleanup check (`251-284`), stating neither is a status-only poll, without referencing the mandatory classification table or live-refresh handoff check. | `.github/agents/ama-backlog-delivery-coordinator.agent.md:251` | view | high | Lines 251-284 inspected |
| C3 | `Stabilization checkpoints` requires dated records in `docs/architecture/cutover-evidence-pack.md` with freshly resolved `origin/main` SHA (`496-505`), but does not explicitly require refreshing open-issue counts, open-PR counts, and active session status from live commands at write time. | `.github/agents/ama-backlog-delivery-coordinator.agent.md:475` | view | high | Lines 475-542 inspected |
| C4 | Step 5 scheduled-check summary (`838-851`) and `Final report` (`1038-1048`) define end-of-check `"When nothing changed"` prose and wave reporting, where explicit five-category table ordering before idle/waiting summaries and live-command count/session/SHA refresh rules must also align. | `.github/agents/ama-backlog-delivery-coordinator.agent.md:838` | view | high | Lines 838-851 and 1038-1048 inspected |
| C5 | Existing `tools/check-legacy-references.py` and `tools/test_check_legacy_references.py` establish repo conventions for hyphenated CLI checkers: `argparse`, exit `0` pass / `1` violations, fence-aware Markdown scanning, `importlib.util.spec_from_file_location` test loading, and avoiding retired path literals without archive tags. | `tools/check-legacy-references.py:1` | view | high | Also verified via `python3 -m unittest` |
| C6 | Repository instructions define AMA Markdown rules (`*` unordered lists, plain ASCII, zero em dashes, zero bolded-prefix list items, language-tagged code fences) and Focused validation tier rules (`D4` / `#1294`). | `.github/copilot-instructions.md:85` | view | high | Lines 85-115 and 330-350 inspected |
| C7 | Recent HVE mechanical validation and Ruff config enforce clean YAML frontmatter (`name`, `description`), resolved relative links, `ord(c) <= 127` ASCII, `target-version = "py312"`, `line-length = 100`, and lint rules `E, F, I, B, UP`. | `src/core/pyproject.toml:25` | view | high | Paired with `.copilot-tracking/hve-builder/2026-11-15/coordinator-instructions-validation-1.md:29` |
| C8 | `Source projects CI` (`src-ci.yml`) path filter lists named `tools/` scripts (`rpi-checks.py`, `ci-affected.py`, `install-actionlint.py`, `backlog-sync.py`, `rename-zava*`); `tools/check-coordinator-handoff.py` is a focused local check, and `HEAD` (`f74e1bf1f`) matches `origin/feat/demo-164-chat-grounding-provenance-0900`. | `.github/workflows/src-ci.yml:4` | view | high | Verified via `git rev-parse` |
| C9 | `tools/test_rpi_phase_witness.py` asserts `.github/agents/ama-backlog-delivery-coordinator.agent.md` contains `tools/rpi_phase_witness.py record launch`, `tools/rpi_phase_witness.py verify`, and `--evidence-dir`; `tools/test_rpi_checks.py` maps the agent file to `preflight`, `namespace`, and `static`. | `tools/test_rpi_phase_witness.py:611` | grep | high | Must preserve step 5 witness strings intact |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* Internal liveness labels (`ready`, `running`, `dependency-blocked`, `human-blocked`, `unknown`) in `.github/agents/ama-backlog-delivery-coordinator.agent.md:134-147` (`C1`) vs rendered five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) required by Issue #1204 AC2/AC4; resolved by keeping `unknown` / `unassessed` as mandatory same-tick investigation states that forbid emitting an idle/waiting summary, and mapping classified issues into the five required table categories (`merged`, `active session` for live `running` `tmux` sessions, `human-blocked` with link, `dependency-blocked` with link, `ready to start` for `ready` work) before any idle, waiting, `"nothing changed"`, or handoff summary.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | Scheduled-check liveness, `"nothing changed"`, checkpoint, and handoff rules span `Liveness and stop decision` (`128-235`), `Recurring schedules` (`251-284`), `Stabilization checkpoints` (`475-542`), step 5 (`838-851`), and `Final report` (`1038-1048`); all five connected locations should agree on AC1-AC3. | `C1`, `C2`, `C3`, `C4` | high | Plan surgical, internally consistent edits across those coordinator sections (`P01`). |
| Q2 | Coordinator handoff/status/checkpoint artifacts record open-issue counts, open-PR counts, active `tmux` sessions, pinned `HEAD` / base SHAs, per-issue classification tables, and end-of-check status summaries; stale handoffs copy earlier counts/SHAs/timestamps or assert global human-blocked idle states while open issues remain unclassified or `ready to start`. | `C1`, `C3`, `C4` | high | Validator must check classification categories + links, summary ordering, unclassified open-issue mismatches, `ready to start` idle contradictions, and stale count/SHA/timestamp blocks (`P02`). |
| Q3 | `tools/check-*.py` uses standard-library `argparse`, `Path`, `re`, exit `0`/`1`, `importlib.util.spec_from_file_location` in `tools/test_*.py`, Python 3.12 typing, and Ruff `E,F,I,B,UP` with 100-char line length. | `C5`, `C7` | high | Match exact `tools/` CLI, typing, and Ruff formatting conventions (`P02`, `P03`). |
| Q4 | Stripping fenced code blocks, requiring non-self links in non-issue cells for `human-blocked` and `dependency-blocked`, guarding normative negations on prose claims, verifying table-before-summary order, checking open-issue count/list coverage, and flagging stale/conflicting/unprovenanced count and SHA blocks gives high-precision offline validation. | `C1`, `C4`, `C5` | high | Incorporate all contrarian safeguards into `tools/check-coordinator-handoff.py` and unit tests (`P02`, `P03`). |
| Q5 | Preserving YAML frontmatter, existing relative links, plain ASCII, `*` list markers, and step 5 `rpi_phase_witness.py` invocations keeps all existing tests (`test_rpi_phase_witness.py`, `test_rpi_checks.py`) and HVE mechanical checks passing. | `C6`, `C7`, `C8`, `C9` | high | Include `test_rpi_phase_witness.py` and mechanical/ASCII/link checks alongside required validation commands (`P03`). |

## Key Discoveries

* `.github/agents/ama-backlog-delivery-coordinator.agent.md` needs coordinated updates in `Liveness and stop decision` (new explicit subsection `### Issue-state classification table and live handoff refresh`), `Recurring schedules`, `Stabilization checkpoints`, step 5 end-of-check status summary, and `Final report` so connected stage gates never diverge (`C1`-`C4`).
* Requiring non-issue-column links on `human-blocked` and `dependency-blocked` rows closes a subtle false-pass loophole where the row's own `#<issue>` identifier in column 1 would otherwise look like a blocker link (`C1`, `C5`).
* Offline stale-handoff detection can deterministically catch four concrete defect classes without network calls: (1) missing live-command refresh metrics/provenance (`open issues`, `open PRs`, `active sessions`), (2) carry-forward/stale wording or `observed_at` vs `written_at` timestamp skew, (3) internal count mismatches between summary counts and classification/PR/session rows, and (4) invalid, placeholder, conflicting, or `--expect-head`/`--expect-base`-mismatched SHAs (`C3`, `C4`, `C5`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach:
  1. Surgically update `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Liveness and stop decision`, `Recurring schedules`, `Stabilization checkpoints`, step 5 check summary, and `Final report`) to forbid claiming `"nothing changed"` or pausing on an unverified blocker while open issues remain unclassified in the current run, mandate a preceding explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before any idle or waiting summary, require handoff and checkpoint notes to refresh open-issue counts, open-PR counts, active session status, and exact SHAs from live commands at write time, and reference `python3 tools/check-coordinator-handoff.py`.
  2. Implement `tools/check-coordinator-handoff.py` (standard library only, Python 3.12, Ruff-clean at line length 100) exposing clean library functions (`check_agent_instructions`, `check_handoff_text`, `check_handoff_file`, `main`) that validate both `.github/agents/ama-backlog-delivery-coordinator.agent.md` and coordinator handoff/status/checkpoint Markdown files.
  3. Implement `tools/test_check_coordinator_handoff.py` using `unittest` covering the live repository agent file, valid active and valid fully-classified waiting/blocked handoffs, missing/reordered classification tables, missing categories in agent instructions, missing links or self-only `#N` on `human-blocked` / `dependency-blocked` rows, unsupported `"nothing changed"` / idle / unverified-blocker pause summaries when open issues are unclassified or `ready to start`, and stale count/SHA/timestamp/carry-forward handoff blocks plus CLI exit codes.
* Rationale: Proves every acceptance criterion (AC1-AC4) deterministically offline with zero external dependencies, preserves all existing coordinator gates (`#1296`, `#1783`, `#1294`, `rpi_phase_witness.py`), and satisfies HVE static/trace and AMA Markdown standards.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`
* Implementation impact: Modifies `.github/agents/ama-backlog-delivery-coordinator.agent.md`; creates `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and dated `.copilot-tracking/` RPI artifacts.
* Confidence: `high`: all target files, style rules, and validation commands are verified locally.

File tree:

```text
.github/agents/
  ama-backlog-delivery-coordinator.agent.md   (modify)
tools/
  check-coordinator-handoff.py                (create)
  test_check_coordinator_handoff.py           (create)
.copilot-tracking/
  research/2026-11-15/delivery-1204-coordinator-guard-research.md
  plans/2026-11-15/delivery-1204-coordinator-guard-plan.md
  details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md
  changes/2026-11-15/delivery-1204-coordinator-guard-changes.md
  reviews/2026-11-15/delivery-1204-coordinator-guard-plan-critique.md
  reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md
  reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md
  rpi-sessions/2026-11-15/delivery-1204-coordinator-guard-state.json
```

### Alternative: Prose-Only Coordinator Update with Regex Smoke Test Only on `.agent.md`

* Approach: Edit `.github/agents/ama-backlog-delivery-coordinator.agent.md` and write a minimal test checking only substring presence in the `.agent.md` file without parsing coordinator handoff/status Markdown tables, idle claims, or stale count/SHA blocks.
* Trade-offs: Faster to write, but fails AC4's explicit requirement to validate coordinator handoff/status Markdown, reject unsupported idle/waiting summaries when unclassified open issues exist, and flag stale count/SHA handoff blocks.
* Evidence refs: `C1`, `C4`, `C5`
* Rejection rationale: Incomplete against AC4 and provides no reusable validation utility for coordinator handoff artifacts.

### Alternative: Live GitHub CLI (`gh`) Polling Inside Default Validator Execution

* Approach: Make `tools/check-coordinator-handoff.py` invoke `gh issue list` and `gh pr list` unconditionally on every invocation.
* Trade-offs: Compares directly against remote GitHub state, but breaks offline determinism, requires network/auth tokens in unit tests, and introduces race conditions when GitHub state changes mid-test.
* Evidence refs: `C5`, `C8`
* Rejection rationale: Offline structural, internal-consistency, timestamp-skew, and optional `--expect-*` CLI parameter validation keeps unit tests deterministic and offline while still supporting live coordinator invocations passing current CLI expectations.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure `tools/check-coordinator-handoff.py` is not automatically triggered by `src-ci.yml` unless explicitly invoked or added in a future CI workflow update; document local execution clearly (`C8`).
* Follow-up: Consider wiring `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static checks in a separate gate-tooling PR if the owner later wants full-gate enforcement.
* Residual uncertainty: Static/trace verification and offline unit tests prove prompt contract rules and Markdown artifact validation deterministically, whereas live multi-tick `tmux` schedule execution remains runtime coordinator behavior outside this focused offline worker session (`C6`, `C7`).

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------||-----------|--------------|--------------|
| D-1204-1: Enforce explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before any idle or waiting summary, and forbid `"nothing changed"` or unverified-blocker pauses while open issues remain unclassified | confirmed | Caller AC1 & AC2; `C1`, `C2`, `C4` | Eliminates unsupported idle ticks and unverified global blocker claims across connected coordinator sections | `C1`, `C2`, `C4` | Update `Liveness and stop decision`, `Recurring schedules`, and step 5 status summary rules |
| D-1204-2: Require handoff and checkpoint notes to refresh open-issue counts, open-PR counts, active session status, and exact SHAs from live commands at write time | confirmed | Caller AC3; `C3`, `C4` | Prevents stale copied counts, zombie session status, and outdated base/HEAD SHAs in handoffs and checkpoints | `C3`, `C4` | Update `Liveness and stop decision`, `Stabilization checkpoints`, step 5, and `Final report` |
| D-1204-3: Implement offline standard-library `tools/check-coordinator-handoff.py` and `unittest` suite `tools/test_check_coordinator_handoff.py` | confirmed | Caller AC4; `C5`, `C7`, `C8` | Provides deterministic validation of both `.agent.md` rules and coordinator handoff/status Markdown artifacts | `C5`, `C7`, `C8` | Validate with `unittest`, `ruff check`, and `ruff format --isolated --line-length 100 --check` |
| D-1204-4: Preserve existing coordinator controls (`#1296` correction cycles, `2026-11-15` local-before-PR rule, `rpi_phase_witness.py` commands, and AMA Markdown style) | confirmed | Repository constraints; `C6`, `C7`, `C9` | Prevents regressions in adjacent coordinator gates and `test_rpi_phase_witness.py` | `C6`, `C7`, `C9` | Verify with `test_rpi_phase_witness.py` and mechanical frontmatter/link/ASCII checks |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none | none | none | none | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Evaluate adding `tools/check-coordinator-handoff.py` to `tools/rpi-checks.py` static group | Automates coordinator-agent contract check during full-gate runs | Separate gate-tooling issue approved by owner | deferred | Q5; `C8`, `C9` |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected (`D-1204-1` through `D-1204-4`).
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`
* Preconditions met: All target sections, parser invariants, contrarian edge cases, style constraints, and focused validation commands verified.
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field | Record |
|-------|--------|
| Research execution status | Complete |
| Completed waves | Wider, Deeper, and Contrarian completed in order for Cycle 1 |
| Lane evidence or inline fallback | Inline investigation across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/*.py`, `.github/workflows/src-ci.yml`, and `.copilot-tracking/` (`focused` posture) |
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C9`) |
| Blockers | none |
| Continuation owner and state | confirmed automatic RPI Agent; automatic continuation to `rpi-plan` |

## Advisory Next Step

| Field | Record |
|-------|--------|
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C9`) |
| Output mode and planning support | `convergence`; yes, Planning Readiness is `Ready` |
| Acting owner | confirmed automatic RPI Agent |
| Required gates or confirmations | Research disposition recorded (`passed`), Planning Readiness `Ready` (`passed`), three-wave cycle complete (`passed`), pre-transition state write (`passed`) |
| Continuation result | automatic continuation to `Plan` (`rpi-plan`) |
| Primary evidence file | .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md |
| Notes for planning or re-entry | Structure plan into three bounded phases: `P01` coordinator instruction updates (`.agent.md`), `P02` `tools/check-coordinator-handoff.py` implementation, and `P03` `tools/test_check_coordinator_handoff.py` unit tests + focused Ruff/mechanical/HVE validation. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All four acceptance criteria and contrarian edge cases are fully resolved from primary repository evidence (`C1`-`C9`); further codebase sweeps would be redundant.

## Sources

No external sources used.

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
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources.
* Missing or limited sections: none

