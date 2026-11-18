<!-- markdownlint-disable-file -->
# RPI Phase Details: Rebase Issue #115 Immutable Blob Ledger Digests onto `#1641` (`e282dc327`)

## Metadata

* Task ID: issue-115-c2-rebase-164-0905
* Task slug: immutable-blob-ledger-digests-115-c2-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-research.md (`C1`–`C8`)

## Phase Index

| Phase ID | Name                                                                                                  | Status  | Detail sections       |
|----------|-------------------------------------------------------------------------------------------------------|---------|-----------------------|
| P01      | Fetch & Rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`) | Complete    | P01, P01-T01          |
| P02      | `src-ci.yml`-Aligned Focused Validation and Pre-Review Reconciliation                                 | Complete    | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Fetch & Rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`)

### Context

`feat/demo-115-blob-ledger` sits at `1b66fd607` (`fa6f8d1dd` + `84cb5608a` + `1b66fd607`). Fetched `origin/feat/demo-164-chat-grounding-provenance-0900` sits at `e282dc3276992a17507351dd4f75d08a8808f56d` (`fa6f8d1dd` + `704c6b07a` `#109` + `6bdcf7f90` `#189` + `e282dc327` `#146`). Research (`C1`, `C2`, `C3`) proved `infra/tests/test_monitoring_alerts.py` is the sole overlapping file across the 24 branch files and 54 upstream files.

### Intent

Replay `84cb5608a` and `1b66fd607` cleanly atop `e282dc327` while keeping untracked `c2-rebase` `.copilot-tracking/` artifacts in place, resolving `infra/tests/test_monitoring_alerts.py` so every `#146` and `#115` assertion remains active and 100-column formatted, and verifying exact commit ancestry and file boundaries.

### Boundaries

* Included: `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, and conflict merge in `infra/tests/test_monitoring_alerts.py`.
* Excluded: Modifying unrelated production/test files, overwriting `1b66fd607` RPI files, or pushing to `origin`.

### Likely Targets

* `infra/tests/test_monitoring_alerts.py`: Keep `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` (`#146`) followed by `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` (`#115`) inside `AlertOwnerAndRunbookTests`, immediately above `WorkbookPanelTests`.

### Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` fetched at `e282dc3276992a17507351dd4f75d08a8808f56d`.

### Validation Expectations

* `git merge-base --is-ancestor e282dc3276992a17507351dd4f75d08a8808f56d HEAD` exits `0`.
* Conflict-marker grep (`^(<{7}|={7}|>{7})`) across `infra/` and `src/` returns zero matches.
* `git diff --name-only e282dc327..HEAD` lists the exact 24 paths from `84cb5608a` (17 files) + `1b66fd607` (7 files).

### Completion Evidence

* Rebased commit SHAs recorded in changes log, `e282dc327` confirmed as ancestor, and `infra/tests/test_monitoring_alerts.py` conflict-free and `ruff format --isolated --line-length 100 --check` clean.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase `84cb5608a` and `1b66fd607` onto `e282dc327` and resolve `infra/tests/test_monitoring_alerts.py`

#### Context

Untracked `.copilot-tracking/*/*/immutable-blob-ledger-digests-115-c2-rebase-*` files have zero overlap with `fa6f8d1dd..e282dc327` and remain untouched during `git rebase` when `git status --short --untracked-files=no` is empty. Replaying `84cb5608a` produces one conflict in `infra/tests/test_monitoring_alerts.py` at the end of `AlertOwnerAndRunbookTests`; once resolved and continued (`GIT_EDITOR=true git rebase --continue`), `1b66fd607` replays cleanly without conflict.

#### Intent

Complete the two-commit rebase onto `e282dc327` preserving commit messages, trailers, privacy-safe authorship, and both `#146` and `#115` alert assertions.

#### Boundaries

* Included: `git status --short --untracked-files=no`, `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, merging `infra/tests/test_monitoring_alerts.py`, `git add infra/tests/test_monitoring_alerts.py`, and `GIT_EDITOR=true git rebase --continue`.
* Excluded: Force-pushing or altering `e282dc327` history.

#### Likely Targets

* `infra/tests/test_monitoring_alerts.py`

#### Dependencies

* Empty `git status --short --untracked-files=no`.

#### Validation Expectations

* Both `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` and `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` plus all 4 `WorkbookPanelTests` methods exist in `infra/tests/test_monitoring_alerts.py` and run (`10` tests total in `test_monitoring_alerts.py`).

#### Completion Evidence

* Clean rebase exit `0` and verified `git log -n 3 --oneline` atop `e282dc327`.

<!-- rpi:phase id=P02 -->
## P02: `src-ci.yml`-Aligned Focused Validation and Pre-Review Reconciliation

### Context

Research (`C6`, `C7`, `C8`) established three host/CI execution facts:
1. Both `src/api/tests/test_diagnostic_log_privacy.py` and `infra/tests/test_diagnostic_log_privacy.py` exist, and `infra/tests/test_bicep_policy.py` imports `zava_forward.orchestrator.digest_blob`, so `unittest discover -s infra/tests` requires `infra/tests` ahead of `src/api/tests` plus `src/orchestrator/src` on `PYTHONPATH`, with `REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1` matching `src-ci.yml:215,234-239`.
2. `src/core` and `src/api` define `pyproject.toml` Ruff configs (`select = ["E", "F", "I", "B", "UP"]`, `line-length = 100`), whereas `infra/` has no `pyproject.toml` and `src-ci.yml:241-249` lints `infra/` files with `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`.
3. `mypy` lives in user site-packages (`~/.local`), while `src/core/pyproject.toml` pins `mypy_path = ["src", "tests"]`, so `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)` checks all local worktree `src/core` modules strictly without sibling-worktree leakage.

### Intent

Execute the complete `src-ci.yml`-equivalent focused validation suite on the rebased tree and complete `rpi-implement` pre-Review reconciliation cleanly ahead of one-pass `rpi-review`.

### Boundaries

* Included: Module-origin verification, full `infra/tests` discovery (`REQUIRE_AZ_BICEP=1`), `src/core/tests -p '*ledger*'`, `src/orchestrator/tests/test_digest_blob.py`, `#146`/`#189`/doc/dependency suites, `ruff check` & `ruff format --check`, `src/core` `mypy`, `az bicep build --stdout`/`lint`, diff-boundary and `user.email` checks, and pre-Review marker reconciliation.
* Excluded: `tools/rpi-checks.py`, `/tmp` virtualenvs, mutating `~/.local` editable installs, authoring the review log inside `rpi-implement`, or `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-phase-details.md`

### Dependencies

* `P01` complete.

### Validation Expectations

* `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src python3 -c "import zava_forward, yaml; paths = list(zava_forward.__path__); assert len(paths) == 5 and all('/feat-115-blob-ledger/' in p for p in paths), paths"` exits `0`.
* `REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=infra/tests:src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` exits `0`.
* `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/core/tests -p '*ledger*' -q` exits `0`.
* `(cd src/core && PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src:tests python3 -m unittest tests/test_monitoring_coverage.py tests/test_simulator_run_controls_189.py tests/test_dependency_rule.py tests/test_live_doc_links.py -q)` and `(cd src/orchestrator && PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests/test_digest_blob.py -q)` exit `0`.
* `python3 -m ruff check src/core src/api infra/tests/test_monitoring_alerts.py`, `(cd src/core && python3 -m ruff format --check .)`, `(cd src/api && python3 -m ruff format --check .)`, `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_monitoring_alerts.py infra/tests/test_bicep_policy.py`, and `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py infra/tests/test_bicep_policy.py` exit `0`.
* `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)` exits `0`.
* `for f in infra/main.bicep infra/modules/storage.bicep infra/modules/containerapps.bicep infra/modules/operationalMonitoring.bicep; do az bicep build --file "$f" --stdout >/dev/null && az bicep lint --file "$f"; done` exits `0`.

### Completion Evidence

* Zero failures across all commands above, verified `e282dc327..HEAD` diff boundary and privacy-safe `user.email`, and all `P01`/`P02` markers checked `[x]` with `Review readiness: Ready for rpi-review`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute `src-ci.yml`-aligned focused validation suite on rebased tree

#### Context

Running the full `infra/tests` suite (`>620` tests with `REQUIRE_AZ_BICEP=1`), `*ledger*` tests in `src/core/tests`, `src/orchestrator/tests/test_digest_blob.py`, cross-feature `#146`/`#189`/doc/dependency suites, `ruff`, `mypy`, and `--stdout` Bicep builds validates every changed and interacting surface without polluting the working tree.

#### Intent

Prove 100% pass rates across all `src-ci.yml`-equivalent checks on the rebased tree.

#### Boundaries

* Included: All validation commands in `P02` Validation Expectations (with `initial_wait` >= 300s for full `infra/tests` discovery).
* Excluded: Running `tools/rpi-checks.py` or modifying unrelated files.

#### Likely Targets

* Read-only verification across `infra/`, `src/core/`, `src/orchestrator/`, and `src/api/`.

#### Dependencies

* `P01-T01` complete.

#### Validation Expectations

* Every command exits `0` with exact test and file counts recorded in `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-changes.md`.

#### Completion Evidence

* Captured exit codes and counts in `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-changes.md`.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Verify diff/identity invariants and reconcile `P01`/`P02` markers for `rpi-review`

#### Context

`rpi-implement` completes pre-Review reconciliation before handing off to `rpi-review`; immediately after `rpi-review` creates the review log and the parent RPI Agent persists final `Follow-up` state, the parent executes the local `docs(rpi)` commit (`Refs #115`, `Co-authored-by` trailer, no push) and verifies clean `git status --short` on the final `HEAD`.

#### Intent

Verify `git diff e282dc327..HEAD --name-only`, confirm repository-local privacy-safe `git config --local user.email` (`8036360+jmservera@users.noreply.github.com` from `gh api user`), reconcile `[x]` markers in the plan and `Complete` status in phase details, and write `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-changes.md` ready for `rpi-review`.

#### Boundaries

* Included: Diff boundary check, `gh api user` / `git config --local user.email` check, and updating plan, phase details, and changes record.
* Excluded: Authoring the review log inside `rpi-implement` or running `git push`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-phase-details.md`

#### Dependencies

* `P02-T01` complete.

#### Validation Expectations

* `git status --short --untracked-files=no` is empty (only untracked `c2-rebase` `.copilot-tracking/` artifacts exist prior to post-Review commit), `git diff e282dc327..HEAD --name-only` contains only the 24 expected `#115` paths, and `git config --local user.email` equals `8036360+jmservera@users.noreply.github.com`.

#### Completion Evidence

* All `P01`/`P02` markers checked `[x]`, `Complete` status in phase details, and `Review readiness: Ready for rpi-review` recorded in changes log.
