---
description: "Primary evidence artifact for Issue #83 BG-010 unaccepted handoff visibility and escalation"
---
<!-- markdownlint-disable-file -->

# Task Research: 83-handoff-escalation

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | RPI Agent (`rpi-research`)                                               |
| Status             | Complete                                                                 |
| Artifact path      | .copilot-tracking/research/2026-11-15/83-handoff-escalation-research.md  |

## Research Brief

* What to research: How role-owned handoffs (`sent`, `received`, `accepted`, `rejected`, `escalated`, `completed`) and SLA/escalation windows (`BG-010`, `FR-009`..`FR-011`) are defined in requirements and implemented/projected across `src/core/src/zava_forward/core/` and `src/api/src/zava_forward/api/`, and what deterministic gaps remain for the third acceptance criterion of Issue #83 ("Unaccepted handoffs are visible and escalated within approved times (BG-010)").
* Why it matters: Issue #83 has two completed acceptance criteria and one remaining open acceptance criterion (`BG-010`). Delivering deterministic SLA evaluation, automatic/explicit overdue escalation projection, accountable escalation target/next action visibility, and shared/role queue surfacing completes the backend/projection evidence without breaking active `role-screens.js` WCAG baseline guards.
* Audience or intended use: RPI planning, implementation, and review phases for `feat/ux-83-handoff-escalation` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Scope: `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, prior `#83` tracking evidence, `src/core/src/zava_forward/core/`, `src/core/tests/`, `src/api/src/zava_forward/api/`, and `src/api/tests/`.
* Non-goals: Modifying `src/api/src/zava_forward/api/web/role-screens.js` (unless strictly unavoidable, avoided per caller guard), altering unrelated safety/consent approval boundaries, or pushing to remote.
* Criteria: Every claim grounded with workspace-relative `path:line`; three research waves (Wider, Deeper, Contrarian) completed in order; concrete SLA window and escalation semantics verified against BRD/PRD and existing core/API code.
* Requested outputs: Convergence recommendation for planning `83-handoff-escalation`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | What are the exact BRD/PRD rules for `BG-010` and `FR-009`..`FR-011`, what handoff/queue/SLA behavior already exists in `src/core` and `src/api`, and what exact changes are needed so unaccepted handoffs (`sent`/`received`) are deterministically evaluated, visibly flagged/escalated within approved times, and surfaced across case and queue projections? |
| Codebase scope                   | `docs/brds/`, `docs/prds/`, `src/core/`, `src/api/`, `.copilot-tracking/` |
| External scope                   | none                                                                    |
| Initial internal candidate areas | `src/core/src/zava_forward/core/workflows.py`, `projection.py`, `taskqueues.py`, `store.py`, `rulecards.py`, `src/api/src/zava_forward/api/server.py` |
| Initial external candidate areas | none                                                                    |
| Research posture                 | focused                                                                 |
| Posture provenance               | caller-specified bounded internal feature and validation tier           |
| Explicit limits / deadline       | Avoid modifying `src/api/src/zava_forward/api/web/role-screens.js`; focused validation tier (`ruff`, `mypy`, `unittest` in modified projects); no push |
| Posture-specific completion basis | focused scope and materiality across BRD/PRD, `src/core`, and `src/api` |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | .copilot-tracking/                                                      |
| Known constraints / excluded sources | Backend/API/projection scope avoiding `role-screens.js` conflicts; preserve human accountability boundaries |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` repository instructions          | Validation tiers, branch/commit rules, Markdown style, authority boundaries | Selected: governs repo conventions and focused validation tier |
| Skill               | `rpi-research`                   | Active phase skill for Research                   | Primary research artifact and 3-wave protocol | Selected: mandatory RPI Research phase contract |
| Skill               | `web-design-guidelines` / frontend skills | Web UI styling/review skills             | Web file changes only                        | Skipped: backend/API projection change avoiding `role-screens.js` |
| Research specialist | `hve-core-all:rpi-researcher`    | General delegated research lane worker            | Bounded independent subagent lane            | Skipped (inline): tightly coupled core/API trace across ~6 Python modules is faster and cleaner inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive execution with explicit caller scope, acceptance criterion (`BG-010`), guardrails, and validation tier | N/A (non-interactive) | Proceed with focused inline three-wave cycle |
| Direction change | None at intake                                              | N/A                       | Keep active brief                                  |
| Convergence      | Non-interactive automatic convergence on Alternative 1 | N/A (non-interactive) | Selected policy-gated BG-010 SLA evaluation, enriched projections, shared/role handoff queues, and overdue escalation sweep |

## Scope and Success Criteria

* Scope: `BG-010` and `FR-009`..`FR-011` requirements and `src/core` + `src/api` handoff state, SLA evaluation, escalation transition/flagging, case projection, and shared/role queue surfacing.
* Assumptions:
  * Existing code already implements parts of handoff states (`sent`, `received`, `accepted`, `rejected`, `escalated`, `completed`) and possibly partial waiting views or CSV exports, which must be verified rather than duplicated or broken.
  * Approved SLA thresholds for handoff acceptance may already be encoded in rulecards, constants, or BRD/PRD definitions.
* Success criteria:
  * Every research question is answered with exact `path:line` citations.
  * Existing handoff tests and projections are mapped so backward compatibility is preserved.
  * Alternatives are compared and one convergence approach is selected.

## Task Research Requests

* Explicit requests: Inspect `sent`, `received`, `accepted`, `rejected`, `escalated`, `completed` and `BG-010` SLA windows in `src/core` and `src/api`; ensure unaccepted handoffs are deterministically evaluated against the approved threshold, automatically or explicitly flagged/transitioned as overdue/escalated with visible escalation status, elapsed/overdue hours, escalation target/accountable owner, and next action in queue and case projections, and visible in shared/role queues (`unowned_handoffs` / `unaccepted_handoffs` / `escalated_handoffs`), avoiding `role-screens.js` edits.
* Inferred research questions:
  * How does `BG-010` define "approved times" and accountable escalation targets in BRD/PRD?
  * How are handoffs stored, mutated, and projected in `store.py`, `workflows.py`, `projection.py`, `taskqueues.py`, `exception_feeds.py`, and `server.py`?
  * Does automatic time-based evaluation mutate stored state or project deterministic overdue/escalated status (or support both deterministic read-time evaluation and explicit sweep/escalation action), and how does SQL queue projection (`test_sqlqueues.py` / `store.py`) interact with it?
* Caller constraints and non-goals: Do not edit `role-screens.js` if possible; do not push; leave clean worktree after commit.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| exclude                                                  | Avoid modifying `src/api/src/zava_forward/api/web/role-screens.js` | Caller prompt / Intake | Keep changes in `src/core` and `src/api` Python backend/projections and tests |
| narrow                                                   | Deliver remaining unchecked AC on #83 (`BG-010`) under focused tier | Caller prompt / Intake | Focus on unaccepted handoff SLA visibility and escalation |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | What do BRD `BG-010` and PRD/BRD `FR-009`..`FR-011` specify for handoff acceptance times, visibility, and escalation ownership? | straightforward | H | answered |
| Q2 | How are handoffs currently represented, transitioned, and tested across `workflows.py`, `projection.py`, `taskqueues.py`, `store.py`, and `server.py`? | depth | H | answered |
| Q3 | What gaps currently exist in deterministic SLA evaluation, escalation status/elapsed/overdue hours/target/next-action fields, explicit escalation workflow, and queue projections (`unowned_handoffs` / `unaccepted_handoffs` / `escalated_handoffs`)? | depth | H | answered |
| Q4 | Could read-time escalation vs stored transition conflict with existing handoff tests, SQL queue queries, or `role-screens.js` baseline guards? | breadth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-03/` and `docs/reference/log.md:9917` plus `docs/architecture/cutover-evidence-pack.md:7164` (`handoff_ageing`, `unaccepted_handoffs`, and `feed_unaccepted_handoffs` added in r1, while approved `BG-010` SLA evaluation, projection fields, shared role queues, and escalation sweeps remained open).
* Reused (verified) findings: `HANDOFF_STATE` / `HANDOFF_PENDING` lifecycle in `workflows.py`, 13-column CSV schema on `/api/handoffs/unaccepted.csv`, and `OD-09` non-fabrication rule on unconfigured datasets.
* Superseded / stale: Issue #83 originally cited `BRD FR-009..FR-011`, whereas BRD 0.21 maps handoffs to `FR-017`/`FR-018`/`FR-057` and PRD maps them to `FR-009`/`FR-011` (`C2`, `C3`, `C21`); both are traced here.

## Candidate Research Areas

* Lifecycle and SLA policy representation (`BG-010`, `OD-09`, `EXA-008`, `FR-011`, `AC-014`) across BRD/PRD/Case Study Addendum and `src/core/src/zava_forward/core/workflows.py`.
* Shared work-queue and case projections in `src/core/src/zava_forward/core/taskqueues.py`, `store.py`, `sqlstore.py`, and `exception_register.py` / `exception_feeds.py`.
* Role-scoped and manager-visible handoff queues (`pending_handoffs`, `unaccepted_handoffs`, `unowned_handoffs`, `escalated_handoffs`) and controlled escalation sweep transitions.
* HTTP API routes in `src/api/src/zava_forward/api/server.py` and cross-cutting regression guards (`test_unaccepted_handoff_csv_api.py`, `test_handoff_api.py`, `test_role_endpoint_inventory.py`, `test_list_export_inventory.py`, `projection.py`, and `web/app.js`).

## Cycle 1

### Wave 1: Wider

Investigated requirements, domain contracts, and prior `#83` evidence alongside core and API modules:

* `BG-010`, BRD `FR-057`, and PRD `FR-011` / `AC-014` require accountable role-owned handoffs where ownership stays with the sender until explicit acceptance, message delivery alone never closes a handoff, and unaccepted handoffs are visible and escalated within approved times (`C1`, `C2`, `C3`).
* `EXA-008` in `docs/case_study_48_addendum.md:210` defines the exercise timing model (receipt confirmation 24h, chase 48h, escalation 72h; sender retains chase responsibility until explicit acceptance), while `OD-09` (`C21`) forbids inventing an unapproved default threshold when no approved policy is configured.
* `workflows.py` models `Offered` (`Sent`), `Received`, `Accepted`, `Declined` (`Rejected`), `Withdrawn`, `Escalated`, and `Completed`, keeps `c["owner"]` unchanged until `accept_handoff`, provides per-case `escalate_handoff`, and exposes `handoff_ageing` / `unaccepted_handoffs` (`C4`, `C5`, `C6`).
* `taskqueues.py` projects `unowned` membership whenever `handoff["state"] in ("Offered", "Received", "Escalated")` and projects `overdue` membership only when explicit `handoff["due_at"]` has elapsed (`C7`, `C8`).
* `exception_register.py` calls `handoff_ageing(case, store.as_of)` without any policy threshold and feeds `needs_escalation` rows into `feed_unaccepted_handoffs` (`C9`, `C10`).
* `server.py` exposes `GET /api/handoffs`, `GET /api/handoffs/unaccepted`, `GET /api/handoffs/unaccepted.csv`, and per-case handoff POST routes (`C11`).

### Wave 2: Deeper

Examined exact projection schemas, SQLite/MSSQL queue persistence, and visibility gaps:

* **Gap A - No approved `BG-010` policy evaluation**: Unlike `taskqueues.approved_priority(policy)` (`C12`), `workflows.py` has no `approved_handoff_policy` resolver for `store.data.get("handoff_policy")`. Even when an owner-approved `BG-010` SLA policy (`status == "Approved"`, named human `owner`, positive finite `acceptance_hours` and optional `urgent_acceptance_hours`, escalation manager/role) is configured on the dataset, `handoff_view`, `handoff_ageing`, `unaccepted_handoffs`, `taskqueues.overdue_tasks`, and `exception_register.py` ignore it unless `?max_age_hours=` is supplied on an individual HTTP query (`C5`, `C6`, `C7`, `C9`).
* **Gap B - Missing SLA & escalation fields in case and queue projections**:
  * `handoff_view(c)` (`C4`) omits `escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `sla_due_at`, `effective_due_at`, `overdue`, `needs_escalation`, `escalation_target`, `escalation_target_code`, `escalation_target_role`, and structured `escalation_action`.
  * `taskqueues.context(...)` (`C8`) projects only 7 keys under `work["handoff"]` (`state`, `destination`, `sender`, `proposed_receiver`, `confirmed_receiver`, `chase_owner`, `resident_update_owner`), omitting `status`, `accountable_owner`, `escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `due_at`, `overdue`, `needs_escalation`, `escalation_target`, and `escalation_action`. When an unaccepted handoff breaches its SLA without a stage-gate blocker or custom `next_action`, `work["next_action"]` still emits generic chase copy rather than escalation guidance.
  * `taskqueues.overdue_tasks` (`C7`) checks only `handoff.get("due_at")`, so a handoff without per-item `due_at` that breaches an approved `BG-010` `acceptance_hours` window never enters `work["overdue"]` or the `overdue` queue (`queue_overdue` in `SqlStore` / `MssqlStore`).
* **Gap C - Silent unaccepted handoffs in role queues & missing sweep transition**:
  * `pending_handoffs` and `unaccepted_handoffs` (`C6`) filter strictly to `user["code"] in (from_code, to_code) or user["role"] in MANAGER_ROLES`. Neither an assigned `escalation_owner_code` (when distinct from sender/receiver) nor colleagues in the destination role (`to_role`) have shared role-owned queue views (`unowned_handoffs`, `escalated_handoffs`) to spot unaccepted or overdue role-targeted handoffs when a proposed individual receiver is unavailable.
  * Only per-case manual `escalate_handoff` exists; there is no deterministic sweep transition (`escalate_overdue_handoffs`) to transition all `Offered`/`Received` handoffs past `due_at` or approved `BG-010` `acceptance_hours` into `state = "Escalated"` with full provenance, history, and audit logging while keeping `accountable_owner` with the sender.

### Wave 3: Contrarian

Challenged candidate designs against strict repository invariants and regression suites:

* **Challenge 1 - Preserve exact 13-key contract and `OD-09` null limit on `handoff_ageing` / `/api/handoffs/unaccepted(.csv)`**:
  * `test_unaccepted_handoff_csv_api.py` (`C13`) asserts `len(row) == 13` and `[list(r) for r in rows] == [FIELDS] * len(rows)`. Adding keys to `handoff_ageing` would break CSV parity tests.
  * `test_handoff_api.py` (`C14`) and `web/app.js` (`C15`, `x.approved_limit_hours === null`) assert that when `DATA` has no approved policy (`OD-09`), `approved_limit_hours` MUST remain `None` and `limit_note` MUST remain `"Approved escalation time not set (OD-09)"`.
  * *Resolution*: Keep `handoff_ageing` at its exact 13 `FIELDS`. Resolve `approved_limit_hours` from `store.data.get("handoff_policy")` only when `approved_handoff_policy(policy)` validates `status == "Approved"`, a named human `owner`, and positive finite `acceptance_hours` (matching `taskqueues.approved_priority`, `C12`). Unapproved/default seed `DATA` retains `None` and `"Approved escalation time not set (OD-09)"`.
* **Challenge 2 - Preserve the 6-column `QUEUE_COLS` schema in `SqlStore` and `MssqlStore`**:
  * `test_taskqueues.py` asserts `len(spec["definitions"]) == 6`, and `sqlstore.py` (`C16`) / `mssqlstore.py` (`C17`) define exact 6 `queue_*` DDL columns (`new`, `priority`, `stale`, `blocked`, `overdue`, `unowned`).
  * *Resolution*: Keep `DEFINITIONS` at 6 queues, feed `effective_due_at` (`due_at` or `sla_due_at`) into `taskqueues.overdue_tasks` so SLA-breached unaccepted handoffs automatically join `overdue` alongside `unowned`, bump `taskqueues.MEMBERSHIP_REVISION`, include `handoff_policy` in `sqlstore._queue_fingerprint`, and expose `unowned_handoffs`, `unaccepted_handoffs`, and `escalated_handoffs` on `WorkflowMixin` and `/api/handoffs/*` without touching DDL columns or `web/role-screens.js`.
* **Challenge 3 - Enforce `PR-002` role-matrix & free-text canary redaction (Issue #116)**:
  * `projection.py` (`C18`) defines `NOTE_KEYS` (`note`, `answer_note`, `next_action`, etc.) and redacts them with `NOTE_HELD` for roles outside `reason_roles()`. `test_role_endpoint_inventory.py` (`C19`) regex-scans `server.py` for every `/api/...` route, requires registration in `GET_ENDPOINTS` / `POST_ENDPOINTS`, and tests all 9 roles against free-text canary leaks.
  * *Resolution*: Never copy staff free-text (`note`, `answer_note`, `next_action`) into non-`NOTE_KEYS` fields such as `escalation_action`; pass role-queue items through `projection.hold_notes` when `not projection.can_see_reason(user)` and register new `/api/handoffs/*` routes in `test_role_endpoint_inventory.py` (`test_list_export_inventory.py`, `C20`, audits only `web/*.js` endpoints).

## Evidence Log

* `C1`: `docs/case_study_48_addendum.md:210` - `EXA-008` defines exercise handoff timing structure (receipt confirmation 24h, chase 48h, escalation 72h) and sender chase accountability until acceptance.
* `C2`: `docs/brds/agentic-retrofit-programme-brd.md:1695` - `FR-057` / `BG-010` require exception-led visibility for overdue handoffs with named escalation owner and sender retention until explicit acceptance.
* `C3`: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1386` - `FR-011` and `AC-014` (`:2110`) define distinct `sent`, `received`, `accepted`, `rejected`, `escalated`, `completed` states and accountable visibility.
* `C4`: `src/core/src/zava_forward/core/workflows.py:17` - `HANDOFF_STATE`, `HANDOFF_PENDING`, and `handoff_view(c)` (`:43`).
* `C5`: `src/core/src/zava_forward/core/workflows.py:60` - `handoff_ageing(c, as_of, max_age_hours=None)` 13-field projection.
* `C6`: `src/core/src/zava_forward/core/workflows.py:293` - `escalate_handoff`, `pending_handoffs` (`:322`), and `unaccepted_handoffs` (`:336`).
* `C7`: `src/core/src/zava_forward/core/taskqueues.py:107` - `overdue_tasks` evaluates `handoff.get("due_at")` at `:158`.
* `C8`: `src/core/src/zava_forward/core/taskqueues.py:348` - `context(...)` computes `unowned` membership, pending-handoff `next_action` (`:371`), and `work["handoff"]` (`:384`).
* `C9`: `src/core/src/zava_forward/core/exception_register.py:150` - `ExceptionRegister` calls `handoff_ageing(case, store.as_of)` and feeds `needs_escalation` rows to `feed_unaccepted_handoffs`.
* `C10`: `src/core/src/zava_forward/core/exception_feeds.py:89` - `feed_unaccepted_handoffs` raises deterministic `stranded_task` items on `ExceptionQueue`.
* `C11`: `src/api/src/zava_forward/api/server.py:813` - `GET /api/handoffs`, `GET /api/handoffs/unaccepted`, `GET /api/handoffs/unaccepted.csv`, and case handoff POST actions (`:1578`).
* `C12`: `src/core/src/zava_forward/core/taskqueues.py:48` - `approved_priority(policy)` pattern requiring `status == "Approved"` and a named `owner`.
* `C13`: `src/api/tests/test_unaccepted_handoff_csv_api.py:24` - Enforces exact 13 `FIELDS` and key order on `unaccepted_handoffs` JSON and CSV responses.
* `C14`: `src/api/tests/test_handoff_api.py:135` - Enforces `approved_limit_hours is None` when no approved policy or query limit is configured.
* `C15`: `src/api/src/zava_forward/api/web/app.js:832` - `waitingRows` validates `approved_limit_hours === null` on unapproved default seed data.
* `C16`: `src/core/src/zava_forward/core/sqlstore.py:59` - `QUEUE_COLS` and `_queue_fingerprint` (`:761`) cache the 6 task-queue columns in SQLite.
* `C17`: `src/core/src/zava_forward/core/mssqlstore.py:48` - Hardcoded `queue_*` columns in T-SQL `TABLES["cases"]`.
* `C18`: `src/core/src/zava_forward/core/projection.py:30` - `NOTE_KEYS`, `STAFF_GET`, and `hold_notes` redaction boundary.
* `C19`: `src/api/tests/test_role_endpoint_inventory.py:17` - Full route coverage check and 9-role canary leak matrix.
* `C20`: `src/api/tests/test_list_export_inventory.py:27` - Audits endpoints invoked from `web/*.js`.
* `C21`: `docs/architecture/cutover-evidence-pack.md:7164` and `docs/reference/log.md:3199` - `OD-09` non-fabrication boundary and prior `#83` r1 status.

## Synthesis and Selected Recommendation

Select **Alternative 1 (Convergence)**:

1. **Deterministic BG-010 SLA Policy & Evaluation (`workflows.py`)**:
   * Add `approved_handoff_policy(policy)` and `approved_handoff_limit_hours(policy, urgency=...)` validating `status == "Approved"`, named human `owner`, and positive finite `acceptance_hours` (with optional `urgent_acceptance_hours`, `escalation_owner`, `escalation_owner_code`, `escalation_role`).
   * Add `handoff_sla(c, *, as_of=None, policy=None, max_age_hours=None, staff=None)` computing `escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `sla_due_at`, `effective_due_at`, `overdue`, `needs_escalation`, `escalation_target`, `escalation_target_code`, `escalation_target_role`, and structured `escalation_action`.
   * Enrich `handoff_view(c, *, as_of=None, policy=None, max_age_hours=None, staff=None)` with these fields while preserving all existing keys; wire `store.as_of`, `store.data.get("handoff_policy")`, and `store.data.get("staff")` in `store.detail`, `store._work_context`, `progress.py`, and `exception_register.py`.
   * Pass `policy=self.data.get("handoff_policy")` in `unaccepted_handoffs` and `exception_register.py` while keeping `handoff_ageing` at its exact 13 `FIELDS` and preserving `None` / `"Approved escalation time not set (OD-09)"` when no approved policy is present.
2. **Queue Projections & SQLite Cache Sync (`taskqueues.py`, `sqlstore.py`)**:
   * Update `taskqueues.overdue_tasks` to evaluate `handoff.get("effective_due_at") or handoff.get("due_at") or handoff.get("sla_due_at")` (keeping `due_at` exact value in the overdue entry) so `BG-010` SLA breaches automatically enter `work["overdue"]` and the `overdue` queue alongside `unowned`.
   * Enrich `work["handoff"]` and overdue/escalated default `work["next_action"]` in `taskqueues.context` with `status`, `accountable_owner`, `escalation_status`, `elapsed_hours`, `overdue_hours`, `approved_limit_hours`, `due_at`, `overdue`, `needs_escalation`, `escalation_target`, `escalation_target_role`, and safe `escalation_action` (respecting `reason_ok` / `HELD`).
   * Bump `taskqueues.MEMBERSHIP_REVISION` and include `handoff_policy` in `sqlstore._queue_fingerprint`.
3. **Shared/Role Handoff Queues & Controlled Overdue Escalation Sweep (`workflows.py`, `server.py`)**:
   * Extend `pending_handoffs` and `unaccepted_handoffs` visibility to include `escalation_owner_code`.
   * Add `unowned_handoffs(user, as_of=None, max_age_hours=None)` and `escalated_handoffs(user, as_of=None, max_age_hours=None)` on `WorkflowMixin` visible to sender (`from_code`), proposed receiver (`to_code`), destination role (`to_role`), escalation target (`escalation_owner_code` / `escalation_target_role`), and `MANAGER_ROLES`, with `projection.hold_notes` redaction for roles outside `reason_roles()`.
   * Add `escalate_overdue_handoffs(user, *, as_of=None, max_age_hours=None, metadata=None)` for `MANAGER_ROLES` to deterministically transition all overdue `Offered`/`Received` handoffs to `Escalated` with audit, history, and provenance while preserving `c["owner"]`.
   * Expose `GET /api/handoffs/unowned`, `GET /api/handoffs/escalated`, and `POST /api/handoffs/escalate-overdue` in `server.py` and register them in `test_role_endpoint_inventory.py`. Leave `web/role-screens.js` untouched.

## Alternatives Considered

* **Alternative 2 (Rejected - Hardcode 72h fallback without approved policy)**: Violates `OD-09` (`C21`) and breaks `test_handoff_api.py` (`C14`), `test_unaccepted_handoff_csv_api.py` (`C13`), `test_handoff_lifecycle.py`, and `web/app.js` (`C15`).
* **Alternative 3 (Rejected - Add a 7th `queue_escalated` column to `taskqueues.DEFINITIONS`)**: Breaks `SqlStore` / `MssqlStore` 6-column `QUEUE_COLS` DDL assertions (`C16`, `C17`).

## Readiness

* **Research Disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Blockers**: None
