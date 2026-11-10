<!-- markdownlint-disable-file -->

# Phase Details: issue-152-empty-queue-coverage-correction-1

Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-correction-1-plan.md
Research: .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-1-research.md

## Initial Direction

Defer and remove the declared branch (research Alternative D). Evidence: C1-C6 in the research artifact.

<!-- P01 -->
## P01: Remove the declared branch and correct tests

* P01-T01 `src/api/src/zava_forward/api/web/app.js` (around the `trustedCoverage` and `queueEmptyExplanation` functions and the list-view call site).
  * Delete `trustedCoverage` and its comment; replace the comment with one stating that no authoritative runtime coverage provenance exists, so an empty own queue is unknown.
  * `queueEmptyExplanation({ view, filtered, rowsLength })` keeps no-match, `empty-all` and unknown outputs byte-identical.
  * Call site passes only `view`, `filtered`, `rowsLength`.
  * Done when: `node --check` passes and no `trustedCoverage`/`declared-unrepresented` remains.
* P01-T02 `src/api/tests/test_queue_empty_state.py`.
  * The Node extractor cuts only `queueEmptyExplanation`.
  * Test ownership: this file only. Removals: `test_valid_bound_declaration_is_a_declared_gap_with_provenance`, the stale-variant matrix and page-value-missing loops (they test the deleted validator). Additions at most two: stale/unrelated/unverified provenance regression and a well-formed declaration case, both through the unchanged `coverage` input still being ignored. Retained: coordinator-default unknown, populated null, no-match, all-cases, no-server-producer, wiring (updated tokens).
  * Semantic coverage: behaviour via real function in Node. Regression coverage: AC1 failing on the original source (verified by extracting the original `trustedCoverage` and `queueEmptyExplanation` from `git show HEAD:` and running the same inputs with original arguments; expected actual state `declared-unrepresented`, not a ReferenceError).

<!-- P02 -->
## P02: Documentation and validation

* P02-T01 `src/api/README.md` around the "An empty My cases list" paragraph: three states become no-match, unknown, all-cases wording; state the declared state is deferred until an authorized trusted producer with current fixture and provenance binding exists; any `work_queues.coverage` is ignored; partial AC-034/043 evidence only.
* P02-T02 Validation: `python3 -m unittest tests.test_queue_empty_state` from `src/api` with installed packages; `node --check`; `git diff --check`; README link review; regression-fails-before check; web-design-guidelines fetched with source recorded. Not run: browser, Playwright, SQL, Docker, `--changed`, full gate.

* P02-T03 Commit and record head/tree; refresh web-design-guidelines before review. Also confirm the unknown copy remains accurate and grep `src`, `tools`, `docs` for declared-gap copy, `work_queues.coverage`, `fixture_version`. Changes record notes supersession of parent declared-state claims.
