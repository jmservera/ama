<!-- markdownlint-disable-file -->
# Review: Issue #163 Proposal-Route Privacy Gate and Pre-Scheduled Memory Expiry Enforcement (Cycle 5)

## Scope and Evidence

* Task ID: issue-163-chat-privacy-region-c5
* Parent Task ID: issue-163-chat-privacy-region-c4
* Review date: 2026-11-15
* Review scope: Full Cycle 5 task (`P01`) and cumulative Issue #163 branch diff against `HEAD`
* Assessed boundary: Cycle 5 remediation of Cycle 4 findings `RV-001` and `RV-002` and Cycle 5 critique disposition `PC-001`, plus cumulative `#163` branch changes across `src/core/src/zava_forward/core/chat_provider_position.py`, `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/src/zava_forward/core/regulatory_privacy.py`, `src/api/src/zava_forward/api/server.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, `docs/reference/log.md`, `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`, `src/core/tests/test_chat_dpia_record.py`, and `src/api/tests/test_chat_panel.py`.
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c5-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c5-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c5-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c5-changes.md
* Other evidence considered: .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c4-review.md; .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md; `git --no-pager diff HEAD`; independent read-only review lens (`rubber-duck`).

## Opening Review State

* Interpreted review goal: Verify that Cycle 5 completely closes Cycle 4 defects `RV-001` and `RV-002` and Cycle 5 critique item `PC-001`, and confirm the cumulative `#163` branch implementation is conformant within the Focused validation boundary (`infra/` out of scope; human DPO/Legal sign-off preserved open under `Refs #163`).
* Review scope: Full Cycle 5 task (`P01`)
* Evidence readiness: Cycle 5 plan, phase details, single-pass plan critique, reconciled changes record, and Cycles 1–4 parent artifacts are present and aligned.
* Acceptance basis: Cycle 5 `FR-01`–`FR-03`, `NFR-01`–`NFR-03`, `AC-01`–`AC-03`, `PC-001` disposition, and Focused validation suite outputs.
* First comparison boundary: Compare `P01-T01` and `P01-T02` against Cycle 4 `RV-001`–`RV-002`, Cycle 5 `PC-001`, and cumulative `git --no-pager diff HEAD`.
* Active read-only boundaries: Write authority limited strictly to `.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c5-review.md` (and session state JSON on transition).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only post-implementation review on 2026-11-15 across Cycle 5 (`P01-T01`, `P01-T02`) and the cumulative `#163` diff, combining direct code/diff verification with an independent read-only `rubber-duck` lens. Confirmed `RV-001`, `RV-002`, and `PC-001` are fully resolved with zero blocking or residual engineering defects in scope and zero new `.copilot-tracking/` references introduced into `src/` or `docs/`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Proposal-Route Privacy Gate, Memory Prompt Gate, Per-Row Memory Expiry Enforcement, and Focused Verification | Reconciled | `POST /api/chat/threads/<tid>/proposals` calls `c.privacy._require()` before `app.assistants.invoke` and `s.chat_add_message`; `ChatPrivacy.memory_status()` and `prompt_memory()` fail closed when `not decision()["approved"]`; `ChatPrivacy.purge_expired()` purges pre-recorded `expires_at` rows while preserving `expires_at is None` rows and inactive `retention_days`; unit tests and linters pass. |
| `Follow-Up Items` | Human DPO/Legal sign-off on `D1`–`D8` (`Refs #163`) and separate Full-tier `infra/` Bicep alignment PR | Reconciled | Preserved outside active `Pxx` scope under Focused validation tier constraints. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/api/src/zava_forward/api/server.py, src/core/src/zava_forward/core/chat_privacy.py | Enforced `c.privacy._require()` on `POST /api/chat/threads/<tid>/proposals` (`RV-001`), gated `memory_status()` / `prompt_memory()` on `decision()["approved"]` (`PC-001`), and restored per-row `expires_at` purging in `purge_expired()` (`RV-002`). | Closes Cycle 4 `RV-001`, `RV-002` and Cycle 5 `PC-001` while keeping `PortabilityTests` green. | Passed (`ruff`, `mypy`, `git diff --check`) | Conformant |
| `P01-T02` | src/api/tests/test_chat_panel.py, src/core/tests/test_chat_privacy.py | Added deterministic assertions for HTTP `403` + uncalled `Assistants.invoke` + unchanged thread messages on `/proposals` under invalid region/DPIA env, and verified `memory_status`/`prompt_memory`/`purge_expired` across `MemoryStore` and `SqlStore`. | `108` core tests, `122` API tests, and `25` rename tests pass. | Passed | Conformant |

## Implementation-Time Plan and Detail Update Assessment

* No implementation-time plan amendments or divergences occurred in Cycle 5.

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` from `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c5-plan-critique.md` (`memory_status` and `prompt_memory` failing closed when `not decision()["approved"]`) was applied directly to `P01-T01` and `P01-T02` and verified across `test_chat_privacy.py` and `test_chat_memory.py`.
* Material revisions: None.
* Dependent-work pause assessment: None required.
* Justification assessment: All planned and critiqued items are cleanly implemented and verified.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Named human DPO and Legal review and sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` | Reserved to named human DPO and Legal owners under Issue #163 criterion 2 and repository regulatory rules. | Owner: Named human DPO and Legal | Open distinct governance follow-up (`Refs #163`). |
| Align `infra/main.bicep` `chatModelSku` default and inject `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` in `infra/modules/containerapps.bicep` | Modifies `infra/`, which requires the Full RPI gate (`tools/rpi-checks.py --all`) explicitly excluded by caller's Focused validation tier. | Separate Full-tier IaC PR after DPO/Legal `D6` confirmation | Open distinct infrastructure follow-up. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

* None (`0` findings across Critical, High, Medium, and Low).

## Defects

* None.

## Routed Findings

* None in active engineering scope; see distinct follow-up items above.

## Residual Work

* Named human DPO and Legal review and sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` (`Refs #163` criterion 2).
* Separate Full-tier IaC PR aligning `infra/main.bicep` `chatModelSku` and `infra/modules/containerapps.bicep` env wiring after DPO/Legal `D6` review.

## Blockers and Remaining Work

* Blockers: Issue #163 criterion 2 (`Lawful basis, staff notice and a DPIA decision are recorded by the DPO and Legal; no retention period is set before approval`) remains intentionally gated on named human DPO and Legal approval (`DPO_LEGAL_APPROVED = False`).
* Remaining in-scope engineering work: None.

## Validation Assessment

* Validation run:
  * `cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy` -> `0` issues (`310` formatted, `363` typechecked).
  * `cd src/api && python3 -m ruff check && python3 -m ruff format --check && PYTHONPATH=../core/src:../agents/src python3 -m mypy` -> `0` issues (`216` formatted, `300` typechecked).
  * `src/core` targeted privacy/provider/memory/DPIA/regulatory suites -> `108` tests `OK`.
  * `src/api` `test_chat_panel.py`, `test_content_standard.py`, `test_accessibility_baseline.py` -> `122` tests `OK (skipped=1)`.
  * `python3 tools/rename-zava-tests.py` -> `25` tests `OK`.
  * `git --no-pager diff --check` -> exit code `0`.
* Skipped or unavailable checks: `tools/rpi-checks.py --all` skipped per caller instruction (`Validation tier: Focused`); hosted CI unobserved locally because caller instructed not to push or open a PR.
* Validation gaps: None within Focused local scope.

## Outcome

* Outcome: Conformant
* Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low
* Rationale: Every Issue #163 engineering objective and every finding across Cycles 1–5 (`chat_provider_position.py`, `chat_privacy.py`, `regulatory_privacy.py`, `server.py`, canonical privacy/DPIA and `src/core` documentation, and deterministic unit suites) is implemented, verified, and free of open defects while keeping human DPO/Legal sign-off (`D1`–`D8`) strictly gated.
* Next recommended RPI stage or follow-up: Transition Cycle 5 to `Follow-up` (`completed`), commit all changes and `.copilot-tracking/` artifacts cleanly on `feat/chat-163-privacy-region` (`Refs #163`) without pushing or opening a PR, and present ranked post-Review follow-ups.
