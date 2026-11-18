<!-- markdownlint-disable-file -->
# Review: Issue #116 Provider-Boundary Output Recheck and Document Derivative Controls

## Scope and Evidence

* Task ID: issue-116-entra-output-0052
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: FR-1..FR-4, NFR-1..NFR-2, acceptance criteria, critique dispositions (`PC-001`..`PC-006`), implementation-time local-judgment refinements, focused-tier validation (`ruff`, `mypy`, `858` `unittest` cases across `src/core`, `src/agents`, and `src/api`), and Issue #116 external follow-up boundary
* Plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-research.md and workspace `git diff` across `src/core`, `src/agents`, and `src/api`

## Opening Review State

* Interpreted review goal: Independently assess whether the completed `P01`..`P03` implementation satisfies all planned Issue #116 provider-boundary output/citation/explanation/error/review/export visibility recheck requirements and document approved-derivative/scoped-necessity-exception + manual-fallback continuity requirements without regressing existing contracts or exceeding review/governance boundaries.
* Review scope: full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`)
* Evidence readiness: Ready; plan, phase details, single plan critique (`PC-001`..`PC-006`), reconciled changes record, research synthesis (`C1`..`C12`), and focused validation results are all present and current.
* Acceptance basis: Plan `## Functional Requirements` (`FR-1`..`FR-4`), `## Non-Functional Requirements` (`NFR-1`..`NFR-2`), `## Acceptance Criteria` (including locked test bounds), and `## Critique Disposition` (`PC-001`..`PC-006`).
* First comparison boundary: Compare `P01`..`P03` source and test diffs against `FR-1`..`FR-4`, `PC-001`..`PC-006`, and the four local-judgment updates recorded in the changes artifact; live Entra B2B tenant configuration and OD-14 / OD-19 control-owner sign-off remain outside the local-testable boundary.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-review.md` (and parent RPI session state transitions); production code, tests, research, plan, phase details, critique, and changes record remain read-only.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only review on 2026-11-15 across all `15` modified source/test files and the reconciled `2026-11-15` RPI tracking set (`research`, `plan`, `phase-details`, `plan-critique`, and `changes`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `Core Projection-Diff Recheck and Document Derivative/Necessity Guards (P01, P01-T01, P01-T02)` | Reconciled | Markers checked `[x]`; `projection.py`, `data_protection.py`, `ai.py`, and `ai_eval.py` match FR-1, FR-3, FR-4, and `PC-001`/`PC-002`/`PC-006`. |
| `P02` (`P02-T01`, `P02-T02`) | `Post-Provider Visibility Rechecks and Document Fallback Wiring (P02, P02-T01, P02-T02)` | Reconciled | Markers checked `[x]`; `ai_tasks.py`, `store.py`, `assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`, and `server.py` match FR-2..FR-4 and `PC-001`..`PC-006`. |
| `P03` (`P03-T01`) | `Regression Tests and Focused Tier Validation (P03, P03-T01)` | Reconciled | Markers checked `[x]`; `13` focused regression test methods added across the three locked canonical test files (`0` removed) and `858` focused tests + `ruff` + `mypy` passed. |
| `## Follow-Up Items` | External OD-14 / OD-19 (`ZF_REASON_ROLES`) sign-off and live Entra B2B tenant configuration | Reconciled | Preserved outside active `Pxx`/`Pxx-Txx` scope in both the plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/projection.py` | Added `normalize_visibility_text`, `withheld_case_values`, side-effect-free `project_case_visibility`, `withheld_scope_values`, `contains_withheld_value`, and `redact_staff_detail` post-provider rechecks on `funding["draft"]`, `documents[].summary`, `derivative_text`, and `necessity_exception.reason` | Diff verified; visible projected scalars subtracted; raw dict and list `measure_decisions` supported | Passed (`test_data_protection`, `test_ai_tasks`, `test_role_endpoint_inventory`, `ruff`, `mypy`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai.py`, `src/agents/src/zava_forward/agents/ai_eval.py` | Enforced `APPROVED_DERIVATIVE` (`reviewed_redacted`), constructed-only `synthetic_safe`, human-approved scoped `validate_necessity_exception`, resident `ai_data_use_consent`, and `FORBIDDEN` output hold in `Ai.look_at`; tagged `PUBLIC_DOCUMENT` in `ai_eval.py` | Diff verified; intact uploaded documents default-deny before any provider call | Passed (`23` tests in `test_data_protection`, `20` tests in `test_ai_eval`, `ruff`, `mypy`) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/ai_tasks.py`, `src/core/src/zava_forward/core/store.py` | Enforced post-provider visibility/permission recheck at the start of `ai_tasks.finish.publish`, stripped `ai_text` from responses while keeping clean `ai_output` on permitted quarantine/attribution records, added `_record_view`, `Store._rec_view`, `ai_priority` rechecks, `live_report(store, user)`, and `add_document` / `read_document` derivative/exception + intact storage/manual-read/download preservation | Diff verified; explicit-file `ruff format` also formatted untouched lines in `store.py` without behavioral impact (`ruff` and `mypy` green) | Passed (`test_ai_tasks`, `test_ai_provider_payload_spy`, `test_ai_statement_sources`, `test_documents`) | Reconciled |
| `P02-T02` | `src/core/src/zava_forward/core/assistants.py`, `chat_isolation.py`, `chat_panel.py`, `chatthreads.py`, `continuity.py`, `src/api/src/zava_forward/api/server.py` | Enforced capability-intersection hold in `assistants.complete` and per-caller role visibility + note holds in `assistants._view`, generalized chat answer/citation/resumed-thread scrubbing (`ChatNotFound` `404` on revoked case), broadened `continuity_export` `limited_export` to require reason + resident + finance visibility, and wired HTTP routes in `server.py` | Diff verified; explicit-file `ruff format` also formatted untouched lines in `assistants.py` without behavioral impact | Passed (`test_assistants`, `test_assistants_dispatch`, `test_chat_isolation`, `test_chat_panel`, `test_continuity`, `test_continuity_epoch_export`) | Reconciled |
| `P03-T01` | `src/core/tests/test_data_protection.py`, `src/api/tests/test_ai_tasks.py`, `src/api/tests/test_role_endpoint_inventory.py` | Added `13` focused regression test methods (`5` core, `6` JSON/SQLite task & HTTP routes, `2` cross-role inventory & document fallback) within locked `<= 18` cap and `0` removals | Verified via `git diff` (`13` added `def test_*`, `0` deleted tests) | Passed (`240` core + `20` agents + `598` API = `858` focused tests `OK`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`projection.py`) | Added pure `project_case_visibility(user, raw_case)` (handling dict and list `measure_decisions`) instead of calling `Store.detail(cid, user)` inside AI rechecks | `test_permitted_read_controls_full_count_top_eight_facts_and_cache` proved `Store.detail` invokes `work_context` / `recommend_handover` side effects; local judgment | Documented in `changes.md` under `Implementation-Time Plan and Detail Updates` | Not needed (preserves `PC-003` projection semantics without side effects) | Reconciled |
| `P02-T01` (`store.py`) | Retained `Store._facts` `c["reason"]` prompt interpolation contract while enforcing post-provider `withheld_scope_values` holds | `LegacyRoleProjection` in `test_ai_provider_payload_spy.py` locks the exact legacy `_facts` prompt string; local judgment | Documented in `changes.md`; verified with `test_ai_provider_payload_spy` and `test_funding_draft_excludes_vulnerability_reason...` | Not needed (preserves `PC-001` and `PC-003` post-provider protection and legacy spy invariant) | Reconciled |
| `P02-T02` (`assistants.py`) | Evaluated `assistants.complete` against the intersection of `withheld_case_values` across `cap_roles` (loading live SQL `cases.body`) while `assistants._view` applies per-caller `withheld_case_values` + `withheld_scope_values` | Capability roles with legitimate `reason` access (`Retrofit Programme Manager`, `Resident Liaison Officer`) require clean completion while narrower readers (`Programme Support Officer`) are held on read/CSV/export; local judgment | Documented in `changes.md`; verified across `test_assistants`, `test_continuity_epoch_export`, and `test_role_endpoint_inventory` | Not needed (preserves FR-2 across both completion and per-reader projection) | Reconciled |
| `P02-T02` (`chat_panel.py`) | Kept `TOOLISH` pre-parse and applied `iso._withheld` on parsed answer and citations after `parse_reply(raw, sources)` | `test_uncited_or_foreign_citation_falls_back_to_cited_case_rules` verifies replies rejected by `parse_reply` route to `decision-rules-fallback` rather than raw `withheld`; local judgment | Documented in `changes.md`; verified in `test_chat_panel` and `test_ai_tasks` | Not needed (preserves FR-2 and existing fallback contract) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six single-pass critique findings (`PC-001`..`PC-006`) and the documented lexical-paraphrase residual risk in `.copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-plan.md` are fully implemented and regression-tested.
* Material revisions: None required during implementation; all four discoveries were local-judgment refinements preserving approved requirements, scope, architecture, and acceptance criteria.
* Dependent-work pause assessment: No material revision occurred and no dependent phase bypassed plan order (`P01` -> `P02` -> `P03`).
* Justification assessment: Fully supported by deterministic unit and HTTP test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Organisational control-owner confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration | Requires named governance/DPO sign-off and cloud tenant administration outside local-testable repository code | Programme / security governance owners | Open external governance/tenant follow-up; kept distinct from active `P01`..`P03` acceptance scope |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Parallel record-scrubbing helpers and remaining ADR-0006 `pyproject.toml` typing/format exclusions on touched core modules

* Related scope: `P01-T01`, `P02-T01`, `P02-T02`
* Evidence: `src/core/src/zava_forward/core/ai_tasks.py` (`_record_view`), `src/core/src/zava_forward/core/store.py` (`_rec_view`), `src/core/src/zava_forward/core/chat_isolation.py` (`scrub_thread`), and `src/core/pyproject.toml` (`[tool.ruff.format].exclude` and `[[tool.mypy.overrides]]` `ignore_errors = true` on `projection`, `ai_tasks`, `store`, `assistants`, `chat_isolation`, `chatthreads`, `continuity`)
* Impact: Non-blocking maintainability / engineering-quality opportunity only; runtime behavior, type checking, lint/format gates, and all acceptance criteria are fully conformant. Consolidating record-level withheld-value scrubbing and graduating `projection.py` / `ai_tasks.py` into strict `mypy` and default `ruff format` reduces future drift risk.
* Destination: follow-up
* Smallest useful next action: Track optional DRY helper consolidation and `pyproject.toml` M6 typing/format graduation as ranked engineering-quality follow-up items for user selection at the post-Review checkpoint.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | follow-up | User-selectable post-Review follow-up backlog | Non-blocking engineering-quality / M6 typing & DRY cleanup opportunity outside Issue #116 acceptance defects |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Organisational control-owner confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration (external Issue #116 governance/tenant scope).
* Optional M6 graduation of `projection.py` and `ai_tasks.py` from `src/core/pyproject.toml` `ignore_errors = true` / format-exclude lists and consolidation of AI/chat record visibility-scrubbing helpers (`RV-001`).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`, `P02`, and `P03` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python -m ruff check . && python -m ruff format --check .` | `src/core`, `src/agents`, `src/api` | Passed | `All checks passed!`; `281`, `62`, and `196` files formatted respectively |
| `python -m mypy src tests` | `src/core`, `src/agents`, `src/api` | Passed | `Success: no issues found` in `334` (`src/core`), `66` (`src/agents`), and `221` (`src/api`) source files |
| `PYTHONPATH=tests python -m unittest ... -q` | `src/core` (`13` focused modules) | Passed | `Ran 240 tests in 31.867s - OK (skipped=19)` |
| `PYTHONPATH=tests:../core/tests python -m unittest tests.test_ai_eval -q` | `src/agents` | Passed | `Ran 20 tests in 6.409s - OK` |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest ... -q` | `src/api` (`16` focused unit & HTTP modules) | Passed | `Ran 598 tests - OK` |
| `python3 tools/rpi-checks.py --all` | Repository-wide full gate | Skipped | Explicitly excluded by caller prompt (`Validation Tier (Focused): Do NOT run tools/rpi-checks.py --all`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every functional requirement (`FR-1`..`FR-4`), non-functional requirement (`NFR-1`..`NFR-2`), acceptance criterion, test-bound lock (`13 <= 18` added methods, `0` removed), and single-pass critique disposition (`PC-001`..`PC-006`) is satisfied with deterministic unit and HTTP verification across JSON, SQLite, and API layers and zero material or implementation defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Ranked post-Review follow-up selection (`RV-001` engineering-quality items and external OD-14/OD-19 + Entra B2B governance) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`ruff check`, `ruff format --check`, `mypy src tests`, and `858` focused `unittest` tests across `src/core`, `src/agents`, and `src/api`); `tools/rpi-checks.py --all` skipped per explicit caller instruction
* Blockers: None
