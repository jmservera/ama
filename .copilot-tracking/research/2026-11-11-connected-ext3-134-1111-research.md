# Research: #134 extension E3 (staged, research and plan only)

Date: 2026-11-11. Head 96fed1c3 (tree db89ed9b). Evidence: [independent E2 report](/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/independent-134-extension2-96fed-1111.json), verdict request_changes, one High. All prior RPI, adverse reports and source are preserved. No source, test or runtime action was taken. E3 is the final grant (original five, E1, E2 spent); no E4.

Finding confirmed from source: Technical readiness (role-screens.js 564-575, 573-576) builds text from c.technical_missing owners and from c.stock_reconciliation (query id, field, owner for unresolved queries). It is selected-home data. E2 classified it as other because its audit tested classification completeness, not exclusion correctness.

## Exhaustive panel map (six screens, role-screens.js)

Home-derived data is any value read from the selected case c (or a per-home call keyed by c.id). Portfolio or ledger values come from queue, report or portfolio calls. Static values are literals.

### asset-board (render 217-256; load 209-214)

| Panel | Lines | Data dependency | Class and rationale |
| --- | --- | --- | --- |
| Evidence boundary | 220-222 | literal plus c.id | home id only (Home scope text); no record data. Positive expectation already asserts it |
| Stock conflict queue across homes | 223-230 | extra.queue from /api/asset/stock-queue (all homes) | portfolio; excluded |
| Stock conflict comparison | 231-237 | c.stock_reconciliation, owners | HOME RECORD; scanned |
| Eligibility | 238-241 | owner from c.stock_reconciliation | HOME RECORD; scanned |
| Missing investment inputs | 242-244 | module constant assetInputs (134) | static; excluded |
| Benefits and phase check | 245-250 | module constant assetGates (141) plus literal | static; excluded |
| Portfolio scope | 251-253 | extra.portfolio total | portfolio count; excluded |
| Ledger-wide AI cohort / usage and alerts | 254-255 | extra.report via assetCost (149), assetUsage (168) | ledger-wide report; excluded |

### programme-queue (render 520-530; overview 505-515 not rendered for a selected home)

| Panel | Lines | Data dependency | Class |
| --- | --- | --- | --- |
| Connected view for c.id | 522-529 | programmeGates(c, orders) 462-476 reads c.work.blockers, c.technical, c.finance.budget, c.quality, work orders for c.id | HOME RECORD; scanned (title prefix) |
| Journey stages for c.id (nested, 490-497) | 490 | module constant journeyStages (478-485), c.id in title and links, role access | home id only, no record data; excluded, id is not a leak marker and the heading and link checks already bind the id |
| Not shown for this role | 23, 527 | literal | static; excluded |

### technical-queue (render 556-621)

| Panel | Lines | Data dependency | Class |
| --- | --- | --- | --- |
| Evidence boundary | 570-572 | literal plus c.id | home id only |
| Technical readiness | 573-576 (reasons 561-569) | c.technical, c.technical_missing items and owners, c.stock_reconciliation id, field and owner, sign-off state text | HOME RECORD; MUST BE SCANNED (E2 High) |
| Source facts | 577-582 | c.stock_reconciliation | HOME RECORD; scanned |
| Design version | 583-586 | c.technical | HOME RECORD; scanned |
| Separate sign-offs | 587-589 | c.technical.signoffs | HOME RECORD; scanned |
| Returns and routing | 590-596 | sign-off history | HOME RECORD; scanned |
| Missing references | 597-599 | c.technical_missing | HOME RECORD; scanned |
| Not shown for this role | 23 | literal | static |

### resident-choice (render 738-775; summary 719-735 is the portfolio overview, not rendered for a selected home)

| Panel | Lines | Data dependency | Class |
| --- | --- | --- | --- |
| Evidence boundary | 742-744 | literal plus c.id | home id only |
| Choice for each measure | 745-749 | c.measure_decisions | HOME RECORD; scanned |
| Paused or withdrawn by the resident | 750-759 | c.measure_decisions | HOME RECORD; scanned |
| Linked update commitment | 760-766 | c.resident_update | HOME RECORD; scanned |
| Service requests and access needs | 767-770 | c.service_requests | HOME RECORD; scanned |
| Choice comes before offered capacity | 771-772 | literal paragraph only | static; excluded |
| Choice and update commitments across open homes | 724-734 | queue from /api/resident/choice-queue | portfolio, only in overview; excluded |

### quality-queue (render 627-662)

| Panel | Lines | Data dependency | Class |
| --- | --- | --- | --- |
| Evidence boundary | 642-645 | literal plus c.id | home id only |
| Handover readiness | 646-648 | blockers from c.quality, c.measures, c.quality_handover_blockers | HOME RECORD; scanned |
| One panel per record titled measure and state | 649-658 | c.quality records (people, evidence, defect, handover) | HOME RECORD; scanned by dynamic rule |
| Quality evidence (no records) | 659 | literal empty state | scanned (no data, harmless) |
| Not shown for this role | 23 | literal | static |

### finance-invoices (render 1268-1285; helpers 1231-1250)

| Panel | Lines | Data dependency | Class |
| --- | --- | --- | --- |
| Evidence boundary | 1274-1277 | literal plus c.id | home id only |
| Invoices waiting for Finance | 1278-1283 | extra.queue from /api/finance (all homes) | portfolio; excluded |
| Invoice line comparison | financeInvoicePanel 1231-1246 | c.finance.invoices | HOME RECORD; scanned |
| AI economics (ledger-wide) | financeEconomicsPanel 1251-1260 | extra.report | ledger-wide; excluded |

## Findings for the plan

* One true omission remains: Technical readiness. The other exclusions each have a source reason in the table: portfolio or ledger data from a cross-home call, a module constant, a literal, or the home id only.
* Evidence boundary and Journey stages carry only the home id. A wrong-home heading is already rejected by the heading and menu predicates, and ids are not leak markers.
* Not found: any other emitted panel in the six screens carries record data.

## Evidence qualification (new, additive)

The independent report found that unit-attempt1.exit, .out and .err under /tmp/z134/e2 hold a later successful run, because a second rename wrote the same basenames. The original adverse bytes of the first unit run (the audit test wrongly included the hazard block) are not retained. The Changes and handoff claim of preservation was therefore wrong for that file. Not corrected by editing prior records and not recreated. The genuine ruffcheck-attempt1 (exit 1, E501) is retained. The final E2 exits (unit, ruffcheck, ruffformat, mypy, browser all 0) were verified by the independent reviewer.

## Readiness

Ready for implementation within E3, local engineering only, pending root and reviewer assessment of the inventory. R1 (A4 reading of ZF-2) stays unresolved. No A4, whole #134, #233 or #149 claim.
