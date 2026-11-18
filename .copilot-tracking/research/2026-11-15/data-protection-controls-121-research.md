<!-- markdownlint-disable-file -->

# Task Research: data-protection-controls-121

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                             |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/data-protection-controls-121-research.md      |

## Research Brief

* What to research: Current implementation, callers, store contracts, PRD/BRD requirements, and knowledge-base documentation for Issue #121 (`Data protection, retention and rights controls`) centered on `src/core/src/zava_forward/core/data_protection.py`, `src/core/tests/test_data_protection.py`, `src/core/README.md`, and `docs/reference/research/chat-memory-dpia.md`.
* Why it matters: Issue #121 requires deterministic local engineering controls for whole-system RAI processing/retention inventory, task manifest necessity validation, intact-attachment derivative/necessity model-dispatch gating, and persisted store-backed/JSON-serializable rights-request workflow without claiming DPO/Legal approval or conflating local deletion with provider erasure.
* Audience or intended use: Planning (`rpi-plan` + `rpi-plan-critique`), implementation (`rpi-implement`), and review (`rpi-review`) in this RPI session, plus coordinator review on `feat/core-121-data-protection-controls`.
* Scope: `src/core/src/zava_forward/core/data_protection.py`, callers across `src/` (`ai.py`, `regulatory_privacy.py`, `store.py`, `api`, `agents`), `src/core/tests/test_data_protection.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md` (and verify whether `docs/reference/research/privacy/` exists or if `chat-memory-dpia.md` is the canonical KB page), `docs/reference/README.md`, `docs/reference/log.md`, and PRD/BRD references (`DH-001` to `DH-007`, `PR-001`, `PR-003`, `CON-003`, `RULE-022`, `NFR-003`).
* Non-goals: Adding a separate governance service, inventing legal conclusions or retention periods, claiming verified DPO/Legal sign-offs, modifying unrelated UI/infra slices, running full Docker/SQL/browser gates, or pushing/opening a PR.
* Criteria: Backward compatibility with existing callers (`ai.py`, `regulatory_privacy.py`, `api`), strict `mypy` compliance in `src/core`, `ruff` check/format cleanliness, complete coverage of all 4 objective areas and unit test proofs, and accurate KB synchronization.
* Requested outputs: Converged design recommendation and exact contract mapping for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                               |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How should `data_protection.py`, its tests, and KB docs be extended to satisfy all Issue #121 RAI processing, dispatch, and rights controls cleanly without breaking existing callers? |
| Codebase scope                   | `src/core/`, `src/api/`, `src/agents/`, `docs/prds/`, `docs/brds/`, `docs/adrs/`, `docs/reference/`                                 |
| External scope                   | none (all regulatory/PRD contracts are held locally in the repository)                                                              |
| Initial internal candidate areas | `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai.py`, `src/core/src/zava_forward/core/store.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md` |
| Initial external candidate areas | none                                                                                                                                |
| Research posture                 | focused                                                                                                                             |
| Posture provenance               | default (bounded internal engineering slice with named target files and explicit acceptance criteria)                               |
| Explicit limits / deadline       | Focused validation tier only; do not push or open PR; do not close #121 (`Refs #121`)                                               |
| Posture-specific completion basis| focused scope and materiality: all callers, schemas, persistence patterns, and doc targets verified with line-level evidence        |
| Edits allowed during research?   | no, research-only                                                                                                                   |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Preserve reference-only / non-approval posture (never claim DPO/Legal sign-off or provider erasure from local deletion)         |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches workspace and docs | Enforces KB conventions, Markdown style, legal/regulatory non-approval boundaries, focused tier rules | Selected: governs codebase and KB conventions |
| Skill               | `rpi-research`                   | Explicit caller invocation                        | Owns three-wave research artifact contract   | Selected: active phase skill   |
| Skill               | `privacy-standards`              | Domain match on data protection                   | Generic privacy reference                    | Skipped: repository PRD (`DH-001..DH-007`) and caller specification already define the exact UK GDPR / RAI contract |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered subagent                          | Independent lane evidence writer             | Skipped (inline fallback): tightly coupled bounded internal slice across <10 local files is faster and more exact inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Caller provided detailed target files, function contracts, doc targets, and validation commands in non-interactive Autopilot mode | No interaction required | Proceed with focused Cycle 1 inline investigation  |
| Direction change | Wave 1 found canonical KB DPIA page at `docs/reference/research/chat-memory-dpia.md` rather than `docs/reference/research/privacy/chat-memory-dpia-retention-163.md` (caller prompt explicitly permitted `(or a dedicated section)`) | Resolved from codebase evidence (`C8`, `C11`, `C12`) | Add dedicated dated `#121` section to `docs/reference/research/chat-memory-dpia.md`, update `docs/reference/README.md` index row, and append to `docs/reference/log.md` |
| Convergence      | Cycle 1 answered all research questions with high-confidence codebase evidence; no residual blockers for local slice | No interaction required | Mark Planning Readiness `Ready` and advance automatic RPI session to `rpi-plan` |

## Scope and Success Criteria

* Scope: `src/core/src/zava_forward/core/data_protection.py`, `src/core/tests/test_data_protection.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, and `docs/reference/log.md`. Read-only compatibility verification against `ai.py`, `ai_tasks.py`, `regulatory_privacy.py`, `api/server.py`, `test_chat_dpia_record.py`, and `test_regulatory_privacy.py`.
* Assumptions:
  * Verified: `data_protection.py` and `test_data_protection.py` are strictly typed under `mypy --strict` (`C9`).
  * Verified: Worktree test execution requires `PYTHONPATH=src/core/src:src/core/tests` so imports resolve to the current worktree rather than the shared editable installation in `/home/azureuser/source/ama` (`C13`).
  * Verified: Existing callers (`ai.py`, `ai_tasks.py`, `regulatory_privacy.py`, `api/server.py`) call `register_report`, `dispatch_hold`, and `document_model_hold` (`C3`, `C4`, `C5`, `C6`, `C7`).
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Whole-system RAI processing & retention inventory in `data_protection.py` separating `staff_identity`, `tenant_identity`, `review_record`, and `future_real_resident` from `fixture_resident` with explicit `subject_population`, `hosting_region_vs_inference_residency` (`uk_hosting_does_not_prove_uk_inference_residency: True`), and 9 actual data/processing classes including `provider_retained_copy`.
  2. Expand `TASKS` to cover `rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, and `case_brief` with `purpose`, `audience`, `permitted_fields`, `prohibited`, and `necessity`, enforcing that `user_permission_granted=True` never establishes necessity or bypasses checks.
  3. Enforce intact document/image model-dispatch control (`look_at_attachment` / `raw_document` in `model_dispatch` and `dispatch_attachment_to_model`) so `storage_permission_granted=True` never approves sending intact material to AI without `reviewed_redacted` (`redaction_reviewer_id` + `redaction_review_id`) or non-synthetic `scoped_necessity_ref` / `necessity_exception`.
  4. Add persisted store-backed / JSON-serializable rights-request workflow (`RightsRequestLedger`, `record_rights_request`, `answer_rights_request`, `rights_status`) with receipt timestamp, 1-month deadline, `locate`/`export`/`erase` action log, and `local_deleted` vs `provider_erasure_confirmed=False`.
  5. Sync `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, and `docs/reference/log.md`, and add comprehensive unit tests in `src/core/tests/test_data_protection.py`.
* Inferred research questions:
  * How do existing callers invoke `data_protection` functions, and what invariants do existing tests assert on `DATA_CLASSES`, `TASKS`, `register_report`, `model_dispatch`, `rights_status`, and `chat-memory-dpia.md`?
  * How does `Store` persist JSON state and audit events while keeping `data_protection.py` compatible with `mypy --strict`?
* Caller constraints and non-goals: Focused validation tier only; do not close `#121` (`Refs #121`); do not push or open a PR; do not invent legal conclusions, retention periods, or DPO/Legal approvals.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focused local engineering and KB slice on `feat/core-121-data-protection-controls`; no Docker/SQL/browser full gate, no push/PR | Caller prompt | Restricts implementation and validation to `src/core` and `docs/` |
| exclude                                                  | Never use closing keyword for `#121`; never claim verified DPO/Legal sign-off or provider erasure from local deletion | Caller prompt + Issue #121 (`C1`) | Enforces `dpo_reviewed=False` and `provider_erasure_confirmed=False` across code and docs |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status   |
|---:|------------------|------------------------------------------|-----------|----------|
| Q1 | What classes, fields, and report keys currently exist in `data_protection.py` and what do callers/tests assert? | depth | H | answered |
| Q2 | How should `TASKS`, `validate_task_payload`, `model_dispatch`, and `dispatch_attachment_to_model` extend existing contracts without breaking legacy callers? | depth | H | answered |
| Q3 | How should `RightsRequestLedger` support both `Store`-backed persistence and standalone JSON serialization under `mypy --strict`? | depth | H | answered |
| Q4 | Which documentation files and existing doc-guard tests (`test_chat_dpia_record.py`, `test_regulatory_privacy.py`) constrain KB updates? | breadth | H | answered |
| Q5 | How must local validation commands be invoked in this multi-worktree shared environment so they test worktree sources reliably? | straightforward | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `src/core/README.md`, `src/core/src/zava_forward/core/data_protection.py`, `src/core/tests/test_data_protection.py`.
* Reused (verified) findings:
  * `data_protection.py` already defines `DataClass`, 8 `DATA_CLASSES` (1 `constructed` + 7 `actual`), 3 regulatory `TASKS`, `validate_necessity_exception`, `model_dispatch`, `dispatch_hold`, `document_model_hold`, `validate_task_payload`, `due_date`, and in-memory `rights_status` (`C2`).
  * PRD `DH-001`..`DH-007` and Issue #121 RAI criteria require whole-system mapping, minimum-necessary task declarations, derivative/scoped-necessity gating on attachments, UK hosting vs inference residency distinction, and logged 1-month rights handling (`C1`, `C10`).
* Superseded / stale:
  * Caller prompt mentioned `docs/reference/research/privacy/chat-memory-dpia-retention-163.md (or a dedicated section)`; `docs/reference/research/privacy/` does not exist in the repo, whereas `docs/reference/research/chat-memory-dpia.md` is the active indexed KB record guarded by `test_chat_dpia_record.py` and `test_regulatory_privacy.py` (`C8`, `C11`, `C12`).

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier only; `Refs #121` non-closing link; no push/PR; strict non-approval / non-provider-erasure boundaries.
* Active research posture and completion basis: `focused`; all target modules, callers, store hooks, typechecker configs, and doc guard tests verified with line-level evidence.
* Explicit limits or deadline effect: Keeps scope tightly within `src/core` and `docs/reference` without touching `src/api` or `infra/`.

#### Wave 1: Wider

* Plan and independent lanes: Inline sweep of Issue #121 body, `data_protection.py` callers across `src/`, AI task names across `src/`, PRD `DH-001`..`DH-007`, and `docs/reference/` privacy files.
* Worker evidence relationships or inline fallback: Inline investigation mapped Q1..Q4 to `C1`..`C8` and `C10`. Found 16 files referencing `data_protection` across `src/core`, `src/api`, and `src/agents`, and located `docs/reference/research/chat-memory-dpia.md` as the canonical KB DPIA page.
* Reflection: `GET /api/data-protection` directly serializes `register_report(os.environ)`, so all additions to `register_report` must remain JSON-safe and never echo secret/reference values (`C6`). Need Wave 2 inspection of `pyproject.toml`, `ai.py`, `ai_registry.py`, `store.py`, and `chat-memory-dpia.md` sections.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Strict typing rules in `src/core/pyproject.toml`, exact call signatures in `ai.py` / `ai_tasks.py` / `regulatory_privacy.py`, `Store.save()` / `Store.audit()` mechanics in `store.py`, and `src/core/README.md` documentation of `#121`.
* Plan and independent lanes: Inline deep read of `pyproject.toml`, `ai.py`, `ai_registry.py`, `ai_tasks.py`, `store.py`, `src/core/README.md`, and `docs/reference/research/chat-memory-dpia.md`.
* Worker evidence relationships or inline fallback: Inline investigation mapped Q1..Q4 details to `C3`..`C9` and `C14`. Verified neither `data_protection` nor `test_data_protection` has mypy overrides, meaning both must pass `mypy --strict` (`C9`). Verified `Store` holds mutable `self.data: dict[str, Any]`, `self.lock: RLock`, `self.save()`, and `self.audit(who, action, case_id, detail)` (`C14`).
* Reflection: Need Wave 3 contrarian testing of baseline test runner behavior in the worktree, doc-guard tests against `chat-memory-dpia.md`, and backward-compatibility hazards in existing `test_data_protection.py` assertions.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether (a) requiring `redaction_reviewer_id` + `redaction_review_id` everywhere on `model_dispatch("raw_document", env, "reviewed_redacted")` would break existing tests, (b) editing `chat-memory-dpia.md` could break doc-guard tests, and (c) bare `python3 -m unittest` resolves the worktree package.
* Plan and independent lanes: Inline check of existing `test_data_protection.py` call sites, `test_chat_dpia_record.py`, `test_regulatory_privacy.py`, and baseline `mypy` + `unittest` execution.
* Worker evidence relationships or inline fallback:
  1. Contrarian finding 1 (`C2`, `C15`): Existing `test_data_protection.py` lines 85, 113, 343, and 477 call `model_dispatch("raw_document", env, "reviewed_redacted")` and `document_model_hold(..., derivative="reviewed_redacted")` under default `task="read_document"` without `redaction_reviewer_id`/`redaction_review_id`. Therefore `dispatch_attachment_to_model` (default `task="look_at_attachment"`) and `model_dispatch(..., task="look_at_attachment")` (plus any call passing reviewer/review args) must require both `redaction_reviewer_id` and `redaction_review_id` (or non-synthetic `scoped_necessity_ref` / `necessity_exception`), while preserving legacy 3-arg `model_dispatch("raw_document", env, "reviewed_redacted")` when `task="read_document"` and reviewer kwargs are omitted, AND existing `TASKS` tests check `spec["fields"]`, so each task entry should expose both `permitted_fields` and `fields`!
  2. Contrarian finding 2 (`C11`, `C12`): `test_chat_dpia_record.py` parses `## Data map` and `## Decision pack for the DPO and Legal` via regex up to the next `^## `, and `test_regulatory_privacy.py` asserts specific phrases in `chat-memory-dpia.md`. Appending a new `## Whole-System Processing, Derivative Dispatch and Rights-Request Controls (2026-11-15, Refs #121)` H2 section preserves every existing section intact!
  3. Contrarian finding 3 (`C13`): Bare `python3 -m unittest` without `PYTHONPATH=src/core/src:src/core/tests` imports `zava_forward.core` from the shared editable install in `/home/azureuser/source/ama/src/core/src` rather than this worktree! In a shared non-sandboxed environment we must NOT overwrite shared pip installs; instead we run `PYTHONPATH=src/core/src:src/core/tests` for unittest and `(cd src/core && python3 -m mypy)` (which uses `mypy_path = ["src", "tests"]` in `pyproject.toml`).
* Reflection: All three contrarian checks caught concrete regressions before a single line of code was written. No material gaps remain.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| Expand `DATA_CLASSES` to 10 entries (1 `constructed` `fixture_resident` + 9 `actual` classes adding `future_real_resident` and `provider_retained_copy`) with explicit `subject_population`, `processing_surfaces`, and `hosting_region_vs_inference_residency` in `register_report` | `C1`, `C2`, `C6`, `C10` | accepted | Satisfies both the 5 explicit `subject_population` values and all 9 actual data/processing classes while keeping `register_report` JSON-safe and backwards compatible | Selected recommendation (Part 1) |
| Expose both `permitted_fields` and `fields` on all 7+ whole-system `TASKS` and enforce `user_permission_granted` non-sufficiency in `validate_task_payload` and `model_dispatch` | `C2`, `C15` | accepted | Satisfies new `permitted_fields` manifest contract while preserving `TaskPayload.test_every_task_declares_purpose_necessity_prohibited` (`spec["fields"]`) | Selected recommendation (Part 2) |
| Implement `dispatch_attachment_to_model` and extend `model_dispatch` with `storage_permission_granted`, `redaction_reviewer_id`, `redaction_review_id`, and `scoped_necessity_ref` | `C2`, `C3`, `C4`, `C15` | accepted | Enforces strict reviewer+review ID or non-synthetic scoped necessity ref for `look_at_attachment` / attachment dispatch without breaking legacy `read_document` tests | Selected recommendation (Part 3) |
| Implement `RightsRequestLedger` using `Protocol`-typed store/JSON persistence plus `record_rights_request`, `answer_rights_request`, and polymorphic `rights_status` | `C2`, `C9`, `C14`, `C15` | accepted | Works with `Store` (`.data` + `.save()` + `.audit()`), JSON file paths, or plain dicts/lists under `mypy --strict`, keeping `local_deleted` strictly separate from `provider_erasure_confirmed=False` | Selected recommendation (Part 4) |
| Create new `docs/reference/research/privacy/chat-memory-dpia-retention-163.md` file | `C8`, `C11`, `C12` | rejected | KB placement rules require integrating into the existing canonical synthesis (`docs/reference/research/chat-memory-dpia.md`), and the caller explicitly allowed `(or a dedicated section)` | Documented as rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope is 100% covered with line-level codebase evidence and contrarian regression checks verified.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: inline: bounded tightly coupled single-package slice (`src/core` + `docs/reference`) investigated directly with exact `grep`/`view`/test probes.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`)           | Tool | Confidence | Notes |
|----|-----------------|----------------------------------|------|------------|-------|
| C1 | Issue #121 specifies whole-system RAI processing/retention criteria, separate mapping of staff/tenant/review/future-real-resident vs constructed fixtures, derivative/necessity dispatch control, UK hosting vs inference residency, and 1-month rights logging, while DPO/Legal sign-offs remain open | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:465` | bash (`gh issue view 121`) + grep | high | Confirms `Refs #121` non-closing posture |
| C2 | `data_protection.py` currently defines 8 `DATA_CLASSES`, 3 `TASKS` (`rule_lookup`, `check_explain`, `alert_triage`), `register_report`, `validate_necessity_exception`, `model_dispatch`, `dispatch_hold`, `document_model_hold`, `validate_task_payload`, `due_date`, and in-memory `rights_status` | `src/core/src/zava_forward/core/data_protection.py:29` | view | high | Primary implementation target |
| C3 | `Ai._request` and `Ai.run` call `data_protection.dispatch_hold("prompt_output", os.environ)` and `Ai.look_at` calls `data_protection.document_model_hold(...)` | `src/core/src/zava_forward/core/ai.py:174` | view | high | Existing callers must remain unbroken |
| C4 | `ai_tasks.run_document` calls `data_protection.document_model_hold(...)` | `src/core/src/zava_forward/core/ai_tasks.py:474` | view | high | Preserves `read_document` flow |
| C5 | `regulatory_privacy.check_special_category_purpose` calls `data_protection.dispatch_hold("tenant_identity", env)` | `src/core/src/zava_forward/core/regulatory_privacy.py:358` | view | high | `tenant_identity` must remain `actual` and `model_bound=True` |
| C6 | `GET /api/data-protection` returns `data_protection.register_report(os.environ)` and `test_ai_tasks.py` asserts `dpo_reviewed` is `False`, `any(c["kind"] == "actual" ...)`, and env ref values are never echoed | `src/api/src/zava_forward/api/server.py:1182` | grep + view | high | `register_report` must never echo reference strings |
| C7 | `src/core/README.md` section `### Data protection register and dispatch gate (#121)` currently states only 8 classes, 3 regulatory tasks, and no persisted rights log | `src/core/README.md:5040` | view | high | Needs update for `#121` engineering slice |
| C8 | `docs/reference/research/chat-memory-dpia.md` is the canonical indexed DPIA/privacy record in `docs/reference/README.md` | `docs/reference/README.md:1083` | grep + view | high | Target for dedicated `#121` KB section + index/log sync |
| C9 | `src/core/pyproject.toml` enforces `mypy` `strict = true` on `src` and `tests`, and neither `data_protection` nor `test_data_protection` is excluded | `src/core/pyproject.toml:32` | view | high | All new types, `Protocol`s, and tests must pass `mypy --strict` |
| C10 | PRD v0.16.0 RAI contract (`DH-001`..`DH-007`, `MAP-02`) states synthetic resident content does not remove actual staff/tenant identity processing from privacy scope and catalog/UK hosting is not UK inference residency | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1690` | view | high | Grounds `hosting_region_vs_inference_residency` |
| C11 | `test_chat_dpia_record.py` regex-parses `## Data map` and `## Decision pack for the DPO and Legal` in `chat-memory-dpia.md` and enforces `Not recorded` cells | `src/core/tests/test_chat_dpia_record.py:24` | view | high | Existing H2 sections in `chat-memory-dpia.md` must stay untouched |
| C12 | `test_regulatory_privacy.py` asserts retention class headings in `docs/reference/research/chat-memory-dpia.md` | `src/core/tests/test_regulatory_privacy.py:87` | grep | high | Append new H2 section cleanly without altering `#217` table terms |
| C13 | Running `unittest` without `PYTHONPATH=src/core/src:src/core/tests` imports `/home/azureuser/source/ama/src/core/src` instead of the current worktree | `src/core/tests/test_data_protection.py:12` | bash | high | Use `PYTHONPATH=src/core/src:src/core/tests` to keep worktree isolated |
| C14 | `Store` persists JSON state in `self.data: dict[str, Any]` via atomic `self.save()`, synchronizes via `self.lock`, and records metadata-only ledger entries via `self.audit(who, action, case_id, detail)` | `src/core/src/zava_forward/core/store.py:173` | view | high | Clean target for `Protocol`-typed `RightsRequestLedger` store adapter |
| C15 | `test_data_protection.py` asserts `spec["fields"]` on every `TASKS` entry, 3-arg `model_dispatch("raw_document", env, "reviewed_redacted")`, and `rights_status(rows, now)` on a `list[dict]` | `src/core/tests/test_data_protection.py:85` | view | high | Preserve backward-compatible signatures alongside stricter attachment/ledger APIs |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* KB path naming: Caller prompt wrote `docs/reference/research/privacy/chat-memory-dpia-retention-163.md (or a dedicated section)`, whereas the repository stores this record at `docs/reference/research/chat-memory-dpia.md` (`C8`, `C11`, `C12`); resolved by repository convention and the caller's explicit `(or a dedicated section)` clause -> add a dedicated dated section in `docs/reference/research/chat-memory-dpia.md`, update `docs/reference/README.md`, and append to `docs/reference/log.md`.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `DATA_CLASSES` has 8 classes (1 constructed + 7 actual). Adding `future_real_resident` and `provider_retained_copy` yields 1 constructed fixture class + 9 actual data/processing classes, mapped across the 5 `subject_population` values and 9 whole-system surfaces, plus `hosting_region_vs_inference_residency` with `uk_hosting_does_not_prove_uk_inference_residency: True`. | `C1`, `C2`, `C6`, `C10` | high | Ready for deterministic implementation in `data_protection.py` |
| Q2 | `TASKS` currently has 3 tasks; adding `agent_chat`, `look_at_attachment`, `intake_summary`, and `case_brief` (and keeping `fields` alongside `permitted_fields`) satisfies whole-system manifest coverage while `user_permission_granted=True` never establishes necessity or bypasses field/length/special-category/derivative checks. | `C2`, `C15` | high | Preserves existing tests while enforcing necessity boundary |
| Q3 | `dispatch_attachment_to_model` (and `model_dispatch` when `task="look_at_attachment"` or redaction metadata is passed) denies intact material even when `storage_permission_granted=True`, requiring `reviewed_redacted` (`redaction_reviewer_id` + `redaction_review_id`) or non-synthetic `scoped_necessity_ref` / `necessity_exception`. | `C2`, `C3`, `C4`, `C15` | high | Satisfies attachment dispatch gate with zero regression on legacy `read_document` tests |
| Q4 | `RightsRequestLedger` typed via structural `Protocol` can back onto a `Store` (`.data["rights_requests"]` + `.save()` + metadata-only `.audit()`), a JSON `Path`/`str`, or in-memory/dict state with `to_dict`/`to_json`/`from_json`, logging `locate`/`export`/`erase` actions and keeping `local_deleted` strictly separate from `provider_erasure_confirmed=False`. | `C2`, `C9`, `C14`, `C15` | high | Fully `mypy --strict` compliant and persisted across store/file reloads |
| Q5 | `docs/reference/research/chat-memory-dpia.md` has active guard tests (`test_chat_dpia_record.py`, `test_regulatory_privacy.py`), and worktree tests require `PYTHONPATH=src/core/src:src/core/tests`. | `C8`, `C11`, `C12`, `C13` | high | Append dedicated `#121` H2 section and run doc-guard tests alongside `test_data_protection.py` |

## Key Discoveries

* Adding `future_real_resident` and `provider_retained_copy` to `DATA_CLASSES` produces exact alignment between the 5 `subject_population` categories (`constructed_resident_fixture`, `current_staff_identity`, `current_tenant_identity`, `current_review_record`, `future_real_resident`) and all 9 actual data/processing classes (`staff_identity`, `tenant_identity`, `review_record`, `future_real_resident`, `raw_document`, `prompt_output`, `audit_ledger`, `telemetry`, `provider_retained_copy`) (`C1`, `C2`, `C10`).
* Neither `data_protection.py` nor `test_data_protection.py` is exempted from `mypy --strict` in `src/core/pyproject.toml`, so store-backed persistence in `RightsRequestLedger` should use a ` typing.Protocol` boundary rather than importing untyped `Store` directly (`C9`, `C14`).
* `test_chat_dpia_record.py` and `test_regulatory_privacy.py` guard existing sections of `docs/reference/research/chat-memory-dpia.md`, and running `unittest` in this worktree requires `PYTHONPATH=src/core/src:src/core/tests` (`C11`, `C12`, `C13`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Extend `src/core/src/zava_forward/core/data_protection.py` in-place (preserving module-level strict typing and backward compatibility for all existing callers) with:
  1. Expanded `DataClass` (`subject_population`, `processing_surfaces`), 10 `DATA_CLASSES` (1 `constructed` `fixture_resident` + 9 `actual` classes adding `future_real_resident` and `provider_retained_copy`), `HOSTING_VS_INFERENCE_RESIDENCY` (`uk_hosting_does_not_prove_uk_inference_residency: True`), and enriched `register_report(env)` exposing `subject_populations`, `hosting_region_vs_inference_residency`, and `whole_system_coverage` without echoing reference values.
  2. Expanded `TASKS` covering `rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, and `case_brief` (each declaring `purpose`, `audience`, `permitted_fields` and alias `fields`, `prohibited`, and `necessity`), with `validate_task_payload` and `model_dispatch` enforcing that `user_permission_granted=True` never establishes task necessity or bypasses field/type/length/special-category/derivative gates.
  3. Attachment dispatch control in `dispatch_attachment_to_model` and `model_dispatch`: `storage_permission_granted=True` never approves AI dispatch of intact material; require `derivative="reviewed_redacted"` with human non-synthetic `redaction_reviewer_id` and `redaction_review_id`, OR non-synthetic `scoped_necessity_ref` / `necessity_exception`, otherwise return `permitted=False` and `manual_path`.
  4. `RightsRequestLedger` + `record_rights_request`, `log_rights_action`, `answer_rights_request`, and polymorphic `rights_status` supporting `Store`-backed persistence (`.data["rights_requests"]` + `.save()` + metadata-only `.audit()`), atomic JSON file persistence, and `to_dict`/`to_json`/`from_json`, enforcing timezone-aware receipt timestamps, 1-calendar-month statutory deadlines, `locate`/`export`/`erase` action logs, and `local_deleted` vs `provider_erasure_confirmed=False` (rejecting any attempt to represent local deletion as confirmed provider erasure).
  5. Synchronized documentation in `src/core/README.md`, a dedicated dated `#121` section in `docs/reference/research/chat-memory-dpia.md`, updated `docs/reference/README.md` index entry, and appended `docs/reference/log.md` entry, backed by comprehensive unit tests in `src/core/tests/test_data_protection.py`.
* Rationale: Delivers every Issue #121 local engineering and RAI processing/retention requirement inside the existing module and `Store` contract without adding a separate governance service, weakening `mypy --strict`, or breaking any existing API/core/agents caller.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`, `C13`, `C14`, `C15`
* Implementation impact:
  * Modify `src/core/src/zava_forward/core/data_protection.py`
  * Modify `src/core/tests/test_data_protection.py`
  * Modify `src/core/README.md`
  * Modify `docs/reference/research/chat-memory-dpia.md`
  * Modify `docs/reference/README.md`
  * Modify `docs/reference/log.md`
* Confidence: high: all callers, type constraints, and doc-guard tests are directly verified in the workspace.

File tree:

```text
src/core/
  README.md                                      (modified)
  src/zava_forward/core/
    data_protection.py                           (modified)
  tests/
    test_data_protection.py                      (modified)
docs/reference/
  README.md                                      (modified)
  log.md                                         (modified)
  research/
    chat-memory-dpia.md                          (modified)
```

### Alternative: Separate SQLite DDL table for rights requests inside `data_protection.py`

* Approach: Open a separate SQLite connection and manage custom DDL inside `data_protection.py`.
* Trade-offs: Provides isolated SQL tables, but violates the Issue #121 RAI scope constraint ("Use the existing API, SQL state and bounded assistant runtime. Do not add a governance service") and parallels what `chat_privacy.py` explicitly avoids ("This module opens no connection and issues no DDL").
* Evidence refs: `C1`, `C2`, `C14`
* Rejection rationale: `Store`-backed (`store.data["rights_requests"]` + `store.save()` + `store.audit()`) and JSON-serializable persistence integrates cleanly with the existing core store architecture and requires zero new services or schema migrations.

### Alternative: Create standalone `docs/reference/research/privacy/chat-memory-dpia-retention-163.md`

* Approach: Create a new subdirectory `docs/reference/research/privacy/` and standalone file instead of adding a section to `docs/reference/research/chat-memory-dpia.md`.
* Trade-offs: Matches the literal filename example in the prompt, but duplicates privacy/DPIA tracking across two files and violates the KB convention ("Integrate new findings into the existing synthesis or project document. Create a new page only when no existing page can hold the topic").
* Evidence refs: `C8`, `C11`, `C12`
* Rejection rationale: `docs/reference/research/chat-memory-dpia.md` already holds both `#163` and `#217` DPIA/retention syntheses and the prompt explicitly permits `(or a dedicated section)`.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Human DPO confirmation of lawful basis per data class and Article 17(3) audit retention (`DH-007`), Legal retention schedule (`DH-003`), and `DH-006` processor/transfer approval remain open governance prerequisites outside this engineering slice; therefore `#121` must remain `Refs #121` and `dpo_reviewed` must remain `False`.
* Follow-up: Expose optional HTTP admin/DPO routes over `RightsRequestLedger` in `src/api` once named DPO intake roles and identity-verification procedures (`D8` in `chat-memory-dpia.md`) are ratified by the owner.
* Residual uncertainty: Provider abuse-monitoring reviewer location for `uksouth` and processor copy erasure confirmation mechanism remain unverified vendor/DPO items (`provider_erasure_confirmed=False`).

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Keep `dpo_reviewed=False` and `provider_erasure_confirmed=False` across all local controls | confirmed | constraint (`C1`, `C10`) | Local code cannot invent legal conclusions, retention periods, or processor erasure confirmation | `C1`, `C2`, `C10` | Preserves honest RAI posture and `Refs #121` |
| Document `#121` contract as a dedicated section in `docs/reference/research/chat-memory-dpia.md` plus `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` | confirmed | evidence (`C8`, `C11`, `C12`) | Follows KB single-synthesis convention and preserves doc-guard tests | `C8`, `C11`, `C12` | Run `test_chat_dpia_record.py` and `test_regulatory_privacy.py` during verification |
| Use `PYTHONPATH=src/core/src:src/core/tests` for unittest execution in this worktree | confirmed | evidence (`C13`) | Avoids importing stale shared editable install or mutating shared Python environment | `C13` | Deterministic worktree-local test verification |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Lawful basis per data class, Article 9 condition, Article 17(3) audit position, retention schedule, and `DH-006` transfer sign-off | Signed DPO and Legal decision record (`D1`..`D8`, `DH-001`..`DH-007`) | DPO and Legal (Juan Manuel Servera) | Required before setting `ZF_DATA_PROCESSING=actual` with real personal data or closing `#121` | follow-up (outside local engineering slice) |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| M | Staff/DPO API route design for `RightsRequestLedger` intake and identity verification | Connects core `RightsRequestLedger` to authenticated HTTP routes once `D8` intake role is named | DPO decision `D8` recorded | deferred | Q3; `C6`, `C8`, `C14` |

## Planning Readiness

* Status: Ready
* Decision state: Converged single-module core design (`data_protection.py`) + unit test suite + KB/README documentation updates.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`, `C13`, `C14`, `C15`
* Preconditions met: All callers, strict typing constraints, persistence hooks, and KB doc guards verified.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                                                      |
| Lane evidence or inline fallback | Inline investigation across `src/core`, `src/api`, `docs/prds`, and `docs/reference`                                           |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (`C1`..`C15`)                                                                                                            |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `rpi-plan`                                                            |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`..`C15`)                                                                                          |
| Output mode and planning support | `convergence`; yes, Planning Readiness is `Ready`                                                            |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness `Ready` (passed); pre-transition state write (passed) |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/data-protection-controls-121-research.md                               |
| Notes for planning or re-entry   | Structure plan into focused phases covering (1) inventory/tasks/attachment dispatch + ledger in `data_protection.py`, (2) unit tests in `test_data_protection.py`, and (3) `src/core/README.md` + KB sync and focused validation |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Further research is immaterial because all local source modules, callers, strict type rules, and KB guard tests have been verified directly.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none

