<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #163 Actual-Mode Provider Gate, Expiry Hold, and Retention Bound Hardening (Cycle 3)

## Task Metadata

* Task ID: issue-163-chat-privacy-region-c3
* Parent Task ID: issue-163-chat-privacy-region-c2
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan.md
* Detail date: 2026-11-15

<!-- rpi:phase id=P01 -->
## P01: Harden Actual-Mode Provider Gate, Expiry Hold, Oversized-Days Bound, and Tests (`RV-001`–`RV-003`)

### Context

Cycle 2 review (`RV-001` through `RV-003`) identified three narrow residual gaps: `evaluate_provider_position()` in `ZF_DATA_PROCESSING=actual` mode when non-synthetic refs are passed directly outside `ChatPrivacy`, `ChatPrivacy.purge_expired()` missing a `retention_days` guard, and `ChatPrivacy.decision()` calling `int(days)` without a `len(days) <= 5` bound.

### Intent

Enforce all three guards cleanly without breaking SQL keyword rules (`PortabilityTests`), content-standard rules (`test_content_standard.py`), or `constructed`-mode synthetic fixtures.

### Boundaries

* Included: `src/core/src/zava_forward/core/chat_provider_position.py`, `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`.
* Excluded: Cycle 1 / Cycle 2 tracking files, `tools/rpi-checks.py --all`.

### Likely Targets

* src/core/src/zava_forward/core/chat_provider_position.py
* src/core/src/zava_forward/core/chat_privacy.py
* src/core/README.md
* docs/reference/research/chat-memory-dpia.md
* src/core/tests/test_chat_provider_position.py
* src/core/tests/test_chat_privacy.py

### Dependencies

* None.

### Validation Expectations

* Focused `src/core` and `src/api` unit suites, `ruff check`, `ruff format --check`, `mypy`, and `git diff --check` exit `0`.

### Completion Evidence

* Passing unit, lint, format, type, and whitespace checks recorded in `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c3-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Enforce `actual_mode_dpo_legal_unapproved` in `evaluate_provider_position()`, gate `purge_expired()`, and bound `len(days) <= 5` (`RV-001`–`RV-003`)

#### Context

See Cycle 2 `RV-001`, `RV-002`, and `RV-003`.

#### Intent

* In `chat_provider_position.py` (`evaluate_provider_position`):
  * When `is_actual and not DPO_LEGAL_APPROVED`, append `"actual_mode_dpo_legal_unapproved"` to `violations` and set `transfer_ref_recorded = bool(transfer_ref_valid and (not is_actual or DPO_LEGAL_APPROVED))`.
* In `chat_privacy.py`:
  * In `ChatPrivacy.decision()`: change `days_valid` to `1 <= len(days) <= 5 and days.isascii() and days.isdigit() and 1 <= int(days) <= 36500`.
  * In `ChatPrivacy.purge_expired(self, now=None)`: add `if not self.decision()["retention_days"]: return 0` at method start (no banned SQL keywords used).
* In `src/core/README.md` and `docs/reference/research/chat-memory-dpia.md`:
  * Mention `"actual_mode_dpo_legal_unapproved"` in `evaluate_provider_position` under `ZF_DATA_PROCESSING=actual` while `DPO_LEGAL_APPROVED` is `False`.

#### Boundaries

* Included: `chat_provider_position.py`, `chat_privacy.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`.
* Excluded: SQL keywords in `chat_privacy.py` or `"human-approved"` phrasing.

#### Likely Targets

* src/core/src/zava_forward/core/chat_provider_position.py
* src/core/src/zava_forward/core/chat_privacy.py
* src/core/README.md
* docs/reference/research/chat-memory-dpia.md

#### Dependencies

* None.

#### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, `PortabilityTests`, `test_content_standard.py`, and `git diff --check` pass.

#### Completion Evidence

* Updated runtime guards and synchronized documentation.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add regression assertions and run focused validation (`RV-001`–`RV-003`)

#### Context

Every Cycle 2 finding is verified with deterministic assertions inside existing test classes (`0` removals; `13` total methods preserved in `test_chat_provider_position.py`).

#### Intent

* Test ownership and bounds (locked before critique):
  * Canonical targets: `src/core/tests/test_chat_provider_position.py` (`exact removals: none`, `maximum new test methods: 0`, keeping `13` total methods by expanding `test_actual_data_mode_rejects_synthetic_and_demo_references`, `test_regulatory_privacy_readiness_and_foundry_query_enforce_provider_position_no_echo`, and `test_retention_stays_inactive_before_approval_or_when_provider_invalid`) and `src/core/tests/test_chat_privacy.py` (`exact removals: none`, `maximum new test methods: 0`, expanding `test_no_expiry_without_retention` and `test_storage_refused_when_provider_or_region_unapproved` on `ChatPrivacyBehaviour`, inherited by `MemoryStoreChatPrivacy`, `SqlChatPrivacy`, and `MssqlChatPrivacy`); generated targets: `none`.
  * Semantic vs regression coverage: semantic assertions verify actual-mode `DPO_LEGAL_APPROVED` fail-closed across all provider entrypoints (`RV-001`) and `purge_expired` retention-hold preservation (`RV-002`); regression assertions verify oversized ASCII digit strings (`"9" * 5000`) do not raise `ValueError` (`RV-003`) while existing `constructed` fixtures remain green.
* In `src/core/tests/test_chat_provider_position.py`:
  * Assert `evaluate_provider_position`, `require_provider_position`, `regulatory_privacy.readiness_report`, and `regulatory_privacy.build_foundry_query` under `ZF_DATA_PROCESSING="actual"` (both `uksouth` and `westeurope` with non-synthetic `CHAT_TRANSFER_REF="TRA-2026-99"` and `REAL_REG_REFS`) all fail closed with `"actual_mode_dpo_legal_unapproved"` (`valid=False`, `transfer_ref_recorded=False`, `live_data_permitted=False`, `permitted=False`) (`RV-001`).
  * Add `"9" * 5000` to the `invalid_days` loop in `test_retention_stays_inactive_before_approval_or_when_provider_invalid` (`RV-003`).
* In `src/core/tests/test_chat_privacy.py`:
  * In `test_no_expiry_without_retention`, after storing a memory item with an expiry under synthetic `constructed` approval, assert that holding/revoking retention (`CHAT_RETENTION_DAYS=""` or `ZF_DATA_PROCESSING="actual"`) causes `purge_expired("9999-01-01T00:00:00+00:00")` to return `0` and preserve the stored item (`RV-002`), and include `"9" * 5000` in `bad_days` in `test_storage_refused_when_provider_or_region_unapproved` (`RV-003`).
* Run focused `src/core` and `src/api` suites, `ruff check`, `ruff format --check`, `mypy`, and `git diff --check`.

#### Boundaries

* Included: `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`.
* Excluded: `tools/rpi-checks.py --all`.

#### Likely Targets

* src/core/tests/test_chat_provider_position.py
* src/core/tests/test_chat_privacy.py

#### Dependencies

* P01-T01

#### Validation Expectations

* All focused test suites, `ruff`, `mypy`, and `git diff --check` exit `0`.

#### Completion Evidence

* Passing outputs recorded in `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c3-changes.md`.

#### Unresolved Items

* None.
