# Research: issue #107 live proof, third pass (2026-11-18)

Disposition: opened. Planning Readiness: pending.

Scope: the two unticked criteria on #107 (independent SQL/worker race tests with old images and restarts; matching approved exercise record, delivered-build acceptance). Demo only, desktop, Tier FOCUSED, docs/evidence only. Prior passes: docs/reference/research/issue-107-live-assistants-evidence-2026-11-18.md and issue-107-live-r2-assistants-evidence-2026-11-18.md. Candidate gap for this pass: an actual older API image (from the demo ACR) run against actual SQL Server with a revoked release, instead of the SQLite proxy.

## Findings

* ACR `crcutovertestrzsrg` has `publicNetworkAccess: Disabled` and network default action `Deny`; `az acr repository show-tags` fails with a connectivity error. Opening it would be an infrastructure change the owner decision does not authorise. An older released image therefore cannot be pulled; the old-image half of criterion 1 stays proxy-only. Old source trees are not a substitute: they predate release admission.
* `az containerapp revision list`: one active revision, `ca-cutover-test-demo-api--0000032` created 2026-11-18T16:20:23Z, image digest `sha256:5368f4e4...c17e5fb`, identical to the r2 digest at revision 0000031. This is a real restart that kept the same image.
* Read-only probe (Entra demo employee, `Retrofit Programme Manager`): five assistants, each release `missing: approved, unexpired release record`, authority holders for release, residual-risk acceptance, suspension and restart all `gap` (OQ-017); forecast `proactive: false`, `call_allowance: 0`, held text `Suspended (SUS-1)`; rai-metrics `tokens: 0`, `fallback: 16`, `persisted: 87`.
* Origin of SUS-1 (r2 open question): `/api/continuity` output retained in deployed-parity-live-r3 shows `epoch 1, suspended [SUS-1, scope all]`, a probe suspension recorded by the #122 audit (docs/reference/log.md). It is stored in SQL and survived the 0000031 to 0000032 restart, so a restart did not lift a suspension. No restart authority is appointed, so none was exercised.
* Criterion 2 approved side still needs a named approver and residual-risk holder (OQ-017); fabricating one is out of scope.

Disposition: executed. Planning Readiness: Ready. Follow-up: r2 note's SQL Server 2022 and SQLite results are reused, not re-run (no source change since; HEAD da33c1ecc).
