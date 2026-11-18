<!-- markdownlint-disable-file -->

# Task Research: issue-116-entra-output-0052

| Field              | Value                                                                       |
|--------------------|-----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                  |
| Researcher / agent | rpi-research (via RPI Agent)                                                |
| Status             | Complete                                                                    |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-research.md |

## Research Brief

* What to research: Current implementation and remaining gaps in `zava_forward.core` and `zava_forward.api` for Issue #116 (`Entra ID sign-in, roles and field-level visibility`) RAI provider-boundary acceptance criteria: (1) output, citation, explanation, error, review-record, and export permission/field-level role visibility recheck so input filtering alone cannot pass unauthorized fields (e.g., contractor vulnerability reasons or restricted identifiers), and (2) document AI processing requirement for an approved derivative or scoped necessity exception while preserving storage, manual reading, permitted download, source permissions, proposal-only writes, resident consent, and independent manual/hazard routes when model processing is denied.
* Why it matters: Input allowlists alone cannot prevent echoed, hallucinated, cached, or downstream-assembled AI outputs, citations, explanations, errors, review records, or exports from leaking unauthorized fields across role boundaries, nor prevent raw unapproved documents from being sent to models or mistakenly blocking manual document access and statutory safety routes when AI processing is refused.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases of the automatic RPI loop for Issue #116.
* Scope: `src/core/src/zava_forward/core/` (projection, AI wrappers, AI tasks, document controls, exports, review records, assistants), `src/api/src/zava_forward/api/` (role-projected routes, AI endpoints, document upload/read/download, export routes), `src/core/tests/`, `src/api/tests/`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and `docs/adrs/0002-pilot-readiness-architecture.md`.
* Non-goals: Creating a parallel serializer or governance/inference service, transferring resident/safety/professional/ranking/financial/release authority to AI, resolving open organisational confirmation OD-14 / OD-19 beyond existing code rules, live Entra B2B browser sign-in, running `tools/rpi-checks.py --all`, or pushing to remote.
* Criteria: Reuse existing capture/projection/provider wrappers; prove via deterministic offline unit tests that input filtering alone cannot leak unauthorized fields in outputs, citations, explanations, errors, review records, or exports; prove document AI requires approved derivative or scoped necessity exception while storage, manual reading, permitted download, source permissions, proposal-only writes, resident consent, and manual/hazard routes remain intact.
* Requested outputs: Synthesized evidence log (`C#`), gap analysis across all output/document surfaces, evaluated alternatives, selected convergence recommendation, and planning readiness assessment.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Where do AI outputs, citations, explanations, errors, review records, exports, and document AI calls bypass or omit post-provider role/permission rechecks or derivative/necessity guards, and how should existing wrappers enforce them cleanly? |
| Codebase scope                   | `src/core/`, `src/api/`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`                             |
| External scope                   | none (codebase and local specification contracts cover all requirements)                                                                                           |
| Initial internal candidate areas | `src/core/src/zava_forward/core/projection.py`, `ai.py`, `ai_tasks.py`, `doc_controls.py`, `documents.py`, `export_fields.py`, `list_export.py`, `assistants.py`, `src/api/src/zava_forward/api/server.py`, `test_role_endpoint_inventory.py`, `test_ai_tasks.py` |
| Initial external candidate areas | none                                                                                                                                                               |
| Research posture                 | balanced                                                                                                                                                           |
| Posture provenance               | default (bounded internal task with named source targets plus adjacent surface discovery across exports, review records, errors, and document routes)              |
| Explicit limits / deadline       | Focused validation tier (`unittest`, `mypy`, `ruff`); do not run `tools/rpi-checks.py --all`; local commit only (do not push)                                      |
| Posture-specific completion basis | balanced scope coverage and adequate evidence across core and API surfaces                                                                                         |
| Edits allowed during research?   | no, research-only                                                                                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                               |
| Known constraints / excluded sources | Reuse current capture/projection/provider wrappers; offline mocked providers only; no web UI overhaul; no push to remote                                           |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                            | Scoped authority or output contract                                           | Selected / skipped reason                                                                 |
|---------------------|---------------------------------------|-----------------------------------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches all repository inputs and tracking paths | Enforces baseline doc reads, reuse of wrappers, focused validation tier, no `.copilot-tracking/` refs in prod code/commits | Selected: mandatory repository governance                                                 |
| Skill               | `rai-standards` / `owasp-llm`         | Semantic match to RAI provider-boundary and output filtering    | Background RAI/LLM boundary principles                                        | Skipped: local PRD v0.16.0+ and Issue #116 contracts define exact codebase rules directly |
| Skill               | `python-foundational`                 | Semantic match to Python package testing/typing                 | Python typing/linting conventions                                             | Skipped: repository `mypy`/`ruff` configs and existing module conventions are authoritative |
| Research specialist | `hve-core-all:rpi-researcher`         | Registered subagent for independent research lanes              | Bounded lane artifact under `.copilot-tracking/research/subagents/`           | Skipped (inline preferred): tightly coupled core/API projection trace fits direct reads   |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                                                 |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|-----------------------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with explicit scope, target parent ancestry (`9a0dd54fa`), acceptance criteria, and validation tier | N/A (non-interactive) | Proceed in `balanced` convergence mode inside active worktree `feat-116-entra-output-0052`                      |
| Direction change | Cycle 1 contrarian verification of existing `ai_registry.LEGACY` hashes, `continuity_export`, and `ai_eval.py` document checks | N/A (non-interactive) | Preserve `ai_registry.LEGACY` binding hashes, keep `Retrofit Programme Manager` full continuity ledger proof intact, and preserve constructed public fixture checks in `ai_eval.py` |
| Convergence      | Cycle 1 completed across Wider, Deeper, and Contrarian waves with complete `path:line` evidence | N/A (non-interactive) | Converged on shared `projection` withheld-value recheck helper + `data_protection` scoped necessity exception and document derivative/consent hold |

## Scope and Success Criteria

* Scope: Inspect `zava_forward.core` and `zava_forward.api` role projection, AI provider wrappers (`Ai.run`, `_chat`, `Ai.evidence`, `Ai.look_at`), AI tasks, reactive assistants, proactive scans, review records, error formatting, exports, and document storage/read/download/AI processing controls.
* Assumptions:
  * Earlier PRs (#275, #1162, #1466) delivered endpoint role inventory, oversized input refusal, and offline provider-spy input payload boundaries, leaving post-provider output/citation/explanation/error/review/export permission recheck and document derivative/necessity + manual-fallback guarantees partially or unevenly enforced. (To be verified in Cycle 1.)
* Success criteria:
  * Every research question is answered with exact `path:line` evidence (`C#`).
  * Existing coverage in `projection.py`, `ai.py`, `ai_tasks.py`, `doc_controls.py`, `documents.py`, and `server.py` is mapped against every item in the two requested Issue #116 increments.
  * Alternatives are compared and one clean wrapper-reusing convergence design is selected.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Enforce and test that permissions and field-level role visibility are rechecked on AI outputs, citations, explanations, errors, review records, and exports so that input filtering alone cannot pass unauthorized fields (e.g., contractor vulnerability reasons or restricted identifiers).
  2. Enforce and test that document AI processing requires an approved derivative or scoped necessity exception, while storage, manual reading, and permitted download remain available when model processing is denied, preserving source permissions, proposal-only writes, resident consent, and independent manual/hazard routes.
* Inferred research questions:
  * Q1: What PRD/ADR contracts and prior PR #1162 / #1466 implementations already exist for Issue #116?
  * Q2: How does role/field-level projection (`projection.py`, `export_fields.py`, `list_export.py`, `server.py`) currently filter records, and how do AI outputs, citations, explanations, errors, review records, and exports flow to callers?
  * Q3: What happens today if a mocked/compromised AI provider returns unauthorized fields, vulnerability reasons, restricted identifiers (UPRN, resident email/phone, vulnerability notes, raw bank/grant secrets), or unauthorized citations in structured outputs, chat explanations, provider/validation errors, persisted review records, or CSV/JSON exports?
  * Q4: How do `Ai.look_at`, `Ai.evidence`, `doc_controls.py`, `documents.py`, `resident_documents.py`, and `server.py` currently gate document AI processing vs storage, manual reading, and download, and how are approved derivatives and scoped necessity exceptions represented?
  * Q5: How do document AI denials interact with source permissions, proposal-only writes, resident consent, and independent manual/hazard routes?
* Caller constraints and non-goals: Reuse existing capture/projection/provider wrappers; no new governance/serializer/inference service; focused validation only; local commit without push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                      |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|----------------------------------------------------------------------------------------|
| narrow                                                   | Focus on remaining local-testable RAI provider-boundary output recheck and document derivative/fallback | Caller intake       | Scopes research and plan to the two named increments while preserving existing tests   |
| exclude                                                  | Do not run `tools/rpi-checks.py --all`; do not push to remote; do not create parallel services          | Caller intake       | Constrains implementation architecture and validation commands                         |

## Research Questions

|  # | Sub-question                                                                                                                                   | Type            | Priority | Status   |
|---:|------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What PRD/ADR rules and existing Issue #116 code/tests define the provider-boundary, output-recheck, and document-derivative contracts?          | straightforward | H        | answered |
| Q2 | How does `projection.py` define role visibility and sensitive fields/terms, and which surfaces currently call or skip it?                      | breadth         | H        | answered |
| Q3 | Can unauthorized fields/terms currently leak through AI outputs, citations, explanations, errors, review records, or exports when inputs were clean? | depth      | H        | answered |
| Q4 | How is document AI processing gated for approved derivatives or scoped necessity exceptions, and do storage, manual read, and download survive denial? | depth     | H        | answered |
| Q5 | How are source permissions, proposal-only writes, resident consent, and independent manual/hazard routes preserved across these paths?         | contrarian/depth| H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, GitHub Issue #116 body, and recent merged PR history (#275, #1162, #1466, #1750, #1752).
* Reused (verified) findings: Issue #116 tracks RAI Provider-Boundary Acceptance Criteria including output/citation/explanation/error/review-record/export permission rechecks and document derivative/scoped necessity exception + manual availability guarantees, reusing current capture/projection/provider wrappers.
* Superseded / stale: Prompt placeholder branch/worktree label `feat-116-provider-boundary-recheck` reconciled to actual initialized worktree `/home/azureuser/source/ama-demo-wt/feat-116-entra-output-0052` (`feat/ai-116-entra-output-0052`) at commit `9a0dd54fa`.

## Executed Research Cycles

### Cycle 1

* **Wave 1 (Wider — inline)**:
  * Mapped all role and field-visibility definitions in `projection.py` (`CONTRACTOR`, `STAFF_ROLES`, `DEFAULT_REASON_ROLES`, `FINANCE_VIEW`, `RESIDENT_VIEW_ROLES`, `can_see_reason`, `contractor_detail`, `redact_staff_detail`, `hold_notes`, `status_only`) and `controls.py` (`C1`, `C2`).
  * Enumerated every AI provider dispatch and post-provider output, citation, explanation, error, review-record, export, and document surface across `ai.py`, `ai_tasks.py`, `store.py`, `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `continuity.py`, `data_protection.py`, and `server.py` (`C3`-`C11`).
* **Wave 2 (Deeper — inline)**:
  * Traced post-provider flows assuming a drifted, prompt-injected, or mocked model returns unauthorized case fields even when prompt inputs were filtered:
    1. `Ai.run` (`ai.py:303-305`) attaches raw unvalidated `ai_text=text` when validation fails, and `ai_tasks.finish` (`ai_tasks.py:296`) spreads `dict(result, ...)` straight into the public API return payload and persists raw `ai_output` (`C3`, `C4`).
    2. `Store._facts(c, reason_ok=False)` (`store.py:851`) interpolates `c['reason']` even when `reason_ok` is `False`, while `ai_tasks.finish` (`ai_tasks.py:258-305`) checks only generic `FORBIDDEN` regex and citation resolution, echoing raw model `text` and raw `unresolved` `[[...]]` strings without rechecking `user`'s role/field visibility (`C4`, `C5`).
    3. `read_document` (`store.py:820-825`) and `funding_draft` (`store.py:1182-1186`) persist AI-generated `doc["summary"]` and `c["funding"]["draft"]` onto the case record; `projection.redact_staff_detail` (`projection.py:168-221`) does not recheck those stored AI texts when another staff role without `can_see_reason`, `RESIDENT_VIEW_ROLES`, or `FINANCE_VIEW` later reads `detail(cid, user)` (`C1`, `C5`).
    4. `ai_priority` (`store.py:964-1035`) validates `cites` via `ai_tasks.priority_items` (`ai_tasks.py:206-225`) but never rechecks item `reason` explanations against withheld case values either at generation time or on read in `_rec_view(rec, user)` (`C4`, `C6`).
    5. `GET /api/ai/report` (`server.py:926`) is open to `MANAGER_ROLES` (`Retrofit Programme Manager` and `Programme Support Officer`), yet `Programme Support Officer` lacks `can_see_reason`; `s.ai_live_report()` (`store.py:1193`, `ai_tasks.py:409-430`) accepts no `user` and returns `reviewer_reasons` verbatim (`C4`, `C11`).
    6. `assistants.py` (`validate_output`, `complete`, `_view`, `export`) serves mixed-visibility capability roles (`works-resident-coordination`, `funding-evidence`, `quality-evidence`, `stock-prioritisation`, `assessment-preparation`) without rechecking returned `output` against withheld case fields across capability roles or holding `verification.note` / `review.note` / event notes when the reading user lacks `can_see_reason(user)` (`C7`).
    7. `ChatIsolation._withheld` (`chat_isolation.py:163-169`) checks only `TOOLISH` and `resident["adjustment"]`, missing withheld contact/hazard/appointment/quality notes, non-status outcomes, `case.reason`, `RESIDENT_VIEW_ROLES`-restricted fields (`phone`, `email`, `representative`), `FINANCE_VIEW`-restricted fields, `INTAKE_FIELDS`, cross-case values, and thread-read rechecks when permissions change (`C8`, `C9`).
    8. `data_protection.py` (`model_dispatch`, `dispatch_hold` at lines `187-232`) has no `scoped necessity exception` representation or validator; `Ai.look_at` (`ai.py:338`) calls `dispatch_hold("raw_document", os.environ)` without passing `derivative`, `necessity_exception`, or document scope; and `store.add_document` / `store.read_document` (`store.py:774-826`) do not record or enforce approved derivatives (`reviewed_redacted` + optional redacted payload), scoped necessity exceptions, or resident `ai_data_use_consent` (`C3`, `C5`, `C10`).
* **Wave 3 (Contrarian — inline)**:
  * Checked whether changing `ai_registry.LEGACY` role tuples would break existing release-binding hashes or endpoint tests: confirmed `ai_registry.legacy_binding` (`ai_registry.py:103-114`) hashes `spec["roles"]` into `permission_version` and `task_contract_version`, and `test_ai_tasks.py:216` exercises `briefing` for all `STAFF_ROLES` (`C12`). Therefore, `ai_registry.LEGACY` must remain untouched while active staff/role/scope and field-visibility rechecks run in `projection`, `ai_tasks`, `store`, `assistants`, `chat_isolation`/`chat_panel`, and `continuity`.
  * Checked whether `ai_eval.py` (`run_document_checks` at lines `488-505`), `test_assistant_release.py:948`, `test_ai_consumption_api.py:1328`, and `test_ai_boundary.py:103-121` call `read_document` / `run_document` / `look_at` in default `"constructed"` mode without `derivative="reviewed_redacted"`: confirmed yes (`C12`). Therefore:
    * Default `"constructed"` mode fixtures without an explicit unapproved derivative marker (`derivative` unset or `"constructed_fixture"`) continue to pass when resident `ai_data_use_consent` is not withheld, preserving 100% compatibility with offline evaluation and release suites.
    * Whenever `ZF_DATA_PROCESSING != "constructed"` (actual mode), OR a document records an unapproved/intact derivative state (e.g., `derivative="intact"` / `"raw"` / `"unredacted"` / `"none"` or `requires_derivative=True` or invalid `necessity_exception`), OR resident `ai_data_use_consent` is recorded and not `"given"`, model dispatch is refused unless `derivative == "reviewed_redacted"` or a valid scoped `necessity_exception` (`task="read_document"`, matching `case_id` and `doc_id`, non-empty `reference` [non-`SYNTH-` in actual mode], named human `approved_by`, non-empty `reason`, unexpired) is supplied.
  * Checked `continuity_export` (`continuity.py:665-795`): `Retrofit Programme Manager` holds `DEFAULT_REASON_ROLES`, `RESIDENT_VIEW_ROLES`, and `FINANCE_VIEW`, so requiring all three for `scope="full"` preserves existing `test_continuity_epoch_export.py` full ledger proof while routing any manager lacking reason, resident, or finance visibility (e.g., `Programme Support Officer` even under `ZF_REASON_ROLES` overrides) to `limited_export(bundle)`.
* **Re-entry decision**: No second cycle required; all five research questions (`Q1`-`Q5`) are resolved with direct `path:line` codebase evidence and zero open ambiguities.

## Evidence Log

| ID  | Path and lines                                                                 | Verified finding                                                                                                                                      |
|-----|--------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/core/src/zava_forward/core/projection.py:29-221`                          | Canonical role sets (`CONTRACTOR`, `STAFF_ROLES`, `DEFAULT_REASON_ROLES`, `FINANCE_VIEW`, `RESIDENT_VIEW_ROLES`) and `contractor_detail` / `redact_staff_detail` / `hold_notes`; does not yet recheck stored AI `documents[].summary` or `funding.draft`. |
| C2  | `src/core/src/zava_forward/core/controls.py:12-15`                             | Defines `FINANCE_ROLES`, `RESIDENT_ROLES`, and `RESIDENT_VIEW_ROLES` (`RLO`, `RC`, `PM`, `PSO`), proving distinct non-overlapping visibility across staff roles. |
| C3  | `src/core/src/zava_forward/core/ai.py:303-370`                                 | `Ai.run` returns raw `ai_text=text` on failed validation; `Ai.look_at` calls `data_protection.dispatch_hold("raw_document", os.environ)` without derivative, necessity-exception, or document scope. |
| C4  | `src/core/src/zava_forward/core/ai_tasks.py:206-430`                           | `priority_items` checks citations only, not `reason` explanations; `finish` leaks `result["ai_text"]` and raw `unresolved` markers without field-visibility rechecks; `live_report(store)` ignores caller `can_see_reason`. |
| C5  | `src/core/src/zava_forward/core/store.py:774-872, 1165-1195`                   | `add_document`, `read_document`, and `get_document` separate storage and download from AI reading, but `read_document` lacks derivative/necessity/consent enforcement and `_facts` leaks `c['reason']` when `reason_ok=False`. |
| C6  | `src/core/src/zava_forward/core/store.py:964-1095`                             | `_rec_view` and `ai_priority` do not recheck item `reason` explanations or `cites` against current `user` role visibility when roles or `ZF_REASON_ROLES` differ. |
| C7  | `src/core/src/zava_forward/core/assistants.py:428-555, 1121-1210, 2044-2098`   | `validate_output` checks schema/citations/`FORBIDDEN` only; `_view` does not hold `verification.note` / `review.note` / event notes for non-reason roles or recheck `output` against withheld case values. |
| C8  | `src/core/src/zava_forward/core/chat_isolation.py:94-179`                      | `ai_consent_state` defines resident AI consent lookup; `_withheld` checks only `TOOLISH` and `resident.adjustment`, omitting notes, outcomes, `case.reason`, phone/email/representative, finance, intake, and cross-case values. |
| C9  | `src/core/src/zava_forward/core/chat_panel.py:555-875`                         | `ChatPanel` formats answers, citations, and rules fallbacks; stored thread reads (`GET /api/chat/threads/{tid}` in `server.py:640-675`) need live role/scope and assistant message visibility rechecks on resume. |
| C10 | `src/core/src/zava_forward/core/data_protection.py:187-232`                    | `model_dispatch` and `dispatch_hold` enforce `needs_derivative` via `derivative == "reviewed_redacted"` in actual mode only, with no scoped necessity exception support. |
| C11 | `src/api/src/zava_forward/api/server.py:640-715, 915-955, 1620-1680`           | Routes `/api/ai/report` (missing `u` on `ai_live_report`), `/api/docs/{cid}/{did}`, `/api/cases/{id}/upload`, `/api/cases/{id}/read-doc`, `/api/assistants/proposals.csv`, and `/api/continuity/export`. |
| C12 | `src/core/src/zava_forward/core/ai_registry.py:69-115`                         | `LEGACY` role tuples feed `legacy_binding` cryptographic hashes; existing tests in `test_ai_tasks.py:1-390`, `test_role_endpoint_inventory.py:1-220`, and `ai_eval.py:488-505` constrain compatibility. |

## Synthesized Findings

* **Q1 & Q2 (Wrapper reuse and canonical visibility model)**: `projection.py` (`C1`) and `controls.py` (`C2`) already own the exact default-deny role and field-level visibility projection (`contractor_detail`, `redact_staff_detail`, `hold_notes`, `can_see_reason`, `RESIDENT_VIEW_ROLES`, `FINANCE_VIEW`). Deriving `withheld_values(store, user, case_ids)` directly from the difference between a raw case detail and `projection.redact_staff_detail` / `contractor_detail` reuses the single source of truth without creating a parallel serializer.
* **Q3 (Six concrete post-provider leak surfaces)**: Input filtering alone currently lets unauthorized values pass through: (1) AI task outputs and failed-validation `ai_text` (`C3`, `C4`), plus case-persisted `documents[].summary` and `funding.draft` (`C1`, `C5`); (2) unresolved `[[...]]` citation markers and post-policy-change priority citations (`C4`, `C6`); (3) `ai_priority` / `_rec_view` `reason` explanations and `_facts` `c['reason']` (`C5`, `C6`); (4) raw `ai_text` attached to failed validation responses (`C3`, `C4`); (5) `ai_live_report` `reviewer_reasons` shown to `Programme Support Officer` and assistant `verification.note` / `review.note` shown to non-reason roles (`C4`, `C7`, `C11`); and (6) `/api/assistants/proposals.csv` (via `_view`) and `continuity_export` under partial-visibility overrides (`C7`, `C11`).
* **Q4 & Q5 (Document derivative / scoped necessity exception and manual continuity)**: Adding `validate_necessity_exception` and `document_ai_hold` in `data_protection.py` (`C10`) and wiring them through `Store.add_document`, `Store.read_document`, `ai_tasks.run_document`, and `Ai.look_at` (`C3`, `C5`) ensures model processing requires either `derivative == "reviewed_redacted"` (sending redacted derivative bytes when supplied rather than intact raw bytes) or a valid scoped necessity exception (`task="read_document"`, matching `case_id` and `doc_id`, named human `approved_by`, `reference` [non-`SYNTH-` in actual mode], `reason`, unexpired), while also honouring resident `ai_data_use_consent`. When model processing is denied, zero provider calls occur and `read_document` returns a proposal-only workflow-only fallback (`source="template"`, `mode="workflow-only"`), leaving document storage (`add_document`), manual case reading (`detail`, `draft`), permitted clean download (`get_document`), source permissions, resident consent routes, and independent manual/hazard routes completely available.

## Alternatives Considered

| Option | Description | Pros | Cons | Disposition |
|--------|-------------|------|------|-------------|
| Option A: Regex/keyword blocklist only | Add regex patterns for phones, emails, and vulnerability words to `ai.FORBIDDEN` | Small code diff | Violates `projection.py` design ("no pattern-based redaction... a reason can be typed in any words"); misses arbitrary case-specific vulnerability adjustments, notes, outcomes, and role-dependent visibility | Rejected (`C1`) |
| Option B: Parallel output serializer service | Build a separate post-processing microservice/module with duplicated role matrices | Isolates AI output schemas | Duplicates `projection.py` role rules, risks drift, and violates Issue #116 non-goal ("do not create a parallel serializer, governance or inference service") | Rejected |
| Option C: Projection-diff withheld-value recheck + `data_protection` derivative/necessity guard inside existing wrappers | Derive per-user (and per-capability-role) withheld case values by comparing raw case data against `projection.redact_staff_detail` / `contractor_detail`, enforce across `ai_tasks`, `store`, `projection`, `assistants`, `chat_isolation`/`chat_panel`, `continuity`, and `server`, and enforce `reviewed_redacted` derivative or scoped `necessity_exception` + resident consent in `data_protection` / `store.read_document` / `Ai.look_at` | Reuses canonical `projection.py` and `data_protection.py` wrappers; automatically covers every role combination and `ZF_REASON_ROLES` override; preserves `ai_registry` hashes, `ai_eval.py`, and manual/download/hazard routes | Requires careful filtering of short generic scalars already present in the projected case so valid cited facts are never false-positively withheld | **Selected** (`C1`-`C12`) |

## Decisions, Risks, and Readiness

* **Current confirmed decisions**:
  * Converge on Option C reusing `projection.py`, `data_protection.py`, `ai.py`, `ai_tasks.py`, `store.py`, `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `continuity.py`, and `server.py`.
  * Keep `ai_registry.LEGACY` unchanged to preserve release-binding hashes (`C12`).
  * Keep `Retrofit Programme Manager` full continuity export intact while routing any manager missing `can_see_reason`, `RESIDENT_VIEW_ROLES`, or `FINANCE_VIEW` to `limited_export`.
  * Enforce approved derivative (`reviewed_redacted`) or scoped necessity exception (`task="read_document"`, `case_id`, `doc_id`, human `approved_by`, `reference`, `reason`, optional `expires_at`) plus resident `ai_data_use_consent` on document AI processing while preserving default constructed public fixtures in offline harnesses when no intact/unapproved derivative marker or consent refusal is set.
* **Key risks & mitigations**:
  * *False-positive withholding on short shared tokens*: Exclude values that still appear as scalars/substrings in the user's projected case view (ignoring `documents[].summary` and `funding.draft` themselves) and require meaningful length (`>= 4` chars) unless the value comes from an explicit sensitive field (`resident.adjustment`, `resident.phone`, `resident.email`, `resident.representative`, `case.reason`, `NOTE_KEYS`, non-status `outcome`, `INTAKE_FIELDS`, `finance`/`grants` refs) not present in the projected view.
  * *Existing test regressions*: Run full `unittest` discovery in `src/core` and `src/api` plus `src/agents/tests/test_ai_eval.py`, `mypy`, and `ruff`.
* **Potential further research**: None needed for this scoped increment; live Entra B2B tenant configuration and organisational confirmation of OD-14 / OD-19 remain external operational follow-ups on Issue #116.
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`

## Artifact Self-Check

* [x] Research brief, scope, non-goals, posture (`balanced`), and extension provenance recorded.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order before convergence synthesis.
* [x] Every material claim maps to stable `C1`-`C12` codebase `path:line` evidence.
* [x] Alternatives evaluated with evidence-based rejection rationale and one convergence recommendation selected.
* [x] Research remained strictly read-only on source files; `Planning Readiness: Ready` recorded.

