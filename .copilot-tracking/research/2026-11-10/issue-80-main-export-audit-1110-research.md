<!-- markdownlint-disable-file -->
# Issue #80 current-main export acceptance and inventory audit: research

> Qualification 2026-11-10: partly superseded by the authoritative [supplement](../../audits/2026-11-10/issue-80-qualified-audit-1110-supplement.md). The claims below of 13 routes, 10 controls and grep-based absence of controls are superseded by eleven CSV paths plus the progress variant (twelve entries), nine controls located, three not located, with a static-search limit. The historical body is unchanged.

* Task: `issue-80-main-export-audit-1110`; parent task: none; parent issue #73 is hierarchy only.
* Date: 2026-11-10. Qualified agent: hve-core-all:rpi-agent, claude-sonnet-5.5.
* Mode: manual; phases advanced one by one only because the Root brief orders the full loop. Planning Readiness: Ready.
* Research disposition: executed (static read of current source; no tests run in this phase).
* Observed base: `c66370042eb08f07839d054433f4483078703cf2`, equal to freshly fetched `origin/main`; worktree clean at intake.

## Scope and boundaries

Audit only: classify what current main offers against the unmet criterion C2, "Every list offers an Excel or CSV export; Excel stays one-way read-only". No source, test, fixture or endpoint change; no freshfive grant; no whole-#80 closure. C4 (owner transition thresholds, ADR 0001 open item "Staged transition (proposed, thresholds to be set by owners)") stays HUMAN/OPEN and is not chosen here. C1 and C3 stay as recorded.

Source basis read in full for this task:

* Issue #80 body and all comments (read-only `gh issue view`), parent #73 body (no implementation dependency declared; "Dependencies: None").
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: FR-029 (line 1404), FR-030 (1405), SA-005 (553), SA-006 (554, "Every list offers an Excel or CSV export. Excel stays one-way read-only; no write back.", trace TR-001), TR-001 (453, "export their permitted cases to Excel or CSV ... with source, version and history"), AC-031/AC-032 (2127-2128, both "Not run").
* `docs/adrs/0001-azure-architecture.md` "Hybrid M365 and Excel transition" (line 197 onward): imports are one-way, Excel ends as a read-only report; thresholds "to be set by owners".
* BRD `docs/brds/agentic-retrofit-programme-brd.md` RULE-026 / AC-096 (1667): no management view, report or export exposes an individual's conversation or memory content.
* Existing export lineage in `git log` and `gh pr`: #303 importer export (merged), #906 closed, #1019 staff-list CSV (merged), #1176 finance/stock CSV (merged), #1241 checklist CSV (merged), #1369 held form draft JSON download (merged), #1371 Closed cases page CSV (merged `e951c523b`, ancestor of the audited base). Comment 2026-11-10T11:36Z on #80 records #1371 merged and the issue left open.
* Current-main source: `src/api/src/zava_forward/api/server.py`, `src/core/src/zava_forward/core/{list_export,projection,store,workflows,procurement,finance,exception_register,doc_controls,governance,continuity}.py`, `src/api/src/zava_forward/api/progress.py`, the web files under `src/api/src/zava_forward/api/web/`, and tests `test_list_export_api.py`, `test_role_endpoint_inventory.py`.

## Resolving the source/provenance gap

Ready-refinement 1903 relied on unpinned static reads of a primary checkout and could not prove "every list". This audit pins the base to `c66370042` and treats the source-bound enumeration in `test_role_endpoint_inventory.py` (`GET_ENDPOINTS`, with `test_inventory_covers_every_route_in_the_server`) as the route inventory, then classifies each route from its handler. Retained `d8ce761a` and composition `9b2572cf` are historical; neither is used as proof of delivery. `d8ce761a` is not an ancestor of the audited base (#1371 reached main as squash commit `e951c523b`, parent `d52f20a51`); the content relation is not asserted and nothing is republished.

## Finding 1: what exports exist on current main

`server.py` lines 165-190 define `LIST_EXPORTS` and `list_rows`; the shared handler (lines 479-485) applies `projection.allowed(u, get_kind(path))` first, calls the same store method as the JSON route, and serialises with `list_export.to_csv` (values only, `safe_cell` formula neutralisation, no read-back code). Additional CSV routes sit outside `LIST_EXPORTS`.

| Route | Rows from | Role gate (source) | UI control (source) |
| --- | --- | --- | --- |
| `/api/cases.csv` | `list_cases` + `Store.export_csv` (view/filter query) | STAFF_ROLES (`cases.csv` in `STAFF_GET`) | `app.js:805,843` "Download for Excel" |
| `/api/cases.csv?report=progress` | `core.progress.export_csv` | STAFF_ROLES | none found in `web/` |
| `/api/closed-cases.csv` | `progress.closed_csv` of the current filtered page | staff then `MANAGER_ROLES` (`progress.py:343-344`) | `progress.js:189` |
| `/api/packages.csv` | `list_packages` (unpaged) | STAFF_ROLES; store `_actor` | none found in `web/` |
| `/api/workorders.csv` | `list_work_orders` (optional `case`; unpaged) | STAFF_ROLES; contractors excluded by `projection.allowed` | none found in `web/` |
| `/api/handoffs.csv` | `pending_handoffs` | STAFF_ROLES; own or manager rows; notes held without reason-view | `app.js:758` |
| `/api/visits.csv` | `visits(view)` | STAFF_ROLES; `view=all` honoured for any staff role by the JSON contract | `app.js:2206` |
| `/api/funding.csv` | `funding_list` | STAFF_ROLES | `app.js:2216` |
| `/api/finance.csv` | `finance_queue` | `FINANCE_ROLES` | `panels.js:575` |
| `/api/asset/stock-queue.csv` | `stock_queue` | `MANAGER_ROLES` (Programme Manager, Programme Support Officer) | `role-screens.js:225` |
| `/api/checklists.csv` | `quality.checklist_rows()` constants, no case data | STAFF_ROLES | `ops.js:217` |
| `/api/form-schemas.csv` | `forms.list_schemas` projected to `SCHEMA_EXPORT_FIELDS` | forms read-rights intersection | `role-screens.js:1334` |

Related, not a list export: `/api/cases/<id>/form-review/<draft>/held-export` is a single-draft JSON (`role-screens.js:1297`), and `/api/continuity/export` is a manager-only JSON bundle (`continuity.py:608`), not Excel or CSV.

One-way boundary: `list_export.py` docstring and the UI sentence "The file is a read-only copy; changes in it are not imported back" appear on funding, checklists, finance, stock and form-schemas controls only. The Closed cases control carries its own read-only note (`progress.js:191-194`); the cases, handoffs and visits controls carry the label "Download for Excel" without a one-way sentence (source observation, not a defect finding). The only read path for spreadsheets is `/api/import-check`, which maps columns and changes nothing.

## Finding 2: source-supported lists/registers with no CSV or Excel export

Each has a handler in `server.py` or a store method and appears in the route inventory. Roles come from the handler or store gate; "unknown" means not read to the point of assurance.

| Route | Shape (source) | Role gate | Consumer in `web/` | Export on main |
| --- | --- | --- | --- | --- |
| `/api/handoffs/unaccepted` | rows sorted by age (`workflows.py:336`) | staff; own or manager | not found | none |
| `/api/resident/choice-queue` | paged items (limit 1-100, offset) of open homes, role-projected | RLO, Retrofit Coordinator, Programme Manager, Programme Support Officer | `role-screens.js:702` | none |
| `/api/exceptions` | register with items, sources, access report | named steward/operator, or manager when unnamed; viewing audited | `role-screens.js:931` | none |
| `/api/retention` | due-documents register | Programme Manager (`doc_controls._manager`) | not found | none |
| `/api/governance` | protocol, benefits, verdicts, releases, breaches registers | manager | not found | none |
| `/api/continuity` | continuity register (suspensions, changes) | manager, Quality Inspector, Building Safety Liaison | not found | JSON bundle only (`/api/continuity/export`) |
| `/api/data-protection` | register report from environment | `data_protection` kind, staff | not found | none |
| `/api/time/mine`, `/api/time/report` | time rows; report manager-only, with suppression | staff/manager | `timecapture.js:35,39` | none |
| `/api/finance/exposure` | single exposure signal | FINANCE_ROLES | `panels.js:571` | none (signal, not a list: unknown) |
| `/api/assistants/proposals`, `/api/assistants` | proposal queue, assistant registry | staff | `assistants.js:181,271` | none |
| `/api/law/alerts`, `/api/law/cards`, `/api/law/sources` | regulatory lists and cards | staff | `law.js`, `chat.js:292` | none |
| `/api/cases/<id>/form-candidates`, `/form-review` | form staging/review lists | forms rights | `role-screens.js` | none (held draft JSON only) |
| `/api/ranking/snapshot`, `/api/map`, `/api/facets`, `/api/briefing` | analytic views, filter options | staff | `app.js` | none (not business lists: facets are filter vocab; ranking/map/briefing unknown) |
| `/api/chat/threads`, `/api/chat/memory` | personal conversation and memory | owner only | `chat.js` | excluded by RULE-026 / AC-096 |

The 2026-11-05 comment on #80 names the same families (governance registers, projected resident queues/history, owner-only chat/memory rights delivery, form staging/review lists, unaccepted handoffs, role-filtered assistant lists, regulatory lists, time rows with suppression, restricted retention/exception queues) and says they are not an instruction to expose all stores.

## Finding 3: web lists and navigation

`web/*.js` builds 48 `h("ul"` nodes and 24 table nodes (counted by `grep -c`). Many are semantic bullet lists, navigation or help text; they are not business registers. Without an owner definition of "list" this audit does not count them, and it does not claim the count of business lists is complete. Per-case sublists (documents, contacts, hazards, appointments, history) are rendered inside the case detail projection; they are not top-level lists and their export status is unknown.

## Finding 4: proof granularity currently on main

* API: `test_list_export_api.py` (11 tests) binds `LIST_EXPORTS` to a literal expected set, compares CSV row counts to JSON rows for finance and stock queues, role limits, formula neutralisation, contractor/signed-out denial and read-only behaviour. It does not assert row content or order for packages, workorders, visits or funding beyond staff parity.
* Browser: UI export controls are exercised only for Closed cases (`progress_browser_check.py`, download and denied reader) and for form schemas (`schema_download_browser_check.py`: keyboard, saved file, denied roles, API). Cases, handoffs, visits, funding, finance, stock and checklists controls are evidenced by source and by static string tests only (for example `test_loading_feedback.py:217`). A button token alone does not establish rows, authorization, or source immutability.
* Blob proof: none of the CSV routes attaches or reads a blob; exports read the store only. No blob evidence is claimed.
* Version/source/approval/supersession history in a CSV is a property of the row contract per list, not of the shared serializer. `packages.csv` carries scope and capacity versions as nested JSON cells; other lists carry none. This is C3's domain (ticked) and is not re-judged here.

## Finding 5: the exact decision needed, and the distinct missing scope

The criterion text cannot be mechanically evaluated because "list" is undefined in SA-006, TR-001 names only "permitted cases", and RULE-026 forbids at least one family. Ambiguity stays unknown; no guess narrows "every". Two evidence-supported distinct gaps:

1. Missing UI entry points for existing API exports: `packages.csv`, `workorders.csv` and `cases.csv?report=progress` have no control in `web/` (source observation; Capacity screens in `ops.js` load only the paged JSON).
2. Source-supported registers/queues with no CSV route (table in Finding 2). Whether each is in the "every list" scope, and each one's row/field/suppression contract, is an owner decision.

Neither is implemented here. Remaining authority: the issue owner decides the in-scope list register and exclusions; each new export needs its own role, projection and retention contract, and its own RPI. No fresh correction allowance is claimed.

## Exclusions

* Unmerged #1395 (`feat/demo-sensor-drafts-111-1110`, base `feat/demo-sensor-review-109-1110`, open) and #1400 (`feat/demo-quality-workflows-89-1109`, base main, open): their UI is not current main and is not counted.
* Retained `d8ce761a` and `9b2572cf`: historical, not delivery proof.
* Importer-side Excel workbook export (#303, `src/importer`), covered by ticked C1/C3, is not re-audited.
* Private datasets, workbooks, SQL, cloud, provider and real accounts: not used.

## Checks planned for implementation

Targeted API: `test_list_export_api`, `test_role_endpoint_inventory`, `test_form_staging_api` (form-schemas CSV). Browser: `checks.schema_download_browser_check` and `checks.progress_browser_check`, one heavy non-queued flock each. Not planned: full suites, SQL, images, full gate, new tests.

## Planning Readiness

Ready. Open owner inputs (not engineering blockers): definition of "list", in-scope register, C4 thresholds.
