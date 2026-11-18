<!-- markdownlint-disable-file -->
# RPI Plan: Rebase Issue #115 Immutable Blob Ledger Digests onto `#164` (`fa6f8d1dd`)

## Task Metadata

* Task ID: issue-115-rebase-164-0820
* Task slug: immutable-blob-ledger-digests-115-rebase
* Parent task: issue-115-immutable-blob-ledger-digests (immutable-blob-ledger-digests-115)
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-rebase-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-rebase-plan-critique.md

## Executive Summary

This plan rebases `feat/demo-115-blob-ledger` (candidate commit `681903493`) onto the updated `origin/feat/demo-164-chat-grounding-provenance-0900` tip (`fa6f8d1dd`, incorporating `#215` `36aeddae3`, `#76` `f71331d42`, and `#216` `fa6f8d1dd`), runs the caller-requested focused validation suite (`ruff check .`, `ruff format --check .`, `mypy`, and the `#115` blob ledger and `test_bicep_policy.py` tests) with `PYTHONNOUSERSITE=1` worktree-isolated namespace paths and `--stdout` Bicep compilation, completes pre-Review reconciliation (`rpi-implement`), and after `rpi-review` and final `Follow-up` state persistence commits the child RPI rebase evidence locally (`Refs #115`) and re-verifies focused validation on the final rebased `HEAD` with `git status --short` completely empty without pushing.

### User Decisions and Requirements Highlights

* Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) and rebase `feat/demo-115-blob-ledger` (`681903493`) onto `origin/feat/demo-164-chat-grounding-provenance-0900`.
* Run focused validation (`ruff check .`, `ruff format --check .`, `mypy`, and the `#115` blob ledger and `test_bicep_policy.py` tests) on the rebased `HEAD`.
* Leave `git status --short` empty and do not push.

### What You May Not Know

* Exactly one file (`src/core/README.md`) conflicts across `243764945..fa6f8d1dd` and `681903493`: both `#115` (`681903493`) and `#76` (`f71331d42`) insert a `2026-11-15` H2 section immediately above the `#108` H2 section at line 9, while `#216` (`fa6f8d1dd`) inserts its H3 section far lower (~line 4913). Keeping `#115` immediately above `#76` preserves reverse-chronological newest-first order and retains every line of `#115`, `#76`, `#108`, and `#216`.
* Global `/usr/bin/python3` on this shared host resolves user-site editable `zava-forward-core` to sibling worktree `feat-164-chat-revocation-0042`; running `unittest` with `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1` and explicit worktree `PYTHONPATH` (`src/core/src`, `src/orchestrator/src`, and `tests` paths, asserting `zava_forward.__path__` contains only this worktree) while keeping system `PyYAML` available isolates PEP 420 `zava_forward` imports cleanly without `/tmp` virtualenvs or shared user-site mutations.

### Unresolved Decisions or Blockers

* None. Hosted CI execution awaits owner push authorization (`Do not push`), and live Azure WORM policy locking (`lockImmutabilityPolicy` after Legal `#121` sign-off) plus live Azure Monitor alert delivery remain open under `Refs #115`.

## Sources and Evidence

* Research artifact: .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-rebase-research.md (`C1`–`C8`)
* Parent RPI state and review: .copilot-tracking/rpi-sessions/2026-11-15/immutable-blob-ledger-digests-115-state.json, .copilot-tracking/reviews/logs/2026-11-15/immutable-blob-ledger-digests-115-review.md

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Continue the RPI loop (`hve-core-all:rpi-agent`) in `/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger` on branch `feat/demo-115-blob-ledger` for GitHub issue #115 starting from clean committed candidate `681903493` (User prompt).
* Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) and rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (User prompt, item 1).
* Run focused validation (`ruff check .`, `ruff format --check .`, `mypy`, and the `#115` blob ledger and `test_bicep_policy.py` tests) on the rebased `HEAD` (User prompt, item 2).
* Leave `git status --short` empty and do not push (User prompt, item 2).

## Goals

* Rebase `feat/demo-115-blob-ledger` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd0493342718a70c134dd9fcb3305cd6c`) while preserving 100% of `#115`, `#76`, `#215`, and `#216` code, Bicep, test, and README documentation changes.
* Verify the rebased `HEAD` against `ruff check .`, `ruff format --check .`, `mypy`, `#115` Blob ledger tests (`src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`, `src/core/tests/test_dependency_rule.py`, `src/core/tests/test_live_doc_links.py`), `az bicep build --file ... --stdout >/dev/null` / `az bicep lint`, and `REQUIRE_AZ_BICEP=1` `infra/tests/test_bicep_policy.py` (plus `infra/tests/test_monitoring_alerts.py`) using `PYTHONNOUSERSITE=1` worktree-only `PYTHONPATH` resolution.
* Reconcile `rpi-implement` evidence ahead of `rpi-review`, and during parent post-Review closeout persist complete RPI child-session artifacts in a clean `docs(rpi)` tracking commit (`Refs #115`) atop the rebased `#115` feature commit so `git status --short` is empty without pushing.

## Scope and Non-Goals

### In Scope

* Rebasing `681903493` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) and resolving `src/core/README.md`.
* Worktree-isolated (`PYTHONNOUSERSITE=1` + `PYTHONDONTWRITEBYTECODE=1`) validation across `src/core`, `src/orchestrator`, and `infra/tests` (`ruff check`, `ruff format --check`, `mypy`, `#115` blob ledger unit tests, `az bicep build --stdout`/`lint`, `test_bicep_policy.py`, `test_monitoring_alerts.py`).
* Child RPI artifacts under `.copilot-tracking/*/*/immutable-blob-ledger-digests-115-rebase-*` reconciled before `rpi-review` and committed locally by the parent RPI agent after `rpi-review` and `Follow-up` state persistence (`Refs #115`, privacy-safe `user.email` `8036360+jmservera@users.noreply.github.com`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`), followed by final `HEAD` validation.

### Non-Goals

* Pushing `feat/demo-115-blob-ledger` to `origin` or modifying remote branches/PRs.
* Running `tools/rpi-checks.py` (full gate) or modifying shared host Python site-packages.
* Expanding `#115` feature scope or modifying `#76`, `#215`, or `#216` implementation files.

## Functional Requirements

* **FR-1 (Ancestry & Conflict-Free Rebase onto `fa6f8d1dd`)**: `feat/demo-115-blob-ledger` is rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd0493342718a70c134dd9fcb3305cd6c`); `src/core/README.md` retains `## Immutable Blob ledger digests and scheduled verification (2026-11-15, Refs #115)` immediately above `## Hazard and safeguarding clock and named owner projection (2026-11-15, Refs #76)` alongside `#108` and `#216`, with zero Git conflict markers and zero unintended file diffs outside `#115` and `.copilot-tracking/`.
* **FR-2 (Focused Lint, Format, Type, Blob Ledger, and Bicep Policy Validation on Rebased Tree)**: Using `PYTHONDONTWRITEBYTECODE=1` and `PYTHONNOUSERSITE=1` with verified worktree-only `PYTHONPATH` (`zava_forward.__path__` restricted to `/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger`), the rebased tree passes:
  1. `ruff check .` and `ruff format --check .` in `src/core` and `src/orchestrator`, plus `ruff check` and `ruff format --check` (`--isolated --select E,F,I,B,UP --target-version py312 --line-length 100`) on `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py`;
  2. `mypy` in `src/core` (`strict = true` across all `src` and `tests` files, enforcing strict typing on `zava_forward.core.ledger_digest_blob` alongside combined `#76` and `#216` modules) and `mypy` in `src/orchestrator` (noting `src/orchestrator/pyproject.toml` skips `digest_blob` and `zava_forward.core.*` by override, while `test_digest_blob.py` and `test_bicep_policy.py` enforce cross-package runtime parity);
  3. `#115` Blob ledger and documentation-boundary tests: `src/core/tests/test_ledger_digest_blob.py`, `src/core/tests/test_dependency_rule.py`, `src/core/tests/test_live_doc_links.py`, and `src/orchestrator/tests/test_digest_blob.py` (with `PYTHONPATH=src:tests:../core/src:../core/tests`);
  4. `az bicep build --file <file> --stdout >/dev/null` and `az bicep lint --file <file>` on `infra/main.bicep`, `infra/modules/storage.bicep`, and `infra/modules/containerapps.bicep`, plus `REQUIRE_AZ_BICEP=1 PYTHONNOUSERSITE=1 PYTHONPATH=src/core/src:src/orchestrator/src` `unittest` execution of `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py`.
* **FR-3 (Pre-Review Reconciliation & Parent Post-Review Clean-HEAD Closeout)**: `rpi-implement` reconciles plan/detail/changes markers, diff boundaries (`fa6f8d1dd..HEAD` containing only `#115`'s 17 committed paths), and privacy-safe `git config --local user.email` before handing off to `rpi-review`; after one-pass `rpi-review` writes the review log and the parent RPI agent persists final `Follow-up` state, the parent commits the 7 child RPI rebase tracking files locally (`docs(rpi): record #115 rebase onto #164 RPI artifacts`, `Refs #115`, required `Co-authored-by` trailer), re-verifies focused validation against the exact final `HEAD` SHA, confirms `git status --short` is empty, and leaves `origin` untouched (`Do not push`).

## Non-Functional Requirements

* **NFR-1 (Shared-Host Environment Isolation)**: Zero `/tmp` virtualenvs, zero `pip` mutations to `/home/azureuser/.local` or global Python editable `.pth` files used by sibling worktrees, and zero untracked bytecode or ARM `.json` build artifacts (`PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`, `az bicep build --stdout >/dev/null`).
* **NFR-2 (Tracking Hygiene & Governance Boundaries)**: Zero `.copilot-tracking/` references in production source, comments, docstrings, or READMEs; `Refs #115` preserved (never `Closes #115`).

## Acceptance Criteria

* [x] AC-1: `git merge-base --is-ancestor fa6f8d1dd0493342718a70c134dd9fcb3305cd6c HEAD` exits `0` on `feat/demo-115-blob-ledger`, and `git diff fa6f8d1dd..HEAD --name-only` contains only `#115`'s 10 `src/core` + `infra/` paths and `.copilot-tracking/` artifacts, with zero conflict markers in `src/core/README.md`.
* [x] AC-2: `ruff check .`, `ruff format --check .`, and `mypy` pass across `src/core` and `src/orchestrator`, and scoped `ruff check` / `ruff format --check` pass on `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` on the rebased tree and final `HEAD`.
* [x] AC-3: `#115` Blob ledger tests (`test_ledger_digest_blob.py`, `test_digest_blob.py`, `test_dependency_rule.py`, `test_live_doc_links.py`), `az bicep build --stdout`/`lint`, and `REQUIRE_AZ_BICEP=1` `infra/tests/test_bicep_policy.py` + `infra/tests/test_monitoring_alerts.py` pass 100% under `PYTHONNOUSERSITE=1` worktree-only imports.
* [x] AC-4: Pre-Review reconciliation completes cleanly in `rpi-implement`, and after post-`rpi-review` parent `Follow-up` closeout commit (`Refs #115`, no push), focused validation passes on final `HEAD` and `git status --short` outputs nothing (empty).

## Test Ownership and Validation Lock

* Applicable test ownership: Existing `#115` suites `src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_monitoring_alerts.py`, plus `src/core/tests/test_dependency_rule.py` and `src/core/tests/test_live_doc_links.py`.
* Exact test removals: `none`
* Maximum new test files: `0`
* Canonical vs generated targets: Canonical `src/core/README.md` conflict merge and `.copilot-tracking/` child RPI records only; zero generated production files.
* Semantic vs regression coverage: Preserves all 18 `test_ledger_digest_blob.py` semantic retention-lock/header/create-only/scheduled-alert tests, `test_digest_blob.py` orchestrator tests, and all positive + 30 negative-mutation policy checks in `test_bicep_policy.py` + `test_monitoring_alerts.py` atop `fa6f8d1dd`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fetch & Rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`)

* <!-- rpi:task id=P01-T01 --> [x] P01-T01: Verify tracked working tree is clean (`git status --short --untracked-files=no`), rebase `681903493` onto `fa6f8d1dd` with untracked child RPI files kept in place, resolve `src/core/README.md` top-of-file H2 section order (`#115` above `#76`), and verify clean ancestry and diff boundary.

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Validation and Pre-Review Reconciliation

* <!-- rpi:task id=P02-T01 --> [x] P02-T01: Verify worktree-only `PYTHONNOUSERSITE=1` `zava_forward.__path__` isolation and run focused validation (`ruff check .`, `ruff format --check .`, `mypy`, `#115` blob ledger tests, `az bicep build --stdout`/`lint`, and `REQUIRE_AZ_BICEP=1` `test_bicep_policy.py` + `test_monitoring_alerts.py`) on the rebased code tree.
* <!-- rpi:task id=P02-T02 --> [x] P02-T02: Verify `fa6f8d1dd..HEAD` diff boundary and privacy-safe `git config --local user.email`, reconcile all `P01`/`P02` plan, phase-details, and changes-record markers, and mark `Ready for rpi-review`.

## Critique Disposition

Single final-candidate `rpi-plan-critique` executed (`.copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-rebase-plan-critique.md`; execution: `Complete`, verdict: `Revise` -> resolved directly to `Ready` with zero user decisions required):

* **PC-001 [High] (`planner-direct`, Resolved)**: Eliminated `/tmp/zf-115-rebase-tracking`, `/tmp/zf-115-rebase-venv`, and `--system-site-packages` + `--no-build-isolation` `pip` installs. Untracked child `.copilot-tracking/` artifacts stay in place across `git rebase`, and Python test/policy suites run with `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1` and explicit worktree `PYTHONPATH` (including `../core/src` for `src/orchestrator` and verified `zava_forward.__path__` origin assertions).
* **PC-002 [High] (`planner-direct`, Resolved)**: Scoped `P02` and `P02-T02` strictly to `rpi-implement` pre-Review reconciliation (`Ready for rpi-review`), moving post-`rpi-review` `Follow-up` state persistence, the local `docs(rpi): record #115 rebase onto #164 RPI artifacts` commit (`Refs #115`), and final `HEAD` / empty `git status --short` verification to parent RPI Agent closeout in `FR-3` and `Handoff`.
* **PC-003 [Medium] (`planner-direct`, Resolved)**: Updated `az bicep build` invocations to `az bicep build --file <file> --stdout >/dev/null` so no untracked `.json` templates are written into `infra/`, and recorded accurate `mypy` coverage boundaries between `src/core` (`strict = true` on `ledger_digest_blob`) and `src/orchestrator` (`digest_blob` skipped by `pyproject.toml` override, runtime parity enforced by `test_digest_blob.py` and `test_bicep_policy.py`).

## Follow-Up Items

* Push rebased `feat/demo-115-blob-ledger` (`fa6f8d1dd` base) and verify hosted CI checks once the owner authorizes remote publication.
* Harden `zava_forward.core.ledger_digest_blob` with `RV-001` (suppress transport `__cause__` chaining) and `RV-002` (parse `x-ms-creation-time` header duration & optional `require_sealed_years_before` check) alongside delegating `zava_forward.orchestrator.digest_blob` internals to `zava_forward.core.ledger_digest_blob`.
* Obtain Legal retention-duration approval (`#121`), execute irreversible Azure `lockImmutabilityPolicy` on deployed `ledger-digests`, and capture live Container Apps `ledger-verify` + Azure Monitor alert delivery evidence for full Issue #115 closure.

## Handoff

* Changes-record target path: .copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-rebase-changes.md
* Review-record target path: .copilot-tracking/reviews/logs/2026-11-15/immutable-blob-ledger-digests-115-rebase-review.md
* Continuation mode: Automatic RPI Agent continues directly to `rpi-implement` (`P01`, `P02`), then runs one-pass `rpi-review`, transitions to `Follow-up`, commits the 7 child RPI rebase tracking files locally (`docs(rpi): record #115 rebase onto #164 RPI artifacts`, `Refs #115`, no push), and re-verifies focused validation plus empty `git status --short` on the final rebased `HEAD`.
