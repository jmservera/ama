<!-- markdownlint-disable-file -->
# Details: #80 Closed cases current-page CSV (issue-80-closed-csv-1110)

## P1 progress.py

```python
CLOSED_EXPORT_FIELDS = ("id", "resident", "address", "town", "postcode", "hazard", "status", "team", "closed_on")

def closed_csv(result: dict[str, Any]) -> str:
    # fixed columns, header row always, values pass safe_cell
```

* Import `csv`, `io` and `safe_cell` from `zava_forward.core.list_export`; write with `csv.writer` (same default dialect as `list_export.to_csv`).
* Each cell is read as `row[field]`; a non-primitive value raises `TypeError` so a future non-primitive summary field cannot leak structure.

## P2 server.py

* `get_kind`: `if path in ("/api/closed-cases", "/api/closed-cases.csv"): return "cases"`.
* Dispatch: `url.path in ("/api/progress", "/api/closed-cases", "/api/closed-cases.csv")`. For the CSV path `read = progress.closed_cases`; after the read, send `progress.closed_csv(result)` as `text/csv; charset=utf-8` with `Content-Disposition: attachment; filename="closed-cases-page.csv"`. The `try` block and its three exception mappings are unchanged, so rejections are JSON errors identical to the JSON endpoint and no attachment header exists for them.

## P3 progress.js

After `controls`/`pageLink`, build `const download = new URLSearchParams(values); download.set("page", String(data.page)); download.set("limit", String(data.limit));`. In `show(...)`, after the results status, add a paragraph with id `closed-download-note` and a native `a` with `href` `/api/closed-cases.csv?${download}` and text "Download this page for Excel". Copy: constructed demonstration data; this page only (up to `limit` cases), not every page; read-only copy so editing the file changes no records; blank Closed on means unknown closure date; Closed does not mean works are completed or approved; the file is read again when you download so it may differ from the rows shown. `aria-describedby` points at the note. No CSS added: existing `a` and focus styles apply.

## P4 tests

Write the failing tests first; confirm failure; then implement P1 to P3. Cases:

* Parity: for default, status, team, search, date start/end combined, page 2, oversized page (clamped), limit 2 and 100, the parsed CSV rows and header equal the JSON `items` for the nine fields (bool as Yes/No, None as blank).
* Empty result: header only.
* History: closure/reopen/unknown/ambiguous covered by the fixture (ZF-1 reopen then accept, ZF-4 unknown blank, unmarked ZF-5 excluded).
* Escaping: cases whose resident or address begin with `=`, `+`, `-`, `@`, TAB or CR, plus Unicode, quote, comma and newline values; parsed cells start with an apostrophe for formula prefixes and round-trip otherwise.
* No mutation: cases and audit unchanged after the CSV call.
* HTTP: anonymous 401, Sam (nonmanager staff) 403, contractor 403, Pam 200 with `text/csv` and the attachment name; denied, 400 and 403 responses have no Content-Disposition and no CSV body; malformed, duplicate and unknown parameters give the same status and body as the JSON path.
* Inventory: add `/api/closed-cases.csv` beside `/api/closed-cases` so the existing role matrix covers it.
* Sqlite subclass inherits the parity tests.

## P5 browser

Extend the existing check after the first Closed page load: assert the link and copy, Tab-focus it, press Enter with `expect_download`, parse the saved bytes and compare ids with the API JSON for the same page; repeat with the filtered query (ZF-3) and page 2 (4 rows); zero-result keeps the link with a header-only file; `reset` removes filters from the link; a 503 on `**/api/closed-cases?*` shows the alert and no link; a nonmanager (sam) sees the manager-only message and no link.

## P6 docs

Add a short paragraph to `src/api/README.md` under the progress and closed archive section.

## Done when

Targeted tests pass; default `mypy`, `ruff check` and `ruff format --check` pass with declared versions; browser check passes; final tree has no edits outside the listed files and `.copilot-tracking`.
