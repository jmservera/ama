<!-- markdownlint-disable-file -->
# Plan: revalidate #1419 on the integrated final-parent head

* Research: .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-final-parent-1110-research.md
* Details: .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-final-parent-1110-phase-details.md
* Scope: tracking and validation only. No source edit. Scope of CSV, role, projection, query and UI unchanged.

## Phases

* [ ] P1 Static: confirm `git diff 37828a41 HEAD -- src` is only test_case_journey.py; record source blob hashes; confirm owned imports.
* [ ] P2 Lint/type/syntax: `python -m ruff check .`, `python -m ruff format --check .`, `python -m mypy` from src/api; `node --check app.js`.
* [ ] P3 Targeted tests (own venv, test-helper PYTHONPATH only): test_case_journey (31), test_unaccepted_handoff_csv_api, test_unaccepted_handoff_download_ui, test_handoff_api, test_list_export_api, test_role_endpoint_inventory, test_handoff_read_guidance, test_finance_grants_screens, test_capacity_browser_check (static, no browser).
* [ ] P4 One minimal real browser rerun of the handoff download and read-guidance modules with ZF_BROWSER_TESTS=1 under the non-blocking heavy lock. If busy: record check blocked, no queue, no pass claim, no repeat campaign. No broad Capacity run.
* [ ] P5 Changes record, Review (once, after implement-done), commit own records, handoff to ROOT/handoff-1419-final-parent-1110.md with head/tree/parent, source hashes, raw checks and AC mapping.

## Validation override (carried, dated 2026-11-10)

Owner demo policy keeps the targeted tier. Basis: existing exact permission/store projection reused; no new role, permission or persistence path. Not a waiver of any failing or missing check, not a full receipt. Original PC-001 (full tier) critique stays historical and is not claimed approved for this tier. Hosted source CI and independent exact-head assessment still required.

## Fix rule

A source or test edit is allowed only for a tightly coupled defect evidenced by P2-P4 and recorded here by dated amendment before the edit. Unexpected functional findings are routed to Root; no fallback or waiver.

## Acceptance mapping (to be filled from observed results in changes/handoff)

CSV route and gates; 13 fields and order; included/excluded states; query matrix; role matrix; privacy; immutability; panel link; empty boundary; targeted checks; open human/hosted gates.

## Critique Disposition

Critique file: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-final-parent-1110-critique.md. Executed once, verdict Revise (3 blocking, 1 non-blocking). All applied directly; no user decision needed.

* PC-001 merge coverage: applied. Full diff from 37828a41 to HEAD reviewed: the only non-tracking change is src/api/tests/test_case_journey.py (+2/-1); everything else is parent .copilot-tracking records. The stub filter (flat, then keep nodes with nodeType) equals production show at src/api/src/zava_forward/api/web/app.js:106; h skips falsy kids at app.js:1752. No config or tool changes.
* PC-002 test evidence: applied. All commands use /home/azureuser/.venvs/issue1419/bin/python; record per-module count, skips and exit code; zero discovered, skipped required browser cases and lock contention are reported as incomplete, never pass or waiver.
* PC-003 exact-head identity: applied. The tested commit is merge a8acaba5d343408d3d750e25a4b0008db446ae79 (tree 0820177872bd42d2f8cba1eb2aad80484f77bdc0). The final commit adds only own records under .copilot-tracking/; the handoff verifies that the diff outside .copilot-tracking between a8acaba and the final HEAD is empty and names the final HEAD for CI and independent assessment.
* PC-004 RV-004: applied. The handoff links RV-004 in the preserved old review and states the corrected routing: pre-existing test-fixture defect fixed by the parent, not an established production defect.
