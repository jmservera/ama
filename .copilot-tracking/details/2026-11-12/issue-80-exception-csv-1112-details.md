<!-- markdownlint-disable-file -->
# Details: #80 browser-built exception-summary CSV, synthetic demo (issue-80-exception-csv-1112)

Research: [research](../../research/2026-11-12/issue-80-exception-csv-1112-research.md). Plan: [plan](../../plans/2026-11-12/issue-80-exception-csv-1112-plan.md). The normative contract is [PR1462 details](../../details/2026-11-11/issue-80-exception-contract-2122-details.md) (sections 3-9). This file only records how that contract is implemented; where they differ, the PR1462 contract wins.

## Files

* `src/api/src/zava_forward/api/web/role-screens.js`: pure projection and CSV builder, control, note, status, download.
* `src/api/tests/test_exception_register_screen.py`, `src/api/tests/test_data_operator_ai_state.py` (mock only) and `src/api/tests/test_exception_register.py` (O3 only): node harness cases; the all-view no-control assertion is replaced deliberately.
* `src/api/checks/data_operator_browser_check.py`: real-browser download, keyboard, request-count and negative checks; the register-panel "no controls" check becomes "exactly one button".
* `src/api/README.md`: note beside the register section (synthetic demo only, limits).
* No server, store, `list_export`, importer, infra, workflow or permission change.

## Implementation rules

* D1. `exceptionSummaryRows(data, items, unreadable)` returns `null` (fail closed) when `data.state !== "ok"`, when `unreadable > 0`, when `items` is empty, or when any item id does not match `^EX-[0-9]{3,}$`. Otherwise one `[reference, kind, state, owner_role]` array per item, in displayed order, no de-duplication or sorting.
* D2. Kind is the label of the six admitted keys only (a frozen list in the exporter, so a future `exceptionKinds` key stays `Unknown` until a new contract admits it), else `Unknown`. State is `open` only when `status === "open"`, else `Unknown`. Owner role is `data_steward` or `digital_operator` only, else `Unknown`. Raw text is never copied; non-strings become `Unknown`.
* D3. `exceptionSummaryCsv(rows)` writes the header `Reference in this view,Kind,State,Configured owner role`, UTF-8 with no BOM, CRLF after every row including the last, and per cell: apostrophe prefix for `= + - @ TAB CR`, double-quote when the cell has a comma, quote, CR or LF, with quotes doubled. Mirrors `list_export.safe_cell` for strings.
* D4. The rows are projected once at render. The click handler uses only that captured array: no `api` call, no storage, no re-read. The CSV text is built at activation from the captured rows, so the snapshot lifetime is the rendered panel.
* D5. The control is a native `button type="button"` named "Download visible summary (CSV)", in a wrapper placed after the "Open exception items" heading and before the table, only when D1 returns rows. It has `aria-describedby` to the note paragraph, and a sibling `role="status"` element (existing, empty at render) updated on activation.
* D6. Activation: `new Blob([csv], {type: "text/csv;charset=utf-8"})`, `URL.createObjectURL`, a temporary anchor with `download="exception-register-visible-summary.csv"` appended, clicked, and removed in a `finally`; the object URL is revoked in a later task and also on failure. Success text: "Download started: N rows, exception-register-visible-summary.csv" (initiation only). Any exception: "No file was created or the download did not start. Nothing was changed." and the URL is revoked if created.
* D7. Plain click listener attached after creation (not the `onclick` attribute, which `h()` wraps with a second live region and disables the control).
* D8. Note text states: demonstrator only, no operational or real-record use approved; four columns only for the items listed here and your role scope; copy at page load, changes nothing; not a complete list and an empty or short file is not all clear; the reference is per-view and not a stable identity; owners, free text, record, source, case, batch and query identifiers and conflict values are not included; handling and retention of a downloaded copy are not decided or managed here. It avoids the forbidden phrases "audit trail" and "audit history" and makes no zero-audit claim.

## Case matrix (from PR1462 section 8)

| Case | Control |
| --- | --- |
| clean populated, role scope | exactly one button |
| any unreadable entry, empty items, roles-not-named, denied (403), unavailable, malformed, 401, aborted, entry | none |
| non-matching id | none |
| unknown kind, status, owner role | button; cell `Unknown` |

## Tests (small, focused)

* Node harness: new clean fixture is offered exactly one button; the existing full fixture (has `7`) offers none; empty, denied, entry, unavailable offer none; byte-exact CSV for the clean fixture including excluded-field markers (owner email, summary, error, ref, record, case, query ids, conflict values never appear); odd kind/status/role to `Unknown`; prototype-key kind (`constructor`) to `Unknown`; non-matching id gives no button; formula/quote/comma/newline parity table with `safe_cell`; activation makes no `api` call, creates one Blob with the right type and bytes, revokes the URL, status text; builder failure reports no file; single-role scope shown by response only.
* Browser: keyboard Tab reaches the button; Enter fires a download named `exception-register-visible-summary.csv`; saved bytes equal the four-column projection of the JSON response read in the same browser; zero requests on activation; no file in the intercepted empty/unavailable/unreadable cases; exactly one `/api/exceptions` call; no write and no model request; no JS error.
* O3 at Store level in `test_exception_register.py`: one read adds exactly one `viewed_exception_register` ledger entry and leaves the data document byte-identical. Browser activation makes zero requests, so it adds none (O2).
* Added from critique: `state !== ok` with items offers none; failure before and after the click still removes the anchor; both-role response; Space activation, visible focus, `aria-describedby` and status text; mocks in `test_data_operator_ai_state.py` and the host harness gain `addEventListener`.
* Not run: no full gate, no axe unless `ZF_AXE_JS` is supplied.
