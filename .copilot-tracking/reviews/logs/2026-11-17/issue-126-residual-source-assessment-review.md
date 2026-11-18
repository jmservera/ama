<!-- markdownlint-disable-file -->
# RPI Review: issue #126 residual source assessment (22 rows)

* Execution: executed once, independent `code-review` sub-agent, read-only, restricted to the 22-row table and changes record at HEAD `01baf8d3df86a28f754da8545d0e8f12012bf350`.
* Outcome: Partial (reviewer verdict). Not a Pass because of one mis-cited reference and thin test links; no closure or acceptance is implied.
* Not repeated in this task (one-pass rule).

## Reviewer verdicts (condensed, original findings preserved)

| Criterion | Verdict |
| --- | --- |
| 1 all 22 rows present once | Pass |
| 2 citations, symbols and blobs exist at HEAD (about 55 sampled lines, 42 blobs, tree id) | Pass with one defect |
| 3 cited tests executed and passed (28 distinct ids; log SHA-256 match) | Pass, weak relevance on some rows |
| 4 no over-claiming (0 of 22 closed; roles proposed or inferred) | Pass |
| 5 lineage (PR1812 commit ancestor of HEAD; main separate) and gaps | Pass |
| 6 git status shows only RPI tracking paths | Pass |

## Findings

1. Medium: MEASURE-04 cited `core/monitoring_coverage.py:162` as review effort; line 162 is the criteria tuple. Review-effort logic is at `REVIEW_EFFORT_STAGES` (line 286) and following. Conclusion stands; citation wrong.
2. Low: MAP-01 test `test_paired_equity...test_ai_task_paired_evaluation_and_transparent_non_ai_comparison` does not exercise `ranking.py` `_support`; the row discloses read, not exercised. Treat as context only.
3. Low: MN-3.2 tiered insufficient while citing tests similar to GOVERN-AUDIT-02 (implemented/source-tested); the distinction (missing retirement review) is not explicit. MN-4.1 proposed is defensible.
4. Low: inline check counts (69 path:line, 44 symbols, 27 tests) were not retained as artifacts; reviewer independent counts agree (28 test ids).
5. Info: the changes record says Complete for P02-P04 with P05 pending; not closure.

## Routing and post-Review handling

* Finding 1 corrected after Review in the table (citation now line 286), recorded in the table row; this review text is unchanged.
* Findings 2-4 route to later work: label MAP-01 test as context, add the tier-rule sentence for MN-3.2, retain check scripts.
* Remaining work (not done here): batch with `test_data_protection`, `test_ai_register_completeness`, `test_source_monitor`, `test_ledger_digest_blob`, `test_regulatory_privacy`, `test_challenges`; all human, DPO/Legal, real-model, witnessed-restore, EU-applicability evidence and qualified owner decisions remain absent.
