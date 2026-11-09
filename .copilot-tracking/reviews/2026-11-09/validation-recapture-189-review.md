<!-- markdownlint-disable-file -->
# Issue 189 validation recapture review (2026-11-09)

One independent read-only Review (code-review agent) of the changes record against the retained raw capture. Executed once; outcome: conformant for the assessed boundary, one medium documentation finding corrected, two low observations. Not repeated for this task. Not an approval of the integrated head: independent exact-head review, hosted CI and human approval remain required.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | Medium (documentation) | The claim that `ok$` counts equal Ran for all API modules was false under a strict ` ... ok$` pattern (39/41, 25/34, 26/27 for three modules where tests print mid-line). | Corrected in the changes record; the `Ran`/`OK` summaries are authoritative. |
| 2 | Low | The changes record was untracked at review time. | Resolved by the evidence commit. |
| 3 | Low | The race hypothesis is plausible but not instrumented. | Already labelled a hypothesis; stays unproven. |

Confirmed by the reviewer: all 16 exit files, counts, 158 skips, the honest and unwaived browser failure (capture and diagnostic rerun 3 at line 156), tree equality of `src`, `infra`, `tools` and `.github` to `d985f1495`, unchanged `src` content hash, 68-entry hash manifest and its own hash, and no overstatement.

## Assessed boundary and routing

Boundary: the recapture records and their raw files. Not assessed: SQL, whole API suite, assistive technology, web guidelines. The browser/axe check is NOT a passing control in the single capture: only 3 of the 11 states ran. Routed later work (user-selected only): scoped correction of the check's non-specific wait, which would be cycle C2 of five and needs explicit authorization; then a fresh browser capture; independent exact-head review and hosted CI.
