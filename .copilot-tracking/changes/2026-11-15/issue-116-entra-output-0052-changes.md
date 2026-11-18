<!-- markdownlint-disable-file -->
# RPI Changes: Issue #116 Provider-Boundary Output Recheck and Document Derivative Controls

## Metadata

* Task ID: issue-116-entra-output-0052
* Related plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: Completed all planned implementation tasks (`P01`..`P03`) and verified focused-tier static checks and unit/HTTP regression suites across `src/core`, `src/agents`, and `src/api`.

## Execution Summary

Delivered the full approved plan (`P01`, `P02`, `P03`) for Issue #116's remaining local-testable RAI provider-boundary output recheck and document derivative/necessity-exception + manual-fallback controls across `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api`, verified by 13 new regression test methods and 858 passing focused tests plus clean `ruff` and `mypy` checks across all three packages.

## Completed Work

### Core Projection-Diff Recheck and Document Derivative/Necessity Guards (`P01`, `P01-T01`, `P01-T02`)

* Modified `src/core/src/zava_forward/core/projection.py` (`P01-T01`): Added `normalize_visibility_text`, `withheld_case_values`, side-effect-free `project_case_visibility`, `withheld_scope_values`, and boundary-safe `contains_withheld_value` derived directly from `contractor_detail` and `redact_staff_detail` (subtracting scalars visible anywhere in the projected view), and updated `redact_staff_detail` to gate `funding["draft"]` to `FINANCE_VIEW`, strip `derivative_text`, hold `necessity_exception.reason` when `not can_see_reason(user)`, and hold stored `funding["draft"]` or `documents[].summary` (`NOTE_HELD`) when contaminated by withheld values or produced via a raw-document necessity exception for a non-reason role.
* Modified `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai.py`, and `src/agents/src/zava_forward/agents/ai_eval.py` (`P01-T02`): Added `APPROVED_DERIVATIVE`, `CONSTRUCTED_DERIVATIVE`, `actual_mode`, `validate_necessity_exception` (requiring named human approver, non-automated tokens, non-`SYNTH-` reference in actual mode, `reason`, `task="read_document"`, matching `case_id` and `doc_id`, unexpired ISO `expires_at`), and `document_model_hold` (default-denying intact uploaded documents and enforcing resident `ai_data_use_consent`), wired `document_model_hold` and `FORBIDDEN` into `Ai.look_at`, and tagged `PUBLIC_DOCUMENT` in `ai_eval.py` with `ai_derivative="synthetic_safe"` for constructed offline evaluation runs.

### Post-Provider Visibility Rechecks and Document Fallback Wiring (`P02`, `P02-T01`, `P02-T02`)

* Modified `src/core/src/zava_forward/core/ai_tasks.py` and `src/core/src/zava_forward/core/store.py` (`P02-T01`): Added post-provider and live-role permission/visibility rechecks at the top of `ai_tasks.finish`'s `publish` callback before `env`/`publish_output`/`statement_sources` (rebinding held outputs to `workflow_text`, clearing `ai_output` on visibility/`FORBIDDEN` holds while keeping clean `ai_output` on permitted quarantine/attribution records, scrubbing unresolved `[[...]]` markers and withheld citations, and omitting raw `ai_text` from public return dicts), readable-MIME-first `document_model_hold` checking in `run_document`, live access/role recheck in `ai_tasks.review` and `ai_tasks.live_report(store, user=None)`, role-projected `Store.draft(..., user=user)`, `Store.ai_run` workflow status fallback, `Store.funding_draft` (`_facts(c, False)`), `Store.ai_priority` and `Store._rec_view` citation/explanation checks, and `Store.add_document` / `Store.read_document` derivative/exception metadata handling preserving intact stored file bytes, human summaries, manual download, and proposal-only state on denial.
* Modified `src/core/src/zava_forward/core/assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`, and `src/api/src/zava_forward/api/server.py` (`P02-T02`): Added capability-wide intersection visibility hold in `assistants.complete` and live per-caller role visibility + review/verification/provenance note holds in `assistants._view` (protecting JSON detail/list and `/api/assistants/proposals.csv`), generalized `ChatIsolation._withheld` and added `ChatIsolation.scrub_thread` wired into `chat_resume` and `GET /api/chat/threads/{tid}` (preserving `ChatNotFound` `404` on revoked case visibility), checked parsed chat answers and citations in `ChatPanel._ask` while keeping `decision-rules-fallback` intact on uncited/foreign replies, broadened `continuity_export` `limited_export` to require `can_see_reason` + `RESIDENT_VIEW_ROLES` + `FINANCE_VIEW` while projecting full-export `ai_records` and `assistant_proposals`, and wired `/api/ai/report`, `/api/cases/{id}/draft`, `/api/cases/{id}/read-doc`, and `/api/chat/threads/{tid}` in `server.py`.

### Regression Tests and Focused Tier Validation (`P03`, `P03-T01`)

* Modified `src/core/tests/test_data_protection.py`, `src/api/tests/test_ai_tasks.py`, and `src/api/tests/test_role_endpoint_inventory.py` (`P03-T01`): Added 13 focused offline regression test methods (within the locked `<= 18` cap, `0` existing tests removed) covering `withheld_case_values` / `withheld_scope_values` / `contains_withheld_value`, `document_model_hold` and `validate_necessity_exception` across actual and constructed modes, `Ai.look_at` zero-call holds, post-provider output/citation/explanation/error/review-record/funding-draft rechecks across JSON and SQLite stores, document approved-derivative `derivative_text` dispatch vs intact storage/manual-read/download/consent-withdrawal/manual-call/hazard continuity, and HTTP cross-role rechecks across `/api/ai/report`, `/api/continuity/export`, `/api/assistants/proposals.csv`, `/api/chat/threads/{tid}`, and `/api/cases/{id}/read-doc`.

## Implementation-Time Plan and Detail Updates

* Local judgment refinements preserving approved plan intent (no scope or requirement change):
  * Added side-effect-free `projection.project_case_visibility(user, raw_case)` (supporting raw dict `measure_decisions` in `redact_staff_detail`) so AI visibility rechecks never invoke `Store.work_context` or `insights.recommend_handover` queue side effects.
  * Preserved the `Store._facts` stage `c["reason"]` prompt contract verified by `LegacyRoleProjection` in `test_ai_provider_payload_spy.py` while keeping post-provider `withheld_scope_values` enforcement active on returned outputs.
  * Evaluated `assistants.complete` against the intersection of `withheld_case_values` across `cap_roles` (rejecting strings forbidden to all roles of the capability) while `assistants._view` enforces the exact caller's live `withheld_case_values` + `withheld_scope_values` on read/CSV/export.
  * Checked `TOOLISH` pre-parse and `iso._withheld` post-`parse_reply` in `ChatPanel._ask` so uncited or out-of-sources replies rejected by `parse_reply` continue routing to `decision-rules-fallback`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` and `ruff format --check .` | `src/core`, `src/agents`, `src/api` | Passed | `0` lint issues and `0` formatting diffs (`281`, `62`, and `196` files formatted respectively) |
| `mypy src tests` | `src/core`, `src/agents`, `src/api` | Passed | `Success: no issues found` across `334` (`src/core`), `66` (`src/agents`), and `221` (`src/api`) source files |
| Focused `unittest` (`src/core`) | `test_data_protection`, `test_ai_provider_payload_spy`, `test_ai_statement_sources`, `test_ai_register_completeness`, `test_rai_release`, `test_rai_release_invalidation`, `test_documents`, `test_document_rescan`, `test_chat_panel`, `test_chat_privacy`, `test_chatthreads`, `test_list_export`, `test_assistants_identity` | Passed | `Ran 240 tests in 31.867s - OK (skipped=19)` |
| Focused `unittest` (`src/agents`) | `test_ai_eval` | Passed | `Ran 20 tests in 6.409s - OK` |
| Focused `unittest` (`src/api`) | `test_ai_tasks`, `test_role_endpoint_inventory`, `test_role_matrix`, `test_ai_boundary`, `test_ai_call_site_inventory`, `test_assistants`, `test_assistants_dispatch`, `test_chat_isolation`, `test_chat_panel`, `test_chat_consent_boundary`, `test_continuity`, `test_continuity_epoch_export`, `test_document_controls`, `test_entra_authoritative`, `test_auth`, `test_list_export_api` | Passed | `Ran 598 tests - OK` across JSON, SQLite, and HTTP server suites |
| Full repository gate (`tools/rpi-checks.py --all`) | Repository-wide | Skipped | Explicitly excluded by caller prompt (`Validation Tier (Focused): Do NOT run tools/rpi-checks.py --all`) |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` all checked `[x]`; local-judgment refinements recorded above)
* Completed-work evidence and handoff prose: reconciled across `src/core`, `src/agents`, and `src/api`
* Validation, blockers, remaining work, and follow-up items: reconciled (`858` focused tests passed, `0` mypy/ruff errors, `0` blockers, `0` remaining active-plan markers)
* Review readiness: ready for single post-implementation `rpi-review`

## Blockers

* None

## Remaining Work

* None in active plan scope (`P01`..`P03` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-plan.md, `## Follow-Up Items`
* Organisational control-owner confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration: External governance and cloud-tenant items on Issue #116 outside local-testable repository code; owned by programme/security governance.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`; remaining: none
* Validation coverage: Focused tier passed (`ruff check`, `ruff format --check`, `mypy src tests`, and `858` focused `unittest` cases across `src/core`, `src/agents`, and `src/api`)
* Blockers: None
* Current plan and detail updates: Recorded four local-judgment implementation refinements preserving plan intent and existing suite invariants
* Planning and critique state: Ready (`PC-001`..`PC-006` resolved)
* Follow-up items: External OD-14 / OD-19 and live Entra B2B configuration
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
