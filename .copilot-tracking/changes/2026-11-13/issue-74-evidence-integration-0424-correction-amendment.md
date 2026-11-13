<!-- markdownlint-disable-file -->
# Correction amendment: #74 evidence integration (issue-74-evidence-integration-0424)

Date 2026-11-13. Documentation-only correction of candidate `1d105e37fef55001b45f922fbd2bfdd3c4973ce6` after the independent review [REVISE](../../reviews/2026-11-13/issue-74-evidence-independent-review-0435-review.md) (preserved byte-for-byte, verdict and evidence unchanged). Not a source correction, budget reset or new authority. Chronology: candidate commit, then independent review, then this amendment.

## IR-001 (Medium), addressed

Raw logs re-read: `core-attempt1.log` ends `ModuleNotFoundError: No module named 'zava_forward'`. `api-attempt1.log` and `api-attempt2-invocation-error.log` are byte-identical (`cmp`), both `No module named 'test_home_case_api'` (wrong selector). Two identical files do not prove two independent executions; the API attempt count is left unclaimed. No API missing-dependency failure is evidenced. The pack bullet and the integration research were corrected, with a supersession note. The original `issue-74-building-separation-0400-v1-unit-changes.md` line 16 and all unit files are unedited. The 8 core and 6 API passes and zero skips are unchanged; no rerun.

## IR-002 and IR-003 (Low)

IR-002: noted in the pack that the original observation plan has unchecked phase boxes; the plan is unmodified. IR-003: axe scope (ZF-2 `main` only) added to the browser evidence row.

## Other updates

Existing index row and log (new appended entry only) updated. No broader scope; source-authority research is not an input; no source grant, tick or closure.

## Validation (documentation)

Link, ASCII and `git diff --check` review; byte comparison of the preserved review and original files. No executable gate.
