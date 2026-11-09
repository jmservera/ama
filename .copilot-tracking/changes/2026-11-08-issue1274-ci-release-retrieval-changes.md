---
title: Issue 1274 hosted CI release retrieval changes
ms.date: 2026-11-08
---

Branch `fix/ci-release-retrieval-1274`, base `0f05e9aae70768def8d1d9c300215f9ee2f11638` (origin/main re-fetched, unchanged). Refs #1274; no closing keyword.

## Changes

* `tools/install-actionlint.py` (new): pinned actionlint 1.7.7 installer. Official browser URL then official release asset API (ids 221573254 archive, 221573261 checksums), 3 attempts per source, 2 s and 5 s delays, 30 s timeout, 8 MiB cap, pinned SHA-256 and size, checksums file must list the pinned archive digest, only the `actionlint` member extracted atomically, token sent only to api.github.com and dropped on redirect, exit 1 and no binary on exhaustion.
* `tools/test_install_actionlint.py` (new, 12 tests): 504 then recovery, exhaustion to API fallback, truncated, wrong checksum, bounded 6-request exhaustion, 404 skip, token handling, oversized, checksums mismatch, invalid or binary-less archive leaves nothing, exit codes.
* `.github/workflows/src-ci.yml`: `Native workflow actionlint` step uses the installer and asserts version 1.7.7; `paths` filter, test, ruff, format and mypy lines include the new tools. Job and check names and permissions unchanged.
* `tools/ci-affected.py` and test: new tools select the namespace job only.
* `tools/rpi-checks.py`: `WORKFLOW_HASHES["src-ci.yml"]` now `4fb913e1ac29772b4a4a6ee82a08f05ab0a917d3cd64974dd461dc960e159122`.
* `infra/README.md`, `docs/reference/log.md`: one paragraph and one log entry.

## Actual validation (exits captured directly, stdin /dev/null)

* test_install_actionlint 12 OK; test_ci_affected OK; test_backlog_sync 17 OK; `tools/test_rpi_checks.py` 86 OK (exit 0, no skips); `infra/tests/test_pipeline.py` exit 0.
* ruff check and format `--isolated` exit 0 on all seven tool files; `mypy --strict` and backlog mypy exit 0; YAML parses; `git diff --check` exit 0.
* Actual integration: real installer run exit 0, both assets verified (browser URL succeeded on attempt 1 at that moment; a live `HEAD` of the same URL earlier returned 504), `actionlint -version` 1.7.7, binary SHA-256 `9f7dedb4e23f89f2922073d1a6720405b7b520d4f5832ebb96f0d55a2958886c`, actionlint on the five native workflows with repository config exit 0. API-only retrieval of both assets separately verified (archive `023070a2...0757`, checksums `ac22e657...51e0`). Nothing from a failed or partial download was executed.
* Skipped with reason: `rpi-checks.py --changed/--all` (workflow path escalates to the full matrix; owner policy is CI-first, no local all-project gate), images, scans, SQL, browser, Azure, API2007.

## Blockers and divergences

* AWF 0.28.23 `install_awf_binary.sh` 504s occur in the gh-aw generated `rubric-score.lock.yml` via upstream `gh-aw-actions/setup`. No repository source hook, so no change and no hand edit. Open partial blocker.
* Old runs do not consume this workflow. Resume route: after owner-approved merge, each of #1243, #1271 and #1273 needs its head to contain the new `src-ci.yml` (normal base update chosen by its owner) and a fresh hosted run on that head. Rerunning old runs reuses the old workflow. #1273 c162 cause was not established here.
