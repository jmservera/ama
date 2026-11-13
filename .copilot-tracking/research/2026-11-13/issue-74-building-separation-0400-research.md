<!-- markdownlint-disable-file -->
# Research: #74 criterion 2 building versus home separation (issue-74-building-separation-0400)

Date 2026-11-13. Base and HEAD at start: 6f2918011d55d63ffc52865073ef45bd7ea9197c (origin/main, freshly fetched). Branch research/demo-building-separation-74-0400. Mode: prospective Research and Plan with one independent critique; planning-only. Disposition: executed (source read only). No product, test or config edit, no test, browser, SQL, Docker, model or app run, no GitHub write.

Read limits: #74 body and all comments (comment text truncated to 900 characters each in the read, so later comment tails were not read), the committed 1406 matrix and changes record, the 2300 regression state, diffs of the home-case files since 47e43ec7, `home_case.py` view, `app.js` `homeCaseView` and `buildingView`, `home_case_browser_check.py` and `test_home_case_api.py` diffs, PR #1500 body excerpts, #1409. Not read in full: PRD FR-001/FR-002 and BRD FR-001/FR-002/NFR-002 (relied on the #74 body and the committed matrices that cite them), the role-agent contracts, `docs/reference/README.md` and `memory.md` (context only, not approval). No raw logs, `.env`, SQL or private dataset read. A search for the `rpi-74-refill-2250-result.json` file timed out and was stopped; it was not read, so its content is cited only as quoted in the 2300 state.

## Criterion

Building-level dependencies, holds, works and costs are shown apart from each home's evidence, decision, cost allocation and outcome (criterion 2; criteria 1, 3, 4 ticked).

## History recovered

* 2026-11-03/04: #907 core slice only, then criteria 1, 3, 4 ticked at core level; 2026-11-05 audit found the no-API/UI gap obsolete.
* 2026-11-09: two session-local synthetic replays on b46a9ad9 (separate regions, populated two-home split). Not maintained evidence.
* 2026-11-10: qualified audit #1406 merged at 47e43ec7: runtime 16 PASS plus COMPLETE at historical c6637004; criterion 2 UNPROVEN; phase-order and validator qualifications remain; #1409 (Low, documentary) is CLOSED and was not a source authorization.
* 2026-11-12: owner admitted an exact test-only G1/G2/G3 slice in two owned files (2300 state, evidence "owner task brief 2026-11-12"); explicitly excluded product source, the funding_confirmed assertion, criterion 2 closure, the outcome tuple, G5 and any new pool. That slice's own state records Review Conformant with limits and next action independent exact-head review plus hosted CI.
* 2026-11-13 02:38Z: #1500 merged (`ad1a17229`), refs #74. Its body reports five browser checks passed including "home 24" and independent bounded local publication Pass; "Browser/AT were not rerun and no conformance is claimed"; "Scoped 96 C4/5 spent, older whole-96 history unknown, no C5 admitted".
* Source authorization: no finite correction grant for #74 was recoverable from the read sources beyond the 2026-11-12 test-only admission. Absence of a grant is recorded as unknown, not as zero spent and not as exhaustion of unrelated slices. This task grants none.

## Actual visible representations on current main (6f29)

| Item | Where shown | Source | Unknown handling |
| --- | --- | --- | --- |
| Home evidence documents | Home panel (region "This home only: evidence, decision, cost allocation and outcome", h2 `hc-home`), h3 "Evidence documents" | `home_case.view` `home.documents`, id/name/kind only | null renders "Unknown: no source-backed records supplied."; empty renders "None recorded." |
| Home decision | Home panel | `home.decision` | "None recorded" when no status |
| Home cost allocation | Home panel, h3 "Cost allocation" | `home.cost_allocation`, own home only | non-finance: restricted notice, payload null |
| Home outcome | Home panel: stage, open/closed, funding confirmed, h3 "Quality outcomes" | `home.stage`, `closed`, `funding_confirmed` (now `funding_ok is True`), `quality` measure/state | Quality null renders Unknown. No handover evidence or measured performance field exists |
| Building systems, dependencies, holds, works | Building panel (h2 `hc-building`, "Shared at building level, not this home's evidence"), one h3 each, and on `#/building/<id>` as separate h2 cards | `buildings.view` payload minus `homes` | "Unknown: no shared building record is linked."; absent category Unknown; empty "Source records explicitly list none." |
| Building shared costs | Building panel h3 "Shared building costs"; building screen card | `building.costs` | restricted for non-finance, Unknown when not supplied |
| Building item applicability (`case_ids`, `package_ids`) | Rendered only on the building screen (`buildingView`, "Affected homes: ... Packages: ..."); not rendered in the home-case building panel | present in the payload for staff with scope | `null` renders Unknown on the building screen only |
| Cross-home inheritance | Notice text; no inheritance path in view | `home_case.view` per-case data only | n/a |

## Execution evidence versus current-main proof

* 47e43ec7 baseline: 16 PASS (core 7, API 3, browser) at c6637004; historical, not current main.
* #1500 adds, in the maintained check and tests (observed in diff only): own document and quality in home panel only (ZF-2 and ZF-3), shared system SYS-1 in building panel only, ZF-3 opened, ZF-3 12000.00 only in building panel and 6000.00 in home panel, five-heading structure, non-finance HTTP payload with no amounts, finance HTTP payload with own allocation and building cost, `funding_confirmed` explicit-True core test. Count arithmetic 16 + 2 + 6 = 24 matches the reported "home 24".
* That 24 is a #1500 author candidate-head report. Whether the checks were rerun on the exact merged 6f29 tree, and whether any hosted workflow runs `home_case_browser_check` (only `src/api/README.md` mentions it among `.github`, `tools` and READMEs searched), is not established here. Treat as unobserved for current main.
* Follow-up 2 of the 2300 state (rerun the touched checks after #82 merges) cannot be resolved: PR #82 does not exist in this repository by number lookup (`gh pr view 82` failed). Dependency status unknown; record, do not infer.

## Gap map (this task's single product)

| ID | Status | Basis |
| --- | --- | --- |
| G1 shared systems apart from home | Delivered in source and maintained check; current-main execution unobserved | #1500 diff |
| G2 own-home documents and quality, ZF-3 opened | Same | #1500 diff |
| G3 non-finance restricted cost over HTTP | Same (API test) | #1500 diff |
| G4 finance amounts over HTTP | Same | #1500 diff |
| Missing or null funding (adverse, critique CR-002) | `home_case.view` maps absent or null `funding_ok` to false and the screen renders "Funding confirmed: no", so an unknown value reads as a negative. Representation decision is open; this was the admitted `funding_confirmed` behavior of #1500 and its test, not changed here | `home_case.py` 156, `app.js` 1344 |
| G6 labelled heading structure | Asserted as a count of five main headings (one h1 plus four h2 per the check's name; levels not separately verified, critique CR-003); each category is an h3 in source only | `home_case_browser_check.py`, `app.js` |
| Dependencies, holds, works, costs separate from home evidence, decision, allocation, outcome | Source already delivers on both screens. No missing behavior established. | `app.js` 1324 to 1395, `home_case.py` view |
| G5 applicability of each shared item (home or package scope, or Unknown) in the home-case building panel | Established display limitation (critique CR-001, High): the home-case building panel lists every building item without scope, so a work item scoped only to ZF-2 (fixture `building_fixture.py` 94) also appears in ZF-3's building panel with no sign of whether it applies. It is correctly outside the home-only panel and is not a cross-home evidence transfer, but a reader cannot tell applicability; the building screen does show it. Whether fixing it is required by the criterion is decision-gated and the 2026-11-12 admission excluded it | `homeCaseView` `shared()` versus `buildingView` |
| Outcome tuple (stage, quality, handover, performance) | Owner definition not approved; handover and performance fields do not exist; PRD v0.21.0 `in-review`, BRD v0.21.0 `draft` per the 1406 matrix | 1406 matrix |
| Keyboard, AT, human acceptance, SQL Server durable-store acceptance, hosted proof | Separate gates, outside this task | #74 comments |

## Authority separation

* Independent local engineering, supported by existing admission: re-observe existing checks on current main (verification only, no source change).
* Decision-gated (not an automatic human blocker for unknown values, but a scope and authority gap): G5 display in the home panel, any outcome-field addition. Both change visible behavior beyond the admitted test-only slice, so need an explicit admission. Unknown applicability must render as Unknown, never inferred from a shared building ID.
* Not locally resolvable: human, AT and live acceptance, hosted CI, SQL Server evidence.

## Planning Readiness

Ready for a verification-only increment (V1) with no source change. Not ready for a source change: no established missing behavior for the literal criterion, and the one display omission (G5) lacks an admission. Criterion 2 is not ticked, narrowed or closed by this task.
