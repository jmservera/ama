# Research: demo basemap configuration (issue 119 demo slice)

Date: 2026-10-25, written 12:20Z before any plan, critique or live change. Worktree `issue119-demo-basemap`, branch `fix/demo-basemap-119`, from main 0245944a. Refs #119 (never closes it).

## Trigger and scope
Owner reports the Leaflet background map is missing on the live demo. Owner approved, via a structured form, "OSM for the synthetic demo and scoped live configuration until 16:02 UTC". That renews only tile configuration and validation authority until 2026-10-25T16:02Z. The USD 50 cumulative incremental cap is not reset, USD 700 applies to resource group `ama` only, other live authority (12:00Z) has expired. Owner accepted: best effort, no SLA, disclosure of browser IP, viewed map area and site origin to OSM, visible attribution, caching and referrer, no case or person data sent, no bulk, offline or headless sweeps. Full #119 production-provider, screen-reader and licence acceptance remains unmet.

## Root cause (confirmed earlier, re-read now)
* `server.py` `tile_config`: when `ZF_TILE_URL` is empty and `ZF_ENV=production` it returns `url=None, host=None`; no OSM fallback in production. The live app has `ZF_TILE_URL` and `ZF_TILE_ATTRIBUTION` present but empty (from the Bicep parameters), and a `ZF_ENV` value set.
* `app.js` lines 1040-1041: `L.tileLayer` is added only when `me.map.tiles` is set, with `referrerPolicy: "strict-origin-when-cross-origin"` and `attribution: me.map.attribution`.
* `App.__init__`: CSP `img-src 'self' data: blob:` plus `tiles.host` when set, so setting a URL widens CSP to exactly one host.
* `SECURITY` headers send `Referrer-Policy: strict-origin-when-cross-origin`; responses use `Cache-Control: no-store` (applies to app responses, not to tile responses, which the browser caches by OSM's headers).
* `OSM_ATTRIBUTION` constant already contains the visible copyright link to openstreetmap.org/copyright.
* A non-empty `ZF_TILE_URL` is validated https-only (`sys.exit` otherwise), so a bad value fails startup, which the revision readiness check will expose.

## Existing evidence
* Tests: `test_ui_support.MapListAndTiles`, `ProductionTiles`, `test_auth.TileConfigTests`: 9 tests pass locally now on the unmodified main (run 12:19Z with the gate venv). They show server-rendered config, CSP following the host, production without URL loading no tiles.
* `src/api/README.md` lines 2165-2166, 2259 and 2367 document the variables and say no licensed provider has been chosen.
* Live app (private backup `/tmp/ama-119/app-before.json`, mode 600): revision `--0000005`, image digest ending `...6b8b6e7e` (0769b52d), single-revision mode, scale 0 to 4, Liveness and Readiness `/healthz`, no IP restrictions. 27 env entries; the two tile entries are empty values; no secretRef env.
* Live state from the seed route: 981 cases, 444 open (aggregate), not repeated here.

## Policy sources (retrieved by the coordinator, to be recorded, not re-fetched)
OSM tile usage policy (operations.osmfoundation.org/policies/tiles/): normal interactive browser use only, exact https endpoint, visible attribution with copyright link, default browser user agent, origin referer, normal browser cache, no bulk, prefetch, offline or headless scanning. OSM privacy policy (osmfoundation.org/wiki/Privacy_Policy).

## Options
1. Set the two env values on the existing app (config only, new revision, same image). Uses existing path, no code, no image, no new resource.
2. Change the code to default to OSM in production. Rejected: removes a deliberate safety fallback and needs an image.
3. Self-hosted or licensed provider. Rejected for now: #119 owner decision, new cost.

## Risks and constraints
* A containerapp update creates a new revision; scale-to-zero cold start is about 40 s; revision must reach Healthy, Running, 100 percent traffic on the same image.
* `az containerapp update --set-env-vars` replaces only named variables and keeps others; it must be proven by an independent before and after env diff (names, values hashed for non-public ones, secretRefs, image, scale, probes, ingress, identity, auth).
* Cost: `az containerapp update` is a config change with no new resource; cost API returned 429 earlier and ActualCost is lagged, so it is never a cap proof; allowance must be conservative and explicit.
* Real render proof must respect OSM no-headless-sweep: at most one stationary viewport (a few tiles) from an isolated local browser at most, or a single-tile HTTP check; otherwise the owner browser check stays unverified.
* Attribution value contains HTML (an anchor). Leaflet attribution accepts it. The env value is set by the operator, not user input.
* Documentation must not claim production provider approval or screen-reader acceptance.

## Planning readiness
Ready. Open item for the plan: exact `az` command and the delta validation procedure, rollback of only the two values, cost guard, validation set, and which docs to update (src/api README map text, infra README runbook, reference log, an evidence note).
