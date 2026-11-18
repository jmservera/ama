<!-- markdownlint-disable-file -->
# Review: Issue #221 Operator Suspension, Incident and Restart Record (Criteria 5 & 6)

## Scope and Evidence

* Task ID: issue-221-operator-suspension-2235
* Review date: 2026-11-14
* Review scope: full task (`P01`, `P02`: `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Issue #221 Criteria 5 (`RULE-024` distinct human `restart_authority` naming, validation, and multi-actor separation) and 6 (`NFR-014` automated end-to-end suspension, manual fallback continuity, statutory Awaab's Law hazard continuity, and authorised restart drill across `src/core` and `src/api`), static/runtime validation (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-4`), critique dispositions (`PC-001`..`PC-004`), implementation-time Entra OID cross-provider identity separation update, and canonical plan `## Follow-Up Items`.
* Plan: .copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-221-operator-suspension-2235-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/issue-221-operator-suspension-2235-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/issue-221-operator-suspension-2235-research.md (`C1`–`C16`); direct source and test inspection of `src/core/src/zava_forward/core/restart_authority.py`, `src/core/src/zava_forward/core/governance.py` (including AST diff check against `HEAD` confirming only `release_record`, `breach_record`, and `breach_restart` changed semantically), `src/core/src/zava_forward/core/continuity.py`, `src/core/README.md`, `src/core/tests/test_operator_suspension_drill.py`, `src/core/tests/test_governance.py`, and `src/api/tests/test_operator_suspension.py`; verified `mypy`, `ruff check`, `ruff format --check`, and `unittest` runs across `src/core` and `src/api`.

## Opening Review State

* Interpreted review goal: Independently verify that the completed `P01` and `P02` implementation satisfies Issue #221 Criteria 5 (`RULE-024`) and 6 (`NFR-014`), plan requirements (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-4`), and plan critique dispositions (`PC-001`..`PC-004`) without breaking emergency containment, privacy redaction, or statutory hazard response continuity.
* Review scope: full task (`P01`, `P02`)
* Evidence readiness: Ready; research, plan, phase details, one-pass plan critique, reconciled changes log, and passing validation evidence are present and internally consistent.
* Acceptance basis: Issue #221 Criteria 5 & 6; `docs/brds/agentic-retrofit-programme-brd.md` (`RULE-024`, `RULE-020`, `AC-078`, `OD-35`); `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (`FR-053`, `FR-028`, `AC-072`, `NFR-014`); `docs/reference/method/operator-suspension-drill-protocol.md`; `plan.md` (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-4`, `PC-001`..`PC-004`).
* First comparison boundary: Reconcile `P01` and `P02` plan markers, phase details, and changes record against actual source and test diffs before evaluating validation coverage and follow-up routing.
* Active read-only boundaries: Canonical review artifact creation only; zero source, test, research, plan, details, critique, or changes mutations during Review.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed 2026-11-14 across the full task boundary (`P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, `PC-001`..`PC-004`, implementation-time Entra OID separation update, `mypy`/`ruff`/`unittest` validation outputs, and `git diff` + AST verification).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01: Core RULE-024 Restart Authority Validation (P01-T01, P01-T02)` | Reconciled | `restart_authority.py`, `governance.py`, `continuity.py`, and `src/core/README.md` match planned `FR-1`..`FR-3` and critique `PC-001`..`PC-003`. |
| `P02` (`P02-T01`) | `P02-T01: Core RULE-024 Unit Tests and End-to-End NFR-014 Drill Suite` | Reconciled | `src/core/tests/test_operator_suspension_drill.py` and `src/core/tests/test_governance.py` verify JSON and SQL stores, three-actor separation, statutory hazard continuity, and safety-hold independence without modifying `pyproject.toml` (`PC-004`). |
| `P02` (`P02-T02`) | `P02-T02: API HTTP End-to-End NFR-014 & RULE-024 Drill Suite and Validation` | Reconciled | `src/api/tests/test_operator_suspension.py` (`test_nfr_014_http_breach_hazard_and_rule_024_restart_drill`) verifies the complete 8-step `NFR-014` HTTP + `TrustedProxyProvider` + `SqlStore` + `Assistants` drill while preserving existing `test_nfr_014_suspension_and_manual_fallback_drill`. |
| Implementation-time update | `Implementation-Time Plan and Detail Updates` (`actors_for_store` + `release_record` `actor_snapshot`) | Reconciled | Reconciled across `AC-1` in `plan.md`, `P02-T02` in `phase-details.md`, and `changes.md`. |
| `Follow-Up Items` | `Live operational OD-35 appointment and witnessed human drill record` | Reconciled | Preserved outside active `Pxx`/`Pxx-Txx` software scope in both `plan.md` and `changes.md`; `docs/reference/method/operator-suspension-drill-protocol.md` remains untouched. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/restart_authority.py` | Created strictly typed `RULE-024` validator (`RULE_024`, `UNAPPOINTED_RESTART_AUTHORITY`, `actor_snapshot`, `actors_for_store`, `reject_automatic_restart`, `validate_restart_authority`, `ensure_distinct_restart_actor`) with static non-echoing messages (`PC-002`) and word-boundary placeholder/AI/actor matching (`PC-003`). | Direct inspection of `restart_authority.py` | `mypy` (`0` errors in 329 files), `ruff check` & `ruff format --check` (`0` errors), `RestartAuthorityUnitTest` (`ok`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/governance.py`, `src/core/src/zava_forward/core/continuity.py`, `src/core/README.md` | Enforced `RULE-024` authority validation, `controls.evidence_text` memory-citation refusal, `reject_automatic_restart`, `PermissionError` authority mismatch/invalidity contract, and multi-person separation across `release_record`, `breach_record`, `breach_restart`, `suspend`, `restart_propose`, and `restart_decide` (`PC-001`, `PC-002`), while preserving omitted-authority emergency containment (`UNAPPOINTED_RESTART_AUTHORITY`) and audience-limited redaction. | Direct diff and AST inspection (`breach_record`, `breach_restart`, `release_record` are the only semantically changed functions in `governance.py`) | `mypy`, `ruff`, `151` `src/core` tests (`ok`), `138` `src/api` tests (`ok`, including privacy canary `test_continuity_epoch_export` and `test_rai_harm_threshold_incident`) | Reconciled |
| `P02-T01` | `src/core/tests/test_operator_suspension_drill.py`, `src/core/tests/test_governance.py` | Added strictly typed unit and `Store`/`SqlStore` end-to-end `RULE-024` & `NFR-014` drill tests proving AI gate blocking, paused-home workflow hold, unaffected manual `log_call`, unimpeded statutory Awaab's Law hazard raise/referral/receipt/acceptance/repair progression on paused homes, safety-hold independence, negative restart matrix, and distinct-human restart. | Direct inspection and test execution logs | `PYTHONPATH=src:tests python3 -m unittest test_operator_suspension_drill test_governance ... -v` (`ok`) | Reconciled |
| `P02-T02` | `src/api/tests/test_operator_suspension.py` | Added `test_nfr_014_http_breach_hazard_and_rule_024_restart_drill` exercising the full 8-step `NFR-014` HTTP + `TrustedProxyProvider` + `SqlStore` + `Assistants` protocol, including pending/ready/in-flight containment, snapshot completeness, manual + statutory hazard fallback continuity, `"Keep suspended"` retention, negative HTTP 400/403 `RULE-024` matrix, distinct OID-bound `ai_restart` clearance, `actual_hold=True` retention, and intact ledger verification. | Direct inspection and test execution logs | `mypy` (`0` errors in 280 files), `ruff` (`0` errors), `138` `src/api` continuity/suspension/RAI tests (`ok`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `AC-1`, `P01-T01`, `P01-T02`, `P02-T02` | Added `actors_for_store` (resolving OID-linked staff roster rows) plus `display_email` and `bound` matching in `restart_authority.py`, and recorded `actor=actor_snapshot(user)` on `governance.release_record` with `self.staff.get(rel_email)` lookup in `governance.breach_restart` so Entra `TrustedProxyProvider` pseudonymous principals (`e-<12hex>@entra.invalid`) cannot self-designate their roster identity or self-approve across auth providers. | Triggered during `P02-T02` HTTP `TrustedProxyProvider` drill verification; directly enforces confirmed user requirement ("requiring distinct human restart authority, rejecting blank/placeholder/self-approval"); no new user decision required. | Reconciled in `plan.md` (`AC-1`), `phase-details.md` (`P02-T02`), and `changes.md` (`Implementation-Time Plan and Detail Updates`). | Immediately relevant current-state update preserving approved intent; critique `PC-001`..`PC-004` remained valid and no repeat critique was required or run. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All 4 findings in `.copilot-tracking/reviews/plans/2026-11-14/issue-221-operator-suspension-2235-plan-critique.md` (`PC-001` non-short-circuiting actor sequences and unconditional `"Keep suspended"` separation; `PC-002` non-echoing messages and `PermissionError` contract; `PC-003` valid `controls.MEMORY_REF` inputs and boundary matching; `PC-004` clean isolated HTTP drill fixture, post-breach `Release` prerequisite, safety-hold independence, and zero `pyproject.toml` edits) were applied in code and verified by tests.
* Material revisions: None. The Entra `actors_for_store` cross-provider identity check closed a concrete auth-provider representation detail within the approved `RULE-024` distinct-human requirement without altering scope, architecture, or acceptance criteria.
* Dependent-work pause assessment: Execution followed strict plan order (`P01-T01` -> `P01-T02` -> `P02-T01` -> `P02-T02`) with no early resumption or bypassed dependency.
* Justification assessment: Fully supported by code, AST comparison, and runtime test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live operational `OD-35` appointment and witnessed human drill record | `docs/reference/method/operator-suspension-drill-protocol.md` forbids agents from fabricating real human `OD-35` appointments or witnessing live operational sign-off; software retains `actual_hold=True` until appointed. | Building Safety Lead, Executive Sponsor, and Project Owner before operational pilot activation | Distinct follow-up route preserved outside active software scope (`docs/reference/method/operator-suspension-drill-protocol.md` verified unmodified). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No defects, decision gaps, or material evidence gaps were found within the assessed software task boundary.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Whole-file Ruff formatting touched unchanged legacy lines in `governance.py`

* Related scope: `P01-T02`
* Evidence: `src/core/src/zava_forward/core/governance.py` (`git diff --stat` shows formatting churn outside `release_record`, `breach_record`, and `breach_restart`; AST comparison against `HEAD` verified `['breach_record', 'breach_restart', 'release_record']` are the sole semantically modified functions, and `python3 -m ruff check . && python3 -m ruff format --check .` passes with `0` issues).
* Impact: Non-functional diff noise during human pull request inspection only; zero runtime, typing, lint, audit-digest, or behavioral impact.
* Destination: follow-up
* Smallest useful next action: Optional non-blocking hygiene note for human PR review that untouched functions in `governance.py` are AST-identical `ruff format` layout updates only; no code change required.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow-up` | Optional PR reviewer context note (no active software fix required) | Non-functional formatting scope observation verified AST-identical outside the 3 target methods |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Live operational `OD-35` restart authority appointment and witnessed human execution of `docs/reference/method/operator-suspension-drill-protocol.md` remain human governance prerequisites before live operational pilot activation (`actual_hold=True` remains enforced in code).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: Local git commit on `feat/ai-221-operator-suspension-2235` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (`AC-4` caller closeout step).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 329 source files` (0 errors) |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | `All checks passed!` and `276 files already formatted` (0 errors) |
| `PYTHONPATH=src:tests python3 -m unittest test_operator_suspension_drill test_governance test_hazard_referral test_rai_release test_rai_release_invalidation test_rai_threshold_live_approval_guard -v` | `src/core` | Passed | `Ran 151 tests in 42.047s — OK (skipped=17)`; full `src/core` discovery also ran 3,414 tests with 0 failures in any governance, continuity, workflow, or store module (only 3 unrelated IoT/CLI modules failed due to uninstalled optional `azure-iot-hub` SDK / console scripts in bare system Python outside an installed `.venv`) |
| `python3 -m mypy` | `src/api` | Passed | `Success: no issues found in 280 source files` (0 errors) |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | `All checks passed!` and `196 files already formatted` (0 errors) |
| `PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests python3 -m unittest test_operator_suspension test_continuity test_continuity_epoch_export test_rai_harm_threshold_incident test_assistant_restart_non_replenishment -v` | `src/api` | Passed | `Ran 138 tests in 126.203s — OK (skipped=39)` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every software requirement (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`), acceptance criterion (`AC-1`..`AC-3`, plus `AC-4` validation and RPI artifact deliverables), and critique disposition (`PC-001`..`PC-004`) for Issue #221 Criteria 5 (`RULE-024`) and 6 (`NFR-014`) is implemented, reconciled, and proven by passing static analysis (`mypy`, `ruff`) and 289 targeted unit and end-to-end drill tests across `src/core` and `src/api` with zero defects or decision gaps.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Building Safety Lead, Executive Sponsor, and Project Owner: appoint live operational `OD-35` authority and witness human execution of `docs/reference/method/operator-suspension-drill-protocol.md` prior to pilot release (`RV-001` requires no code change) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `mypy` (`0` errors across 329 `src/core` + 280 `src/api` files), `ruff check` & `ruff format --check` (`0` errors across `src/core` + `src/api`), `unittest` (`151` `src/core` + `138` `src/api` relevant tests passed, `0` failed)
* Blockers: none
