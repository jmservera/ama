# Plan: issue #350 slice 1 (2026-11-04)

Task: issue-350-anon-api-401. Research: ../research/2026-11-04-issue-350-anon-api-401-research.md. Details: ../details/2026-11-04-issue-350-anon-api-401-details.md.

Stacked slices:

* [x] Slice 1: executed test pinning anonymous `/api/*` 401 JSON and page 302 for browser-style requests (this PR, Refs #350).
* [ ] Slice 2: platform auth action change in Bicep with live trusted-principal proof (infrastructure and security; needs live Azure; not started).
* [ ] Slices for criteria 2 to 10: owner/Azure prerequisites; not started.

Critique (one pass, direct): the test must not imply criterion 1 is met, because the platform intercept is untested offline. Applied: PR and log say Refs only and name the unmet half. No product code change, so no AI, consent or approval boundary is touched.
