---
title: Progressive Excalidraw Architecture Views
description: Seven slide-sized editable diagrams, text alternatives, legends and PowerPoint build guidance
ms.date: 2026-10-23
ms.topic: reference
---

## Reading and Editing

Every drawing is exactly 1600x900, the PowerPoint 16:9 aspect ratio.
Open its `.excalidraw` file in a compatible local editor. Boxes, text and
arrows are native elements; official Azure icons are embedded SVG files.
No network fetch is needed to display the icons. SVG/PNG previews carry the
same geometry; do not use them as the editing source.

These are curated static source views of the exercise, not live inventory.
Keep "configured", "gated", "historical", "proposed" and "not tested" labels.
A service icon does not prove deployment. Logical diagrams do not establish
network isolation. No Foundry Agent Service, API gateway, universal cache,
active separate agent worker or live IoT connection is implied.

## Slide Map

| View | Main / backup use | Editable source | Preview |
| --- | --- | --- | --- |
| 01: the idea | S04 | [Excalidraw](./01-the-idea.excalidraw) | [SVG](./01-the-idea.svg) / [PNG](./01-the-idea.png) |
| 02: AI placement | S06 | [Excalidraw](./02-ai-placement.excalidraw) | [SVG](./02-ai-placement.svg) / [PNG](./02-ai-placement.png) |
| 03: runtime | S10 | [Excalidraw](./03-runtime.excalidraw) | [SVG](./03-runtime.svg) / [PNG](./03-runtime.png) |
| 04: controlled AI flow | B07 / B21 / demo | [Excalidraw](./04-controlled-ai-flow.excalidraw) | [SVG](./04-controlled-ai-flow.svg) / [PNG](./04-controlled-ai-flow.png) |
| 05: operations | B16 | [Excalidraw](./05-operations.excalidraw) | [SVG](./05-operations.svg) / [PNG](./05-operations.png) |
| 06: sensor target | B19 | [Excalidraw](./06-sensor-target.excalidraw) | [SVG](./06-sensor-target.svg) / [PNG](./06-sensor-target.png) |
| 07: Tokenomics | S11 / B25 | [Excalidraw](./07-tokenomics.excalidraw) | [SVG](./07-tokenomics.svg) / [PNG](./07-tokenomics.png) |

## Shared Legend

* Deep green text and solid rails: application, human or logical workflow
  relationships described in the sources, not a fresh deployment test.
* Pale blue: evidence, identity or configured dependencies.
* Pale purple: bounded model assistance.
* Amber and dashed boxes: unknown, proposed or deferred work. Read the words;
  colour alone is not the status.
* Dashed runtime arrows: configured or conditional dependencies, not evidence
  that every current connection passed live acceptance.
* Arrowheads show the request/dependency or workflow direction. Responses
  are implicit unless the text says otherwise.

## The Idea Architecture

### Text Alternative and Key Relationships

Residents choose and staff own the case; professionals approve. They use a
controlled Container Apps workbench. Workflow keeps commitments, deterministic
rules enforce boundaries and AI prepares source-bound help. Azure SQL retains
cases and audit; Blob retains files. Unknown stays unknown. Generative drafts
and typed decisions enter a review queue, not an approval. The surrounding
page is not a network boundary.

Three clicks if helpful: people; workbench/evidence; bounded AI. The entire
static slide must be understandable with no animation.

## AI Placement Architecture

### Text Alternative and Key Relationships

Three distinct tools serve different tasks. Rules apply explicit policy,
arithmetic, eligibility, freshness, consent requirements and work-release
conditions. A learned decision model scores supplied candidates for form
selection or evidence-support screening and can abstain. Generative AI drafts
source-bound explanation. All routes retain current evidence and authority;
models produce proposals, not permission. Decision 1 is not the deterministic
workflow engine, and no cost/latency advantage has been established.

Reveal left to right, then the common boundary. No arrow implies that all
tasks must call all three tools.

## Runtime Architecture

### Text Alternative and Key Relationships

A staff browser reaches the Container Apps API. Entra/EasyAuth provides
identity; the API separately enforces role, case and field scope. The API
hosts workflow and five bounded assistants. SQL stores cases, proposals and
audit. Blob stores files with SQL references/hashes. The gated model call
returns an unreviewed output and usage where available. Direct Azure OpenAI
and a separately gated Decision 1 candidate path are not a deployed Foundry
Agent Service orchestrator. Current live acceptance is separate.

Show the browser/API/SQL rail first. Add identity, models and files second.
The model link means request and implicit response; it is not a model writing
directly into SQL. The Blob arrow is initiated by the API, not the store.
Do not add network walls to this logical view.

## Controlled AI Flow Architecture

### Text Alternative and Key Relationships

Capture current role/case scope, permitted evidence and source/version IDs.
Make a bounded model call outside the database lock. Validate schema,
citations and freshness; reject or retain explicit errors rather than fabricate
a success. Store a valid output as unreviewed. A person checks the source and
current permissions; a separate domain action still needs its own authority.
Model failure, disabled assistance or exhausted allowance leaves owned manual
work. Hazards bypass the optional AI path. Citation presence is not semantic
truth.

Use four appears for explanation; keep the failure strip always visible.
Do not animate a token stream to imply fresh inference.

## Operations Architecture

### Text Alternative and Key Relationships

Access uses Entra, managed identities and Key Vault references. Source
configuration includes private backing services. Container Apps, Registry and
CI form the runtime/release picture; Monitor/Log Analytics and scoped usage
support operations. An Azure budget alert is a notification, not a spending
stop. Expansion requires genuine sign-in/role denial, SQL persistence,
task-bound inference, restore/recovery, human acceptance and current costs/
terms. Whole-system recovery and production readiness are not established.

This is a responsibility/control view, not a deployment/network topology.
No connectors are needed: the three columns are concerns, not request hops.

## Sensor Target Architecture

### Text Alternative and Key Relationships

A device or explicitly labelled simulator uses a distinct identity and stable
reading ID. The target transport is Azure IoT Hub Basic, device-to-cloud only
for the exercise. The API validates mapping/time and appends idempotently to
SQL, with owned data-quality exceptions. A derived deterministic signal may
request human review; it does not diagnose a hazard or change priority.
Missing data is insufficient. All telemetry boxes and arrows are dashed
because this end-to-end live path is not accepted. A solid separate human
safety route handles resident reports independently.

Do not label a simulator or finite offline consumer as deployed telemetry.
No new IoT threshold, device credential or operational legal claim is supplied.

## Tokenomics Architecture

### Text Alternative and Key Relationships

Observe historical usage: 6,884 tokens in five operator runs with no human
acceptance. Account for inference, attributable hosting, review/correction,
assurance and support. Divide by an agreed human-accepted proposal count
above a quality floor; that unit cost is unknown today. Existing finite
call/token/expiry controls and partial usage capture are not money caps.
Complete metering, currency/task/period budgets and per-request call/depth
limits are proposed and untested.

The arrows explain the economic measurement method, not implemented billing
integration. Reveal the unknown denominator at the same time as the token
number. Never let the observation appear to be a measured price.

## Azure Icon Provenance

The bundled icons preserve Microsoft's bytes and aspect ratios. Most are
copied byte-for-byte from the repository's 2026-10-14 selection from
`Azure_Public_Service_Icons_V24.zip`; IoT Hub was extracted from the same
official pack on 2026-10-23. The official icon/terms page was freshly retrieved
on 2026-10-23:
<https://learn.microsoft.com/en-us/azure/architecture/icons/>.

Microsoft permits use, copying, distribution and display in architecture
diagrams, training materials and documentation; other rights are reserved.
Do not crop, flip, rotate, distort or use a service icon for the custom product,
Decision 1 or a person. Azure OpenAI, Foundry, Container Apps, SQL, Storage,
app registration, Key Vault, Monitor, Cost Management and IoT Hub icons retain
their product meanings.

Official IoT path:
`Azure_Public_Service_Icons/Icons/iot/10182-icon-service-IoT-Hub.svg`.
Other original paths are recorded in the source register's E06 provenance.
