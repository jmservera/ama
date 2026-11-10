<!-- markdownlint-disable-file -->

# Phase Details: issue-152-empty-queue-coverage-correction-2

Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-correction-2-plan.md
Research: .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-2-research.md

## Initial Direction

Remove the nonessential comment (research Alternative C). Evidence: C1-C5, local reproduction.

<!-- P01 -->
## P01: Remove the comment and validate

* P01-T01 `src/api/src/zava_forward/api/web/app.js`: delete the two comment lines directly above `function queueEmptyExplanation`. Test ownership: `src/api/tests/test_content_standard.py` and `test_queue_empty_state.py` unchanged. Removals: the two comment lines only. Additions: none. Generated targets: none. Done when the diff shows only those lines removed.
* P01-T02 Validation from `src/api`: `python3 -m unittest tests.test_content_standard.CopyAudit.test_no_internal_terms_in_web_copy` (failed before, reproduced at the candidate head; passes after); `python3 -m unittest tests.test_content_standard tests.test_queue_empty_state`; `node --check` app.js; `git diff --check`. Semantic coverage: the audit is the regression; the queue test shows behaviour unchanged. Not run: `--changed`, full gate, browser, SQL, Docker.
* P01-T03 Commit with repo-local identity; record head/tree in the delivery response. Refresh web-design-guidelines before Review.
