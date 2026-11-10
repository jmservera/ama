<!-- markdownlint-disable-file -->

# Changes: issue-152-empty-queue-coverage-correction-1

Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-correction-1-plan.md
Details: .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-correction-1-phase-details.md
Scope: full plan (P01, P02). `Refs #152`; first correction of a partial C5 slice, not whole-issue delivery. Tier focused.

## Supersession

This correction supersedes the declared-state claims in the preserved parent artifacts (issue-152-empty-queue-coverage research, plan, details, critique, changes, review and state), which are unchanged. Those artifacts describe a `declared-unrepresented` state that no longer exists in the client.

## P01 Source and test

* `src/api/src/zava_forward/api/web/app.js`: removed `trustedCoverage` and the declared branch; `queueEmptyExplanation({ view, filtered, rowsLength })` returns no-match, `empty-all`, unknown (unchanged copy) or null; call site passes only those values. Any `work_queues.coverage` is ignored. (P01-T01)
* Implementation-time local update (tightly coupled): the `asOf` variable in `listView`, written but no longer read once the declared branch was removed, was deleted. `policy` is still used. `node --check` and the unit test were rerun after this edit.
* `src/api/tests/test_queue_empty_state.py`: extractor cuts only `queueEmptyExplanation`; removed the declared-gap test and the validator variant matrix; added `test_unverified_provenance_never_becomes_a_declared_gap` (well formed, `stale-or-unrelated-fixture`/`unverified declaration`, malformed all stay unknown without declared wording); no-match, populated, all-cases, coordinator-default, no-producer retained; wiring test now asserts the row-count argument and that the removed names are absent. (P01-T02)

## P02 Documentation and validation

* `src/api/README.md`: empty-queue paragraph states coverage is unknown for lack of an authoritative provenance source, the client ignores any coverage value, and the declared state is deferred pending an owner-approved trusted producer. No AC-034/043, device, accessibility, user or deployment completion claim. (P02-T01)
* Regression-before: the original `trustedCoverage` plus `queueEmptyExplanation` with original arguments and matching context, `fixture_version` `stale-or-unrelated-fixture`, `source` `unverified declaration` returned state `declared-unrepresented` (Node v24.21.0). The new test passes on the corrected source.
* Web guidelines: web-design-guidelines activated; source `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` fetched in full (no failure, no truncation) on 2026-11-09 before edits. Refresh occurs in Review.
* Grep across `src`, `tools`, `docs` (PC-002): no remaining `declared-unrepresented`, `trustedCoverage`, `work_queues.coverage` consumer or declared-gap copy except tests asserting absence and `src/api/checks/workbench_browser_check.py:270`, which asserts the text lacks "declared gap" (still true; not run here). `fixture_version` hits elsewhere are unrelated (sensor backfill, progress check). The unknown copy is unchanged and still accurate.

## Validation

| Check | Result |
|---|---|
| `python3 -m unittest tests.test_queue_empty_state` (src/api, Python 3.12.3) | 7 tests OK, exit 0 |
| `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_workbench` | 5 tests OK |
| `node --check` app.js (Node v24.21.0) | exit 0 |
| `ruff 0.17.3 check` and `format --check` on the test file | exit 0 |
| `mypy 2.4.1` on the test file | no issues |
| `git diff --check` | exit 0 |

Not run, by instruction: `tools/rpi-checks.py --changed`/`--all`, Playwright/browser (including the workbench browser check), SQL, Docker, hosted CI, independent review. `tests.test_workbench_live_defaults` also not run (it reads real endpoints). No prior receipt substituted.

## Follow-Up Items

* Owner decision on a dataset-owned runtime coverage producer with authority binding (original F1).
* Manifest status semantics (original F2).
* Coordinator: exact-head `--changed`, browser, independent review and hosted checks.
