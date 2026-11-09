---
title: Zava Forward Architecture Views
description: Current capstone application and Azure reference views, with preserved dated architecture diagrams and explicit source/implementation limits
ms.date: 2026-11-08
ms.topic: concept
---

## Scope and Reading Order

For the current 8 November capstone application and Bicep-grounded reference
views, use the [new diagram package](../capstone/source/diagrams/architecture/text-equivalent.md):
an original [CxO application concept](../capstone/source/diagrams/architecture/cxo-architecture.svg)
and [full Azure reference](../capstone/source/diagrams/architecture/azure-architecture.svg).
The full editable model includes a core frame for appendix B10/page 38 and
separate device, operations, production/background and resident options.
Its [wide deployment projection](../capstone/source/diagrams/architecture/azure-deployment.svg)
is a second frame in the same model, used on new main slide 13. It includes
the sensor-to-SQL chain, shared-API telemetry/averages responsibility,
resident website, support services and gated options at presentation scale.
It is source-grounded, not a fresh cloud inventory, adoption or compliance
acceptance. The tagged diagrams below now include the same 8 November
continuation; original 14 October generators and validation evidence are
preserved unchanged.

For issue #441, the separate
[UNREGISTERED resident service proposal](../../.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/resident-service-unregistered-proposal.md)
records owner-selected Option B, a portal/workflow increment before the
independently gated resident-answer task. It includes editable Excalidraw,
same-model SVG/Chrome PNG and accessible text. Its ID is null; it is not a
numbered/finalized ADR, native PNG export or deployed portal. Registration
acceptance remains UNMET, with supported allocator/bootstrap deferred.
Named review is default; the selected bounded routine exception is proposed
but OFF pending separate authority/evaluation/release. OD-52-55 remain open.
The original executive "no resident portal needed" and staff-assisted
topology describe their historical baseline, not current proposal exclusion.
No existing ADR or runtime is changed. The refreshed executive asset includes
a separate website while preserving assisted choice and the proposal gates.

For issues #200/#201, use the dated
[cut-over evidence pack](./cutover-evidence-pack.md), its
[row-level parity audit](./cutover-parity-audit.tsv) and
[remaining-reference inventory](./cutover-reference-inventory.tsv).
The pack preserves the original failed bootstrap, later bounded continuations
and unchecked historical gates. Its
[2026-10-27 retirement record](./cutover-evidence-pack.md#owner-authorized-directory-retirement-2026-10-27)
records the owner's later cut-over sign-off and archive `v0.21.0`, not a new
deployment or whole-issue acceptance. The original cut-over evidence remains historical; the diagram delivery
views now add the dated source continuation without rewriting that evidence.

These are two views of the same solution, not two alternative architectures.
Their retained core layout describes the sources on
[PR #68](https://github.com/jmservera/ama/pull/68) at
`062434a1fedbf6a87d1374c767c2bf0a11491ab6`, using the dated 14 October
handover for the exercise. The lower 8 November continuation adds
source-coded telemetry and read-only analysis, plus explicitly gated
averages persistence and resident integration targets. Current source
paths and SHA-256 hashes are embedded; original layout IDs, icons and
bindings are retained. These are not a fresh inventory, deployment or
production approval.

| Audience | Editable source | Vector preview | High-resolution image |
| --- | --- | --- | --- |
| CEO, CFO and executive sponsors | [Executive Excalidraw](./zava-forward-executive-architecture.excalidraw) | [Executive SVG](./zava-forward-executive-architecture.svg) | [Executive PNG](./zava-forward-executive-architecture.png) |
| CTO and technical architects | [Technical Excalidraw](./zava-forward-technical-architecture.excalidraw) | [Technical SVG](./zava-forward-technical-architecture.svg) | [Technical PNG](./zava-forward-technical-architecture.png) |

Open the `.excalidraw` file in Excalidraw or a compatible local editor. Boxes,
text and arrow bindings are native and editable; service icons are embedded
SVG images, not a flattened architecture picture. Related service labels,
icons and bodies are grouped. Read the technical image at full size or zoom
in the editable drawing rather than reducing it to a presentation thumbnail.

The executive view is intentionally a logical solution overview including
people. Its outer frame is not a network boundary. The technical resource
group and Container Apps environment boundaries are distinct; PaaS services
are not presented as VNet-hosted applications.

## Presentation Adaptation

The [24-slide capstone working deck](../../.copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/slide-deck/zava-forward-executive-draft.pptx)
adapts these materials into native editable PowerPoint architecture on
slides 10, 19, 23 and 24. The executive view remains on the main route;
runtime, operations and deferred topology use readable optional slides
rather than a reduced full technical image.
[Presentation handover and previews](../capstone/README.md)
record the UX improvements, source mapping and remaining human checks.
The Excalidraw sources retain their original core IDs and editing authority,
with a dated continuation rather than a rewritten historical generator.
The current 55-page deck uses the application concept on page 12, full
deployment projection on page 13 and reference core on page 38.
A presentation adaptation is not a new deployment or decision.

## Executive Architecture

![Executive architecture: staff Container Apps Workbench, SQL/Blob and conditional AI under human approval; a gated home sensor route via IoT Hub/Event Hubs into validated SQL telemetry/history and on-read exercise averages, with gated targets for persisted averages and Quality linkage; a separate resident showcase with separately supplied SQL, gated shared-case identity and optional public Sweden Central AI outside the core.](./zava-forward-executive-architecture.svg)

### Legend

* Solid green arrows: interactions documented for the existing core.
* Blue dashed arrows and blue cards: configured dependencies.
* Purple dashed model path: conditional assistance, not standing autonomy.
* Human cards: resident choice and accountable staff approval, not Azure
  services or automated agents.

### Key Relationships

Staff assist residents without requiring digital participation. A distinct
resident website offers own-case access and assisted choice; its shared-case
managed external identity is a gated target, not staff enrolment.
Microsoft sign-in
and service-side permissions protect the workbench. One API hosts the workflow
and five bounded assistants; SQL retains controlled records and proposals,
while Blob holds document files. AI returns drafts for review, not consent,
quality acceptance, bookings, work release, funding submission or payment.

The five capabilities are stock prioritisation, assessment preparation,
funding evidence, works/resident coordination and quality evidence.
They are not five applications or five autonomous programme managers.
Normal five-assistant authority is absent and proactive scans are off after
the finite operator QA. Other existing AI draft routes are not being declared
disabled by that statement.

The intended outcome is less chasing and fewer evidence gaps without
weakening resident choice or independent review. It is a value hypothesis:
the operator model paths and persistence checks do not measure business
benefit.

Home sensors feed Basic B1 IoT Hub and the dedicated Event Hubs transport.
The source-coded finite API intake validates and deduplicates accepted
readings into restricted Azure SQL history; rejected input has owned DQ.
The shared-API telemetry/averages responsibility reads retained rows and
trusted consent. Exercise window means are computed on read. Persisted
per-home averages in that existing API/SQL boundary are the owner-requested
target, separately gated and not implemented. There is no new ADX, Fabric
or standalone analytics worker. Averages support context/manual review,
not diagnosis, consent, quality acceptance or safety release.
The current quality-evidence helper uses measures, checklists and document
evidence; sensor linkage to Quality Verification is proposed, not delivered.
The retained-analysis/comparison functions are reusable core code, not proof
of a served API analysis endpoint, scheduler or Workbench sensor integration.

The following text topology preserves the executive drawing's component and
relationship structure:

```mermaid
flowchart LR
    staff["Staff assist residents"] --> api["Container Apps workbench and workflow"]
    entra["Microsoft Entra ID"] -. configured sign-in .-> api
    people["People own approval"] --> api
    api --> sql[("Azure SQL: cases, audit, proposals")]
    api -. configured documents .-> blob[("Azure Blob: files")]
    api <-. conditional scoped drafts .-> model["Azure OpenAI"]
    homes["Home sensors: live use gated"] -.-> hub["Basic B1 IoT Hub"]
    hub -. Hub identity route .-> events["Dedicated Event Hubs"]
    events -. finite receive adapter .-> telemetry["Shared-API telemetry / averages service"]
    telemetry <--> history[("SQL readings / delivery / DQ history")]
    telemetry --> analysis["Read-only history / exercise averages on read"]
    analysis -. target persistence / quality linkage gated .-> api
    resident["Separate resident website: own-case / assisted choice"] -.-> residentSql[("Independently supplied showcase SQL")]
    resident -. optional / default OFF .-> residentAi["Public Sweden Central model: outside core"]
```

## Technical Architecture

![Technical architecture: Entra/browser entry, shared API, SQL/Blob, Foundry, network/monitoring controls and deferred workloads; gated IoT Hub/Event Hubs sensor receipt into validated SQL telemetry/history and on-read exercise averages, with gated targets for persisted averages and Quality linkage; a separate resident site with independently supplied SQL, gated external identity/shared-case integration and optional public Sweden Central AI outside the core.](./zava-forward-technical-architecture.svg)

### Legend

* Green: core implementation or interaction documented in the dated handover.
* Blue: configuration or infrastructure-source relationship, not an assertion
  that every path has been independently accepted.
* Purple: conditional connector or assistant path requiring effective
  authority, permissions or setup.
* Amber: deferred design. Worker images remain placeholders; the five
  assistants do not run through those queues.
* Arrowheads show the initiator/dependency direction. Responses are implicit;
  the double-headed model link shows context out and drafts/usage back.
* A grouped diagnostics path represents resource/container diagnostic settings
  to Log Analytics; it is not proof of full application tracing.

### Key Relationships

| Interaction | Contract and boundary | Evidence |
| --- | --- | --- |
| Browser -> sign-in -> protected app | Existing Entra registration; EasyAuth verifies identity. Selected design (owner decision 2026-10-24, [ADR 0002](../adrs/0002-pilot-readiness-architecture.md#entra-authoritative-staff-access-owner-decision-2026-10-24-refs-360)): the API takes tenant, object id and app roles from the validated principal with no SQL staff lookup, then enforces case scope and fields; the serving revision is verified separately. `/` is public; `/app` and data APIs are protected. | [Container Apps/auth](../../infra/modules/containerapps.bicep), [auth provider](../../src/api/src/zava_forward/api/auth.py) |
| Ingress -> API | HTTPS ingress targets port 8088; `/healthz` is the implemented probe. The Python server serves the UI and APIs in one deployment. | [Container Apps](../../infra/modules/containerapps.bicep), [server](../../src/api/src/zava_forward/api/server.py) |
| API -> SQL | Managed-identity access; controlled workflow, audit and proposal state. Five-assistant deduplication, reservations and fenced claims use short transactions; inference occurs outside database locks. | [SQL module](../../infra/modules/sql.bicep), [SQL adapter](../../src/core/src/zava_forward/core/mssqlstore.py), [assistants](../../src/core/src/zava_forward/core/assistants.py) |
| API -> Blob | The document adapter transfers bytes to the `evidence` container; SQL retains references and content hashes. Five-assistant capture uses permitted metadata, not arbitrary document contents. | [Document adapter](../../src/core/src/zava_forward/core/documents.py), [storage](../../infra/modules/storage.bicep), [capture allowlists](../../src/core/src/zava_forward/core/assistants.py) |
| API -> model -> proposal | Direct Azure OpenAI chat-completions calls from the API managed identity. Foundry account/project and `standard`/`capable` deployments provide models, not a deployed Foundry Agent Service orchestrator. Citation/schema validation precedes storage. | [AI client](../../src/core/src/zava_forward/core/ai.py), [Foundry](../../infra/modules/foundry.bicep), [ADR 0002 runtime](../adrs/0002-pilot-readiness-architecture.md#five-assistant-exercise-runtime-2026-10-13) |
| Human -> proposal review | Current permission, source, version and status are rechecked. Source verification precedes acceptance/edit. Review updates proposals/audit, not controlled domain approvals. | [Assistants](../../src/core/src/zava_forward/core/assistants.py), [five PRD contracts](../prds/zava-forward-retrofit-programme-demonstrator.md#five-reactive-and-proactive-assistants-2026-10-13) |
| EasyAuth -> token Blob; renewal -> vault | A separate private `auth-tokens` store holds delegated tokens. The daily 03:00 UTC job obtains a five-day user-delegation SAS and updates one vault secret. EasyAuth uses that reference; no browser token retrieval. | [Token-store module](../../infra/modules/authTokenStore.bicep), [renewal implementation](../../src/orchestrator/src/zava_forward/orchestrator/token_store.py) |
| API -> Graph; browser -> tile provider | Graph receives the current user's delegated `User.Read` token for `/me/photo/$value`; photo bytes, not tokens, return to the browser. The browser fetches configured map tiles separately; there is a list/cluster alternative. | [Photo proxy](../../src/core/src/zava_forward/core/profile.py), [server](../../src/api/src/zava_forward/api/server.py), [browser](../../src/api/src/zava_forward/api/web/app.js) |
| Workloads -> ACR; operator -> deployment | Images pull using workload identities. Operator builds/deploys are distinct from GitHub CI's tests, non-root image checks, scan and SBOM. No automatic Azure deployment is implied. | [Registry](../../infra/modules/registry.bicep), [CI](../../.github/workflows/mvp-ci.yml), [operator handover](../../infra/README.md#five-assistant-version-current-handover) |
| Diagnostics/metrics -> operations | Resource/container diagnostics and SQL audit target Log Analytics. Application Insights is workspace-linked and its connection string is supplied; full structured traces are not established. API/model/SQL alerts target the action group. | [Monitoring](../../infra/modules/monitoring.bicep), [alerts and budget](../../infra/main.bicep) |
| Budget -> notification | 80% actual and 100% forecast alerts notify the configured email; this is not a hard spending stop. Shared assistant reservations and effective scoped authority are separate controls. | [Budget](../../infra/main.bicep), [assistant limits](../../src/agents/README.md#operator-authority-and-finite-allowance) |
| Deferred schedule/queues/workers | Five-minute orchestrator -> `agent-tasks` -> separate agents; `import-jobs` -> import job -> limited SQL role and Blob quarantine. Agent/model and API/checkpoint paths are proposed contracts, not working placeholder code. | [Deferred workload definitions](../../infra/modules/containerapps.bicep), [ADR 0001](../adrs/0001-azure-architecture.md#decisions) |
| Conditional M365 -> workbench boundary | SharePoint/Excel imports are proposed, one-way and permission-gated. `Sites.Selected` plus a site grant is not the own-photo `User.Read` permission. Teams Workflows is an optional operations webhook, never an approval or safety-response path. | [M365 design](../adrs/0001-azure-architecture.md#m365-configuration-integration-and-use), [site grant](../../infra/scripts/grant-sharepoint-access.sh), [action group](../../infra/modules/monitoring.bicep) |
| Home sensors -> IoT Hub -> Event Hubs -> shared-API intake | Basic B1/private Hub; Hub MI uses the trusted-service route to dedicated Event Hubs. The finite SDK adapter initiates receive over the Event Hubs PE. Live routing, mapping, calibration, consent and method acceptance remain separate. | [Hub and transport](../../infra/modules/iothub.bicep), [finite SDK adapter](../../src/api/src/zava_forward/api/iot_stream.py), [API intake](../../src/api/src/zava_forward/api/sensor_ingestion.py) |
| Telemetry service -> SQL history / read-only averages | Validated idempotent readings and restricted delivery/DQ history are retained. Analysis reads trusted consent and rows; exercise means are computed on read. The named telemetry/history/averages service is a shared-API capability backed by existing SQL; persisted averages are a gated target, not a new schema or deployed worker. | [SQL consumer](../../src/core/src/zava_forward/core/sensor_consumer.py), [retained analysis](../../src/core/src/zava_forward/core/sensor_analysis_store.py), [exercise means](../../src/core/src/zava_forward/core/synthetic/sensor_scenarios.py), [current quality-helper categories](../../src/core/src/zava_forward/core/assistants.py#L47) |
| Separate resident website -> independently supplied dependencies | Own-case scope and assisted choice are distinct from staff login. Showcase SQL is independently supplied, not proved to be shared staff SQL. Optional public Sweden Central AI is off by default and outside the core/private/UK inference claim. Managed external identity/shared-case integration remains a gated target. | [Resident deployment](../../infra/resident-demo.bicep), [resident preview fields](../../src/core/src/zava_forward/core/resident_preview.py), [optional model](../../infra/resident-assistant.bicep) |

The reduced text topology below groups supporting resource declarations.
The Excalidraw view carries the detailed service labels, statuses and routes.

```mermaid
flowchart TB
    browser["Staff browser"] -. sign-in .-> entra["Entra registration and roles"]
    browser --> auth["HTTPS ingress and EasyAuth"]
    entra -. issuer and roles .-> auth
    browser -. tile images .-> tiles["Configured map tile provider"]
    subgraph rg["ama: UK South development exercise"]
        identities["Per-workload managed identities"]
        vault["Key Vault: auth secret and token SAS"]
        subgraph aca["Container Apps environment"]
            auth -. verified principal .-> api["Single API: workflow and five shared assistants"]
            renewal["Daily token SAS renewal job"]
        end
        api --> sql[("SQL retrofit: domain and proposal state")]
        api -. document bytes .-> blob[("Blob evidence")]
        api <-. scoped context and model output .-> model["Foundry account/project and Azure OpenAI deployments"]
        vault -. secret references .-> auth
        auth -. SAS access .-> tokens[("Separate auth-token Blob")]
        renewal -. delegation key .-> tokens
        renewal -. one-secret rotation .-> vault
        api -. identity image pull .-> acr["Container Registry"]
        sql -. diagnostic settings .-> logs["Azure Monitor / Log Analytics"]
        insights["Application Insights"] -. workspace link .-> logs
        model -. metric alerts .-> ops["Action group and budget notifications"]
        network["VNet / NSGs / private endpoints / DNS / AMPLS"]
    end
    api -. delegated own-photo request .-> msgraph["Microsoft Graph"]
    subgraph deferred["Deferred; not the five-assistant runtime"]
        orchestrator["Five-minute orchestrator placeholder"] -. enqueue .-> queues[("Task/import/poison queues")]
        queues -. KEDA .-> agents["Agent app placeholder"]
        queues -. import event .-> importer["Import job placeholder"]
        agents -. context and proposal contract .-> api
        agents -. model invocation .-> model
        orchestrator -. checkpoints through API .-> api
        importer -. limited SQL role .-> sql
        importer -. quarantine .-> otherblob[("Same Blob account: other containers")]
        edge["Optional production Front Door/WAF; historical #344 deployment"]
    end
    m365["SharePoint/Excel: proposed; Teams: optional"] -. snapshot import .-> importer
    ops -. optional Teams Workflows .-> m365
    homes["Home sensors: synthetic today / live gates"] -.-> hub["Basic B1 IoT Hub"]
    hub -. Hub MI trusted-service route .-> eventhub["Dedicated Event Hubs"]
    telemetry["Shared-API finite telemetry intake"] -. API initiates receive via PE .-> eventhub
    telemetry --> sql
    analysis["Read-only retained history / averages on read"] --> sql
    averageTarget["TARGET: persist per-home averages in existing API / SQL"] -. gated .-> sql
    resident["Separate resident website: own-case / assisted choice"] -.-> residentSql[("Independently supplied showcase SQL")]
    resident -. optional / default OFF .-> residentModel["Public Sweden Central AI: outside core"]
```

## State, Trade-Offs and Known Limits

The retained 14 October exercise record names `ca-forward-test-api--0000012`,
runtime source `cd14b3b379026a87ebfa3e9058ac10c0df7888eb`. The handover records
five real operator model paths and independent SQL-content/restart proof,
not a staff-browser acceptance session, calibrated semantic quality or benefit.
No cloud read, paid model call, new authority or resource change was performed
to create these diagrams.

The diagrams do not depict sensor ingestion. The simulator-only humidity and
temperature capture path, deterministic review signal and proposed map overlay
are documented in
[ADR 0002](../adrs/0002-pilot-readiness-architecture.md#sensor-data-capture-analysis-and-map);
they are not implemented or represented as deployed integrations here.

* The existing API/SQL proposal service is the current implementation.
  Separate queue workers would add deployment, failure and permission
  boundaries; they remain deferred rather than being drawn as necessary
  infrastructure for the five capabilities.
* These drawings retain the historical exercise hosting and its documented
  development network exceptions, not the proposed #360 direct-demo rollout.
  Bicep declares VNet integration, two subnets, NSGs, private endpoints and DNS.
  Public access is also allowed in development. The default production
  profile and intended Front Door public edge/private backend are not the
  observed exercise.
  Network ranges in the drawing are IaC defaults, not newly measured routes.
* Owner decision 2026-10-16 (Refs #360): the synthetic demo uses direct
  Container Apps HTTPS with Entra browser sign-in, not a mandatory Front Door.
  The [migration proposal](../../infra/README.md#direct-demo-ingress-migration-proposal-2026-10-16-360)
  creates a separate external environment/subnet and suffixed apps/jobs,
  retaining private backing services and identities. Default/production
  isolation and the optional edge path remain unchanged. This is offline
  configuration, not a live diagram update or observed sign-in; owner migration/
  cost approval, SQL/AI proof and retirement authorization remain open in the
  [cut-over audit](./cutover-evidence-pack.md#direct-demo-ingress-offline-scope-2026-10-16).
* SQL append-only events and a hash chain are not proof of the proposed
  immutable external digest anchor. The `audit-archive` policy is defined
  unlocked in Bicep; the application does not implement/verify the complete
  anchoring workflow.
* `EVIDENCE_STORE=sharepoint` is a topology parameter, not an implemented
  SharePoint document adapter. The current adapter chooses local or
  `azure-blob`; diagrams do not claim that setting a parameter creates a
  connector.
* The earlier ADR 0001 API identity table excludes model invocation for the
  separate-runner design. `enableApiAi=true` and ADR 0002 deliberately provide
  the current API's direct model path. This is a dated topology distinction,
  not proof that the original table applies unchanged to the MVP.
* Bicep scale settings are design/configuration, not a new capacity test.
  Model failure preserves manual work; SQL failure can block controlled writes.
  Token-renewal failure requires action before SAS expiry. Safety intake must
  have its own named human route, not depend on AI or Teams.

No significant new architectural choice is made by these views; existing
[ADR 0001](../adrs/0001-azure-architecture.md) and
[ADR 0002](../adrs/0002-pilot-readiness-architecture.md) retain decision history.

## Complete Capstone Guide Check

Checked against the complete [assessment guide](../reference/method/ama-capstone-assessment-guide.md),
not only its architecture criteria. This is a source/communication check,
not an official score, independent stakeholder review or panel acceptance.

| Criterion | Diagram contribution and remaining evidence |
| --- | --- |
| A1 Architecture | Explicit single-runtime and deferred boundaries; scale settings are configuration, not performance proof. |
| A2 Trade-offs | Existing lean API versus deferred workers; private production target versus current development; ADR alternatives retained. |
| A3 Governance | Identity, field/case gates, human approvals, network exceptions and AI scope shown; legal/privacy and production approvals remain separate. |
| A4 Completeness | Working core is distinguished from placeholders and conditional connectors; no blanket end-to-end acceptance. |
| A5 Operations | Diagnostics, renewal, failure domains, alerts and budget semantics shown; measured SLOs/unit economics remain open. |
| A6 AI evaluation | Direct model path and typed/cited proposals shown; model benefit and semantic calibration are not inferred from five successful calls. |
| A7 Autonomy | Five assistants are bounded proposal services; proactive OFF and absent standing authority are explicit. |
| B1 Narrative | Executive view centres one accountable workflow, not a service catalogue; live narrative delivery is unobserved. |
| B2 Audience | Separate executive and CTO views of the same architecture; audience comprehension is not independently tested. |
| B3 Demo | Figures can explain the control boundary; no live demo or recovery is manufactured. |
| B4 Q&A | Sources and unknowns support challenge; actual composure/depth require observed Q&A. |
| B5 Delivery | No rehearsal, timing or presenter performance follows from diagram creation. |
| B6 Written craft | Editable sources, previews, text equivalents and source-linked interaction contracts; native editor/render checks retained. |
| B7 Evidence | PR baseline and dated handover are distinguished from target design; benefit remains a hypothesis. |
| C1 Discovery | Staff, residents, professional and Finance authority remain distinct; company facts are not invented. |
| C2 Listening | Owner-requested format and audiences honoured; no stakeholder dialogue/acceptance simulated. |
| C3 Honesty | Public-network, deferred-code, telemetry, audit and AI-acceptance limits are disclosed. |
| D1 Substance | These explain the project; they are not a separately completed thought-leadership artifact. |
| D2 Craft | Diagram publication does not establish a separate artifact's publish-readiness. |
| D3 Reach | Committing diagrams is not evidence of external dissemination or reviewer acceptance. |

Section floors A >= 21/35, B >= 21/35, C >= 9/15 and D >= 9/15, no individual
criterion scored 1, thought-leadership submission and required masterclasses
remain separate requirements. No floor clearance is claimed.

## Icon Provenance and Editing

Azure images are unmodified SVGs from Microsoft's
[official architecture icon pack](https://learn.microsoft.com/en-us/azure/architecture/icons/),
`Azure_Public_Service_Icons_V24.zip`, retrieved 14 October 2026. Microsoft
permits copying/distribution/display for architecture diagrams, training and
documentation; other rights are reserved. Product names stay adjacent, aspect
ratios are preserved, and icons are neither cropped, flipped nor recoloured.
Custom application modules and people are not represented as Microsoft
products.

[Asset provenance](./assets/README.md) identifies each selected icon.
The authoring script and source manifest are retained in the dated
[working folder](../../.copilot-tracking/architecture-diagrams/2026-10-14/zava-forward/).
Native Excalidraw sources are the editing authority; SVG/PNG are previews.
Both were exported locally through Excalidraw, without uploading repository
content to a third-party drawing service.

[Authoring and validation evidence](../../.copilot-tracking/architecture-diagrams/2026-10-14/zava-forward/validation.md)
records native group/arrow editing, browser layout checks, icon integrity,
preview dimensions and delivery hashes.

The [8 November continuation builder](./update-architecture.mjs) starts from
the committed original artifacts at `b671116d`, not from a rewritten
historical script. It keeps original element IDs, embedded icon bytes and
existing arrow bindings, replaces retired source locators and adds native
editable nodes/edges. The
[current validation receipt](../../.copilot-tracking/architecture-diagrams/2026-11-08/zava-forward/validation.json)
records local CLI 0.3.0 render dimensions/hashes and geometry checks. Current
preview outputs were staged in that dated directory, visually reviewed and
then copied to the delivery paths. No account, upload, live cloud lookup,
infrastructure adoption or runtime change was used.

After local native SVG export, run
`node docs/architecture/annotate-previews.mjs <render-directory>` to attach
the title, accessible text equivalent and exact native-file hash without
changing render geometry. This restores the preview's accessible SVG
semantics; it is not a new accessibility conformance acceptance.
