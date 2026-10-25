# Phase details: demo basemap configuration (issue 119 demo slice)

Date: 2026-10-25, before the critique and live change. SUPERSEDED in part by the plan's critique section: use single quotes for the command, no scripted single-tile HTTP request, and rollback success means both keys present with empty values.

## Phase 1 validation commands
* From `src/api`, gate venv: `python -m unittest test_ui_support.MapListAndTiles test_ui_support.ProductionTiles test_auth.TileConfigTests` (9 expected).
* Offline delta: load `/tmp/ama-119/app-before.json`, replace the two env values, compare to the post-update export; only those two env entries may differ among container env, image, resources, probes, scale, ingress, identity, secrets, registries and auth config (sanitized comparison; values that are not public are hashed, never printed).

## Phase 2 command (exact)
`az containerapp update -g ama -n ca-cutover-test-demo-api --set-env-vars "ZF_TILE_URL=https://tile.openstreetmap.org/{z}/{x}/{y}.png" "ZF_TILE_ATTRIBUTION=<existing OSM_ATTRIBUTION string, imported from server.py>"`. The attribution is read from the code constant, not retyped. The command is run once; no loop.

## Phase 3 checks
* `az containerapp revision list`: new revision active, Healthy, Running, traffic 100, old revision inactive.
* `az containerapp show`: image digest `...0769b52d...`, scale 0-4, probes unchanged.
* In-container read-only check with the existing PTY exec route: `python -c "from zava_forward.api.server import tile_config; print(tile_config())"` (prints the public URL, attribution and host only).
* Anonymous GET `/` and a protected route: 200 and 401; forged principal header on `/api/cases`: 401. The serving CSP is read from response headers of `/healthz` or `/`.
* Render proof: one stationary viewport only if policy permits; otherwise one single-tile HTTP request with a default browser-style user agent. Owner browser check stays unverified.

## Rollback
Set the two values to empty strings with `--set-env-vars ZF_TILE_URL= ZF_TILE_ATTRIBUTION=` (the original values were empty), then confirm the revision.

## Docs
`src/api/README.md` (map paragraph and development note), `infra/README.md` (runbook entry near line 1417), `docs/reference/log.md` (append) and an evidence note; update `docs/reference/README.md` index only if a new file is added.
