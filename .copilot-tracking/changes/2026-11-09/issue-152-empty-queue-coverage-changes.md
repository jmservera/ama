<!-- markdownlint-disable-file -->

# Changes Record: issue-152-empty-queue-coverage

Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-plan.md
Details: .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-phase-details.md
Critique: .copilot-tracking/challenges/2026-11-09/issue-152-empty-queue-coverage-critique.md
Scope declared: full plan (P01-P03). Started 2026-11-09 04:09 UTC from b46a9ad9a9619db535368d1b2cbbddec8110e122.

## Pre-edit gate (P01 precondition)

* web-design-guidelines activated; source `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` fetched with curl at 2026-11-09 04:10:58 UTC, HTTP 200, 8055 bytes, all rule groups read. Fetch succeeded fully; a second fetch occurs before Review.

## P01 Client helper and wiring

* `src/api/src/zava_forward/api/web/app.js`: added `trustedCoverage` and `queueEmptyExplanation` (lines ~462-486); `listView` keeps `asOf = d.as_of` and calls the helper for the empty `li` (lines ~805, 824, 845). Old strings "No open cases are assigned to you. This does not mean the programme has no work." and "No cases match these filters." are preserved as leading text for existing checks.
* Reset, focus, live regions, native controls, sorting, own/all scope and authorization code are untouched.

## P02 Tests

* New `src/api/tests/test_queue_empty_state.py`: Node `vm` runs the real functions from `app.js`; 8 tests covering Coordinator empty default Unknown, PM `ZF-5` populated queue has no explanation, no-match with and without a valid declaration, valid declared gap with provenance, 11 invalid-declaration variants plus empty page values, all-cases wording, tripwire that `taskqueues.contract` has no `coverage` key, and wiring tokens.
* `src/api/checks/workbench_browser_check.py`: added a per-role empty-explanation expectation (no `li.empty` for populated queues; Unknown and no "declared gap" for empty ones) and a no-match "not a statement about scenario coverage" expectation. These are NOT executed (browser/Playwright forbidden while the heavy lock is held).

## P03 Validation and docs

* `src/api/README.md` shared-IA section: documents the three states, the unvalidated-producer absence and the test.
* Checks run (from `src/api`): `python3 --version` 3.12.3; `ruff --version` 0.17.3; `mypy --version` 2.4.1; node v24.21.0.
  * `node --check src/zava_forward/api/web/app.js`: exit 0.
  * `ruff check tests/test_queue_empty_state.py checks/workbench_browser_check.py`: All checks passed.
  * `ruff format --check tests/test_queue_empty_state.py`: pass (after formatting). `ruff format --check checks/workbench_browser_check.py` reports pre-existing drift at lines I did not touch (e.g. 386, 401, 422, 440, 594); I did not reformat the whole file to avoid an unrelated diff.
  * `mypy tests/test_queue_empty_state.py`: Success, no issues.
  * `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_content_standard tests.test_design_system tests.test_accessibility_baseline tests.test_queue_empty_state tests.test_workbench -q`: Ran 51 tests, OK.
* Not run: Playwright/browser (including `test_workbench_live_defaults` and `workbench_browser_check`), SQL, Docker, `rpi-checks --changed/--all` (coordinator will admit exact-head `--changed`). No prior receipt is used.

## Implementation-time web-design-guidelines pass (against the fetched rules)

* src/api/src/zava_forward/api/web/app.js:482 - date rendered as ISO `as_of` text, not `Intl`/`fmtDate`; kept deliberately because the helper is pure and the declaration value is a version-binding identifier; low severity, recorded for Review.
* src/api/src/zava_forward/api/web/app.js:824 - empty state handled in existing `aria-live=polite` results region; no new interactive element, animation, colour signal, or focus change. Pass.
* Other rules (focus, forms, animation, touch, images, dark mode) not touched by this change: pass/not applicable. No visual rendering was performed.

## Discoveries and classification

* Used a one-off Python string replacement to apply the `listView` wiring edit in `app.js` (one occurrence asserted) rather than the edit tool; result verified by `node --check` and the wiring test. Process note only.
* The server-side briefing sentence (`store.py:881`) shares the old empty-state wording; it is a separate surface and unchanged (local judgment).
* Follow-ups F1-F3 in the plan remain outside this task.

## Late implementation amendment (2026-11-09 04:13 UTC, before the review record was created)

* Self-review of the added browser expectation found that, for roles with an empty own queue, the existing wait (`.item` count equals 0) is satisfied before the list loads, so `li.empty` could be absent and the new check would fail spuriously. Added `empty.wait_for()` for empty roles in `src/api/checks/workbench_browser_check.py`. `ruff check` and `py_compile` exit 0 afterwards. Still unexecuted in a browser. The older own-ID assertion that shares the same race is pre-existing and untouched.

## Status

Implementation complete for declared scope; all P01-P03 markers checked; blockers none for the scope; remaining: independent review, exact-head `--changed` gate with Playwright, hosted CI, owner device decision.
