<!-- markdownlint-disable-file -->
# RPI Plan: Rebase Issue #115 Immutable Blob Ledger Digests onto `#1641` (`e282dc327`)

## Task Metadata

* Task ID: issue-115-c2-rebase-164-0905
* Task slug: immutable-blob-ledger-digests-115-c2-rebase
* Parent task: issue-115-rebase-164-0820 (immutable-blob-ledger-digests-115-rebase)
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-plan-critique.md

## Executive Summary

This plan rebases `feat/demo-115-blob-ledger` (current `HEAD` `1b66fd607`, comprising `#115` implementation commit `84cb5608a` and prior rebase RPI commit `1b66fd607`) onto the updated `origin/feat/demo-164-chat-grounding-provenance-0900` tip (`e282dc327`, PR `#1641`, incorporating `#109` `704c6b07a`, `#189` `6bdcf7f90`, and `#146` `e282dc327`), resolves the sole conflict in `infra/tests/test_monitoring_alerts.py` by preserving both `#146`'s job-rank and cost/budget/anomaly alert assertions and `#115`'s immutable Blob ledger digest verification and alerting assertions, executes `src-ci.yml`-aligned focused validation across `infra/tests`, `src/core`, `src/orchestrator`, and `src/api`, completes `rpi-implement` pre-Review reconciliation, and after one-pass `rpi-review` and `Follow-up` state persistence commits the dated `c2-rebase` `.copilot-tracking/` artifacts locally (`Refs #115`, `Co-authored-by` trailer) without pushing, leaving a clean frozen working tree.

### User Decisions and Requirements Highlights

* Fetch `origin feat/demo-164-chat-grounding-provenance-0900` and rebase `feat/demo-115-blob-ledger` (`1b66fd607`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`, PR `#1641`).
* Resolve the conflict in `infra/tests/test_monitoring_alerts.py` by preserving both `#146` (PR `#1778`) job-rank/cost/budget/anomaly alerts and `#115` immutable Blob ledger digest verification & alerting assertions.
* Run focused validation matching `src-ci.yml` (`infra/tests` discovery, `src/core/tests -p '*ledger*'`, `ruff check`, `ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py`, and `src/core` `mypy`).
* Update `.copilot-tracking/` artifacts for the rebased head and commit with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; do NOT push and leave a clean frozen working tree.

### What You May Not Know

* Across `fa6f8d1dd..1b66fd607` (24 files) and `fa6f8d1dd..e282dc327` (54 files), `infra/tests/test_monitoring_alerts.py` is the **only** overlapping path: both `#146` (`e282dc327`) and `#115` (`84cb5608a`) append one test method at line 72 of `AlertOwnerAndRunbookTests` right before `WorkbookPanelTests`. Keeping `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` (`#146`) followed by `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` (`#115`) preserves 100% of both suites cleanly.
* Two `src-ci.yml` alignment subtleties affect local execution on this shared host: (1) both `src/api/tests/test_diagnostic_log_privacy.py` and `infra/tests/test_diagnostic_log_privacy.py` exist while `infra/tests/test_bicep_policy.py` imports `zava_forward.orchestrator.digest_blob` and `infra/tests/test_staff_azure.py` imports `azure-*` SDK packages from `~/.local`, so `infra/tests` `unittest` discovery must place `infra/tests` ahead of `src/api/tests` and include `src/orchestrator/src` on `PYTHONPATH` under `REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1` (with verified worktree-only `zava_forward.__path__` across all 5 `src/*` distributions); and (2) `infra/` has no `pyproject.toml`, so `src-ci.yml` runs `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` on `infra/` files rather than unconfigured Ruff `0.17.3` `FURB`/`ISC` rules on legacy `infra/scripts/` files (while `python3 -m ruff check src/core src/api infra/tests/test_monitoring_alerts.py` also passes 100%).

### Unresolved Decisions or Blockers

* None. Remote branch push / hosted CI execution remains deferred under `Do NOT push`, and irreversible Azure `lockImmutabilityPolicy` execution (`#121` Legal sign-off) plus live Azure Monitor alert delivery remain open under `Refs #115`.

## Sources and Evidence

* Research artifact: .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-research.md (`C1`–`C8`)
* Prior rebase RPI state and review: .copilot-tracking/rpi-sessions/2026-11-15/immutable-blob-ledger-digests-115-rebase-state.json, .copilot-tracking/reviews/logs/2026-11-15/immutable-blob-ledger-digests-115-rebase-review.md
* CI workflow specification: .github/workflows/src-ci.yml

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), updating dated artifacts under `.copilot-tracking/` (`research/`, `plans/`, `changes/`, `reviews/`) for Issue `#115` (`Immutable Blob ledger digests with retention lock and scheduled verification`) in `/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger` on branch `feat/demo-115-blob-ledger` (`1b66fd607`) (User prompt).
* Run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`, PR `#1641`) (User prompt, item 1).
* Resolve the conflict in `infra/tests/test_monitoring_alerts.py` (and any other file merged in PR `#1778` / `#146`) by preserving both `#146`'s cost/budget/anomaly/job-rank alerts and `#115`'s immutable Blob ledger digest verification & alerting assertions (User prompt, item 2).
* Run focused validation matching `src-ci.yml` across `infra/tests`, `src/core/tests` (`*ledger*`), `ruff check`, `ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py`, and `(cd src/core && python3 -m mypy)` (User prompt, item 3).
* Commit updated `.copilot-tracking/` artifacts for the rebased head with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, do NOT push, and leave a clean frozen working tree (User prompt, item 4).

## Goals

* Rebase `feat/demo-115-blob-ledger` (`84cb5608a` and `1b66fd607`) cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc3276992a17507351dd4f75d08a8808f56d`) with zero data loss across `#109`, `#189`, `#146`, and `#115` and zero overwritten historical RPI records.
* Merge `infra/tests/test_monitoring_alerts.py` cleanly so both `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` (`#146`) and `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` (`#115`) execute alongside all `WorkbookPanelTests` cost/budget/anomaly assertions within 100-column `ruff format` style.
* Prove full `src-ci.yml`-equivalent focused validation passes on the rebased tree and final committed `HEAD`, leaving `git status --short` completely empty without pushing.

## Scope and Non-Goals

### In Scope

* Rebasing `84cb5608a` and `1b66fd607` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`) and resolving `infra/tests/test_monitoring_alerts.py`.
* Worktree-isolated (`PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1`) focused validation matching `src-ci.yml` across `infra/tests`, `src/core`, `src/orchestrator`, and `src/api`, plus `--stdout` Bicep compilation/lint verification.
* Recording this RPI loop in `.copilot-tracking/*/*/immutable-blob-ledger-digests-115-c2-rebase-*`, reconciling `rpi-implement` before `rpi-review`, and committing the 7 `c2-rebase` tracking artifacts locally during parent post-Review `Follow-up` closeout (`Refs #115`, privacy-safe `user.email` `8036360+jmservera@users.noreply.github.com`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`).

### Non-Goals

* Pushing `feat/demo-115-blob-ledger` to `origin` or mutating remote PRs.
* Running `tools/rpi-checks.py` (full gate) or modifying shared `~/.local` Python editable `.pth` installs.
* Touching unrelated `infra/scripts/` files or rewriting committed `84cb5608a` / `1b66fd607` historical RPI critique/review files.

## Functional Requirements

* **FR-1 (Ancestry & Conflict Resolution onto `e282dc327`)**: `feat/demo-115-blob-ledger` is rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc3276992a17507351dd4f75d08a8808f56d`); `infra/tests/test_monitoring_alerts.py` retains all 4 baseline `AlertOwnerAndRunbookTests` methods, `#146`'s `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook`, `#115`'s `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers`, and all 4 `WorkbookPanelTests` cost/budget/AI-usage/AI-limit methods with zero conflict markers and zero unintended diffs outside `#115` and `.copilot-tracking/`.
* **FR-2 (`src-ci.yml`-Aligned Focused Validation)**: With `PYTHONDONTWRITEBYTECODE=1` and verified worktree-only `zava_forward.__path__` isolation across all 5 `src/*` distributions (allowing `~/.local` `azure-*` SDK packages required by `infra/tests/test_staff_azure.py`), the rebased tree passes:
  1. Full `infra/tests` suite (`REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=infra/tests:src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`), placing `infra/tests` ahead of `src/api/tests` to prevent `test_diagnostic_log_privacy` shadowing (`C6`) and including `src/orchestrator/src` for `test_bicep_policy.py` (`C7`);
  2. `#115` ledger and cross-feature unit suites: `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/core/tests -p '*ledger*' -q`, plus `src/core` `test_monitoring_coverage.py`, `test_simulator_run_controls_189.py`, `test_dependency_rule.py`, `test_live_doc_links.py`, and `src/orchestrator/tests/test_digest_blob.py`;
  3. Ruff lint and format checks matching `src-ci.yml` (`C8`): `python3 -m ruff check src/core src/api infra/tests/test_monitoring_alerts.py`, `(cd src/core && python3 -m ruff format --check .)`, `(cd src/api && python3 -m ruff format --check .)`, `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_monitoring_alerts.py infra/tests/test_bicep_policy.py`, and `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py infra/tests/test_bicep_policy.py`;
  4. Strict type checking in `src/core`: `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)` (`strict = true` across combined `#109`, `#189`, `#146`, and `#115` `src` + `tests`);
  5. Offline Bicep build/lint (`az bicep build --file <file> --stdout >/dev/null && az bicep lint --file <file>`) across `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, and `infra/modules/operationalMonitoring.bicep`.
* **FR-3 (Pre-Review Reconciliation & Parent Post-Review Clean-Tree Commit)**: `rpi-implement` reconciles all `P01`/`P02` markers, diff boundaries (`e282dc327..HEAD` containing only `#115`'s 10 `src/core` + `infra/` paths and `#115` `.copilot-tracking/` artifacts), and privacy-safe `git config --local user.email` (`8036360+jmservera@users.noreply.github.com`) before handing off to `rpi-review`; after one-pass `rpi-review` creates `.copilot-tracking/reviews/logs/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-review.md` and the parent RPI Agent persists final `Follow-up` state, the parent commits the 7 `immutable-blob-ledger-digests-115-c2-rebase-*` files locally (`docs(rpi): record #115 c2 rebase onto #1641 (e282dc327) RPI artifacts`, `Refs #115`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`), re-verifies targeted checks and `test -z "$(git status --short)"` on the final `HEAD`, and does not push.

## Non-Functional Requirements

* **NFR-1 (Shared-Host Isolation & Zero Ephemeral Debris)**: Zero `/tmp` virtualenvs, zero `pip` writes to `/home/azureuser/.local` editable `.pth` files, and zero untracked `.pyc` or ARM `.json` build files (`PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`, `az bicep build --stdout >/dev/null`).
* **NFR-2 (RPI & Governance Integrity)**: Preserve prior committed critique/review artifacts (`84cb5608a`, `1b66fd607`) unmodified, keep zero `.copilot-tracking/` references in production files or READMEs, and use `Refs #115` (never `Closes #115`).

## Acceptance Criteria

* [x] AC-1: `git merge-base --is-ancestor e282dc3276992a17507351dd4f75d08a8808f56d HEAD` exits `0` on `feat/demo-115-blob-ledger`, `git diff e282dc327..HEAD --name-only` contains only `#115`'s 10 `src/core` + `infra/` paths and `#115` `.copilot-tracking/` artifacts, and `infra/tests/test_monitoring_alerts.py` contains both `#146` and `#115` alert tests with zero conflict markers.
* [x] AC-2: Full `infra/tests` discovery (`600` tests, `REQUIRE_AZ_BICEP=1`), `src/core/tests -p '*ledger*'` (`18` tests), `src/orchestrator/tests/test_digest_blob.py` (`30` tests), and cross-feature `#146`/`#189`/doc-link/dependency-rule tests (`52` tests) pass 100% under verified worktree-only `zava_forward.__path__`.
* [x] AC-3: `ruff check` (`src/core`, `src/api`, `infra/tests/test_monitoring_alerts.py`, and `--isolated --select E,F,I,B,UP` `infra/` targets), `ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py`, `(cd src/core && python3 -m mypy)` (`350` files), and `az bicep build --stdout`/`lint` all exit `0`.
* [x] AC-4: Pre-Review reconciliation completes cleanly in `rpi-implement` (verified), and after post-`rpi-review` parent `Follow-up` commit (`Refs #115`, `Co-authored-by` trailer, no push), `git status --short` is completely empty on the final rebased `HEAD`.

## Test Ownership and Validation Lock

* Applicable test ownership: Merged `infra/tests/test_monitoring_alerts.py` (`#146` + `#115`), existing `#115` suites (`src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`, `infra/tests/test_bicep_policy.py`), and full `infra/tests` discovery (`test_*.py`) plus `src/core` `test_monitoring_coverage.py`, `test_simulator_run_controls_189.py`, `test_dependency_rule.py`, and `test_live_doc_links.py`.
* Exact test removals: `none`
* Maximum new test files: `0`
* Canonical vs generated targets: Canonical conflict resolution in `infra/tests/test_monitoring_alerts.py` and dated `.copilot-tracking/*/*/immutable-blob-ledger-digests-115-c2-rebase-*` RPI artifacts only; zero generated production files.
* Semantic vs regression coverage: Preserves all 10 `test_monitoring_alerts.py` tests (`4` baseline/gate + `1` `#146` `job-rank` + `1` `#115` installed ledger alerts + `4` `#146` cost/budget/anomaly workbook panel tests -> `10` total tests in `test_monitoring_alerts.py`), all `18` `test_ledger_digest_blob.py` tests, all `30` `test_digest_blob.py` tests, and the full `infra/tests` suite (`>620` tests under `REQUIRE_AZ_BICEP=1`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fetch & Rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`)

* <!-- rpi:task id=P01-T01 --> [x] P01-T01: Verify tracked working tree is clean (`git status --short --untracked-files=no`), rebase `84cb5608a` and `1b66fd607` onto `e282dc327` keeping untracked `c2-rebase` RPI artifacts in place, resolve `infra/tests/test_monitoring_alerts.py` preserving both `#146` and `#115` alert tests, and verify ancestry and diff boundaries.

<!-- rpi:phase id=P02 -->
### [x] P02: `src-ci.yml`-Aligned Focused Validation and Pre-Review Reconciliation

* <!-- rpi:task id=P02-T01 --> [x] P02-T01: Verify worktree-only `zava_forward.__path__` isolation across all 5 `src/*` distributions and run full `infra/tests` discovery (`REQUIRE_AZ_BICEP=1`), `src/core/tests -p '*ledger*'`, `src/orchestrator/tests/test_digest_blob.py`, `#146`/`#189`/doc/dependency suites, `ruff check`/`ruff format --check`, `src/core` `mypy`, and `az bicep build --stdout`/`lint`.
* <!-- rpi:task id=P02-T02 --> [x] P02-T02: Verify `e282dc327..HEAD` diff boundary and privacy-safe `git config --local user.email`, reconcile all `P01`/`P02` plan, phase-details, and changes-record markers, and mark `Ready for rpi-review`.

## Critique Disposition

* Single final-candidate `rpi-plan-critique` executed on 2026-11-15 (`.copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-plan-critique.md`): Verdict `Pass` (`0 Critical`, `0 High`, `0 Medium`, `0 Low`). No plan revisions or user escalations required; candidate finalized as `Ready` for `rpi-implement`.

## Follow-Up Items

* Push rebased `feat/demo-115-blob-ledger` (`e282dc327` base) and verify hosted CI checks once the owner authorizes remote publication.
* Harden `zava_forward.core.ledger_digest_blob` with `RV-001` (suppress transport `__cause__` chaining) and `RV-002` (parse `x-ms-creation-time` header duration & optional `require_sealed_years_before` check) alongside delegating `zava_forward.orchestrator.digest_blob` internals to `zava_forward.core.ledger_digest_blob`.
* Obtain Legal retention-duration approval (`#121`), execute irreversible Azure `lockImmutabilityPolicy` on deployed `ledger-digests`, and capture live Container Apps `ledger-verify` + Azure Monitor alert delivery evidence for full Issue `#115` closure.

## Handoff

* Changes-record target path: .copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-changes.md
* Review-record target path: .copilot-tracking/reviews/logs/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-review.md
* Continuation mode: Automatic RPI Agent dispatches single-pass `rpi-plan-critique`, applies compatible findings directly, continues to `rpi-implement` (`P01`, `P02`), runs one-pass `rpi-review`, transitions to `Follow-up`, commits the 7 `immutable-blob-ledger-digests-115-c2-rebase-*` tracking files locally (`docs(rpi): record #115 c2 rebase onto #1641 (e282dc327) RPI artifacts`, `Refs #115`, `Co-authored-by` trailer, no push), and verifies clean `git status --short` on the final rebased `HEAD`.
