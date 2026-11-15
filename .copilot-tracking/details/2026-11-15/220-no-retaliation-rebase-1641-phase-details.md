<!-- markdownlint-disable-file -->
# RPI Phase Details: Rebase and Verify Issue #220 Non-Retaliation Guard onto PR #1641

## Metadata

* Task ID: 220-no-retaliation-rebase-1641
* Task slug: 220-no-retaliation-rebase-1641
* Related plan: .copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/220-no-retaliation-rebase-1641-research.md, .github/workflows/src-ci.yml, src/core/src/zava_forward/core/challenges.py, src/core/tests/test_challenge_no_retaliation_220.py, src/api/tests/test_challenge_no_retaliation_api_220.py

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Fetch Parent Ref, Rebase #220 Stack onto PR #1641 Head, and Isolate Scratch Python Environment | Planned | P01, P01-T01, P01-T02 |
| P02 | Add `no_retaliation_guard` Facade & Test Selector Alias, Run Focused Tier Validation, Clean Up, and Commit `src/` | Planned | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Fetch Parent Ref, Rebase #220 Stack onto PR #1641 Head, and Isolate Scratch Python Environment

### Context

`feat/ai-220-no-retaliation` (`1a626f1c1`) contains two `#220` commits (`b67bd2a94` and `1a626f1c1`) based on `fa6f8d1dd` (`#1774`), while parent `PR #1641` (`origin/feat/demo-164-chat-grounding-provenance-0900`) advanced by 6 sibling commits (`704c6b07a..ad005cd5f`). Read-only `git merge-tree` confirmed zero conflicts (`src/core/README.md` and `src/core/src/zava_forward/core/assistants.py` auto-merge cleanly). Because this Linux host shares `~/.local` across concurrent worktrees, `src/api` validation needs a workspace-local scratch virtualenv rather than mutating `~/.local`.

### Intent

Set repository-local privacy-safe git author/committer config, fetch and rebase `feat/ai-220-no-retaliation` onto `origin/feat/demo-164-chat-grounding-provenance-0900`, verify both parent sibling hunks and `#220` hunks, and create workspace-local `.venv-220-rebase` for full `src/core` + `src/api` verification.

### Boundaries

* Included: `gh api user` + `git config --local`, `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, post-rebase diff/ancestry audit, and workspace-local `.venv-220-rebase` setup.
* Excluded: Modifying `web/role-screens.js`, rewriting parent-branch commits, mutating `~/.local`, writing to `/tmp`, or pushing to `origin`.

### Likely Targets

* `.git/config`: Repository-local `user.name` and `user.email` (`{id}+{login}@users.noreply.github.com`).
* `src/core/README.md` and `src/core/src/zava_forward/core/assistants.py`: Auto-merged files verified post-rebase.
* `.venv-220-rebase`: Ephemeral workspace-local scratch virtualenv (deleted in `P02-T02`).

### Dependencies

* None.

### Validation Expectations

* `git merge-base HEAD origin/feat/demo-164-chat-grounding-provenance-0900` equals `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900`.
* `git log --oneline origin/feat/demo-164-chat-grounding-provenance-0900..HEAD` lists the 2 rebased `#220` commits in order, and `git diff --check` exits `0`.
* `.venv-220-rebase/bin/python -c "import zava_forward.core, zava_forward.agents, zava_forward.api; print(zava_forward.core.__file__)"` resolves inside `/home/azureuser/source/ama-demo-wt/feat-220-no-retaliation/src/`.

### Completion Evidence

* Configured repository-local git identity `Juan Manuel Servera <8036360+jmservera@users.noreply.github.com>` from `gh api user`; fetched and rebased `feat/ai-220-no-retaliation` (`b67bd2a94`, `1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`697b00c0a`, incorporating sibling merges through `#1785`, `#1781`, and `#1788`) producing `135bd2a3e` and `5803323ad`; verified `git range-diff`, intact `#1778` `monitoring_status` + `#117` `is_available_case_document` + `#220` `Assistants.challenge` in `assistants.py`, intact `#1782` + `#115` + `#117` + `#220` sections in `src/core/README.md`, and untouched `web/role-screens.js`; provisioned `.venv-220-rebase` resolving `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api` from this worktree.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure privacy-safe git identity, fetch `origin/feat/demo-164-chat-grounding-provenance-0900`, and rebase `#220` commits

#### Context

Per `.github/copilot-instructions.md`, commits and rebases must use repository-local `{id}+{login}@users.noreply.github.com` resolved dynamically from `gh api user`. Untracked `.copilot-tracking/.../220-no-retaliation-rebase-1641-*` files do not overlap any tracked path on either branch and remain untouched during `git rebase`.

#### Intent

Resolve `id` and `login` (and `name` fallback to `login`) via `gh api user`, set `git config --local user.name` and `git config --local user.email`, fetch `origin feat/demo-164-chat-grounding-provenance-0900`, check `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900` (inspecting any `ad005cd5f..origin/feat/demo-164-chat-grounding-provenance-0900` delta before rebasing and aborting cleanly on any unexpected conflict), run `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, and verify `git range-diff fa6f8d1dd..1a626f1c1 origin/feat/demo-164-chat-grounding-provenance-0900..HEAD` plus `assistants.py` (`#1778` `monitoring_status` + `#220` `Assistants.challenge`) and `src/core/README.md` (`#1782` `paired_equity.evaluate` + `#220` sections) to confirm zero dropped hunks and untouched `web/role-screens.js`.

#### Boundaries

* Included: Repository-local git identity configuration, `git fetch`, `git rebase`, and post-rebase tree verification.
* Excluded: Global git config edits, force-pushing, or modifying unrelated files.

#### Likely Targets

* `feat/ai-220-no-retaliation` commit ancestry (`b67bd2a94`, `1a626f1c1` replayed onto `origin/feat/demo-164-chat-grounding-provenance-0900`).

#### Dependencies

* None.

#### Validation Expectations

* `git diff --check HEAD` exits `0`; `git diff origin/feat/demo-164-chat-grounding-provenance-0900..HEAD --name-only` matches the `#220` file set with `web/role-screens.js` absent.

#### Completion Evidence

* `git config --local user.name` (`Juan Manuel Servera`) and `git config --local user.email` (`8036360+jmservera@users.noreply.github.com`) configured; rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`697b00c0a`) as `135bd2a3e` and `5803323ad` with `git range-diff` confirming lossless replay alongside `#1778`, `#1782`, `#115`, `#117`, and `#144`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Provision workspace-local `.venv-220-rebase` with editable worktree packages

#### Context

`python3 -m venv --system-site-packages` sets `ENABLE_USER_SITE = False`, hiding third-party packages installed under `~/.local/lib/python3.12/site-packages`, while `~/.local` itself may contain stale editable `.pth` pointers from other worktrees. Adding a tail `zzz_user_site_fallback.pth` file inside `.venv-220-rebase/lib/python3.12/site-packages/` and installing `-e src/core -e src/agents -e src/api` (`--no-build-isolation --no-deps`) ensures this worktree's `zava_forward.*` packages win import resolution ahead of `~/.local` third-party dependencies.

#### Intent

Create `.venv-220-rebase`, configure tail `zzz_user_site_fallback.pth` to `python3 -m site --user-site` if that directory exists, install `-e src/core -e src/agents -e src/api` with `--no-build-isolation --no-deps`, and verify imports of `aiohttp`, `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api`.

#### Boundaries

* Included: Workspace-local `.venv-220-rebase` creation and local editable `--no-deps` installation.
* Excluded: Network package downloads, `/tmp` writes, or edits to `~/.local`.

#### Likely Targets

* `.venv-220-rebase` (ephemeral directory in repository root, removed in `P02-T02`).

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* `.venv-220-rebase/bin/python` imports `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api` from `/home/azureuser/source/ama-demo-wt/feat-220-no-retaliation/src/`.

#### Completion Evidence

* Created `.venv-220-rebase` with tail `zzz_user_site_fallback.pth`, editable `--no-deps` installs of `src/core[dev]`, `src/agents`, and `src/api[dev]` (plus missing dev test wheel `azure-iot-hub==2.7.0` / `six==1.17.0` inside `.venv-220-rebase` only, zero edits to `~/.local`), and cleaned temporary `*.egg-info`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Add `no_retaliation_guard` Facade & Test Selector Alias, Run Focused Tier Validation, Clean Up, and Commit `src/`

### Context

Caller Task 1 and Task 2 reference `src/core/src/zava_forward/core/no_retaliation_guard.py` and `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`, whereas `#220` commit `b67bd2a94` placed the canonical guard implementation in `zava_forward.core.challenges` and tests in `test_challenge_no_retaliation_220.py` (`src/core`) and `test_challenge_no_retaliation_api_220.py` (`src/api`).

### Intent

Create thin, strictly typed `no_retaliation_guard.py` and `test_no_retaliation_guard_220.py` modules delegating to the canonical `#220` modules, document them in `src/core/README.md`, run both the exact caller command and full `src-ci.yml`-equivalent Focused Tier checks across `src/core` and `src/api`, delete `.venv-220-rebase`, and commit the `src/` changes cleanly before `rpi-review`.

### Boundaries

* Included: `src/core/src/zava_forward/core/no_retaliation_guard.py`, `src/core/tests/test_no_retaliation_guard_220.py`, `src/core/README.md`, Focused Tier validation across `src/core` and `src/api`, `.venv-220-rebase` deletion, and pre-Review `src/` git commit.
* Excluded: Duplicating business logic from `challenges.py`, modifying `web/role-screens.js`, or pushing to `origin`.

### Likely Targets

* `src/core/src/zava_forward/core/no_retaliation_guard.py` (new thin typed facade).
* `src/core/tests/test_no_retaliation_guard_220.py` (new thin typed test selector alias + facade export test).
* `src/core/README.md` (updated `#220` verification command documentation).

### Dependencies

* `P01`.

### Validation Expectations

* Exact caller Task 2 command in `src/core` exits `0`.
* `src-ci.yml`-equivalent Focused Tier unit, dependency-rule, content-standard, `ruff check . && ruff format --check .`, and `mypy` checks in `src/core` and `src/api` all exit `0`.
* `.venv-220-rebase` is deleted and `src/` changes are committed cleanly with `Refs #220` and Copilot trailer.

### Completion Evidence

* Passed full `src-ci.yml` `unittest discover -s tests -q`, `ruff check . && ruff format --check .`, and `env -u PYTHONPATH mypy` across `src/core` (`3,685` tests, `0` failures; `304` files formatted; `357` files `mypy` clean) and `src/api` (`3,772` tests, `0` failures; `214` files formatted; `298` files `mypy` clean; `node --check web/panels.js` clean), removed `.venv-220-rebase`, passed the exact bare-`python3` caller Task 2 command (`Ran 7 tests in 0.510s OK`, `ruff`, `ruff format --check`, `mypy` `357` source files), and committed `src/` changes in `fb950840a` (`Refs #220` + Copilot trailer).

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Create `no_retaliation_guard.py` and `test_no_retaliation_guard_220.py` and update `src/core/README.md`

#### Context

Thin re-export modules (`from __future__ import annotations`, explicit `__all__`) satisfy `mypy --strict`, `ruff check`, `ruff format --check`, and `test_dependency_rule.py` (`ALLOWED = {"core"}`) while keeping `zava_forward.core.challenges` and `test_challenge_no_retaliation_220.py` as the single source of truth.

#### Intent

Create `src/core/src/zava_forward/core/no_retaliation_guard.py` re-exporting all 18 public non-underscore symbols of `zava_forward.core.challenges` (`ACCESSIBLE_ROUTE`, `FORBIDDEN_ADVERSE_FIELDS`, `NON_DIGITAL_CHANNELS`, `NOT_INFERRED`, `PROTECTION`, `RESOLVED`, `ROUTES`, `SAFEGUARDS`, `STATUSES`, `SUBJECT_KINDS`, `SUBMITTER_KINDS`, `ChallengeRegister`, `ChallengeSafeguardError`, `Node`, `Record`, `assert_no_adverse_challenge_effects`, `build_non_retaliation_assurance`, and `reject_adverse_mapping`) with `test_content_standard.py`-safe docstrings; create `src/core/tests/test_no_retaliation_guard_220.py` re-exporting `ChallengeRegisterNoRetaliationTests`, `StoreAndSqlStoreNoRetaliationLifecycleTests`, and `AssistantsProposalChallengeNoRetaliationTests` from `test_challenge_no_retaliation_220` plus `NoRetaliationGuardFacadeTests` (asserting 18-symbol public set and `is` identity parity against `zava_forward.core.challenges`) and a typed `load_tests` deduplication hook (running only `NoRetaliationGuardFacadeTests` when `pattern == "test*.py"` under `unittest discover` and all 4 `TestCase` classes otherwise) that passes `env -u PYTHONPATH python3 -m mypy`; and update both `#220` anchors in `src/core/README.md` (`lines 5139-5146` verification block and `lines 5213-5260` `## Affected-person challenge and correction route (#220)`) to document `no_retaliation_guard` and `test_no_retaliation_guard_220.py`.

#### Boundaries

* Included: `no_retaliation_guard.py`, `test_no_retaliation_guard_220.py`, and `src/core/README.md`.
* Excluded: `.copilot-tracking/` path citations inside `src/` files or commit messages.

#### Likely Targets

* `src/core/src/zava_forward/core/no_retaliation_guard.py`
* `src/core/tests/test_no_retaliation_guard_220.py`
* `src/core/README.md`

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, `test_no_retaliation_guard_220`, and `test_dependency_rule` pass in `src/core`.

#### Completion Evidence

* Created `src/core/src/zava_forward/core/no_retaliation_guard.py` (18-symbol typed facade over `zava_forward.core.challenges`), `src/core/tests/test_no_retaliation_guard_220.py` (typed selector alias + `NoRetaliationGuardFacadeTests` + `load_tests` deduplication + held `form_review` catalog isolation regression test), updated both `#220` anchors in `src/core/README.md`, and preserved `finance_decision_holds` (`status == "Held"`) isolation in `src/core/src/zava_forward/core/resident_decisions.py` (`_form_staging_records`).

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Execute full `src-ci.yml` Focused Tier checks, remove `.venv-220-rebase`, run post-cleanup caller check, and commit `src/` + implementation `.copilot-tracking/`

#### Context

Running full `src-ci.yml` `unittest discover -s tests -q`, `ruff`, and `mypy` checks inside `.venv-220-rebase` across `src/core` and `src/api` exercises all 6 newly rebased `PR #1641` sibling suites alongside `#220`. Deleting `.venv-220-rebase` and then running the exact `/usr/bin/python3` caller Task 2 one-liner (`PYTHONPATH=src:tests` in `src/core`, with `PYTHONPATH` unexported for `mypy`) proves the cleaned worktree works identically. Committing `src/` and reconciled implementation `.copilot-tracking/` records separately before `rpi-review` ensures `git status --short` is empty entering `rpi-review`.

#### Intent

1. Run `.venv-220-rebase` `src/core` checks (`python -m unittest discover -s tests -q`, `ruff check . && ruff format --check .`, `mypy`) and `src/api` checks (`PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q`, `ruff check . && ruff format --check .`, `mypy`), plus `node --check src/api/src/zava_forward/api/web/panels.js`.
2. Remove `.venv-220-rebase`, then run `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy` on the cleaned worktree.
3. Verify `git diff --check`, commit `src/core/src/zava_forward/core/no_retaliation_guard.py`, `src/core/tests/test_no_retaliation_guard_220.py`, and `src/core/README.md` (`Refs #220`, Copilot trailer, zero `.copilot-tracking/` references), reconcile `plan.md`, `phase-details.md`, and `changes.md` with that `src/` commit SHA and test outputs, and commit those `.copilot-tracking/*/2026-11-15/220-no-retaliation-rebase-1641-*` artifacts (`Refs #220`, Copilot trailer, no push) so `git status --short` is empty entering `rpi-review`.

#### Boundaries

* Included: Local Focused Tier test/lint/format/typecheck runs, `.venv-220-rebase` cleanup, and local `src/` commit.
* Excluded: `git push` or modifying `.copilot-tracking/` review artifacts before `rpi-review`.

#### Likely Targets

* `src/core/src/zava_forward/core/no_retaliation_guard.py`, `src/core/tests/test_no_retaliation_guard_220.py`, `src/core/README.md`, and `.copilot-tracking/changes/2026-11-15/220-no-retaliation-rebase-1641-changes.md`.

#### Dependencies

* `P01-T02`, `P02-T01`.

#### Validation Expectations

* All test, lint, format, and typecheck commands exit `0`; `.venv-220-rebase` no longer exists; `git show --stat HEAD` shows the clean `src/core` commit with Copilot trailer.

#### Completion Evidence

* Full `src/core` discovery (`Ran 3685 tests in 808.262s OK (skipped=420)`), full `src/api` discovery (`Ran 3772 tests in 2071.256s OK (skipped=635)`), `ruff check . && ruff format --check .`, `env -u PYTHONPATH mypy`, and `node --check src/api/src/zava_forward/api/web/panels.js` all exited `0`; `.venv-220-rebase` removed; bare-`python3` caller Task 2 command in `src/core` exited `0` (`Ran 7 tests in 0.510s OK`); committed `src/` in `fb950840a` (`feat(core): add no_retaliation_guard facade and preserve held form-review isolation (Refs #220)`).

#### Unresolved Items

* None.
