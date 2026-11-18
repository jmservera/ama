<!-- markdownlint-disable-file -->

# Task Research: issue-163-chat-privacy-region

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (RPI Agent automatic loop)                                             |
| Status             | In progress                                                                         |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md     |

## Research Brief

* What to research: Existing chat and memory privacy, data-map, retention, and DPIA modules in `src/core` (`chat_privacy.py`, `regulatory_privacy.py`, and callers in `src/agents` / `src/api` / `infra`) plus canonical privacy reference documentation under `docs/reference/` and upstream BRD/PRD/ADR contracts for Issue #163 criterion 5 ("Model provider data handling and region position is recorded").
* Why it matters: Issue #163 requires recording and enforcing the model provider data-handling and region position contract (Azure OpenAI / Foundry UK South / EU data-zone residency posture, zero model training on customer prompts/completions, abuse-monitoring/content-filtering data handling disclosure, cross-border transfer prohibition without DPO/Legal sign-off, and no active retention period before DPO/Legal approval) while keeping DPO/Legal human approval explicitly gated.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases for Issue #163 on branch `feat/chat-163-privacy-region`.
* Scope: `src/core` privacy modules and tests, `src/api` / `src/agents` / `infra` consumers where relevant, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, `docs/reference/log.md`, and upstream BRD/PRD/ADR references.
* Non-goals: Simulating or fabricating human DPO/Legal sign-off for lawful basis, staff notice, DPIA decision, or live retention periods; running `tools/rpi-checks.py --all`; pushing to remote or opening a PR.
* Criteria: Answer all sub-questions with line-anchored `C#` evidence, verify existing provider-terms documentation and code contracts, evaluate alternatives for fail-closed region/training/transfer/retention validation, and establish convergence recommendation for `rpi-plan`.
* Requested outputs: Dated primary research artifact with three-wave cycle log, evidence table, convergence recommendation, and Planning Readiness evaluation.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                                       |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How do `src/core` and `docs/reference/` currently model chat/memory privacy, provider data handling, region residency, transfer gates, and pre-approval retention blocking? |
| Codebase scope                   | `src/core/`, `src/agents/`, `src/api/`, `infra/`, `docs/`                                                                                                                   |
| External scope                   | none (repository-contained specification, regulatory snapshots, and recorded vendor documentation posture unless an unresolved gap requires verification)                   |
| Initial internal candidate areas | `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/src/zava_forward/core/regulatory_privacy.py`, `src/core/tests/test_chat_privacy.py`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/research/chat-demo-storage-approval-2026-11-01.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/adrs/0004-per-user-agent-chat-and-memory.md` |
| Initial external candidate areas | none                                                                                                                                                                        |
| Research posture                 | balanced                                                                                                                                                                    |
| Posture provenance               | default (bounded engineering slice with named target modules plus adjacent `src/api`/`src/agents`/`infra` consumer verification)                                            |
| Explicit limits / deadline       | Focused validation tier (`src/core` / `src/api` unit tests, `ruff`, `mypy`); do not run `tools/rpi-checks.py --all`; do not push or open PR                                 |
| Posture-specific completion basis| balanced scope coverage and adequate evidence across `src/core`, adjacent consumers, and `docs/reference/`                                                                  |
| Edits allowed during research?   | no, research-only                                                                                                                                                           |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                                        |
| Known constraints / excluded sources | Keep human DPO/Legal criterion 2 unticked and unapproved; do not read private datasets; preserve existing callers and focused test compatibility                        |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                                | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|---------------------------------------|---------------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches workspace files and `.copilot-tracking/`    | Repository documentation, privacy/legal boundaries, KB log/index, focused tier   | Selected: governs legal/DPIA human gate, KB updates, and validation rules                 |
| Skill               | `privacy-standards`                   | Plugin skill matching UK GDPR / DPIA / data-handling domain         | Advisory privacy control taxonomy only; cannot override repo contracts           | Skipped: repository already defines bespoke UK GDPR / DPIA / ADR 0002 & 0004 schemas      |
| Skill               | `python-foundational`                 | Plugin skill for Python typing/linting conventions                  | Advisory Python style only                                                       | Skipped: local `src/core` module patterns, `ruff`, and `mypy` config are directly visible |
| Research specialist | `hve-core-all:rpi-researcher`         | Host-registered general research subagent                           | Bounded delegated lane artifact under `.copilot-tracking/research/subagents/`    | Skipped (inline): tightly coupled 5-8 file inspection across `src/core` and `docs/`       |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                                    |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with complete caller objectives, target modules, validation tier, and human-gate rules     | Not applicable       | Proceed in confirmed automatic loop with `balanced` posture and `convergence` output mode          |
| Direction change | Pending cycle execution                                                                                                | Not applicable       | None yet                                                                                           |
| Convergence      | Pending cycle synthesis                                                                                                | Not applicable       | None yet                                                                                           |

## Scope and Success Criteria

* Scope: `src/core` chat/regulatory privacy contracts and unit tests, consumer touchpoints in `src/agents` / `src/api` / `infra`, and canonical reference documentation (`docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, `docs/reference/log.md`, plus upstream BRD/PRD/ADR alignment).
* Assumptions:
  * `chat_privacy.py` and/or `regulatory_privacy.py` already implement parts of Issue #163 (data map, DSR locate/delete, diagnostic log & performance exclusion, special-category warnings/redaction) and may partially or not yet encode model provider data handling and region position.
  * `docs/reference/research/chat-memory-dpia.md` already has a 2026-11-01 vendor-terms note that needs checking against exact contract enforcement and all five elements specified in Objective 2.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Research existing chat/memory privacy, data-map, and DPIA modules in `src/core` (`regulatory_privacy.py`, `chat_privacy.py`, or related modules) and `docs/reference/`.
  2. Determine how to record and enforce the model provider data-handling and region position contract (Azure OpenAI / Foundry UK South / EU data-zone residency posture, zero model training on customer prompts/completions, abuse-monitoring/content-filtering data handling disclosure, cross-border transfer prohibition without DPO/Legal sign-off, and no retention period active before DPO/Legal approval) in both `src/core` and the canonical privacy reference documentation.
  3. Identify deterministic unit test coverage needed in `src/core/tests/` verifying exposure, validation, fail-closed rejection on unapproved regions or provider training flags, and preservation of the DPO/Legal human gate.
* Inferred research questions:
  * How do `src/api`, `src/agents`, or `infra` interact with `chat_privacy.py` and `regulatory_privacy.py`, and how does the synthetic-data demo storage approval (`chat-demo-storage-approval-2026-11-01.md`) coexist with the production DPO/Legal gate?
  * Do any existing tests in `src/api/tests/test_content_standard.py` or `src/core/tests/` constrain wording, exports, or schemas in `chat_privacy.py` or `docs/reference/`?
* Caller constraints and non-goals: Focused validation tier only; do not run `tools/rpi-checks.py --all`; keep human DPO/Legal criterion unticked; commit locally with Copilot trailer; do not push or open PR.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                     |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------------------|
| narrow                                                   | Focused validation (`src/core` / `src/api` unit tests, `ruff`, `mypy`); exclude `tools/rpi-checks.py --all` | Caller intake       | Constrains implementation/review verification commands                                |
| exclude                                                  | Keep criterion 2 (DPO/Legal lawful basis, staff notice, DPIA decision, retention approval) unticked     | Caller intake       | Prevents treating engineering contract as human legal sign-off                        |
| exclude                                                  | Do not push branch or open PR                                                                           | Caller intake       | Final git state stops at clean local commit on `feat/chat-163-privacy-region`         |

## Research Questions

|  # | Sub-question                                                                                                                                              | Type            | Priority | Status |
|---:|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|--------|
| Q1 | What privacy, data-map, retention, and DPIA structures already exist in `chat_privacy.py`, `regulatory_privacy.py`, and related `src/core` modules?       | depth           | H        | answered |
| Q2 | How do `docs/reference/research/chat-memory-dpia.md`, `chat-demo-storage-approval-2026-11-01.md`, BRD, PRD, and ADRs 0002/0004 specify provider region and data handling? | depth | H | answered |
| Q3 | How do consumers in `src/agents`, `src/api`, and `infra` read or enforce chat/model privacy, region, and demo-vs-live DPIA/retention gates?               | breadth         | H        | answered |
| Q4 | What gaps or edge cases exist in recording and enforcing the 5 provider/region/retention invariants fail-closed without breaking demo-mode fixtures or tests? | depth       | H        | answered |
| Q5 | Which unit tests, linters, type checks, and KB index/log updates are required to validate and document the change cleanly?                                | straightforward | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/regulatory/README.md`, GitHub Issue #163 body.
* Reused (verified) findings: Issue #163 has 4 of 6 criteria ticked and 2 unticked: criterion 2 (DPO/Legal human gate) and criterion 5 ("Model provider data handling and region position is recorded"). `docs/reference/README.md` line 1083 notes that `docs/reference/research/chat-memory-dpia.md` had provider terms documented 2026-11-01 as vendor documentation (not DPO-accepted), while `chat-demo-storage-approval-2026-11-01.md` states `#163 criteria 2 and 5 stay deferred`.
* Superseded / stale: None; codebase and reference inspection confirmed exact line-level gaps.

## Research Cycles

### Cycle 1

#### Wave 1 — Wider (Inline)

* Fallback / inline disposition: Tightly coupled internal repository inspection executed inline across `src/core`, `src/agents`, `src/api`, `infra`, and `docs/`.
* Breadth findings:
  * `src/core/src/zava_forward/core/chat_privacy.py` defines `DATA_MAP`, `MODEL_PROVIDER_POSITION`, `ChatNotApproved`, and `ChatPrivacy` (`C1`, `C2`).
  * `src/core/src/zava_forward/core/regulatory_privacy.py` defines strictly typed retention review (`retention_alignment`, `retention_report`), DPIA readiness (`GATE_REFS`, `CRITERIA`, `readiness_report`), and Foundry query minimisation (`build_foundry_query`) (`C3`, `C4`).
  * `src/core/src/zava_forward/core/data_protection.py` defines `actual_mode(env)` (`ZF_DATA_PROCESSING == "actual"`) and `is_synthetic_ref(value)` (`SYNTH-` prefix detection) (`C5`).
  * `src/api/src/zava_forward/api/server.py` exposes `/api/chat/status` returning `warning`, `retention`, `storage_approved`, `activation`, `demo_activation`, `demo_disclaimer`, and `limits` (`C6`).
  * `docs/reference/research/chat-memory-dpia.md`, `docs/adrs/0004-per-user-agent-chat-and-memory.md`, `infra/main.bicep`, `infra/resident-assistant.bicep`, and `infra/README.md` establish the `uksouth` primary residency boundary and `swedencentral` / `DataZoneStandard` EU data-zone boundary (`C7`, `C8`, `C9`, `C10`).

#### Wave 2 — Deeper (Inline)

* Detailed contract and gap findings:
  * Passive provider dictionary: `MODEL_PROVIDER_POSITION` in `chat_privacy.py:82-95` is only a static unvalidated dictionary with string fields (`provider`, `region`, `zava_stores_prompts`, `foundry_agent_memory`, `documented_terms`, `open_items`) (`C1`). Neither `chat_privacy.py` nor `regulatory_privacy.py` validates or enforces:
    1. Approved residency posture (`uksouth` domestic UK residency with `Standard` regional deployment vs `EU_DATA_ZONE` EEA regions / `DataZoneStandard` vs rejected `GlobalStandard` or non-UK/non-EU regions like `eastus`/`westus`).
    2. Zero model training on customer prompts, completions, and memory (`customer_data_training=False`; fail closed if any provider training flag is enabled).
    3. Structured abuse-monitoring and synchronous content-filtering disclosure (`Azure AI Content Safety` synchronous prompt/completion harm filtering vs default 30-day flagged-sample storage and human review unless Microsoft approves modified abuse monitoring, plus the EEA-only documented reviewer location guarantee vs unverified UK South reviewer location).
    4. Cross-border transfer prohibition without explicit DPO/Legal transfer sign-off (`CHAT_TRANSFER_REF`; required before any processing outside `uksouth`, including EU data-zone regions or `DataZoneStandard`, and rejecting `SYNTH-` or demo references in `actual` personal-data mode).
  * Pre-approval retention gap: In `chat_privacy.py:125-134`, `ChatPrivacy.decision()` computes `retention_set = bool(self._ref("CHAT_RETENTION_REF")) and days.isdigit() and int(days) > 0` independently of `approved = not missing` (`C2`). Consequently, if `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS` are present while `CHAT_DPIA_REF`, `CHAT_LAWFUL_BASIS_REF`, or `CHAT_NOTICE_REF` is missing (or when `SYNTH-` / demo refs are supplied under `ZF_DATA_PROCESSING="actual"`), `decision()["retention_days"]` currently becomes active before DPO/Legal approval, and `days.isdigit()` without `days.isascii()` accepts non-ASCII digits such as `"\u00b2"`.
  * Reference documentation gap: `docs/reference/research/chat-memory-dpia.md:103-131` (`## Model provider and region`) describes vendor terms narratively from the 2026-11-01 snapshot (`C7`), without recording the structured machine-enforced residency matrix (`uksouth` `Standard` domestic posture vs EU data-zone `DataZoneStandard`/EEA posture vs prohibited `GlobalStandard`/third-country regions), the runtime environment contract (`CHAT_PROVIDER_REGION`, `CHAT_DEPLOYMENT_TYPE`, `CHAT_PROVIDER_TRAINING`, `CHAT_CROSS_BORDER_TRANSFER`, `CHAT_TRANSFER_REF`, `CHAT_ABUSE_MONITORING_MODIFIED_REF`), or the pre-approval retention hard gate.

#### Wave 3 — Contrarian (Inline)

* Counter-evidence, invariants, and regression traps verified:
  * Legacy typing/formatting exclusions trap: `src/core/pyproject.toml:32-119` excludes `chat_privacy.py` and `test_chat_privacy.py` from `ruff format` and sets `mypy` `ignore_errors = true` on `zava_forward.core.chat_privacy` and `tests.test_chat_privacy` (`C11`). Placing new contract logic only in `chat_privacy.py` and `test_chat_privacy.py` would bypass `mypy` and `ruff format --check`. Creating a dedicated strictly typed, ruff-formatted module `src/core/src/zava_forward/core/chat_provider_position.py` (wired into `chat_privacy.py`, `regulatory_privacy.py`, and `/api/chat/status`) AND a dedicated strictly typed test file `src/core/tests/test_chat_provider_position.py` (alongside updates in `test_chat_privacy.py` and `test_chat_dpia_record.py`) ensures full strict `mypy` and `ruff format --check` enforcement.
  * SQL portability guard trap: `PortabilityTests.test_chat_privacy_has_no_own_sql_or_connection` in `src/core/tests/test_chat_privacy.py:213-224` scans `inspect.getsource(cp)` for SQL tokens (`INSERT OR`, `REPLACE INTO`, `AUTOINCREMENT`, `PRAGMA`, `sqlite3`, `CREATE TABLE`, `chat.sqlite`, `executescript`, `OBJECT_ID`, and `SELECT/DELETE FROM/INSERT INTO/UPDATE ... chat_`) (`C12`). `chat_privacy.py` must remain completely free of those tokens.
  * Backward-compatibility assertions in `test_chat_privacy.py:47-58` (`C13`):
    * `cp.MODEL_PROVIDER_POSITION["zava_stores_prompts"]` must remain `False`.
    * `"uksouth"` must remain in `cp.MODEL_PROVIDER_POSITION["region"]`.
    * `cp.MODEL_PROVIDER_POSITION["documented_terms"]["status"]` must remain `"vendor_documentation_not_dpo_accepted"`.
    * `cp.MODEL_PROVIDER_POSITION["documented_terms"]["source"]` must remain `"https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy"`.
    * `cp.MODEL_PROVIDER_POSITION["documented_terms"]["retrieved"]` must match `^\d{4}-\d{2}-\d{2}$`.
    * At least one item in `cp.MODEL_PROVIDER_POSITION["open_items"]` must contain `"DPO and Legal"`.
  * DPIA Markdown parser guard trap: `ChatDpiaRecordGuard` in `src/core/tests/test_chat_dpia_record.py:20-87` parses `docs/reference/research/chat-memory-dpia.md` (`C14`):
    * `## Data map` rows for `chat_message`, `chat_thread`, and `chat_memory` (and `cp.DATA_MAP` rows `message`, `thread`, `memory`) MUST keep retention cells starting with `"Unknown"`.
    * `## Decision pack for the DPO and Legal` MUST keep exact decision IDs `D1` through `D8`, each with `"Not recorded"` in the last column (no fabricated sign-off).
  * Plain-language content guard trap: `src/api/tests/test_content_standard.py:165-171` scans every `.py` file under `src/core/src/zava_forward/core/` and `src/api/src/zava_forward/api/` and fails if `"human-approved"` (except `"human-approved by"`) appears (`C15`).
  * Demo deployment profile vs `actual_mode` trap: `infra/modules/containerapps.bicep:236-246` sets `ZF_ENV=production` alongside `ZF_DEPLOYMENT_PROFILE=demo` and demo `CHAT_*_REF` pointers (`C16`). Live personal-data mode is gated specifically by `ZF_DATA_PROCESSING=actual` (`data_protection.actual_mode(env)`), NOT `ZF_ENV`. Using `actual_mode(env)` ensures synthetic demo deployments and existing unit tests (`APPROVED` with `SYNTH-*` refs) continue to work seamlessly while `ZF_DATA_PROCESSING=actual` rejects `SYNTH-*` and `chat-demo-storage-approval-*` / draft DPIA references fail-closed.

## Evidence Log

| ID  | Source (`path:line`)                                                      | Finding                                                                                                                                      |
| --- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| C1  | `src/core/src/zava_forward/core/chat_privacy.py:82-95`                    | `MODEL_PROVIDER_POSITION` is currently a static narrative dict with `vendor_documentation_not_dpo_accepted` and no active validator.         |
| C2  | `src/core/src/zava_forward/core/chat_privacy.py:125-145`                  | `ChatPrivacy.decision()` currently evaluates `retention_set` without requiring `approved` (`not missing`) or ASCII-only digits, and `_require()` does not validate provider/region posture. |
| C3  | `src/core/src/zava_forward/core/regulatory_privacy.py:45-185`             | Strictly typed retention simulation and DPIA readiness reporting (`GATE_REFS`, `CRITERIA`, `dpo_reviewed: False`).                           |
| C4  | `src/core/src/zava_forward/core/regulatory_privacy.py:345-415`            | `build_foundry_query` enforces query minimisation and special-category purpose hold before Foundry calls.                                    |
| C5  | `src/core/src/zava_forward/core/data_protection.py:72-80`                 | `is_synthetic_ref` (`SYNTH-`) and `actual_mode` (`ZF_DATA_PROCESSING == "actual"`) distinguish synthetic demo refs from live personal data.  |
| C6  | `src/api/src/zava_forward/api/server.py:1207-1222`                        | `/api/chat/status` surfaces `ChatPrivacy.decision()` warning, retention, and `storage_approved` to staff clients.                            |
| C7  | `docs/reference/research/chat-memory-dpia.md:103-162`                     | `## Model provider and region` and `## Decision pack for the DPO and Legal` (`D1`–`D8` all `Not recorded`).                                  |
| C8  | `docs/reference/research/chat-demo-storage-approval-2026-11-01.md:1-60`   | Synthetic demo storage record explicitly keeps Issue #163 criteria 2 and 5 deferred and forbids production reliance.                         |
| C9  | `infra/main.bicep:219-231`                                                | Primary platform location defaults to `uksouth` with `Standard` model deployments (`gpt-4.1-mini`, `gpt-4.1`).                               |
| C10 | `infra/resident-assistant.bicep:6-41`                                     | Dedicated synthetic resident assistant uses `swedencentral` (`Standard`), while `infra/README.md:1540` documents `DataZoneStandard` EU option. |
| C11 | `src/core/pyproject.toml:32-119`                                          | `chat_privacy.py` and `test_chat_privacy.py` are excluded from `ruff format` and `mypy`; new modules/tests are checked under strict `mypy`.  |
| C12 | `src/core/tests/test_chat_privacy.py:213-224`                             | `PortabilityTests` scans `chat_privacy.py` source to forbid embedded SQL keywords or `chat_` SQL statements.                                 |
| C13 | `src/core/tests/test_chat_privacy.py:47-71`                               | Asserts required keys/values in `MODEL_PROVIDER_POSITION` and `test_no_retention_period_before_approval` with `SYNTH-*` refs in synthetic mode. |
| C14 | `src/core/tests/test_chat_dpia_record.py:20-87`                           | Guards `chat-memory-dpia.md` data-map classes, `Unknown` retention prefix, and `D1`–`D8` `Not recorded` status.                              |
| C15 | `src/api/tests/test_content_standard.py:165-171`                          | Bans standalone `"human-approved"` phrasing across `src/core` and `src/api` Python modules.                                                  |
| C16 | `infra/modules/containerapps.bicep:236-246`                               | Container Apps demo sets `ZF_ENV=production` + `ZF_DEPLOYMENT_PROFILE=demo`; live personal-data gate must key off `ZF_DATA_PROCESSING=actual`. |

## Parent Synthesis and Convergence Recommendation

* Cycle re-entry evaluation: All five research questions (`Q1`–`Q5`) are answered with line-anchored codebase evidence (`C1`–`C16`), and the Contrarian wave surfaced six concrete compatibility/lint/type/guard constraints before planning. No further research cycle is needed.
* Selected approach (Accepted):
  1. Create a strictly typed, ruff-formatted module `src/core/src/zava_forward/core/chat_provider_position.py` defining the canonical model provider data-handling and region position contract (`PRIMARY_REGION = "uksouth"`, `EU_DATA_ZONE_REGIONS`, `APPROVED_DEPLOYMENT_TYPES = ("Standard", "DataZoneStandard")`, `ABUSE_MONITORING_DISCLOSURE`, `CONTENT_FILTERING_DISCLOSURE`, `MODEL_PROVIDER_CONTRACT`, `evaluate_provider_position(env=..., ...)`, and `require_provider_position(env=..., ...)`), and wire it into `chat_privacy.py` (`MODEL_PROVIDER_POSITION`, `ChatPrivacy.provider_position()`, `ChatPrivacy.decision()`, and `ChatPrivacy._require()`) as well as `regulatory_privacy.readiness_report()` and `/api/chat/status` (additive `provider_position` field).
  2. Enforce all five contract invariants fail-closed:
     * Residency posture: `uksouth` (`Standard`) is the domestic UK residency posture (`residency_zone="uk_south"`, `cross_border_transfer=False`). `EU_DATA_ZONE_REGIONS` (such as `swedencentral`, `westeurope`, `northeurope`, `francecentral`, `germanywestcentral`, `italynorth`, `polandcentral`, `spaincentral`) or `DataZoneStandard` classify as `residency_zone="eu_data_zone"` with `cross_border_transfer=True`. Any region outside `uksouth` + `EU_DATA_ZONE_REGIONS` (e.g. `eastus`, `westus`, empty/unknown) fails closed with `unapproved_region`; any global deployment SKU (e.g. `GlobalStandard`, `GlobalBatch`, `GlobalProvisionedManaged`) fails closed with `unapproved_deployment_residency`.
     * Zero model training: Customer prompts, completions, and opt-in memory are never used to train, fine-tune, or improve foundation models (`zero_model_training=True`, `customer_data_training=False`). Any truthy or non-disabled training flag (`CHAT_PROVIDER_TRAINING` or explicit `customer_data_training`) fails closed with `provider_training_prohibited`.
     * Abuse-monitoring and content-filtering disclosure: Structured disclosure records synchronous `Azure AI Content Safety` prompt/completion harm filtering (stateless, no training reuse) and platform-default abuse monitoring (up to 30-day encrypted flagged-prompt/completion retention and Microsoft human review unless modified abuse monitoring is approved and recorded via `CHAT_ABUSE_MONITORING_MODIFIED_REF`, explicitly noting that Microsoft documents EEA-only human-reviewer residency for EEA deployments while UK South reviewer location remains unverified pending DPO confirmation).
     * Cross-border transfer prohibition without DPO/Legal sign-off: Processing outside domestic `uksouth` `Standard` (including `eu_data_zone` regions, `DataZoneStandard`, or explicit `CHAT_CROSS_BORDER_TRANSFER`) fails closed with `cross_border_transfer_unapproved` unless `CHAT_TRANSFER_REF` is recorded (and in `ZF_DATA_PROCESSING=actual` mode, `SYNTH-*` or demo-approval references are rejected fail-closed as `synthetic_or_demo_ref_in_actual_mode`).
     * Pre-approval retention prohibition and preserved DPO/Legal human gate: `ChatPrivacy.decision()` activates `retention_days` ONLY when `approved` is `True` (all three of `CHAT_DPIA_REF`, `CHAT_LAWFUL_BASIS_REF`, and `CHAT_NOTICE_REF` are valid for the active processing mode, plus `provider_position["valid"]` is `True`), `CHAT_RETENTION_REF` is valid for the active mode, and `CHAT_RETENTION_DAYS` is a positive ASCII integer (`1..36500`). In `ZF_DATA_PROCESSING=actual` mode, `SYNTH-*` refs and demo-only markdown pointers (`chat-demo-storage-approval-*` or draft `chat-memory-dpia.md`) are rejected so synthetic/demo references can never unlock live personal-data storage, retention, or transfers. `dpo_legal_approved` / `dpo_reviewed` remains `False` and `documented_terms["status"]` remains `"vendor_documentation_not_dpo_accepted"`.
  3. Update `docs/reference/research/chat-memory-dpia.md` (`## Model provider and region`, `## Decision record`, `## Status record`, `ms.date: 2026-11-15`), `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` while preserving every `D1`–`D8` `"Not recorded"` entry and `Unknown` data-map retention prefix, and leaving Issue #163 criterion 2 unticked/human-gated.

## Alternatives Considered

| Alternative | Disposition | Rationale |
| --- | --- | --- |
| Selected: New strictly typed `chat_provider_position.py` integrated into `chat_privacy.py`, `regulatory_privacy.py`, and `/api/chat/status` | Accepted | Ensures strict `mypy` and `ruff format --check` run on the new contract (`C11`), preserves `chat_privacy.py` backward-compatible exports and SQL portability (`C12`, `C13`), and gives both `ChatPrivacy` and `regulatory_privacy.readiness_report` a single source of truth. |
| Put all new logic only inside `chat_privacy.py` and `test_chat_privacy.py` | Rejected | Both files are in `src/core/pyproject.toml` legacy exclusions for `ruff format` and `mypy` (`C11`), which would bypass strict type-checking and formatting verification on the new contract. |
| Treat `EU_DATA_ZONE_REGIONS` or `DataZoneStandard` as unconditional pass without `CHAT_TRANSFER_REF` | Rejected | Violates Objective 2 ("cross-border transfer prohibition without DPO/Legal sign-off") because transferring UK staff/resident data from the UK to EEA/EU data-zone regions is a cross-border transfer from Zava's `uksouth` primary boundary unless DPO/Legal sign-off is recorded. |
| Reject `SYNTH-*` references unconditionally in synthetic/default mode | Rejected | Would break existing unit tests (`test_chat_privacy.py`, `test_chat_memory.py`) and synthetic demo deployments (`C13`, `C16`). Instead, flag `synthetic_or_demo_refs=True` and `dpo_legal_approved=False` in all modes, and reject `SYNTH-*`/demo refs fail-closed when `ZF_DATA_PROCESSING=actual` (`C5`). |

## Decisions, Risks, and Readiness

* Confirmed decisions:
  * Issue #163 criterion 2 (`Lawful basis, staff notice and a DPIA decision are recorded by the DPO and Legal; no retention period is set before approval`) remains gated on human DPO/Legal sign-off; `D1`–`D8` in `chat-memory-dpia.md` stay `"Not recorded"`.
  * Focused validation tier applies (`src/core` and `src/api` unit tests, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`).
  * Commit locally on `feat/chat-163-privacy-region` with the `Co-authored-by` trailer; do not push or open a PR.
* Open risks / blockers:
  * Human DPO and Legal review (`D1`–`D8`) remains an explicit governance prerequisite before live pilot/production chat/memory enablement (non-blocking for recording and enforcing the engineering contract in Issue #163 criterion 5).
* Potential further research:
  * None required for Issue #163 criterion 5.
* Research disposition: `executed`
* Planning Readiness: `Ready`
