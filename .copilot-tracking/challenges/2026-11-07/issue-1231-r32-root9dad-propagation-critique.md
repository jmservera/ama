# Issue 1231 r32 critique (single pass, author-only, before the merge)

* C1 Medium: Taking the child's ranking blobs could lose a root ranking change. Checked: root ranking semantics are unchanged vs 8010 (already propagated in R30); the merge diff is re-verified in step 4.
* C2 Medium: The root diff against the child shows many state-file deletions; a merge must not drop child RPI. Step 4 checks name-status for deletions.
* C3 Low: Main drift b284d0d3 (score only). Not merged; recorded for rebaseline.
* C4 Low: Author-only critique; independent assessment pending.

Proceed.
