# Research: issue 144 live container hosting proof (demo)

Task issue-144-live. Demo only, rg ama, owner decisions 2026-11-18. Unticked criteria: (1) images real, versioned, deployed through the pipeline; (3) hardening enforced in the deployed app.

Research disposition: executed. Planning Readiness: Ready.

## Findings

* Apps and jobs all run digest-pinned images from the private ACR; no quickstart placeholder remains.
* `gh run list --workflow src-deploy.yml` is empty; the workflow needs private self-hosted runners and protected environments. Pipeline deployment cannot be proven for the demo. ACR public access is Disabled, so tags cannot be listed.
* Exec into the live replica: uid 10001, CapEff 0, CapBnd default, NoNewPrivs 0, root fs overlay rw.
* ARM schemas 2025-07-01 and 2025-02-02-preview define no securityContext; the deployed template has none.
* Load run (150 clients, 60 s, /healthz): 15,819 requests, all 200, scale 0 to 4, revision unchanged.

Canonical evidence: docs/reference/research/issue-144-container-hosting-live-evidence-2026-11-18.md
