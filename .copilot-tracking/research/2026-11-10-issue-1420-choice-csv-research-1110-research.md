<!-- markdownlint-disable-file -->
# Task Research: Issue 1420 resident-choice portfolio page CSV summary (2026-11-10)

* Task: `issue-1420-choice-csv-research-1110`, slug `issue-1420-choice-csv-research-1110`
* Worktree `issue-1420-choice-csv-research-1110`, branch `docs/resident-choice-csv-1420`
* Frozen parent `12d3ac842c0474b424ed15498d6716d9c93099cf`, tree `7d3d053ce5e9a961b25e97dda4d08d3a3475dce4`, on local `test/demo-export-entrypoints-80-1110`; it contains fetched main `6d4cd62475ba89a214055f761b8e3276ef063d44` (confirmed ancestor by `git merge-base --is-ancestor`)
* Research disposition: executed (static source inspection only; no runtime, no test run, no dataset)
* Planning Readiness: Ready for planning. A faithful summary is possible within the boundary, with three product questions for Root (see Open questions); none blocks planning.
* Issue: [issue record](../github-issues/issue-1420.md), https://github.com/jmservera/ama/issues/1420

## Pin and ancestry disclosure

* The parent has since advanced (adverse C3 to `1dfcb0ee`, checker-only, and a C4 diagnosis). This research deliberately pins the known ancestor `12d3ac842`, not the moving parent.
* `git diff 6d4cd62...HEAD` over the nine relevant files (`store.py`, `projection.py`, `controls.py`, `resident_decisions.py`, `list_export.py`, `export_fields.py`, `server.py`, `role-screens.js`, `test_resident_choice_queue.py`) is empty, so the resident-choice source equals fetched main. Parent movement after `12d3ac842` was not inspected and is not used.
* No fetch, merge, rebase or adoption happened. The eventual child target is the parent while unmerged; Root re-evaluates after the parent merges.
* Paths: C = `src/core/src/zava_forward/core/`, A = `src/api/src/zava_forward/api/`. Line numbers are in the frozen tree.

## Required reading and boundaries

Read: [original case study](../../docs/case_study_48_original.md), [addendum](../../docs/case_study_48_addendum.md) (consent rule CON-006 at line 1244 and NFR-005 constructed-data rule), [reference index](../../docs/reference/README.md), [memory](../../docs/reference/memory.md) (context only, not evidence), the [content standard](../../docs/reference/research/ux/content-standard.md) and the existing CSV paragraph in [api README](../../src/api/README.md) (lines 661 to 668). Coordinator scope file `scope-resident-choice-export-2230.md` was read as a lead only; every claim below was re-validated in this worktree.

Not performed: the web-design-guidelines fetch and design-skill reads that the repository requires before web edits (no web edit is made now); they are a precondition of the later implementation phase. No SQL, Docker, cloud, provider, browser or credential was used.

## Verified existing contract

### Route, roles and gates

* `GET /api/resident/choice-queue`, `A/server.py:790-796`. Returns `{items, total, limit, offset}`.
* Kind mapping `A/server.py:244`: `/api/resident/choice-queue` -> `resident_choice_queue`; the kind is already in `STAFF_GET` (`C/projection.py:37-38`); generic gate `A/server.py:492-493` (`projection.allowed`): contractor and Application Administrator are denied, unknown roles denied (`C/projection.py:65-72`), seven staff roles pass the generic gate.
* Store gate `C/store.py:541-546`: exactly Resident Liaison Officer, Retrofit Coordinator, Retrofit Programme Manager, Programme Support Officer (equal to `RESIDENT_VIEW_ROLES`, `C/controls.py:12-13`). Building Safety Liaison, Grants and Evidence Officer and Quality Inspector pass the generic gate but are refused by the store with `PermissionError` -> 403 JSON. UI mirror `A/web/role-screens.js:665,698-702`.
* Unauthenticated: 401 JSON before any route logic (`A/server.py:470-471`).

### Rows and paging

* Open (nonclosed) homes only, `sorted(cid ...)` (string sort of case ids), sliced `ids[offset:offset+limit]` before `detail()` projection (`C/store.py:548-556`).
* `detail()` returning `None` skips an item silently; `total` is `len(ids)` of all nonclosed ids, taken before any skip. So `len(items)` can be less than `min(limit, total - offset)`; the UI wording "Shows N of total" is therefore the truthful label and an export must report `len(items)` as rows, not infer it.
* Query (`A/server.py:276-283`, `472`): `parse_qs(url.query)` without `keep_blank_values`. Only `limit` (default 50, clamp 1..100) and `offset` (default 0, clamp 0..10^9) are read. Consequences, all of which apply unchanged to the CSV route if it reuses the same `q` and `num()`:
  * blank value is dropped, so `limit=&limit=7` yields 7 (not the first value, not a rejection);
  * repeated nonblank values use the first;
  * non-integer (`limit=abc`, `limit=%20`) -> `ValueError` -> 400 JSON;
  * out-of-range clamps silently (`limit=0` -> 1, `limit=1000` -> 100, `offset=-5` -> 0);
  * unknown parameters are ignored, no filter, search, status, owner or case view exists.

### Projection shape

* Items are exactly `id, address, town, measure_decisions, resident_update` (`C/store.py:550-555`), built from `detail(cid, user)`, i.e. role-redacted (`C/projection.py:148-201`). The four allowed roles are all in `RESIDENT_VIEW_ROLES`, so the nested choice and update structures are present for each; redaction differences among them concern reason and note text (`can_see_reason`, `DEFAULT_REASON_ROLES`, `C/projection.py:28,148-201`), which this proposal does not export.
* Per measure (`C/resident_decisions.py:875-890`): `measure`, `status` (latest answer if it matches the current scope revision, else `Not recorded`), `context` (scope, revision, design_version), `versions` (full history with `note`, `answered_by`, `source`, `representative_ref`, `recorder_identity`, `review_ref`, scope, design_version, context_revision, status, at, ...), `readiness` (`Needs human review` or `Resident decision current`) and `review`.
* Decision statuses `Waiting, Accepted, Declined, Paused, Withdrawn` (`C/resident_decisions.py:24`). Paused, Withdrawn and Declined each open a `Needs human review` record naming the `decision_version` (`:1404-1430`). Accepted after a stop clears it only with supplied review evidence.
* `scope` is a staff-entered reference of up to 100 characters (`k.text(..., 100)`, `:1355`), not an enumeration. `context_revision` and `design_version` are integers. This matters for the export (see Open questions).
* `resident_update` carries purpose, owner, owner_identity, due_at, basis, safe_contact_ref, status (`Outstanding` or `Proposed`), version, history (`:1668-1700`).

### The real UI

* Screen `resident-choice`, route `#/screens?screen=resident-choice`, `A/web/role-screens.js:698-721`. `overview` fetches `/api/resident/choice-queue?limit=100&offset=0` fixed (`:702`); the sidebar "Choose a home" is a separate `/api/cases?view=all&limit=20&offset=page*20` list (`:78`, `:83-99`) and the selected-home `render` is separate per-case history. Three scopes, not to be conflated.
* Overview table: Home; Measure choices (latest version); Paused or withdrawn; Update commitment (`:710-717`), built by `choiceQueueRow` (`:688-696`). The Home cell is `id, address, town`. Measure cell per measure: `<measure>: current <status>` plus, if versions exist, `; latest recorded v<n> <status> (scope <s>, revision <r>, design <d>)`, joined by `; `, or `No measure choices recorded`. The stopped cell lists measures where `choiceStopped` holds, as `<measure>: <state>[ (current answer <status>)] (v<n>, scope, revision, design)[, needs human review before any restart]`, or `None recorded`. `choiceStopped` is true when the current status is Paused or Withdrawn, or when `review.status` is `Needs human review` and `review.decision_version` points at a Paused or Withdrawn version (`:667-674`), so a stale or superseded stop stays visible. Declined is not listed there. The commitment cell shows `status: purpose. Owner, due, safe route` or `No commitment recorded`.
* Statement text: "Read-only. Shows N of total open homes, in home ID order, as your role may see them" (`:713`). Failure shows a blocked panel "The cross-home queue could not be loaded." (`:718`), not an empty table. Empty rows give "No records supplied. This does not establish readiness." (`:33`).
* Existing UI tests pin this: `src/api/tests/test_resident_choice_screen.py` (`test_queue_summary_is_read_only_and_names_scope`, asserts no `a`, `button`, `form`, `input`, `select`, `textarea` anywhere in the overview tree; and that the exact `scope S-9` text appears) and `src/api/checks/role_screens_browser_check.py:719-726` (no `tel:`, `mailto:` or `button` in the summary region). A new download link is an `<a>`: it breaks the first, not the second if placed outside the table region.

### Existing CSV surfaces do not equal this queue

* `LIST_EXPORTS` (`A/server.py:172-173`) plus `list_rows` (`:181-199`) and the generic dispatch (`:494-500`) cover packages, workorders, handoffs (pending), visits, funding, finance, stock-queue, checklists and form-schemas. `test_list_export_api.py::test_registry_matches_lists` asserts the exact set, so adding the route there would break it and would reuse a serializer that derives headers from rows.
* `list_export.to_csv` (`C/list_export.py:31-41`) takes headers from the first-seen row keys, renders Mapping/list cells with `json.dumps` (so nested `measure_decisions` would be dumped whole) and writes no header for zero rows. Feeding it the queue items is the blind nested dump the issue forbids.
* `cases.csv` (`A/server.py:648-655`, `C/store.py:1256` `export_csv`) is the case list: Reference, Resident, Address, Town, Postcode, Phone, Stage, Status, Owner, days, last contact, next visit. `progress.csv` (`A/server.py:~527-552`) and `closed-cases.csv` (`A/progress.py:418-430`, `A/server.py:501-511`) are different cohorts and reports. None serialize choices or commitments.
* The nearest precedent is `closed_csv` in `A/progress.py:39,418-430`: fixed column tuple, header always written, primitive cells only (`TypeError` otherwise), shared `safe_cell`, `Content-Disposition` attachment `closed-cases-page.csv`, UI link "Download this page for Excel" with a page-only note (`A/web/progress.js:176-196`).

### Shared serializer behavior that applies

`safe_cell` (`C/list_export.py:18-28`): `None` -> empty string; bool -> `Yes`/`No`; mapping/list/tuple -> compact sorted JSON; everything else `str()`; text starting with `=`, `+`, `-`, `@`, tab or CR gets a leading apostrophe. `csv.writer` quotes commas, quotes and newlines, but `safe_cell` does not check embedded newlines or Unicode. The export must therefore pass only strings and integers it composed itself; a `None` would render as an empty cell, which for a choice status could be misread as "nothing" rather than "Unknown" - so every missing value is mapped to an explicit label before `safe_cell`.

### Tests and registry hotspots that a new route touches

* `test_role_endpoint_inventory.py:69-74` regex-scans `server.py` for every quoted `/api/...` route and requires an entry (or prefix) in `GET_ENDPOINTS` (`:17-24`), a single very long shared line also holding the handoffs, packages and other csv paths. A new `/api/resident/choice-queue.csv` string in `server.py` makes this test fail until that list gains the path. `test_every_role_against_every_endpoint` then runs the route as every role and asserts no 500 and denies for Contractor/unknown roles.
* `get_kind` (`A/server.py:202-244`) has a final dict return on one long line shared with 1419's likely edits; a separate `if` before it avoids that hunk.
* `test_resident_choice_queue.py:33-65` covers the store method only (shape, refusal, closed exclusion with paging total, no mutation). It is not export proof.

## Evidence that does not exist (stated, not guessed)

* No decision on whether `scope`, update due date or town may appear in an export; no privacy, retention or consent approval; no real record used; no runtime, browser, hosted CI or accessibility result observed. Constructed (synthetic) fixtures only in any future check. The coordinator's duplicate and ownership position is a supplied premise.

## Selected approach

Add a read-only, page-only CSV beside the existing overview that serializes a closed set of text and integer summary columns derived from the same `resident_choice_queue(u, limit, offset)` call, with its own serializer and stable header, never via `list_export.to_csv` or `LIST_EXPORTS`. See the [plan](../plans/2026-11-10-issue-1420-choice-csv-research-1110-plan.md) and [details](../details/2026-11-10-issue-1420-choice-csv-research-1110-details.md).

Rejected alternatives:

* Register in `LIST_EXPORTS`: breaks the registry test, shares 1419's hunks, header-less empty, nested JSON cells, wrong filename.
* Dump nested JSON per home: exposes notes, identities, source and review refs, owner, purpose and safe route; blind widening.
* One row per home and measure: friendlier to filter but then row count no longer equals "homes on this page", home-without-measures needs a special row, and "N of total" meaning splits. Kept as option B for Root.
* Export all pages or add filters: contradicts the issue boundary and the fixed page contract.
* Fetch-and-blob download or the `download` attribute: with `download`, a JSON error body could be saved as a ".csv" and look like success; a plain attachment link navigates to the visible JSON error instead.

## Open questions for Root (planning does not block)

* Q1 scope reference. The UI shows `scope <free text up to 100 chars>` to the same roles. Default proposed: not exported (free text, no redaction exists by design, see `C/projection.py` header comment); binding is carried by the integer revision and design columns. Alternative: include it verbatim as the UI does. Root decides.
* Q2 update commitment detail. Default: status only (`Outstanding`, `Proposed` or `No commitment recorded`). Due date is not on the exclusion list but is not in the minimal summary; alternative: add an ISO UTC `due_at` column.
* Q3 grain and page labels. Default: one row per home, four repeated page-context columns so that every row is labelled as a page; header-only on empty carries no counts (stated limitation). Alternative: long format (home x measure) or filename-only labelling.
* Also needs admission: a new in-package module and the changed assertion in `test_resident_choice_screen.py` (details section 4).

## Limitations that stay stated

* The file is one page of at most 100 homes (UI) or 50 (no parameters), read again at download time; it is not all open homes and not a readiness, consent or approval report.
* `Not recorded`, `None recorded`, `No commitment recorded`, `No measure choices recorded` and `Unknown` are absence labels, never consent or readiness.
* Home reference is a pseudonymous case id; with a lookup it remains linkable to an address. Even exported values are not authorized for real records; demonstration data only.
* Excel opens UTF-8 without a byte-order mark as the local code page; the shared serializers have the same property and this plan does not change it.
