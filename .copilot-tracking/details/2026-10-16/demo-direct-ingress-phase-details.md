# Demo direct ingress phase details

Task ID: issue-360. Slug: demo-direct-ingress.

## P01-T01

Add demoDirectIngress to main and Container Apps; use a workload-only suffix so
all backing names and identity references remain the same. Add a conditional
dedicated delegated subnet and NSG allowing Internet TCP 443, not 80 or arbitrary
Internet ports. Keep old subnets present. Skip internal environment DNS for the
external demo; NoProxy and public FQDN callbacks. Guard production and edge
combinations, forbid public backing access and unsafe unauthenticated demos.
Compile and evaluate guard matrices/private module inputs with existing tests.

## P02-T01

Direct setup flag/tag selects correct API without az afd or cdn. Ambiguity
must be explicit, not first-match selection. Verify external environment and
ingress, reject arbitrary public-url overrides. Reuse idempotent registration,
secret, roster and enforcement helpers. Diagnose actual missing extensions in
the isolated profile. Preserve Front Door behavior and unit coverage.
Extend private proof smoke or shared probe helper: no redirect following,
health/welcome 200, API 401, browser redirect to exact Microsoft login host,
and optional wrong-role session 403 supplied privately, never logged.
Don't call simulated roles real authorization acceptance.

PC-002: direct probe mode bypasses only private-DNS validation, not TLS/status
checks. Retain private defaults. Require health/root/welcome 200; native and
browser JSON API 401; malformed bearer and forged principal 401; browser /app
302 to HTTPS login.microsoftonline.com. Inspect redirects without automatic
following; allow only individually validated bounded same-origin auth hops.
Browser API 302 is a failure, never success. Optional private wrong-role session
must yield 403; absent session is Not run. Test hostile/malformed redirects.

PC-003: direct setup forces NoProxy. Inherited Return401/bearer configuration
requires explicit --enable-browser (or actionable refusal); never globally
change bearer preservation. Test stale Custom/Standard forwarding, direct
FQDN callbacks with retained existing callbacks, idempotence and zero afd/cdn.

## P03-T01

Runbook includes new environment/apps/jobs, no-move rule, private DNS resolution,
NSG, identity/RBAC, exact digest/env/auth/config parity, staged activation,
single active scheduled consumer, acceptance, rollback and gated retirement.
Keep SQL private, identities/data/PE/DNS intact. No old environment deletion
until its jobs/apps/private-edge dependencies are retired under owner approval.
Explain no standing Consumption environment charge vs running replica/log/network
and retained edge overlap costs. Historical MVP git evidence must not copy
obsolete broad public exposure. Update evidence pack, relevant ADR statement,
KB index and append-only log.

PC-001: runbook inventory covers agents, orchestrator, token renewal, ledger
verification and imports. Initially create environment only, then API only
with all other consumers disabled/omitted using a compiled staging control.
Queue workers at minReplicas=0 are NOT inactive. Before trigger activation,
pause old producers, stop new claims, drain/disposition in-flight work and
running jobs, then enable only the new generation. Rollback reverses this
sequence without dual writers or replaying imports.

## P04-T01

Use existing infra unittest discovery, Bicep compiler, scoped Ruff/mypy.
Record tool failures honestly, fix introduced failures. One independent review
routes findings transparently; do not claim live acceptance. Commit on existing
clean topic branch, resolve gh account and set repository-local privacy email,
include required trailer, push non-forced and open main-based PR with Refs #360.
