<!-- markdownlint-disable-file -->
# Issue 231 positive browser coverage plan (2026-11-10)

Task `issue-231-positive-coverage-1110`; Refs #231 and parent #149. Details: `.copilot-tracking/details/2026-11-10-issue-231-positive-coverage-1110-details.md`. Research: `.copilot-tracking/research/2026-11-10-issue-231-positive-coverage-1110-research.md`. FOCUSED tier (test coverage only, no runtime contract change).

## Scope

Add two explicit positive scenarios, `231p` (technical complete) and `231qp` (quality accepted), to the existing `src/api/checks/role_screens_browser_check.py`, with a private checker-local fixture wrapper. Negative `231` and `231q` selectors, expectations and branch stay unchanged. No other source, no new checker, no edits to `role_screens_fixtures.py`, `atlas_tensions_browser_check.py` or its test.

## Phases

* [x] P0 Unchanged baseline: Node-render/unit tests and browser `231`/`231q` (done, passed; see research).
* [ ] P1 Implement scenarios, private wrapper and positive branch in the checker.
* [ ] P2 Run selected browser `231p`, `231qp` and negative `231`, `231q` under the lock; unit/Node tests; Ruff 0.17.1 and mypy 2.4.0 on the changed file; verify negative controls still reject positive phrases.
* [ ] P3 Update `src/api/README.md` scenario paragraph; changes record; review (one pass); commit locally with the repository-local privacy-safe identity.

## Success criteria

* Positive scenarios pass only on real server projections (`technical_missing` and `quality_handover_blockers` empty by the server's own computation), with no `page.route` fulfil of detail data.
* Negative selectors unchanged and still pass; negative branch still rejects the two positive phrases.
* No POSTs, case record unchanged before and after, no uncaught errors, 1280 and 320 px Tab reach of every labelled table region, pinned axe handled as before (run or recorded skip).
* No claim of WCAG, assistive-technology, usability, live or production acceptance.

## Stop conditions

Baseline or product failure, a real projection that cannot be satisfied from existing synthetic helpers, an unavailable lock or Chromium: stop and report unchanged. No post-review repair or fresh correction allowance is granted; correction balance UNKNOWN.
