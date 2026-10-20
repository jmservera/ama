<!-- markdownlint-disable-file -->

# Task Research: issue-119-map-options

| Field | Value |
| --- | --- |
| Date | 2026-10-20 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Research disposition | executed |
| Planning Readiness | Ready |
| Artifact path | .copilot-tracking/research/2026-10-20/issue-119-map-options-research.md |

## Research Brief

Issue #119 (owner direction in #126 comment 6290697705): research map tile
licence, cost and privacy options for owner review, retain the accessible list,
buy and select nothing, send no private coordinates, and perform a real
screen-reader check of the existing list only if a screen reader is genuinely
available.

## Findings

* Existing delivery: Leaflet bundled in `web/vendor`; `tile_config()` in
  `src/api/src/zava_forward/api/server.py` reads `ZF_TILE_URL` (https) and
  `ZF_TILE_ATTRIBUTION`; development default is public OSM; production without a
  URL has no tiles and only the list. The tile URL reaches every signed-in
  browser through `/api/me` `map.tiles`.
* Accessible list: `details.maplist` with `summary#maplist-h`, a labelled `ul`,
  cluster buttons, point links, polite status line and an error alert
  (`web/app.js` about lines 1015-1060).
* Tools: no NVDA, Orca, espeak or speech-dispatcher; only `at-spi2-core`; no
  display; no axe package; Playwright Chromium present. No screen-reader run is
  possible. DOM or snapshot checks are engineering evidence only.
* Public vendor pages read on 2026-10-20 (no private coordinates sent): OSM tile
  policy and copyright; Azure Maps pricing, transactions, geography, auth;
  OS Maps API docs; MapTiler pricing, terms, privacy. Several price, plan and
  processor-term pages were unreadable (JS-only or blank) and are recorded as
  unverified.
* Not reviewed: Google, Mapbox, HERE, Esri, Stadia.

## Planning Readiness

Ready: docs-only synthesis plus a protocol. Gate risk: criterion 2 (actual
screen-reader test) cannot be met on this host.

## Outstanding

Human or assistive-technology run; provider price, terms and processor
verification; owner decision.

## Clarification 2026-10-20 (appended after coordinator intervention)

This record was authored in draft commit 69fa487a by a pass that did NOT activate the rpi-research, rpi-plan, rpi-implement or rpi-review skills, and its critique was an ad hoc rubber-duck pass, not rpi-plan-critique. Treat it as pre-RPI, unverified draft material, not an executed RPI phase or accepted outcome. Lifecycle evidence is in the issue-119-map-options-recovery-* artifacts and recovery state. Nothing above was edited.
