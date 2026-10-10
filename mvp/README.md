# Proper Warm MVP

A working case-management application for the Proper Warm retrofit programme.
It follows the simplicity requirements SA-001 to SA-010 in the
[PRD](../docs/prds/proper-warm-retrofit-programme-demonstrator.md) and the
[prototype learnings review](../docs/reference/research/ux/prototype-learnings-and-simplicity-review.md).

## Accepted fictional exercise workbench

The AMA exercise is the whole learning programme; this MVP is its continuing
Proper Warm customer solution, not an isolated test. The owner has directed
restarting the iteration with the existing 60,000-home generated stock and
retained 980 programme cases. `mvp/data/properwarm.json` is the existing
2026-10-08 snapshot, not a newly generated replacement. The stock register
and generator live in the owner's private `support/synthetic-data/` area;
real map addresses have invented residents and must not be committed.
New prototypes, PoCs and MVPs must demonstrate enabled real AI on that
generated data, with source provenance and human review. The configuration
and 18-case launch below are regression fixtures, not the deployment baseline.

### Current continuing MVP

The deployed MVP now uses `properwarm-programme`, a copy of the retained
980-case `retrofit` database with its original case fields, history and audit
head. Exactly 60,000 original generated stock rows are imported separately.
The generated data is disposable and can be reloaded, not an operational
backup requirement. The stock and programme populations are distinct:
443 cases are open and 537 closed in the existing snapshot; neither generated
closure nor map proximity establishes verified handover or property linkage.

Open [the stock map](https://ca-properwarm-mvp.livelybay-cc3a435c.uksouth.azurecontainerapps.io/#/stock)
or [the programme workbench](https://ca-properwarm-mvp.livelybay-cc3a435c.uksouth.azurecontainerapps.io/#/exercise).
Sign in with the existing generated staff identities and configured shared
demo password, not the `ex-*` regression accounts. The current image is
`crpropermvp7569.azurecr.io/properwarm@sha256:0b6b04395c905c6dd6a51520ba8b91d702b4b9b1c6499a4276ed435956307299`,
revision `ca-properwarm-mvp--0000018`.

Real Microsoft Decision 1 selected a generated case's source-bound EPC
candidate, retaining probabilities, input version, source IDs, token usage
and `Not reviewed`. Real GPT-4.1-mini produced a citation-verified case
summary. Neither action approved a field, works, funding or resident choice.
The scoring endpoint is
`https://aif-warm-dev-yu44m.services.ai.azure.com/providers/microsoft/v1/systemone`;
the generic `cognitiveservices.azure.com` host returned authentication
failure for this provider. The optional provider `confidence` field is
validated, not substituted for selection probability thresholds.

`#/stock` shows SQL pages of 50 homes, local-authority/EPC/search filters and
OpenStreetMap/Leaflet grouped markers reconciled to the same filter. Original
OSM anchors/attribution are retained; no simulated tenure or occupant is
asserted as a fact about the real building. Programme case links remain
explicitly unverified instead of being inferred from proximity.

The owner removed the prior budget constraint for this rebuild.
`PW_INFERENCE_ENFORCE_CAP=false` disables only the spend-cap gate;
task authorization, source bounds, per-call liability reservations and actual
model usage remain. The earlier USD450 configuration below is historical.

### Reproduce the generated-data import

With operator Entra access to a dedicated SQL database, mount the existing
private generated data read-only and run:

```bash
PW_SQL_SERVER=<server>.database.windows.net PW_SQL_DATABASE=properwarm-programme \
PW_SQL_AUTH=default PW_DOC_STORE=local \
python3 -m properwarm_mvp.programme --state /state \
  --data /data/properwarm.json --stock /data/private-north-east-stock-register.csv
```

For this deployment, the original database was copied using
`az sql db copy -g ama -s sql-warm-dev-spw6p -n retrofit --dest-name properwarm-programme --service-objective GP_S_Gen5_2`.
Retained documents use the existing non-public `evidence` Blob container.
Set `PW_PROGRAMME=1`, `PW_EXERCISE=1` (bounded controls), `PW_AI=on`,
`PW_STORE=mssql`, `PW_SQL_DATABASE=properwarm-programme`,
`PW_DOC_STORE=azure-blob`, `PW_BLOB_CONTAINER=evidence`, and the Foundry
task/access settings. Startup requires reviewed `PW_PROGRAMME_SHA256` and
`PW_STOCK_SHA256` matching imported metadata. An incompatible database is
not silently reseeded. A deliberately regenerated dataset requires a new
reviewed import, not an artificial claim of identical source bytes.

### Historical regression fixture

The accepted PRD v0.12.0 exercise has a separate local startup and connected
workbench at `#/exercise`. It does not use the private-geography seed or claim
operational acceptance. Create a fresh state directory under this repository,
then run from `mvp/`:

```bash
mkdir -p .exercise-state
PW_EXERCISE=1 PW_STATE="$PWD/.exercise-state" PW_STORE=sqlite \
PW_DOC_STORE=local PW_AI=off python3 -m properwarm_mvp.server
```

Do not set `PW_DATA`, an external document backend or inherited store overrides.
The factory refuses incompatible seeds/databases without overwriting them.
Use the server's development sign-in password with the fictional staff emails
`ex-geo-01@example.test`, `ex-pm-01@example.test`,
`ex-pm-02@example.test`, `ex-pso-01@example.test`,
`ex-rc-01@example.test`, `ex-rc-02@example.test`,
`ex-rlo-01@example.test`, `ex-qi-02@example.test`,
`ex-bsl-01@example.test` and `ex-con-01@example.test`.
These are distinct exercise identities, not real delegated officers.
Perspective navigation never changes the signed-in role.

### Deployed Azure exercise

On 2026-10-10 the owner authorized replacing the previous deployed MVP.
The connected exercise is available at
[Proper Warm](https://ca-properwarm-mvp.livelybay-cc3a435c.uksouth.azurecontainerapps.io/#/exercise).
Use the existing configured demo password and the fictional staff identities
above; no password is published in the repository. This remains shared demo
authentication, not production Entra user authentication.

The replacement uses the existing UK South Container App, SQL server and
storage account. `properwarm-exercise` is a separate Basic (5 DTU, 2 GB) Azure
SQL ledger database with seven-day backup retention.
`exercise-evidence` is a non-public Blob container. The old `retrofit`
databases were not migrated or overwritten. All browser JavaScript, CSS,
Leaflet assets and runtime/evaluation files are packaged in the complete
container image; fixture source bytes/forms are retained in SQL, and uploaded
document bytes use Blob rather than ephemeral app disk.

The deployed image is pinned to
`crpropermvp7569.azurecr.io/properwarm@sha256:115d35582cad11492b40e06192a5c97f523725f0fe74ab2c99f5a8b77c05405a`.
This digest records the historical AI-disabled replacement, not the current
delivery target. The latest corrected AI-enabled revision is
`ca-properwarm-mvp--0000013`, image SHA-256
`756793ff0fa073de3bac34ebbb9c85046edcaf870a60b95b2aafe7bf1b54e61a`.
GPT-4.1-mini has produced a source-verified summary; message generation
succeeded but its citation verification did not pass. Decision 1 is deployed
but live calls still return authentication failure despite the scoped role
assignment. No Decision 1 success or full MVP completion is claimed.
Only one replica is permitted. The app uses
the existing user-assigned identity for SQL/Blob, with `db_datareader` and
`db_datawriter` runtime grants. Bootstrap temporarily required `db_ddladmin`;
it was removed after initialization, and the next image revision started
successfully without it. Future schema migrations require an operator to
grant/revoke the necessary DDL permission, not silent permission escalation.

[Exercise infrastructure](../infra/exercise.bicep) reproduces the separate
database/container without changing the old databases:

```bash
az deployment group create -g ama -n properwarm-exercise-data \
  --template-file infra/exercise.bicep
```

Historical regression-only configuration (do not use as the new MVP baseline):
`PW_EXERCISE=1`, `PW_DATA=` (cleared),
`PW_STORE=mssql`, `PW_SQL_SERVER=sql-warm-dev-spw6p.database.windows.net`,
`PW_SQL_DATABASE=properwarm-exercise`, `PW_SQL_AUTH=msi`,
`PW_SQL_CLIENT_ID` set to the existing API identity's client ID,
`PW_STATE=/state`, `PW_AS_OF=2026-10-10`, `PW_DOC_STORE=azure-blob`,
`PW_BLOB_ACCOUNT_URL=https://stwarmdevspw6p.blob.core.windows.net`,
`PW_BLOB_CONTAINER=exercise-evidence`, `PW_BLOB_CLIENT_ID` set to that same
identity. Real AI now uses `PW_AI=on` and the configured Foundry endpoint,
approved-task/access flags and SQL-backed liability reservations.
Do not disable AI to present this fixture as a completed new MVP.
Preserve existing password
and session-key secret references. `/tmp` seed paths are intentionally refused.
Use `az acr login`, build/push the whole `mvp/` Docker context, and update the
Container App to the resulting immutable image digest.

Live checks verified HTTPS sign-in, all eleven web-file hashes, actual browser
form creation/parsing with unresolved D/E conflict, building navigation,
390px reflow, managed-identity document upload/download and exact SQL
case/audit-head plus Blob-byte retention across a revision restart.
This is deployment evidence, not Azure load testing, scheduled recovery
reconciliation, human UX, production security or actual-model acceptance.
Existing development network access settings were reused, not tightened into
a production network boundary. Basic SQL and one bounded app replica reduce
incremental spend; total subscription costs still require operator review
against the USD 450 monthly cap.

* Two story homes are separate from sixteen forecast homes. Story approvals,
  resident choice, awards and cash start absent. Analytical readiness is not
  permission to release works. Small stakeholder cells and complementary totals
  are suppressed; the forecast tables describe constructed scenarios, not outcomes.
* `GET /api/exercise` supplies profiles, workflows, source-versioned forecast
  tables and explicit unresolved gates. `GET /api/cases/{id}/exercise` supplies
  role/template-authorized drafts and evidence. `POST` on the latter applies
  one named `action`; the workbench contains the manual journey instructions.
* Form actions are `create-form`, `extract`, `select`, `review`, `human-field`,
  `calculate`, `attachments`, `review-pack` and `export`. Source metadata,
  route and raw bytes come from the owning case, not candidate JSON sent by
  the browser. Ordinary field review cannot create a declaration, certification,
  resident decision or approval. Pack reviewer differs from every current field
  reviewer. Reviewed JSON downloads reproduce stored snapshots and never submit.
  The same-home screen also downloads its role-projected case/event/decision
  and source-version history independently of AI; this is not a cohort export.
* `source-correct` requires `source_id`, replacement `raw_text` and a reason,
  preserves prior bytes/versions, invalidates exact dependent reviews and leaves
  the sibling untouched. Matching corrected EPC sources resolve the source-of-record
  EPC; a field correction alone does not. Stale external award references suspend
  funding readiness.
* `funding-event` records separate `application-submitted`,
  `application-disposition`, `award`, `claimable`, `claim-submitted`,
  `claim-disposition` and `cash` evidence. Supply `form_id`, exact current
  `export_id`, `evidence`, explicit `amount` when required and
  `disposition: "Accepted"` or `"Rejected"` for dispositions.
  The predecessor is recorded; disposition is independent from submission.
  Cumulative cash cannot exceed accepted claim. No external action occurs.
* `lifecycle` accepts only the next `target`: Intake, Assessment, Funding,
  Ready, Installation, Provider completed, Independent QA, Handover,
  Financial closure. Reuse existing design/sign-off, resident, capacity,
  quality, invoice and handoff panels. Four sign-offs have distinct identities
  different from the designer. Resident choice binds exact measure/scope and
  design version; unknown or scheduling-only representatives cannot decide works.
* Work release checks readiness plus committed capacity. Provider completion
  cannot satisfy acceptance. Quality returns, fixes, independent reinspection
  and resident handover remain separate. `milestone` records independently
  verified mobilisation/installation/handover evidence against a same-home
  work order. Invoice lines must match exact `WO-id:milestone` references and
  GBP 3,600/12,600/1,800 amounts, not fabricated reference strings. Closure
  requires GBP 18,000 provider reconciliation, external invoice-payment
  records and accepted claim/cash reconciliation.
* `external-hazard-reference` records supplied fictional `authority`, `version`,
  `reference`, `evidence`, boolean `released`, and optionally `hazard_index`
  after referral. It preserves prior references and never evaluates their
  sufficiency. Legacy local hazard release, whole-case choice, instant handover,
  funding/claim shortcuts and instant installation advance are denied by API.
* `handoff` records explicit `step` values `sent`, `received`, `accepted`,
  `returned`, `escalated` and `completed`, with separate actor/evidence/reason.
  Sending requires named receiver, due date or `Unknown`, urgency and owned
  next action. Receipt never transfers ownership; acceptance requires separately
  recorded receipt. Sender/current owner retains chase until acceptance.
  Legacy handoff shortcuts are refused in exercise mode.
* `resident-update` creates an independently owned commitment with purpose,
  due/basis, safe channel/adjustment reference or explicit unknown and next update.
  `proposed`, `sent` and explicit `reassign` use an existing `update_id` and
  evidence/reason. Handoffs never clear or reassign it. A supplied send reference
  does not imply resident receipt/understanding and performs no actual contact.
* `return` records an earlier lifecycle `target`, named `receiver`, source
  `evidence`, reason and owned `next_action`. It preserves history and existing
  evidence; actual evidence changes still require their domain/source action
  and dependent review. It is not a forward transition or approval shortcut.
  Optional `affected_milestones` is a list of exact existing same-home
  `WO-id:milestone` references. These become stale with return source/history;
  current invoice matching, payment-status continuation and financial closure
  refuse stale references. Renew using the existing independent `milestone`
  action and its stage/evidence checks. Historical invoice dispositions,
  external payment references and cash are not erased or executed again.
* Each story home links to a read-only building page and back to its sibling.
  Building context keeps shared systems/dependencies/holds/cost explicitly
  unknown where no shared evidence exists. Each home retains its own
  role-projected choice, evidence, cost and gates; package identity grants no
  applicability and contractor links show only assigned homes.
* `hazard-followup` records separately supplied external receipt/acceptance/
  chase evidence against a referred `hazard_index`, authority, external actor
  or unknown, observed timestamp, reference and owned follow-up. It never
  releases a hold, changes awareness/classification or closes the external clock.
* Optional `assist`, `support` and `narrative` actions retain source/version/hash bindings,
  proposal/reviewer status and transport provenance. Inherited `AI_ENDPOINT`
  never activates exercise calls. Disabled/failure/manual states are explicit;
  `PW_AI=off` always keeps narrative manual. No billable calls were executed.
  Decision scoring uses separate explicit `PW_DECISION_ENDPOINT`,
  `PW_DECISION_DEPLOYMENT` and independently reviewed
  `PW_DECISION_METADATA_{ENDPOINT,DEPLOYMENT,MODEL,MODEL_VERSION}`,
  `PW_DECISION_METADATA_REVIEWED=true`, `PW_DECISION_DEPLOYMENT_TYPE`
  and `PW_DECISION_REGION`. These do not authorize inference: all shared
  `PW_INFERENCE_*` access/terms/cost/quota/price/spend/task gates still apply.
  Exercise scoring and generation reserve conservative upper charges atomically
  in `PW_STATE/inference-liabilities.sqlite`. Existing accrued spend cannot be
  lowered by another process, retained reservations never auto-refund/roll over,
  and projected spend at USD 405 blocks transport (USD 360 requires review).
  Missing/unwritable ledger fails closed. This is tested liability reservation,
  not actual pricing, invoice reconciliation or billable authorization.
  Selection/support context includes only authorized sources with current
  candidates for the requested field, and only its labelled excerpt, with full
  document hash/source binding retained. Support requires an explicit `claim`;
  it is never evidence verification or an approval.
* `versions` permits a template owner to record an explicit `schema_version`
  and/or `rule_version` with a reason. Unknown versions block export; restoring
  the approved version does not restore stale reviews. Financial dispositions
  bind their preceding form/export/digest. A corrected rejected submission
  requires its exact rejected `retry_of` reference and a fresh reviewed export;
  unchanged re-exports/reviews do not count as correction. Upstream staleness
  propagates through the exact financial predecessor chain. A fresh current
  award may restore readiness without activating old stale awards. Cash remains
  cumulative across claims on the one fictional opportunity, even when a claim
  becomes stale, and duplicate external receipt references are refused.

### Narrow exercise data portability contract

`GET /api/exercise/data?population=all` downloads independent JSON case, event,
decision, evidence-reference, source/version and review/supersession histories.
Population may also be `story`, `forecast` or `scale`; an unknown value is
rejected. Metadata identifies the version, as-of time, role-projected scope,
population and count. Contractors receive only their server-owned assigned scope,
with the existing contractor detail projection: no finance, resident reasons,
raw evidence, coordination notes, decisions or approvals. Exports are read-only,
not a new source of authority, and work with AI disabled.

`POST /api/exercise/data` accepts three explicit actions:

* `import-preview`: `filename` ending `.xlsx`, `workbook_base64`, a `reason`
  of at most 300 characters, and an explicit `fields` selection from
  `coordination_note` and `task_due_date`. The frozen sheet is `Case updates`.
  Physical row 1 must contain unique `case_id`, `coordination_note` and
  `task_due_date` headers; displayed mappings use actual worksheet cell
  columns. Inline/shared text strings are supported. Dates must be literal
  `YYYY-MM-DD`, not serial numbers. Notes must be nonempty and at most
  300 characters. Formula, unsupported cell, unknown ID, duplicate/conflicting
  ID and controlled-column rows have explicit errors requiring manual repair
  and a fresh preview. Missing mappings reject the workbook.
* `bulk-preview`: `case_ids` explicitly selects 1-25 case IDs; `changes`
  contains only `coordination_note` and/or `task_due_date`, with a `reason`.
  Every case's exact prior value, change, fingerprint and validation disposition
  is shown. No ownership changes are permitted: the sender retains ownership
  until an individually authorised handoff is accepted.
* `commit`: supply the preview's `token`, `input_hash` and
  `expected_fingerprints` object keyed by physical row number (bulk previews
  use selection row numbers). The server persists the trusted preview inside
  a case and rechecks each full case fingerprint. Commit inputs cannot replace
  fields, roles or authority. Stale and invalid rows do not change; all per-row
  outcomes are returned and audited, alongside successful rows. Retrying the
  same committed token returns its original outcomes without duplicate changes.
  Preview retention is the latest 20 previews per anchor case.

Only server-rostered Programme Managers and Programme Support Officers may
preview/commit. Bulk/import cannot write stock, owner, safety, consent,
declarations, procurement, funding, payments, claims or controlled approvals.
Changes are labelled unverified coordination metadata, with prior value,
actor, timestamp, reason, source SHA-256, physical row/mapping, input hash and
case fingerprint retained in history. The original XLSX bytes are only read
in memory and remain unchanged.

Limits are 5 MiB compressed, 500 data rows, 20 ZIP entries and 20 MiB total
expanded contents. Duplicate ZIP entries, external worksheet relationships,
encrypted archives, DTDs/entities and malformed XML are refused. Arbitrary Excel
structures, formulas, authoritative stock imports, owner bulk reassignment and
XLSX export are not supported. This narrower contract does not assert full
PRD data portability or overall exercise acceptance.

Run the independent data fixtures with
`TMPDIR="$PWD/.test-scratch" PYTHONPATH=. python3 -m unittest discover -s tests -p test_exercise_data.py -v`
from `mvp/` after creating `.test-scratch`.

Validation commands (run from `mvp/`, using a repository-local scratch directory
for legacy tests which use Python temporary-file APIs):

```bash
mkdir -p .test-scratch
TMPDIR="$PWD/.test-scratch" PYTHONPATH=. python3 -m unittest discover -s tests -p test_exercise_workbench.py -v
TMPDIR="$PWD/.test-scratch" PYTHONPATH=. python3 -m unittest discover -s tests -q
node --check web/exercise.js
node --check web/app.js
node --check web/panels.js
```

Thirty connected integration tests exercise same-home SQLite durability, exact
EPC invalidation/sibling isolation, independent form review/export, separate
financial states through closure, QA return/fix/reinspection, scoped resident
choice, capacity/safety blocks, zero-call inherited inference configuration,
projection, startup isolation and HTTP shortcut denial. A focused matrix covers
all eleven profiles against six form-creation permissions and eight protected
batch denials, not every controlled action. Exact two-measure fixtures retain
scope/design/version and representative authority, isolating pause/withdrawal
from unrelated choice and hazard service. Five service types preserve explicit
outcome/owners/contact needs/status/update without treating contact as consent.
Need-based contact-reference projection preserves stored history, including
Unknown values, and applies to API/export/model facts. These are local
engineering evidence, not full PRD acceptance. Live Decision 1/generative
inference, human-adjudicated evaluation and net-effort comparison remain
blocked. The local browser runner records eleven profile orientation probes,
nine workflow navigation entries, actual parser conflict, narrow form reflow,
actual doubled body text, keyboard focus, input labels, visible 24px control
targets and declared palette contrast. A CSS 4x zoom probe is explicitly not
native browser zoom. It is not eleven completed user
tasks or nine completed workflow browser journeys. Local runtime probes use
200 warm HTTP samples per list/detail/write/dashboard operation, one session
and one writer, and an exact clean SQLite restart/backup-copy comparison.
Two 30-minute core/scale runs pass separately, with five/twenty authenticated
sessions, two coordination writers, >=200 samples/op and no errors. Scale
contains 60000 fictional homes/600000 embedded linked traces. List/detail/
dashboard/write p95 are 0.0101/0.0048/0.0063/0.1506s core and
0.0989/0.0419/0.0490/0.0787s scale. Five scheduled interactions/s is not
exactly five HTTP requests/s: writes perform preview and commit. A 500-row
import and 25-case batch pass as a separate Store-level scale probe, not
concurrent core HTTP imports. Later strict mixed core does execute a 500-row
HTTP import and 25-case batch during five-session/two-writer load, with twenty
5000000-byte documents and 150 story-home upload/note events. It passes all
p95 targets with zero errors; core p95 list/detail/dashboard/write are
0.0068/0.0028/0.0051/0.0340s and import preview 0.0568s. Later exact-rate scale
schedules 9000 HTTP requests over thirty minutes, not 9000 interactions:
p95 0.0978/0.0439/0.0486/0.0863s, zero errors. Maximum latencies remain in the
raw evidence. Independent comparisons preserve all controlled field groups,
all scale trace contents, document bytes and both full audit chains.
These do not establish every permission combination, separately timed initial
cold startup or cloud capacity.
Background commit/retry interruption and document-byte restore now have
focused probes. A headed Chrome/Xvfb run proves native 400% browser zoom
separately from CSS emulation. Scheduled RPO/disaster reconciliation and
human/screen-reader acceptance remain unexecuted. The combined headed browser
run passes 53 finite checks, including eleven controlled profile safe blocks,
bidirectional building navigation, distinct sibling consent/design and an
independently owned resident commitment/operational handoff journey.
The latest headed run passes 57 checks, adding actual accessible complaint
intake, service-owner close refusal and independent redress-owner closure;
works withdrawal remains unchanged. Fresh local 18-home initial startup is
separately measured at 0.3231s to first health 200, not cloud/scale cold startup.
Resident panels display exact scope/design version and permitted representative
references. Shared DOM rendering recursively flattens nested child arrays so
all labelled form controls are real nodes rather than text.
Explicit handoff/update/return and hazard receipt/acceptance contracts now have
focused tests, including unchanged commitment ownership across handoffs and
process exits before commit/after commit before response. Their complete
role/browser fixture matrix remains unexecuted. Arbitrary new-source ingestion
and full claim resubmission recovery need further validation.
Return controls can name explicit technical sign-offs and same-home form
fields and milestone references for re-review. Empty scope is routing-only, never guessed consent or
source invalidation. Named fields use exact input-version dependencies;
historical financial receipts remain recorded even when readiness is suspended.
Versioned returns expose source, initiating authority, receiving owner and next
action, with restricted form details hidden from non-Finance views.
All 36 earlier-stage pairs and ten invalid-scope shapes have atomic
fixtures. Exact paid/unpaid milestone return fixtures retain unaffected
milestones, invoice/QA/choice/cash history and refuse stale payment/closure
until independent renewal. Malformed/foreign/duplicate milestone scopes fail
atomically; non-Finance projections omit restricted milestone details.
The latest headed browser passes 61 finite checks, including foreign-milestone
scope refusal. Complete quality/procurement dependency and milestone
version/re-review matrices are still not validated.
The labelled event controls and optional JSON editor are manual
exercise tools, not a validated production form experience.

### Offline exercise restore boundary

The exercise operator owns backup, failure, restore and reconciliation during
weekday 09:00-17:00 UTC coverage; the backup operator covers absence.
This is not a 24/7 safety service. Hazard response remains outside this app.

Stop controlled work before selecting an isolated restore candidate. Preserve
the original database, seed, document directory, digests and inference
liability ledger; never replace them with a blank fixture. Back up SQLite using
its backup API, not a live raw database-file copy that omits WAL changes.
Copy document bytes as well as case metadata and record source hashes,
backup time, audit head and last independently known acknowledged changes.
The current app does not schedule a 15-minute backup service.

Before exposing a restored database to the server, insert the
`exercise_recovery_pending` key in its SQLite `meta` table with a JSON record
of operator, backup/source audit heads, affected cases, missing-event findings
or explicit unknown, and owned next action. The standard exercise factory
refuses startup while that key exists. Inspect candidates offline only;
no agent or UI action clears it. Validate SQLite integrity, exact case/audit
snapshots and document-byte hashes, and enumerate missing post-backup events.
Preserve unresolved inference liabilities independently; restore must not
reset the technology spending baseline or reservations.

Only the named exercise operator may clear the marker after documenting
recovery/reconciliation of missing acknowledged changes and duplicate checks
in retained offline evidence. If event sufficiency, document completeness or
spend remains unknown, keep the candidate offline and use owned manual queues.
The marker is a local launch interlock, not tamper-resistant production
recovery approval. Focused tests detect one deliberately missing acknowledged
event and refuse candidate startup; they do not claim completed disaster
reconciliation or production availability.

Run local engineering probes with installed Python Playwright and Google
Chrome, from `mvp/`. Each state directory must be new; neither script deletes
existing state. Outputs label the precise workload and missing checks.

```bash
PYTHONPATH=. python3 tests/exercise_browser_check.py --state "$PWD/.exercise-browser" --output "$PWD/.exercise-browser/results.json"
PYTHONPATH=. python3 tests/exercise_runtime_check.py --state "$PWD/.exercise-runtime" --output "$PWD/.exercise-runtime/results.json"
```

The container includes the fictional fixtures and task registry. Exercise
startup overrides the legacy dataset default with `-e PW_DATA=` and uses
`-e PW_EXERCISE=1 -e PW_STORE=sqlite -e PW_DOC_STORE=local -e PW_AI=off`.
Mount an explicitly writable `/state`; the image stays non-root/read-only.

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

## Configuration

| Variable | Purpose |
| --- | --- |
| `PW_STORE` | `json` (default), `sqlite` or `mssql` (Azure SQL, see below) |
| `PW_SQL_SERVER`, `PW_SQL_DATABASE`, `PW_SQL_AUTH`, `PW_SQL_CLIENT_ID`, `PW_SQL_PORT`, `PW_SQL_TRUST_CERT`, `PW_SQL_TOKEN`, `PW_SQL_USER`, `PW_SQL_PASSWORD` | Azure SQL connection; `PW_SQL_AUTH` is `msi` (default), `default`, `token` or `password` (CI container only) |
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

### Azure SQL store

`PW_STORE=mssql` uses `mssqlstore.py`, a T-SQL dialect over the same `SqlStore`
logic, with the pinned `mssql-python` driver (`requirements.txt`, hashes
checked in the image build; the image adds `libltdl7` and `libkrb5-3`). Writers are
serialised across replicas by a transaction holding an exclusive application
lock (the equivalent of SQLite's write lock), every compared text column uses a
binary collation so ordering matches the other stores, and a connection dropped
between requests is reopened. Sign-in is Microsoft Entra with the app's managed
identity (`PW_SQL_AUTH=msi`, plus `PW_SQL_CLIENT_ID` for a user-assigned one), so
there is no database password. The audit table is an append-only ledger table
when the database has Azure SQL ledger enabled (the engine refuses update and
delete), otherwise an `INSTEAD OF` trigger does it. Every other table in a ledger
database also keeps row history, which matters for erasure and retention
(DPIA item to resolve before real data).

The first start seeds an empty database from `PW_DATA`; the image carries no data,
so seed once from an operator machine with `PW_SQL_AUTH=token` and
`PW_SQL_TOKEN=$(az account get-access-token --resource https://database.windows.net/ --query accessToken -o tsv)`.
The app identity needs a contained user with `db_datareader`, `db_datawriter` and
`db_ddladmin` (see `infra/scripts/create-sql-users.sql`). `tests/test_mssqlstore.py`
runs the SQL store suites and the list-read parity suite against a real SQL Server
when `PW_TEST_MSSQL=1` (and `PW_SQL_*` point at a throwaway database).

## Honest limits

* The data is constructed. The generator (`pw_names.py`, `build_mvp_dataset.py`)
  makes names, phone numbers on Ofcom drama ranges and example email domains.
  The product screens do not say so; this README and the repository do.
* Azure on 2026-10-09 (dev subscription, constructed data): the app ran on Azure SQL with a
  managed identity, documents in Blob, two replicas, and a restart kept a written record with the
  ledger intact. Sign-in there is still the shared password because Entra built-in
  authentication needs an app registration that was not available. Nothing was load tested in
  Azure and Blob contents were not listed directly (no data-plane role).
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

* The ranking policy is a hash-checked file but not signed off: no named
  owner yet. The hash detects edits, it does not prove who approved them.
  Snapshots are written when a manager requests one and the data has changed,
  as a file, not on every change or in a database table. The as-of date is the
  date the store was first loaded, and day counts come from the stored
  `days_in_stage`, not recomputed from it. AI value against the deterministic
  order is only captured as the overlap on each recommendation record.
* The SQL store is verified only on sqlite. Lists, search, sorts and counts
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
* The Dockerfile pins a base digest and runs as uid 10001 with no data baked in.
  It was built and started locally with Docker; it has not been deployed. The
  `mvp-ci.yml` workflow has not run on GitHub.
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
  --security-opt no-new-privileges`, with only `/tmp` and `/state` (`PW_STATE`)
  mounted as tmpfs, the seed data mounted read-only, and writes to `/state`
  succeed while writes to `/app` and `/` fail;
* a Trivy scan fails the job on any HIGH or CRITICAL finding that has a fix
  available (`ignore-unfixed`). Unfixed findings in the pinned Debian base are
  not blocked, so they are visible in a local `trivy image` run but not
  gated. The fix for a fixable OS package is the `apt-get upgrade` in the
  Dockerfile, never an ignore file;
* an SPDX SBOM (`properwarm-mvp-sbom` artifact) is generated and uploaded.

Actions are pinned by commit SHA. The workflow result on GitHub is what proves
these checks; running the same commands locally is only a preview. Document
files default to `PW_STATE/docs`, or set `PW_DOC_DIR`; the app writes nowhere
else. The SQL Server integration job is not part of this job.

## Tests

```bash
cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests -v
```

The tests also cover the SQL store (including `test_sqlreads.py`), documents, ledger, role matrix, workflows, auth and time capture. They use small fixtures and a generated 60,000-case dataset, and need no
private data. The AI tests use a scripted model or the template path (no network).

Browser check (needs python3 playwright and chromium, and the built dataset):
`cd mvp && PYTHONPATH=. python3 tests/browser_check.py`.
