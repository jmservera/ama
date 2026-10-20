---
title: Map tile provider licence, cost and privacy options (#119)
description: Sourced options review for the Zava Forward map basemap, with licence, attribution, coverage, cost, processor and privacy implications, and what remains unverified. A proposal for owner review, not a selection or a purchase
ms.date: 2026-10-20
ms.topic: reference
---

## Status and boundary

This is a research proposal for owner review under the owner direction
recorded in issue #126 (comment 6290697705, 2026-10-20): research map
licence, cost and privacy options, retain the accessible list and make no
purchase. Nothing here selects a provider, creates an account, key or
subscription, changes configuration or approves terms. No legal, privacy or
procurement sign-off has been given. Pricing, terms and policies change; each
row records the date it was read (2026-10-20) and must be re-read before any
decision. The review used only public documentation pages. No request carried
private, staff or resident coordinates.

Existing delivery is unchanged. The map uses Leaflet bundled in `web/vendor`
and a tile provider set by `ZF_TILE_URL` (https only) and `ZF_TILE_ATTRIBUTION`.
In development the default is the public OpenStreetMap server; with
`ZF_ENV=production` and no `ZF_TILE_URL` no tiles load and the accessible list
is the only route (see the [API guide](../../../../src/api/README.md) and
[ADR 0002 decision 5](../../../adrs/0002-pilot-readiness-architecture.md)).

## What a tile request reveals

Observed from the current code (`src/api/src/zava_forward/api/web/app.js`,
`server.py`) and documentation:

* The browser, not the server, requests tiles. The provider sees the staff or
  contractor browser IP address, user agent, a Referer limited to the app
  origin (`strict-origin-when-cross-origin`), the tile `z/x/y` and any
  credential in the URL.
* No case data, home identifier, resident name or query text is in a tile
  request. The app does not use a provider geocoding or search service, and
  this review recommends none.
* `maxZoom` is 19. A tile is about 76 m wide at the equator at zoom 19; at the
  pilot latitude (about 55 degrees north) that is about 44 m, and about 175 m at
  zoom 17 (calculated, not measured). A map centred on one property at high
  zoom therefore tells the provider, linked to the viewer's IP, roughly which
  street or building was viewed. ADR 0002 says the request "leaks only the
  viewed area and zoom". That is accurate but should not be read as no
  location disclosure at high zoom. Whether this is personal data about
  residents is a question for the Data Protection Officer, not decided here.
* The configured tile URL is returned to every signed-in browser
  (`/api/me` `map.tiles`). A provider key in that URL would be visible to
  staff and contractor users. Providers that require a key or token in the URL
  need either a restricted, rotatable credential accepted as exposed, or a
  same-origin tile proxy that keeps the credential on the server.

## Options reviewed

Currency and prices are as published on the date read. "Not verified" means the
source could not be read in full or is a secondary source.

| Option | Licence, terms and attribution | Coverage | Cost evidence | Processor and privacy position | Read |
| --- | --- | --- | --- | --- | --- |
| A. Public OpenStreetMap tiles (`tile.openstreetmap.org`), current development default | [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/): best-effort, no SLA, may be blocked without notice, heavy or inappropriate use not allowed, commercial or donation-seeking services warned access may be withdrawn. Visible attribution required, identifying User-Agent, Referer must be sent, cache per headers or at least 7 days, no prefetch or offline use. Data is ODbL ([copyright](https://www.openstreetmap.org/copyright)) | Global, community-edited | Free of charge | Governed by the OSMF Privacy Policy. Policy says do not submit personal or confidential data and that aggregated usage logs are published. No data processing agreement is offered | 2026-10-20 |
| B. Azure Maps (ADR 0002 proposal) | Microsoft Product Terms and Data Protection Addendum apply but the licensing page could not be read, so tile caching, attribution and permitted-use terms are not verified. Render has a Get Map Attribution API | Global; UK street-level detail not verified | [Pricing page](https://azure.microsoft.com/en-gb/pricing/details/azure-maps/): Gen2 only (Gen1 retired 2026-09-15 per [Learn](https://learn.microsoft.com/en-us/azure/azure-maps/how-to-manage-pricing-tier)); 5,000 free Base Map Tile transactions a month, 15 tiles per transaction, so 75,000 free tiles ([Learn](https://learn.microsoft.com/en-us/azure/azure-maps/understanding-azure-maps-transactions)). The fetched pricing page rendered paid rates as "$-" and says prices are USD converted to local currency monthly, so the paid rate and GBP value are not verified. A figure of 4.50 USD per 1,000 transactions appears only in secondary sources and is not relied on | Account geography can be set to the Europe endpoint `eu.atlas.microsoft.com` to keep stored request data in Europe, with replication within the geography; it does not limit where users access it ([Learn](https://learn.microsoft.com/en-us/azure/azure-maps/geographic-scope), page dated 2022, updated 2026-03-25). ARM template regions listed are `westeurope` and `northeurope`, not `uksouth`, so UK-only residency is not shown. Microsoft processor role for location data is described in secondary sources only | 2026-10-20 |
| C. Ordnance Survey Maps API via OS Data Hub | [OS Maps API](https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api.md): raster ZXY or WMTS, Web Mercator or British National Grid, styles Road, Outdoor, Light and Leisure, OpenData and Premium layers. API key required. Attribution: copyright statement, terms link and error-report link must sit inside the embedded map on web apps, and the OS logo applies ([branding](https://docs.os.uk/os-apis/core-concepts/os-api-branding.md)). The [OS API Service Terms](https://osdatahub.os.uk/support/legal/api-terms) require adequate security against unauthorised use and were not read (page needs JavaScript) | Great Britain only; updated 15 working days after each product refresh | Plans page needs JavaScript and was not read. Secondary summary, not verified: OpenData free; Premium plan with up to 1,000 GBP of free premium transactions a month then about 0.0331 GBP per 15-tile view (a second secondary summary read later the same day also quotes about 0.000525 GBP per leisure-scale 15-tile view, so the secondary figures are inconsistent and none is relied on); Public Sector Plan free for registered PSGA members ([OS public sector page](https://www.ordnancesurvey.co.uk/customers/public-sector/os-data-hub-public-sector) confirms the PSGA plan exists but not the terms). Live projects are rate limited to 600 transactions a minute per API, development projects 50 ([policy](https://docs.os.uk/os-apis/core-concepts/rate-limiting-policy.md)). Whether Zava North Homes, a fictional case-study body, would qualify for PSGA is unknown | OS says for a public interactive web map use a backend proxy and do not embed credentials in client JavaScript, and that a key in the URL or header can be reused by others ([authentication](https://docs.os.uk/os-apis/core-concepts/authentication.md)); an internal, non-public prototype may not need one. OS Data Hub processor terms and request logging not verified | 2026-10-20 |
| D. MapTiler Cloud (commercial OSM-based) | [Pricing](https://www.maptiler.com/cloud/pricing/): Free plan for testing, proof of concept, personal or non-commercial use with a MapTiler logo; Flex 30 USD a month plus extra traffic billed monthly; Custom prepaid with 99.9 percent SLA. Which plan permits commercial use was not legible in the fetched table. [General terms](https://www.maptiler.com/terms/) and attribution rules not read in detail | Global; UK detail not verified | USD, as above; no GBP figure | Swiss company (MapTiler AG); [privacy policy](https://www.maptiler.com/privacy-policy/) covers IP address and service use. Whether a data processing agreement and UK/EU transfer basis are offered is not verified | 2026-10-20 |
| E. Self-hosted OSM-derived tiles in the Zava Azure estate | OSM data is ODbL with attribution and share-alike on derived databases (copyright page). Tile server licences and the [Protomaps](https://docs.protomaps.com/) PMTiles option were not verified in detail. The OSMF policy points to self-hosting and vector tiles as the alternative for offline or heavy use | UK extract available from public mirrors such as Geofabrik; coverage as OSM | No price evidence gathered; storage, compute and update operations would be Zava costs against the existing monthly budget | No third-party request carries viewing data; the processor is the Azure estate already in the ADR. Highest operations burden; ADR 0002 rejected it as "not now" | 2026-10-20 |

Not reviewed, so neither recommended nor rejected here: Google Maps Platform,
Mapbox, HERE, Esri and Stadia Maps.

## Bounded options for owner review

These are comparative observations for the owner to decide on, not a
selection, ranking or approval. Each keeps the existing Leaflet client,
`ZF_TILE_URL` contract and accessible list. Any prioritisation belongs to the
owner after the verification items below close.

* Option A is documented as a development and synthetic-demonstration default
  only. Its policy does not support production traffic, and it must not be used
  with real homes.
* Options B and C are the two candidates with a documented UK-relevant fit.
  C is Great Britain only and has published attribution and proxy guidance,
  but its cost depends on an unverified PSGA or free-allowance position. B
  keeps terms in the Microsoft tenant as ADR 0002 proposed, but its paid
  rate, UK detail, attribution and processor terms are not yet verified and its
  Europe geography is not the pilot `uksouth` region.
* Option E removes any third-party tile request. It carries the highest
  operations burden and was recorded in ADR 0002 as "not now".
* Option D is a commercial alternative whose commercial-use plan and
  processor terms are not verified.
* Implementation inference, not vendor evidence: the current Leaflet image-tile
  request cannot attach an Entra `Authorization` header, which Azure Maps Entra
  authentication requires, so a URL key, a SAS token or a same-origin tile proxy
  would be needed unless a different tile-loading implementation were built.
  For URL-credentialed providers (B or C), the configured URL reaches every
  signed-in browser and OS advises against client-side credentials, so a
  same-origin, authenticated, rate-limited proxy is a design question to
  weigh. A proxy hides viewer IPs from the provider but adds a service,
  logging and caching rules to own, and it must never be an open proxy. No
  proxy is built here.
* The owner may wish to decide a maximum zoom or property-centred view policy
  with the DPO, because high zoom narrows the disclosed area to about one
  street.

## Cost estimate method (illustrative)

Azure Maps transactions per month are the number of base-map tile requests
divided by 15, rounded up per request, with the first 5,000 free (Learn).
The OS Premium plan reportedly bills per 15-tile view, but that rests on the
unverified secondary summary above and is not an established rule. Real usage
is unknown: the
pilot user count, session length and tile cache hit rate are not evidenced, so
no monthly figure is given. A finite costed execution plan, once usage is measured on synthetic sessions,
needs separate owner approval before any paid execution, not only before a paid
account is created. This proposal authorises no spend. The owner budget is
USD500 in total for the October 2026 calendar month (expiry 2026-10-25T16:02Z),
and it includes accrued and forecast costs and liabilities across resource group
`ama` and other scopes, so any provider charge competes with existing Azure and
inference costs. Aggregate headroom is not known here, and unknown or unbounded
headroom blocks all paid execution. The cap is not a new allocation, unknown
costs must not be assumed zero or double counted, and nothing here authorises
retiring a resource.

## Cannot yet be verified

* Microsoft Product Terms and Data Protection Addendum position for Azure Maps
  tile requests, including tile caching limits, attribution wording and whether
  Microsoft acts as processor or controller for the request metadata.
* Azure Maps paid rate and GBP value from the official page (rendered blank).
* OS Data Hub API Service Terms, plan prices, whether a housing association is
  a PSGA member, and OS Data Hub's data protection terms.
* MapTiler commercial-use plan and data processing terms.
* UK street-level detail and update frequency for A, B and D at the relevant
  zooms for Zava North Homes areas.
* Real tile volumes, a proxy design and its cost, and any legal view on whether
  a viewed tile area is personal data.
* The Data Protection Officer's view and any DPIA update.
* Whether the owner wishes to buy at all, and the real organisation's
  procurement route.

## Accessible list and screen-reader evidence

The accessible list alternative ("Show the map areas as a list (keyboard and
screen reader friendly)") exists and is unchanged. Real screen-reader evidence
is still missing. See the
[manual check record](./wcag-conformance-baseline.md#map-list-alternative-screen-reader-check-119)
for the protocol, the tools found on the 2026-10-20 host, and the unmet gate.
No UI file was changed.
