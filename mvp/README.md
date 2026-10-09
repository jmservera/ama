# Proper Warm MVP

A working case-management application for the Proper Warm retrofit programme.
It follows the simplicity requirements SA-001 to SA-010 in the
[PRD](../docs/prds/proper-warm-retrofit-programme-demonstrator.md) and the
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
  (`properwarm_mvp/ranking.py`): open safety issue, then priority support or an
  adjustment, then longest time in stage, then earlier stage, then case id as
  the fixed tie-break. Each card shows its rank and plain reasons, the list
  header shows the policy version, and `GET /api/ranking/policy` returns the
  versioned rules. The policy owner is "to be named" and the rule order is an
  unsigned draft.
* "Suggest my top 5" on My cases asks AI for a second opinion beside the
  rule-based order, labelled "AI-drafted, human-approved", with a cited reason
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
  AI-drafted label. Output stays "Not reviewed" until a person accepts, edits or
  rejects it. Workflow-only mode (request flag `mode: "workflow"`, the "Workflow
  only" tick box, or `PW_AI=off`) skips the model for every task and is
  recorded. Each task leaves a comparison record (case ids, AI output,
  workflow-only output, fallback reason, reviewer action and override) in the
  recommendation store, in both the JSON and the sqlite store.
* Documents: upload pdf, png, jpg, docx, xlsx, csv or txt (5 MB), see an
  evidence checklist (EPC, survey, design, consent) and download files.
* Funding: a person moves each application through draft, approved,
  submitted and confirmed. Approval needs complete evidence and the Grants
  and Evidence Officer or a manager. The system never submits anything.
* A hash-chained audit log records every change. `GET /api/audit-check`
  (manager) and `python -m properwarm_mvp.ledger` verify the chain; a digest of
  the head can be written to `PW_DIGEST_DIR` (`POST /api/ledger/digest`) and is
  re-checked on verify. The digest is a local file, not yet an immutable Blob.
* Role-based field projection is enforced on the server (`projection.py`).
  Contractors see only their own cases with "needs notice" and a named contact
  (the case owner), never the vulnerability reason, resident name or contact
  details. Staff see the reason only for the roles in `PW_REASON_ROLES`
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
* Documents sit behind a `DocumentStore` interface (`documents.py`). The local
  filesystem store is the default (`PW_DOC_STORE=local`, `PW_DOC_DIR`). The Azure
  Blob store (`PW_DOC_STORE=blob`) uses urllib against the Blob REST API with a
  SAS token (`PW_BLOB_SAS`) or a managed identity token (`PW_BLOB_CLIENT_ID`
  optional); config is `PW_BLOB_ACCOUNT_URL` and `PW_BLOB_CONTAINER`. Uploads
  allow an extension list and 5 MB, need a staff role (contractors cannot
  upload or download) and write audit entries for upload, download and failure.
* The map has a "Show the map areas as a list" alternative: a keyboard and
  screen reader list of clusters (zoom in) or homes (open case), with a polite
  live status line. The tile provider comes from `PW_TILE_URL` (https only) and
  the CSP follows it. With `PW_ENV=production` and no `PW_TILE_URL` no tiles
  load and only the list works.
* AI evaluation harness, offline: `PYTHONPATH=. python3 -m properwarm_mvp.ai_eval`
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
* Staff time capture (PR-004) is off by default. It records only when
  `PW_TIME_CAPTURE=on`, `DPIA_APPROVED` and `PW_TIME_CONSULTATION` each hold a
  reference, and the person has acknowledged the staff notice
  (`POST /api/time/acknowledge`, audited); own entries only;
  reports are manager-only, aggregated and suppress groups under
  `PW_TIME_MIN_GROUP` (default 5). It uses its own database, never the case store.
* Download any list for Excel, and check a spreadsheet: columns are matched
  for you, rows to fix are listed and the file is never changed.

## Configuration

| Variable | Purpose |
| --- | --- |
| `PW_STORE` | `json` (default) or `sqlite` (durable SQL store, see below) |
| `PW_SQLITE`, `PW_STATE`, `PW_DATA`, `PW_DIGEST_DIR` | database file, state folder, seed data, ledger digests |
| `PW_AUTH` | `password` (dev, default) or `trusted-proxy` (Entra) |
| `PW_ENV` | `production` refuses the password provider and the OSM tile default |
| `PW_SESSION_KEY` | signs dev session cookies; set the same value on every replica |
| `PW_ENTRA_TENANT_ID`, `PW_TRUSTED_PROXY`, `PW_ROLE_MAP`, `PW_AUTH_EMAIL_FALLBACK` | Entra provider |
| `PW_REASON_ROLES` | roles that may see a vulnerability reason |
| `PW_TILE_URL`, `PW_TILE_ATTRIBUTION` | map tile provider |
| `PW_TIME_CAPTURE`, `DPIA_APPROVED`, `PW_TIME_CONSULTATION`, `PW_TIME_DB`, `PW_TIME_MIN_GROUP` | time capture |
| `PW_DOC_STORE`, `PW_DOC_DIR`, `PW_BLOB_ACCOUNT_URL`, `PW_BLOB_CONTAINER`, `PW_BLOB_SAS`, `PW_BLOB_CLIENT_ID` | document store |

### SQL store

`PW_STORE=sqlite` uses `sqlstore.py` on stdlib sqlite3 as the dev and test
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

Azure SQL mapping (designed, not run): `rowversion` becomes a `ROWVERSION`
column or an explicit `BIGINT` incremented in the same `UPDATE`; the append-only
triggers become `INSTEAD OF` triggers or a role with `INSERT` only on the ledger
schema, with SQL ledger tables an option; JSON text columns become `NVARCHAR(MAX)`
with `ISJSON`; `BEGIN IMMEDIATE` becomes a transaction at `SERIALIZABLE` or an
`UPDLOCK` on the head row; digests go to immutable Blob storage; the per-year
ledger table question in ADR 0002 stays open.

### Entra ID on Container Apps

Code: `auth.py`. Nothing below has been done or run in Azure.

* Create an app registration (single tenant) and define app roles whose values
  match the map (default `ProperWarm.Coordinator`, `.LiaisonOfficer`,
  `.ProgrammeManager`, `.Contractor` and so on, see `DEFAULT_ROLE_MAP`) or
  supply `PW_ROLE_MAP` JSON. Assign users and groups to them.
* Enable built-in authentication on the Container App with "require
  authentication" so unauthenticated requests are blocked, and make the ingress
  the only route to the container so `X-MS-CLIENT-PRINCIPAL` cannot be forged.
* Set `PW_AUTH=trusted-proxy`, `PW_TRUSTED_PROXY=1`, `PW_ENTRA_TENANT_ID` and
  `PW_ENV=production`. A token must be `aad`, from that tenant, with exactly
  one mapped role; the role comes from the token, never the staff file.
* Provision each staff record with the Entra object id (`oid`). Email matching
  is off unless `PW_AUTH_EMAIL_FALLBACK=1`. Contractor guests need the same.
* Sign-out redirects to `/.auth/logout`. State-changing requests need an
  `X-PW-CSRF` header under this provider.

## Run it locally

The working data is built from the private stock-geography register. It holds
real OpenStreetMap addresses with invented residents, contractors and staff, so
it is git-ignored, binds to loopback only and must never be committed, deployed
or shared. The repository must stay private.

```bash
python3 support/synthetic-data/retrofit-flow/proper-warm-year-one/generator/build_mvp_dataset.py --seed 20260901
cd mvp
PW_PASSWORD=choose-a-password python3 -m properwarm_mvp.server
```

Open `http://127.0.0.1:8088` and sign in with a staff email from the data (for
example `aisha.rahman@propernorthhomes.example`). Without `PW_PASSWORD` a random
password is printed at start-up. The data builder shifts all dates so the
history ends today and prints no real personal data.

## Honest limits

* The data is constructed. The generator (`pw_names.py`, `build_mvp_dataset.py`)
  makes names, phone numbers on Ofcom drama ranges and example email domains.
  The product screens do not say so; this README and the repository do.
* Dev sign-in is a single shared password. The Entra provider is tested only
  with hand-built principal headers, never against a real tenant or Container
  Apps authentication. The contractor screens are tested through the server and
  not with a contractor account in a browser (the sample data has no contractor
  users). Contractor status text can still say work is stopped for a safety
  issue, and free-text notes are not redacted.
* AI needs `AI_ENDPOINT` (and optionally `AI_DEPLOYMENT`,
  `AI_DEPLOYMENT_STRONG`) and a managed identity with the Cognitive Services
  OpenAI User role. Without them the app uses plain templates. Nothing is
  sent; there is no live integration with housing or repairs systems.
* In development the map loads tiles from tile.openstreetmap.org unless
  `PW_TILE_URL` is set. No licensed provider has been chosen or tested.
* Live changes sit on local disk and uploads default to local disk. The Blob
  store has run only against a fake transport in unit tests, never real
  storage, and its managed identity path has not run in Azure. Upload checks
  are an extension list and a size cap: no content sniffing, no malware scan.
  On Azure Container Apps local disk is lost on restart, so run one replica
  and treat it as a demo.
* Scale: the in-memory store handles 60,000 synthetic cases for filtered pages
  in tens of milliseconds (about 0.6 s for the first, cold ranking build). The
  sqlite store answers list pages, search, sorts and counts in SQL at 60,000
  cases in roughly 50 to 150 ms on a development machine. These are dev
  machine figures, not production latency, and not Azure SQL.
* Ranking snapshots are not yet stored per run and the policy is a Python
  constant, not a signed-off policy file. AI value against the deterministic
  order is measured only on constructed scenarios, plus overlap on each live recommendation record.
* The SQL store is verified only on sqlite. Lists, search, sorts and counts
  use SQL, but case detail, map, statistics, visits, facets, the CSV export,
  the closed list and every write still use the in-memory copy that is kept
  in step with the database. Keyset paging covers the default sort only.
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
* The Dockerfile pins a base digest and runs as uid 10001 with no data baked in.
  It was built and started locally with Docker; it has not been deployed. The
  `mvp-ci.yml` workflow has not run on GitHub.
* Retention periods and legal bases remain proposals for the DPO and Legal.

## Tests

```bash
cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests -v
```

The tests also cover the SQL store (including `test_sqlreads.py`), documents, ledger, role matrix, workflows, auth and time capture. They use small fixtures and a generated 60,000-case dataset, and need no
private data. The AI tests use a scripted model or the template path (no network).

Browser check (needs python3 playwright and chromium, and the built dataset):
`cd mvp && PYTHONPATH=. python3 tests/browser_check.py`.
