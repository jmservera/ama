# Plan: demo basemap configuration (issue 119 demo slice)

Date: 2026-10-25, written after the research artifact and before critique and any live change. Source: `.copilot-tracking/research/2026-10-25/demo-basemap-119-research.md`. Refs #119; no closing keyword. Details: `.copilot-tracking/details/2026-10-25/demo-basemap-119-phase-details.md`.

## Decision
Option 1: set only `ZF_TILE_URL=https://tile.openstreetmap.org/{z}/{x}/{y}.png` and `ZF_TILE_ATTRIBUTION` to the existing `OSM_ATTRIBUTION` string on `ca-cutover-test-demo-api`. No code change is planned, so no new image, no UI edit and no web-guidelines fetch (nothing web is edited). Documentation only: src/api README map text, infra README runbook entry, reference log, and an evidence note. Disclose OSM terms and the scoped owner approval; do not claim #119 acceptance.

## Phases
1. Prospective validation: focused local tile tests; exact planned delta computed offline from the private backup; independent critique of the plan.
2. Live (scoped to 16:02Z): re-check cost with 429 handling; fresh private full backup; independent offline delta check; `az containerapp update --set-env-vars`; verify new revision.
3. Validation: new revision Healthy, Running, 100 percent traffic, image digest unchanged; env diff is exactly the two values; in-container `tile_config()` read-only; serving CSP; healthz 200; anonymous and forged-header protected API 401; at most one stationary viewport or a single tile HTTP check; seed aggregate counts unchanged only if cheap.
4. Report promptly: `/tmp/ama-119-demo-basemap-live.md` and an issue comment before the publication gate.
5. Docs, independent review, full exact-head gate, official receipt verification, push, draft PR Refs #119.

## Cost guard
Config-only change, no new resource, no scaling change. Query ActualCost RG `ama` with retry and backoff on 429; treat the result as lagged, add a conservative allowance (carry forward the earlier 37 USD estimate of cumulative incremental, plus one more day at the observed rate). If it cannot be reasonably established, stop before the update. The revision restart adds seconds of consumption.

## Rollback
Only the two env values: set both back to empty (exact original state) with the same command form, or reactivate `--0000005` is not needed (single revision mode; the update creates `--0000006`). Keep `app-before.json` private.

## Out of scope
Graph, RBAC, network, new resources, scaling, probes, database, provider account, image build, source change.

## Independent critique (rubber-duck, run once, 12:2xZ): verdict FAIL as written, all findings accepted, plan amended below
1. Blocking: shell quoting. The attribution contains double quotes, `&`, `<`, `>`. Use single-quoted literal assignments: `'ZF_TILE_URL=https://tile.openstreetmap.org/{z}/{x}/{y}.png'` and `'ZF_TILE_ATTRIBUTION=&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'` (identical to `OSM_ATTRIBUTION`; a test-time equality check against the code constant is added to validation). Before and after full-spec diff proves other env and secretRefs are preserved.
2. Blocking: rollback asserted. Rollback success is defined as: both keys present with value equal to the empty string, or, if the CLI removes them, deliberately removed with the drift disclosed (`tile_config()` result is identical; Bicep declares both keys empty). Post-rollback verification must read both keys.
3. Blocking: the scripted single-tile HTTP check is not interactive browser use and a spoofed browser user agent does not cure that. REMOVED from the plan. Render evidence is at most one real stationary browser render (an isolated local browser on a local synthetic run of the same code, no panning, zooming or crawling) or none, leaving the owner browser check unverified.
4. Non-blocking, accepted: browser validation, if run, must show the attribution visibly rendered and the single tile request carrying an origin-only Referer to OSM; header inspection alone is not proof.
5. Non-blocking, accepted: deterministic gates. Immediately before the update, check the UTC time: stop if update and validation cannot finish before 16:02Z. Cost gate: prior cumulative incremental estimate (about 37 USD, from the seed route) plus a quantified allowance for this update and any rollback (set at 1 USD) must stay at or under 50 USD, otherwise stop. A 429 or stale ActualCost does not block if that bound is demonstrably under the cap; it must be stated as an estimate, never as a measured cap.
