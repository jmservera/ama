<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #133 Criterion 5 - No Causation, Blame or Savings Promise in Generated or Templated Text

## Metadata

* Task ID: rpi-133-no-causation-blame-savings-20261115T0316Z
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver Issue #133 Criterion 5 (`[ ] No causation, blame or savings promise appears in any generated or templated text`) via deterministic, enforce-at-boundary validation across all generated and templated aftercare text (concern acknowledgements, receipts, investigation summaries, remedy templates, evaluator view summaries, legacy quality aftercare notes, and optional `FR-036` AI concern-pack proposal drafts/summaries), preserving resident verbatim statements in `statement` / `household_statement` / `original.statement`, adding focused unit and API tests across `test_aftercare*` in `src/core` and `src/api` (respecting `src/api/pyproject.toml` `mypy_path` sharing `../core/tests`), and validating with `ruff check`, `ruff format --check`, `mypy`, and the `test_aftercare*` suites.
* Research and evidence considered:
  * .copilot-tracking/research/2026-11-15/133-no-causation-blame-savings-research.md
  * .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md
  * .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md
  * src/core/src/zava_forward/core/aftercare.py
  * src/core/src/zava_forward/core/aftercare_intake.py
  * src/core/src/zava_forward/core/quality.py
  * src/core/src/zava_forward/core/controls.py
  * src/core/src/zava_forward/core/ai_registry.py
  * src/api/src/zava_forward/api/server.py
  * src/api/src/zava_forward/api/web/aftercare.js
  * src/core/pyproject.toml
  * src/api/pyproject.toml
  * src/core/tests/test_aftercare.py
  * src/core/tests/test_aftercare_intake.py
  * src/core/tests/test_quality_procurement.py
  * src/api/tests/test_aftercare_screen.py
  * src/api/tests/test_aftercare_served.py
  * src/api/tests/test_content_standard.py
  * src/api/tests/test_role_endpoint_inventory.py
  * src/api/tests/test_role_matrix.py
  * src/agents/tests/test_epic104_bounded_ai_invariants.py
* Decisions, dependencies, and acceptance criteria considered: Architectural preserve-resident-statement boundary (`FR-6`), clause-scoped uncertainty handling (`FR-2`), boundary fail-closed rejection (`FR-3`..`FR-5`), `FR-036` disabled-live posture (`FR-4`, `C16`), test budget lock (`FR-7`, `NFR-2`), strict typing across `src/core` and `src/api` (`NFR-1`), sequential phase dependencies (`Phase 1` -> `Phase 2` -> `Phase 3`), and acceptance criteria `AC-1`..`AC-5`.
* Assessment boundary: Evaluates plan and phase-detail credibility strictly against the supplied tracking artifacts and repository source, test, and `pyproject.toml` files for Issue #133 Criterion 5. Hosted CI receipts and unrelated Issue #133 criteria remain outside this boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 / C1 / AC-1 | Covered | Lexical expansion for lifestyle attribution, fault/blame, measure causation, and financial/energy savings promises in `aftercare.py` covers Criterion 5 vocabulary, subject to `PC-001`. |
| FR-2 / CF1 / P01-T01 | Partial | `P01-T01` misstates current `aftercare.py:94-124`, breaks committed indirect-uncertainty tests in `src/core/tests/test_aftercare.py:252-260` via `UNCONDITIONAL_PATTERNS`, and introduces newline and `,`/`and`/`or` clause-split bypasses (`PC-001`). |
| FR-3 / FR-4 / CF3 / CF4 / P01-T02 | Partial | `P01-T02` misnames `record_closure` `owner` as `recorded_by`, omits `staff_recorded` concern `recorded_by`, misnames pack `reviewer_function` as `owner` in `from_state`, drops `"not_needed"` from required remedy-evidence handling, and omits `evaluator_view` `unknowns` wrapping (`PC-002`). |
| FR-3 / FR-4 / C11 / C12 / C16 / P02-T01 / AC-2 / AC-3 | Partial | `P02-T01` proposes a `NEUTRAL_NOTE_ERROR` string that fails `neutral_text` itself, references nonexistent `CONCERN_ROLES`, omits `AftercareService`'s `owner_label(actor["role"])` review contract and blank-input `ValidationError` handling, and misses `receipt["owner"]["label"]` when `status == "unknown"` in `_validate` (`PC-002`, `PC-003`). |
| FR-5 / CF2 / C19 / C20 / P02-T02 | Partial | `P02-T02` runs note validation ahead of `_quality_operation` authorization (`400` before `403` for unauthorized callers) and delegates directly to `aftercare.neutral_text`, whose `ValueError` echoes matched phrases (`PC-004`). |
| FR-6 / C3 / C4 / C15 / AC-4 | Covered | Resident/representative verbatim concern capture (`statement`, `household_statement`, `original.statement`, `representative_basis`) and static `aftercare.js` screen copy remain preserved without silent rewriting. |
| FR-7 / NFR-1 / NFR-2 / P03-T01 / P03-T02 / AC-5 | Partial | `P02-T02` and `P03-T02` pass `[tool.ruff.format].exclude` files explicitly to `ruff format --check`, and `P03-T01` lacks a guardrail against importing untyped `test_quality_procurement` into strict-typed `test_aftercare_served.py` under `src/api/pyproject.toml` (`PC-005`). |

## Verdict

* Verdict: Revise
* Rationale: The overall boundary architecture and preserve-verbatim resident statement design are sound, but five concrete mismatches with the actual codebase (`PC-001`..`PC-005`) would cause existing unit tests, snapshot round-trips, authorization checks, strict `mypy` in `src/api`, or `ruff format --check` commands to fail during implementation. Every finding is a direct planner correction grounded in supplied repository files and requires no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: P01-T01 pattern split and normalization order break committed tests and create clause-boundary bypasses

* Related IDs: FR-2, CF1, C1, Phase 1, P01-T01, P03-T01, AC-1, AC-5
* Evidence: src/core/src/zava_forward/core/aftercare.py:94-124; src/core/tests/test_aftercare.py:216-218,252-260; .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md:54,73,174; .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md:99-112
* Concern: First, Research `CF1` and the plan assume `aftercare.py:113-124` short-circuits whole strings via `if _UNCERTAIN.search(cleaned): return text`, whereas `aftercare.py:94-124` already uses span-bounded `_UNCERTAIN.sub(" ", ...)` requiring `(?:cannot determine|can ?not determine|unknown|not known|no evidence)\s+(?:whether|if)\b`. Second, `P01-T01` moves resident-blame and savings paraphrase patterns into `UNCONDITIONAL_PATTERNS` ("Never excused by `_UNCERTAIN`"), which directly rejects three committed assertions in `src/core/tests/test_aftercare.py:256-258` (`"Cannot determine whether the resident caused it"`, `"Unknown whether the tenant was at fault"`, and `"Unknown whether savings of any size were seen"`) while `Test Ownership & Budget Lock` forbids removing existing tests. Third, `P01-T01` collapses `\s+` (including `\n`) to `" "` in `_normalize_for_guard` before splitting clauses on `[.!?;:\n]+` (making `\n` in the splitter dead code and merging newline-separated sentences) and omits `,` and `\b(?:and|or|so|while|though|although)\b` from the clause splitter, regressing `src/core/tests/test_aftercare.py:218` (`"Unknown whether the tenant caused it and the tenant caused it"`) and comma-spliced causal claims.
* Impact: Implementing `P01-T01` as written immediately breaks `EvaluatorTests.test_neutral_factual_and_uncertain_statements_are_accepted` and `test_paraphrased_blame_and_savings_promises_are_rejected`, while introducing multi-line and conjunction/comma bypasses for causal claims.
* Smallest useful change: Update `FR-2`, `What You May Not Know`, and `P01-T01` to retain span-bounded `_UNCERTAIN.sub(" ", ...)` (strictly anchored to indirect `whether|if` clauses) and `_NEGATED_CLAIM.sub(" ", ...)` ahead of `PARAPHRASE_PATTERNS` evaluation while keeping `BANNED_PHRASES` unconditional; replace `[\r\n]+` with `"; "` before collapsing horizontal whitespace `[ \t\f\v]+` in `_normalize_for_guard`; and expand both `_UNCERTAIN` and `_NEGATED_CLAIM` stop-lookaheads to halt at `[.!?;:,\n\u2014\u2013]`, ` - `, `--`, and `\s(?:and|but|or|however|therefore|thus|hence|consequently|yet|so|whereas|while|though|although)\b` (or `$`).
* Action owner: planning parent
* Exact resolving evidence: Revised `FR-2` and `What You May Not Know` in `.copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md` and revised `P01-T01` in `.copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md` preserving `src/core/tests/test_aftercare.py:216-218,252-260` while blocking newline, comma, and conjunction mixed-clause bypasses.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: P01-T02 and P02-T01 misname closure, concern, and pack fields and drop `"not_needed"` remedy-evidence validation

* Related IDs: FR-4, CF3, CF4, C11, C14, Phase 1, P01-T02, Phase 2, P02-T01, AC-2, AC-5
* Evidence: src/core/src/zava_forward/core/aftercare.py:201-230,276-281,349-373,410-416,446-463; src/core/src/zava_forward/core/aftercare_intake.py:725; src/core/tests/test_aftercare.py:130,345-365; .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md:75,138; .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md:145-151,232
* Concern: `FR-4` and `P01-T02` contain four schema/invariant mismatches against `aftercare.py`: (1) `P01-T02` and `P02-T01` require remedy `evidence` only when `status == "completed"`, whereas `aftercare.py:225,354` requires non-empty `evidence` and `outcome_recorded` for `status in ("completed", "not_needed")`; (2) `FR-4` and `P01-T02` validate `recorded_by` on `record_closure` and closure entries in `from_state`, whereas `record_closure` (`aftercare.py:362-373`) uses parameter and dict key `"owner"` (`item["owner"]`), while `"recorded_by"` is the `staff_recorded` key on concerns in `raise_concern` (`aftercare.py:279`), which `P01-T02` omits; (3) `P01-T02` validates `pack["owner"]` in `from_state`, whereas `propose_pack` (`aftercare.py:456`) stores `"reviewer_function"` and has no `"owner"` key; and (4) `P01-T02` omits wrapping `evaluator_view` `unknowns` items (`aftercare.py:410-412` and `aftercare_intake.py:765`) in `neutral_text`.
* Impact: Checking `closure["recorded_by"]` or `pack["owner"]` in `from_state` breaks `SnapshotTests.test_round_trip_through_json_keeps_everything` (`src/core/tests/test_aftercare.py:345-365`), and allowing `evidence=None` on `status == "not_needed"` writes corrupt state that `from_state` (`aftercare.py:225`) subsequently rejects with `StateInvalid` (`503`).
* Smallest useful change: Correct `FR-4`, `P01-T02`, and `P02-T01` so that (a) `set_remedy` requires non-empty neutral `evidence` for `status in ("completed", "not_needed")` and validates optional non-blank `evidence` for `"open"` / `"in_progress"`, (b) `record_closure` and `from_state` validate closure `owner` (and `home_ref`) while `raise_concern` and `from_state` validate optional `recorded_by` on `staff_recorded` concerns, (c) `from_state` validates pack `reviewer_function` (not `pack["owner"]`), and (d) `evaluator_view` wraps `unknowns` strings in `neutral_text`.
* Action owner: planning parent
* Exact resolving evidence: Updated field names (`closure["owner"]`, concern `recorded_by`, `pack["reviewer_function"]`), `status in ("completed", "not_needed")` remedy rules, and `evaluator_view` `unknowns` wrapping in `.copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md` and `.copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: P02-T01 NEUTRAL_NOTE_ERROR fails neutral_text and AftercareService pack methods omit VIEW_ROLES and owner_label wiring

* Related IDs: FR-3, FR-4, C11, C12, C16, Phase 2, P02-T01, AC-2, AC-3, AC-4
* Evidence: src/core/src/zava_forward/core/aftercare.py:72,101-104,467-481; src/core/src/zava_forward/core/aftercare_intake.py:48-50,245-256,310-318,620-640; .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md:227-237
* Concern: First, `P02-T01` specifies `NEUTRAL_NOTE_ERROR = "Keep this note factual and observational, without stating a cause, blaming anyone or promising lower bills or energy savings."` and asserts that it passes `neutral_text`. Because `_NEGATED_CLAIM` stops at `,` and `\sor\s` (`aftercare.py:103`), `", blaming anyone or promising lower bills or energy savings."` remains unstripped and matches existing `r"\b(?:lower|smaller|cheaper) (?:energy )?bills?\b"` (`aftercare.py:72`) as well as `P01-T01`'s new `(energy|bill|cost|financial) savings` pattern, causing `neutral_text(NEUTRAL_NOTE_ERROR)` to raise `ValueError`. Second, `P02-T01` gates `AftercareService.propose_pack` and `review_pack` on `CONCERN_ROLES`, which does not exist in `aftercare_intake.py` (`RECORD_ROLES`, `VIEW_ROLES`, and `MANAGER` are defined at lines 48-50), and does not specify that `AftercareService` stores `rec["owner"]` as `owner_label(owner_role)` (`f"{role} (synthetic scenario owner)"`) rather than `actor["name"]` (`aftercare_intake.py:626-639`); passing `actor["name"]` to `reg.review_pack` always fails `reg._own` with `PermissionError`. Third, `_free_text` (`aftercare_intake.py:311`) silently returns `""` without populating `errors` when input is blank/whitespace, and `_validate` (`aftercare_intake.py:252`) skips checking `receipt["owner"]["label"]` when `receipt["owner"]["status"] == "unknown"`.
* Impact: `NEUTRAL_NOTE_ERROR` fails neutrality checks on error payloads/constants; `AftercareService.propose_pack` / `review_pack` hit `NameError` or always fail owner verification; blank `reason` / `ai_summary` bypass structured `ValidationError`; and tampered unknown-owner receipt labels bypass `_validate`.
* Smallest useful change: Replace `NEUTRAL_NOTE_ERROR` in `P02-T01` with plain-language copy containing zero prohibited n-grams without widening `_NEGATED_CLAIM` across commas/`or` (for example, `"Keep this note factual and observational. Record only what was reported, observed or checked."`); gate `propose_pack` and `review_pack` on `VIEW_ROLES`, refuse `review_pack` when the concern owner is `UNKNOWN_OWNER`, and pass `owner_label(actor["role"])` as `reviewer` to `reg.review_pack` matching `_owner_action`; add explicit `ValidationError` entries when `reason` is blank or optional `ai_summary` is whitespace-only; and validate `receipt["owner"]["label"]` (requiring `UNKNOWN_OWNER` when `status == "unknown"`) and `receipt["recorded_by"]` fields in `_validate`.
* Action owner: planning parent
* Exact resolving evidence: Updated `P02-T01` in `.copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md` specifying a `neutral_text`-clean `NEUTRAL_NOTE_ERROR`, `VIEW_ROLES` and `owner_label(actor["role"])` semantics for `propose_pack`/`review_pack`, blank-field `ValidationError` rules, and complete receipt restore checks in `_validate`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: P02-T02 quality.py add_aftercare step order risks 400-before-403 status inversion and phrase echoing

* Related IDs: FR-5, CF2, C19, C20, Phase 2, P02-T02, P03-T02, AC-2
* Evidence: src/core/src/zava_forward/core/quality.py:130-145,394-402; src/core/src/zava_forward/core/aftercare.py:115-116; src/core/tests/test_quality_procurement.py:92-112; src/api/tests/test_role_matrix.py:32-33,73-74; .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md:276-282,366-369
* Concern: `P02-T02` places `controls.req_text`, `controls.is_memory_reference(note)`, and `aftercare.neutral_text(note)` ahead of `with self._quality_operation(user, case_id) as (c, user):`, where `current_actor` and `decision_scope` enforce authorization (`PermissionError` -> HTTP `403`). Direct `store.add_aftercare` calls by unauthorized or forged actors (`test_quality_current_actor_all_writes` in `src/core/tests/test_quality_procurement.py:92-112`) with invalid or non-neutral notes would raise `ValueError` instead of `PermissionError`. In addition, calling `aftercare.neutral_text(note)` uncaught raises `ValueError(f"Generated text must not contain '{phrase}'.")` (`aftercare.py:116`), echoing the matched phrase in developer wording rather than `FR-5`'s fixed plain-language non-echoing message.
* Impact: Authorization precedence regresses for invalid/non-neutral inputs on direct service calls, and HTTP `400` responses from `/api/cases/<cid>/quality-aftercare` echo matched banned substrings.
* Smallest useful change: Update `P02-T02` so `add_aftercare` enters `with self._quality_operation(user, case_id) as (c, user):` before running `req_text` / length / `is_memory_reference` / `aftercare.neutral_violations(note)` checks (still prior to `self._qrec` and `rec["aftercare"].append`, guaranteeing zero state or audit mutation), raises fixed plain-language `ValueError` messages without echoing caller text or matched phrases, and adds `tests/test_role_matrix.py` to `P03-T02`'s API regression command.
* Action owner: planning parent
* Exact resolving evidence: Updated validation ordering and non-echoing `ValueError` contract in `P02-T02` plus `tests/test_role_matrix.py` inclusion in `P03-T02` of `.copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Validation commands pass ruff-format-excluded files explicitly and P03-T01 lacks a cross-package mypy import guardrail

* Related IDs: FR-7, NFR-1, C22, C23, Phase 2, P02-T02, Phase 3, P03-T01, P03-T02, AC-5
* Evidence: src/core/pyproject.toml:42-60; src/api/pyproject.toml:43-87; src/core/src/zava_forward/core/quality.py:380,389; .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md:289,339-341,360,363
* Concern: `src/core/pyproject.toml:42-49` excludes legacy-migrated `src/zava_forward/core/quality.py` and `tests/test_quality_procurement.py` from `[tool.ruff.format]`, and `src/api/pyproject.toml:43-49` excludes `tests/test_content_standard.py`. Passing those paths explicitly on the CLI to `python3 -m ruff format --check` (`P02-T02` line 289 and `P03-T02` lines 360, 363) overrides `pyproject.toml` excludes and fails on pre-existing >100-character lines (such as `quality.py:380,389`) or encourages out-of-scope reformatting. Separately, `src/api/pyproject.toml:55,84-86` shares `../core/tests` on `mypy_path` and checks `test_aftercare_served.py` under `strict = true` without a `test_quality_procurement` override; if `P03-T01`'s new `test_quality_aftercare_http_rejects_causation_blame_and_savings` imports `EVIDENCE` from `test_quality_procurement` (as untyped `test_role_matrix.py` does), `cd src/api && python3 -m mypy` will follow the import into untyped `../core/tests/test_quality_procurement.py` and fail.
* Impact: Planned Phase 2 and Phase 3 validation commands fail on unchanged legacy lines or cross-package strict `mypy` imports despite clean implementation code.
* Smallest useful change: Update `Validation Strategy` in the plan and `P02-T02` / `P03-T02` in phase details to run package-level `python3 -m ruff check` and `python3 -m ruff format --check` in `src/core` and `src/api` (or omit `[tool.ruff.format].exclude` files from explicit `ruff format --check` file lists), and specify in `P03-T01` that `test_aftercare_served.py` constructs inline typed quality-submission evidence rather than importing untyped `test_quality_procurement` or `dataset` helpers.
* Action owner: planning parent
* Exact resolving evidence: Updated `ruff format --check` commands in `.copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md` and `.copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md` (`P02-T02`, `P03-T02`) plus explicit inline typed fixture note in `P03-T01`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Preserving resident and representative concern descriptions verbatim in `statement`, `household_statement`, `original.statement`, and `representative_basis` (`FR-6`) while enforcing `neutral_text` on every staff-authored, sensor-context, AI-draft, templated, and deserialized field honors PAS 2035:2023 resident-voice fidelity and Criterion 5 simultaneously.
* Rejecting tampered non-neutral persisted state in `AftercareRegister.from_state` and `AftercareService._validate` (`FR-4`) closes storage-reload bypasses cleanly so corrupt snapshots fail closed (`503`) rather than rendering causation, blame, or savings claims.
* Residual risk: Deterministic lexical and regex validation cannot prove general semantic entailment for arbitrary novel phrasing outside the pattern set; keeping `FR-036` (`aftercare-concern-pack`) disabled for live model routing (`ai_registry.py:136-143`) and requiring named-owner human review (`AftercareRegister.review_pack`) bounds this residual risk appropriately for Criterion 5.

## Questions or Blocking Evidence Gaps

* None. All five findings are resolved directly from the supplied repository code, tests, and `pyproject.toml` configurations without user input or additional research.

## Limitations

* Critique is static and read-only over the supplied plan, phase details, research, source modules, tests, and package configurations; test and linter execution belongs to `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions for `PC-001`..`PC-005` to `.copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md` and `.copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md`, then finalize the plan without re-running critique.
* User response required: no
