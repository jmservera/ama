# Changes: #134 extension E3 (final, of 3)

Start head 701b8a4e99a3a53769ac1d49cce354cf5c040d7f, tree 8e70625123a464f3143c401e3894fd7360e20583; main e691255ff; original base 35eb0e559c. Owned source: src/api/checks/connected_home_browser_check.py, src/api/tests/test_connected_home_check.py. No product, API, auth, role, helper or README change. Plan approved by the independent plan assessment (no findings).

## Source changes

* Technical readiness moved into RECORD_PANELS (selected-home data: missing-item owners, stock conflict query ids, owners and sign-off state). It is now scanned for sibling leakage by the same production predicate.
* AUDITED_OTHER replaced by a reviewed manifest EXCLUDED: each excluded panel has a kind (portfolio-call, constant or home-id-only), an exact role-screens.js anchor and a reason. AUDITED_OTHER remains as the derived title view.
* The browser record-leak control now runs for Technical readiness and Source facts, restoring the page after each.

## Renderer and exclusion manifest (role-screens.js, anchors verified by test)

| Screen | Scanned (selected-home data) | Excluded, kind, anchor |
| --- | --- | --- |
| asset-board | Stock conflict comparison, Eligibility | Evidence boundary (home-id-only, "Home scope: ${c.id} only"); stock queue (portfolio-call, /api/asset/stock-queue); Missing investment inputs (constant, assetInputs.map); Benefits and phase check (constant, assetGates.map); Portfolio scope (portfolio-call, /api/cases?view=all&limit=1); two Ledger-wide panels (portfolio-call, /api/ai/report) |
| programme-queue | Connected view for (includes the nested Journey stages) | Evidence boundary (constant); Shared queue (portfolio-call, loadPage(0)); Lifecycle and funnel (portfolio-call, /api/coordinator?view=all) |
| technical-queue | Technical readiness, Source facts, Design version, Separate sign-offs, Returns and routing, Missing references | Evidence boundary (home-id-only) |
| resident-choice | Choice for each measure, Paused or withdrawn, Linked update commitment, Service requests | Evidence boundary (home-id-only); portfolio commitments (portfolio-call, queue.items); Choice comes before offered capacity (constant) |
| quality-queue | Handover readiness, Quality evidence, dynamic "Measure: State" | Evidence boundary (home-id-only) |
| finance-invoices | Invoice line comparison (helper-generated) | Evidence boundary (home-id-only, except the queue); Invoices waiting (portfolio-call, financeQueueRows(queue)); AI economics (portfolio-call, financeEconomicsPanel(extra?.report)) |

The audit is a reviewed dependency judgement from these anchors. It is not a proof of JavaScript data flow. Qualifications: the Programme and Resident overview is rendered with a selected home but sits outside .screen-evidence and derives cross-home data. Evidence boundary and Journey stages are id-only; the heading and menu predicates do not independently validate them, and Journey stages sits inside Connected view so its text may be scanned. No nested identity or A4 acceptance.

## Tests (12 pure tests; added or replaced)

* Literal-title negatives listed in the test, not taken from the inventory, for every home-data destination including summaries, owners, Source facts and the dynamic Quality panel. Each starts clean and requires rejection.
* Exact Technical readiness case: valid ZF-2 observation passes, then the real ZF-1 text "Source conflict <id> (<field>) is unresolved." is injected and rejected by sibling_failures; the id is absent from ZF-2 data.
* Manifest test: each exclusion's anchor exists, its panel text reads no selected-home field other than the id, and home-id-only panels contain the id.
* Retained: portfolio and ledger other-home marker positive case, renderer title coverage.

## Evidence (fresh directory /tmp/z134/e3-20261111T170206Z; full stdout, stderr and numeric exit per command; new basename per attempt)

| Name | Exit | Note |
| --- | --- | --- |
| before-unit | 1 | Harness error (old module imported without its sibling check module). Not a regression result. Retained. |
| before2-unit | 1 | Failing-before: HEAD checker with the new tests, 2 tests fail (Technical readiness leak not rejected). |
| after-unit / after-ruffcheck / after-ruffformat / after-mypy | 0 / 1 / 1 / 0 | Ruff E501 (3 lines) and format finding in the new test file. Genuine adverse, retained. |
| after2-unit / after2-ruffcheck / after2-ruffformat / after2-mypy | 0 / 0 / 0 / 0 | After line-length fix; 12 tests OK; mypy 234 files. |
| browser (flock -n -E99 timeout 900, once) | 0 | 142 PASS, 0 FAIL, empty stderr; Technical readiness control rejected. |

Browser identity: Chromium 156.0.8078.4 from browser.version; Playwright 1.64.0. Axe not run. The scratch trees old/ and oldb/ in the evidence directory hold the HEAD checker copy used for failing-before.
Evidence qualification: E2 unit-attempt1 original adverse bytes were overwritten earlier and are not retained or recreated; the E2 E501 adverse and all prior records are untouched.

## Limits

Six screens, five logins, Asset proxy, no rows 6/7/8/11, intake, aftercare, event order, eight-stage consistency, AT, users, consent, approvals. R1 (A4 reading of the ZF-2 control) stays unresolved. No criterion ticked; no #134, #233 or #149 claim. E3 of 3 is spent; no further correction without new owner authority.
