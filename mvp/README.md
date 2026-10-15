# Zava Forward MVP

A working case-management application for the Zava Forward retrofit programme.
It follows the simplicity requirements SA-001 to SA-010 in the
[PRD](../docs/prds/zava-forward-retrofit-programme-demonstrator.md) and the
[prototype learnings review](../docs/reference/research/ux/prototype-learnings-and-simplicity-review.md).

## What staff see

* Sign in once and land on "My cases today", with open safety issues first.
* A full-screen case card: contact details, preferences and support needs, a
  plain status line, owner, contractor, next visit and history.
* Log a call, record the resident's own answer, hand a case to a colleague and
  draft a message. Nothing is sent automatically.
* "Ready to book" is checked on the server: the resident's decision, funding
  and any open safety issue must all be confirmed. Unknown never passes.
* Filter the list by stage, local authority, wave, owner or flag, and sort by
  urgency, longest wait, last contact, name or next visit.
* The default "Most urgent first" order is a deterministic ranking
  (`zavaforward_mvp/ranking.py`): open safety issue, then priority support or an
  adjustment, then longest time in stage, then earlier stage, then case id as
  the fixed tie-break. Each card shows its rank and plain reasons, the list
  header shows the policy version, policy hash and as-of date, and
  `GET /api/ranking/policy` returns the versioned rules. The rules live in
  versioned files in `policies/` (for example `ranking-v1.json`) with a policy
  id, version, owner, status, effective date and a SHA-256 content hash over
  the canonical JSON. Every file is verified when loaded and a mismatch stops
  the load. Old versions stay in the folder and can be re-run. Ranking takes
  the case data, a policy and an explicit `as_of` date and reads no clock.
  `GET /api/ranking/snapshot?policy=1.0.0` (managers only) returns the
  snapshot: policy version and hash, as-of, and per case the rank, reason codes
  and deciding rule. It is also written beside the data when it changes. The
  policy owner is "to be named" and the rule order is an unsigned draft.
* "Suggest my top 5" on My cases asks AI for a second opinion beside the
  rule-based order, labelled "AI suggestion, not approved", with a cited reason
  per case. It is stored in a separate recommendations list and is never read
  by the ranking, owners, stages or queues. A person accepts, edits (untick
  cases) or rejects it, with a reason for edit and reject, and the answer goes
  in the audit log. Without a model a rules-based template is used.
* The case list loads 50 at a time ("Show more"; the API allows up to 100 and
  returns the total). The Overview map is requested by viewport and shows grid
  clusters with counts when more than 500 homes are in view. List and map totals
  agree for the same filter. The CSV download still returns the whole filtered list.
* Filters sit in a left panel and update the list without reloading the page.
  The briefing is cached until case data changes.
* Overview: counts that filter the map when clicked, a zoomable OpenStreetMap
  of open cases (Leaflet bundled in `web/vendor`; names show on hover; teal normal, amber waiting 60+ days,
  red open safety issue), charts by stage, authority, wave and waiting time,
  contractor and team workload. Visits lists booked appointments by day.
  The dated synthetic generator now guarantees six additional forward
  assessment visits and retains historical attended/no-access/cancelled
  contrasts. See the [coverage recipe](../docs/reference/research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13)
  for reproducible dates, queue counts, private outputs and safety limits.
* "Who could take this on": top three colleagues with plain reasons (role
  fit for the stage, current workload, who already knows the resident).
* AI assistance, always a draft for a person: a morning briefing, a drafted
  message, a "catch me up" summary, funding application wording, and reading
  an uploaded document. It runs on Azure OpenAI through the managed identity.
  Output is checked, every run is audited, and a plain template is used when
  the model is unavailable. Each output carries source citations that must
  resolve to a real field or record of the case (for example "Stage: Survey
  booked", "Case history 2026-09-30"). They are checked on the server: output
  whose citations do not resolve is marked Unverified, uncited summary bullets
  and uncited priority items are dropped, and the sources are shown beside the
  "AI suggestion, not approved" label. Output stays "Not reviewed" until a person accepts, edits or
  rejects it. Workflow-only mode (request flag `mode: "workflow"`, the "Workflow
  only" tick box, or `ZF_AI=off`) skips the model for every task and is
  recorded. Each task leaves a comparison record (case ids, AI output,
  workflow-only output, fallback reason, reviewer action and override) in the
  recommendation store, in both the JSON and the sqlite store.
* Documents: upload pdf, png, jpg, docx, xlsx, csv or txt (5 MB), see an
  evidence checklist (EPC, survey, design, consent) and download files.
* Funding: a person moves each application through draft, approved,
  submitted and confirmed. Approval needs complete evidence and the Grants
  and Evidence Officer or a manager. The system never submits anything.
* A hash-chained audit log records every change. `GET /api/audit-check`
  (manager) and `python -m zavaforward_mvp.ledger` verify the chain; a digest of
  the head can be written to `ZF_DIGEST_DIR` (`POST /api/ledger/digest`) and is
  re-checked on verify. The digest is a local file, not yet an immutable Blob.
* Role-based field projection is enforced on the server (`projection.py`).
  Contractors see only their own cases with "needs notice" and a named contact
  (the case owner), never the vulnerability reason, resident name or contact
  details. Staff see the reason only for the roles in `ZF_REASON_ROLES`
  (default Resident Liaison Officer, Building Safety Liaison, Retrofit Programme
  Manager); others see "Extra support noted". Every role is tested against every
  endpoint (`tests/test_role_matrix.py`). Free-text notes are not redacted.
* Workflow screens on the case page: send a case back to an earlier stage with a
  reason, reopen a closed case (manager, from the "Closed cases" page), offer,
  accept, decline or withdraw a handoff (pending handoffs show on the work
  list), and safety referral (raise, refer, record repair, release by a
  different person). All use the existing API and its server-side checks.
* Contractor screens: "My jobs" and a job page show only the address, stage,
  next visit, "needs notice" and a named contact. The server projects the data
  (`projection.py`); the screens never request resident detail. The rank and
  reasons are not sent to contractors either.
* Quality acceptance (FR-017, `quality.py`): per measure, evidence against a
  versioned checklist (every check needs a note of what was seen), then accept
  or return with a defect and an owner, fix, reinspect, resident handover and
  aftercare notes. States move one step at a time on the server and are
  audited. Whoever accepts must differ from whoever submitted, recorded or
  fixed the work, and nothing is accepted automatically. Provider submissions
  are stored as evidence only.
* Procurement and capacity (FR-016, `procurement.py`): packages with period,
  versioned scope and contract reference; offered capacity kept apart from
  capacity committed with evidence; controlled work orders (each change a new
  version with its issuer, none issued beyond evidenced commitment);
  appointment outcomes, completion and correction. Managers get "Capacity and
  work orders"; contractors see only their own orders, with "needs notice" and
  no reason. Packages and orders are held as one document in the JSON file or
  the sqlite `meta` table, so they work in both stores.
* Documents sit behind a `DocumentStore` interface (`documents.py`). The local
  filesystem store is the default (`ZF_DOC_STORE=local`, `ZF_DOC_DIR`). The Azure
  Blob store (`ZF_DOC_STORE=blob`) uses urllib against the Blob REST API with a
  SAS token (`ZF_BLOB_SAS`) or a managed identity token (`ZF_BLOB_CLIENT_ID`
  optional); config is `ZF_BLOB_ACCOUNT_URL` and `ZF_BLOB_CONTAINER`. Uploads
  allow an extension list and 5 MB, need a staff role (contractors cannot
  upload or download) and write audit entries for upload, download and failure.
* The map has a "Show the map areas as a list" alternative: a keyboard and
  screen reader list of clusters (zoom in) or homes (open case), with a polite
  live status line. The tile provider comes from `ZF_TILE_URL` (https only) and
  the CSP follows it. With `ZF_ENV=production` and no `ZF_TILE_URL` no tiles
  load and only the list works.
* Evaluation dataset registry (`evals/registry.json`) lists every golden and
  evaluation dataset with version, owner and purpose; a test fails for an
  unregistered file in `evals/`. The stock-scale fixture (60,000 homes, 600,000
  events, wholly fictional, seeded) is rebuilt with
  `PYTHONPATH=. python3 -m zavaforward_mvp.scale_fixture`, writes to the
  Git-ignored `data/scale-fixture/` and is never committed. Dataset owners are
  an open owner decision.
* AI evaluation harness, offline: `PYTHONPATH=. python3 -m zavaforward_mvp.ai_eval`
  runs golden scenarios (`evals/ai_priority_golden.json`) with a scripted model
  and checks that ranking and case data never change, the output stays Proposed
  and needs a person's reason to edit or reject. It fails on any critical miss
  (a case with an open safety issue missing from the AI top-k) and on any cited
  fact that is not in the case data, and reports top-k overlap, Spearman rank
  correlation, run-to-run variation on identical input, latency, model and
  prompt version, reviewer accept/edit/reject counts with reasons, and the
  AI's added value against the deterministic and workflow-only orders on the
  same cases. `--json` prints the full report; managers can read it, with the
  live reviewer counts, at `GET /api/ai/report`. Negative controls in
  `tests/test_ai_tasks.py` break each property and expect the harness to fail.
  The report also carries an `evidence` block (issue #108): SHA-256 of the
  frozen golden file, prompt version, provider (scripted), "not evaluated" for
  actual-model and human effectiveness, calibration "not applicable", benefit
  claim "not permitted", and the open items (Foundry model, version and quota
  confirmation in the chosen region, authorised live calls, held-out split and
  thresholds, human protocol, Finance validation). Any critical miss fails the
  run.
* Staff time capture (PR-004) is off by default. It records only when
  `ZF_TIME_CAPTURE=on`, `DPIA_APPROVED` and `ZF_TIME_CONSULTATION` each hold a
  reference, and the person has acknowledged the staff notice
  (`POST /api/time/acknowledge`, audited); own entries only;
  reports are manager-only, aggregated and suppress groups under
  `ZF_TIME_MIN_GROUP` (default 5). It uses its own database, never the case store.
* Download any list for Excel, and check a spreadsheet: columns are matched
  for you, rows to fix are listed and the file is never changed.

* Finance, grants, sign-offs and resident decisions (FR-018, FR-019, FR-013,
  FR-014; code in `finance.py`, `grants.py`, `signoffs.py`,
  `resident_decisions.py`, `controls.py`):
  * Budgets, commitments, invoice or valuation intake, line-level match
    exceptions, payment holds and a Finance decision are recorded per case
    (`POST /api/cases/{id}/finance`, queue at `GET /api/finance`). Nothing is
    ever paid; payment status is a note. Unknown inputs (no budget, no
    milestone evidence) block a match.
  * Grant stages (opportunity, award, claimable, submitted, accepted or
    rejected, cash received) are kept apart from invoices, each with a source
    and a second approver (`/grant`; also shown in the funding list).
  * Assessment, design, building and coordination sign-offs by separate roles
    with a design version; a design change sends only the affected sign-offs
    back for human reassessment, and missing items join the "ready" checks
    once a design is recorded (`/technical`).
  * The resident's answer is recorded per measure with versions, pauses and
    withdrawals, starts as "Not recorded" and is never inferred; service and
    complaint requests carry a desired outcome, a redress owner and coded
    contact needs (`/resident`).
  * Whoever prepares an approval cannot give it, and these refuse any bulk
    request. Contractors get none of it and other staff roles do not see
    finance or grant detail.

## Law store (ADR 0005, phase 1)

`zavaforward_mvp/lawstore.py` loads the dated snapshots in `docs/reference/regulatory/`
into append-only tables (`reg_source`, `reg_version`, `reg_provision`, `reg_gap`) and
writes each snapshot once, content hashed, through a snapshot interface. The target is
Azure only: `ZF_LAW_STORE=mssql` uses Azure SQL (the `ZF_SQL_*` settings of the main
store; append-only ledger tables when the database is ledger enabled, otherwise an
append-only trigger) and `AzureBlobSnapshots` (`ZF_LAW_BLOB_ACCOUNT_URL`,
`ZF_LAW_BLOB_CONTAINER`, `DefaultAzureCredential`; writes never overwrite). SQLite and a
local folder (`ZF_LAW_DB`, `ZF_LAW_BLOBS`) are local test doubles only. Seed with
`python -m zavaforward_mvp.lawstore REGULATORY_DIR DB_FILE BLOB_DIR` (or
`ZF_LAW_STORE=mssql python -m zavaforward_mvp.lawstore REGULATORY_DIR`); a changed file
becomes a new version and nothing existing is altered. Partial sources carry
`completeness: partial` and results say so. Leasehold, complaints handling, TrustMark
and licensed PAS 2035 are gaps answered as "no source held". The keyword index
(`rebuild_index`) is derived from SQL. The same suite runs on SQL Server in the CI
`mssql` job (`test_lawstore.MssqlStoreTests`). Open items: the Azure Blob container
immutability (WORM) policy and the Azure SQL deployment are infrastructure and are not
verified here; the Azure Blob client is tested only against a fake container. The
read-only viewer at `/law.html` and `/api/law/*` serves staff roles with no AI. Seeded
versions are `not_reviewed` with owner "to be named"; this is a reference copy, not
legal advice or approval. Seed metadata is `law/law-source-register.json`.

## Rule cards (ADR 0005, phase 2)

`zavaforward_mvp/rulecards.py` holds versioned rule cards in append-only tables
(`rule_card_version`, `rule_card_event`, `rule_card_review`, `rule_card_review_event`) with a draft, approved,
active, held, retired lifecycle. A card is drafted by the `rule_author` role and only
its named `rule_owner` can approve, activate, hold, release or retire it; an author
cannot approve their own card. Versions, approver, approval date and effective dates
are retained. `source_changed` records an open review item (RULE-021, AC-068) naming the
affected card, active version, requirements and tests, source versions and effective date,
and never alters an approved card. `assess_review` lets only the card's named owner record
the interpretation, tests, effective date, notification, rollback and any hold; it never
activates a rule, so activation still needs propose, approve and activate by named humans.
The card-to-requirement and test trace for the two seed cards is a static exercise map;
unmapped cards are flagged for the owner. The two seed cards (hazard awareness clock, automated decision
safeguard) are labelled exercise fixtures with simulated approvals only; they are not
law or real approval, and the owner, clock durations and citations remain open items
for named Compliance and DPO approval. Mapping the roles to Entra app roles (#116)
and the rule engine are not done here.

## Configuration

| Variable | Purpose |
| --- | --- |
| `ZF_STORE` | `json` (default), `sqlite` or `mssql` (Azure SQL, see below) |
| `ZF_SQL_SERVER`, `ZF_SQL_DATABASE`, `ZF_SQL_AUTH`, `ZF_SQL_CLIENT_ID`, `ZF_SQL_PORT`, `ZF_SQL_TRUST_CERT`, `ZF_SQL_TOKEN`, `ZF_SQL_USER`, `ZF_SQL_PASSWORD` | Azure SQL connection; `ZF_SQL_AUTH` is `msi` (default), `default`, `token` or `password` (CI container only) |
| `ZF_SQLITE`, `ZF_STATE`, `ZF_DATA`, `ZF_DIGEST_DIR` | database file, state folder, seed data, ledger digests |
| `ZF_AUTH` | `password` (dev, default) or `trusted-proxy` (Entra) |
| `ZF_ENV` | `production` refuses the password provider and the OSM tile default |
| `ZF_SESSION_KEY` | signs dev session cookies; set the same value on every replica |
| `ZF_ENTRA_TENANT_ID`, `ZF_TRUSTED_PROXY`, `ZF_ROLE_MAP`, `ZF_AUTH_EMAIL_FALLBACK` | Entra provider |
| `ZF_REASON_ROLES` | roles that may see a vulnerability reason |
| `ZF_TILE_URL`, `ZF_TILE_ATTRIBUTION` | map tile provider |
| `ZF_TIME_CAPTURE`, `DPIA_APPROVED`, `ZF_TIME_CONSULTATION`, `ZF_TIME_DB`, `ZF_TIME_MIN_GROUP` | time capture |
| `ZF_DOC_STORE`, `ZF_DOC_DIR`, `ZF_BLOB_ACCOUNT_URL`, `ZF_BLOB_CONTAINER`, `ZF_BLOB_SAS`, `ZF_BLOB_CLIENT_ID` | document store |

### SQL store

`ZF_STORE=sqlite` uses `sqlstore.py` on stdlib sqlite3 as the dev and test
driver, with the same `Store` interface. Each case row has a row version and a
save is `UPDATE ... WHERE rowversion = ?`; a lost race returns HTTP 409, and
nothing is written. The audit table is full-content, append-only (triggers
refuse update and delete) and hash-chained. Indexes cover the list filters,
owner, open safety issues, postcode, address and the ledger sequence, and a test
checks the query plans use them. No per-process state is needed for
correctness: a second process catches up from a database sequence before every
operation, and dev sign-in cookies are signed, not held in memory.

List reads are answered by SQL: each row carries derived, indexed columns
(a fixed-width rank key built by `ranking.sql_key`, days, owner, contractor,
stage, flags, search text). Filters, sorts, search, totals, header counts and
paging run in SQL, and ranks are global (a window over open cases). The default
sort also has keyset paging (`after` cursor, `next_cursor` in the response),
which the work list uses for "Show more"; other sorts use offset in SQL. A
migration adds the columns and rebuilds keys when the ranking policy version
changes. Tests check parity with the in-memory store, query plans and a
60,000-case timing.

Azure SQL is implemented by `mssqlstore.py` and has run with the API managed
identity. It uses explicit `BIGINT` row versions, `NVARCHAR(MAX)` JSON bodies,
binary text collation and a transaction-owned `sp_getapplock` writer lock.
The audit table is append-only ledger when the database supports/enables it,
otherwise an `INSTEAD OF UPDATE, DELETE` trigger rejects mutation. External
immutable digest anchoring and the per-year ledger-table design in ADR 0002
remain open; a hash chain alone does not prove those proposed controls.

### Entra ID on Container Apps

Code: `auth.py`. The current demonstrator uses this provider in Azure;
the owner confirmed working workbench sign-in on 2026-10-12. Local tests and
provisioning checks do not substitute for each user's consent/acceptance.

* Create an app registration (single tenant) and define app roles whose values
  match the map (default `ZavaForward.Coordinator`, `.LiaisonOfficer`,
  `.ProgrammeManager`, `.Contractor` and so on, see `DEFAULT_ROLE_MAP`) or
  supply `ZF_ROLE_MAP` JSON. Assign users and groups to them.
* Enable built-in authentication on the Container App with "require
  authentication" so unauthenticated requests are blocked, and make the ingress
  the only route to the container so `X-MS-CLIENT-PRINCIPAL` cannot be forged.
* Set `ZF_AUTH=trusted-proxy`, `ZF_TRUSTED_PROXY=1`, `ZF_ENTRA_TENANT_ID` and
  `ZF_ENV=production`. The platform principal type must be `aad` or `Bearer`,
  from that tenant, with exactly one distinct mapped role; the role comes from
  the validated platform principal, never the staff file.
* Provision each staff record with the Entra object id (`oid`). Email matching
  is off unless `ZF_AUTH_EMAIL_FALLBACK=1`. Contractor guests need the same.
  Use the [tenant staff initializer](../infra/README.md#tenant-staff-and-application-role-initialization)
  to reconcile enabled tenant members, app roles and SQL bindings together.
  It replaces current generated staff/owner labels while preserving workload
  codes and historical actors, then restarts the startup-cached roster.
  Assigning an enterprise-app role without this binding still fails closed.
* Sign-out redirects through `/.auth/logout` to the public welcome;
  "Use another account" instead enters `/sign-in?switch=1` directly with
  `prompt=select_account`, without signing out of Microsoft first. Choosing
  another account is deliberate, not automatic; cancelling need not clear
  the previous session. See [flow diagnostics and acceptance](../infra/README.md#account-selection-and-safe-flow-diagnostics).
  State-changing requests need an
  `X-ZF-CSRF` header under this provider.

The public `/` page shows Zava Forward and its logo without loading workbench
scripts or data. Its button enters `/sign-in`; `/app` is protected. Production
session/role failures show Microsoft sign-in or an authorisation message,
never the local shared-password form.

The native account panel shows the authenticated Entra display name/email,
existing workbench role and own Microsoft profile photo. It does not rewrite
synthetic staff records or broaden contractor projections. Escape/outside
click closes the panel; keyboard focus and a 375-pixel layout are supported.
Missing photos/access errors display initials and an explicit status.

`/api/account/photo` authenticates and authorises the current user before
fetching the fixed Graph `/me/photo/$value` URL. The delegated platform token
stays server-side, redirects are refused, and timeout/type/signature/2 MiB
limits apply. There is at most one provider refresh attempt for token expiry.
See [staged token-store setup and permissions](../infra/README.md#public-welcome-and-microsoft-account-photos).
This uses only delegated own-user `User.Read`, not tenant-wide application
photo access. Local password development shows initials without requesting
Microsoft tokens.

The CSP permits temporary `blob:` URLs only for images, so the server-proxied
photo can render; script/default/frame source permissions are unchanged.

## Run it locally

The working data is built from the private stock-geography register. It holds
real OpenStreetMap addresses with invented residents, contractors and staff, so
it is git-ignored, binds to loopback only and must never be committed, deployed
or shared. The repository must stay private.

```bash
python3 support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py --seed 20260901
cd mvp
ZF_PASSWORD=choose-a-password python3 -m zavaforward_mvp.server
```

Open `http://127.0.0.1:8088` and sign in with a staff email from the data (for
example `aisha.rahman@zavanorthhomes.example`). Without `ZF_PASSWORD` a random
password is printed at start-up. The data builder shifts all dates so the
history ends today and prints no real personal data.

### Azure SQL store

`ZF_STORE=mssql` uses `mssqlstore.py`, a T-SQL dialect over the same `SqlStore`
logic, with the pinned `mssql-python` driver (`requirements.txt`, hashes
checked in the image build; the image adds `libltdl7` and `libkrb5-3`). Writers are
serialised across replicas by a transaction holding an exclusive application
lock (the equivalent of SQLite's write lock), every compared text column uses a
binary collation so ordering matches the other stores, and a connection dropped
between requests is reopened. Sign-in is Microsoft Entra with the app's managed
identity (`ZF_SQL_AUTH=msi`, plus `ZF_SQL_CLIENT_ID` for a user-assigned one), so
there is no database password. The audit table is an append-only ledger table
when the database has Azure SQL ledger enabled (the engine refuses update and
delete), otherwise an `INSTEAD OF` trigger does it. Every other table in a ledger
database also keeps row history, which matters for erasure and retention
(DPIA item to resolve before real data).

The first start seeds an empty database from `ZF_DATA`; the image carries no data,
so seed once from an operator machine with `ZF_SQL_AUTH=token` and
`ZF_SQL_TOKEN=$(az account get-access-token --resource https://database.windows.net/ --query accessToken -o tsv)`.
The app identity needs a contained user with `db_datareader`, `db_datawriter` and
`db_ddladmin` (see `infra/scripts/create-sql-users.sql`). `tests/test_mssqlstore.py`
runs the SQL store suites and the list-read parity suite against a real SQL Server
when `ZF_TEST_MSSQL=1` (and `ZF_SQL_*` point at a throwaway database).

## Frozen protocol, benefits register and release gates (issue #126)

`zavaforward_mvp/governance.py` records, and never decides, the pilot governance in the existing store (JSON or SQL, so it survives a restart). Managers use `GET /api/governance` and `POST /api/governance/{protocol-freeze,protocol-approve,benefits-record,benefits-approve,release,breach,restart}`. No AI assistant, ranking or tool has any part in it.

* Protocol (RULE-019, AC-062): a version freezes all thirteen required fields. A different person approves it with the OD-36 DPIA and lawful measurement-basis references. A change needs a reason and a new approval. `capture_gate()` keeps Phase 0 capture closed until the latest version and the BG-011 register are approved.
* Benefits register (BG-011, OD-18): event definitions and the MDE are recorded. `target_verdict` never returns pass or fail when the MDE is missing or exceeds a target (20% cycle time, 25% coordination hours); it returns "Not assessable" or "Interval estimate only".
* Release decisions (RULE-020, AC-063): each phase (Phase 0 capture, Shadow testing, Live pilot) and tranche has a Release or Withhold record with requirements, evidence, unresolved issues, cost and risk envelope reference and named approvers. Releasing Phase 0 capture needs the capture gate; Shadow testing needs entry evidence, and Shadow testing and Live pilot need Phase 0 capture released first.
* Guardrail breach (RULE-024, AC-078): `breach_record` (managers, quality inspectors and building safety liaisons, so a hazard-aware role can raise a breach without waiting for a manager) pauses the home, work package, archetype or workstream. `breach_restart` needs a different person, the OD-35 authority reference, accepted remediation evidence and a Release decision recorded after the breach. `guard_case_event` calls `require_not_paused` (home by case id or address, archetype by home type) and, for cases flagged `pilot`, `require_capture_open` in `log_call`, `set_decision`, `advance` and `return_case`; emergency and statutory hazard response continues outside any pause.

Tests: `tests/test_governance.py` (JSON and SQL stores, labelled synthetic demonstration values). Open items, not invented here: the real OD-18 definitions and MDE, the OD-36 DPIA and lawful basis, the OD-35 named authority, actual approvers, how cases are enrolled in the pilot cohort (the `pilot` flag), pause scopes for work package and workstream, and extending the guard to the remaining case workflows. The RAI closure registers in the issue (eleven residuals and eleven unassessed checks, a fresh current-source assessment, owner acceptances) are not delivered or claimed closed by this change; every item stays proposed or insufficient until qualified owners and fresh evidence exist, and live use stays blocked.

### Per-year ledger digests, load check and recovery drill (issue #114)

* `python -m zavaforward_mvp.ledger --seal-years` writes one immutable `year-YYYY.json`
  digest per completed year (entries, first link, head); `--by-year` verifies every
  year on its own, the links between years and each sealed digest, and reports a
  dropped sealed year. A self-consistent rewrite of a sealed year is caught only by
  its digest, so those files belong in the immutable Blob container. Proven in
  `tests/test_recovery.py`; run the scheduled `--by-year` check before relying on the ledger.
* `python -m zavaforward_mvp.loadcheck --data zavaforward.json --homes 60000` runs the
  NFR-002 mix (five sessions, two writers) against the configured store and prints
  p50/p95/max per class. Local SQLite on 2026-10-15 over 60,000 labelled synthetic
  homes for 30 s: list p95 0.28 s, detail 0.30 s, write 0.33 s, no errors (limits 1 s,
  1 s, 2 s). Open items: the same run against Azure SQL, dashboard and import preview
  classes, and cost (needs Azure meter rates and measured vCore time).
* `zavaforward_mvp/recovery.py` erases a resident's personal fields and keeps a
  personal-data-free deletion register outside the database. The register is one
  write-once entry per erasure under the reserved case id `_erasures` in the document
  backend: Azure Blob Storage when `ZF_DOC_STORE=azure-blob` (same configuration as case
  documents), a local folder only as the local-test backend. The entry is written
  before the redaction, so a crash between the two leaves an erasure that
  `reapply_deletions` completes (audited as `erasure_reapplied`), never an unrecorded
  one; if the register cannot be written, nothing is redacted, and an unreadable
  register is an error, never an empty one. Tests: a SQLite backup restore proves the
  erasure returns, a fake Blob transport proves the register backend and the write
  ordering.
* Unverified: the Azure SQL point-in-time restore drill (DH-005) has not been run;
  the register has not been run against a real storage account, nor has its
  retention or immutability policy been configured or tested; the Blob container
  should carry a WORM/immutability policy, which is infrastructure and unproven here;
  cost (storage, transactions, restore) is not measured.

## Honest limits

Current scope is the continuing exercise, not production acceptance. Dated
earlier observations remain in the ADRs and pinned #58 evidence; they must not
be read as the current deployment state. The
[current infrastructure handover](../infra/README.md#current-exercise-handover-2026-10-13)
records the tested/deployed image and identity initialization.

* The data is constructed. The generator (`zf_names.py`, `build_mvp_dataset.py`)
  makes names, phone numbers on Ofcom drama ranges and example email domains.
  The product screens do not say so; this README and the repository do.
* The 2026-10-12 rebuild ran the retained 980-case programme on real Azure SQL
  with workload-identity reads/writes, both real model tiers and restart
  persistence checks. Blob is the configured evidence store. Generated stock
  remains 60,000 homes; it is not 60,000 live SQL programme cases. No Azure
  load, full recovery, backup-restoration or production acceptance is claimed.
* Shared-password sign-in remains local development only; production rejects
  it. Azure uses built-in Entra authentication, app roles and explicit SQL
  staff bindings. The owner reports working administrator/Coordinator sign-in.
  A tenant-member Contractor allocation now exists, but browser acceptance
  for all roles, B2B guests, own photo and actual different-account replacement
  remains unproved. Unit principals and an anonymous chooser are not that proof.
  Contractor status text can still mention a safety stop and free-text notes
  are not redacted.
* AI needs `AI_ENDPOINT` (and optionally `AI_DEPLOYMENT`,
  `AI_DEPLOYMENT_STRONG`) and a managed identity with the Cognitive Services
  OpenAI User role. Both model tiers were exercised with `source=ai`; a
  template result alone is not real-inference acceptance. Nothing is
  sent; there is no live integration with housing or repairs systems.
* In development the map loads tiles from tile.openstreetmap.org unless
  `ZF_TILE_URL` is set. No licensed provider has been chosen or tested.
* Local development defaults to local state/documents; Azure selects the
  SQL/Blob backends through configuration. Do not apply local-disk durability
  claims to that deployment or infer tested Blob restoration/erasure from
  configuration alone. Upload checks are an extension list and a size cap:
  no content sniffing or malware scan. Local files/digests on Container Apps
  remain ephemeral and do not establish external immutable audit anchoring.
* Scale: the in-memory store handles 60,000 synthetic cases for filtered pages
  in tens of milliseconds (about 0.6 s for the first, cold ranking build). The
  sqlite store answers list pages, search, sorts and counts in SQL at 60,000
  cases in roughly 50 to 150 ms on a development machine. These are dev
  machine figures, not production latency, and not Azure SQL.
* The ranking policy is a hash-checked file but not signed off: no named
  owner yet. The hash detects edits, it does not prove who approved them.
  Snapshots are written when a manager requests one and the data has changed,
  as a file, not on every change or in a database table. The as-of date is the
  date the store was first loaded, and day counts come from the stored
  `days_in_stage`, not recomputed from it. AI value against the deterministic
  order is only captured as the overlap on each recommendation record.
* SQL Server parity tests and live Azure SQL checks supplement sqlite tests;
  neither establishes production scale or every full-workflow requirement.
  Lists, search, sorts and counts
  use SQL, but case detail, map, statistics, visits, facets, the CSV export,
  the closed list and every write still use the in-memory copy that is kept
  in step with the database. Keyset paging covers the default sort only.
* Quality and procurement: checklists are examples, not signed-off standards;
  there is no contractor login to submit evidence (a staff member records it on
  their behalf); capacity is counted in homes, not hours or money; procurement
  data is one document, so two managers writing at once get a conflict and
  retry; the screens were syntax-checked and exercised through the API, not
  run in a browser or with a screen reader.
* Time capture has no screens, only the API. It is enabled by environment, not
  an audited admin action. The staff notice text is a draft and the
  consultation reference is a flag, not evidence of the consultation. The AI
  evaluation uses a scripted model, so it checks behaviour, not model quality:
  latency, run-to-run variation and added value are scripted figures, not
  live-model measurements, and the golden cases are small and constructed.
  Citations prove a cited fact exists in the case, not that the claim made from
  it is right, and document reading cites the document record, not a passage.
* Browser checks: `tests/browser_check.py` drives the real server with
  Playwright (login, list with rank and reasons, show more, return, reopen,
  map list). It is run by hand, is not in the unittest run or CI, and was
  run in desktop Chromium only. No screen reader or mobile run was done.
* The Dockerfile pins a base digest and runs as UID 10001 with no data baked in.
  Versioned images have been deployed; MVP CI test/image/mssql jobs and both
  validation workflows passed for source head `8ca4a3d` on 2026-10-13.
  The deployed account-switch image is linked in the infrastructure handover,
  not assumed rebuilt from later documentation-only commits. Future edits need
  their own checks; a scorer's successful execution is not product acceptance.
* Finance and sign-off rules are a proposal on constructed data: the role
  mapping (for example Quality Inspector for assessment) is a stand-in for the
  PAS 2035 roles, matching is simple exact comparison, amounts are not tied to a
  real ledger, there is no supplier or contract master, and the screens were
  syntax-checked but not run in a browser or with a screen reader. The product
  has no bulk edit yet, so the bulk refusal is tested on the API only.
* Retention periods and legal bases remain proposals for the DPO and Legal.

## Container hardening checks in CI

The `image` job in `.github/workflows/mvp-ci.yml` builds the image and checks:

* it runs as UID 10001 and contains no working data;
* it starts and answers `/healthz` with `--read-only --cap-drop ALL
  --security-opt no-new-privileges`, with only `/tmp` and `/state` (`ZF_STATE`)
  mounted as tmpfs, the seed data mounted read-only, and writes to `/state`
  succeed while writes to `/app` and `/` fail;
* a Trivy scan fails the job on any HIGH or CRITICAL finding that has a fix
  available (`ignore-unfixed`). Unfixed findings in the pinned Debian base are
  not blocked, so they are visible in a local `trivy image` run but not
  gated. The fix for a fixable OS package is the `apt-get upgrade` in the
  Dockerfile, never an ignore file;
* an SPDX SBOM (`zavaforward-mvp-sbom` artifact) is generated and uploaded.

Actions are pinned by commit SHA. The workflow result on GitHub is what proves
these checks; running the same commands locally is only a preview. Document
files default to `ZF_STATE/docs`, or set `ZF_DOC_DIR`; the app writes nowhere
else. The SQL Server integration job is not part of this job.

## Tests

### Five retrofit assistants (2026-10-13 implementation)

The existing workbench now has five separate v1.0.0 capabilities:
`stock-prioritisation`, `assessment-preparation`, `funding-evidence`,
`works-resident-coordination` and `quality-evidence`. Each case card exposes
the controls permitted for the current role. "Assistant proposals" opens the
shared role-owned queue. This is a proposal service, not a case automation
engine: generation and review never change ranking, ownership, funding,
consent, appointments, work orders, safety holds or quality sign-offs.

| Capability | Request and proposal-review roles | Synthetic proactive gap check |
| --- | --- | --- |
| Stock | Retrofit Coordinator, Retrofit Programme Manager | Missing home EPC/type/build year or conflicting disclosed survey values |
| Assessment | Retrofit Coordinator, Retrofit Programme Manager | Missing Survey/Design metadata or hash, missing design version, changed relevant source |
| Funding | Grants and Evidence Officer, Retrofit Programme Manager | Missing measures/route/reference/grant/budget, incomplete supplied invoice inputs, claim-phase source-history/Funding evidence gaps; changed relevant source/terms |
| Works/resident coordination | Retrofit Coordinator, Resident Liaison Officer, Retrofit Programme Manager | Offered handoff, missed recorded appointment or overdue open service-request update |
| Quality | Quality Inspector, Retrofit Programme Manager | Missing measure/checklist evidence, conflicting evidence, obsolete checklist or changed relevant source |

These are selected synthetic exercise rules (`synthetic-gaps-2026-10-13-v1`),
not approved company rules or an assessment of funding eligibility. Unknown
fields, missing document versions/content hashes and unavailable provider
usage remain explicit unknowns/nulls. Existing document records are not
backfilled or silently asserted to have hashes. New uploads record SHA-256
and version 1 in the existing document metadata.

Source capture is an allowlist safe for every permitted reader: stock excludes
resident support/safety ranking inputs and private ranking reasons; other
non-finance capabilities exclude finance. Coordination includes disclosed
contact/access preferences but no vulnerability reason, handoff free text or
complaint narrative. Funding includes structured budget, commitments, invoice
lines, grants and permitted evidence metadata, not an old `funding_draft`
invocation. Document filenames, AI summaries and arbitrary document contents
are not copied into shared proposals. Citations identify captured categories
and hashes, not passages or proof that the model's conclusion is correct.
Each response rechecks the current staff record, role and optional `case_ids`
and `areas` scopes. Contractors and unknown roles are default-denied. A revoked
staff role cannot read an earlier proposal merely by retaining a session.

Human review has two separate operations: first explicitly record source
verification with a note, then accept or edit-accept. The accepting person
must have their own current verification. Quality review additionally uses the
existing independence check against evidence submitters, recorders and fixers.
This is independent proposal review, not competent technical sign-off or
quality acceptance. Failed, malformed, template, missing-citation and stale
proposals cannot be verified or accepted. Rejection and history remain
available to authorized current readers; a rejected worker cannot complete
over that decision. Manual case work remains available during model calls,
disabled configuration, failure, exhaustion and stale evidence. Case controls
render before auxiliary assistant reads finish. Those reads share a 10-second
abort deadline with a visible manual fallback; detached/different-route panels
ignore late results.

#### Operator authority and finite allowance

The new service requires `ZF_STORE=sqlite` or `mssql`. JSON-only operation keeps
the existing app usable but exposes disabled assistance/manual routes.
No new AI/model dependency or resource is required. Existing AI endpoint and
standard deployment settings are used; no model is called by the test suites.

Automatic scanning is off by default. Both reactive execution and proactive
execution require a configured AI provider and a valid bounded operator
authority. Configuration alone is not approval: an operator must obtain
scoped approval for rollout, the authority reference, expiry and finite call/
token allowances before configuring these settings.

| Environment setting | Default | Effective constraint |
| --- | --- | --- |
| `ZF_ASSIST_AUTHORITY` | Empty (disabled) | Approved exercise reference, 1-120 characters; never a credential |
| `ZF_ASSIST_EXPIRES` | Empty (disabled) | Explicit timezone-bearing ISO timestamp; database time enforces expiry |
| `ZF_ASSIST_CALL_ALLOWANCE` | 0 (disabled) | Finite aggregate provider-dispatch allowance, 1-1000000 |
| `ZF_ASSIST_TOKEN_ALLOWANCE` | 0 (disabled) | Finite aggregate tokens, at most 1000000000000; must cover one full reservation |
| `ZF_ASSIST_PROACTIVE` | `0` | `1` enables periodic purpose-principal scans after valid authority/limits |
| `ZF_ASSIST_SCAN_INTERVAL` | 60 seconds | 5-3600 |
| `ZF_ASSIST_SCAN_SIZE` | 20 cases | 1-100; keyset cursor visits subsequent open cases |
| `ZF_ASSIST_INPUT_CHARS` | 12000 | 1000-24000 including system and evidence prompts |
| `ZF_ASSIST_OUTPUT_CHARS` | 8000 | 1000-16000; typed summary/findings/unknowns validation |
| `ZF_ASSIST_OUTPUT_TOKENS` | 600 | 100-2000 |
| `ZF_ASSIST_TIMEOUT` | 20 seconds | 1-40; bounded wall-clock dispatch wait; late output is not used |
| `ZF_ASSIST_ACTIVE_CALLS` | 2 | 1-4 local physical call slots and shared unexpired SQL attempt slots |
| `ZF_ASSIST_ATTEMPTS` | 2 | 1-3 per immutable proposal key |
| `ZF_ASSIST_BACKOFF` | 30 seconds | 1-3600, multiplied by the completed attempt count |
| `ZF_ASSIST_LEASE` | 60 seconds | 10-120, at least timeout + 5 seconds |

All replicas must use the same approved effective authority and limits.
SQL serializes reservations under the existing transaction/application-lock
adapter. Every dispatch, including a retry or lease takeover, reserves one
call and `INPUT_CHARS + OUTPUT_TOKENS` tokens before provider access. Input
characters conservatively upper-bound input tokens without adding a tokenizer.
Known valid usage replaces the token reservation with actual tokens. Missing,
out-of-range or timeout usage retains the full bounded reservation liability;
it is never recorded as zero. Uncertain failures retain a shared active-attempt
slot until the database lease deadline; a timed-out physical call retains its
local semaphore slot until it actually returns.

Allowance is keyed by the authority reference hash, shared across replicas and
restarts. The same reference cannot increase the existing allowance or extend
its stored expiry. There is no daily reset or indefinite replenishment.
Exhausted/expired shared allowance disables further automatic scans and is
visible through the registry and queue, not just at provider dispatch.
Another reference means a separately approved finite exercise, not an
automatic rollover. Token allowances are not a currency guarantee; the
operator must derive finite approved limits from deployment pricing and retain
unknown billing liability. Exactly-once inference/billing is not promised:
expired leases can lead to another bounded attempt while remote completion
remains uncertain.

#### SQL durability and lifecycle

Startup adds four idempotent tables (`assistant_tasks`, `assistant_allowance`,
`assistant_attempts`, `assistant_events`), a pending index and append-only
event protection. MSSQL startup DDL and assistant migrations serialize with
the existing transaction-owned `sp_getapplock` write lock. The startup identity
needs the existing schema-creation privileges (for example the already
documented `db_ddladmin`) and permission to use that application lock.
In a ledger-enabled database, `assistant_events` is explicitly created with
`LEDGER = ON (APPEND_ONLY = ON)`. Do not attach the ordinary SQL Server
INSTEAD OF trigger to a system-versioned ledger table: that is unsupported.
An existing updatable-ledger event table fails closed for operator repair;
startup never drops it or deletes its evidence. Non-ledger SQL and SQLite
retain their append-only triggers. Real SQL Server tests cover both database
modes, failed destructive event writes and restart persistence.
Runtime needs SELECT on cases/staff/meta and assistant state, INSERT/UPDATE
on task/allowance/attempt state, and INSERT/SELECT on assistant events. It does
not need new domain write permissions for assistance. Deployment/operator
privilege verification and real MSSQL acceptance are separate from local
dialect emulation. A failed assistant migration leaves assistance visibly
disabled with an operator-migration/manual-route message; it does not prevent
otherwise available ordinary case work or quietly start a provider worker.

Each short transaction uses an independently owned Store-adapter connection.
No provider network call holds the Store/domain/database lock. A durable SHA-256
task key includes capability/version, case, canonical intended proposal identity
(the registered purpose) and material permitted-source/schema/rule/document
signatures. Changed intent or dependencies cannot replay another proposal;
mode is separate append-only provenance. Repeated scans and reactive/proactive
collisions with the same identity recover the same proposal. Claims have an
owner, monotonic fence, database-time lease and CAS completion. Lost
acknowledgements are looked up, not blindly re-dispatched. Review compares the
current material signature and proposal revision in the same serialized SQL
transaction; unrelated contact notes do not stale a proposal.
MSSQL assistant transactions use serializable isolation so current role,
case and permitted metadata reads remain protected through review commit,
including against writers outside the application's cooperative write lock.
The independently owned connection resets to read-committed before closing.

The existing process starts at most `ACTIVE_CALLS` proposal workers and,
when enabled, one scanner. A scanner cannot overlap locally, and SQL capture/
enqueue transactions serialize across replicas. Local physical provider calls
are also bounded by a semaphore; shared unexpired attempt slots bound
replica-wide claims. Shutdown closes provider-thread admission under a short
dispatch gate, so a delayed poll/claim cannot admit inference after stop.
The gate holds neither SQL nor provider work. An existing reservation remains
conservative if shutdown intervenes; an already admitted call may still finish.
The interruptible stop event stops scans/polls and abandons dispatch waits;
outstanding daemon provider calls cannot make late domain or proposal writes.
Expiry/fencing, not thread ownership, governs recovery.
Disable assistance by removing its authority or setting proactive off, and
restore the previous image to roll back. Old images ignore the new tables;
do not delete evidence, reseed data or reset the allowance.

#### API and non-destructive exercise

These calls require a currently authorized signed-in session and, for the
trusted proxy, the existing `X-ZF-CSRF: 1` POST header. They write only
task/proposal/event/allowance state. Invocation can spend approved allowance
when workers are enabled: do not perform live invocation without its scoped
approval. Registry/list/detail are non-billable reads.

```bash
# $BASE is the existing service; use its authenticated session cookie.
curl -b "$COOKIE" "$BASE/api/assistants"
curl -b "$COOKIE" "$BASE/api/assistants/proposals?case_id=ZF-1"
curl -b "$COOKIE" "$BASE/api/assistants/proposals/$PROPOSAL_ID"

# 202 response contains id, state, revision, bounded snapshot and manual route.
curl -b "$COOKIE" -H 'Content-Type: application/json' -H 'X-ZF-CSRF: 1' \
  -d '{"case_id":"ZF-1"}' \
  "$BASE/api/assistants/stock-prioritisation/invoke"

# Repeat the invoke endpoint for any of the other four registered IDs.
# Use the latest revision returned by detail; verification precedes acceptance.
curl -b "$COOKIE" -H 'Content-Type: application/json' -H 'X-ZF-CSRF: 1' \
  -d '{"action":"verify","revision":3,"source_verified":true,"note":"Checked each cited source and retained unknowns."}' \
  "$BASE/api/assistants/proposals/$PROPOSAL_ID/review"
curl -b "$COOKIE" -H 'Content-Type: application/json' -H 'X-ZF-CSRF: 1' \
  -d '{"action":"accept","revision":4,"note":"Accept this proposal only, not a domain decision."}' \
  "$BASE/api/assistants/proposals/$PROPOSAL_ID/review"
```

List pages are bounded to 50 proposals and return `next_after`; pass it as
`?after=<cursor>` for the next page. Detail returns 50 latest history events;
`history_next_offset` supplies the next `?history_offset=<offset>` page.
Current roles/scopes are rechecked for each page, including earlier history.
The queue and case-card history controls expose these continuation reads.

`edit-accept` additionally supplies `output` with exactly `summary`, `findings`
(each has `text` and a non-empty `citations` list of captured `source:*` IDs)
and `unknowns`. `reject` supplies the current `revision` and a bounded `note`.
Stale revision returns 409; denied current role/scope returns 403; invalid
verification/output/state returns 400. Invocation, list/detail and review have
separate service authorization. Scanning has no staff-callable API: the
registered purpose principal is `service:retrofit-evidence-proposals`, not
a manager impersonation. The scheduler calls `Assistants.scan()` only with
valid authority/limits and proactive opt-in.

Validation: `tests/test_assistants.py` exercises all five reactive/proactive
contracts, reader matrices, failure/disabled/malformed paths, current roles,
source review, unchanged controlled state, independent SQLite connections,
claims/leases/restart/lost acknowledgements, retries/aggregate liability,
shared limits, blocked-provider/manual access and shutdown admission. Conditional
`MssqlContractTests`, `MssqlReviewTests`, `MssqlDurabilityTests`, `MssqlApiTests`
and `MssqlLedgerTests`
run the same contracts on actual SQL Server. They require `ZF_TEST_MSSQL=1`,
the existing password/driver settings and a disposable local service
(`localhost`, `127.0.0.1` or Docker alias `sql`). They create/reset only
`zf_test_assistants`, `zf_test_assistants_ledger` and
`zf_test_assistants_ledger_invalid`; never point these tests at the pilot or
Azure SQL. The ledger fixtures replace only their fixed local test databases.
CI runs these alongside the existing general store parity suite. SQL-shape
emulation alone is still not actual SQL proof. The isolated non-billable browser
exercise uses fixtures, not the retained dataset:

```bash
cd mvp
PYTHONPATH=. python3 -m unittest discover -s tests -p test_assistants.py
PYTHONPATH=. python3 tests/assistants_browser_check.py
node --check web/assistants.js

# Disposable local SQL only; set the existing ZF_SQL_* test settings first.
ZF_TEST_MSSQL=1 PYTHONPATH=.:tests python3 -m unittest \
  test_assistants.MssqlContractTests test_assistants.MssqlReviewTests \
  test_assistants.MssqlDurabilityTests test_assistants.MssqlApiTests \
  test_assistants.MssqlLedgerTests
```

The browser exercise needs the existing Playwright test dependency and Chromium;
it can use installed Google Chrome or `CHECK_BROWSER_EXECUTABLE`. The parent
owns image build, real platform evidence, approved rollout and independent
Review. The historical reset cancellation was explicitly cleared on 2026-10-14.
Real operator provider/SQL/restart execution is now recorded below; local mocks
still do not substitute for real staff/human acceptance.

Corrected-source execution on 2026-10-13: 47 nonbillable assistant tests passed;
full discovery reported 379 tests, 310 passed and 69 conditional SQL skips.
The actual disposable SQL run passed all 69 tests: 26 existing store tests and
43 assistant contract/review/durability/API tests, including concurrent first
assistant-table creation on retained case/audit state. The isolated desktop Chromium
exercise passed 19 checks, including pending-assistance manual writes,
deadline fallback and late-result navigation, with no page errors. Both changed
JavaScript files passed syntax checks. Provider responses and human-verification
actions in these suites are test fixtures, not real model or human acceptance.
No retained dataset, private configuration, live provider or Azure deployment
was changed. Actual SQL Server proof does not establish deployed Azure SQL
identity/permissions, real provider quality or CON-009/AC-057 delivery.

Later generated-data validation on 2026-10-13 exposed a populated Visits
rendering defect: arrays of day groups were dropped although the API returned
38 bookings. The shared renderer now flattens node arrays before filtering.
The two-day/case-link regression brings the assistant browser exercise to
21 passing checks. Latest exact-source image05 additionally passes 21
nonbillable generated-data UI/API/local-restart checks with 38 visible visits,
12 Finance rows and 601 source work orders, preserved independent SQLite
domain hashes and five disabled/manual proposals with zero provider attempts.
Tenant bindings and Azure/model acceptance are not exercised by that isolated
validation. Subsequently, on 2026-10-14, the owner explicitly reauthorized
the exact exercise database reset and all offered bounded delivery. Image05
now serves in revision `--0000012`, pinned to manifest
`sha256:e0254cb3a0599c21802f0b6515f975550cf00ddce4849d04fd3fa3d50683af20`.
The restored ledger baseline has 980 cases, 11 tenant staff, 38 visits and
the generated queues. Process-local operator authority permitted five actual
registered Azure OpenAI calls: all five proposals are distinct/citation-validated
ready, with 6884 total tokens and 15 immutable ledger events. Independent
SQL domain and assistant-table content hashes survive actual revision restart.
No human verification/acceptance is recorded. Normal serving assistant
authority remains absent/proactive off; this is not standing spend approval,
staff-browser acceptance, semantic calibration or measured value.

```bash
cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests -v
```

The tests also cover the SQL store (including `test_sqlreads.py`), documents, ledger, role matrix, workflows, auth and time capture. They use small fixtures and a generated 60,000-case dataset, and need no
private data. The AI tests use a scripted model or the template path (no network).

Browser check (needs python3 playwright and chromium, and the built dataset):
`cd mvp && PYTHONPATH=. python3 tests/browser_check.py`.
