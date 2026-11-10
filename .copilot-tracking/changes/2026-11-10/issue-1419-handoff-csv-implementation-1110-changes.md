<!-- markdownlint-disable-file -->
# RPI Changes: unaccepted handoff CSV implementation (#1419)

* Task slug: issue-1419-handoff-csv-implementation-1110
* Plan: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-implementation-1110-plan.md
* Base: merge 4350c3063f5e79703848ac4bdb136c219170d777 (tree 33daf78d81a344b191b269ea619b5aca608ac1a4)
* Interruption: VM reboot 2026-11-10T23:08Z; resumed with artifacts and venv intact; no source edits existed.

## Implementation start (2026-11-10)

Plan-done recorded (seq 3). No source edits yet. Validation tier: targeted (owner demo policy override, not a waiver).

## Changes

* src/api/src/zava_forward/api/server.py: one EXPORT_KINDS entry `/api/handoffs/unaccepted.csv` -> `handoffs`; module-level `_max_age_hours(url)` (first value, blank kept, blank/missing = none, finite float with 0 < v < 1e6 else 400); one shared branch for the JSON and CSV paths (400 same body, 403 PermissionError, CSV via `list_export.to_csv`, `text/csv; charset=utf-8`, `attachment; filename="unaccepted-handoffs.csv"`). 401 and the kind 403 stay before parsing.
* src/api/tests/test_role_endpoint_inventory.py: one GET_ENDPOINTS entry.
* src/api/src/zava_forward/api/web/app.js (pendingHandoffs success path only): native anchor "Download handoff waiting times for Excel" with href `/api/handoffs/unaccepted.csv`, download `unaccepted-handoffs.csv`, plus plain helper text. Existing "Download for Excel" link unchanged. Retry/session helpers, startupFailure, fetchReadRetrying untouched.
* src/api/README.md: ageing paragraph and List-exports sentence.
* NEW src/api/tests/test_unaccepted_handoff_csv_api.py (13 server tests) and src/api/tests/test_unaccepted_handoff_download_ui.py (4 Node-slice, 2 opt-in browser).
* Not changed: core, roles, projection, list_export, thresholds, mutation, ops.js, capacity checker, core README (stale "not yet wired" line left, out of scope).

## Corrections recorded

* The brief/refinement "fourteen fields" claim was wrong: the actual contract has 13 fields and the public issue body needs no change. Withdrawn is also excluded.
* PC-101 limitation (critique, accepted): the link shows only when the user's own pending list is non-empty; empty CSV is tested by direct request.

## Validation record

Tier: targeted (owner demo policy override; not a waiver of any failing check, not a full-gate receipt). Hosted source CI and independent exact-head assessment remain required.

First adverse attempts (kept): UI module run by dotted name failed ImportError (needs `unittest discover -s tests`); Node test `KeyError: 'download'` fixed with `.get`; ruff E501 on the UI test docstring (re-wrapped); mypy 2 errors in the CSV test (`no-untyped-call` plus unused ignore; fixed by moving the ignore to the `App(...)` line).

Final results (own venv /home/azureuser/.venvs/issue1419, editable from this WT, `PYTHONPATH=../core/tests:../agents/tests` test-helper only):

* `python -m ruff check .` All checks passed; `ruff format --check .` 145 files formatted; `mypy` Success, 228 files; `node --check app.js` ok.
* test_unaccepted_handoff_csv_api 13 OK; test_unaccepted_handoff_download_ui 6 OK (2 skipped without flag; with ZF_BROWSER_TESTS=1 all 6 OK in real Chromium, heavy lock acquired, none skipped); test_handoff_api 7 OK; test_list_export_api 11 OK; test_role_endpoint_inventory 24 OK; test_handoff_read_guidance 9 OK (with flag, browser cases ran); test_finance_grants_screens 20 OK.
* test_case_journey: 31 run, 1 FAILURE `test_priority_invocation_and_procurement_preserve_history_barriers` (Node `TypeError ... reading 'nodeType'` in capacityView). It fails identically on an unmodified detached worktree of HEAD (temporary, removed), so it is pre-existing in parent-owned Capacity code (merged parent 2cc340), not introduced and not in owned hunks. Not fixed and not waived; unresolved for the parent.
* Not run: full local gate, SQL, Docker, hosted CI, human/assistive-technology review.
