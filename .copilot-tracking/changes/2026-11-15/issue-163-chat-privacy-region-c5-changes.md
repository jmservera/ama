<!-- markdownlint-disable-file -->
# Changes Record: Issue #163 Proposal-Route Privacy Gate and Pre-Scheduled Memory Expiry Enforcement (Cycle 5)

* Task ID: issue-163-chat-privacy-region-c5
* Parent Task ID: issue-163-chat-privacy-region-c4
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c5-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c5-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c5-plan-critique.md
* Declared scope: Full plan (`P01`)
* Implementation status: Complete

## Active Execution Summary

Completed full-plan implementation (`P01-T01` and `P01-T02`), closing Cycle 4 review findings `RV-001` and `RV-002` and Cycle 5 critique item `PC-001` and reconciling all Cycle 5 artifacts before Cycle 5 `rpi-review`.

## Completed Work by Plan Area

### Proposal-Route Privacy Gate, Memory Prompt Gate, and Per-Row Expiry Enforcement (`P01-T01`)

* `src/api/src/zava_forward/api/server.py`: Added `c.privacy._require()` at the start of `POST /api/chat/threads/<tid>/proposals` (`if parts[2] == "proposals":`) before `app.assistants.invoke(...)` and `s.chat_add_message(...)`, refusing proposal queueing and thread message persistence with HTTP `403` (`ChatNotApproved`) whenever DPO/Legal references or model-provider settings become invalid (`RV-001`).
* `src/core/src/zava_forward/core/chat_privacy.py`:
  * Updated `ChatPrivacy.memory_status(user, task="")` to require `d["approved"]` after preserving existing switch-reason precedence (`not gl`, `not opted`, `not tk`), ensuring `memory_status()["active"]` is `False` and `prompt_memory()` / `ChatIsolation.build_prompt()` returns `[]` for previously opted-in users whenever privacy or model-provider settings become invalid (`PC-001`).
  * Restored unconditional per-row `expires_at` purging in `ChatPrivacy.purge_expired()` (`repo.purge_memory(now or self._now())`), so memory rows created earlier with a recorded `expires_at` deadline are purged once past expiry even if provider or approval settings later become invalid, while rows created without an approved retention period (`expires_at is None`) never expire and `decision()["retention_days"]` / `purge_retention()` stay `None` / `applied=False` (`RV-002`).

### Deterministic Unit Assertions and Focused Validation (`P01-T02`)

* `src/api/tests/test_chat_panel.py`: Expanded `test_proposal_request_uses_the_assistants_path_and_checks_role` to verify HTTP `403`, `Assistants.invoke.assert_not_called()`, and zero appended thread messages on an existing case thread under `CHAT_PROVIDER_REGION="eastus"` and `CHAT_DPIA_REF=""`, followed by HTTP `202` when valid (`RV-001`).
* `src/core/tests/test_chat_privacy.py`: Updated `test_no_expiry_without_retention` on `ChatPrivacyBehaviour` (exercised across both `MemoryStoreChatPrivacy` and `SqlChatPrivacy`) to verify `memory_status()["active"] is False`, `prompt_memory() == []`, preservation of `expires_at is None` rows, and purging of previously recorded `expires_at` rows across both `CHAT_PROVIDER_REGION="eastus"` and `ZF_DATA_PROCESSING="actual"` (`RV-002`, `PC-001`).

## Discoveries, Amendments, and Divergences

* None.

## Validation Evidence

* `cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy`: Passed (`All checks passed!`, `310 files already formatted`, `Success: no issues found in 363 source files`).
* `cd src/api && python3 -m ruff check && python3 -m ruff format --check && PYTHONPATH=../core/src:../agents/src python3 -m mypy`: Passed (`All checks passed!`, `216 files already formatted`, `Success: no issues found in 300 source files`).
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_chat_provider_position.py tests/test_chat_privacy.py tests/test_chat_memory.py tests/test_chat_dpia_record.py tests/test_regulatory_privacy.py tests/test_regulatory_privacy_audit_217.py -q`: Passed (`Ran 108 tests in 13.703s — OK`).
* `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_chat_panel.py tests/test_content_standard.py tests/test_accessibility_baseline.py -q`: Passed (`Ran 122 tests in 40.913s — OK (skipped=1)`).
* `python3 tools/rename-zava-tests.py`: Passed (`Ran 25 tests in 0.564s — OK`).
* `git --no-pager diff --check`: Passed (exit code `0`).
* `tools/rpi-checks.py --all`: Intentionally skipped per caller instruction (`Validation tier: Focused`).

## Blockers and Remaining Work

* Blockers: None.
* Remaining in-scope work: None (`P01-T01` and `P01-T02` complete).
* Follow-up items outside active scope:
  * Named human DPO and Legal review and sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` (`Refs #163`).
  * Separate Full-tier IaC PR aligning `infra/main.bicep` `chatModelSku` and injecting `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` in `infra/modules/containerapps.bicep` after DPO/Legal `D6` confirmation.
