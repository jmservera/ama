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
  the model is unavailable.
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
* Workflows, API only (no screens yet): return a case to an earlier stage with a
  reason, reopen (manager), offer, accept, decline or withdraw a handoff, and
  safety referral (raise, refer, record repair, release by a different person).
* The map has a "Show the map areas as a list" alternative: a keyboard and
  screen reader list of clusters (zoom in) or homes (open case), with a polite
  live status line. The tile provider comes from `PW_TILE_URL` (https only) and
  the CSP follows it. With `PW_ENV=production` and no `PW_TILE_URL` no tiles
  load and only the list works.
* AI evaluation harness, offline: `PYTHONPATH=. python3 -m properwarm_mvp.ai_eval`
  runs golden scenarios (`evals/ai_priority_golden.json`) with a scripted model
  and checks that ranking and case data never change, the output stays Proposed
  and needs a person's reason to edit or reject.
* Staff time capture (PR-004) is off by default. It records only when
  `PW_TIME_CAPTURE=on` and `DPIA_APPROVED` holds a reference; own entries only;
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
| `PW_TIME_CAPTURE`, `DPIA_APPROVED`, `PW_TIME_DB`, `PW_TIME_MIN_GROUP` | time capture |

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
  Apps authentication. The contractor view exists in the API but the front end
  has no contractor screens.
* AI needs `AI_ENDPOINT` (and optionally `AI_DEPLOYMENT`,
  `AI_DEPLOYMENT_STRONG`) and a managed identity with the Cognitive Services
  OpenAI User role. Without them the app uses plain templates. Nothing is
  sent; there is no live integration with housing or repairs systems.
* In development the map loads tiles from tile.openstreetmap.org unless
  `PW_TILE_URL` is set. No licensed provider has been chosen or tested.
* Uploaded files and live changes sit on local disk. On Azure Container Apps
  that disk is lost on restart, so run one replica and treat it as a demo;
  production would use Blob Storage and Azure SQL.
* Scale is checked only in memory. A test builds 60,000 synthetic cases and a
  filtered page returns in tens of milliseconds on a development machine
  (about 0.6 s for the first, cold ranking build). That is not a production
  latency: the store is still one JSON file and one process, ranking is rebuilt
  after any change, non-default sorts and the CSV export scan every case, and
  paging uses an offset, not the keyset paging planned in
  [ADR 0002](../docs/adrs/0002-pilot-readiness-architecture.md).
* Ranking snapshots are not yet stored per run and the policy is a Python
  constant, not a signed-off policy file. AI value against the deterministic
  order is only captured as the overlap on each recommendation record.
* The SQL store is verified only on sqlite. Reads are still served from an
  in-memory copy and list paging is still offset based, so ADR 0002 keyset
  paging in SQL is not done. Documents stay on local disk, not Blob.
* The workflow endpoints and time capture have no screens. Time capture is
  enabled by environment, not an audited admin action, and lacks the staff
  notice and consultation checks in the ADR. The AI evaluation uses a scripted
  model, so it checks behaviour, not model quality.
* The Dockerfile pins a base digest and runs as uid 10001 with no data baked in.
  It was built and started locally with Docker; it has not been deployed. The
  `mvp-ci.yml` workflow has not run on GitHub.
* Retention periods and legal bases remain proposals for the DPO and Legal.

## Tests

```bash
cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests -v
```

The tests also cover the SQL store, ledger, role matrix, workflows, auth and time capture. They use small fixtures and a generated 60,000-case dataset, and need no
private data. The AI priority tests use the template path (no model).
