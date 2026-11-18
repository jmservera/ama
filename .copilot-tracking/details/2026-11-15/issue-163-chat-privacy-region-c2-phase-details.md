<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #163 Model Provider Data-Handling and Region Position Remediation (Cycle 2)

## Task Metadata

* Task ID: issue-163-chat-privacy-region-c2
* Parent Task ID: issue-163-chat-privacy-region
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan.md
* Detail date: 2026-11-15

<!-- rpi:phase id=P01 -->
## P01: Remediate Core Privacy, Retention, Foundry Ambient-Env, and Disclosure Defects (`RV-001`–`RV-004`)

### Context

Cycle 1 review (`RV-001` through `RV-004`) identified four concrete edge-case flaws across `chat_provider_position.py`, `chat_privacy.py`, and `regulatory_privacy.py`.

### Intent

Enforce repository-recorded `DPO_LEGAL_APPROVED` on `ZF_DATA_PROCESSING=actual` storage and retention, preserve conservative unverified abuse-monitoring disclosures, enforce ASCII `1..36500` bounds on `CHAT_RETENTION_DAYS`, and honor ambient `os.environ` (or fail closed on malformed `env`) in `regulatory_privacy`.

### Boundaries

* Included: `src/core/src/zava_forward/core/chat_provider_position.py`, `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/src/zava_forward/core/regulatory_privacy.py`.
* Excluded: SQL queries/keywords inside `chat_privacy.py` (`PortabilityTests`), changes to `regulatory_privacy.CRITERIA` 8-tuple (`PC-001`), or flipping `DPO_LEGAL_APPROVED` to `True`.

### Likely Targets

* src/core/src/zava_forward/core/chat_provider_position.py
* src/core/src/zava_forward/core/chat_privacy.py
* src/core/src/zava_forward/core/regulatory_privacy.py

### Dependencies

* None.

### Validation Expectations

* `ruff check .`, `ruff format --check .`, and strict `mypy` pass in `src/core`.

### Completion Evidence

* Updated runtime gates in `chat_provider_position.py`, `chat_privacy.py`, and `regulatory_privacy.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Gate `ZF_DATA_PROCESSING=actual` on `DPO_LEGAL_APPROVED`, enforce ASCII `1..36500` retention bounds, and preserve conservative unverified abuse-monitoring disclosure (`RV-001`, `RV-003`, `RV-004`)

#### Context

1. `RV-001`: `ChatPrivacy.decision()` rejected `SYNTH-*`/demo refs in `ZF_DATA_PROCESSING=actual`, but allowed arbitrary non-synthetic env strings (`"DPIA-2026-99"`, `"RET-2026-99"`) to activate `approved=True` and `retention_days=30` while `dpo_legal_approved` remained `False`.
2. `RV-003`: `days.isdigit() and int(days) > 0` crashed with `ValueError` on `"\u00b2"` and accepted non-ASCII `"\u0663\u0660"` and `"36501"`.
3. `RV-004`: `evaluate_provider_position()` flipped `default_sample_retention_days` to `0` and `human_review_possible` to `False` when unverified `CHAT_ABUSE_MONITORING_MODIFIED_REF` was present.

#### Intent

* In `chat_provider_position.py`:
  * Export `DPO_LEGAL_APPROVED: Final[bool] = False` and set `"dpo_legal_approved": DPO_LEGAL_APPROVED` in `evaluate_provider_position` and `MODEL_PROVIDER_CONTRACT`.
  * Add `modified_abuse_monitoring_verified: bool` (`False`) to `AbuseMonitoringDisclosure` and `ABUSE_MONITORING_DISCLOSURE`, and keep `"default_sample_retention_days": 30` and `"human_review_possible": True` even when `mode == "modified_recorded_unverified"`.
* In `chat_privacy.py`:
  * Import `DPO_LEGAL_APPROVED` from `.chat_provider_position`.
  * Compute `actual_hold = is_actual and not DPO_LEGAL_APPROVED`.
  * Compute `approved = not missing and not synthetic_in_actual and not actual_hold and bool(pos["valid"])`.
  * Compute `days_valid = days.isascii() and days.isdigit() and 1 <= int(days) <= 36500` and `retention_set = approved and retention_ref_ok and days_valid`.
  * Expose `"actual_mode_unapproved": actual_hold` and `"dpo_legal_approved": DPO_LEGAL_APPROVED` in `decision()`.
  * In `ChatPrivacy._require()`, check `d["actual_mode_unapproved"]` after `missing` and `synthetic_refs_in_actual_mode`, raising `ChatNotApproved("Chat and memory storage is refused in actual data mode until named human DPO and Legal sign-off is recorded in the repository.")`.

#### Boundaries

* Included: `chat_provider_position.py`, `chat_privacy.py`.
* Excluded: Changing `constructed` mode (`ZF_DATA_PROCESSING` unset or `"constructed"`) behavior.

#### Likely Targets

* src/core/src/zava_forward/core/chat_provider_position.py
* src/core/src/zava_forward/core/chat_privacy.py

#### Dependencies

* None.

#### Validation Expectations

* `test_chat_provider_position.py` and `test_chat_privacy.py` pass alongside `mypy` and `ruff`.

#### Completion Evidence

* `actual` mode fails closed on both synthetic and non-synthetic refs while `DPO_LEGAL_APPROVED` is `False`; `CHAT_RETENTION_DAYS` enforces ASCII `1..36500`; `AbuseMonitoringDisclosure` preserves conservative defaults.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce ambient `os.environ` when `env=None` and fail closed on non-mapping `env` in `regulatory_privacy.py` (`RV-002`)

#### Context

In `regulatory_privacy.py`, `build_foundry_query(..., env: Any = None)` passed `env if isinstance(env, Mapping) else {}`, turning `env=None` into `{}` and bypassing ambient `os.environ` provider/region violations (`RV-002`).

#### Intent

* Define a small private helper `_provider_env(env: Any) -> Mapping[str, str] | None` in `regulatory_privacy.py`:
  * If `env is None`, return `None` (so `evaluate_provider_position(None)` reads `os.environ`).
  * If `isinstance(env, Mapping)`, return `env`.
  * Otherwise (malformed non-`None`, non-`Mapping` input), return `{"CHAT_PROVIDER_REGION": ""}` so `evaluate_provider_position` fails closed (`unapproved_region`) without echoing `env`.
* Use `_provider_env(env)` in both `readiness_report(env: Any = None)` (using `os.environ` for `GATE_REFS` when `env is None`, and `{}` for `GATE_REFS` when `env` is non-`Mapping`) and `build_foundry_query(..., env: Any = None)`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/regulatory_privacy.py`.
* Excluded: Altering `CRITERIA` or echoing raw env strings.

#### Likely Targets

* src/core/src/zava_forward/core/regulatory_privacy.py

#### Dependencies

* P01-T01

#### Validation Expectations

* `test_regulatory_privacy.py`, `test_regulatory_privacy_audit_217.py`, and `test_chat_provider_position.py` pass alongside strict `mypy`.

#### Completion Evidence

* `build_foundry_query` and `readiness_report` fail closed when `env=None` and `os.environ` violates provider/region/training rules or when `env` is a non-`Mapping` object.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Align Documentation, Whitespace Hygiene, and Regression Tests (`RV-001`–`RV-005`)

### Context

`RV-005` identified overbroad no-echo prose in `src/core/README.md`, missing HTTP `GET /api/chat/status` test assertions, and trailing EOF blank lines in `docs/reference/log.md` and `docs/reference/research/chat-memory-dpia.md`, alongside regression tests needed for `RV-001`–`RV-004`.

### Intent

Align documentation and whitespace hygiene, add targeted core and API HTTP tests within locked test bounds, and run focused validation.

### Boundaries

* Included:
  * Docs: `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/log.md`.
  * Test ownership and bounds (`exact removals: none`):
    * `src/core/tests/test_chat_provider_position.py` (`<= 3` new/expanded test methods; total `<= 16`).
    * `src/core/tests/test_chat_privacy.py` (`<= 1` expanded test method).
    * `src/api/tests/test_chat_panel.py` (`1` new HTTP `/api/chat/status` test method).
* Excluded: `tools/rpi-checks.py --all`, Cycle 1 review log edits.

### Likely Targets

* src/core/README.md
* docs/reference/research/chat-memory-dpia.md
* docs/reference/log.md
* src/core/tests/test_chat_provider_position.py
* src/core/tests/test_chat_privacy.py
* src/api/tests/test_chat_panel.py

### Dependencies

* P01

### Validation Expectations

* Focused `unittest` suites in `src/core` and `src/api`, `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, and `git diff --check` all exit `0`.

### Completion Evidence

* Clean test, lint, format, type, and whitespace verification recorded in `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c2-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Fix `src/core/README.md` no-echo claim, `chat-memory-dpia.md` unverified modified-abuse wording, and EOF blank lines (`RV-004`, `RV-005`)

#### Context

`ChatPrivacy.decision()["refs"]` returns operator-configured refs by existing design, whereas `provider_position` and `regulatory_privacy.readiness_report()` are strict no-echo dicts (`RV-005`).

#### Intent

* Update `src/core/README.md` to state that `ChatPrivacy.provider_position()`, `ChatPrivacy.decision()["provider_position"]`, `/api/chat/status` (`provider_position`), and `regulatory_privacy.readiness_report()` never echo raw governance reference strings or unallowlisted environment values, and document `DPO_LEGAL_APPROVED = False` blocking `ZF_DATA_PROCESSING=actual`.
* Clarify in `docs/reference/research/chat-memory-dpia.md` that `CHAT_ABUSE_MONITORING_MODIFIED_REF` records `"modified_recorded_unverified"` while preserving conservative `default_sample_retention_days: 30` and `human_review_possible: True` until DPO/Legal subscription verification, and that `ZF_DATA_PROCESSING=actual` stays refused while `DPO_LEGAL_APPROVED` is `False`.
* Remove trailing blank lines at EOF in `docs/reference/log.md` and `docs/reference/research/chat-memory-dpia.md`.

#### Boundaries

* Included: `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/log.md`.
* Excluded: Rewriting prior `docs/reference/log.md` entries or changing `D1`–`D8` status.

#### Likely Targets

* src/core/README.md
* docs/reference/research/chat-memory-dpia.md
* docs/reference/log.md

#### Dependencies

* P01

#### Validation Expectations

* `git diff --check` exits `0` and `test_chat_dpia_record.py` + `test_content_standard.py` pass.

#### Completion Evidence

* Clean diff with zero whitespace warnings and accurate documentation claims.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Add core and HTTP `/api/chat/status` regression tests and run focused validation (`RV-001`–`RV-005`)

#### Context

Every Cycle 1 finding requires a deterministic regression assertion that would fail without Cycle 2's fix.

#### Intent

* In `src/core/tests/test_chat_provider_position.py`:
  * Assert non-synthetic refs (`"DPIA-2026-99"`, `"LB-2026-99"`, `"NOTICE-2026-99"`, `"RET-2026-99"`, `CHAT_RETENTION_DAYS="30"`) under `ZF_DATA_PROCESSING="actual"` still yield `approved=False`, `actual_mode_unapproved=True`, `retention_days=None`, and raise `ChatNotApproved` (`RV-001`).
  * Assert both `regulatory_privacy.readiness_report()` and `regulatory_privacy.build_foundry_query(...)` with omitted `env` (`env=None`) under `patch.dict(os.environ, {"CHAT_PROVIDER_REGION": "eastus"})` and with malformed `env="PRIVATE-ENV-CANARY"` fail closed (`live_data_permitted=False` / `permitted=False`, `provider_position["valid"]=False`) and never echo `"PRIVATE-ENV-CANARY"` (`RV-002`, `PC-001`).
  * Assert `CHAT_RETENTION_DAYS` values `"\u00b2"`, `"\u0663\u0660"`, `"0"`, and `"36501"` return `retention_days=None` without raising `ValueError` (`RV-003`).
  * Update the modified abuse-monitoring test to assert `modified_abuse_monitoring_verified is False`, `default_sample_retention_days == 30`, and `human_review_possible is True` under `mode == "modified_recorded_unverified"` (`RV-004`).
* In `src/core/tests/test_chat_privacy.py`:
  * Expand `test_storage_refused_when_provider_or_region_unapproved` across `MemoryStore` and `SqlStore` to cover `"\u00b2"`, `"\u0663\u0660"`, `"36501"`, and non-synthetic refs in `ZF_DATA_PROCESSING="actual"` (`PC-002`).
* In `src/api/tests/test_chat_panel.py`:
  * Add `test_status_exposes_provider_position_and_refuses_unapproved_region` verifying `GET /api/chat/status` returns `provider_position` (`region="uksouth"`, `zero_model_training=True`, `dpo_legal_approved=False`), flips `storage_approved` to `False` and `provider_position["valid"]` to `False` under `CHAT_PROVIDER_REGION="PRIVATE-REGION-CANARY"` or `CHAT_PROVIDER_TRAINING="true"`, and never echoes `PRIVATE-REGION-CANARY` or raw `CHAT_TRANSFER_REF` values in the JSON response (`RV-005`).
* Run focused `unittest` suites, `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, and `git diff --check`.

#### Boundaries

* Included: `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`, `src/api/tests/test_chat_panel.py`.
* Excluded: `tools/rpi-checks.py --all`.

#### Likely Targets

* src/core/tests/test_chat_provider_position.py
* src/core/tests/test_chat_privacy.py
* src/api/tests/test_chat_panel.py

#### Dependencies

* P01, P02-T01

#### Validation Expectations

* All test suites, `ruff`, `mypy`, and `git diff --check` exit `0`.

#### Completion Evidence

* Passing execution outputs recorded in `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c2-changes.md`.

#### Unresolved Items

* None.
