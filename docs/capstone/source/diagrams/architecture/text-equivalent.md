---
title: Application and Azure Architecture Views
description: Accessible relationships, source locators and acceptance limits for the CxO concept and full Azure reference diagram
ms.date: 2026-11-08
ms.topic: concept
---

## Views And Reproduction

Two views explain the same product direction at different depths:

| Audience | Editable source | Vector | Native PNG |
| --- | --- | --- | --- |
| CXOs: people, application responsibilities and trust | [CxO Excalidraw](./cxo-architecture.excalidraw) | [CxO SVG](./cxo-architecture.svg) | [CxO PNG](./cxo-architecture.png) |
| Architects: complete Azure source topology and gated alternatives | [Azure Excalidraw](./azure-architecture.excalidraw) | [Full Azure SVG](./azure-architecture.svg) | [Full Azure PNG](./azure-architecture.png) |
| Core projection, appendix B10/page 38; full-size source for detail | `core` frame in the same Azure Excalidraw | [Core SVG](./azure-core.svg) | [Core PNG](./azure-core.png) |
| Complete wide deployment projection, main page 13 | `deployment` frame in the same Azure Excalidraw | [Deployment SVG](./azure-deployment.svg) | [Deployment PNG](./azure-deployment.png) |

The [generator](./build-architecture.mjs) owns the diagram models and
source-bound derivatives. Boxes, text, arrows and service icons remain
editable. The SVG represents the same nodes and flows; editor frame chrome
is omitted. The core projection is not a third architecture and intentionally
does not shrink every alternative into page 38. The new 2400 x 1170
deployment frame is a compact, connected projection of the same complete
source model, including support services and gated options, not a third
contradictory architecture. All its labels are at least 34 native pixels,
about 12.1 pt at the approved 5.8-inch-high slide contain size. The CxO
1600 x 850 view has a 26-pixel minimum, about 12 pt at 5.45 inches high.
The detailed core view points to main page 13 and the full-size editable
map rather than claiming all small control labels are main-slide text.

```bash
node docs/capstone/source/diagrams/architecture/build-architecture.mjs
node docs/capstone/source/diagrams/architecture/build-architecture.mjs --check
node docs/architecture/update-architecture.mjs --check
EXCALIDRAW_BROWSER_PATH=/path/to/existing/chrome node --test docs/capstone/source/diagrams/architecture/test-architecture.mjs docs/capstone/source/diagrams/architecture/test-geometry.mjs
excalidraw render docs/capstone/source/diagrams/architecture/cxo-architecture.excalidraw --out /absolute/external/cxo.png --padding 0 --scale 1.5 --max-width 2400 --max-height 1275 --fonts-url none
node docs/capstone/source/diagrams/architecture/export-reference.mjs | excalidraw render - --out /absolute/external/azure.png --padding 0 --scale 1.5 --max-width 3600 --max-height 3090 --fonts-url none --timeout 120000
excalidraw render docs/capstone/source/diagrams/architecture/azure-architecture.excalidraw --frame-id core --out /absolute/external/azure-core.png --padding 0 --scale 1.5 --max-width 3600 --max-height 1215 --fonts-url none --timeout 120000
excalidraw render docs/capstone/source/diagrams/architecture/azure-architecture.excalidraw --frame-id deployment --out /absolute/external/azure-deployment.png --scale 1.5 --fonts-url none --timeout 120000
```

Supply `--browser-path` for an existing Chromium/Chrome installation when
needed. Excalidraw CLI 0.3.0 renders locally without an account or upload;
this run used existing Chromium 1194. Do not install a new browser or
overwrite delivery files as an implicit setup action. Review derivatives
before deliberately updating the media catalog.
For a local runtime directory, set `TMPDIR` to a short dedicated path
before launching Chromium; long paths can exceed the browser's socket
limit. The 8 November run staged exports in
[dated tracking](../../../../../.copilot-tracking/architecture-diagrams/2026-11-08/zava-forward/validation.json),
reviewed them before updating delivery copies and used no new dependency.
`export-reference.mjs` is an ephemeral selection of the authoritative
Azure scene: it omits the duplicate deployment projection and hides editor
frame chrome. It changes no authoritative nodes, arrows or source claims.

## CxO Application Concept

Read the simple view left to right:

1. Employees use the company's Microsoft identity for the Workbench and
   the Microsoft 365 environment. Each application still has separate
   permission assignments; a sign-in is not permission to read everything.
2. The Workbench presents role-specific work for coordination, resident
   liaison, Finance, Quality and Programme. A shared case has an owner,
   evidence and an explicit next action.
3. The case service/API checks role, case and field scope and applies coded
   workflow gates. People remain responsible for consent, professional
   sign-off, funding decisions and release.
4. Case/database records retain state, metadata and audit. Evidence storage
   retains file bytes, versions and scan state; the database references them.
   A stored or scanned file is not a verified conclusion.
5. AI receives the permitted task projection and returns a draft/advisory
   answer for review. It does not receive an unrestricted database/document
   feed or a case-decision write tool.
6. Excel files may originate in a modelled shared OneDrive/M365 working area.
   Existing controlled file preview/import tooling is shown; a live Graph
   connector or company-specific OneDrive configuration is not established.
7. Residents retain assisted service and may choose a separate own-case
   website/advice route. The existing synthetic resident showcase is separate;
   shared-case integration and managed external identity remain gated targets.
8. Home sensors feed Basic B1 IoT Hub, its MI trusted-service route and a
   dedicated Event Hubs stream. The API initiates receive over the Event
   Hubs private endpoint. The source-coded finite intake validates,
   deduplicates and appends accepted readings into restricted SQL history;
   rejected input creates an owned DQ exception. Live transport, calibration,
   consent and operational use remain separate gates.
9. The household telemetry/history/averages service is a capability of
   the shared API backed by the existing SQL store, not a standalone
   worker or a new Azure product. Retained analysis is read-only; exercise
   baseline/early/late means are computed on read. The owner-requested
   persisted per-home averages are a visible gated target, not an
   implemented schema/materialization store. The current quality-evidence
   helper uses measures, checklists and documents; post-retrofit sensor
   linkage to Quality Verification remains proposed.
   Retained analysis and comparison are reusable core functions; their
   existence does not establish a served API analysis endpoint, scheduler
   or Workbench sensor-aggregate integration.
10. Insufficient, stale or declined telemetry preserves manual review with
    no priority effect. Averages are context, not diagnosis, consent,
    task creation, quality acceptance or safety release.

The outer boundary is **logical application/data scope**, not a VNet, data
residency guarantee or contractual provider boundary. It is one closed
editable outline with a notch at its lower left: the Home sensors box stays
outside, and the IoT Hub, Event Hubs, API telemetry service and SQL history
boxes stay inside, so no outline line cuts through a label or node. Solid lines mean
source-coded interactions; dashed paths mean separately gated integration
or activation. AI remains untrusted advice across an evidence/decision
boundary even where its box appears within the product concept.
The [full view](./azure-architecture.svg) makes the separate resident public
Sweden Central model option visible; the simple view must not be read as
"all inference is private and in the UK".

Source locators and limits:

| Relationship | Source and limit |
| --- | --- |
| Company identity and application roles | [TrustedProxyProvider](../../../../../src/api/src/zava_forward/api/auth.py#L101) and [role map](../../../../../src/api/src/zava_forward/api/auth.py#L34); platform authentication and real configuration remain separate |
| Coded workflow and controlled human action | [Gate outcomes](../../../../../src/core/src/zava_forward/core/gates.py#L1), [transition checks](../../../../../src/core/src/zava_forward/core/gates.py#L105) and [advance](../../../../../src/core/src/zava_forward/core/store.py#L635); no deployed LangGraph/GraphState runtime is implied |
| Proposal preparation versus case authority | [Five retrofit helpers](../../../../../src/agents/README.md#five-retrofit-assistants-2026-10-13-implementation); source-coded permissions and finite authority, not semantic/human benefit acceptance |
| One skill-selected conversational call | [Employee bounded chat](../../../../../src/api/README.md#employee-chat-with-bounded-skills-530); no router, tools, booking or domain write |
| Existing Excel tooling | [Importer](../../../../../src/importer/README.md); read-only preview, lineage, quarantine and export, not a live OneDrive connector |
| Resident field scope | [Resident preview catalog](../../../../../src/core/src/zava_forward/core/resident_preview.py#L24); separate identity and own-case grants are required |
| Devices | [Bounded streaming record](../../../../reference/research/iot-sensor-analytics-research-plan.md#bounded-streaming-engineering-2026-10-27-refs-110-184); synthetic/source evidence, not live resident monitoring acceptance |
| Telemetry/history storage and owned DQ | [SQL consumer](../../../../../src/core/src/zava_forward/core/sensor_consumer.py), [finite API intake](../../../../../src/api/src/zava_forward/api/sensor_ingestion.py), [SDK adapter](../../../../../src/api/src/zava_forward/api/iot_stream.py); validated idempotent SQL append, not an always-running service configured by main |
| Retained analysis and averages | [Read-only entry](../../../../../src/core/src/zava_forward/core/sensor_analysis_store.py#L21), [exercise window means](../../../../../src/core/src/zava_forward/core/synthetic/sensor_scenarios.py#L350); current computed-on-read analysis, separately gated averages persistence target |
| Quality-helper separation | [Quality-evidence categories](../../../../../src/core/src/zava_forward/core/assistants.py#L47) and [projection](../../../../../src/core/src/zava_forward/core/assistants.py#L156); no current telemetry aggregate integration |

## Full Azure Reference View

A bounded System Architecture Reviewer analysed Bicep at
`c50e9f0b888e267d5949cab09069d31b6c740e3b`. It supplied a source topology,
precision findings and exact locators; it did not adopt an ADR, query Azure,
deploy, inspect credentials or certify current operation.
That original model and its review remain historical evidence. The
8 November continuation checks the current source files directly and
embeds exact path, anchor/line and SHA-256 references in native/SVG
metadata. `source_basis_head` records `b671116d`, the checkout at the
8 November authoring start, while whole-file hashes identify the actual
files used; an uncommitted authoring delta is
not falsely described as already contained in that commit.
No infrastructure declaration, runtime, service adoption or live
deployment is changed by the diagrams.

The selected main view is the **direct-demo shared-API realization**.
Its corporate sign-in registration is configured separately. `enableApiAi`
must select direct model access; task release, privacy and financial
admission are independent gates. Background workloads have an independent
switch: direct API AI does not automatically remove them.
Placeholder/default images are not an accepted operating deployment.

The real network enclosure contains the ACA subnets and private-endpoint
subnet. SQL, Blob, Foundry, IoT Hub, Event Hubs, Registry, Vault and Monitor
are managed services **outside the VNet**, reached through private endpoints
where declared. The source/render frame is only an organisational grouping.
Linked private DNS and NSGs are network controls, not model judgement.

### Numbered Main Flows

| Number | Interaction and authority | Exact source at the reviewed base |
| --- | --- | --- |
| 1 | Staff sign in through the configured Entra application and HTTPS | [ACA auth](../../../../../infra/modules/containerapps.bicep#L221), [registration](../../../../../infra/entra/app-registration.json#L1); exact tenant/audience and assignments remain required |
| 2 | EasyAuth supplies a verified principal; the API separately authorises role/case/field operations | [Current identity decision](../../../../adrs/0002-pilot-readiness-architecture.md#entra-authoritative-staff-access-owner-decision-2026-10-24-refs-360), [auth provider](../../../../../src/api/src/zava_forward/api/auth.py#L101) |
| 3 | API managed identity reaches private SQL for case state, metadata, audit and proposals | [SQL module](../../../../../infra/modules/sql.bicep#L34), [SQL configuration](../../../../../infra/modules/containerapps.bicep#L166); contained users/grants initialized separately |
| 4 | Authorised file transfer reaches Blob through the API/private endpoint; SQL holds references and hashes | [Blob containers](../../../../../infra/modules/storage.bicep#L58), [API document configuration](../../../../../infra/modules/containerapps.bicep#L171); no live OneDrive connector |
| 5 / 6 | API sends an authorised evidence subset to Foundry/OpenAI; drafts/citations/usage return for validation and human review | [Conditional API AI rights](../../../../../infra/main.bicep#L328), [model configuration](../../../../../infra/modules/containerapps.bicep#L178), [Foundry](../../../../../infra/modules/foundry.bicep#L16); no unrestricted SQL tool or AI case-write authority |
| 7 | Residents may use assisted service or the separate synthetic showcase; future external identity/shared-case integration is dashed | [Resident deployment inputs](../../../../../infra/resident-demo.bicep#L14), [synthetic session](../../../../../infra/resident-demo.bicep#L128); not staff Entra enrolment or a proved shared staff database |
| 8 | Simulated/private-reachable devices use individual credentials and the Hub's private endpoint | [Device boundary](../../../../../infra/modules/iothub.bicep#L95), [simulator](../../../../../infra/live-simulator-job.bicep#L69); credential issue/private reachability separately authorised |
| 9 | Hub system identity routes to the dedicated Event Hub using the trusted-service exception | [Hub route](../../../../../infra/modules/iothub.bicep#L112); routing-ready and sender-role propagation required, not a route through the consumer PE |
| 10 | The API initiates receive through the Event Hub PE with entity-scoped Data Receiver | [Receiver grant](../../../../../infra/modules/iothub.bicep#L147), [Event Hub PE](../../../../../infra/modules/iothub.bicep#L202); SDK/configuration activation is not proved by IaC |
| 11 | The same API intake capability validates and idempotently appends accepted sensor readings to SQL; bad input becomes owned DQ | [API composition](../../../../../src/api/src/zava_forward/api/sensor_ingestion.py), [SQL consumer](../../../../../src/core/src/zava_forward/core/sensor_consumer.py); no automatic diagnosis, consent, quality acceptance or safety release |
| Read / target | The telemetry/history/averages capability reads restricted retained history and trusted consent; exercise means are computed on read. Persisted per-home averages in existing API/SQL are a gated target, not implemented. | [Retained analysis](../../../../../src/core/src/zava_forward/core/sensor_analysis_store.py), [exercise comparator](../../../../../src/core/src/zava_forward/core/synthetic/sensor_scenarios.py); no separate worker, accepted causal method or current quality-helper linkage |

Arrowheads show the initiating request; responses are implicit except the
bidirectional 5/6 advice link. Receive is client-initiated, not an Event Hub
push granting authority. Main exposes IoT outputs but does not configure the
API consumer; the lower branch is conditional capability design, not a
second deployed API or a live stream claim. The wide projection shows both
the Event Hubs-to-intake data direction and API-initiated receive direction;
they do not imply server-push authority. The duplicated SQL node in the
sensor lane refers to the same retained-reading case database, not an
independently adopted telemetry product.

### Supporting Services And Conditional Profiles

| Family | Representation and important condition | Sources |
| --- | --- | --- |
| Human versus workload identity | Entra entry is distinct from API/agent/orchestrator/import managed identities | [Workload identities](../../../../../infra/modules/identity.bicep#L6); role assignments do not prove professional delegation |
| Secrets and image supply | Key Vault secret-reference resolution; Registry MI image pull | [Vault](../../../../../infra/modules/keyvault.bicep#L15), [Registry](../../../../../infra/modules/registry.bicep#L15); accepted worker images/transport remain separate |
| Network/private access | ACA subnet modes, PE subnet, NSGs and linked private DNS; Blob/Queue/Vault/Registry/AI/Hub/EH/Monitor and optional token PEs are grouped | [Network](../../../../../infra/modules/network.bicep#L27), [PE helper](../../../../../infra/modules/privateEndpoint.bicep), [environment DNS](../../../../../infra/modules/envDns.bicep#L1) |
| Observability | Log Analytics, App Insights and private-only AMPLS; IoT/Event Hub metrics-only diagnostics | [Monitoring](../../../../../infra/modules/monitoring.bicep#L14), [IoT diagnostics](../../../../../infra/modules/iothub.bicep#L169); platform diagnostics do not establish complete application traces |
| Operations | Alerts/action group/workbook/budget notifications; candidate alerts default off | [Operational monitoring](../../../../../infra/modules/operationalMonitoring.bicep#L17), [main alerts](../../../../../infra/main.bicep#L460); notifications are not hard currency stops |
| Storage and audit | Seven Blob containers, task/import/poison queues, versions/quarantine/exports/digests; ledger/PITR/locks are control details | [Storage](../../../../../infra/modules/storage.bicep#L20), [SQL](../../../../../infra/modules/sql.bicep#L34); unlocked retention policies and quarantine declarations are not independent audit/scanner acceptance |
| Daily jobs/optional token store | Daily ledger job; separate token-only Blob and renewal job, gated ready state | [Ledger job](../../../../../infra/modules/containerapps.bicep#L400), [token storage](../../../../../infra/modules/authTokenStore.bicep#L15), [renewal](../../../../../infra/modules/containerapps.bicep#L266) |
| Asynchronous alternative | Separate worker, importer, orchestrator and queues are an amber inset, not the five current integrated helpers | [Worker/jobs](../../../../../infra/modules/containerapps.bicep#L301), [queue grants](../../../../../infra/main.bicep#L270); placeholder/queue adapter/post-back operation is not established |
| Production entry alternative | Front Door Premium/WAF/Private Link targets internal ACA, not the direct demo; modes are mutually exclusive | [Edge](../../../../../infra/modules/edge.bicep#L23), [main guards](../../../../../infra/main.bicep#L194), [existing-stack option](../../../../../infra/public-edge-existing.bicep#L32); origin/connection acceptance required per deployment |
| Separate resident option | Own-case SQL endpoint supplied independently; optional separate public Sweden Central Standard OpenAI account; managed external identity/shared-case target proposed | [Resident](../../../../../infra/resident-demo.bicep#L14), [resident model](../../../../../infra/resident-assistant.bicep#L24); default off and not inside the core private/UK boundary |
| Synthetic simulator | Separate job with an existing read-only certificate mount and SQL identity prerequisite | [Simulator](../../../../../infra/live-simulator-job.bicep#L18); Azure Files/certificates are referenced dependencies, not newly provisioned by main |

Every main Bicep service family is represented or deliberately grouped.
In the wide projection, the jobs-to-main-Blob arrow denotes the digest
archive dependency only. Optional token-only Blob is explicitly separate;
renewal readiness and simulator certificate mounts are independent
dependencies, not all writes to the evidence account.
Guards, locks, auditing, backup windows and individual alert resources are
control/source detail rather than additional request-path boxes.
No APIM, Cosmos DB, AI Search, Fabric, Power BI or Foundry Agent Service
orchestrator is added by analogy to a reference picture.

## Security, Privacy And Compliance Boundaries

Two distinct boundaries govern the design:

* Identity/reachability: an authenticated principal is admitted through the
  selected ingress, then separately checked against application scope.
  Workload managed identities use separately granted service access.
* Evidence/decision authority: authorised facts cross to an optional model;
  untrusted drafts cross back to validation/review. Approval, consent,
  professional judgement and real-world action remain separate.

Controls are source-authored, not universal privacy/compliance acceptance.
Storage roles remain broader than container-specific labels may suggest;
API SQL grants retain startup DDL authority, so runtime grant narrowing is
open. Model `GlobalStandard`, UK resource placement or a private endpoint
does not establish UK-only processing. The resident Sweden Central/public
option is deliberately separate.
Approved data purposes, lawful basis, notices, retention/erasure, processor
terms, professional authority, sensor consent/calibration and actual
recovery/capacity/alert owners require named human decisions.
Budget alerts warn; the separate application financial-admission contract
can stop dispatch only under its approved evidence and source conditions.

No live cloud inventory, secret, private dataset, model experiment, deployment
or new operational authority was used or granted in this authoring task.
The original [dated architecture views](../../../../architecture/README.md)
remain historical and are not overwritten.

## Original Composition And Icon Rights

The supplied
[conversation knowledge-mining reference](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/idea/unlock-insights-from-conversational-data)
and [multimodal processing reference](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/idea/multi-modal-content-processing)
guide the numbered-flow/labelled-service composition only. Their diagrams,
services and customer facts were not copied.

Existing icons are unchanged selections from the documented
[V24 source pack](../../../../architecture/assets/README.md).
The [official icon terms](https://learn.microsoft.com/en-us/azure/architecture/icons/)
were checked on 8 November 2026; the page offers V25 and permits architectural,
training and documentation use. The additional unchanged selections are:

| Local file | V25 archive member | SHA-256 |
| --- | --- | --- |
| [iot-hub.svg](./icons/iot-hub.svg) | `Azure_Public_Service_Icons/Icons/iot/10182-icon-service-IoT-Hub.svg` | `919f07454d5648351455a60965a443c83b51e1f725ab70478d5f579349a29649` |
| [event-hubs.svg](./icons/event-hubs.svg) | `Azure_Public_Service_Icons/Icons/analytics/00039-icon-service-Event-Hubs.svg` | `55187fecea1de7b135e53cc100bc765ad06ab419365263456bf548906c3107f8` |

V25 archive URL:
`https://arch-center.azureedge.net/icons/Azure_Public_Service_Icons_V25.zip`;
SHA-256 `f293d99252b3638557dd08ccbff9f2529083473d39b373fb2af29a7200351339`.
Icons retain their source bytes and aspect ratios, with no recolouring,
crop, flip or rotation. Neutral shapes represent people and product
responsibilities. These permitted assets do not clear unrelated original
deck images for a new external publication.
