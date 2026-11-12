<!-- markdownlint-disable-file -->
# Research: post-fix-wave checkpoint for #440 (2026-11-12)

* Task ID: `post-fix-wave-440-1112`; branch `docs/demo-fix-wave-checkpoint-440-1112`; model label asserted (Claude Sonnet 5.5), no host attestation.
* Research disposition: `executed`. Planning Readiness: `Ready`.
* Trigger: completion of one specific feature/fix wave (issues #128, #98, #115; PRs 1481, 1483, 1482) under existing issue #440. Not a whole-product audit, epic closure, new issue, new feature or reset of earlier correction budgets. The preceding checkpoint is the post-153 section (PR 1480, merge `cd81888e4a81cf4c712d50b357ca900fd5c8c06b`); it is a baseline, not a fresh result.
* Mandatory reads: `case_study_48_original.md` (read in full), `case_study_48_addendum.md` (158 KB; section headings and the sections relevant to ledger, paired equity and held forms only, not end to end), `docs/reference/README.md` index (entries for #440 checkpoints), `docs/reference/memory.md` (headings and preferences; context, not evidence), `docs/reference/regulatory/README.md` not needed (no regulatory claim is made).

## Identities (fresh `git fetch origin main`, 2026-11-12)

* `origin/main` = worktree HEAD = `e155c88ed6357259a11520e7150b7ad9d349b9f8`, root tree `82eea54a212bbb442e7c2257e1349480faa18505`; `src` `7b61d44bc705c2a52799bf1e3478f383de503dff`, `docs` `8fe82ba5b6370c7cada2febae74e062b2669ed04`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `infra` `be7fa0b2502ed1b27f3fcfb76f8207143e50850e`. Worktree clean at start.
* Delta from baseline `cd81888e4` (`git diff --stat`, non-tracking paths): 11 files, 216 insertions, 28 deletions; `tools` tree unchanged.
* PR 1481 (#128, `feat`/`fix` title mismatch: commit says feat, PR title says fix) merge `59eac895112ebb97cfa6c27413b3d398e6f056e4`, tree `8fcebb38afee1d8eb995c75981f8512f3ba40a75`, head `090b7aa2655e`, merged 2026-11-12T21:38:04Z. Paths: `paired_equity.py`, `test_paired_equity.py`, `src/core/README.md`, `equity-journey-test-plan.md`, `log.md`.
* PR 1483 (#115) merge `43b2187b918206666c63cb25d8b338be09791118`, tree `67cbe8ede92d4f9f02ac3a3f71d0de06872f6b55`, head `a8d4ff4dbfc6`, merged 21:50:20Z. Paths: `digest_blob.py`, `test_digest_blob.py`, `infra/tests/test_bicep_policy.py`, `src/orchestrator/README.md`.
* PR 1482 (#98) merge `e155c88ed6357259a11520e7150b7ad9d349b9f8`, tree `82eea54a...`, head `7679894a3973`, merged 22:00:46Z. Paths: `form_export.py`, `test_form_export.py`, `src/core/README.md`. Two commits squashed: the fix and a hosted-typing correction (test helper imports).
* #128, #98, #115, #440 OPEN (live `gh`). No closing keyword in the three merges (`Refs`).

## What each change does (source read at the pin)

* #128 `paired_equity.py`: adds `source_completeness` (contrast `source_record` complete versus missing) as a fourth required dimension; `_position` returns `None` when the ranker leaves the case out and `_check_pair` reports `excluded` instead of raising `StopIteration`. Only consumers: tests. `fairness_evidence` and `activation_allowed` stay false.
* #115 `digest_blob.py`: `main()` wraps `_publish_and_verify()`; `DocumentStoreError` text unchanged; any other `Exception` prints `LEDGER_DIGEST_ALERT ledger verification could not run: <TypeName>` and exits 1; absent URL exit 2 and `--reconcile` unchanged; `SystemExit` passes through. Bicep test binds the two ledger alert queries to `ALERT_MARKER` and `OK_MARKER` (static, `infra/tests/test_bicep_policy.py`).
* #98 `form_export.py`: `export_freshness` now compares the digest-covered `open_issues` per saved field, reports "An open validation issue changed.", and treats a malformed issue list as Invalid (`_issues_by_field`). Consumers: core tests; the API server only calls `draft_export` (held download at `server.py:1204`), not `export_freshness`, so there is no HTTP surface for the freshness fix.

## Requirement and ADR anchors (document-qualified; proposed or draft, not approval)

* PRD `zava-forward-retrofit-programme-demonstrator.md` 0.21.0 `in-review`, blob `c788b917bafa`: FR-043 (stale propagation to exactly dependent items; AC-051, `Not run` in the PRD), FR-042 (reviewed export does not establish submission), FR-054 and AC-073 (paired cohorts, missing data never lowers priority). BRD `agentic-retrofit-programme-brd.md` 0.21.0 `draft`, blob `34d88395de86` (NFR-008, NFR-009, RULE-005 cited by #128). ADR 0002 (status Proposed, blob `cbe21530043f`): decision 2 (digests to immutable Blob container with retention lock and scheduled verification) and DH-007. ADR 0003 `d60645397b20` and 0006 `956da1a3b804` Accepted (context only). The older PRD `proper-warm-...` 0.13.0 is not the current PRD.
* #115 criteria both unticked (immutable container with retention lock; scheduled verification alerts on mismatch). #98 criteria 1 and 4 ticked previously; 2 and 3 unproven. #128 criteria unmet.

## Adverse and process qualifications to preserve (from original artifacts)

* #128: the independent critique ran after the draft plan/implementation draft was written; its High finding (exclusion crash) was added to scope and fixed failing-first. Review CLEAN with one non-defect note (reference-only exclusion passes under the stated rule).
* #98: first focused mypy ran on `form_export.py` only, not the configured scope; hosted SourceCI run 43308748514 failed configured `mypy` with two `attr-defined` errors at `test_form_export.py:170,172`; corrected in the same PR (correction 1). Pinned tool versions differed from the installed ones.
* #115: initial wrong-tool/config checks; ruff 0.17.3 installed versus 0.17.1 pinned; pre-existing RUF100 at `test_bicep_policy.py:168`; the review agent could not run orchestrator tests in its own environment; Low open note (a `DocumentStoreError` while opening the store would print its message; no store module raises it); residuals: `SystemExit` from SQL configuration bypasses the marker; tracebacks no longer printed for unexpected errors.
* 1483: per the coordinator brief, an immediate GraphQL `UNKNOWN` merge-state response was followed by a normal guarded accepted merge. I did not re-observe this; PR 1483 shows `MERGED` at 21:50:20Z.

## Check plan inputs (local-first ladder)

* Cross-package contract: orchestrator marker constants against the Bicep alert queries (infra static test); core held-form tests plus the API held-download HTTP test (`src/api/tests/test_form_held_download_api.py`, local server fixture, synthetic); `test_form_dependencies.py` (stale propagation consumer); `test_journey_register.py` (paired equity dependency).
* Not relevant or not run: SQL Server (`ZF_TEST_MSSQL`), browser harness, Docker image, scanners, hosted CI, Azure, models, live endpoint, private data, `support/`.
* Unmerged candidates 107, 134, 153, 157, 435, 82 and their sibling functionality are excluded.

## Findings so far

* No new defect is confirmed at research time. The three merged residuals above already live in the feature review artifacts; owners are #115 (SystemExit, traceback, store-open Low note) and #128 (reference-only exclusion note). No new issue is authorised.
