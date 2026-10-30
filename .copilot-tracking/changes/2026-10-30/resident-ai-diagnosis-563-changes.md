<!-- markdownlint-disable-file -->
---
title: Resident AI fallback diagnosis and coordinator handoff
description: Confirmed rollback explanation and blocked enabled-runtime root cause, Refs #563
ms.date: 2026-10-30
---

# RPI Changes: Resident AI diagnosis

## Metadata

* Task ID: 563
* Task slug: resident-ai-diagnosis-563
* Related plan: .copilot-tracking/plans/2026-10-30/resident-ai-diagnosis-563-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/resident-ai-diagnosis-563-phase-details.md
* Research: .copilot-tracking/research/2026-10-30/resident-ai-diagnosis-563-research.md
* Implementation date: 2026-10-30
* Branch: ops/resident-ai-diagnosis-563
* Starting base: d934478fa4b877a17f83773a7f9eb7c2bd37b218

## Execution Status

* Status: P01 evidence packaging and requested local validation complete; exact enabled-runtime diagnosis Blocked.
* Declared scope: full bounded evidence-only plan, not an activation or unproved fix.
* Completed: P01/P01-T01 report and coordinator handoff, P01-T02 local validation.
* Completed additionally: P02-T01 one independent Review.
* Remaining: P02-T02 local commit.
* No source/doc cause was proved. No runtime source, regression test or cloud configuration was changed.

## Execution Summary

The current disabled label has a proved explanation: the prior executor removed
both AI settings during mandatory rollback after a genuine enabled-advisor
fallback. The failed enabled revision already had the correct names and values.
There is no evidence-based corrective environment change to provide.

The exact cause of that enabled attempt is NOT established. SQL reservation
failure or denial, managed-identity acquisition, transport/timeout, response
parsing/validation and expiry/limits share one fallback label and log marker.
The stopped enabled pod is unavailable; historical Log Analytics access is
network-perimeter denied and App Insights access is denied. These are diagnosis
access failures, not evidence that the resident application's identity lacks
model permissions. Unknown model dispatch/completion/spend remains unknown.

## Completed Work

### P01-T01: Incident Timeline and Causal Boundary

| Time UTC on 2026-10-30 | Observation | Source |
|---|---|---|
| Before activation | Consented disabled request returns "Summary by rules - AI is not enabled" | Merged owner-enable changes and sibling timeout-recovery changes |
| 18:06:57 | Enabled revision recover-ai-180649 created; retained management metadata shows both correct AI settings, existing MSI/client, same image; Healthy/Provisioned | Research W1 |
| 18:08:05.952 | Fresh login HTTP 200 after revision readiness/warm | Sibling timeout-recovery changes |
| 18:08:08.071 | Own-case HTTP 200, content visible | Same |
| 18:08:10.050-18:08:13.965 | Consented synthetic pest question dispatched and HTTP 200 returned "Summary by rules - AI unavailable or usage limit reached", not AI-generated | Same, research C5 |
| After failed proof | Both optional settings removed; recover-safe-180814 ready/100%; original effective configuration restored | Same; current management metadata W7 corroborates |
| This diagnosis | Current latest=ready recover-safe-180814; both AI names absent, min0/max1 and digest unchanged | W7 |

Source branch factories read `ZF_DEMO_ASSISTANT_ENABLED` and
`ZF_DEMO_ASSISTANT_ENDPOINT`; the disabled-label branch runs only when the
advisor is absent. The unavailable label is produced inside the enabled
advisor's failure handler. These labels must not be conflated.

### Verified Configuration, Not a Proposed Correction

The retained failed revision already contained all of these non-secret values:

```text
ZF_DEMO_ASSISTANT_ENABLED=true
ZF_DEMO_ASSISTANT_ENDPOINT=https://aoai-resident-469.openai.azure.com
ZF_SQL_AUTH=msi
ZF_SQL_CLIENT_ID=ba252cc4-6059-4248-9f21-f6ae7f0cd4d1
```

Runtime hardcodes deployment `resident-mini` and API version `2024-10-21`.
Azure deployment show confirms `resident-mini`, Succeeded,
`gpt-4.1-mini` version `2025-04-14`, Standard capacity 1.
The endpoint returned by the account matches, allowing its trailing slash.
The resident identity's principal has account-scoped Cognitive Services OpenAI
User, created 2026-10-27T10:42:13Z. No developer/key credential chain is used.
The employee agent worker's configuration is a different path, not a resident
enablement fix.

Do NOT reapply these settings as a "correction": that simply repeats the
configuration that failed verification. Current absence is the safe rollback.
Do not add an unrecognized deployment variable, alter IAM, extend expiry,
increase timeouts, bypass reservation or open networking based on this evidence.

### Candidate Cause Assessment

| Candidate | Finding | Evidence / limitation |
|---|---|---|
| Config name mismatch | Contradicted for enabled attempt | Runtime names exactly match retained revision; enabled unavailable label observed |
| Role propagation | No supporting evidence | Account-only role is three days old; actual token result remains unknown |
| Endpoint/deployment name | No name mismatch | Source and Azure metadata match; successful transport not proved |
| Code fault | No causal defect established | Existing generated-answer regression passes; deployed source/image equivalence not attested |
| Cold start | Earlier issue, not an explanation of the demonstrated enabled fallback | Later ready/warmed revision, fresh login and own-case success preceded 3.915s assistant response |
| Payload size | Not reproduced for observed synthetic question | Public stage probe: 1920-1976 bytes, limit 4096 |
| SQL admission/cap/rate/permissions | Unresolved | Reservation happens before token/HTTP; no SQL result available; no SQL read attempted |
| Identity/HTTP/timeout/output validation | Unresolved | Generic source fallback and denied historical telemetry cannot distinguish stages |

The source's 5-second transport timeout does not explain a 3.915-second end-to-end
reply on its own; no transport dispatch or timeout was observed. Do not treat
elapsed wall time, a healthy revision or a correct role assignment as model
success/failure evidence.

## Read-Only Azure Command/Result Record

All commands used RG ama, an ama resource ID, or the discovered ama workspace.
No Azure command with write semantics, site request, sign-in, model call, SQL
connection, credential file or secret retrieval occurred in this diagnosis.
The metadata projections intentionally exclude secret-reference values,
credential settings and arbitrary environment values.

Commands used `--only-show-errors -o json` unless indicated otherwise.

| Command | Actual result |
|---|---|
| `az containerapp show -g ama -n ca-resident-demo --query <identity/revision/traffic/image/envNames/scale projection>` | Exit 0; current disabled rollback state as above |
| `az containerapp revision show -g ama -n ca-resident-demo --revision ca-resident-demo--recover-ai-180649 --query <name/time/state/image/four-safe-env-values/scale projection>` | Exit 0; enabled correct configuration, now inactive/stopped |
| `az cognitiveservices account deployment show -g ama -n aoai-resident-469 --deployment-name resident-mini --query '{name:name,state:properties.provisioningState,model:properties.model,sku:sku}'` | Exit 0; Succeeded matching deployment |
| `az role assignment list --assignee-object-id ab308885-7010-41b8-8b70-9ef5eabe40d0 --scope /subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aoai-resident-469 --query '[].{role:roleDefinitionName,scope:scope,created:createdOn,updated:updatedOn}'` | Exit 0; account-only expected role, creation date above |
| `az monitor app-insights component list -g ama` with safe projection | Exit 2; unsupported command, corrected below |
| `az monitor app-insights component show -g ama --query '[].{name:name,appId:appId,workspace:workspaceResourceId}'` | Exit 0; appi-cutover-test, no keys queried |
| `az monitor log-analytics workspace list -g ama --query '[].{name:name,customerId:customerId}'` | Exit 0; log-cutover-test, workspace 3f6f76f1-9d76-413d-bc86-bcbc92fce2be |
| `az containerapp show -g ama -n ca-resident-demo --query properties.environmentId -o tsv` | Exit 0; cae-cutover-test-demo in ama |
| `az containerapp env show -g ama -n cae-cutover-test-demo --query '{name:name,destination:properties.appLogsConfiguration.destination,workspaceCustomerId:properties.appLogsConfiguration.logAnalyticsConfiguration.customerId}'` | Exit 0; azure-monitor destination |
| `az cognitiveservices account show -g ama -n aoai-resident-469 --query '{name:name,endpoint:properties.endpoint,disableLocalAuth:properties.disableLocalAuth,publicNetworkAccess:properties.publicNetworkAccess}'` | Exit 0; matching endpoint, local keys disabled, public model networking Enabled |
| `az monitor log-analytics query --workspace 3f6f76f1-9d76-413d-bc86-bcbc92fce2be --analytics-query <bounded classified aggregate query> --timespan 1d` | Exit 1; InsufficientAccessError / NspValidationFailedError; no rows retrieved |
| `az monitor app-insights query --app ebe710dc-ee27-493e-af25-b694a53a1e13 --resource-group ama --analytics-query <bounded aggregate> --offset 1d` | Exit 3; ID interpreted as resource name; corrected below |
| Same aggregate with `--app appi-cutover-test --resource-group ama` | Exit 1; InsufficientAccessError, no rows retrieved |
| `az containerapp logs show -g ama -n ca-resident-demo --type system --tail 300 --only-show-errors` | Exit 0; three envelopes, no historical failure marker recovered |
| `az containerapp logs show -g ama -n ca-resident-demo --type console --tail 300 --revision ca-resident-demo--recover-ai-180649 --only-show-errors` | Exit 3; no replica, zero recovered rows |

The log commands were executed by external session helper
files/resident_diagnostic_logs.py, which emits only fixed marker counts,
command argv and exit status; raw messages never enter this record.
No access workaround or network/permission change was attempted after denial.

The failed Log Analytics query was:

```kusto
ContainerAppConsoleLogs_CL
| where TimeGenerated between (datetime(2026-10-30T18:06:30Z) .. datetime(2026-10-30T18:10:00Z))
| where ContainerAppName_s == 'ca-resident-demo'
| extend event=case(
    Log_s has 'outcome=rules_fallback', 'rules_fallback',
    Log_s has 'prompt_tokens=', 'usage_counts',
    Log_s has 'ManagedIdentityCredential.get_token succeeded', 'managed_identity_success',
    Log_s has 'ManagedIdentityCredential.get_token failed', 'managed_identity_failed',
    Log_s has 'Synthetic resident showcase', 'startup',
    Log_s has 'Traceback', 'traceback', 'other')
| summarize count() by RevisionName_s, event
```

The App Insights aggregate was:

```kusto
union isfuzzy=true requests, dependencies, exceptions, traces
| where timestamp between (datetime(2026-10-30T18:06:30Z) .. datetime(2026-10-30T18:10:00Z))
| summarize count() by itemType, cloud_RoleName
```

## Exact Next Coordinator Action

Use an EXISTING authorized private telemetry route to query the existing
log-cutover-test workspace. Do not change networking/RBAC or enable AI just to
obtain access. First inspect only fixed classified events for the actual
failed revision and interval:

```kusto
ContainerAppConsoleLogs_CL
| where TimeGenerated between (datetime(2026-10-30T18:07:45Z) .. datetime(2026-10-30T18:08:20Z))
| where ContainerAppName_s == 'ca-resident-demo'
    and RevisionName_s == 'ca-resident-demo--recover-ai-180649'
| extend event=case(
    Log_s has 'resident_assistant outcome=rules_fallback', 'rules_fallback',
    Log_s has 'resident_assistant prompt_tokens=', 'usage_counts',
    Log_s has 'ManagedIdentityCredential.get_token succeeded', 'managed_identity_success',
    Log_s has 'ManagedIdentityCredential.get_token failed', 'managed_identity_failed',
    Log_s has 'Response status:', 'sdk_response_status', '')
| where event != ''
| extend sdk_status=extract(@"Response status:\s*(\d{3})", 1, Log_s)
| project TimeGenerated, RevisionName_s, event, sdk_status
| order by TimeGenerated asc
```

SDK status/identity success can concern SQL or managed-identity token HTTP, not
necessarily OpenAI inference; correlate the stage before attributing it.
No row or generic-only fallback does not identify a cause. If no richer
historical evidence exists, the coordinator must separately scope privacy-safe
allowlisted stage/reason diagnostics before a later independently authorized
reproduction; no reproduction or diagnostic deployment is authorized here.
Keep prompts, case/resident identifiers, tokens, headers, raw exception text and
model output out of telemetry and handoff. No new corrective config is
established by this task.

## Implementation-Time Plan and Detail Updates

No material divergence from the evidence-only candidate. The one independent
critique executed Complete / Pass, zero findings, for packaging only.
Its wording implying the caller explicitly selected a fallback packaging
outcome is not adopted as a new user decision: the parent records it solely as
an honest blocked-result disposition under the original diagnostic request.
The original critique is preserved unchanged.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|---|---|---|---|
| Existing generated-answer unit regression | Synthetic model transport | Passed | 1 test, 0.001s; no cloud/model calls |
| Public synthetic stage payload probe | Repair question, all STAGE_TEXT entries | Passed | 1920-1976 bytes, below 4096; not deployed incident proof |
| Caller full API discovery, initial system runtime | Existing local tests | Failed (dependency setup) | 1343 tests in 484.691s, 318 skips; missing azure.eventhub and installed zava-forward-api metadata |
| Ruff lint / format / mypy, initial system runtime | src/api | Unavailable | Each exit 127, ruff/mypy not installed |
| Pinned external runtime restoration | src/core, src/agents, src/api[dev] | Passed | Task-owned external venv; pip exit0, no manifest/source edits |
| Caller full API discovery, restored runtime | Existing local tests | Passed | 1370 tests in 480.249s; 318 opt-in/integration skips remain unexecuted |
| Ruff lint / format, restored runtime | src/api | Passed | ruff 0.17.1, lint clean; 60 files already formatted |
| mypy, restored runtime | src/api | Passed | mypy 2.4.0, no issues in 116 source files |
| Complete publication gate | Exact final candidate | Not run / not claimed | Local commit only; future publication requires complete gate |
| Live sign-in / actual inference / issue acceptance | Resident site | Not run | Explicit caller prohibition |

## Pre-Review Reconciliation

* P01 complete: report and all four requested commands have actual results. Initial setup failure retained; restored runtime rerun passed, with 318 skipped tests not claimed as execution.
* Root-cause goal and corrective change remain blocked by B1, not checked complete.
* Plan/details/changes agree on seven tracking files, no source changes, one Review then local persistence.
* Ready for one independent Review of evidence packaging, not causal acceptance. P02-T02 local persistence is scheduled after the original Review.

## Blockers

* B1: historical enabled-advisor failure stage is unavailable through permitted accessible routes. Coordinator owns approved private telemetry retrieval. This blocks exact root cause/correction, not local evidence persistence.

## Remaining Work

* P02-T02 local commit.

## Follow-Up Items

* Rank 1: retrieve bounded historical telemetry through existing approved private access (W4-W6).
* Rank 2, conditional: separately scope safe stage/reason observability only if historical evidence cannot distinguish the stage (C6).
* No child work or cloud action begins without coordinator direction and applicable authorization.

## Return-to-Caller State

* Implementation scope: full evidence-only plan; no runtime behavior change.
* Diagnosis status: Blocked for exact historical enabled failure; current disabled rollback explained.
* Review execution/outcome: Complete / Not accepted as causal diagnosis; original adverse outcome retained.
* Local persistence: pending; no push authorized.

## P01-T02: Initial Local Validation and Dependency Recovery

The first attempt acquired the shared lock and executed all four requested
commands from src/api with the exact caller PYTHONPATH. External original log:
`/home/azureuser/.copilot/session-state/1e8164bc-6760-4b17-bde0-fefe41056013/files/resident-diagnosis-validation.log`.
Unittest exit1: 1343 tests, 484.691s, 318 skips, two setup errors:
`azure.eventhub` missing during test_iot_stream import, and missing installed
zava-forward-api distribution metadata in test_version. Ruff lint/format and
mypy each exit127 because the executables are absent. No source test assertion
failure or passing full validation is claimed.

Immediately relevant execution update, not a plan divergence: restore the
existing src/core, src/agents and src/api[dev] distributions into a task-owned
external virtual environment using pip, only after these actual dependency
failures, then run the same four commands under the same shared lock. Keep
the first failed log immutable. No dependency manifest or runtime source edit,
uv, cloud fallback or diagnostic retry is authorized.

### Restored Runtime and Complete Requested Rerun

The following ran under `flock -w 600 /tmp/ama-rpi-heavy.lock` and exited0:

```bash
python3 -m venv --system-site-packages /home/azureuser/.copilot/session-state/1e8164bc-6760-4b17-bde0-fefe41056013/files/diagnosis-runtime
/home/azureuser/.copilot/session-state/1e8164bc-6760-4b17-bde0-fefe41056013/files/diagnosis-runtime/bin/python3 -m pip install --quiet -e src/core -e src/agents -e "src/api[dev]"
```

The four commands were then run sequentially inside a fresh acquisition of
the same requested lock, from src/api. PATH prepended that external venv; no
other application/credential setting was supplied:

```bash
export PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
python3 -m unittest discover -s tests -q
ruff check .
ruff format --check .
mypy
```

Each command exited0. Unittest ran1370 tests in480.249s, OK with318 skips
(integration/opt-in coverage not exercised by discovery). Ruff0.17.1 lint
passed and format check reported60 files already formatted. Mypy2.4.0
reported no issues in116 source files. No tests were added/removed or changed.
No live Azure/SQL/model acceptance follows from these local results.

External originals remain under this session's files directory:

| Log | SHA256 |
|---|---|
| resident-diagnosis-validation.log, original failed setup | 168ccfa4bc1da268d4c9f1ad299195325be42a6521aa2f4a64113f7c80217169 |
| diagnosis-dependency-restore.log, quiet successful restore | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| resident-diagnosis-validation-restored.log, all four exits0 | dc532bf1c9d722f322a5422c7139229f7cfab089941e9aed69f105c5208678c1 |

Dependency recovery is an immediately relevant execution refinement allowed by
the plan after actual missing-package failures, not a new source fix, a second
critique or a diagnostic inference retry. Plan markers/details and state are
reconciled for the one original Review. Full publication gate, actual-model
evaluation, private telemetry/SQL and human acceptance remain unperformed.

## P02-T01: Original Independent Review and Parent Disposition

Exactly one independent Review executed Complete / Not accepted:
.copilot-tracking/reviews/logs/2026-10-30/resident-ai-diagnosis-563-review.md.
Original finding text/outcome is preserved, not re-reviewed or rewritten.

| Finding | Original classification | Parent routing/disposition |
|---|---|---|
| RV-001 | High, exact cause/corrective config unproved | Accepted B1; later coordinator research via approved private telemetry, no current source fix |
| RV-002 | Low, local persistence scheduled after Review | Parent executes P02-T02; not causal delivery or issue acceptance |
| RV-003 | Medium, alleged temporary-directory lock conflict | Not adopted as an actionable execution defect: caller explicitly prescribed `flock -w 600 /tmp/ama-rpi-heavy.lock`; no incompatible restriction is evidenced in this execution context. Preserve original finding and this disagreement without inventing a new requirement or changing/rerunning the lock |

This is parent disposition of the returned evidence, not implementation or
closure verification of a Review finding. The unresolved causal outcome
remains Not accepted regardless of the disputed lock observation. No second
Review, source correction, deployment or diagnostic reproduction occurs.

## P02-T02: Scheduled Local Persistence Boundary

Resolve the authenticated GitHub account immediately before committing and
derive `{id}+{login}@users.noreply.github.com`; configure repository-local
identity and supply it for both author and committer. Stage exactly seven
resident-ai-diagnosis-563 artifacts, preserve all original activation files,
and include the required Copilot trailer with Refs #563 only. No push.

The original assessed candidate is committed before recording its actual hash
and verified boundary in a subsequent evidence-only closeout commit. This
avoids presenting an unexecuted local commit as already verified. No complete
publication gate or eligible receipt is claimed or generated.
