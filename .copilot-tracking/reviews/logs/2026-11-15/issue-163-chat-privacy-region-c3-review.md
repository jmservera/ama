<!-- markdownlint-disable-file -->
# Review: Issue #163 Actual-Mode Provider Gate, Expiry Hold, and Retention Bound Hardening (Cycle 3)

## Scope and Evidence

* Task ID: issue-163-chat-privacy-region-c3
* Parent Task ID: issue-163-chat-privacy-region-c2
* Review date: 2026-11-15
* Review scope: Full Cycle 3 task (`P01`)
* Assessed boundary: Cycle 3 remediation of Cycle 2 findings `RV-001` through `RV-003` across `chat_provider_position.py`, `chat_privacy.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `src/core/tests/test_chat_provider_position.py`, and `src/core/tests/test_chat_privacy.py`, plus end-to-end Issue #163 branch diff against `HEAD` (`04e5da42e`).
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c3-changes.md
* Other evidence considered: .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c2-review.md; .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md; `infra/main.bicep` (`chatModelSku = 'GlobalStandard'`); `infra/modules/containerapps.bicep`; `git diff HEAD`; independent read-only review lens (`rubber-duck`).

## Opening Review State

* Interpreted review goal: Verify that Cycle 3 closes Cycle 2 findings `RV-001` through `RV-003` cleanly and check the complete Issue #163 contract for any remaining fail-open assumptions before freezing the local `Refs #163` commit.
* Review scope: Full Cycle 3 task (`P01`)
* Evidence readiness: Cycle 3 plan, phase details, `Pass` plan critique, reconciled changes record, and Cycle 1/2 artifacts are present and current.
* Acceptance basis: Cycle 3 requirements, acceptance criteria, `Pass` critique, and `980+` focused unit tests plus `ruff`, `mypy`, and `git diff --check`.
* First comparison boundary: Compare `P01-T01` and `P01-T02` changes against Cycle 2 `RV-001`–`RV-003` and deployed infrastructure defaults without mutating source, test, doc, or prior RPI artifacts.
* Active read-only boundaries: Write authority limited strictly to `.copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c3-review.md` (and parent RPI session state JSON on transition).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only post-implementation review on 2026-11-15 across Cycle 3 `P01` and the full Issue #163 diff (`HEAD` `04e5da42e`), combining direct verification with an independent read-only `rubber-duck` lens. Confirmed all three Cycle 2 findings (`RV-001` through `RV-003`) are closed and tested, while the independent lens surfaced one cross-boundary hardening finding (`RV-001` Medium): `evaluate_provider_position()` defaults omitted `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` to `"uksouth"` and `"Standard"` even in `ZF_DATA_PROCESSING=actual` and without recording whether deployment settings were explicitly attested, whereas `infra/main.bicep` currently defaults `chatModelSku = 'GlobalStandard'` and `infra/modules/containerapps.bicep` does not inject `CHAT_PROVIDER_REGION` or `CHAT_DEPLOYMENT_TYPE`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Actual-Mode Provider Gate, Expiry Hold, Digit-Length Bound, and Regression Assertions | Reconciled for Cycle 2 `RV-001`–`RV-003`; 1 cross-boundary gap (`RV-001`) | Cycle 2 `RV-001`, `RV-002`, and `RV-003` are completely closed and verified, while `evaluate_provider_position` still silently defaults omitted `CHAT_PROVIDER_REGION` / `CHAT_DEPLOYMENT_TYPE` in `ZF_DATA_PROCESSING=actual` instead of requiring explicit deployment attestation (`RV-001`). |
| `Follow-Up Items` | Named human DPO and Legal sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` | Reconciled | Preserved outside engineering `Pxx` scope under `Refs #163`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/core/src/zava_forward/core/chat_provider_position.py, src/core/src/zava_forward/core/chat_privacy.py, src/core/README.md, docs/reference/research/chat-memory-dpia.md | Added `"actual_mode_dpo_legal_unapproved"` in `evaluate_provider_position()`, gated `ChatPrivacy.purge_expired()` on `retention_days`, and bounded `1 <= len(days) <= 5` before `int(days)`. | Closes Cycle 2 `RV-001`–`RV-003`; leaves omitted-env unattested deployment default in `actual` mode (`RV-001`). | Passed (`ruff`, `mypy`, `git diff --check`) | Defect `RV-001` on unattested defaults |
| `P01-T02` | src/core/tests/test_chat_provider_position.py, src/core/tests/test_chat_privacy.py | Added regression assertions for actual-mode provider/Foundry gates, `purge_expired()` hold, and `"9" * 5000` retention days. | Deterministic unit coverage within locked `13`-method bound. | Passed (`207` + `80` core, `525` + `122` API, `124` agents, `25` rename tests) | Conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` formatting (`chat_provider_position.py`) | Formatted `transfer_ref_recorded` on one line per `ruff format --check`. | `ruff format --check` output during `P01-T02`. | Recorded under Discoveries in `c3-changes.md`. | Not needed. | Justified and reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Cycle 3 critique `.copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan-critique.md` returned `Verdict: Pass` (`0` findings).
* Material revisions: None.
* Dependent-work pause assessment: None required.
* Justification assessment: `RV-001` below is a surgical `src/core` + `docs/reference/` hardening (`rpi-implement` / Cycle 4) that preserves synthetic `constructed`-mode fixtures (`#891` / `#281`) while failing closed on omitted `CHAT_PROVIDER_REGION` / `CHAT_DEPLOYMENT_TYPE` in `ZF_DATA_PROCESSING=actual` and surfacing `deployment_attested: False` whenever defaults are used; `infra/main.bicep` `chatModelSku` alignment is routed separately as a Full-tier IaC follow-up outside Issue #163 Focused scope.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Obtain named DPO and Legal sign-off on decisions `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention | Reserved to named human DPO and Legal owners under Issue #163 criterion 2. | Owner: Named human DPO and Legal | Open distinct governance follow-up (`Refs #163`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: `evaluate_provider_position` silently defaults omitted `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` to `uksouth` / `Standard` in `actual` mode and lacks an explicit deployment-attestation flag despite `infra/main.bicep` defaulting `chatModelSku` to `GlobalStandard`

* Related scope: `P01-T01`, `P01-T02`
* Evidence: `infra/main.bicep` (`param chatModelSku string = 'GlobalStandard'`) and `infra/main.bicepparam` / `infra/main.pilot.example.bicepparam` currently default Foundry model deployments to `GlobalStandard`, and `infra/modules/containerapps.bicep` does not inject `CHAT_PROVIDER_REGION` or `CHAT_DEPLOYMENT_TYPE` into the API container environment. Meanwhile, `evaluate_provider_position()` in `src/core/src/zava_forward/core/chat_provider_position.py` falls back to `PRIMARY_REGION` (`"uksouth"`) and `"Standard"` whenever those variables/arguments are omitted, even when `ZF_DATA_PROCESSING="actual"`, and does not expose a `deployment_attested` boolean distinguishing explicit deployment attestation from synthetic/constructed defaults.
* Impact: While `constructed` mode (`ZF_DATA_PROCESSING` unset) intentionally defaults to `uksouth` / `Standard` for synthetic unit fixtures (`#281`) and the owner-approved synthetic demo (`#891`), silently defaulting omitted `CHAT_PROVIDER_REGION` / `CHAT_DEPLOYMENT_TYPE` in `ZF_DATA_PROCESSING="actual"` would allow a future `DPO_LEGAL_APPROVED = True` flip to pass provider checks on an unattested `GlobalStandard` container deployment unless explicit `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` settings are required in `actual` mode and `deployment_attested` is surfaced in all modes. (Changing `infra/main.bicep` / `containerapps.bicep` itself belongs to a separate Full-tier IaC change outside Issue #163's Focused `src/core` + `docs/reference/` boundary.)
* Destination: `rpi-implement`
* Smallest useful next action: In `evaluate_provider_position()`, expose `deployment_attested: bool` (`True` only when both region and deployment type are explicitly supplied via non-empty env or keyword args), require explicit `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` when `is_actual` is `True` (appending `"unattested_region_in_actual_mode"` / `"unattested_deployment_in_actual_mode"` when omitted while preserving `constructed`-mode synthetic defaults), document the `infra/main.bicep` `chatModelSku = 'GlobalStandard'` discrepancy in `docs/reference/research/chat-memory-dpia.md` and `src/core/README.md`, and add unit assertions.

## Validation Assessment

* Executed checks:
  * `src/core`: `ruff check`, `ruff format --check` (`310` files), `mypy` (`363` files), `test_*chat*.py` (`207` tests), `test_*privacy*.py` (`80` tests, `skipped=1`) — all `0` failures.
  * `src/api`: `ruff check`, `ruff format --check` (`216` files), `mypy` (`300` files), `test_*chat*.py` (`525` tests, `skipped=1`), `test_chat_panel.py` + `test_content_standard.py` + `test_accessibility_baseline.py` (`122` tests, `skipped=1`) — all `0` failures.
  * `src/agents`: `test_*chat*.py` (`124` tests) and `tools/rename-zava-tests.py` (`25` tests) — `0` failures.
  * `git --no-pager diff --check`: exit code `0`.
* Missing or skipped checks: `tools/rpi-checks.py --all` intentionally skipped per Focused validation instruction.
* Sufficiency for verdict: Sufficient for `Execution status: Complete` and `Outcome: Defects found`.

## Outcome

* Outcome: Defects found
* Rationale: Cycle 3 resolved all three Cycle 2 findings (`RV-001`–`RV-003`), and independent cross-boundary review against `infra/main.bicep` (`chatModelSku = 'GlobalStandard'`) identified one remaining fail-closed hardening item (`RV-001` Medium) inside `chat_provider_position.py` + `docs/reference/research/chat-memory-dpia.md` before final commit.
* Severity summary: 0 Critical, 0 High, 1 Medium (`RV-001`), 0 Low.
* Actionable counts by destination: `1` routed to `rpi-implement` (`RV-001`); `2` distinct open follow-ups outside Focused `#163` engineering scope (human DPO/Legal `D1`–`D8` sign-off; Full-tier IaC `infra/main.bicep` / `containerapps.bicep` `chatModelSku` and `CHAT_PROVIDER_REGION` / `CHAT_DEPLOYMENT_TYPE` wiring).

## Recommended Next Stage

* Primary destination: `rpi-implement` (via bounded automatic Cycle 4 task `issue-163-chat-privacy-region-c4` under `#1798` correction-cycle grant, cycle 4 of `<= 5`).
* Open follow-up items outside active scope:
  1. Named human DPO and Legal review and sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` (`Refs #163`).
  2. Separate Full-tier infrastructure PR updating `infra/main.bicep` (`chatModelSku` default from `GlobalStandard` to `Standard` once DPO/Legal confirm `D6`) and injecting `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` in `infra/modules/containerapps.bicep`.
