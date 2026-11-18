<!-- markdownlint-disable-file -->
# RPI Plan: Issue #116 Provider-Boundary Output Recheck and Document Derivative Controls

## Task Metadata

* Task ID: issue-116-entra-output-0052
* Task slug: issue-116-entra-output-0052
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-plan-critique.md

## Executive Summary

This plan delivers the remaining local-testable RAI provider-boundary acceptance criteria for Issue #116 (`Entra ID sign-in, roles and field-level visibility`) across `zava_forward.core` and `zava_forward.api`. Input allowlists alone cannot stop a drifted, prompt-injected, cached, or downstream-assembled model output from echoing or fabricating fields that a signed-in role is forbidden to see, nor stop raw unapproved documents from being sent to an AI model or mistakenly breaking manual case work when model dispatch is refused.

First, we extend `projection.py` with a projection-diff withheld-value helper derived directly from the canonical `contractor_detail` and `redact_staff_detail` projections, and enforce post-provider and read/export role-visibility rechecks across AI task outputs, citations, priority explanations, validation-failure/error payloads, persisted case summaries/drafts, review records and live review reports, reactive/proactive assistant proposals and CSV exports, chat answers/citations/resumed threads, and continuity exports. Second, we extend `data_protection.py`, `ai.py`, `ai_tasks.py`, `store.py`, and `server.py` so document AI processing requires an approved derivative (`reviewed_redacted`) or a validated scoped necessity exception (`task="read_document"`, matching `case_id` and `doc_id`, named human `approved_by`, `reference`, `reason`, unexpired) plus resident `ai_data_use_consent`, while preserving document storage, manual reading, permitted clean download, source permissions, proposal-only writes, resident consent updates, and independent manual/hazard routes whenever model processing is denied.

### User Decisions and Requirements Highlights

* Recheck permissions and field-level role visibility on AI outputs, citations, explanations, errors, review records, and exports so input filtering alone cannot pass unauthorized fields (such as vulnerability reasons, adjustments, contact details, notes, or restricted identifiers).
* Require an approved derivative or scoped necessity exception for document AI processing while keeping storage, manual reading, permitted download, source permissions, proposal-only writes, resident consent, and independent manual/hazard routes available when model processing is denied.
* Reuse existing capture, projection, and provider wrappers in `zava_forward.core` and `zava_forward.api` without introducing a parallel serializer, governance, or inference service.
* Validate using the focused tier (`unittest` in `src/core` and `src/api`, plus `mypy` and `ruff` check/format), do not run `tools/rpi-checks.py --all`, and leave a clean frozen local commit on `feat/ai-116-entra-output-0052` without pushing.

### What You May Not Know

* `ai_registry.LEGACY` role tuples are hashed into release-binding contracts (`permission_version` and `task_contract_version`), and existing offline evaluation harnesses (`ai_eval.py`) run constructed public fixtures in default `"constructed"` mode; preserving both contracts keeps release/evaluation gates green while enforcing strict derivative/exception and post-provider visibility checks.
* `Ai.run` currently attaches raw `ai_text` on validation failure and `ai_tasks.finish` spreads that dictionary into the HTTP response, creating an error/fallback leak vector that must be stripped alongside output/citation checks.
* `Programme Support Officer` is in `MANAGER_ROLES`, `RESIDENT_VIEW_ROLES`, and `FINANCE_VIEW` yet outside `DEFAULT_REASON_ROLES`, making `/api/ai/report`, `/api/continuity/export`, and `/api/assistants/proposals.csv` critical cross-role verification targets.

### Unresolved Decisions or Blockers

* None for this scoped local-testable increment. External organisational confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Entra B2B tenant configuration remain tracked as follow-up items outside this code increment.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) writing dated `2026-11-15` artifacts under `.copilot-tracking/` for Issue #116 (`Entra ID sign-in, roles and field-level visibility`) on branch `feat/ai-116-entra-output-0052` anchored to `feat/demo-164-chat-grounding-provenance-0900` (`9a0dd54fa`).
* Enforce and regression-test that permissions and field-level role visibility are rechecked on AI outputs, citations, explanations, errors, review records, and exports so input filtering alone cannot pass unauthorized fields (for example contractor vulnerability reasons or restricted identifiers) (Issue #116; caller prompt).
* Enforce and regression-test that document AI processing requires an approved derivative or scoped necessity exception, while storage, manual reading, and permitted download remain available when model processing is denied, preserving source permissions, proposal-only writes, resident consent, and independent manual/hazard routes (Issue #116; caller prompt).
* Reuse current capture, projection, and provider wrappers; do not create a parallel serializer, governance, or inference service (Issue #116).
* Validate at the focused tier (`unittest` in `src/core` and `src/api`, `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .`), do not run `tools/rpi-checks.py --all`, and commit all changes and `.copilot-tracking/` artifacts locally with the Copilot trailer without pushing (caller prompt).

## Goals

* Eliminate post-provider and post-persistence role-visibility bypasses across AI outputs, citations, explanations, errors, review records, and JSON/CSV exports using `projection.py` as the single visibility source of truth.
* Enforce fail-closed document AI dispatch requiring an approved derivative (`reviewed_redacted`) or validated scoped necessity exception plus resident AI data-use consent, while keeping storage, manual reading, permitted clean download, proposal-only boundaries, and manual/hazard workflows uninterrupted on denial.
* Prove both increments with deterministic offline regression tests across JSON/SQLite stores and HTTP API endpoints without regressing existing suites or release-binding hashes.

## Scope and Non-Goals

### In Scope

* Shared projection-diff withheld-value extraction and normalized matching in `src/core/src/zava_forward/core/projection.py` (subtracting all scalar strings visible anywhere in `projected_case`), plus role-aware rechecking of `documents[].summary` and `funding.draft` (`FINANCE_VIEW` gating on `funding.draft`, clean derivative preservation, and `NOTE_HELD` on withheld-value taint or raw-exception summaries for `not can_see_reason(user)`).
* Post-provider and read-time permission/visibility rechecks across `ai.py`, `ai_tasks.py`, `store.py`, `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`, and `src/api/src/zava_forward/api/server.py`.
* Approved-derivative (`reviewed_redacted`, `"synthetic_safe"` permitted only when `not actual_mode(env)`, and optional redacted derivative payload), scoped `necessity_exception` validation threaded explicitly through `data_protection.py` and `Ai.look_at`, resident `ai_data_use_consent` enforcement, and `src/agents/src/zava_forward/agents/ai_eval.py` constructed fixture alignment, with uninterrupted storage, manual reading, permitted download, and manual/hazard routes when denied.
* Focused unit and HTTP regression tests in `src/core/tests/test_data_protection.py`, `src/api/tests/test_ai_tasks.py`, and `src/api/tests/test_role_endpoint_inventory.py` plus regression verification of `src/agents/tests/test_ai_eval.py`.

### Non-Goals

* Introducing a new microservice, parallel serializer, or inference/governance daemon.
* Altering `ai_registry.LEGACY` cryptographic binding hashes or granting AI autonomous approval/write authority.
* Live Entra ID / B2B tenant deployment or resolving external organisational governance items OD-14 / OD-19.
* Running `tools/rpi-checks.py --all` or pushing commits to `origin`.

## Functional Requirements

* FR-1: Projection-derived withheld-value recheck
  * Observable acceptance criteria: Comparing a raw case against `projection.contractor_detail` or `projection.redact_staff_detail` for `user` identifies every case scalar withheld from `user` (including `resident.adjustment`, `case.reason`, `NOTE_KEYS`, non-status `outcome`, `RESIDENT_VIEW_ROLES` contact/representative fields, `FINANCE_VIEW` finance/grant fields, `INTAKE_FIELDS`, and out-of-scope case sensitive values) with Unicode/whitespace normalization and without blocking values legitimately visible in `user`'s projected case view.
* FR-2: Post-provider and read/export visibility enforcement across all six surfaces
  * Observable acceptance criteria: When a mocked provider returns unauthorized fields or citations despite filtered inputs, or when role/`ZF_REASON_ROLES` permissions differ at read/review/export time:
    1. AI task outputs (`message`, `summary`, `briefing`, `funding_draft`, `priority`, `read_document`) rebind held responses before `env`, `publish_output`, and `statement_sources` to a role-safe `workflow_text` (`source="template"`, `mode="workflow-only"`), omit `ai_text` from public API responses, set `ai_output=None` on visibility/forbidden holds while preserving clean `ai_output` on permitted-scope quarantine/attribution/unverified records, restrict `funding.draft` to `FINANCE_VIEW` using `_facts(c, False)`, and hold contaminated or raw-exception `documents[].summary` / `funding.draft` with `NOTE_HELD` in `redact_staff_detail`.
    2. Unresolved `[[...]]` markers and resolved citations containing withheld values are scrubbed/dropped rather than echoed.
    3. `ai_priority` item `reason` explanations, `_facts(c, reason_ok=False)`, and `Store.ai_run` workflow fallback templates withhold `c["reason"]`, `r["unavailable"]`, and unauthorized values both at generation time and in `_rec_view(rec, user)`.
    4. Validation failures, provider errors, and API error handlers never echo raw model `ai_text` or withheld case fields.
    5. `ai_tasks.review`, `ai_tasks.live_report(store, user)` (`GET /api/ai/report`), and `assistants._view` withhold reviewer/verification/review/provenance notes when `not projection.can_see_reason(user)` and recheck proposal/review outputs against `withheld_scope_values`.
    6. Exports (`/api/cases.csv`, `/api/assistants/proposals.csv`, and `/api/continuity/export`) enforce role visibility, returning `limited_export` whenever the caller lacks full reason, resident, and finance visibility and projecting `ai_records` / `assistant_proposals` in the full-export branch against `withheld_scope_values`.
    7. Chat answers, citations, and resumed threads (`ChatIsolation._withheld`, `ChatPanel._ask`, `GET /api/chat/threads/{tid}`, `chat_resume`) withhold unauthorized case or cross-case values and raise `ChatNotFound` (`404`) when case visibility is revoked.
* FR-3: Document approved derivative or scoped necessity exception and resident consent gate
  * Observable acceptance criteria: Document AI processing (`Ai.look_at`, `ai_tasks.run_document`, `Store.read_document`, `POST /api/cases/{id}/read-doc`) threads `derivative` and `necessity_exception` explicitly and refuses model dispatch (`_chat` / `urlopen` call count `0`) unless resident `ai_data_use_consent` is not withheld (`"given"` when set) AND either `derivative == "reviewed_redacted"` (dispatching redacted `derivative_text` bytes when provided while keeping intact file bytes in `docstore`), `derivative == "synthetic_safe"` when `not data_protection.actual_mode(env)` (explicitly rejected in `actual` mode), or a valid scoped `necessity_exception` (`reference` [non-`SYNTH-` in actual mode], named human `approved_by`, `reason`, `task="read_document"`, matching `case_id` and `doc_id`, unexpired `expires_at`) is present whenever `actual_mode(env)` is `True` or the document carries derivative/exception policy metadata; `ai_eval.py` (`PUBLIC_DOCUMENT`) passes cleanly in constructed evaluation runs.
* FR-4: Uninterrupted storage, manual reading, permitted download, proposal-only writes, and manual/hazard routes when model processing is denied
  * Observable acceptance criteria: When document AI processing is denied for missing/unapproved derivative, invalid/expired/wrong-scope necessity exception, withheld resident AI consent, or `ZF_AI_OFF=1`, the document remains stored via `add_document` / `POST /api/cases/{id}/upload`, readable in `detail` / `draft` without clobbering existing human notes, downloadable by permitted staff via `get_document` / `GET /api/docs/{cid}/{did}` (while contractors remain `403` and malware-flagged files remain blocked), proposal-only (`approval="Not reviewed"`, `instruction_status="Not an instruction"`, no authoritative state mutation), and independent of resident consent updates (`POST /api/cases/{id}/resident`) and manual/hazard routes (`call`, `decision`, `hazard-raise`, `hazard-refer`, `hazard-release`).

## Non-Functional Requirements

* NFR-1: Deterministic offline execution and zero external calls on hold
  * Objective threshold or evaluation condition: `0` network/provider calls when model dispatch is denied; `0` live external endpoints required in tests.
  * Operating condition or verification approach, if needed: Verified via mocked provider spies in `unittest` across JSON and SQLite stores.
  * Observable acceptance criteria: Provider spy call count equals `0` on every denied document AI path and post-provider rechecks run deterministically offline.
* NFR-2: Static type safety, lint/format cleanliness, and backward compatibility
  * Objective threshold or evaluation condition: `0` `mypy` errors, `0` `ruff check` / `ruff format --check` violations, and `100%` pass rate across `src/core`, `src/api`, and `src/agents/tests/test_ai_eval.py`.
  * Operating condition or verification approach, if needed: Focused validation commands run from workspace/component roots.
  * Observable acceptance criteria: All focused test, type, and lint checks exit `0` with `ai_registry.LEGACY` binding hashes unchanged.

## Acceptance Criteria

* Post-provider outputs, resolved and unresolved citations, priority explanations, failed-validation/error responses, review records (`review`, `/api/ai/report`, assistant notes), chat replies/resumed threads, and exports (`/api/cases.csv`, `/api/assistants/proposals.csv`, `/api/continuity/export`) withhold any field value hidden from the caller's role by `projection.py`, even when mocked model responses inject those values after input filtering.
* Persisted case `documents[].summary` and `funding.draft` containing values hidden from a reading staff role are replaced with `projection.NOTE_HELD` in `projection.redact_staff_detail`.
* Document AI processing refuses intact/unapproved documents (and documents whose resident `ai_data_use_consent` is refused/withdrawn) without calling the provider unless `derivative == "reviewed_redacted"` or a valid scoped `necessity_exception` bound to `task="read_document"`, `case_id`, and `doc_id` with a named human approver is supplied.
* When `derivative == "reviewed_redacted"` includes `derivative_text`, only the redacted derivative bytes reach `Ai.look_at` while the intact uploaded bytes remain stored and downloadable by permitted staff.
* When document model processing is denied, upload/storage, manual case/document reading, permitted clean download, source permissions (`403` contractor default-deny), proposal-only boundaries, resident consent updates, and manual/hazard routes continue to succeed.
* Focused `unittest` suites (`src/core`, `src/api`, `src/agents/tests/test_ai_eval.py`), `mypy`, `ruff check .`, and `ruff format --check .` all pass.
* Test ownership and bounds lock:
  * Removals: `none` (zero existing tests removed or weakened).
  * Canonical test targets: `src/core/tests/test_data_protection.py`, `src/api/tests/test_ai_tasks.py`, and `src/api/tests/test_role_endpoint_inventory.py` (maximum `18` focused test methods added across those three existing files; `0` new test files; `0` generated files modified).
  * Semantic vs regression coverage: Semantic assertions verify unauthorized canaries never appear in body/citations/explanations/errors/reviews/CSV/JSON exports and provider spy call counts stay `0` on held documents while storage/manual-read/download/consent/hazard routes succeed; regression runs verify all existing core, API, and `ai_eval` suites pass unchanged.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-plan.md                                                                   |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md                                                        |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-plan-critique.md with Revise disposition (`PC-001`..`PC-006` all directly applied and resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-research.md                                                            |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation after resolving all six direct critique findings (`PC-001`..`PC-006`)                              |
| Continuation context             | Active automatic RPI Agent parent continues directly to `rpi-implement`                                                                  |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-research.md`: Cycle 1 evidence (`C1`-`C12`), leak-surface trace, contrarian compatibility invariants, and selected Option C convergence design.
* `src/core/src/zava_forward/core/projection.py`, `controls.py`, `data_protection.py`, `ai.py`, `ai_tasks.py`, `store.py`, `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`: Canonical projection, AI wrapper, assistant, chat, continuity, and document store modules.
* `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_ai_tasks.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/core/tests/test_data_protection.py`: API route handlers and canonical regression test suites.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Projection-Diff Recheck and Document Derivative/Necessity Guards

* Intent: Implement the shared projection-derived withheld-value helper and document derivative / scoped necessity exception / resident consent controls in `zava_forward.core`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add projection-diff withheld-value helpers and stored AI summary/draft rechecks in `projection.py`

* Requirement and evidence: FR-1, FR-2 (`C1`, `C2`, `C5`)
* Expected result: `projection.py` exposes `withheld_case_values`, `withheld_scope_values`, and `contains_withheld_value` derived from `contractor_detail` / `redact_staff_detail`, and `redact_staff_detail` replaces stored `documents[].summary` and `funding.draft` with `NOTE_HELD` when they contain values withheld from `user`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce approved derivative, scoped necessity exception, and resident AI consent in `data_protection.py`, `ai.py`, and `ai_eval.py`

* Requirement and evidence: FR-3, FR-4 (`C3`, `C8`, `C10`, `C12`, `PC-002`)
* Expected result: `data_protection.py` validates scoped necessity exceptions, rejects `"synthetic_safe"` in `actual` mode, and evaluates `document_model_hold` (checking resident `ai_data_use_consent`, actual-mode `dispatch_hold`, and explicit derivative/exception metadata); `Ai.look_at` threads `derivative` and `necessity_exception` explicitly before any provider call and checks `FORBIDDEN`; and `ai_eval.py` marks `PUBLIC_DOCUMENT` with `ai_derivative="synthetic_safe"` for constructed evaluation runs.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Post-Provider Visibility Rechecks and Document Fallback Wiring Across Tasks, Store, Assistants, Chat, Continuity, and API

* Intent: Enforce post-provider and read/review/export permission and field-visibility rechecks across all six output surfaces and wire document derivative/exception metadata and manual fallback continuity through `store.py` and `server.py`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Enforce post-provider output, citation, explanation, error, and review-record rechecks in `ai_tasks.py` and `store.py`, plus document metadata/fallback preservation

* Requirement and evidence: FR-2, FR-3, FR-4 (`C3`, `C4`, `C5`, `C6`)
* Expected result: `ai_tasks.finish` strips `ai_text`, verifies active staff/case access, and withholds outputs/citations/`unresolved` markers containing withheld values; `Store._facts` stops leaking `c['reason']` when `reason_ok=False`; `ai_priority` and `_rec_view` recheck `reason` explanations and `cites`; `live_report(store, user=None)` holds `reviewer_reasons` when `not can_see_reason(user)`; and `add_document` / `read_document` support `ai_derivative`, `derivative_text`, `requires_derivative`, and `necessity_exception` while keeping storage, manual reading, permitted download, and human summaries intact when AI is denied.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Enforce post-provider and read/export visibility rechecks in `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`, and `server.py`

* Requirement and evidence: FR-2, FR-3, FR-4 (`C7`, `C8`, `C9`, `C11`)
* Expected result: `assistants.complete` and `assistants._view` (protecting JSON detail/list and `/api/assistants/proposals.csv`) withhold outputs violating role visibility and hold verification/review/provenance notes when `not can_see_reason(user)`; `ChatIsolation._withheld`, `ChatPanel._ask`, `chat_resume`, and `GET /api/chat/threads/{tid}` withhold unauthorized case/cross-case values in answers, citations, and resumed histories; `continuity_export` requires reason + resident + finance visibility for full export; and `server.py` passes `u` to `s.ai_live_report(u)` and accepts optional derivative/exception metadata on upload and `read-doc`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Regression Tests and Focused Tier Validation

* Intent: Add deterministic offline unit and HTTP regression tests for both Issue #116 increments and run focused tier validation (`unittest`, `mypy`, `ruff`).
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add unit and HTTP regression tests in `test_data_protection.py`, `test_ai_tasks.py`, and `test_role_endpoint_inventory.py` and run focused validation

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2 (`C1`-`C12`)
* Expected result: Focused regression tests prove post-provider output/citation/explanation/error/review/export visibility rechecks and document derivative/scoped necessity exception + storage/manual-read/download/consent/proposal-only/hazard continuity across JSON, SQLite, and HTTP routes; all focused `unittest`, `mypy`, and `ruff` checks pass cleanly.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md

## Dependencies

* Editable installs of `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api` in the active Python environment: Required so `unittest`, `mypy`, and `ruff` validate the live worktree sources (`src/core/src`, `src/api/src`).
* Existing `projection.py` and `data_protection.py` contracts: Reused directly so no parallel serializer or governance service is introduced and `ai_registry.LEGACY` release-binding hashes remain stable.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| 2026-11-15 `PC-001` [Critical]: Role-aware `funding["draft"]` and `documents[*]["summary"]` gating | resolved | Restricted `funding["draft"]` to `FINANCE_VIEW`, updated `Store.funding_draft` to pass `_facts(c, False)`, and held `funding["draft"]` / `doc["summary"]` for `not can_see_reason(user)` only when matching case-withheld values or produced via a raw-document `necessity_exception`, keeping clean `Grants and Evidence Officer` drafts and `Retrofit Coordinator` / `Quality Inspector` summaries intact. |
| 2026-11-15 `PC-002` [Critical]: `ai_eval.py` constructed fixture, actual-mode `synthetic_safe` block, and `Ai.look_at` `necessity_exception` threading | resolved | Added `ai_eval.py` (`PUBLIC_DOCUMENT` `ai_derivative="synthetic_safe"`) and `src/agents` test verification; rejected `"synthetic_safe"` whenever `actual_mode(env)` is `True`; threaded `derivative` and `necessity_exception` explicitly through `Ai.look_at` and `data_protection.model_dispatch` / `dispatch_hold`. |
| 2026-11-15 `PC-003` [High]: Use `store.detail`, sanitize `Store._facts` and `Store.ai_run` fallback `tmpl`, and include `Store.ai_priority` / `Store._rec_view` | resolved | Replaced `_raw_case_detail` with `store.detail(cid)` vs `store.detail(cid, user)`, masked `c["reason"]` and `r["unavailable"]` in `Store._facts` and `Store.ai_run` fallback templates for non-reason roles, aligned task names (`message`, `summary`, `briefing`, `funding_draft`, `priority`, `read_document`), and specified post-provider and read-time rechecks in `Store.ai_priority` and `Store._rec_view`. |
| 2026-11-15 `PC-004` [High]: Preserve clean `ai_output` on quarantine/attribution/unverified records and rebind `r` before `statement_sources` / `publish_output` | resolved | Kept `r["ai_text"]` in `Ai.run`, placed the visibility/permission recheck at the top of `ai_tasks.finish`'s `publish(late)` callback before `env`, `add_record`, `publish_output`, and `statement_sources`, cleared `ai_output` only on permission/visibility/`FORBIDDEN` holds while keeping clean `ai_output` comparison evidence intact, and omitted `ai_text` from the public HTTP return dict. |
| 2026-11-15 `PC-005` [High]: `ai_live_report(user)`, `ai_tasks.review`, full-branch `continuity_export` projection, and `ChatNotFound` (`404`) on revoked case access | resolved | Threaded `user` into `Store.ai_live_report(user=None)` / `ai_tasks.live_report(store, user=None)`, added case-visibility + `withheld_scope_values` rechecks on `ai_tasks.review` and full-branch `continuity_export` alongside `limited_export`, and preserved `ChatNotFound` (`404`) when case visibility is revoked on `chat_resume` / `GET /api/chat/threads/{tid}`. |
| 2026-11-15 `PC-006` [Medium]: Subtract visible projected scalars in `withheld_case_values` and guard `metadata=None` in `Store.add_document` | resolved | Subtracted all scalar strings still visible anywhere in `projected_case` from `withheld_case_values` so popped sub-trees never trigger false positives, and validated document derivative/exception metadata inside `change_provenance.operation` with `isinstance(metadata, Mapping)` guarding before `docstore.put`. |
| 2026-11-15 Residual risk: Novel semantic paraphrases of unrecorded facts | accepted_with_risk | Matches Issue #116 and `projection.py:13-18` design: input allowlists + `NOTE_HELD` on free-text notes + exact normalized withheld-value post-checks enforce role boundaries without false-assurance regex redaction. |

## Follow-Up Items

* Organisational control-owner confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration: External governance and cloud-tenant items on Issue #116 outside local-testable repository code; owned by programme/security governance.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
