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
* A hash-chained audit log records every change.
* Download any list for Excel, and check a spreadsheet: columns are matched
  for you, rows to fix are listed and the file is never changed.

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
* Sign-in is a single shared local password for staff accounts. It is not
  Entra ID. Production would use Entra ID, the Azure design in
  [ADR 0001](../docs/adrs/0001-azure-architecture.md) and the controls in the
  data-handling baseline.
* AI needs `AI_ENDPOINT` (and optionally `AI_DEPLOYMENT`,
  `AI_DEPLOYMENT_STRONG`) and a managed identity with the Cognitive Services
  OpenAI User role. Without them the app uses plain templates. Nothing is
  sent; there is no live integration with housing or repairs systems.
* The map loads tiles from tile.openstreetmap.org (the only external request,
  allowed in the CSP). Production would use a licensed tile service.
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
* Retention periods and legal bases remain proposals for the DPO and Legal.

## Tests

```bash
cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests -v
```

Tests use small fixtures and a generated 60,000-case dataset, and need no
private data. The AI priority tests use the template path (no model).
