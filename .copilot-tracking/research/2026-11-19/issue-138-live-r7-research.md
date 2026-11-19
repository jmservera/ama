# Research, issue 138 seventh demo run (Refs #138)

Disposition: executed (read-only recheck). Planning Readiness: Ready for a no-source-change outcome.

Baseline: docs/reference/research/issue-138-live-r6-2026-11-19.md. The `verify-federation` operation and
its test are already on main, so criterion 1 has its buildable code. Live state recorded in
docs/reference/research/issue-138-live-r7-2026-11-19/readonly-recheck.txt is unchanged: 0 federated
credentials on six identities, no `AZURE_*` variables, only `*-plan` environments with 0 protection rules,
0 `src-deploy.yml` runs. Every remaining criterion needs GitHub admin, Entra changes, a runner or a push,
all outside the demo's no-production-change and no-push limits.
