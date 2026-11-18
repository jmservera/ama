<!-- markdownlint-disable-file -->
# RPI Phase Details: Hazard and Safeguarding Clock and Named Owner Projection (Issue #76)

## Metadata

* Task ID: issue-76
* Task slug: ux-76-hazard-clock-owner
* Related plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/reference/regulatory/building-safety-awaabs-law/2025-10-27-hazards-in-social-housing-prescribed-requirements-england-regulations-2025.xml

## Phase Index

| Phase ID | Name                                                            | Status | Detail sections          |
|----------|-----------------------------------------------------------------|--------|--------------------------|
| P01      | Core Hazard and Safeguarding Clock and Named-Owner Projection   | Ready  | P01, P01-T01, P01-T02    |
| P02      | Web Queue and Case Card Display Without Modifying `role-screens.js` | Ready  | P02, P02-T01             |
| P03      | Focused Core and API/UI Unit Tests and Component Documentation  | Ready  | P03, P03-T01, P03-T02    |
| P04      | Focused-Tier Validation and Guard Verification                  | Ready  | P04, P04-T01             |

<!-- rpi:phase id=P01 -->
## P01: Core Hazard and Safeguarding Clock and Named-Owner Projection

### Context

Research findings `C5`, `C8`, `C9`, `C10`, `C11`, `C12`, and `C16` show that `taskqueues.context(...)` is the single shared `work` builder invoked by `Store.page_cases`, `SqlStore.page_cases`, `MssqlStore`, and `Store.detail`, while `workflows.hazard_view(...)` builds per-item safety entries on `Store.detail`. Centralizing clock and accountable-owner computation in `taskqueues.py` and reusing it in `workflows.py` guarantees `FR-034` cross-view agreement.

### Intent

Ensure every hazard and safeguarding item in queue projections and case card detail responses carries complete, deterministic fail-closed statutory/operational clock fields and non-blank named accountable/escalation owner fields while respecting contractor and `can_see_reason` redaction rules.

### Boundaries

* Included: `taskqueues.py`, `workflows.py`, `store.py`, `sqlstore.py`, `insights.py`, `ranking.py`, `projection.py`.
* Excluded: Modifying external hazard-service authority semantics (`RULE-003`), exposing staff safety data to contractors or resident preview, or altering unrelated workflow rules.

### Likely Targets

* `src/core/src/zava_forward/core/taskqueues.py`: Safeguarding extraction, open-safety helpers, `project_safety_clock_and_owner(...)`, `overdue_tasks(...)`, and `context(...)`.
* `src/core/src/zava_forward/core/workflows.py`: Add `"Safeguarding"` to `HAZARD_CATEGORIES`, enrich `hazard_view(...)`, and add `safeguarding_view(...)`.
* `src/core/src/zava_forward/core/store.py`: Pass `staff=data.get("staff", [])` to `taskqueues.context`, `hazard_view`, and `safeguarding_view`; project `safeguarding` flag on `summary` and `safeguarding_items` on `detail`; include open safeguarding items in `focus`, `gate_reasons`, and `counts`.
* `src/core/src/zava_forward/core/sqlstore.py`, `insights.py`, `ranking.py`, `projection.py`: Keep `hazard` flag and `hold_notes` redaction aligned for standalone safeguarding items.

### Dependencies

* None.

### Validation Expectations

* Existing `src/core/tests/test_taskqueues.py`, `test_resident_preview.py`, and `test_issue_220_challenge_route.py` continue to pass alongside new unit tests.

### Completion Evidence

* `taskqueues.context` and `Store.detail` return identical clock and named-owner metadata for every hazard and safeguarding item in both JSON `Store` and SQLite `SqlStore`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement unified clock, accountable-owner, and safeguarding item helpers in `taskqueues.py` and `workflows.py`

#### Context

`taskqueues.py` currently builds `hazard_clocks` only from `case.get("hazards", [])`, omits structured deadline/remaining-hour/fail-closed clock statuses, and sets `owner = "Unknown"` without surfacing a named accountable/escalation owner when unallocated (`C8`, `C12`). Meanwhile `resident_preview_fixture.py` uses `safeguarding=dict(note=...)` as a canary-only note container on ordinary cases (`C16`).

#### Intent

Provide one canonical projection helper covering both hazards and safeguarding items with explicit fail-closed clock semantics and non-blank named accountable/escalation owners.

#### Boundaries

* Included:
  * Increment `taskqueues.MEMBERSHIP_REVISION` from `3` to `4` so reopened `SqlStore` databases recompute cached queue columns (`PC-003`).
  * Safeguarding item discovery helper `raw_safeguarding_items(case)`: extracts dicts from `case.get("safeguarding_items")` (`list`), `case.get("safeguarding")` when `list`, and `case.get("safeguarding")` when `dict` containing at least one item-identifying key in `{"id", "status", "state", "priority", "category", "kind", "aware_at", "raised_at", "reported_at", "noticed", "response_due_at", "due_at", "owner", "named_owner", "sender", "destination", "accepted_by", "referred", "repaired", "released"}` so note-only `{"note": ...}` canary containers in `resident_preview_fixture.py` are ignored (`PC-003`). Items in `case.get("hazards", [])` with `category == "Safeguarding"` or `kind == "safeguarding"` are tagged `item_kind = "safeguarding"`.
  * Active safety check: an item is open/active when `not item.get("released")` and `str(item.get("status") or "").strip().lower() not in {"closed", "released", "resolved"}`.
  * `overdue_tasks(...)`: evaluate recorded `response_due_at`/`due_at` and `resident_update_due_at` on open standalone safeguarding items (`safeguarding/{i}/...`) while keeping derived awareness-only target deadlines out of `overdue_tasks` when `response_due_at`/`due_at` is unrecorded (`PC-003`).
  * Clock calculation `project_safety_clock_and_owner(item, *, case, as_of, staff=None, default_kind="hazard")`:
    * Reference window hours and `clock_label`:
      * `item_kind == "safeguarding"`: `24` hours (`"Safeguarding 24h emergency response clock"`) when `priority` in `{"Emergency", "Immediate", "Urgent", "P1"}`; otherwise `48` hours (`"Safeguarding 48h referral response clock"`).
      * `item_kind == "hazard"`: `24` hours (`"Awaab's Law 24h emergency action clock (recorded reference)"`) when `priority` in `{"Emergency", "P1"}`; `336` hours / 14d (`"Operational 14d work-start clock (recorded reference)"`) when `priority == "Routine"` or (`priority == "Significant"` and `bool(item.get("accepted_at"))`); otherwise `168` hours / 7d (`"Operational 7d hazard investigation clock (recorded reference)"`).
    * Deadline resolution:
      * Valid timezone-aware `response_due_at` or `due_at` takes precedence (`clock_basis = "recorded_service_deadline"`).
      * Else valid timezone-aware `aware_at <= now` derives `deadline = awareness + timedelta(hours=window_hours)` (`clock_basis = "operational_reference_from_awareness"`).
      * Else `deadline = None` (`clock_basis = "missing_timestamp_fail_closed"`).
    * Status & remaining hours:
      * If valid `responded_at <= now`: `clock_status = "completed"`, `clock_deadline_utc = utc_iso(deadline) if deadline else None`, `clock_remaining_hours = 0.0 if deadline else None`.
      * Else if `deadline is None`: `clock_status = "fail_closed_missing_timestamp"`, `clock_deadline_utc = None`, `clock_remaining_hours = None`.
      * Else: `rem = round((deadline - now).total_seconds() / 3600, 1)`, `clock_deadline_utc = utc_iso(deadline)`, `clock_remaining_hours = rem`, `clock_status = "overdue" if deadline < now else "running"`.
  * Accountable owner resolution (`FR-003` receipt-is-not-acceptance, `PC-002`):
    * Match identity dicts or string names against `staff` roster (by `code`, `oid`, `email`, or case-insensitive `name`) to recover `name`, `role`, and `id` (`code` or `email` or `oid`).
    * Direct owner checks `accepted_by` -> (`destination` ONLY when `bool(item.get("accepted_at"))`) -> `sender` -> `item.get("follow_up")` -> `item.get("owner")` -> `item.get("named_owner")` (ignoring blank/`"Unknown"`/`"Anonymous"`).
    * Escalation owner checks unaccepted/designated `destination` -> named `case.get("owner")` (`owner_code`, `owner_role` / roster) -> named roster staff in `"Building Safety Liaison"` then `"Retrofit Programme Manager"` -> duty fallback (`"Safeguarding duty lead"` / `"ESC-SG-DUTY"` / `"Building Safety Liaison"` for safeguarding; `"Building Safety Liaison duty lead"` / `"ESC-BSL-DUTY"` / `"Building Safety Liaison"` for hazards).
    * Preserves legacy `owner` (`direct_name` if allocated else `"Unknown"`) and `owner_named` (`bool(direct_name)`), while always populating non-blank `named_owner`, `accountable_owner`, `owner_role`, `owner_id`, `unassigned` (`not bool(direct_name)`), `escalation_owner`, `escalation_owner_role`, and `escalation_owner_id`.
  * Plain-language check (`PC-004`): ensure `owner_status` and blocker/action copy contain zero `CopyAudit` banned patterns (`\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b`).
  * `workflows.py`: add `"Safeguarding"` to `HAZARD_CATEGORIES`, enrich `hazard_view(...)` (backfilling scalar `owner = enriched["named_owner"]` when `h.get("owner")` is missing/blank/`"Unknown"` on the returned view dict without mutating `c["hazards"]`, `PC-001`), and add `safeguarding_view(...)` returning normalized standalone safeguarding view dicts (`standalone_safeguarding=True`, `category`, `released`, `state`, `hold`, scalar `owner`, plus clock/owner metadata).
* Excluded: UI changes (handled in `P02`).

#### Likely Targets

* `src/core/src/zava_forward/core/taskqueues.py`
* `src/core/src/zava_forward/core/workflows.py`

#### Dependencies

* None.

#### Validation Expectations

* `mypy` and `unittest` on `test_taskqueues.py` pass with zero regressions on legacy `hazard_clocks` assertions.

#### Completion Evidence

* Shared helper functions exist and populate all clock and owner fields on `work["hazard_clocks"]`, `work["safeguarding_clocks"]`, `work["safety_items"]`, `hazard_view`, and `safeguarding_view`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire staff roster, safeguarding case-card detail, redaction, and SQL store parity

#### Context

`Store.page_cases`, `SqlStore.page_cases`, and `Store.detail` must emit identical `work` dictionaries (`FR-034`) and consistent `hazard`/`safeguarding` summary flags (`C5`, `C10`, `C11`, `C14`), while `projection.hold_notes` must redact free-text safeguarding notes for roles without `can_see_reason(user)` and contractors must remain default-deny (`PR-002`).

#### Intent

Connect the unified safety projection across JSON `Store`, SQLite `SqlStore` (and inherited `MssqlStore`), ranking/insights, and staff/contractor redaction.

#### Boundaries

* Included:
  * `insights.has_hazard(c)`, `ranking._hazard(c)`, `Store.counts()` (`store.py:450`), and `SqlStore._row(c)` (`sqlstore.py:979`): treat open hazards OR open standalone safeguarding items as open safety issues so `flag="hazard"`, urgent ranking, `Store.counts()["hazards"] == SqlStore.counts()["hazards"]`, `Store.summary(c)["hazard"]`, and `role_screens_browser_check.py` `.flag.danger` counts match everywhere (`PC-003`).
  * `Store.summary(c)`: add `safeguarding=taskqueues.has_open_safeguarding(c)` alongside `hazard=insights.has_hazard(c)` (neither is in `projection.SUMMARY_FIELDS`, keeping contractor summaries clean).
  * `Store._work_context(c, user, data, cases)`: pass `staff=data.get("staff") or list(self.staff.values())` into `taskqueues.context(...)` so `SqlStore._refresh_queue_membership` always receives the staff roster (`PC-003`).
  * `Store.gate_reasons`, `Store.status_line`, `Store.focus`, and `Store.require_safety_clear`: replace raw `h["owner"]` / `h["category"]` indexing with safe lookups across open hazards and open standalone safeguarding items backed by resolved `named_owner` (`PC-003`).
  * `Store.detail(case_id, user)`: build `safeguarding_views = [safeguarding_view(...)]`, set `d["safeguarding_items"] = safeguarding_views`, and set `d["hazards"] = [hazard_view(...)] + [dict(s) for s in safeguarding_views]` so unmodified `role-screens.js` (`safety-lead` and `hazard-triage`) lists standalone safeguarding items with non-`"Unknown"` scalar `owner` and never renders `"Mismatch"` when `row["hazard"]` is `True`, while existing cases without standalone safeguarding retain exact `d["hazards"]` counts and indices (`PC-001`).
  * `projection.hold_notes(d)`: ensure dicts in `d.get("hazards", [])` and `d.get("safeguarding_items", [])` (`("category" in c and "released" in c) or c.get("item_kind") == "safeguarding"`) have `NOTE_KEYS` plus non-empty `"summary"`, `"reason"`, `"source"`, and `"job"` replaced with `NOTE_HELD` when `not can_see_reason(user)`, while leaving all structured `clock_*` and owner fields untouched (`PC-004`).
* Excluded: Web client rendering (`P02`).

#### Likely Targets

* `src/core/src/zava_forward/core/store.py`
* `src/core/src/zava_forward/core/sqlstore.py`
* `src/core/src/zava_forward/core/insights.py`
* `src/core/src/zava_forward/core/ranking.py`
* `src/core/src/zava_forward/core/projection.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `Store` and `SqlStore` produce identical `page_cases` and `detail` safety projections; `test_resident_preview.py` and `test_task_queue_api.py` pass.

#### Completion Evidence

* Staff detail and queue responses expose aligned hazard and safeguarding clocks and owners; contractors receive none; non-reason staff have free-text notes held while keeping clock and named owner.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Web Queue and Case Card Display Without Modifying `role-screens.js`

### Context

`listView` (`web/app.js:907`), every specialist role screen (`web/role-screens.js:98`), and `caseView` (`web/app.js:808, 1086, 1132, 1149, 1154`) render `workSummary(work)` from `web/app.js:797`, and `safetyPanel(c, id, refresh)` (`web/app.js:1586-1795`) renders per-item safety cards on the case card (`C7`). Updating only `web/app.js` updates all queue and case-card surfaces while keeping `web/role-screens.js` untouched.

### Intent

Display the statutory/operational clock and named accountable owner (including fail-closed missing-timestamp state and unassigned escalation-owner state) on every hazard and safeguarding item in queue views and case cards, complying with `web-design-guidelines`, `SA-003`, and existing DOM/VM test contracts (`C13`, `C14`, `C15`, `C17`, `C18`).

### Boundaries

* Included: Loading `web-design-guidelines` and updating `HAZ_CATEGORIES`, `workSummary(work)`, and `safetyPanel(c, id, refresh)` in `src/api/src/zava_forward/api/web/app.js`.
* Excluded: Any edit to `src/api/src/zava_forward/api/web/role-screens.js` or `style.css` fixed-positioning/table counts.

### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`: `HAZ_CATEGORIES`, `workSummary`, `safetyClockOwnerText` / `safetyPanel`.

### Dependencies

* P01.

### Validation Expectations

* `test_role_screens.py`, `test_safety_panel_ux.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, and `test_list_export_inventory.py` pass.

### Completion Evidence

* Queue rows and case cards visibly display clock label, clock status, remaining hours / UTC deadline (or fail-closed missing-timestamp status), and named accountable owner (plus unassigned + escalation owner when unallocated) for both hazards and safeguarding items.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Load `web-design-guidelines` and update `workSummary` and `safetyPanel` in `web/app.js`

#### Context

Repository Web Development Guidance requires loading `web-design-guidelines` and fetching its current rule source before editing web files. Contrarian findings `C13`, `C14`, and `C15` establish three strict DOM invariants:
1. `test_role_screens.py:168` slices `app.js` from `function workSummary(` to `function workSteps(`, so `workSummary` must remain immediately above `workSteps`, use no external helpers outside that slice, and emit no `undefined`/`NaN` when synthetic legacy clock fixtures omit `clock_label` or `named_owner`.
2. `role_screens_browser_check.py:448-458` requires one `.safety-clock` element per `work["hazard_clocks"]` entry containing `aware_at`, `owner`, `response_due_at`, `resident_update_due_at`, and `${clock.authority} owns timing.`.
3. `test_safety_panel_ux.py:162-165, 178` requires `<dl class="safety-facts">` to keep exact 4 `<dt>` elements without `"Unknown"`.

#### Intent

Render clear, plain-language clock and named-owner lines in `workSummary` and `safetyPanel` while honoring every DOM and copy-audit invariant.

#### Boundaries

* Included:
  * Invoke `skill: "web-design-guidelines"` and fetch its source checklist before editing `web/app.js`.
  * Add `"Safeguarding"` to `HAZ_CATEGORIES` (`web/app.js:1428`).
  * In `workSummary(work)` (`web/app.js:797-805`), append structured clock details (`Clock: ${clock.clock_label} ...`) and accountable-owner details (`Accountable owner: ${clock.named_owner} (${clock.owner_role}, ${clock.owner_id})`, plus `Unassigned item; escalation owner: ${clock.escalation_owner}` when `clock.unassigned` is true) inside each `p.safety-clock` when those fields are present on `clock`.
  * In `caseView(id)` (`web/app.js:1013`), compute `openHaz` across open `(c.hazards || [])` and open `(c.safeguarding_items || [])` so standalone safeguarding items show the `"Safety issue open"` badge and hoist `safetyPanel` (`PC-001`).
  * In `safetyPanel(c, id, refresh)` (`web/app.js:1734`), filter `(c.hazards || []).filter((x) => !x.standalone_safeguarding)` for the mutable hazard cards (preserving original `c.hazards` indices and keeping `li.safety-item` count at 3 on standard 3-hazard fixtures), always render `<p class="safety-clock-owner">` immediately above `<dl class="safety-facts">` using either projected `clock_*`/`named_owner` fields or deterministic client-side fallback from raw fixture fields + `me.staff` (`PC-004`), and render standalone `c.safeguarding_items` once as read-only `li.safeguarding-item` cards with `<p class="safety-clock-owner">` (`PC-001`).
  * Verify zero occurrences of any `CopyAudit` banned pattern (`\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b`) across added UI copy and comments in `web/app.js` (`PC-004`).
* Excluded: Editing `web/role-screens.js`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Node VM tests in `test_role_screens.py` and `test_safety_panel_ux.py` pass alongside counted baseline guards.

#### Completion Evidence

* `web/app.js` renders hazard and safeguarding clocks and named/escalation owners across queue rows and case cards with `git diff .../role-screens.js` empty.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Core and API/UI Unit Tests and Component Documentation

### Context

Locked test plan (`NFR-3`): exact test removals = `none`; maximum test file additions = `2` (`src/core/tests/test_hazard_safeguarding_clock_owner_76.py` and `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py`), plus concise contract notes in `src/core/README.md` and `src/api/README.md`.

### Intent

Add high-signal unit tests that would fail without this change and cover every statutory/operational clock state, named/escalation owner fallback, safeguarding representation, redaction boundary, `FR-034` cross-view agreement, and UI rendering path.

### Boundaries

* Included: `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`, `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py`, `src/core/README.md`, `src/api/README.md`.
* Excluded: Trivial constant restatements or modifying baseline guard thresholds.

### Likely Targets

* `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`
* `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py`
* `src/core/README.md`
* `src/api/README.md`

### Dependencies

* P01, P02.

### Validation Expectations

* Both new test files run cleanly under `unittest discover` and pass `ruff` and `mypy`.

### Completion Evidence

* All semantic and edge-case tests pass and component READMEs reflect the clock and named-owner contract.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`

#### Context

Core projection must be verified across all clock branches, owner allocation states, safeguarding shapes, store backends (`Store` and `SqlStore`), and redaction roles.

#### Intent

Prove core and SQL store clock and named-owner invariants for hazards and safeguarding items.

#### Boundaries

* Included test cases:
  1. Awaab's Law 24h emergency, 7d significant investigation, and 14d work-start/routine hazard clocks (`running`, `overdue`, `completed`), plus external `response_due_at` precedence (`clock_basis == "recorded_service_deadline"`).
  2. Safeguarding 24h emergency and 48h referral clocks across `safeguarding_items` list, `safeguarding` dict/list, and `category="Safeguarding"` hazards.
  3. Fail-closed clock behavior (`clock_status == "fail_closed_missing_timestamp"`, `clock_deadline_utc is None`, `clock_remaining_hours is None`) when timestamps are missing, unparseable, naive, or in the future relative to `as_of`.
  4. Named accountable owner never blank/anonymous: allocated items populate `named_owner`, `accountable_owner`, `owner_role`, `owner_id` with `unassigned=False`; unallocated items (even when `case["owner"]` is missing/Unknown) set `unassigned=True` and populate `named_owner`/`accountable_owner` from `escalation_owner` while keeping legacy `owner == "Unknown"` and `owner_named is False`.
  5. `FR-034` agreement between `page_cases` (`mine`, `all`, role queues) and `detail` across both `Store` and `SqlStore`, plus contractor default-deny withholding, non-reason staff `NOTE_HELD` redaction with preserved clock/owner, and passive canary `safeguarding={"note": "..."}` non-interference.
* Excluded: Browser/HTTP rendering (covered in `P03-T02`).

#### Likely Targets

* `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner_76.py" -v` from `src/core` passes.

#### Completion Evidence

* Focused core test module covers all 5 behavioral groups and passes `ruff` and `mypy`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Add `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py` and update READMEs

#### Context

API endpoints (`/api/cases` and `/api/cases/{id}`) and `web/app.js` (`workSummary` used by `My cases today`, `All open cases`, and `role-screens.js`, plus `safetyPanel` on the case card) must be proven end-to-end.

#### Intent

Verify HTTP/API responses and real `web/app.js` DOM rendering of hazard and safeguarding clocks and named/escalation owners, and document the contract in `src/core/README.md` and `src/api/README.md`.

#### Boundaries

* Included:
  * API tests over `GET /api/cases?view=mine`, `GET /api/cases?view=all`, role-queue filters, and `GET /api/cases/{id}` across safety, non-reason staff, and contractor roles, asserting `FR-034` agreement, plain-language `SA-003` compliance, and redaction.
  * Node VM / DOM tests executing real `workSummary(row.work)` (the exact renderer called by `listView` and `role-screens.js`) and `safetyPanel(detail, id, refresh)` from `web/app.js` for allocated, unallocated (escalated), overdue, and missing-timestamp (fail-closed) hazard and safeguarding items.
  * Concise documentation updates in `src/core/README.md` and `src/api/README.md`.
* Excluded: Modifying `web/role-screens.js`.

#### Likely Targets

* `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py`
* `src/core/README.md`
* `src/api/README.md`

#### Dependencies

* P01, P02.

#### Validation Expectations

* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner_api_76.py" -v` from `src/api` passes.

#### Completion Evidence

* API/DOM test suite passes and READMEs are updated.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Focused-Tier Validation and Guard Verification

### Context

Focused-tier validation requires `ruff check`, `ruff format --check`, `mypy`, and `unittest` across `src/core` and `src/api`, explicit verification of the three named counted baseline guards, verification that `web/role-screens.js` is untouched, and full reconciliation of RPI tracking artifacts before `rpi-review`.

### Intent

Prove zero regressions across all static analysis and unit/guard suites and prepare reconciled implementation evidence for Review.

### Boundaries

* Included: Running validation commands in `src/core` and `src/api`, recording exact command outputs in `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-changes.md`, and checking off completed plan tasks.
* Excluded: `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-changes.md`
* `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md`
* `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* All `ruff`, `mypy`, and `unittest` commands exit 0; `git status --short` shows no modifications to `web/role-screens.js`.

### Completion Evidence

* Reconciled changes artifact with exact test counts and command exit codes.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Execute `ruff`, `mypy`, and `unittest` across `src/core` and `src/api` and reconcile artifacts

#### Context

Before entering `rpi-review`, RPI Agent requires reconciliation of plan markers, phase details, changes evidence, blockers, remaining work, follow-ups, and validation state.

#### Intent

Run all focused-tier checks and finalize implementation tracking artifacts.

#### Boundaries

* Included:
  * `ruff check src tests`, `ruff format --check src tests`, `mypy src tests`, and `python3 -m unittest discover -s tests -q` in `src/core` and `src/api` (with `PYTHONPATH=../core/tests:../agents/tests` in `src/api`).
  * Targeted confirmation of `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, `test_role_screens.py`, `test_safety_panel_ux.py`, `test_taskqueues.py`, `test_sqlqueues.py`, `test_resident_preview.py`, and `test_resident_preview_api.py`.
  * Verify `git diff --name-status` confirms `web/role-screens.js` is untouched, test removals `0`, and new test files `<= 2`, reconcile `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-changes.md`, plan `[x]` markers, and phase statuses before `rpi-review`, and after `rpi-review` completes commit all changes + `.copilot-tracking/` artifacts locally on `feat/ux-76-hazard-clock-owner` using repository-local `gh api user` noreply email, `Refs #76`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (`PC-005`).
* Excluded: Remote push.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-changes.md`

#### Dependencies

* P01, P02, P03.

#### Validation Expectations

* Exit code 0 for every check.

#### Completion Evidence

* Recorded command outputs and reconciled plan/details/changes artifacts.

#### Unresolved Items

* None.
