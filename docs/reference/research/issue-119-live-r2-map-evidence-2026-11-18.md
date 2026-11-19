---
title: Map Tile Provider and Accessible List Live Demo Evidence, Second Run (Issue 119)
description: Second per-criterion audit of issue 119 on the deployed synthetic demo, with a re-read of the vendor pages the options review still lists as unverified, what was proven, what was not and why
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

This run repeats and extends the [first live audit](./issue-119-live-map-evidence-2026-11-18.md),
which stays unchanged. Owner decisions of 2026-11-18: this is the synthetic
demo, desktop only. Live Azure was authorised (resource group `ama`, cap USD
700, no drills, no Key Vault rotation, no production change). Azure billing
reconciliation, DPO and Legal approval and person-run assistive-technology
testing are not needed for the demo.

Nothing was created or changed in Azure (one read-only `az containerapp show`),
so nothing needed deleting. No source file changed. Sign-in credentials were
read from the owner's files at run time and never printed; a literal scan of
the evidence folder for the three credential values found no match, and the
application host suffix was replaced with `<app-fqdn-suffix>` in the retained
JSON and scripts. Screenshots that showed resident names were not retained and
names are removed from the retained JSON; only the map overview screenshots
remain.

Target: `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000031`,
Playwright Chromium at 1366 by 900, employee test account, 2026-11-18 about
15:40 UTC. Evidence is in
`.copilot-tracking/evidence/2026-11-18/issue-119-live-r2/`.

## Live observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Deployed tile provider | `ZF_TILE_URL` is `https://tile.openstreetmap.org/{z}/{x}/{y}.png`; attribution is the OpenStreetMap contributors link. `/api/me` `map` returns the same pair. No licensed provider is configured | `az containerapp show` environment query for the two tile variables (observed, raw output not retained); `probe2.json` `me_map` |
| Map renders | Overview shows 443 homes; 15 tile images loaded, 33 tile requests, no failed request, no console message; attribution "Leaflet \| (c) OpenStreetMap contributors" | `probe2.json`, [screenshot](../../../.copilot-tracking/evidence/2026-11-18/issue-119-live-r2/map-desktop-1366.png) |
| Tile request content | HTTP 200, Referer limited to the app origin, headless Chromium User-Agent, `Cache-Control: max-age=90111, stale-while-revalidate=604800, stale-if-error=604800` | `probe3.json` `tile` |
| List alternative | `details.maplist` holds 443 links; the accessibility tree exposes a `complementary` landmark "Map information and home summary", `status` regions, the list and named links | `probe2.json` |
| Keyboard path | Enter on the summary opens the list, Tab reaches the first link, Enter opens the case page | `probe3.json` `keyboard` |
| Tiles blocked (aborted in the browser) | Status note says the background could not load and the list still works; 443 list items remain | `probe3.json` `blocked` |

## Vendor pages re-read on 2026-11-18

Public pages only; no private data was sent. These rows update the draft
status in the [options review](./ux/map-tile-provider-options.md#update-at-2026-11-18).

| Provider | Now re-read from the primary page | Still not verified |
| --- | --- | --- |
| Azure Maps | [Pricing](https://azure.microsoft.com/en-gb/pricing/details/azure-maps/): 5,000 free Base Map Tiles; 15 tile requests make one transaction; volume discounts from 100,000 transactions, "Contact Us" above 500K. [Transactions](https://learn.microsoft.com/en-us/azure/azure-maps/understanding-azure-maps-transactions) (ms.date 2026-08-28): Get Map Attribution is nonbillable. [Geographic scope](https://learn.microsoft.com/en-us/azure/azure-maps/geographic-scope) (updated 2026-03-25): residency choices are Europe or United States, request data is stored in the chosen geography and may be replicated within it, and access location is not limited | Paid Base Map rate (the page shows "$-"); GBP value; UK-only residency (no UK geography is listed); Microsoft Product Terms and Data Protection Addendum position for tile requests; attribution wording |
| Ordnance Survey Maps API | [Docs](https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api.md): API key required, Great Britain coverage, raster tiles, update 15 working days after each product refresh, tiles cannot be re-styled | Plan prices, free allowances, PSGA eligibility, API service terms, data protection terms (the plans page was not retrievable) |
| MapTiler Cloud | [Pricing](https://www.maptiler.com/cloud/pricing/): Free for testing, proof of concept, prototyping, personal or non-commercial use with a MapTiler logo; Flex 30 USD a month plus extra traffic; Custom prepaid with 99.9 percent SLA | Which plans permit commercial use (the feature row did not render); included usage and extra rates; data processing terms |
| OpenStreetMap data | [Copyright](https://www.openstreetmap.org/copyright): ODbL, credit OpenStreetMap and state the ODbL; the page begins to say the project cannot provide a free-of-charge map API or tiles for third parties (the fetch truncated the sentence, so the rest was not read) | Full wording of that limit |

## Acceptance criteria

| Criterion | Status | Basis and limit |
| --- | --- | --- |
| Provider licence, cost, coverage and processor terms recorded | Partly proven for the demo; unproven for production | Proven for the demo provider: licence basis (OSM data under ODbL via the OSMF tile service, attribution shown), cost (no charge under the policy, no SLA), coverage (global, tiles load for the demo area) and the viewer data a tile request reveals (IP, User-Agent, origin Referer, `z/x/y`). Proven for the options: the re-read rows above, including that Azure Maps has no UK geography and OS covers Great Britain only. Processor terms: OSMF offers no processor agreement and the request goes straight from the browser. Unproven: no licensed provider is chosen, no price or processor agreement exists for any commercial option, and the unread items in the table above remain open |
| Screen reader test of the list alternative | Unproven as a screen reader run; engineering proxies proven | Person-run assistive-technology testing is not needed for the demo (owner decision 2026-11-18) and no screen reader was run. Proven instead: accessibility tree with landmark, status, list and named links; keyboard path; list usable when tiles fail. These do not establish screen reader acceptance |

## Production-only items

These cannot be proven on the demo and stay open on issue 119 for production.

* Select a licensed provider and contract it: owner, procurement and DPO decision, with a priced plan and a data processing agreement.
* Confirm tile caching, attribution and permitted-use terms for the chosen provider and the real organisation.
* Decide a same-origin tile proxy or restricted key if the provider needs a credential in the URL, and a maximum-zoom policy with the DPO.
* Run the screen reader protocol of the [WCAG baseline](./ux/wcag-conformance-baseline.md#map-list-alternative-screen-reader-check-119) with real assistive technology and users.
* Replace the public OSM service before real homes are shown; its policy says access may be withdrawn for commercial services.

## Adverse and corrective evidence

* The list holds 443 items inside a `details` element; announcement order and verbosity were not observed under assistive technology.
* The test host runs headless Chromium, so the User-Agent is the headless default.
* The tile-failure state was simulated by aborting tile requests, not by a provider outage.
* The probes sent 33 tile requests from the first probe plus the loads of the second probe to the public OSM service (none bulk).
* The OS plans page and the MapTiler feature table did not render in the fetch, and the Azure Maps paid rate is still blank; none of those figures is claimed.
