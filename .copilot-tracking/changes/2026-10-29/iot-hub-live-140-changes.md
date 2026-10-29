---
title: Live IoT Hub implementation evidence
ms.date: 2026-10-29
---

Task 140-184 / iot-hub-live-140. Declared scope: full plan.
Plan `.copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md`.
Base fetched before work: ecbb5a80470292c885764c28d6833c0e5ef63dfa.
Original critique Revise retained; PC002-004 applied, unsupported PC001
temporary-file claim rejected in favor of explicit owner /tmp/mv direction.

## Intake and Research commands (read-only)

* `git status --short`, `git branch --show-current`, `git log -1`: clean topic
  feat/iot-hub-live-140 at latest main; no matching open PR.
* `gh issue view 140 --json title,body,state`, same for184 and137: read all.
* `git fetch origin main --quiet; git rev-parse origin/main`: base above.
* `az account show --query '{name:name,state:state}'`: enabled session.
* `az resource list -g ama --query '[].{name:name,type:type,location:location}'`:
  existing B1 hub and PE found; no dedicated Event Hubs namespace.
* `az containerapp list -g ama --query '[].{name:name,min:properties.template.scale.minReplicas}'`:
  four apps all0; job list query triggerType: eight allManual.
* `az resource show` exact hub with safe property projection: B1 capacity1,
  uksouth, two partitions, retention1, identityNone, publicDisabled,
  disableLocalAuth true, fallback enabled, one private endpoint.
* `az monitor diagnostic-settings list` projected logs/metrics: existing
  to-log-analytics enables Connections/DeviceIdentityOperations/Routes/
  Configurations; DeviceTelemetry off; AllMetrics on. Must disable all logs.
* `az containerapp job show` initializer image/command/env-name projection:
  proof image, args initialize. `job start --help`: execution override supported.
* `az role assignment list --scope <exact-hub> --include-inherited` role/type
  projection: operator Owner, no registry data grant observed. No grants made.
* Python current-user token captured in memory via
  `az account get-access-token --resource https://iothubs.azure.net`;
  HTTPS GET `/statistics/service?api-version=2021-04-12` returned401 with public
  disabled, not a conclusive network/role distinction. Token never emitted.
* `az monitor metrics list-definitions` projected telemetry names:
  ingress.success/allProtocol and egress success/fallback available.
* `az bicep version`: 0.48.1. Production module build --stdout redirected
  to /dev/null and lint: exit0, no warnings.
* /tmp/mv Python3.12.3, API/core distributions and SDKs installed; pyodbc
  metadata absent. Existing unrelated ama-350-feedback-sql left untouched.
  SQL2022 image available. `lslocks` showed no heavy-gate lock holder.
* Official Microsoft Entra documentation retrieved2026-10-29 confirms built-in
  receive requires shared key; no service-key workaround authorized or used.

## P01/P02 implementation

Added isolated existing-hub reconciliation profile and runtime SKU/unit guards.
Added DeviceActivation for bounded publishing; routed receiver explicitly rejects
it before credential construction. Existing routed activation/decode unchanged.
Five added focused test methods (two infra, three API), no removals.

### Relevant local admission before cloud mutation

* Missing installed import from /tmp/mv found; restored declared distributions:
  `/tmp/mv/bin/pip install --quiet -e 'src/core[sql]' -e src/agents -e src/api`,
  exit0. Correct driver is mssql-python, not pyodbc; no dependency added.
* Initial API Ruff E501 corrected by owning-project Ruff formatter; initial
  Bicep consumer group required properties.name warning corrected.
* `cd src/api; /tmp/mv/bin/ruff check .; ruff format --check .; mypy`:
  exit0, 58 formatted files, 110 source files type checked.
* Targeted API iot_stream and test lint/format/mypy: exit0, two files typed.
* API unittest `test_iot_stream test_sensor_ingestion -q` with caller PYTHONPATH:
  73 passed, 20.973seconds.
* Core unittest `test_sensor_stream test_resident_sensors -q`: 21 passed.
* Bicep build/lint both production module and isolated profile: exit0.
  `build-params` isolated profile: exit0.
* Infra IoT compiled semantic/mutation suite:16 passed; existing Bicep policy
  suite:54 passed (before guard extension; repeat final boundary later).
* Initial standalone what-if parser failed on nullable delta; Azure what-if
  itself succeeded. Corrected reader uses `delta or []`, no raw values emitted.
* Initial direct hub PUT what-if showed deletions of service-managed endpoint
  properties including privateEndpointConnections. Admission correctly refused;
  no apply. Narrowed to an `existing` hub and child writes, retaining all actual
  hub properties by construction. Existing hub SKU/unit verified by runtime
  minLength guards. Optional guard defaults leave main/production behavior intact.
* Latest isolated build/lint and16 semantic tests pass. Current what-if:
  api-consumer NoChange; to-log-analytics Modify logs/metrics only; every
  unrelated resource Ignore, hub not PUT. Exact existing child IDs match.
* Current-operator role lookup (OID from token in memory, role names only):
  only Owner inherited, no IoT Registry Contributor/Data Contributor.
  Do not self-grant, enable service SAS or temporarily expose hub for futile
  unauthorized registry access. No device/certificate generated.
* First disposable SQL readiness attempt failed (connection/environment setup);
  owned container removed in finally. Reused documented _Conn/connection_string,
  separate ZF_SQL_PORT, trust flag1 and bounded memory on second attempt:
  actual owned loopback SQL2022 responsive; `test_sensor_ingestion -q` with
  ZF_SENSOR_MSSQL=1:45 passed in19.831seconds; container removed in finally.
  This is actual local SQL, not live IoT-to-SQL.

## Validation and live outcomes

* `az deployment group create -g ama --name iot-live-140-private --parameters
  infra/iot-hub-live.bicepparam --mode Incremental --query
  properties.provisioningState`: Succeeded. Only admitted existing hub children.
* Post-apply diagnostic count query: enabledLogCount0, enabledMetricCount1.
  Hub B1/1/uksouth/private endpoint exact ID/identityNone/fallbacktrue/local
  authdisabled/publicDisabled/partitions2/retention1 all preserved.
* `az monitor metrics list --metric d2c.telemetry.ingress.success --aggregation
  Total --interval PT1M --offset 1h`, count-only query: all60 samples zero.
  No send was attempted and no live receive/SQL-write causality claimed.
* Existing Manual initializer execution-only template: safe env names and exact
  proof container verified; override command `python -c <counts-only code>`,
  existing image/env/identity/resources unchanged. Nonsecret transient JSON
  outside repository removed in finally. One start returned execution
  `job-cutover-test-init-tw2uy2m`, logs `{"sql_counts":"FAILED"}`.
  The probe used a fluent cursor assumption unsupported by the documented
  mssql-python _Conn pattern; fixed to separate execute/fetch. Failure remains
  original evidence, no counts inferred.
* Amend finite operator execution admission from one to maximum two to allow
  this explicit correction, not an automatic retry. Stop exact first execution
  before corrected start; each still has40second process deadline, no job
  template change, at most two existing platform attempts per execution.
  Conservative total bound2400 replica-seconds (<USD0.08 compute/memory scenario,
  within USD1 reserved shared/job allowance); no third attempt permitted.
* After first probe, live inventory still four apps min0 and eight jobs Manual.
* First execution reached Failed after exact stop; no longer running. Corrected
  second execution `job-cutover-test-init-1uyp2pt` also Failed, fixed sanitized
  evidence `phase=connect, kind=ConnectionStringParseError`. Thus the original
  suspected fluent-cursor issue was not the observed cause; no counts inferred.
* Local `inspect.signature(mssql_python.connect)` confirms `timeout: int=0`
  is a function argument; `Connection Timeout=10` was an unsupported connection
  string property in this driver. Remove that property and use `timeout=20`.
  This is concrete diagnosed correction, not a blind retry. Admit at most one
  final corrected execution (three total, six platform attempts maximum,
  conservative bound3600 replica-seconds/<USD0.12 compute scenario within
  USD1 reserved job/metrics). Never a fourth; preserve failures. Every process
  still self-terminates40seconds, trigger/template remain untouched.
* Final corrected execution `job-cutover-test-init-7lx886f` Succeeded:
  start2026-10-29T19:06:25Z, end19:06:59Z; log19:06:53Z reports
  sensor_reading, sensor_delivery and sensor_data_quality_exception each
  table_present=false/count0. These are absent tables, not existing empty
  tables. No consumer rows exist to claim. No DDL or row data read.
* SQL probe used the original initializer image/env/identity, only execution
  command changed. Query shape for each closed-list table:
  `IF OBJECT_ID(N'dbo.<table>',N'U') IS NULL SELECT 0,CAST(0 AS bigint)
  ELSE SELECT 1,COUNT_BIG(*) FROM dbo.<table>`. Separate cursor.execute/fetchone;
  mssql_python.connect(...,autocommit=True,timeout=20), MSI user-assigned identity
  from existing env, timer40seconds exits124 on overrun. No values/credentials
  were printed or persisted. Transient template JSON removed after every start.
* Post-apply what-if recheck still reports groupNoChange and diagnosticsModify
  from Azure-normalized log/metric arrays; no hub PUT or unrelated writes.
  Do not claim a byte-identical diagnostic what-if. Actual enable counts0/1
  were verified and no repeat apply was performed.
* Final API package Ruff/format/mypy exit0 (58 formatted files,110 typed);
  combined API/core relevant unittest94 passed20.858seconds. Final production
  and isolated build/lint/build-params exit0; existing infra policy54 passed,
  IoT16 passed including actual wrong-SKU/unit guard evaluation. Infra targeted
  Ruff/format and `git diff --check` pass. Local SQL45 passed as above.
* Final `az role assignment list --assignee <current-oid> --include-inherited
  --include-groups --scope <exact-hub> --query '[].roleDefinitionName'`:
  exit0, only Owner. This includes group-derived assignments, not just direct
  grants. Registry data authority not granted; no operator role added.
* Final exact owned execution list: twoFailed, oneSucceeded, no running test
  executions. All four apps min0; all eight jobs Manual. No resource group,
  SQL public access, app revision or job definition changed.

## Amendments and Divergences

Isolated entry point instead of deploying production module: necessary to avoid
unapproved Event Hub, endpoints, roles and budget-resource writes. Production
module remains validated and unchanged. Existing hub reused rather than new.
What-if refusal further narrows deployment to existing hub children, avoiding
all hub PUT/endpoint-attachment ambiguity. Public connectivity and device issue
are parked: existing operator lacks registry data authority and no new operator
role is permitted. No credentials to rotate or delete were created.

SQL admission update from actual config: initializer retry1, timeout600,
0.5CPU/1Gi. No template changes permitted. Bound one execution with at most
two platform attempts, each process self-terminating45seconds; conservative
platform upper bound1200 replica-seconds (<USD0.04 at ordinary consumption
rates before shared logging, reserved USD1). This is an existing retry, not an
operator rerun. Record/stop exact execution on1200second overrun. No automatic
retry by operator. This finite actual bound replaces the assumed retry0/300
prerequisite; plan current state updated accordingly.

## Remaining work and blockers

Implementation and bounded live/private-SQL inspection complete; live telemetry
itself parked on actual authorization/network/adapter/schema/revision gates.
No synthetic devices or credential files created; no cleanup of those required.
Two owned local SQL containers removed. Three owned cloud executions terminal,
first two Failed, third Succeeded; no persistent test resource created.
Four app minima0/eight Manual jobs verified at final boundary. Documentation includes cost/environment/ADR,
API contract, synthesis/index and append-only log.
Remaining lifecycle: original independent Review, local commit, complete gate
on committed exacthead if admitted; no push. Human approval stays unmet.

## Post-Review local lifecycle outcome

Original independent Review executed Complete, full live-delivery outcome
Not accepted. No substantive runtime/infra code defect found. Preserve RV001
live residuals, RV002 reviewer-specific filesystem claim, RV003 low historical/
current SQL-limit prose reconciliation and RV004 then-pending local lifecycle.
No source correction or repeated Review occurred. RV002 does not override the
parent's actual tools or the owner's explicit /tmp/mv instruction; no parent
temporary-file prohibition exists. RV003 is routed to later evidence cleanup,
not silently relabelled resolved. Original critique/Review remain unchanged.

Resolved GitHub identity with `gh api user`: login jmservera, id8036360.
Set repository-local name and privacy-safe author/committer address
`8036360+jmservera@users.noreply.github.com`.
Explicitly staged19 implementation/documentation/original RPI files and committed
`2115ac9f51a08f4b86d60e88ae2d72e1eda8a3f9`, message
`feat(iot): reconcile approved B1 hub and separate publisher activation`,
`Refs #140 #184`, required Copilot coauthor trailer. No push.

Fetched main again: ecbb5a80470292c885764c28d6833c0e5ef63dfa unchanged.
Actual heavy-lock lookup found no owner; nonqueued admission acquired.
Created a clean detached exact-head worktree outside the repository to avoid
development caches/egg-info as candidate inputs. Ran unchanged complete gate:

```bash
python3 tools/rpi-checks.py --all \
  --base ecbb5a80470292c885764c28d6833c0e5ef63dfa \
  --out /home/azureuser/.copilot/session-state/83204432-d5b6-46b3-b6df-63a5f308ead9/files/iot-full-gate-2115ac9f \
  --lock-timeout 0
```

Exit1, status failed,169 recorded commands. External original receipt:
`/home/azureuser/.copilot/session-state/83204432-d5b6-46b3-b6df-63a5f308ead9/files/iot-full-gate-2115ac9f/receipt.json`.
Receipt binds head2115ac9f/baseecbb5a80, full scope.
Completed groups: preflight, core, agents, orchestrator, importer, namespace,
static, infra, migration, four image contracts and logo0600. API general
discovery command itself exit0,1332 tests in509.724seconds,318 skips.
The runner rejects unexpected required integration/dependency skips, including
50 assistant SQL skips labelled `needs disposable SQL Server (ZF_TEST_MSSQL=1)`
and other opt-in SQL/browser skips. Its API group therefore fails; browser and
full mssql groups are blocked by prerequisite. This is not a full pass and does
not replace the separately successful targeted actual local SQL45 evidence.
Do not add a skip token, relax policy or fix unrelated runner/discovery code
inside this completed task. Route gate admission separately.

Explicit failed-receipt verification command, with the same base:
`python3 tools/rpi-checks.py --verify-receipt <external-receipt> --base <base>`
returned exit1, `BLOCKED: Receipt does not establish an eligible run`, as expected.
No publication evidence is claimed. Final lifecycle-evidence-only commit
necessarily changes HEAD; the failed2115ac9f receipt remains historical, not a
receipt for that later commit. A future publication requires a new complete
gate after fixing the routed admission issue and obtaining remaining approvals.

Gate-owned running containers remaining0. Both directly owned local SQL
containers removed, three cloud test executions terminal, no device credentials
or identities created, no persistent cloud test resources needing deletion.
Preserve failed gate receipt/logs and gate verification images under retention
policy; remove only the known supplementary clean exact-head worktree and
transient session probe scripts/template/execution-name scratch after use.
No original evidence, foreign resource, score file or remote branch changed.

Final bounded result: existing hub reconciled, source activation separation
delivered, required focused checks passed; live sensor-to-resident flow blocked.
USD10/month baseline hub/<=USD0.97 three-day attribution is an estimate, not
actual invoice. No new fixed paid resource or ongoing simulator was introduced.
Manual full-loop session ends blocked on owner/live and publication gates,
with no automatic child work.
