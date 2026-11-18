<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 83 Unaccepted Handoff Visibility and SLA Escalation (BG-010)

## Metadata

* Task ID: 83-handoff-escalation
* Task slug: 83-handoff-escalation
* Related plan: .copilot-tracking/plans/2026-11-15/83-handoff-escalation-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/83-handoff-escalation-research.md

## Phase Index

| Phase ID | Name                                                                            | Status    | Detail sections          |
|----------|---------------------------------------------------------------------------------|-----------|--------------------------|
| P01      | Core BG-010 Handoff SLA Evaluation, Projections, Queues, and Overdue Sweep     | Ready     | P01, P01-T01, P01-T02    |
| P02      | HTTP API Handoff Queue and Escalation Sweep Routes                              | Ready     | P02, P02-T01             |
| P03      | Focused Unit Tests and Static/Runtime Verification                              | Ready     | P03, P03-T01, P03-T02    |

<!-- rpi:phase id=P01 -->
## P01: Core BG-010 Handoff SLA Evaluation, Projections, Queues, and Overdue Sweep

### Context

`workflows.py` currently tracks handoff states (`Offered` -> `Sent`, `Received`, `Accepted`, `Declined` -> `Rejected`, `Withdrawn`, `Escalated`, `Completed`) and provides `handoff_ageing` and per-case `escalate_handoff`, while `taskqueues.py` flags `unowned` on pending handoffs and `overdue` only when `handoff["due_at"]` is set (`C4`..`C8`). However, approved `BG-010` policy windows on `store.data.get("handoff_policy")` are not evaluated, case/queue projections lack escalation status, elapsed/overdue hours, escalation target, and escalation guidance, destination-role/escalation queues (`unowned_handoffs`, `escalated_handoffs`) are absent, and no deterministic overdue escalation sweep exists (`C5`..`C9`).

### Intent

Deliver complete, deterministic `BG-010` SLA evaluation, projection enrichment, shared/role handoff queues, `SqlStore` cache synchronization, `ExceptionRegister` integration, and controlled overdue escalation sweeps in `zava_forward.core`.

### Boundaries

* Included: `workflows.py`, `taskqueues.py`, `store.py`, `sqlstore.py`, `exception_register.py`, and `src/api/src/zava_forward/api/progress.py` (`handoff_view` call site).
* Excluded: DDL table alterations on `SqlStore`/`MssqlStore`, changes to the 13-key `handoff_ageing` dict structure, and any frontend JS edits.

### Likely Targets

* `src/core/src/zava_forward/core/workflows.py`: Policy helpers, `handoff_sla`, `handoff_view`, `handoff_ageing`, `pending_handoffs`, `unaccepted_handoffs`, `unowned_handoffs`, `escalated_handoffs`, `escalate_overdue_handoffs`.
* `src/core/src/zava_forward/core/taskqueues.py`: `MEMBERSHIP_REVISION`, `overdue_tasks`, and `context`.
* `src/core/src/zava_forward/core/store.py` and `sqlstore.py`: Pass `as_of`, `handoff_policy`, and `staff` to `handoff_view`; include `handoff_policy` in `_queue_fingerprint`.
* `src/core/src/zava_forward/core/exception_register.py` and `src/api/src/zava_forward/api/progress.py`: Pass `handoff_policy` / `as_of` so `BG-010` SLA breaches feed `ExceptionRegister` and progress overdue indicators consistently.

### Dependencies

* None.

### Validation Expectations

* Existing `test_handoff_lifecycle.py`, `test_taskqueues.py`, `test_sqlqueues.py`, `test_exception_register.py`, and `test_exception_feeds.py` pass without regression alongside new `BG-010` assertions.

### Completion Evidence

* Updated `zava_forward.core` modules passing `mypy`, `ruff`, and unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement BG-010 SLA helpers, enriched handoff views, role queues, and overdue escalation sweep in workflows.py

#### Context

`handoff_ageing` must preserve its exact 13 keys (`FIELDS` in `test_unaccepted_handoff_csv_api.py`, `C13`) and keep `approved_limit_hours=None` when no approved policy is configured (`C14`, `C15`). At the same time, `handoff_view`, role queues, and escalation sweeps need complete `BG-010` metadata and strict `PR-002` redaction (`C18`).

#### Intent

Add policy-gated `BG-010` SLA evaluation, projection fields, shared/role handoff queues (`unowned_handoffs`, `unaccepted_handoffs`, `escalated_handoffs`), and idempotent `escalate_overdue_handoffs` in `workflows.py`.

#### Boundaries

* Included:
  * `approved_handoff_policy(policy)`: Returns normalized approved policy dict when `isinstance(policy, dict)`, `policy.get("status") == "Approved"`, `owner` is a named human (not blank/`"Unknown"`/`"to be named"`), and `acceptance_hours` is a finite `int | float > 0` (rejecting `bool`), plus optional finite positive `urgent_acceptance_hours`, `policy_id` / `version`, `escalation_owner`, `escalation_owner_code`, and `escalation_role` (defaulting to `"Retrofit Programme Manager"`). Returns `None` otherwise.
  * `approved_handoff_limit_hours(policy, *, urgency=None)`: Resolves `urgent_acceptance_hours` when `urgency == "Urgent"` and present on an approved policy, else `acceptance_hours`, else `None`.
  * Instant parsing helper accepting both `YYYY-MM-DD` dataset `as_of` dates (normalized to `00:00:00+00:00` UTC like `taskqueues.instant`) and timezone-aware ISO timestamps, while raising `ValueError` on malformed strings or naive timestamps containing a time component.
  * `handoff_sla(c, *, as_of=None, policy=None, max_age_hours=None, staff=None)`: Pure deterministic evaluation tolerant of missing `offered_at` (`elapsed_hours=None`, `sla_due_at=None`), comparing exact elapsed seconds `(now - offered).total_seconds() > limit * 3600` (`+1s` breach parity), preserving full sub-minute UTC ISO precision on `sla_due_at`, selecting the chronologically earlier parsed UTC instant of `due_at` and `sla_due_at` for `effective_due_at` (tie-breaking to `due_at`), clamping `elapsed_hours = max(0.0, round(raw_seconds / 3600, 2))` when snapshot `as_of < offered_at`, and returning `approved_limit_hours`, `sla_due_at`, `effective_due_at`, `elapsed_hours`, `overdue`, `overdue_hours`, `needs_escalation`, `escalation_status`, `escalation_target`, `escalation_target_code`, `escalation_target_role`, and deterministic `escalation_next_action` (never interpolating raw staff free-text notes or private resident/address fields).
  * `handoff_view(c, *, as_of=None, policy=None, max_age_hours=None, staff=None)`: Preserves all existing keys (including untouched `next_action` under `projection.NOTE_KEYS`) and merges `handoff_sla` fields (`escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `sla_due_at`, `effective_due_at`, `overdue`, `needs_escalation`, `escalation_target`, `escalation_target_code`, `escalation_target_role`, `escalation_next_action`).
  * `handoff_ageing(c, as_of, max_age_hours=None, *, policy=None)`: Continues raising `KeyError`/`ValueError` on missing/malformed `offered_at` or naive time-bearing `as_of`; resolves `limit = max_age_hours` if explicitly passed, else `approved_handoff_limit_hours(policy, urgency=h.get("urgency"))`; evaluates exact elapsed seconds `raw_seconds > limit * 3600` with reason `f"Unaccepted for more than the approved {float(limit)} hours"`; keeps `limit_note=None` when an explicit `max_age_hours` override is supplied without an approved policy, `f"Approved escalation limit: {float(limit)}h ({policy_ref})"` when resolved from approved `policy`, and `"Approved escalation time not set (OD-09)"` when `limit is None`; returns exact 13 `FIELDS` in exact order.
  * Visibility & shared/role queues on `WorkflowMixin`:
    * `pending_handoffs(user)`: Passes `as_of=self.as_of, policy=self.data.get("handoff_policy"), staff=self.data.get("staff")` to `handoff_view`, includes `user["code"] in (h.get("from_code"), h.get("to_code"), h.get("escalation_owner_code")) or (not h.get("to_code") and h.get("to_role") == user.get("role")) or user["role"] in MANAGER_ROLES`, and keeps `projection.hold_notes` redaction when `not projection.can_see_reason(user)`.
    * `unaccepted_handoffs(user, as_of=None, max_age_hours=None)`: Defaults `as_of` to `_now()`, passes `policy=self.data.get("handoff_policy")` into `handoff_ageing`, and applies the same visibility predicate (`from_code`, `to_code`, `escalation_owner_code`, role-only `not to_code and to_role == user["role"]`, or `MANAGER_ROLES`) so named-colleague privacy (`test_unaccepted_handoff_csv_api.py:218`) stays intact.
    * `unowned_handoffs(user, as_of=None, max_age_hours=None)`: Defaults `as_of` to `_now()`; returns open pending handoffs (`state in HANDOFF_PENDING`, `confirmed_receiver is None`) visible to `from_code`, `to_code`, destination role (`h.get("to_role") == user.get("role")`), `escalation_owner_code`, or `MANAGER_ROLES`, ordered deterministically (`not overdue`, `-overdue_hours`, `-elapsed_hours`, `case_id`), projecting `case_id`, `stage`, `accountable_owner`, `accountable_owner_code`, `chase_owner`, `chase_owner_code`, `destination`, `proposed_receiver`, `confirmed_receiver`, `status`, `escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `due_at`, `sla_due_at`, `effective_due_at`, `overdue`, `needs_escalation`, `escalation_target`, `escalation_target_code`, `escalation_target_role`, `next_action`, `escalation_next_action`, and `as_of` (no resident/address canaries), redacted via `projection.hold_notes` when `not projection.can_see_reason(user)`.
    * `escalated_handoffs(user, as_of=None, max_age_hours=None)`: Defaults `as_of` to `_now()`; filters `unowned_handoffs`-shaped rows to those where `state == "Escalated"` or `overdue` (`needs_escalation`) is `True`, additionally visible when `escalation_target_role == user.get("role")`.
  * `escalate_overdue_handoffs(user, *, as_of=None, max_age_hours=None, reason=None)`: Verifies `user["role"] in MANAGER_ROLES` first (`PermissionError` otherwise); defaults `as_of` to `_now()` and validates `as_of`/`max_age_hours`; evaluates all cases with `state in ("Offered", "Received")`; for each overdue handoff enters `with change_provenance.controlled(self, user, cid) as (c, actor):`, resolves manager target staff record (from approved `handoff_policy`, or a `Retrofit Programme Manager` / `MANAGER_ROLES` staff member, or `user`), updates `c["handoff"]` (`state="Escalated"`, `escalated_at=_now("microseconds")`, `escalation_owner`, `escalation_owner_code`, `auto_escalated=True`, `answer_note` holding reason text so `projection.NOTE_KEYS` redacts it properly), appends history via `self._handoff_event(c, actor)` with `auto_escalated=True`, and persists/audits via `self._save_workflow(actor, "handoff_escalated", cid, ...)`; leaves `c["owner"]` unchanged; returns a deterministic summary dict (`as_of`, `evaluated_count`, `escalated_count`, `already_escalated_count`, `escalated_case_ids`, `items`).
* Excluded: Modifying `accept_handoff` ownership-transfer semantics or changing the 13 keys of `handoff_ageing`.

#### Likely Targets

* `src/core/src/zava_forward/core/workflows.py`

#### Dependencies

* None.

#### Validation Expectations

* `handoff_ageing` returns exact 13 keys; `escalate_overdue_handoffs` is idempotent and preserves audit chain integrity; restricted roles see `NOTE_HELD` on `next_action`.

#### Completion Evidence

* Unit tests in `test_handoff_lifecycle.py`, `test_unaccepted_handoff_csv_api.py`, and `test_handoff_escalation_83.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire BG-010 SLA deadlines and escalation fields into taskqueues, store, sqlstore, progress, and exception_register

#### Context

`taskqueues.overdue_tasks` currently inspects only `handoff.get("due_at")` (`C7`), `work["handoff"]` projects only 7 static keys (`C8`), `sqlstore._queue_fingerprint` hashes `priority_policy` + `as_of` + `MEMBERSHIP_REVISION` (`C16`), and `exception_register.py` calls `handoff_ageing(case, store.as_of)` without `policy` (`C9`).

#### Intent

Connect `BG-010` SLA deadlines and escalation fields across `taskqueues.py`, `store.py`, `sqlstore.py`, `progress.py`, and `exception_register.py` so `Store` and `SqlStore` work projections and exception queues reflect overdue unaccepted handoffs automatically.

#### Boundaries

* Included:
  * `taskqueues.py`:
    * Bump `MEMBERSHIP_REVISION` from `3` to `4` (updating any literal check in `test_sqlqueues.py` if present).
    * In `overdue_tasks`, check `handoff_due = handoff.get("effective_due_at") or handoff.get("due_at") or handoff.get("sla_due_at")` (where `handoff_view` computes `effective_due_at` as the earlier UTC instant of `due_at` and `sla_due_at`), preserving exact behaviour when only `due_at` is passed directly in unit tests (`test_taskqueues.py:249`).
    * In `context(...)`, enrich `work["handoff"]` with `status`, `accountable_owner`, `escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `due_at`, `overdue`, `needs_escalation`, `escalation_target`, `escalation_target_role`, and deterministic `escalation_next_action` alongside all 7 existing keys (`state`, `destination`, `sender`, `proposed_receiver`, `confirmed_receiver`, `chase_owner`, `resident_update_owner`).
    * In `context(...)`, when `not selected and pending and handoff`: if `handoff.get("next_action")` is set, return `text(handoff.get("next_action")) if reason_ok else HELD`; otherwise if `handoff.get("state") == "Escalated"` or `handoff.get("needs_escalation")`, return `text(handoff.get("escalation_next_action"))`; otherwise keep `"Ask the proposed receiver to accept or decline; the sender must keep chasing."`.
  * `store.py`: Read `data.get("handoff_policy")` and `data.get("staff")` in `_work_context` (passing `as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff")` to `handoff_view(c)`), pass `as_of=self.as_of, policy=self.data.get("handoff_policy"), staff=self.data.get("staff")` in `detail`, and include `json.dumps(self.data.get("handoff_policy"), sort_keys=True)` in `Store._queue_candidates`'s `_queue_index` cache key.
  * `sqlstore.py`: Add `"handoff_policy"` to `SqlStore.DOCS`, to the `meta` preload tuple in `_refresh_queue_membership` (alongside `"staff"` if needed for manager target resolution), to the shared-meta invalidation set in `SqlStore.save`, and to `_queue_fingerprint` so `handoff_policy` survives seed/save/reopen and cached `queue_overdue` / `queue_unowned` flags stay synchronized with `Store`.
  * `exception_register.py`: Pass `as_of=as_of, policy=store.data.get("handoff_policy"), staff=store.data.get("staff")` to `handoff_view` (`:148`) and `policy=store.data.get("handoff_policy")` to `handoff_ageing` (`:153`) so `BG-010` SLA breaches automatically raise `stranded_task` items in `ExceptionRegister`.
  * `src/api/src/zava_forward/api/progress.py`: Pass `as_of=store.as_of, policy=store.data.get("handoff_policy"), staff=store.data.get("staff")` to `handoff_view(case)` at line 307.
* Excluded: Changing `taskqueues.DEFINITIONS` or `QUEUE_COLS`.

#### Likely Targets

* `src/core/src/zava_forward/core/taskqueues.py`
* `src/core/src/zava_forward/core/store.py`
* `src/core/src/zava_forward/core/sqlstore.py`
* `src/core/src/zava_forward/core/exception_register.py`
* `src/api/src/zava_forward/api/progress.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_taskqueues.py`, `test_sqlqueues.py`, and `test_exception_register.py` pass; `Store` and `SqlStore` return identical `overdue` and `unowned` case lists under an approved `BG-010` policy.

#### Completion Evidence

* Passing unit tests across `Store` and `SqlStore`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: HTTP API Handoff Queue and Escalation Sweep Routes

### Context

`server.py` currently serves `/api/handoffs`, `/api/handoffs/unaccepted`, and `/api/handoffs/unaccepted.csv` (`C11`). Adding `/api/handoffs/unowned`, `/api/handoffs/escalated`, and `POST /api/handoffs/escalate-overdue` exposes the shared role queues and overdue sweep over HTTP while `test_role_endpoint_inventory.py` (`C19`) verifies role access and canary non-leakage across every server route.

### Intent

Expose role-gated HTTP endpoints for `unowned_handoffs`, `escalated_handoffs`, and `escalate_overdue_handoffs` and register them in `RoleEndpointInventory`.

### Boundaries

* Included: `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py`.
* Excluded: Any modification to `src/api/src/zava_forward/api/web/role-screens.js` or other `web/*.js` files.

### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/tests/test_role_endpoint_inventory.py`

### Dependencies

* P01.

### Validation Expectations

* `RoleEndpointInventory` passes across all 9 roles with zero missing routes and zero canary leaks.

### Completion Evidence

* `test_role_endpoint_inventory.py` and `test_handoff_escalation_api_83.py` passing.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add GET /api/handoffs/unowned, GET /api/handoffs/escalated, and POST /api/handoffs/escalate-overdue and register in role inventory

#### Context

`projection.STAFF_GET` already authorizes `kind="handoffs"` for `STAFF_ROLES` and denies contractors and `Application Administrator` (`C18`). `server._handoff_age_limit` already validates `?max_age_hours=` with a plain-language `400` error (`C11`).

#### Intent

Wire the three handoff visibility/escalation routes in `server.py` and add them to `GET_ENDPOINTS` and `POST_ENDPOINTS` in `test_role_endpoint_inventory.py`.

#### Boundaries

* Included:
  * Register `"/api/handoffs/unowned": "handoffs"` and `"/api/handoffs/escalated": "handoffs"` in `server.get_kind(path)` so central `projection.allowed(u, get_kind(url.path))` grants `STAFF_ROLES` and denies contractors and `Application Administrator`.
  * Extract shared `_parse_max_age_hours(raw)` helper used by `_max_age_hours(url)` and `POST /api/handoffs/escalate-overdue` (rejecting booleans, non-numbers, `NaN`/`inf`, and values outside `0 < v < 1e6` with `"max_age_hours must be a positive number of hours."`).
  * `GET /api/handoffs/unowned` and `GET /api/handoffs/escalated`: Handle alongside `/api/handoffs/unaccepted` using `_max_age_hours(url)` and optional single query parameter `?as_of=` (`400` on invalid timestamp/limit).
  * `POST /api/handoffs/escalate-overdue`: Authorized under central `do_POST` staff gate; check `u["role"] in MANAGER_ROLES` first (raising `PermissionError` -> `403` before body parameter parsing so unauthorized staff always get `403`), then parse optional `as_of`, `max_age_hours`, and `reason` from JSON body, call `s.escalate_overdue_handoffs(...)`, and return `200` JSON summary (`ValueError` -> `400`).
  * `src/api/tests/test_role_endpoint_inventory.py`: Add `"/api/handoffs/unowned"` and `"/api/handoffs/escalated"` to `GET_ENDPOINTS` and `("/api/handoffs/escalate-overdue", {})` to `POST_ENDPOINTS`.
* Excluded: Modifying `web/role-screens.js`.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/tests/test_role_endpoint_inventory.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `403` for contractors/non-managers on sweep, `400` on bad `max_age_hours` or naive `as_of`, `200` for authorized roles, zero canary leaks.

#### Completion Evidence

* Passing `test_role_endpoint_inventory.py` and `test_handoff_escalation_api_83.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Unit Tests and Static/Runtime Verification

### Context

Caller requirement 4 mandates focused unit tests in `src/core/tests/test_handoff_escalation_83.py` (and `src/api/tests/` for extended API endpoints/projections) proving visibility and timely escalation of unaccepted handoffs (`BG-010`), and requirement 5 mandates `ruff check`, `ruff format --check`, `mypy`, and `unittest` across modified projects.

### Intent

Add focused, edge-case-complete core and API tests and run all Focused-tier static and unit test checks cleanly.

### Boundaries

* Included: `src/core/tests/test_handoff_escalation_83.py`, `src/api/tests/test_handoff_escalation_api_83.py`, and Focused-tier CLI verification.
* Excluded: Unrelated test files or browser Playwright suites touching `role-screens.js`.

### Likely Targets

* `src/core/tests/test_handoff_escalation_83.py`
* `src/api/tests/test_handoff_escalation_api_83.py`

### Dependencies

* P01, P02.

### Validation Expectations

* All new and existing unit tests, `mypy`, `ruff check`, and `ruff format --check` exit `0`.

### Completion Evidence

* Captured CLI outputs recorded in `.copilot-tracking/changes/2026-11-15/83-handoff-escalation-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Author focused unit tests in src/core/tests/test_handoff_escalation_83.py and src/api/tests/test_handoff_escalation_api_83.py

#### Context

Tests must fail without the `BG-010` implementation and verify edge cases across lifecycle states, timestamps, policy approval gates, SQLite parity, role visibility, redaction, exception feeds, and sweep idempotency.

#### Intent

Create `src/core/tests/test_handoff_escalation_83.py` and `src/api/tests/test_handoff_escalation_api_83.py`.

#### Boundaries

* Included:
  * `src/core/tests/test_handoff_escalation_83.py`:
    1. Approved `BG-010` policy validation (`Approved` + named owner + routine/urgent hours vs draft/unnamed/invalid policies keeping `OD-09` `None`).
    2. Exact SLA boundary (`elapsed == limit` is within window; `elapsed > limit` is overdue with exact `elapsed_hours` and `overdue_hours`) for both `Sent` (`Offered`) and `Received` states, while `Accepted`, `Rejected` (`Declined`), `Withdrawn`, and `Completed` handoffs never trigger overdue escalation.
    3. Case (`detail["handoff"]`) and queue (`work["handoff"]`, `work["overdue"]`, `work["queues"]`, `work["next_action"]`) projections across both `Store` and `SqlStore` (including `_queue_fingerprint` refresh when `handoff_policy` is approved).
    4. Shared/role queue visibility in `unowned_handoffs`, `unaccepted_handoffs`, and `escalated_handoffs` across sender, proposed receiver, destination-role colleague (`to_role`), escalation target, manager, and unrelated role, including `NOTE_HELD` free-text redaction.
    5. `ExceptionRegister` automatic raising of policy-breached unaccepted handoffs as `stranded_task` items.
    6. `escalate_overdue_handoffs` sweep transitioning overdue `Sent` and `Received` handoffs to `Escalated`, preserving sender `c["owner"]`, maintaining intact audit ledger digest, refusing non-manager callers (`PermissionError`), rejecting naive timestamps (`ValueError`), and remaining idempotent on repeat execution.
  * `src/api/tests/test_handoff_escalation_api_83.py`:
    1. `GET /api/handoffs/unowned`, `GET /api/handoffs/escalated`, `GET /api/handoffs/unaccepted`, `GET /api/handoffs/unaccepted.csv`, and `GET /api/cases/<id>` under an approved `BG-010` policy (verifying destination-role visibility, 13-column CSV preservation, `PR-002` `NOTE_HELD` redaction, contractor `403`, and `400` validation on bad `max_age_hours`/`as_of`).
    2. `POST /api/handoffs/escalate-overdue` manager authorization (`200` for manager, `403` for non-manager/contractor), case/queue projection updates after sweep, and idempotency.
* Excluded: Trivial constant assertions.

#### Likely Targets

* `src/core/tests/test_handoff_escalation_83.py`
* `src/api/tests/test_handoff_escalation_api_83.py`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Both new test modules run cleanly under `unittest` and `mypy`.

#### Completion Evidence

* Passing test outputs.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Execute Focused-tier validation across src/core and src/api and verify role-screens.js guard

#### Context

All changes touch `src/core` and `src/api` under the Focused validation tier.

#### Intent

Verify editable package installation if needed, run `ruff check`, `ruff format --check`, `mypy`, and full `unittest` discovery in `src/core` and `src/api`, and verify zero diff on `web/role-screens.js`.

#### Boundaries

* Included: CLI execution of linters, type checks, unit test suites, and `git diff --name-only` verification.
* Excluded: Pushing to remote.

#### Likely Targets

* `src/core` and `src/api` test and typecheck runners.

#### Dependencies

* P03-T01.

#### Validation Expectations

* Zero warnings/errors across `ruff`, `mypy`, and `unittest`.

#### Completion Evidence

* Recorded command exit codes and test counts in `.copilot-tracking/changes/2026-11-15/83-handoff-escalation-changes.md`.

#### Unresolved Items

* None.
