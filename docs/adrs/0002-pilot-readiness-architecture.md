---
title: ADR 0002 Pilot-Readiness Architecture for the Zava Forward MVP
description: Proposed decisions for moving the working MVP to pilot readiness over about 60,000 homes - durable store, Blob, Entra ID and field visibility, deterministic ranking, map scale, deployment and gated staff time capture
author: AMA programme
ms.date: 2026-10-13
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
[MVP README](../../mvp/README.md) honest limits and
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
| Map | Server-side bounding-box queries with grid clustering by zoom, same filter object as the list, licensed tile provider | PR-005 |
| Deployment | Two or more replicas, zone redundant where available, `uksouth`, hardened image, scan and tests in CI | No state on the container; fixes the honesty gap |
| Staff time capture | Built behind a feature flag that is off by default and cannot be switched on without a recorded DPIA reference | PR-004 |

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

Proposal:

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

* DPO to confirm the lawful basis per data class, the Article 9 condition and
  that audit data can be retained against an erasure request under
  Article 17(3). Legal to set the legal retention period (PR-001, PR-003,
  DH-007).
* Named owner of the ranking policy and sign-off of the first rule order.
* The roles that have a need to see a vulnerability reason, and the allow and
  deny matrix (OD-14, OD-19).
* Contractor identity model (B2B guests or another route) and tenant owner
  consent.
* Which homes are in live scope out of about 60,000, since the BRD pilot
  assumed 80 to 100 candidate homes (OD-17).
* Licensed tile provider: licence, cost, coverage and processor terms.
* Document malware scanning service.
* Per-year audit table approach and ledger digest verification, to be proven
  by test before it is relied on.
* DPIA, staff notice and consultation view for time capture (OD-36).
* Measured load, latency and cost; the PRD targets stay unmeasured until then.
* Model transfer position for `uksouth` (OQ-012, DH-006).

## Related documents

* [ADR 0001](./0001-azure-architecture.md)
* [Zava Forward Workbench PRD v0.10.0](../prds/zava-forward-retrofit-programme-demonstrator.md)
* [Gap Analysis and Next Build](../reference/research/gap-analysis-next-build.md)
* [Zava Forward MVP](../../mvp/README.md)

## Implementation status

Historical snapshot from 2026-10-08 on branch `feat/mvp-deterministic-ranking`,
with explicitly dated 2026-10-09 deployment updates. "Done" means built and
covered by the tests/local runs available then, not pilot acceptance. Earlier
blocked/unrun rows below are not the current #65 status; see the later delta.

| Item | Status | Deviations |
| --- | --- | --- |
| Ranking policy and AI recommendation (decision 4) | Done | Policy is a hash-checked versioned file with a registry of old versions; ranking snapshot stored as a file and served to managers (not a `ranking_snapshot` table, no scheduled publish step); as_of is the load date of the data, not a per-case stage date; named policy owner and sign-off still open |
| Store interface hardening and durable SQL store (decision 1) | Partial | Azure SQL store (`mssqlstore.py`) built: 26 parity tests on SQL Server 2022 and a run on the dev Azure SQL with a managed identity (2026-10-09), 980 constructed cases; no Azure load test. SQLite remains the dev store; list reads, search, sorts and counts in SQL with keyset paging for the default sort (60,000-case timing tested on sqlite); detail, map, stats, visits, export, closed list and writes still use the in-memory copy; mapping to Azure SQL documented only |
| Ledger hash chain and verify (decisions 1, 2) | Partial | Verify command and endpoint done; digests are local files, not immutable Blob |
| Field projection by role (decision 3) | Done | Free-text notes are not redacted; contractor screens built (needs notice and named contact only) and tested through the server, not with a contractor login in a browser |
| Quality acceptance and procurement (PRD FR-016, FR-017) | Done (API and screens) | Independent acceptance, defects, reinspection, handover and aftercare; packages, evidenced capacity and versioned work orders; both stores; procurement kept as one document, not per-row tables; contractors read their own work orders only; no contractor evidence upload; screens not run in a browser |
| Return, reopen, handoff, safety referral | Done (API and screens) | Screens checked by a Playwright run in desktop Chromium (return, reopen, list, map list); handoff and safety screens checked only for rendering; no screen reader run |
| AI evaluation harness (decision 4) | Partial | Offline, scripted model, ten golden scenarios plus task checks; measures overlap, Spearman, critical misses (fails on any), citation validity, run-to-run variation, latency, model and prompt version, reviewer outcomes and added value; citations validated server-side with a comparison record per AI task and a workflow-only mode; no live-model measurement |
| Accessible map alternative and tile provider (decision 5) | Partial | List view and env-configured provider done; no licensed provider chosen; server tests for the list and tile config, plus a manual Playwright check of the map list; no screen reader run |
| Dockerfile and CI (decision 6) | Partial | Image built and started locally; workflow not yet run on GitHub; not deployed; no scan or multi-replica test |
| Staff time capture (decision 7) | Partial | Off by default, needs `DPIA_APPROVED`, a consultation reference and a staff notice acknowledgement before recording; notice text is a draft, enabled by env with no audited admin action, API only (no screens) |
| Entra ID provider (decision 3) | Partial | Header parsing and role mapping tested with synthetic principals only; Azure configuration documented in the README, not done |
| Blob documents (decision 2) | Partial | `DocumentStore` interface with local and Azure Blob implementations (urllib, SAS or managed identity), size and type limits, role checks, audit; Blob store run only against a fake transport; no malware scan or content sniffing |
| Finance, grants, technical sign-offs and resident decisions (FR-013, FR-014, FR-018, FR-019) | Done (API and screens) | Record-only finance with separate approvers and no bulk path; constructed data, proposed role mapping, exact-match comparison, screens not run in a browser |
| Azure provisioning, replicas, region, load test (decision 6) | Partial | Dev app `ca-properwarm-mvp` on Azure SQL and Blob with a managed identity, min 2 and max 4 replicas, restart persistence checked (2026-10-09); the app is not yet in Bicep, Entra built-in authentication is blocked on an app registration, no load test, region and private networking for the pilot not decided |

### Current Exercise Delivery Delta (2026-10-13)

| Area | Later evidence | Remaining boundary |
| --- | --- | --- |
| SQL and deployment | #65 from-empty Bicep rebuild retained 980 programme cases; the API identity read/wrote SQL and retained audit writes across restart; both model tiers returned source=ai | Generated stock is 60,000 homes; no Azure load/backup-restore proof or calibrated AI benefit |
| Identity and sessions | Callback check, private staff reconciliation, public welcome, own-photo transport and explicit account-picker route are deployed; owner reports administrator/Coordinator sign-in | Different-account replacement, own live photo/consent, all roles, B2B guests and full permissions remain separate acceptance |
| Containers and CI | Tested account-switch image/revision and private configuration-preservation gate are recorded in the operator handover; MVP CI and both validations passed at source head 8ca4a3d | Later edits need their own checks; no production resilience or blanket assurance claim |
| Documents and audit | SQL/Blob configuration replaces the local-only development defaults; append-only audit controls and startup-cache convergence are implemented | Malware/content scanning, external immutable digests, deletion/retention approval and recovery remain open |

The [current handover](../../infra/README.md#current-exercise-handover-2026-10-13)
and [MVP limits](../../mvp/README.md#honest-limits) own the version-linked
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
