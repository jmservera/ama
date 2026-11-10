<!-- markdownlint-disable-file -->
# Review record: independent assessment of the issue 230 paging check

* Subject: frozen local candidate head `3b54035d662b066985842050bdcaa4c19c158e33`, tree `50d4dc5a4aae2ac90750524e0df459da90406815`, base `736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd`, branch `test/demo-programme-paging-230-1110`, target `feat/demo-ux-coverage-parent-149-1110` (unchanged).
* This is a metadata record. Original artifacts, state, critique, review, handoffs and the original seven-event witness are preserved unchanged.

## Independent assessment (supplied, recorded as received)

* Reviewer: independent Functional review (code-review skill, standard depth) of the complete nine-file, 627-line patch.
* Verdict: approve. Findings: critical 0, high 0, medium 0, low 0.
* Basis: static reading of the patch and the existing recorded evidence (original runs 1 to 9, controls, static log, original witness events) plus targeted adjacent source (`role-screens.js` pager, harness launch). The independent reviewer did not run tests, a browser, git or hash recomputation. It did not execute any new test, and this record does not claim it did.
* Approval is confined to this initial coverage change and the supplied evidence. It is not CI, merge, whole-issue, whole-WCAG, assistive-technology, usability, human, live or production acceptance. Target-parent integration (the moving parent) is not covered.

## Root-supplied verification (not re-run in this loop)

* Original seven-event witness verify exit 0; log sha256 `acdac88a1c745456857548349fdc5e6f457360e8a68727b638d9220f4f9d813a`; diff check exit 0 at the head.

## Original evidence restated

* Baseline before the change: 24 Node/unit tests pass; story 230 browser run 62 PASS with axe skipped.
* Final original run 9 (checker sha256 `6c65fe0344f882e886db7b782713b836b4f4c7c59d1d703313c2b3fd7ecbcda9`): exit 0, 89 PASS at 1280 and 320 px. Axe was skipped, so there is no axe result.
* Observed: real `/api/cases?view=all&limit=50&offset=N` pages of 50 and 10 (60 permitted synthetic cases, unique labels); native keyboard Next and Previous; no GET from Previous on page 1 or Next on the last page; page-local filter and Reset with the not-a-portfolio-total wording; selected home retained; GET sequence 50, 50, 0.
* Fault injection: one explicitly constructed, intercepted `offset=50` abort per width. It is not a real network incident and not backend proof. Old rows, filter status and selected home were retained, recovery text was visible, and retry reached page 2.
* Read-only and origins: no post-sign-in writes, no case-record change, no uncaught page errors, no horizontal overflow; concrete module origins and the served `role-screens.js` hash matched the worktree.
* Static and unit controls: Ruff 0.17.1 and mypy 2.4.0 clean; test_programme_screen 16, test_role_screens 8, test_workbench 5, test_queue_empty_state 7, core test_needs_inventory 11 pass; recipe SHA N/A.

## Adverse history preserved

* Runs 2 to 5 and 7 failed on unreviewed initial-checker assertions (wrong heading text, initial-load GET counted, off-screen `content-visibility` giving empty `innerText` at 320 px). They are initial development failures, not a source-repair cycle. Run 8 and run 9 passed.
* Runs 1 and 6 were refused by the heavy lock (held by another session); stopped with no queue, spin or bypass.
* The original review was coordinator-performed because nested agents were forbidden.

## Witness dispositions

* Original loop (`phase230-paging-coverage-evidence-1110`): events 1 to 7 ok, `commit-complete` claimed the head above. Not retrospectively proved by this loop.
* This record loop (`phase230-independent-record-evidence-1110`): launch, research-open, plan-done and implement-start accepted before this file; review-done and commit-complete follow.

## Limits

* The numeric post-review correction balance remains UNKNOWN. No repair allowance is granted and no budget reset is inferred.
* Issues #230 and #149 remain open. This work refs #230 and #149 only.
* A final metadata assessment by the same independent reviewer is required before publication.
