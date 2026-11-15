<!-- markdownlint-disable-file -->
# RPI Phase Details: Epic #218 Responsible AI Release, Challenge and Incident Control

## Metadata

* Task ID: issue-218-rai-release-discipline
* Task slug: rai-218-release-discipline
* Related plan: .copilot-tracking/plans/2026-11-15/rai-218-release-discipline-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/rai-218-release-discipline-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/brds/agentic-retrofit-programme-brd.md, docs/case_study_48_addendum.md

## Phase Index

| Phase ID | Name                                                               | Status    | Detail sections            |
|----------|--------------------------------------------------------------------|-----------|----------------------------|
| P01      | Implement Core RAI Control Plane, OQ-017 Gate, and Traceability    | ready     | P01, P01-T01, P01-T02      |
| P02      | Wire API Readiness Payloads and Component Documentation            | ready     | P02, P02-T01               |
| P03      | Focused Unit Tests and Validation                                  | ready     | P03, P03-T01, P03-T02      |

<!-- rpi:phase id=P01 -->
## P01: Implement Core RAI Control Plane, OQ-017 Gate, and Traceability

### Context

Research (`C5`..`C16`) established that `src/core/src/zava_forward/core/rai_control_plane.py` does not yet exist, `assistant_release.record` does not require `approved_by` + `named_approval_id` on `actual`/live releases, `assistants.record_release` rolls back on `PermissionError`/`ValueError` without emitting an audit entry, and no centralized machine-readable traceability table or separated `rai_exercise_acceptance` / `real_ai_delivery_gate` report exists yet.

### Intent

Provide a single typed `rai_control_plane.py` module in `src/core` and wire it cleanly into existing release, assistant, live-report, governance, and store surfaces without breaking existing `src/core` or `src/api` tests.

### Boundaries

* Included: `src/core/src/zava_forward/core/rai_control_plane.py`, `rai_release.py`, `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, `store.py`, and `src/core/tests/release_support.py`.
* Excluded: `src/agents/`, `src/orchestrator/`, `src/importer/`, `infra/`, and `tools/`.

### Likely Targets

* src/core/src/zava_forward/core/rai_control_plane.py: New Epic #218 control-plane module.
* src/core/src/zava_forward/core/rai_release.py: Optional-key `approved_by` / `named_approval_id` check on `missing_binding(..., live=True)` and shared placeholder/non-human validation.
* src/core/src/zava_forward/core/assistant_release.py: Strict `OQ-017` `approved_by` + `named_approval_id` + live monitoring threshold check in `record()` when `cls == "actual"` or `live` is requested.
* src/core/src/zava_forward/core/assistants.py: Rejection audit emission (`store.audit` + committed `assistant_events` row) in `record_release()` for live activation attempts, plus separated readiness sections in `registry()`.
* src/core/src/zava_forward/core/ai_tasks.py: Include `rai_exercise_acceptance` and `real_ai_delivery_gate` in `live_report()`.
* src/core/src/zava_forward/core/governance.py: Include `rai_exercise_acceptance` and `real_ai_delivery_gate` in `governance_view()`.
* src/core/src/zava_forward/core/store.py: Add `rai_readiness_report()` helper and pass optional `assistants_service` into `ai_live_report` / `governance_view`.
* src/core/tests/release_support.py: Populate synthetic `approved_by` and `named_approval_id` when `cls == "actual"`.

### Dependencies

* None.

### Validation Expectations

* `(cd src/core && python3 -m mypy)` and `(cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -q)` pass with 0 errors.

### Completion Evidence

* `rai_control_plane.py` implemented, typed, and wired across `src/core` modules.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Author `src/core/src/zava_forward/core/rai_control_plane.py`

#### Context

Callers and tests need deterministic `OQ-017` live activation rejection + audit emission, a 15-requirement traceability table/helper, and separated `rai_exercise_acceptance` vs `real_ai_delivery_gate` payloads (`C1`..`C14`).

#### Intent

Implement `rai_control_plane.py` with zero external runtime dependencies and strict `mypy` annotations.

#### Boundaries

* Included:
  * `OQ_017 = "OQ-017"`, `LiveActivationApprovalError(PermissionError)` carrying `code="OQ-017"`, `task_id`, and `reasons`.
  * `valid_named_human_approver(value)` and `valid_named_approval_id(value)` rejecting empty/whitespace, non-strings, non-human tokens (`system`, `agent`, `bot`, `automation`, `automated`, `copilot`, `assistant`, `ai`, `llm`, `service`), and placeholder/fictional/unapproved tokens (`unknown`, `unavailable`, `none`, `unapproved`, `unassigned`, `placeholder`, `fictional`, `mock`, `synthetic`, `example`, `todo`, `tbd`, `tbc`, `n/a`, `null`, `auto`).
  * `validate_live_task_approval(task_id, approval)` normalizing `lookup_id = str(task_id or "").strip().removeprefix("legacy:")` before checking registered & enabled task (`ai_registry.get(lookup_id)`), `approved_by`, and `named_approval_id` (accepting mapping or keyword fields), returning normalized metadata or deterministic `OQ-017` rejection reasons.
  * `emit_live_activation_rejection_audit(store, *, actor, task_id, reasons, assistants_service=None)` committing immediately on SQL-backed stores via `store._audit_immediate({"ts": store.now(), "user": actor_id, "action": "rai_live_activation_rejected", "case_id": "-", "detail": detail})` when `hasattr(store, "_audit_immediate")` (avoiding `SqlStore` `self.local.pending` buffering inside `store.lock`) and otherwise acquiring `with store.lock:` before `store.audit(...)` on JSON `Store` / stub stores, plus committing a `live-activation-rejected` row in `assistant_events` in its own short transaction when `assistants_service` has active SQL (never opening nested `BEGIN IMMEDIATE`). Apply the same immediate-commit audit helper for `rai_live_activation_recorded`.
  * `activate_live_task(store, task_id, approval=None, *, approved_by=None, named_approval_id=None, actor=None, assistants_service=None, release_body=None)` validating `OQ-017` first; on any failure, emitting the audit record and raising `LiveActivationApprovalError`; when `assistants_service` and `release_body` are supplied, delegating to `assistants_service.record_release` with `evidence_class="actual"`, `approved_by`, and `named_approval_id`; otherwise recording `rai_live_activation_recorded` immediately on the store audit ledger and returning the validated activation receipt.
  * `REQUIRED_TRACEABILITY_IDS` and `REQUIREMENT_TRACEABILITY` covering `FR-051`, `FR-052`, `FR-053`, `FR-054`, `NFR-014`, `AC-069`, `AC-070`, `AC-071`, `AC-072`, `AC-073`, `OQ-017`, `OQ-018`, `OQ-019`, `RULE-024`, and `RULE-020` with workspace-relative repository test-target descriptors (`path::ClassName.test_method` or `path::ClassName`), plus `requirement_traceability()`, `requirement_traceability_map()`, `traceability_summary()`, and an AST-based target verifier `verify_traceability_targets(repo_root)` that validates both `src/core/tests` and `src/api/tests` callables without importing `zava_forward.api` or `zava_forward.agents`.
  * `exercise_acceptance_report(store, *, user=None, assistants_service=None, db=None)` returning `{"rai_exercise_acceptance": ..., "real_ai_delivery_gate": ...}` where `rai_exercise_acceptance` verifies local deterministic RAI controls independently of live model cut-over and `real_ai_delivery_gate` inspects SQL release state strictly read-only under `with assistant_release.read_only():` using a caller-supplied `db` connection or a read-only `store.assistant_connection()` query (never opening a nested `BEGIN IMMEDIATE` `assistants_service.transaction()`).
  * Strict typing boundary: keep `src/core/pyproject.toml` untouched, annotate every function/helper completely, and bind untyped migrated `core` modules (`ai_registry`, `assistant_release`, `challenges`, `continuity`, `cohort_eval`, `monitoring_coverage`, `human_review_effectiveness`, `regulatory_privacy`) through `Any`-typed module aliases or `Protocol` interfaces so `(cd src/core && python3 -m mypy)` passes under `strict = true`.
* Excluded: Modifying existing HTTP route paths or web UI files.

#### Likely Targets

* src/core/src/zava_forward/core/rai_control_plane.py: New module.

#### Dependencies

* `ai_registry`, `rai_release`, `challenges`, `continuity`, `cohort_eval`, `monitoring_coverage`, `human_review_effectiveness`, `regulatory_privacy`.

#### Validation Expectations

* Pure functions deterministic and `mypy`-clean under `src/core`.

#### Completion Evidence

* Module imports cleanly and exposes all control-plane, traceability, and readiness functions.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Integrate `rai_control_plane` across `rai_release.py`, `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, `store.py`, and `release_support.py`

#### Context

Live activation can also be attempted via `assistant_release.record` / `assistants.record_release` (`POST /api/assistants/releases`) with `evidence_class="actual"`, and operators read status/readiness via `store.ai_live_report`, `store.governance_view`, and `assistants.registry` (`C6`..`C9`, `C14`..`C17`).

#### Intent

Ensure every live activation path enforces `OQ-017` (`approved_by` + `named_approval_id`) with audit emission, and every status/readiness surface in `src/core` emits `rai_exercise_acceptance` separately from `real_ai_delivery_gate`.

#### Boundaries

* Included:
  * `rai_release.py`: In `missing_binding(record, binding, keys, now, live=False)`, when `live` is True and `"approved_by"` or `"named_approval_id"` is present in `record`, validate them so invalid values fail closed while preserving `test_rai_threshold_live_approval_guard.py` (`LiveReleaseApprover`) when bare dicts omit those keys.
  * `assistant_release.py`: In `record()`, after the manager/executive role check, detect live activation intent (`isinstance(body, Mapping)` and (`body.get("evidence_class") == "actual"` or `bool(body.get("live"))`)) ahead of `task not in task_ids` and `approvers` checks while leaving `constructed-fixture` error paths untouched: validate `approved_by`, `named_approval_id`, registered/enabled task (allowing `"legacy:"` prefix only when `lookup_id in task_ids`), appointed approver email (citing `OQ-017` when missing/unappointed on live activation), and `monitoring_coverage.check_monitoring_declaration(body.get("monitoring_declaration"), task_enabled=True, live=True)["missing"]`, raising `LiveActivationApprovalError` (`PermissionError` subclass citing `OQ-017`) on any missing/invalid live approval and storing `approved_by` and `named_approval_id` on `rec`.
  * `assistants.py`: In `record_release()`, detect live activation intent (`isinstance(body, Mapping)` and (`body.get("evidence_class") == "actual"` or `bool(body.get("live"))`)) at entry so that if `authorize(user, True)`, `not self.sql`, or `rel.record(...)` raises `(PermissionError, ValueError)` (after transaction rollback when `self.sql` is active), `rai_control_plane.emit_live_activation_rejection_audit(...)` persists the `OQ-017` rejection audit on both `self.sql` and `not self.sql` stores before re-raising. In `registry(user)`, attach `**rai_control_plane.exercise_acceptance_report(...)` on both the early `not self.sql` return and the SQL return (passing `db=db` inside `with assistant_release.read_only():` or computing after `with self.transaction() as db:` exits, never opening a nested `BEGIN IMMEDIATE`).
  * `ai_tasks.py`: In `live_report(store, user=None, assistants_service=None)`, include `rai_exercise_acceptance` and `real_ai_delivery_gate` from `rai_control_plane.exercise_acceptance_report`.
  * `governance.py`: In `governance_view(self, user, assessment=None, assistants_service=None)`, merge `**rai_control_plane.exercise_acceptance_report(self, user=user, assistants_service=assistants_service)` after `_need_manager` succeeds and outside `with self.lock:` so `store.lock` is never held across SQLite reads.
  * `store.py`: Add `rai_readiness_report(self, user=None, assistants_service=None)` and accept optional `assistants_service=None` in `ai_live_report`.
  * `src/core/tests/release_support.py`: Set `approved_by="Amina Okafor, RAI Assurance Lead"` and `named_approval_id="SYN-OQ017-APPROVAL-1"` in `fixture()` when `cls == "actual"` (unless overridden in `**over`).
* Excluded: Changing top-level keys of `GET /api/ai/report`.

#### Likely Targets

* src/core/src/zava_forward/core/rai_release.py: Optional live field guard.
* src/core/src/zava_forward/core/assistant_release.py: `OQ-017` check in `record()`.
* src/core/src/zava_forward/core/assistants.py: Rejection audit on live `record_release()` and readiness sections in `registry()`.
* src/core/src/zava_forward/core/ai_tasks.py: Readiness sections in `live_report()`.
* src/core/src/zava_forward/core/governance.py: Readiness sections in `governance_view()`.
* src/core/src/zava_forward/core/store.py: `rai_readiness_report()` and `ai_live_report(..., assistants_service=None)`.
* src/core/tests/release_support.py: Synthetic live approval fields for `cls == "actual"`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Existing `test_rai_release.py`, `test_rai_threshold_live_approval_guard.py`, `test_assistant_release.py`, `test_governance.py`, and `test_ai_tasks.py` continue to pass without regression.

#### Completion Evidence

* Rejected live `record_release` calls leave verifiable `store.audit` and `assistant_events` entries while keeping `assistant_releases` clean.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Wire API Readiness Payloads and Component Documentation

### Context

`src/api/src/zava_forward/api/server.py` owns `app.assistants` alongside `app.store` (`s`). Passing `assistants_service=app.assistants` into `s.ai_live_report(u, assistants_service=app.assistants)` and `s.governance_view(u, ..., assistants_service=app.assistants)` ensures the API's `real_ai_delivery_gate` reflects live SQL assistant release state accurately while preserving all existing top-level response keys and route inventories (`C17`, `C18`).

### Intent

Expose SQL-accurate `rai_exercise_acceptance` and `real_ai_delivery_gate` sections in `src/api` status/readiness endpoints and update component documentation.

### Boundaries

* Included: `src/api/src/zava_forward/api/server.py`, `src/core/README.md`, `src/api/README.md`.
* Excluded: Web UI static files under `src/api/src/zava_forward/api/web/`.

### Likely Targets

* src/api/src/zava_forward/api/server.py: Pass `assistants_service=app.assistants` in `/api/ai/report` and `/api/governance`.
* src/core/README.md: Document `rai_control_plane.py` (`OQ-017` live gate, traceability, separated readiness report).
* src/api/README.md: Document `rai_exercise_acceptance` and `real_ai_delivery_gate` on `/api/ai/report` (`live`), `/api/governance`, and `/api/assistants`, plus `OQ-017` audit emission on `/api/assistants/releases`.

### Dependencies

* P01.

### Validation Expectations

* `test_heldout_eval_api.py`, `test_role_endpoint_inventory.py`, `test_list_export_inventory.py`, and `mypy` in `src/api` pass.

### Completion Evidence

* HTTP responses from `/api/ai/report`, `/api/governance`, and `/api/assistants` include consistent `rai_exercise_acceptance` and `real_ai_delivery_gate` sections.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Wire `assistants` service context into `GET /api/ai/report` and `GET /api/governance` in `server.py` and document in `src/core/README.md` and `src/api/README.md`

#### Context

In `server.py`, `app.assistants` holds the SQL-backed `Assistants` service whereas `app.store` does not hold a back-reference to `app.assistants`. Passing `assistants_service=app.assistants` lets `real_ai_delivery_gate` inspect live SQL release coverage when called over HTTP.

#### Intent

Thread `assistants_service=app.assistants` into `s.ai_live_report` and `s.governance_view` in `server.py` (with backwards-compatible fallback if a test doubles `s` with a custom stub whose signature accepts only `(u)` or `(u, assessment)`) and document the behavior in `src/core/README.md` and `src/api/README.md`.

#### Boundaries

* Included: `server.py` `/api/ai/report` and both `/api/governance` branches (default and `?assessment=...`, using safe fallback if a test stub store lacks the `assistants_service` keyword parameter), `src/core/README.md`, `src/api/README.md`.
* Excluded: New HTTP endpoints or UI script changes.

#### Likely Targets

* src/api/src/zava_forward/api/server.py: Safe `assistants_service=app.assistants` forwarding.
* src/core/README.md: Concise Epic #218 section.
* src/api/README.md: Concise Epic #218 readiness & release-audit note.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `PYTHONPATH=../core/src:../agents/src python3 -m mypy` in `src/api` passes cleanly.

#### Completion Evidence

* Updated `server.py` and READMEs pass diff/link review and unit tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Unit Tests and Validation

### Context

Every Epic #218 acceptance criterion must be proven by focused unit tests in `src/core` and `src/api`, and all touched packages must pass `unittest`, `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` without invoking `tools/rpi-checks.py`.

### Intent

Lock focused, non-redundant unit and API tests covering all three acceptance criteria and edge cases, then execute the focused validation suite.

### Boundaries

* Included:
  * Locked test ownership:
    * Exact removals: `none`
    * Maximum additions: 2 test files (`src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py`), <= 20 focused test methods combined.
    * Canonical targets: `rai_control_plane`, `assistant_release`, `assistants`, `store`, `server`.
    * Generated targets: `none`.
    * Semantic-versus-regression coverage:
      * Semantic: `OQ-017` rejection & audit emission across blank/missing/system/placeholder `approved_by` and `named_approval_id`, disabled task (`chat-case-conversation`), and unappointed approver; dynamic import verification of all 15 traceability entries and explicit deferrals; independent `rai_exercise_acceptance` pass vs `real_ai_delivery_gate` block under offline, `ZF_AI=off`, unapproved SQL, and active suspension states.
      * Regression: `GET /api/ai/report` 5-key top-level contract, `store.verify_audit()` hash-chain integrity, `LiveReleaseApprover` bare-dict compatibility.
* Excluded: `tools/rpi-checks.py`, Playwright browser suites, and unrelated packages.

### Likely Targets

* src/core/tests/test_rai_control_plane_218.py: Core unit tests for AC 1, AC 2, and AC 3.
* src/api/tests/test_rai_release_readiness_api_218.py: HTTP API tests for AC 1 (`POST /api/assistants/releases` live rejection + audit) and AC 3 (`GET /api/ai/report`, `GET /api/governance`, `GET /api/assistants` separated readiness sections + manager RBAC).

### Dependencies

* P01, P02.

### Validation Expectations

* `(cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -q)` -> exit 0
* `(cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q)` -> exit 0
* `(cd src/core && python3 -m mypy)` -> exit 0
* `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` -> exit 0
* `python3 -m ruff check src/core src/api` -> exit 0
* `python3 -m ruff format --isolated --line-length 100 --check src/core src/api` -> exit 0

### Completion Evidence

* Recorded command outputs in `.copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add focused unit tests in `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py`

#### Context

Focused tests must fail without our changes and cover the exact acceptance criteria and edge cases.

#### Intent

Create `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py`, and include `test_rai_control_plane_218` and `test_rai_release_readiness_api_218` in the `OQ-017` and `FR-051`/`AC-069` traceability entries so the dynamic traceability resolver verifies them as well.

#### Boundaries

* Included: `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py` with full `strict = true` `mypy` type annotations (`-> None`, `Any`-typed untyped-module aliases, zero `pyproject.toml` edits), immediate SQL `sql_store.audit_entries()` + `sql_store.verify_audit()` assertions on rejected live activation, AST-based cross-package traceability verification in `src/core/tests` (plus `importlib` verification across both `src/core/tests` and `src/api/tests` inside `src/api/tests/test_rai_release_readiness_api_218.py`), and coverage of both `/api/governance` and `/api/governance?assessment=...`.
* Excluded: Duplicate trivial constant checks.

#### Likely Targets

* src/core/tests/test_rai_control_plane_218.py: Core unit tests.
* src/api/tests/test_rai_release_readiness_api_218.py: API endpoint and live-release rejection audit tests.

#### Dependencies

* P01, P02.

#### Validation Expectations

* Both new test modules run cleanly individually and inside full package discovery, and pass `mypy` and `ruff`.

#### Completion Evidence

* Passing test runs for both new files.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Run focused-tier validation on `src/core` and `src/api`

#### Context

Caller instructions require targeted `unittest`, `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` on touched packages (`src/core`, `src/api`) and forbid running `tools/rpi-checks.py`.

#### Intent

Verify zero test, typing, lint, or formatting regressions across `src/core` and `src/api`.

#### Boundaries

* Included: `src/core` and `src/api` `unittest`, `mypy`, `ruff check`, and `ruff format --check`.
* Excluded: `tools/rpi-checks.py`.

#### Likely Targets

* `src/core`, `src/api` (read-only verification commands).

#### Dependencies

* P03-T01.

#### Validation Expectations

* All six validation commands exit 0.

#### Completion Evidence

* Exact pass summaries recorded in `.copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md`.

#### Unresolved Items

* None.
