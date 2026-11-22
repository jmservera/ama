# Research: issue 2202 deploy merged demo changes, 2026-11-22

Refs #2202. Synthetic demo, desktop only. Owner decisions 2026-11-18 apply.

## Research disposition

Executed. Planning Readiness: Ready.

## Evidence

* Worktree HEAD equals origin/main 0d2081ef7a (PRs 2224 to 2228 merged).
* Read-only Azure probe: API app, job-live-simulator and job-live-receiver all run crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:60b1d026...; latest API revision ca-cutover-test-demo-api--0000043.
* ACR crcutovertestrzsrg is Disabled, default action Deny, export policy disabled; /tmp/acr-push.sh opens and restores it via a trap.

## Findings

* One image serves the API app and both live jobs, so one build and push, then three image updates (no Bicep).
* Primary note will be docs/reference/research/issue-2202-live-deploy-2026-11-22.md.

## Follow-ups (ranked)

1. Re-run any criterion left unproven after rollout.
