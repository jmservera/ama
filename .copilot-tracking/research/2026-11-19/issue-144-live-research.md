# Issue 144 live research, 2026-11-19

Unticked criteria: (1) images real, versioned, deployed through the pipeline; (3) hardening enforced in the deployed app.

Evidence already recorded in docs/reference/research/issue-144-live-deployed-images-2026-11-19.md and issue-144-container-hosting-live-evidence-2026-11-18.md. Re-run today: `az containerapp list` and `az containerapp job list` for group `ama`, piped to infra/scripts/deployed_images.py, gave 13 containers, all digest-pinned, exit 0. Deployed `securityContext` is null.

Planning Readiness: Ready (disposition: reused, plus a fresh live re-run). Buildable code for either criterion: none. Criterion 1 needs the src-deploy workflow on self-hosted runners with OIDC (never run; not permitted here). Criterion 3: Container Apps ARM has no securityContext, so read-only root and capability drop cannot be declared; redeploying is a production change.
