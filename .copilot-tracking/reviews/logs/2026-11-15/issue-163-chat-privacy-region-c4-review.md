<!-- markdownlint-disable-file -->
# Review: Issue #163 Actual-Mode Deployment Attestation and IaC Mismatch Disclosure (Cycle 4)

## Scope and Evidence

* Task ID: issue-163-chat-privacy-region-c4
* Parent Task ID: issue-163-chat-privacy-region-c3
* Review date: 2026-11-15
* Review scope: Full Cycle 4 task (`P01`)
* Assessed boundary: Cycle 4 remediation of Cycle 3 finding `RV-001` and Cycle 4 critique disposition `PC-001`, plus cross-route privacy/retention verification across `src/core/src/zava_forward/core/chat_provider_position.py`, `src/core/src/zava_forward/core/chat_privacy.py`, `src/api/src/zava_forward/api/server.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`, and `src/api/tests/test_chat_panel.py`.
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c4-changes.md
* Other evidence considered: .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c3-review.md; .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md; `git diff HEAD`; independent read-only review lens (`rubber-duck`).

## Opening Review State

* Interpreted review goal: Verify that Cycle 4 closes Cycle 3 `RV-001` and Cycle 4 `PC-001` accurately within the Focused validation boundary (`infra/` out of scope) and confirm no privacy-gate bypass or retention defect remains across `src/core` and `src/api`.
* Review scope: Full Cycle 4 task (`P01`)
* Evidence readiness: Cycle 4 plan, phase details, single-pass plan critique, reconciled changes record, and Cycle 3 parent artifacts are complete and aligned.
* Acceptance basis: Cycle 4 functional/non-functional requirements, acceptance criteria, `PC-001` critique disposition, and Focused validation suite outputs.
* First comparison boundary: Compare `P01-T01` and `P01-T02` against Cycle 3 `RV-001`, Cycle 4 `PC-001`, and all chat/memory routes in `src/core` and `src/api`.
* Active read-only boundaries: Write authority limited strictly to `.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c4-review.md` (and session state JSON on transition).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only post-implementation review on 2026-11-15 across Cycle 4 (`P01-T01`, `P01-T02`), combining direct code/diff inspection with an independent read-only `rubber-duck` lens. Confirmed Cycle 3 `RV-001` and Cycle 4 `PC-001` are fully resolved in `chat_provider_position.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, and `test_chat_provider_position.py`, while surfacing two genuine blocking defects (`RV-001` High on `POST /api/chat/threads/<tid>/proposals` bypassing `c.privacy._require()`, and `RV-002` Medium on `ChatPrivacy.purge_expired()` retaining previously scheduled `expires_at` memory rows indefinitely after provider/approval settings become invalid).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Actual-Mode Deployment Attestation, IaC Mismatch Disclosure, and Unit Verification | Reconciled for `P01` | Cycle 3 `RV-001` and Cycle 4 `PC-001` are cleanly closed; cross-route inspection surfaced `RV-001` in `server.py` (`POST /api/chat/threads/<tid>/proposals`) and `RV-002` in `ChatPrivacy.purge_expired()`. |
| `Follow-Up Items` | Human DPO/Legal sign-off on `D1`–`D8` (`Refs #163`) and separate Full-tier `infra/` Bicep alignment PR | Reconciled | Preserved outside active `Pxx` scope under Focused validation tier constraints. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/core/src/zava_forward/core/chat_provider_position.py, src/core/README.md, docs/reference/research/chat-memory-dpia.md | Added `deployment_attested` (`False` on `MODEL_PROVIDER_CONTRACT`, `False` when omitted or when `uksouth` + `DataZoneStandard` fails residency), required explicit `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` in `ZF_DATA_PROCESSING=actual` (`unattested_region_in_actual_mode`, `unattested_deployment_in_actual_mode`), and documented the `infra/main.bicep` `GlobalStandard` mismatch. | Closes Cycle 3 `RV-001` and Cycle 4 `PC-001`. | Passed (`ruff`, `mypy`, `git diff --check`) | Conformant |
| `P01-T02` | src/core/tests/test_chat_provider_position.py | Expanded deterministic assertions for `deployment_attested` and actual-mode attestation failures across `evaluate_provider_position`, `readiness_report`, and `build_foundry_query`. | `81` targeted core tests, `122` API tests, and `25` rename tests pass. | Passed | Conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` formatting | Applied `ruff format` (`100`-char line length) to `chat_provider_position.py`. | Local judgment recorded in `c4-changes.md`. | Recorded in `c4-changes.md`. | Not needed. | Justified and reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` from `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan-critique.md` (`deployment_attested = False` on `uksouth` + `DataZoneStandard` and `MODEL_PROVIDER_CONTRACT["deployment_attested"] is False`) was applied directly and verified in unit tests.
* Material revisions: None in Cycle 4. Note on `RV-002`: Cycle 3 gated `ChatPrivacy.purge_expired()` on `self.decision()["retention_days"]` to satisfy Cycle 2 `RV-002`, which inadvertently froze enforcement of already-recorded per-row `expires_at` deadlines whenever provider or approval settings later become invalid (`retention_days is None`). Restoring per-row `expires_at` purging in `purge_expired()` while keeping `decision()["retention_days"] = None` (so new items get `expires_at = None` and `purge_retention()` stays inactive without an approved period) satisfies both storage-limitation expiry enforcement and "nothing expires while no retention period is approved" without contradiction.
* Dependent-work pause assessment: None required.
* Justification assessment: Both `RV-001` and `RV-002` are small, deterministic fixes in `src/api/src/zava_forward/api/server.py` and `src/core/src/zava_forward/core/chat_privacy.py` suitable for Cycle 5 (`issue-163-chat-privacy-region-c5`, cycle 5 of `<= 5`).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Named human DPO and Legal review and sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` | Reserved to named human DPO and Legal owners under Issue #163 criterion 2. | Owner: Named human DPO and Legal | Open distinct governance follow-up (`Refs #163`). |
| Align `infra/main.bicep` `chatModelSku` and inject `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` in `infra/modules/containerapps.bicep` | Modifies `infra/`, which requires the Full RPI gate (`tools/rpi-checks.py --all`) explicitly excluded by caller's Focused validation tier. | Separate Full-tier IaC PR after DPO/Legal `D6` review | Open distinct infrastructure follow-up. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: `POST /api/chat/threads/<tid>/proposals` bypasses `c.privacy._require()` on existing threads when provider or privacy approval becomes invalid

* Related scope: Issue #163 Objective 2 & 3 (`server.py` chat privacy/provider gate consistency)
* Evidence: In `src/api/src/zava_forward/api/server.py` under `if parts[2] == "proposals":`, the route resumes an existing thread `tid`, calls `app.assistants.invoke(...)`, and writes a stored assistant message directly via `s.chat_add_message(...)` without calling `c.privacy._require()`. By contrast, `POST /api/chat/threads` (`c.privacy.start_thread`) and `POST /api/chat/threads/<tid>/messages` / `ask` (`iso.privacy._require()` in `chat_panel.py`) enforce `_require()` on every turn.
* Impact: If a thread was created while privacy/provider settings were valid and `CHAT_PROVIDER_REGION`, `CHAT_DEPLOYMENT_TYPE`, `CHAT_MODEL_TRAINING`, or DPO/Legal references subsequently become invalid, `POST /api/chat/threads/<tid>/proposals` still enqueues an AI proposal and appends a stored message to `chat_message` instead of failing closed with HTTP `403`.
* Destination: `rpi-implement`
* Smallest useful next action: Require `c.privacy._require()` at the start of `if parts[2] == "proposals":` in `src/api/src/zava_forward/api/server.py` before invoking `app.assistants.invoke(...)` or `s.chat_add_message(...)`, and add a regression assertion in `src/api/tests/test_chat_panel.py` verifying HTTP `403` (with zero new thread messages) on an existing thread when `CHAT_PROVIDER_REGION="eastus"` or `CHAT_DPIA_REF=""`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: `ChatPrivacy.purge_expired()` stops deleting already-expired `chat_memory` items when provider or approval settings later become invalid

* Related scope: Issue #163 Objective 2 & 3 (`src/core/src/zava_forward/core/chat_privacy.py`)
* Evidence: `ChatPrivacy.purge_expired()` currently checks `if not self.decision()["retention_days"]: return 0` before calling `repo.purge_memory(now or self._now())`. Because `repo.purge_memory` executes `DELETE FROM chat_memory WHERE expires_at IS NOT NULL AND expires_at < ?`, items created without an approved retention period already have `expires_at = None` and never expire; however, items created earlier under a valid retention period carry an explicit per-row `expires_at` deadline that stops being enforced if `CHAT_PROVIDER_REGION`, `CHAT_MODEL_TRAINING`, or approval env vars later turn `decision()["retention_days"]` to `None`.
* Impact: Already-expired personal memory items (`expires_at < now`) can be retained indefinitely past their recorded expiry date whenever permission to store new data is suspended or provider validation fails.
* Destination: `rpi-implement`
* Smallest useful next action: Remove the `if not self.decision()["retention_days"]: return 0` guard in `ChatPrivacy.purge_expired()` so `repo.purge_memory(now or self._now())` always honours previously recorded `expires_at` timestamps while `expires_at IS NULL` items (created without an approved retention period) remain untouched and `decision()["retention_days"]` / `purge_retention()` remain `None` / `applied=False` before approval or under invalid provider settings; update `src/core/tests/test_chat_privacy.py` accordingly.

## Defects

* `RV-001` (High, destination: `rpi-implement`)
* `RV-002` (Medium, destination: `rpi-implement`)

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child automatic RPI cycle (`issue-163-chat-privacy-region-c5`) | Enforce `c.privacy._require()` on `POST /api/chat/threads/<tid>/proposals` |
| `RV-002` | `rpi-implement` | Child automatic RPI cycle (`issue-163-chat-privacy-region-c5`) | Honour previously recorded `expires_at` timestamps in `ChatPrivacy.purge_expired()` independently of current write approval |

Later implementation of a routed finding does not require this Cycle 4 Review record to be rewritten.

## Residual Work

* Named human DPO and Legal review and sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` (`Refs #163` criterion 2).
* Separate Full-tier IaC PR updating `infra/main.bicep` `chatModelSku` and `infra/modules/containerapps.bicep` env wiring after DPO/Legal `D6` review.

## Blockers and Remaining Work

* Blockers: None for engineering Cycle 5; human DPO/Legal sign-off remains gated for Issue #163 criterion 2.
* Remaining work: Remediate `RV-001` and `RV-002` in child cycle `issue-163-chat-privacy-region-c5`.

## Validation Assessment

* Validation run: Focused validation (`ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, `81` targeted core tests, `122` API tests, `25` rename tests, `git diff --check`) all exited `0` in Cycle 4.
* Skipped or unavailable checks: `tools/rpi-checks.py --all` skipped per caller instruction (`Validation tier: Focused`).
* Validation gaps: Add regression assertions for `POST /api/chat/threads/<tid>/proposals` under invalid provider/privacy posture (`RV-001`) and `purge_expired()` enforcement of pre-recorded `expires_at` rows after provider/approval invalidation (`RV-002`).

## Outcome

* Outcome: Defects found
* Severity summary: 0 Critical, 1 High (`RV-001`), 1 Medium (`RV-002`), 0 Low
* Rationale: Cycle 4 cleanly resolved Cycle 3 `RV-001` and Cycle 4 `PC-001`, while independent cross-route inspection surfaced two concrete privacy/expiry edge cases (`RV-001`, `RV-002`) that should be closed before committing on `feat/chat-163-privacy-region`.
* Next recommended RPI stage or follow-up: Start child automatic RPI cycle `issue-163-chat-privacy-region-c5` (cycle 5 of `<= 5`) to close `RV-001` and `RV-002`.
