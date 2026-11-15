<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #135 Data Steward and Digital Operator Exception Queue

## Metadata

* Task ID: issue-135-2330
* Task slug: exception-queue-135-2330
* Related plan: .copilot-tracking/plans/2026-11-14/exception-queue-135-2330-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/exception-queue-135-2330-research.md, docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/content-standard.md

## Phase Index

| Phase ID | Name                                                                               | Status | Detail sections                |
|----------|------------------------------------------------------------------------------------|--------|--------------------------------|
| P01      | Core Exception Queue, Feeds, and Store Register Enrichment                         | ready  | P01, P01-T01, P01-T02, P01-T03 |
| P02      | Interactive Employee Workbench Exception Queue UI and API Contract Verification    | ready  | P02, P02-T01, P02-T02          |
| P03      | Focused Tier Validation, Web Guidelines Review, and Clean Local Commit             | ready  | P03, P03-T01                   |

<!-- rpi:phase id=P01 -->
## P01: Core Exception Queue, Feeds, and Store Register Enrichment

### Context

`src/core/src/zava_forward/core/exception_queue.py`, `exception_feeds.py`, and `exception_register.py` already implement named-staff role scoping (`STEWARD = "data_steward"`, `OPERATOR = "digital_operator"`), conflict dual-value storage, failure feeds, and single-latest audit-backed recovery requests. Research (`C1`–`C3`, `C6`, `C12`) identified targeted additive enrichments needed so every Issue #135 criterion is deterministically represented on the item, access, and banner contracts without breaking any existing test assertions.

### Intent

Produce complete, immutable-copy exception items, recovery audit trails, rejected-batch import routing, explicit access scope metadata, and continuity-aware honest outage banners with plain-language `next_steps` in `src/core`.

### Boundaries

* Included: `src/core/src/zava_forward/core/exception_queue.py`, `src/core/src/zava_forward/core/exception_feeds.py`, `src/core/src/zava_forward/core/exception_register.py`, `src/core/tests/test_exception_queue.py`, and `src/core/tests/test_exception_feeds.py`.
* Excluded: Automatic task replay, silent conflict winner selection, resident/external release, or mutating `self.data` during `exception_register()`.

### Likely Targets

* src/core/src/zava_forward/core/exception_queue.py: Add `resolution_owner` on conflict items, `failure_category` on failure items, `correlation_id` and `recovery_context` on all items, timestamped `at` and append-only `audit_trail` on `request_recovery`, and plain-language `next_steps` on `outage_banner`.
* src/core/src/zava_forward/core/exception_feeds.py: Preserve `correlation_id` from AI task records (`correlation_id` or `envelope.request_id` / `id`) in `feed_failed_ai_runs` `original_source`.
* src/core/src/zava_forward/core/exception_register.py: Route rejected `import_batches` alongside `import_refusals`, retain full ordered per-item recovery `audit_trail` in `_recovery_requests` / `_with_recoveries`, expose `viewer_roles` and `allowed_kinds` in `access`, and reflect active `continuity` AI suspensions and recorded `service_outages` onto `queue` outage state.
* src/core/tests/test_exception_queue.py and src/core/tests/test_exception_feeds.py: Add focused semantic unit tests for new fields and invariants.

### Dependencies

* None.

### Validation Expectations

* `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p "test_exception_*.py" -v` exits `0`.

### Completion Evidence

* Updated `src/core` modules and green `mypy`, `ruff`, and `test_exception_*.py` test runs.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Enrich ExceptionQueue and exception_feeds contracts

#### Context

Queued items from `ExceptionQueue.queue()` currently omit top-level `resolution_owner` on conflicts (present only in `conflict_view`), explicit `failure_category` on failures, `correlation_id`, `recovery_context`, `at` timestamp and `audit_trail` in `request_recovery()`, and plain-language `next_steps` in `outage_banner()` (`C1`, `C2`).

#### Intent

Ensure `ExceptionQueue` and `exception_feeds` populate every required `#135` field deterministically while preserving deep-copied immutability, `eligibility == "Unknown"`, and `unresolved_eligibility is True`.

#### Boundaries

* Included:
  * In `ExceptionQueue._add`: compute deterministic `correlation_id` (checking `original.get("correlation_id")` when `isinstance(original, Mapping)` and non-empty string, else `extra.get("ref")` or `item_id`), initialize `"audit_trail": []`, and attach `"recovery_context"` containing `correlation_id`, `ref` (`extra.get("ref")`), `owner`, `owner_role`, `runbook`, `allowed_actions`, `automatic_replay: False`, and `automatic_release: False`.
  * In `ExceptionQueue.raise_conflict`: include `"resolution_owner": self._owner(kind, owner)` on the conflict item alongside `values` (`value`, `source`, `date`, `version`).
  * In `ExceptionQueue.raise_failure`: include `"failure_category": kind` on the failure item.
  * In `ExceptionQueue.request_recovery`: capture `at = self._clock()`, include `"at": at` inside `item["recovery"]`, append `{"at": at, "by": actor, "action": action, "reason": why, "replayed": False, "released": False}` to `item["audit_trail"]`, and include `"audit_trail": deepcopy(item["audit_trail"])` on `item["recovery"]`.
  * In `ExceptionQueue.outage_banner`: return plain-language `"next_steps"` list/text tailored to `outage` (continue manual case work and urgent human safety route; check the named component/incident owner before asking a human to re-run; nothing replays or releases automatically), `unknown` (do not treat missing health checks as healthy; verify source records manually and keep urgent safety work on the human route), and `no_known_outage` (continue normal scoped review; verify source records before resolving or requesting a human re-run).
  * In `feed_failed_ai_runs`: extract `correlation_id` from `rec.get("correlation_id")` or `(rec.get("envelope") or {}).get("correlation_id")` or `(rec.get("envelope") or {}).get("request_id")` or `(rec.get("envelope") or {}).get("meter_id")` when present and store in `original_source["correlation_id"]` (without leaking AI/personal text).
  * In `feed_failed_imports`: extract non-empty string `correlation_id` from `batch.get("correlation_id")` and `refusal.get("correlation_id")` into `original_source["correlation_id"]` when present.
  * In `feed_stranded_tasks`: when `source` is empty on an overdue unowned task, fall back to deterministic `ref = f"task:{task.get('case_id') or UNKNOWN}:{task.get('task') or UNKNOWN}"` so sourceless stranded tasks still receive a stable `recovery_key` and non-volatile `correlation_id`.
* Excluded: Changing existing field types or removing any existing dictionary keys returned by `ExceptionQueue`.

#### Likely Targets

* src/core/src/zava_forward/core/exception_queue.py: Queue item schema, `request_recovery`, and `outage_banner`.
* src/core/src/zava_forward/core/exception_feeds.py: `feed_failed_ai_runs` correlation metadata extraction.

#### Dependencies

* None.

#### Validation Expectations

* `python3 -m unittest tests/test_exception_queue.py tests/test_exception_feeds.py` in `src/core` passes.

#### Completion Evidence

* Conflict items include `resolution_owner`; failure items include `failure_category`; all items include `correlation_id`, `recovery_context`, and `audit_trail`; `outage_banner` includes plain-language `next_steps`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Connect rejected import batches, full recovery audit trail, access scope, and honest outage states in ExceptionRegisterMixin

#### Context

`ExceptionRegisterMixin` in `src/core/src/zava_forward/core/exception_register.py` rebuilds `ExceptionQueue` from store state and overlays audit-ledger recovery actions (`C3`). Currently it ignores `self.data.get("import_batches")`, retains only the latest recovery entry per key instead of the full `audit_trail`, and never feeds active AI continuity suspensions (`self.data.get("continuity")`) or recorded `service_outages` into `queue` (`C3`, `C6`). Existing tests (`C12`) require that `self.data` is never mutated on read, `access["roles"]` contains only `{caller_email: [...]}`, `banner["state"] == "unknown"` when no outage is active, and `NOT_CONNECTED` appears in `sources` when neither refusals nor import batches have been transferred.

#### Intent

Wire rejected `import_batches`, full recovery `audit_trail`, explicit `viewer_roles` / `allowed_kinds` access metadata, and honest continuity/service outage reporting into `ExceptionRegisterMixin` with zero read-side mutation.

#### Boundaries

* Included:
  * Read `self.data.get("import_batches")` and optional `(self.data.get("import_exceptions") or {}).get("rejected_batches")` (persisted across restarts by `SqlStore.DOCS` without editing `sqlstore.py`) without mutating `self.data`; validate batch mappings safely (reporting malformed entries in `unrouted`), route rejected batches (`status == "rejected"`) via `feed_failed_imports(queue, valid_batches, steward, shown_refusals)` when `steward` is named (or report unrouted rejected batches if no `data_steward` is named), and update `_exception_sources` so `NOT_CONNECTED` remains exact when both `stored_refusals is None` and no batch source is present, while stating connected refused-file and rejected-batch counts honestly when either is present.
  * Update `_recovery_requests()` to return ordered per-key history lists (`dict[str, list[dict[str, Any]]]`) of valid `exception_recovery_requested` audit entries, and update `_with_recoveries()` to copy each item via `deepcopy(item)` and assign a freshly constructed `trail` list (`item["audit_trail"] = trail` and `item["recovery"]["audit_trail"] = deepcopy(trail)`) for entries whose `action` is in `ALLOWED_ACTIONS[item["kind"]]`, so repeated calls in `request_exception_recovery` are strictly idempotent and never duplicate `audit_trail` entries.
  * Note on re-action rules: in `request_exception_recovery`, keep `closed` items immutable (`ValueError("This item is already closed.")`), while allowing an item in `held` or `rerun_requested` to record a subsequent valid audited action (such as `hold` -> `resolve_by_owner` or `hold` -> `request_rerun`), proving multi-entry `audit_trail` progression.
  * Provide a shared read-only outage-detection helper on `ExceptionRegisterMixin` inspecting `self.data.get("continuity")` (treating malformed non-`None` continuity documents via `not continuity.history_valid(doc)` and suspensions where `s.get("status") == "Suspended" or s.get("actual_hold", True)` as active outages) plus unrecovered `self.data.get("service_outages")`, and apply detected outages via `queue.record_detected_outage(component, since, note)` on both `state == "ok"` and `state == "roles_not_named"` banners. Keep `NO_HEALTH_CHECK` exact in `_exception_sources` when zero outages are active; when active outages > 0, state the recorded outage/suspension count in `_exception_sources` while still noting that no automated live service probe is connected.
  * In `exception_register()`, add `"viewer_roles": list(report["roles"].get(email, []))` and `"allowed_kinds": [k for k, r in report["scope"].items() if r in staff[email]]` inside `access` while keeping `access["roles"] == {email: list(report["roles"].get(email, []))}` and `access["scope"] == report["scope"]` (and keeping `roles_not_named` returning `access: {"roles": {}, "scope": {}, "viewer_roles": [], "allowed_kinds": []}`).
* Excluded: Mutating `self.data`, `cases`, `recommendations`, `import_refusals`, or `import_batches` during `exception_register` or `request_exception_recovery`.

#### Likely Targets

* src/core/src/zava_forward/core/exception_queue.py: Helper to attach detected system/continuity outages without mutating store data or failing when only a steward is configured.
* src/core/src/zava_forward/core/exception_register.py: `_build_exception_queue`, `_recovery_requests`, `_with_recoveries`, `exception_register`, and `_exception_sources`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Both `Store` (JSON) and `SqlStore` (SQLite) pass `src/api/tests/test_exception_register.py` with zero regressions.

#### Completion Evidence

* `exception_register` and `request_exception_recovery` expose rejected batches, full `audit_trail`, `viewer_roles`/`allowed_kinds`, and continuity/service `outage` banners across both stores.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Strengthen src/core unit tests for all five Issue #135 invariants

#### Context

`src/core/tests/test_exception_queue.py` and `src/core/tests/test_exception_feeds.py` cover baseline queue and feed behavior and should directly lock the enriched `#135` contract (`C1`, `C2`).

#### Intent

Add focused unit assertions in existing `src/core/tests/` files proving `resolution_owner`, `failure_category`, `correlation_id`, `recovery_context`, timestamped multi-step `audit_trail`, preserved `Unknown` eligibility and `original_source`, and `outage_banner` `next_steps`.

#### Boundaries

* Included: `src/core/tests/test_exception_queue.py` and `src/core/tests/test_exception_feeds.py` (exact test removals: `none`; <= 6 focused new test methods/assertions).
* Excluded: Trivial constant tests or duplicate implementation restatements.

#### Likely Targets

* src/core/tests/test_exception_queue.py: Assertions for `resolution_owner` on queued conflict items, `failure_category`/`correlation_id`/`recovery_context`, multi-step `hold` -> `resolve_by_owner`/`request_rerun` `audit_trail` with `at` timestamps, and `outage_banner` `next_steps` + `record_detected_outage`.
* src/core/tests/test_exception_feeds.py: Assertions for `correlation_id` preservation on `feed_failed_ai_runs` without leaking prompt/output text, plus `resolution_owner` on `feed_stock_conflicts` queued items.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `python3 -m unittest discover -s tests -q` in `src/core` exits `0`.

#### Completion Evidence

* Passing unit suite in `src/core` plus clean `mypy` and `ruff`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Interactive Employee Workbench Exception Queue UI and API Contract Verification

### Context

`GET /api/exceptions` and `POST /api/exceptions/recovery` are already wired in `src/api/src/zava_forward/api/server.py` and registered in `test_role_endpoint_inventory.py` (`C4`, `C5`), while `role-screens.js` (`#/screens?screen=data-operator&exceptions=1`) is locked as a strictly read-only specialist view by four `#229` test suites (`C8`, `C9`). Interactive employee workbench views with write actions live in `src/api/src/zava_forward/api/web/app.js` (`C10`). Before editing any file under `web/`, repository instructions require loading `redesign-existing-projects` and `web-design-guidelines` and fetching the current guidelines source.

### Intent

Build the accessible, Fluent 2-compliant `#/exceptions` operator and data steward exception queue view in `web/app.js` with controlled, audited recovery forms and plain-language outage/access panels, and prove all five Issue #135 criteria across API and shipped JS UI tests.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/app.js`, `src/api/tests/test_exception_register.py`, and new `src/api/tests/test_exception_queue_ui.py` (plus `src/api/src/zava_forward/api/web/index.html` only if a non-intrusive static attribute or landmark enhancement is warranted without adding banned words or extra scripts).
* Excluded: Modifying `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/workbench.py` (`me.navigation`), or `src/api/checks/workbench_browser_check.py`.

### Likely Targets

* src/api/src/zava_forward/api/web/app.js: Add `"key"` to `mutationKey`, add `#/exceptions` route label in `routeStatus` and route dispatch to `exceptionsView()`, add plain navigation links to `#/exceptions` from `importView` and `handoffWaitingView`, and implement `exceptionsView()` with accessible outage banner, scoped access card, conflict dual-value comparison with `resolution_owner`, owned failure items with `failure_category` / `correlation_id` / `recovery_context`, preserved `Unknown` eligibility and `original_source`, and controlled `POST /api/exceptions/recovery` form + `audit_trail` history.
* src/api/tests/test_exception_register.py: Add SQLite + JSON store and HTTP endpoint tests (`/api/exceptions` and `/api/exceptions/recovery`) covering all 5 `#135` criteria.
* src/api/tests/test_exception_queue_ui.py: New Node-VM test executing the shipped `exceptionsView` and `mutationKey` from `web/app.js` against synthetic contracts and mock `POST /api/exceptions/recovery` calls.

### Dependencies

* P01; activation of `redesign-existing-projects` and `web-design-guidelines` skills + fetched guidelines source before editing `web/app.js`.

### Validation Expectations

* `cd src/api && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests/test_exception_register.py tests/test_exception_queue_ui.py tests/test_exception_register_screen.py tests/test_data_operator_screen.py tests/test_data_steward_screen_wcag.py tests/test_role_screens.py tests/test_handoff_waiting_view.py tests/test_case_journey.py tests/test_epic149_role_workbench_heading_hierarchy.py tests/test_content_standard.py tests/test_design_system.py tests/test_app_js_notices_content.py -v` exits `0`.

### Completion Evidence

* Shipped `#/exceptions` UI in `web/app.js` passing lexical copy audit, design-system audit, `#229` read-only role-screen guards, and end-to-end API + Node-VM UI tests.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Activate web skills and implement accessible #/exceptions view and controlled recovery in web/app.js

#### Context

`web/app.js` uses `h(tag, attrs, ...kids)`, `api(path, body, signal)`, `ownedNotice(reason, nextAction)`, and `show(...nodes)` (`C10`). Every line in `web/app.js` is audited by `test_content_standard.py` (`C13`), which bans `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, and `envelope(s)` while allowing `"Keep on hold"`.

#### Intent

Implement `#/exceptions` (`exceptionsView`) in `web/app.js` following Fluent 2 tokens, WCAG 2.2 AA native semantics, fetched Web Interface Guidelines, and the plain-language content standard.

#### Boundaries

* Included:
  * Load `redesign-existing-projects` and `web-design-guidelines` skills and fetch the current Web Interface Guidelines URL before editing `web/app.js`.
  * Update `mutationKey(path, body)` in `web/app.js` to include `"key"` in its key list so `POST /api/exceptions/recovery` deduplicates per `(key, action)` without blocking distinct items.
  * Update `route()` in `web/app.js`: keep the `me.services?.cases === false` block (`Application Administrator`) unchanged so denied roles are not misrouted, match `const baseHash = hash.split("?")[0];` for `baseHash === "#/exceptions"` in `routeStatus` (`"Data steward and operator exception queue"`), and dispatch `if (baseHash === "#/exceptions") return await exceptionsView();`.
  * Add plain ASCII contextual links (`<a href="#/exceptions">Open the data steward and operator exception queue</a>`) in `importView()` and `handoffWaitingView()`, keeping all copy in `handoffWaitingView()` strictly ASCII (`text.isascii()`) and placing `EXCEPTIONS_DENIED`, `EXCEPTIONS_READ_ERROR`, and `exceptionsView` outside the `const WAITING_READ_ERROR`..`async function listView` Node-VM slice tested by `test_handoff_waiting_view.py`.
  * Implement `exceptionsView()` in `web/app.js` using pure ASCII strings and strict Epic #149 heading hierarchy (`<h1>Data steward and digital operator exception queue</h1>` rendered first in every loading, `ok`, `roles_not_named`, `403`, and read-error state, with `<h2>` sections and `<h3>` item subheadings never skipping levels):
    1. **Outage & service state banner** (`<section class="card" aria-label="Service and model outage status">`): rendered after `<h1>`, displaying non-colour state prefix (`Action needed: Service outage recorded`, `Warning: Service state Unknown`, or `Recorded check: No outage recorded at last check`), `banner.text`, affected `banner.components` (component name, `since`, `note`) when in `outage`, and plain-language `banner.next_steps`.
    2. **Operator and data steward access scope** (`<section class="card" aria-label="Your exception queue access">`): displays register state (`ok` vs `roles_not_named`), signed-in viewer's configured roles (`access.roles` / `access.viewer_roles`), permitted exception categories (`access.allowed_kinds`), full category-to-role ownership mapping (`access.scope`), `sources`, and `unrouted` warnings. On `403` (`e.status === 403`), displays `EXCEPTIONS_DENIED` explicitly embedding `"Owner: the programme owner. Next action: ask the programme owner to name a data steward and a digital operator before opening this queue."` (avoiding `ownedNotice`'s `application support` default); on other read errors, displays `EXCEPTIONS_READ_ERROR` naming `Owner: application support.` plus a `Check again` button.
    3. **Exception items & conflict dual-value display**: for each item in `data.items`:
       * Shows item `id`, human-readable category label, explicit `failure_category` (for failures) or conflict type, status with text cue (`Open`, `Paused for review`, `Human re-run requested`, `Closed by resolution owner`), configured `owner` and `owner_role`, `correlation_id`, `eligibility` (`Unknown: unresolved; original record kept`), and `original_source` summary (case/query/batch/record/file references, never overwriting or selecting a winner).
       * For conflict items (`Array.isArray(item.values)`), renders an accessible comparison table (`<caption>`, `<th scope="col">`) showing every competing value alongside its `source`, `date`, and `version`, plus explicit `Resolution owner: ${item.resolution_owner || item.owner}` and `"No winning source is selected automatically."`
       * Shows `recovery_context` (`runbook` guidance and explicit `"No automatic replay or resident/external release"` policy note).
    4. **Controlled, audited recovery form & audit trail**:
       * Maps action codes (`item.recovery_policy.allowed_actions` and `audit_trail[].action`) through one helper (`exceptionActionLabel(action)`) returning `"Request human re-run"` for `"request_rerun"`, `"Record owner resolution"` for `"resolve_by_owner"`, and `"Keep on hold"` otherwise, so zero bare banned stems appear in code, comments, or identifiers.
       * Renders existing `audit_trail` entries (`at`, `by`, `exceptionActionLabel(entry.action)`, `reason`, and `"Replayed: no; released: no"`).
       * When `item.status !== "closed"` and `item.recovery_key` is present, renders a native `<form>` with labelled `<select>` for `item.recovery_policy.allowed_actions` (mapping `"request_rerun"` -> `"Request human re-run"`, `"resolve_by_owner"` -> `"Record owner resolution"`, and fallback -> `"Keep on hold"` so no bare banned word appears!), labelled `<textarea maxlength="400">` for required reason (`autocomplete="off"`), inline accessible field error (`class="field-error"`, `role="status"`, `aria-invalid="true"`, `aria-describedby`) when reason is blank or server returns `400`/`403`, and submit `<button>` calling `api("/api/exceptions/recovery", { key: item.recovery_key, action, reason })` that updates the rendered item and announces completion in `role="status"` without automatic replay or release.
* Excluded: Using any bare word matching `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` anywhere in `web/app.js` (except the exact whitelisted phrase `"Keep on hold"`), inline styles, `innerHTML`, or edits to `role-screens.js`.

#### Likely Targets

* src/api/src/zava_forward/api/web/app.js: `mutationKey`, `route`, `handoffWaitingView`, `importView`, and `exceptionsView`.

#### Dependencies

* P01-T01, P01-T02; loaded `redesign-existing-projects` and `web-design-guidelines` skills.

#### Validation Expectations

* `python3 -m unittest tests/test_content_standard.py tests/test_design_system.py tests/test_app_js_notices_content.py tests/test_workspace_scripts.py` in `src/api` exits `0`.

#### Completion Evidence

* `#/exceptions` view implemented in `web/app.js` with full keyboard/screen-reader semantics and zero copy-audit or design-system violations.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Add focused API register and Node-VM UI tests for end-to-end #135 enforcement

#### Context

Existing `src/api/tests/test_exception_register.py` tests `SqlStore` and `Store` register basics (`C12`), while `test_exception_register_screen.py` tests read-only `role-screens.js` (`C9`). New tests must verify the HTTP endpoints (`GET /api/exceptions` and `POST /api/exceptions/recovery`), enriched store register fields, and the interactive `#/exceptions` UI in `web/app.js` end-to-end.

#### Intent

Prove all five Issue #135 acceptance criteria across `SqlStore`, `Store`, HTTP `/api/exceptions` + `/api/exceptions/recovery`, and shipped `web/app.js` (`exceptionsView`).

#### Boundaries

* Included:
  * Extend `src/api/tests/test_exception_register.py` (exact removals: `none`; <= 6 new test methods) to verify:
    1. Conflict items return `resolution_owner`, both values with `source`/`date`/`version`, `eligibility == "Unknown"`, and `original_source`.
    2. Rejected `import_batches` / `import_exceptions["rejected_batches"]` (`status == "rejected"`), `failed_ai_run` (with `correlation_id`), and `stranded_task` (including sourceless task fallback `ref`) route to their scoped owners with explicit `failure_category`, `correlation_id`, and `recovery_context` in both `SqlStore` and `Store` without editing `sqlstore.py`.
    3. Multi-step recovery (`hold` followed by `resolve_by_owner` / `request_rerun`) via `POST /api/exceptions/recovery` records actor, timestamp, action, and reason in ordered `audit_trail` with `POST` response `audit_trail` length == `GET` `audit_trail` length == `2` (proving idempotent `_with_recoveries`), enforces `403`/`400` boundaries, and never replays or mutates underlying case/recommendation/batch records.
    4. Active AI continuity suspension (`store.suspend(...)` and constructed-only restart where `actual_hold` remains `True`) transitions `GET /api/exceptions` `banner["state"]` from `"unknown"` to `"outage"` on both `ok` and `roles_not_named` responses with plain-language `next_steps` and non-contradictory `sources`, while `access` exposes `viewer_roles` and `allowed_kinds`.
  * Create `src/api/tests/test_exception_queue_ui.py` (1 new file; <= 6 test methods) executing shipped `web/app.js` (`mutationKey` and `exceptionsView`) in Node's `vm`:
    1. Renders `<h1>` first with non-skipping `h1 -> h2 -> h3` heading order and `<table>` `<caption>`/`<th scope="col">` semantics, scoped access (`viewer_roles`, `allowed_kinds`, `scope`), honest outage states (`unknown` and active `outage` with plain-language `next_steps`), dual-value conflicts with `source`/`date`/`version`/`resolution_owner`, and failure items (`failed_import`, `failed_ai_run`, `stranded_task`) with `failure_category`, `correlation_id`, `recovery_context`, `Unknown` eligibility, and `original_source`.
    2. Validates controlled recovery form: blocks blank reason client-side with `aria-invalid="true"`, submits `POST /api/exceptions/recovery` with `{key, action, reason}`, renders updated status + `audit_trail` (`by`, `at`, `action`, `reason`, no-replay/no-release), and hides the form once `closed`.
    3. Renders honest `403` denied, `roles_not_named`, and network/server failure states with named owner and next action, and escapes untrusted markup as plain text.
* Excluded: Editing `src/api/checks/workbench_browser_check.py` or deleting any existing tests.

#### Likely Targets

* src/api/tests/test_exception_register.py: HTTP and SQL/JSON store tests for enriched `#135` contract.
* src/api/tests/test_exception_queue_ui.py: Node-VM execution tests for `#/exceptions` in `web/app.js`.

#### Dependencies

* P01, P02-T01.

#### Validation Expectations

* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests/test_exception_register.py tests/test_exception_queue_ui.py -v` in `src/api` exits `0`.

#### Completion Evidence

* Passing `test_exception_register.py` and `test_exception_queue_ui.py` covering all 5 `#135` criteria end-to-end.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Tier Validation, Web Guidelines Review, and Clean Local Commit

### Context

Repository instructions classify bounded feature/UI/core issues without infrastructure, Dockerfile, dependency-manifest, workflow, or SQL-schema/migration changes under the Focused validation tier, while requiring strict `mypy`, `ruff`, affected unit/UI/copy/design-system suites, and a Web Interface Guidelines audit of changed web files.

### Intent

Verify zero static, lint, format, unit, copy-audit, design-system, or web-guideline regressions across `src/core` and `src/api`, reconcile all `.copilot-tracking/` artifacts, and prepare for the single `rpi-review` pass and local commit (`Refs #135`).

### Boundaries

* Included: Running validation commands in `src/core` and `src/api`, reviewing changed lines of `src/api/src/zava_forward/api/web/app.js` against fetched Web Interface Guidelines, and writing `.copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md`.
* Excluded: Pushing to `origin` or modifying `workbench_browser_check.py`.

### Likely Targets

* .copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md: Complete implementation, test, and validation evidence record.

### Dependencies

* P01, P02.

### Validation Expectations

* In `src/core`: `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -q` exits `0`.
* In `src/api`: `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests/test_exception_register.py tests/test_exception_queue_ui.py tests/test_exception_register_screen.py tests/test_data_operator_screen.py tests/test_data_steward_screen_wcag.py tests/test_role_screens.py tests/test_role_endpoint_inventory.py tests/test_handoff_waiting_view.py tests/test_case_journey.py tests/test_epic149_role_workbench_heading_hierarchy.py tests/test_content_standard.py tests/test_design_system.py tests/test_app_js_notices_content.py tests/test_static_assets.py tests/test_workspace_scripts.py -q` exits `0`.

### Completion Evidence

* Zero-error validation outputs recorded in `.copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run mypy, ruff, and focused unittest suites in src/core and src/api and record implementation evidence

#### Context

All modified packages (`src/core` and `src/api`) must pass type-checking, linting, formatting, and targeted unit/UI regression suites before transitioning to `rpi-review`.

#### Intent

Confirm deterministic Focused-tier compliance and reconcile plan, phase details, state JSON, and changes record.

#### Boundaries

* Included: Validation runs in `src/core` and `src/api`, Web Interface Guidelines check of `web/app.js`, and reconciling `P01`–`P03` markers and `.copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md`.
* Excluded: Remote git operations (`git push`).

#### Likely Targets

* .copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md: Implementation changes and validation log.
* .copilot-tracking/plans/2026-11-14/exception-queue-135-2330-plan.md: Checked phase/task markers upon completion.

#### Dependencies

* P01, P02.

#### Validation Expectations

* All `mypy`, `ruff`, and `unittest` commands exit `0`; `git diff -- src/api/checks/workbench_browser_check.py` is empty.

#### Completion Evidence

* Reconciled changes record, plan markers, and state JSON ready for `rpi-review`.

#### Unresolved Items

* None.
