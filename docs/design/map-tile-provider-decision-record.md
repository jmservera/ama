---
title: Map tile provider decision record and accessible map alternative (#119)
description: Decision record for the Zava Forward basemap provider and the standing accessible list alternative. Proposed only; no licensed provider is selected and no spend is authorised
ms.date: 2026-11-17
ms.topic: reference
---

## Status

Proposed. No licensed provider is selected. This record states what is
decided, what is not, and who decides the rest. It adds no key, account,
subscription or configuration, and it authorises no spend.

Issue #119 has two criteria and both stay unmet by this record:

* Provider licence, cost, coverage and processor terms recorded: unmet. The
  [options review](../reference/research/ux/map-tile-provider-options.md)
  compares five options, but only the OSM tile policy and the Azure Maps free
  allowance were re-read; every other vendor statement is draft, unverified,
  and no binding rate, licence or processor term exists.
* Screen reader test of the list alternative: unmet. No human or
  assistive-technology run has happened (see the
  [manual check record](../reference/research/ux/wcag-conformance-baseline.md#map-list-alternative-screen-reader-check-119)).

## Context

Staff and contractors see a Leaflet map of open cases. The browser requests
tiles directly, so the provider sees the viewer IP address, user agent, the
app origin as Referer, and the tile `z/x/y` (about 44 m wide at zoom 19 at the
pilot latitude, calculated). No case data, resident name or query text is in a
tile request. The provider is set only through `ZF_TILE_URL` (https) and
`ZF_TILE_ATTRIBUTION`; see [ADR 0002 decision 5](../adrs/0002-pilot-readiness-architecture.md)
and the [API guide](../../src/api/README.md).

## Decision

| Scope | Decision | Basis |
| --- | --- | --- |
| Synthetic demo | OpenStreetMap standard tiles may be configured for the low-traffic synthetic demo only, with visible attribution. | Owner approval recorded on issue #119 on 2026-10-25, scoped and time-limited; policy re-read that day. |
| Production or real homes | No provider. With `ZF_ENV=production` and an empty `ZF_TILE_URL` the server loads no tiles and the list alternative is the only route. | Code behaviour in `tile_config`; ADR 0002 decision 5 records public OSM tiles as demo only. |
| Licensed provider | Not selected. Candidates remain Azure Maps (ADR 0002 proposal), Ordnance Survey Maps API, MapTiler Cloud and self-hosted tiles. | Options review; every candidate lacks verified terms. |

## Gate before a licensed provider is chosen

All of the following must exist as dated evidence before any selection:

1. Re-read official licence, attribution, caching, coverage and processor or
   data processing terms for the shortlisted provider, with source URL and read
   date.
2. A written view from the Data Protection Officer on the viewed-area
   disclosure, and any DPIA update.
3. Procurement and legal approval of the binding terms.
4. A finite costed plan that fits verified headroom under the owner's current
   all-in October 2026 ceiling (USD 700; headroom Unknown at the options-review
   date), approved by the owner before any paid execution, including account
   creation.
5. A decision on whether a provider credential in the tile URL is accepted as
   visible to every signed-in browser, or a same-origin authenticated,
   rate-limited tile proxy is designed. No proxy is built here.

## Accessible alternative requirement

The map is never the only route to case information. This holds for every
provider, including when tiles fail or no provider is configured.

* The map panel keeps a `<details class="maplist">` list. Its summary reads
  "Show the map areas as a list (keyboard and screen reader friendly)" and it is
  synchronised with the filter and viewport. Clusters list home count, open safety issues and a
  zoom action; points list the home link and a plain-text status.
* A tile load failure is announced in a polite status line that points to the
  list.
* Requirements: FR-020 and AC-023 (equivalent table beside the map) and AC-067
  (the accessible list mirrors the map status text), in the
  [demonstrator PRD](../prds/zava-forward-retrofit-programme-demonstrator.md).
* Evidence status: automated source, Node-VM and browser checks exist
  (`test_ui_support.py`, `test_wcag_workbench_baseline_151.py`). They show
  markup and state, not what a screen reader announces. The human run
  (one screen reader per desktop OS, per the baseline protocol) is outstanding
  and no conformance is claimed.
* Changing provider must not remove or weaken the list, the attribution line or
  the tile-failure note.

## Who decides what remains

* Provider selection, spend and processor terms: the owner, with the DPO,
  procurement and legal.
* Screen reader acceptance: a human tester using the baseline protocol.
* Agents may retrieve, compare and flag changes. They must not select a
  provider, enter a key or approve terms.
