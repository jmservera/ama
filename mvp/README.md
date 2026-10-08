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
* Overview: counts, a map of open cases (teal normal, amber waiting 60+ days,
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
* Uploaded files and live changes sit on local disk. On Azure Container Apps
  that disk is lost on restart, so run one replica and treat it as a demo;
  production would use Blob Storage and Azure SQL.
* Retention periods and legal bases remain proposals for the DPO and Legal.

## Tests

```bash
cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests -v
```

Tests use a small fixture and need no private data.
