---
title: Map Tile Provider and Accessible List Live Demo Evidence (Issue 119)
description: Per-criterion record of the two unticked criteria of issue 119 on the deployed synthetic demo, with what was proven, what was not and why
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live
Azure was authorised (resource group `ama`, cap USD 700, no drills, no Key
Vault rotation, no production change). Azure billing reconciliation, DPO and
Legal approval and person-run assistive-technology testing are not needed for
the demo. No source file changed. No Azure resource or setting was created or
changed, so nothing needs deleting. Credentials were read from the owner's
files at run time and never printed; a literal scan of every retained evidence
file for the account name and password found no match, and the application
host name was replaced with `<app-fqdn>` in the retained JSON.

Target: `ca-cutover-test-demo-api`, Playwright Chromium, 1366 by 900, signed in
with the employee test account (Entra), 2026-11-18 about 12:40 to 12:55 UTC.
The map sits on the Overview screen (`/app#/overview`), not on the landing
page (first attempt, retained as adverse evidence). Evidence files are under
`.copilot-tracking/evidence/2026-11-18/issue-119-live/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Deployed tile provider | `ZF_TILE_URL` on the app is the public `https://tile.openstreetmap.org/{z}/{x}/{y}.png` with an OpenStreetMap contributors attribution. No licensed provider is configured | `az containerapp show` environment query (the two tile variables only; observed, raw output not retained); `probe2.json` `me_map` |
| Content security policy | `img-src 'self' data: blob: https://tile.openstreetmap.org` | `probe2.json` `csp` |
| Map renders with tiles | Overview shows "Map of open cases" with 443 homes shown; 15 loaded tile images, 33 tile requests, no failed request, no console message; attribution "Leaflet \| (c) OpenStreetMap contributors" visible | `probe2.json`, [screenshot](../../../.copilot-tracking/evidence/2026-11-18/issue-119-live/map-desktop-1366.png) |
| What a tile request carries | HTTP 200, `Referer` is the app origin only, default browser User-Agent (headless Chromium), response `Cache-Control: max-age=87635, stale-while-revalidate=604800` | `probe3.json` `tile` |
| OSM Tile Usage Policy, re-read | Best-effort, no SLA; access may be blocked without notice; attribution, identifying User-Agent and Referer required; no bulk or offline use; "Commercial services ... access may be withdrawn at any point"; subject to the OSMF Privacy Policy | `osm-tile-policy-2026-11-18.txt` (page text retained) |
| List alternative present | `details.maplist` "Show the map areas as a list (keyboard and screen reader friendly)" holds 443 links, each named with home, status and sensor state | `probe2.json` |
| Accessibility tree of the sidebar | Chromium accessibility snapshot exposes a `complementary` landmark named "Map information and home summary", two `status` regions, the list as `list` with `listitem` links and the `details` summary | `probe2.json` `aria_snapshot_map_info` |
| Keyboard path | Focus on the summary, Enter opens it, Tab moves to the first list link (visible focus ring), Enter opens that case page | `probe3.json` `keyboard` |
| Tiles blocked (provider unavailable simulated by aborting the tile host in the browser) | The status note reads "The map background could not load. The homes and the list of map areas still work..."; the list still has 443 items | `probe3.json` `blocked` |

## Acceptance criteria

| Criterion | Status | Basis and limit |
| --- | --- | --- |
| Provider licence, cost, coverage and processor terms recorded | Partly proven for the demo; unproven for production | Proven: the demo provider, its licence basis (OSM data under ODbL via the OSMF tile service, attribution shown), cost (no charge under the policy; no SLA) and coverage (global, tiles load for the demo area) are recorded, and the policy was re-read today. Processor terms: OSMF is not a contracted processor; the policy points to its Privacy Policy and the tile request reveals the viewer IP, user agent and origin Referer plus the viewed `z/x/y` (see the [options review](./ux/map-tile-provider-options.md)). Not proven: a licensed provider is not chosen, no price or processor agreement exists for any commercial option, and the options review rows other than OSM stay "draft, unverified". The OSM policy states commercial services may lose access, so the public service is a demo-only default. Choosing and contracting a provider is a production decision (owner, DPO, procurement), not provable on the demo |
| Screen reader test of the list alternative | Unproven as a screen reader run; engineering proxies proven | Person-run assistive-technology testing is not needed for the demo (owner decision 2026-11-18) and no screen reader is installed on the test host or was run. Proven instead: the accessibility tree exposes landmark, status, list and named links, the keyboard path works, and the list stays usable when tiles fail. These are engineering checks and do not establish screen reader acceptance |

## Adverse and corrective evidence

* On 2026-11-18 (r3) five screenshots that showed resident and officer names were removed from `.copilot-tracking/evidence/2026-11-18/issue-119-live/`: `map-list-open`, `keyboard-focus-list`, `keyboard-opened-case`, `tiles-blocked-list-works` and `landing-no-map`. Person names in the probe JSON link text were redacted to `[name removed]` at independent review. `map-desktop-1366.png` shows no names and is kept.

* The first probe went to `/app` and found no map (`probe1-landing-no-map.json`); the map is on `#/overview`. Kept as run.
* The list holds 443 items inside a `details` element; announcement order and
  verbosity under real assistive technology were not observed.
* The test host runs headless Chromium, so the User-Agent in the tile request is
  the headless default, not a production browser mix.
* The tile-failure state was simulated in the browser, not by an actual provider
  outage.
* The tile requests of these probes reached the public OSM service (about 100
  tile requests in total, none bulk).
