# Proper Warm local demonstrator

This is a local viability demonstrator for the Proper Warm retrofit programme. It uses fictional evidence, a local Python server and SQLite. It is not an operational case-management system, and its outputs are not evidence that a legal, safety, funding or company requirement has been met.

## Safety boundaries

* Use synthetic data only. Do not enter resident, staff, address, contact, health, support or other personal information.
* Local startup binds to `127.0.0.1` by default. The container image also defaults to loopback; only the Bicep internal-ingress configuration selects the container listener. Never expose that listener publicly.
* It has no M365, Dataverse, Dynamics 365 or resident-system integration. Azure
  model inference is opt-in and receives only the bounded fictional case
  snapshot, never the source workbook, whole dataset or private overlay.
* The private `support/synthetic-data/retrofit-flow/proper-warm-year-one/stock-geography/` overlay is excluded.
* The missed-appointment threshold is a provisional synthetic test rule, not an approved operational control. Only a confirmed appointment with verified resident no-access counts; escalation is strictly greater than the configured threshold.
* Stage gates, safety holds, reviews and threshold changes demonstrate workflow behavior only. Human review remains necessary, and company ratification is outstanding.
* Local SQLite data is stored in `prototype/.data/` by default. It is disposable demo state, not a backup or production data store.
* In the Azure Container Apps example, SQLite is on the container's ephemeral filesystem. A restart or revision replacement can lose its state; the example has one replica and no Azure Files or production persistence.

## Requirements

* Python 3.12 or newer.
* The dependencies in `requirements.txt` (`openpyxl`, `azure-identity`).
* The repository's published fictional evidence pack at `docs/reference/research/retrofit-synthetic-data/`.

## Run locally

From the repository root, create an environment and install the dependencies
with pip through the configured company proxy. Do not disable TLS checks:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r prototype/requirements.txt
```

Start the server in PowerShell:

```powershell
$env:PYTHONPATH = "prototype"
python -m properwarm.server
```

On macOS or Linux, use `PYTHONPATH=prototype python -m properwarm.server`. Open <http://127.0.0.1:8765> in a browser. The server accepts `--port`, `--data-dir` and `--source-dir` options for local testing. Stop it with `Ctrl+C`.

The first start seeds local SQLite state from the synthetic `candidate-lifecycle.csv` and `safety-holds.csv` files. The app reads selected synthetic fields only. It fails if either required source or its required columns are missing. Demo database and journal files remain under `prototype/.data/` unless `--data-dir` is set.

## Container and compile-only Azure example

The container package includes a separate sanitized seed directory, not the full source CSVs. Generate it from the approved synthetic pack and build the image from the repository root:

```powershell
python prototype/scripts/build_container_seed.py
docker build -f prototype/Dockerfile -t properwarm-demo:local .
```

The Docker image defaults to loopback. The Azure Container Apps template sets `APP_INTERNAL_INGRESS=true` together with internal-only environment and app ingress; the server maps that explicit mode to the container interface. Do not set this mode outside an internal-ingress environment.

The full template is [deploy/main.bicep](deploy/main.bicep). It requires an
existing Container Apps infrastructure subnet, a separate model private-endpoint
subnet, virtual-network ID and a container image available to Azure. It creates
Log Analytics, an internal environment/app, a user-assigned managed identity,
an Entra-only Azure OpenAI resource/model deployment and inference RBAC.
Private DNS and a private endpoint keep model public-network access disabled.
The full app template is compile-only and not deployment-tested; it does not
provision a virtual network or image registry and is not production guidance.
Compile without deploying:

```powershell
az bicep build --file prototype/deploy/main.bicep --stdout
```

### Model-only local development

[deploy/local-dev.bicep](deploy/local-dev.bicep) deploys only the model resource,
pinned model version and developer inference role. Unlike the full template,
the developer endpoint is internet-addressable but its firewall denies all
except the supplied approved workstation/company-proxy IPv4 addresses. API keys
are disabled. The application itself stays loopback-only. A changing egress IP needs an
explicit firewall redeployment, not broad access or a TLS bypass.
When routing uses more than one egress, supply `additionalAllowedIps` as well
as `allowedIp`. Redeployment replaces the allowlist: retain every individually
approved rule rather than overwriting an administrator's additional address.

Deploy only after confirming the intended subscription, resource group,
region, principal and usage charges. Example placeholders are not credentials:

```powershell
az deployment group create --subscription <subscription-id> --resource-group <demo-resource-group> --name properwarm-local-model --template-file prototype/deploy/local-dev.bicep --parameters allowedIp=<egress-ipv4> developerPrincipalId=<entra-object-id>
```

Take `endpoint` and `deploymentName` from deployment outputs. Authenticate in
the resource's tenant with an identity holding Cognitive Services OpenAI User:

```powershell
az login
$env:AZURE_OPENAI_ENDPOINT = "<endpoint-output>"
$env:AZURE_OPENAI_DEPLOYMENT = "<deploymentName-output>"
$env:PYTHONPATH = "prototype"
python -m properwarm.server
```

No endpoint, subscription, IP, token or principal needs committing. Do not
paste credentials into the UI. Without configuration, model actions explicitly
report unavailable; the existing human workflow still works. Network/auth/
model failures produce failed run records, never canned AI success.

## Role/task workspaces and agent responsibilities

The programme, frontline coordination, assurance and operator/intake views
organise the same synthetic evidence around different tasks. They change queue
emphasis and available UI sections. They are **not authentication or server
authorization**: this local synthetic demo still allows its documented API
actions. A real role-secured service needs Entra claims and server-enforced
permission checks before operational use.

The implemented Case Review Agent autonomously chooses the order/grouping of
three read-only tools: case inspection, transition-gate inspection and appointment
inspection. It has at most four model calls and six tool calls. Every run ends
in a validated proposal awaiting a human, or an explicit failure. It cannot
change gates, advance a case, grant consent, approve works or communicate with
residents. Accepting its draft acknowledges a proposal, not a safety decision;
the normal domain controls must still be satisfied separately.

| Responsibility | Delivered status | Human handoff |
| --- | --- | --- |
| Case Review Agent | Real Azure inference when configured; bounded read-only evidence tools, grounded blocker checks, persisted run and review | Safety lead for active holds; otherwise a supported human task owner |
| Deterministic gate/threshold engine | Delivered; not an AI agent | Named reviewer owns synthetic evidence and case actions |
| Stock prioritisation, assessment, grant/funding, coordination and quality agents | Future capabilities; not implemented by the Case Review Agent | Investment, resident decisions, professional approval, submission and acceptance remain human-owned |

The model drafts prose; machine checks validate finding codes, exact source
references, mandatory blockers, owner and output shape. They do not establish
the factual/legal correctness of all prose. Treat every draft as untrusted until
reviewed. The UI displays provenance, tool trace and explicit acceptance/rejection.
Changed evidence or configuration makes acceptance stale; rejection remains
available. Runs, failed states and reviewer decisions survive local restart
and appear in the evidence export. A running record is committed before the
first inference call. Process interruption leaves it visibly unfinished, not
successful or silently replayed; durable restart/retry orchestration is a future
scaling requirement.

## Model evaluation and selection

`gpt-4.1-mini` version `2025-04-14` is a provisional lower-cost structured-output
candidate, not a measured best model. Workflow-only processing remains the
paired baseline: exact gate/hold/counter checks already work without AI. A
larger model (for example `gpt-4.1`) is an alternative for later comparison;
it is not justified until source fidelity, critical-exception recall, review
effort, latency and token-based cost are compared on the same cases.

```powershell
python prototype/scripts/evaluate_agent.py --out prototype/.data/offline-agent-evaluation.json
python prototype/scripts/evaluate_agent.py --live --out prototype/.data/live-agent-evaluation.json
```

The six paired fictional cases cover missing gates, readiness, safety hold,
investigation, closure and unmapped stage. A report records exact blocker
coverage, schema/citation checks, trace, model/prompt hash, latency and token
usage alongside the workflow-only output/time. A failed case exits nonzero.
Offline reports are labelled contract doubles and prove software handling,
not model quality. Live reports require real inference; human review effort
and incremental task value remain unmeasured until a reviewer study. No synthetic
test is a sector-policy or operational approval. Failure-injection regression
tests reject unauthorized tools, missing blockers, invented references,
nonproductive loops, real-data markers and stale reviews.

For optional headless UI/API regression, install Playwright with pip and its
Chromium runtime, then run the explicit test-double harness. It creates a
temporary loopback server/database, never changes the development database and
stops the server on success or failure:

```powershell
python -m pip install playwright
python -m playwright install chromium
python prototype/scripts/validate_workbench.py --out prototype/.data/workbench-validation.json
python prototype/scripts/validate_workbench.py --live-smoke --out prototype/.data/live-workbench-validation.json
```

### Recorded development evidence (2026-10-05)

| Check | Observed result | What it does not establish |
| --- | --- | --- |
| Prototype unittest | 25 tests passed, including original workflow/import regressions | Production acceptance or security review |
| Offline paired evaluation | 6/6 contracts passed | Actual model quality |
| Native browser/API harness | Task controls, citations, accept/reject, stale review, outage, investigation/closure/reopening, import/export and mobile width passed; no browser JavaScript errors | Human usability/accessibility study or live model execution |
| Local sequential overview timing | 20 requests, 991 synthetic cases, concurrency 1: median 58.69 ms, p95 68.06 ms, unique request IDs | Sustained throughput, multi-user capacity or approved SLO |
| Bicep | Full app and model-only entrypoints compiled; model-only deployment succeeded | App deployment or private-endpoint end-to-end test |
| Live Azure paired evaluation | 6/6 passed with `gpt-4.1-mini-2025-04-14`, prompt `case-review-v2`; safety-hold and investigation findings both retained | Alternative-model comparison, human review effort, operational accuracy or business savings |
| Live Azure UI/API smoke | Real case proposal, persisted trace/provenance, source links and synthetic-runner rejection passed; case stage, gates and appointments unchanged | Actual human review or a scored capstone rehearsal |

Initial calls failed with a firewall 403. The owner added a second individually
approved egress IP; after propagation inference worked. Entra-only authentication,
deny-default firewall, no trusted-service bypass and owner-approved individual
egress rules remain in force; unrestricted access was not enabled. The first
live pass achieved 5/6: the closed-case proposal included an unsupported finding
and was rejected, not applied. Prompt v2 clarified exact tool-provided finding
coverage and inactive-case handling without weakening the validator; a regression
test and a new six-case live run passed.

The successful paired run recorded median agent latency 12,559.85 ms and
nearest-rank p95 17,671.53 ms across six sequential cases, versus median 0.030 ms
for workflow-only finding calculation. It used 5,328 prompt tokens and 1,138
completion tokens, 12 model calls and 18 tool calls. The separate real browser
handoff took 18,029.53 ms with 898 prompt and 196 completion tokens. The model
adds substantial latency and token cost to already-correct deterministic checks;
its proposed value is readable handoff drafting, not superior blocker detection.
Reviewer effort and task benefit still need measurement before retaining this
AI step in a production workflow.

Reports and screenshots stay in ignored `.data/`; no credentials or personal
network identifiers are delivery evidence. A fresh capstone score is still
required, and Section B rehearsal/validation evidence is not supplied by
automated UI or contract tests.

## Architecture, tradeoffs and scaling path

The current separation is `server -> storage/domain` for consequential writes
and `server -> agent -> read-only tools -> Azure inference` for proposals.
The structured proposal contract and source snapshot are the handoff boundary;
the model has no database write interface. SQLite uses transactional persistence
and the proposal-review path takes a writer lock while reconciling its snapshot.
Audit records are a demo trace, not a tamper-proof compliance archive.

| Stage | Architecture decision | Required evidence before moving on |
| --- | --- | --- |
| Local viability (delivered) | One process/SQLite; minimal dependencies and fast reproducible tests over distributed complexity | Current domain/agent/API/UI tests; no production scalability claim |
| Internal container example (full template only) | One replica/ephemeral SQLite avoids unsafe multi-writer shared files; private model endpoint and managed identity | Image build, private DNS/reachability and persistence validation; app remains undeployed |
| Multi-user/scalable service (not implemented) | Replace Store with transactional Azure SQL repository; add Entra API authorization; stateless API replicas only after authoritative state moves | Migration/backfill parity, optimistic concurrency/idempotency, load and failover tests, backup/restore and role-denial tests |
| Durable agent work (not implemented) | Persist run/job state outside request threads; durable queued execution and human-review waits instead of in-memory coordination | Exactly-once decision acceptance, bounded retry/dead-letter, restart replay, queue saturation and cost controls |

Increasing Container Apps replicas before replacing SQLite would create divergent
state, not scaling. No automatic transition on model failure is permitted:
the recorded failure routes to explicit human workflow handling. Request IDs
correlate JSON request/agent logs with persisted run IDs; model steps/tokens
are recorded. Performance SLOs, sustained throughput and business-unit cost
require measured workloads and approved targets, not resource-allocation guesses.
HTTP log timing ends at response-header generation; the client-side harness
measures through response retrieval. Model duration includes inference/tool work.

## Test and regenerate the sample workbook

Run the regression suite from the repository root:

```powershell
python -m unittest discover -s prototype/tests -v
python -m compileall -q prototype/properwarm
```

Rebuild the fictional three-row workbook:

```powershell
python prototype/scripts/build_demo_workbook.py
```

In the workbench, select `prototype/seed/demo-import.xlsx`, preview every row disposition, then commit the preview. Import accepts only the declared nine-column synthetic schema, rejects invalid rows, preserves source-row lineage and rechecks conflicts at commit. It does not modify the workbook or overwrite an existing case.

## Workbench flow

* Search and filter fictional cases, then inspect current stage, gates, holds and history.
* Change synthetic gate controls and advance only when required gates pass and no active hold blocks progression.
* Record confirmed appointment outcomes, review events, closure and reopening. Closure starts a new active episode while retaining prior history.
* Configure the synthetic missed-appointment threshold and inspect the audit history. The default is 5; five eligible events do not escalate and the sixth does.
* Download the JSON evidence export to inspect cases, source lineage, events, audit entries and current configuration.

All actions remain within the running demonstrator and do not contact residents or alter source evidence. In the container example, access is restricted to the configured internal network.

## Architecture

The editable local architecture diagram is [architecture/proper-warm-local-prototype.excalidraw](architecture/proper-warm-local-prototype.excalidraw). It describes the implemented local flow; the compile-only Azure example does not represent an approved production architecture.

## Limitations

This prototype demonstrates deterministic controls and a separately configured
bounded model proposal path against fictional evidence. It does not prove company
process fit, rule validity, resident acceptance, accessibility conformance,
security for operational data, incremental AI value, delivery outcomes or
regulatory compliance. Threshold ratification, operational configuration
governance, hosting, identity, integrations and production persistence require
separate evidence and approval. Model-only development deployment is distinct
from the undeployed internal-app template.
