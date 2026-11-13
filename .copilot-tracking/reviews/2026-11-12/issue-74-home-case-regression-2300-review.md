<!-- markdownlint-disable-file -->
# Review: #74 home case regression slice (issue-74-home-case-regression-2300)

Execution: executed once after implementation by an independent code-review subagent (read-only, no author context; it read the diff, artifacts and evidence files and did not re-run checks), 2026-11-12. Not repeated. Independent exact-head human review is still required before publication and is not claimed.
Assessed boundary: branch research/demo-74-followup-2250 on base eac1206c6ca08bd551e3d0d2384bb87a1f05c24f, the working tree of the two changed files before the local commit; the commit adds only the RPI artifacts, state and a result file around that tree.
Outcome: Conformant with limits. No material finding open.

## Findings

* Low (applied): the changes record said the A2 mutation "fails the building flag"; the evidence shows a `KeyError` test error at line 130. The record now says so. No material finding.

## Evidence checked by the reviewer

* Scope: exactly two modified files; no product source edit; no `funding_confirmed` assertion; no criterion 2, outcome tuple or G5 claim.
* Each new assertion has a matching failing scratch mutation (browser M1-M8, API A1-A4); the corrected and discarded first runs are disclosed.
* The ZF-3 navigation follows the ZF-2 reflow and axe scan and precedes the write guard and JS error check; final browser run 24 PASS, COMPLETE with axe 4.10.3; API 5 OK; core 7 OK.
* #82 overlap: path-level only; hunks disjoint (append at end of class).

## Limits and residual risks

* Focused tier only: no complete gate, no `--changed`, no hosted CI (no push), no SQL Server, no assistive-technology evidence, Chromium only, synthetic data.
* Isolation is proven for the seeded sentinel records only; shared document names are identical across the two homes.
* Both new tests and the browser check depend on COST-1 having the same 6000.00 allocation and 12000.00 building cost on both homes.
* Criterion 2 of #74 is not proven or ticked; owner outcome definition (G5, outcome tuple) is untouched. A PR must use `Refs #74`.
