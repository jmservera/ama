---
title: Retrofit Synthetic Evidence Pack - Zava Forward Year One
description: Fifteen months of synthetic operating records from a professional retrofit delivery team that knows it has bottlenecks but not where they are
ms.date: 2026-10-15
ms.topic: reference
---

> [!WARNING]
> SYNTHETIC DATA. Every record in this folder is fictional and was generated
> for design, analysis and agent-testing practice. Nothing here is a Proper
> North Homes fact, and no person, address, supplier or organisation is real.
> Every table carries `is_synthetic=true`.

## Purpose

The AMA exercise refers to the whole learning programme, not an isolated test
application. The owner requires future prototype/PoC/MVP iterations to reuse
the existing data generator and generated stock, and demonstrate enabled
bounded AI against realistic generated inputs.

This public operating pack is not the full stock register. The private
60,000-home geography register (seed 4820260930, generated 2026-09-30) and
the existing 980-case MVP snapshot (built 2026-10-08) remain separate linked
data assets, with different denominators. The private MVP generator uses real
OpenStreetMap map addresses with invented residents; the warning above
applies to this public pack, not to every geographic anchor in that private
output. Keep private outputs out of Git, preserve versions/identifiers/history,
and report missing stock-to-case linkage explicitly. Small constructed
regression/forecast fixtures do not replace the generated-data MVP.

### MVP Operational Coverage (2026-10-13)

The owner requests a regenerated exercise database and more populated workbench
sections, especially visits. The requested eval-dataset-creator supplied a
read-only schema/coverage audit; the parent implemented and tested the existing
generator. This does not alter the public CSV pack or resolve blind constraint
findings. The initial reset was cancelled on 2026-10-13; explicit reauthorization
on 2026-10-14 permitted recreation and seeding of the exercise Azure SQL
database. The coverage below now exists in the serving exercise baseline,
with all 11 original tenant staff bindings retained privately. This does not
make synthetic records real resident, approval or business-outcome evidence.

```bash
python3 support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py \
  --seed 20260901 --as-of 2026-10-13 --out /private/path/zavaforward.json
```

The explicit as-of date makes regeneration repeatable. The generator preserves
source contacts, hazards and decisions, exports simulation state histories and
uses each appointment's actual source supplier instead of the installation
contractor for every visit. Six designated future assessment appointments are
added only to available open cases without unresolved safety holds or existing
bookings; historical contrasts do not enter the booked-visits queue.

| Generated and seeded exercise coverage | Count | Boundary |
| --- | --- | --- |
| Retained geography stock / programme cases | 60000 / 980 | Separate denominators; 443 open programme cases |
| Distinct geography anchors | 825 | Flats may share a building anchor; not unique stock-unit linkage |
| Cases linked to a stock home ID / unlinked | 980 / 0 | Reported in `stock_link`; 16 stock homes are shared by more than one case |
| Stock fabric attributes (60000 homes) | 5 | Build year, age band, dwelling type, construction, heating; synthetic assumptions, not company facts |
| Appointments / visible booked visits | 1578 / 38 | Source bookings plus clearly labelled fixtures |
| Current-week booked visits | 11 | Receipt counts 2026-10-12 to 2026-10-18; API has no date-range filter |
| Designated forward visits | 6 | Four in that week; no invented works release or consent |
| Packages / source-issued work orders | 1 / 601 | Imported simulation issuance/completion, not live instructions or QA acceptance |
| Invoices / quality records / pending grants | 13 / 12 / 12 | Proposed budgets, unpayable received/held invoices, unverified submissions and pending opportunities |
| Offered handoffs / open service requests | 4 / 12 | No invented acceptance, resolution or redress |

The generator writes a private `.coverage.json` receipt beside its output.
It contains counts, seed, date and version, not addresses or people. New
structures carry `is_synthetic`; the whole dataset is synthetic-labelled.
Operator seeding preserves the 11 existing private tenant staff/oid bindings
instead of generating identities from the generator's ten fictional staff.
Initial SQL loading preserves procurement/as-of; restart never silently
replaces live records. Four focused tests cover determinism, exact visit
cohorts, referential/control boundaries and SQL seed/restart persistence.

### Contractor, finance, grant, safety and consent lifecycle coverage (2026-10-15)

Issue #173, parent #167. Labelled synthetic fixtures under ADR 0005; none is
law, an approval, an acceptance or a payment. The `.coverage.json` receipt now
carries a `lifecycle` block with seeded counts per state and the deferred
list. Two further open cases gain one Raised commitment and one Valuation
(Received), so the receipt shows 1 raised commitment and 13 invoices or valuations.

| Record | Seeded states | Deferred (recorded, not invented) |
| --- | --- | --- |
| Work order | Issued, Completed (source simulation facts) | Appointed, Withdrawn |
| Budget / commitment | Proposed / Raised | Approved (needs a different named approver) |
| Invoice / payment | Received, Exceptions (held); Not payable yet | Matched, accepted, rejected; Awaiting payment run, Paid outside this system |
| Grant | Not recorded, with a pending proposal to Opportunity | Opportunity (proposed only, not confirmed), Award, Claimable, Submitted, Accepted, Rejected, Cash received |
| Quality | Submitted | Accepted, Returned, Fixed, Handed over |
| Safety hold | Open and Released, from source hazards | None |
| Resident decision | Not recorded (default) | Waiting, Accepted, Declined, Paused, Withdrawn |

Open items for the owner: whether a labelled demo-only approved/paid/awarded
or consent-answered record is wanted for UI demonstrations; and the sibling
issues #90, #94, #95, #85 and #86 that may own those states.

### Determinism, manifests and refresh policy (2026-10-15)

Reproducibility (issue #176, parent #165). Historical pack generators are in
`support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/`;
migrated scale and sensor tools are in `src/core/src/zava_forward/core/synthetic/`
under accepted ADR 0006. New executable work belongs in `src/`, not `mvp/`.

| Generator | Reproducibility inputs | Manifest or receipt fields | Byte-identical test |
| --- | --- | --- | --- |
| `build_mvp_dataset.py` (MVP JSON) | `--seed`, `--as-of` (defaults to the clock, so always pass it) and the stock register | `seed`, `as_of`, `generator_version`, `generator_revision` in the JSON and its `.coverage.json` receipt | `test_same_seed_date_and_register_are_byte_deterministic` |
| `generate_pack.py` (public CSV pack) | `--seed` (omitted draws a random seed, so always pass it) and `--as-of` (defaults to the extract date 2026-09-30; sets `generated_at`, never the clock) | `seed`, `version`, `generated_at`, `as_of`, `generator_revision`, per-file `file_sha256` in `manifest.json` | `test_pack_generator_is_byte_deterministic_with_manifest` |
| Stock fabric (`zf_stock_fabric.py`, seed 4820260930) and EPC (`zf_stock_epc.py`, seed 4820261015) | `--seed` and the register CSV; output depends only on seed and home ID, no clock | `seed`, `version`, `generator_revision` in each summary JSON | `test_stock_fabric_and_epc_generators_are_byte_deterministic_with_revision` |
| Stock register (seed 4820260930, 60000 homes) | Seed recorded in `private-stock-manifest.json` | Seed, version, generated date only | None: the register generator is not in the repository (it samples real OpenStreetMap anchors) |
| Wholly fictional stock-scale fixture (not the private stock register) | `--seed`, `--as-of` snapshot label, `--homes`, `--events-per-home`; events remain calendar-year 2026 | `seed`, `version` 1.2.0, `as_of`, dependency-aware `generator_revision`, per-file `file_sha256` | `src/core/tests/test_synthetic_determinism.py`: all files, changed seed, historical payload hashes |
| Sensor backfill (labelled synthetic climate, not device evidence) | `--seed`, `--as-of` exclusive UTC end, `--days`, `--cadence`, `--homes`; fixed recorded stock seed | `seed`, `version` sensor-backfill-v2, `as_of`, UTC start/end, dependency-aware `generator_revision`, per-file `file_sha256` including estimate and register | Same src test file: all files/multiple shards, changed seed/date, exact window, estimate propagation, historical payload hashes |

`generator_revision` is a SHA-256 prefix over the generator source files, so
a changed generator is visible in the manifest without relying on Git
metadata or the clock. The committed `manifest.json` predates these fields
and still carries a wall-clock `generated_at`; it is not rewritten here
because that would replace published pack files. The next approved refresh
adds the new fields.

The src tools hash their generator source and the shared provenance helper,
synthetic package initializer and stage-order source; sensor also includes
the scale generator. Source revision is a full SHA-256, not a wall-clock or
Git commit identifier. The older support generators retain their existing
16-character SHA-256 prefixes. Byte equality is evidenced on the local
Python 3.12 environment; source fingerprints do not pin Python's random/math
implementation across arbitrary runtimes. Reproduce with the same runtime
and parameters. Sensor's omitted as-of retains 2024-10-01 as start, even for
custom days; the full 730-day default ends on 2026-10-01.
See the [core CLI recipes](../../../../src/core/README.md#datasets-fixtures-and-synthetic-tools).

Refresh policy (proposed defaults; the owner has not yet approved them).

* Cadence: regenerate only on a recorded trigger, such as a schema or
  generator change, a rubric or scenario change, or a new exercise baseline
  date. No scheduled refresh.
* Approval: the project owner approves each refresh, naming seed, as-of date
  and target. Regulatory or scenario-rule changes also need the named human
  approval required by the repository's legal evidence conventions.
* Version: a refresh that changes any row, or the seed, bumps the pack
  `version`; a regeneration with the same seed, as-of date and
  `generator_revision` must reproduce the manifest hashes exactly.
* Live records: a refresh writes to a new path or version and never
  overwrites live exercise records. Operator seeding keeps the existing
  Azure SQL records and the 11 private tenant staff bindings; restart does
  not replace them. Replacing a live database needs explicit reset
  authority, as on 2026-10-14. Prior versions and their manifests are kept.
  The src scale/sensor writers enforce a new or empty destination and reject
  an existing nonempty directory (including stale shards) or direct symlink.
  This is not a concurrent transaction, rollback on disk failure, or a guard
  on the older support writers: publish their refreshes only to new paths.
  No generator is authorized to reset an existing database.
* Evidence boundary: refreshed data stays synthetic, with no real personal
  data, and is not evidence of resident or business outcomes.

Open items for the owner (not decided here).

* Approve or amend the cadence, approver and versioning defaults above.
* Provide or commit the stock register generator, or accept the recorded seed
  as the only reproduction route; the first acceptance criterion is not met
  for the stock register until then. The fabric and EPC generators derived
  from the register are now tested byte-identical; the committed private
  summaries predate `generator_revision` and are not rewritten here.
* The earlier "no sensor generator" statement is superseded by the migrated
  sensor-backfill tool and bounded byte-level tests above. Approve full-stock
  storage/cost and resolve external climate/device evidence separately (see
  [IoT sensor analytics research plan](../iot-sensor-analytics-research-plan.md));
  a small deterministic sample is not a verified full-stock sensor run.
* Decide whether to regenerate the committed pack manifest with the new
  fields.

This pack gives the Zava Forward discovery a realistic body of operating
records to analyse. It models a competent, busy retrofit team one year into
delivery. The team knows the programme is behind plan and suspects several
bottlenecks, but its own reports cannot show where the time goes.

The pack supports the
[Retrofit Flow and Constraint Discovery Brief](../../../brds/retrofit-flow-discovery-brief.md):
reconstruct each home's path from candidate to accepted handover, separate
active work from waiting, find unaccepted handoffs and return loops, and test
candidate constraints against evidence. It also provides test data for later
agent and workflow concepts. Redesigning the process is a later step.

The pack was generated so that analysis can be blind. The generator, its
parameters and an answer key are held outside the knowledge base by the
project owner. Record your findings before consulting them.

## Scenario

### The Programme

* Zava Forward mobilised in July 2025 to move homes towards EPC C. It
  identified 980 candidate homes in four waves (July 2025, October 2025,
  January 2026 and April 2026), plus ad hoc additions.
* Candidates identified from 2025-07-01 to 2026-06-30 form the twelve-month
  baseline population. Homes added from July to September 2026 are included
  but fall outside the baseline.
* The year-one plan was 600 completions by September 2026. The extract date
  is 2026-09-30.
* Most homes are funded through a Warm Homes: Social Housing Fund Wave 3
  route, with internal capital where a home is not grant eligible. The award,
  grant rates and claim cycle are synthetic assumptions, not company facts.
* The candidate homes sit in three fictional localities: an urban core with
  1960s and 1970s low-rise blocks, former coalfield towns with terraces and
  semis, and a rural and coastal area with off-gas bungalows.

### The Team

| Code | Role |
| --- | --- |
| `PM-01` | Retrofit Programme Manager |
| `PS-01` | Programme Support Officer, maintains the tracker |
| `RC-01`, `RC-02` | In-house retrofit coordinators (PAS 2035 design review and sign-off) |
| `RC-03` | Framework retrofit coordinator, part time from April 2026 |
| `RLO-01` to `RLO-03` | Resident liaison officers, one per locality; `RLO-03` left in May 2026 |
| `GEO-01` | Grants and Evidence Officer, 0.8 FTE |
| `QA-01` | Quality inspector |
| `BSL-01` | Building safety liaison with the repairs and hazard service |
| `SUP-RA` | Retrofit assessment framework |
| `DES-1` | Retrofit design consultancy |
| `SUP-F1`, `SUP-F2`, `SUP-HP`, `SUP-HT` | Suppliers for fabric measures, external wall insulation, heat pumps and heating |

### How the Team Works

These practices are the team's normal, reasonable ways of working. They are
listed because they shape the records.

* The programme tracker is a SharePoint spreadsheet with one row per home.
  Each row holds the current status, owner, RAG, delay code, notes and
  milestone dates. Changing a status overwrites the previous value.
* The delay-code list was revised on 2 February 2026 from six broad codes to
  fourteen specific codes. Rows not touched since then keep the old code.
* The group formed from the merger of two heritage associations, so many
  homes carry a legacy reference as well as the group property ID. The
  repairs system and some suppliers still use legacy references.
* Assessment reports reach the design consultancy through a shared mailbox.
  Designs go back to the coordinators by email.
* Suppliers report appointments and completions through their own portals.
  Exports use UK `dd/mm/yyyy` dates.
* Damp, mould and other hazards found during retrofit visits are referred to
  the separate repairs and hazard service, and a retrofit hold is placed in
  the tracker.
* Programme Support catches up on tracker updates before the monthly
  programme board, and closed cases are swept at the end of each month.
* Grant claims are prepared quarterly.

### What the Team Sees

The programme board report for September 2026 shows 466 completions against
a plan of 600, with GBP 0.83 million of grant claimed. Delay codes on open
cases point most often at contractors, then residents. Earlier in the year
many homes sat "in design" for months. Staff believe the causes are supplier
capacity, residents not engaging and a slow design consultancy. Nobody has
yet joined the records together to test that belief.

## Files

| File | Source it imitates | Grain | Rows |
| --- | --- | --- | --- |
| [property-register.csv](./property-register.csv) | Asset management system extract | One row per property record, including merger duplicates | 996 |
| [candidate-lifecycle.csv](./candidate-lifecycle.csv) | Programme tracker (current state only) | One row per candidate, including duplicate rows | 992 |
| [lifecycle-events.csv](./lifecycle-events.csv) | First-pass event log assembled from tracker history, mailboxes and system extracts | One row per stage event | 9,859 |
| [resident-journey.csv](./resident-journey.csv) | Housing management and CRM household view | One row per candidate household | 980 |
| [resident-contacts.csv](./resident-contacts.csv) | CRM contact log | One row per contact | 5,905 |
| [appointments.csv](./appointments.csv) | Assessor and supplier portal exports | One row per booked visit | 1,530 |
| [safety-holds.csv](./safety-holds.csv) | Hazard referral register joined to the repairs system | One row per retrofit-channel hazard | 97 |
| [quality-evidence.csv](./quality-evidence.csv) | QA inspection log and evidence tracker | One row per inspection, submission or review | 1,381 |
| [grant-and-finance.csv](./grant-and-finance.csv) | Finance and grant tracker | One row per candidate, plus a duplicate line | 981 |
| [contractor-capacity.csv](./contractor-capacity.csv) | Supplier KPI returns and the internal leave planner | One row per resource per month | 135 |
| [programme-board-snapshots.csv](./programme-board-snapshots.csv) | Monthly programme board report | One row per month, section and item | 480 |
| [edge-case-returns.csv](./edge-case-returns.csv) | Team issues and escalations log | One row per logged issue | 172 |
| [delay-code-dictionary.csv](./delay-code-dictionary.csv) | Delay-code lists v1 and v2 | One row per code | 20 |
| [data-dictionary.md](./data-dictionary.md) | Field definitions, keys and allowed values | | |
| [manifest.json](./manifest.json) | Seed, dates and row counts | | |
| [handover-examples.md](./handover-examples.md) | Example handovers taken from the records | | |
| [missing-information-plan.md](./missing-information-plan.md) | Evidence still missing and next iterations | | |
| [evidence-gap-register.csv](./evidence-gap-register.csv) | Evidence domains and their coverage in this pack | | |

`candidate_id` links the tracker, events, contacts, appointments, quality,
finance and issues tables. Some source rows carry only a property reference,
and that reference may be the group ID, a legacy reference or a mistyped
value. Matching them to candidates is part of the analysis.

## Working With the Records

Expect the imperfections of real operational data from a professional team.
They include mixed date formats, legacy and mistyped references, duplicate
records from the merger, events missing from source extracts, statuses not
yet updated and milestones not entered. They also include free-text dates,
currency formatting and delay codes from two dictionary versions. Report
these issues rather than silently correcting or discarding them. Keep unknown
or disputed causes visible.

Suggested discovery questions:

1. Where did each home spend its calendar time, and how much of it was
   waiting rather than work?
2. Who owned each waiting period, and which handoffs were never acknowledged?
3. Did the constraint stay in one place over the year or move?
4. How do the team's delay codes compare with the time attribution rebuilt
   from events?
5. How far apart are practical completion, documentary acceptance, resident
   handover and accepted handover, and why?
6. Were suppliers short of capacity or short of ready work?
7. Do access failures, refusals and withdrawals fall evenly across
   households?
8. Which delays could have been predicted from data held before the survey?
9. Are any safety holds still open after the underlying repair was completed?

## Limits

* The scenario is one synthetic realisation. Its rates, durations and
  constraints do not describe Zava North Homes or the sector.
* Costs, grant amounts, supplier contracts and staffing are illustrative.
* Energy outcomes, bills, comfort, complaints and resident satisfaction are
  not modelled.
* Regulatory timing appears only as dates for context. Any statutory
  interpretation needs the sources in the
  [Regulatory Source Register](../../regulatory/README.md) and human legal or
  compliance review.

## Document and form fixtures (2026-10-15)

Issue #171 adds `generator/zf_documents.py` (under
`support/synthetic-data/retrofit-flow/zava-forward-year-one/`) and the committed
output `src/importer/evals/document_form_fixtures.json`, tested by
`src/importer/tests/test_document_form_fixtures.py`.

Document-control fixtures (scan classes, retention triggers and legal holds for
120 homes from the same register) come from `generator/zf_document_controls.py`,
output `src/core/evals/document_control_fixtures.json`, tested by
`src/api/tests/test_document_controls.py`.

* Source: one home per neighbourhood cluster drawn from the 60,000-home synthetic
  stock register, seeded (`--seed 20260901`), so output is byte-identical for the
  same seed and register. Every record carries `is_synthetic` and a SYNTHETIC label.
  No addresses, residents or image bytes are included; photos are descriptors.
* Families: 120 (30 tuning, 30 calibration, 60 held-out), split by family and
  cluster so no home or cluster appears in two splits. Each has a survey report,
  EPC certificate, invoice, photo descriptor, twelve gold field values and the
  synthetic form schema `SYN-FUND-FORM-1.0`.
* Seeded defects (AC-049): duplicate home, missing required, missing conditional,
  wrong unit, wrong currency, changed total, unknown eligibility and unapproved
  match budget. Each defect has a fixture-owned expected rule, field, status and
  reviewed-pack block; every split contains every kind.
* Dependency manifest (AC-051): per family, exact affected and unaffected field and
  calculation IDs for an invoice-template change and an EPC supersession.

Open items: the real funding form schema, terms and approved rules are unresolved
(PRD OQ-015), so the schema is a labelled placeholder with no approver. Gold labels
are generator-owned; the PRD requires human engineering adjudication before
held-out testing, which has not happened. Documents are plain-text fixtures, not
rendered PDFs or images.

## Synthetic data needs inventory and phase gate (2026-10-15)

Issue #166, parent #165. The machine-readable inventory is
[needs-inventory.json](./needs-inventory.json) (version 1.2.0, draft awaiting
owner review). It lists 13 needs with source reference, consuming issues,
volume, proposed owner and generator coverage (covered, partial or missing).

Gate rule: a build epic that consumes synthetic data cites its inventory row
(`SN-nn`) before work starts, and a partial or missing row needs a recorded
owner decision on volume and scope first. The epics gated today are #109
(SN-09, partial), #157 (SN-08, partial), #104 (its cited rows SN-01 to
SN-07 and SN-10) and #144 (SN-01, SN-04, SN-12). These are issue-specific
citations, not blanket approval of every row in a numeric range.

The versioned [constructed-scenario manifest](./scenario-manifest.json)
links the exact inventory version, review date and all thirteen reviewed rows.
This iteration records an automated engineering review of public repository
evidence, not owner ratification. Its eleven profile paths and nine workflow
checks remain explicitly deferred to #103; no defaults, safe endpoints,
connected lifecycle or full FR-035 acceptance are claimed.

Before each iteration starts, review every row; bump the inventory version
and review date, update the manifest binding, version and iteration, and
append the [knowledge log](../../log.md). Preserve prior versions in Git.
`src/core/tests/test_needs_inventory.py` checks the reciprocal link, exact
version/date, complete unique reviewed rows and this iteration's pending-owner
boundary, including negative mutations. It does not enforce GitHub issue
chronology or grant approval. A data-consuming epic must record its SN row
citations and the required owner scope/volume decisions before build work
starts; an automated review or a passing test cannot waive that gate.

Coverage corrections in v1.2.0 distinguish existing stock, EPC, chat, scale
and sensor fixture tooling from accepted application coverage. Sensor
backfill is partial, not missing; full-stock materialization, external climate
verification and live coverage remain unevidenced. Projected generator volumes
do not resolve the open owner volume/scope decisions.

Open items: owner approval of the inventory and row owners, volumes for
SN-03, SN-08 and SN-09, and reconciliation with the 2026-10-14 backlog
handoff matrix, which is not in the repository.

### Generator gap closure (2026-10-15)

Issue #167, parent #165. Inventory version 1.1.0 adds a `gap_closure` entry to
every need and a `generator_conventions` block in
[needs-inventory.json](./needs-inventory.json).

| Gap | Child story or owner |
| --- | --- |
| SN-01 stock link and fabric attributes | #168 |
| SN-02 residents and tenancy | #169 |
| SN-03 surveys and EPC | #170 |
| SN-04 to SN-06 contractors, finance, grants, safety and consent | #173 |
| SN-08 chat and memory | #172 |
| SN-09 sensors | #177 and #184 |
| SN-11, SN-12, SN-13 | #103, #144 (load fixture) and #176 |
| SN-07, SN-10 (delivered) | #171 and #174, closed |

Extensions reuse the existing generator modules, the recorded seed, the
existing identifiers and `is_synthetic=true`; no second generator is added.
`src/core/tests/test_needs_inventory.py` retains the inventory binding checks.
The src [coverage baseline tool](../../../../src/core/README.md#generator-coverage-baseline-167)
adds semantic route validation and a deterministic, read-only JSON report:

```bash
python3 -m zava_forward.core.synthetic.coverage \
  docs/reference/research/retrofit-synthetic-data/needs-inventory.json
```

Run from the repository root after installing core. It rejects malformed or
duplicate need/issue identifiers, missing convention declarations, blank
closure rationale, unexplained deferrals and delivered claims for partial or
missing needs. Negative and CLI tests live in
`src/core/tests/test_generator_coverage.py`; existing generator tests continue
to check seeded output, links, labels and human-decision boundaries using a
wholly fictional register rather than private geography.

The unchanged merged v1.2.0 baseline has 13 routed needs: two covered, eleven
partial, none missing. This validates recorded routes and declaration presence,
not child delivery, owner scope decisions or generated-record conformity.
The scale fixture's homes/events carry a manifest-level synthetic label,
not per-record `is_synthetic=true`; the universal convention above is therefore
an intended rule with an unevidenced existing-output gap, not a proven result.
No second generator, private output or owner deferral is introduced.

Open items: owner confirmation of the mapping, and whether regenerating the
private SN-01 register from a committed generator sits in #168 or is deferred.
No deferral is recorded yet.

## Stock-to-case link and fabric attributes (2026-10-15)

Closes the generator gap in [#168](https://github.com/jmservera/ama/issues/168).

* Every case carries `synthetic_stock_anchor_id`. The private MVP JSON now has
  a `stock_link` report (linked, unlinked with IDs, distinct homes, shared
  homes) and a `stock_fabric` block per case, derived from the linked stock row.
* `zf_stock_fabric.py` adds build year, age band, dwelling type, construction
  and heating to each of the 60,000 register homes. Output depends only on the
  seed and the home ID. Rebuild with
  `python3 support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_stock_fabric.py`
  (writes a git-untracked fabric CSV and the committed
  `private-stock-fabric-summary.json` with counts and weights).
* The distributions (age band by locality, construction by age band, heating by
  locality) are exercise assumptions chosen by the generator author. They are
  not Zava North Homes facts, surveys or EPC data and must not be cited as such.
* The case `home.built` and `home.type` values from the 980-case model remain a
  separate denominator and are not reconciled with `stock_fabric`.

## Stock EPC, survey and conflict fixtures (2026-10-15)

Delivers [#170](https://github.com/jmservera/ama/issues/170) under #167. All
values are labelled synthetic fixtures under the owner decision in ADR 0005
(2026-10-15); they are not lodged EPCs, survey results or company facts.

* `zf_stock_epc.py` adds, for each of the 60,000 register homes, an EPC record
  (band, SAP, lodged and expiry dates, status, recorded age band, dwelling
  type, construction, heating) and, for about 35% of homes, a survey record
  (type, date, surveyed SAP and band, surveyed age band, construction, heating).
  Output depends only on the seed and the home ID.
* Reconciliation: EPC and survey attributes are derived from the stock fabric
  (`zf_stock_fabric.py`). Without a seeded conflict they equal the fabric
  values and the EPC and surveyed SAP differ by at most 3 points. The EPC band
  is derived from the SAP with the standard A-G cut-offs.
* Seeded conflicts (8% of surveyed homes, 1,679 in the default build) are
  listed in the committed `private-stock-epc-conflict-manifest.csv` with type,
  EPC value and surveyed value: band, heating, construction or age band
  differs. `private-stock-epc-summary.json` holds counts and assumptions.
  The full EPC CSV is git-untracked; rebuild with
  `python3 support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_stock_epc.py`.
* Each case in the private MVP JSON gains a `stock_epc` block from its linked
  stock home, and `stock_epc_seed` is recorded.
* Open: the band, SAP and conflict rates are generator-author assumptions, not
  calibrated to Zava North Homes data. The case `epc_band` model in
  `zf_model.py` is a separate denominator and is not reconciled with
  `stock_epc`. Owner confirmation of the conflict mix is not recorded.
