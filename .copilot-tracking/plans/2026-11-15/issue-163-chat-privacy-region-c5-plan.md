<!-- markdownlint-disable-file -->
# Implementation Plan: Issue #163 Proposal-Route Privacy Gate and Pre-Scheduled Memory Expiry Enforcement (Cycle 5)

* Task ID: issue-163-chat-privacy-region-c5
* Parent Task ID: issue-163-chat-privacy-region-c4
* Date: 2026-11-15
* Status: ready
* Research: .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md (`reused`)
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c5-phase-details.md

## Executive Summary

Cycle 4's post-implementation review confirmed that actual-mode deployment attestation (`deployment_attested`, `unattested_region_in_actual_mode`, `unattested_deployment_in_actual_mode`) and IaC mismatch documentation were cleanly resolved, while surfacing two remaining defects (`RV-001` High and `RV-002` Medium):

1. `POST /api/chat/threads/<tid>/proposals` in `src/api/src/zava_forward/api/server.py` resumes an existing thread, invokes `app.assistants.invoke(...)`, and appends a stored message via `s.chat_add_message(...)` without calling `c.privacy._require()`, allowing proposals and thread storage to proceed after privacy or model-provider settings become invalid (`RV-001`).
2. `ChatPrivacy.purge_expired()` in `src/core/src/zava_forward/core/chat_privacy.py` returns `0` when `self.decision()["retention_days"]` is currently `None`, preventing `repo.purge_memory(...)` (`DELETE FROM chat_memory WHERE expires_at IS NOT NULL AND expires_at < ?`) from deleting memory rows that already carry a recorded `expires_at` deadline when provider or approval settings later become invalid (`RV-002`).

Cycle 5 (`P01`) adds `c.privacy._require()` to `POST /api/chat/threads/<tid>/proposals` before `app.assistants.invoke(...)` / `s.chat_add_message(...)`, restores unconditional per-row `expires_at` purging in `ChatPrivacy.purge_expired()` while keeping `decision()["retention_days"] = None` and `purge_retention()["applied"] = False` whenever approval or provider posture is invalid, updates `src/core/README.md` if needed, expands deterministic assertions in `src/api/tests/test_chat_panel.py` and `src/core/tests/test_chat_privacy.py`, and verifies the Focused validation suite (`ruff`, `mypy`, unit suites, `git diff --check`).

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c4-review.md (`RV-001`, `RV-002`)
* src/api/src/zava_forward/api/server.py (`POST /api/chat/threads/<tid>/proposals`)
* src/core/src/zava_forward/core/chat_privacy.py (`ChatPrivacy.purge_expired`, `ChatPrivacy.decision`, `ChatPrivacy.purge_retention`)
* src/core/src/zava_forward/core/chatthreads.py (`purge_memory`: `DELETE FROM chat_memory WHERE expires_at IS NOT NULL AND expires_at < ?`)
* src/api/tests/test_chat_panel.py and src/core/tests/test_chat_privacy.py

## User Decisions and Requirements

* Complete the full RPI loop for Issue #163 in `/home/azureuser/source/ama-demo-wt/feat-163-chat-privacy-region` on branch `feat/chat-163-privacy-region` under the `Focused` validation tier (`src/core` / `src/api` unit tests, `ruff`, `mypy`; do not run `tools/rpi-checks.py --all`; do not touch `infra/`; do not push or open a PR).
* Fail closed on unapproved model-provider regions, SKUs, or training flags across chat and memory storage entrypoints while keeping DPO/Legal sign-off (`D1`–`D8`) human-gated and preventing any retention period from being set before approval.
* Close Cycle 4 review findings `RV-001` and `RV-002` under the bounded automatic correction-cycle grant (`cycle 5 of <= 5`, `#1798`).

## Goals

* Gate `POST /api/chat/threads/<tid>/proposals` on `c.privacy._require()` so invalid privacy or model-provider settings refuse proposal creation and thread message storage with HTTP `403` (`RV-001`).
* Ensure `ChatPrivacy.purge_expired()` deletes memory rows whose previously recorded `expires_at` deadline has passed even if write approval or provider settings later become invalid, while rows created without an approved retention period (`expires_at IS NULL`) never expire and `decision()["retention_days"]` / `purge_retention()` stay inactive (`RV-002`).
* Lock deterministic unit assertions for both fixes and pass Focused validation cleanly.

## Scope and Non-Goals

* In scope:
  * `src/api/src/zava_forward/api/server.py` (`POST /api/chat/threads/<tid>/proposals`)
  * `src/core/src/zava_forward/core/chat_privacy.py` (`ChatPrivacy.purge_expired`) and `src/core/README.md` (if wording touches `purge_expired`)
  * `src/api/tests/test_chat_panel.py` and `src/core/tests/test_chat_privacy.py`
* Non-goals / out of scope:
  * Modifying `infra/main.bicep` or `infra/modules/containerapps.bicep` (requires Full RPI gate outside Focused scope).
  * Recording DPO/Legal sign-off (`DPO_LEGAL_APPROVED` stays `False`; `D1`–`D8` stay `"Not recorded"`).
  * Pushing or opening a pull request.

## Functional Requirements

* `FR-01`: In `src/api/src/zava_forward/api/server.py`, `POST /api/chat/threads/<tid>/proposals` must call `c.privacy._require()` before `app.assistants.invoke(...)` and `s.chat_add_message(...)`, returning HTTP `403` (`ChatNotApproved`) with zero queued proposals and zero appended thread messages whenever DPO/Legal references or model-provider settings (such as `CHAT_PROVIDER_REGION="eastus"`) are unapproved.
* `FR-02`: In `src/core/src/zava_forward/core/chat_privacy.py`, `ChatPrivacy.purge_expired(now=None)` must execute `repo.purge_memory(now or self._now())` without short-circuiting on `self.decision()["retention_days"]`, so:
  * Memory items created when no retention period was approved have `expires_at = None` and are never deleted by `purge_expired()` (`0` rows deleted).
  * Memory items created earlier under an approved retention period (carrying a non-null `expires_at` timestamp) are deleted once `expires_at < now`, even if DPO/Legal references, provider settings (`CHAT_PROVIDER_REGION="eastus"`), or `ZF_DATA_PROCESSING=actual` later block creating new data (`decision()["approved"] == False` and `decision()["retention_days"] is None`).
  * `ChatPrivacy.decision()["retention_days"]` remains `None` and `ChatPrivacy.purge_retention()` remains a no-op (`applied=False`) whenever approval or provider posture is invalid.
* `FR-03` (`PC-001`): In `src/core/src/zava_forward/core/chat_privacy.py`, `ChatPrivacy.memory_status(user, task="")` must require `self.decision()["approved"]` (preserving existing switch-reason precedence `not gl` -> `not opted` -> `not tk` -> `not approved`) so `memory_status(...)["active"]` is `False` and `prompt_memory(user, task)` returns `[]` for previously opted-in users whenever privacy or model-provider settings become unapproved.

## Non-Functional Requirements

* `NFR-01`: Pass `ruff check`, `ruff format --check`, and `mypy` in both `src/core` and `src/api`, plus `git --no-pager diff --check`, with zero errors.
* `NFR-02`: Keep `.copilot-tracking/` references strictly out of `src/`, `docs/`, and commit messages.
* `NFR-03`: Preserve SQL portability invariants in `chat_privacy.py` (`PortabilityTests`: zero raw SQL keywords or connection creation in `chat_privacy.py`).

## Acceptance Criteria

* `AC-01`: `POST /api/chat/threads/<tid>/proposals` on a previously created case thread returns HTTP `403`, enqueues zero proposals, and appends zero messages when `CHAT_PROVIDER_REGION="eastus"` or `CHAT_DPIA_REF=""` (`RV-001`).
* `AC-02`: `ChatPrivacy.purge_expired()` deletes `0` rows when `expires_at` is `None` (created without an approved retention period), and deletes expired rows (`expires_at < now`) that were recorded under a prior valid retention period even when called through a `ChatPrivacy` instance whose provider or approval settings are now invalid (`RV-002`); and `memory_status(...)["active"]` is `False` / `prompt_memory(...)` returns `[]` for a previously opted-in user when provider or approval settings become invalid (`PC-001`).
* `AC-03`: Focused validation (`ruff`, `mypy`, `src/core` and `src/api` unit suites, `tools/rename-zava-tests.py`, `git diff --check`) passes with `0` failures.

## Test Ownership and Validation Lock

* Canonical test targets:
  * `src/api/tests/test_chat_panel.py` (expand existing `test_proposal_request_uses_the_assistants_path_and_checks_role`; `0` removals, `0` new test methods)
  * `src/core/tests/test_chat_privacy.py` (update `test_no_expiry_without_retention` and `test_expiry_set_and_purged_when_retention_approved` on `ChatPrivacyBehaviour`, exercising both `MemoryStoreChatPrivacy` and `SqlChatPrivacy`; `0` removals, `0` new test methods)
* Generated targets: `none`
* Exact removals: `none`
* Maximum additions: `0` new test files, `0` new test methods (focused assertion additions inside `2` existing test methods per file)
* Semantic vs regression coverage: Semantic assertions verifying HTTP `403` + unchanged thread messages + unchanged assistant proposal listing on `/proposals` under invalid provider/DPIA env (`RV-001`), and per-row `expires_at` enforcement vs `expires_at is None` preservation across invalid provider/approval env (`RV-002`).
* Required validation evidence: `ruff check`, `ruff format --check`, and `mypy` in `src/core` and `src/api`; `src/core` privacy/provider unit suites; `src/api` `test_chat_panel.py`, `test_assistants.py` (targeted or full panel/privacy check), `test_content_standard.py`, `test_accessibility_baseline.py`; `tools/rename-zava-tests.py`; `git --no-pager diff --check`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Enforce Proposal-Route Privacy Gate, Restore Per-Row Memory Expiry Purging, and Verify (`RV-001`, `RV-002`)

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Gate `/api/chat/threads/<tid>/proposals` on `c.privacy._require()` and honour recorded `expires_at` in `ChatPrivacy.purge_expired()` (`RV-001`, `RV-002`)

* Dependencies: None
* Primary files: `src/api/src/zava_forward/api/server.py`, `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/README.md`

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Update deterministic unit assertions in `test_chat_panel.py` and `test_chat_privacy.py` and run Focused validation (`RV-001`, `RV-002`)

* Dependencies: `P01-T01`
* Primary files: `src/api/tests/test_chat_panel.py`, `src/core/tests/test_chat_privacy.py`

## Implementation Context Record

| Field | Value |
|-------|-------|
| Interpreted goal | Close Cycle 4 findings `RV-001` and `RV-002` cleanly in Cycle 5 before final review and local `Refs #163` commit |
| Research disposition | `reused` (`.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c4-review.md`) |
| Active boundary | Focused validation tier (`src/core`, `src/api`, `docs/`); `infra/` untouched; no push or PR |
| Changes-record role | .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c5-changes.md (Complete; P01-T01 and P01-T02 verified) |
| Planning execution and readiness | Complete and reconciled for Review |

## Critique Disposition

* Critique artifact: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c5-plan-critique.md
* Critique execution status: Complete
* Verdict: Revise (`1` Medium finding: `PC-001`)
* Dispositions:
  * `PC-001` (Medium, direct planner correction — Applied): Added `FR-03` and updated `AC-02`, `P01-T01`, and `P01-T02` so `ChatPrivacy.memory_status()` requires `self.decision()["approved"]` after preserving switch-reason precedence (`not gl`, `not opted`, `not tk`), ensuring `memory_status()["active"]` is `False` and `prompt_memory()` returns `[]` for previously opted-in users whenever privacy or model-provider posture becomes invalid.

## Follow-Up Items

* Obtain named human DPO and Legal review and sign-off on decisions `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention (`Refs #163` criterion 2).
* Align `infra/main.bicep` `chatModelSku` default (currently `'GlobalStandard'`) and inject explicit `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` in `infra/modules/containerapps.bicep` in a separate Full-tier IaC PR after DPO/Legal `D6` confirmation.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c5-changes.md
* Ready phase or task: Complete (`P01`); ready for single-pass Cycle 5 `rpi-review`
* Remaining provisional question or blocker: None
