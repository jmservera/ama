<!-- markdownlint-disable-file -->
# RPI Plan Critique: Rebase and Verify Issue #220 Non-Retaliation Guard onto PR #1641

## Metadata

* Task ID: 220-no-retaliation-rebase-1641
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements:
  1. Fetch and rebase `feat/ai-220-no-retaliation` (`1a626f1c1`, commits `b67bd2a94` and `1a626f1c1`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (updated head of parent `PR #1641`), preserving all sibling changes on the parent branch (`#1775`, `#1777`, `#1778`, `#1779`, `#1780`, `#1782`, `#1783`) and all `#220` changes (`src/core/src/zava_forward/core/no_retaliation_guard.py`, `src/core/tests/test_no_retaliation_guard_220.py`, and existing `#220` `src/core` + `src/api` modules).
  2. Run focused validation matching `.github/workflows/src-ci.yml`, including the exact caller command `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`.
  3. Record the rebase validation in `.copilot-tracking/` for `#220`, commit cleanly with repository-local privacy-safe git identity and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and leave a clean worktree without pushing.
* Research and evidence considered:
  * .copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md
  * .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md
  * .copilot-tracking/research/2026-11-15/220-no-retaliation-rebase-1641-research.md (`C1` through `C9`)
  * .copilot-tracking/reviews/2026-11-15/220-no-retaliation-review.md (`RV-001` and baseline `#220` validation evidence)
  * .github/workflows/src-ci.yml
  * src/core/src/zava_forward/core/challenges.py
  * src/core/tests/test_challenge_no_retaliation_220.py
  * src/core/tests/test_dependency_rule.py
  * src/api/tests/test_challenge_no_retaliation_api_220.py
  * src/api/tests/test_content_standard.py
  * src/core/README.md
* Decisions, dependencies, and acceptance criteria considered:
  * Convergence Option A from research (`C8`, `C9`): retain canonical `#220` implementation in `src/core/src/zava_forward/core/challenges.py` and `src/core/tests/test_challenge_no_retaliation_220.py` while adding thin typed re-export modules `src/core/src/zava_forward/core/no_retaliation_guard.py` and `src/core/tests/test_no_retaliation_guard_220.py`.
  * Shared-host constraints: zero edits to `src/api/src/zava_forward/api/web/role-screens.js`, zero writes to `/tmp` or shared `~/.local` editable installs, `Refs #220` (non-closing) commit linkage per `RV-001`, and zero `git push`.
  * Plan requirements `FR-1`, `FR-2`, `FR-3`, `NFR-1`, `NFR-2`, phase ordering `P01` (`P01-T01`, `P01-T02`) -> `P02` (`P02-T01`, `P02-T02`), and the locked test-file/source-file scope ceiling (`1` new test alias module, `1` new core facade module, `0` removals).
* Assessment boundary:
  * Evaluates plan credibility, technical correctness, `unittest` discovery/selector semantics, strict `mypy` and `ruff` behavior under unexported `PYTHONPATH`, `test_dependency_rule.py` and `test_content_standard.py` invariants, rebase hunk-preservation verification, and git commit/clean-worktree sequencing from the supplied read-only artifacts.
  * Does not mutate git state, execute live SQL Server (`mssql` job in `.github/workflows/src-ci.yml`), or observe hosted GitHub Actions CI prior to future branch push.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller Req 1 / `FR-1` / `C2`..`C5` / `P01-T01` | Partial | `git merge-tree` proves clean auto-merge onto `ad005cd5f`, but `P01-T01` lacks a post-fetch guard if `origin/feat/demo-164-chat-grounding-provenance-0900` advanced past `ad005cd5f` and omits `git range-diff` + explicit parent-hunk verification (`PC-004`). |
| `NFR-1` / `C7` / `P01-T02` | Covered | Workspace-local `.venv-220-rebase` with `--no-build-isolation --no-deps` editable installs and tail `zzz_user_site_fallback.pth` isolates `zava_forward.*` resolution without mutating `~/.local` or `/tmp`. |
| Caller Req 1 & 2 / `FR-2` / `C8`, `C9` / `P02-T01` | Partial | Thin facade/alias design avoids logic duplication and satisfies `test_dependency_rule.py`, but `test_no_retaliation_guard_220.py` causes duplicate test runs under `unittest discover` and risks `mypy` sibling-import failure without `PYTHONPATH` (`PC-002`), while `no_retaliation_guard.py` omits `reject_adverse_mapping` and companion public symbols from `challenges.py` and leaves dual `#220` anchors in `src/core/README.md` ambiguous (`PC-003`). |
| Caller Req 2 / `FR-3`, `NFR-2` / `C1`, `C6`, `C7` / `P02-T02` | Partial | Runs the exact caller one-liner and 10 named test modules, but omits `.github/workflows/src-ci.yml` full `unittest discover -s tests` runs in `src/core` and `src/api`, leaving all 6 newly rebased parent `PR #1641` sibling test suites (`#1775`..`#1782`) and form-staging suites unexecuted against rebased `#220` (`PC-001`). |
| Caller Req 3 / `FR-3`, `NFR-1` / `P02-T02` & `Dependencies` | Partial | `P02-T02` runs the bare-`python3` caller command before deleting `.venv-220-rebase` rather than verifying the final cleaned state, and leaves `.copilot-tracking/` artifacts untracked at `P02-T02` completion despite `NFR-1` requiring zero untracked entries at `rpi-review` (`PC-004`). |

## Verdict

* Verdict: Revise
* Rationale: The rebase topology (`C2` through `C5`), workspace-local venv isolation (`P01-T02`), and thin facade/alias strategy (`Option A`) are sound and well-grounded, but four direct planner corrections (`PC-001` through `PC-004`) are needed before implementation so that `P02-T02` actually executes full `src-ci.yml` `unittest discover` across the 6 newly rebased `PR #1641` sibling suites, `test_no_retaliation_guard_220.py` neither double-executes heavy Store/SQLite suites under `unittest discover` nor fails `mypy` when `PYTHONPATH` is unexported, `no_retaliation_guard.py` exports the complete public guard contract including `reject_adverse_mapping`, and `.copilot-tracking/` commits plus post-cleanup caller verification leave a clean worktree entering `rpi-review`.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: P02-T02 cherry-picks pre-rebase #220 test modules instead of running src-ci.yml unittest discover across src/core and src/api

* Related IDs: Caller Req 2, `FR-3`, `C2`, `C3`, `C5`, `C6`, `C7`, `P02`, `P02-T02`
* Evidence: .github/workflows/src-ci.yml (`lines 82-87`), .copilot-tracking/research/2026-11-15/220-no-retaliation-rebase-1641-research.md (`Wider Wave`, `Deeper Wave`, `C2`-`C7`), .copilot-tracking/reviews/2026-11-15/220-no-retaliation-review.md (`Validation Evidence`), .copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md (`Acceptance Criteria`, `lines 110-113`), and .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md (`P02-T02`, `lines 207-210`)
* Concern: `.github/workflows/src-ci.yml` (`line 87`) runs `python -m unittest discover -s tests -v` across all tests in `src/core` and `src/api`. By contrast, `P02-T02` runs only 6 named `src/core` modules and 4 named `src/api` modules. None of the new test suites introduced by the 6 upstream `PR #1641` sibling commits (`#1775` sensor non-authority, `#1777` simulator controls, `#1778` monitoring harm declarations in `assistants.py`/`rai_release.py`, `#1779` bounded AI invariants, `#1780` reproducible sensor receipts, `#1782` RAI cohort/paired equity) or `#220`-adjacent `test_form_staging` / `test_form_review` suites are executed after rebasing `#220`'s changes to `assistants.py`, `ai_tasks.py`, `resident_decisions.py`, `server.py`, and `web/panels.js`.
* Impact: Cross-feature regressions between `#220` (`Assistants.challenge`, `_withhold_sensors`, `ai_tasks.review`, `form_staging` challenge targets) and the 6 newly rebased `PR #1641` commits (`#1775`..`#1782`) would escape local Focused Tier validation while hosted CI remains unrun under the no-push rule.
* Smallest useful change: Update `FR-3`, `Acceptance Criteria`, and `P02-T02` so `.venv-220-rebase` runs full `python -m unittest discover -s tests -q` in `src/core` and `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` in `src/api` (plus `node --check src/api/src/zava_forward/api/web/panels.js`), matching `.github/workflows/src-ci.yml`, alongside the exact caller Task 2 command.
* Action owner: planning_parent
* Exact resolving evidence: Revised `plan.md` (`FR-3`, `Acceptance Criteria`, `P02-T02`) and `phase-details.md` (`P02-T02`) requiring full `unittest discover -s tests` in `src/core` and `src/api`, verified during implementation by exit-`0` full-suite counts in `.copilot-tracking/changes/2026-11-15/220-no-retaliation-rebase-1641-changes.md`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Unconditional TestCase re-exports and sibling test import in test_no_retaliation_guard_220.py cause duplicate unittest discover execution and risk mypy lookup failure without PYTHONPATH

* Related IDs: Caller Req 2, `FR-2`, `NFR-2`, `C6`, `C8`, `C9`, `P02-T01`, `P02-T02`
* Evidence: .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md (`P02-T01`, `lines 179-183`), .github/workflows/src-ci.yml (`lines 82-92`), and src/core/tests/test_challenge_no_retaliation_220.py (`lines 25-60`, `ChallengeRegisterNoRetaliationTests`, `StoreAndSqlStoreNoRetaliationLifecycleTests`, `AssistantsProposalChallengeNoRetaliationTests`)
* Concern: Two coupled Python loader/typechecker mechanics affect `src/core/tests/test_no_retaliation_guard_220.py`:
  1. `unittest.TestLoader.loadTestsFromModule` collects every `unittest.TestCase` subclass in `dir(module)` regardless of `__module__`. Re-exporting the 3 `TestCase` classes from `test_challenge_no_retaliation_220` without a `load_tests` protocol hook causes `python -m unittest discover -s tests -v` (`pattern == "test*.py"` in `src-ci.yml:87`) to execute every JSON `Store`, SQLite `SqlStore`, and SQLite `Assistants` lifecycle test twice with duplicate `test_challenge_no_retaliation_220.*` test IDs.
  2. In the exact caller command `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`, `PYTHONPATH=src:tests` applies only to the first subcommand before `&&` and is not set during `python3 -m mypy`. If `mypy` checks `tests/test_no_retaliation_guard_220.py` without `tests` on `mypy_path`, a bare `from test_challenge_no_retaliation_220 import ...` fails `mypy` with `import-not-found` unless `src/core/pyproject.toml` already resolves top-level `tests/` modules or the alias module imports in a `mypy --strict`-safe manner without modifying `pyproject.toml` or double-loading the module under both `test_challenge_no_retaliation_220` and `tests.test_challenge_no_retaliation_220` in `sys.modules`.
* Impact: Duplicate integration-test runs and duplicate test identifiers in `src-ci.yml` discovery, or `python3 -m mypy` failure on the exact caller Task 2 command when `PYTHONPATH` is unexported.
* Smallest useful change: Specify in `P02-T01` that `src/core/tests/test_no_retaliation_guard_220.py`:
  1. Binds `ChallengeRegisterNoRetaliationTests`, `StoreAndSqlStoreNoRetaliationLifecycleTests`, and `AssistantsProposalChallengeNoRetaliationTests` (in `__all__`) in a way verified to pass `env -u PYTHONPATH python3 -m mypy` in `src/core` without `pyproject.toml` edits and without double-importing `test_challenge_no_retaliation_220` under two `sys.modules` keys.
  2. Implements typed `load_tests(loader: unittest.TestLoader, standard_tests: unittest.TestSuite, pattern: str | None) -> unittest.TestSuite` returning `loader.loadTestsFromTestCase(NoRetaliationGuardFacadeTests)` only when `pattern == "test*.py"` (full-suite `unittest discover`, where `test_challenge_no_retaliation_220.py` already runs in the same pass) and returning `standard_tests` whenever `pattern != "test*.py"` (`pattern is None` for `python3 -m unittest test_no_retaliation_guard_220 -q` and explicit `-p` patterns).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02-T01` specifying `load_tests` deduplication and unexported-`PYTHONPATH` `mypy --strict` compatibility, proven in `P02-T02` by `PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 -v` running all 4 `TestCase` classes (`6+` tests) while `unittest discover -s tests -v` runs each `#220` test ID once and `env -u PYTHONPATH python3 -m mypy` exits `0`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: no_retaliation_guard.py omits reject_adverse_mapping and companion public symbols from challenges.py and leaves dual src/core/README.md #220 anchors and content-standard scan unanchored

* Related IDs: Caller Req 1, `FR-2`, `NFR-2`, `C7`, `C8`, `C9`, `P02-T01`
* Evidence: src/core/src/zava_forward/core/challenges.py (`lines 22-88`, `109-128`, `168-174`, `264-357`), src/core/README.md (`lines 5137-5146` and `lines 5213-5260`), src/api/tests/test_content_standard.py (`lines 155-162`), and .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md (`P02-T01`, `lines 177-185`)
* Concern: `P02-T01` lists 10 symbols to re-export in `src/core/src/zava_forward/core/no_retaliation_guard.py`, omitting `reject_adverse_mapping` (`src/core/src/zava_forward/core/challenges.py:168`, explicitly documented in `src/core/README.md:5228` alongside `FORBIDDEN_ADVERSE_FIELDS` and `assert_no_adverse_challenge_effects` as one of the three fail-closed guard primitives) as well as public constants/types `PROTECTION`, `ACCESSIBLE_ROUTE`, `ROUTES`, `SUBJECT_KINDS`, `STATUSES`, `RESOLVED`, and `Record`. In addition, `src/core/README.md` has two distinct `#220` passages (`lines 5139-5146` verification command block and `lines 5213-5260` `## Affected-person challenge and correction route (#220)`, where `lines 5248-5249` still list only `test_challenges.py` and `test_issue_220_challenge_route.py`), and `src/api/tests/test_content_standard.py:155-162` scans every `src/core/src/zava_forward/core/*.py` file for disallowed `"human-approved"` wording.
* Impact: Partial re-export leaves `zava_forward.core.no_retaliation_guard` missing `reject_adverse_mapping` and `PROTECTION`, risks drift between the two `#220` sections in `src/core/README.md`, and risks a `test_content_standard.py` failure if `no_retaliation_guard.py` docstrings use banned phrasing.
* Smallest useful change: Update `FR-2` and `P02-T01` so `no_retaliation_guard.py` re-exports the complete public non-underscore contract of `zava_forward.core.challenges` (`ACCESSIBLE_ROUTE`, `FORBIDDEN_ADVERSE_FIELDS`, `NON_DIGITAL_CHANNELS`, `NOT_INFERRED`, `PROTECTION`, `RESOLVED`, `ROUTES`, `SAFEGUARDS`, `STATUSES`, `SUBJECT_KINDS`, `SUBMITTER_KINDS`, `ChallengeRegister`, `ChallengeSafeguardError`, `Node`, `Record`, `assert_no_adverse_challenge_effects`, `build_non_retaliation_assurance`, and `reject_adverse_mapping`) in explicit `__all__`, `NoRetaliationGuardFacadeTests` verifies exact symbol-set and object-identity (`is`) parity against `challenges`, `no_retaliation_guard.py` docstrings comply with `test_content_standard.py:155-162`, and `P02-T01` anchors both `src/core/README.md` `#220` passages (`lines 5139-5146` and `lines 5213-5260`).
* Action owner: planning_parent
* Exact resolving evidence: Revised `FR-2` and `P02-T01` listing the full 18-symbol `__all__` and both `src/core/README.md` anchors, verified by `NoRetaliationGuardFacadeTests`, `mypy --strict`, and `test_content_standard.py`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Post-fetch parent SHA verification, post-cleanup bare caller check, and pre-Review .copilot-tracking commit sequencing are underspecified

* Related IDs: Caller Req 1, Caller Req 3, `FR-1`, `FR-3`, `NFR-1`, `P01-T01`, `P02-T02`, `Dependencies`
* Evidence: .copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md (`FR-1` `line 77`, `FR-3` `lines 86-89`, `NFR-1` `lines 93-96`, `Dependencies` `lines 173-174`) and .copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md (`P01-T01` `lines 82-103`, `P02-T02` `lines 206-225`)
* Concern: Three execution-order details create avoidable rebase and review risk:
  1. `FR-1` permits rebasing onto `ad005cd5f` "or latest fetched tip if advanced", whereas Research (`C2`-`C5`) only verified `git merge-tree` and semantic compatibility up to `ad005cd5f`. `P01-T01` does not instruct the implementer to check whether `origin/feat/demo-164-chat-grounding-provenance-0900` advanced past `ad005cd5f` after `git fetch`, inspect any `ad005cd5f..origin/feat/demo-164-chat-grounding-provenance-0900` delta before rebasing, and verify lossless commit replay with `git range-diff fa6f8d1dd..1a626f1c1 origin/feat/demo-164-chat-grounding-provenance-0900..HEAD` plus presence of `#1778` `monitoring_status` in `Assistants.catalog()` and `#1782` `paired_equity.evaluate` in `src/core/README.md`.
  2. `P02-T02` executes the caller Task 2 bare-`python3` command (`step 1`) before removing `.venv-220-rebase` (`step 3`), instead of running the exact caller command after `.venv-220-rebase` deletion to prove the clean post-cleanup state works identically for downstream checks.
  3. `NFR-1` (`plan.md:96`) requires zero untracked files or scratch directories at `rpi-review` and closeout, and Caller Req 3 requires recording rebase validation in `.copilot-tracking/` and committing cleanly with the Copilot trailer, yet `P02-T02` commits only `src/` and leaves all `.copilot-tracking/*/2026-11-15/220-no-retaliation-rebase-1641-*` artifacts untracked entering `rpi-review` (which is read-only toward git history).
* Impact: Uninspected upstream commits past `ad005cd5f` could alter merged behavior silently, pre-cleanup execution of the caller command fails to test the final cleaned environment, and untracked `.copilot-tracking/` artifacts at `P02-T02` completion violate `NFR-1` and Caller Req 3 during `rpi-review`.
* Smallest useful change:
  1. In `P01-T01`, verify `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900` after `git fetch` (inspecting `ad005cd5f..origin/feat/demo-164-chat-grounding-provenance-0900` if advanced and aborting cleanly on any unexpected conflict), and run `git range-diff fa6f8d1dd..1a626f1c1 origin/feat/demo-164-chat-grounding-provenance-0900..HEAD` plus explicit checks that `#1778` (`Assistants.catalog()` `monitoring_status`) and `#1782` (`src/core/README.md` `paired_equity.evaluate`) remain intact alongside `#220`.
  2. In `P02-T02`, run `.venv-220-rebase` full `src-ci.yml` checks first, delete `.venv-220-rebase`, then run the exact bare-`python3` caller Task 2 command on the cleaned worktree, commit the 3 `src/core/` files cleanly (`Refs #220` + Copilot trailer, zero `.copilot-tracking/` references in the `src/` commit), update `plan.md`, `phase-details.md`, and `changes.md` with that commit SHA and validation evidence, and commit those reconciled `.copilot-tracking/*/2026-11-15/220-no-retaliation-rebase-1641-*` artifacts (`Refs #220` + Copilot trailer) so `git status --short` is clean entering `rpi-review` (with only `220-no-retaliation-rebase-1641-review.md` committed by the parent after `rpi-review`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01`, `P02-T02`, `NFR-1`, and `Dependencies` incorporating `git range-diff` + post-fetch SHA verification, post-cleanup bare caller verification, and explicit pre-Review `.copilot-tracking/` commit ownership leaving `git status --short` empty before `rpi-review` and at final closeout.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Research `C2` through `C5` directly verified 3-way merge cleanliness (`git merge-tree` exit `0`) and confirmed that `#1778`'s `release_support.fixture()` automatically populates `monitoring_declaration` for `#220`'s assistant proposal challenge tests.
* Workspace-local `.venv-220-rebase` with `--no-build-isolation --no-deps` editable installs and a tail `zzz_user_site_fallback.pth` fallback cleanly protects sibling worktrees sharing `~/.local` while ensuring this worktree's `zava_forward.*` packages win import resolution.
* Preserving canonical `zava_forward.core.challenges` and `test_challenge_no_retaliation_220.py` while exposing thin typed `no_retaliation_guard.py` and `test_no_retaliation_guard_220.py` modules satisfies both internal `#220` callers and the coordinator's exact Task 1/Task 2 module names without code duplication.
* Residual risk (explicitly accepted within Focused Tier / caller scope): Hosted GitHub Actions CI (`src-ci.yml`) and live SQL Server (`mssql` service container job) are not executed remotely in this turn because Caller Req 3 prohibits `git push`, and whole-issue `#220` external human legal/RAI and assistive-technology acceptance remain tracked under `RV-001` (`Refs #220`).

## Questions or Blocking Evidence Gaps

* None. All four findings are direct, bounded planner corrections supported by the supplied repository files and caller requirements.

## Limitations

* Critique stayed strictly read-only across repository code, git refs, and planning sources; runtime verification of `mypy`, `ruff`, and `unittest discover` against the rebased tree occurs in `P02-T02` during `rpi-implement`.
* `src/core/pyproject.toml` and `src/api/pyproject.toml` were referenced indirectly via `.copilot-tracking/research/2026-11-15/220-no-retaliation-rebase-1641-research.md` (`C6`, `C7`) rather than listed in the direct read-only file set, which reinforces requiring `env -u PYTHONPATH python3 -m mypy` verification in `PC-002`.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Revise `FR-2`, `FR-3`, `NFR-1`, `Acceptance Criteria`, `Dependencies`, `P01-T01`, `P02-T01`, and `P02-T02` directly in `.copilot-tracking/plans/2026-11-15/220-no-retaliation-rebase-1641-plan.md` and `.copilot-tracking/details/2026-11-15/220-no-retaliation-rebase-1641-phase-details.md` to incorporate `PC-001` through `PC-004`, record critique dispositions, finalize the plan without a second critique pass, and proceed to `rpi-implement`.
* User response required: no
