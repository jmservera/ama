<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #121 Whole-System Data Protection, Retention, Derivative Dispatch, and Rights-Request Controls

## Metadata

* Task ID: issue-121-data-protection-controls
* Task slug: data-protection-controls-121
* Related plan: .copilot-tracking/plans/2026-11-15/data-protection-controls-121-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/data-protection-controls-121-research.md, src/core/src/zava_forward/core/data_protection.py, src/core/tests/test_data_protection.py, src/core/README.md, docs/reference/research/chat-memory-dpia.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Implement whole-system data protection inventory, task manifests, attachment dispatch, and rights ledger | ready | P01, P01-T01, P01-T02, P01-T03 |
| P02 | Add focused unit tests for inventory, manifests, attachment dispatch, and rights persistence | ready | P02, P02-T01 |
| P03 | Synchronize documentation, run focused validation, and freeze local commit | ready | P03, P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Implement whole-system data protection inventory, task manifests, attachment dispatch, and rights ledger

### Context

`src/core/src/zava_forward/core/data_protection.py` currently holds an 8-class reference register, 3 regulatory tasks, `validate_necessity_exception`, `model_dispatch`, `dispatch_hold`, `document_model_hold`, `validate_task_payload`, `due_date`, and an in-memory `rights_status` helper (`C2`). Issue #121 requires expanding this module to represent the whole-system RAI processing and retention inventory, all whole-system AI task manifests, strict intact-attachment model-dispatch gating, and a persisted store-backed / JSON-serializable rights-request ledger (`C1`, `C10`, `C14`).

### Intent

Complete all production logic changes in `src/core/src/zava_forward/core/data_protection.py` in a strictly typed (`mypy --strict`), stdlib-only manner that preserves every existing caller signature (`ai.py`, `ai_tasks.py`, `regulatory_privacy.py`, `api/server.py`).

### Boundaries

* Included: `src/core/src/zava_forward/core/data_protection.py` and registering `"rights_requests"` in `SqlStore.DOCS` / `SqlStore.MERGE_PRESERVED_DOCS` in `src/core/src/zava_forward/core/sqlstore.py`.
* Excluded: New microservices, custom SQLite/Azure SQL DDL, changes to `src/api` routes, or invented legal/DPO approvals.

### Likely Targets

* src/core/src/zava_forward/core/data_protection.py: Primary implementation module for inventory, task manifests, attachment dispatch, and rights-request ledger.
* src/core/src/zava_forward/core/sqlstore.py: Register `"rights_requests"` in `DOCS` and `MERGE_PRESERVED_DOCS` so `SqlStore` persists the rights-request document in the existing `meta` table.

### Dependencies

* None.

### Validation Expectations

* `(cd src/core && python3 -m mypy)` and `python3 -m ruff check src/core/src/zava_forward/core/data_protection.py src/core/src/zava_forward/core/sqlstore.py` exit `0`.

### Completion Evidence

* Updated `data_protection.py` exporting the expanded constants, functions, and `RightsRequestLedger` class with strict type annotations.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Expand DataClass inventory, subject populations, whole-system surfaces, and residency posture

#### Context

Currently `DATA_CLASSES` defines 8 classes (`fixture_resident`, `staff_identity`, `tenant_identity`, `review_record`, `raw_document`, `prompt_output`, `audit_ledger`, `telemetry`) without `subject_population`, `processing_surfaces`, `future_real_resident`, `provider_retained_copy`, or `hosting_region_vs_inference_residency` (`C2`). `GET /api/data-protection` serializes `register_report(os.environ)` directly and asserts `dpo_reviewed` is `False` and env reference strings are never echoed (`C6`).

#### Intent

Separate constructed resident fixtures from current staff/tenant identities, review records, and future real resident processing across all 9 actual data/processing classes and whole-system processing surfaces, and record explicit UK application hosting vs inference residency non-equivalence.

#### Boundaries

* Included:
  * Define `SUBJECT_POPULATIONS = ("constructed_resident_fixture", "current_staff_identity", "current_tenant_identity", "current_review_record", "future_real_resident")` and `WHOLE_SYSTEM_SURFACES = ("inputs", "raw_document_bytes", "prompts_outputs_citations", "reviewer_identity", "audit", "telemetry_tokens", "provider_processing", "provider_retained_copies")`.
  * Add defaulted `subject_population: str = ""` and `processing_surfaces: tuple[str, ...] = ()` fields after existing defaulted fields on `DataClass` (preserving valid dataclass field ordering and positional `DataClass(...)` constructor compatibility) while explicitly populating both fields on all 10 `DATA_CLASSES` entries.
  * Populate 10 `DATA_CLASSES` (1 `constructed`: `fixture_resident` with `subject_population="constructed_resident_fixture"`; plus 9 `actual` classes: `staff_identity` -> `current_staff_identity`, `tenant_identity` -> `current_tenant_identity` describing current signed-in tenant/resident or representative account identity claims while retaining `special_category=True, model_bound=True`, `review_record` -> `current_review_record`, `future_real_resident` -> `future_real_resident` describing future real resident household, contact, adjustment, and case-record personal data with `special_category=True, model_bound=True`, `raw_document` -> `future_real_resident` with `special_category=True, model_bound=True, needs_derivative=True`, `prompt_output` -> `current_staff_identity` with `model_bound=True`, `audit_ledger` -> `current_staff_identity`, `telemetry` -> `current_staff_identity`, and `provider_retained_copy` -> `current_staff_identity` with `model_bound=True` covering provider processing and retained abuse-monitoring/stateful copies).
  * Define `HOSTING_REGION_VS_INFERENCE_RESIDENCY` mapping containing `application_hosting_region: "uksouth"`, `uk_hosting_does_not_prove_uk_inference_residency: True`, `synthetic_resident_does_not_exempt_actual_staff: True`, `inference_residency_verified: False`, and `transfer_position_approved: False`.
  * Enrich `register_report(env)` per-class dicts with `subject_population` and `processing_surfaces` (`list[str]`), and top-level report keys `subject_populations` (grouping class IDs per population and separating `constructed` from `actual`), `hosting_region_vs_inference_residency`, and `whole_system_coverage` (mapping every surface in `WHOLE_SYSTEM_SURFACES` to its covering class IDs), while keeping `dpo_reviewed=False` and never echoing env reference values.
* Excluded: Echoing any `DP_*_REF` environment value or claiming `dpo_reviewed=True`.

#### Likely Targets

* src/core/src/zava_forward/core/data_protection.py: `DataClass`, `DATA_CLASSES`, `BY_ID`, `SUBJECT_POPULATIONS`, `WHOLE_SYSTEM_SURFACES`, `HOSTING_REGION_VS_INFERENCE_RESIDENCY`, and `register_report`.

#### Dependencies

* None.

#### Validation Expectations

* `register_report({})` is JSON-serializable, preserves all existing keys (`label`, `owners`, `dpo_reviewed`, `classes`, `statement`), includes the 9 actual classes and 5 subject populations, and never echoes reference strings.

#### Completion Evidence

* `DATA_CLASSES` and `register_report` implemented and verified via unit tests and `mypy`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Expand whole-system TASKS manifest and enforce non-sufficiency of user permission and intact attachment gates

#### Context

`TASKS` currently declares only `rule_lookup`, `check_explain`, and `alert_triage` using key `"fields"` (`C2`). Existing tests assert `spec["fields"]` (`C15`), while Issue #121 requires `TASKS` to cover `rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, and `case_brief` with `purpose`, `audience`, `permitted_fields`, `prohibited`, and `necessity`, and requires enforcing that `user_permission_granted=True` never establishes necessity and `storage_permission_granted=True` never approves sending intact attachments to AI.

#### Intent

Provide complete minimum-necessary manifests for all whole-system AI tasks and fail-closed necessity and derivative/scoped-necessity gates in `validate_task_payload`, `model_dispatch`, `dispatch_hold`, `document_model_hold`, and `dispatch_attachment_to_model`.

#### Boundaries

* Included:
  * Build task entries via a typed helper `_task_spec(purpose, audience, necessity, prohibited, permitted_fields)` that populates both `"permitted_fields"` and `"fields"` (pointing to the same `dict[str, tuple[type[Any], int]]` mapping) across all 7 required whole-system tasks (`rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, `case_brief`) PLUS legacy `"read_document"` so every dispatchable task is governed by an explicit `TASKS` manifest.
  * Align `SPECIAL_FIELDS` with `regulatory_privacy.SPECIAL_CATEGORY_FIELDS` while retaining all 7 existing members (`health`, `disability`, `ethnicity`, `religion`, `safeguarding`, `vulnerability`, `notes`, `adjustment`, `medical`, `biometric`, `genetic`, `sexual_orientation`, `trade_union`, `criminal`, `hardship`); ensure no `permitted_fields` map contains any `SPECIAL_FIELDS` or raw unredacted resident identity/contact/bytes field.
  * Update `validate_task_payload(task: str, payload: Mapping[str, Any], *, user_permission_granted: bool = False) -> dict[str, Any]`:
    * Always return `user_permission_granted=bool(user_permission_granted)` and `user_permission_establishes_necessity=False`.
    * Return `permitted=False` for unknown tasks regardless of `user_permission_granted`.
    * Strip undeclared keys (including any `"user_permission_granted"` key inside `payload`), `SPECIAL_FIELDS`, wrong-type values, and values exceeding `limit` — checking `int` safely via `type(value) is int and 0 <= value <= limit` (rejecting `bool`) and `str` via `isinstance(value, str) and len(value) <= limit` — never echoing field values.
    * Whenever `not kept` (including `{}` or `{"user_permission_granted": True}` or payloads containing only undeclared/special-category/invalid fields), return `permitted=False` with a clear minimum-necessary denial reason even when `user_permission_granted=True`; include `necessity=spec["necessity"]` and `prohibited=spec["prohibited"]`.
  * Update `model_dispatch`, `dispatch_hold`, `document_model_hold`, and `dispatch_attachment_to_model`:
    * Extend `model_dispatch` with keyword-only parameters `user_permission_granted: bool = False`, `storage_permission_granted: bool = False`, `redaction_reviewer_id: str | None = None`, `redaction_review_id: str | None = None`, `scoped_necessity_ref: str | None = None`, and `payload: Mapping[str, Any] | None = None` alongside existing `necessity_exception`, `task`, `case_id`, `doc_id`, `as_of`.
    * Unconditionally include `user_permission_establishes_necessity=False` and `storage_approves_ai_dispatch=False` on EVERY return dict from `model_dispatch` and `dispatch_attachment_to_model` across all early-return and final branches.
    * Validate `task in TASKS` BEFORE the `c.kind == "constructed"` return so unknown tasks fail closed even on constructed fixtures and even when `user_permission_granted=True`. When `payload is not None`, run `validate_task_payload(task, payload, user_permission_granted=user_permission_granted)` ahead of permitting dispatch and deny (`permitted=False`) if `not checked["permitted"]` or any field appears in `rejected`, `dropped`, or `special_category_dropped`.
    * Helper `_valid_redaction_review(reviewer_id, review_id)` verifies both strings are non-empty (`<= 120` chars), neither uses case-insensitive `.upper().startswith("SYNTH-")` or placeholder tokens (`synthetic`, `placeholder`, `mock`), and `reviewer_id` contains no `_AUTOMATED_APPROVERS` token.
    * Helper `_valid_scoped_necessity_ref(ref, task)` verifies `ref` is a non-empty string (`<= 120` chars), does not use case-insensitive `.upper().startswith("SYNTH-")` or placeholder/wildcard tokens (`*`, `all`, `any`, `synthetic`, `placeholder`, `mock`), and `task` is in `{"look_at_attachment", "read_document"}`.
    * Strict fail-closed attachment precedence for `needs_derivative` classes (`raw_document`): `storage_permission_granted=True` (`upload_permitted=True`, `download_permitted=True`) NEVER permits intact material. Reject `derivative == CONSTRUCTED_DERIVATIVE` (`"synthetic_safe"`) immediately (`permitted=False`, `manual_path=MANUAL_PATH`) with no fallback. When `derivative == "reviewed_redacted"`: if `task == "look_at_attachment"` or `redaction_reviewer_id is not None` or `redaction_review_id is not None`, require `_valid_redaction_review(redaction_reviewer_id, redaction_review_id)` and fail closed immediately if invalid (no `OR` fallback to `scoped_necessity_ref`), preserving 3-arg backward compatibility only when `task == "read_document"` and both reviewer args are `None`. When `derivative != "reviewed_redacted"`: if `necessity_exception is not None`, validate it strictly via `validate_necessity_exception(..., task=task, actual=True)` and fail closed immediately if invalid (no fallback to `scoped_necessity_ref`); otherwise permit only if `scoped_necessity_ref` passes `_valid_scoped_necessity_ref(scoped_necessity_ref, task)`; otherwise deny (`permitted=False`) with `manual_path=MANUAL_PATH`.
    * Forward optional keyword arguments (`user_permission_granted`, `storage_permission_granted`, `redaction_reviewer_id`, `redaction_review_id`, `scoped_necessity_ref`, `payload`, plus `task` on `document_model_hold` defaulting to `"read_document"`) through `dispatch_hold` and `document_model_hold`.
    * Implement `dispatch_attachment_to_model(env: Mapping[str, str] | None = None, *, derivative: str | None = None, redaction_reviewer_id: str | None = None, redaction_review_id: str | None = None, scoped_necessity_ref: str | None = None, necessity_exception: Any = None, storage_permission_granted: bool = False, upload_permitted: bool = False, download_permitted: bool = False, user_permission_granted: bool = False, payload: Mapping[str, Any] | None = None, task: str = "look_at_attachment", case_id: str | None = None, doc_id: str | None = None, as_of: str | date | datetime | None = None) -> dict[str, Any]` delegating through `model_dispatch("raw_document", ...)` (treating `storage_permission_granted or upload_permitted or download_permitted` uniformly as never approving AI dispatch) and always requiring valid human non-synthetic `redaction_reviewer_id` + `redaction_review_id` whenever `derivative == "reviewed_redacted"`.
* Excluded: Modifying `Ai.look_at` transport behavior in ways that break existing offline `constructed` mode tests.

#### Likely Targets

* src/core/src/zava_forward/core/data_protection.py: `TASKS`, `validate_task_payload`, `validate_necessity_exception`, `model_dispatch`, `dispatch_hold`, `document_model_hold`, and `dispatch_attachment_to_model`.

#### Dependencies

* P01-T01 (`BY_ID`, `DATA_CLASSES`).

#### Validation Expectations

* All existing `Dispatch`, `DispatchWiring`, `TaskPayload`, and `DocumentDerivativeAndProjectionTests` tests continue to pass alongside new attachment and task-necessity tests.

#### Completion Evidence

* Functions implemented with complete type annotations and verified under `mypy --strict`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Implement persisted Store-backed and JSON-serializable RightsRequestLedger workflow

#### Context

Currently `rights_status(requests, now)` only classifies an in-memory `list[dict[str, Any]]` and notes `"In-memory classification only: no rights log is persisted or answered here."` (`C2`). `Store` persists state in `store.data` via `store.save()`, locks via `store.lock`, and appends metadata-only ledger entries via `store.audit(who, action, case_id, detail)` (`C14`).

#### Intent

Provide `RightsRequestLedger` plus `record_rights_request`, `log_rights_action`, `answer_rights_request`, and polymorphic `rights_status` supporting `Store`-backed persistence, atomic JSON file persistence, and pure JSON serialization while strictly separating `local_deleted` from `provider_erasure_confirmed=False`.

#### Boundaries

* Included:
  * Register `"rights_requests"` in `SqlStore.DOCS` and `SqlStore.MERGE_PRESERVED_DOCS` in `src/core/src/zava_forward/core/sqlstore.py` so `SqlStore` (and `MssqlStore`) persists and reloads `store.data["rights_requests"]` via the existing `meta` table with zero new SQL DDL.
  * Define a structural `Protocol` `_RightsStoreProtocol` (`data: dict[str, Any]`, `save() -> None`, plus optional `lock` and `audit` inspected safely via `getattr`) so `RightsRequestLedger` accepts any `Store` / `SqlStore` instance cleanly under `mypy --strict`.
  * Define `RIGHTS_KINDS = ("access", "rectification", "erasure", "restriction", "objection", "portability")` and `RIGHTS_ACTIONS = ("locate", "export", "erase")`.
  * Implement `RightsRequestLedger`:
    * `__init__(self, store: Any = None, *, path: str | os.PathLike[str] | None = None, initial: Sequence[Mapping[str, Any]] | None = None)` supporting store-backed, file-backed (loads JSON on init if file exists and writes atomically via `.tmp` + `os.replace` on every mutation), or in-memory operation. Never cache a reference to `store.data["rights_requests"]` in `__init__`; always read and write `store.data["rights_requests"]` dynamically inside `with store.lock:` (or `contextlib.nullcontext()` when no `.lock` attribute exists) so `SqlStore._proc_sync()` never detaches in-memory state. Inside the lock, when `hasattr(store, "db")` call `store.audit(...)` BEFORE `store.save()` so `SqlStore` commits the `meta` document and queued `audit` row in one transaction; otherwise call `store.save()` BEFORE `store.audit(...)` (matching JSON `Store`). Never include raw `subject_key` in `store.audit` detail strings (emit metadata-only details with `request_id`, `kind`, `action`, `record_count`, `local_deleted`, `provider_erasure_confirmed=False`).
    * `record_request(self, *, request_id: str, kind: str, subject_key: str, received_at: str | datetime, actor: str = "staff", subject_population: str = "current_staff_identity", notes_ref: str = "") -> dict[str, Any]`: validates non-empty IDs, valid `kind` in `RIGHTS_KINDS`, valid timezone-aware `received_at` (`due_date` computed immediately and persisted as `due_at`), rejects duplicate `request_id`, stores BOTH `"id"` and `"request_id"` (preserving legacy `rights_status` row key `"id"`), initializes `actions: []`, `answered_at: None`, `local_deleted: False`, `provider_erasure_confirmed: False`, `provider_erasure_status: "unverified_external_processor"`, `audit_retention_refusal: None`, persists, and emits `subject_key`-free metadata-only `store.audit(actor, "rights.request.recorded", "-", ...)`.
    * `log_action(self, request_id: str, *, action: str, actor: str, at: str | datetime, target_scope: str = "local_store", record_count: int = 0, local_deleted: bool = False, provider_erasure_confirmed: bool = False, audit_retained_reason: str | None = None) -> dict[str, Any]`: validates `action` in `RIGHTS_ACTIONS`, timezone-aware `at`, non-negative `record_count`; raises `ValueError` if `provider_erasure_confirmed` is `True` (enforcing that local deletion or local action logging can never assert provider erasure); updates `local_deleted = record["local_deleted"] or (action == "erase" and bool(local_deleted))`, sets `provider_erasure_confirmed = False` and `provider_erasure_status = "not_confirmed_by_local_deletion"` when `local_deleted` becomes `True`, records optional `audit_retention_refusal` (DH-007 Article 17(3) refusal justification reference without personal content), appends the immutable action entry, persists, and emits `subject_key`-free metadata-only `store.audit`.
    * `answer_request(self, request_id: str, *, answered_at: str | datetime, actor: str, outcome: str = "completed", summary_ref: str = "", local_deleted: bool | None = None, provider_erasure_confirmed: bool = False, audit_retention_refusal: str | None = None) -> dict[str, Any]`: validates timezone-aware `answered_at` (`>= received_at`), raises `ValueError` if `provider_erasure_confirmed` is `True`, updates `answered_at`, `answered_by`, `outcome`, `summary_ref`, updates `local_deleted` if provided while keeping `provider_erasure_confirmed = False`, computes `within_one_month = answered_dt.date() <= due_dt.date()`, persists, and emits `subject_key`-free metadata-only `store.audit`.
    * Serialization methods: `requests(self) -> list[dict[str, Any]]`, `get(self, request_id: str) -> dict[str, Any]`, `status(self, now: datetime) -> dict[str, Any]`, `to_dict(self) -> dict[str, Any]`, `to_json(self) -> str`, `from_dict(cls, data: Mapping[str, Any]) -> RightsRequestLedger`, `from_json(cls, raw: str) -> RightsRequestLedger`.
  * Module-level functions `record_rights_request`, `log_rights_action`, `answer_rights_request` (each accepting `RightsRequestLedger | Store | SqlStore | str | os.PathLike[str]` via a helper `_coerce_ledger(target)`), and updated `rights_status(requests_or_ledger, now)`:
    * `rights_status` accepts `RightsRequestLedger`, a `Store`/`SqlStore`-like object, a file path, a dict with `"requests"`/`"rights_requests"`, or a plain `Sequence[Mapping[str, Any]]` (preserving 100% compatibility with existing `RightsClock.test_states`), requires timezone-aware `now`, and reports per-row `id`, `kind`, `due`, `state` (`open`, `overdue`, `answered`, `answered_late`), `within_one_month`, `action_kinds`, `local_deleted`, and `provider_erasure_confirmed` (`False`), plus top-level `persisted` boolean and explicit local-vs-provider erasure note.
* Excluded: Storing raw resident/staff message bodies or personal data values inside the rights ledger or audit entries.

#### Likely Targets

* src/core/src/zava_forward/core/data_protection.py: `RIGHTS_KINDS`, `RIGHTS_ACTIONS`, `RightsRequestLedger`, `record_rights_request`, `log_rights_action`, `answer_rights_request`, `due_date`, and `rights_status`.
* src/core/src/zava_forward/core/sqlstore.py: Add `"rights_requests"` to `DOCS` and `MERGE_PRESERVED_DOCS`.

#### Dependencies

* None.

#### Validation Expectations

* `RightsClock` existing tests pass unchanged; new persistence tests verify `Store`-backed save/audit, JSON file reload, `to_json`/`from_json` round-trip, 1-month deadline states, and `ValueError` on `provider_erasure_confirmed=True`.

#### Completion Evidence

* `RightsRequestLedger` and helper functions implemented and verified by unit tests and `mypy --strict`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Add focused unit tests for inventory, manifests, attachment dispatch, and rights persistence

### Context

`src/core/tests/test_data_protection.py` currently has 23 tests across `Register`, `Dispatch`, `DispatchWiring`, `TaskPayload`, `RightsClock`, and `DocumentDerivativeAndProjectionTests` (`C15`), and is type-checked under `mypy --strict` (`C9`).

### Intent

Add focused, high-signal unit tests proving all five Issue #121 behavioral requirements and edge cases without removing or weakening any existing test.

### Boundaries

* Included: `src/core/tests/test_data_protection.py` (exact removals: `none`; maximum additions: `<= 18` test methods).
* Excluded: Redundant constant-echo tests or modifications to unrelated test files.

### Likely Targets

* src/core/tests/test_data_protection.py: Canonical unit test module for `zava_forward.core.data_protection`.

### Dependencies

* P01.

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests TMPDIR=/dev/shm python3 -m unittest discover -s src/core/tests -p "test_data_protection*.py" -v` runs and passes all existing + new tests; `(cd src/core && python3 -m mypy)` exits `0`.

### Completion Evidence

* Passing test output recorded in `.copilot-tracking/changes/2026-11-15/data-protection-controls-121-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add inventory, residency, task-manifest, attachment-dispatch, and persisted rights tests

#### Context

Each of the five test areas requested in Objective 3 maps to concrete failure modes that would pass on the old implementation and fail without P01.

#### Intent

Add focused unit test methods covering:
1. Subject-population separation (`constructed_resident_fixture` vs `current_staff_identity`, `current_tenant_identity`, `current_review_record`, `future_real_resident`) and `hosting_region_vs_inference_residency["uk_hosting_does_not_prove_uk_inference_residency"] is True`.
2. Whole-system coverage across all 9 actual data/processing classes (`staff_identity`, `tenant_identity`, `review_record`, `future_real_resident`, `raw_document`, `prompt_output`, `audit_ledger`, `telemetry`, `provider_retained_copy`) and all 8 `WHOLE_SYSTEM_SURFACES`, confirming `SYNTH-` refs never satisfy actual classes and reference values never echo.
3. Per-task manifest validation across all 7 required whole-system tasks (`rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, `case_brief`) plus legacy `"read_document"`, proving `purpose`, `audience`, `permitted_fields`, `prohibited`, and `necessity`, and proving `user_permission_granted=True` never authorizes an undeclared task (including on `constructed` fixtures), an empty `{}` / all-prohibited payload, a `bool`-as-`int` / oversize / special-category field, or a disallowed `payload` passed to `model_dispatch`.
4. Intact attachment dispatch (`dispatch_attachment_to_model`, `model_dispatch(..., task="look_at_attachment")`, and `dispatch_hold`/`document_model_hold` forwarding) proving `storage_permission_granted=True` (`upload_permitted=True`, `download_permitted=True`) still denies intact material and returns `manual_path`, `reviewed_redacted` requires human non-synthetic `redaction_reviewer_id` and `redaction_review_id` (rejecting missing, case-insensitive `synth-`, or automated reviewer IDs with no `OR` rescue from `scoped_necessity_ref`), `scoped_necessity_ref` permits non-synthetic refs while rejecting `SYNTH-` or wildcard refs (and never rescues `CONSTRUCTED_DERIVATIVE` or an invalid `necessity_exception`), and `user_permission_establishes_necessity=False` / `storage_approves_ai_dispatch=False` appear on every dispatch return branch.
5. `RightsRequestLedger` persistence across JSON `Store`, SQLite `SqlStore` reopen (`SqlStore.DOCS`), and atomic JSON file reload + `to_json`/`from_json`, proving receipt-to-answer persistence, `locate`/`export`/`erase` action log, `subject_key`-free audit entries, 1-calendar-month statutory deadline states (`open`, `overdue`, `answered`, `answered_late`), `local_deleted=True` keeping `provider_erasure_confirmed=False`, and `ValueError` when attempting to set `provider_erasure_confirmed=True`.

#### Boundaries

* Included: `src/core/tests/test_data_protection.py`.
* Excluded: Modifying other test files.

#### Likely Targets

* src/core/tests/test_data_protection.py: New test classes/methods for Issue #121 RAI processing, attachment dispatch, and persisted rights ledger.

#### Dependencies

* P01-T01, P01-T02, P01-T03.

#### Validation Expectations

* All tests in `test_data_protection.py` pass and type-check cleanly under `mypy --strict`.

#### Completion Evidence

* Green unittest and mypy runs.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Synchronize documentation, run focused validation, and freeze local commit

### Context

`src/core/README.md` (`C7`) still describes `data_protection` as having 8 classes, 3 regulatory tasks, and no persisted rights log. `docs/reference/research/chat-memory-dpia.md` (`C8`) is the canonical KB DPIA synthesis guarded by `test_chat_dpia_record.py` (`C11`) and `test_regulatory_privacy.py` (`C12`).

### Intent

Synchronize `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, and `docs/reference/log.md`, verify all focused checks and KB doc guards pass, and record a single clean frozen commit on `feat/core-121-data-protection-controls`.

### Boundaries

* Included: `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, `docs/reference/log.md`, `.copilot-tracking/` artifacts, and local Git commit.
* Excluded: Altering `## Data map`, `## Decision pack for the DPO and Legal`, or `#217` retention table headings in `chat-memory-dpia.md`; ticking any DPO review checkbox; closing `#121`; pushing or opening a PR.

### Likely Targets

* src/core/README.md: Update `### Data protection register and dispatch gate (#121)` to describe the 10-class (1 constructed + 9 actual) inventory, `subject_population`, `hosting_region_vs_inference_residency`, 7-task `TASKS` manifest, `dispatch_attachment_to_model`, and `RightsRequestLedger` while explicitly stating DPO/Legal approvals and provider erasure confirmation remain open (`Refs #121`).
* docs/reference/research/chat-memory-dpia.md: Update `ms.date: 2026-11-15` and append `## Whole-System Processing, Derivative Dispatch and Rights-Request Controls (2026-11-15, Refs #121)` documenting the subject-population split, 9 actual classes, UK hosting vs inference residency boundary, task necessity manifest, intact-attachment derivative/necessity control, and persisted rights ledger with `local_deleted` vs `provider_erasure_confirmed=False`.
* docs/reference/README.md: Refresh the `chat-memory-dpia.md` index entry summary and date (`2026-11-15`).
* docs/reference/log.md: Append a `[2026-11-15] update | Issue #121 whole-system data protection, derivative dispatch and rights-request controls (Refs #121)` entry without modifying prior entries.

### Dependencies

* P01, P02.

### Validation Expectations

* Focused commands pass:
  * `python3 -m ruff check src/core/src/zava_forward/core/data_protection.py src/core/src/zava_forward/core/sqlstore.py src/core/tests/test_data_protection.py`
  * `python3 -m ruff format --check src/core/src/zava_forward/core/data_protection.py src/core/tests/test_data_protection.py`
  * `(cd src/core && python3 -m mypy)`
  * `PYTHONPATH=src/core/src:src/core/tests TMPDIR=/dev/shm python3 -m unittest discover -s src/core/tests -p "test_data_protection*.py" -v`
  * Regression/doc-guard verification: `PYTHONPATH=src/core/src:src/core/tests TMPDIR=/dev/shm python3 -m unittest src/core/tests/test_chat_dpia_record.py src/core/tests/test_regulatory_privacy.py src/core/tests/test_ai_dispatch_marker.py -v`

### Completion Evidence

* Clean `git status --short` after final commit (after `rpi-review` artifact is also written and verified so the frozen local commit includes the complete RPI evidence set).

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Update core README and knowledge-base privacy synthesis, index, and log

#### Context

AMA Repository Instructions require updating `docs/reference/README.md` and appending to `docs/reference/log.md` whenever a knowledge-base file changes materially, using `*` for unordered lists, plain ASCII punctuation, and no em dashes or bolded-prefix list items.

#### Intent

Accurately document the `#121` core contract and its governance boundaries across `src/core/README.md` and `docs/reference/`.

#### Boundaries

* Included: `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* Excluded: Rewriting historical log entries or modifying guarded blank DPO cells.

#### Likely Targets

* src/core/README.md: `### Data protection register and dispatch gate (#121)`.
* docs/reference/research/chat-memory-dpia.md: `ms.date` and appended `#121` H2 section.
* docs/reference/README.md: `Chat and Memory Data Protection Analysis Record` row.
* docs/reference/log.md: Appended `[2026-11-15]` entry.

#### Dependencies

* P01.

#### Validation Expectations

* Markdown links resolve; ASCII style rules respected; `test_chat_dpia_record.py` and `test_regulatory_privacy.py` pass.

#### Completion Evidence

* Clean `git diff` across documentation files and passing doc-guard tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Run focused validation suite and configure Git identity for frozen local commit

#### Context

The coordinator requested running focused validation only, resolving privacy-safe Git identity if needed, and committing all changes and `.copilot-tracking/` artifacts cleanly on `feat/core-121-data-protection-controls` with the Copilot co-author trailer without pushing or opening a PR.

#### Intent

Verify all lint, format, strict type, unit, and doc-guard checks pass and configure repository-local privacy-safe Git identity during `rpi-implement` so one single clean frozen commit on `feat/core-121-data-protection-controls` captures all source, documentation, and finalized `.copilot-tracking/` review/state artifacts immediately after `rpi-review` without amending commits.

#### Boundaries

* Included: Focused validation commands, repository-local Git user configuration (`{id}+{login}@users.noreply.github.com` from `gh api user`), and local commit with `Refs #121` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
* Excluded: Full Docker/SQL/browser gate, `git push`, `gh pr create`, or closing keywords for `#121`.

#### Likely Targets

* Local Git branch `feat/core-121-data-protection-controls` and `.copilot-tracking/changes/2026-11-15/data-protection-controls-121-changes.md`.

#### Dependencies

* P01, P02, P03-T01.

#### Validation Expectations

* Zero warnings/errors across `ruff check`, `ruff format --check`, `mypy`, and `unittest`, and clean `git status --short` at handoff.

#### Completion Evidence

* Recorded command exit codes in changes artifact and clean `git log -n 1` / `git status --short`.

#### Unresolved Items

* None.
