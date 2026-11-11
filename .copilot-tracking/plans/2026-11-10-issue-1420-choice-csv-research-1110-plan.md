<!-- markdownlint-disable-file -->
# Implementation Plan: Resident-choice portfolio page CSV summary (issue 1420)

* Task slug: `issue-1420-choice-csv-research-1110`; research: [research](../research/2026-11-10-issue-1420-choice-csv-research-1110-research.md); details: [details](../details/2026-11-10-issue-1420-choice-csv-research-1110-details.md); critique: [critique](critiques/2026-11-10-issue-1420-choice-csv-research-1110-plan-critique.md)
* Pin: parent `12d3ac842c0474b424ed15498d6716d9c93099cf` (tree `7d3d053ce5e9a961b25e97dda4d08d3a3475dce4`), containing main `6d4cd62475ba89a214055f761b8e3276ef063d44`. The parent has advanced since (C3 `1dfcb0ee` checker-only, C4 diagnosis); that movement is not used.
* Status: PLAN ONLY. Product proposal, not source approval, not real-data, privacy, retention or operational-export authority. Implementation, tests and Review are not admitted here and none ran.

## Objective

A truthful CURRENT PORTFOLIO PAGE SUMMARY CSV of the resident-choice queue: the same page the overview shows, as a read-only download. It is not all pages, not sidebar row parity and not a consent, readiness or approval report.

## Contract (proposal)

### Route and query

* `GET /api/resident/choice-queue.csv`, dedicated branch in `server.py` next to the JSON route, not in `LIST_EXPORTS`, not via `list_export.to_csv`.
* Same `q`, `num()` and store call as JSON: `limit` default 50 clamp 1..100; `offset` default 0 clamp 0..10^9; blank values dropped (`limit=&limit=7` is 7); repeated uses first; unknown parameters ignored; non-integer is 400 JSON. No new filter, cohort, role or owner scope.
* Roles: exactly Resident Liaison Officer, Retrofit Coordinator, Retrofit Programme Manager, Programme Support Officer succeed. Quality Inspector, Building Safety Liaison, Grants and Evidence Officer: 403 JSON from the store `PermissionError`. Contractor, Application Administrator and unknown roles: 403 or 404 JSON from the generic gate. Signed out: 401 JSON. Any error has JSON content type, no `Content-Disposition` and no CSV body; a loader exception must be 5xx JSON, never a header-only 200.
* Success: `200 text/csv; charset=utf-8`, `Content-Disposition: attachment; filename="resident-choice-queue-page.csv"`.

### Header (fixed, always written, header-only when zero rows)

`Home reference,Measure choices (latest recorded version),Paused or withdrawn (needs human review),Update commitment status,Homes skipped before this page,Page size limit,Homes in this file,Open homes in total`

* One row per home on the page, in store order (case id string sort).
* Home reference: case id only. Address and town excluded.
* Measure choices: per measure `<measure>: current <status>; latest recorded v<n> <status> (revision <r>, design <d>)`, joined by `; `; `No measure choices recorded` when none. Status missing is `Not recorded`; any other missing is `Unknown`. Scope free text is excluded by default (Q1).
* Paused or withdrawn: exact port of the UI rules (`choiceStopped`, `choiceStopVersion`, `choiceStoppedSummary`, `role-screens.js:665-687`), including the stale-stop and `, needs human review before any restart` text; `None recorded` otherwise. Declined appears only in the measure column; that is a stated limitation, same as the UI.
* Update commitment status: `Outstanding` or `Proposed` as stored, `Unknown` if blank, `No commitment recorded` if none. Purpose, owner, due date (Q2), safe route excluded.
* Homes skipped before this page = effective offset; Page size limit = effective limit; Homes in this file = `len(items)`; Open homes in total = store `total`. Repeated on each row so any single row labels the page. Values are integers.
* Excluded entirely: raw nested records, notes, answered_by, recorder and representative identities, contact and address details, adjustment text, purpose, owner, safe-contact route, household history, evidence bytes, retention metadata.
* Measure names are staff-entered text (`resident_decisions.py:869`). The serializer must fail closed: a measure name not in the repository's controlled measure vocabulary (Root to confirm the source list, Q5) renders as `Measure name withheld` instead of free text. Same fail-closed stance for any other string not drawn from a closed set (statuses must be one of the five decision statuses or `Not recorded`, update status one of `Outstanding`, `Proposed`; otherwise `Unknown`).
* Unknown is not absence: when `versions`, `status` or `review` is missing or malformed for a measure, the stopped column shows `Unknown (evidence unavailable)` for that measure, never `None recorded`. `None recorded` is used only when every measure has complete evidence and none is stopped.
* Retained review: a measure whose `review.status` is `Needs human review` for a Declined version (including after a later Waiting, `resident_decisions.py:1425`) is listed in the stopped column as `<measure>: Declined, needs human review` so the review is not lost; the column title stays "Paused or withdrawn (needs human review)" and the UI note states it also lists retained review flags. This extends, and so deliberately differs from, the UI predicate; Root to confirm (Q6).
* Absence labels never mean consent, readiness or approval. Version numbers and revision and design binding are kept so a choice is not read without its binding; Paused, Withdrawn and human-review meaning is carried verbatim.

### Empty, error and safety cells

* Zero items: header row only (stable, local to the new serializer; shared serializer unchanged). Because the header carries no counts, header-only means "no rows on this page", not "no open homes" (offset past the end, or all page items omitted). Stated in the UI note.
* All cells are strings or ints composed by the new module, then passed through shared `safe_cell`: formula-prefix apostrophe for `=,+,-,@,tab,CR`, `csv.writer` quoting of commas, quotes, newlines. No `None`, no Mapping or list reaches `safe_cell`; unexpected nested values raise rather than being dumped as JSON.
* `Homes in this file` below `min(limit, total - offset)` signals items omitted because their detail was unavailable; the UI note says so.

### UI

* In `role-screens.js` portfolio `summary(queue)` only, in the loaded-items branch: a plain `<a href="/api/resident/choice-queue.csv?limit=<queue.limit>&offset=<queue.offset>">Download this page for Excel</a>`, outside the table region, no `<button>`, no `download` attribute (so a JSON error is shown, not saved as a fake `.csv`), with an adjacent note (`aria-describedby`): only the homes shown on this page, not every page; read-only copy re-read at download and may differ; choices, pauses and commitment status summarised without answer notes, names, contact or address details; "Not recorded", "None recorded" and "No commitment recorded" mean nothing recorded, not consent or readiness; an empty file does not show that nothing needs attention. Load failure keeps the blocked panel and no link. Constructed demonstration data note only if environment labelling requires (not assumed).
* Per-home selected view and sidebar unchanged.

## Future ownership (after explicit Root admission only)

| File | Change | Class |
| --- | --- | --- |
| `src/api/src/zava_forward/api/server.py` | one `get_kind` line and one dispatch branch near the JSON route (~790) | shared file, narrow hunks |
| `src/api/src/zava_forward/api/resident_choice_export.py` | new serializer | new owned file (admission needed) |
| `src/api/tests/test_resident_choice_export.py` | new dedicated tests | new owned file |
| `src/api/src/zava_forward/api/web/role-screens.js` | link and note in `summary(queue)` | owned hunk |
| `src/api/tests/test_resident_choice_screen.py` | replace the "no `a`" assertion by "exactly one CSV link, no button and form" plus link tests | existing file, admission needed |
| `src/api/tests/test_role_endpoint_inventory.py` | add the new path as its own new line of `GET_ENDPOINTS` | shared hotspot |
| `src/api/checks/role_screens_browser_check.py` | optional story 232 extension | existing, not run until a browser is admitted |
| `src/api/README.md` | optional paragraph near line 661 | shared hotspot |

Read-only: core `store.py`, `projection.py`, `controls.py`, `resident_decisions.py`, `list_export.py`. No role, core or schema change. Not touched: `ops.js`, `capacity_browser_check` (owned by active #80), `LIST_EXPORTS`, `test_list_export_api.py`.

## Integration ordering

* Sibling 1419 may own `server.py` CSV registry and parser, `app.js` handoff panel and list-export tests. Shared files (`server.py`, `test_role_endpoint_inventory.py`, README) need an explicit ordered integration decision by Root before any source work; no blind parallel implementation. 1419 UI source is distinct from this UI source.
* Eventual child target is the declared #80 parent while unmerged; Root re-evaluates after parent merge and must re-pin because the parent has advanced.
* No source authority from spent 132/135 or held 131/144/1360/1362/1401/2.

## Synthetic check plan (not run now)

All with constructed data only, no private or default dataset, credentials, provider, SQL, Docker, cloud, browser or deploy.

1. Roles: four allowed roles succeed with identical bodies for identical store state (hypothesis to verify); Quality Inspector, Building Safety Liaison, Grants and Evidence Officer, Contractor, Application Administrator and an unknown role denied without Content-Disposition or CSV; signed out 401.
2. Closed exclusion; id order; offsets; default 50/0; clamps (`limit=0`, `1000`, `offset=-5`); blank, repeated and unknown params; non-integer 400.
3. Omitted-detail qualification: patch `detail` to return `None` for one id; `Homes in this file` less than expected while total counts all.
4. Empty: header-only, exact bytes; offset past end header-only.
5. Cells: formula prefixes, quotes, commas, newlines in a measure name or status; absence labels never blank.
6. Strict fields: canary strings in notes, answered_by, recorder, representative, address, adjustment, purpose, owner, safe route, household history, retention fields, scope must be absent; header equals the fixed tuple; no JSON braces.
7. State unchanged: case, choice, update and audit state identical before and after a download.
8. Fail-closed and unknown cases: unrecognised measure name withheld; missing status, versions or review gives `Unknown (evidence unavailable)`, not `None recorded`; Declined then Waiting keeps the review entry; HTTP-injected loader failure (patched store method raising) returns 5xx JSON with no `Content-Disposition` and no CSV.
9. UI static test (node vm): link present only with items, href uses `queue.limit` and `queue.offset`, no button or `download` attribute, note text present, none on load failure; browser story 232 extension later.

## Validation tier and gates

Focused tier (non-gate, no workflow, dependency, permission, deployment or security-control change): targeted `src/api` unit tests plus the existing inventory and resident-choice tests; record classification; independent exact-head review, human approvals and hosted CI still required; an unobserved hosted workflow is not a pass. Doubt takes the full tier. Before any web edit: load `web-design-guidelines` and fetch its source, read relevant design skills, preserve Fluent 2, WCAG and plain-language content standard.

## Stop conditions

Stop and ask Root if: a faithful summary needs fields on the exclusion list; shared hunks cannot be ordered against 1419; the advanced parent changes any of the nine source files; the scope column or due date is demanded without a privacy decision.

## Open questions for Root

* Q1 include scope free text (default no). Q2 add due date (default no). Q3 grain: home row (default) versus home x measure; repeated page columns versus filename-only labels. Q4 admit new module and the `test_resident_choice_screen.py` change, and order the shared edits with 1419. Q5 controlled measure vocabulary source and withheld label. Q6 retained Declined review in the stopped column.

## Phase status

* Research executed, Plan done; the single critique (Approve with changes) findings are applied (see critique). Implementation, tests and Review not started and not claimed. Whole #80 and #73 stay open; no criterion ticked.
