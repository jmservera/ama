<!-- markdownlint-disable-file -->
# Details: #80 exception-register CSV contract (issue-80-exception-contract-2122)

Research: [research](../../research/2026-11-11/issue-80-exception-contract-2122-research.md). Plan: [plan](../../plans/2026-11-11/issue-80-exception-contract-2122-plan.md). Critique: [critique](../../plans/2026-11-11/issue-80-exception-contract-2122-critique.md).

Status of everything below: PROPOSED. It is a design contract for a possible later source slice. It is not approved, not implemented, not an owner decision and not an operational export approval. No source slice is admitted by this document.

## 1. Chosen shape

A browser-only, four-field "visible summary" CSV built in the data steward and operator screen from the `/api/exceptions` response that screen already fetched and rendered. No new endpoint, no second request, no change to `exception_register`, `Store`, roles, projection or `list_export`.

Rejected for this slice: a server `GET /api/exceptions.csv` route. It would add a second authorised read and audit line, a new `get_kind` and endpoint-inventory entry, and a second 403 path, without exposing anything the visible summary lacks. It becomes the design only if the owner later wants fields beyond the screen (then a new field-level contract and a fresh admission are needed).

## 2. Definitions

* Controlled domain: every record the register reads or could affect: cases and their tasks, handoffs and stock queries, recommendations and AI run records, import-refusal evidence, the exception queue, rule, funding, finance, governance, retention, continuity and registry stores, and the persisted data document (`ZF_DATA`).
* Existing audit behaviour: the `Store.audit` append to the hash-chained audit ledger that `exception_register` already performs on view (`viewed_exception_register`) and on denial (`denied`). This is explicitly PERMITTED and unchanged.
* Visible summary: the rows of the table "Exception items returned for you" that the screen rendered from the one authorised response, restricted to the four fields in section 4.
* Readable item: an item for which the screen's `exceptionItem` check passes (object with string `id` and string `kind`).

## 3. Source-of-truth and write rules

* R1. The file content comes only from the already-received, already-rendered response for the signed-in user. The export step makes no network request (no `/api/exceptions` repeat, no `.csv` route, no other API call).
* R2. The export step writes nothing to the controlled domain. The page load that precedes it keeps its existing, permitted audit lines; the export activation itself adds zero audit lines because it makes zero requests.
* R3. No browser persistence: no localStorage, sessionStorage, cookie, IndexedDB or cache write caused by the export. The object URL is created on activation and revoked after the download is started.
* R4a. The note and status text do not assert that the register's data is synthetic, because the register reads whatever store is configured; the demonstrator boundary is stated as the absence of approval, not as a claim about the data.
* R4. No AI provider, model, cloud, transport or spend call. Values are copied as text and never interpreted.
* R5. The source file, ledger, import refusals and history are unchanged: the diff of any later slice must show no edit under `exception_register.py`, `exception_queue.py`, `exception_feeds.py`, `import_refusals.py`, `store.py`, `list_export.py`, importer, infra or the existing register tests' read-only assertions.
* R6. Read-only and one-way: the file is a copy; editing it changes nothing, and nothing reads it back (consistent with `list_export` and FR-030/SA-006).

## 4. Fields (exactly four, in this order)

| Column header | Value | Source on the response | Unknown rule |
| --- | --- | --- | --- |
| Reference in this view | `item.id` only when it matches `^EX-[0-9]{3,}$` | `items[].id` | A readable item whose id does not match makes the list unsafe: no file is offered (fail closed, section 6) |
| Kind | the screen label for `item.kind`, only for the six kinds in `exceptionKinds` | `exceptionKinds[kind]` | `Unknown` for any other kind; the raw kind text is never copied |
| State | `item.status` only when it is `open` (the one value the register produces today) | `items[].status` | `Unknown` for anything else; the raw text is never copied |
| Configured owner role | `item.owner_role` only when it is `data_steward` or `digital_operator` | `items[].owner_role` | `Unknown` for anything else; the raw text is never copied |

Every exported cell is therefore either an `EX-` reference, a fixed label from the screen's closed vocabulary, or the word `Unknown`; no free text from the response can reach the file. If a future producer adds a kind or status, it exports as `Unknown` until a new contract admits it.

Never exported: `summary`, `error`, `runbook`, `original_source` and any record, batch, case or query id, conflict `values`, `owner` (an email that can name a colleague), `eligibility`, `ref`, the banner, sources, unrouted text, access report, note, and any other field. A later change that adds a field needs a new contract and admission.

The header carries "in this view" because `EX-NNN` is assigned by insertion order per request and is not a durable identifier. The visible note (section 7) says so.

## 5. CSV format (formula-safe)

* UTF-8, comma separator, CRLF row terminator, one header row, no BOM, no blank trailing row beyond the final CRLF, no footer or caveat rows, no merged or metadata rows.
* Every cell, header included, is text. Same neutralisation as `list_export.safe_cell`: a value starting with `=`, `+`, `-`, `@`, TAB or CR is prefixed with an apostrophe before quoting. A cell containing a comma, double quote, CR or LF is double-quoted with internal quotes doubled. Because section 4 normalises every cell to a reference, a fixed label or `Unknown`, the CSV writer receives only strings. It must not reuse the `safe_cell` conversions for booleans, null or mappings (Yes/No, empty text, embedded JSON); a non-string reaching it is a defect, not an exported value.
* Row order is the order of the displayed table. One row per readable item, no de-duplication, no sorting, no truncation.
* File name `exception-register-visible-summary.csv`; MIME `text/csv;charset=utf-8`.

## 6. Bounded and all-records meaning

* The register response is not paginated. "All records" means every readable item the one authorised response contained for this signed-in user at render time, in that user's role scope only. A user holding only the steward role never receives operator items and the reverse; a person named with both roles receives both sets, because that is the server's scope. Scope is always the server's; the browser neither widens nor narrows it.
* It does not mean every exception in the system, any other user's scope, any unconnected source, any unrouted record, or a complete health picture. The page's Sources and Unrouted lists remain the statement of what is not connected, and the file says nothing about them.
* The file is a snapshot of the rendered response, not a fresh read. It can differ from the register after a reload.
* If any returned entry was unreadable (`unreadable > 0`), the list is not complete and no file is offered (fail closed), because a file cannot carry the "not complete" notice.

## 7. User-visible requirements

* The control is a native `button` with type `button` placed immediately after the "Exception items returned for you" table heading and before the table, with the visible name "Download visible summary (CSV)". It is reachable and operable by keyboard (Tab, Enter and Space), has a visible focus indicator, a target size meeting the existing control standard, and no colour-only meaning.
* A note programmatically associated (`aria-describedby`) with the button states, in plain language: this is a demonstrator feature and no operational or real-record use is approved; this copies only the four columns shown for the items listed here, for your role scope; it is a copy at the time this page loaded and does not change anything; it is not a complete exception list and an empty or short file would not mean all clear; the Reference is only valid in this view; the owner and free text are not included.
* After activation a `role="status"` message states that a download of N rows named exception-register-visible-summary.csv was started, for example "Download started: 3 rows, exception-register-visible-summary.csv". The browser cannot prove the file was saved, so the message never says it was saved. If the browser cannot build the file the message says no file was created and nothing was changed.
* The register screen text, columns, empty state and unavailable state are otherwise unchanged. Opening the entry link and registers' existing read-only wording are unchanged.

## 8. Case matrix

| Case | Server and screen outcome (existing, unchanged) | Export control | File |
| --- | --- | --- | --- |
| Authorised, one or more readable items, none unreadable | `state: ok`, table shown | Offered | Header plus one row per item |
| Authorised, filtered-empty or role-scope-empty (`state: ok`, `items: []`) | Existing "No exception items were returned. This is not an all clear" text | Not offered; the existing text stays the only statement | None. No header-only file, because it could be read as an all clear |
| Manager with no steward or operator named (`state: roles_not_named`, `items: []`) | Existing roles-not-named panel | Not offered | None |
| Permission denied by the register (403: not named, or non-manager with none named) | Existing "Access denied ... Your access has not changed" panel; audit `denied` persists as today | Not offered | None; nothing from the denied response is turned into data |
| Permission denied by the role projection gate before the register runs (403 "Your role does not include this.", `server.py:506-507`) | Same denied panel; no register audit line is written (existing behaviour, not changed or required) | Not offered | None |
| Unauthenticated (401) | Existing sign-in handling | Not offered | None |
| Unavailable, network or server failure, aborted load, superseded navigation | Existing "could not be shown ... Do not read this as all clear" panel, or no render for an abort | Not offered | None |
| Malformed response (`validExceptionRegister` fails) | Existing unavailable panel | Not offered | None |
| Some entries unreadable | Existing "list is not complete" notice | Not offered (fail closed) | None |
| Unknown kind, status or owner role on a readable item | Existing rendering | Offered | That cell is `Unknown`; raw text never copied |
| Readable item whose id does not match `EX-` and digits | Existing rendering | Not offered (fail closed) | None |
| Browser fails to build or start the download after activation | Not applicable to server | Offered, then status says no file was created or the download did not start | None; no retry request, no write |

Filtered-empty here means role-scope-empty: the register has no query filters, so the only "filter" is the server's role scope.

## 9. Observable requirements for any later slice

A later slice must show these with real evidence; this proposal does not claim them.

* O1. A real browser download event fires on keyboard activation (initiation, not proof of saving beyond the captured file) with suggested name `exception-register-visible-summary.csv`, and the saved bytes equal the four-column rendering of the returned items (compared with the JSON response, not the DOM).
* O2. Network log for the activation: zero requests. The full-view test still sees exactly one `/api/exceptions` call.
* O3. Ledger and data: the audit ledger line count after activation equals the count after load (existing view line only); the persisted data document and every controlled-domain record is byte-identical before and after the whole view-plus-download sequence (extends `test_reading_changes_nothing`).
* O4. Each row of the matrix in section 8 behaves as stated, with no button in the not-offered cases.
* O5. Formula-safety: the writer's escaping of already-normalised strings (leading `=`, `+`, `-`, `@`, TAB, CR, embedded quote, comma, newline) matches `list_export.safe_cell` plus `csv.writer` output for the same strings, checked in the test as a parity table. Separate expectations: odd kind, status, owner role and non-string inputs become `Unknown`; a non-matching id fails the list closed with no file.
* O6. Field exclusion: a fixture whose items carry marker strings in every excluded field proves none appears in the file; an single-role operator viewer never receives steward rows and the reverse, and a viewer holding both roles receives both sets.
* O7. Accessibility: native button semantics, keyboard, focus, note association, status announcement, with real automated and manual evidence claimed only if run; none is claimed here.

## 10. Unchanged source and history

Source, persisted history, the audit ledger format, the register's roles, projection and retention, and every existing export are unchanged by this task. The only changes are the dated tracking artifacts in this task's commit.

## 11. Next executable slice (not admitted)

Slice name: 80-exception-visible-summary-csv. Needs a fresh coordinator admission and a fresh RPI loop as a new #80 criterion-2 source slice, separate from any exhausted allowance.

* Files (expected): `src/api/src/zava_forward/api/web/role-screens.js` (button, builder, status), `src/api/tests/test_exception_register_screen.py` (replace the all-views no-control assertion with: no controls in entry, denied, empty and unavailable; exactly one button in the populated full view; add CSV, formula and exclusion cases), a real-browser check (extend the existing browser harness or add a focused check under `src/api/checks/`, chosen by that slice) that logs in against a real `Store` over HTTP with named staff and a clean populated fixture, for O1-O3 and O7, and the README note beside the register section. If a test-file or check-file list changes, that slice states it in its own plan. No server, store, list_export, importer, infra or workflow edits.
* Dependencies: #135 served register (on main) unchanged; no dependency on other #80 slices; no owner decision.
* Tests: node screen harness cases for O4-O6; the node screen harness needs a new clean populated fixture because its current "full" fixture includes an unreadable entry (`7`) and must keep offering no button; `test_exception_register.py` (HTTP/Store level) gets only the O3 data-unchanged and ledger-count assertions around two reads; the real-browser download, zero-request and keyboard evidence (O1, O2, O7) belongs in the browser check, not in that file.
* Validation tier: focused tier per the repository policy, classified by its actual impact (web-only, no permission, deployment or security-control change), to be recorded by that slice.

## 12. Remaining policy questions (not decided here)

* P1. Who is named data steward and digital operator (existing #135 open decision). The summary works with the configured placeholders and implies no appointment.
* P2. Operational handling and retention of a downloaded copy, and whether any real, non-synthetic use of this download is wanted. Not needed for a synthetic demonstration and must not be inferred from this document.
* P3. Whether the owner wants an operational "no exceptions" notice. The proposal chooses to offer none because an empty file could mislead; changing that needs an owner decision and its own contract.
* P4. Owner thresholds for the staged Excel transition (#80 criterion 4) remain unset and are unrelated to this contract.

No decision above is made, assumed or waived. Human approval, resident consent, legal and compliance gates and independent review are unchanged.
