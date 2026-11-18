<!-- markdownlint-disable-file -->
# RPI Changes: Issue #133 Criterion 5 — No Causation, Blame, or Savings Promise in Aftercare Text

## Metadata

* Task ID: rpi-133-no-causation-blame-savings-20261115T0316Z
* Related plan: .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: None
* Status basis: All six planned tasks across `P01`, `P02`, and `P03` are complete and verified against `ruff`, `mypy`, `test_aftercare*`, and cross-cutting invariant suites.

## Execution Summary

Delivered full boundary enforcement for Issue #133 Criterion 5 (`No causation, blame or savings promise appears in any generated or templated text`). Hardened `neutral_text` and `neutral_violations` in `zava_forward.core.aftercare` against Unicode NFKC/invisible/soft-hyphen obfuscation (evaluating both stripped and space-substituted variants), multi-clause uncertainty/negation leakage, resident lifestyle blame, measure-causation proof claims, and financial/energy savings promises; enforced `neutral_text` across all `AftercareRegister` staff writes, templates, `FR-036` concern-pack drafts/reviews, and `from_state` restores; enforced plain-language no-echo `ValidationError` and template/restore guards in `AftercareService` (`aftercare_intake.py`) and `Store.add_aftercare` (`quality.py`); updated `src/core/README.md`; and added 15 focused tests across `src/core` and `src/api`.

## Completed Work

### Core `neutral_text` normalization, clause-stop lookahead, and lexical expansion

* Related phase or task: `P01-T01`
* Files: `src/core/src/zava_forward/core/aftercare.py`
* What changed and why: Added `_normalize_for_guard` (Unicode NFKC, both invisible-deleted and invisible-to-space normalization variants, typographic quote/apostrophe folding, collapsed whitespace for `BANNED_PHRASES`, and newline-to-semicolon clause stops for `PARAPHRASE_PATTERNS`), exposed `neutral_violations(text) -> tuple[str, ...]`, tightened `_UNCERTAIN` and `_NEGATED_CLAIM` clause-boundary lookaheads, and expanded `BANNED_PHRASES` and `_PARAPHRASE_SPECS` across lifestyle blame, blame inflections (`blam(e|es|ed|ing)`), measure-causation proof claims, and savings/payback promises.
* Completion evidence: `neutral_violations` and `neutral_text` implemented in `aftercare.py`.
* Validation: Passed `src/core/tests/test_aftercare*.py` (`Ran 131 tests, OK (skipped=15)`), `ruff`, and strict `mypy`.

### `AftercareRegister` boundary and snapshot neutrality enforcement

* Related phase or task: `P01-T02`
* Files: `src/core/src/zava_forward/core/aftercare.py`
* What changed and why: Enforced `neutral_text` across `_context` keys/values, `intake_form`, `intake_errors`, `raise_concern` (`home_ref`, `owner`, `recorded_by`, `accessible_route`, `sensor_context`), `record_outcome` (`evidence`), `set_remedy` (`evidence` for both completed/not_needed and optional open/in_progress notes), `record_closure` (`home_ref`, `owner`), `view`, `evaluator_view` (`unknowns`, `notice`), `propose_pack`, `review_pack` (`reviewer`, `reason`, `approval`), and `from_state` restoration while keeping household `statement` and `representative_basis` verbatim.
* Completion evidence: All `AftercareRegister` write, template, pack, and snapshot paths guarded in `aftercare.py`.
* Validation: Passed `src/core/tests/test_aftercare*.py` (`Ran 131 tests, OK (skipped=15)`).

### `AftercareService` plain-language write, pack-proposal, template, and restore guards

* Related phase or task: `P02-T01`
* Files: `src/core/src/zava_forward/core/aftercare_intake.py`
* What changed and why: Added `NEUTRAL_NOTE_ERROR`, guarded `_free_text(..., require_neutral=True)` in `record_outcome` and `set_remedy` (after `VIEW_ROLES` actor check to preserve `403` precedence), guarded `_context_errors` keys/values, added bounded `VIEW_ROLES` / `owner_label(actor["role"])`-gated `propose_pack` and `review_pack` service methods without adding any HTTP model route, wrapped every templated string across `form`, `_receipt`, `_display`, `concerns`, `record_closure`, `evaluator_view`, and `_comparison` with `neutral_text`, and validated receipt neutrality in `_validate`.
* Completion evidence: `AftercareService` boundaries enforced in `aftercare_intake.py`.
* Validation: Passed `test_aftercare_intake.py`, `test_aftercare_served.py`, `test_aftercare_screen.py`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, and `test_epic104_bounded_ai_invariants.py`.

### Handover quality `add_aftercare` guard and `src/core/README.md` update

* Related phase or task: `P02-T02`
* Files: `src/core/src/zava_forward/core/quality.py`, `src/core/README.md`
* What changed and why: Guarded `Store.add_aftercare` inside `_quality_operation` against chat-memory citations (`controls.is_memory_reference`) and non-neutral causation/blame/savings phrasing (`aftercare.neutral_violations` -> `NEUTRAL_NOTE_ERROR`) before mutating case records or audit logs while preserving `403` precedence for unauthorized actors; documented the #133 neutral-text boundary rules in `src/core/README.md`.
* Completion evidence: `quality.py` and `src/core/README.md` updated.
* Validation: Passed `test_quality_procurement.py` (`Ran 136 tests, OK`) and served HTTP `/api/cases/ZF-1/quality-aftercare` tests.

### Focused core, intake, and served HTTP neutral-boundary regression suites

* Related phase or task: `P03-T01`, `P03-T02`
* Files: `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/api/tests/test_aftercare_served.py`
* What changed and why: Added 7 unit tests in `test_aftercare.py` (within `+12` budget), 5 service/restore/quality tests in `test_aftercare_intake.py` (within `+8` budget), and 3 HTTP-served tests in `test_aftercare_served.py` (within `+4` budget), including recursive payload and `aftercare.js` screen literal neutrality checks. Local judgment during `P03-T01` added dual invisible-character normalization (`_INVISIBLE` deletion + `_INVISIBLE_SPACE` substitution), `blam(e|es|ed|ing)` inflection coverage, and non-word `%` boundary handling when the new adversarial corpus caught those three edge cases.
* Completion evidence: All 15 added test methods pass alongside all existing suites.
* Validation: Passed all focused-tier linters, formatters, type-checkers, and unit/API/invariant suites below.

## Implementation-Time Plan and Detail Updates

None required; local judgment fixes within `P01-T01` (`_INVISIBLE_SPACE` dual normalization, `blame_inflections`, `%` boundary) preserved the approved plan design and acceptance criteria without scope or contract changes.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check` | `src/core`, `src/api`, `src/agents` | Passed | `All checks passed!` across all three packages |
| `ruff format --check` | `src/core`, `src/api`, `src/agents` | Passed | `281`, `196`, and `62` files already formatted |
| `mypy --no-incremental --cache-dir /dev/null` | `src/core`, `src/api`, `src/agents` | Passed | `Success: no issues found` in `334`, `280`, and `66` source files |
| `unittest discover -s tests -p "test_aftercare*.py"` | `src/core` | Passed | `Ran 131 tests in 178.267s — OK (skipped=15)` (opt-in MSSQL tests skipped without disposable SQL Server) |
| `unittest discover -s tests -p "test_quality_procurement.py"` | `src/core` | Passed | `Ran 136 tests in 52.947s — OK` |
| `unittest discover -s tests -p "test_aftercare*.py"` | `src/api` | Passed | `Ran 28 tests in 12.197s — OK` (`test_aftercare_served.py`, `test_aftercare_screen.py`) |
| `unittest tests/test_content_standard.py tests/test_role_endpoint_inventory.py tests/test_role_matrix.py` | `src/api` | Passed | `Ran 66 tests in 14.663s — OK` |
| `unittest tests/test_epic104_bounded_ai_invariants.py` | `src/agents` | Passed | `Ran 22 tests in 2.374s — OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02` all `[x]`)
* Completed-work evidence and handoff prose: Current
* Validation, blockers, remaining work, and follow-up items: Current (`focused` validation tier per repository instructions for bounded feature slice; zero blockers; zero remaining active-plan tasks)
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md, `## Follow-Up Items`
* Criterion 1 of Issue #133 (`Household or representative can raise a concern through an accessible route without needing digital access`) and DPO sign-off on outcome data remain open outside Criterion 5; tracked on Issue #133 for subsequent delivery/human review.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`; remaining active-plan markers: none
* Validation coverage: Focused tier complete (`ruff check`, `ruff format --check`, strict `mypy`, `src/core` `test_aftercare*` + `test_quality_procurement`, `src/api` `test_aftercare*` + `test_content_standard` + `test_role_endpoint_inventory` + `test_role_matrix`, `src/agents` `test_epic104_bounded_ai_invariants`)
* Blockers: None
* Current plan and detail updates: None beyond `[x]` completion markers
* Planning and critique state: Ready (`PC-001`..`PC-005` resolved)
* Follow-up items: Issue #133 Criterion 1 and DPO outcome-data sign-off
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
