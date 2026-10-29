<!-- markdownlint-disable-file -->
# Research: live IoT Hub exercise, Refs #140 #184

## Research Brief

Date: 2026-10-29. Identity: 140-184 / iot-hub-live-140.
Prepare a bounded, owner-approved B1/one-unit hub deployment and synthetic
device-to-consumer-to-SQL proof, with visible resident sensor view as the goal.
Audience: owner and implementation/review. Output: convergence for planning.
Evidence root: `.copilot-tracking/research/2026-10-29/`.

## Research Parameters and Direction Controls

Focused posture, selected because caller supplied exact code paths, issues and
deployment limits. USD5 incremental through 2026-10-31, ama/uksouth only.
No new Event Hub, private endpoints, broad RBAC, app revisions, public SQL,
real devices, private datasets, .env, source/log credentials or remote writes.
Keep apps min replicas zero and all eight jobs Manual. Local commit only.
Credential owner may be recovered from repository evidence; transient local
credentials outside the repository must be deleted.

## Extension Registry and Participation

Repository instructions and RPI phase contracts selected. No web changes planned,
so visual/a11y skills not applicable. Research specialist delegation skipped:
the hub/adapter/auth constraints form one continuous trace best handled inline.
No interaction required: explicit scope and safe parking directions are supplied.
Read original specification, addendum, reference index and owner memory.
Memory is context, not deployment authority.

## Questions and Prior Knowledge Gate

1. Can the existing module deploy only the approved hub, without other resources?
2. Can the existing consumer use the built-in endpoint without new paid services?
3. What cloud/local paths can prove ingestion without a new revision or SQL exposure?
4. What cost, identity lifecycle and validation evidence must remain open?

## Research Cycle 1

### Wider (opening)

Inspect module/main parameter contracts, ADR decision 6, simulator/consumer,
tests, deployment helpers, existing resource inventory and read-only job profiles.
Owner-supplied paid-hub approval supersedes only the dated source-only prohibition.

### Evidence Log

* C1: `infra/modules/iothub.bicep:52`: existing module creates a paid Standard
  Event Hub, two private endpoints, roles and budget, not only the approved hub.
* C2: `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:47`: built-in
  endpoint needs shared service-key authentication; keyless production adapter is
  the dedicated Event Hub. No authority to create that adapter in this task.
* C3: `infra/README.md:3210`: Juan Manuel Servera is recorded exercise credential
  issue/rotation/revocation owner; individual synthetic device identities selected.
* C4: `src/api/src/zava_forward/api/iot_stream.py:29`: existing activation requires
  dedicated namespace, routed endpoint and X.509-only device authentication.

### Wider reflection

The existing production graph cannot be deployed unchanged within the owner's
hub-only limit. Investigate an explicit isolated exercise profile, retaining
private/keyless production defaults and clearly distinguishing interim auth.

### Deeper

* C5: live read-only inventory (`az resource list -g ama`, 2026-10-29)
  already contains `iot-cutover-test-rzsrg`, B1/one unit/uksouth, two partitions,
  one-day retention, private endpoint, public Disabled, local auth disabled.
  Reuse it; creating a second hub would violate one-hub/minimum-cost intent.
* C6: live diagnostics currently enable Connections/DeviceIdentityOperations;
  source metrics-only protection has not reached Azure. Fix the existing
  diagnostic setting before issuing any synthetic identity.
* C7: all four apps min replicas 0; all eight jobs Manual. Existing initializer
  is a proof image with `initialize` args, not an installed current consumer.
  Execution command override is available; no persistent job update is needed
  for counts-only SQL inspection.
* C8: current authenticated user's inherited roles include Owner, but no
  IoT Registry Contributor/Data Contributor. Keyless statistics probe returned
  HTTP401 with public access disabled; this does not distinguish network from
  data authorization. No role grant is authorized for the operator.
* C9: `src/core/tests/sensor_consumer_fixture.py:67` selects real local SQL
  through `ZF_SENSOR_MSSQL=1`; existing tests already support constructed SQL
  proof without reading private data.
* C10: `src/api/src/zava_forward/api/iot_stream.py:319` couples publisher
  activation to routed consumer readiness unnecessarily. Device publishing
  needs its own explicit finite approval, not a fictional Event Hub assertion.

Deeper reflection: preserve production module and receiver, add a standalone
hub-only entry point matching the existing resource. Keep local/service auth
disabled, existing private endpoint intact, public access only as an explicit
bounded development opt-in if needed. If registry authorization fails, park
devices rather than mint service policies or self-grant.

### Contrarian

W1: https://learn.microsoft.com/en-us/azure/iot-hub/authenticate-authorize-azure-ad
(retrieved 2026-10-29), "Permissions for IoT Hub service APIs": built-in
Event Hubs-compatible endpoint needs shared-key connection-string auth. Entra
receive requires a custom Event Hub. Owner-only ARM access does not imply
registry data access. This confirms that enabling an arbitrary Data Receiver
role on the hub is not a consumer solution.

Rejected: deploy unchanged production module (unapproved paid resources and
endpoints); enable service SAS or use iothubowner keys (weakens current auth
without separate direction); self-grant registry roles (explicitly forbidden);
claim local/fake transport is live end-to-end (false); create another hub
(existing B1 already meets size/scope). Cloud resident visibility may also
require a separately approved application revision and SQL projection update.

Contrarian reflection: safe progress is hub reconciliation, a bounded X.509
publisher attempt using existing operator authority only, and actual local SQL
proof when cloud transport is blocked. Do not promise live rows/gauges without
observing them.

## Findings, Alternatives and Decision State

Selected approach: isolated hub-only Bicep entry point and explicit device-only
publisher activation; no change to default private/keyless routed module.
Use temporary self-signed per-device X.509 credentials with mode0600 outside
the repository, delete run-owned identity and files on exit, and emit counts
only. Probe existing registry authority; missing authority is a blocker, not
permission to grant it. Existing credential owner is Juan Manuel Servera (C3).
Counts-only in-VNet SQL inspection and local SQL tests remain useful even if
live proof cannot proceed. Preserve explicit unmet #140/#184 criteria.

Cost: existing hub means no new fixed hub charge versus inspected baseline.
Public list-price B1 USD10/month is supplied owner cost-check evidence and
matches the 2026-10-27 budget entry. Conservative three-day attribution at
10/31*3 = USD0.97 through October31, excluding small shared metric/job usage;
reserve the rest of USD5, no extra paid transport infrastructure. No new Azure
budget resource is permitted by hub-only direction. A budget estimate is not
an enforced spending stop.

Stop research after one complete focused cycle: material alternatives and
authorization gaps are identified; implementation can expose the exact safe
boundary without broader discovery. Required human/operational review remains
unmet.

## Readiness

Research disposition: executed. Planning Readiness: Ready for bounded delivery
with conditional live proof; not ready for unrestricted cloud consumption.
Self-check: three waves in order, stable C/W evidence, alternatives and actual
unknowns preserved. No source/cloud mutation in Research.
