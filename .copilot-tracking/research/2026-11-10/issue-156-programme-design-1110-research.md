# Research: #156 Programme case queue/paging proposed v1 state design (2026-11-10)

Status: stub written before research-open; findings below added after the boundary.

* Task: issue-156-programme-design-1110; branch docs/demo-programme-design-156-1110
* Pin: b471c56a066d678b50106d9051cfb788e2c9e573 (target feat/demo-ux-coverage-parent-149-1110; parent #149 is an integration topic, not MAIN acceptance)
* Selected surface (coordinator): Programme case queue/paging, supporting #230
* Research disposition: executed (witness research-open seq 2 preceded these findings)
* Planning Readiness: Ready

## Delivered-check (stop rule)

No equivalent current versioned programme queue state design exists. A search of `docs/` for page-local/paging/offset finds only engineering notes and PRD text (`customer-journeys/residents.md`, PRDs, `src/api/README.md` context, ADR 0002, cut-over pack). Register rows C01, C02, T02 and the #230 row in `zava-forward-prototype-profile-review.md` (lines 88, 103-104, 340) state "Current design: Not supplied". The #231 section in `programme.md` is delivery status, not a state design. Disposition: proceed.

## Admission input (source-qualified)

`ROOT/admission-156-fresh-1110.json` (issue body and comments: C1 unticked, designs not supplied, balance UNKNOWN) and `ROOT/demo-source-admissions-156-154-233-1110.md` (#156: gate exists, missing design deliverables remain; a selected screen's proposed versioned state/recovery design is legitimate work). `ROOT/handoff-230-paging-completion-1110.md` is a frozen LOCAL candidate (head 3b54035d6, not in the pin, not accepted MAIN or AT proof). Only its handoff text and checker docstring were read.

## Current behaviour at the pin (source reading only, nothing executed)

Files: `src/api/src/zava_forward/api/web/role-screens.js` (RS), `app.js`, `style.css`.

| Id | Observation | Source |
| --- | --- | --- |
| F1 | Screen `programme-queue` is installed for Retrofit Programme Manager, Programme Support Officer and Retrofit Coordinator. | RS 4-5, 498-504 |
| F2 | Two lists on one screen. Side list "Choose a home": `/api/cases?view=all&limit=20&offset=page*20`, paged by links with URL `page=`, selected case in URL `case=`. Main "Shared queue": `limit=50`, paged by in-memory buttons, offset not in the URL. | RS 78-100; 309-345, 504 |
| F3 | Selecting a home is a route change and `overview` reloads shared-queue offset 0, so the shared queue appears to return to its first page on home selection (inference from code, not executed). | RS 504-505 |
| F4 | Shared-queue rows have plain text in the Home cell; no link opens the case. Opening a case is via the side list. | RS 288-298 |
| F5 | Filter: select "Scope", Apply filter, Reset to default view. Scope kept in URL `scope=` by `history.replaceState`; filters the loaded page only. Status "N of M records on this page shown ... no record is changed". Page text "The scope filter applies to this page only ... Not a portfolio total." Scope persists across paging. | RS 262-282, 309-346 |
| F6 | Pager shown only when total exceeds the first page length. Previous/Next are buttons, not disabled at the ends; presses at an end are no-ops. | RS 340-345 |
| F7 | Paging loading text "Loading page. The current rows stay until it arrives." Failure text "That page could not be loaded. The rows shown are unchanged. Try again, or open a case from the case list." No dedicated retry control and no focus move; failure and page status share one `role=status` paragraph. | RS 326-336 |
| F8 | Filtered-to-zero rows render the table message "No records supplied. This does not establish readiness." beside "0 of N records on this page shown"; the two can be read as the page having no data. | RS 33-35 vs 316-318 |
| F9 | Initial load failure goes to the router catch: "Workspace unavailable" `role=alert` with Try again. 401 returns to sign-in; other API denials show the server message or the generic read error. | app.js 448-456, 77-81, 55 |
| F10 | Screen not installed for role: "Screen unavailable ... Your access has not changed." Invalid `page`: "Invalid screen page" with Reset. | RS 56-66 |
| F11 | Initial load text "Loading recorded evidence." with `aria-busy`. | RS 77 |
| F12 | DOM order is side list, then main (evidence boundary, shared queue with pager, filter form, status, table). At 900 px and below one column, so the 20-row side list precedes the shared queue. Wide tables sit in a named focusable `table-scroll` region. | RS 120-125, style.css 218, 257-264 |
| F13 | `show()` focuses the app region on route change unless focus is already in the same context; in-place paging does not move focus. | app.js 99-108 |

## Existing decisions and evidence this design honours

* D01 Fluent 2 selected (owner, #150); D02 context visible and case return recoverable; D04 honest partial recovery, permissions separate from navigation (`zava-forward-prototype-profile-review.md` 114-118).
* UX-02/03/07 candidate checks (same file 958-984): visible effect of context, honest loading/no-match/failure, return restores filter, selection, queue position and focus. Full UX-07 restoration is recorded as unmet.
* Programme journey 1 (`customer-journeys/programme.md` 55-65): sender keeps chase until accepted; blocked cases chased.
* Design system (`design-system.md` 36-46, 101-126): native semantics, distinct loading/empty/failed/unknown/denied states, no colour-only status, empty distinguished from failed.
* WCAG baseline (`wcag-conformance-baseline.md` 34-50, 205): 320/390/1280 and 200% text; no screen-reader, zoom, reflow or target-size test completed (G-1).
* Supported devices proposal: proposed, not decided; no device commitment is made here.
* Content standard: blocked/error pattern of reason, owner, next action.

## Missing evidence and owner decisions (not invented)

1. Named design/Programme review: none.
2. Whether shared-queue offset belongs in the URL and whether the two lists merge: owner/design decision (options in the design).
3. Role/field contracts for Programme Support Officer and Retrofit Coordinator beyond the installed role list: not supplied, not specified.
4. Help contact for persistent failure: none supplied; the design reuses only the existing generic "application support" owner wording.
5. Assistive-technology, usability and device evidence: none.
6. Trace parser: `tools/check-design-trace.py` treats a row as supplied only with a versioned link and no NOT SUPPLIED text. Partial proposed availability cannot be represented, so the register stays Blocked (expected).

## Selected approach

Hold the design in `docs/reference/research/ux/customer-journeys/programme.md` as a new dated section (that journey page already carries dated continuation sections), version `programme-queue-paging-v1` (proposed). Add one additive dated note near the register's #230 context, an index entry and an append-only log entry. No new page, no checker change.
