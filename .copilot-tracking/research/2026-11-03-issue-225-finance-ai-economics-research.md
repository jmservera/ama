# Research: issue 225 finance AI economics section (2026-11-03)

Prior delivery (merged): #657 (invoice queue, line comparison, funding route, field draft, readiness view) and #785 (exception explanations). #490 was closed unmerged.

Evidence in the current tree (`src/api/src/zava_forward/api/web/role-screens.js`):

* `finance-invoices` had an AI economics block with two Unknown rows and the shared `assetCost` fields.
* `finance-funding` showed only `assetCost`; it lacked reconciliation, Total Cost of AI components and a booked-value row.
* Tokenomics source: `docs/reference/resources/ai-tokenomics.md` (draft v0.5.2 practice, not a standard). Five value destinations are needed for a booked value. BRD OD-51 is open: no price, budget or target.

Acceptance status before this slice: criteria 1 to 3 delivered and unit-tested; criterion 4 (WCAG browser, axe, AT) unproven; criterion 5 partly (Fluent 2 not assessed); tokenomics criterion partly (no per-component rows, no booked-value destinations, absent on the funding screen).

Planning readiness: Ready. Slice: one shared economics panel on both finance screens.
