# Research: issue 349 live tenant prerequisites (2026-11-18)

Opening note. Disposition: executed. Prior note docs/reference/research/entra-signin-live-demo-2026-11-18.md exists; this run re-verifies live, adds read-only Azure/Graph probes for registration, redirect URIs, roles, vault reference, and fresh browser proofs under .copilot-tracking/evidence/2026-11-18/issue-349-live2/.
Planning Readiness: Ready (set at close of research below).

## Result

Disposition executed. Planning Readiness: Ready. Findings and the per-criterion table are in
docs/reference/research/issue-349-tenant-prerequisites-live-r3-2026-11-18.md; evidence in
.copilot-tracking/evidence/2026-11-18/issue-349-live2/. Key new facts: the Entra authorize request carries redirect_uri
<app-host>/.auth/login/aad/callback and sign-in completes (edge callback registered); credential is a Key Vault
reference; vault public-disabled with private endpoint; Graph reads denied (provisioner, audience, role definitions,
redirect list unreadable). Adverse: account-picker screenshot rendered blank and was deleted.
