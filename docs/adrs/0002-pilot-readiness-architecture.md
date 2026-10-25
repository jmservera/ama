---
title: ADR 0002 Pilot-Readiness Architecture for the Zava Forward MVP
description: Proposed decisions for moving the working MVP to pilot readiness over about 60,000 homes - durable store, Blob, Entra ID and field visibility, deterministic ranking, map scale, deployment and gated staff time capture
author: AMA programme
ms.date: 2026-10-24
ms.topic: reference
---

## Status

Proposed. This ADR records proposals by the AMA programme. It does not record
approval by the owner, the DPO, Legal, the Board, control owners or any
customer role. Where the owner has given direction, the text says so and cites
the source; everything else is a proposal. No real resident data may be loaded
until the open items in [Open items](#open-items) are closed (DH-002, DH-006).

This ADR amends [ADR 0001](./0001-azure-architecture.md) for the MVP. It does
not replace the ADR 0001 demonstrator design for the agent, orchestrator and
import workloads, which remain deferred.

The owner accepted the bounded staff identity and application-role decision
on 2026-10-24 in
[Entra-authoritative staff access](#entra-authoritative-staff-access-owner-decision-2026-10-24-refs-360).
That decision replaces the SQL staff-binding prerequisite for staff sign-in;
it does not accept this ADR as a whole or establish implementation, deployment,
human acceptance or operational approval.

### Private Publisher Capacity Delta (2026-10-19, Refs #360)

The new owner direction authorizes necessary resource operations inside existing
`ama`, never deletion of the group, public backing access or tenant authority.
The [bounded runbook](../../infra/README.md#bounded-private-publisher-capacity-attempt-2026-10-19-refs-360)
and [evidence delta](../architecture/cutover-evidence-pack.md#bounded-rg-publication-continuation-2026-10-19)
record fresh exact provider preflight refusals for both B2als_v2 and D2as_v5 in
UK South. Their unrestricted SKU GET and available quota did not establish
capacity; no publisher was allocated. The private-pool preview region list
does not establish UK South support. The tested temporary VM allocation
template is an undeployed candidate, not a new accepted production architecture.

No image was published/pulled/run/pinned, no initializer/settings/identity change
or secret-preservation round-trip occurred, and no SQL/application/private data
was read. Current direct HTTPS routes remain deny-all403. Existing application
credentials lack Graph permission hints and failed bounded application
discovery, so #349 tenant/interactive acceptance remains separate. #360d/e and
real SQL/AI/browser/role evidence remain unmet. Existing Front Door and `ama`
are retained. Historical observations/proposals below remain dated history,
not silently revalidated live outcomes or authorization for another allocation.

Later cycle2 source disposition: the template's original unrestricted outbound
defaults were rejected. Explicit private-ACR/platform exceptions and deny-all
outbound now replace that policy, without changing inbound/private-backing or
exact-RG/resource guards. See the
[runbook policy](../../infra/README.md#explicit-outbound-restriction-2026-10-19-cycle2)
for exact addresses/ports and Azure platform exceptions. No package Internet
access, broad service-tag allow or FQDN-filtering claim is permitted. The stock
image has no proven private/offline build-tool bootstrap, so this remains a
capacity- and bootstrap-blocked source design, not an approved deployable
publisher. No new infrastructure, allocation, preflight, image/pin or live
acceptance occurred. Original adverse evidence remains unchanged.

### Source-Grounded Architecture Views (2026-10-14)

[Executive and technical Excalidraw diagrams](../architecture/README.md)
explain this ADR's current single-API exercise implementation alongside the
deferred ADR 0001 queue/worker design. They include official Azure icons,
source-linked interactions and explicit public-network, telemetry, audit,
model-authority and M365 limitations. No new architecture decision, approval,
deployment or successful acceptance test follows from these diagrams.

### Exercise Applicability (2026-10-11)

Every subsequent accepted application exercise build means a delivered AMA
prototype, PoC or MVP, including updates to this application. It must
exercise actual Azure hosting, real SQL state (existing Azure SQL realization)
and at least one registered real AI task under BRD CON-007/AC-086 and
PRD CON-009/AC-057. Preserve the generated 60,000-home stock and retained
980-case programme/history/evidence; small fixtures remain tests. Reuse
unchanged services but verify the changed build's connections and state/
audit persistence after restart. Local-only acceptance is superseded.

The context and implementation tables below are dated history/proposals.
[Pinned #58](../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11)
reports real SQL/Blob deployment and selection/generation, not full pilot
approval or every later source-tested control in the deployed revision.
Entra user login, full permissions, cloud performance/recovery and direct
human acceptance remain separate gates. No unconditional Decision-task
placement, premium topology or new spending authority is implied.
Missing effective budget/authorization blocks real-platform acceptance;
fallback keeps case access safe but cannot supply a successful delivery gate.

## Context

The `mvp/` application is a Python standard-library server. It keeps all state
in one JSON file on local disk, writes uploads to local disk, signs staff in
with one shared password, draws every open case on a Leaflet map using
OpenStreetMap public tiles, and calls Azure OpenAI through a managed identity.
On Azure Container Apps that disk is lost on restart, so it runs as one replica
and is a demonstration, not a pilot (see the
[MVP README](../../src/api/README.md) honest limits and
[Gap Analysis and Next Build](../reference/research/gap-analysis-next-build.md)).

Owner direction recorded on 2026-10-08 and now written into the
[PRD v0.10.0](../prds/zava-forward-retrofit-programme-demonstrator.md) as
PR-001 to PR-008 and DH-007:

* Load the whole stock of about 60,000 homes (PR-005, OD-17).
* Rank homes deterministically with a published, versioned policy and reason
  codes; AI prioritisation is a recommendation only (PR-006, PR-007).
* Contractors never see the reason for a vulnerability or adjustment (PR-002).
* Keep audit entries in full for the legal retention period (DH-007).
* Allow individual staff time capture only with a DPIA (PR-004, OD-36).
* AI recommends, drafts, reconciles and flags; a person approves every action
  (PR-008, OD-19).

Related requirements: FR-001 (versioned home case), FR-003 (service-enforced
role permissions), FR-005 (versioned edits), FR-012 (policy version and reason
codes), FR-025 to FR-028 (suggestions, review, citations, workflow-only
path) and FR-030 (export independent of the AI provider).

Scale note: 60,000 homes is small for a relational database. The scale problem
in the MVP is not row count but that every request works on the whole JSON
document in memory, every save rewrites it, and the map draws every point.
Decisions below fix those mechanisms, not raw capacity.

## Decisions

| Concern | Decision (proposal unless marked) | Rationale |
| --- | --- | --- |
| System of record | Azure SQL Database behind the existing `Store` interface, Entra-only authentication, in `uksouth` | Keeps ADR 0001, ACID transitions, row-version concurrency, ledger tables |
| Documents | Blob storage in `uksouth`, private, versioned, identity access only; metadata in SQL | Survives restarts and replicas; supports legal hold and immutable policies |
| Audit | Append-only SQL ledger table holding full entries; digests uploaded to an immutable Blob container with a time-based retention lock; scheduled verification | Meets DH-007 and makes the tamper-evidence claim testable |
| Sign-in | Entra ID with app roles, validated by the service; shared password removed | FR-003 and PR-002 need server-enforced identity |
| Field visibility | One server-side projection layer, default deny, per role and per field; contractor view has no vulnerability reason in any API, export, search, audit view or AI prompt | PR-002 enforced in one place and tested |
| Ranking | Deterministic function of case data and a versioned policy file, stored as a ranking snapshot with reason codes | PR-006 |
| AI prioritisation | Separate recommendation record, never read by the ranking function or any queue | PR-007, PR-008 |
| Sensor observations | Simulator-only source for the demonstration; validate and append readings in Azure SQL, derive versioned deterministic review signals, and reuse the map/review queue. Azure IoT Hub is the ingestion product per owner direction (see [ADR 0003](./0003-journey-derived-capabilities-runtime-fit.md), decision 6); no separate Event Hubs or time-series tier | Three observations per simulated day do not justify a separate streaming estate; raw readings are evidence, not diagnoses or investment scores |
| Five reactive/proactive assists | Shared versioned proposal service in the existing MVP API, with SQL-owned deduplication/reservations/fenced leases; bounded automatic execution and recipient-compatible evidence | PRD FR-047/AC-058 to AC-061; no separate estate, model authority or domain approval |
| Map | Server-side bounding-box queries with grid clustering by zoom, same filter object as the list, licensed tile provider | PR-005 |
| Deployment | Two or more replicas, zone redundant where available, `uksouth`, hardened image, scan and tests in CI | No state on the container; fixes the honesty gap |
| Staff time capture | Built behind a feature flag that is off by default and cannot be switched on without a recorded DPIA reference | PR-004 |

### Five-Assistant Exercise Runtime (2026-10-13)

The owner requested implementation of the
[five capability contracts](../prds/zava-forward-retrofit-programme-demonstrator.md#five-reactive-and-proactive-assistants-2026-10-13)
in the existing MVP. Stock, assessment, funding, works/resident coordination
and quality each have distinct source permissions, deterministic proactive
predicates and human owners. This amends the lean exercise realization;
the separate queue/agent/orchestrator estate in ADR 0001 remains proposed.
Use existing SQL/AI/API/UI rather than five applications or new resources.

Proposal identity binds capability/version, case, canonical intended proposal
identity (the registered purpose) and material dependencies; a changed intent
cannot replay an earlier proposal when dependencies are unchanged.
Reactive/proactive invocation provenance is separate. SQL owns bounded
attempts, durable allowance reservations, database-time claims and fenced
lease takeover/completion. A lost acknowledgement is reconciled by lookup.
Timeouts and missing usage preserve liability; at-least-once inference may
incur bounded duplicate cost and is not exactly-once billing. Capture provider,
model, usage and outcome separately from workflow/manual/template status.

The API captures immutable recipient-compatible evidence in short transactions,
calls the provider outside domain/database locks and validates typed output.
An explicit service-purpose principal does not impersonate a staff member.
Registry/source/schema/rule/document hashes invalidate only affected proposals.
Every prompt, stored answer, citation, API read and review enforces the same
source-to-reader boundary; current roles/case scope are rechecked, including
revocation. Human source verification precedes accept/edit; current permission,
dependency and proposal status/version are checked atomically. Review writes
proposal/audit only, not ranking, consent, funding, bookings, work release,
holds or quality acceptance. Funding assistance does not reuse the legacy
mutating funding-draft path. Independent QA remains separate from preparation.

Automatic scans remain off until valid scoped authority and effective input,
output, frequency, concurrency, retry and durable shared allowance limits
exist. Missing authority/budget is a real delivery blocker. Disabled/throttled/
failed assistance exposes an owned manual route without blocking case access.
Worker shutdown is interruptible and scans cannot overlap uncontrolled.
Startup migrations are additive, idempotent and serialized on each SQL
backend; deployment/migration permission must not silently expand runtime
access. Old-image rollback disables assistance and restores traffic without
deleting retained cases, audit or task evidence.

Acceptance requires independent-connection races, lease takeover/late-worker
denial, budget contention, stale/revoked reviews, slow-provider/manual-work
and per-capability trigger/source/unchanged-state evidence. The delivery record
must additionally link exact source/image/serving revision, preserved private
SQL/AI/auth configuration, workload identity, a registered real invocation
and independent SQL task/audit before/after/restart under AC-057. Technical
success is not semantic calibration, approved company policy, human
acceptance, comparative benefit or production approval.

#### Implementation and Build Evidence

Initial candidate source `c4b28e3168770252fb35a79074dc2202ef375514` implements the five v1.0.0
contracts, shared case controls/review queue, SQL claims/reservations and
source-verified proposal review in the existing MVP. The
[operator/API contract](../../src/agents/README.md#five-retrofit-assistants-2026-10-13-implementation)
lists exact disabled defaults and finite authority/expiry/call/token limits.
Safe fixed worker/scan warnings expose failures without private exception text;
worker polling backs off instead of silently failing every second.

The local image `zavaforward-mvp:assistants-20261013-01` has image ID
`sha256:a9314193655f4a206553cd294cd9df0b280c40d497ca3c067f32c18d891a54e3`,
not an ACR manifest digest or serving revision. Source CI
[38446725200](https://github.com/jmservera/ama/actions/runs/38446725200)
passed unit/JS, hardened-image/scan/SBOM and real SQL Server store parity
(26 tests). Parent regression discovery passes 333 tests with those 26
integration tests skipped locally; 44 focused tests and 15 reported Chromium
checks cover the new assist paths. The disposable local SQL bootstrap could
not authenticate, so its five-assistant SQL probe did not pass; general CI
store parity did not establish that new proposal path's real-SQL behavior.

The initial Review identified two contract defects, subsequently implemented:
a delayed poll/claim could admit inference after shutdown, and the case view
awaited auxiliary reads without a deadline before rendering ordinary controls.
Corrected runtime source `bf383c40369fa67db3d0cbbe7c9473c24ababbe8` closes
provider-thread admission under the same short gate as stop, outside SQL and
inference. Shutdown-interrupted reservations remain conservative. Case controls
render immediately; auxiliary reads share a 10-second abort deadline and
ignore disconnected/different-route results. Timeout is explicit manual
fallback, not a success-shaped empty proposal.

The corrected local image `zavaforward-mvp:assistants-20261013-02` has image ID
`sha256:d3e652cec1bdef8846270a75c124d55743bdb757231ffaeae585cc423e6b8786`
and the exact runtime-source OCI revision above. Non-root UID10001,
read-only root, no capabilities, writable SQLite state, health and byte-exact
current UI/logo checks passed. Source CI
[38457772710](https://github.com/jmservera/ama/actions/runs/38457772710)
passed all three jobs, including image scan/SBOM and the then-current 68 actual
SQL tests. Additional first-table-creation concurrency coverage brings the
local actual SQL run to 69: 26 general tests and 43 assistant contract/review/
durability/API tests on a dedicated disposable SQL Server database. The same
conditional suites now run in the existing CI SQL job. Full local discovery
is 379 tests, 310 passed and 69 conditional SQL skips; 47 nonbillable assistant
tests and 19 Chromium checks cover the corrected behaviors.

Final validation source `560c30c56bef93edb06275984dbe49c23b34ebc8` leaves the
image's shipped runtime/UI/policies/dependency files unchanged from `bf383c4`.
CI [38461679776](https://github.com/jmservera/ama/actions/runs/38461679776)
passes all three jobs: 379 discovered tests with 69 conditional skips, all
69 actual SQL tests, and hardened-image/Trivy/SBOM checks.

The earlier local SQL authentication failure is historical, not an active
disposable-SQL blocker. Actual SQL tests cover migrations, five proposal paths,
role/current-source review, fenced claims, allowance contention and recovery;
their provider and human-verification actions remain fixtures. They do not
prove actual Azure workload permissions, model quality or human acceptance.
The completed initial Review remains historical evidence, not silently
rewritten as acceptance of the corrected build.

These earlier build-only receipts are historical. The owner subsequently
authorized the existing-app rollout and finite QA (10 calls, 126000 reserved
tokens, one-hour authority, proactive off, up to USD 5 incremental target).
The `d3e652ce` image was published to ACR and deployed as revision
`ca-forward-test-api--0000010`. Independent managed-identity SQL reads preserved
980 cases, 11 staff, three metadata entries, 15 recommendations and audit
head/count 40; private configuration/authentication/identity comparisons matched.
No model call ran: ledger-enabled Azure SQL rejects an INSTEAD OF trigger on
its default updatable, system-versioned ledger event table.

#### Fresh Ledger and Synthetic Coverage Learning (2026-10-13)

Source `99aeaac6b17c19090875b2e23990a6666a58c534` explicitly creates
`assistant_events` as `LEDGER = ON (APPEND_ONLY = ON)` in ledger databases,
using the ordinary trigger only outside ledger databases. It refuses an
existing incompatible ledger table without dropping evidence. The
[official append-only ledger example](https://learn.microsoft.com/sql/relational-databases/security/ledger/ledger-how-to-append-only-ledger-tables?view=sql-server-ver17)
was checked on 2026-10-13. The concurrent intended-proposal identity correction
`687e4aa` is preserved in combined source
`ec7721b51f815e034f9afee82dcf09cd6c4019ac`. Actual disposable SQL passes
73 tests, including fresh-ledger five-path/immutability/restart,
incompatible-table refusal and changed-intent identity. Full discovery finds
389 tests: 316 pass and 73 conditional SQL tests skip. The local image
`assistants-20261013-04` has ID
`sha256:d5eba379f5fd2ce5d9a38965357c193be88eb1882f8e62f75b06faa5aa52fe22`;
it was not a published or serving manifest and is superseded locally below.

Populated-data Chromium then exposed API38/UI0 visits: the shared page renderer
discarded arrays of day-group elements before checking node types. Source
`a76d281` flattens those arrays and adds a two-day/case-link browser regression.
Latest exact-source image `assistants-20261013-05`, revision
`cd14b3b379026a87ebfa3e9058ac10c0df7888eb`, has local ID
`sha256:e0254cb3a0599c21802f0b6515f975550cf00ddce4849d04fd3fa3d50683af20`.
All 21 assistant/browser regressions and 21 exact-image generated-data checks
pass: 38 rendered visits, 12 Finance rows, 601 source work orders, populated
funding/quality controls and five disabled/manual requests. Independent
SQLite hashes and actual local image restart preserve the controlled domain
and proposal evidence, with zero provider attempts. This is local preparation,
not Azure SQL, real-model or human acceptance. Full discovery remains
389 tests (316 passed, 73 conditional SQL skips).

Fresh SQL seed loading now preserves generated procurement and as-of metadata,
without overwriting nonempty databases on restart. The
[synthetic coverage recipe](../reference/research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13)
retains the existing generator/60000-stock lineage and 980-case denominator.
Pending budgets/grants, received/held invoices, submitted unverified quality,
offered handoffs and open requests are fixtures, not approval evidence.

The owner stopped retained-data migration; the initial reset was cancelled
on 2026-10-13, then explicitly reauthorized with all remaining delivery on
2026-10-14. Only exercise database `retrofit` was recreated with ledger,
serverless/backup/diagnostic settings restored, original contained SQL
users/grants and all 11 private tenant staff bindings retained. The new
980-case/date/procurement baseline deliberately replaces the previous
recommendations/audit, not an unchanged-data migration.

Image05/source `cd14b3b` is published and serving as revision `--0000012`,
manifest `sha256:e0254cb3a0599c21802f0b6515f975550cf00ddce4849d04fd3fa3d50683af20`.
Actual workload-managed-identity SQL verifies 38 visits, 12 Finance rows,
12 quality/grant/request records, one package/601 orders and four offered
handoffs. Renewed process-local operator QA invoked all five registered
services through Azure OpenAI `standard`/`gpt-4.1-mini-2025-04-14`; all return
distinct citation-validated ready proposals, five attempts/6884 tokens,
15 append-only ledger events and one finite allowance. Independent domain
hashes and assistant-table content hashes/outputs/usage survive actual
revision restart. No proposal is source-verified or accepted by a human.

Normal serving assistant authority remains absent, proactive off; the bounded
operator authority did not become a permanent paid-worker configuration.
This establishes actual deployed service/model/SQL/restart evidence, not
a real staff-authenticated browser/API acceptance session, semantic quality,
role/accessibility acceptance or measured business value. Those gates remain
open; historical Reviews are not rewritten.

### Responsible AI Control Plane (2026-10-14)

Proposed extension of the existing single-API/SQL runtime; no new service or
production authority. The [PRD RAI contract](../prds/zava-forward-retrofit-programme-demonstrator.md#responsible-ai-release-and-oversight-contract-2026-10-14)
adds FR-051 to FR-054, AC-069 to AC-073 and NFR-014. Existing source-tested
proposal controls and bounded operator calls do not prove these new gates.

| Surface | Proposed control and evidence | Accountable function for live approval |
| --- | --- | --- |
| Task registry and dispatch | SQL-owned release/impact record bound to task/model/prompt/policy/data/permission versions; reject absent, stale, expired or suspended releases for reactive and proactive work | Programme product owner and competent task/control owner |
| Ranking and sensor policy | Evaluate deterministic policy, missing-data treatment and AI recommendations by declared cohort; sensors absent or invalid remain unknown, not low need; retain reason codes and approved disparity disposition | Asset, Data and Performance, Safety and Resident Engagement |
| Proposal review | Recheck sources, role, material versions and release state atomically; reviewers inspect evidence and record a source-based correction/rejection, including unflagged critical fields | Competent reviewer and independent Assurance |
| Challenge and correction | Link a staff-recorded resident/staff challenge to explanation, source/policy/proposal version, human owner and resolution; invalidate only dependent proposals/reviews | Housing, Resident Engagement and record owner |
| Monitoring and incident | Versioned indicator/threshold record; critical harm suspends affected task and reliance on pending/ready proposals, retains permitted history and preserves manual/hazard routes; human approval and corrective tests required to restart | Digital operator with Safety, DPO and product owner |
| Context, audit and telemetry | Reuse recipient-safe projections on input/output/citations/review/export; exclude source text from operational telemetry by default; approve minimum-necessary prompt/review/incident retention and resolve immutable storage versus erasure | Digital, DPO and Legal |

The [failed assessment attempt](../case_study_48_addendum.md#assessment-attempt-and-evidence-limits)
is retained alongside the [validated recovery](../case_study_48_addendum.md#verified-recovery-and-open-dispositions-2026-10-14)
and [baseline RAI report](../reference/research/reports/2026-10-14/rai-report-ama-20261014.md).
Its 11 PARTIAL residuals (8 MEDIUM, 3 LOW) remain open; proposal-only authority,
source verification and manual routes reduced nine original severity claims.
The owner accepted the bounded baseline report for remediation planning on
2026-10-15, not this amendment or an operational release. The report does not
prove this amendment implemented or accepted. Current
staff/tenant identity processing needs explicit privacy scope review despite
constructed resident content; restart persistence does not prove recovery.

Keep these records in the existing authoritative SQL/API control plane and
reuse the manual workflow. A registry flag alone is insufficient: prove that
pending claims, queued retries, publication and already-ready proposals cannot
escape suspension or material-version invalidation. Historical proposals and
human decisions remain reconstructable without becoming reusable approval.
The API identity's combined SQL/Blob/model capability is an exercise trade-off,
not the isolated-worker identity design in ADR 0001.

Mandatory RAI tests cover version mismatch, cohort/missing-data disparities,
plausible wrong answers and reviewer automation bias, non-digital challenge,
injected instructions/forged evidence, cross-role prompt/output leakage and
suspension during active/queued work. Run them against the actual serving
version before claiming exercise acceptance; retain separate legal, direct-user,
privacy and live-use gates. Representative fairness and understanding cannot
be inferred from generated residents or role-agent reviews.

#### Finding-Evidence Register Engineering (2026-10-18, #126)

The implemented claim register reuses GovernanceMixin and the existing checked
`governance` meta document. No new table, service, AI task or role grant is added.
SQL's existing serialized writer rechecks the registered manager, performs
checked-document compare-and-swap, and appends claim plus audit atomically.
Event reconciliation and an immediate post-COMMIT witness distinguish rejection
from committed-but-unacknowledged writes, requiring reload rather than blind
repetition. JSON retains its documented non-atomic cross-file crash boundary.

Detached reads retain all 22 open original checks and explicit insufficiency.
Current assessment is caller-declared exact source/task/release context, not a
build attestation; default is Unknown. Supplied decision-maker or independent-
acceptance references are unverified claims, never assignment, signature,
qualified acceptance or closure. Existing task-release admission and manual/
safety/consent/finance/continuity controls remain independent. See the
[core contract](../../src/core/README.md#constructed-rai-evidence-claims-2026-10-18-126)
for local JSON/SQLite/disposable SQL and hardened-image evidence; none establishes
the separate real AI/Azure, human, legal/privacy or operational gates.

### 1. Durable store: Azure SQL or PostgreSQL

Proposal: Azure SQL Database behind the `Store` interface, not PostgreSQL.

Design:

* One `Store` implementation per backend (`JsonStore` stays for tests and the
  local demo; `SqlStore` is new). The server calls only the interface.
  Methods that today return the whole dataset are replaced by query methods
  that take a filter and a page.
* The new driver is a dependency. The stdlib-only rule is relaxed for the
  database driver only; pin it and record it in the SBOM.
* Schema: `home`, `building`, `case`, `case_event`, `person_staff`,
  `document`, `funding_application`, `ranking_snapshot`, `ai_recommendation`,
  `audit_entry`, `policy_version`. Every mutable row has a `rowversion` and
  writes fail closed on a mismatch, so two replicas cannot overwrite each
  other.
* Indexes for 60,000 homes: a clustered key on the case id; nonclustered
  indexes on (stage, local_authority, wave, owner_id, rank) for list filters;
  a filtered index for open safety issues; an index on the ranking snapshot
  (policy_version, rank); a grid-cell index for the map (see decision 5). Text
  search uses indexed address, postcode and reference columns, not a scan of
  names.
* Paging is keyset paging on the stable ranking order: `WHERE (rank, id) >
  (@last_rank, @last_id) ORDER BY rank, id`, with a page size cap of 100 and
  a total count computed only on request. Offset paging is not used because
  it degrades and shifts under concurrent writes.
* Briefing and dashboard caches are keyed on the database change version, not
  an in-process counter, so replicas agree.

Audit chain in full for the legal period (DH-007, owner direction):

* Audit entries are stored as an append-only ledger table with the full
  content, including personal content. Entries are never updated or deleted
  by the retention job during the legal retention period.
* The hash chain keeps one head row per chain. Appending takes an update lock
  on the head, so concurrent replicas serialise on the chain and the chain
  stays linear.
* Daily ledger digests are written to an immutable Blob container with a
  locked time-based retention policy no shorter than the legal period. A
  scheduled job verifies the ledger against the stored digests and raises an
  alert on failure. Until this runs, the tamper-evidence claim stays
  unsubstantiated, as ADR 0001 already states.
* An erasure request touches operational tables only. A request that cannot
  be met because audit data must be kept is refused for that data, logged,
  justified and told to the resident (DH-007). The DPO must confirm
  Article 17(3) first.
* Expiry at the end of the legal period is an open design item: append-only
  ledger tables are hard to purge selectively. Proposal to test: write audit
  entries to one ledger table per retention year so that a whole table can be
  retired after Legal approves, and confirm the digests still verify.
* The legal retention period is not set here. Legal sets it (PR-003).

Trade-offs:

| Option | For | Against | Verdict |
| --- | --- | --- | --- |
| Azure SQL Database (serverless for dev, provisioned general purpose for pilot) | Already designed and deployed in ADR 0001 (Bicep, contained-user script, Entra-only); native ledger and digest upload; rowversion; PITR | Proprietary; ledger tables cannot be selectively purged; ODBC driver in the image; serverless auto-pause causes cold starts, so not for pilot | Chosen |
| Azure Database for PostgreSQL Flexible Server | Open source, portable, row-level security, pgaudit, rich indexes (GiST for geo) | No native ledger, so the audit chain needs application-level hashing plus external anchoring we must build and prove; new Bicep, identity and CI work; ADR 0001 already examined and declined this | Rejected for now; revisit if portability becomes a requirement |
| Keep the JSON file on a mounted Azure Files share | Smallest change | No concurrency control, whole-file rewrite, corruption risk across replicas, does not scale to 60,000 homes | Rejected |
| Cosmos DB | Scale and geo features | Weak multi-entity transactions for gated transitions, cost model, no ledger | Rejected (consistent with ADR 0001) |

### 2. Blob storage for documents and ledger digests

Proposal:

* Uploaded documents go to a private `documents` container, one blob per
  version, named by an opaque id, never by resident name or address. Metadata
  (case, type, uploader, hash, content type, size, version) is in SQL. Blob
  versioning and soft delete are on.
* The 5 MB limit and the type allow-list stay. The server checks content type
  and magic bytes and a malware scan result before a document becomes
  readable. Until a scanner is chosen, documents are held as unscanned and
  not served to contractors (open item).
* Downloads go through the service, which checks the role and the case, then
  streams the blob. No public or long-lived SAS URLs.
* Digests go to a separate `ledger-digests` container with a locked
  time-based immutable policy. Documents are not placed in an immutable
  container, so erasure of a document is possible where lawful.
* Storage shared keys are disabled; the service uses its managed identity.

Rejected: SharePoint as the document store now (ADR 0001 keeps it
conditional; it adds Graph permissions and licence questions); documents
inside SQL (bloats backups, no benefit); a mounted file share (no versioning
or immutability).

### 3. Entra ID sign-in, role claims and field-level visibility

The original proposal follows. For staff identity and application-role
authority, the owner decision of 2026-10-24 below takes precedence over any
requirement to provision or match an internal staff record before sign-in.
Other proposed controls and their approval status are unchanged.

Original proposal:

* Sign-in uses the Container Apps built-in authentication (Entra ID, one app
  registration, authorisation code flow). The service accepts only requests
  that carry the validated principal injected by the platform and rejects any
  request that reaches it without one, so the header cannot be forged by
  bypassing ingress. The shared password and its code path are deleted, not
  kept behind a flag.
* Roles are Entra app roles on the registration, assigned to groups, and read
  from the `roles` claim. Group claims are not used because of token overage.
  Staff, manager, grants officer, safety lead, data analyst, and contractor
  are the starting roles; the allow and deny matrix is owned by control
  owners (OD-19) and is an input, not a decision here.
* Staff records are matched to the Entra object id, not to email text.
* Contractors and providers sign in as Entra B2B guest users limited to a
  contractor role (proposal, open item for the tenant owner), and see only
  their own assigned work.

#### Observed exercise identity and session learning (2026-10-13)

Historical observations only. The SQL staff-binding sign-in gate described
here is superseded prospectively by the 2026-10-24 owner decision below.
Recorded preservation results and other dated observations are not rewritten
or represented as evidence for the new implementation.

This dated update supplements, not rewrites, the proposals and historical
implementation tables. [#65](https://github.com/jmservera/ama/pull/65) and the
[initialization guide](../../infra/README.md#tenant-staff-and-application-role-initialization)
record deployed built-in authentication and owner-reported administrator and
Coordinator access. Full pilot identity/permission acceptance remains separate.

* Platform authentication, app-role claims and the internal staff `oid` binding
  are separate gates. The observed Coordinator denial had a valid role but no
  staff binding. Default Access is unmapped, not a business permission. Keep
  the exact tenant and single distinct mapped role checks; email fallback
  remains off. Direct user/group app grants count; nested groups do not
  inherit application assignments.
* The repeatable private-roster initializer preserves existing bindings and
  workload codes. Ten existing positions plus one supplier-scoped Contractor
  use eleven distinct tenant members for eight role kinds. This is a demo
  allocation, not company staffing, competence or the proposed B2B model.
  The member-only initializer does not resolve the guest/pilot open item.
* SQL staff is startup-cached. An idempotent SQL no-op must still support
  replacing every serving replica after a failed restart. Identity/current
  owner-label reconciliation uses the API's transaction-owned database lock;
  one generic audit event extends, rather than renames, historical actors.
  Exact private comparison preserved all 980 programme cases, workload codes,
  supplier scopes, six recommendations and nineteen prior audit rows.
* Public welcome is distinct from the protected workbench/API. A changed
  ingress FQDN requires callback re-initialization in an isolated authorised
  management profile, not a shared password or replacement registration.
  Deployed production refuses password auth; a local development provider
  remains, unlike the proposal above to delete that code path entirely.
* Own-user account photo uses delegated `User.Read` and the platform's private
  token store, with scoped scheduled renewal. The browser receives only
  private binary output. Blob object URLs require `blob:` in CSP `img-src`
  only, not relaxed script/frame/default sources. A public-logo-as-Blob
  rendering check proves transport/CSP, not a person's actual photo.
* Switching account is a new login with explicit `prompt=select_account`,
  not provider logout followed by ordinary SSO. Normal Sign out retains
  platform logout. Easy Auth owns state/nonce/callback and session issuance;
  cancellation or selecting the same account is not successful replacement.
* Existing Azure Monitor routing collects constant auth-flow events; generic
  access logs would risk publishing callback queries/tokens. Verify actual
  table/schema and ingestion rather than assuming legacy `_CL` names.
  Image-only rollout compares private app/auth configuration and ready
  serving replicas, preserving SQL/AI, secret references and token store.

References checked 2026-10-13: Microsoft's
[account-selection behavior](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#request-an-authorization-code)
and [non-cascading group assignments](https://learn.microsoft.com/entra/identity/enterprise-apps/assign-user-or-group-access-portal).
Operational steps and evidence boundaries:
[callback initialization](../../infra/README.md#post-deployment-api-authentication-initialization),
[own-photo setup](../../infra/README.md#public-welcome-and-microsoft-account-photos)
and [account diagnostics](../../infra/README.md#account-selection-and-safe-flow-diagnostics).
Actual already-signed-in account replacement, full permissions, accessibility,
lawful processing and production approval are not established by these checks.

#### Entra-authoritative staff access (owner decision 2026-10-24, Refs #360)

Status: accepted by the AMA project owner on 2026-10-24 for staff identity
and application-role authority. This records the owner's direction, not a
completed implementation or successful acceptance test. The remainder of this
ADR retains its existing status.

Context and alternatives: the earlier exercise required both Entra role
assignment and a matching SQL staff OID binding. A valid assigned principal
could therefore be denied because a second identity registry was incomplete
or cached. The owner selects Entra-authoritative staff identity and application
roles, rather than repairing or retaining SQL staff provisioning as a login
prerequisite. Azure SQL remains authoritative for business records, scoped
object grants and workflow evidence, not staff authentication or application
role assignment.

Decision:

* Staff sign-in uses a platform-verified Entra principal for the exact
  configured tenant and application. The service validates the trusted
  principal's tenant, one unambiguous valid object ID and supported application
  role claims. Tenant and object ID are canonical UUIDs. Missing, malformed,
  conflicting or unauthorized claims fail closed. Default Access alone and
  unrecognized roles do not establish application permission. Preserve the
  single distinct mapped staff-role rule; explicit supplemental capabilities
  do not count as a second staff role.
* Authentication must not query SQL, read a staff cache or require a
  pre-provisioned staff row. Neither email, UPN, display name, a client-selected
  role nor a client-supplied identity key grants access. There is no email
  fallback. Application roles and capabilities are assigned in Entra, not
  inferred from database roster entries.
* The authenticating ingress must validate issuer, audience and session/token
  validity and prevent clients from supplying or bypassing its trusted
  principal headers. Parsing a principal header, or setting a trusted-proxy
  flag, is not proof of authentication. Unverified direct-origin traffic is
  denied. The application must not accept tokens for another application.
  Status: this is a release gate, not yet evidenced by the code, which checks
  only the trusted-proxy flag. External anonymous, forged-header and
  direct-origin negative probes must pass before any release or acceptance.
* The explicit `ZavaForward.ApplicationAdmin` application role supports
  application-option visibility. It is not a wildcard permission for protected
  actions, records, fields, exports, model inputs or private chats. Alone it
  yields the distinct role "Application Administrator", outside the staff
  roles: every option is listed, flagged "needs a role with this authority",
  and the only readable endpoint is the caller's own account; business data,
  exports, the staff directory and every state change are refused. With one
  staff role it composes without replacing that role: that role's data,
  fields, exports and actions apply, every option stays visible and options
  beyond that role are flagged, and no further authority is added.
  Every protected operation evaluates its actual role/capability and domain
  predicates on the server.
* Case scope, object grants, provider/supplier assignment, field projection,
  resident consent and representative authority remain business controls.
  Professional competence, named delegations, Finance authority, independent
  QA, no-self-approval, rule approval and AI restart requirements are retained.
  ApplicationAdmin does not grant RuleOwner, AIRestart, professional sign-off,
  resident choice or another person's private thread/memory access.
* The canonical tenant/object-ID pair is the stable staff identity for audit,
  case ownership and distinct-person comparisons, independent of role, email,
  name and account-selection changes. Derived storage keys must preserve that
  identity without ambiguous aliasing. Legacy case-owner codes and historical
  audit entries are retained; any association with an Entra principal is
  explicit and verified, never guessed from email.
  Continuity: after authentication, a verified tenant and OID that match
  exactly one enabled roster row keep that row's business code, email and name for
  ownership, handoffs and audit (never matched by email; ambiguous or
  disabled matches fall back to the derived key). A row naming another tenant
  never matches, and a row without a tenant matches only the tenant the store
  records as owning legacy rows (`legacy_roster_tenant`); without that record
  such rows do not match. Person independence (author, approver, named owner)
  is judged on the canonical tenant and OID: a transactional, append-only
  alias record links the derived and legacy codes/emails of one verified
  person, so disabling or failing to read a binding cannot turn an author into
  a second person. Rule-card authoring and approval fail closed when that
  record cannot be written or read. Role and capabilities still
  come only from claims. Scoped finance and contract authority is resolved
  from the matched row by immutable identity only at the protected operation,
  with expiry, revocation, scope and independence checks unchanged. Entra
  staff without a roster binding become selectable handoff recipients once they
  sign in (a bounded registry written in one serialized read-merge-write
  transaction and projected to `/api/me` as recipients). A Contractor signs in only
  with exactly one enabled Contractor row bound to the OID with a company;
  absent or ambiguous is denied and provider object scope is unchanged. The
  derived key is a truncated digest, a known collision limit. A roster may retain
  assignment metadata and labels but must not become a second login or
  application-role registry.
* An authenticated principal is not thereby an appointed approver or owner
  of every case. Unresolved legacy identity associations or required scoped
  grants deny the affected operation without reinstating SQL provisioning as
  a general authentication requirement. Re-authorize current permission and
  scope for protected reads and writes; stale sessions are not evidence that
  revocation has propagated.
* Graph or Microsoft 365 reconciliation is explicit, least-privilege and
  idempotent. Before writing, verify the exact tenant, application/client ID,
  enterprise service principal, enabled target user object ID and intended
  application-role ID. Resolve mutable login text only to verify the intended
  object, not as durable identity. Verify role propagation on the enterprise
  app. Dry run is non-mutating; apply adds only the authorized missing role
  definition or assignment and preserves unrelated roles, assignments,
  principals and application configuration. A repeat run is a no-op.
  Ambiguous, mismatched or unverifiable targets refuse writes. Runtime staff
  access does not require directory-management permissions or a SQL initializer.

Consequences: removing the second login registry avoids staff-binding and
cache-restart failures and keeps staff roles under Entra management. It makes
the ingress trust boundary, claim freshness and explicit capability checks
critical, and requires verified continuity between legacy workload identities
and stable Entra identities. New identity handling must not silently orphan
ownership/history or widen administrative access. Missing domain authority
continues to block its protected action, not basic staff authentication.

Lineage and acceptance boundary: this subsection prospectively supersedes
only the staff-binding login prerequisite in this section and its 2026-10-13
learning. ADR 0002 continues to amend ADR 0001 for the MVP; other decisions,
proposals, historical observations and ADR 0004/0005 authority boundaries
remain unchanged. Source changes, local tests, directory assignments, a
deployed image and a successful browser sign-in are separate evidence claims.
No cloud operation, spending, deployment, issue closure, real-data use or
professional/legal approval is authorized or proven by this decision alone.
The existing real Azure/SQL/AI, restart/preservation, exact-build review and
human acceptance gates remain applicable.

#### Proposed field-level visibility

* All reads leave the service through role-specific projections: an explicit
  allow-list of fields per role and per object. A field absent from a role's
  list is not returned. New fields are hidden until added to a list.
* Vulnerability and adjustment data is split into `needs_notice` and
  `named_contact` (visible to contractors) and `reason` (visible only to roles
  with a recorded need). The reason is held in a separate column set so a
  contractor query cannot select it, even through a coding error in a
  projection.
* The same rule applies to list responses, search (a contractor cannot search
  on reason text), exports, the audit viewer, error messages, caches (cache
  key includes role) and AI prompts. A contractor-facing draft is built from
  the contractor projection, so the model never receives the reason.
* Tests: a matrix test calls every endpoint as every role and fails if a
  forbidden field name or seeded reason string appears anywhere in the
  response, including exports and drafts (AC-004, AC-005).

Trade-offs:

| Option | For | Against | Verdict |
| --- | --- | --- | --- |
| Built-in Entra authentication plus service-side projections | No token code in a stdlib server, platform handles sessions and refresh; aligns with ADR 0001 | Depends on platform headers; local dev needs a stub with the same contract | Chosen |
| Validate JWTs in the app | Portable | Hand-written token validation is a security risk in a stdlib server | Rejected |
| Hide fields in the browser by role | Quick | Not enforcement; fails FR-003 | Rejected |
| SQL row-level security only | Strong at the data layer | Does not cover column projection, exports or AI prompts alone; useful as defence in depth later | Deferred |
| Keep a shared password for the pilot | No setup | No identity, no audit of who | Rejected |

### 4. Home ranking: deterministic policy versus AI recommendation

Proposal: ranking is a pure, deterministic function. AI prioritisation is a
separate recommendation that never feeds back.

Ranking:

* Raw sensor readings and derived sensor signals do not directly change the
  investment ranking. A valid, approved trend may create a separately owned
  `SENSOR_REVIEW_DUE` task in the condition-assessment queue. Only a
  human-verified finding may be considered in a later, approved ranking-policy
  version.
* The policy is a versioned file in the repository (and a `policy_version`
  row) with a named owner field, an effective date, a content hash and
  the rule order. Changing it creates a new version; old versions are kept
  and can be re-run. The named owner is a role holder to be named by the
  business (open item); the file is not valid for a pilot without one.
* Input is the case data plus the policy version. No clock reads, random
  numbers, model calls or database ordering effects: the "as of" date is an
  explicit input stored with the snapshot.
* Rule order starting point (from owner direction, for the policy owner to
  confirm): open safety issue first, then days waiting (longer first), then
  reference ascending as the final tie-break so no two homes tie.
* Every ranked home stores its reason codes (for example `SAFETY_OPEN`,
  `WAIT_DAYS_GE_60`) and the rule that decided its position. The list shows
  the codes and a plain-language label.
* Snapshots are written to `ranking_snapshot` (policy_version, as_of, home,
  rank, reason codes) when data changes or a policy is published. Lists read
  the snapshot with the keyset paging above. Staff can still filter and sort
  by other columns; the ranking is the default order, not a lock.
* A golden test fixes input, policy version and expected order; an identical
  re-run must be byte-identical.

AI recommendation:

* A separate `ai_recommendation` record holds the suggested order or flagged
  homes, its cited reasons (FR-027), model and prompt version, and status.
  A person can accept, edit or reject it with a reason (FR-026). Accepting
  creates a task or draft only.
* No code path joins the recommendation into ranking, queue membership or
  case state. A test asserts the ranking snapshot is unchanged after any AI
  call.
* The workflow-only path (the deterministic order) is always present
  (FR-028).

Evaluation harness (supports OD-34, the pilot gate decision):

* Held-out set built from constructed data with labels agreed by named human
  reviewers; no real resident data. Labels are the human-judged "should be
  looked at first" set for each scenario.
* For each run record: policy version, model and prompt version, the
  deterministic order and the AI order.
* Measures: top-k overlap and rank correlation between the two orders;
  critical misses (open safety issue not in the AI's recommended top-k, target
  zero in agreed tests); reason-citation validity (every cited fact exists in
  the case); reviewer accept, edit and reject rates with reasons; run-to-run
  variation of the AI order on identical input; latency and cost per run.
* Report the AI's added value as the difference against the deterministic
  order on the same cases (PR-007). Thresholds for any pilot use are set by
  the owner, not by this ADR.

Trade-offs:

| Option | For | Against | Verdict |
| --- | --- | --- | --- |
| Deterministic ranking plus AI recommendation beside it | Explainable, reproducible, auditable; AI value measured | AI order cannot improve the queue until a person accepts it | Chosen (owner direction) |
| AI-ranked queue | Might find non-obvious priorities | Not reproducible, cannot cite a fixed policy, conflicts with PR-006 and PR-008 | Rejected |
| Weighted score model | Smooth trade-offs | Hard to explain, tuning disputes, ties need extra rules | Rejected for the first policy; may become a later version |
| No ranking, filters only (the earlier note) | Simplest | Superseded by owner direction 2026-10-08 | Rejected |

### 5. Map at 60,000 homes and the tile provider

Proposal:

* The browser never receives all homes. It asks for `GET /api/map` with the
  viewport bounding box, zoom level and the same filter object the list uses.
  The server returns clusters (cell centre, count, highest-severity flag, and
  the share waiting 60 days or more) at low zoom and individual points (id,
  position, severity flag only) at high zoom, capped at 500 items per
  response, with a flag when truncated.
* Clustering is a grid: each home stores precomputed cell keys for a few zoom
  bands, indexed, so the query is an indexed range plus a group by. No spatial
  extension is needed at this scale; Azure SQL spatial indexes remain an
  option if grid cells prove too coarse.
* The map and the list take one shared filter parameter set, so counts agree
  (AC-023). A cluster click zooms or applies the area to the list.
* Keyboard and screen-reader route: a cluster and point list beside the map
  with focusable links and counts. This closes the focus gap recorded in the
  gap analysis and is the primary accessible route (NFR-001).
* Marker colour meanings stay as in the MVP; the colour is never the only cue.
* An optional sensor overlay uses the same bounding-box, filters, role checks
  and grid aggregation. Clusters expose counts of homes due for human review
  and homes with insufficient sensor data; individual points expose only a
  categorical state. Raw readings and device identifiers are available only
  in an authorised property detail view, not in map tiles or cluster payloads.
  The accessible list mirrors the overlay and its status text.
* Tiles: use a licensed provider. Proposal: Azure Maps render tiles with
  Entra authentication, because it stays in the Microsoft tenant and keeps the
  subscription and data terms in one place. Alternative: Ordnance Survey Maps
  API through OS Data Hub for UK base mapping. Licence terms, cost, UK street
  detail and a processor position are unverified and are an open item. The
  tile request leaks only the viewed area and zoom, never case data, and the
  CSP allows only the chosen provider's host.
* Leaflet stays, bundled in `web/vendor`.

Trade-offs:

| Option | For | Against | Verdict |
| --- | --- | --- | --- |
| Server-side bbox and grid clusters, licensed tiles | Bounded payload, shared filter, works with indexes | New API, grid precompute on import and on address change | Chosen |
| Client-side clustering of all points | Simple | Ships 60,000 homes (and their positions) to every browser, slow, and exposes more than a role may need | Rejected |
| Vector tiles generated per filter | Smooth | Heavy infrastructure for one team | Rejected |
| Continue OSM public tiles | Free | Policy allows light use only; not for production traffic | Demo only |
| Self-hosted tiles | Control | Operations burden | Not now |

### Sensor Data Capture, Analysis and Map

This is a proposed non-production design for the AMA demonstration, not an
inventory of Zava North Homes' equipment or an approved production integration.
The only assumed sensor types are humidity and temperature, with three
observations per configured sensor per simulated day. Device count, real
sampling cadence, protocol, calibration, data owner, lawful basis, retention
and operational thresholds remain unknown. It aligns with BRD RULE-014 and
AC-047: invalid or missing measurements are insufficient, a normal reading
does not prove quality, and residents may decline sensor use subject to the
approved data-protection basis.

The demonstration path is a seeded simulator that sends constructed readings
through the same server-side ingestion contract intended for a future
authenticated adapter. The API validates schema version, stable reading ID
(unique within a sensor), sensor-to-property mapping and its effective dates,
units, UTC observation time, receipt time, duplicate/out-of-order status,
device calibration status and configured plausibility limits. The sensor and
reading IDs form an idempotency key. Accepted readings are appended; rejected
or unmapped inputs create an owned data-quality exception and never silently
update property condition. The simulator is explicitly identified by source
type, scenario and seed and is not exposed as a device or resident system.
There is no public unauthenticated ingestion endpoint.

Keep observation, derived analysis and business decisions separate:

| Record | Proposed content | Authority |
| --- | --- | --- |
| `sensor_mapping` | Sensor identifier, UPRN, optional approved zone, effective dates, device status and calibration evidence reference | Data/device owner confirms mapping and status; do not place resident identity in the mapping |
| `sensor_reading` | Stable reading ID, sensor ID, observed/received timestamps, relative humidity percentage, temperature in degrees C, source/schema version, quality status and optional simulator scenario/seed | Append-only raw observation; never overwrites a survey, resident report or approved condition |
| `sensor_analysis` | Sensor/property, analysis window, expected/valid sample counts, latest valid time, completeness, derived trend category, analysis/rule version and run ID | Deterministic derived summary; reproducible from retained readings and versioned rules. Preserve sensor-level results; do not average multiple devices into a property value without an approved aggregation rule |
| `sensor_review_task` | Trigger reason, evidence references, owning queue, status and human disposition | Human review record; cannot close or downgrade a hazard or safety hold |

At this cadence, the current API and SQL store can validate, persist and
calculate summaries without a separate streaming broker or time-series
service. An idempotent API operation accepts simulator batches; a scheduled
completeness pass identifies missing or stale expected readings. A later
device adapter must authenticate the source independently and call the same
contract. Review the ingestion topology only after actual device protocols,
delivery guarantees, device counts, latency needs and operating ownership are
known.

Amendment (2026-10-14): the AMA project owner directed that Azure IoT Hub is
the product for IoT, so the earlier advice not to add IoT Hub for the demo is
replaced by [ADR 0003 decision 6](./0003-journey-derived-capabilities-runtime-fit.md).
The simulator then sends telemetry as an IoT Hub device, and the API consumer
still appends to Azure SQL through the same validation contract. Do not add
Event Hubs separately.

Analysis checks data quality before applying a trend rule. Completeness is
measured against the demonstration cadence of three readings per simulated
day. A versioned configuration defines the analysis window and any
humidity/temperature conditions; for example, a synthetic scenario can
exercise repeated elevated humidity observations with temperature as context.
No numeric threshold or window is asserted here. The AMA simulator may use
explicitly fictional scenario settings to exercise the rule. Missing samples,
stale data, invalid mapping/calibration, clock problems or invalid units
produce `INSUFFICIENT`, not a green/normal state. No AI is used to calculate
the rule or change ranking. Raw readings are not placed in AI prompts or
diagnostic telemetry; a later AI use would need a separately approved purpose,
field access and evaluation.

The map adds a separately selectable sensor layer to the existing server-side
bounding-box and grid-cluster API. At portfolio zoom it shows counts by
`REVIEW_DUE`, `INSUFFICIENT` and `NO_REVIEW_SIGNAL`; the last label means only
that no configured rule triggered on sufficient data, not that the home is
safe or damp-free. At property zoom it shows the latest valid humidity and
temperature, timestamps, valid/expected sample count, trend window,
provenance, calibration/mapping status and rule version to authorised roles.
If the latest valid observation is stale, it is labelled with its age and is
not presented as a current condition.
The map never displays a health diagnosis, resident identity or raw sensor
history in cluster responses. Status text and the adjacent list/table remain
available without relying on marker colour or location.

Prioritisation has two stages. A valid, owner-approved sensor rule may add
`SENSOR_REVIEW_DUE` to the condition-assessment queue so a person can verify
the evidence; existing safety holds, statutory response handling and resident
reports remain independent and take precedence. The signal does not start or
back-date a statutory clock, diagnose a hazard, release a hold, or directly
change the investment ranking. Only a human-verified finding may enter a
subsequent, approved version of the deterministic investment policy with
published reason codes. Absence of a sensor, stale data, insufficient coverage
or resident decline must never lower a home's ranking or suppress service.

Before any non-synthetic use, the DPO, Legal, data owner, Asset and competent
safety/technical roles must confirm the lawful basis, DPIA, resident choice,
field permissions, retention, calibration/maintenance responsibility,
device-to-property mapping, freshness and gap rules, analysis window and
thresholds, handoff owner and evaluation evidence. This ADR does not grant
those approvals.

The simulator acceptance checks should include three generated observations
per configured sensor per simulated day; duplicate, out-of-order, missing,
stale, mis-mapped, invalid-unit and uncalibrated inputs; deterministic replay
under a fixed rule version; map/list count parity; visible synthetic provenance;
human task creation; and proof that absence or a no-trigger sensor state cannot
alter resident reports, safety holds or investment ranking, and that an AI
recommendation cannot change those controls or ranking.

### 6. Deployment: replicas, region, hardening and CI

Proposal:

* Region: `uksouth` for the whole pilot stack (SQL, Blob, Container Apps,
  Key Vault, Log Analytics). The `northeurope` dev environment remains
  development only. Inference may still be processed outside the UK in
  `uksouth` because no data-zone model option was listed; no personal data
  goes to a model until the transfer position is approved (DH-006, OQ-012).
* Replicas: minimum 2, maximum 4, HTTP concurrency scaling, zone redundant
  where the environment supports it. The container holds no state: no live
  JSON, no uploads, no in-process caches that affect correctness. Health and
  readiness probes check the database. Writes fail closed if SQL is
  unreachable; reads may serve with a stale banner only if the owner agrees.
* Container image hardening: non-root user (already set), read-only root file
  system with an in-memory temp directory, all Linux capabilities dropped,
  no shell tools beyond what the app needs, base image pinned by digest,
  dependencies pinned and hashed, and no data baked into the image. The
  current Dockerfile copies the working data file into the image; that must
  stop because the file holds real addresses. Container Apps does not expose
  some of these settings, so they are enforced in the image and verified in
  CI (as ADR 0001 already notes).
* Secrets: none by default; managed identities for SQL, Blob and the model.
* CI (extends `.github/workflows/mvp-validation.yml`, which already compiles,
  runs `unittest discover` in `mvp/tests`, checks the JavaScript syntax and
  refuses committed data): add a SQL integration job against a SQL Server
  container, the role-by-field matrix test, the ranking golden test, a
  restart-persistence test, an image build with vulnerability scan that fails
  on high or critical findings, an SBOM artifact, and a check that the image
  runs as non-root with a read-only root file system. Deployment to the pilot
  environment depends on all of these passing.
* Restore and deletion drills (DH-005) are required before real data.

Trade-offs:

| Option | For | Against | Verdict |
| --- | --- | --- | --- |
| Container Apps, 2 to 4 stateless replicas | Already deployed, cheap, matches ADR 0001 | Some hardening settings are image-only | Chosen |
| Single replica with restart persistence | Simplest | No availability; a deploy is an outage | Rejected for pilot |
| AKS | Full control | Operations overhead for one app | Rejected |
| App Service | Simple for one web app | ADR 0001 reasons stand (per-workload identity, jobs) | Rejected |
| Multi-region | Resilience | Cost and complexity not justified at pilot | Deferred |

### 7. Staff time capture gated on DPIA

Proposal (owner direction PR-004, OD-36; the DPIA is not done):

* Time capture is designed and may be built, but ships disabled. The service
  refuses to enable it unless configuration holds a DPIA reference id, a
  staff notice version and a recorded consultation reference. Enabling is an
  audited administrator action, not a deploy-time default.
* Data is held in its own tables, separate from case data, with its own
  retention value set from the DPIA. Staff see their own entries.
* Reports are aggregated for process measurement with small-group
  suppression. There is no per-person league table and no export of
  individual rows to line managers. Using the data as a performance rating
  needs a separate decision (PR-004).
* The staff notice and the paired-measurement definitions (OD-18) are inputs
  from the owner and the DPO, not built here.

Rejected: always-on capture to gather a baseline early (breaks PR-004);
passive activity tracking from screen or keystroke data (disproportionate,
no support in the documents).

## Consequences

* Good: state survives restarts and replicas; the audit claim becomes
  testable; contractor visibility is enforced and tested in one layer; the
  ranking is reproducible and explainable; the map and list stay usable at
  60,000 homes; AI value is measured against a fixed baseline.
* Cost: a database driver, SQL migrations, an app registration and role
  administration, a licensed tile subscription and a scan job are new running
  parts. SQL pilot compute is a recurring cost; serverless auto-pause is not
  used for the pilot.
* Risk: ledger tables and the legal period make eventual purge hard; the
  design is unproven until the per-year table test passes.
* Risk: lawful basis, retention, DPIA and the contractor identity model are
  not approved, so real data stays blocked even when the build is complete.

## Alternatives considered and rejected

The per-decision tables above list the rejected options. In short:
PostgreSQL, a file share, Cosmos DB, JWT validation inside the stdlib server,
browser-only hiding, an AI-ranked queue, client-side clustering of all homes,
OSM public tiles in production, a single replica, AKS, and always-on staff
time capture.

## Open items

* Named RAI release, residual-risk and incident owners; current intended-use/jurisdiction screening; representative cohort and oversight evidence; challenge route and suspend/restart drill under PRD AC-069 to AC-073.

* DPO to confirm the lawful basis per data class, the Article 9 condition and
  that audit data can be retained against an erasure request under
  Article 17(3). Legal to set the legal retention period (PR-001, PR-003,
  DH-007).
* Named owner of the ranking policy and sign-off of the first rule order.
* Sensor/device inventory, protocol, property mapping owner, calibration and
  maintenance evidence, approved cadence, retention and data-protection basis.
* Competent owner-approved sensor validity/trend thresholds and review-window,
  queue-ownership, triage and evaluation rules. Synthetic simulator settings
  do not resolve these operational decisions.
* The roles that have a need to see a vulnerability reason, and the allow and
  deny matrix (OD-14, OD-19).
* Contractor identity model (B2B guests or another route) and tenant owner
  consent.
* Which homes are in live scope out of about 60,000, since the BRD pilot
  assumed 80 to 100 candidate homes (OD-17).
* Licensed tile provider: licence, cost, coverage and processor terms.
* Document malware scanning service: enable Defender for Storage on the account and run the tag reader against it (issue #117); the local scanner is a demo test only.
* Retention periods, legal-hold authority and the retention job schedule: DPO and Legal set them (PR-003); the demo periods are placeholders.
* Per-year audit table approach and ledger digest verification, to be proven
  by test before it is relied on.
* DPIA, staff notice and consultation view for time capture (OD-36).
* Measured load, latency and cost; the PRD targets stay unmeasured until then.
* Model transfer position for `uksouth` (OQ-012, DH-006).

## Related documents

* [ADR 0001](./0001-azure-architecture.md)
* [Zava Forward Workbench PRD v0.10.0](../prds/zava-forward-retrofit-programme-demonstrator.md)
* [Gap Analysis and Next Build](../reference/research/gap-analysis-next-build.md)
* [Zava Forward MVP](../../src/api/README.md)

## Implementation status

Historical snapshot from 2026-10-08 on branch `feat/mvp-deterministic-ranking`,
with explicitly dated 2026-10-09 deployment updates. "Done" means built and
covered by the tests/local runs available then, not pilot acceptance. Earlier
blocked/unrun rows below are not the current #65 status; see the later delta.

| Item | Status | Deviations |
| --- | --- | --- |
| Ranking policy and AI recommendation (decision 4) | Done | Policy is a hash-checked versioned file with a registry of old versions; ranking snapshot stored as a file and served to managers (not a `ranking_snapshot` table, no scheduled publish step); as_of is the load date of the data, not a per-case stage date; named policy owner and sign-off still open |
| Store interface hardening and durable SQL store (decision 1) | Partial | Azure SQL store (`mssqlstore.py`) built: 26 parity tests on SQL Server 2022 and a run on the dev Azure SQL with a managed identity (2026-10-09), 980 constructed cases; no Azure load test. SQLite remains the dev store; list reads, search, sorts and counts in SQL with keyset paging for the default sort (60,000-case timing tested on sqlite); detail, map, stats, visits, export, closed list and writes still use the in-memory copy; mapping to Azure SQL documented only |
| Ledger hash chain and verify (decisions 1, 2) | Partial | Verify command and endpoint done; Blob digest publisher, scheduled verifier, `ledger-digests` container and alert built (issue #115) but not yet deployed or locked; the retention lock and legal period are owner decisions |
| Field projection by role (decision 3) | Done | Free-text notes are not redacted; contractor screens built (needs notice and named contact only) and tested through the server, not with a contractor login in a browser |
| Quality acceptance and procurement (PRD FR-016, FR-017) | Done (API and screens) | Independent acceptance, defects, reinspection, handover and aftercare; packages, evidenced capacity and versioned work orders; both stores; procurement kept as one document, not per-row tables; contractors read their own work orders only; no contractor evidence upload; screens not run in a browser |
| Return, reopen, handoff, safety referral | Done (API and screens) | Screens checked by a Playwright run in desktop Chromium (return, reopen, list, map list); handoff and safety screens checked only for rendering; no screen reader run |
| AI evaluation harness (decision 4) | Partial | Offline, scripted model, ten golden scenarios plus task checks; measures overlap, Spearman, critical misses (fails on any), citation validity, run-to-run variation, latency, model and prompt version, reviewer outcomes and added value; citations validated server-side with a comparison record per AI task and a workflow-only mode; no live-model measurement |
| Accessible map alternative and tile provider (decision 5) | Partial | List view and env-configured provider done; no licensed provider chosen; server tests for the list and tile config, plus a manual Playwright check of the map list; no screen reader run |
| Dockerfile and CI (decision 6) | Partial | Image built and started locally; workflow not yet run on GitHub; not deployed; no scan or multi-replica test |
| Staff time capture (decision 7) | Partial | Off by default, needs `DPIA_APPROVED`, a consultation reference and a staff notice acknowledgement before recording; notice text is a draft; also needs a notice approval reference and an audited manager enabling action (`#/time` screen); approval references themselves are still owner decisions (OD-36) |
| Entra ID provider (decision 3) | Partial | Header parsing and role mapping tested with synthetic principals only; Azure configuration documented in the README, not done |
| Blob documents (decision 2) | Partial | `DocumentStore` interface with local and Azure Blob implementations (urllib, SAS or managed identity), size and type limits, role checks, audit; Blob store run only against a fake transport; scan-before-availability with a labelled synthetic local scanner and a Defender for Storage tag reader (fake transport only, issue #117); retention listing, owner-approved deletion and legal hold with synthetic-demo periods; real scanner, Defender enablement and approved periods open |
| Finance, grants, technical sign-offs and resident decisions (FR-013, FR-014, FR-018, FR-019) | Done (API and screens) | Record-only finance with separate approvers and no bulk path; constructed data, proposed role mapping, exact-match comparison, screens not run in a browser |
| Azure provisioning, replicas, region, load test (decision 6) | Partial | Dev app `ca-properwarm-mvp` on Azure SQL and Blob with a managed identity, min 2 and max 4 replicas, restart persistence checked (2026-10-09); the app is not yet in Bicep, Entra built-in authentication is blocked on an app registration, no load test, region and private networking for the pilot not decided |

### Pilot Region and Capability Evidence Delta (2026-10-18, Refs #137)

The [owner's 2026-10-15 comment](https://github.com/jmservera/ama/issues/137#issuecomment-6192754703),
retrieved and verified live on 2026-10-18 and 2026-10-19, selects pilot region `uksouth` and
subscription owner @jmservera. It does not select the separate SQL region or
approve zone redundancy, sizing, cost, deployment or access. The historical
2026-10-08/09 table above is unchanged and does not represent today's decisions.

The [dated management-plane evidence](../../infra/README.md#read-only-pilot-capability-and-quota-evidence-2026-10-18-refs-137)
records exact catalog matches, empty quotas, a denied Container Apps location
query and failed IoT usage queries. Approved subscription binding, complete
quota/zone evidence and named human review remain unavailable. This is not
reserved capacity, fresh deployability, approval of the whole-stack proposal
in decision 6, or issue acceptance. The unchanged pilot example and reviewed
reference gates remain non-deployable.
The identical GET reproduction on 2026-10-19 matched the reported fields and
failure categories; it neither replaces the dated first observations nor
resolves their unknowns. The issue's later historical delivery comment still
calls region/ownership open without a replacement owner decision; that
contradiction is explicitly retained in the infrastructure evidence.

### Current Exercise Delivery Delta (2026-10-13)

| Area | Later evidence | Remaining boundary |
| --- | --- | --- |
| SQL and deployment | #65 from-empty Bicep rebuild retained 980 programme cases; the API identity read/wrote SQL and retained audit writes across restart; both model tiers returned source=ai | Generated stock is 60,000 homes; no Azure load/backup-restore proof or calibrated AI benefit |
| Identity and sessions | Callback check, private staff reconciliation, public welcome, own-photo transport and explicit account-picker route are deployed; owner reports administrator/Coordinator sign-in | Different-account replacement, own live photo/consent, all roles, B2B guests and full permissions remain separate acceptance |
| Containers and CI | Tested account-switch image/revision and private configuration-preservation gate are recorded in the operator handover; MVP CI and both validations passed at source head 8ca4a3d | Later edits need their own checks; no production resilience or blanket assurance claim |
| Documents and audit | SQL/Blob configuration replaces the local-only development defaults; append-only audit controls and startup-cache convergence are implemented | Malware/content scanning, external immutable digests, deletion/retention approval and recovery remain open |

The [current handover](../../infra/README.md#current-exercise-handover-2026-10-13)
and [MVP limits](../../src/api/README.md#honest-limits) own the version-linked
operator detail. This delta neither rewrites the historical table nor approves
the proposed decisions, control-owner matrix or production rollout.

### Retained Draft Architecture Learning (2026-10-13)

The [PM/UX closure review](../reference/research/gap-analysis-next-build.md#draft-experiment-closure-review-2026-10-13)
captures all four unmerged drafts against main `71aaf9d`. These are reusable
control/regression lessons, not new approved architecture decisions or a
claim that the draft implementation is running in the current deployment.

| Pinned source | Retained lesson | Current adoption/assurance boundary |
| --- | --- | --- |
| #19 [local demonstrator contract](https://github.com/jmservera/ama/blob/5e52ceb7d5937f21a5eb7380ad009833608ed811/prototype/README.md) | Bound model inputs/tools/calls; commit a run before inference, preserve explicit failed/unfinished states and reject stale acceptance. Machine schema/source checks do not establish prose correctness. | Preserve the evidence pattern, not the alternative local SQLite app or compile-only/private-network templates. Durable resume/retry and current real-service/task-quality acceptance need separate proof. |
| #24 [transaction/replay store](https://github.com/jmservera/ama/blob/6029dc248911ddd3eebece5fb2067d881920494c/apps/proper-warm/src/store.mjs) | Case version, event and idempotency response commit together. Bind replay to case, actor and canonical intent, including expected version. Exact retry returns the committed response; changed intent/actor conflicts. Incompatible/unreadable state fails rather than silently reseeding. | A localhost SQLite implementation is not proof of equivalent Azure SQL concurrency/durability. Carry the regression semantics into the current store and uncertain-outcome UI; tab-local retained intent is not restart-proof recovery. |
| #24/#27 [quality replacement and runbook](https://github.com/jmservera/ama/blob/51d8ae41caaa4535ad53c7268f874ce5334242ee/docs/architecture/proper-warm-runbook.md#two-minute-demonstration) | Replacing accepted quality evidence invalidates separate handover acceptance. The reported completion count went 1 -> 0 -> 1 only after fresh independent handover evidence and explicit advancement; prior history/invoice/update commitments remain. | Keep an executable replacement/return/reacceptance regression, not only happy-path stage counts. The #27 runbook is pinned to `40e248a`, earlier than final #24; it is not a second runtime verification. |
| #58 [quality source](https://github.com/jmservera/ama/blob/6cbcb36e63597c6f4b90268207b5f1afbce4bb4a/mvp/properwarm_mvp/quality.py) and [control report](https://github.com/jmservera/ama/pull/58#issuecomment-6102962478) | Evidence and installation/quality milestones must bind the exact current completed work-order and scope version. Material correction/rescope stales affected downstream evidence and blocks incompatible release/payment, while preserving paid history and resident choices. Independent review cannot be supplied by a provider submission or AI draft. | Later draft source/tests differ from main and recorded revision 18. Compare/adopt scoped invalidation and financial lineage, then prove changed-source/image/config/revision behavior; do not infer runtime parity or merge wholesale. |
| #27 [resource ledger](https://github.com/jmservera/ama/blob/51d8ae41caaa4535ad53c7268f874ce5334242ee/docs/architecture/proper-warm-resources.md) | Separate created local resources from proposed Azure services, record ownership/persistence, and inventory before teardown. A docs-only PR creates neither application evidence nor cloud resources. | Its no-Azure-resource statement is experiment-local, not today's `ama` inventory. Proposed queue/agent-state services remain unreconciled with ADR 0001; do not copy that topology or execute old cleanup commands. Current operations stay in the infra handover. |

Retiring #19/#24/#27 preserves these pins and intentionally declines their
alternative delivery routes, not the control requirements. #58 remains an
unresolved selective carry-forward queue. Application acceptance continues
to require actual AI/SQL/Azure, effective authorization/budget, source-bound
workflows and failure/recovery evidence; independent quality, value, human UX,
legal and production gates remain separate. No resource teardown is
authorized by this documentation review.
