---
title: Map Tile Provider and Accessible List Live Demo Evidence, Fourth Run (Issue 119)
description: Fourth per-criterion check of issue 119 on the deployed synthetic demo, with a fresh live probe, a re-read of the OpenStreetMap policy pages and a clear split between demo proof and production-only items
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

This run repeats the [first](./issue-119-live-map-evidence-2026-11-18.md) and
[second](./issue-119-live-r2-map-evidence-2026-11-18.md) live audits, which stay
unchanged. Owner decisions of 2026-11-18: this is the synthetic demo, desktop
only; live Azure is authorised (resource group `ama`, cap USD 700, no drills, no
Key Vault rotation, no production change); billing reconciliation, DPO and Legal
approval and person-run assistive-technology testing are not needed for the demo.

Nothing was created or changed in Azure (two read-only `az containerapp show`
calls), so nothing needed deleting. No source file changed (docs-only, focused
tier). Credentials were read at run time and never printed; a literal scan of the
evidence folder for the sign-in values found no match. The application host is
replaced by `<app-fqdn-suffix>`; screenshots and JSON fields that showed resident
names were removed.

Target: `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000032`,
Playwright Chromium at 1366 by 900, employee test account, 2026-11-18 about 16:55
UTC. Evidence is in `.copilot-tracking/evidence/2026-11-18/issue-119-live/`
(`probe2.json`, `probe3.json`, `probe2.py`, `probe3.py`, `map-desktop-1366.png`).

## Live observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Deployed tile provider | `ZF_TILE_URL` is `https://tile.openstreetmap.org/{z}/{x}/{y}.png` with the OpenStreetMap contributors attribution link; `/api/me` `map` returns the same pair. No licensed provider is configured | `az containerapp show` env query (observed in this run); `probe2.json` `me_map` |
| Map renders | 443 homes; 33 tile requests, 15 tile images loaded, no failed request, no console message; attribution "Leaflet \| (c) OpenStreetMap contributors" | `probe2.json` |
| Tile request content | HTTP 200; Referer limited to the app origin; headless Chromium User-Agent; `Cache-Control: max-age=87231, stale-while-revalidate=604800, stale-if-error=604800`; `image/png` | `probe3.json` `tile` |
| List alternative | 443 list items in the `details` list; accessibility tree shows a `complementary` landmark "Map information and home summary", `status` regions, a labelled list | `probe2.json` |
| Keyboard path | Summary takes focus, Enter opens the list, Tab reaches the first link (`#/case/...`), Enter opens the case page | `probe3.json` `keyboard` |
| Tiles blocked (aborted in the browser) | Status says the background could not load and the list still works; 443 list items remain | `probe3.json` `blocked` |

## Provider terms re-read on 2026-11-18

The [OSMF Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)
and [OSM copyright page](https://www.openstreetmap.org/copyright) were read in
full this run, which closes the truncated-sentence gap left by the second run.

* Licence: data is ODbL; credit OpenStreetMap and make clear the data is under
  the ODbL. Tile use must follow the policy.
* Cost and service: the copyright page states OSM "cannot provide a free-of-charge
  map API or map tiles for third-parties" and points to the tile policy; the
  policy says availability is best effort with no SLA and that capacity is
  donation funded.
* Permitted use: interactive viewing by a human, caching per HTTP headers (at
  least 7 days otherwise), a valid Referer, no bulk download, no offline use.
* Privacy and processor terms: use is under the OSMF Privacy Policy; no
  processor or data protection agreement is offered; OSMF publishes anonymised
  aggregated tile usage data.
* Withdrawal: "Commercial services, or those that seek donations, should be
  especially aware that access may be withdrawn at any point."
* Coverage: global tiles (seen loading for the demo area).

The Ordnance Survey plans page (the guessed URL returns Page Not Found), Azure
Maps paid rates, the MapTiler commercial-use matrix and any data processing
agreement for a commercial option were not obtained; no figure for them is
claimed. Earlier rows in the [options review](./ux/map-tile-provider-options.md)
and the second run stand.

## Acceptance criteria

| Criterion | Status | Basis and limit |
| --- | --- | --- |
| Provider licence, cost, coverage and processor terms recorded | Proven for the demo provider (OSMF tiles); unproven for any licensed provider | Demo provider: licence (ODbL, attribution shown on the live map), cost (no charge, best effort, no SLA, not offered for commercial dependence), coverage (global; tiles load), processor terms (none offered; the browser calls the provider directly and the provider sees IP, User-Agent, origin Referer and `z/x/y`). The issue asks for a licensed provider; none is selected, priced or contracted, so the criterion as written is not met. Not needed for the demo: DPO and Legal approval |
| Screen reader test of the list alternative | Unproven | No screen reader was run: person-run assistive-technology testing is not needed for the demo (owner decision 2026-11-18). Automated proxies pass: landmark, status regions, labelled list, keyboard path, list works with tiles blocked. These do not establish screen reader acceptance |

Neither box should be ticked on #119 from this evidence.

## Production-only items

* Select, price and contract a licensed provider with a data processing agreement; owner, procurement and DPO decision.
* Confirm caching, attribution and permitted-use terms for the chosen provider; decide a same-origin proxy or restricted key and a maximum-zoom policy.
* Run the [screen reader protocol](./ux/wcag-conformance-baseline.md#map-list-alternative-screen-reader-check-119) with real assistive technology.
* Replace the public OSM service before real homes are shown.

## Adverse evidence and limits

* The list holds 443 items inside a `details` element; announcement order and verbosity were not observed under assistive technology.
* Headless Chromium sends its default User-Agent, which the OSM policy discourages for apps; real browsers send their own.
* The tile-failure state was simulated by aborting requests, not by a provider outage.
* The probe loads sent about 33 tile requests each to the public OSM service (none bulk).
* Cache-Control max-age differs between runs (90111 then 87231 seconds); the value is provider controlled.
