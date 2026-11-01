# Research: intermittent /vendor/leaflet.js failure (#524)

* Task: issue-524-workspace-script-retry; disposition: executed; Planning Readiness: Ready.
* Already delivered: PR #527 (f41ecbc3, 2026-10-28) added `retryWorkspaceScript` (two retries, 250/500 ms back-off, 5 s timeout, release-versioned URL reuse, terminal plain-language error with `reloadWorkspace`) in `src/api/src/zava_forward/api/web/app.js`, with Node VM tests in `src/api/tests/test_workspace_scripts.py` (error then ready; error twice then terminal message; timeout/load not reinjected; concurrent sharing). All 4 tests pass on this branch (2026-11-01).
* Cause evidence:
  * Local: `StaticAssets` serves leaflet.js with body length equal to the file size (147552 bytes), a content ETag, and `no-cache, must-revalidate` (unversioned) or `immutable` (versioned `?v=`). No truncation or caching defect in the server code.
  * Config: `infra/main.bicep` and `infra/modules/containerapps.bicep` default `apiMinReplicas` to 0 (scale to zero).
  * Live probe 2026-11-01 01:0x UTC: `GET /vendor/leaflet.js` on the cutover-test employee app timed out at 30 s with no response (HTTP 000), consistent with the recorded 24 s cold-start `/healthz` on 2026-10-31.
  * Conclusion: most likely cause is replica cold start or scale-from-zero producing a failed or stalled static request, not a server asset defect. Not proven for the owner's 2026-10-28 incident (no platform logs retrieved); recorded as likely, unconfirmed.
* Not verified: authenticated live recovery check (owner attested 2026-10-31 that the test user may be used after #616 and #617 are deployed; those fixes are not yet confirmed deployed; no credentials in this session).
* Residual risk: a 5 s per-attempt timeout is shorter than observed cold starts (24 s+), so retries may exhaust on a cold replica. Follow-up, out of this slice's scope.
