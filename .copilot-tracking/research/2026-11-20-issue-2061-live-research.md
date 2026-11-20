# Issue 2061 research (2026-11-20)

Task: issue-2061-live. Option A (owner, 2026-11-20): one external Container Apps environment, keep the public endpoint and Entra registrations, production design unchanged. Research disposition: executed. Planning Readiness: Ready.
Base: origin/main 9fa2dbeaa (checked 2026-11-20).

## Findings

* `demoDirectIngress` already deploys a separate external environment `cae-<prefix>-demo` on subnet `snet-aca-demo` with prefix `<prefix>-demo` apps. The live second environment `cae-cutover-test` is the same stack deployed without the flag (internal, subnet `snet-aca`, private DNS zone `jollytree-20e6e99e...`).
* `live-receiver-job.bicep` and `live-simulator-job.bicep` already default to and are scope-guarded on `cae-cutover-test-demo`; `resident-demo.bicep` defaults to it. They need no re-pointing. `public-edge-existing.bicep` requires an internal environment and an Entra-authenticated API; it is a production-profile entry point and is unused by the demo profile.
* Live inventory (read-only, 2026-11-20): `ca-cutover-test-api` and `ca-cutover-test-agents` plus eight jobs sit in the internal environment; `ca-cutover-test-demo-api` and `ca-resident-demo` sit in the external one. Only `ca-cutover-test-agents` has no ingress; every other app has `external: true`.
* Identities: `id-cutover-test-api` is shared by both APIs and by the ledger-verify, rank-publish, smoke, mi-http, public-audit and verify jobs.
* Entra: `ca-cutover-test-demo-api` uses a real registration (client GUID `0dbb6baf-c8af-414f-ad0b-5daa7695cbc9`, secret setting present). `ca-cutover-test-api` has the placeholder client `systemAssignedIdentity` and no registration, so no redirect URI of a real registration belongs to the internal environment. `az ad app list` is denied (insufficient privileges), so redirect URIs and the logout URL are unreadable and cannot be compared before and after.
* The managed infrastructure resource groups (`ME_cae-...`) are not readable (AuthorizationFailed), so the internal load balancer and public IP resource ids cannot be listed by this login.

## Design decisions

* New `demoSingleEnvironment` parameter in `main.bicep`, valid only with `demoDirectIngress` (development profile). It splits the job identity from the public API identity and records the single-environment contract.
* New optional identity `id-<prefix>-internal` (only when the parameter is true) for the ledger digest and ranking-publish jobs, which today reuse the public API identity. Without the parameter the outputs fall back to the API identity, so production is unchanged.
* The vnet keeps `snet-aca`; it is listed as an owner-approved cleanup item rather than removed by template, because a vnet update that drops a subnet in use fails.
