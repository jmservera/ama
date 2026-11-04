<!-- markdownlint-disable-file -->
# Review: issue 948

Execution: one self-review of the final diff. Outcome: conformant for the slice.

* Both acceptance criteria are met by tested code. The report gains a `dropped_accepted_proposals` field on each candidate and the baseline; consumers reading `verdict.regressions` will see the new key. No consumer elsewhere in `src/` was found.
* Remaining: independent exact-head review, hosted CI and human approval. No model, price or spend approval is implied.
