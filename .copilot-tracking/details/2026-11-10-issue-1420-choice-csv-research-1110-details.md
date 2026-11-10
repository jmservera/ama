<!-- markdownlint-disable-file -->
# Implementation Details: Resident-choice portfolio page CSV summary (issue 1420)

Plan: [plan](../plans/2026-11-10-issue-1420-choice-csv-research-1110-plan.md). Research: [research](../research/2026-11-10-issue-1420-choice-csv-research-1110-research.md). Pin parent `12d3ac842`. Proposal only; nothing here is implemented or approved.

## 1. Serializer `resident_choice_export.py` (new)

* `CHOICE_QUEUE_EXPORT_FIELDS`: the eight headers in the plan, fixed tuple.
* `choice_queue_csv(page: Mapping) -> str`: reads `items`, `limit`, `offset`, `total` from the store result; builds each row from `id`, `measure_decisions`, `resident_update` only (never `address`, `town`, nested `versions[].note` and the rest).
* Helpers port the UI rules: `latest(measure)` = highest version in `versions`; `binding` = `revision <r>, design <d>` from the version's `context_revision` and `design_version`; `stopped(measure)` = current status Paused or Withdrawn, or `review.status == "Needs human review"` with `review.decision_version` naming a Paused or Withdrawn version; summary text identical to the UI wording.
* Fail closed: measure names outside the controlled vocabulary become `Measure name withheld`; statuses outside the closed sets become `Unknown`; incomplete measure evidence gives `Unknown (evidence unavailable)` in the stopped column; a Declined version with retained `Needs human review` is listed (plan Q5, Q6). Add an HTTP test that patches `resident_choice_queue` to raise and asserts 5xx JSON, no `Content-Disposition`, no CSV.
* Missing: status -> `Not recorded`, other -> `Unknown`; no value ever blank. Cells coerced with `str()` for text and `int` for counts; anything else raises `TypeError` (same stance as `closed_csv`), mapped by the route to 5xx JSON.
* Output: `csv.writer` over `io.StringIO`, header always, each cell through `list_export.safe_cell`, `\r\n` line endings as the shared writer.

## 2. Route `server.py` (narrow hunks)

* `get_kind`: separate `if path == "/api/resident/choice-queue.csv": return "resident_choice_queue"` before the final dict line.
* Dispatch near the JSON route (~790): same `num(q, "limit", 50, 1, 100)` and `num(q, "offset", 0, 0, 10**9)`, `s.resident_choice_queue(u, limit, offset)`, serializer, `_send(200, body, "text/csv; charset=utf-8", {"Content-Disposition": ...})`. Reuse the neighbouring `PermissionError` handling so errors stay JSON; no partial CSV before serialization finishes (build the full body first).
* Local import inside the branch to avoid import-order churn in a file 1419 also edits.

## 3. UI `role-screens.js`

* In `summary(queue)` loaded-items branch only: anchor plus note paragraph using existing helpers' element style; href built from `queue.limit` and `queue.offset` coerced to integers; text per plan. No `button`, no `download`.

## 4. Existing assertions that must change

* `test_resident_choice_screen.py::test_queue_summary_is_read_only_and_names_scope` forbids any `a`: change to allow exactly one anchor whose href starts `/api/resident/choice-queue.csv`, still forbid the others; keep the failure test asserting no anchor.
* `role_screens_browser_check.py` story 232: the region locator forbids `button` and `tel:`/`mailto:` only; the link sits outside the region so no edit needed unless the checker is later run and the layout differs. Not run now.

## 5. Tests `test_resident_choice_export.py` (new)

* Serializer unit tests with constructed pages (no store): header-only empty, absence labels, stale stop text, formula and newline cells, canary absence, TypeError on nested values.
* HTTP tests following `test_progress_dashboard.py:1142-` (ThreadingHTTPServer, login cookies, synthetic dataset like `test_resident_choice_queue.py`): roles, 401, params matrix, closed exclusion, ordering, omitted detail via patch, unchanged state and audit, no Content-Disposition on errors, body parity with serializer.
* `test_role_endpoint_inventory.py`: add the path as a new line; the existing all-roles test then covers no-500.

## 6. Order of work after admission

1. Root orders the shared edits against 1419 and admits files.
2. Re-pin to the then current parent and re-diff the nine source files.
3. Implement serializer and tests (red), route, UI, assertions; run targeted tests only; independent Review.

## 7. Risks

* 1419 conflicts in `server.py` and the inventory list. Mitigation: one-line additive hunks, ordered integration.
* Role parity is a hypothesis; redaction may differ for note and reason fields not exported.
* Case id is linkable to an address elsewhere; not an authorization of real exports.
* Excel UTF-8 without BOM; same as existing exports.
