<!-- markdownlint-disable-file -->
# Issue 189 SQL/main integration review (2026-11-09)

One independent read-only Review (code-review agent) of merge `105ea6cb5` over the integration delta. Executed once; outcome: conformant for the assessed boundary, one low documentation finding. Not repeated for this task. Not an approval of the final integrated head: independent exact-head review, hosted CI and human approval remain required.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | Low (documentation) | The changes record cited skip decorators at `test_resident_decisions.py` lines 3228/4154; actual lines are 3232/4159. `test_priority_order.py` uses an `OPT_IN` helper at `:1743`. | Corrected in the changes record (documentation-only, no source change); no later work. |

Confirmed: merge source diff equals main's `9f9aacc8b..8d6f029ca` (12 files, +2862/-75), no resolution edits; view-only gate (`server.py:1132`) precedes the simulator hook (`:1134`) and #1308 handlers (`:1246-1272`); no `do_PUT/DELETE/PATCH`, no bypassing route; Stop only for a parsed control, Start and Stop disabled for view-only and non-writable controls.

Reviewer did not rerun tests, `node --check` or the browser check; those results are the coordinator-visible producer exits in the changes record.

## Assessed boundary and routing

Boundary: merge delta, composition and records. Not assessed: actual SQL (65 + 93 skipped cases remain unverified), whole API suite, assistive-technology review, web-guidelines refresh. Routed later work: coordinator independent exact-head review and hosted CI; SQL proof only where #1292's owned gate applies; no new C1/C2 cycle was needed. Disclosed boundaries (unparseable control has no Stop; audit-only malformed bulk-edit record precedes the view-only gate) are existing behaviour.
