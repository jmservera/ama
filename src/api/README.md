---
title: Zava Forward API and web workbench
description: Staff features, configuration, local run, honest limits and container checks for the api project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-17
ms.topic: reference
---

## Coordinator heatmap and lifecycle funnel (#101)

Original Review RV-001 exposed false403 for staff with a mixed-case stored email.
Correction ONE normalizes the coordinator lookup key without weakening current
identity checks. Actual JSON/SQLite HTTP regressions and a mixed-case Chromium
journey pass. Original Defects found verdict remains unchanged; independent
coordinator acceptance is still pending.

From Overview, choose **Coordinator heatmap and lifecycle funnel**. The existing
workbench/Leaflet map now has a scoped read-only coordinator mode, not a new
framework. Manual case routes and the legacy overview remain available.

```text
GET /api/coordinator?view=all&as_of=2026-10-10T12:00:00Z&area=Test
GET /api/coordinator?view=all&as_of=2026-10-10T12:00:00Z&metric=exits&metric_stage=Contact%20paused
```

Registered staff only; contractors and unknown/revoked actors are denied before
aggregation. `view=mine` (default) means current owner-code assignment; `all`
means the existing staff-wide permitted open cases, not additional case authority.
The [core contract](../core/README.md#read-only-coordinator-populations-101)
defines denominator, stopped work, draft priority, observed flow and unknowns.
Existing source filters `stage/area/wave/owner/contractor/flag/queue` and `q`
are shared by map, heatmap, funnel and record pages. `group_by` is `area`
(default), `building` or `archetype` (recorded home type, not an approved technical
classification). Missing groups remain explicitly Unknown.

`as_of` is required and selects recorded events, not historical membership;
optional `start` is inclusive UTC. The current `stage` source filter never
changes meaning when `metric_stage` drills an observed entry/exit/return/reopen.
For example, a current Contacting resident case can appear in exits from Contact
paused. Metrics also include `current`, `stopped`, `missing_geocode`,
`unknown_history`, `priority` and `filtered_out`. Unapproved priority refuses
drillthrough. `filtered_out` means source filter/search exclusions, not lifecycle
exclusion, and cannot select a group/stage cell. Unknown/empty/repeated parameters
refuse with 400; `limit=1..100` and nonnegative `offset` page stable case IDs.

Map `total` equals record selection total, including missing/invalid coordinates;
`mapped`, `missing_geocode` and `in_view` are separate. Panning narrows only
mapped viewport coverage, not the record denominator. Every count link retains
source filters and event window. Tables and native keyboard links/buttons remain
equivalents to heat colours and map gestures. **Show these as a list** focuses
the complete selected record table, including cases without coordinates.
No new map provider, licence, ranking, approval, history writer, AI or service.

From `src/api`, after editable source installation:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest \
  test_coordinator_api.CoordinatorApi test_coordinator_api.JsonCoordinatorApi -q
ZF_COORDINATOR_BROWSER=1 PYTHONPATH=tests:../core/tests:../agents/tests \
  ../../.venv/bin/python -m unittest \
  test_coordinator_api.CoordinatorApi.test_actual_browser_keyboard_filters_drill_map_unknowns_and_denials -v
```

`ZF_COORDINATOR_MSSQL=1` selects `test_coordinator_api.MssqlCoordinatorApi`
against an explicitly task-owned loopback SQL Server only. Its UUID-named
`zf_coordinator101_*` fixture databases are dropped after each test; no shared
database is eligible. The browser uses the actual local application, synthetic
SQLite, keyboard filter/exit/record/map-list/cluster navigation, coverage/unknown
labels, count parity, denials and 320/390/1280px reduced-motion reflow. Local
engineering evidence is not WCAG, human understanding, Azure or independent
coordinator acceptance.

## Historical progress report and export (#102)

Existing staff-only report paths support explicit `report=progress`:

```text
GET /api/stats?report=progress&as_of=2026-10-10T12:00:00Z&view=all&ready=2
GET /api/cases.csv?report=progress&as_of=2026-10-10T12:00:00Z&view=all&ready=2
```

Use URL encoding for offset timestamps (`+` becomes `%2B`). `as_of` is required,
timezone-aware and not future. Optional `start` must be timezone-aware and no
later than `as_of`. Both boundaries are inclusive for events; observed interval
clocks are clipped to the requested period. Supported `view` values are
`mine` (default), `all`, and manager-only `closed`. Existing stage/area/wave/
owner/contractor/flag/queue source filters are reused; their membership is
explicitly current-record selection, not historical reconstruction.
Unknown/empty/repeated parameters or invalid assumptions return 400. Contractor/
unknown roles are denied; direct Store calls enforce the same staff boundary.

The [core report contract](../core/README.md#historical-progress-evidence-and-declared-forecasts-102)
defines source mapping, partial/unknown history, independent handoff clocks
and forecast limitations. Optional `ready` declares a hypothetical ready count,
not actual consent or technical readiness. Optional positive `capacity`,
`duration`, `weeks` default to 2/1/4. Without declared `ready`, a requested
scenario is refused; with no scenario parameters Forecast is unavailable.
No model/provider is called. Forecasts cannot release work or approve outcomes.

JSON and the `progress.csv` attachment serialize the same `progress/v1` report,
including definitions, source locators, exact as-of/cohort/denominators,
unresolved exceptions, assumptions, sensitivities and Not reviewed approval.
CSV uses UTF-8, LF, standard quoting and fixed `section,value` rows; each value
is a compact sorted-key JSON cell. Parsing those cells reconstructs the exact
JSON report. Case IDs and events have stable ordering; repeat inputs produce
identical CSV. Raw identities, notes, resident fields and supplied source/
commercial evidence are not included. Empty cohorts/history remain visibly
unresolved. Default `/api/stats` and `/api/cases.csv` responses are unchanged.
No existing screen was redesigned or wired to this optional mode.

After pip editable core/agents/API installation, run from `src/api`:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest \
  test_progress_report_api.ProgressApi test_progress_report_api.JsonProgressApi -q
```

`ZF_PROGRESS_MSSQL=1` selects `test_progress_report_api.MssqlProgressApi`.
It refuses non-loopback SQL servers, creates UUID-named `zf_progress102_*`
databases and deliberately retains them: do not target shared/live systems.
Configure existing `ZF_SQL_*` privately for a uniquely named local Docker SQL
Server. SQLite and actual MSSQL exercise reload, external-writer refresh,
report/CSV parity and unchanged audit. Image checks run the authenticated
local report as UID/GID 10001 with read-only root and reduced capabilities.
These are engineering checks, not browser, WCAG, human, operational, AI or
Azure acceptance. Prospective capture now covers the actual controlled
stage/handoff/quality writers described in the core contract; absent historical
periods and nonexistent general forward/closure writers stay unknown.
The same existing HTTP 503 `outcome=committed` contract handles a committed
transition whose refresh/acknowledgement failed, without reporting rejection.
Verified operational capacity and complete historical coverage remain separate
evidence prerequisites.
The one original Review found blank-query and UTC-range handling defects;
correction ONE adds explicit refusals and failing-first regressions. Final
focused checks ran 88 tests plus eight actual loopback MSSQL tests, and the
corrected non-root image exercised exact installed source hashes and HTTP
report/export behavior. The original adverse Review is retained; these
targeted checks are not a second full Review or independent coordinator Pass.

Coordinator correction TWO addresses a reachable mixed-precision handoff:
precise offer/accept events surround legacy minute-truncated receipt events.
Reports preserve source versions and valid lifecycle sequence, expose precision
and cutoff unknowns, and never manufacture a wait duration or assert a
boundary-ambiguous event occurred before as-of. Precisely backward or otherwise
invalid history remains contradictory. New handoff writes preserve UTC
microseconds; old history is untouched. JSON/CSV retain identical definitions,
event order, as-of and denominators. The independent exact-28227fa8
Revise / Medium disposition and original adverse Review remain retained;
targeted correction evidence does not self-award acceptance.

## Resident commitments and remedy API (#88)

Existing `POST /api/cases/{case_id}/resident` and case detail remain the only
routes. The [core contract](../core/README.md#resident-commitments-and-independent-remedy-clocks-88)
defines named owners, independent clocks, legacy confirmation and SQL validation.
The existing resident panel records full commitments and shows response/remedy
status, owner and date separately, including open items after response closure.
Nothing sends messages, proves receipt, determines lease responsibility or
changes an approval. Existing non-digital service/complaint routes stay available.

Additional actions: `update_record`, `remedy_confirm`, `remedy_update` and
`service_reopen`. Remedy actions include request `id`; all four include integer
`expected_version`. Version zero means absent/unversioned, not permission to
overwrite a known record. `remedy_confirm` supplies owner/basis; remedy progress
supplies status/note and optional reassigned owner; response reopen supplies note.
Service intake additionally offers Charge query and Household dispute.
Existing service update/close request shapes remain compatible; `status` means
response, never remedy. Handoff inputs no longer create partial commitments.

`service_reassign` recovers a departed response assignee through the same endpoint.
Only an existing Retrofit Programme Manager or Programme Support Officer may
submit request `id`, integer `expected_version`, `responsibility` service/redress,
new current eligible named `owner` email and reason `note`. The existing panel
shows this form only to those roles, and shows old/new owner, actor, reason and
time in request history. No manager becomes owner implicitly. Server-side writer
validation also rejects stale versions, changed identities and non-independent
complaint/review assignments. Remedy ownership and other clocks remain unchanged.
Response status owner/date follows responsibility, not shared-person email:
redress for Closed or Independent review, otherwise service. Reassigning the
other responsibility preserves that status clock, including legacy Unknowns.

Invalid input returns 400, stale version/writer 409 and missing/current-owner
authority 403. Post-COMMIT synchronization or subsequent detail failure returns
409 with `outcome: "committed"` and explicit reload/reconcile instructions, not
a claim that nothing was recorded. Scoped resident forms retain input and inline
live errors; uncertain/committed results disable ordinary resubmit until reload.
Registered roles are server-enforced; neither a request role nor owner label
grants authority. New references and nested handoff commitment snapshots are
hidden from non-resident-view roles; contractor allowlists remain unchanged.

`test_resident_api` runs authenticated loopback HTTP with small fictional SQLite.
`ZF_RESIDENT_BROWSER=1` enables its actual Chromium journey: invalid commitment,
keyboard create/reassign, close response with remedy still open, remedy close/
reopen, response-only reopen, departed-owner manager recovery with retained
invalid input/error focus, recovered-owner update, independent response closure
and 320/390/1280 widths with reduced motion.
This is engineering evidence, not screen-reader, human usability or WCAG acceptance.

## Grant and application records (#95)

Existing `POST /api/cases/{case_id}/grant` and `/funding` routes now use
the [core current-human designation and evidence contract](../core/README.md#grant-lifecycle-and-human-exercise-designation-95).
Missing/stale staff or missing, revoked, expired, wrong-state/case/route
designation returns 403; missing event evidence, legacy unknown-currency
proposal or unsupported currency returns 400; stale SQL writers return 409.
Request-supplied roles/designations cannot confer authority. No endpoint submits
to a funder, executes payment or grants real financial authority.

Funding `approve`, `submit` and `confirm` requests keep `{action, text}`:
`text` must now contain the event-specific evidence reference (1-200 characters).
Application confirmation is explicitly labelled as application status, not a
grant award or cash receipt, and requires its own reference in the existing
panel. Application events leave the separate grant history/provider finance
unchanged. Opportunity GBP 40 million is never inherited as award/cash.
The Finance role still exposes the panel, but visibility is not designation.
No existing staff is automatically granted authority; real delegation remains
unverified and exercise authority is refused in production.

`tests/test_grant_lifecycle_api.py` uses authenticated loopback HTTP with tiny
temporary synthetic SQLite. `ZF_GRANT_BROWSER=1` additionally runs actual local
Playwright over the changed confirmation control, missing-evidence refusal and
Opportunity-only/Confirmed-application mixed state. These are focused engineering
checks, not full WCAG, human usability, real delegation or deployed acceptance.

## Per-measure quality API (#91)

The existing `POST /api/cases/{id}/quality-*` routes keep their request shapes.
`quality-submit` records checklist evidence and accepts the current
`context_revision`; when replacing Accepted/Handed over evidence it invalidates
all former same-measure acceptance/handover, not other measures. The
[core quality contract](../core/README.md#per-measure-quality-and-handover-controls-91)
describes retained lineage, independence and transactional behavior.
`quality-fix` now requires a nonempty `note` describing remediation and its
photo/document/inspection reference. `quality-reinspect` requires Fixed state.
No endpoint grants professional authority or pays anyone.

The authenticated actor, never body-supplied name/role, authorizes every write.
Contractors continue to receive 403 for all quality/finance writes; staff record
provider evidence through the existing manual route. Foreign supplier cases
remain inaccessible. Unknown/revoked staff and self-accepting identity aliases
are denied. Malformed/negative indices, missing remediation and actions on a
superseded record return 400. SQL optimistic conflicts return 409.
A confirmed committed decision whose post-commit refresh fails returns 503
with `outcome: "committed"` and explicit guidance to reload and inspect history
before retrying. It is not reported as success or rolled back; the committed
success audit and any legitimate audit prefix remain exactly once.

The existing quality panel labels remediation evidence, retains input and
focuses the missing-evidence field on failure. Replacement asks for confirmation
and displays the prior acceptance/handover as historical, with no old action
buttons. A fresh independent acceptance and resident handover remain necessary.
The actual fictional loopback Chromium journey exercised those steps, keyboard
fix submission, cancellation/confirmation, labelled controls and 320/390/1280px
reflow with reduced motion and no page errors. It also exercised an actual
post-COMMIT refresh failure, visible committed/reload guidance and reload
confirming accepted state. This is engineering evidence, not a WCAG,
screen-reader, resident-understanding or competent-human sign-off.
Existing form/navigation accessibility gaps remain outside this narrow change.

`test_role_matrix.QualityMatrix` exercises the actual authenticated SQLite HTTP
routes, contractor/foreign-case denials, forged-body refusal, remediation,
replacement, explicit committed-refresh outcome, and unchanged finance/grant
records. The shared `server.py` change is only the quality-specific exception
handler; its #95 overlap is declared. No `app.js`, `finance.py`, dataset fixture,
scenario manifest or shared SQL helper change was required.
The current BRD FR-017 describes handoff information; PRD FR-017 describes this
quality lifecycle. They are not represented as identical requirement numbers.

## Record-only finance API (#94)

`POST /api/cases/{case_id}/finance` retains its existing single-record action
contract; `GET /api/finance` retains the human exception/hold queue.
The [core finance guide](../core/README.md#record-only-finance-controls-94)
describes current identity, line matching and persistence controls.
No endpoint pays, submits banking instructions or grants authority.
External-payment statuses are notes only. Budget/commitment and grant/cash
records are unchanged by those notes.

Current registered Finance staff are rechecked for every write, including
transaction-time SQL validation. A preparer with an alias sharing email, staff
code or OID receives 403 when attempting their own approval/disposition or
hold release; distinct permitted staff with the same role are supported.
Unknown match inputs and held/stale acceptance return 400 with the existing
plain-language error. Optimistic SQL writer conflicts return 409.
Existing screens already render the returned zero-based exception `line` as a
human one-based line number; no web assets or browser behavior were changed.

`tests/test_finance_match_api.py` exercises authenticated loopback HTTP over
temporary fictional SQLite, including actual same-role identity refusals,
unknown line exceptions/queue, held disposition, external status notes and
reopened ledger invariance. Backend-only checks do not claim browser/WCAG,
company delegation, Azure or real payment acceptance.
Core correction TWO also covers SQL recovery failure after an executed audit
INSERT: no failed approval event can be flushed at lock exit. Original errors
retain explicit recovery diagnostics. The endpoint contract and web assets
are unchanged; independent coordinator closure of PR #383 remains pending.
Authorized integration onto main `bbbc924` also retains merged stock/technical
actor validation, refusal ownership and checked-document recovery. Combined
stock API/workflow/role checks ran with the required `src/api` module path;
the existing opt-in stock browser check was skipped, not newly certified.
## Provider capacity and order API (#90)

Existing authenticated package, capacity and work-order routes retain their
response shapes. `POST /api/packages` requires a nonempty `contract_version`;
omitted, empty and whitespace-only versions return 400 without creating a
package. The existing screen displays an inline error and focuses the version
field without losing other inputs. Creation is a draft, never a grant of
authority. Positive capacity requires
the [core source and trusted delegation contract](../core/README.md#evidenced-provider-capacity-and-controlled-orders-90).
There is no endpoint to appoint a contract manager.

`POST /api/packages/{id}/capacity` accepts the existing `contractor`, `offered`,
`committed`, `evidence` reference and the structured `details` object below.
IDs/version/dates must refer to a real original upload in the current local
store, not this illustrative identifier:

```json
{
  "contractor": "Fictional Provider",
  "offered": 9,
  "committed": 1,
  "evidence": "SYN-COMMITMENT",
  "details": {
    "source_case_id": "SYN-HOME",
    "document_id": "actual-upload-id",
    "source_version": "1",
    "source_date": "2026-10-17",
    "reviewed_on": "2026-10-17",
    "valid_from": "2026-10-17",
    "valid_to": "2026-12-31",
    "unit": "home-work-order",
    "case_ids": ["SYN-HOME"],
    "status": "Committed"
  }
}
```

Unknown/invalid legacy capacity stays visible with `evidence_status` and
`usable_committed: 0`, rather than becoming available. A larger offer never
permits a second order against one committed unit. Existing orders may
progress at exact quota. Issue, every appointment outcome, reissue,
completion, correction and withdrawal each append a version/issuer snapshot.
The existing case advance route cannot confirm an unbooked or unevidenced
order. Contractors receive 403 for package reads and all procurement writes;
order reads filter by their current supplier identity.

The existing Capacity screen supplies labelled original-source/version/date/
unit/home fields, explicit unknown status, keyboard submission and inline
failure focus. Human authority and resident approvals remain server checks,
not screen permissions. AI/template notes say not an instruction; accepting
a proposal never issues an order.

Run the exact HTTP and domain suites from `src/api` with installed editable
packages. The optional browser check uses only temporary fictional SQLite,
blocks non-loopback requests and exercises manager/contractor journeys:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests \
  python -m unittest test_quality_procurement test_procurement_api test_role_matrix -q
PYTHONPATH=tests:../core/tests:../agents/tests \
  python checks/procurement_browser_check.py
```

With the existing opt-in SQL Server harness configured against a disposable
local container, select `test_mssqlstore.MssqlProcurement` and
`test_mssqlstore.MssqlProcurementApi`. Never point its destructive fixture
reset at shared/live SQL. Local browser widths 320/390/1280, keyboard and
reduced-motion checks are not human, screen-reader or full WCAG acceptance.
No live orders, payments, AI inference, company delegation or Azure SQL were
exercised. Existing #78 provenance and #97 forms contracts remain unchanged.

Shared-transaction integration coverage also selects
`test_mssqlstore.MssqlStockDecisions`,
`test_mssqlstore.MssqlFinanceSignoffs`,
`test_mssqlstore.MssqlStoreTests` and
`test_mssqlstore.MssqlImproveTests` against that disposable local server.
The finance suite replays existing budget, matching, approval-separation and
signoff controls; it does not incorporate another unmerged finance topic.
For merged #94's exact finance-match and recovery controls, additionally
select `test_finance_match_controls.MssqlFinanceChecks` with
`ZF_FINANCE_MSSQL=1` against the same disposable local server. That existing
fixture creates and removes only its uniquely named test databases.

## Form schema and candidate API (#97)

This is unapproved schema registration and candidate-only collection, not a
form approval, reviewed draft, field-review workflow or submission endpoint.
Every request requires authentication and current registered staff rights:
the intersection of existing Finance-view, resident-record-view and
reason-view permissions. Normally only the Programme Manager has all three.
Schema metadata never grants permission. Other roles cannot read retained
raw values or source/locator metadata through these endpoints.

| Method and path | Contract |
| --- | --- |
| `POST /api/form-schemas` | Register the next immutable schema version, 201; always `Unapproved` |
| `GET /api/form-schemas` | `{"schemas":[...]}` with definition, digest, actor/time and null approval evidence |
| `POST /api/cases/{case_id}/form-candidates` | Append one source-bound batch, 201; returns staged candidates or owned manual recovery |
| `GET /api/cases/{case_id}/form-candidates` | `{"batches":[...]}`; current-rights and source-presence/clean-scan check on every read |

Schema requests contain exactly `id`, `version`, `form_type`, `template`,
`reviewer`, `funding`, `rule_refs` and `fields`. Version is a positive sequential
integer starting at one per schema ID. Form type is `technical`,
`work-package`, `invoice` or `funding`. `template`, calculation and rule
references contain `id`, string `version` and `evidence_ref`.
The reviewer is an existing staff email, not an inferred approval.

`funding` contains `status`, `scheme_id`, `route`, `evidence_ref`.
`Unknown` and `Not applicable` require null references; funding forms cannot
be not applicable. `Evidenced` requires a scheme ID, supplied evidence
reference and route `competitive`, `allocation`, `award-return` or `claim`.
This records supplied metadata only, not actual approved scheme authority.

Each field contains exactly `id`, `section_id`, `type`, `unit`, `options`,
`required`, `required_when`, `source_authority`, `evidence_required`,
`calculation_ref`, `category`. Types and units are described in the
[core guide](../core/README.md#form-schema-registry-and-candidate-staging-97).
Options are nonempty unique finite scalars for enum fields only. Conditions
are `{field_id, equals}` references to another declared field, never executable
expressions. Source policies are `{kind, rank, evidence_ref}` with unique
existing document kinds/positive precedence ranks; evidence requirements are
nonempty text references. `category` is `value` or a human-only
`declaration`, `signature`, `attestation`, `consent` or `approval`.
Only `value` fields can receive candidates. Bounds are 200 fields/candidates
per request and 16,000 characters per raw value.

For an already registered unapproved `SYN-TECH` version one and an actual
uploaded text document containing `EPC D`, the staging request shape is:

```json
{
  "schema_id": "SYN-TECH",
  "schema_version": 1,
  "document_id": "actual-upload-id",
  "processing": {
    "kind": "text",
    "parser": "synthetic-importer",
    "parser_version": "test-1",
    "model_version": null,
    "route_evidence": null,
    "error_record": null
  },
  "candidates": [
    {"field_id": "epc", "raw_value": "D", "locator": {"start": 4, "end": 5}}
  ]
}
```

This example is not an approved template. Hash/version/date are copied from
the actual uploaded source, not accepted from the request. Text spans and
CSV cells are verified against exact source bytes; parser/model identity is
separately labelled `Supplied, unverified`. OCR imports use `kind: "ocr"`,
`{page, region}` locator, and supplied `route_evidence`/`error_record`; they
retain asserted lineage with `Unverified OCR import`, never claim pixel
verification or approve/run an OCR route. Unsupported/unreadable sources
record manual recovery with no invented candidates.

Malformed/forged keys and source mismatch return 400, denied identity/rights,
human-only fields or source-policy mismatch 403, missing/foreign case or
source 404, concurrency conflict 409, source-store outage 502 and unexpected
storage failure 503 with a metadata-only diagnostic. Reload after an uncertain
failure before retrying. Unknown funding routes and all unapproved versions
remain unusable for approved preparation; candidates never become accepted
fields or change source, consent, grants, payment or submission state.

The fixture exercise starts a responsive ephemeral loopback HTTP app over
temporary synthetic SQLite, authenticates fixture staff, registers/stages/reads,
checks forbidden paths and never calls inference:

```bash
PYTHONPATH="$PWD/src/api:$PWD/src/core/tests:$PWD/src/agents/tests" \
  python -m unittest discover -s src/api/tests -p test_form_staging_api.py -v
```

Run from the repository root with editable src packages installed. No UI
change, actual human approval, live AI/Azure/SQL Server, approved template
binding or #98 review/validation/pack/staleness acceptance is claimed.

## Controlled bulk preview API (#78)

Two additive authenticated POST routes expose the
[core administrative contract](../core/README.md#controlled-administrative-bulk-edits-78).
No web assets, role screen or existing case action changes. Trusted-proxy
requests still need the existing `X-ZF-CSRF: 1` header. Contractors and unknown
roles are denied; a role-visible screen cannot grant editing authority.

`POST /api/bulk-edits/preview` accepts exactly:

```json
{
  "case_ids": ["ZF-1", "ZF-2"],
  "changes": {
    "case_reason": "to check the supplied administrative reference"
  },
  "source": "SYN-REGISTER",
  "source_version": "v3",
  "reason": "Correct the constructed case explanation"
}
```

Select 1-100 distinct IDs. Allowed fields are `case_reason`,
`handoff_due_at` and `handoff_next_action`; handoff fields require an existing
active handoff. No null/empty values, inferred source/version, silent
truncation, extra keys, role/actor override or arbitrary nested JSON is accepted.
This route is also the preview path for a single permitted administrative edit.
It does not replace existing evidence, ownership or controlled workflows.

The 200 response contains `preview_id`, `status`, actor, source/version/reason
and ordered `records`. Each record has `case_id`, `changes` with field
`old`/`new`, `failures` and an outcome. Examples of a successful preview record:

```json
{
  "case_id": "ZF-1",
  "changes": {
    "case_reason": {
      "old": "to agree a visit",
      "new": "to check the supplied administrative reference"
    }
  },
  "failures": [],
  "outcome": "would_apply"
}
```

| Situation | Preview / apply behavior |
| --- | --- |
| All targets valid | `pending`, per-case `would_apply` or `no_change`; no case mutation |
| Any missing/noneditable/invalid target | `blocked`, failures for that ID, no inaccessible values; valid changed peers `batch_blocked` |
| All unchanged | `pending`, all `no_change`; apply records a batch result but no fabricated field history |
| Unknown keys/controlled fields/malformed request | 400 with explicit error and metadata-only refusal audit |
| Foreign creator or current authority/OID revoked | 403, no target content or edits |
| Stale, corrupted, blocked or consumed preview | 409, fresh preview required; no partial batch |
| Unexpected storage failure | 503 with explicitly uncertain outcome; inspect case history and request a fresh preview before retry |

After inspecting every record, `POST /api/bulk-edits/apply` accepts only:

```json
{"preview_id": "the-server-returned-preview-id"}
```

No new target/change is accepted at apply. Only the same current creator can
apply it, and all permission/freshness checks repeat under the SQL writer lock.
Success returns `status: applied` with each result `applied` or `no_change`.
The retained source/version/actor/time/reason and old/new fields are visible
in existing case detail `edit_history`, with normal note-visibility redaction.
Batch result and history survive SQLite reopening. Replaying a consumed
preview is denied, including after an uncertain commit acknowledgement.
Immutable issued outcomes, empty failures, exact ordered target/record coverage
and complete snapshots are required both before staging and at SQL commit.
Mutable status alone cannot enable blocked records; cached and persisted
status-only resets are refused with no case/history/success-audit changes.
No-op targets are also permission/freshness checked inside the transaction.

Technical, consent, safety, procurement, budget, invoice, payment, claim,
quality, defect/complaint closure and contractor-instruction fields are absent
from the allowlist and are rejected server-side, including mixed allowed plus
forbidden requests. Ownership transfer still requires receiver acceptance.
Resident-update commitments, independent hazard clocks and approvals are never
changed by an administrative due-date or next-action edit.

| Issue #78 criterion | Bounded evidence |
| --- | --- |
| Edits retain source/version/actor/time/reason | `test_exact_preview_before_apply_and_provenance_reopens`, exact history/audit equality and monotonic version tests |
| Targets, changes, failures, per-case outcomes before apply | Core and real loopback HTTP exact-shape tests, mixed missing/foreign/valid and no-op targets; zero pre-apply mutation |
| No controlled bulk approvals | Closed allowlist tests across all controlled categories, actual HTTP denials, creator/role/OID and transactional stale/guardrail races |

Correction TWO implements the earlier RV-002 evidence-upload and handoff
caller/API/UI gap using required explicit inputs and complete immutable
per-change events, not fabricated defaults or wider bulk fields; see the
[single-record core contract](../core/README.md#single-record-upload-and-handoff-change-sources-correction-two).
Original Review and review512a59c4 Revise remain historical evidence;
coordinator independent reassessment of the final head is required.
FR-005/006/007 here use PRD numbering;
the same-number BRD entries concern lifecycle and technical release. This is
not full PRD, human usability, WCAG, live SQL Server or operational acceptance.
The bulk UI is unchanged. The directly dependent upload/offer/accept forms
were changed and exercised in local Chromium as described below; no general
UI/WCAG or user-acceptance claim is implied.

### Upload and handoff explicit change metadata (correction TWO)

`POST /api/cases/{id}/upload` now requires `source`, `source_version`, `reason`
in addition to existing `name`, `kind` and base64 `data`. For example:

```json
{
  "name": "survey.txt",
  "kind": "Survey",
  "data": "U3ludGhldGljIGV2aWRlbmNl",
  "source": "SYN supplied survey register",
  "source_version": "register revision 7",
  "reason": "Add the supplied survey evidence"
}
```

`offer-handoff`, legacy `handover`, and `accept-handoff` require the same
three source strings plus `handoff_version`, the current number of
`handoff_history` events in case detail (zero if absent). Acceptance example:

```json
{
  "source": "SYN handoff request register",
  "source_version": "request revision 2",
  "reason": "Take responsibility for the documented next action",
  "handoff_version": 1
}
```

Use the actual current history count, not the example value. Source/version/
reason must be nonblank strings at most 200/100/300 characters. Missing old
payload metadata now returns 400 with the field and fix; stale handoff returns
409/reload; wrong recipient or revoked actor returns 403. Requests cannot
override server actor/time/change-version/old-new fields. These inputs assert
what the person checked, not source authority or an approval. The file hash
and server change version never substitute for supplied source version.

Upload returns ordinary case detail with document source fields and
`document_history`. Offer/accept return enriched `handoff_history`. Each
complete event binds exact old/new references/ownership and registered
actor/UTC time/version and is identically retained in append-only audit,
transactionally with case changes in SQL. No accepted field, finance/safety/
consent/quality approval, contractor instruction or bulk owner change is added.
Older history is not rewritten; absent metadata displays Unknown (legacy).
Roles without note visibility do not gain source/reason/change access.

Existing native/Fluent-token upload/offer/accept UI now collects these fields,
supports Enter submission and browser required-field validation, retains input
on errors with a focusable polite inline message, and disables only during a
save. Named recipient must still accept. Do not retry blindly after a storage
failure: reload history to check an uncertain commit first.

Local synthetic browser reproduction, using the already-installed Playwright:

```bash
PYTHONPATH=src/api:src/core/tests:src/agents/tests \
  .venv/bin/python src/api/checks/provenance_browser_check.py
```

The check creates responsive loopback HTTP and temporary SQLite fixtures,
blocks external requests, exercises missing-field focus and keyboard upload/
offer/accept, stale inline refusal/input retention, recipient ownership,
390px reflow/reduced motion and event/audit equality after reopen. No private
stock, inference, live platform, actual template authority or WCAG/screen-reader
conformance is claimed.

## Regulatory evaluation and card cadence labels (#216)

`GET /api/law/cards` and `GET /api/law/cards/{card_id}` add a read-only
`source_freshness` object to every returned card/version. It includes
`status` (`in_cadence`, `out_of_cadence`, `unknown`), plain-language `label`,
`as_of` and per-source monitoring evidence. The same object accompanies
bounded regulatory chat cards; the panel renders the card link, text label
and historical as-of date without a colour-only signal. Older stored turns
without the field explicitly show unknown cadence.

Retained versions in storage do not acquire this read-only field. The lifecycle
HTTP regression compares the complete decorated history before/after reopening
and every retained storage field after removing only the additive decoration.
A loaded law store with no sources returns draft cards with unknown cadence
and role-visible unknown checks, without publishing alerts. An unavailable law
store instead returns 503/unknown for check/alert requests. Post-commit safety
intake logs the unavailable-store exception and returns
`rule_checks.status: unknown` with the human safety route; saved work is not rolled back. That
diagnostic is not an uncaught test error or evidence that a rule passed.

Cadence is measured from a successful configured source-monitor observation,
not a retrieval timestamp or inferred legal commencement. Missing evidence is
unknown; known overdue evidence remains labelled even if another source is
unknown. An overdue label does not approve, retire or disable a rule, resolve
a source conflict or suppress an independent hazard alert. Cards retain all
existing source/version/approval gates. This is not a live-currentness claim.

The [per-check evaluation audit](../agents/README.md#regulatory-evaluation-gates-216)
records exact citation/refusal development grading, critical hazard omissions,
a generated stateless 60,000-home baseline, and explicit human/continuing-stock
gaps. There is no overall pass. With no measured staff comparison, the report
recommends cards-only shipment. Existing chat remains disabled by default and
available only under its explicit synthetic-development admission; this change
does not approve operational chat or activate a release.

Local validation starts a responsive loopback app on an ephemeral port using
temporary synthetic SQLite data, checks health, authenticates fixture staff,
reads collection/history labels and a cited turn, and proves retained alerts
unchanged. Outbound inference is forbidden by the harness:

```bash
PYTHONPATH="$PWD/src/api/tests:$PWD/src/core/tests:$PWD/src/agents/tests" \
  python3 -m unittest test_regulatory_chat_api test_rule_alerts -q
```

Human comprehension/accessibility, actual staff classifications and
acknowledgements, live Azure SQL and continuing-stock acceptance are not
established by these checks. No Azure changes or private data are required.

## Home-specific cited chat, offline synthetic slice (#214)

The existing home/case chat panel contains an optional cited regulatory lookup.
It is hidden unless the [core synthetic admission contract](../core/README.md#synthetic-home-specific-cited-chat-214)
passes. It supports hazard and automated-decision source lookup, restores owned
historical turns, shows provision/fact IDs with status and dates, and exposes a
one-action doubt button. Excerpts remain quotes, never an assessment that law
applies or a duty is satisfied. No model is called, even if ordinary Foundry
credentials are configured. The API retrieves; the agents library renders a
fixed five-part answer. No sixth assistant or live AI task is activated.

| Method and path | Contract |
| --- | --- |
| `GET /api/chat/regulatory/status` | Synthetic admission, free-text warning and metadata-only own-role retention review; 403 when disabled or unauthorized |
| `POST /api/chat/regulatory/threads` | `{"case_id":"ZF-1"}`; owned thread bound to that home/case |
| `GET /api/chat/regulatory/threads/{id}` | Owner-only historical messages, source snapshots and current role/case checks |
| `POST /api/chat/regulatory/threads/{id}/ask` | `{"content":"What do the hazard sources say for this home?"}`; exact source/fact answer or explicit refusal |
| `POST /api/chat/regulatory/threads/{id}/doubt` | `{"turn":2}`; atomically copy that stored question/answer pair into the named exercise owner's isolated inbox |
| `GET /api/chat/regulatory/inbox` | Juan Manuel Servera's provisioned exercise principal only; no access to senders' threads or memory |

No client owner, role, facts, model, source version or date overrides are
accepted. Generic chat ask/messages/proposals cannot bypass this bounded path.
Generic history uses the same regulatory guard. Missing/ambiguous named owner
or an invalid pair returns 400; role/field refusal 403; foreign/missing thread
or case 404; a concurrent/archive conflict 409. Unexpected failures log an
explicit 503 and warn that a turn/receipt may already be durable; reload before
retrying. A successful doubt response means a local exercise inbox copy, not
email delivery, actual human review or legal approval. The named recipient
must already be uniquely provisioned in the synthetic staff register; the
application does not create an account or invent an operational delegation.

The panel offers the named owner's inbox and current case's copied turns.
Copies remain separately owned/deletable under existing chat storage; sender
deletion does not retract a copy already explicitly sent. Operational retention,
rights handling and actual staff use remain unapproved. Ordinary case workflow,
human safety routes, deterministic cards and rule-engine alerts stay independent.

### Acceptance audit (2026-10-16)

Issue checkboxes are deliberately untouched; the coordinator owns merge-time
updates. "Pass" below means observed bounded offline engineering evidence,
not full ADR 0005 adoption or operational acceptance.

| #214 criterion | Offline result and evidence | Remaining unmet boundary |
| --- | --- | --- |
| Every statement cites a provision/fact with status/dates; unsupported dropped | Pass for exact excerpt/fact fragments: `test_every_fragment_is_exact_and_cited`, snapshot/hash and size tests. Unsupported questions return no factual fragments | No generated-prose claim validation or actual-model evaluation; unknown effective dates stay null |
| Role-scoped categories and question minimisation | Pass: core minimisation tests, API revocation and foreign-thread denial; fresh SQL staff read. No health/contact/free-text/memory retrieval | Purpose coverage limited to two source lookups; actual company field/purpose ratification unmet |
| No legal conclusions/advice, future law active or inferred terms | Pass for closed output surface and frozen refusal cases; source-gate and interpretation tests | Partial for arbitrary legal-intent recognition: lexical classifier is not general semantic understanding. Live legal/source approval unmet |
| Conflicting sources both shown and escalated | Partial: changed approved versions and disagreeing same-purpose cards show both, no winner, `requires_human`; explicit doubt route works | Arbitrary semantic contradictions cannot be detected. Actual human resolution not performed; no automatic private-content sharing |
| One-action doubt to named owner | Pass locally: atomic selected-pair copy, idempotent receipt, missing owner denial, role recheck, rollback/reopen and owner-only HTTP inbox tests | No live notification or human acknowledgement; actual delegation/provisioning unmet |
| Retrieved text is data, with injection tests | Pass structurally: malicious source text is an inert quote; zero provider/tool calls, safe DOM and no controlled writes | No actual-model injection test or general model-safety claim |
| Model-negative never suppresses rule-engine alert | Pass for offline negative/unavailable-answer dataflow: retained alerts and safety hold equality in `test_card_conflict_and_no_rule_alert_suppression` | No actual model-negative provider run; this path has no model or rule write capability |
| Turns stored with sources | Pass in JSON/SQLite: full versioned envelope, evidence IDs, immutable historical snapshots, restart and isolated handoff tests | Azure SQL execution, approved retention/privacy and continuing-stock acceptance not run |

The [frozen evaluation](../agents/evals/regulatory_chat_results.json) records
3/3 exact cited answers and 10/10 expected refusals. The test comparator uses
the same deterministic cards with actual provision links: six joined permitted
home facts across three answers versus none in cards alone, with three
structural card/provision/home lookups versus one joined request. This is
bounded offline lookup value only, not measured staff effort or AI superiority.
Real inference, held-out evaluation, staff comprehension, live approval,
60,000-home stock and Azure acceptance remain unmet and are not disguised by
passing local tests.

Install the editable core/agents/API packages and declared development tools
with pip. From the repository root:

```bash
PYTHONPATH="$PWD/src/api/tests:$PWD/src/core/tests:$PWD/src/agents/tests" \
  python3 -m unittest test_regulatory_chat_api test_regulatory_chat \
  test_regulatory_answers -q
```

The HTTP harness starts a loopback application on an ephemeral port over only
temporary synthetic SQL data, checks health/case responsiveness, exercises the
actual cited routes, historical reads and explicit owner handoff, forbids
outbound inference, then stops the server. Browser interaction and human
accessibility/comprehension are not established by HTTP/static DOM tests.

## Regulatory security, privacy and audit (#217)

On trusted-proxy ingress, all regulatory endpoints require the separate
`ZavaForward.RegulatoryChat` capability in addition to a permitted staff role.
RuleAuthor and RuleOwner do not imply chat access. Capabilities require a unique
provisioned principal binding; email fallback cannot grant them. Generic history,
archive and delete routes enforce the same capability for regulatory threads;
thread lists omit them when it is absent. Existing owner/role/home isolation
remains. The claim-derived staff role cannot regain hazard facts from a wider
register role. Local password mode remains a synthetic development convenience,
not evidence of Entra authentication or operational segregation.

The regulatory panel displays the existing special-category/free-text warning
and unknown or simulated retention. Status returns `privacy` with draft DPIA
state, `dpo_reviewed=false`, `deletion_enabled=false`, own-role regulatory thread
IDs/counts and unknown per-class law/card/check/alert/audit periods. Simulated
CHAT_RETENTION settings list review-due ages only; they are not a purge or an
approved schedule. Both archived sender threads and separately owned referral
copies require DPO retention/rights/hold alignment.

| #217 acceptance criterion | Evidence and honest disposition |
| --- | --- |
| DPIA with DPO completed before live data use | Unmet. [Draft for Juan Manuel Servera's DPO review](../../docs/reference/research/chat-memory-dpia.md#regulatory-assistant-dpia-draft-for-dpo-review-2026-10-16-refs-217), no completed consultation/sign-off or live-data permission |
| Chat/check retention with DPO-set periods | Unmet. Existing chat settings reused for metadata-only simulated review; all real periods, check/alert disposal, holds, backups and immutable history alignment require DPO review |
| Minimum Foundry fields and special-category purpose controls | Partial. Existing offline retrieval excludes health, contact, narrative, memory and unrelated home fields; role/purpose tests pass and no provider is called. No regulatory Foundry query or actual-provider privacy evidence exists |
| Separate Entra author, approver and chat roles | Partial. Distinct capability mapping, registration/script parity, no-self-approval and HTTP denials pass locally. Actual tenant assignments, ingress and revocation not tested or applied |
| Rule changes, approvals, checks, alerts and turns audit-logged | Locally demonstrated with append-only rule/check/alert events and transactional SQL turn/referral metadata audit; failure rollback, restart, idempotency and chain checks pass. Azure SQL/ledger archive evidence not collected; JSON separate-file atomicity remains unsupported |
| Prompt-injection and cross-role disclosure tests pass | Met for this offline synthetic slice: injected question/source containment, no controlled writes, no health-canary disclosure, current claim role versus register, capability denial on direct/generic routes, foreign threads and role-change denial. No actual-model adversarial or production assurance |
| Art 22A to 22C proposal/flag-only, named human and reasons | Partial. No chat decision-write path; version-2 significant-decision check requires explicit reasons beyond an evidence ID. Actual human authority/reasons/contestability and legal assessment remain unverified; no statutory compliance claim |

Issue checkboxes remain unchanged for the merge coordinator. ADR 0005 acceptance
permits synthetic development only. This slice uses no actual staff/resident
data, Azure changes or model calls and claims no operational approval.

With installed projects and tools, run from the repository root:

```bash
PYTHONPATH="$PWD/src/api/tests:$PWD/src/core/tests:$PWD/src/agents/tests" \
  python3 -m unittest test_regulatory_chat_api test_auth test_rule_alerts \
  test_regulatory_chat test_regulatory_privacy test_rule_engine test_rulecards \
  test_chat_privacy test_chatthreads test_regulatory_answers -q
PYTHONPATH="$PWD/infra/tests" python3 -m unittest test_identity_rbac -q
```
No Azure resources or private data are required or accessed.

## Rule-card approval API (#211)

The existing law store now exposes exercise rule cards, without an AI call or
approval tool for agents. Configure the existing `ZF_LAW_DB`/`ZF_LAW_BLOBS` local
test doubles or `ZF_LAW_STORE=mssql` deployment backend. Startup retains two
labelled, unassigned draft seed cards. Creating a later assigned-email version
does not approve it or change the seed's retained history.

| Method and path | Contract |
| --- | --- |
| `GET /api/law/cards` | Latest version of each card, with exercise label and approval history |
| `GET /api/law/cards/{card_id}` | Every version and event, plus currently eligible active version |
| `GET /api/law/cards/reviews` | Source-change review records; no automatic interpretation |
| `POST /api/law/cards` | New immutable exercise draft; authenticated rule author required |
| `POST /api/law/cards/{card_id}/{version}/approve` | Named owner, distinct from the version's author |
| `POST /api/law/cards/{card_id}/{version}/activate` | Named owner; version must be approved |
| `POST /api/law/cards/{card_id}/{version}/hold` | Named owner; active card and nonempty `note` required |
| `POST /api/law/cards/{card_id}/{version}/release` | Named owner; held card only |
| `POST /api/law/cards/{card_id}/{version}/retire` | Named owner; approved, active or held card only |

Draft body (synthetic example, replace the owner with a provisioned staff email):

```json
{
  "card_id": "synthetic-example",
  "title": "Exercise human review",
  "trigger": "Synthetic proposed resident decision",
  "applicability": "Synthetic exercise only",
  "provisions": ["Illustrative citation, requires owner verification"],
  "clock": "No operational duration approved",
  "safe_default": "Route to the human review queue",
  "escalation_role": "Named exercise owner",
  "approver": "owner@example.test",
  "effective": "2026-10-16",
  "retirement": null
}
```

Other POST bodies are `{}`, except hold: `{"note":"Exercise source doubt"}`.
Actor, author, role, event date and exercise status are server-derived; attempts
to supply those fields are rejected. Dates must be canonical ISO dates, with
retirement after effective date. Domain/state denials return 409, malformed HTTP
fields 400, insufficient capability 403, absent authentication 401 and an
unconfigured law store 503. Unknown card history/routes return 404.

All reads require an existing staff law-view role; contractors/unknown roles are
denied. All writes additionally require the trusted-proxy provider and dedicated
Entra claims `ZavaForward.RuleAuthor` or `ZavaForward.RuleOwner`, respectively.
These reserved capabilities cannot supply a workbench role themselves, even
through `ZF_ROLE_MAP`. They are derived only after one unique tenant/object-ID
match to provisioned staff. Email fallback still permits existing workbench
login but never rule authority. Password sessions and staff-file `rule_roles`
cannot grant write authority. Existing `X-ZF-CSRF: 1` protection applies.
The canonical provisioned email is retained, not a claimed email or display name.
Having both capabilities never permits self-approval.

These are code-level contracts, not tenant role assignments or legal delegation.
The ingress must validate principals and prevent direct access; local synthetic
principal tests do not verify signatures or hosted ingress. Legal/Compliance/DPO
owner nomination in #209 is not approval of any card. Approval events remain
explicitly simulated, and non-exercise cards remain refused. Legacy display-name
events are preserved verbatim and do not confer new email-bound authority.
A rule-card UI, real card/legal approvals, real tenant assignments and SQL
Server/Azure acceptance are not delivered by this slice. The bounded exercise
engine integration in #212 is described below; it supplies no missing approval.
The current infrastructure registration script/manifest defines only workbench
roles; adding and assigning the two dedicated rule capabilities is still an
explicit administrator deployment follow-up, not an implicit role grant.

The local app exercise in `tests/test_auth.py:RuleHttpTests` starts a loopback
HTTP server over temporary synthetic data, checks health and app responses,
executes the lifecycle and deny matrix, reopens persistence, then stops the
server and removes its temporary files. Run it from `src/api`:

```bash
PYTHONPATH="$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests" \
  python3 -m unittest tests.test_auth.RuleHttpTests -q
```

## Deterministic step-alert API (#212)

The API composes the [bounded core engine](../core/README.md#deterministic-checks-and-alerts-212)
over the existing SQL case store and law SQL adapter. JSON-only case stores
cannot execute checks. There are no new approvals in delivered data: seeds stay
unapproved exercise drafts, and prose-only cards cannot execute a guessed clock.
An author may add the optional `check` contract documented in core when
proposing a new version; the existing human approval lifecycle still applies.

| Method and path | Contract |
| --- | --- |
| `GET /api/law/alerts?case={case_id}` | Role-scoped open alerts, grouped per home, ordered by due time and harm; omit `case` for the role's cross-home view. Includes owner-classified false-positive counts/rate and unclassified denominator. |
| `POST /api/law/checks/{case_id}` | Empty object only. Recheck persisted SQL facts with a server-derived data trigger; return only checks in the caller's alert audience. No supplied facts, clock, awareness date, owner or suppression. |
| `POST /api/law/alerts/{alert_id}/acknowledge` | Exact named owner and trusted rule-owner capability; body `{"note":"Human acknowledgement evidence"}`. |
| `POST /api/law/alerts/{alert_id}/outcome` | Same authority, with human action/outcome evidence in `note`; breach risk must already be acknowledged. |
| `POST /api/law/alerts/{alert_id}/false_positive` | Same authority; retained classification evidence only, never suppression or risk resolution. |
| `POST /api/law/alerts/{alert_id}/confirmed` | Same authority; alternative retained classification. |

Hazard audiences are Building Safety Liaison, Resident Liaison Officer and
Retrofit Programme Manager. Decision-safeguard audiences are Retrofit
Coordinator and Retrofit Programme Manager. The exact named owner may also
read their alerts, subject to an authenticated supported staff role.
Contractors and unknown roles cannot access either checks or alerts.
Existing case authorization is rechecked for case-specific routes; all
currently supported staff have case-read scope. Field-need projection also
withholds disposition notes from roles without that need. No raw hazard notes,
resident details or proposal text are included in check evidence pointers.
Guessed alert IDs or unrelated owners are denied. Password sessions cannot
acknowledge, close or classify alerts. All authority and disposition timestamps
are server-derived; attempted overrides are rejected.

Successful ordinary case mutations trigger a check after commit, using
`step_transition` if the journey stage changed and `data_change` otherwise.
Package/work-order, import and early-return AI/document routes are covered on
the next scheduled SQL sweep, not synchronously by those endpoints. The core
CLI is the bounded schedule entry point; no hosted timer is configured here.
Data-trigger retries retain the original checkpoint time; a fresh scheduled
minute is required to advance an unchanged clock.

Alerts contain the safe action, named decision owner, clock/due time if
applicable, exact citation/status, original evaluation time, current-control
availability, and latest check result/time. This is not an independently
refreshed compliance certificate. Advisory alerts disappear when a newer check
is clear or the control is inactive. An unresolved breach stays visible and
requires its owner outcome even if later checks change. No disposition releases
a safety hold or sends a resident message.

Unconfigured or failed engines return 503/unknown on alert service requests.
For committed case work, `rule_checks.status: unknown` and the manual safety
route are included in the successful case response, and the failure is logged;
no successful or fresh persisted check is invented. Emergency reporting,
referral, receipt, acceptance and independent human hazard work do not depend
on engine availability. Continue the existing human emergency/hazard service,
never wait for an alert, AI or a legal interpretation.

Local core/API tests establish these bounded contracts, not live-platform
acceptance. Alerts are API/step metadata only: no workbench alert UI, production
timer, source/card legal approval, tenant capability assignment, staff
comprehension/precision trial or continuing-stock Azure/SQL Server acceptance
is delivered. The decision-safeguard evidence contract has no general-purpose
writer in this slice; absent evidence remains unknown. Refs #212 remains open.

## Stock reconciliation API (#84)

`POST /api/cases/{id}/stock-reconciliation` records an unresolved staff query:

```json
{
  "field": "epc",
  "query_owner": "sam@example.test",
  "left": {
    "value": "D",
    "source_id": "SYN-REGISTER-84",
    "date": "2026-01-01",
    "version": "1",
    "validation_state": "Unvalidated"
  },
  "right": {
    "value": "E",
    "source_id": "SYN-SURVEY-84",
    "date": "2026-02-01",
    "version": "2",
    "validation_state": "Disputed"
  }
}
```

The example is constructed, not a real home. Allowed fields are `epc`, `type`
and `built`; the owner must be registered non-contractor staff. Each assertion
needs exactly the shown fields; validation is `Unvalidated`, `Validated`,
`Disputed` or `Unknown`. Dates cannot be future; EPC is A-G, build year an
integer and home type bounded text. Equal values and identical source/version
pairs are rejected. The authenticated session supplies recorder identity.
Invalid inputs return 400, unauthenticated requests 401, denied roles/bulk
requests 403. The response is the projected case detail; contractors receive
neither comparisons nor technical decisions.

Opening additionally requires the registered case owner or programme/manager
role. Staff role membership alone does not grant responsibility for every case.

`POST /api/cases/{id}/stock-query-event` appends a disposition:

```json
{
  "query_id": "SQ-1",
  "action": "withdraw",
  "reason": "Duplicate of another recorded query"
}
```

The original raiser or a programme/manager role may withdraw. For a human
reconciliation attestation use `"action": "resolve"` and add a nonempty
`"evidence": "SYN-HUMAN-REVIEW-84"` reference. Resolution is restricted to
registered named humans with the existing Retrofit Programme Manager or
Programme Support Officer role. The server binds identity from the session,
not the body; agents cannot resolve or sign off. Every disposition needs a
reason, refers to a query on this case and is terminal. Invalid/repeated
dispositions return 400; unauthorized requests return 403.

The response derives each query's current `Unresolved`, `Withdrawn` or
`Reconciled` status and retains the separate `stock_reconciliation_events`
history (event ID, query ID, status, action, reason, optional evidence,
timestamp and recorder identity). The original comparison remains unchanged
in storage. The read-only panel shows the status and human event provenance.
Only unresolved queries block technical approval; disposition never releases
other stock, safety, building or independent approval gates. No source or
home field is automatically selected/updated. Source-authority, resolution
rules and eligibility stay Unknown/owner-approval-needed, not an approved
operational reconciliation policy.

Stock and technical writes also recheck the current SQL staff identity/role/OID,
even for an existing authenticated session whose cached staff record is stale.
Changed or removed identities receive 403; their old session cannot retain
approval authority. The writer transaction revalidates before commit. A known
precommit SQL failure leaves neither a new case version nor its success audit;
the original error propagates, with recovery uncertainty explicitly reported.
No new endpoint, role grant or sign-off competence attestation is introduced.
Original Review, 2026-10-17: **Not accepted**, RV-001. Authorized correction ONE
clears failed pending work before recovery reads and restores known cache
snapshots; early/persistent read failures now preserve the original error and
cannot flush the failed success event on exit or a later save. A failed reload
logs uncertainty and forces retry on the next operation, not a success fallback.
Bounded independent verification closes RV-001 for this correction after 91
focused tests and two snapshot probes; the original adverse Review is retained.

The case view displays both values, source metadata and query owner, with
authority/resolution/eligibility explicitly `Unknown`. A different case shows
its own comparisons, never a carried-over rationale. Existing technical forms
record named human decisions, not AI approval; separate sign-offs show the
design version each person reviewed. Conflict, building and hazard holds reuse
the [core controls](../core/README.md#stock-comparisons-and-human-technical-sign-offs-84).
No stock source wins automatically, no resident decision is inferred and no
case is silently excluded or automatically reprioritised.

Support status and input coverage are explicit in staff detail/list. Missing
flags are `Unknown`, not `"None"`; compatibility Boolean notice indicators
still represent observed support only. Existing governed AI proposal paths
remain available, with release admission and human approval unchanged.

Local synthetic HTTP tests run from `src/api`:

```bash
PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_stock_reconciliation_api.py' -v
ZF_STOCK_BROWSER=1 PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_stock_reconciliation_api.py' -v
```

The second command requires the existing development Playwright dependency
and Chromium. It runs the real loopback application with synthetic SQL state,
checks rendered values, source metadata, owner, Unknown labels, heading/keyboard
access and navigation to another case. The default unit suite skips that
opt-in browser method. This is engineering evidence, not direct human
accessibility/competence acceptance, live inference, SQL Server or Azure proof.

The selected changed-path local SQL Server parity suite is separate from
browser evidence. In a throwaway local SQL Server database only, using the
existing `ZF_TEST_MSSQL=1` and localhost `ZF_SQL_*` settings:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_mssqlstore.MssqlStockDecisions -v
```

Initially eight tests passed on 2026-10-17; correction ONE passed ten, reusing canonical constructed core cases for
comparison/disposition and four sign-off success, current actor denial,
second-connection authority change, transactional case/audit failures,
reopen/no delayed audit and context cleanup. Added early/persistent actual
recovery-read failures exercise technical/comparison/terminal paths, original
error, empty pending state, released locks, failed retry and later recovery.
Transactional refusal errors retain their original identity on reload failure.
This is local SQL Server adapter
evidence, not Azure/Entra acceptance or approved professional/source authority.
Source-authority/resolution/eligibility rules, operational delegation and
real-platform acceptance remain unmet; nomination/tenure routing is separate.

A working case-management application for the Zava Forward retrofit programme.
It follows the simplicity requirements SA-001 to SA-010 in the
[PRD](../../docs/prds/zava-forward-retrofit-programme-demonstrator.md) and the
[prototype learnings review](../../docs/reference/research/ux/prototype-learnings-and-simplicity-review.md).

This file is the former `mvp/README.md` (ADR 0006, issue #199, M6), split by owning project. It keeps
the staff-facing behaviour, configuration, sign-in, local run, honest limits and container checks of
the `api` project. Domain modules are documented in [core](../core/README.md) (law store, rule cards,
SQL stores, governance, ledger, chat storage, continuity and synthetic tools), the ledger digest job in
[orchestrator](../orchestrator/README.md), and the assistants, AI evaluation harness and dated
assistant validation record in [agents](../agents/README.md). The index of projects is
[src/README.md](../README.md).

Paths such as `tests/test_x.py` and `web/` below are relative to `src/api/` unless a `src/` path is
given. Module names without a path (`store`, `ranking`, `projection`, `quality`, `procurement`,
`finance`, `documents` and so on) are `zava_forward.core.<module>` in `src/core/src/zava_forward/core/`.
Run the suites from `src/api` with
`PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests`, after
`pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`. When `ZF_DATA` is not
set, the data file defaults to `~/.zava-forward/data/zavaforward.json`, outside
the checkout. `ZF_DATA` accepts an explicit JSON file or a data directory;
an explicit filename is preserved. Runtime and generator resolve the same folder.

## Resident decisions and representative API (#86)

The resident panel records only supplied human decisions. Answer and answered-by
selectors start blank; the displayed default is `Not recorded`. The historical
case-wide answer is labelled as history, with no consent editor; its legacy
`decision` endpoint remains role-checked history only and cannot release work.
First record a technical design, then the exact measure scope and source.
The [core contract](../core/README.md#resident-decisions-and-representatives-86)
defines currentness, authority, release dependencies and evidence limits.

Authenticated resident-workflow staff use `POST /api/cases/{id}/resident`:

For decision/scope/authority/safe-contact recording and disclosure checks,
only registered named Liaison Officers (Neighbourhood/Resident Engagement) and
Retrofit Coordinators may write. Managers and Programme Support view only;
their attempts, including the legacy `decision` route, return 403. Existing
complaint/redress actions retain separate named-owner restrictions. The panel
uses server-projected `can_record_resident`, rather than treating every manager
as a resident recorder. Other staff do not receive private evidence narratives.
Contractor detail contains `resident_readiness: [{"measure": "...", "flag":
"Proceed"}]` (or `Hold`), never decision reasons, wishes, authority or safe routes.
Unrelated vulnerability restrictions remain unchanged for staff.

Staff detail includes `resident_retention`: five calendar years from first
recorded resident contact, including withdrawal and expired authority. Unknown
first-contact history is explicit. `GET /api/retention` includes due
`doc_id: "resident-decisions"` entries for manager review. A manager posts
`{"id": "resident-decisions"}` to `/api/cases/{id}/retention-approve` to remove
the current resident payload; legal hold returns 403, not-yet-due or unknown
origin returns 400. At expiry, work and representative disclosure reliance hold
even before deletion. See the [core retention contract](../core/README.md#resident-decisions-and-representatives-86)
for the exact deletion inventory and ledger/backups/cross-case limitations.

| `action` | Required input and control |
| --- | --- |
| `scope_record` | `measure`, `scope`, integer current `design_version`, `source`; creates a new context revision and no answer |
| `decision_record` | `measure`, integer `context_revision`, supplied `status`, `answered_by`, `source`; `note` for decline/pause/withdrawal; `representative_ref` for representative; `review_ref` when accepting after a review flag |
| `safe_contact_record` | Resident-confirmed `safe_contact_ref`, supplied `source`; increments contact history, does not send anything |
| `representative_record` | `representative_ref`, `measure`, integer `context_revision`, `status`, `tasks`, `source`, `authority_date`, `review_date`, `resident_wishes`, current `safe_contact_ref`; appends authority version |
| `disclosure_check` | `representative_ref`, `measure`, integer `context_revision`, `task`; checks current task authority only, sends nothing |
| `service_open` | Existing service fields (route, summary, desired outcome, handler/redress owners, next update); `Independent review` also needs `review_measure`, integer `review_decision_version`, `review_reference` |
| `service_update`, `service_close` | Existing request ID/status/update/outcome; independent review is update/close-only for its named independent reviewer |

Answer statuses: Waiting, Accepted, Declined, Paused, Withdrawn. Authority
statuses: Confirmed, Unclear, Disputed, Revoked. Tasks: Receive information,
Communicate, Attend, Works decision. Review and authority dates use YYYY-MM-DD;
authority cannot start in the future, review follows evidence, and reliance
stops on the review date. The UI records one task per authority version; the API
supports a list of evidenced tasks. Register separate task/scope authority
references when multiple active authorities are needed; latest version of each
reference is authoritative, never the most recent representative globally.

The API ignores forged recorder/actor fields. Missing/stale/invalid context,
source or authority returns 400, wrong staff/reviewer role returns 403, and
blocked controlled release returns 409. `disclosure_check` is not a send token:
no downstream transport consumes it and no message is sent. Legacy
representative-addressed templates remain refused; authorized staff AI
proposals are non-addressed drafts and still require human review.

Work-order issue/reissue/correction requires `resident_bindings`, for example:

```json
{"resident_bindings": [{"measure": "Loft insulation", "context_revision": 1}]}
```

The manager UI accepts `Measure|revision; Measure|revision`, with no inferred
binding from free-text scope. Booking/completion checks the saved version.
Quality evidence accepts an explicit integer `context_revision`; unbound
evidence can be recorded via the API but cannot be accepted or handed over.
The quality UI asks which scope revision the evidence covers. A withdrawn
sibling cannot block an explicitly independent bound work order or QA record.

Complaints and independent review stay available after pause/closure and AI
failure. They record an owned request, not delivery to the association's formal
complaints service. The panel directs staff to the named officer and accessible
non-digital route without inventing a real complaints URL, response timetable
or delegation. The real route, human independence/accessibility and
without-detriment acceptance remain unproven.

`tests/test_resident_api.py` starts the actual app on loopback with synthetic
staff/home data and SQLite, checking health/static assets, authentication,
decisions/withdrawal, redress, authority/privacy and restart. Core semantic tests
also use a synthetic AI adapter, not live model inference. Real inference,
SQL Server/Azure and human acceptance remain unmet; no private data or new
deployment is used. Docker build/run depends on CI when local daemon access is
denied.

## RAI task release API (#219)

`GET /api/assistants` now includes role-filtered `registered_tasks` for the
merged eleven-task registry: intended/prohibited use, stakeholders, current
`binding`, selected `release` (ID/version/digest), structured `release_denial`
and the explicit OQ-017 authority gap. Existing five-assistant fields remain.
Configured JSON-store AI denies without durable SQL release evidence; use
SQLite locally or Azure SQL for deployment, not a JSON bypass.

`POST /api/assistants/releases` uses the existing authenticated Programme
Manager plus `ZF_ASSIST_RELEASE_APPROVERS` allowlist. Copy the task's current
binding and supply the [core contract](../core/README.md#task-bound-rai-release-records-219)
fields, `task` (assistant ID or `legacy:<retained-task>`), `evidence_class`,
`serving_model`, residual-risk note and future ISO expiry. The server records
the authenticated approver, never a client-supplied approver identity. Posting
a replacement revokes previous active records for that task across endpoints
and deployments; it does not overwrite historical proposals. Suspend/revoke
routes are unchanged; restart requires a newly recorded release.

Denials expose missing evidence, the unappointed authority/project contact and
manual route, and persist in assistant events or the legacy audit/comparison
record. Web draft notes show the denial reason. Superseded priority proposals
are visibly non-actionable; server-side accept/edit checks remain authoritative.
Release does not grant sending, works consent, safety, financial or domain-write
authority. It permits bounded proposals that still require human review.

Local synthetic HTTP exercise (no real AI, Azure or private data):

```bash
cd src/api
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_assistants.ApiTests.test_release_record_local_http -v
```

This starts the real App on an ephemeral loopback port, checks health,
authenticated registry/release/invoke/detail/revoke routes, zero calls while
denied, one nonbillable scripted provider call when released, unapproved output
and unchanged domain state. It shuts down the listener and removes its temporary
synthetic files. Direct human, live model and Azure acceptance are not implied.

## Hazard referral and retrofit hold API (#85)

Authenticated staff use the existing safety panel on open or closed retrofit
records. It labels observations as unverified, shows source/awareness, referral
destination, follow-up owner, whole-home hold scope, separate sent/received/
accepted evidence, external service response/resident-update times and explicit
unknowns. It sends no referral or resident communication itself. Use the
existing hazard service directly for urgent concerns; neither AI nor a
retrofit hold may delay that route.

| Path after `/api/cases/{id}/` | Body and control |
| --- | --- |
| `hazard-raise` | Reported `category`, `priority`, optional `note`, required `source`, timezone-aware `aware_at` not in the future; staff, including closed retrofit records |
| `hazard-refer` | `index`, `to`, external case/job `job`, sending `evidence`; staff; prospective binding for active legacy records |
| `hazard-receive` | `index`, receipt `evidence`; named safety receiver, once |
| `hazard-accept` | `index`, acceptance `evidence`; named safety receiver, after receipt, once |
| `hazard-times` | `index`, external timing `evidence`, at least one of timezone-aware `response_due_at`, `responded_at`, `resident_update_due_at`, `resident_updated_at`; accepting receiver; no overwrite |
| `hazard-repaired` | `index`, external repair `evidence`; accepting receiver; observation only |
| `hazard-release` | `index`, release reason `note`, external supporting `evidence`; independent safety-role actor, after repair evidence; home retrofit hold only |

Missing evidence/invalid state or index returns 400; wrong role/receiver or
non-independent release returns 403. Active holds return 409 on controlled
retrofit progression. No classify, pause-clock, reset-clock or close-hazard API
exists. Server-supplied actors and home scope ignore forged client authority.
All actions are manual, one-case decisions; consent and other home/building
gates stay independent. See the [core contract](../core/README.md#hazard-referral-and-home-retrofit-holds-85).

The listed release-role checks are demonstrator safeguards, not ratified
release authority. Repairs, Safety and Housing owner approval of release
responsibility, response/resident-update timing and escalation policy remains
outstanding (RV-002). Human-recorded due times do not establish an approved
service timetable. These acceptance criteria remain unchecked.

`tests/test_hazard_api.py` runs a real HTTP application on loopback with
fictional staff/home data and SQLite state. It exercises health/static serving,
authenticated closed-record intake, receipt/acceptance/timing/repair/release,
role isolation, legacy binding, restart durability and refusal of cached sessions
after current staff role/OID changes. This is local synthetic
application evidence, not real model inference, verified service transport,
Azure deployment or human/browser acceptance. The canonical
`test_mssqlstore.MssqlHazardReferral` adapter separately exercised actual local
SQL Server durability and transaction-time current caller/destination checks
on 2026-10-17 (16 run, one JSON-only skip), using a task-owned disposable
loopback container and tiny fictional cases. That does not prove Azure or
verified external receipt.
The existing AI release and human-review gates are unchanged; no fallback or
model output can waive a hold. Full #85 acceptance and the mandatory
real-platform application exercise remain unmet without the outstanding
owner/live evidence. Docker image checks are delegated to CI if the local
daemon is inaccessible.

The existing endpoints and screen require no new fields or UI changes for the
current-actor correction. They still record human assertions, not service
commands: no resident message, hazard classification, calculated statutory
clock or external closure occurs. Independent restart identity now compares
recorded normalized email/code/OID, not case-sensitive email alone. SQL refuses
and discards a failed event and its success audit while preserving earlier audit.
If synchronization fails after an acknowledged SQL commit, it reports the
committed outcome and never replays already-committed audit. The one independent
Review's original Not accepted finding is retained; correction ONE has local
regression/actual SQL evidence, not independent final-head closure.
For JSON, a post-save audit failure is explicitly a potentially persisted outcome
requiring reload/reconciliation, not an invitation to retry blindly. See the
[backend evidence boundary](../core/README.md#current-hazard-actor-and-persistence-evidence-2026-10-17).
No new browser run or accessibility acceptance is claimed for this backend-only
change; the Fluent 2/native screen and manual paths are unchanged.

## Design-system foundations (#150)

The [design-system inventory](../../docs/reference/research/ux/design-system.md)
records the owner's Fluent UI (Fluent 2) adoption decision, the sourced token
mapping, seven component states and AI draft-review boundaries. This is a partial
native-foundation/non-colour slice, not a completed Fluent UI runtime migration.
Markers use circle/O, square/W and triangle/! with matching key and status names.
Clusters show home and safety counts (including zero); filter tiles visibly say
"Selected". Overview data tables use named keyboard-scrollable regions on narrow
screens. Existing consent, approval, AI and server authority are unchanged.

From `src/api`, after installing the projects and `.[dev]` with pip:

```bash
python -m playwright install chromium
python -m checks.design_system_browser_check
```

This check starts the real API on a temporary loopback port against 505 fictional
homes from the shared test fixture. Real map APIs exercise point and cluster modes;
only basemap tiles are replaced by a synthetic pixel, so no external tile service
or private dataset is used. It checks rendered tokens, non-colour signals,
keyboard navigation, 320/390/1280px reflow, forced colours and reduced motion.
The source API CI job runs it with pinned Playwright as a development-only
dependency; production requirements/images do not gain a browser dependency.
Human/screen-reader acceptance, full Fluent component integration and live
AI/SQL Server/Azure validation are not established by these local checks.

## Shared workbench information architecture (#152)

`/api/me` includes `navigation` entries with `href`, `label` and `scope`,
computed by the API from existing endpoint/Finance/manager rules. The client
renders these entries without a new role map. Metadata is not authorization:
direct API calls retain all existing server checks. The default remains the
signed-in person's assigned cases, or assigned contractor jobs; programme
directories and overview are explicitly labelled broader scopes. There is no
role simulator. No role-specific screen redesign or new permission is included.

The shell has a keyboard skip link, named navigation, visible/semantic current
destination and a persistent scope/result announcement. Each staff case row has
one case-opening link, plain recorded status and a recorded next action, not an
AI-invented workflow decision. Cases open full screen. Back to the list keeps
the last mine/all scope and filters, but deliberately reloads page one: it does
not promise restored pagination, selected row, scroll position or row focus.
Direct case entry falls back to the own queue.

"Reset my queue" clears search, stage, authority area, wave, owner, flag, work queue, sort
and all-cases override; it restores own cases in the existing safety-first
policy order, focuses the reset control and announces refreshed results.
Obsolete loads/debounce are cancelled on route replacement; failed loads show
an explicit retry, and session expiry returns to sign-in. An empty own queue
is distinguished from no filter matches. Reset does not modify records.
Cancelling a pending briefing invalidates its cached panel so the next queue
requests it again; a completed briefing remains cached. Briefing failures show
an explicit retry. The browser check holds responses across My cases -> All
cases -> My cases and verifies recovery without stale-response replacement.
Safety reports and stopped-work details remain expanded ahead of routine case
forms, with existing named owners, external timings and explicit unknowns.
Contractors retain their minimum-necessary projection, not staff safety data.

The versioned [shared-IA manifest](./checks/workbench-manifest.json) declares
eight implemented auth roles, exact synthetic own queues/navigation and all
eleven PRD perspectives/nine workflows with partial or deferred coverage.
It is not full AC-034/043, accepted role mapping or validated user research.
From `src/api`, using the installed src packages and `.[dev]`:

```bash
python -m checks.workbench_browser_check
python -m checks.design_system_browser_check
```

The second command is the existing CI entry point and runs both browser suites.
Each starts and stops its own healthy loopback API with constructed data in an
automatically cleaned, ignored repository-root `.venv/` scratch subdirectory;
no credentials, model endpoints or private data settings are inherited.
The IA checks cover eight roles, mine/all/reset/back/history, delayed and failed
requests, expiry, contractor projection, queue/case reflow at 320/390/768/1024/
1280 CSS pixels and 200% root text enlargement. This is Chromium engineering
evidence, not browser-zoom, screen-reader or human acceptance. The baseline
also exercises return from a queue with more than 50 rows.

Supported devices/browsers and field/mobile use still need the owner's
decision. The full eleven-profile/nine-workflow journey manifest remains
incomplete. AI routes, real-provider configuration and human review/release
gates are unchanged; the isolated checks make no live model call and do not
satisfy mandatory real-inference/SQL Server/Azure exercise acceptance.
No SQL, deployment, resident consent or controlled approval behavior changed.
Local Docker access was permission denied; image evidence must come from CI.

## Role task queues and shared case context (#76)

### Queue signal completion (#77, 2026-10-17)

The existing Queue definitions disclosure now also defines all five Show only
signals, including extra support, 60-day stage waiting, resident decision and
funding states. Sidebar terms and descriptions stack for readability. Missing
support stays unknown; a waiting signal is not a statutory deadline and no
signal grants consent, funding approval or safety-service authority.

The live workspace status explicitly names the authenticated perspective,
workflow stage, search and own/all-cases scope. The existing Stage filter is
the workflow-stage scope, not a scenario picker or the optional AI "Workflow
only" setting. Stage narrows the chosen own/all scope within existing rights;
it never replaces the authenticated role. No role simulator is added.

Reset consumes both `work_queues.default.view` and its filters/order, keeping
first-page/null-selection, logical focus and result announcements. The current
`work-queues-1` default remains own/urgent. Selecting a case continues to reload
that case's recorded rationale and proposed reviewers; an empty reviewer list
explicitly shows proposed owner Unknown, leaving current ownership unchanged.

The existing `python -m checks.workbench_browser_check` runs the real local
app/API with three constructed cases, discriminating surnames and an alternate
server all/name default. It checks exact rendered IDs/order/scope, reset's
offset=0/no-cursor request, two cases' own rationale/reviewers, unknown reviewer,
expanded definitions at 320/390/1280px and reduced motion. Optional
`ZF_QUEUE_SCREENSHOTS` saves synthetic-only screenshots to a chosen directory.
This is first-page request evidence, not a three-case multipage test.
No real model, private stock, SQL Server or Azure is exercised. Full scenario
workflow coverage, operational definition ratification, human/screen-reader
acceptance and mandatory live-platform application acceptance remain unmet.

This is a bounded offline extension of the existing role workbench, not a new
identity provider, role simulator, permission policy or operational acceptance.
The [parity audit](../../docs/architecture/mvp-to-src-parity-matrix.md#role-task-queue-offline-slice-2026-10-16)
records each issue criterion before and after the change. The authenticated
role still determines access; own/all scope, queue, search and other filters
intersect and never grant rights.

Staff `/api/me` now publishes `work_queues`: version `work-queues-1`, six
definitions, availability/limitations, default filter state and null selection.
The single existing reset consumes that server default, restores own cases in
the existing deterministic order on page one, focuses itself and announces
scope, all filters, version and result count. No case is selected automatically.
No changes to records, ranking, assignments or approvals result from filtering
or reset. No matches and no assigned open cases remain distinct.

`GET /api/cases?queue=new` and `/api/cases.csv?queue=new` use the same filter
before totals, ordering and pagination. Other filters/sorts still apply.
Unknown queue IDs return 400 on both endpoints; an unavailable approved-priority
queue returns an empty result, with its explanation in the visible definitions.
Contractors cannot use staff queues and receive no new context or staff metadata.
Queue selection retains the snapshot-scoped case-ID hot cache; SQL stores load
misses from transactionally maintained indexed membership columns. See the
[60,000-case write-cold/repeat measurements and remaining ranking/refresh costs](../core/README.md#generated-60000-case-queue-timing-327-2026-10-16).
Filtering and reset do not change that authorisation boundary.

| Queue ID | Visible definition and source |
| --- | --- |
| `new` | Current `stage_since` is between zero and seven days old, inclusive. This describes arrival in the current stage, not case creation. |
| `priority` | Open cases under an explicitly approved ranking policy with a named owner. The existing policy is draft, so this queue is unavailable/empty. Accepted AI advice never qualifies as approved programme priority. |
| `stale` | Last supplied EPC record's `documents.at` is older than 30 days, Survey older than 180 days, or a technical sign-off explicitly needs reassessment. Record timestamps are review triggers, not certificate expiry or proof of source validity/currentness. |
| `blocked` | Existing safety, unresolved stock and shared-building stops, plus unmet funding/resident/technical final-check prerequisites. Future-step prerequisites are labelled separately from current stops. |
| `overdue` | An outstanding recorded handoff acceptance, case resident-update or external safety-service response/update deadline is strictly before the snapshot. Each completion is checked independently; accepting a handoff does not complete a resident-update commitment. No deadline is invented from stage age. |
| `unowned` | Handoff Offered, Received or Escalated, with no accepted receiver. A proposed receiver is not a confirmed owner, and the sender keeps chase responsibility. Accepted/Completed/Declined/Withdrawn are excluded. |

Evaluation uses the dataset `as_of`, with date-only values interpreted at UTC
midnight. This reproducible snapshot is displayed, not presented as a live
safety-service clock. Missing, malformed or future observation/record dates
remain Unknown; timezone-less datetime values are Unknown. Future deadlines
are not overdue; equal deadlines become overdue only after the snapshot.
External timing authority remains with the existing hazard and repairs service.
Legacy `noticed` alone cannot establish precise awareness or elapsed hours.

Staff list/detail share the same `work` object: case/current owner, reason,
one next action, origin/evidence/version/snapshot, blocker step/reason/named
owner/responsible role/action, separate handoff owners, evidence-review status,
outstanding deadlines and recorded hazard-clock observations. Safety/stock/
building stops take precedence over a pending handoff, current-stage return
or final-check prerequisite. A role-only responsibility keeps named owner
Unknown; no person is assigned by inference. Missing next action prompts
the case owner to record it rather than fabricating a workflow instruction.

The case, current-context part of history, proposed-reviewer panel and
"Task sources" disclosure reuse this same object. Historical events retain
their event-time owner/reason; context refresh never rewrites those events.
Case switching cancels obsolete loads and binds the displayed context to the
selected case. Domain source comparisons and sign-off records remain intact.
Human-written reason/action/source aliases follow existing need-to-know rules
before serialization, including derived list/status fields; this does not
approve the operational role/redaction matrix.

The new core semantics/store tests and real loopback SQLite HTTP tests use
constructed data, exact threshold/lifecycle expectations and 120 interleaved
matching/nonmatching cases to verify pre-page filtering, cursor totals/order,
sorting and CSV agreement. The extended existing Playwright check exercises
the actual local app, all eight implemented roles, visible definitions,
queue membership, current-context agreement, case switching, delayed responses,
all-filter reset, focus/status and responsive layout. An alternate server
default proves reset is not hardcoded in the browser.

From the repository root, with `/tmp/zf164` already containing the project
development dependencies (pip only), for targeted checks:

```bash
ROOT="$PWD"
BASE="$ROOT/src/core/src:$ROOT/src/agents/src:$ROOT/src/api/src"
(cd src/core && PYTHONPATH="$ROOT/src/core/tests:$BASE" /tmp/zf164/bin/python -m unittest discover -s tests -p 'test_taskqueues.py' -v)
(cd src/api && PYTHONPATH="$ROOT/src/api/tests:$ROOT/src/core/tests:$ROOT/src/agents/tests:$BASE" /tmp/zf164/bin/python -m unittest discover -s tests -p 'test_task_queue_api.py' -v)
(cd src/api && PYTHONPATH="$BASE" /tmp/zf164/bin/python -m checks.workbench_browser_check)
```

Operational queue-definition ratification, named ranking-policy approval and
OQ-005/OD-14/OD-19 role/field/redaction/delegation decisions remain open.
These engineering checks do not establish direct human accessibility/usability,
real AI, SQL Server, Azure deployment or complete eleven-profile/nine-workflow
acceptance. Refs #76; the issue is not closed by this slice.

## Return and handoff API (#83)

All mutations below are authenticated, one-case human actions. The server
supplies authority and receiving/current owner; client-supplied authority or
owner fields cannot override them. Source references are human-recorded text,
not automatically verified evidence.

| Path after `/api/cases/{id}/` | Body and control |
| --- | --- |
| `return` | `to_stage`, `reason`, `source`, `next_action`; authorised staff, earlier stage only |
| `reopen` | `reason`, `source`, `next_action`; manager, closed case only |
| `offer-handoff` | `to`, required `source`, `source_version`, `reason`, current `handoff_version`; optional `note`, `urgency` (Routine/Urgent), timezone-aware `due_at`, `next_action`, `resident_update_to`, `resident_update_due_at`; owner or manager |
| `receive-handoff` | Empty object; named receiver, Sent only; not acceptance |
| `accept-handoff` | Required `source`, `source_version`, `reason`, current `handoff_version`; named receiver only, Sent/Received/Escalated |
| `decline-handoff` | `reason`; named receiver, Sent/Received/Escalated |
| `withdraw-handoff` | Empty object; sender or manager, Sent/Received/Escalated |
| `escalate-handoff` | `to` (manager email), `reason`; sender or manager, Sent/Received |
| `complete-handoff` | `note`; accepting current owner, Accepted only |
| `handover` | Legacy alias for an offer with the same required source/version/reason/handoff-version metadata; never immediate reassignment |

`GET /api/handoffs` returns unaccepted work visible to the sender, receiver and
managers, including canonical `status` and separately labelled responsibility
fields. Persisted `state` keeps Offered/Declined compatibility; detail returns
versioned `returns` and `handoff_history`. Unauthorized or replayed transitions
return an explicit error without a transition. New return/reopen requests
without source/next action now fail with HTTP 400.

BG-010's approved-time escalation criterion stays unmet: due dates are
human-selected and escalation is manual; OD-09 policy and operational acceptance
are not available. No timer, automatic resident contact, live model effectiveness,
SQL Server result or Azure deployment is claimed by local synthetic tests.
AI assistance remains available under its existing configuration/release/human
review gates; this deterministic workflow adds no model authority.

## Building shared context (issue #75)

Staff can follow an explicitly linked home to `#/building/{building_id}` and
back to either linked home. `GET /api/buildings/{building_id}` returns the
[core source-backed model](../core/README.md#building-shared-context-issue-75),
with separate systems, dependencies, stopped-work reasons, works and shared
costs. Missing/unknown data is labelled, not interpreted as an approval.
Linked homes expose only their case ID, stage and closed flag in this view,
not resident details, home evidence, decisions or allocations.

Only existing staff roles can read buildings; contractors and unknown roles
receive 403, unauthenticated requests 401, missing records 404 and invalid
building data 400. Building costs and home `cost_allocation` are returned only
to the existing `FINANCE_VIEW` roles. Other staff see a restricted-cost notice,
with amounts omitted server-side. The building screen is read-only and cannot
approve, instruct works, release safety restrictions, contact residents or pay.
Home AI assistance remains available through its existing proposal-only and
human-review paths; shared free text and costs are not added to prompts.

`tests/test_buildings.py` starts the real application on loopback with a
wholly fictional two-home SQLite fixture. It checks health/static serving,
authenticated navigation, role/amount isolation, scoped blocked advancement,
unaffected sibling advancement and availability of the existing assistant
registry. No live model inference, Azure deployment, actual SQL Server or
human/browser accessibility acceptance is implied. There is no register
editor or automatic retrofit of building data into an already populated store.

## What staff see

The #344 public edge now targets the existing immutable src API, not a rebuilt
legacy app. Deployment and tenant prerequisites are documented in the
[public browser continuation](../../infra/README.md#public-browser-continuation-2026-10-16-344).
Welcome/health are intentionally public; workbench pages require Entra and
protected JSON APIs must return 401 without a user. Browser redirect mode is
the infrastructure default (`entraBearerOnly=false`), not successful sign-in.
The proof's invalid registration/absent staff block real-user acceptance (#349).
The [dated feature audit](../../docs/architecture/mvp-to-src-parity-matrix.md#public-deployment-feature-audit-2026-10-16)
separates image presence, public intercepts and rendered/authorized behavior;
missing deployment/data/model/photo/law prerequisites are tracked by #350.

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
  (`src/core/src/zava_forward/core/ranking.py`): open safety issue, then priority support or an
  adjustment, then longest time in stage, then earlier stage, then case id as
  the fixed tie-break. Each card shows its rank and plain reasons, the list
  header shows the policy version, policy hash and as-of date, and
  `GET /api/ranking/policy` returns the versioned rules. The rules live in
  versioned files in `src/core/src/zava_forward/core/policies/` (for example `ranking-v1.json`) with a policy
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
  of open cases (Leaflet bundled in `web/vendor`; circle/O normal, square/W waiting
  60+ days, triangle/! open safety issue; status names and matching list),
  charts by stage, authority, wave and waiting time,
  contractor and team workload. Visits lists booked appointments by day.
  The dated synthetic generator now guarantees six additional forward
  assessment visits and retains historical attended/no-access/cancelled
  contrasts. See the [coverage recipe](../../docs/reference/research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13)
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
  Every upload is scanned before it can be downloaded or read by the document
  assistant (`doc_controls.py`; `ZF_SCANNER=local|defender`). The local scanner
  is a labelled synthetic test: a marker and a type check, not an antivirus
  engine. The Defender scanner reads the Defender for Storage blob tag through a
  fake transport only, and a pending result keeps the file unavailable. A
  programme manager lists documents past their retention trigger
  (`GET /api/retention`), approves each deletion (`retention-approve`) and can
  place or release a case legal hold (`legal-hold`, `legal-hold-release`); a
  hold blocks deletion. Periods are synthetic-demo placeholders, not an approved
  schedule, and the deletion log keeps no file name or content.
  The [bounded SQL rescan job](../orchestrator/README.md#bounded-document-rescan-job-117)
  now supplies an offline schedulable invocation, not a hosted timer or Defender
  activation. Its worker retains unavailable infected/mismatched bytes and holds;
  it cannot approve deletion or release a hold. Existing API/manual behavior
  and owner approval boundaries are unchanged.
* Funding: a person moves each application through draft, approved,
  submitted and confirmed. Approval needs complete evidence and the Grants
  and Evidence Officer or a manager. The system never submits anything.
* A hash-chained audit log records every change. `GET /api/audit-check`
  (manager) and `python -m zava_forward.core.ledger` verify the chain; a digest of
  the head can be written to `ZF_DIGEST_DIR` (`POST /api/ledger/digest`) and is
  re-checked on verify. The digest is a local file, not yet an immutable Blob.
* Role-based field projection is enforced on the server (`projection.py`).
  Contractors see only their own cases with "needs notice" and a named contact
  (the case owner), never the vulnerability reason, resident name or contact
  details. Staff see the reason only for the roles in `ZF_REASON_ROLES`
  (default Resident Liaison Officer, Building Safety Liaison, Retrofit Programme
  Manager); others see "Extra support noted". Every role is tested against every
  endpoint (`tests/test_role_matrix.py`, plus `tests/test_role_endpoint_inventory.py`,
  which fails when a server route is missing from its inventory and checks
  contractor canaries across API, CSV export, search, audit and AI prompts).
  Free-text notes (decided for the exercise): no pattern redaction, which gives
  false assurance. Free-text fields are excluded by allow-list from contractor
  responses and AI prompts, and roles without a recorded need see "Held for
  roles with a recorded need" for contact notes and outcomes, appointment and
  hazard notes. The reason-role list remains a proposal (OD-14, OD-19).
* Workflow screens on the case page: return to an earlier stage or reopen a
  closed case (manager), recording reason, source reference, next action,
  authenticated authority and existing receiving owner. Offer, record receipt,
  accept, decline, manually escalate to a manager, withdraw or complete a handoff.
  Receipt does not imply acceptance; the sender keeps case/chase ownership until
  the named receiver accepts. Pending sender/receiver/manager work lists and case
  detail distinguish accountability, destination, proposed/confirmed receiver,
  chase owner, urgency, due date, next action and resident-update commitment.
  Missing values remain unknown; no message is sent automatically. Existing
  resident-update commitments survive every transition and subsequent offers.
  Safety referral has separately evidenced receipt/acceptance and an
  evidence-backed independent home-hold release; see the #85 contract above.
  All actions use server-side checks; the old `handover` endpoint now offers
  rather than immediately reassigning. See the [core contract](../core/README.md#return-reopen-and-handoff-accountability-83).
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

* Staff time capture (PR-004) is off by default. It records only when
  `ZF_TIME_CAPTURE=on`, `DPIA_APPROVED`, `ZF_TIME_CONSULTATION` and
  `ZF_TIME_NOTICE_APPROVED` each hold a reference, one manager has requested
  enabling (`POST /api/time/request-enable`, audit
  `time_capture_enable_requested`) and a manager in a different role has taken
  the audited enabling action (`POST /api/time/enable`, audit
  `time_capture_enabled`, which names the requester; void if a reference later
  changes), and the person has acknowledged the staff notice
  (`POST /api/time/acknowledge`, audited); own entries only; screens at `#/time`;
  reports are manager-only, aggregated and suppress groups under
  `ZF_TIME_MIN_GROUP` (default 5). The enabling record, entries and
  acknowledgements are tables (`time_request`, `time_enabled`, `time_entry`,
  `notice_ack`) in the shared SQL store (SQLite, or Azure SQL with
  `ZF_STORE=mssql`), apart from case data, with portable DDL. Only the JSON demo
  store falls back to a local SQLite file (`ZF_TIME_DB`). Why the requester and
  the enabler differ: one role should not both propose and switch on monitoring
  of staff. The demo data has a single manager role, so enabling there needs a
  second user with the `Programme Support Officer` role (Entra app role
  `ZavaForward.SupportOfficer`); the status reason says so.
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

## Conversation panel (issue #159)

An optional, collapsed panel on the case card ("Ask the assistant about this case") for staff roles that may chat.
It is never needed to finish a task: every ordinary control stays on the page and works when chat is refused or
the model is down.

* `POST /api/chat/threads/{id}/ask` returns `{kind, reply, citations, label, model, workflow_only}`. The logic is
  `zava_forward.core.chat_panel` (core); the provider call is `zava_forward.agents.chat.ChatModel` (agents),
  composed in `server.py` in process until #144. Thread storage, consent gate (`CHAT_DPIA_REF`,
  `CHAT_LAWFUL_BASIS_REF`, `CHAT_NOTICE_REF`), redaction and per-user isolation are the merged #160 to #163 code.
* Every turn re-reads the staff role and the case through the user's own projection, so a revoked role or a case
  out of scope stops the next turn (403 or 404).
* Citations are ids of the projected case facts (`ZF-1/stage`). Uncited or unknown citations are dropped; with none
  left, or no case facts, the panel abstains and says so. Every reply carries "AI suggestion, not approved".
* A model failure (`disabled`, `timeout`, `provider-unavailable` or an unusable reply) returns `kind: fallback`,
  `workflow_only: true` and a plain message. A reply that carries tool or record-change syntax is withheld.
* `POST /api/chat/threads/{id}/proposals` with a `capability` calls the existing `Assistants.invoke`, so the request
  follows the existing source check and independent role review. The chat has no other write path.
* Web: `web/chat.js` (a `details` disclosure, a labelled form, an `aria-live="polite"` log and a `role="status"`
  line). Tests: `tests/test_chat_panel.py`, `core/tests/test_chat_panel.py`, `agents/tests/test_chat_model.py`.
* Not evidenced here: a screen-reader test (needs a manual run with a named reader), a live model run (no Azure
  endpoint locally) and real chat data (DPIA, lawful basis and notice references are unset, so storage stays refused).

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
| `ZF_TIME_CAPTURE`, `DPIA_APPROVED`, `ZF_TIME_CONSULTATION`, `ZF_TIME_NOTICE_APPROVED`, `ZF_TIME_DB`, `ZF_TIME_MIN_GROUP` | time capture |
| `ZF_DOC_STORE`, `ZF_DOC_DIR`, `ZF_BLOB_ACCOUNT_URL`, `ZF_BLOB_CONTAINER`, `ZF_BLOB_SAS`, `ZF_BLOB_CLIENT_ID` | document store |
| `ZF_SCANNER` | `local` (default) or `defender` content scanner |

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
  Use the [tenant staff initializer](../../infra/README.md#tenant-staff-and-application-role-initialization)
  to reconcile enabled tenant members, app roles and SQL bindings together.
  It replaces current generated staff/owner labels while preserving workload
  codes and historical actors, then restarts the startup-cached roster.
  Assigning an enterprise-app role without this binding still fails closed.
* Sign-out redirects through `/.auth/logout` to the public welcome;
  "Use another account" instead enters `/sign-in?switch=1` directly with
  `prompt=select_account`, without signing out of Microsoft first. Choosing
  another account is deliberate, not automatic; cancelling need not clear
  the previous session. See [flow diagnostics and acceptance](../../infra/README.md#account-selection-and-safe-flow-diagnostics).
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
See [staged token-store setup and permissions](../../infra/README.md#public-welcome-and-microsoft-account-photos).
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
python3 -m pip install --no-deps -e src/core -e src/agents -e src/api   # modules moved in M1 to M5 (ADR 0006)
python3 support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py --seed 20260901   # writes to ZF_DATA, default ~/.zava-forward/data/zavaforward.json
ZF_PASSWORD=choose-a-password python3 -m zava_forward.api
```

Open `http://127.0.0.1:8088` and sign in with a staff email from the data (for
example `aisha.rahman@zavanorthhomes.example`). Without `ZF_PASSWORD` a random
password is printed at start-up. The data builder shifts all dates so the
history ends today and prints no real personal data.

## Honest limits

Current scope is the continuing exercise, not production acceptance. Dated
earlier observations remain in the ADRs and pinned #58 evidence; they must not
be read as the current deployment state. The
[current infrastructure handover](../../infra/README.md#current-exercise-handover-2026-10-13)
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
* Time capture is enabled by environment references plus a requested and
  separately enabled audited action; the screens were exercised through the
  API, not in a browser. The staff notice text is a draft and the
  consultation reference is a flag, not evidence of the consultation. The AI
  evaluation uses a scripted model, so it checks behaviour, not model quality:
  latency, run-to-run variation and added value are scripted figures, not
  live-model measurements, and the golden cases are small and constructed.
  Citations prove a cited fact exists in the case, not that the claim made from
  it is right, and document reading cites the document record, not a passage.
* Browser checks: `src/api/checks/browser_check.py` drives the real server with
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
  now has the closed administrative bulk contract described above; controlled
  finance/sign-off approval refusal remains independent of that allowlist.
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

```bash
cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -v
(cd ../orchestrator && PYTHONPATH=../core/tests python3 -m unittest discover -s tests -v)
```

The tests also cover the SQL store (including `test_sqlreads.py`), documents, ledger, role matrix, workflows, auth and time capture. They use small fixtures and a generated 60,000-case dataset, and need no
private data. The AI tests use a scripted model or the template path (no network).

Browser check (needs python3 playwright and chromium, and the built dataset):
`python3 src/api/checks/browser_check.py` (the dataset at `ZF_DATA`).

## Regulatory alert and home chat UX (#215)

Synthetic development only under ADR 0005, accepted on 2026-10-16. The home
view now presents `/api/law/alerts?case=<id>` outside the optional chat. Each
visible alert shows what was noticed, source ID/status/effective/retrieval
dates, safe action, decision owner, clock and recorded due time. Latest check
and current-control status distinguish retained breach risk from an active
control. The browser does not calculate statutory deadlines, acknowledge
alerts, release holds or alter approvals. No visible alerts is not a safety
or compliance conclusion. Coverage stays unknown when the service says unknown
or cannot be reached. Refresh failures remove old results rather than present
them as current.

The existing bounded regulatory chat renders source excerpts, home facts,
unknowns, safe next action and human decision owner as separate sections.
Source quotations and stored evidence are unchanged. Plain-language
explanations are on by default and can be toggled with a labelled checkbox;
they explain the interface, not the law. Provision links open a source record
in a new tab, with an explicit warning. Missing sources, unsupported terms,
disabled lookup and outages have visible text and a human route, not a silent
success. Source excerpts retain snapshot/currentness and truncation caveats.
The existing doubt action sends the actual turn to Juan Manuel Servera's
synthetic exercise inbox; its receipt is not legal approval or a resident
message. Failed referrals are explicit and retryable.

### Audience patterns and delivery boundary

These patterns follow the [regulatory literacy research](../../docs/reference/research/ux/regulatory-literacy-for-journeys.md),
not validated staff needs or new legal advice. Role guidance never grants
access: existing server projection and alert audiences still govern every read.
All staff see data-minimisation guidance and the named exercise doubt owner.

| Issue audience | Know at least / alert pattern | Home-chat and doubt pattern | Existing account / evidence boundary |
| --- | --- | --- | --- |
| Repairs and intake, including housing/contact staff | Recognise a possible damp, mould or emergency report; record awareness without guessing; use the human hazard route without waiting. Show the recorded clock and safe action, not an inferred legal deadline. | Ask for hazard sources and recorded home facts; uncertainty goes to the human safety service and exercise owner. | Resident Liaison Officer guidance and scoped hazard alerts exercised locally. There is no distinct repairs account or validated operational procedure. |
| Building Safety | Categorisation, recorded clocks and independent evidence need human judgement; completion is not assurance. | Compare cited source records; interpretive questions go to Juan Manuel Servera as exercise owner, never to an automatic hold release. | Building Safety Liaison guidance exercised; existing owner capabilities are unchanged. |
| Assessor and coordinator | Appointed PAS roles, risk path and independent evidence matter. Only an overview is held; licensed text and contract incorporation are unverified. | Identify the missing licensed/contract source and ask the appointed coordinator/Compliance; no invented PAS requirement. | Retrofit Coordinator and Quality Inspector guidance exercised. No separate assessor role is created. |
| Programme | A policy target is not a duty in force, completed task, investment approval or award. Read source status and dependencies. | Source lookup may inform a proposal; applicability, source conflict and approval stay human. | Retrofit Programme Manager and Programme Support Officer guidance exercised. |
| Finance and grants | Obtain the actual award letter/agreement; an allocation annex does not authorise a claim or commitment. | Requests for binding grant/contract terms have no supported answer without the actual document; refer to funding owner/Finance, with exercise legal doubt to Juan Manuel Servera. | Grants and Evidence Officer guidance exercised; no new financial approval or grant lookup capability is claimed. |
| Data handlers | Purpose limits, sensitive health/vulnerability data, consent versus other lawful bases and meaningful human involvement in significant decisions. | Do not type personal details; use bounded automated-decision source lookup where supported and the exercise DPO doubt route. | Cross-cutting guidance for all seven staff account roles exercised. No new data-handler access role. |
| Suppliers | Follow agreed contract/scheme requirements; contract and TrustMark terms are not held. Obtain them from the named contact/contracts manager. Safety intake cannot wait. | Staff chat is unavailable; named-contact human route in the supplier home view. A supplier chat/alert interface remains design-only. | Existing Contractor view guidance exercised; law/alert/chat endpoint denial retained. No supplier rights added. |

Supplementary design-only patterns: leasehold-service staff must obtain the
actual lease and Legal review before explaining responsibility. Residents and
representatives need a human-reviewed plain explanation of choices, safe
contact, complaints/redress and a non-digital route, not a legal-duty lesson.
Neither audience receives a new chat interface or invented source in this slice.

### Local engineering checks

Unit discovery requires only the installed runtime distributions, not Playwright
or a browser. The regulatory harness imports its browser APIs only when browser
operations run; target-size boundary and axe-integrity assertions always run in
the unit suite. A subprocess regression also blocks Playwright imports even
when the dev extra is installed. From the repository root:

```bash
python3 -m venv /tmp/v215c
/tmp/v215c/bin/pip install -e src/core -e src/agents -e src/api
(cd src/api && PYTHONPATH="$PWD/../core/tests:$PWD/../agents/tests" \
  /tmp/v215c/bin/python -m unittest discover -s tests -q)
```

Install `src/api[dev]` in that venv before running Ruff, mypy or browser checks.
Playwright stays dev-only; asking to run a browser check without it fails
explicitly rather than skipping browser coverage.

The browser check uses the actual loopback HTTP app, SQL case store, law store
and wholly constructed `regulatory_fixture` data. It does not read `ZF_DATA`
or private working files. Provider calls are blocked; browser network access
outside loopback is aborted. A pinned local axe script runs inside Chromium;
no application content is sent to the download host. From the repository root,
after installing the project distributions and API dev extras with pip:

```bash
python3 -m playwright install chromium
curl -fsSL https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js \
  -o /tmp/axe-4.10.3.min.js
export PYTHONPATH="$PWD/src/api/tests:$PWD/src/core/tests:$PWD/src/agents/tests"
python3 src/api/checks/regulatory_ux_check.py \
  --axe /tmp/axe-4.10.3.min.js --out /tmp/regulatory-ux-results.json
python3 -m unittest test_regulatory_chat_api test_rule_alerts test_chat_panel \
  test_chat_isolation test_accessibility_baseline test_design_system test_role_matrix -q
(cd src/api && python3 -m unittest test_regulatory_ux_check -q)
(cd src/api && ruff check . && ruff format --isolated --line-length 100 --check checks/regulatory_ux_check.py && mypy)
```

The check verifies the axe 4.10.3 SHA-256 before execution:
`880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`.
API tests precede core tests in the absolute `PYTHONPATH` to avoid colliding
test module names. Checks cover WCAG 2.2 A/AA axe tags on the changed surfaces,
native Enter/Space controls, Tab/Shift-Tab traversal, visible focus, post-answer
and doubt focus, text statuses, 320/390/1280px reflow and 200% text sizing.
Every exercised state also measures visible enabled controls, links and
disclosure summaries: at least 24px width/height, preserving the cited-lookup
summary's stronger shipped 44px height. Citation links now have a 24px
inline-block target rather than an 18px inline text box. The supplier guidance
is static and has no interactive targets.
The test also checks persisted doubt/history, missing sources, retained risk
after source change, service outage, disabled lookup, staff guidance and
contractor denial. It is an engineering check, not a complete WCAG conformance
assessment, human screen-reader test or operational release gate.

Observed locally on 2026-10-16: 17 axe states had zero detected violations;
eight states retained `color-contrast` incomplete results for textareas whose
background axe could not establish (reported as partially obscured). Those
results require further assessment, not a pass declaration. Keyboard traversal,
focus and reflow assertions passed. The 86 targeted API and 33 core regression
tests, API ruff/format and strict mypy passed. These observations do not satisfy
the full WCAG criterion or the staff comprehension criterion.

The `src-api` job in [source CI](../../.github/workflows/src-ci.yml) now runs
this UX regression check next to `checks.design_system_browser_check`, using
the same installed Chromium and an absolute API/core/agents test path.
It fetches the pinned axe version with bounded retries/timeouts; the harness
verifies the SHA-256 before executing it. A failed download emits a CI warning
and omits only axe, never the target-size, keyboard, reflow, role or local API
assertions. Supplied wrong-hash content fails rather than downgrading. JSON
results explicitly record axe execution/skipping and are uploaded as
`regulatory-ux-results`. To run without axe locally:

```bash
python3 src/api/checks/regulatory_ux_check.py --out /tmp/regulatory-ux-no-axe.json
```

Review follow-up on 2026-10-16: the exact new CI shell block passed locally both
with a successful download and a deliberately failed curl. Both paths checked
142 targets across 17 states, minimum measured width/height 24px; cited-lookup
summary height 44px. The axe path retained the same eight contrast incompletes.
Deleting `.regulatory summary{cursor:pointer;min-height:2.75rem;padding:.5rem 0}`
from the served stylesheet failed the actual browser check at `cited-answer`:
the summary measured 1198 x 24px, below its 44px design floor. Restoring the rule
passed both CI paths. The unstyled 24px summary alone is not an AA violation;
the stronger assertion protects the existing intended target. Three harness
unit tests also cover 24px boundaries, static supplier content and corrupt axe.
The subsequent CI import-boundary repair adds a fourth harness test that
rejects any discovery-time Playwright import, without skipping those assertions.
After merging current main, the runtime-only `/tmp/v215c` environment reproduced
the eager-import failure. With browser imports deferred, all 561 API tests pass
(110 opt-in skips), both before and after installing Playwright 1.64.0.
API Ruff/format and strict mypy pass; both source CI browser harnesses pass
against the synthetic loopback app. Regulatory results remain 17 states,
142 targets, zero detected axe violations and eight incomplete contrast states.
The 86 targeted API and 33 core tests, design-system browser check and API
ruff/format/mypy passed. Hosted CI is pending, not claimed passed: the owner
requested push without waiting. Full issue acceptance remains unchanged.

### Staff comprehension protocol (Not run; unmet)

Before actual staff use, obtain participant/research authorization and privacy
review from the relevant real owners; the exercise owner decision does not
provide these. Recruit at least three authorised participants from each of
repairs, housing and grants, including keyboard/assistive-technology users where
possible. Obtain informed voluntary consent, accessible/non-digital instructions
and the right to stop. Use only fictional homes, sources and exercise identities.
Do not record actual resident information, private staff identifiers or unconsented
audio/video. Agree storage, access, retention and deletion before collection.

Give each participant the same five tasks without legal coaching: recognise an
urgent hazard while chat is unavailable; identify noticed/source/status/action/
owner/clock; distinguish future/unknown evidence from an active control; handle
a missing grant/contract source without inventing terms; and route a doubtful
turn and explain what its receipt does not approve. Counterbalance deterministic
cards with provision links against chat on equivalent fictional tasks. Record
task success, unsafe actions, source/status/owner comprehension, completion time,
assistance, accessibility barriers and confidence, using anonymous study codes.

Predeclare success as at least 90% correct required answers overall and at least
80% in each participant group, with zero critical errors (delayed hazard intake,
invented approval/consent/terms, future-as-active duty, or a claim that a doubt
receipt establishes compliance). Two reviewers independently score against a
frozen answer key; reconcile disagreements with reasons. Report denominators,
failures, group differences and uncertainty, not just averages. Small formative
samples cannot establish generalised staff comprehension or chat value.
Stop a task immediately if real personal information or a safety misconception
appears; explain the safe route, record the failure and revise before a new
approved round. The human owner reviews results before any staff-use decision.
No participants were tested here; no comprehension result or chat-value pass is
claimed.

### Issue criterion audit

| #215 criterion | Local disposition | Evidence and remaining gap |
| --- | --- | --- |
| Patterns defined per role with know-at-least content | Met as synthetic design/implemented existing-role guidance | Seven-audience matrix above, real role-loop browser assertions and supplier human-route/denial check. Separate repairs, Finance, resident and supplier-chat journeys are not delivered or user-validated. |
| Each alert states noticed/source/status/safe action/owner/clock | Met for the existing scoped alert contracts | Browser asserts required fields against a real SQL-backed breach-risk alert; current-control state, empty visibility and outage are explicit. No new rule coverage is claimed. |
| WCAG 2.2 AA, no colour-only status, keyboard, plain language | Partial; full criterion unmet | Automated axe and keyboard checks cover changed surfaces, textual statuses, focus, toggles and reflow. Comprehensive manual/assistive-technology conformance remains unassessed. |
| Doubt and no-source states explicitly designed | Met in bounded synthetic slice | Persisted exercise inbox receipt, visible unsupported/missing-source state, disabled/outage text and manual owner route. No real owner notification or approval claimed. |
| Comprehension tested with repairs, housing and grants staff | Unmet / Not run | Protocol only. Actual staff testing is unavailable and remains required before use. |

No issue checkboxes are changed by this implementation. Real delegates,
verified applicable sources, operational acceptance and the ADR 0005 measured
chat-value ship test remain open.
