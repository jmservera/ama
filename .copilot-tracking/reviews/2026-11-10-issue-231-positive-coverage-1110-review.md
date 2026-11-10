<!-- markdownlint-disable-file -->
# Issue 231 positive browser coverage review (2026-11-10)

Review executed once, by the implementing agent over the working-tree diff against `736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd` (two files: `src/api/checks/role_screens_browser_check.py`, `src/api/README.md`), before the commit. Author review only: it is not the independent exact-head assessment, which remains required before publication. Refs #231 and parent #149 only.

## Outcome

Conformant for the FOCUSED tier on the assessed boundary, with the residuals below. No open material finding; nothing is routed back to Implement or a second Review in this task.

## Checks against the brief

* Baseline first: unchanged unit and `231`/`231q` browser cases passed before any edit; no stop condition.
* Negative controls: the diff removes only three lines (the `STORY_ACCESSIBLE` tuple, the scroll-into-view tuple and the data dispatch line, each extended or reshaped); the `231`/`231q` expectations, `STORY_231`, and the negative `else` branch are textually unchanged. The mutation proof showed the negative selectors fail on positive data and the positive selectors fail on negative data.
* Real projection: no `page.route` for positive detail; empty `technical_missing` and `quality_handover_blockers` come from the server's own computation (probe and rendered state). Hazards are absent rather than released; no gate, rule, migration, role or approval inference. Synthetic `SYN` names are test inputs, not professional approval.
* Coverage: record-not-approval wording, source, checklist and person evidence, one textual ready record, no blocked wording, native labelled table regions reached by Tab at 1280 and 320 px, same home retained, no write controls, no POSTs, case record equal before and after, no uncaught errors (generic checks), pinned axe ran at 1280 px with no violations and `incomplete []`.
* Ownership: no change to `role_screens_fixtures.py`, `atlas_tensions_browser_check.py`, `test_atlas_tensions_checker.py`, app, backend, Core, SQL, schema, panels or styles. #130 and #111 excluded.
* Recipe: not a registered recipe, so SHA and Core manifest updates are N/A.

## Residuals (not defects)

* `ruff format --check` fails on a baseline hunk (the pre-existing `evaluate` line in `check_design_system_use`); not edited here and not caused by this change.
* axe runs once at 1280 px (existing handling); Tab reach is repeated at 320 px. No conformance claim; human assistive-technology, WCAG, usability, live and production acceptance of #231 remain unproven and separate.
* `web-design-guidelines` source retrieval was not performed because no web file (JS, CSS, HTML) was changed; the change is checker and documentation only.
* The fixture is one constructed home; other positive combinations (several measures, handed-over records) are not covered.
* Correction balance UNKNOWN; no repair or fresh allowance used or granted.
