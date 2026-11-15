<!-- markdownlint-disable-file -->

# Task Research: exception-queue-135-2330

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                 |
| Researcher / agent | rpi-research (via RPI Agent)                                               |
| Status             | Ready                                                                      |
| Artifact path      | .copilot-tracking/research/2026-11-14/exception-queue-135-2330-research.md |

## Research Brief

* What to research: Current implementation and remaining gaps across `src/core` and `src/api` (server, web UI, and tests) against all five acceptance criteria of Issue #135 ("Data steward and digital operator exception queue").
* Why it matters: Issue #135 has partial delivery on `main` and recent commits on the parent stack (`origin/feat/demo-233-same-home-tensions-0825`), and requires deterministic end-to-end enforcement across core, API, and UI without silent correction, automatic replay, or ungrounded outage display.
* Audience or intended use: Planning and implementation phases (`rpi-plan`, `rpi-implement`, `rpi-review`) in this automatic RPI loop.
* Scope: `src/core/src/zava_forward/core/` (`exception_queue.py`, `exception_feeds.py`, `exception_register.py`, `import_refusals.py`, `recovery.py`, `store.py`, `taskqueues.py`, `continuity.py`, `ai_tasks.py`), `src/api/src/zava_forward/api/` (`server.py`, `workbench.py`, `web/index.html`, `web/app.js`, `web/styles.css`), `src/core/tests/`, `src/api/tests/`, and UX/PRD documentation (`docs/prds/`, `docs/reference/research/ux/`).
* Non-goals: Modifying `src/api/checks/workbench_browser_check.py` (unless updating `scenario-manifest.json` recipe SHA, avoided unless required), pushing to remote, changing live infrastructure, or relaxing existing safety/human-approval gates.
* Criteria: Deterministic enforcement and end-to-end test proof for all 5 acceptance criteria of Issue #135: (1) conflicting source values with both values, source, date, version, and named `resolution_owner`; (2) failed imports, failed model calls, and stranded tasks in an owned exception queue; (3) controlled, audited operator recovery with no automatic replay or release; (4) preserved unresolved eligibility and original source; (5) scoped and visible operator access plus honest outage state with plain-language next steps.
* Requested outputs: Synthesized gap analysis, exact contract/API/UI architecture recommendation, and planning readiness assessment.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                                                 |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | What already satisfies Issue #135 across `src/core` and `src/api`, and what exact contract, API, UI, and test gaps remain for each of the five acceptance criteria?                   |
| Codebase scope                   | `src/core`, `src/api`, `docs/prds`, `docs/reference/research/ux`, `.copilot-tracking/*135*`                                                                                           |
| External scope                   | Web Interface Guidelines source required before web edits in later phases (`none` needed for internal codebase gap discovery unless external rule verification is triggered)          |
| Initial internal candidate areas | `src/core/src/zava_forward/core/exception_*.py`, `recovery.py`, `src/api/src/zava_forward/api/server.py`, `web/index.html`, `web/app.js`, `src/core/tests/`, `src/api/tests/`         |
| Initial external candidate areas | none                                                                                                                                                                                  |
| Research posture                 | balanced                                                                                                                                                                              |
| Posture provenance               | default (bounded task with named source targets and adjacent cross-layer core/API/UI integration points)                                                                              |
| Explicit limits / deadline       | Do not modify `src/api/checks/workbench_browser_check.py` without updating `scenario-manifest.json`; focused validation tier; do not push                                             |
| Posture-specific completion basis| balanced scope coverage and adequate evidence across all five Issue #135 criteria in core, API, UI, and tests                                                                         |
| Edits allowed during research?   | no, research-only                                                                                                                                                                     |
| Resolved evidence root           | `.copilot-tracking/` default                                                                                                                                                          |
| Known constraints / excluded sources | Preserve Fluent 2 design system, WCAG 2.2 AA baseline, and plain-language content standard; no private dataset reads; no `.copilot-tracking/` citations in production code/commits |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                                                     | Scoped authority or output contract                                              | Selected / skipped reason                                                                                      |
|---------------------|----------------------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches workspace inputs and tracking artifacts          | Enforces Fluent 2, WCAG baseline, plain-language standard, validation tiers, and branch/commit rules | Selected: mandatory repository governance for research and downstream web/API/core changes.                    |
| Skill               | `redesign-existing-projects` & `web-design-guidelines` | Matches web UI changes in `src/api/.../web/`                             | Guides accessible existing-app UI updates and web review                         | Deferred to Plan/Implement: Research is read-only; recorded so Plan/Implement activate them before web edits.  |
| Skill               | `accessibility`                  | Matches WCAG/ARIA requirements for operator exception UI                 | WCAG 2.2 / ARIA semantics reference                                              | Skipped during Research: existing repository UX docs (`wcag-conformance-baseline.md`, `content-standard.md`) define project rules directly. |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-visible general research lane worker                                | Bounded subagent research artifact under `.copilot-tracking/research/subagents/` | Skipped (inline execution): target files in `src/core` and `src/api` are tightly coupled across one contract trace; inline reads avoid cross-layer drift. |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                              |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit 5-criterion scope, named target modules, and validation tier | N/A (non-interactive)| Proceed with `balanced` posture in `convergence` mode across all 5 criteria of Issue #135.   |
| Direction change | None at intake                                                                                        | N/A                  | Maintain initial scope and constraints.                                                      |
| Convergence      | Completed Cycle 1 Wider/Deeper/Contrarian analysis across `src/core` and `src/api`                    | N/A (automatic mode) | Converged on additive core/API contract enrichment + `#/exceptions` interactive workbench route in `app.js` while preserving read-only `role-screens.js`. |

## Scope and Success Criteria

* Scope: Inspect `src/core` exception/recovery/conflict/outage modules, `src/api` endpoints and `web/index.html` + `web/app.js` + tests, and prior `#135` tracking records to determine exact coverage and remaining gaps for all 5 acceptance criteria.
* Assumptions: Prior `#135` commits delivered parts of `exception_queue.py`, `exception_feeds.py`, `exception_register.py`, `recovery.py`, and read-only employee exception register views, which must be verified directly in current `HEAD` (`c8dca2c89`) rather than assumed complete or absent.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect existing exception queue implementation in `src/core` and `src/api`; ensure all 5 criteria of `#135` are deterministically enforced and tested end-to-end across core/API/UI; do not modify `workbench_browser_check.py` without updating `scenario-manifest.json`.
* Inferred research questions: Which endpoints, UI panels, and core functions already exist on `c8dca2c89`? How are recovery actions, conflicting source values, failed model calls, failed imports, stranded tasks, unresolved eligibility, operator access scope, and model/service outage states currently modeled and rendered? What existing tests enforce UI/content/endpoint contracts (such as `test_role_endpoint_inventory.py`, `test_content_standard.py`, `test_data_operator_screen.py`, `test_exception_register*.py`)?
* Caller constraints and non-goals: Focused validation tier (`mypy`, `ruff`, focused unit tests); commit locally with `Refs #135`; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Focused validation tier (`mypy`, `ruff`, focused unit tests in modified project dirs); do not push      | User intake         | Constrains downstream implementation/validation plan without restricting research. |
| exclude                                                  | Do not modify `src/api/checks/workbench_browser_check.py` unless updating `scenario-manifest.json` SHA  | User intake         | Preserves frozen workbench browser check recipe unless strictly required.          |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type (depth / breadth / straightforward) | Priority | Status |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|--------|
| Q1 | How are conflicting source values, source/date/version metadata, named `resolution_owner`, unresolved eligibility, and original source modeled and displayed across `core`, `api`, and `web`? | depth                                    | H        | closed |
| Q2 | How do failed imports, failed model calls, and stranded tasks enter and surface in the owned exception queue/register across `core`, `api`, and `web`? | depth                                    | H        | closed |
| Q3 | What controlled, audited operator recovery actions exist in `core`, `api`, and `web`, and how do they prevent automatic replay, silent overwrite, or external/resident release? | depth                                    | H        | closed |
| Q4 | How are scoped operator access and honest service/model outage states (with plain-language next steps) surfaced in the exception queue API and UI? | depth                                    | H        | closed |
| Q5 | What cross-cutting repository invariants (role endpoint inventory, WCAG/design system/plain-language content checks, SQL/JSON store parity, frozen browser manifests) constrain changes in `src/core` and `src/api`? | breadth                                  | H        | closed |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14-135-conflict-recovery-research.md`, `.copilot-tracking/reviews/2026-11-14/135-conflict-recovery-1844-review.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`.
* Reused (verified) findings: `ExceptionQueue`, `exception_feeds`, `ExceptionRegisterMixin`, `GET /api/exceptions`, and `POST /api/exceptions/recovery` are already shipped on HEAD `c8dca2c89` (`C1`, `C2`, `C3`, `C4`, `C5`).
* Superseded / stale: Earlier `#135` research predated the `POST /api/exceptions/recovery` store overlay and `#229` read-only `role-screens.js` static guards; verified directly against current files (`C3`, `C5`, `C8`, `C9`).

## Cycle 1 Execution

### Wave 1: Wider

* Inspected `src/core/src/zava_forward/core/exception_queue.py`, `exception_feeds.py`, `exception_register.py`, `recovery.py`, `continuity.py`, and `projection.py` (`C1`, `C2`, `C3`, `C6`, `C7`).
* Inspected `src/api/src/zava_forward/api/server.py`, `workbench.py`, `web/index.html`, `web/app.js`, and `web/role-screens.js` (`C4`, `C5`, `C8`, `C10`, `C11`).
* Inspected test suites in `src/core/tests/` (`test_exception_queue.py`, `test_exception_feeds.py`) and `src/api/tests/` (`test_exception_register.py`, `test_exception_register_screen.py`, `test_data_operator_screen.py`, `test_data_steward_screen_wcag.py`, `test_role_screens.py`, `test_role_endpoint_inventory.py`, `test_content_standard.py`, `test_design_system.py`, `test_app_js_notices_content.py`, `test_static_assets.py`, `test_workspace_scripts.py`) (`C9`, `C12`, `C13`, `C14`).

### Wave 2: Deeper

* **Criterion 1 (Conflicting source values & `resolution_owner`)**:
  * `ExceptionQueue.raise_conflict` (`C1`) validates >=2 distinct values with `value`, `source`, `date`, and `version`, and `conflict_view` returns `resolution_owner: item["owner"]`, `eligibility: "Unknown"`, and `original_source`. However, items returned by `ExceptionQueue.queue()` and `GET /api/exceptions` (`C3`) carry `owner` and `owner_role` without a top-level `resolution_owner` field on conflict items (`C1`).
  * `feed_stock_conflicts` (`C2`) extracts unresolved `stock_reconciliation` queries on open cases, preserving both sides (`value`, `source`, `date`, `version`) and `original_source` (`case_id`, `query_id`, `field`, `query_owner`, `left`, `right`).
* **Criterion 2 (Failed imports, failed model calls, stranded tasks, correlation IDs & recovery context)**:
  * `ExceptionQueue.raise_failure` (`C1`) supports `FAILURE_KINDS = ("failed_import", "failed_ai_run", "failed_integration", "stranded_task")` with role-checked named `owner`. Items carry `kind`, `owner`, `owner_role`, and `ref`, but lack explicit `failure_category`, `correlation_id`, and `recovery_context` fields (`C1`, `C2`, `C3`).
  * `ExceptionRegisterMixin._build_exception_queue` (`C3`) routes `feed_failed_ai_runs`, `feed_stranded_tasks`, `feed_unaccepted_handoffs`, `feed_stock_conflicts`, and `import_refusals`, but passes `[]` instead of stored importer `import_batches` to `feed_failed_imports(queue, [], steward, shown)` (`C3`). Routing `self.data.get("import_batches")` alongside `import_refusals` connects rejected importer batches when present without altering `NOT_CONNECTED` when neither is present (`C3`, `C12`).
* **Criterion 3 (Controlled, audited recovery; no automatic replay or release)**:
  * `ExceptionQueue.request_recovery` (`C1`) and `ExceptionRegisterMixin.request_exception_recovery` (`C3`) enforce named staff scope, `ALLOWED_ACTIONS`, non-empty `reason` (<=400 chars), owner-only `resolve_by_owner`, `replayed: False`, `released: False`, `automatic_replay: False`, and `automatic_release: False`.
  * Two gaps found: (a) `ExceptionQueue.request_recovery` (`C1`) omits `"at"` timestamp and per-item `"audit_trail"` on `item["recovery"]`, while `ExceptionRegisterMixin._recovery_requests` (`C3`) retains only the latest `exception_recovery_requested` entry per key rather than the full per-item `audit_trail`; (b) no interactive workbench view in `web/app.js` / `web/index.html` calls `POST /api/exceptions/recovery` or renders recovery controls and recorded audit trails (`C8`, `C10`, `C11`).
* **Criterion 4 (Unresolved eligibility and original source preserved)**:
  * Both `ExceptionQueue` (`C1`) and `ExceptionRegisterMixin` (`C3`) keep `eligibility: "Unknown"`, `unresolved_eligibility: True`, and deep-copied `original_source` unchanged across `hold`, `request_rerun`, and `resolve_by_owner`, leaving `self.data` untouched (`C12`). Interactive UI must display `eligibility`, `unresolved_eligibility`, and `original_source` before and after recovery.
* **Criterion 5 (Scoped & visible operator access; honest outage state with plain-language next steps)**:
  * `ExceptionRegisterMixin.exception_register` (`C3`) enforces `ZF_EXCEPTION_STAFF` scoping, returns `access` (`roles` limited to caller's entry + `scope`), and calls `queue.outage_banner(None)`.
  * Two gaps found: (a) `outage_banner` (`C1`) returns `{state, text, components, last_checked}` without an explicit plain-language `next_steps` field; (b) `_build_exception_queue` (`C3`) never reflects active AI continuity suspensions (`self.data.get("continuity")` open `Suspended` records from `continuity.py`, `C6`) or recorded `service_outages` in `queue`, so `banner["state"]` cannot transition to `"outage"` during an active model/AI suspension. Reflecting active `continuity` suspensions and `service_outages` into `queue` sets `banner["state"] == "outage"` with plain-language `next_steps` when suspended while preserving `state == "unknown"` (`"Do not assume it is healthy"`) when no outage/suspension is active (`C1`, `C3`, `C6`, `C12`).

### Wave 3: Contrarian

* **Challenge 1: Adding recovery controls directly to `role-screens.js` (`data-operator`)**:
  * **Counter-evidence**: `test_role_screens.py`, `test_data_operator_screen.py`, `test_exception_register_screen.py` (`C9`), and `checks/data_operator_browser_check.py` statically and dynamically forbid any `<button>` (other than jump targets and CSV summary), `<form>`, `<input>`, `<select>`, `<textarea>`, `POST`, or extra `fetch` inside `role-screens.js`.
  * **Disposition**: Rejected editing `role-screens.js` for write controls. Place the interactive exception queue and controlled recovery view in `web/app.js` at `#/exceptions` (matching `#/handoff-waiting` and `#/import` in `app.js`, `C10`), with entry links from workbench views and `#app` workspace shell without mutating `workbench.py`'s `me.navigation` (`C7`, `C14`) or `role-screens.js` (`C8`, `C9`).
* **Challenge 2: Using words like `"hold"`, `"provenance"`, `"gate"`, `"trace"`, `"snapshot"`, or `"envelope"` in `web/app.js` or `web/index.html`**:
  * **Counter-evidence**: `test_content_standard.py` (`C13`) scans every line of every `.js` and `.html` file in `web/` with `BANNED = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b", re.I)`, allowing only exact substrings in `ALLOWED` (which includes `"Keep on hold"`). Even a JS identifier, comment, or string comparison like `action === "hold"` on a line without `"Keep on hold"` will fail `CopyAudit.test_no_internal_terms_in_web_copy`!
  * **Disposition**: Accepted strict lexical rule for `web/app.js` and `web/index.html` — never use bare banned stems anywhere in `web/` edits; map recovery actions from server-supplied `item.recovery_policy.allowed_actions` using `"Keep on hold"` (whitelisted) as the fallback label for non-`request_rerun` / non-`resolve_by_owner` actions.
* **Challenge 3: Mutating `self.data` or changing default `banner["state"]` during `GET /api/exceptions`**:
  * **Counter-evidence**: `test_exception_register.py` (`C12`) asserts byte-identical `json.dumps(self.store.data, sort_keys=True)` before and after `exception_register()` (`test_one_view_adds_one_ledger_entry_and_leaves_the_data_unchanged`), `view["banner"]["state"] == "unknown"` when no outage is active (`test_banner_is_unknown_and_unconnected_sources_are_stated`), and `view["access"]["roles"] == {"human0@example.test": ["data_steward"]}` (`test_access_roles_show_only_the_callers_own_entry`).
  * **Disposition**: Read `self.data.get("continuity")` and `self.data.get("import_batches")` strictly without `setdefault` or mutation, preserve `access.roles` as caller-only, add `viewer_roles` and `allowed_kinds` alongside `roles` and `scope`, and preserve `banner.state == "unknown"` whenever no active suspension/outage is recorded.
* **Challenge 4: Concurrent duplicate recovery clicks in `app.js`**:
  * **Counter-evidence**: `mutationKey(path, body)` in `app.js` (`C10`) keys in-flight POST requests by `[path, body.action || ..., id, index, measure, case_id, package, capability, turn]`, which omits `body.key`. Including `body.key` (or `key` fallback) ensures distinct exception items have distinct in-flight mutation keys while duplicate submissions on the same item+action are blocked.

## Evidence Log

| ID  | Source (`path:line`)                                                          | Verified fact                                                                                                                                      |
|-----|-------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/core/src/zava_forward/core/exception_queue.py:18-297`                    | `ExceptionQueue` enforces `STEWARD`/`OPERATOR` scoping, 2+ distinct conflict values (`value`, `source`, `date`, `version`), `ALLOWED_ACTIONS`, `NO_AUTOMATION`, `outage_banner`, and `access_report`, but omits top-level `resolution_owner` on queued conflict items, `failure_category`/`correlation_id`/`recovery_context`, `at`/`audit_trail` in `request_recovery`, and `next_steps` in `outage_banner`. |
| C2  | `src/core/src/zava_forward/core/exception_feeds.py:15-219`                    | Read-only feeds route `failed_ai_run` (fallback/quarantined AI tasks), `stranded_task` (unowned overdue tasks & `needs_escalation` handoffs), `failed_import` (rejected batches & refused files), and `source_conflict` (unresolved `stock_reconciliation`). |
| C3  | `src/core/src/zava_forward/core/exception_register.py:29-345`                 | `ExceptionRegisterMixin` implements `exception_register` and `request_exception_recovery` backed by `audit_entries()`, currently passing `[]` for batches in `_route_refusals`, `None` with no continuity/outage feed to `outage_banner`, and retaining only the latest recovery entry per key. |
| C4  | `src/api/src/zava_forward/api/server.py:790-794`                              | `GET /api/exceptions` calls `s.exception_register(u, exception_register.staff_from_env(os.environ))` and maps `PermissionError` to HTTP `403`.      |
| C5  | `src/api/src/zava_forward/api/server.py:1419-1427`                            | `POST /api/exceptions/recovery` calls `s.request_exception_recovery(...)` and maps `PermissionError` to `403` and `ValueError` to `400`.           |
| C6  | `src/core/src/zava_forward/core/continuity.py:73-185`                         | `continuity.py` stores AI incident suspensions (`status == "Suspended"` or open `actual_hold`) with `id`, `scope`, `reason`, and `incident_owner`, plus `MANUAL_NOTE` plain-language fallback guidance. |
| C7  | `src/api/src/zava_forward/api/workbench.py:18-85`                             | `navigation(user)` defines top-level workbench nav links (`#/` through `#/screens`); auxiliary staff routes (`#/handoff-waiting`, `#/import`) resolve in `app.js` without changing `navigation(user)`. |
| C8  | `src/api/src/zava_forward/api/web/role-screens.js:1080-1270`                  | `#/screens?screen=data-operator&exceptions=1` is a strictly read-only register view (`exceptionRegisterView`) with CSV summary download and jump nav. |
| C9  | `src/api/tests/test_exception_register_screen.py:128-235`                     | Existing tests enforce zero write calls and zero `button`/`form`/`input`/`select`/`textarea` controls (except jump targets) in `role-screens.js`.  |
| C10 | `src/api/src/zava_forward/api/web/app.js:62-95,387-470,2010-2030`             | `app.js` owns `api()`, `mutationKey()`, `ownedNotice()`, and `route()` for interactive workbench routes (`#/handoff-waiting`, `#/import`, etc.).   |
| C11 | `src/api/src/zava_forward/api/web/index.html:1-60`                            | Single-page workbench shell loading `style.css` and `app.js` with `<p id="workspace-status">` and `<main id="app">`.                               |
| C12 | `src/api/tests/test_exception_register.py:55-315`                             | Existing SQL/JSON register tests require read-only `self.data`, caller-only `access.roles`, `unknown` default banner state, and `NOT_CONNECTED` when no imports are transferred. |
| C13 | `src/api/tests/test_content_standard.py:15-95`                                | `CopyAudit` bans `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, and `envelope(s)` across all `web/*.js` and `web/*.html`, allowing `"Keep on hold"`. |
| C14 | `src/api/checks/workbench_browser_check.py:15-120`                            | Frozen workbench browser check validates login, case queue counts, and `#nav`; keeping `workbench_browser_check.py` and `workbench.py` unchanged avoids manifest SHA churn. |

## Synthesis and Converged Recommendation

### Selected Recommendation

Deliver an **additive cross-layer completion** across `src/core` (`exception_queue.py`, `exception_feeds.py`, `exception_register.py`), `src/api` (`web/app.js`, `web/index.html` if needed, keeping `server.py` endpoints compatible), and focused end-to-end tests in `src/core/tests/` and `src/api/tests/`:

1. **Core Queue & Feed Contract (`exception_queue.py`, `exception_feeds.py`)**:
   * Add explicit `resolution_owner` on conflict items (`CONFLICT_KINDS`) in `ExceptionQueue.raise_conflict` so queued items and `GET /api/exceptions` carry `resolution_owner` alongside `values` (`value`, `source`, `date`, `version`).
   * Add explicit `failure_category` (`kind` on `FAILURE_KINDS`), deterministic `correlation_id` (preserving `correlation_id` from `original_source` when supplied, otherwise `ref` or item `id`), and structured `recovery_context` (`correlation_id`, `ref`, `owner`, `owner_role`, `allowed_actions`, `runbook`, `automatic_replay: False`, `automatic_release: False`) on queued items; preserve `correlation_id` in `feed_failed_ai_runs` when present on AI task records.
   * Record `at` timestamp (`self._clock()`) and append-only per-item `audit_trail` entries (`{at, by, action, reason, replayed: False, released: False}`) in `ExceptionQueue.request_recovery` while preserving `eligibility == "Unknown"`, `unresolved_eligibility is True`, and deep-copied `original_source`.
   * Enrich `ExceptionQueue.outage_banner` with plain-language `next_steps` tailored to each state (`outage`, `unknown`, `no_known_outage`).
2. **Store Exception Register (`exception_register.py`)**:
   * Route rejected importer batches from `self.data.get("import_batches")` (read-only) alongside `import_refusals` into `feed_failed_imports`, reporting unreadable batch records in `unrouted` and updating `sources` honestly when batches are connected while keeping `NOT_CONNECTED` unchanged when neither refusals nor batches exist.
   * Reflect active AI continuity suspensions (`self.data.get("continuity")` open `Suspended` records or invalid continuity history) and any recorded `self.data.get("service_outages")` (read-only) onto `queue.set_outage(...)` using a synthetic internal or operator outage record so `banner` deterministically reports `state == "outage"` with affected components and plain-language `next_steps` during outages/suspensions, and remains `state == "unknown"` otherwise.
   * Retain the full ordered per-item recovery `audit_trail` in `_recovery_requests` and `_with_recoveries` alongside the latest `recovery` state.
   * Surface explicit `viewer_roles` and `allowed_kinds` in `access` while keeping `access["roles"]` scoped strictly to the signed-in caller.
3. **Interactive Workbench Exception Queue UI (`web/app.js`, `web/index.html`)**:
   * Add `#/exceptions` route (`exceptionsView()`) in `web/app.js` (and `body.key` in `mutationKey`, plus plain links to `#/exceptions` from `importView` and `handoffWaitingView` and account/workspace context without altering `me.navigation` or `role-screens.js`).
   * Render: (a) honest outage/service status banner with plain-language `next_steps`; (b) scoped operator/steward access panel (`viewer_roles`, `allowed_kinds`, role scope map, and denied/roles-not-named guidance with named owner and next action); (c) conflict items showing both source values (`value`, `source`, `date`, `version`), named `resolution_owner`, preserved `original_source`, and `eligibility: Unknown` (unresolved); (d) failed imports, failed model calls (`failed_ai_run`), and stranded tasks with explicit `owner`, `failure_category`, `correlation_id`, and `recovery_context`; and (e) controlled, audited recovery form (`select` action from `allowed_actions`, required `reason` input with accessible `<label>` and `aria-invalid`/`aria-describedby` validation, explicit no-automatic-replay / no-automatic-release notice, submission via `POST /api/exceptions/recovery`, and rendered recovery `audit_trail` showing actor, timestamp, action, and reason).
   * Respect Fluent 2 tokens, WCAG 2.2 AA native semantics, and `test_content_standard.py` lexical rules (zero banned terms: no bare `hold`, `gate`, `provenance`, `trace`, `snapshot`, `envelope`; use whitelisted `"Keep on hold"`).

### Alternatives Considered and Rejected

* **Alternative A: Add recovery forms inside `role-screens.js` (`#/screens?screen=data-operator&exceptions=1`)** — Rejected because `#229` contract tests (`C9`) explicitly lock `role-screens.js` as a zero-POST, zero-form read-only specialist view.
* **Alternative B: Create new `/api/exceptions/*` endpoints** — Rejected because `GET /api/exceptions` and `POST /api/exceptions/recovery` (`C4`, `C5`) are already allowlisted in `test_role_endpoint_inventory.py` and `projection.STAFF_GET` (`C7`); additive enrichment preserves full compatibility.

## Risks, Open Questions, and Further Research

* **Open Questions**: None blocking implementation. Organisational naming of real people to `data_steward` and `digital_operator` remains an owner configuration via `ZF_EXCEPTION_STAFF`, which the code already handles honestly via `roles_not_named`.
* **Key Risks**: Tripping `test_content_standard.py` lexical scan in `app.js` or breaking `test_exception_register.py` default banner/import assertions; mitigated by explicit unit + Node VM UI + copy audit tests.
* **Further Research Needed**: Fetch current Web Interface Guidelines source when activating `web-design-guidelines` prior to editing `web/app.js` during `rpi-implement`.

## Readiness and Handoff

* **Research execution status**: Completed (Cycle 1: Wider, Deeper, Contrarian waves completed).
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Self-check**:
  * All 5 research questions (`Q1`–`Q5`) answered with `C1`–`C14` `path:line` evidence: Pass
  * Wider, Deeper, and Contrarian waves executed in order: Pass
  * Convergence recommendation and rejected alternatives documented: Pass
  * Research-only constraint honored (zero source edits during Research): Pass

