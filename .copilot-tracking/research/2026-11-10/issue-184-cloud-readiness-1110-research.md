<!-- markdownlint-disable-file -->
# Issue 184 IoT demo deployment-readiness metadata slice: research (2026-11-10, Refs #184 #440)

Original research for task `issue-184-cloud-readiness-1110`. It is separate from, and does not rewrite, any earlier issue 184 research, plan, review or handoff. Research disposition: `executed`, in two parts: Part A repository identity and boundaries (written before `research-open`), Part B dated ARM configuration observations (appended after `research-open`, no earlier text changed).

## Task and boundary

* Slice: read-only, current Azure Resource Manager (ARM) configuration observations of the already declared development IoT Hub, the demo API app and the two already named demo job identities, so that a later live-transport or deployment admission has current real metadata. It is not a source correction, a renewed budget, or an inference, transport or deployment campaign.
* Child simulator, consumer and receiver source is already merged (PR 1304 recovery, PR 1088 simulator container, PR 508 consumer, PR 557 hub, among others). No source is duplicated or repaired here.
* Parent context: #184 (feature, `Not started` wording in its body is historical; criteria 1 and 3 stay open, criterion 2 is ticked), #110 consumer, #140 hub, #440 recurring checkpoint. All four whole-issue criteria sets stay OPEN. No issue, board or PR remote write.
* Linked current #440 sensor checkpoint: [Sensor-review wave actual-main checkpoint (2026-11-10, Refs #440 #109 #111 #184 #1288)](../../../docs/architecture/cutover-evidence-pack.md#sensor-review-wave-actual-main-checkpoint-2026-11-10-refs-440-109-111-184-1288), recorded on `main` by commit `0da7b8573` (PR 1412). It is local-only and qualified, and it records no Azure observation. This slice adds the missing Azure configuration dimension without altering it.

## Part A: repository identity facts (read from `4d8443d44`, tree `d1f46e82fa63`)

| Fact | Source | Class |
| --- | --- | --- |
| Approved project resource group `ama`; demo app `ca-cutover-test-demo-api` | task brief; [`infra/resident-demo.bicep`](../../../infra/resident-demo.bicep) scope guard; [`src/api/README.md`](../../../src/api/README.md) 2026-10-27 inspection | Owner-approved identity, repository-declared |
| Existing development hub `iot-cutover-test-rzsrg`, `uksouth`, `B1` x 1 unit | [`infra/iot-hub-live.bicepparam`](../../../infra/iot-hub-live.bicepparam) (`name`, `location`, `skuName`, `unitCount`) | Declared parameters, not an observation |
| Hub cost scope in that file ended 2026-10-31 (<= USD1 attributed, within USD5 additional) | same file comment; [`infra/README.md`](../../../infra/README.md) "Bounded existing-hub exercise (2026-10-29)" | Expired scope: metadata reads do not renew it |
| Exact simulator job name `job-live-simulator` (Schedule, `*/5 * * * *`, replicaTimeout 240, retry 0, parallelism 1, user-assigned identity) | `jobName` in [`infra/live-simulator-job.bicep`](../../../infra/live-simulator-job.bicep) | Authored and compiled only, "NOT deployed" per its header and `infra/README.md` |
| Exact receiver (consumer) job name `job-live-receiver` (Manual, replicaTimeout `windowSeconds + 120`, retry 0, `ZF_SIM_ROUTING_READY` defaults `0`) | `jobName` in [`infra/live-receiver-job.bicep`](../../../infra/live-receiver-job.bicep) | Authored and compiled only |
| Existing environment `cae-cutover-test-demo`; an existing private registry; images must be digest-pinned | both job templates | Declared |
| Earlier live exercise (2026-10-29): hub already B1/1 unit, two partitions, one-day retention, identity None, local auth disabled, public network Disabled, built-in `api-consumer` group, metrics-only diagnostics; live device issue/send parked | `infra/README.md` "Bounded existing-hub exercise" | Historical dated observation, not current |
| 2026-11-08 source handoff: "current job inventory has only Manual jobs, so nothing sends today"; nothing executed | `infra/README.md` "Finite demo deployment plan" | Historical, unnamed inventory |
| [`infra/main.test.bicepparam`](../../../infra/main.test.bicepparam) test profile | repository | Placeholder: NOT used as resource identity or authority |

The two job names are explicit, unique and unambiguous in the project references, so their subqueries are admitted; no other job, resource or name is queried or searched. If ARM reports a job as not found, that is one dated observation about that exact name, not a general statement about other jobs.

## Part A: evidence boundaries applied to every later statement

* A resource that exists does not show ingestion works. A configured image or tag is not an immutable build or proven runtime. A schedule is not an execution. The hub existing is not a current authorized transport budget (scope ended 2026-10-31, not renewed). Local fixtures, fake networks and constructed SQLite are not Azure acceptance.
* Unknown, denied, throttled or unreadable is never recorded as absent or zero.
* Earlier history stays: the spent source cycle (PR 1304 and the local handoffs `handoff-184-type-prerequisite.md`, `handoff-184-postpolicy.md`, `handoff-184-current-main-validation.md`, all LOCAL, not independently reviewed) and the qualified #440 sensor witness chains (publication HOLD) are neither repaired nor re-asserted.

## Part A: query design (fixed before `research-open`)

At most eight existing-authenticated Azure CLI metadata invocations in total, including at most one transient read retry. Every command sets `AZURE_EXTENSION_USE_DYNAMIC_INSTALL=no`, uses core `az resource show` with `--query` projections only, and writes only its projected JSON, exit code and UTC time to the external Root evidence folder `evidence-184-cloud-readiness-1110`. No login, extension or tool install, config change, `az resource list`, `az role`, `az monitor`, secret or key command.

| Q | Target (exact) | Projected fields only |
| --- | --- | --- |
| Q1 | Hub `iot-cutover-test-rzsrg` in `ama` (`Microsoft.Devices/IotHubs`) | location, sku name/tier/capacity, state, provisioningState, identity type, publicNetworkAccess, disableLocalAuth, events partitionCount and retention days, routes count, fallbackRoute enabled flag, private endpoint connection count. No endpoint strings, authorization policies or keys |
| Q2 | Hub built-in consumer group `api-consumer` (child of the same hub) | existence, provisioningState-level fields only |
| Q3 | App `ca-cutover-test-demo-api` in `ama` (`Microsoft.App/containerApps`) | location, provisioningState, runningStatus, latestReadyRevisionName, identity type, container names and images, ingress transport, value of the single non-secret flag `ZF_SENSOR_REVIEW_DRAFTS` |
| Q4 | Job `job-live-simulator` in `ama` (`Microsoft.App/jobs`) | existence, provisioningState, triggerType, cron, replicaTimeout, retryLimit, parallelism, identity type, container name and image, count (not value) of the `ZF_SIM_APPROVAL` env entry |
| Q5 | Job `job-live-receiver` in `ama` | existence, provisioningState, triggerType, replicaTimeout, retryLimit, parallelism, identity type, container name and image, value of `ZF_SIM_ROUTING_READY` |
| Q6 to Q8 | Reserve: at most one transient read retry of a failed Q1 to Q5 query (identical command). Not used for any new target | none |

If Q2's child-type syntax is rejected without a transient cause, Q2 stops and its field set is recorded Unknown; it is not retried with a guessed variant beyond the single retry in the budget.

## Planning readiness (Part A)

Ready: scope, identities, boundaries, budget and output rules are bounded. Part B appends the observations after `research-open`.

## Part B: dated ARM configuration observations (2026-11-10, 17:54Z to 17:55Z)

Appended after `research-open` (witness seq 2). Five of eight Azure CLI metadata invocations were used; zero retries; three left unspent. Every command used `AZURE_EXTENSION_USE_DYNAMIC_INSTALL=no`, core `az resource show` with a `--query` projection, and the existing authenticated context (no login, install or config change). Raw minimal outputs, stderr and per-attempt timings are in the external Root folder `38e61c82-3c44-4b97-af59-9eed5c151ac7/files/evidence-184-cloud-readiness-1110/` (`Qn.attemptN.out|err|meta`). No subscription id, principal id, endpoint or secret is recorded here.

| Q | Target | Exit | Observed configuration (ARM, at the stated time) | Unknown or not shown |
| --- | --- | --- | --- | --- |
| Q1 17:54:17Z | Hub `iot-cutover-test-rzsrg`, `ama` | 0 | location `uksouth`; SKU `B1`, tier `Basic`, capacity 1; state `Active`; provisioningState `Succeeded`; identity type `None`; publicNetworkAccess `Disabled`; disableLocalAuth `true`; built-in events endpoint 2 partitions, 1 day retention; custom routes 0; fallback route enabled `true`; private endpoint connections 1 | Whether any device is registered, any message is flowing or any receiver is attached; current usage, quota and spend; whether the private route is reachable from the API or a job; approval or budget |
| Q2 17:54:23Z | Consumer group `api-consumer` on the hub built-in events endpoint | 0 | Present (name and type returned) | Whether anything reads from it; the receiver's data-plane authorization (Entra receive on this tier needs a shared service key per the 2026-10-29 note, and service SAS is disabled) |
| Q3 17:54:29Z | App `ca-cutover-test-demo-api`, `ama` | 0 | location `UK South`; provisioningState `Succeeded`; runningStatus `Running`; latest ready revision `--0000027`; identity type `UserAssigned`; one container `api`, image reference from the existing private registry pinned by digest `sha256:1605ca20f...bcca0f64` (abbreviated; registry host omitted); ingress transport `Http`; the container env list contains no entry named `ZF_SENSOR_REVIEW_DRAFTS` (projection `containers[].env[?name==...].value` returned `[[]]`, i.e. an env list with no matching name; this is the only env projection and no other env name or value was read) | Which source commit built that digest; whether the revision serves live sensor data; SQL sensor schema and rows; the app's Entra and RBAC reach to any hub |
| Q4 17:54:35Z | Job `job-live-simulator`, `ama` | 3 | ARM `ResourceNotFound` for that exact name and type in `ama` | Whether some other differently named job exists (not enumerated, by design); not retried because it is not transient |
| Q5 17:54:40Z | Job `job-live-receiver`, `ama` | 3 | ARM `ResourceNotFound` for that exact name and type in `ama` | same as Q4 |

### Interpretation (bounded)

* The hub, its consumer group and the demo API app exist and are configured as above at the observation time. For the fields both observations record (SKU and capacity, partitions, one-day retention, identity `None`, local auth disabled, public network `Disabled`, a fallback route and a private attachment), the values equal the 2026-10-29 dated record in `infra/README.md`; this slice adds only the exact custom-route count (0) and private endpoint connection count (1). A configuration match is not proof the private path works.
* The two Bicep-declared job names, which the repository describes as "authored and compiled only, not deployed", were not found under those exact names at 17:54Z. This is consistent with that description and means the simulator and receiver jobs as authored are not deployed. It says nothing about the Manual jobs mentioned in the 2026-11-08 handoff, whose names are not recorded in the repository and were deliberately not searched.
* So the two jobs as authored are not deployed under those exact names: no scheduled simulator and no receiver job exists under the declared names. Nothing here establishes that no other resource or job (including the unnamed Manual jobs the 2026-11-08 handoff mentions, historical and unverified here) can send or receive. No execution, ingestion, UI or quality success is implied by any resource existing.
* The API image is referenced by digest, which is immutable as a reference, but its source commit and runtime content are unproven by this slice.
* The hub being `Active` and B1 does not renew the expired 2026-10-31 cost scope; transport remains unauthorized until a fresh finite approval exists.

### Gaps for any later admission (unchanged Unknown)

Device registrations and certificates, hub-to-sensor-readings route and receiver identity grants, SQL table existence and grants, image build provenance, current usage and budget alert, and the identity of any other existing jobs. Each needs a separate, explicitly authorized observation.

### Planning readiness

Ready. Research disposition `executed`. Part B satisfies the "current real resource/config metadata" input; further Azure queries are not needed for the plan.
