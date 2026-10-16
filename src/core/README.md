---
title: Zava Forward core library
description: Domain, store, ledger, law store, chat storage and synthetic-data documentation for the core project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-16
ms.topic: reference
---

The shared domain library (`zava_forward.core`): stores (JSON, SQLite, Azure SQL), ledger, law store,
rule cards, governance, continuity, chat storage and isolation, and the synthetic tools. It imports no
workload. The sections below are moved unchanged from the former `mvp/README.md` (ADR 0006, issue #199,
M6); the staff-facing behaviour and configuration are in [api](../api/README.md).

Test paths named `tests/...` are in `src/core/tests/` unless they name another project:
`test_chat_isolation` and `test_continuity` are in `src/api/tests/`. Run the suite from `src/core` with
`python3 -m unittest discover -s tests`. Data fixtures and generated datasets are written to the
per-user `ZF_DATA` folder, never under `src/`.

## Derived role task queues (#76)

`taskqueues` provides the shared, read-only `work-queues-1` definition/default
contract and case task context. Store and SqlStore return identical projected
context in staff list/detail. Both retain a process-local case-ID membership
cache before filtering/counting/paging. JSON builds all six memberships together
from the canonical evaluator on a cache miss.

SqlStore and MssqlStore persist six `queue_*` integer columns, each indexed with
the case ID. Seeding and case writes maintain membership in the same transaction
as the body, sequence and audit. Ordinary unlinked-case writes evaluate only
changed cases. Shared building/procurement and linked-home writes conservatively
recompute all memberships using authoritative SQL bodies and shared documents,
not a stale process copy. Older schemas add default-zero columns without marking
them ready; startup backfills before certifying the complete generation. Reopening
a populated database does not need the seed file.

A persisted fingerprint covers queue definition version, dataset `as_of`,
complete ranking policy and current resident-authority/retention day. Changes
force a full refresh; flags, fingerprint and generation publish atomically.
Every lookup, including a hot hit, checks freshness under a short cross-process
writer lock and synchronises the case copy. A cache miss selects only IDs from
the relevant covering SQL index. Filtering, global ranking and sorting still
run in memory after lookup; they are not constant-time. Cached IDs contain no
viewer-projected context: visibility, ownership, filters and returned narratives
are checked anew for each request. No approval, assignment or event semantics
change. CSV still projects every matching output row.
The API guide documents [definitions, source fields, snapshot clock, redaction
and remaining owner decisions](../api/README.md#role-task-queues-and-shared-case-context-76).
JSON/SQLite semantic tests cover seven/30/180-day boundaries, unknowns,
handoff lifecycle, independent deadlines, missing named owners and 120-case
paging/sort/export parity. Role-only responsibility never invents a named owner;
draft policy and accepted AI advice cannot produce approved programme priority.

### Generated 60,000-case queue timing (#327, 2026-10-16)

Local Python 3.12 SQLite results, not Azure or private-stock evidence. The
reproducible fixture is `test_sqlreads.queue_cases(60000)`, seed 5, snapshot
2026-10-16: fictional Test Road homes with deterministic stage dates, EPC dates,
handoffs and resident-update deadlines; 58,224 are open. Measurements exclude
generation/database initialisation and include the same lightweight evaluator
counter in both runs. Baseline is the exact merged `Store`/`SqlStore` source at
`aedd616` (#336), loaded in memory without altering the checkout. Three rounds
per queue each commit a one-case `benchmark_revision` change, read the first
50-row page with a cold application cache, then repeat that identical page.
These are application-cold reads after a write, not flushed OS/database caches.
The unavailable priority queue has no output rows.

All values are median milliseconds, before/after this SQL-membership change:

| Queue | Matches | Cold before | Cold after | Repeat before | Repeat after | Write before / after |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| new | 19,375 | 2900.0 | 1062.9 | 60.8 | 54.1 | 16.6 / 5.1 |
| priority (draft policy) | 0 | 2850.5 | 1140.5 | 0.2 | 0.2 | 6.1 / 4.7 |
| stale | 14,539 | 3487.7 | 1107.9 | 59.2 | 41.0 | 4.2 / 4.7 |
| blocked | 58,224 | 3153.5 | 1241.0 | 191.8 | 145.0 | 3.4 / 4.0 |
| overdue | 18,326 | 3029.8 | 1157.0 | 55.3 | 54.3 | 2.5 / 3.6 |
| unowned | 11,675 | 3032.2 | 1130.5 | 43.6 | 34.2 | 3.8 / 4.1 |

Cold reads evaluate exactly 50 output contexts, down from 58,274; priority
evaluates zero rather than 58,224. Repeat reads still evaluate output contexts.
Global ranking is rebuilt after each write, even for the empty queue, and
remains a significant cold cost. Across these rounds cold times ranged
2281.6-4305.1 ms before and 474.9-1259.4 ms after. Baseline write outliers
reached 1005.2 ms; final writes ranged 3.3-7.4 ms. These small, noisy samples
do not establish a write-speed improvement or a production latency guarantee.

Fresh database initialisation, measured separately including seed/backfill,
was 14.213 s before and 15.029 s after. Day, policy, definition or snapshot
refreshes and shared-dependency writes can still recompute the whole stock
under the writer lock; their latency is not represented by the ordinary
one-case write column. No live Azure SQL timings were collected.

A later full-suite run after integrating `main` at `79b153b` observed cold
medians of 1.33-2.00 s, repeat medians of 0.3-222.6 ms and initialisation of
25.521 s. Context counts remained exactly 50/zero. This additional observation
illustrates timing variability; the paired table is not a stable latency promise.

The earlier cache-only #336 measurement was 3217.4/3090.6 ms for a first cold
`new` page: it did not materially improve cold latency. That historical
second-page experiment is not interchangeable with this post-write benchmark.

Run from `src/core` in the installed pip venv:

```bash
python -m unittest discover -s tests -p test_queue_benchmark.py -v
python -m unittest discover -s tests -p test_sqlqueues.py -v
python -m unittest discover -s tests -p test_taskqueues.py -v
```

The benchmark asserts bounded context calls, not a noisy cold-time ceiling.
It fails for all six queues with the baseline source. Separate mutation checks
also fail when SQL lookup, incremental writes or shared-dependency maintenance
are disabled. The existing `test_sqlreads` scale test retains its 1500 ms
repeat-page ceiling. JSON/SQLite parity covers every queue, sort and view,
including positive approved priority, search, combined filters, exports and
cursors. SQL tests verify physical flags, index plans, backfill without a seed,
rollback and cross-process shared-context/generation handling. Server-free
tests check SQL Server integer schema/migration, index translation and portable
lookup/write statements. `MssqlQueueMembership` wires the same behavior tests
into the existing opt-in SQL Server harness; skipped live tests are not evidence
of actual Azure SQL execution.

## Resident decisions and representatives (#86)

`resident_decisions` records supplied human statements, never inferred consent.
Every measure starts `Not recorded`, including when a historical case-wide
answer says Accepted. A staff member first records the exact measure scope,
its source and the current technical design version. Scope revisions increase
monotonically; any case-wide technical design change invalidates the current
resident contexts conservatively. Changing back never restores an old answer.
New answers require the exact current context revision, a supplied source and
who spoke. Recorded home, measure, scope, design, actor, time and version remain
in history. Contact, access, AI drafts and other measures cannot populate them.

A pause, withdrawal or decline creates a human-review flag for that measure.
Its siblings' statements are unchanged. Restart requires a new supplied
acceptance and human-review evidence; neither a complaint outcome nor an AI
proposal clears it. Case advancement checks every measure; work-order versions
and quality records bind explicit measure/context revisions and check only
those dependencies. Unbound legacy work/quality records cannot release work.
Package scope changes require reissue with explicit current resident bindings.
Safety, technical, funding and shared-building checks remain independent.
The existing SQL transaction rechecks resident bindings, current authority and
case row versions before commit, including operations that only change work
orders. SQLite concurrency/restart and a separate synthetic Azure SQL exercise
are tested; this is not real resident or operational acceptance.

Each representative reference has versioned task-limited authority: measure,
scope/design, source, evidence date, review date, resident's stated wishes and
confirmed safe-contact reference/revision. Scheduling/attendance/interpreting
does not grant works-decision authority. Authority must be Confirmed, cover the
requested task/current context, start no later than today and have a review date
strictly after today (the review date itself stops reliance). Unclear, disputed,
revoked, superseded, missing or expired authority stops representative decisions
and disclosure checks until staff confirms through the safe route. A contact
change, even changing back, requires new authority. Historical representative
acceptance is rechecked at use time against its exact latest authority version;
another valid representative cannot substitute. A resident's direct supplied
statement remains recordable independently. Nothing is sent by the checker.

Independent review is a separate service type linked to an actual recorded
measure-decision version. Its reviewer must be neither the contested recorder
nor the request handler; only the named reviewer updates/closes that review.
Complaints retain separate handler/redress owners and independent closure.
These routes remain recordable on paused or closed retrofit cases and do not
change consent, ranking inputs, hazards, tenancy or repair state. No live formal
complaints integration or real-user without-detriment evidence is established.

The owner confirmed the field matrix on
[2026-10-16](https://github.com/jmservera/ama/issues/86#issuecomment-6209881675).
Existing `Resident Liaison Officer` represents Neighbourhood/Resident Engagement;
`Retrofit Coordinator` represents Retrofit staff. Both record and view decisions,
authority evidence, wishes and safe-contact references. `Retrofit Programme
Manager` and `Programme Support Officer` view, but cannot record these fields,
including through the legacy decision endpoint. Writers must match a registered
named human, not merely supply a role. Separate complaint/redress actions retain
their existing named-owner controls; they cannot change works decisions.
Other staff do not receive authority/contact/source/wishes narratives.
Resident viewing rights do not depend on `ZF_REASON_ROLES`; unrelated vulnerability
and contact-note restrictions still apply. Contractors receive only per-measure
`Proceed` or `Hold` resident readiness, never the underlying resident reason,
wishes, vulnerability or safe-contact details. Other existing operational
allow-listed fields remain. AI tasks use narrow task inputs; no authority,
wishes, safe-contact history or complete decision record enters those inputs.
Views detach histories before redaction. Audit uses event/version metadata;
new legacy decision notes are no longer copied into the immutable ledger.

The [owner's first-contact clarification](https://github.com/jmservera/ama/issues/86#issuecomment-6209904857)
sets retention to five calendar years from the resident's first recorded
interaction, not the decision, withdrawal, authority expiry or work completion.
`RESIDENT_RETENTION_YEARS` in `resident_decisions.py` is the configurable constant.
The earliest eligible valid nonfuture `contacts`/`resident_contact_history` timestamp or
`resident.first_contact_at` establishes the origin. Recording contact or a
resident-confirmed safe route preserves the earliest marker until deletion. Missing/invalid
history stays `Unknown`, never inferred from a decision; reconcile it before
operational use. The schema has no universal cross-case resident identity:
importers must preserve the resident's actual first-contact marker across cases,
not match people by name or address.

`resident_retention` in staff detail reports origin, due date and expiry.
February 29 anniversaries use February 28 in a non-leap year. At the anniversary,
decisions and representative disclosure/consent checks cannot release work,
even if legal hold retains the records. Withdrawn decisions and expired
authority use exactly the same schedule. The existing manager retention list
includes a `resident-decisions` item; approve it through `retention-approve`
to remove current scoped decisions, authorities, wishes, safe-contact references/
history, resident reviews and scopes, reset the legacy answer, clear the resident
representative and remove service-request representative references. The cached
first-contact marker is cleared. A personal-data-free tombstone retains only the
count of general contacts present at deletion, alongside the deletion date.
Complaint outcomes and general contact
records have separate purposes and are not silently deleted. Legal hold blocks
deletion, not expiry. Deletion is manager-reviewed, not a configured automatic
purge job. Existing ledger text, backups and SQL row history are not erased by
current-payload removal; operational erasure needs a separately approved design.

The [owner's restart decision](https://github.com/jmservera/ama/issues/86)
(2026-10-16) starts a new five-year period from the first contact recorded after
deletion, not from deletion itself. Until that contact, origin and due date are
`Unknown`. The tombstone excludes the retained pre-deletion contact prefix, even
when renewed contact has the same day/minute timestamp. Either a newly logged
general contact or a newly confirmed safe-contact route can start the period;
later contacts do not extend it. Old decisions, authority and scopes are not
revived: staff must record fresh scoped evidence. Expiry still holds release and
representative disclosure until manager-approved deletion and renewed evidence.
Each later approved deletion establishes a new boundary. For older date-only
deletion records without a count tombstone, general contacts on or before the
deletion date are conservatively excluded because their same-day ordering cannot
be recovered; a later-day contact or fresh safe-contact confirmation can establish
the new period. Neither path infers resident consent.

Cards, missing-decision filters and AI citation labels use current scoped
status, not the legacy answer. The SQL missing-decision filter deliberately uses
the existing live in-memory path because authority can expire without a write;
other indexed filters remain unchanged. Existing AI proposal configuration,
release and human-review controls remain enabled as before. Representative-
addressed legacy templates refuse unchecked disclosure; staff-facing AI
message/summary proposals do not depend on that addressed template and remain
unapproved drafts, never consent or sending.

`tests/test_resident_decisions.py` covers JSON/SQLite exact-context decisions,
authority expiry/supersession/contact, sibling-only work/QA release, independent
review, privacy persistence and stale transaction refusal. Synthetic adapter
calls are not live inference. Formal complaint routing, human accessibility/
without-detriment acceptance, actual model and full hosted workflow acceptance
remain unmet. The opt-in `AzureResidentDecisions` test exercises the SqlStore
behavior through MssqlStore on an isolated Azure SQL database using constructed
DATA only, verifies reopened state/current-payload purge and an intact audit
chain, and reports the database ledger mode. It refuses database names outside
the `resident86test` prefix. The operator must create a fresh database, supply
Entra authentication, and remove verification resources afterward:

```bash
ZF_RESIDENT_AZURE_TEST=1 PYTHONPATH=src/core/tests python3 -m unittest test_resident_decisions.AzureResidentDecisions -v
```

This is a real SQL engine check, not evidence that historical database copies
were erased or that any real resident accepted the service.

## Stock comparisons and human technical sign-offs (#84)

`stock.py` validates staff-recorded conflicting assertions for `epc`, `type`
or `built`. Each comparison preserves two different values and each source's
identifier, ISO date, version and recorded validation state, plus a registered
query owner and authenticated recorder. Comparisons append as `SQ-n` with a
case-local version. The original home value is unchanged; authority,
resolution and eligibility remain `Unknown`. A source assertion labelled
`Validated` is not a decision that it is authoritative.

Unresolved queries expose an owned blocker before a design exists and after
sign-off. They prevent technical approval and installation progression, never
remove a home from ranking or block independent hazard intake. There is no
automatic resolver, eligibility-rule engine or stock overwrite. An approved
source-authority/resolution workflow remains future work.

Only the registered case owner or a programme/manager role may open a query.
`stock_query_event` appends a separate `SQE-n` event referencing `SQ-n`; it
never edits the original assertion or any previous event. A query's original
raiser (not merely its assigned query owner), or a programme/manager role,
may `withdraw` with a reason. Only a registered named human in the existing
`Retrofit Programme Manager` or `Programme Support Officer` roles may `resolve`,
with a reason and human review evidence reference. Agents and client-supplied
actor identities cannot exercise these rights. Repeated terminal events fail.

Effective `Withdrawn`/`Reconciled` status is derived from those events in
views and blockers. Reconciliation records a human attestation only: no
source wins, no home value changes, no professional sign-off is given, and
authority, resolution policy and eligibility remain `Unknown`/
owner-approval-needed. These are minimal exercise permissions, not ratified
operational resolution rules or competence/delegation. A new query is needed
to raise a later concern; closed history cannot be reopened or overwritten.
Other unresolved queries and independent technical, building and hazard gates
remain effective after disposition.

JSON retains assertions/events and the hash-chained audit. SQL inherits this
case-body contract and commits the new event and audit together using existing
rowversion checks; concurrent terminal events fail closed. Technical approval
also rechecks current stock holds inside the SQL writer transaction. No new
schema or dialect-specific inserts/error classes are introduced. Local
SQLite evidence does not establish SQL Server/Azure acceptance.

The existing `signoffs.py` owns separate assessment, design, building and
coordination decisions. They require registered staff identities in the
existing exercise roles, distinct people and no self-approval of the recorded
design. History records the actor email/role and design version. A design change
returns only the selected design-dependent sign-offs; omitted selection returns
all design-dependent sign-offs, but empty, duplicate or invalid selections are
rejected before mutation. Unaffected decisions keep their original version.
Human reapproval is explicit. Existing building blockers and home hazard holds
are reused, with no transfer of sibling approvals or resident consent.
These role mappings do not attest professional competence or actual delegation.

Support is tri-state: `Yes` for an observed true flag or recorded adjustment;
`No` only for an explicit false flag and `"None"` adjustment; otherwise
`Unknown`. `support_coverage` separately reports `Unknown` if either input is
missing, including mixed positive cases. Compatibility Boolean `support` and
contractor `needs_notice` mean observed positive only, not known absence.
Staff detail/list, counts, visits, filters and AI facts share this meaning.
Unknown inputs remain in the existing nonpositive support ranking bucket;
safety, waiting time, stage and case-ID factors remain independent. No new
health inference or policy weight is introduced. SQL refreshes existing
derived support/rank columns once using `meta.support_encoding=1`, preserving
source assertions, workflow state and audit; no new SQL schema/dialect is added.

`tests/test_stock_reconciliation.py` covers JSON/SQLite semantics and upgrade
behavior. The [API guide](../api/README.md#stock-reconciliation-api-84) describes
the staff endpoint, rendered synthetic check and remaining acceptance gates.
Live SQL Server/Azure, real model use, source authority, competent human review
and direct user acceptance are not established by these local tests.

## Task-bound RAI release records (#219)

`assistant_release.py` reuses the migrated `assistant_releases` and
`assistant_events` tables. `rai_release.py` owns pure typed validation/selection;
`ai_registry.py` owns the eleven registered tasks. No workload import, new
schema, SQL dialect extension or SQL/blob dependency for agents is added.
Existing records without the extended contract deny dispatch until a human
records a replacement; startup never upgrades an old approval automatically.

A record requires `release_version`, registry-matching `intended_use`,
`prohibited_uses` and `affected_stakeholders`, a named `accountable_owner`,
`impact_assessment`, `residual_risk_decision: Accept`, a residual-risk note,
`evaluation_decision: Pass`, 1-20 approved evaluation references in `evidence`,
and all seven `material_change_triggers`: `intended_use`, `model`, `prompt`,
`policy`, `data`, `evidence`, `permissions`. A reference is a human-recorded
assertion, not an automated finding that an evaluation passed. Evidence class
distinguishes `constructed-fixture` from `actual`; constructed records cannot
authorize the real `Ai` client.

Bindings include the task use/impact contract hash and evaluation protocol
version, model, registry/schema, prompt, policy, data/provenance and permission
versions. `ai_prompts.py` supplies actual retained-task instructions and their
hash for dispatch, release matching and stored output metadata. Routine case
edits stale source-dependent proposals; changed use, model, instructions,
policy, evidence or permissions invalidate the release or its dependent work.
`AI_MODEL_VERSION` supplies the expected provider model identifier for the fast
deployment; `AI_MODEL_VERSION_STRONG` supplies it for strong requests (defaults
to the fast value). Unattested configured models deny actual dispatch. A
returned model comparison is not independent serving-version attestation.

Approval supersedes every active record for that task, including old routing
configurations, while preserving events. One record approves one deployment;
changing the task's fast/strong route requires renewed approval. A rollback
cannot revive a superseded record. Activations retain release ID/version/body
digest; renewal creates a distinct assistant activation without overwriting
old work. Claim, dispatch, completion, detail/review and export reliance recheck
that reference. Cached briefings, ordinary/document reviews and separate
priority views/reviews also recheck the selected record. Changed releases
during calls discard/quarantine results, even when a replacement has the same
binding. Manual templates, human review, consent and safety controls remain.

Historical AI output requires a nonempty exact release reference and a currently
selected matching record even when inference is switched off. Reliance uses the
task's registered current fast/strong deployment, not its stored historical
alias. Configured briefing fallbacks without a current release are retried rather
than reused from cache, so recording matching approval restores generation
without an unrelated case edit. Workflow-only and unconfigured template caching
and manual/template acceptance remain available.

Configured JSON-store inference now denies because it has no SQL-owned release
record; it remains usable for manual/workflow-only work. Synthetic output
tests explicitly install test-only authorization rather than weakening this
production boundary. No real resident data or model call is needed to exercise
the release-control semantics.

OQ-017 remains open: live release, residual-risk acceptance, suspension and
restart holders and competent-review delegations are not evidenced. The
project contact in a denial is not a grant of those authorities. Approved real
evaluation, provider attestation, Azure SQL race evidence and direct human
oversight remain separate gates. Local synthetic checks do not approve live use.

## Hazard referral and home retrofit holds (#85)

The existing `workflows` module records an unverified observation and links an
external hazard/repair case. Reported category and urgency are not the service's
classification. The existing hazard and repairs service owns categorisation,
clocks, action, resident updates and closure; no command here changes them.
No transport is implemented: sending, receipt, acceptance, repair and timing
references are human-recorded assertions, not independently verified delivery.

New observations require a source/channel reference and timezone-aware
`aware_at`. Reporter, recording time and hold scope are server-derived.
Every hold explicitly covers the linked home/case, not its whole building or
another household. Referral requires a destination staff safety receiver,
external case/job reference and sending evidence. It does not imply receipt.
Only that receiver can separately record receipt and then acceptance, each
with evidence. Sender retains referral follow-up until acceptance; the retrofit
case owner and resident decision never change through these actions.

The receiver may record external response/resident-update due and actual
times, supported by an evidence reference. Unknown times stay unknown;
existing observations cannot be overwritten here. These are not calculated
statutory clocks, service updates or promises of compliance. Previously unknown
external times can still be recorded after retrofit work restarts; lifting that
restriction does not end the external response or updates. Each transition
has an immutable versioned snapshot and an audit-ledger entry, persisted using
the existing case body on JSON, SQLite and SQL Server without a new schema.
Local durability evidence covers JSON/SQLite, not actual SQL Server.

External repair evidence must follow receipt and acceptance. A different
safety-role actor, neither reporter nor repair recorder, must record the
release reason and external supporting evidence. This releases only the
retrofit hold, not the external hazard case. Active holds block technical
sign-off, installation advancement, new/reissued/corrective work orders,
booking/completion and quality acceptance/handover. Existing building,
resident consent, funding and technical gates remain independent.
Manual hazard intake/referral remains available despite AI failure, retrofit
pause or a closed retrofit record, without reopening or changing that record.

SQL-backed guarded transitions reload the dependent home's hazards and check
its row version inside the committing transaction, including work orders that
do not modify the case itself. The existing SQLite writer transaction and
SQL Server transaction-owned application lock serialize intake against that
validation and commit. A hold or stale dependency refuses the entire transition
and its audit entry; it cannot be waived by a process-local precheck.

The safety-role mapping and independent release check above are demonstrator
controls, not ratified operational authority. Repairs, Safety and Housing owners
have not approved who may release a retrofit hold, response/resident-update
timing, or escalation policy (RV-002). Recorded due times are external assertions,
not an approved timetable. Original issue acceptance remains unmet and unchecked.

Legacy hazards display unknown missing provenance rather than inferred dates
or receivers. Active legacy referrals/repairs need a prospective evidenced
referral binding, retaining the original record, then new receipt, acceptance
and repair evidence. Already released legacy holds stay released.
New evidence/source narratives are withheld from staff without a recorded
need and contractors see no hazard record; they are not added to AI prompts.

`tests/test_hazard_referral.py` covers these semantics on JSON and SQLite,
including restart, legacy continuation, invalid actors/indexes/replays,
closed-record intake, consent/building gates and model-source minimisation.
Interleaved two-store SQLite regressions cover all guarded transitions,
including the previously reproducible work-order completion race; these do
not claim actual SQL Server durability or operational approval.
Operational timing/escalation policy, real service integration, permitted real
model inference, SQL Server/Azure workflow and human acceptance remain open.
AI remains available through existing configuration/release/human-review
gates; this slice grants it no safety authority and cannot certify those gates.

## Return, reopen and handoff accountability (#83)

`workflows.py` is shared by JSON/SQLite local stores and the Azure SQL store.
Every new return/reopen requires a reason, source reference and next action,
and records version, prior/current stage, authenticated initiating authority and
the existing named case owner as receiving owner. A return/reopen never assigns
another owner. Older history is preserved; absent provenance is unknown, not
verified or reconstructed. Selective downstream approval invalidation under
FR-043 is not established by this slice.

Handoffs expose canonical `status` alongside the legacy `state`: `Offered` means
Sent and `Declined` means Rejected. Received, Accepted, Escalated and Completed
are distinct states; Withdrawn remains an explicit terminal alternative.
Only a named recipient may receive/accept/reject. Only the sender or a manager
may withdraw or manually escalate to a named manager. Completion requires the
accepting current owner and a note; it completes the handoff, not the retrofit.
Receipt and escalation never transfer ownership. Acceptance alone changes the
case owner and chase owner. An accepted unfinished handoff cannot be overwritten.
The legacy `hand_over` method now creates an offer using the same checks.

Case detail and immutable `handoff_history` snapshots distinguish accountable
owner, destination role, proposed/confirmed receiver and chase owner. Urgency,
due date, next action and resident-update owner/commitment are independent fields;
missing values remain null. Due dates require an explicit timezone and normalize
to UTC. A pending resident-update commitment survives rejection, withdrawal,
acceptance, completion and replacement offers; handoffs cannot silently change
it. No message is sent, consent inferred or safety hold released.

`pending_handoffs` includes sent/received/escalated work for sender, recipient
and managers. Existing need-role projection holds notes, source references and
next-action text; contractors and unknown roles cannot use these workflows.
The coordination assistant's existing deterministic trigger includes all three
unaccepted states, without gaining action or approval authority.

These are local engineering controls, not approved operational escalation
timings. BG-010/OD-09 remains open: optional human-selected due dates and manual
escalation do not prove acceptance/escalation within approved periods. EXA-008's
24/48/72-hour fixtures are not a production SLA or statutory clock.

Semantic tests: `tests/test_handoff_lifecycle.py` runs on JSON and SQLite;
HTTP tests and a CI-only SQL Server replay live in `../api/tests/`.

## Building shared context (issue #75)

`buildings.py` implements the PRD FR-002 read model. Seed data can contain a
`buildings` list and each home case can carry an explicit `building_id`.
Building records contain exactly `id`, `name`, positive integer `version`,
`source`, `systems`, `dependencies`, `holds`, `works` and `costs`. Each category
is `null` when unknown or a list (including `[]` for explicitly none).
No building approval, resident evidence or home allocation fields are accepted.

* Systems contain `id`, `label` and `source`.
* Dependencies, holds and works add `owner`, `status`, `case_ids` and
  `package_ids`. Case IDs must identify homes explicitly linked to this building;
  package IDs must exist in procurement. `null` applicability is unknown,
  `[]` means none and nonempty lists are exact explicit references. Building
  membership and description text never establish package applicability.
* Dependencies and holds have recorded status `Open`, `Resolved` or `Unknown`;
  works have `Proposed`, `In progress` or `Completed`. These imported statuses
  are source assertions, not application-generated approvals or safety releases.
* Costs contain `id`, `work_id`, `amount_gbp` and `source`. They reference an
  explicit shared work, and GBP amounts are finite nonnegative decimal strings
  with at most two fractional places, bounded at GBP 100,000,000. No allocation
  formula, grant eligibility, spending authority or payment is inferred.
* Home `cost_allocation` entries (`shared_cost_id`, `amount_gbp`, `source`)
  remain on each home, as do documents, consent, technical, funding, quality
  and closure state. Allocations are not added to shared building costs.

Missing/invalid explicitly linked context and applicable unresolved
dependencies/holds block home advancement. New, reissued and corrective work
instructions check the exact package; unknown scope fails closed, an explicit
unaffected home/package does not block. Home readiness considers all applicable
packages. Hazard intake/referral and resident contact remain independent.
Unlinked legacy homes retain their existing behavior, not a claim that
building checks have passed.

JSON Store retains the document in `live.json`; SQL Store seeds, synchronizes
and persists it through the existing checked-document `DOCS` interface inherited
by MssqlStore, without new SQL or DDL. Existing live files and populated databases
are **not reseeded** from a modified seed; absent context stays unknown.
Loading real registers and governed updates/release authority are future work.
There is no building editor or release endpoint in this slice.

`tests/building_fixture.py` supplies a wholly fictional two-home block, two
packages, ventilation work and GBP costs. `tests/test_buildings.py` verifies
JSON/SQLite reopen, independent gates/evidence, explicit/unknown applicability,
role projection, blocked instructions, and uninterrupted hazard intake/referral.
API tests and staff navigation are documented in [api](../api/README.md#building-shared-context-issue-75).
Local SQLite evidence does not establish live SQL Server or Azure behavior.

## Datasets, fixtures and synthetic tools

The [synthetic needs inventory](../../docs/reference/research/retrofit-synthetic-data/needs-inventory.json)
and [scenario manifest](../../docs/reference/research/retrofit-synthetic-data/scenario-manifest.json)
bind each iteration's engineering review by inventory version/date and SN row.
Run `python3 -m unittest discover -s tests -p test_needs_inventory.py -v`
from this project to check that binding and negative mutations. This is a
recorded pre-build gate, not owner approval or full scenario acceptance;
partial/missing needs still require an owner volume/scope decision before
data-consuming build work starts.

### Generator coverage baseline (#167)

From the repository root, inspect the public routing metadata without reading
datasets or generating files:

```bash
python3 -m zava_forward.core.synthetic.coverage \
  docs/reference/research/retrofit-synthetic-data/needs-inventory.json
```

### Stock fabric and case references (#168)

Inventory row SN-01 remains partial. This iteration reuses PR 246's
`stock-fabric-v1` draw algorithm and seed 4820260930, moved into
`zava_forward.core.synthetic.stock_fabric`; it does not generate a second
stock register. The retained builder and EPC generator now import installed
core. Install with pip before invoking those support tools.

```bash
python3 -m zava_forward.core.synthetic.stock_fabric \
  --register /private/path/private-north-east-stock-register.csv \
  --cases /private/path/zavaforward.json \
  --out /private/path/new-stock-fabric-snapshot
```

Without explicit paths, the register is `private-north-east-stock-register.csv`
and the new snapshot is `stock-fabric/` under `ZF_DATA` (or
`~/.zava-forward/data/`). `ZF_DATA` can be a directory or the runtime seed file;
a file selects its parent. The CLI refuses repository destinations, symlinks
to them and nonempty snapshots. It checks the resolved destination and its
ancestors for `.git` files or directories, including when installed outside
a checkout and when the snapshot directory does not exist yet. It validates
inputs before creating output.
Snapshots contain `stock-fabric.csv`, `summary.json` and, with `--cases`,
`linked-cases.json`. No generated output belongs in git or an image.

Every fabric row carries `fabric_is_synthetic=true` and `is_synthetic=true`.
Build year/age band, dwelling type, construction and heating are modelling
assumptions, not company facts, survey results or EPCs. Summary weights/counts,
seed, v1 draw version, source revision and payload SHA-256 hashes are recorded.
Core revisions use full SHA-256; retained support manifests retain their
16-hex revision shape and now include the moved core dependency sources.

`resolve_cases` and `link_report` account for every case. Valid identifiers are
opaque nonblank strings without outer whitespace; no coercion or fuzzy repair.
Missing/invalid/not-found/ambiguous anchors produce explicit unlinked reasons.
Duplicate/invalid case IDs fail rather than collapse rows. Bulk fabric
generation rejects duplicate/invalid stock IDs. Each `case.stock_link` gives
`case_id`, nullable `stock_home_id`, status/reason, `shared_anchor`, synthetic
label and non-unit scope. A unique register reference is not verified dwelling
identity. Legacy `distinct_stock_homes` and `stock_homes_shared_by_cases` count
source anchors, not dwellings. Shared anchors stay explicit and valid as source
references; they never transfer consent, approvals or household identity.

`attach_fabric` refreshes only derived stock linkage/fabric, discards prior
derived `stock_epc` so it cannot outlive a changed link, and leaves operational
home fields, histories, consent and approvals unchanged. The retained builder
then rebuilds its synthetic EPC block for uniquely matched source rows; the
standalone CLI does not rebuild EPCs. Original input files are never overwritten.
Top-level reports remain seed metadata; per-case evidence survives existing
JSON-body SQL persistence without schema changes. Existing populated stores
are not reseeded or migrated automatically.

`tests/test_stock_fabric.py` verifies a connected fictional 60,000-row register
and retained 980-case builder, pre-move v1 golden values, diagnostics, CLI safety,
byte-level reproducibility, revision sensitivity and closed SQLite restart.
This is local engineering evidence only: actual private corpus reproduction,
owner inventory approval, unit reconciliation and real AI/SQL Server/Azure/human
application acceptance remain unverified. AI configuration and human
approval/resident-consent gates are unchanged; this data tool grants no authority.

### Coverage baseline results and limits

The deterministic JSON report includes every need, coverage totals, child
issues or justified deferrals, convention declarations and pending owner items.
Covered needs require delivered closure, and delivered closure requires covered
coverage. Invalid IDs, duplicate rows/references, blank rationale, malformed
issues, missing declarations or contradictory coverage/closure fail with a
nonzero exit and no JSON report. Missing needs and deferred closures instead
appear in `open_gaps` with a JSON report and exit 1, even with a child route or
deferral rationale. Partial needs with child routes do not trigger that exit.
`tests/test_generator_coverage.py` owns these semantic checks and CLI regressions;
the existing generator/determinism tests retain their output-contract checks.

`routing_shape_validated=true` means only metadata shape and consistency passed;
it replaces the overbroad `routing_validated` field. Issue existence is explicitly
`issue_existence=not-assessed`: a well-shaped reference such as `#99999` is
accepted without proving it exists. No GitHub lookup or complete issue registry
is used, and exit 0 is not evidence that child issues exist or are delivered.

Inventory v1.2.0 has two covered and eleven partial needs, with no missing
rows. A well-shaped route is not proof that the child exists or is delivered,
that generated records meet every convention, or that the owner approved scope. In particular,
the scale fixture's homes/events use a synthetic manifest label rather than
per-record `is_synthetic=true`; the inventory's universal declaration is not
fully evidenced. This tool does not change those historical snapshots.
Private regeneration, owner mapping/volume decisions, full SQL-scale tests,
real AI/Azure and human acceptance remain separate gates. Existing human
approvals, resident consent and AI release controls are unchanged. Dataset
generation still uses the existing tools and `ZF_DATA`, not this metadata CLI.

* Evaluation dataset registry (`src/agents/evals/registry.json`) lists every golden and
  evaluation dataset with version, owner and purpose; a test fails for an
  unregistered file in `mvp/evals/` or any `src/<project>/evals/` folder. The stock-scale fixture (60,000 homes, 600,000
  events, wholly fictional, seeded) is rebuilt with
  `python3 -m zava_forward.core.synthetic.scale_fixture` (moved in M3), writes to
  `scale-fixture/` under the per-user `ZF_DATA` folder (default
  `~/.zava-forward/data/`, outside the repository) and is never committed. Dataset owners are
  an open owner decision.
* Chat and memory fixtures (#172): `PYTHONPATH=src/agents/tests python3 -m
  chat_fixture` (test support, moved to `src/agents/tests` in M3) writes seeded, labelled-synthetic personas
  (two per PRD perspective, mapped to existing app roles), threads, memory
  items, opt-in states, exclusion probes, and isolation, expiry and deletion
  cases to `chat-fixture/` under the `ZF_DATA` folder. Case IDs come from the
  60,000-home stock. Retention is an illustrative 90 days, not a policy
  (BRD OD-45/OD-46 open); expectations are targets for #160 to #164.
* Sensor backfill (#177/#183): `python3 -m zava_forward.core.synthetic.sensor_backfill
  --estimate-only` prints the volume and size estimate for two years of hourly
  temperature and humidity across all 60,000 homes (about 1.05 billion rows,
  about 118 GiB as CSV, measured on a 20-home sample); `--homes N` writes
  sharded CSV, `sensors.csv`, `estimate.json` and `manifest.json` (seed,
  versions, climate source, parameters, hash) to `sensor-backfill/` under
  the `ZF_DATA` folder. Same seed gives identical bytes. Every row is
  `SYNTHETIC` with a stock home ID and `SENS-SYN-` sensor ID; `load_into()`
  validates and appends idempotently on sensor ID plus reading ID, and
  `SQL_DDL` is the Azure SQL schema. Open: Met Office and Environment Agency
  open data are not yet retrieved (climate is a labelled synthetic model),
  #110 consumer validation is mirrored by `validate_reading()` and must be
  reconciled when #110 lands, and a full-stock run needs a storage and cost
  decision.
### Register-backed sensor history (#177)

The explicit `--register` mode (`sensor-backfill-stock-v1`) reuses merged
`stock-fabric-v1`, seed 4820260930, rather than drawing unrelated dwelling
attributes or treating the scale fixture as the private stock. Supply a wholly
synthetic CSV with `synthetic_home_id`, `is_synthetic=true`,
`building_form_osm`, `locality_theme` and `monitoring_consent`. Building form and
locality use the same defaults as the fabric generator when absent. Monitoring
choices are exactly `granted`, `declined`, or `unknown`; missing/blank is unknown.
These are fictional fixture choices, never real resident consent or permission
to activate devices. Other columns are discarded, not copied or fingerprinted.
Do not supply private resident/device data.

Both estimate and write require explicit positive `--homes N` no larger than
the register. IDs are unique opaque strings, sorted before selecting the first
N, then monitoring choices are applied. Excluded homes are not replaced by
other opted-in homes. Declined and unknown homes have no sensor or readings;
an all-excluded subset produces zero-count metadata and an empty sensor CSV.
Coverage records register/selected/unselected/monitored counts, every selected
ID and each exclusion reason. Register anchors are not verified stock-unit IDs.

```bash
python -m zava_forward.core.synthetic.sensor_backfill \
  --register /private/synthetic-fixtures/stock.csv --homes 12 \
  --days 730 --as-of 2026-10-15 --estimate-only
python -m zava_forward.core.synthetic.sensor_backfill \
  --register /private/synthetic-fixtures/stock.csv --homes 12 \
  --days 730 --as-of 2026-10-15 \
  --out /private/synthetic-fixtures/new-sensor-history
```

Outputs must be outside any repository and in a new/empty nonsymlink folder.
`estimate.json` is written before reading shards, measured from up to 20 of the
actual granted sensors. The estimate includes dropout; it is not a guaranteed
upper bound or SQL storage quote. No full-stock write is an implied approval.
Manifest metadata records normalized allowlisted register SHA-256, source
fingerprints, fabric/adapter versions, window, coverage and all payload hashes.
`stock-fabric.csv` preserves selected v1 fabric plus fictional monitoring choices.
Changing only an ignored column or CSV row order does not change output.

The projection reuses the existing equations: loss = dwelling factor * age
factor * construction factor. Stock build year selects the existing age bucket.
Construction factors are Solid brick 1.15, Stone 1.20, Cavity brick 1.0,
precast concrete 1.10, Timber frame 0.90, partial-fill cavity 0.85 and full-fill
cavity 0.75. Heating schedules are seeded equal-choice morning/evening, all-day
or low; they are variation fixtures, not judgements of residents. All factors
and bounds are exercise assumptions, not calibrated physics or climatic facts.
The current equations and basic fault rates remain in `sensor_backfill.py`;
construction factors and exact fabric mappings are in `sensor_stock.py`.
No dated measure history is supplied: `retrofitted=False` is a modelling
assumption, not evidence that no works occurred, and no before/after claim follows.

Stock sensor IDs are `SENS-SYN-` plus full SHA-256 of the home ID; reading IDs
append epoch seconds. Home IDs must fit 128 UTF-16 code units. For a fresh
SQL Server database apply `STOCK_SQL_DDL` (`stock-reading-v1`, sensor
VARCHAR(73), reading VARCHAR(96), home NVARCHAR(128)), then call
`load_into(conn, output, create_schema=None)`. Legacy `SQL_DDL` and CSV payloads
are unchanged; do not use the narrow legacy DDL for stock mode. The loader
does not migrate databases. SQLite tests and portable conditional-insert checks
do not prove live SQL Server execution.

This is partial #177 delivery: #178-#183 remain open, not owner-deferred.
Historical Met Office/Environment Agency records and licence confirmation,
dated retrofit measures, full behaviour and configurable fault/truth classes,
and #110's future consumer validation are still missing. Owner #178 permits
clearly labelled synthetic climate as fallback; no CO2/energy is generated.
No AI review, hazard diagnosis, ranking change, resident action or approval
occurs in the generator. Existing AI release/human gates are unchanged.
`tests/test_sensor_stock.py` covers bounded 730-day histories, fabric/ID/choice
reconciliation, byte reproducibility, bounds, estimates, hashes and local loads.

### Existing reproducibility and plausibility evidence

* Reproducibility and refresh (#176): scale fixture v1.2.0 and sensor backfill
  v2 record seed, version, `as_of`, dependency-aware `generator_revision` and
  SHA-256 for every payload file. Both require a new or empty output folder;
  a repeat write to an existing snapshot fails without replacing files.
  Generate a new versioned destination rather than deleting live data.
  Source fingerprints are independent of Git HEAD, clock and output location;
  exact reproduction also requires the same Python/runtime environment.
  Scale `--as-of` is a snapshot label, not an event cutoff: its events remain
  calendar-year 2026 fixtures. Sensor `--as-of YYYY-MM-DD` is the exclusive UTC
  end of `--days` days; omitting it preserves the historical 2024-10-01 start
  (730 days ends on 2026-10-01). `--estimate-only` accepts the same window.
  Cadence must divide 1440 minutes and all sizes must be positive.
  Example, after setting `ZF_DATA` to a private folder outside the repository:

  ```bash
  python -m zava_forward.core.synthetic.scale_fixture --seed 174 \
    --as-of 2026-10-15 --out "$ZF_DATA/scale-fixture-2026-10-15-v1.2.0"
  python -m zava_forward.core.synthetic.sensor_backfill --seed 183 \
    --as-of 2026-10-15 --days 2 --cadence 60 --homes 12 \
    --out "$ZF_DATA/sensor-backfill-2026-10-15-v2"
  ```

  `tests/test_synthetic_determinism.py` checks every output byte, multiple
  sensor shards, source/hash metadata, window propagation, unchanged historical
  payloads and refused refreshes. This wholly fictional stock-scale fixture
  is not the private OSM-anchored stock register. That generator remains absent;
  neither these tests nor the sensor sample establishes full-stock feasibility.
  The [refresh cadence and approval policy](../../docs/reference/research/retrofit-synthetic-data/README.md#determinism-manifests-and-refresh-policy-2026-10-15)
  is still proposed. These tools confer no approval, resident consent,
  live SQL reset authority or permission to replace private tenant bindings.
* Sensor plausibility tests (#191): `tests/test_sensor_plausibility.py` runs in
  the existing MVP CI unittest step over 150 stock homes for two years. It
  fails on out-of-bounds or flat-line series, checks seasonal and diurnal
  structure and humidity by age band and dwelling, and checks that dropout,
  outlier and stuck fault rates match the configured injection. Expected
  outdoor ranges are labelled exercise values until the climate source in #178
  is retrieved and recorded (open item).

## Law store (ADR 0005, phase 1)

`src/core/src/zava_forward/core/lawstore.py` loads the dated snapshots in `docs/reference/regulatory/`
into append-only tables (`reg_source`, `reg_version`, `reg_provision`, `reg_gap`) and
writes each snapshot once, content hashed, through a snapshot interface. The target is
Azure only: `ZF_LAW_STORE=mssql` uses Azure SQL (the `ZF_SQL_*` settings of the main
store; append-only ledger tables when the database is ledger enabled, otherwise an
append-only trigger) and `AzureBlobSnapshots` (`ZF_LAW_BLOB_ACCOUNT_URL`,
`ZF_LAW_BLOB_CONTAINER`, `DefaultAzureCredential`; writes never overwrite). SQLite and a
local folder (`ZF_LAW_DB`, `ZF_LAW_BLOBS`) are local test doubles only. Seed with
`python -m zava_forward.core.lawstore REGULATORY_DIR DB_FILE BLOB_DIR` (or
`ZF_LAW_STORE=mssql python -m zava_forward.core.lawstore REGULATORY_DIR`); a changed file
becomes a new version and nothing existing is altered. Partial sources carry
`completeness: partial` and results say so. Leasehold, complaints handling, TrustMark
and licensed PAS 2035 are gaps answered as "no source held". The keyword index
(`rebuild_index`) is derived from SQL. The same suite runs on SQL Server in the CI
`mssql` job (`test_lawstore.MssqlStoreTests`). Open items: the Azure Blob container
immutability (WORM) policy and the Azure SQL deployment are infrastructure and are not
verified here; the Azure Blob client is tested only against a fake container. The
read-only viewer at `/law.html` and the source/search routes under `/api/law/`
serve staff roles with no AI; the separate [rule-card API](../api/README.md#rule-card-approval-api-211)
adds controlled exercise writes. Seeded
versions are `not_reviewed` with owner "to be named"; this is a reference copy, not
legal advice or approval. Seed metadata is `src/core/src/zava_forward/core/law/law-source-register.json`.

## Rule cards (ADR 0005, phase 2)

`src/core/src/zava_forward/core/rulecards.py` (moved from `mvp/` in M1 of #199) holds versioned rule cards in append-only tables
(`rule_card_version`, `rule_card_event`, `rule_card_review`, `rule_card_review_event`,
`rule_card_check`) with a draft, approved,
active, held, retired lifecycle. A card is drafted by the `rule_author` role and only
its named `rule_owner` can approve, activate, hold, release or retire it; an author
cannot approve their own card. Versions, approver, approval date and effective dates
are retained. `source_changed` records an open review item (RULE-021, AC-068) naming the
affected card, active version, requirements and tests, source versions and effective date,
and never alters an approved card. `assess_review` lets only the card's named owner record
the interpretation, tests, effective date, notification, rollback and any hold; it never
activates a rule, so activation still needs propose, approve and activate by named humans.
`LawStore.rules` reuses this store on the existing SQLite or SQL Server adapter.
Initialization idempotently adds the two draft exercise seeds. Public mutations
hold the shared adapter reentrant lock and a database write transaction before
version/state reads, including supersession and assessment holds; a failure
rolls back the whole mutation. SQLite uses its writer lock, SQL Server reuses
the existing cross-replica application lock. Rule IDs are explicitly allocated
inside that transaction, without SQLite-only identity syntax or pagination.
The existing SQL Server backend initializes append-only ledger tables (when
enabled) or append-only triggers. Local adapter-contract tests are not a live
SQL Server run.

Changed source ingestion now adds review records inside the same transaction as
source/provision rows. First ingestion and unchanged retries add no review.
Card contents, approval events and snapshots are never overwritten. The derived
keyword index is rebuilt after commit and repaired by unchanged retries; an
index failure does not undo already committed source/review evidence. Failed
ingestion can leave an unreferenced immutable blob; it is not deleted or treated
as approved evidence. Existing SQLite rule histories and identity strings remain
unchanged on reopen. Direct core callers remain trusted internal code; HTTP
authority is enforced by the API, never by accepting request role strings.

The card-to-requirement and test trace for the two seed cards is a static exercise map;
unmapped cards are flagged for the owner. The two seed cards (hazard awareness clock, automated decision
safeguard) remain unapproved drafts until a distinct named exercise owner acts;
any approval is explicitly simulated. They are not
law or real approval, and the owner, clock durations and citations remain open items
for named Compliance and DPO approval. The API binds separate Entra rule
capabilities to a unique provisioned identity; actual tenant assignments, human
approval of specific cards and the rule-card UI remain open. The bounded
exercise engine below does not supply those approvals.

## Source change monitoring and review (#213)

`source_monitor.SourceMonitor` extends the delivered #127 review workflow on
the #210 law store, #211 rule cards and #212 deterministic evaluator.
It is a bounded offline exercise, not a live legal monitoring service.
Juan Manuel Servera is the exercise Legal, Compliance and DPO owner.
Approval-bearing records explicitly say `simulated` and `EXERCISE ONLY`;
neither agent output nor a fixture is real human legal approval.

The store reuses the law SQL adapter, immutable snapshot store and rule-card
transaction. Four append-only tables retain configuration revisions,
observations, candidate changes and lifecycle events. SQLite triggers enforce
local append-only behavior. SQL Server uses ledger tables when enabled,
otherwise denial triggers, with the existing transaction-scoped exclusive
`zavaforward_write` application lock. Only the local adapter/SQL contracts have
been exercised here, not a live SQL Server or Azure run.

### Detection and bounded impact

`configure(source_id, cadence_days=..., likelihood=..., rationale=...,
impact=..., actor=..., role=...)` records a positive 1..366-day interval, exact
`High`/`Medium`/`Low` likelihood, the register rationale and explicit lists of
`requirements`, `journeys`, `tests` and `communications`. The source must
already exist. Configuration is owner-controlled and append-only; repeating
the same configuration is idempotent. Use the
[register](../../docs/reference/regulatory/README.md#change-assessment-and-monitoring-register)
to select the interval and rationale, including increased cadence around
commencement; the code does not guess an interval from prose or turn
likelihood into legal importance. Unconfigured sources are not monitored.

`due(source_id, today)` measures cadence from the last successful retrieval,
not the last attempt. Failures remain recorded but do not reset the timer:
a due source stays eligible for the next run, including the next day. A source
with no successful observation is always due. A successful retry starts a new
cadence interval; success is not verification. Dates before the latest attempt,
including a failed attempt, are rejected.

`observe` accepts explicit UTF-8 bytes, publication metadata, provenance,
discovery method and an exercise date, or an explicit retrieval error.
It compares hashes/metadata against the retained law-store baseline and stores
content, metadata or retrieval-failure review items, including a capped
200-line unified difference with an explicit truncation flag. Full candidate
bytes remain in a content-addressed snapshot alongside, not over, the baseline.
Missing observations are failures, not successful checks. Scraping, feed and
metadata results all start unverified. Changed bytes do not inherit the old
source's completeness; an explicit completeness assertion still requires
owner review.

Candidates never enter `reg_version`, `reg_provision` or the search index.
Detection does not alter a card or its lifecycle. Exact canonical source IDs
match cards, not source-name substrings. Each change freezes matched card
versions/states, requirements, journeys, tests and communications and links the
existing per-card review records by candidate/configuration IDs. The source
version on those reviews is the actual baseline, not an invented published
candidate version. Empty impact fields or no matched cards are explicitly
unmapped; nonempty lists establish completeness only for that bounded
configuration, not exhaustive legal impact analysis.

### Simulated owner release and rollback

These are trusted in-process functions, not an authenticated public API.
`actor="Juan Manuel Servera"` and `role=rulecards.OWNER` are exercise call
inputs, not proof of identity. No monitor approval/configuration/activation
endpoint was added; the role endpoint inventory is unchanged. Provisioned
HTTP card identities keep their existing independent author/owner boundary.

1. The distinct author drafts an immutable replacement with an executable
   contract; the named card owner separately approves it. Existing active or
   held cards can instead receive an explicit `no_change` disposition.
2. The exercise owner calls `monitor.approve` with provenance/completeness
   review evidence, interpretation, notification and rollback plans, effective
   date, every affected card's exact target and local regression cases. Failed
   or explicitly partial retrievals and incomplete impact lists cannot pass.
   Existing linked card reviews receive the corresponding simulated owner
   assessment. This does not publish a source or send communications.
3. `monitor.regress` runs the frozen cases through the existing deterministic
   evaluator after approval, retaining observed/expected results and pass/fail.
   Every configured test ID and target must be covered. Cases contain
   `test_id`, `card_id`, `facts` and `expected` result states. They are bounded
   data, not Python expressions, arbitrary commands or a Python-suite runner.
   Configured IDs identify these regression cases; listing a suite path alone
   is not evidence that that suite ran.
4. `monitor.activate` is another named-owner action. It requires the latest
   run for the exact approval to pass and refuses dates before the effective
   date, candidate date or regression. It rechecks source/configuration,
   candidate integrity, exact card histories, evaluator version and current,
   complete, reviewed citations under the transaction. A failed rerun cannot
   reuse an older pass; material observations invalidate approval even if
   bytes later revert. Harmless duplicate observations do not.
5. Replacement activation cannot supersede a human hold. A separately
   approved/regressed `no_change` decision can release that exact held card.
   Direct card `activate`/`release`, including alternate versions, cannot
   bypass monitoring once a card has a detected change.
   A newly drafted card citing a changed source also joins the gate and
   requires a refreshed observation. If a card cites multiple changed sources,
   activation fails closed: coordinated multi-source release is not supplied
   by this offline slice and one source's approval cannot stand for another.
6. `monitor.rollback` requires the same owner and a reason. It atomically
   compares the exact activation histories and restores captured eligible
   prior active versions, or retires a replacement where none was active.
   A no-change hold release can be rolled back to the captured hold.
   Intervening holds, retirements, new card versions, repeated rollback or
   expired/ineligible prior versions block rollback rather than undo later
   human decisions. All earlier versions, dates and events remain.

Ordinary unmonitored card activation now also refuses a date outside the
card's effective/retirement window, preserving the previous active version
until an eligible replacement is actually activated. Detection never delays
independent emergency, resident or hazard routes.

Publication of a candidate as a verified law-store version is deliberately
not implemented. Positive release tests use clearly synthetic reviewed
baseline provisions already held by the law store. A card citing an
unpublished candidate, stale, missing, partial or unreviewed provision cannot
pass runtime-equivalent eligibility. This offline rule-release demonstration
is not proof of activating a newly published legal interpretation.

### Acceptance audit

| Issue #213 acceptance criterion | Bounded local result | Unmet boundary |
| --- | --- | --- |
| Differences stored with affected cards, journeys, tests and communications | Met for configured fixtures: retained differences, exact card histories, source versions, impact lists, owner and linked reviews | Live discovery and exhaustive legal/journey/template impact mapping are not delivered |
| Scraping is unverified until provenance and completeness review | Met locally: discovery is unverified; simulated owner evidence is required and retained separately | No actual official provenance/currentness or human legal review is claimed |
| Detection never overwrites approved cards | Met locally: candidate isolation, immutable snapshots/cards and retained lifecycle histories | Live storage permissions and immutable Blob policy remain unverified |
| Approval, regression, effective-date activation and rollback | Met for simulated single-source existing-source executable cards, including failures, holds and atomic rollback; overlapping changed sources fail closed | Coordinated multi-source release, verified new-source publication, actual human approval, operational regression/accessibility/privacy/communications suites and live activation remain unmet |
| Configurable cadence per source | Met locally: explicit versioned intervals, due boundary and bounded orchestrator pages | No hosted regulatory timer, official adapter, missed-run alert or adaptive calendar policy is deployed |
| High/Medium/Low likelihood per register | Met as an exact validated enum with retained register rationale | No automatic register-to-runtime policy synchronization or owner ratification is claimed |

`tests/test_source_monitor.py` covers local detection, authority, provenance,
coverage, failure/staleness, effective dates, no-change/holds, actual runtime
eligibility, restart, concurrent adapters, append-only SQL contracts and atomic
multi-card release/reversal. Run from `src/core`:

```bash
PYTHONPATH="$PWD/tests" /tmp/zf164/bin/python -m unittest discover -s tests -p 'test_source_monitor.py' -q
/tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy
```

The [offline job recipe](../orchestrator/README.md#offline-source-change-job-213)
does no scraping and has no approval or activation command. Refs #213; these
local results do not close the issue.

## Deterministic checks and alerts (#212)

`rule_engine` reads persisted SQL case bodies and row versions, never a model's
fact snapshot. It has no model, resident-message, awareness-write or hold-release
interface. Existing hazard intake/referral and independent human hold release
remain authoritative. A bounded `clear` means only that particular check passed,
not that a home is compliant, safe, or released.

New draft cards may include an optional immutable `check` object. Its exact
contents appear in card history before the existing distinct named-owner
approval and activation. No contract is attached to old versions or seed drafts.
The two allowed kinds are:

| Kind | SQL case evidence and deterministic result |
| --- | --- |
| `hazard-awareness-clock` | Explicit `hazards` list; an empty list is not applicable. Each open record needs a valid, non-future timezone-aware `aware_at`, report `source`, known `priority` and explicit `released` boolean. `hours` is an owner-supplied integer 1..8760, not a guessed statutory period. Due time is awareness plus those elapsed hours; at due time the result is breach risk. Within `attention_hours` before due it is attention; before that it is clear for this clock only. Missing duration/evidence is unknown. Evidenced independent human release can be clear, but the checker never changes a hold. |
| `automated-decision-safeguard` | Explicit `automated_decisions` list; missing is unknown, empty is not applicable. An explicitly non-significant entry is not applicable. Significant entries need named `decision_owner` and proposal `source`; explicit `state: pending` is attention. `state: recorded` additionally needs human `evidence` and a non-future timezone-aware `decided_at` to be clear. Missing or contradictory evidence stays unknown. This field has no general-purpose writer or AI write path in this slice. |

For example, an exercise author can propose
`"check": {"kind": "hazard-awareness-clock", "hours": 48, "attention_hours": 24}`.
Those numbers are an illustrative fictional contract, not legal advice or
approved operational timings. The decision kind accepts only `kind`, no clock.
Unknown keys, expressions, model awareness dates and suppression flags are
rejected. Prose clocks are never parsed into executable rules.

Only an active, human-approved card inside its effective/retirement dates is
executable. A newer draft does not disable a prior eligible active version.
Every citation must be an exact held provision ID, such as
`source-id@v1#0001`. Missing citations, incomplete/unreviewed sources or
superseded versions prevent clear and return unknown. Consultations, historical
sources and future effective dates return `not applicable` and never fire as
active controls. These are local metadata checks, not verification that
legislation is currently correct.
Seed references and their review state remain unchanged.

Checks retain card/version/status, exact citations and source statuses, case
revision/evidence pointers, input hash, journey step, UTC evaluation time, safe
action, named decision owner and clock. All results, including throttled ones,
are retained. Checks, alert publication and the checkpoint commit atomically in
the law-store SQL adapter. Tables are append-only ledger tables on a
ledger-enabled SQL backend, otherwise protected by append-only triggers.
No SQLite replace/ignore/automatic-ID syntax is added.

Data/step retries use stable case-revision, card/source fingerprint and engine
version keys; schedule retries add a UTC minute bucket. Replaying a key returns
its original persisted time/results, even later or after restart. API case
mutations evaluate after commit; schedule pages revisit persisted cases to
recover missed or failed dispatch. Intermediate revisions that were never
checked are not reconstructed. Supply trusted SQL/law configuration, then run:

```bash
python -m zava_forward.core.rule_engine --limit 100 --after ""
```

Run successive pages using `next_after` until a page is empty, then restart at
the beginning on the next scheduled sweep. The maximum page is 100; the
existing store's backend-specific pagination is reused. The command does not
install a timer or change a deployment. A failed page exits unsuccessfully;
retry from the previous page token. Already committed home checkpoints replay,
and a later sweep advances the clocks.

Alerts group by explicit home ID (case ID when no separate home ID is held),
then rank by due time, harm, and stable IDs. Home groups rank by their first
alert. Attention publication is limited to once per 24 elapsed hours for a
home/card/step/evidence item; it never suppresses evaluations or breach
escalations. Latest attention/unknown episodes replace their older visible
copies; clear/inactive checks remove those advisory copies from the open view.
Unresolved breach risks remain visible across changes, holds and retirement,
labelled with their original evaluation and current-control availability.
Only the exact named owner with trusted `rule_owner` capability can acknowledge
or record outcomes/classifications. Breach outcome requires acknowledgement;
neither action changes the underlying hazard hold. An unresolved underlying
risk can raise a new alert after a recorded outcome.

False-positive and confirmed classifications are append-only and mutually
exclusive per alert, with total/classified/unclassified counts and
`false_positives / classified` (null for zero classified alerts). This is an
owner-classified fatigue indicator, not measured clinical/legal accuracy.
Classification never suppresses checks or substitutes for breach acknowledgement
and outcome. Read scopes and HTTP behavior are in the
[API guide](../api/README.md#deterministic-step-alert-api-212).

Local tests use constructed SQL facts and explicitly simulated approvals only.
Issue #329 regressions assert exact source-gating results and retained citation
metadata, with no evaluator call or persisted alert for ineligible sources.
Attention tests use distinct cases on the same home and changed due-time
episodes on one case: checks/checkpoints persist while publications are
suppressed just before 24 hours and allowed at exactly 24 hours. Independent
home/card/step/item keys and cross-case breach escalation have positive controls.
Nine in-memory mutations of source gates, shared throttling, its boundary and
each key dimension fail the intended assertions. These tests exposed no
production defect; the existing rule-engine implementation is unchanged.
Actual legal approvals, a deployed timer, step UI, real staff precision and
comprehension trials, operational retention policy, continuing 60,000-home
acceptance and live SQL Server/Azure verification remain unmet. Refs #212,
not issue closure or production acceptance.

### Issue #212 acceptance audit

Statuses below describe observed local engineering evidence only.
`test_rule_engine` is in core/tests; `test_rule_alerts` and the endpoint
inventory are in api/tests. No row grants operational or legal approval.

| Issue acceptance criterion | Local status and evidence | Unmet boundary |
| --- | --- | --- |
| Five cited results and status | Met locally: exact-threshold, missing-evidence, explicit empty applicability and cited source/status tests | No genuinely approved operational card or live source-currentness verification |
| Missing evidence unknown, never clear | Met locally: absent/invalid/future awareness, source, release and decision evidence tests | No fabricated source or human evidence fills gaps |
| Future/consulted rules never active | Met locally: future card/source dates, consultation, historical, partial/unreviewed and superseded source tests | No legal currentness claim |
| Model never sets awareness or suppresses checks | Met locally: no model dependency/write interface; unsupported spec/body fields denied; SQL facts unchanged by checks | No real-model safety evaluation is claimed |
| Safe action, owner, clock; breach acknowledgement/outcome | Met locally: payload assertions, exact-owner/capability and acknowledgement-before-outcome HTTP tests | Real decision-owner delegation and tenant assignment not evidenced |
| No alert sends a resident message | Met locally: no send interface or messaging side effect; HTTP lifecycle preserves contact records and holds | Human communication stays in its separate existing workflow |
| Home grouping, clock/harm ranking, attention limits, false positives | Partial end-to-end: local grouping/ranking, 24-hour publication and retained-classification tests pass | Missing distinct home IDs isolate cases instead of inventing cross-case home identity; no real staff precision/false-positive trial |
| Safety routes work with engine down | Met locally: absent/evaluation/persistence failure HTTP tests preserve emergency intake/referral and show unknown/manual route | No Azure outage exercise |
| Idempotent and checkpointed | Met locally: exact retries, later-time retry, restart, concurrent adapters, atomic rollback and scheduled catch-up/page tests | No deployed timer or live SQL Server recovery evidence; unevaluated intermediate revisions are not reconstructed |

The API makes alerts available at their recorded journey step, but a workbench
alert component is not delivered. Together with real approvals, hosted
scheduling, staff trial and live-platform evidence, this remains an explicit
unmet end-to-end acceptance boundary rather than an issue-closing claim.

## SQL store

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

## Azure SQL store

`ZF_STORE=mssql` uses `mssqlstore.py`, a T-SQL dialect over the same `SqlStore`
logic, with the pinned `mssql-python` driver (`src/api/requirements.txt`, hashes
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

`src/core/src/zava_forward/core/governance.py` records, and never decides, the pilot governance in the existing store (JSON or SQL, so it survives a restart). Managers use `GET /api/governance` and `POST /api/governance/{protocol-freeze,protocol-approve,benefits-record,benefits-approve,release,breach,restart}`. No AI assistant, ranking or tool has any part in it.

* Protocol (RULE-019, AC-062): a version freezes all thirteen required fields. A different person approves it with the OD-36 DPIA and lawful measurement-basis references. A change needs a reason and a new approval. `capture_gate()` keeps Phase 0 capture closed until the latest version and the BG-011 register are approved.
* Benefits register (BG-011, OD-18): event definitions and the MDE are recorded. `target_verdict` never returns pass or fail when the MDE is missing or exceeds a target (20% cycle time, 25% coordination hours); it returns "Not assessable" or "Interval estimate only".
* Release decisions (RULE-020, AC-063): each phase (Phase 0 capture, Shadow testing, Live pilot) and tranche has a Release or Withhold record with requirements, evidence, unresolved issues, cost and risk envelope reference and named approvers. Releasing Phase 0 capture needs the capture gate; Shadow testing needs entry evidence, and Shadow testing and Live pilot need Phase 0 capture released first.
* Guardrail breach (RULE-024, AC-078): `breach_record` (managers, quality inspectors and building safety liaisons, so a hazard-aware role can raise a breach without waiting for a manager) pauses the home, work package, archetype or workstream. `breach_restart` needs a different person, the OD-35 authority reference, accepted remediation evidence and a Release decision recorded after the breach. `guard_case_event` calls `require_not_paused` (home by case id or address, archetype by home type) and, for cases flagged `pilot`, `require_capture_open` in `log_call`, `set_decision`, `advance` and `return_case`; emergency and statutory hazard response continues outside any pause.

Tests: `tests/test_governance.py` (JSON and SQL stores, labelled synthetic demonstration values). Open items, not invented here: the real OD-18 definitions and MDE, the OD-36 DPIA and lawful basis, the OD-35 named authority, actual approvers, how cases are enrolled in the pilot cohort (the `pilot` flag), pause scopes for work package and workstream, and extending the guard to the remaining case workflows. The RAI closure registers in the issue (eleven residuals and eleven unassessed checks, a fresh current-source assessment, owner acceptances) are not delivered or claimed closed by this change; every item stays proposed or insufficient until qualified owners and fresh evidence exist, and live use stays blocked.

### Per-year ledger digests, load check and recovery drill (issue #114)

* `python -m zava_forward.core.ledger --seal-years` writes one immutable `year-YYYY.json`
  digest per completed year (entries, first link, head); `--by-year` verifies every
  year on its own, the links between years and each sealed digest, and reports a
  dropped sealed year. A self-consistent rewrite of a sealed year is caught only by
  its digest, so those files belong in the immutable Blob container. Proven in
  `src/core/tests/test_recovery.py`; run the scheduled `--by-year` check before relying on the ledger.
* `python -m zava_forward.core.synthetic.loadcheck --data zavaforward.json --homes 60000` runs the
  NFR-002 mix (five sessions, two writers) against the configured store and prints
  p50/p95/max per class. Local SQLite on 2026-10-15 over 60,000 labelled synthetic
  homes for 30 s: list p95 0.28 s, detail 0.30 s, write 0.33 s, no errors (limits 1 s,
  1 s, 2 s). Open items: the same run against Azure SQL, dashboard and import preview
  classes, and cost (needs Azure meter rates and measured vCore time).
* `src/core/src/zava_forward/core/recovery.py` erases a resident's personal fields and keeps a
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

## Per-user chat thread storage (issue #160)

`chatthreads.py` stores chat threads and messages per user (ADR 0004 decision 3), behind the `Store` interface: the
in-memory `Store` keeps them in its live file, `SqlStore` and `MssqlStore` in the additive, idempotent `chat_thread` and
`chat_message` tables (Azure SQL in deployment, SQLite for local tests). A thread carries the server-derived owner,
case reference, assistant task and version, and model identity; a message carries its role, evidence references and,
for assistant messages, the model. `chat_create_thread`, `chat_add_message`, `chat_list_threads`, `chat_resume`,
`chat_archive` and `chat_delete` always filter on the owner (another user's thread is reported as not found). Writes use
the thread row version and raise `ConflictError` when a caller's expected version is stale. The audit ledger receives
metadata only (thread id, case, counts, role), never message text or title, so deleting a thread leaves the chain intact.
Not in this slice: the panel (#159), model calls, memory (#161), isolation hardening (#162), retention and export
(#163; retention policy is unlocked for the exercise, legal retention lock deferred). Fixtures are synthetic.
Tests: `tests/test_chatthreads.py` (in-memory and SQLite parity; `MssqlChatThreads` runs with `ZF_TEST_MSSQL=1`).

## Chat and memory isolation (issue #162)

`chat_isolation.py` sits on the #160 repository and #163 privacy rules and adds no tables. Endpoints (staff roles only; contractors and unknown roles are denied, default deny): `GET/POST /api/chat/threads`, `GET /api/chat/threads/{id}`, `POST /api/chat/threads/{id}/messages|archive|delete`, `GET/POST /api/chat/memory` (the POST needs `task` and a prior opt-in), `GET /api/chat/memory/status?task=`, `POST /api/chat/memory/opt-in|opt-out|erase|global|task` and `POST /api/chat/memory/{id}/edit|delete` (the #285 lifecycle; `global` and `task` switches are administrator-only), `POST /api/chat/breakglass`. The owner is always the authenticated user; request fields such as `owner` or `email` are ignored, and another user's thread, or a case outside the caller's scope, is reported as not found (404, so existence cannot be probed). Prompts carry the masked question and only memory from `privacy.prompt_memory` (opt-in, switch-gated, labelled non-authoritative); stored model replies are redacted like user messages.

* Every turn re-reads the user's current role and re-projects the case through the same `store.detail` projection as the case card, so a changed or revoked role applies on the next turn.
* The prompt holds only the caller's own thread, own unexpired memory and the projected case, each inside `UNTRUSTED` blocks with the block delimiters neutralised. The channel has no tools; replies are text only, labelled as unapproved, and a reply carrying tool-call or record-change syntax or a withheld reason is replaced by a refusal.
* Break-glass is refused until `CHAT_BREAKGLASS_REF` (owner policy reference) is recorded and the caller role is named in `CHAT_BREAKGLASS_ROLES`. When allowed it needs a purpose, expires within 60 minutes, returns counts and ids only (never content) and writes granted and refused attempts to the audit ledger.
* Open items: the break-glass and administrator content-access policy is an owner decision (BRD OD-46) and is not decided here; whether contractors may use chat is undecided (denied); the injection set in `src/api/tests/test_chat_isolation.py` is a recorded regression set, not evidence of complete coverage; real-model behaviour was not exercised.

Tests: `src/api/tests/test_chat_isolation.py` (extends the role matrix; replays the synthetic isolation fixture cases).

## Service continuity, versioning and export (issue #122)

`continuity.py` adds a persisted AI suspension (whole release or one registered task), a restart gate, a versioned
change register and a supplier-independent evidence export. Synthetic demonstration data only.

* Suspend: `POST /api/continuity/suspend` records scope, incident owner, containment, constructed communication
  (never sent), and the affected queued, leased and ready proposals, and raises an epoch.
* Enforcement: the epoch is read on the caller's own SQL connection at invoke, scan, claim, dispatch, complete and
  review, and shown in list and detail views; it does not depend on disabled buttons. In-flight provider calls may
  finish and stay charged or unknown; late results are quarantined and never actionable. No remote cancellation or
  exactly-once billing is claimed.
* Manual fallback: suspended AI paths return the workflow template with the reason; case work, resident challenge
  and hazard response are unaffected. Reject stays available.
* Restart: `restart-propose` (corrective evidence) then `restart-decide` by a different manager, with the current
  epoch and a named authority reference. Self-approved, stale, replayed or unauthorised restarts fail. The authority
  reference is recorded, not verified.
* Changes: `POST /api/continuity/change` and `change-reverse` version model, rule and configuration changes with an
  evaluation result (a failed evaluation is Blocked); reversal is a superseding record.
* Export: `GET /api/continuity/export` returns `zf-evidence-export/1` with a digest and ledger chain checked offline by
  `continuity.verify_export`, with no AI supplier needed. The bundle carries `complete` and `incomplete_reasons`: when
  the 5,000 assistant-proposal limit is hit it is flagged incomplete (with total and exported counts) and
  `verify_export` reports it not valid, so a truncated bundle is never presented as whole. The bundle records the ledger
  head (count and hash) and any sealed digests; `verify_export` fails when the entries do not reach that head. A
  recorded head can be rewritten together with the entries, so pass `expected_head` from a copy held outside the
  application (an immutable digest) to detect that.
* JSON store: AI task suspension, restart gating, the change register and export are enforced and tested on the JSON
  store. The five assistants are durable SQL only, so the bundle states `assistants.supported: false` and exports no
  assistant proposals there; assistant suspension on a JSON store is unsupported.
* Open owner items: witnessed authorised drill, recovery and response limits, supplier contract terms, Azure SQL
  drill evidence, interface identifier mapping, and the named restart authority.
## Synthetic home-specific cited chat (#214)

`regulatory_chat.RegulatoryChat` is the API-owned offline retrieval and storage
boundary. It reuses existing `LawStore`, approved exercise cards and
`citation_eligibility`, not a new vector store. The agents callback receives only
a bounded data bundle; it has no database, write tool or provider connection.
Only active simulated cards with complete, reviewed, current-version,
non-future provisions support an answer. Seeds stay unapproved. Held,
retired, missing, partial and unreviewed sources cannot support an answer.
Changed approved-source versions and same-purpose cards with differing
safe-action/clock text are flagged as potential conflicts, not reconciled.
This is not general semantic conflict detection or a live source-currentness check.

The supported lookup purposes are hazard sources and automated-decision sources.
Hazard facts are restricted further to Building Safety Liaison, Resident Liaison
Officer and Programme Manager roles: at most two hazards' enumerated category
and priority, after the existing case projection. No vulnerability, health,
address, resident name, contact, report narrative, memory or previous assistant
answer is retrieved. Other roles receive source excerpts and an explicit
missing-facts statement. Automated-decision lookup currently retrieves sources
only; it does not infer a decision or home applicability.

Fact citations bind the case/path, value and observation time by hash, with
unknown effective date; law citations retain immutable provision/version,
status, effective/retrieval dates and hash. Excerpts are limited to 350
characters and explicitly mark truncation and unverified live currentness.
The complete `regulatory-chat-v1` envelope is stored in the existing isolated
assistant message, with string IDs in evidence. Questions are limited to 1,000
characters, sources to four, cards to two and facts to four. An envelope over
the existing 8,000-character message limit fails before writing; it is never
silently truncated.

Answer pairs and explicit selected-turn doubt copies use single chat-repository
transactions. JSON restores a pre-image on failure; SQLite uses rollback.
A copied pair lives in the uniquely provisioned Juan Manuel Servera exercise
owner's own isolated thread, with a sender receipt and idempotent retries.
The sender's other messages and memory are not shared. Both current roles/case
rights are checked; SQL provisioning is read freshly, not from the legacy
staff cache. Trusted-proxy roles remain claim-derived instead of being replaced
by a wider staff-register role. Historical reads deny changed roles instead of
replaying wider content. SQL turn/referral metadata audit now commits in the
same transaction as the messages and receipt; an audit failure rolls back both.
The JSON file store alone retains the post-commit separate-ledger error boundary;
it is not evidence of SQL audit atomicity. Audit holds metadata only.
Copies have independent thread ownership/deletion; deleting the sender's
thread does not delete the explicit owner's copy. No email or live delivery
is implied. No rule-engine alert, consent, safety hold or case fact is changed.

Admission requires `ZF_REGULATORY_CHAT=synthetic-demo`, omitted/test/development
`ZF_ENV`, the loaded dataset's `regulatory_chat_exercise=synthetic-demo`
declaration (SQL `meta` key or JSON root) and all three existing privacy
references prefixed `SYNTH-`. These are simulated exercise references, not
actual privacy approvals; the marker is a trusted fixture declaration, not a
detector of real data. Do not set it on private or operational data. Unknown or
production environments deny. No automatic dataset marking or owner
provisioning is performed. Ordinary chat and memory gates are unchanged.

### Regulatory privacy and audit (#217)

`regulatory_privacy.retention_report` aligns own-thread review metadata with
the existing `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS` settings. Without
both, periods and due status are unknown. For synthetic reporting, both must
be valid, the reference must start `SYNTH-` and days must be 1..36500 (technical
input bound, not a legal period). Review due is creation time plus days,
inclusive at the exact due instant, and includes archived regulatory threads.
No content is loaded, no records are deleted and no DPO approval is inferred.
Other source/card/check/alert/audit periods stay explicitly unknown. This is
not a complete retention or rights implementation; the
[draft DPIA](../../docs/reference/research/chat-memory-dpia.md#regulatory-assistant-dpia-draft-for-dpo-review-2026-10-16-refs-217)
requires DPO review and remains unapproved.

Rule/card approvals, source reviews, checks and alerts already retain append-only
SQL history. SQL chat turn events now include actor/role, case/thread/sequence,
model, citation IDs and answer hash, never question/answer/excerpt/health content.
Referrals retain receipt and decision-owner linkage, once per selected pair.
Rollback-after-audit-insert and reopen tests cover the chain head and data.
Metadata and linkable hashes are not anonymous; DPO retention review is still needed.

Engine contract version 2 requires nonempty `reasons` as well as named human,
source, evidence and decision timestamp before a significant-decision check is
clear. An evidence ID alone, absent reasons or whitespace reasons stays unknown.
Version 1 checkpoints are not reused. This is a bounded evidence check, not
proof of a real human decision or UK GDPR compliance.

Run the synthetic core proofs with an installed editable package, from the
repository root:

```bash
PYTHONPATH="$PWD/src/core/tests" python3 -m unittest \
  test_regulatory_chat test_chat_panel test_chatthreads test_rule_engine \
  test_rulecards test_source_monitor -q
```
