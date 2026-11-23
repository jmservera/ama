# Research: #2164 r4 (2026-11-23)

Disposition: executed (re-verification). Planning Readiness: Ready.

* Issue asks: decide whether roster-bound Entra staff inherit roster scope; add tests for view_only with an eligible role and for scope bypass. Refs #2163, #360.
* Main b11b8259bd contains 6a03928ccb (#2274, 2026-11-22T21:26:50Z); `Assistants.authorize` re-reads the bound roster row (src/core/src/zava_forward/core/assistants.py:1507).
* Live: `ca-cutover-test-demo-api--0000054` (created 2026-11-22T23:14Z, digest sha256:3f2be664...faf945), `ca-resident-demo--0000026`. ACR is network-restricted (publicNetworkAccess Disabled), so digest to commit mapping is unavailable.
* Tests re-run: api 2 OK; core test_assistants_identity 5 OK.
* Demo evidence note: docs/reference/research/issue-2164-roster-scope-recheck-2026-11-22.md (to be extended).
