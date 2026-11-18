<!-- markdownlint-disable-file -->
# RPI Plan: Rebase and Verify Issue #220 Non-Retaliation Guard onto PR #1641

## Task Metadata

* Task ID: 220-no-retaliation-rebase-1641
* Task slug: 220-no-retaliation-rebase-1641
* Planning status: Implementation-ready (critique dispositions applied)
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/220-no-retaliation-rebase-1641-plan-critique.md

## Executive Summary

This plan rebases `feat/ai-220-no-retaliation` (`1a626f1c1`, `2` commits: `b67bd2a94` and `1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f`, the updated head of parent `PR #1641`, `6` sibling commits ahead of prior merge-base `fa6f8d1dd`), preserves every parent-branch sibling change and every `#220` change across `src/core` and `src/api`, provides thin typed facade/alias modules (`src/core/src/zava_forward/core/no_retaliation_guard.py` and `src/core/tests/test_no_retaliation_guard_220.py`) so the exact caller module selector (`python3 -m unittest test_no_retaliation_guard_220 -q`) and `zava_forward.core.no_retaliation_guard` imports resolve cleanly alongside canonical `zava_forward.core.challenges` and `test_challenge_no_retaliation_220.py`, verifies Focused Tier `src-ci.yml` checks across `src/core` and `src/api`, and records committed `.copilot-tracking/` evidence on a clean local worktree without pushing.

### User Decisions and Requirements Highlights

* **Clean parent-stack rebase**: Fetch and rebase `feat/ai-220-no-retaliation` (`1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900`, preserving all sibling commits on `PR #1641` and all `#220` commits and files.
* **Exact `src-ci.yml` Focused Tier validation**: Execute `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`, supplemented by `src/core` and `src/api` `#220`, dependency-rule, and content-standard suites matching `src-ci.yml`.
* **Local tracking commit and clean worktree**: Record the rebase validation in `.copilot-tracking/` for `#220`, commit cleanly with privacy-safe repository-local git identity and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and leave `git status --short` empty without pushing.

### What You May Not Know

* Read-only `git merge-tree --write-tree HEAD origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f`) exits `0`: the only two files touched on both sides (`src/core/README.md` from `#1782` and `src/core/src/zava_forward/core/assistants.py` from `#1778`) modify completely disjoint sections/methods (`Assistants.catalog()` vs `_view()`, `_withhold_sensors()`, and `Assistants.challenge()`), and `#1778`'s `release_support.fixture()` automatically supplies `monitoring_declaration` to `#220`'s assistant proposal challenge tests.
* Commit `b67bd2a94` implemented `#220` guard logic in `src/core/src/zava_forward/core/challenges.py` and tests in `src/core/tests/test_challenge_no_retaliation_220.py` (`src/api/tests/test_challenge_no_retaliation_api_220.py`), whereas the caller prompt references `src/core/src/zava_forward/core/no_retaliation_guard.py` and `python3 -m unittest test_no_retaliation_guard_220 -q`. Adding thin, strictly typed re-export modules (`no_retaliation_guard.py` and `test_no_retaliation_guard_220.py`) follows the established repository alias pattern (`src/api/tests/test_alert_chat_keyboard_provenance.py`) without duplicating logic.
* Because this host shares `~/.local` across concurrent worktrees, `src/api` type-checking and HTTP tests run inside an ephemeral workspace-local `.venv-220-rebase` (with `--system-site-packages` + a tail `zzz_user_site_fallback.pth` entry) that is deleted before staging and `rpi-review`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI rebase and verification continuation (`research` -> `plan` -> `implement` -> `review`) for Issue `#220` (`feat/ai-220-no-retaliation`) in `/home/azureuser/source/ama-demo-wt/feat-220-no-retaliation` (caller prompt).
* Fetch and rebase `feat/ai-220-no-retaliation` (`1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (the updated head of parent `PR #1641`), preserving all sibling changes on the parent branch and all `#220` changes (`src/core/src/zava_forward/core/no_retaliation_guard.py`, `src/core/tests/test_no_retaliation_guard_220.py`, and existing `#220` `core` + `api` files) (caller Task 1).
* Run focused validation matching `src-ci.yml`: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy` (caller Task 2).
* Record the rebase validation in `.copilot-tracking/` for `#220`, commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and leave a clean worktree without pushing (caller Task 3).
* Preserve `src/api/src/zava_forward/api/web/role-screens.js` untouched, avoid mutating shared `~/.local` editable installs across concurrent worktrees, and maintain `Refs #220` (never a closing keyword) because external operational SQL Server and human governance/AT acceptance remain open (`RV-001` in parent review `.copilot-tracking/reviews/2026-11-15/220-no-retaliation-review.md`; `.github/copilot-instructions.md`).

## Goals

* Rebase `feat/ai-220-no-retaliation` cleanly onto the current tip of `origin/feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) with zero lost hunks or regressions in either sibling `PR #1641` commits or `#220` commits.
* Provide clean, zero-duplication typed re-export modules `src/core/src/zava_forward/core/no_retaliation_guard.py` and `src/core/tests/test_no_retaliation_guard_220.py` so both the caller's exact module selector and canonical `#220` modules pass under `unittest`, `ruff`, `mypy --strict`, and `DependencyRuleTests`.
* Validate both the exact caller `src/core` command and `src-ci.yml`-equivalent `src/core` and `src/api` Focused Tier checks in an isolated workspace-local scratch venv without side effects on sibling worktrees.
* Freeze committed `src/` and `.copilot-tracking/` artifacts cleanly with privacy-safe git identity and the Copilot trailer while leaving `git status --short` empty and unpushed.

## Scope and Non-Goals

### In Scope

* Rebasing commits `b67bd2a94` and `1a626f1c1` on `feat/ai-220-no-retaliation` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` or latest fetched tip if advanced).
* Adding `src/core/src/zava_forward/core/no_retaliation_guard.py`, `src/core/tests/test_no_retaliation_guard_220.py`, updating `src/core/README.md` to document the stable guard module facade and test selector, and preserving `form_review` `finance_decision_holds` (`status == "Held"`) isolation in `src/core/src/zava_forward/core/resident_decisions.py` (`_form_staging_records`).
* Focused Tier validation across `src/core` and `src/api` matching `.github/workflows/src-ci.yml` (`unittest`, `ruff check`, `ruff format --check`, `mypy`).
* Dated `.copilot-tracking/` RPI continuation artifacts (`220-no-retaliation-rebase-1641-*`) committed locally with the Copilot trailer.

### Non-Goals

* Pushing any ref to `origin` (`git push` is prohibited by caller Task 3).
* Modifying `src/api/src/zava_forward/api/web/role-screens.js`, infrastructure/Bicep, workflows, Dockerfiles, or package dependency manifests.
* Mutating shared `~/.local` Python site-packages or writing outside the worktree.

## Functional Requirements

* **FR-1 (Lossless Rebase onto Updated `PR #1641` Head)**: Fetch `origin/feat/demo-164-chat-grounding-provenance-0900`, verify `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900` (inspecting any delta past `ad005cd5f` before rebasing), and rebase `feat/ai-220-no-retaliation` (`b67bd2a94`, `1a626f1c1`) onto its tip, preserving all parent sibling commits (`#1775`, `#1777`, `#1778`, `#1779`, `#1780`, `#1782`, `#1783`, and any inspected newer commit on `origin/feat/demo-164-chat-grounding-provenance-0900`) and all `#220` changes across `src/core` and `src/api`.
  * Observable acceptance criteria: `git merge-base HEAD origin/feat/demo-164-chat-grounding-provenance-0900` equals `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900`; `git range-diff fa6f8d1dd..1a626f1c1 origin/feat/demo-164-chat-grounding-provenance-0900..HEAD` shows lossless 2-commit replay; `#1778` (`Assistants.catalog()` `monitoring_status`) and `#1782` (`src/core/README.md` `paired_equity.evaluate`) remain intact alongside `#220`; `git diff --check` exits `0`.
* **FR-2 (Stable `no_retaliation_guard` Facade and `test_no_retaliation_guard_220` Test Selector)**: Expose `src/core/src/zava_forward/core/no_retaliation_guard.py` re-exporting the complete 18-symbol public non-underscore contract of `zava_forward.core.challenges` (`ACCESSIBLE_ROUTE`, `FORBIDDEN_ADVERSE_FIELDS`, `NON_DIGITAL_CHANNELS`, `NOT_INFERRED`, `PROTECTION`, `RESOLVED`, `ROUTES`, `SAFEGUARDS`, `STATUSES`, `SUBJECT_KINDS`, `SUBMITTER_KINDS`, `ChallengeRegister`, `ChallengeSafeguardError`, `Node`, `Record`, `assert_no_adverse_challenge_effects`, `build_non_retaliation_assurance`, and `reject_adverse_mapping`) with `test_content_standard.py`-compliant docstrings, and `src/core/tests/test_no_retaliation_guard_220.py` re-exporting the 3 `#220` `unittest.TestCase` classes from `test_challenge_no_retaliation_220` plus `NoRetaliationGuardFacadeTests` with a typed `load_tests` deduplication hook (running all 4 `TestCase` classes on direct `unittest test_no_retaliation_guard_220` invocation while running only `NoRetaliationGuardFacadeTests` under `pattern == "test*.py"` full-suite discovery) and `env -u PYTHONPATH python3 -m mypy` compatibility, documented at both `#220` anchors in `src/core/README.md`.
  * Observable acceptance criteria: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q` runs all `#220` core non-retaliation tests plus 18-symbol facade identity assertions and exits `0`; `unittest discover -s tests` executes each `#220` test ID once without duplication; `env -u PYTHONPATH python3 -m mypy` and `test_dependency_rule.py` pass.
* **FR-3 (Focused Tier `src-ci.yml` Verification & Clean Frozen Commits)**: Verify full `src-ci.yml` `unittest discover -s tests -q`, `ruff check . && ruff format --check .`, and `mypy` checks across `src/core` and `src/api` (plus `node --check src/api/src/zava_forward/api/web/panels.js`) via `.venv-220-rebase`, delete `.venv-220-rebase`, re-verify the exact caller command in `src/core` on the cleaned worktree, commit `src/` and reconciled implementation `.copilot-tracking/` artifacts cleanly before `rpi-review`, and commit finalized review + state `.copilot-tracking/` artifacts after `rpi-review` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.
  * Observable acceptance criteria: All validation commands exit `0`, `.venv-220-rebase` is removed before running the final bare-`python3` caller check and staging, `git status --short` is empty both entering `rpi-review` and at closeout, and `origin` refs remain unpushed.

## Non-Functional Requirements

* **NFR-1 (Shared-Environment Isolation & Hygiene)**
  * Objective threshold or evaluation condition: Zero writes to `/tmp` or `~/.local` site-packages; scratch virtualenv `.venv-220-rebase` lives inside the worktree during validation only and is deleted before `git add` / `git commit` and `rpi-review`.
  * Operating condition or verification approach: Inspect `git status --short --ignored` and verify `zava_forward.*` import paths point inside `/home/azureuser/source/ama-demo-wt/feat-220-no-retaliation/src/`.
  * Observable acceptance criteria: Zero untracked or scratch directories remain in the worktree at `rpi-review` and closeout.
* **NFR-2 (Strict Typing, Lint/Format Compliance, and Content Standard)**
  * Objective threshold or evaluation condition: `0` errors from `ruff check`, `ruff format --check`, `mypy` (`strict = true`), `test_dependency_rule.py`, and `test_content_standard.py`; `0` `.copilot-tracking/` references in `src/` files or commit messages; `web/role-screens.js` unmodified.
  * Operating condition or verification approach: Run `ruff check`, `ruff format --check`, `mypy`, `test_dependency_rule`, and `test_content_standard` across `src/core` and `src/api`.
  * Observable acceptance criteria: Every check exits `0` and `git diff origin/feat/demo-164-chat-grounding-provenance-0900..HEAD -- src/api/src/zava_forward/api/web/role-screens.js` is empty.

## Acceptance Criteria

* `feat/ai-220-no-retaliation` is rebased cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` or inspected fetched tip), verified via `git range-diff`, preserving all parent sibling commits (`assistants.py` `#1778` `monitoring_status`, `src/core/README.md` `#1782` `paired_equity.evaluate`, etc.) and all `#220` `src/core` and `src/api` changes.
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy` exits `0` on the cleaned worktree after `.venv-220-rebase` removal.
* Full `src-ci.yml` Focused Tier suites in `src/core` (`python -m unittest discover -s tests -q`, `ruff check . && ruff format --check .`, `mypy`) and `src/api` (`PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q`, `ruff check . && ruff format --check .`, `mypy`, plus `node --check src/api/src/zava_forward/api/web/panels.js`) all exit `0` with zero duplicate `#220` test executions during `unittest discover`.
* Test ownership and scope lock: exact test file removals = `none`; maximum new test files = `1` (`src/core/tests/test_no_retaliation_guard_220.py`, thin typed alias + `load_tests` deduplication + 18-symbol facade parity check over canonical `src/core/tests/test_challenge_no_retaliation_220.py`); maximum new canonical source files = `1` (`src/core/src/zava_forward/core/no_retaliation_guard.py`, thin typed 18-symbol facade over `zava_forward.core.challenges`); generated targets = `none`.
* Reconciled `src/` updates (`no_retaliation_guard.py`, `test_no_retaliation_guard_220.py`, `src/core/README.md`, and `resident_decisions.py` held `form_review` isolation guard) and dated `.copilot-tracking/` RPI artifacts (`220-no-retaliation-rebase-1641-*`) are committed cleanly in separate `src/` and `.copilot-tracking/` commits using repository-local `{id}+{login}@users.noreply.github.com` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, with `Refs #220`, `git status --short` empty both before `rpi-review` and at closeout, and no `git push`.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/220-no-retaliation-rebase-1641-plan-critique.md (`Complete` / `Revise`; `PC-001`..`PC-004` resolved directly) |
| Relevant research | .copilot-tracking/research/2026-11-15/220-no-retaliation-rebase-1641-research.md (`C1`–`C9`) |
| Changes-record role | .copilot-tracking/changes/2026-11-15/220-no-retaliation-rebase-1641-changes.md is created by `rpi-implement` as its evidence record |
| Planning execution and readiness | Complete and Ready for `rpi-implement` (`P01`) |
| Continuation context | Confirmed automatic RPI Agent parent continues to `rpi-implement` automatically |

## Sources

* .copilot-tracking/research/2026-11-15/220-no-retaliation-rebase-1641-research.md: Cycle 1 `C1`–`C9` rebase merge-tree, `#1778`/`#1782` semantic compatibility, selector alias analysis, and Focused Tier environment requirements.
* .copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md and .copilot-tracking/reviews/2026-11-15/220-no-retaliation-review.md: Parent `#220` Criterion 5 architecture and `RV-001` external acceptance boundary.
* .github/workflows/src-ci.yml, src/core/pyproject.toml, and src/api/pyproject.toml: Canonical test, lint, format, and `mypy` strict commands and ADR 0006 legacy exclusions.
* src/api/tests/test_alert_chat_keyboard_provenance.py and src/core/tests/test_dependency_rule.py: Established thin test-module alias pattern and `src/core` import rules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fetch Parent Ref, Rebase #220 Stack onto PR #1641 Head, and Isolate Scratch Python Environment

* Intent: Configure repository-local privacy-safe git identity, rebase `feat/ai-220-no-retaliation` (`b67bd2a94`, `1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900`, verify merged hunks, and provision workspace-local `.venv-220-rebase` without mutating `~/.local`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Configure privacy-safe git identity, fetch `origin/feat/demo-164-chat-grounding-provenance-0900`, and rebase `#220` commits

* Requirement and evidence: FR-1, NFR-2; research `C1`–`C5` in .copilot-tracking/research/2026-11-15/220-no-retaliation-rebase-1641-research.md
* Expected result: `git config --local user.email` uses `{id}+{login}@users.noreply.github.com` from `gh api user`; `feat/ai-220-no-retaliation` replays both `#220` commits cleanly atop `origin/feat/demo-164-chat-grounding-provenance-0900` preserving `#1778` `assistants.py` `monitoring_status` and `#1782` `src/core/README.md` hunks alongside all `#220` hunks, with `git diff --check` clean and `web/role-screens.js` untouched.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Provision workspace-local `.venv-220-rebase` with editable worktree packages

* Requirement and evidence: FR-3, NFR-1; research `C6`, `C7`
* Expected result: `.venv-220-rebase` resolves `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api` from `/home/azureuser/source/ama-demo-wt/feat-220-no-retaliation/src/` ahead of `~/.local` fallback dependencies without modifying `~/.local`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Add `no_retaliation_guard` Facade & Test Selector Alias, Run Focused Tier Validation, Clean Up, and Commit `src/`

* Intent: Deliver thin typed `no_retaliation_guard.py` and `test_no_retaliation_guard_220.py` modules, run exact caller Task 2 and `src-ci.yml`-equivalent `src/core` + `src/api` Focused Tier validation, delete `.venv-220-rebase`, and commit `src/` cleanly before `rpi-review`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Create `no_retaliation_guard.py` and `test_no_retaliation_guard_220.py` and update `src/core/README.md`

* Requirement and evidence: FR-2, NFR-2; research `C8`, `C9`; critique `PC-002`, `PC-003`
* Expected result: `src/core/src/zava_forward/core/no_retaliation_guard.py` cleanly re-exports all 18 public non-underscore symbols from `zava_forward.core.challenges` (including `reject_adverse_mapping` and `PROTECTION`) with `test_content_standard.py`-safe docstrings; `src/core/tests/test_no_retaliation_guard_220.py` re-exports all 3 `#220` core test suites from `test_challenge_no_retaliation_220` plus `NoRetaliationGuardFacadeTests` with `load_tests` deduplication for `unittest discover` and `env -u PYTHONPATH python3 -m mypy` safety; both `#220` anchors in `src/core/README.md` document the facade and test selector without `.copilot-tracking/` references.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Execute full `src-ci.yml` Focused Tier checks, remove `.venv-220-rebase`, run post-cleanup caller check, and commit `src/` + implementation `.copilot-tracking/`

* Requirement and evidence: FR-3, NFR-1, NFR-2; research `C1`, `C6`–`C9`; critique `PC-001`, `PC-004`
* Expected result: `.venv-220-rebase` runs full `unittest discover -s tests -q`, `ruff check . && ruff format --check .`, and `mypy` across `src/core` and `src/api` (plus `node --check` on `web/panels.js`) with `exit=0`; `.venv-220-rebase` is deleted; exact caller command (`cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`) passes (`exit=0`) on the cleaned worktree; `src/core/` additions and reconciled implementation `.copilot-tracking/` records are committed in clean commits (`Refs #220` + Copilot trailer) leaving `git status --short` empty entering `rpi-review`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md

## Dependencies

* `P01-T01` (fetch SHA audit, rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900`, and `git range-diff` + parent-hunk check) precedes `P01-T02` and `P02`.
* `P01-T02` and `P02-T01` precede `P02-T02` full `src-ci.yml` validation, `.venv-220-rebase` cleanup, post-cleanup bare caller check, and pre-Review `src/` + implementation `.copilot-tracking/` commits.
* After `rpi-review` writes `.copilot-tracking/reviews/2026-11-15/220-no-retaliation-rebase-1641-review.md` and transitions session state to `Follow-up` / `completed`, the RPI Agent parent commits `review.md` + `state.json` locally without pushing so `git status --short` ends empty.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
| --- | --- | --- |
| `2026-11-15` `PC-001` [High]: Run full `src-ci.yml` `unittest discover -s tests` across `src/core` and `src/api` instead of cherry-picking pre-rebase modules | Resolved (direct planner correction) | Updated `FR-3`, `Acceptance Criteria`, and `P02-T02` so `.venv-220-rebase` executes full `unittest discover -s tests -q`, `ruff check . && ruff format --check .`, and `mypy` in both `src/core` and `src/api` (plus `node --check` on `web/panels.js`), exercising all 6 newly rebased `PR #1641` sibling suites (`#1775`..`#1782`) alongside `#220`. |
| `2026-11-15` `PC-002` [Medium]: Prevent duplicate `unittest discover` runs and unexported-`PYTHONPATH` `mypy` import issues in `test_no_retaliation_guard_220.py` | Resolved (direct planner correction) | Updated `FR-2` and `P02-T01` so `test_no_retaliation_guard_220.py` implements typed `load_tests` (running only `NoRetaliationGuardFacadeTests` when `pattern == "test*.py"` during `unittest discover` and all 4 `TestCase` classes otherwise) and verifies `env -u PYTHONPATH python3 -m mypy` without `pyproject.toml` edits. |
| `2026-11-15` `PC-003` [Medium]: Re-export complete 18-symbol public `challenges` contract (including `reject_adverse_mapping`) in `no_retaliation_guard.py`, keep docstrings `test_content_standard.py`-safe, and update both `#220` anchors in `src/core/README.md` | Resolved (direct planner correction) | Updated `FR-2` and `P02-T01` to re-export all 18 public non-underscore symbols in `no_retaliation_guard.py`, assert exact public symbol-set and `is` identity parity in `NoRetaliationGuardFacadeTests`, avoid banned phrasing in `src/core`, and anchor both `#220` passages in `src/core/README.md`. |
| `2026-11-15` `PC-004` [Medium]: Verify post-fetch parent SHA + `git range-diff`, run bare caller Task 2 check after `.venv-220-rebase` removal, and commit reconciled `.copilot-tracking/` artifacts before `rpi-review` | Resolved (direct planner correction) | Updated `FR-1`, `FR-3`, `P01-T01`, `P02-T02`, and `Dependencies` to verify post-fetch SHA and `git range-diff`, run the exact bare-`python3` caller check after `.venv-220-rebase` cleanup, and commit `src/` and reconciled implementation `.copilot-tracking/` records separately before `rpi-review`. |
| Residual risk (accepted within caller scope) | Accepted | Remote GitHub Actions (`src-ci.yml`) and live SQL Server container (`mssql` job) are not pushed/run remotely because Caller Task 3 prohibits `git push`; Issue `#220` external human governance/AT acceptance remains tracked under `RV-001` (`Refs #220`). |

## Follow-Up Items

* Extend `src/api/checks/challenge_browser_check.py` with interactive Playwright + axe-core 4.10.3 assertions specifically clicking `#challenge-reopen-<id>` and toggling representative/safety-concern fields (outside rebase scope; existing 5 journeys already pass).
* Run live native SQL Server `_priority_correction_rows` verification and Issue `#220` human RAI/legal governance + assistive-technology comprehension sign-off (`RV-001` from parent task; outside local Focused Tier rebase scope).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/220-no-retaliation-rebase-1641-changes.md
* Ready phase or task: Complete (`P01` and `P02` complete; ready for `rpi-review`)
* Remaining provisional question or blocker: None
