# Issue 144 live r2 research (2026-11-19)

Scope: synthetic demo, desktop only. Read-only Azure queries, resource group ama. Disposition: reused prior evidence plus fresh re-check. Planning Readiness: Ready (no buildable slice).

## Fresh re-check (2026-11-19, no secrets)

* `az containerapp show -g ama -n ca-cutover-test-demo-api`: latest revision 0000033; zero env names match ZF_CONTAINER_HARDENING or PYTHONDONTWRITEBYTECODE; no volumes declared.
* `gh run list --workflow src-deploy.yml`: no runs, so the pipeline has not published the live images.

## Unticked criteria

* Worker and job images real, versioned, deployed through the pipeline: classifier script and live digest proof already delivered (docs/reference/research/issue-144-live-deployed-images-2026-11-19.md). Remaining proof needs the private self-hosted runners and protected environments (production-only).
* Container hardening in the deployed app: needs a redeploy of a hardened image to a live app, which the owner decision rules out (no production changes). Marked unproven.

Conclusion: every remaining criterion is production-only; no new code or test is justified.
