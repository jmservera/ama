<!-- markdownlint-disable-file -->
# RPI Changes: Issue #163 Actual-Mode Provider Gate, Expiry Hold, and Retention Bound Hardening (Cycle 3)

## Metadata

* Task ID: issue-163-chat-privacy-region-c3
* Parent Task ID: issue-163-chat-privacy-region-c2
* Date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c3-phase-details.md
* Declared scope: Full plan (`P01`)
* Implementation status: Complete

## Active Execution Summary

Completed full-plan implementation (`P01-T01` and `P01-T02`), closing all three Cycle 2 review findings (`RV-001` through `RV-003`) and reconciling plan markers, phase details, changes evidence, and focused validation before Cycle 3 `rpi-review`.

## Completed Work by Plan Area

### Actual-Mode Provider Gate, Expiry Hold, and Digit-Length Bound (`P01-T01`)

* `src/core/src/zava_forward/core/chat_provider_position.py`: Updated `evaluate_provider_position()` so `is_actual and not DPO_LEGAL_APPROVED` appends `"actual_mode_dpo_legal_unapproved"` to `violations` and sets `transfer_ref_recorded` to `False`, closing `ZF_DATA_PROCESSING=actual` across `evaluate_provider_position`, `require_provider_position`, `regulatory_privacy.readiness_report`, `regulatory_privacy.build_foundry_query`, and `GET /api/chat/status` (including EU cross-border configurations with non-synthetic `CHAT_TRANSFER_REF`) while preserving `constructed`-mode synthetic fixture simulation (`RV-001`).
* `src/core/src/zava_forward/core/chat_privacy.py`:
  * Gated `ChatPrivacy.purge_expired()` on `self.decision()["retention_days"]`, returning `0` without deleting stored memory rows whenever no retention period is active/approved (`RV-002`).
  * Bounded `ChatPrivacy.decision()` `days_valid` with `1 <= len(days) <= 5` before `int(days)` so oversized ASCII digit strings (`"9" * 5000`) return `retention_days=None` without raising `ValueError` under Python's `int_max_str_digits` guard (`RV-003`).
* `src/core/README.md` and `docs/reference/research/chat-memory-dpia.md`: Noted `"actual_mode_dpo_legal_unapproved"` under `ZF_DATA_PROCESSING=actual` while keeping `D1` to `D8` `"Not recorded"` and `DPO_LEGAL_APPROVED = False`.

### Regression Assertions and Focused Validation (`P01-T02`)

* `src/core/tests/test_chat_provider_position.py` (`13` test methods, `0` removals, `0` new methods): Expanded `test_actual_data_mode_rejects_synthetic_and_demo_references`, `test_retention_stays_inactive_before_approval_or_when_provider_invalid`, and `test_regulatory_privacy_readiness_and_foundry_query_enforce_provider_position_no_echo` to assert `ZF_DATA_PROCESSING="actual"` fail-closed behavior (`"actual_mode_dpo_legal_unapproved"`, `transfer_ref_recorded=False`, `live_data_permitted=False`, `permitted=False`) for both `uksouth` and `westeurope` + `CHAT_TRANSFER_REF="TRA-2026-99"`, and `"9" * 5000` in `CHAT_RETENTION_DAYS`.
* `src/core/tests/test_chat_privacy.py` (`0` removals, `0` new methods): Expanded `test_no_expiry_without_retention` and `test_storage_refused_when_provider_or_region_unapproved` on `ChatPrivacyBehaviour` (exercised across `MemoryStoreChatPrivacy` and `SqlChatPrivacy`) to assert `purge_expired("9999-01-01T00:00:00+00:00") == 0` preserves pre-populated expiring memory rows under both unconfigured retention hold and `ZF_DATA_PROCESSING="actual"` hold, and that `"9" * 5000` returns `retention_days=None`.

## Discoveries, Amendments, and Divergences

* Local judgment (`ruff format`): Single-lined `transfer_ref_recorded` boolean expression in `chat_provider_position.py` to match `ruff format --check` (`100`-character line width). No plan amendments or divergences occurred.

## Validation Evidence

* `cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy`: Passed (`All checks passed!`, `310 files already formatted`, `Success: no issues found in 363 source files`).
* `cd src/api && python3 -m ruff check && python3 -m ruff format --check && PYTHONPATH=../core/src:../agents/src python3 -m mypy`: Passed (`All checks passed!`, `216 files already formatted`, `Success: no issues found in 300 source files`).
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_*chat*.py" -q`: Passed (`Ran 207 tests in 115.028s — OK`).
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_*privacy*.py" -q`: Passed (`Ran 80 tests in 14.740s — OK (skipped=1)`).
* `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_*chat*.py" -q`: Passed (`Ran 525 tests in 201.996s — OK (skipped=1)`).
* `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_chat_panel.py tests/test_content_standard.py tests/test_accessibility_baseline.py -v`: Passed (`Ran 122 tests in 36.945s — OK (skipped=1)`).
* `cd src/agents && PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest discover -s tests -p "test_*chat*.py" -q`: Passed (`Ran 124 tests in 17.792s — OK`).
* `python3 tools/rename-zava-tests.py`: Passed (`Ran 25 tests in 0.491s — OK`).
* `git --no-pager diff --check`: Passed (exit code `0`, zero whitespace/EOF errors).
* `tools/rpi-checks.py --all`: Intentionally skipped per caller instruction (`Validation tier: Focused`).

## Blockers and Remaining Work

* Blockers: None.
* Remaining in-scope work: None (`P01-T01` and `P01-T02` complete).
* Follow-up items outside active scope: Named human DPO and Legal review and sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` (`Refs #163`).
