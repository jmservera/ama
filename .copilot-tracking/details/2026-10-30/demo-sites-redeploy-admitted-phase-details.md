---
title: Admitted demo redeployment phase details
ms.date: 2026-10-30
---

Task 8053a799-0279-4f5c-b23b-adea3537291b; demo-sites-redeploy-admitted.

<!-- rpi:task id=P01-T01 -->
## P01-T01

Fresh raw backups of two apps, auth/history, eight full jobs, ACR and Hub/role
readback. Baseline compare prior unchanged protected state; operational drift
must be investigated, not overwritten. Current main matches retained build pin.
Actual image config rehash via docker save and source-label inspection. No
rebuild or reading private data/.env. Journal argv/exits/time and output hashes,
never token output.

Implement fresh publisher based on inspected route, correcting cleanup to check
fresh full expected state before EACH mutation. Baseline private Disabled,
existing empty IP rules and defaultAllow/exportDisabled/adminDisabled/bypassNone.
Resolve current VM public IPv4; add that /32 while public remains Disabled,
enable export, enable public with defaultDeny. Tokens in memory/stdin, private
owned Docker config, no ACR Tasks. Each operation/HTTP bounded by remaining
420s forward budget. Push both existing unique tags, fetch index/platform/
config digest chain, compare actual config bytes/source label, retain old
manifest presence before/after. Finally close public Disabled first even on
drift; restore only known owned IP/default/export deltas after exact readback.
Normalize bare-IP or /32 representation. Bound total600s, signals go through
finally. Restore entire stable baseline (only lifecycle exclusions), credential
cleanup exact files. Missing proof blocks SQL/apps.

<!-- rpi:task id=P02-T01 -->
## P02-T01

Use pinned-source STOCK_SQL_DDL register and capture SensorConsumer._schema
DDL with recording adapter (mssql=True), override read-only schema-check only
while recording, not on live DB. Never configure/seed/delete/insert controls.
Existing job retains image/identity/env/resources/template; start only one
execution with command override, parallelism1/completion1/timeout600 and
temporarily retry0. Verify no active execution, complete job baseline before
retry change. Restore retry field ONLY after comparing full baseline plus
owned delta, seven other jobs read-only.

Worker uses mssql_python with MSI/login/query timeouts20, XACT_ABORT and explicit
transaction, finite lock timeout. Six additive table definitions only if absent.
Metadata shape and count checks before/after, no row output; existing table
counts unchanged, new counts0. Capture prior view definition hash/columns.
Read principal SID/rights via canonical verifier before/after; existing allowlist
aggregate unchanged. Apply only third GO batch of pinned resident-showcase.sql,
no grants/schema/allowlist batches. Verify exact17-column SELECT TOP0 and count
under EXECUTE AS with guaranteed REVERT; COMMIT once. Exceptions emit only
type/status then rollback; no SQL/data bodies.

Bind post-COMMIT marker to worker/input hashes using deterministic input digest
and worker digest injected in execution env (not self-referential). Record
execution name, replica/attempt/completion and terminalSucceeded with exactly
one marker. Missing marker/ambiguous start is blocked, inspect same execution
only; never reapply. Restore retry in finally and prove all eight full definitions
equal except lifecycle fields; conflicting drift blocks downstream writes.

Implementation amendment: initial execution Failed with explicit pre-COMMIT
rollback/committed=false, then exact job restoration. One read-only metadata/
counts diagnostic execution is admitted to identify the exact failed predicate.
Only a root-cause-corrected unambiguous later write may proceed, not replay or
schema/data/permission widening. Preserve original worker/executor/hash/outputs.

<!-- rpi:task id=P02-T02 -->
## P02-T02

Fresh protected whole-app and separate auth readback plus job/ACR proof before
each write. Raw ARM API2025-07-01 PATCH only properties.template copied from
backup; edit image and unique revisionSuffix only, omit service-only imageType/
ephemeralStorage from request, retain environment absence/null/secretRef exactly.
One forward request per app. Probe /healthz to wake min0, verify target
latest=ready, Healthy/Provisioned, active100%, ready replica, digest and full
history one added/no removed. Compare full protected app excluding ONLY
expected image/suffix/service lifecycle fields; separate auth exact equality.

On actual startup failure, collect bounded console AND system logs privately
before ONE failure-only recovery to baseline template/digest with unique suffix;
max600s, inspect ambiguous writes without replay. Report nondelivery. Employee
failure never touches healthy resident. Auth/protected drift blocks further
mutation rather than overwriting unknown changes. Unexercised rollback remains
unexercised, not certified.

<!-- rpi:task id=P03-T01 -->
## P03-T01

Curl public health/shell/assets using finite deadlines and source-byte checks.
Anonymous employee /app,/app.js,/ops.js and shared assets deny; resident /api
checks use known protected route, no submitted credentials/model calls.
Playwright fresh context public pages1365x900 and390x844, collect aggregate
overflow/widget/status/console evidence directly into private raw receipt via
tool result (not fabricated transcription). Record Entra final origin/path only,
no OAuth parameters. No password, credential retrieval or private pages.
Owner checks chat thread/selector/consent/errors, expanded-map marker/header
synchronization, case icons/steps/blockers/tabs after Entra sign-in.
Final all app minima0, eight jobsManual, full ACR/auth/protected state; source
pin and approved Hub role preserved. Commands/results hashed and exported.

<!-- rpi:task id=P03-T02 -->
## P03-T02

Reconcile plan/details/changes/state before exactly one independent Review.
Reviewer reads actual fresh executors, journal, retained raw cloud metadata and
browser evidence; does not replay cloud mutations/tests. Preserve its original
outcome, route findings to later work without post-Review implementation.
Resolve gh authenticated id/login, compute noreply email, set repository-local
email and explicit author/committer identities. Stage only new task artifacts,
Conventional Commit with Refs and exact Copilot trailer. No push/amend/rewrite.
Publication gate is not run/claimed for a local evidence-only handoff.

## Implementation Reconciliation Before Review

P01/P02/P03-T01 complete; P03-T02 pending Review/local persistence.
Original one-execution expectation was amended after explicit rolled-back
failures, a rejected pre-DDL guard, one read-only schema diagnostic, rollback-
only rehearsal and local ledger reproduction. Final schema commit succeeded;
separate final view correction uses the actual working-tree SQL hash, not a
false unchanged-main claim. Exact generated ledger codes7..10 verified.
Source amendment: COALESCE optional sensor JSON to[]; one new actual-SQL
regression, no removals.44 selected tests pass,0 skips; Ruff lint/format pass.
No image rebuild or source-pin substitution.

Initial SQL shape/count acceptance missed NULL sensor JSON because optimizer
pruned the scalar projection. Counts-only full-projection probe identified
522 NULLs; actual local regression reproduced it. Corrective transaction
verified522 JSON arrays under resident identity before COMMIT, all six table
counts0 and unchanged522 allowlist/view. No row values emitted.
Exact old-view behavior recovered through minimal source-backed correction;
not a destructive ledger/table rollback. Existing resident target required one
restart and one deactivate/activate reset after dependency repair. Exactly one
new forward revision per app and no recovery-image request.

Latest=ready/Healthy/Provisioned/traffic100/ready replica, full protected app and
separate auth equality, prior histories and old manifests, all app minima0,
eight complete Manual job definitions, stable exact ACR, Hub/role IDs preserved.
Final curl health/source bytes pass and anonymous protections remain.
Native public Playwright trace and screenshots retained ignored/private;
direct result recovered from own session tool event, not handwritten literals.
Resident widget assets200/runtime/launcher/dialog present; desktop/narrow
overflow false. Resident initial unattributed resource404 and employee image CSP error remain
reported, no full clean-console/a11y/semantic acceptance. Entra sign-in reached,
no credentials used; authenticated chat/map/case acceptance owner-run.
Original critique unchanged; one current full-boundary Review is now eligible.
