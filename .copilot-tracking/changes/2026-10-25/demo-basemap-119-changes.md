# Changes: demo basemap configuration (issue 119 demo slice)

Date: 2026-10-25. Actual order: research (12:16Z), plan and details, independent critique (verdict FAIL as drafted, all five findings accepted into the plan), then implementation (live config 12:18Z, then docs). No source, image or UI change.

## Live (operational, separate from source)
* 12:18:15Z `az containerapp update --set-env-vars` with single-quoted values for `ZF_TILE_URL` and `ZF_TILE_ATTRIBUTION` on `ca-cutover-test-demo-api`. Revision `--0000006` Healthy, Running, 100 percent, same image digest. Sanitized diff: only the two entries changed (27 entries both sides; image, resources, probes, scale, ingress, secrets, registries, identity identical). In-container `tile_config()` shows the OSM URL, host and attribution; CSP `img-src` allows only `https://tile.openstreetmap.org`; `/healthz` 200; anonymous and forged-header protected API 401. Private backups `/tmp/ama-119/`; report `/tmp/ama-119-demo-basemap-live.md`; issue comment 119 (6397549257).
* Critique-driven deviations applied: single quotes; no scripted tile HTTP check (not interactive browser use); deterministic time and cost gates (about 38 USD estimate versus 50 USD, ActualCost stale and lagged, never a cap proof).
* Rollback not used.

## Repository
* `infra/README.md`: runbook entry with before and after, quoting, rollback, OSM terms and limits.
* `src/api/README.md`: development note that the demo app uses the OSM URL under a scoped approval, not a provider choice.
* `docs/reference/log.md`: appended entry. No new knowledge-base file, so no index change.

## Not done or not verified
Browser render of the map, visible attribution on screen, origin-only Referer on a real tile request, owner browser check. Production provider, licence, cost, coverage, processor choice and screen-reader acceptance (#119) remain unmet. Existing tests (9 tile tests) passed on unmodified main before the change; no test changed.

## Review-driven errata (independent review PASS-WITH-FINDINGS, recorded without rewriting the earlier text)
* Timestamps: the minute stamps "12:20Z" (research), "12:2xZ" (critique) and "12:19Z" (tests) in the earlier artifacts were estimates written from memory and are wrong. Actual clock readings in the session: the focused tests and research file were produced before the plan; the plan and critique were complete by 12:18:01Z (shell `date -u`); the first live command began at 12:18:15Z (`/tmp/ama-119/update.log`). The order research, plan, critique, live change is supported by that log and by the critique text being appended to the plan before the update; the minute stamps are not evidence.
* The details file was written before the critique and keeps its superseded steps (double-quoted command, scripted single-tile fetch, rollback without a success definition). The plan's critique section is authoritative; the command actually run used single quotes, no tile fetch was made, and rollback success means both keys present with empty values.
* Plan sentence "or reactivate --0000005 is not needed" meant: in single revision mode the update created `--0000006` and no reactivation of `--0000005` is part of the rollback.
* Time and cost gates: the UTC check (12:18:01Z, before the 16:02Z limit) and the stale ActualCost query (298.91 USD, 12:18Z, immediately before the update) ran just before the command; the 1 USD fixed allowance from the critique, not the plan's "one more day", was used for the 38 USD estimate.
* Exact quoting is recorded in the infra README entry; `update.log` holds only start and status.
