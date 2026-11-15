<!-- markdownlint-disable-file -->
# RPI Plan: Issue #133 Aftercare Concern Route and Lived-Performance Review

## Task Metadata

* Task ID: aftercare-133-2346
* Task slug: aftercare-133-2346
* Planning status: Ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-14/aftercare-133-2346-plan-critique.md

## Executive Summary

This plan delivers the remaining local domain, service, UI, deterministic-guard, and verification work in `src/core` and `src/api` for **Issue #133** (*Aftercare concern route and lived-performance review*). Households or their representatives must be able to raise discomfort, higher-bill, control-use, or other post-retrofit concerns through both digital self-service and staff-recorded non-digital channels (`phone`, `in_person`, `paper`, `assisted_visit`, and `representative`), retaining the original account, channel, named owner, investigation outcome, and remedy status across handover and financial closure and never dismissing a resident report because sensors look normal.

At the same time, generated, templated, evaluator, pack, and staff-authored outcome/remedy text must pass a deterministic neutral-language guard that rejects causation claims, resident-blame wording (including occupant behaviour, thermostat settings, or ventilation habits), and bill-savings promises or guarantees. Finally, the evaluator lived-performance view must preserve `unknown` counts and readings without coercing them to `none` or `0`, state denominators explicitly, and surface `FR-036` AI registry governance proving that any optional AI concern pack remains an unapproved, human-reviewed proposal with no live mutation authority.

### User Decisions and Requirements Highlights

* Complete accessible digital + staff-recorded non-digital concern intake (`phone`, `paper`, `in_person`, `representative`, `assisted_visit`), preserving original account, channel, owner, investigation outcome, and remedy status across handover/financial closure and normal sensor readings.
* Enforce and test a deterministic no-causation, no-blame (occupant behaviour, thermostat, ventilation), and no-savings-promise guard across generated, templated, and evaluator/aftercare text while keeping household verbatim statements intact.
* Preserve `unknown` without coercion to `none` or `0` in evaluator baseline, outcome, and unresolved-concern views, and bind optional AI concern packs to `FR-036` proposal-only human-review governance.
* Remove bulk `sys.modules` eviction from test helpers so `unittest discover` preserves Python class identity across test modules, validate with `mypy`, `ruff check`, `ruff format --check`, and focused `unittest` suites, and commit locally with `Refs #133` without pushing.

### What You May Not Know

* `src/core/tests/aftercare_fixture.py` currently pops `zava_forward.core*` entries from `sys.modules` when tests execute alongside the shared editable install; replacing that loop with `sys.path` and in-place namespace `__path__` precedence avoids class-identity mismatches during `unittest discover`.
* `src/api/src/zava_forward/api/server.py` enforces authenticated staff sessions across `/api/*` (`test_role_endpoint_inventory.py`), while live resident-portal authentication remains gated by PRD `OD-54`; keeping the digital household contract in `AftercareService` and `web/aftercare.js` preserves the staff-server security boundary.
* `aftercare-concern-pack` is registered as `disabled` and `unapproved` in untyped `ai_registry.py` under `FR-036` (requiring typed `cast(...)` bindings in strict-`mypy` modules `aftercare.py` and `aftercare_intake.py`), `AftercareService.handle` maps `ValidationError` to `HTTP 400` with `GET /api/aftercare/evaluator` as the evaluator route, and `src/api` static scanners (`test_list_export_inventory.py`, `test_content_standard.py`) enforce dynamic endpoint variables and plain-language vocabulary across `web/aftercare.js`.

### Unresolved Decisions or Blockers

* None for local `#133` engineering. External dependencies outside `#133` (`OD-54` live resident identity enrolment, DPO formal sign-off, and `FR-036` held-out benchmark approval for live `aftercare-concern-pack` inference) remain documented non-goals; the commit will therefore reference `Refs #133`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI workflow (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) in `/home/azureuser/source/ama-demo-wt/feat-133-aftercare-concern-2346` on branch `feat/demo-133-aftercare-concern-2346` targeting `feat/demo-233-same-home-tensions-0825` (caller brief).
* Ensure a household or representative can raise an aftercare concern (`discomfort`, `higher_bill`, `control_use`, `other`) through an accessible route including digital and staff-recorded non-digital channels (`phone`, `paper`, `in_person`, `representative`, `assisted_visit`), preserving original account, channel, owner, investigation outcome, and remedy status that handover or financial closure cannot erase, and never dismissing a resident report because a sensor reading is normal (caller brief; Issue #133; PRD `FR-049`, `AC-063`).
* Enforce and test a deterministic guard across generated, templated, or evaluator/aftercare summary text so that no causation claim, resident-blame wording (such as blaming occupant behaviour, thermostat settings, or ventilation use), or bill-savings promise/guarantee appears in any generated or templated aftercare/evaluator output (caller brief; Issue #133; PRD `CON-008`).
* Verify that the evaluator view shows baseline, outcomes, and unresolved concerns with stated denominators and unknowns (`unknown` preserved, never coerced to `none` or `0`), and that any optional AI concern pack stays a registered proposal requiring human review under `FR-036` (caller brief; Issue #133; PRD `FR-036`, `CON-003`).
* Write all dated RPI artifacts under `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-14/aftercare-133-2346*` (caller brief).
* Do NOT use bulk `del sys.modules[...]` or `sys.modules.pop(...)` in test files, which breaks class identity during `unittest discover` (caller brief).
* Validate modified packages (`src/core` and `src/api`) with `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and focused `unittest` suites covering new and existing aftercare/handover tests (caller brief; `.github/copilot-instructions.md`).
* Commit cleanly on `feat/demo-133-aftercare-concern-2346` with `Refs #133` and the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer, and do NOT push (caller brief).

## Goals

* Complete digital and staff-recorded non-digital aftercare concern intake parity (including the `"representative"` channel, legacy `"call_back"` support normalization, digital-only household receipt isolation, and multi-select support adjustments in the web UI) while preserving original records across closure and normal sensor states.
* Eliminate deterministic neutral-text bypasses across newline-wrapped sentences, occupant/thermostat/ventilation/lifestyle blame paraphrases, finite causal verbs, bill-savings guarantees, and staff-authored outcome/remedy/pack-review evidence fields without censoring verbatim household statements.
* Ensure the evaluator lived-performance view and web screen preserve `unknown` without coercion to `0` or `"No concerns raised"`, state explicit denominators, and surface `FR-036` `ai_registry` proposal-only human-review governance metadata.
* Ensure all `src/core` and `src/api` test modules load cleanly under `unittest discover` with zero `sys.modules` bulk eviction.

## Scope and Non-Goals

### In Scope

* `src/core/tests/aftercare_fixture.py` removal of `sys.modules.pop` loop in favour of `sys.path` and in-place namespace `__path__` precedence.
* `src/core/src/zava_forward/core/aftercare.py` and `aftercare_intake.py` channel parity (`"representative"`), `"call_back"` -> `"callback_window"` normalization, digital-only `household_receipt` scoping, hardened `strip_unsafe_sentences` and `PARAPHRASE_PATTERNS`, `neutral_text` enforcement on staff outcome/remedy/pack-review/restore text, and `FR-036` `ai_registry` metadata on `propose_pack` and `evaluator_view`.
* `src/api/src/zava_forward/api/web/aftercare.js` channel/route/support labels, `spec.multiple` support for `support_needed`, optional `owner_note`/`support_note` rendering, strict `unknown` non-coercion in `aftercareEvaluatorView`, and `FR-036` proposal-only human-review governance rendering.
* Focused semantic and regression tests in `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/api/tests/test_aftercare_screen.py`, and `src/api/tests/test_aftercare_served.py`, plus `src/core/README.md` and `src/api/README.md` updates.

### Non-Goals

* Opening unauthenticated endpoints on `src/api/src/zava_forward/api/server.py` (staff session boundary remains mandatory; live resident portal authentication stays gated by `OD-54`).
* Enabling live LLM inference or HTTP mutation endpoints for `aftercare-concern-pack` (`FR-036` keeps the task `disabled` and `unapproved` until held-out benchmarks and formal sign-off exist).
* Altering `#87` `src/core/src/zava_forward/core/quality.py:add_aftercare` handover notes.
* Pushing commits to `origin` or opening/updating a remote pull request.

## Functional Requirements

* FR-1 (Accessible digital and non-digital intake parity): Households or representatives can raise `discomfort`, `higher_bill`, `control_use`, or `other` concerns via `digital` or `staff_recorded` routes across `phone`, `in_person`, `paper`, `assisted_visit`, and `representative` channels, with optional `support_needed` adjustments (including `"call_back"` normalized to `"callback_window"` and multi-select UI serialization).
  * Observable acceptance criteria: `NON_DIGITAL_CHANNELS` includes `"representative"`, `intake_form` and `staff_form` list its neutral label, `household_receipt` rejects `staff_recorded` concern IDs with uniform `PermissionError`, and `web/aftercare.js` renders human-readable channel/route/support labels and multi-select `support_needed` without `"Unknown"` placeholders on valid digital or staff forms.
* FR-2 (Closure immutability and sensor non-dismissal): Handover or financial closure and normal sensor readings cannot erase, overwrite, auto-close, or negate any resident concern, original statement, channel, named owner, investigation outcome, or remedy status.
  * Observable acceptance criteria: Recording handover or financial closure or attaching normal sensor context leaves open concerns/remedies visible in `closure_status()` and `evaluator_view()`, and rejects `sensor_normal_dismissed` or sensor-based auto-dismissal.
* FR-3 (Deterministic neutral-language guard): Generated, templated, evaluator, pack, and staff-authored outcome/remedy/review text rejects causation claims, resident-blame wording (occupant behaviour/lifestyle/habits, thermostat/heating-control settings, ventilation/window/drying-clothes habits, user error), and bill-savings/reduction promises or guarantees, including across newline-wrapped sentences, while preserving verbatim household `statement` and `representative_basis`.
  * Observable acceptance criteria: `neutral_text` rejects all causation, blame, and savings-promise corpus phrases; `strip_unsafe_sentences` never reconstructs a banned phrase across newlines; `record_outcome`, `set_remedy`, `review_pack`, and `from_state` reject non-neutral staff evidence/reasons while household statements containing blame/bill text remain accepted verbatim.
* FR-4 (Evaluator baseline/outcome view, `unknown` preservation, and `FR-036` AI pack governance): `evaluator_view()` and `aftercareEvaluatorView()` present baseline vs post-work summary, outcomes, and unresolved concerns with stated denominators, preserve `unknown` without coercing to `none` or `0`, and expose `FR-036` `ai_registry` metadata (`proposal-pack`, `unapproved`, `live_authorized: false`, `requires_human_review: true`) on optional AI concern packs and the evaluator payload.
  * Observable acceptance criteria: Non-array, null, or `"unknown"` `row.concerns` and `homes_with_usable_comparison` render `"Unknown"` in `aftercareEvaluatorView()` rather than `"0"` or `"No concerns raised"`, `propose_pack()` and `evaluator_view()` carry `FR-036` registry governance fields, and `/api/aftercare/concerns/<id>/{pack,packs,concern-pack}` remains `404`/`405`.

## Non-Functional Requirements

* NFR-1 (`unittest discover` class-identity stability): Test modules must never perform bulk `del sys.modules[...]` or `sys.modules.pop(...)` eviction.
  * Objective threshold or evaluation condition: Zero occurrences of `sys.modules.pop` or `del sys.modules` in `src/core/tests/aftercare_fixture.py` and aftercare test files; full `unittest discover` passes in both `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Run `python3 -m unittest discover -s tests -q` in `src/core` and `src/api` with worktree `PYTHONPATH`.
  * Observable acceptance criteria: All discovered tests pass without `isinstance` / `assertRaises(ValidationError)` class-identity failures.
* NFR-2 (Static type, lint, format, and accessibility compliance): Modified Python and web code satisfies strict static typing, formatting, linting, and accessible HTML semantics (`WCAG 2.2 AA` / Fluent 2 native form associations, `aria-live`, and non-colour text indicators).
  * Objective threshold or evaluation condition: Zero errors from `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and UI accessibility/Node VM screen assertions.
  * Observable acceptance criteria: All four checks exit `0` in `src/core` and `src/api`.

## Acceptance Criteria

* AC-1: `NON_DIGITAL_CHANNELS` includes `"representative"` alongside `"phone"`, `"in_person"`, `"paper"`, and `"assisted_visit"`; `"call_back"` normalizes to `"callback_window"`; `household_receipt` serves only `route == "digital"` concerns; and handover/financial closure and normal sensors never erase or dismiss a concern.
* AC-2: `neutral_text` and `strip_unsafe_sentences` deterministically block causation claims, occupant behaviour/thermostat/ventilation/lifestyle blame wording, and bill-savings/reduction promises across single-line and multiline inputs, and enforce neutrality on staff `record_outcome`, `set_remedy`, `review_pack`, and `from_state` text while preserving household `statement` and `representative_basis` verbatim.
* AC-3: `evaluator_view` and `aftercareEvaluatorView` display baseline, outcomes, unresolved concerns, and stated denominators while preserving `"unknown"` / null / non-array values as `"Unknown"` (never `"0"` or `"none"`), and surface `FR-036` `aftercare-concern-pack` proposal-only human-review governance metadata with live pack HTTP routes kept closed (`404`/`405`).
* AC-4: `web/aftercare.js` renders explicit channel/route/support labels, supports `multiple` selection on `support_needed`, handles optional `owner_note`/`support_note` cleanly on digital and staff forms, and preserves accessible label/help/error associations.
* AC-5: `src/core/tests/aftercare_fixture.py` contains no `sys.modules` eviction; `mypy`, `ruff check`, `ruff format --check`, and `unittest` suites pass in `src/core` and `src/api`; and all changes plus dated RPI artifacts are committed cleanly on `feat/demo-133-aftercare-concern-2346` with `Refs #133` and the Copilot trailer without pushing.

## Test Ownership and Verification Lock

* Canonical source targets: `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py`, `src/api/src/zava_forward/api/web/aftercare.js`, `src/core/README.md`, `src/api/README.md`.
* Generated targets: `none`.
* Test helper revision: `src/core/tests/aftercare_fixture.py` (remove `sys.modules.pop` loop; zero test removals).
* Exact test removals: `none`.
* Maximum net new test methods: at most `18` focused test methods across existing suites (`src/core/tests/test_aftercare.py` <= `8`, `src/core/tests/test_aftercare_intake.py` <= `5`, `src/api/tests/test_aftercare_screen.py` <= `4`, `src/api/tests/test_aftercare_served.py` <= `1`); zero new test files.
* Semantic vs regression coverage:
  * Semantic tests verify new behavior that fails before the change: `"representative"` non-digital channel intake, `"call_back"` support normalization, digital-only `household_receipt` isolation, multiline `strip_unsafe_sentences`, occupant thermostat/ventilation/lifestyle blame + causal verb + savings-guarantee rejection, staff `record_outcome`/`set_remedy`/`review_pack`/`from_state` neutrality enforcement, `FR-036` `concern_pack_task` metadata, multi-select `support_needed` in `aftercare.js`, and non-array/`"unknown"` `row.concerns` rendering `"Unknown"` in `aftercareEvaluatorView`.
  * Regression suites verify existing behavior remains intact: handover/financial closure immutability, sensor non-dismissal, idempotent replay, PII rejection, role authorization (`test_role_endpoint_inventory.py`), and `unittest discover` across `src/core` and `src/api`.
* Validation commands (Focused tier — scoped `src/core` + `src/api` refinement with no workflow, Bicep, Dockerfile, SQL-schema, dependency-manifest, or security-boundary weakening changes):
  * `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -q`
  * `cd src/api && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/aftercare-133-2346-plan.md                                                                            |
| Phase details                    | .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md                                                                 |
| Latest critique                  | .copilot-tracking/reviews/2026-11-14/aftercare-133-2346-plan-critique.md with Revise disposition (PC-001..PC-007 resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-14/aftercare-133-2346-research.md                                                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/aftercare-133-2346-changes.md is created or continued by implementation as its evidence record      |
| Planning execution and readiness | Complete; implementation-ready                                                                                                           |
| Continuation context             | Confirmed automatic RPI Agent session continues directly to Implement (rpi-implement)                                                    |

## Sources

* `.copilot-tracking/research/2026-11-14/aftercare-133-2346-research.md`: Cycle 1 evidence log (`C1`–`C18`), contrarian checks, and convergence selection across `src/core` and `src/api`.
* `.copilot-tracking/reviews/logs/2026-11-14/133-aftercare-concern-2142-review.md`: Prior `#133` review findings (`RV-001`–`RV-004`) incorporated into `P01` and `P02`.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Requirements `FR-049`, `AC-063`, `FR-036`, `CON-003`, `CON-008`, and `OD-54`.
* `docs/reference/research/ux/customer-journeys/programme.md`: Evaluator and aftercare journey rules (`O13`, `O14`) requiring sensor non-dismissal and human-reviewed proposals.
* `src/core/src/zava_forward/core/aftercare.py`, `aftercare_intake.py`, `ai_registry.py`, and `src/api/src/zava_forward/api/web/aftercare.js`: Existing domain, HTTP service, AI registry, and web UI contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Intake Channel Parity, Receipt Isolation, and Fixture Safety

* Intent: Eliminate `sys.modules` bulk eviction in `aftercare_fixture.py` and complete accessible digital + non-digital concern intake (`"representative"` channel, `"call_back"` support normalization, and digital-only `household_receipt`).
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Remove bulk `sys.modules` eviction from `src/core/tests/aftercare_fixture.py`

* Requirement and evidence: Caller constraint (`Do NOT use bulk del sys.modules[...] in test files`); research `C1`, `C2`.
* Expected result: `aftercare_fixture.py` configures `sys.path` and namespace `__path__` in-place without popping or deleting `sys.modules` entries, preserving class identity across `unittest discover`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `"representative"` non-digital channel, `"call_back"` support alias, and digital-only `household_receipt` check

* Requirement and evidence: FR-1, AC-1; research `C3`, `C4`, `C5`.
* Expected result: `NON_DIGITAL_CHANNELS`, `CHANNEL_LABELS`, `ACCESSIBLE_ROUTE`, and `raise_concern` invalid-channel error text include `"representative"`, `intake_form` sets `"multiple": True` on `support_needed`, `normalize_support_needed` maps `"call_back"` to `"callback_window"`, and `AftercareService.household_receipt` raises uniform `PermissionError` for non-digital concerns.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Deterministic Causation, Resident-Blame, and Savings-Promise Guard

* Intent: Close multiline sentence-stripping, occupant/thermostat/ventilation/lifestyle blame paraphrases, causal verb variants, savings-promise variants, and staff-authored outcome/remedy/pack-review bypasses in `src/core`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Harden `strip_unsafe_sentences` and expand `PARAPHRASE_PATTERNS` in `aftercare.py`

* Requirement and evidence: FR-3, AC-2; research `C6`, `C7`.
* Expected result: `strip_unsafe_sentences` folds intra-sentence line breaks and re-validates joined output with `neutral_text`; `PARAPHRASE_PATTERNS` rejects occupant behaviour/lifestyle/habits (including singular `'s` possessives), present/past/gerund thermostat/heating-control and ventilation/window/trickle-vent/drying-clothes blame, `"user error"`, finite `"stems/arises/results from"`, causal-subject/adverse-object `"is responsible for"`, and bill-savings/reduction promises without false positives on neutral ownership notes, uncertainty, negations, or `control_use` labels.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Enforce `neutral_text` on staff outcome, remedy, pack-review, and restored evidence fields

* Requirement and evidence: FR-3, AC-2; research `C8`, `C9`, `C16`.
* Expected result: `AftercareRegister.record_outcome`, `set_remedy`, `review_pack`, `from_state` (`outcome["evidence"]`, non-empty `remedy["evidence"]`, and pack `ai_summary`/`recorded_facts`/`questions_for_investigator`/`approval`/`manual_route`/`notice`/`review["reason"]`, keeping `household_statement` exempt), and `AftercareService.record_outcome`/`set_remedy` reject non-neutral staff evidence/reasons (returning `HTTP 400` field-keyed `ValidationError` on HTTP routes), while household `statement` and `representative_basis` stay verbatim.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Evaluator Unknown Preservation, FR-036 Pack Governance, and Accessible Web UI

* Intent: Bind `FR-036` `ai_registry` proposal-only metadata into `propose_pack` and `evaluator_view`, and update `web/aftercare.js` so digital/non-digital forms, multi-select support adjustments, and evaluator `unknown` values render accurately and accessibly.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Attach `FR-036` `ai_registry` proposal-only governance metadata in `aftercare.py` and `aftercare_intake.py`

* Requirement and evidence: FR-4, AC-3; research `C12`, `C13`, `C18`.
* Expected result: `AftercareRegister.propose_pack` and `AftercareService.evaluator_view` (`GET /api/aftercare/evaluator`, `concern_pack_task`) expose typed `FR-036` task registry fields via `cast(...)`-bound `ai_registry.get(CONCERN_PACK_TASK)` and `ai_registry.authorizes_live(CONCERN_PACK_TASK)` (`task_id`, `requirement: "FR-036"`, `kind`, `state`, `approval_state`, `live_authorized: False`, `requires_human_review: True`, `manual_route`, `purpose`, `influence`), keeping HTTP pack mutation routes unexposed (`404`/`405`).
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Update `src/api/src/zava_forward/api/web/aftercare.js` for channel/support labels, multi-select, `unknown` non-coercion, and `FR-036` notice

* Requirement and evidence: FR-1, FR-4, NFR-2, AC-3, AC-4; research `C10`, `C11`.
* Expected result: `web/aftercare.js` renders dedicated channel and exact `SUPPORT_OPTIONS` labels, supports `spec.multiple` with array-preserving selection on `support_needed`, handles optional `owner_note`/`support_note` and null digital `recorded_by` via `h(...)`, posts via dynamic subpath variable compatible with `test_list_export_inventory.py`, preserves `"Unknown"` for non-array/null/`"unknown"` `v.rows`, `row.concerns`, `totals.concerns_raised`, and `homes_with_usable_comparison` in `aftercareEvaluatorView`, and renders `test_content_standard.py`-compliant `FR-036` human-review proposal copy.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Focused Core and API Tests, Documentation Sync, and Verification

* Intent: Add focused semantic tests in `src/core` and `src/api`, update package READMEs, run all static checks and `unittest` suites, and confirm clean state before review.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Extend `test_aftercare.py` and `test_aftercare_intake.py` in `src/core`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, AC-1, AC-2, AC-3, AC-5.
* Expected result: Focused `src/core` unit tests verify `"representative"` channel intake, `"call_back"` normalization, digital-only `household_receipt`, multiline `strip_unsafe_sentences`, occupant thermostat/ventilation/lifestyle blame + causal verbs + savings guarantees, staff outcome/remedy/pack-review neutrality, `FR-036` `concern_pack_task` metadata, and absence of `sys.modules` eviction in `aftercare_fixture.py`.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Extend `test_aftercare_screen.py` and `test_aftercare_served.py`, update READMEs, and run `mypy`, `ruff`, and `unittest`

* Requirement and evidence: FR-1, FR-4, NFR-1, NFR-2, AC-3, AC-4, AC-5.
* Expected result: Node VM and API tests verify `representative` channel, multi-select `support_needed`, digital vs staff channel formatting, `unknown` non-coercion in `aftercareEvaluatorView`, and `FR-036` notice; `src/core/README.md` and `src/api/README.md` document the refined contracts; `mypy`, `ruff check`, `ruff format --check`, and `unittest discover` exit `0` in `src/core` and `src/api`.
* Detail section: P04-T02 in .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md

## Dependencies

* Shared Python environment (`mypy`, `ruff`, `unittest`) and Node.js (`node` binary used by `src/api/tests/test_aftercare_screen.py`): available in the worktree environment; `PYTHONPATH` must place worktree `src` ahead of editable `.pth` directories during `unittest` runs.
* `web-design-guidelines` skill: must be loaded and checked before modifying `src/api/src/zava_forward/api/web/aftercare.js` per `.github/copilot-instructions.md`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [Critical] (`ai_registry` symbols & strict `mypy`) | Resolved | Updated `P03` and `P03-T01` to use `ai_registry.get(CONCERN_PACK_TASK)` and `ai_registry.authorizes_live(CONCERN_PACK_TASK)` via typed `cast(...)` callables and real registry keys (`id`, `kind`, `state`, `approval_state`, `manual_route`, `purpose`, `influence`, `enabled`). |
| `PC-002` [High] (`from_state` pack keys, `HTTP 400`, `/api/aftercare/evaluator`) | Resolved | Updated `P02-T02`, `P03-T01`, and `P04` to validate real pack keys (`ai_summary`, `recorded_facts`, `questions_for_investigator`, `approval`, `manual_route`, `notice`, `review["reason"]`) while exempting `household_statement`, guard `_present(outcome.get("evidence"))`, assert `HTTP 400`, and target `GET /api/aftercare/evaluator`. |
| `PC-003` [High] (`support_needed` `"multiple": True`, array re-render, exact `SUPPORT_OPTIONS` keys) | Resolved | Updated `P01-T02` to set `"multiple": True` in `aftercare.py:intake_form()` and `P03-T02` to omit blank option on `<select multiple>`, preserve array `value` across re-renders, and map the exact seven `SUPPORT_OPTIONS` keys (`large_print`, `easy_read`, `interpreter`, `bsl`, `callback_window`, `paper_letter`, `support_person`). |
| `PC-004` [High] (`test_list_export_inventory.py`, `h(...)`, digital `recorded_by`, `test_content_standard.py`) | Resolved | Updated `P03-T02` and `P04-T02` to interpolate the POST target via variable (`const target = ...`), handle null `receipt.recorded_by` on digital receipts, use `h(...)`, and ensure all copy/comments pass `neutral_text` and `test_content_standard.py`. |
| `PC-005` [Medium] (Scoped `responsible for`, singular `'s`, present/gerund control blame) | Resolved | Updated `P02-T01` and `P04-T01` to scope `responsible for` to causal/fault subjects or adverse outcomes, use `(?:s'|'s|s)?`, and cover present/past/gerund control and ventilation blame verbs. |
| `PC-006` [Medium] (`aftercare.py:517` channel error text & `src/core/README.md` channel lists) | Resolved | Updated `P01-T02` and `P04-T02` to include `"representative"` in `ACCESSIBLE_ROUTE`, `raise_concern` invalid-channel `ValueError`, and `src/core/README.md` channel lists. |
| `PC-007` [Low] (`v.rows` and `totals.concerns_raised` `"unknown"` guards in `aftercareEvaluatorView`) | Resolved | Updated `P03-T02` and `P04-T02` to guard `Array.isArray(v.rows)` and `acWhole(totals.concerns_raised)` while preserving `${usable.count} of ${usable.denominator} homes have a usable comparison` when valid. |
| Residual risk (AT & live sign-off) | Accepted with risk | Node VM and Playwright checks verify engineering contracts; live assistive-technology usability and DPO/FR-036 live activation remain outside `#133` local engineering (`Refs #133`). |

## Follow-Up Items

* Resident showcase portal (`resident_demo`) live session write route for aftercare concerns: outside `#133` local engineering scope because PRD `OD-54` gates live/authenticated resident portal identity and session persistence; tracked for the `OD-54` resident-portal increment.
* Held-out benchmark and release sign-off for `aftercare-concern-pack` live model drafting: outside `#133` scope because `FR-036` requires separate quality/effort benchmarks and named governance approval before enabling `CONCERN_PACK_TASK` in `ai_registry.py`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/aftercare-133-2346-changes.md
* Ready phase or task: All phases complete (`P01`–`P04`); ready for `rpi-review`
* Remaining provisional question or blocker: None
