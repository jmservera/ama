<!-- markdownlint-disable-file -->
# Issue 1818 live8 review (single pass)

Outcome: conformant for the focused scope; FULL tier outstanding.

* Diff equals the held commit's source, test and infra text; artifacts not carried over.
* Findings routed: R8-1 run the full gate when the heavy lock is free (blocker for merge); R8-2 approve the receiver `INSERT` grant before deploy; R8-3 re-run the browser checks and SQL Server grant test on the final HEAD.
