<!-- markdownlint-disable-file -->
# Review: Issue #133 Criterion 5 — No Causation, Blame, or Savings Promise in Generated or Templated Aftercare Text

## Scope and Evidence

* Task ID: rpi-133-no-causation-blame-savings-20261115T0316Z
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Functional requirements `FR-1`..`FR-5`, non-functional requirements `NFR-1`..`NFR-2`, top-level `## Acceptance Criteria`, critique dispositions `PC-001`..`PC-005`, `src/core` (`aftercare.py`, `aftercare_intake.py`, `quality.py`, `README.md`, `test_aftercare.py`, `test_aftercare_intake.py`), and `src/api` (`test_aftercare_served.py`)
* Plan: .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/133-no-causation-blame-savings-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/133-no-causation-blame-savings-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/133-no-causation-blame-savings-research.md, working-tree git diff across `src/core` and `src/api`, focused-tier validation runs across `src/core`, `src/api`, and `src/agents`, and an independent read-only code-review subagent lens

## Opening Review State

* Interpreted review goal: Verify once against canonical RPI evidence that Criterion 5 of Issue #133 (`No causation, blame or savings promise appears in any generated or templated text`) satisfies `FR-1`..`FR-5`, `NFR-1`..`NFR-2`, all plan acceptance criteria, and critique dispositions `PC-001`..`PC-005` without regressions or scope drift.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready — research, plan, phase details, single-pass plan critique, reconciled changes record, working-tree diff, and focused-tier validation outputs are complete and consistent.
* Acceptance basis: `## Functional Requirements` (`FR-1`..`FR-5`), `## Non-Functional Requirements` (`NFR-1`..`NFR-2`), `## Acceptance Criteria`, and `## Critique Disposition` (`PC-001`..`PC-005`) in .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md
* First comparison boundary: Reconcile `P01`, `P02`, and `P03` markers and completed-work records against the working-tree diff and critique dispositions.
* Active read-only boundaries: Read-only across source code, tests, docs, research, plan, phase details, plan critique, and changes record; write authority limited strictly to this canonical review record and parent RPI session state.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass full-boundary comparison on 2026-11-15 across all six planned tasks (`P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, `P03-T01`, `P03-T02`), critique dispositions `PC-001`..`PC-005`, focused-tier lint/type/unit/served-HTTP validation outputs, and an independent read-only code-review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Core `neutral_text` normalization, clause-stop lookahead, and lexical expansion | Reconciled | `_normalize_for_guard`, `neutral_violations`, clause-scoped `_UNCERTAIN` / `_NEGATED_CLAIM`, and expanded `BANNED_PHRASES` / `_PARAPHRASE_SPECS` match `FR-1`..`FR-3` and `PC-001`. |
| `P01` / `P01-T02` | `AftercareRegister` boundary and snapshot neutrality enforcement | Reconciled | All register write, template, `FR-036` concern-pack draft/review, and `from_state` snapshot paths enforce `neutral_text` while keeping household `statement` and `representative_basis` verbatim (`FR-4`, `PC-002`). |
| `P02` / `P02-T01` | `AftercareService` plain-language write, pack-proposal, template, and restore guards | Reconciled | `NEUTRAL_NOTE_ERROR`, `_free_text(..., require_neutral=True)`, `_context_errors`, bounded `propose_pack` / `review_pack` service methods, wrapped service templates, and `_validate` receipt checks match `FR-5` and `PC-003`; two low-severity edge-case hardening opportunities noted in `RV-001`. |
| `P02` / `P02-T02` | Handover quality `add_aftercare` guard and `src/core/README.md` update | Reconciled | `QualityMixin.add_aftercare` checks `controls.is_memory_reference` and `aftercare.neutral_violations` inside `_quality_operation` before mutating case records (`FR-5`, `PC-004`), and `src/core/README.md` documents the expanded boundary. |
| `P03` / `P03-T01` | Focused core, intake, and served HTTP neutral-boundary regression suites | Reconciled | Added `+7` (`test_aftercare.py`), `+5` (`test_aftercare_intake.py`), and `+3` (`test_aftercare_served.py`) tests within locked budgets (`<= +12`, `<= +8`, `<= +4`) with zero new HTTP routes; optional explicit `App` restart readback after `400` noted in `RV-002`. |
| `P03` / `P03-T02` | `ruff`, `mypy`, `test_aftercare*`, and cross-cutting invariant validation | Reconciled | Package-level `ruff check`, `ruff format --check`, strict `mypy`, `test_aftercare*`, `test_quality_procurement`, `test_content_standard`, `test_role_endpoint_inventory`, `test_role_matrix`, and `test_epic104_bounded_ai_invariants` all passed (`NFR-1`, `NFR-2`, `PC-005`). |
| `Follow-Up Items` | Issue #133 Criterion 1 and DPO sign-off on outcome data | Reconciled | Kept outside active `P01`..`P03` completion claims in both the plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/aftercare.py` | Dual invisible-character normalization (`_INVISIBLE` deletion + `_INVISIBLE_SPACE` folding), NFKC, curly-quote folding, newline-to-semicolon clause breaks, bounded `_CLAUSE_STOP` lookaheads, and expanded lifestyle-blame / measure-causation / savings rules; adversarial 5k–10k near-miss inputs run in `<4 ms`. | `neutral_violations` and `neutral_text` in `src/core/src/zava_forward/core/aftercare.py` | `src/core` `ruff`, `mypy`, `test_aftercare*` (`Ran 131 tests, OK`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/aftercare.py` | Guarded `_context` keys/values, `intake_form`, `intake_errors`, `raise_concern`, `record_outcome`, `set_remedy` (all statuses), `record_closure`, `view`, `evaluator_view`, `propose_pack`, `review_pack`, and `from_state` while preserving household `statement` and `representative_basis` verbatim. | `AftercareRegister` methods and `from_state` in `src/core/src/zava_forward/core/aftercare.py` | `src/core` `test_aftercare*` (`Ran 131 tests, OK`) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/aftercare_intake.py` | Added `NEUTRAL_NOTE_ERROR`, guarded `/outcome`, `/remedy`, `/sensor-context`, and bounded `VIEW_ROLES` / `owner_label`-gated `propose_pack` / `review_pack` without adding HTTP routes, wrapped all templated outputs with `neutral_text`, and validated receipt fields and unknown-owner labels in `_validate`. | `AftercareService` and `_validate` in `src/core/src/zava_forward/core/aftercare_intake.py` | `src/core` `test_aftercare_intake.py`, `src/api` `test_aftercare_served.py`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, `src/agents` `test_epic104_bounded_ai_invariants.py` | Reconciled with non-blocking hardening note `RV-001` |
| `P02-T02` | `src/core/src/zava_forward/core/quality.py`, `src/core/README.md` | Enforced `controls.is_memory_reference` and `aftercare.neutral_violations` inside `_quality_operation` before mutating `rec["aftercare"]`, preserving `403` precedence for unauthorized callers; documented #133 neutral-text guarantees in `src/core/README.md`. | `QualityMixin.add_aftercare` in `src/core/src/zava_forward/core/quality.py` and `## Aftercare concern route and evaluator view (#133)` in `src/core/README.md` | `src/core` `test_quality_procurement.py` (`Ran 136 tests, OK`), `src/api` `test_role_matrix.py`, `test_aftercare_served.py` | Reconciled |
| `P03-T01` | `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/api/tests/test_aftercare_served.py` | Added 15 focused tests (`+7`, `+5`, `+3`, zero removals) proving obfuscation refusal, multi-clause uncertainty refusal, verbatim resident statements, snapshot/receipt tamper refusal, HTTP `400` non-echo/non-mutation, and recursive neutrality across API payloads and `aftercare.js` screen literals. | Test diffs across `src/core/tests/` and `src/api/tests/` | All `src/core` and `src/api` suites exited `0` | Reconciled with minor restart-readback hardening note `RV-002` |
| `P03-T02` | `.copilot-tracking/changes/2026-11-15/133-no-causation-blame-savings-changes.md` | Executed full focused-tier lint, format, strict type-check, and unit/served-HTTP/invariant test matrix across `src/core`, `src/api`, and `src/agents`. | `## Validation Record` in `.copilot-tracking/changes/2026-11-15/133-no-causation-blame-savings-changes.md` | All 8 recorded validation groups passed with exit code `0` | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (local judgment recorded in changes log) | Evaluated both invisible-deleted and invisible-to-space normalized variants (`"guar\u00adanteed"` and `"will\u200bsave"`), added `blam(e\|es\|ed\|ing)` inflection matching, and used `(?:%\|\b)` after percentage numerals (`"20% on heating"`). | Triggered during `P03-T01` adversarial test execution; no user decision needed because changes strictly strengthened `FR-1` and `FR-3` within approved design. | Documented in `.copilot-tracking/changes/2026-11-15/133-no-causation-blame-savings-changes.md` under `P03-T01` and `## Implementation-Time Plan and Detail Updates`. | Not needed — preserved approved plan, scope, acceptance criteria, and `PC-001`..`PC-005` dispositions. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five findings (`PC-001`..`PC-005`) in `.copilot-tracking/reviews/plans/2026-11-15/133-no-causation-blame-savings-plan-critique.md` have recorded `Resolved` dispositions in `.copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md` and are honored in code and tests (`_UNCERTAIN` / `_NEGATED_CLAIM` span stops, exact `closure["owner"]` / `recorded_by` / `reviewer_function` / `not_needed` fields, `NEUTRAL_NOTE_ERROR` self-check, `VIEW_ROLES` + `owner_label` pack gating, `_validate` unknown-owner receipt check, `_quality_operation` `403`-before-`400` ordering, package-level `ruff format --check` respecting excludes, inline typed `checklist_for` quality fixture, and `+7`/`+5`/`+3` test-addition budgets).
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No material revision occurred; phases executed strictly in dependency order (`P01` -> `P02` -> `P03`).
* Justification assessment: Local regex/normalization refinements in `P01-T01` are fully supported by unit test evidence and preserve confirmed user intent.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Issue #133 Criterion 1 (`Household or representative can raise a concern through an accessible route without needing digital access`) and DPO sign-off on outcome data | User scoped this RPI loop specifically to Criterion 5 (`No causation, blame or savings promise appears in any generated or templated text`). | Separate Issue #133 RPI slice for Criterion 1 plus human DPO review/sign-off. | Open distinct follow-up route; properly excluded from Criterion 5 active tasks and completion claims. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Harden `AftercareService` intra-`VIEW_ROLES` owner-precedence ordering and `homes=None` `home_ref` error mapping

* Related scope: `P02-T01`
* Evidence: `src/core/src/zava_forward/core/aftercare_intake.py` (`record_outcome`, `set_remedy`, `review_pack`, `record_concern`, `record_closure`, `handle`, and `_route`)
* Impact: Callers outside `VIEW_ROLES` receive `403` ahead of `400` validation as required, and `App` configures a `homes` allowlist so arbitrary `home_ref` strings are rejected before reaching `AftercareRegister`. However, two secondary edge cases remain for direct or non-owner callers: (1) a caller inside `VIEW_ROLES` who is not the named concern owner (or calls on an unassigned concern) hits stateless `_free_text` validation (`400`) before `_txn` checks per-record `owner` (`403`), and `_route` checks required JSON string keys before dispatching to `self._staff`; (2) a direct library caller constructing `AftercareService(store, homes=None)` without a `homes` allowlist and passing a banned phrase inside `home_ref` hits `AftercareRegister`'s `ValueError` in `handle()`, which formats the matched canonical rule token rather than a field-keyed `ValidationError`. Neither path allows prohibited text to persist, register, or render.
* Destination: distinct follow-up
* Smallest useful next action: Move per-field validation after concern-owner lookup (and coarse `_staff` checks ahead of `_route` body key extraction) and validate `home_ref` with `neutral_violations` when `self.homes is None` in a small hardening follow-up.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Add explicit `App` restart SQLite readback assertion after rejected HTTP `400` calls in `test_aftercare_served.py`

* Related scope: `P03-T01`
* Evidence: `src/api/tests/test_aftercare_served.py` (`test_served_write_routes_refuse_non_neutral_notes_without_echo_or_mutation` and `test_served_quality_aftercare_route_refuses_non_neutral_note_and_preserves_403`) compared with `P03-T01` prose in `.copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md`
* Impact: Raw disk non-mutation is already proven in `src/core/tests/test_aftercare_intake.py` (`self.path.read_bytes()` equality) and live SQLite `GET` / `self.store` non-mutation is proven in `src/api/tests/test_aftercare_served.py`, but cycling `self.stop(); self.store.db.close(); self.start()` after the `400` responses would mirror `test_replay_conflict_and_restart_readback` directly across a full SQLite reopen cycle.
* Destination: distinct follow-up
* Smallest useful next action: Append a `self.stop(); self.store.db.close(); self.start()` readback check to the `400` non-mutation test in `src/api/tests/test_aftercare_served.py` during the `RV-001` hardening follow-up.

## Defects

* None blocking Issue #133 Criterion 5 acceptance criteria (two non-blocking `Low`-severity hardening items routed as distinct follow-up work in `RV-001` and `RV-002`).

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | distinct follow-up | Optional `AftercareService` edge-case hardening follow-up (`aftercare_intake.py`) | Non-blocking secondary edge case (`homes=None` library callers and intra-`VIEW_ROLES` non-owner `400`-before-`403` ordering); zero persistence/render leak on `App`. |
| `RV-002` | distinct follow-up | Optional served-test restart readback assertion (`test_aftercare_served.py`) | Non-blocking test-depth polish; disk-byte and live SQLite non-mutation are already covered. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Harden `AftercareService` intra-`VIEW_ROLES` owner `403` ordering ahead of field validation and `homes=None` `home_ref` `ValidationError` mapping (`src/core/src/zava_forward/core/aftercare_intake.py`).
* `RV-002`: Add explicit `App` restart SQLite readback assertion after rejected `400` writes in `src/api/tests/test_aftercare_served.py`.
* Plan follow-up: Prove Issue #133 Criterion 1 (accessible non-digital household/representative concern route) and obtain human DPO sign-off on outcome data.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`, `P02`, and `P03` are complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python -m ruff check` | `src/core`, `src/api`, `src/agents` | Passed | `All checks passed!` across all three packages |
| `python -m ruff format --check` | `src/core`, `src/api`, `src/agents` | Passed | `281`, `196`, and `62` files already formatted |
| `python -m mypy --no-incremental --cache-dir /dev/null` | `src/core`, `src/api`, `src/agents` | Passed | `Success: no issues found` across `334`, `280`, and `66` source files |
| `python -m unittest discover -s tests -p "test_aftercare*.py" -q` | `src/core` | Passed | `Ran 131 tests in 178.267s — OK (skipped=15)` (opt-in disposable SQL Server harness tests skipped when `ZF_TEST_MSSQL_URL` is unset) |
| `python -m unittest discover -s tests -p "test_quality_procurement.py" -q` | `src/core` | Passed | `Ran 136 tests in 52.947s — OK` |
| `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p "test_aftercare*.py" -q` | `src/api` | Passed | `Ran 28 tests in 12.197s — OK` |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest tests/test_content_standard.py tests/test_role_endpoint_inventory.py tests/test_role_matrix.py -q` | `src/api` | Passed | `Ran 66 tests in 14.663s — OK` |
| `PYTHONPATH=tests:../core/tests python -m unittest tests/test_epic104_bounded_ai_invariants.py -q` | `src/agents` | Passed | `Ran 22 tests in 2.374s — OK` |

## Outcome

* Outcome: Residual work
* Outcome rationale: All four top-level plan acceptance criteria, `FR-1`..`FR-5`, `NFR-1`..`NFR-2`, and `PC-001`..`PC-005` are implemented and verified green across `src/core`, `src/api`, and `src/agents` — zero causation, blame, or savings promises appear in any generated or templated aftercare text, prohibited inputs are deterministically rejected before persistence/proposal/render while resident statements stay verbatim, and all linters, strict `mypy`, and 383 executed unit/API/invariant tests pass. Two non-blocking `Low`-severity edge-case hardening items (`RV-001` and `RV-002`) were identified by independent review and are routed transparently as distinct follow-up work alongside Issue #133 Criterion 1.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | `RV-001` (`AftercareService` intra-`VIEW_ROLES` owner `403` ordering & `homes=None` `home_ref` `ValidationError`), `RV-002` (`test_aftercare_served.py` post-`400` SQLite restart readback), and Issue #133 Criterion 1 + DPO outcome-data sign-off |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: Focused tier passed (`ruff check`, `ruff format --check`, strict `mypy` across `334+280+66` files, and `131+136+28+66+22 = 383` unit/served/invariant tests; `15` opt-in MSSQL tests skipped without disposable SQL Server)
* Blockers: None
