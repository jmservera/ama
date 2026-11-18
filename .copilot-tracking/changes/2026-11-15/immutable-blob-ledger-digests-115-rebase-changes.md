<!-- markdownlint-disable-file -->
# RPI Changes: Rebase Issue #115 Immutable Blob Ledger Digests onto `#164` (`fa6f8d1dd`)

## Metadata

* Task ID: issue-115-rebase-164-0820
* Related plan: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-rebase-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: None
* Review readiness: Ready for `rpi-review`
* Status basis: Rebased `feat/demo-115-blob-ledger` (`681903493` -> `84cb5608a`) cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), verified all focused lint, format, strict type, Blob ledger, doc-link, dependency-rule, Bicep `--stdout` build/lint, and Bicep policy/alert tests (`0` failures), and reconciled all pre-Review markers and boundaries.

## Completed Changes

### `P01-T01` Rebase `feat/demo-115-blob-ledger` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`)

* Fetched `origin feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd0493342718a70c134dd9fcb3305cd6c`) and ran `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` with `git status --short --untracked-files=no` empty so untracked child RPI files remained intact in place.
* Resolved the single expected merge conflict in `src/core/README.md` by placing `## Immutable Blob ledger digests and scheduled verification (2026-11-15, Refs #115)` immediately above `## Hazard and safeguarding clock and named owner projection (2026-11-15, Refs #76)`, preserving reverse-chronological newest-first order alongside `#108` and `#216` sections with zero conflict markers.
* Verified `git merge-base --is-ancestor fa6f8d1dd0493342718a70c134dd9fcb3305cd6c HEAD` (`84cb5608a`) and confirmed `git diff --stat origin/feat/demo-164-chat-grounding-provenance-0900..HEAD` matches the exact 17-file `#115` footprint (`17 files changed, 3768 insertions(+), 9 deletions(-)`).

### `P02-T01` Worktree-Isolated Focused Validation on Rebased Tree (`84cb5608a`)

* Verified PEP 420 namespace isolation under `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src/core/src:src/orchestrator/src`: `zava_forward.__path__` resolved exclusively to `['/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger/src/core/src/zava_forward', '/home/azureuser/source/ama-demo-wt/feat-115-blob-ledger/src/orchestrator/src/zava_forward']` with system `PyYAML` available and zero global `~/.local` mutations.
* `src/core`: `ruff check .` (`All checks passed!`), `ruff format --check .` (`295 files already formatted`), and `PYTHONPATH=src:tests mypy` (`Success: no issues found in 348 source files`, `strict = true` covering `zava_forward.core.ledger_digest_blob` alongside `#76` and `#216`).
* `src/orchestrator`: `ruff check .` (`All checks passed!`), `ruff format --check .` (`16 files already formatted`), and `PYTHONPATH=src:tests:../core/src:../core/tests mypy` (`Success: no issues found in 19 source files`).
* `infra/tests`: `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py` (`All checks passed!`) and `ruff format --check --isolated --target-version py312 --line-length 100 ...` (`2 files already formatted`).
* `#115` Core & Orchestrator Blob ledger, dependency-rule, monitoring-coverage, and live-doc-link tests:
  * `src/core`: `tests.test_ledger_digest_blob` (18 tests), `tests.test_dependency_rule` (2 tests), `tests.test_live_doc_links` (2 tests) -> `Ran 22 tests in 3.042s — OK` (plus `tests.test_monitoring_coverage` 34 tests — `OK`).
  * `src/orchestrator`: `tests.test_digest_blob` (30 tests) -> `Ran 30 tests in 0.262s — OK`.
* Bicep build/lint (`--stdout >/dev/null`) & ARM policy/alert mutation suites:
  * `az bicep build --file <f> --stdout >/dev/null && az bicep lint --file <f>` across `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, and `infra/modules/monitoring.bicep` -> exited `0` with zero untracked `.json` files written.
  * `REQUIRE_AZ_BICEP=1 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH=src/core/src:src/orchestrator/src python3 -m unittest infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py -v` -> `Ran 72 tests in 88.195s — OK`.
  * `python3 tools/rename-zava-tests.py` -> `Ran 25 tests in 0.504s — OK`.

### `P02-T02` Pre-Review Reconciliation & Boundary Verification

* Confirmed `git diff fa6f8d1dd0493342718a70c134dd9fcb3305cd6c..HEAD --name-only` contains only the 17 `#115` paths (`10` `src/core` + `infra/` paths and `7` original `#115` `.copilot-tracking/` artifacts), `git status --short --untracked-files=no` is empty, and `git config --local user.email` is `8036360+jmservera@users.noreply.github.com` (privacy-safe `gh api user` address).
* Confirmed zero new `.copilot-tracking/` references were added to production code, comments, docstrings, or READMEs (`test_live_doc_links` and `test_cutover_audit` boundaries preserved).
* Checked all `P01`, `P01-T01`, `P02`, `P02-T01`, and `P02-T02` markers in the plan and marked `Phase Index` `Complete` in phase details (`PC-002`: parent post-`rpi-review` `Follow-up` closeout owns committing the 7 child RPI rebase tracking files and re-verifying focused checks + empty `git status --short` on final `HEAD` without pushing).

## Plan and Detail Updates

* Updated `Phase Checklist` (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`) and `AC-1`–`AC-4` markers in `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-rebase-plan.md` (noting parent post-Review closeout completes the final-HEAD commit/re-verification clause of `AC-4`).
* Updated `Phase Index` (`P01`, `P02` -> `Complete`) in `.copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-rebase-phase-details.md`.
* Discoveries classified: Local judgment only — zero material scope, architecture, or requirement divergences.

## Blockers and Remaining Work

* Blockers: None.
* Remaining active-plan markers: None (`P01` and `P02` complete).
* Parent post-Review closeout step (`FR-3` / `PC-002`): Execute one-pass `rpi-review`, persist `Follow-up` state, commit the 7 child RPI rebase tracking files locally (`docs(rpi): record #115 rebase onto #164 RPI artifacts`, `Refs #115`), and re-verify focused validation + empty `git status --short` on final `HEAD` without pushing.

## Follow-Up Items

* Push rebased `feat/demo-115-blob-ledger` (`fa6f8d1dd` base) and verify hosted CI checks once the owner authorizes remote publication.
* Harden `zava_forward.core.ledger_digest_blob` with `RV-001` (suppress transport `__cause__` chaining) and `RV-002` (parse `x-ms-creation-time` header duration & optional `require_sealed_years_before` check) alongside delegating `zava_forward.orchestrator.digest_blob` internals to `zava_forward.core.ledger_digest_blob`.
* Obtain Legal retention-duration approval (`#121`), execute irreversible Azure `lockImmutabilityPolicy` on deployed `ledger-digests`, and capture live Container Apps `ledger-verify` + Azure Monitor alert delivery evidence for full Issue #115 closure.
