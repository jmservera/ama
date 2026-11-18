<!-- markdownlint-disable-file -->
# RPI Changes: Issue #163 Model Provider Data-Handling and Region Position Remediation (Cycle 2)

## Task Metadata

* Task ID: issue-163-chat-privacy-region-c2
* Parent Task ID: issue-163-chat-privacy-region
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan-critique.md
* Declared scope: Full plan (`P01`, `P02`)
* Execution status: Complete

## Summary

Cycle 2 implementation completed `P01` and `P02`, closing all five Cycle 1 post-implementation review findings (`RV-001` through `RV-005`) across `chat_provider_position.py`, `chat_privacy.py`, `regulatory_privacy.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/log.md`, `src/core/tests/`, and `src/api/tests/`.

## Completed Plan Items

### Core Privacy, Retention, Foundry Ambient-Env, and Disclosure Remediation (`P01`, `P01-T01`, `P01-T02`)

* `src/core/src/zava_forward/core/chat_provider_position.py`: Exported `DPO_LEGAL_APPROVED: Final[bool] = False` and added `modified_abuse_monitoring_verified: False` to `AbuseMonitoringDisclosure`, preserving conservative `default_sample_retention_days: 30` and `human_review_possible: True` under `mode="modified_recorded_unverified"` (`RV-001`, `RV-004`).
* `src/core/src/zava_forward/core/chat_privacy.py`: Gated `ZF_DATA_PROCESSING=actual` approval and retention on `DPO_LEGAL_APPROVED` (`actual_mode_unapproved`) in `ChatPrivacy.decision()` and `ChatPrivacy._require()`, and tightened `CHAT_RETENTION_DAYS` validation to `days.isascii() and days.isdigit() and 1 <= int(days) <= 36500` (`RV-001`, `RV-003`).
* `src/core/src/zava_forward/core/regulatory_privacy.py`: Added `_provider_env(env)` so `readiness_report()` and `build_foundry_query(...)` evaluate `os.environ` when `env is None` and fail closed on non-`None`, non-`Mapping` `env` values (`RV-002`).

### Documentation Precision, Whitespace Hygiene, and Regression Tests (`P02`, `P02-T01`, `P02-T02`)

* `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, and `docs/reference/log.md`: Scoped no-echo claims accurately to `provider_position` and `regulatory_privacy.readiness_report()`, documented conservative unverified modified abuse-monitoring disclosures and `DPO_LEGAL_APPROVED = False` actual-mode blocking, and stripped trailing EOF blank lines (`RV-004`, `RV-005`).
* `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`, and `src/api/tests/test_chat_panel.py`: Added deterministic assertions for non-synthetic refs in `ZF_DATA_PROCESSING=actual` mode (`RV-001`), omitted `env` (`os.environ`) and malformed non-mapping `env` in `readiness_report()` and `build_foundry_query(...)` (`RV-002`, `PC-001`), non-ASCII (`"\u00b2"`, `"\u0663\u0660"`) and `>36500` `CHAT_RETENTION_DAYS` (`RV-003`, `PC-002`), conservative unverified abuse-monitoring disclosures (`RV-004`), and HTTP `GET /api/chat/status` `provider_position` exposure and no-echo failure behavior (`RV-005`).

## Validation Evidence

* `src/core` focused unit suites (`test_chat_provider_position.py`, `test_chat_privacy.py`, `test_chat_dpia_record.py`, `test_chat_memory.py`, `test_chatthreads.py`, `test_chat_panel.py`, `test_regulatory_chat.py`, `test_regulatory_privacy.py`, `test_regulatory_privacy_audit_217.py`, `test_data_protection.py`, `test_scenario_manifest.py`, `test_needs_inventory.py`, `test_live_doc_links.py`): `265` + `test_live_doc_links.py` (`51` in combined provider/DPIA/doc-links run) passed (`OK`).
* `src/api` focused chat/privacy/accessibility/content suites (`test_chat_panel.py`, `test_home_chat_api.py`, `test_regulatory_chat_api.py`, `test_chat_isolation.py`, `test_chat_consent_boundary.py`, `test_diagnostic_log_privacy.py`, `test_accessibility_baseline.py`, `test_content_standard.py`): `205` tests passed (`OK`, `skipped=1`).
* `src/agents` chat suite (`test_*chat*.py`): `124` tests passed (`OK`).
* `python3 tools/rename-zava-tests.py`: `25` tests passed (`OK`).
* `src/core`: `python3 -m ruff check .`, `python3 -m ruff format --check .` (`310` files), and `python3 -m mypy` (`363` files): `0` issues.
* `src/api`: `python3 -m ruff check .`, `python3 -m ruff format --check .` (`216` files), and `PYTHONPATH=../core/src:../agents/src python3 -m mypy` (`300` files): `0` issues.
* `git --no-pager diff --check`: `0` issues (exit code `0`).
* Full gate `tools/rpi-checks.py --all`: Intentionally skipped per caller instruction (`Validation tier: Focused`).

## Implementation Updates and Discoveries

* Local judgment (`test_chat_provider_position.py`): When `CHAT_PROVIDER_REGION="eastus"` (or blank) without `CHAT_TRANSFER_REF`, `evaluate_provider_position` records both `"unapproved_region"` and `"cross_border_transfer_unapproved"`; asserted `"unapproved_region" in violations` while keeping `permitted=False` and no-echo checks strict.

## Blockers and Remaining Work

* Active blockers: None.
* Remaining active plan markers: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]`).

## Follow-Up Items

* Obtain named DPO and Legal sign-off on decisions `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention.
