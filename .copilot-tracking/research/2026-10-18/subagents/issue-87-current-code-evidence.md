# Issue 87 current-source evidence lane

## Lane contract and status

| Field | Value |
|---|---|
| Cycle / ordered waves | Cycle 1: Wider -> Deeper -> Contrarian |
| Lane | Internal current-source inventory only |
| Posture | Focused |
| Scope | `src/` component READMEs, current domain/API/UI code and current tests/configuration. No `mvp/`, private data, requirement wording, GitHub provenance, or parent artifact. |
| Evidence goal | Establish present readers/writers, invariants, test seams and credible bypasses for appointment commitment controls, sufficient for parent planning. |
| Limit / stop | Stop at saturated inventory of the named components and paths. |
| Status | Complete; source inventory is comprehensive within scope. |

All locations below were retrieved from the pinned base workspace on 2026-10-18. Facts are distinguished from planning implications; no source was changed.

## Wider wave — inventory

### Current write/read topology

1. `ProcurementMixin` is the appointment/capacity owner. It has package/capacity/work-order state and explicitly distinguishes offered and committed capacity (`src/core/src/zava_forward/core/procurement.py:1-9,74-75`). `record_wo_appointment` is the sole identified domain appointment writer (`:375-396`); server route dispatch maps `/api/workorders/{id}/appointment` to it (`src/api/src/zava_forward/api/server.py:144-148,728-746,847`), and `ops.js` calls that endpoint (`src/api/src/zava_forward/api/web/ops.js:196-205`).
2. Capacity is recorded by `set_capacity` (`procurement.py:292-312`) and requires a committed home-work-order quota backed by source/version, document bytes/hash, current review, dates, covered cases and named authority (`:162-234`). The UI describes offered versus committed and sends those source fields (`ops.js:164-187`).
3. Work-order versions snapshot resident bindings, issuer, authority, contract/scope/capacity versions and appointment history (`procurement.py:345-353`); manager/contractor views expose deliberately different fields (`:440-501`). Existing tests assert version/audit history and contractor isolation (`src/core/tests/test_quality_procurement.py:382-431`; `src/api/tests/test_procurement_api.py:153-189`).
4. `require_booked_capacity` is read by the direct domain `advance` gate (`src/core/src/zava_forward/core/store.py:504-527`), not by a separate endpoint-specific layer. It demands one active `Appointed` order, last appointment `Booked`, current named manager/appointment authority, then rechecks capacity and resident bindings (`procurement.py:504-531`). A legacy case-level `appointments` field exists in the synthetic fixture (`src/core/tests/dataset.py:53-60`) but is not a reader for this gate.
5. Resident consent is independent: `resident_gate` requires current measure scope/revision and `Accepted` decision; representative decisions additionally require a current, scoped `Works decision` authority (`src/core/src/zava_forward/core/resident_decisions.py:299-330`). Representative authority task types distinguish `Works decision` from information/communication/attendance (`:25-30,283-297`). Paused/withdrawn decisions create human review and are measure-scoped (`:469-496`); regression coverage confirms one measure's pause/withdrawal blocks only affected work while another can proceed (`src/core/tests/test_resident_decisions.py:571-617`).
6. Existing resident update/remedy contracts are separate follow-up actions with version/owner guards and committed-response recovery (`resident_decisions.py:123-218,396-405,638-707`; `server.py:922-937`). Existing deletion honors an already-active case legal hold only for resident-record deletion (`resident_decisions.py:374-391`); this lane found no current blanket legal-hold gate around appointment/advance controls.
7. Existing gates remain cumulative: work order issue/appointment/completion/correction invokes safety, resident and (as applicable) building checks (`procurement.py:315-425`); direct advance also uses generic, building, safety, resident, then booked-capacity gates (`store.py:504-527`). The active-hazard safety gate blocks work and requires independent restart evidence/decision (`store.py:465-469`). Quality evidence remains a distinct feature; its procurement test module contains the capacity controls (`test_quality_procurement.py:333-587`).

### Retained adjacent controls relevant to planning

* Contract delegation validates named current manager, reference/version, nonrevocation, permitted action/supplier/scope-version/package and inclusive validity dates (`procurement.py:82-111`); capacity authority is checked at record and later use (`:205-234,292-312`).
* SQL save runs resident and procurement revalidation inside the writer transaction (`src/core/src/zava_forward/core/sqlstore.py:546-568`). Procurement SQL validation refreshes actor, procurement meta snapshot, covered case row versions and authority (`procurement.py:53-70`).
* Procurement operation recovery discards/reloads SQL state on failure and tracks an in-memory rollback/audit ordering (`procurement.py:113-155`); `_proc_save` audits before `save` for SQL and saves before audit for JSON (`:152-160`). Tests cover failed recovery, authority/source races, last-slot race, advance dependency races and audit rollback (`test_quality_procurement.py:790-980`).
* Current README prose identifies #101 as read-only coordinator behavior with no writer/schema changes (`src/core/README.md:8-52`), #117 as bounded document rescan with explicit synthetic opt-in and no retention/hold release authority (`:66-118`), and #88 as the resident commitments/remedy endpoint contract (`src/api/README.md:136-180`). Those are retained boundaries, not appointment decisions.

**Wider reflection:** the current design already has a narrow, server-owned commitment chain and SQL revalidation seam. It does not have an explicit tri-party appointment-agreement record or a distinct offer-versus-commitment appointment model; `Booked` currently records only outcome/date/by/at.

## Deeper wave — behaviour and test evidence

### `Booked` and current capacity

* A Booked outcome parses a date, rechecks evidenced capacity for that date, safety, resident binding and building gate, then moves `Issued -> Appointed`; any non-Booked outcome while appointed returns it to `Issued` before appending outcome and creating a version (`procurement.py:375-396`). Completion also repeats capacity/safety/resident checks (`:398-409`).
* `_evidenced_capacity` refuses offered-only/legacy capacity, stale/mismatched source, changed scope/contract/covered home, invalid accepting manager/authority, out-of-period date and committed deficit (`:205-235`). Committed use counts all `Issued`, `Appointed`, and `Completed` orders (`:18-20,256-257`).
* Existing tests cover evidence refusal, quota limit, booking outside package period, full quota snapshot/history, stale dates/scope/source/deficit and inclusive delivery boundaries (`test_quality_procurement.py:366-380,443-458,503-587`). HTTP covers capacity source requirement, quota threshold and advance refusal (`test_procurement_api.py:119-151`).
* The browser fixture exercises source inputs, quota issue/book, contractor denials, keyboard flow, local-only routing and responsive layouts (`src/api/checks/procurement_browser_check.py:1-194`).

### Persistence, authority, and recovery

* All public procurement writers start `_proc_operation` and named manager validation; its SQL context saves dependency snapshots for commit-time validation (`procurement.py:113-151`). `advance` is protected by `change_provenance.controlled` and invokes the booked-capacity reader before setting the stage (`store.py:504-527`).
* SQL concurrency tests currently prove only one last-slot order and that concurrent withdrawal/rescope/capacity loss causes advance to restore/fail closed (`test_quality_procurement.py:903-929`); source/authority interleaving and audit failure rollback follow (`:931-980`). The test module’s `SqlFlows` uses `SqlStore` (`:627-633`).
* The API catches generic `ConflictError` as HTTP 409 and procurement endpoints pass through the shared POST authorization/role projection (`server.py:758-852,952-965`). Resident committed-but-response-failed behavior is explicitly 409 with `outcome=committed` (`:922-937`); no equivalent special appointment-response recovery contract was identified.

### UI and validation commands

* UI has one free-text note/date field for Booked and one generic appointment-outcome select; it has no resident/re-presentative/staff confirmation capture, deferral/options/household-control surface, or human-investigation state (`ops.js:188-205`).
* API project supplies `ruff`, strict `mypy`, and Playwright dev dependencies (`src/api/pyproject.toml:13-16,24-57`); core likewise configures ruff/mypy (`src/core/pyproject.toml:15-41`). The core README’s generic full-suite command is `python3 -m unittest discover -s tests` from `src/core` (`src/core/README.md:55-60`). Targeted existing checks are, from `src/core`, `../../.venv/bin/python -m unittest test_quality_procurement -q`; from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_procurement_api -q`, and the browser script can be run under the same API paths after Playwright setup.
* Docker’s API build context is `src`, copies only component source/wheels into the runtime image, creates `app`, runs as UID/GID `10001`, does not bake working data, and documents `/data` mount plus `/state` volume (`src/api/Dockerfile:1-28`). This supports source-context/nonroot validation.

**Deeper reflection:** constraints can be attached at the existing `record_wo_appointment`/version and `require_booked_capacity`/advance seams, with SQL validation context and browser/API/core fixtures available. The existing appointment payload and version schema are too sparse to prove required confirmation provenance or bounded representative authority for an appointment; extending them requires carefully scoped invalidation and test additions.

## Contrarian wave — credible bypasses, gaps, and alternatives

1. **Legacy `Booked` ambiguity:** a persisted current order with `appointments[-1].outcome == "Booked"` passes the current reader if other capacity/authority/binding checks pass; it carries no agreement provenance. Treat historical Booked as unknown rather than silently retrofitting confirmation. Alternative: a separate appointment-agreement record/version referenced by the booking, leaving legacy outcomes unconfirmed.
2. **Offer/commitment conflation risk in UI interpretation:** source capacity correctly separates offered and committed (`procurement.py:292-312`), but appointment UI only exposes Booked outcome/date (`ops.js:196-205`). A new offer flow must remain derived/server-calculated and not become a caller-supplied commitment. Alternative: server-derived offer token/version with expiry and revalidation at commitment.
3. **Direct domain/API mutation:** `advance` directly invokes the booked-capacity gate (`store.py:504-527`), but other future callers of `record_wo_appointment`, `complete_work_order`, or raw persistence must not rely only on UI. Put authorization/confirmation logic inside domain writers and SQL commit validation, with endpoint/UI only presenting it.
4. **Concurrency/audit window:** current tests cover races around issue/advance, but no identified test races two appointment commitments or material confirmation invalidation. New control needs transaction-time revalidation, one-success audit assertions, and truthful post-COMMIT reconciliation rather than a retry that duplicates a commitment.
5. **Resident authority is not appointment agreement:** existing `Works decision` authority is measure/scope/safe-contact/review bounded (`resident_decisions.py:283-330`), but does not itself record household appointment agreement. Alternative: reuse it solely as eligibility to record representative confirmation, while retaining independent resident decision/works consent.
6. **Household constraints, options, deferral/no-access:** no matching state model was found in procurement writer/UI. Existing `No access` is merely an appointment outcome (`procurement.py:18-20,375-396`) and should not become inferred resident agreement. Human investigation-only exceptions need explicit nonautomated state, actor/evidence and gate behavior; eligible verified confirmed resident no-access cannot be inferred from current code.
7. **Material-change invalidation:** current capacity/source/scope/authority changes are rechecked (`procurement.py:205-235,504-531`) and decision scope revision invalidates acceptance (`resident_decisions.py:299-330`), but there is no appointment-provenance dependency graph. Alternative: compare each agreement’s precise dependencies (affected measure binding, household/representative authority, option/constraint, contractor capacity/version) so only affected agreement provenance is invalidated.
8. **Do not widen:** do not import an unmerged blanket legal hold. Present legal hold behavior is narrowly resident-retention deletion (`resident_decisions.py:374-391`), while document rescan explicitly has no hold-release power (`core README:66-118`).

## Evidence relationships for parent synthesis

| Question | Evidence relationship |
|---|---|
| Current Booked writer and readers | Supports: `record_wo_appointment` writes Booked and versions it (`procurement.py:375-396`); `require_booked_capacity` reads current authoritative appointment for direct advance (`:504-531`; `store.py:504-527`). |
| Capacity/authority gate | Supports: quota source, coverage, period, authority and SQL rechecks (`procurement.py:53-70,162-235`; `sqlstore.py:546-568`). |
| Existing consent vs representative decision | Supports independent works consent and bounded `Works decision` delegation (`resident_decisions.py:283-330,469-496`); leaves appointment agreement absent. |
| Bypass/recovery posture | Supports existing authorization, conflict, audit and race foundations (`test_quality_procurement.py:790-980`); leaves appointment-specific double-write/post-COMMIT tests absent. |
| Endpoint/UI plumbing | Supports server dispatch and thin manager UI (`server.py:144-148,728-746`; `ops.js:124-207`); leaves tri-party/household/deferral/investigation UI absent. |
| Retained neighboring contracts | Supports keeping #88, #90, #85, #91, #102, #101 and #117 separations: docs/current code cited above; no source change proposed. |

## Gaps and stop decision

* Parent must apply requirement wording and GitHub provenance to decide exact threshold semantics, including the stated strict default-5 rule; this lane did not research those sources.
* Exact domain model/retention for tri-party confirmation, household constraints/options/deferral, confirmed no-access exception and material-change dependency set is absent from current source and needs parent decision.
* No `mvp/`, private datasets, or unmerged #389 material was examined.

**Stop decision:** focused current-source inventory saturated: identified domain/API/UI readers and writers, adjacent gate contracts, SQL/JSON persistence and recovery seams, existing synthetic fixture/browser paths, and configured validation/container context. Further internal sources would be redundant without parent-selected design decisions.
