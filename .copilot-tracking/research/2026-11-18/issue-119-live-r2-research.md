---
title: Issue 119 live research r2 (opening)
ms.date: 2026-11-18
---

## Scope

Second live audit of issue 119 (synthetic demo, desktop only), preserving the earlier `issue-119-live` artifacts unchanged. Criteria: (1) provider licence, cost, coverage and processor terms recorded; (2) screen reader test of the list alternative.

Planned: re-read the deployed tile configuration (Azure CLI, existing login), re-probe the employee map with Playwright, and re-read the official vendor pages that the options review still labels draft or unverified (Azure Maps, Ordnance Survey, MapTiler, OSM copyright) so that criterion 1 rests on dated primary sources.

## Status

Opened before substantive search. Findings are appended below as gathered.

## Findings

* Deployed config, read with `az containerapp show` (existing login, read-only): `ZF_TILE_URL` is `https://tile.openstreetmap.org/{z}/{x}/{y}.png`, attribution is the OpenStreetMap contributors link; revision `ca-cutover-test-demo-api--0000031`. `/api/me` `map` returns the same pair. No licensed provider is configured.
* Playwright (Chromium, 1366 by 900, Entra employee test account, `#/overview`): 15 tile images loaded, 33 tile requests, no failed request, no console message, attribution "Leaflet | (c) OpenStreetMap contributors"; list alternative holds 443 links; keyboard path (Enter on summary, Tab to first link, Enter opens the case) works; with tile requests aborted the status note says the background could not load and the list still has 443 items. Tile response `Cache-Control: max-age=90111, stale-while-revalidate=604800, stale-if-error=604800`; request Referer is the app origin only. Evidence: `.copilot-tracking/evidence/2026-11-18/issue-119-live-r2/` (`probe2.json`, `probe3.json`, screenshots).
* Vendor pages re-read 2026-11-18: Azure Maps pricing page (en-gb) still renders the paid Base Map Tile rate as "$-" with 5,000 free; 15 tiles equal one transaction; "Contact Us" above 500K; volume discounts from 100,000 transactions. Learn transactions page (ms.date 2026-08-28) confirms 15 tiles = 1 transaction and that Get Map Attribution is nonbillable. Learn geographic scope page (updated 2026-03-25): EU or US geography only; request data stored in the chosen geography, replication within it, no limit on where users access; no UK geography. OS Maps API page: key required, Great Britain coverage, 15 working days update, raster tiles, you cannot restyle; plans and prices page not retrievable (the guessed docs path returned "Page Not Found"). MapTiler pricing: Free for testing, PoC, personal or non-commercial use; Flex 30 USD a month plus extra traffic; Custom prepaid with 99.9 percent SLA; the commercial-use feature row did not render legibly. OSM copyright page: ODbL, credit OSM and state the ODbL; "we cannot provide a free-of-charge map API or map tiles for third-pa[rty]" (truncated in the fetch; the full sentence was not read).
* Net change to the options review: Azure Maps free allowance, 15-tile rule, nonbillable attribution call and EU/US-only geography are now re-read from primary pages (the paid rate is still unreadable); MapTiler plan names and the non-commercial limit of Free are re-read; the OS plan prices, OS API terms, Azure Maps processor terms and MapTiler DPA remain unread.
* Research disposition: executed. Planning Readiness: Ready. Outcome expected: docs-only change (new dated research note, index and log entries, plus a dated update to the options review).
