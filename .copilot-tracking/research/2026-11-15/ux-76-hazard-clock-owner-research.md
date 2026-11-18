<!-- markdownlint-disable-file -->

# Task Research: ux-76-hazard-clock-owner

| Field              | Value                                                                       |
|--------------------|-----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                  |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                     |
| Status             | Complete                                                                    |
| Artifact path      | .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-research.md  |
| Planning Readiness | Ready                                                                       |
| Disposition        | executed                                                                    |

## Research Brief

* What to research: Inspect how role-based task queues, `my_cases_today` / shared work queue projections, and case cards project and render hazard and safeguarding items across `src/core/src/zava_forward/core/` (`taskqueues.py`, `projection.py`, `hazard.py`, `home_case.py`, `sqlstore.py`, `mssqlstore.py`, `exception_queue.py`) and `src/api/src/zava_forward/api/` (`server.py`, `workbench.py`, `web/app.js`, `web/role-screens.js`), plus applicable PRD/BRD requirements (`FR-003`, `FR-004`, `FR-032`, `FR-034`, `SA-001` to `SA-003`, `SA-007`) and baseline guard tests (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`).
* Why it matters: Six of seven acceptance criteria on Issue #76 ("Role-based task queues, case card and shared work queue") are already satisfied; the sole remaining unchecked criterion (`Hazard and safeguarding items show a clock and named owner`) is safety-critical under Awaab's Law and safeguarding response rules and must never omit or anonymize clock state or accountable ownership.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases for `ux-76-hazard-clock-owner`.
* Scope: `src/core/src/zava_forward/core/`, `src/core/tests/`, `src/api/src/zava_forward/api/`, `src/api/tests/`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/brds/agentic-retrofit-programme-brd.md`, and component READMEs (`src/core/README.md`, `src/api/README.md`).
* Non-goals: Pushing to remote, unrelated visual overhauls, breaking counted baseline guards, or modifying `src/api/src/zava_forward/api/web/role-screens.js` unless strictly unavoidable.
* Criteria: Every hazard and safeguarding item across role queues, shared work queue / `my_cases_today`, and case card responses explicitly includes and displays (1) a statutory/operational clock (`clock_status`, `clock_remaining_hours` / `clock_deadline_utc`, `clock_label`, failing closed with an explicit clock state when timestamps are missing) and (2) a named accountable owner (`named_owner` / `owner_role` + `owner_id` / `accountable_owner`, never blank or anonymous, surfacing escalation owner and unassigned flag when unallocated); existing FR-034 consistency and baseline UI/export guards remain green.
* Requested outputs: Synthesized evidence log, requirement and code-path mapping, evaluation of implementation alternatives, convergence recommendation, and planning readiness record.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How are hazard and safeguarding items currently stored, projected, and rendered in role queues, `my_cases_today` / shared work queue, and case cards, and what contract ensures every such item always exposes and displays both a fail-closed clock and a non-blank named accountable owner? |
| Codebase scope                       | `src/core/`, `src/api/`, `docs/prds/`, `docs/brds/`, `docs/reference/`                                                                                  |
| External scope                       | none (repository regulatory snapshots and codebase contracts only)                                                                                      |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/taskqueues.py`, `projection.py`, `hazard.py`, `home_case.py`, `sqlstore.py`; `src/api/src/zava_forward/api/server.py`, `workbench.py`, `web/app.js`, `web/role-screens.js`; `docs/prds/zava-forward-retrofit-programme-demonstrator.md` |
| Initial external candidate areas     | none                                                                                                                                                    |
| Research posture                     | balanced                                                                                                                                                |
| Posture provenance                   | default (bounded internal task with named modules and adjacent guard tests/UI consumers that could materially affect design)                             |
| Explicit limits / deadline           | Avoid modifying `src/api/src/zava_forward/api/web/role-screens.js` if possible; preserve counted baseline guards; focused validation tier; do not push  |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across core/SQL queue projections, case cards, API/UI rendering, FR-034 agreement, and baseline guards    |
| Edits allowed during research?       | no, research-only                                                                                                                                       |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                                            |
| Known constraints / excluded sources | Codebase and local regulatory/PRD snapshots only; preserve human/resident approval boundaries and Awaab's Law statutory framing                         |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                                             | Scoped authority or output contract                                              | Selected / skipped reason                                                                                  |
|---------------------|-----------------------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace files and tracking artifacts   | Adds validation-tier rules, web guidance, regulatory citation rules, commit rules | Selected automatically as repository-wide instruction                                                      |
| Skill               | `web-design-guidelines`           | Conditional match if web UI files (`web/app.js`, HTML) are edited | Pre-edit and review checklist for changed web UI files                           | Deferred during read-only Research; activate before any web file edit if convergence includes web changes |
| Skill               | `redesign-existing-projects`      | Existing-app UI design improvements                              | Preserves Fluent 2, WCAG baseline, and plain-language standard                   | Skipped for Research: task is targeted hazard/safeguarding clock & owner projection, not a visual redesign |
| Research specialist | `hve-core-all:rpi-researcher`     | Registered general RPI research lane worker                      | Independent subagent lane artifact                                               | Skipped: tightly coupled trace across core projection -> API -> UI rendering fits inline inspection best   |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                      | Answers / unanswered | Resulting decision or selected further research       |
|------------------|------------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------|
| Intake           | Non-interactive session with complete caller brief, named targets, guard constraints, and validation rules | N/A (non-interactive)| Proceed with `balanced` posture and `convergence` mode |
| Direction change | None needed; Wave 1-3 findings confirmed zero-edit reuse of `role-screens.js` via `workSummary`            | N/A                  | Retain `role-screens.js` untouched                    |
| Convergence      | Evidence supports one shared `taskqueues.py` + `workflows.py` + `web/app.js` contract                      | N/A                  | Converge on Option A and advance to `rpi-plan`        |

## Scope and Success Criteria

* Scope: Hazard and safeguarding representation, clock calculation, and named accountable owner resolution across `src/core` (`taskqueues.py`, `projection.py`, `hazard.py`, `home_case.py`, `sqlstore.py`, `mssqlstore.py`, `exception_queue.py`) and `src/api` (`server.py`, `workbench.py`, `web/`), plus PRD/BRD requirements (`FR-003`, `FR-004`, `FR-032`, `FR-034`, `SA-001`..`SA-003`, `SA-007`) and baseline guard tests.
* Assumptions:
  * Earlier Issue #76 work delivered `my_cases_today`, role task queues, filters/sorts, blocked-step reason/owner/next-action, FR-034 view agreement, and FR-032 single reset, but hazard and safeguarding items may still lack explicit structured and rendered clock + named owner fields across all queue and case-card surfaces.
  * `sqlstore.py` / `mssqlstore.py` may either delegate to `taskqueues.py` / `projection.py` or build SQL projections directly; this must be verified rather than assumed.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one convergence recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Inspect how role-based task queues, `my_cases_today` / shared work queue projection, and case cards project hazard and safeguarding items in `src/core/src/zava_forward/core/` and `src/api/src/zava_forward/api/`.
  * Determine how to ensure every hazard and safeguarding item in queue projections and case card responses explicitly includes and displays a statutory/operational clock (`clock_status`, `clock_remaining_hours` / `clock_deadline_utc`, `clock_label`, failing closed when timestamps are missing) and a named accountable owner (`named_owner` / `owner_role` + `owner_id` / `accountable_owner`, never blank or anonymous, surfacing escalation owner and unassigned flag if unallocated).
  * Verify constraints around `src/api/src/zava_forward/api/web/role-screens.js` and counted baseline guards (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`).
* Inferred research questions:
  * How are hazard and safeguarding items represented on a home/case record in synthetic seed data, JSON store, and SQLite/MSSQL stores?
  * Does `hazard.py` already compute Awaab's Law 24h / 7d / 14d clocks or safeguarding response clocks, and what fields/statuses does it emit?
  * How is staff roster / named owner resolved across `identity.py`, `profile.py`, `taskqueues.py`, `projection.py`, and `FR-034` agreement checks?
  * How do `workbench.py`, `server.py`, `web/app.js`, and `web/role-screens.js` render `my_cases_today`, role task queues, shared work queue, and case cards?
* Caller constraints and non-goals: Avoid modifying `web/role-screens.js` if possible; preserve counted baseline guards; focused tier validation; commit locally with `Refs #76`, do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Deliver remaining unchecked AC on #76: `Hazard and safeguarding items show a clock and named owner`     | Caller intake brief | Focuses investigation on hazard/safeguarding clock and named-owner surfaces        |
| exclude                                                  | Avoid editing `web/role-screens.js` if possible; do not break counted baseline tests; do not `git push` | Caller intake brief | Requires checking how `app.js` / `server.py` / `workbench.py` render queue & cards |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type            | Priority | Status |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|--------|
| Q1 | What do PRD (`FR-003`, `FR-004`, `FR-032`, `FR-034`, `SA-001..003`, `SA-007`), BRD, and regulatory snapshots specify for hazard/safeguarding clocks and named owners? | breadth         | H        | answered |
| Q2 | How do `workflows.py` and `taskqueues.py` model hazards, safeguarding referrals/flags, clocks, and owners on case records?                        | depth           | H        | answered |
| Q3 | How do `taskqueues.py`, `projection.py`, `store.py`, `sqlstore.py`, and `mssqlstore.py` project `my_cases_today`, role queues, shared work queue, and case cards? | depth           | H        | answered |
| Q4 | How are named staff owners / escalation owners resolved across `store.py` / `taskqueues.py` / `projection.py`, and how is FR-034 cross-view agreement enforced? | depth           | H        | answered |
| Q5 | How does `src/api` (`server.py`, `web/app.js`, `web/role-screens.js`) expose and display queue rows and case cards, and what do the baseline guard tests enforce? | breadth         | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/regulatory/README.md`, `docs/reference/research/sector/housing-association-primer.md`, GitHub Issue #76 body, and prior Issue #76 research/review artifacts from `2026-10-16` and `2026-10-18`.
* Reused (verified) findings: Awaab's Law Phase 1 is in force from 27 October 2025 (`SI 2025/1042`), Phase 2 guidance targets 30 November 2026 (`docs/reference/regulatory/README.md`); Issue #76 has 6/7 criteria checked and only `Hazard and safeguarding items show a clock and named owner` unchecked.
* Superseded / stale: Issue #76 body still mentions `Delivered in mvp/`; per repository instructions, `mvp/` was retired at cut-over on 2026-10-27 and `src/` (`core`, `api`, etc.) is canonical. Initial candidate names `hazard.py`, `exception_queue.py`, and `workbench.py` do not exist as separate modules; the live modules are `workflows.py`, `taskqueues.py`, `store.py`, `sqlstore.py`, `projection.py`, `server.py`, `web/app.js`, and `web/role-screens.js`.

## Cycle 1 Execution (Wider, Deeper, Contrarian)

### Wave 1: Wider (Standards, Regulatory Boundaries, and Surface Inventory)

* Regulatory and PRD boundaries (`C1`, `C2`, `C3`):
  * Under `SI 2025/1042` (`The Hazards in Social Housing (Prescribed Requirements) (England) Regulations 2025`, legislation snapshot in force 27 October 2025, reg. 5(8)), emergency hazards carry a 24-hour action period from awareness, while significant damp and mould hazards carry statutory investigation and make-safe timescales managed by the landlord's hazard and repairs service (`C1`).
  * `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (`SA-001`..`SA-003`, `SA-007`, `FR-003`, `FR-004`, `FR-032`, `FR-034`, `CON-001`) and `rulecards.py` (`RULE-003`) require every hazard and safeguarding item to display a visible clock and named owner that are never hidden by simplification (`SA-007`), never use internal jargon (`gate`, `hold`, `provenance`, `trace` banned from UI copy by `SA-003`), keep `page_cases` and `detail` projections in cross-view agreement (`FR-034`), and preserve external hazard-service timing authority (`RULE-003`, `CON-001`) (`C2`, `C3`).
* Queue and case-card surface inventory (`C4`, `C5`, `C6`, `C7`):
  * `GET /api/cases` (`server.py:751`) serves `My cases today` (`view="mine"`), `All open cases` shared work queue (`view="all"`), task-queue filters (`queue=new|priority|stale|blocked|overdue|unowned`), and every specialist role screen queue via `Store.page_cases` (`store.py:368-406`) and `SqlStore.page_cases` (`sqlstore.py:1466-1505`, inherited by `MssqlStore`) (`C4`, `C5`).
  * `GET /api/cases/{case_id}` (`server.py:993`) serves case card detail via `Store.detail` (`store.py:462-520`) (`C6`).
  * In the web UI, `listView` (`web/app.js:907`), every specialist role screen in `web/role-screens.js:98`, and `caseView` (`web/app.js:808, 1086, 1132, 1149, 1154`) all call the shared `workSummary(work)` helper (`web/app.js:797-805`), while `safetyPanel` (`web/app.js:1586-1795`) renders per-item safety cards on the case card (`C7`).

### Wave 2: Deeper (Data Contracts, Clock Semantics, Owner Resolution, and Store Parity)

* Current `taskqueues.context` and `workflows.hazard_view` gaps (`C8`, `C9`, `C10`):
  * `taskqueues.context` (`taskqueues.py:211-265`) projects active entries from `case.get("hazards", [])` into `work["hazard_clocks"]` with legacy fields (`owner`, `owner_named`, `owner_status`, `response_state`, `resident_update_state`, `aware_at`, `elapsed_hours`, `response_due_at`, `resident_update_due_at`, `authority`), but:
    1. It does not inspect safeguarding records (`case.get("safeguarding_items")`, `case.get("safeguarding")`, or `"Safeguarding"` category/kind items), and `"Safeguarding"` is absent from `HAZARD_CATEGORIES` (`workflows.py:15`) and `HAZ_CATEGORIES` (`web/app.js:1428`) (`C8`, `C9`).
    2. It does not emit explicit statutory/operational clock fields (`clock_status`, `clock_remaining_hours`, `clock_deadline_utc`, `clock_label`, `clock_basis`) with an explicit fail-closed state when both `response_due_at` and valid non-future `aware_at` are missing (`C8`).
    3. When no direct follow-up owner is allocated on an item, `clock["owner"]` is `"Unknown"` without structured accountable-owner fields (`named_owner`, `accountable_owner`, `owner_role`, `owner_id`, `unassigned`, `escalation_owner`, `escalation_owner_role`, `escalation_owner_id`) (`C8`).
    4. `workflows.hazard_view` (`workflows.py:101-111`) and `Store.detail` (`store.py:493-496`) do not attach the computed clock or accountable-owner fields to `detail["hazards"]` and do not project `detail["safeguarding_items"]` (`C9`, `C10`).
* Store parity and redaction (`C5`, `C11`):
  * Both `Store.page_cases` (`store.py:397`), `SqlStore.page_cases` (`sqlstore.py:1497`), and `Store.detail` (`store.py:495`) call `self.work_context(c, user)` -> `Store._work_context(c, user, data, cases)` (`store.py:414-425`), which has access to `data.get("staff", [])` for deterministic owner ID/role and escalation-owner resolution (`C5`, `C10`).
  * `projection.contractor_summary` (`projection.py:85-89`) and `projection.contractor_detail` (`projection.py:92-104`) use strict field allowlists (`SUMMARY_FIELDS`, `DETAIL_FIELDS`) that withhold `work`, `hazard`, `safeguarding`, `hazards`, and `safeguarding_items` from contractors. `projection.redact_staff_detail` (`projection.py:147-195`) preserves `work` across `hold_notes(d)` (`projection.py:173-176`) while replacing free-text `NOTE_KEYS` (`note`, `source`, `job`, etc.) with `NOTE_HELD` for staff roles without `can_see_reason(user)`. Thus structured clock and named-owner fields remain visible to all staff roles (`SA-007`) without leaking free-text safeguarding notes (`C11`).

### Wave 3: Contrarian (Regression Traps, Baseline Guards, and Compatibility Invariants)

* Contrarian check 1 — `test_taskqueues.py` unrecorded follow-up owner contract (`C12`):
  * `test_unnamed_clock_owner_is_stated_plainly_and_never_invented` (`src/core/tests/test_taskqueues.py:188-206`) asserts that when `accepted_by`, `sender`, and `owner` are absent on a hazard, `clock["owner"] == "Unknown"`, `clock["owner_named"] is False`, `"No named follow-up owner is recorded"` is in `clock["owner_status"]`, and `case["owner"]` is in `clock["owner_status"]`.
  * Consequence: Overwriting `clock["owner"]` would break `test_taskqueues.py`. Preserving `clock["owner"]` / `clock["owner_named"]` / `clock["owner_status"]` for the direct follow-up slot while adding explicit `named_owner`, `accountable_owner`, `owner_role`, `owner_id`, `unassigned`, `escalation_owner`, `escalation_owner_role`, and `escalation_owner_id` satisfies both invariants cleanly: unallocated items explicitly state `unassigned=True` and surface the named `escalation_owner` as `named_owner` / `accountable_owner` so a named accountable owner is never blank or anonymous (`C12`).
* Contrarian check 2 — `test_role_screens.py` VM slice and `role_screens_browser_check.py` `.safety-clock` count (`C13`, `C14`):
  * `src/api/tests/test_role_screens.py:168-169` executes `app.slice(app.indexOf("function workSummary("), app.indexOf("function workSteps("))` inside an isolated Node `vm` context without the rest of `web/app.js`, and passes synthetic legacy `hazard_clocks` dicts that omit new fields (`test_role_screens.py:135-146`). Therefore `function workSummary(work)` must remain immediately above `function workSteps(work)`, must be self-contained (using only `h` and JS built-ins), and must degrade cleanly without `undefined`/`NaN` when legacy fixture clocks omit `clock_label` or `named_owner` (`C13`).
  * `src/api/checks/role_screens_browser_check.py:448-458` asserts `link.locator(".safety-clock").count() == len(work["hazard_clocks"])` and verifies that `aware_at`, `owner`, `response_due_at`, `resident_update_due_at`, and `f"{clock['authority']} owns timing."` appear in `.safety-clock` text, plus `link.locator(".flag.danger").count() == int(bool(row.get("hazard")))` (`role_screens_browser_check.py:431`). Including active safeguarding clocks inside `work["hazard_clocks"]` (with `item_kind="safeguarding"`, and also exposing `work["safeguarding_clocks"]` for direct filtering) plus reflecting open safeguarding items in `insights.has_hazard` / `Store.summary()["hazard"]` keeps every `.safety-clock` and `.flag.danger` invariant 1-to-1 across `app.js` and `role-screens.js` without editing `role-screens.js` (`C14`).
* Contrarian check 3 — `test_safety_panel_ux.py` `<dl class="safety-facts">` exact `<dt>` count (`C15`):
  * `src/api/tests/test_safety_panel_ux.py:162-165` and `178` assert `facts.querySelectorAll("dt").length === 4` and `!text(card.querySelector(".safety-facts")).includes("Unknown")`.
  * Consequence: Adding `<dt>` rows inside `.safety-facts` would break `test_safety_panel_ux.py`. Instead, rendering a dedicated `<p class="safety-clock-owner">` summary block inside `li.safety-item` above `<dl class="safety-facts">` (with plain-language non-`"Unknown"` phrasing even if inspected, and keeping `.safety-facts` at 4 `<dt>` pairs) plus rendering standalone `c.safeguarding_items` when non-empty preserves both `test_safety_panel_ux.py` and `case_view_ux_browser_check.py:275` (`li.safety-item` count 3 on standard 3-hazard fixture cases) (`C15`).
* Contrarian check 4 — `resident_preview_fixture.py` canary `safeguarding={"note": ...}` (`C16`):
  * `src/core/src/zava_forward/core/synthetic/resident_preview_fixture.py:102` attaches `safeguarding=dict(note=f"{CANARY}-SAFEGUARDING-NOTE-{cid}")` to ordinary cases `SYN-C1` and `SYN-C2`, which `_drive()` then takes through `store.issue_work_order(...)` (`resident_preview_fixture.py:233`).
  * Consequence: A bare `{"note": ...}` canary container (no referral/item metadata keys beyond `"note"`) is a free-text note fixture, not an open safeguarding item, and must not block `issue_work_order`. Active safeguarding items are extracted from `case["safeguarding_items"]` (any list of dicts, including `[{}]`), `case["safeguarding"]` when a `list` of dicts or a `dict` with item keys beyond `"note"`, and any `case["hazards"]` entry with `category == "Safeguarding"` or `kind == "safeguarding"` (`C16`).
* Contrarian check 5 — Counted baseline guards (`C17`, `C18`):
  * `test_accessibility_baseline.py` pins `INVALID_ATTR_FLOOR = 8` (`aria-invalid` across `web/*.js`), `DATA_TABLE_COUNT = 13` (`h("table",` across `web/*.js`), and `FIXED_RULE_CAP = 2` (`position:fixed` in `style.css`) (`C17`).
  * `test_epic149_form_error_summary_associations.py` forbids `RAW_ERROR = re.compile(r"\b(?:undefined|NaN|traceback)\b", re.I)` and requires matching API paths; `test_list_export_inventory.py` pins export route inventory (`C18`). None are disturbed by `<p>` / `<ul>` / `<li>` rendering in `workSummary` and `safetyPanel`.

## Evidence Log

| ID  | Source (`path:line`)                                                                  | Finding                                                                                                                               |
|-----|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `docs/reference/regulatory/building-safety-awaabs-law/2025-10-27-hazards-in-social-housing-prescribed-requirements-england-regulations-2025.xml:1` | Awaab's Law (`SI 2025/1042`, in force 27 Oct 2025, reg. 5(8)) prescribes 24h emergency action from awareness and statutory damp/mould investigation and make-safe windows. |
| C2  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:107`                       | `SA-001`..`SA-003`, `SA-007`, `FR-003`, `FR-004`, `FR-032`, `FR-034`, `CON-001` require visible clocks and named owners on hazard and safeguarding items across queues and case cards, never hidden by simplification, with plain language and cross-view agreement. |
| C3  | `src/core/src/zava_forward/core/rulecards.py:47`                                      | `RULE-003` confirms external hazard and repairs service owns statutory categorisation and timing while Zava displays recorded/operational reference clocks. |
| C4  | `src/api/src/zava_forward/api/server.py:751`                                          | `GET /api/cases` delegates all staff queue views (`mine`, `all`, filtered role queues) to `Store.page_cases` / `SqlStore.page_cases`. |
| C5  | `src/core/src/zava_forward/core/store.py:368`                                         | `Store.page_cases` (and `SqlStore.page_cases` at `sqlstore.py:1466`) attaches `r["work"] = self.work_context(c, user)` to every staff summary row. |
| C6  | `src/api/src/zava_forward/api/server.py:993`                                          | `GET /api/cases/{case_id}` delegates case card detail to `Store.detail(cid, u)`. |
| C7  | `src/api/src/zava_forward/api/web/role-screens.js:98`                                 | Every specialist role queue screen renders `workSummary(row.work)` imported from `web/app.js:797`, matching `listView` (`web/app.js:907`) and `caseView` (`web/app.js:808, 1086`). |
| C8  | `src/core/src/zava_forward/core/taskqueues.py:211`                                    | `taskqueues.context` builds `work["hazard_clocks"]` only from `case["hazards"]` and lacks safeguarding items, structured `clock_status`/`clock_remaining_hours`/`clock_deadline_utc`/`clock_label`, and non-blank `named_owner`/`accountable_owner`/`escalation_owner`/`unassigned` fields. |
| C9  | `src/core/src/zava_forward/core/workflows.py:14`                                      | `HAZARD_CATEGORIES` omits `"Safeguarding"` and `hazard_view` (`workflows.py:101`) does not project clock or named accountable owner metadata. |
| C10 | `src/core/src/zava_forward/core/store.py:414`                                         | `Store._work_context` and `Store.detail` (`store.py:493`) hold `data.get("staff", [])` and `self.as_of`, enabling shared clock and roster-backed owner/escalation projection across queue rows and case cards. |
| C11 | `src/core/src/zava_forward/core/projection.py:85`                                     | Contractors receive allowlisted `SUMMARY_FIELDS`/`DETAIL_FIELDS` only; `redact_staff_detail` (`projection.py:173`) preserves `work` and non-note fields while replacing `NOTE_KEYS` (`note`, `source`, `job`) with `NOTE_HELD` when `not can_see_reason(user)`. |
| C12 | `src/core/tests/test_taskqueues.py:188`                                               | `test_unnamed_clock_owner_is_stated_plainly_and_never_invented` requires `clock["owner"] == "Unknown"` and `clock["owner_named"] is False` when direct follow-up owner is unrecorded, so new `named_owner`/`accountable_owner`/`escalation_owner`/`unassigned` fields must complement rather than overwrite `owner`. |
| C13 | `src/api/tests/test_role_screens.py:168`                                              | `test_role_screens.py` evaluates `app.slice(app.indexOf("function workSummary("), app.indexOf("function workSteps("))` in isolation with synthetic legacy clock fixtures. |
| C14 | `src/api/checks/role_screens_browser_check.py:431`                                    | Browser checks assert `link.locator(".flag.danger").count() == int(bool(row.get("hazard")))` and `link.locator(".safety-clock").count() == len(work["hazard_clocks"])` with legacy clock fields visible in text. |
| C15 | `src/api/tests/test_safety_panel_ux.py:162`                                           | `test_safety_panel_ux.py` asserts `.safety-facts` has exactly 4 `<dt>` elements and never contains `"Unknown"`. |
| C16 | `src/core/src/zava_forward/core/synthetic/resident_preview_fixture.py:102`            | `resident_preview_fixture.py` sets `safeguarding=dict(note=f"{CANARY}-SAFEGUARDING-NOTE-{cid}")` on `SYN-C1`/`SYN-C2` and issues work orders in `_drive()` (`line 233`). |
| C17 | `src/api/tests/test_accessibility_baseline.py:55`                                     | Pins `aria-invalid` floor (`8`), `h("table",` count (`13`), and `position:fixed` cap (`2`). |
| C18 | `src/api/tests/test_epic149_form_error_summary_associations.py:1`                     | Pins `undefined`/`NaN`/`traceback` absence, form error associations, API route parity, and alongside `test_list_export_inventory.py:1` pins export endpoint inventory. |

## Synthesis and Evaluation of Alternatives

### Alternatives Compared

| Option | Summary | Pros | Cons | Disposition |
|--------|---------|------|------|-------------|
| Option A (Selected) | Shared safety clock + accountable-owner helper in `taskqueues.py` reused by `workflows.hazard_view` / `safeguarding_view`, `Store.summary` / `Store.detail` / `SqlStore`, `workSummary(work)` in `web/app.js`, and a `<p class="safety-clock-owner">` summary inside `safetyPanel` in `web/app.js` | Single source of truth (`FR-034` guaranteed); zero edits to `web/role-screens.js`; preserves all `test_taskqueues.py`, `test_role_screens.py`, `role_screens_browser_check.py`, `test_safety_panel_ux.py`, `resident_preview_fixture.py`, and counted baseline guards | Requires careful self-contained JS formatting inside `workSummary` and `safetyPanel` | Selected (`C5`, `C7`, `C8`, `C12`–`C18`) |
| Option B | Separate API wrapper in `server.py` post-processing `/api/cases` and `/api/cases/{id}` plus separate UI edits in both `app.js` and `role-screens.js` | Leaves `src/core` smaller | Violates caller preference not to touch `role-screens.js`, splits logic away from `Store`/`SqlStore` unit callers, and risks `FR-034` drift | Rejected (`C4`, `C5`, `C7`) |
| Option C | Overwrite legacy `clock["owner"]` with escalation owner and add 5th/6th `<dt>` rows to `.safety-facts` | Fewer keys in JSON | Breaks `test_taskqueues.py:198` (`owner == "Unknown"`) and `test_safety_panel_ux.py:163` (`dt.length === 4`) | Rejected (`C12`, `C15`) |

### Selected Convergence Recommendation

Implement **Option A**:
1. **Unified Safety Clock & Accountable-Owner Projection (`taskqueues.py` + `workflows.py`)**:
   * Add `"Safeguarding"` to `HAZARD_CATEGORIES` (`workflows.py`) and `HAZ_CATEGORIES` (`web/app.js`), and extract standalone safeguarding items from `case.get("safeguarding_items")` (`list[dict]`) and `case.get("safeguarding")` (`list[dict]` or item `dict` with keys beyond a bare `{"note": ...}` canary container).
   * Build one deterministic helper `project_safety_clock_and_owner(item, case=..., as_of=..., staff=..., default_kind=...)` that computes:
     * `item_kind`: `"safeguarding"` or `"hazard"`.
     * Statutory/operational clock fields:
       * `clock_label`: e.g. `"Awaab's Law 24h emergency action clock (recorded reference)"` (`Emergency` / `P1`, 24h), `"Awaab's Law / operational 7d investigation clock (recorded reference)"` (`Significant` pre-acceptance, 168h), `"Operational 14d work-start clock (recorded reference)"` (`Significant` post-acceptance or `Routine`, 336h), `"Safeguarding 24h emergency response clock"` (`Safeguarding` + `Emergency`/`Immediate`/`P1`, 24h), or `"Safeguarding 48h referral response clock"` (`Safeguarding` standard/unrecorded priority, 48h).
       * `clock_deadline_utc`: normalized UTC ISO-8601 (`...Z`) using recorded external `response_due_at` / `due_at` first (`clock_basis="recorded_service_deadline"`), else valid timezone-aware `aware_at <= now` + target window (`clock_basis="operational_reference_from_awareness"`), else `None` (`clock_basis="missing_timestamp_fail_closed"`).
       * `clock_remaining_hours`: `round((deadline - now).total_seconds() / 3600, 1)` (`0.0` when completed if deadline known, negative when overdue, `None` when timestamps are missing).
       * `clock_status`: `"completed"` (`responded_at <= now`), `"fail_closed_missing_timestamp"` (when `clock_deadline_utc is None`), `"overdue"` (`deadline < now`), or `"running"` (`deadline >= now`).
     * Accountable owner fields (never blank, `"Unknown"`, or anonymous):
       * Direct allocated owner resolved from `accepted_by` -> `destination` -> `sender` -> `item.get("owner")` -> `item.get("named_owner")` with roster lookup against `staff` for `owner_id` (`code` / `email`) and `owner_role`.
       * Escalation owner always resolved from designated `destination` -> named case owner (`case["owner"]`, `case["owner_code"]`, `case["owner_role"]` / roster) -> named roster lead in `Building Safety Liaison` / `Retrofit Programme Manager` -> explicit duty role lead (`"Building Safety Liaison duty lead"` / `"Safeguarding duty lead"`, role `"Building Safety Liaison"`, ID `"ESC-BSL-DUTY"` / `"ESC-SG-DUTY"`).
       * When allocated: `unassigned = False`, `named_owner = direct_name`, `accountable_owner = direct_name`. When unallocated: `unassigned = True`, `named_owner = escalation_owner`, `accountable_owner = escalation_owner`, while preserving legacy `owner = "Unknown"` and `owner_named = False` on `work["hazard_clocks"]`.
   * Project both active hazards and active safeguarding items into `work["hazard_clocks"]` (plus filtered `work["safeguarding_clocks"]` and `work["safety_items"]`), `detail["hazards"]` (`hazard_view`), and `detail["safeguarding_items"]` (`safeguarding_view`), and reflect active safeguarding items in `insights.has_hazard` / `ranking._hazard` / `SqlStore._row` (`sqlstore.py:979`) so `Store` and `SqlStore` match on `hazard` flags and `FR-034`.
2. **UI Display Without Editing `web/role-screens.js` (`web/app.js`)**:
   * Activate `web-design-guidelines` prior to editing `web/app.js`.
   * Extend self-contained `workSummary(work)` (`web/app.js:797-805`) so `.safety-clock` renders the statutory/operational clock (`clock_label`, `clock_status`, remaining hours / UTC deadline or fail-closed missing-timestamp notice) and named accountable owner (`named_owner`, `owner_role`, `owner_id`, plus explicit unassigned + escalation-owner text when `unassigned` is true) alongside existing phrases, gracefully omitting optional clauses only when synthetic test fixtures omit the new fields.
   * Extend `safetyPanel(c, id, refresh)` (`web/app.js:1734`) with a `<p class="safety-clock-owner">` line inside each hazard card (leaving `.safety-facts` at 4 `<dt>` pairs) and a safeguarding items list when `c.safeguarding_items` is non-empty, using plain language free of banned copy-audit terms (`gate`, `hold`, `provenance`, `trace`).

## Risks, Open Questions, and Potential Further Research

* Open questions: None blocking planning (`Q1`–`Q5` all answered with code/doc citations).
* Residual risks to manage in Plan & Implement:
  * Keep `SA-003` banned internal words (`gate`, `hold`, `provenance`, `trace`) out of all user-visible strings added to `taskqueues.py` and `web/app.js`.
  * Ensure `projection.hold_notes` redacts free-text `note`/`source`/`job` inside `detail["safeguarding_items"]` for staff without `can_see_reason(user)` while keeping clock and named-owner fields intact, and verify contractors never receive `safeguarding` or `safeguarding_items`.
* Potential further research: None required; cycle 1 reached saturation across core, SQL store, API, UI, and regression/guard suites.

## Planning Readiness and Handoff

* Research disposition: `executed`
* Planning Readiness: `Ready`
* Re-entry decision: No second research cycle needed; all five research questions and contrarian compatibility checks are resolved with `path:line` evidence (`C1`–`C18`).

## Self-Check

* [x] Research brief, parameters, extension registry, participation record, direction controls, and prior-knowledge gate recorded.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order without source edits.
* [x] Every finding maps to stable `C1`–`C18` codebase/snapshot `path:line` evidence IDs.
* [x] Alternatives compared with evidence-grounded selection of Option A (`convergence` mode).
* [x] Planning Readiness (`Ready`) and Research disposition (`executed`) recorded for RPI Agent handoff to `rpi-plan`.

