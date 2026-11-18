<!-- markdownlint-disable-file -->
# RPI Changes Log: Rebase Issue #115 Immutable Blob Ledger Digests onto `#1641` (`e282dc327`)

## Metadata

* Task ID: issue-115-c2-rebase-164-0905
* Task slug: immutable-blob-ledger-digests-115-c2-rebase
* Plan: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-c2-rebase-phase-details.md
* Declared scope: Full plan (`P01`, `P02`)
* Execution status: Complete

## P01: Fetch & Rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc327`)

* Fetched `origin/feat/demo-164-chat-grounding-provenance-0900` (`e282dc3276992a17507351dd4f75d08a8808f56d`) after verifying `git status --short --untracked-files=no` was empty (`P01-T01`).
* Rebased `feat/demo-115-blob-ledger` (`84cb5608a` + `1b66fd607`) onto `e282dc327`, resolving the sole merge conflict in `infra/tests/test_monitoring_alerts.py` inside `AlertOwnerAndRunbookTests` by retaining `#146`'s `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` followed by `#115`'s `test_installed_ledger_alerts_name_owner_resolvable_runbook_and_core_markers` above `WorkbookPanelTests`.
* Replayed commits produced `63ebab9e0` (`feat(core,infra): enforce immutable blob ledger digests and mismatch alerts`) and `1c572b4a9` (`docs(rpi): record #115 rebase onto #164 RPI artifacts`); `git merge-base --is-ancestor e282dc3276992a17507351dd4f75d08a8808f56d HEAD` exited `0`, zero conflict markers remained across `infra/` and `src/`, and `git diff --name-only e282dc327..HEAD` matched the exact 24 expected `#115` paths.

## P02: `src-ci.yml`-Aligned Focused Validation and Pre-Review Reconciliation

* Verified `zava_forward.__path__` isolation across all 5 `src/*` distributions both with and without `PYTHONNOUSERSITE=1` (`['/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger/src/{core,agents,api,orchestrator,importer}/src/zava_forward']`) (`P02-T01`).
* Executed full `infra/tests` discovery (`600` tests, `0` failures, `0` errors, `4` skipped under `REQUIRE_AZ_BICEP=1`), direct `infra/tests/test_monitoring_alerts.py` (`10` tests, `OK`), `src/core/tests` `-p '*ledger*'` (`18` tests, `OK`), cross-feature `src/core` tests (`52` tests across `test_monitoring_coverage.py`, `test_simulator_run_controls_189.py`, `test_dependency_rule.py`, `test_live_doc_links.py`, `OK`), `src/orchestrator/tests/test_digest_blob.py` (`30` tests, `OK`), `ruff check` and `ruff format --check` (`297` `src/core` files, `213` `src/api` files, `2` `infra/tests/` files), `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)` (`350` source files, `0` issues), and offline `az bicep build --stdout` + `az bicep lint` across `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, and `infra/modules/operationalMonitoring.bicep` (`P02-T01`).
* Verified `gh api user` privacy-safe identity (`8036360+jmservera@users.noreply.github.com`) matches `git config --local user.email`, confirmed `git status --short --untracked-files=no` is empty on rebased commit `1c572b4a9`, and reconciled all `P01`/`P02` plan, phase-details, and changes-log markers (`P02-T02`).

## Discoveries, Amendments, and Divergences

* **Immediately relevant current-state update (`P02-T01`, `PYTHONNOUSERSITE=1` vs `~/.local` `azure-*` SDKs)**: During full `infra/tests` discovery, setting `PYTHONNOUSERSITE=1` hid `azure-storage-blob`, `azure-identity`, and `azure-core` installed in `~/.local/lib/python3.12/site-packages`, causing `infra/tests/test_staff_azure.py` (`ProfileCredentialTests`) to raise `ModuleNotFoundError: No module named 'azure'`. Direct verification confirmed that omitting `PYTHONNOUSERSITE=1` while setting `PYTHONPATH=infra/tests:src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src:...` still resolves all 5 `zava_forward.__path__` entries strictly inside `/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger/src/*/src/zava_forward` (zero sibling-worktree leakage) and passes all `74` `test_staff_azure.py` tests and all `600` `infra/tests` tests cleanly. Updated `FR-2`, `AC-2`, and `P02-T01` wording accordingly.

## Validation Summary

* `REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=infra/tests:src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` -> `Ran 600 tests in 173.444s — OK (skipped=4)`
* `REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=infra/tests:src/core/src:src/agents/src:src/api/src:src/orchestrator/src:src/importer/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest infra/tests/test_monitoring_alerts.py -v` -> `Ran 10 tests in 5.800s — OK`
* `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/core/tests -p '*ledger*' -q` -> `Ran 18 tests in 0.013s — OK`
* `(cd src/core && PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src:tests python3 -m unittest tests/test_monitoring_coverage.py tests/test_simulator_run_controls_189.py tests/test_dependency_rule.py tests/test_live_doc_links.py -q)` -> `Ran 52 tests in 6.788s — OK`
* `(cd src/orchestrator && PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests/test_digest_blob.py -q)` -> `Ran 30 tests in 0.207s — OK`
* `python3 -m ruff check src/core src/api infra/tests/test_monitoring_alerts.py` & `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_monitoring_alerts.py infra/tests/test_bicep_policy.py` -> `All checks passed!`
* `(cd src/core && python3 -m ruff format --check .)` (`297` files), `(cd src/api && python3 -m ruff format --check .)` (`213` files), & `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_alerts.py infra/tests/test_bicep_policy.py` (`2` files) -> `All formatted`
* `(cd src/core && PYTHONDONTWRITEBYTECODE=1 python3 -m mypy)` -> `Success: no issues found in 350 source files`
* `for f in infra/main.bicep infra/modules/storage.bicep infra/modules/containerapps.bicep infra/modules/operationalMonitoring.bicep; do az bicep build --file "$f" --stdout >/dev/null && az bicep lint --file "$f"; done` -> `0 errors, 0 lint diagnostics`

## Review Readiness

* Review readiness: Ready for `rpi-review` (full declared scope `P01` and `P02` complete; zero tracked working-tree modifications; post-Review parent `Follow-up` closeout owns committing the 7 `immutable-blob-ledger-digests-115-c2-rebase-*` tracking files locally without pushing).
