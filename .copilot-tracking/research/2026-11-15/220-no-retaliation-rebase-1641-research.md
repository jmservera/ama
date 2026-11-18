---
title: "Task Research: 220-no-retaliation-rebase-1641"
description: "RPI research artifact for rebasing feat/ai-220-no-retaliation (1a626f1c1) onto origin/feat/demo-164-chat-grounding-provenance-0900 (ad005cd5f, PR #1641) and verifying Issue #220 non-retaliation invariants"
ms.date: 2026-11-15
---

| Field | Value |
| --- | --- |
| Date | 2026-11-15 |
| Researcher / agent | rpi-research (via RPI Agent automatic mode) |
| Status | Complete |
| Research disposition | executed |
| Planning Readiness | Ready |
| Artifact path | .copilot-tracking/research/2026-11-15/220-no-retaliation-rebase-1641-research.md |

## Research Brief

* What to research: Branch topology, 3-way merge overlap, cross-feature semantic interactions, module/selector naming contracts, and `src-ci.yml` Focused Tier validation requirements for rebasing `feat/ai-220-no-retaliation` (`1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f`, updated head of parent `PR #1641`).
* Why it matters: Parent `PR #1641` (`origin/feat/demo-164-chat-grounding-provenance-0900`) advanced by 6 sibling commits (`704c6b07a..ad005cd5f`: `#1775`, `#1777`, `#1778`, `#1779`, `#1780`, `#1782`, `#1783`) since `feat/ai-220-no-retaliation`'s merge-base `fa6f8d1dd`. Rebasing without inspecting semantic interactions in `assistants.py`, `release_support.py`, `ai_registry.py`, and `src/core/README.md`, or ignoring the caller's exact validation module selector (`test_no_retaliation_guard_220` / `no_retaliation_guard.py`), risks silent semantic drift or selector `ModuleNotFoundError`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in this automatic RPI continuation loop, plus `PR #1641` stack integration.
* Scope: Git commit range `fa6f8d1dd..1a626f1c1` vs `fa6f8d1dd..ad005cd5f`, `src/core/` and `src/api/` `#220` modules and test suites, `.github/workflows/src-ci.yml`, and `.copilot-tracking/` evidence.
* Non-goals: Pushing to `origin`, modifying `src/api/src/zava_forward/api/web/role-screens.js`, mutating shared `~/.local` editable installs across sibling worktrees, or running full container/live-SQL gates.
* Criteria: Zero merge conflicts or lost hunks on either `PR #1641` sibling commits or `#220` commits; exact caller command (`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`) and full `#220` `src/core` + `src/api` Focused Tier checks pass with exit `0`; clean local commit with Copilot trailer and clean worktree without pushing.
* Requested outputs: Three-wave synthesis (`C1`–`C9`), convergence recommendation, and planning readiness decision.
* Output mode: convergence

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | Q1–Q4 below |
| Codebase scope | `src/core/`, `src/api/`, `.github/workflows/src-ci.yml`, `.copilot-tracking/*/2026-11-15/220-no-retaliation*` |
| External scope | none |
| Research posture | focused |
| Posture provenance | default for bounded internal branch rebase continuation with named commits, parent branch, and explicit validation command |
| Explicit limits / deadline | Focused validation tier matching `src-ci.yml`; clean worktree without `git push` |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | Shared non-sandboxed host with active sibling worktrees: never overwrite shared `~/.local` editable installs; keep `web/role-screens.js` untouched; keep `.copilot-tracking/` paths out of production code, docstrings, and commit messages |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; `rpi-research` contract; domain skills and specialists; examples and preferences.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches workspace | Enforces KB/case-study context, Focused Tier validation (`#1294`), privacy-safe git email, Copilot commit trailer, no-push safety | Selected: mandatory repository governance |
| Skill | `rpi-research` | Active RPI continuation phase 1 | Three-wave cycle (`Wider` -> `Deeper` -> `Contrarian`), `C#` `path:line` evidence, convergence synthesis | Selected: canonical RPI research skill |
| Skill | `web-design-guidelines` | Web UI edits only | Pre-edit and review checklist for modified web files | Skipped: no web files (`web/*.js`, `web/*.html`) change in this rebase continuation |
| Specialist | `hve-core-all:rpi-researcher` | General delegated lane worker | Independent subagent lane artifact | Skipped (inline fallback): 2-commit git topology and 2-file auto-merge inspection fit cleanly in direct inline reads |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
| --- | --- | --- | --- |
| Intake | Non-interactive CLI session with explicit branch, commit SHA `1a626f1c1`, parent branch `origin/feat/demo-164-chat-grounding-provenance-0900`, validation command, and no-push instruction | Supplied in caller prompt | Execute focused Cycle 1 research and automatic RPI continuation |
| Convergence | Cycle 1 completed Wider, Deeper, and Contrarian waves with exact git merge-tree and codebase evidence | Converged | Select Option A (clean rebase onto `ad005cd5f` + thin typed `no_retaliation_guard.py` and `test_no_retaliation_guard_220.py` facade/alias modules + core & API Focused Tier validation) |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| ---: | --- | --- | --- | --- |
| Q1 | What commits separate `feat/ai-220-no-retaliation` (`1a626f1c1`) from `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f`), and do any files conflict during 3-way rebase? | breadth | H | answered |
| Q2 | Do the 6 new upstream sibling commits (`704c6b07a..ad005cd5f`) introduce any semantic or runtime contract change affecting `#220` (`assistants.py`, `release_support.py`, `src/core/README.md`, `ai_tasks.py`, `challenges.py`, `resident_decisions.py`, or `src/api`)? | depth | H | answered |
| Q3 | How do the caller-named paths/selectors (`no_retaliation_guard.py`, `test_no_retaliation_guard_220`) relate to the committed `#220` files (`challenges.py`, `test_challenge_no_retaliation_220.py`, `test_challenge_no_retaliation_api_220.py`)? | contrarian | H | answered |
| Q4 | How should Focused Tier validation matching `src-ci.yml` execute across `src/core` and `src/api` without mutating shared host `~/.local` packages? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `.copilot-tracking/research/2026-11-15/220-no-retaliation-research.md`, `.copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md`, `.copilot-tracking/changes/2026-11-15/220-no-retaliation-changes.md`, `.copilot-tracking/reviews/2026-11-15/220-no-retaliation-review.md`, and sibling PR `#1641` rebase records (`215-rebase-1641-0511-research.md`, `ux-76-hazard-clock-owner-c2-rebase-research.md`).
* Reused (verified) findings: Verified directly on `1a626f1c1` that `#220` Criterion 5 implementation (`b67bd2a94`) and `#76` hazard-projection test alignment (`1a626f1c1`) sit directly atop `fa6f8d1dd` (`#1774`).
* New delta requiring investigation: `origin/feat/demo-164-chat-grounding-provenance-0900` advanced from `fa6f8d1dd` to `ad005cd5f` (`6` commits), and the caller validation command invokes `python3 -m unittest test_no_retaliation_guard_220 -q`.

## Cycle 1 Execution (Wider -> Deeper -> Contrarian)

### Wider Wave

* Fetched `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f`) and inspected `fa6f8d1dd..1a626f1c1` (`2` commits on `feat/ai-220-no-retaliation`: `b67bd2a94` and `1a626f1c1`) against `fa6f8d1dd..ad005cd5f` (`6` commits on parent `PR #1641`: `704c6b07a` `#1775` sensor non-authority, `6bdcf7f90` `#1777` simulator run controls, `e282dc327` `#1778` monitoring harm declarations, `2c5402f9a` `#1779` bounded AI invariants, `3aacab3a6` `#1780` reproducible sensor analysis receipts, `0358b9ad5` `#1782` RAI cohort/paired equity controls, and `ad005cd5f` `#1783` coordinator/instructions docs) (`C1`, `C2`).
* Executed read-only `git merge-tree --write-tree --messages HEAD origin/feat/demo-164-chat-grounding-provenance-0900`: exited `0` (`96c66508cfce483f75de58889d3e37dd4b5a4e44`), auto-merging the only two overlapping files (`src/core/README.md` and `src/core/src/zava_forward/core/assistants.py`) with zero conflicts (`C2`).

### Deeper Wave

* Inspected the two overlapping files line by line (`C3`, `C4`):
  * In `src/core/src/zava_forward/core/assistants.py`, upstream `#1778` (`e282dc327`) added `monitoring_status=monitoring_coverage.check_monitoring_declaration(...)` inside `Assistants.catalog()` (`lines 1579–1619`), whereas `#220` (`b67bd2a94`) added challenge state projection in `_view()`, sensor challenge-note redaction in `_withhold_sensors()`, and `Assistants.challenge()` in disjoint methods. Zero method overlap exists (`C3`).
  * In `src/core/README.md`, upstream `#1782` (`0358b9ad5`) updated the `#222/#128` cohort evaluator and `paired_equity.evaluate` subsections (`lines 444–468` and `1057–1070`), whereas `#220` (`b67bd2a94`) updated the `#220` affected-person challenge status record in a disjoint section (`C4`).
* Inspected upstream `#1778` (`e282dc327`) changes to `rai_release.py` and `src/core/tests/release_support.py` (`C5`): `#1778` made `monitoring_declaration` mandatory on serving-release records and updated `release_support.fixture(...)` (`src/core/tests/release_support.py:12-35`) to populate `monitoring_declaration` automatically. Both `src/core/tests/test_challenge_no_retaliation_220.py:863` and `src/api/tests/test_challenge_no_retaliation_api_220.py` install release fixtures via `RELEASE_SUPPORT.install(self.store)`, so rebased `#220` assistant proposal challenge tests remain 100% compatible with `#1778` and `#1779` (`C5`).
* Inspected `.github/workflows/src-ci.yml` (`lines 69–98`) and `pyproject.toml` (`src/core/pyproject.toml:30-75`, `src/api/pyproject.toml:33-85`) (`C6`, `C7`):
  * `src/core` runs `unittest`, `ruff check`, `ruff format --check`, and `mypy` (`strict = true`) cleanly with both `/usr/bin/python3` (`PYTHONPATH=src:tests`) and editable installs (`C6`).
  * `src/api` requires editable `src/core`, `src/agents`, and `src/api` distributions in an isolated workspace-local scratch venv (`.venv-220-rebase` with `--system-site-packages` + tail `zzz_user_site_fallback.pth`, deleted immediately after validation) so `mypy` resolves `zava_forward.agents.*` without touching shared `~/.local` site-packages used by concurrent worktrees (`C7`).

### Contrarian Wave

* Tested the exact caller command from Task 2 (`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`) against the committed `#220` tree (`C8`, `C9`):
  * **Material selector discovery (`C8`):** Commit `b67bd2a94` implemented the non-retaliation guard inside `src/core/src/zava_forward/core/challenges.py` (`FORBIDDEN_ADVERSE_FIELDS`, `NOT_INFERRED`, `SAFEGUARDS`, `ChallengeSafeguardError`, `assert_no_adverse_challenge_effects`, `build_non_retaliation_assurance`) and named the core test suite `src/core/tests/test_challenge_no_retaliation_220.py` (with API suite `src/api/tests/test_challenge_no_retaliation_api_220.py`). Because `python3 -m unittest test_no_retaliation_guard_220 -q` imports module `test_no_retaliation_guard_220` directly rather than running pattern discovery, omitting `src/core/tests/test_no_retaliation_guard_220.py` causes `ModuleNotFoundError` (`exit=1`) on the exact caller validation command and any post-run coordinator verification.
  * **Pattern check against repository conventions (`C9`):** Existing `#215` tests (`src/api/tests/test_alert_chat_keyboard_provenance.py:1-15` and `215-rebase-1641-0511`) solve this exact coordinator module-selector contract via thin, strictly typed re-export alias modules without duplicating production logic or tests, and `src/core/tests/test_dependency_rule.py:27-33` permits any internal `zava_forward.core.*` import (`ALLOWED = {"core"}`).
  * **Alternative B (Rejected — Rename `challenges.py` or `test_challenge_no_retaliation_220.py`):** Rejected because `challenges.py` is imported across `resident_decisions.py`, `assistants.py`, `test_challenges.py`, `test_issue_220_challenge_route.py`, `test_challenge_no_retaliation_220.py`, and `test_challenge_no_retaliation_api_220.py`, and `src/core/README.md` documents `test_challenge_no_retaliation_220.py`.
  * **Option A (Selected — Thin typed facade + test alias modules alongside canonical `#220` modules):** Add `src/core/src/zava_forward/core/no_retaliation_guard.py` (re-exporting the canonical guard symbols from `zava_forward.core.challenges`) and `src/core/tests/test_no_retaliation_guard_220.py` (re-exporting the 3 `unittest.TestCase` suites from `test_challenge_no_retaliation_220` plus a focused `NoRetaliationGuardFacadeTests` export parity check). Both the literal caller command (`test_no_retaliation_guard_220`) and `unittest discover` in `src/core` and `src/api` pass cleanly with zero logic duplication.

## Canonical Evidence Register

* `C1` (`.github/copilot-instructions.md:62-95`): Repository validation governance defines the Focused Tier for bounded module/rebase continuations (`unittest`, `ruff`, `mypy`, affected component checks, and explicit note when hosted CI is unobserved due to `Do not push`).
* `C2` (`src/core/README.md:444`, `src/core/src/zava_forward/core/assistants.py:1579`): `git merge-tree --write-tree HEAD origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f`) exits `0` with clean auto-merges in `src/core/README.md` and `src/core/src/zava_forward/core/assistants.py`.
* `C3` (`src/core/src/zava_forward/core/assistants.py:1579-1620`): Upstream `#1778` (`e282dc327`) edits `Assistants.catalog()` only, disjoint from `#220`'s `_view()`, `_withhold_sensors()`, and `Assistants.challenge()`.
* `C4` (`src/core/README.md:441-470`, `src/core/README.md:1057-1070`): Upstream `#1782` (`0358b9ad5`) edits `#222/#128` cohort and `paired_equity` sections only, disjoint from `#220`'s challenge documentation.
* `C5` (`src/core/tests/release_support.py:10-35`, `src/core/tests/test_challenge_no_retaliation_220.py:863`): `release_support.fixture()` injects `#1778`'s required `monitoring_declaration` automatically when `RELEASE_SUPPORT.install(self.store)` runs in `#220` tests.
* `C6` (`.github/workflows/src-ci.yml:69-98`, `src/core/pyproject.toml:30-75`): `src/core` CI runs `unittest discover -s tests -v`, `ruff check . && ruff format --check .` (with ADR 0006 legacy exclusions), and `mypy` (`strict = true`).
* `C7` (`src/api/pyproject.toml:55-68`, `src/api/tests/test_content_standard.py:14-60`): `src/api` CI runs `unittest discover -s tests -v` (with `PYTHONPATH` including `src/core/tests` and `src/agents/tests`), `test_content_standard.py` lexical audit, `ruff check . && ruff format --check .`, and `mypy`.
* `C8` (`src/core/src/zava_forward/core/challenges.py:1-60`, `src/core/tests/test_challenge_no_retaliation_220.py:34-46`): Canonical `#220` guard functions live in `zava_forward.core.challenges` and tests live in `test_challenge_no_retaliation_220.py`; caller Task 1 & Task 2 explicitly reference `src/core/src/zava_forward/core/no_retaliation_guard.py` and `python3 -m unittest test_no_retaliation_guard_220 -q`.
* `C9` (`src/api/tests/test_alert_chat_keyboard_provenance.py:1-15`, `src/core/tests/test_dependency_rule.py:6-33`): Thin re-export alias modules are an established repository pattern and satisfy `DependencyRuleTests` (`ALLOWED = {"core"}`).

## Synthesis, Readiness, and Self-Check

* Selected convergence recommendation (Option A):
  1. Configure repository-local privacy-safe git author/committer (`gh api user` -> `{id}+{login}@users.noreply.github.com`) and rebase `feat/ai-220-no-retaliation` (`b67bd2a94`, `1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f`), verifying every sibling commit on `PR #1641` and both `#220` commits remain intact.
  2. Add thin, strictly typed `src/core/src/zava_forward/core/no_retaliation_guard.py` and `src/core/tests/test_no_retaliation_guard_220.py` re-exporting the canonical `zava_forward.core.challenges` guard API and `test_challenge_no_retaliation_220` test cases, and document the module alias in `src/core/README.md`.
  3. Run the exact caller validation command in `src/core` (`PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`) plus full `src-ci.yml`-equivalent unit, dependency-rule, content-standard, `ruff`, and `mypy` checks across `src/core` and `src/api` using an ephemeral workspace-local `.venv-220-rebase` (cleaned up immediately before staging/committing).
  4. Commit source/test/doc additions and finalized `.copilot-tracking/` artifacts cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leaving `git status --short` empty without pushing.
* Research execution status: Complete
* Research disposition: `executed`
* Planning Readiness: `Ready`
* Self-check: All 4 questions answered with `C1`–`C9` `path:line` evidence; research-only boundary respected (zero source edits during Research); ready for automatic parent transition to `rpi-plan`.
