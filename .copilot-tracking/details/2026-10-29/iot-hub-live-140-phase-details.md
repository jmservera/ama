---
title: Live IoT Hub phase details
ms.date: 2026-10-29
---

Task 140-184 / iot-hub-live-140. Authoritative plan:
`.copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md`.

<!-- P01 -->
## P01: Hub-only deployment boundary

Current-state amendment after refused direct-PUT what-if: use existing hub only,
no hub creation/update, preserve every service-owned property/attachment. Actual
B1/one-unit/location checks guard child writes. Production module unchanged.

<!-- P01-T01 -->
### P01-T01

Use an isolated `infra/iot-hub-live.bicep` and explicit `.bicepparam`, not main.
Existing `infra/modules/iothub.bicep` already has consumer, metrics, B1 constraints
and keyless outputs; unchanged production graph is intentionally not deployable
under current hub-only authority. The isolated graph references one B1 hub, built-in
api-consumer group, metrics-only diagnostic and empty scope-check deployment.
No authorizationPolicies, role assignment, new private endpoint, budget resource,
custom namespace or key output. Preserve existing hub name, tags and network
state. Compile and enumerate the actual graph in tests; no hub PUT or networking
parameter exists in this narrowed reconciliation profile.

<!-- P01-T02 -->
### P01-T02

Record baseline before mutation: hub SKU/auth/routing/private endpoint count,
four app minima and eight Manual triggers. What-if Incremental in ama, inspect
only nonsecret change summaries. Stop if deletion or resource outside exact
hub/children is proposed. Deploy with output query limited to provisioningState,
then verify actual properties/metrics-only setting and original PE count.
Never deploy `main.bicep` or the whole production module in this live action.
Admission dependency: P02-T01 implementation and all relevant local tests/static
checks must pass before P01-T02 apply. Pin exact existing hub/child IDs, reject
hub Create/Delete/replacement or unknown property drift. Preserve exact PE
attachment IDs, identity, routing/fallback, TLS, tags and partition/retention;
enumerate explicit device/module flags and diagnostics/group reconciliation.
Each apply has <=600seconds operator wait, no blind retry; record any uncertain
deployment and inspect status before any later action.

<!-- P02 -->
## P02: Bounded publisher and runtime proof

Actual authority update: current operator only Owner, no registry data grant.
Do not expose hub or attempt identity issuance under absent authority; park
live proof. No credential files/identities created. Local SQL45 tests passed.
Actual initializer retry1/timeout600 retained; maximum three operator starts
after diagnosed probe corrections, at most six platform attempts/3600seconds
conservative bound, each process has40second self-exit. Third Succeeded,
all three sensor tables absent/count0. No fourth attempt; no persistent writes.

<!-- P02-T01 -->
### P02-T01

Introduce explicit device-only activation carrying hostname, approval reference,
ama scope; no invented Event Hub assertion. HubPublisher accepts it or existing
Activation. HubReceiver remains routed-only and rejects device-only activation.
Test malformed host, missing approval, wrong group, compatibility and refusal.
Do not weaken decode X.509-only or SQL consent/calibration/identity checks.

<!-- P02-T02 -->
### P02-T02

Conditional procedure, not executed on observed absent registry authority:
generate one short-lived self-signed X.509 cert/key in a temporary outside-repo
directory, owner-only permissions; issue via existing operator Entra token in
memory only. First inspect exact synthetic device absence; do not overwrite
any existing identity. On 401/403 stop, record authorization failure and cleanup;
no role grant or policy-key route. If created, send at most two canonical replay
messages through HubPublisher, speed/rate/time budget enforced. Compare hub
ingress metrics counts after expected metric lag. Delete only owned identity,
remove files, restore original public access even on failure. If deletion or
restore fails, surface exact outstanding resource and block completion.
One lookup/create/delete each with <=20seconds HTTP timeout; no blind retries.
At most three metric queries within180seconds, no background polling. Apply
plan PC004 USD1 hub/USD1 shared job-metric/USD3 contingency reservation and
October31 23:59:59Z new-activity cutoff; no schedule or persistent simulator.

<!-- P02-T03 -->
### P02-T03

Use existing initializer image/environment/identity and an execution-only
python command importing installed mssql_python to query COUNT_BIG on sensor_reading
if it exists. No seed loads, DDL, row reads or job-definition changes. Record
table availability/count only and job completion; no cloud consumer revision.
For local proof create a labelled disposable SQL2022 container with random
loopback port, generated password in process memory/env only; never use the
unrelated existing shared SQL container. Run existing constructed sensor/API
tests with ZF_SENSOR_MSSQL=1 against only that container. Remove owned container.
Live-to-local transport remains blocked if no approved receive path; report it.
Cloud admission depends on successful local SQL proof. Actual immutable job
retry1/timeout600 gives max1200seconds per execution. Three bounded starts
maximum after diagnosed corrections; every process self-terminates40seconds
and final login timeout is20 via connect keyword (unsupported connection-string
timeout property removed). Stop only exact owned execution on overrun and
verify terminal status. All three are terminal; third Succeeded. No cloud
schema/row mutation or real dataset read.

<!-- P03 -->
## P03: Documentation and handoff

<!-- P03-T01 -->
### P03-T01

Append dated ADR authorization/cost boundary, retain historical source-only
decision. Infra guide describes separate profile, existing-hub reuse, exact
credential owner, explicit auth blocker, cost/time window and stop condition.
Update index and append KB log; do not update owner memory or original case.

<!-- P03-T02 -->
### P03-T02

Use /tmp/mv, install current project distributions only if required dependency
failure or manifest change. API PYTHONPATH:
src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Run Ruff, format --check, mypy and relevant unittest in owning projects.
Run compiled infra tests. Keep all original failures and corrections in changes.
One independent original post-implementation Review; route findings to later
work rather than rerunning Review. Resolve GitHub account and local noreply
author/committer; commit all implementation/original RPI evidence with trailer.
Then run complete local gate against fetched reviewed-main into a new external
directory with nonqueued lock admission. Never publish on failed/unavailable gate;
no push is requested in any case.
