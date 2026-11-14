<!-- markdownlint-disable-file -->
# RPI Plan: Issue #133 Aftercare Accessible Concern Routes and Neutral-Text Enforcement in src/core

## Task Metadata

* Task ID: 133-aftercare-concern-2142
* Task slug: 133-aftercare-concern-2142
* Planning status: implementation-ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/133-aftercare-concern-2142-plan-critique.md

## Executive Summary

This plan completes the two remaining locally verifiable engineering criteria for Issue #133 (**Aftercare concern route and lived-performance review**, `FR-049`, `AC-063`) inside `src/core`: enabling a household or authorized representative to raise an aftercare concern through an accessible digital or non-digital route with optional communication adjustments, and ensuring no causation, blame, or savings promise can appear in any generated or templated text across the aftercare core modules.

First, `zava_forward.core.aftercare` and `zava_forward.core.aftercare_intake` are extended so accessibility support adjustments (`large_print`, `interpreter`, `call_back`, `support_person`) are offered without medical gatekeeping, validated in plain language, and persisted on the concern record, durable receipt, and household/staff views. Alongside the existing staff-assisted non-digital channels (`phone`, `in_person`, `paper`, `assisted_visit`), `AftercareService` gains a self-service household/representative digital intake (`household_form`, `submit_household_concern`, `household_receipt`, and matching `/api/aftercare/household-*` routes) while keeping the staff-gated `form` and `record_concern` contract unchanged.

Second, `neutral_text`, `strip_unsafe_sentences`, and `assert_templates_neutral` are hardened to close multiline and punctuation clause-masking bypasses (`:`, `!`, `?`, dashes, and newlines following uncertainty or negated-claim prefixes), fold invisible and hyphen separators, block additional causal, blame, and savings paraphrases, and guard every fixed template and dynamically generated string across `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py` while leaving the household's verbatim statement and representative authority text untouched.

### User Decisions and Requirements Highlights

* Deliver both target Issue #133 acceptance criteria inside `src/core` on branch `feat/quality-133-aftercare-concern-2142` without modifying `src/api` or pushing to the remote.
* Write all four `.copilot-tracking/` stage artifacts (`research/`, `plans/`, `changes/`, `reviews/`) in RPI order.
* Pass the exact bare verification command in `src/core` (`python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v`), then commit cleanly with the Copilot `Co-authored-by` trailer leaving `git status --short` empty.

### What You May Not Know

* In this multi-worktree environment, `~/.local` editable `.pth` files point to `/home/azureuser/source/ama/src/core/src`, which shadows linked worktrees when `unittest discover` runs without `PYTHONPATH=src`. Adding a small repo-local `src/core/tests/aftercare_fixture.py` imported by `test_aftercare*.py` prepends the active worktree's `src/core/src` safely without mutating shared user site-packages.
* Persisted `zf-aftercare-intake/1` snapshots remain 100% backward-compatible: `support_needed` defaults to `[]` when absent, and existing `staff_recorded` records with empty `support_needed` retain their exact 7-element SHA-256 request fingerprint.
* Engineering checks in `src/core` prove domain contracts, plain-language templates, and neutral-text enforcement, while end-to-end assistive-technology WCAG acceptance, named human owners, evaluator role sign-off, and the DPO outcome-data position remain external governance/UI gates documented honestly in `src/core/README.md`.

### Unresolved Decisions or Blockers

* None within `src/core` scope.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for Issue #133 on branch `feat/quality-133-aftercare-concern-2142` in `/home/azureuser/source/ama-demo-wt/feat-133-aftercare-concern-2142`.
* Deliver in `src/core`: a household or representative can raise an aftercare concern through an accessible route including a non-digital one (Issue #133 AC1; `docs/prd-zava-north-homes-retrofit-demonstrator.md` `FR-049`, `AC-063`).
* Deliver in `src/core`: no causation, blame, or savings promise appears in any generated or templated text (Issue #133 AC5; `docs/reference/research/ux/content-standard.md`).
* Write all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`).
* Verify in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*aftercare*.py' -v`.
* Commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` using privacy-safe repository-local Git email, and do not push (`git status --short` must be empty).

## Goals

* Enable both households and authorized representatives to raise aftercare concerns through accessible digital and non-digital routes (`phone`, `in_person`, `paper`, `assisted_visit`) with persisted optional communication/accessibility support adjustments and plain-language guidance.
* Eliminate causation, blame, and savings-promise bypasses and ensure every fixed template and dynamically generated string across `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py` is verified neutral without altering household verbatim statements.
* Preserve backward compatibility with persisted `zf-aftercare-intake/1` state documents, existing staff-assisted route contracts, and `src/api` aftercare screen expectations while ensuring bare `unittest discover` tests the active worktree.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/aftercare.py`: accessible support options (`SUPPORT_OPTIONS`, `SUPPORT_OPTION_CODES`, `SUPPORT_NOTE`, `normalize_support_needed`), optional `support_needed` field and validation in `intake_form` / `intake_errors`, plain-language `intake_error_summary`, `support_needed` persistence in `AftercareRegister.raise_concern` / `from_state`, hardened `neutral_text` / `strip_unsafe_sentences` / `assert_templates_neutral`, and neutrality checks on all templates and generated strings.
* `src/core/src/zava_forward/core/aftercare_intake.py`: `support_needed` support on `record_concern`, self-service accessible digital route (`household_form`, `submit_household_concern`, `household_receipt`, and `/api/aftercare/household-form` + `/api/aftercare/household-concerns` routes), backward-compatible `_validate` / `_fingerprint` / `_receipt` / `_display` handling for both `staff_recorded` and `digital` concerns, and comprehensive template/generated-string neutrality enforcement.
* `src/core/src/zava_forward/core/aftercare_store.py`: import-time `assert_templates_neutral` over all user-facing persistence/conflict/unconfirmed templates.
* `src/core/tests/aftercare_fixture.py`, `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, and `src/core/tests/test_aftercare_store.py`: local worktree `src` path resolution and focused semantic/adversarial tests.
* `src/core/README.md`: accurate documentation of delivered `src/core` aftercare capabilities and remaining external gates.

### Non-Goals

* Modifying `src/api` or `aftercare.js` (verified read-only for compatibility).
* Modifying shared `~/.local` Python site-packages or `.pth` files.
* Claiming human assistive-technology WCAG sign-off, named operational owners, evaluator role authorization, or DPO sign-off from `src/core` code.
* Pushing commits or editing GitHub Issue #133.

## Functional Requirements

* Accessible household and representative concern raising across digital and non-digital routes (`FR-049`, `AC-063`, Research `C1`, `C3`, `C5`, `C6`, `C8`, `C9`):
  * Observable acceptance criteria: Both `household` and `representative` (requiring non-empty `representative_basis` kept verbatim) can raise concerns via `AftercareRegister.raise_concern` (`digital` and `staff_recorded` across `phone`, `in_person`, `paper`, `assisted_visit`) and via `AftercareService` (`submit_household_concern` / `POST /api/aftercare/household-concerns` for accessible self-service digital intake with automatic plain-language `next_update` default and receipt readback `GET /api/aftercare/household-concerns/<id>?request_id=...`, plus `record_concern` / `POST /api/aftercare/concerns` for staff-assisted non-digital intake).
* Accessible communication/support adjustments and plain-language error guidance (Research `C1`, `C5`, `C12`, `C15`):
  * Observable acceptance criteria: `intake_form()` exposes `support_note`, `support_options`, and an optional `support_needed` field (`large_print`, `interpreter`, `call_back`, `support_person`) requiring no justification; `intake_errors()` validates `support_needed` when provided while keeping `intake_errors({})` restricted to the four required fields; `intake_error_summary()` produces one plain-language lead sentence naming the staff-assisted fallback; and `support_needed` round-trips through concern records, receipts, household views, and snapshots.
* Neutrality of all generated and templated text (Research `C4`, `C5`, `C7`, `C9`, `C11`, `C13`):
  * Observable acceptance criteria: `neutral_text()` rejects literal banned phrases, Unicode/invisible-character/hyphen evasions, causal/blame/savings paraphrases (`because of`, `attributable/attributed to`, `guarantee/promised savings`, `save/pay less on bills`, `blamed/blaming`, `wastes/wasted energy/heat`, `fault/error of the household`), and multiline/colon/exclamation/question/dash second-clause injections after uncertainty or negated-claim prefixes, while accepting neutral factual and genuine single-clause uncertainty/caveat statements; `assert_templates_neutral()` and `neutral_text()` guard every fixed template and dynamically generated string in `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py`; household `statement` and `representative_basis` remain verbatim and unblocked by `neutral_text`.

## Non-Functional Requirements

* Backward compatibility and state integrity (Research `C8`, `C10`, `C15`):
  * Objective threshold or evaluation condition: 100% of existing `AftercareRegister` and `zf-aftercare-intake/1` snapshots without `support_needed` restore cleanly with unchanged SHA-256 request fingerprints, and existing `src/api/tests/test_aftercare_screen.py` passes unmodified against the updated `src/core`.
  * Operating condition or verification approach, if needed: Unit snapshot/replay tests in `src/core/tests/test_aftercare*.py` and compatibility run of `test_aftercare_screen.py`.
  * Observable acceptance criteria: Zero regressions across all 123 baseline aftercare tests and `src/api` screen contract tests.
* Deterministic worktree verification and static quality (Research `C14`):
  * Objective threshold or evaluation condition: Zero `mypy` strict errors, zero `ruff check` findings, zero `ruff format --check` diffs, and zero failures in bare `python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` executed from `src/core`.
  * Operating condition or verification approach, if needed: Execute the caller's exact verification command in `src/core` without `PYTHONPATH`.
  * Observable acceptance criteria: Exit code `0` across all four chained commands with `test_aftercare*.py` verified to import modules from the current worktree `src/core/src`.

## Acceptance Criteria

* A household or authorized representative can raise an aftercare concern via both the accessible digital route (`AftercareRegister.raise_concern("digital", ...)` and `AftercareService.household_form` / `submit_household_concern` / `/api/aftercare/household-*`) and every non-digital channel (`phone`, `in_person`, `paper`, `assisted_visit` via `AftercareRegister` and `AftercareService.form` / `record_concern`), with optional `support_needed` adjustments preserved on records, receipts, and views, plain-language error summaries, and no jargon.
* Household `household_receipt` readback returns only the household-safe concern status and receipt when presented with the matching `request_id`, never exposing staff sensor context or other concerns.
* Every fixed template and dynamically generated string across `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py` passes `neutral_text()` / `assert_templates_neutral()`, and adversarial tests prove rejection of literal phrases, paraphrases, invisible/width/hyphen evasions, and multiline/punctuation clause-masking bypasses while preserving verbatim household `statement` and `representative_basis`.
* Pre-existing `zf-aftercare-intake/1` snapshots without `support_needed` load and replay identically, and `test_aftercare_screen.py` remains green.
* Test ownership and budget lock:
  * Canonical source targets: `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/src/zava_forward/core/aftercare_store.py`, `src/core/README.md`; generated targets: `none`.
  * Test targets: `src/core/tests/aftercare_fixture.py` (new worktree-local `src` import resolver), `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/core/tests/test_aftercare_store.py`.
  * Exact test removals: `none`.
  * Maximum test additions: at most 14 focused test methods across `test_aftercare.py`, `test_aftercare_intake.py`, and `test_aftercare_store.py` (semantic behavioral tests covering AC1 digital + non-digital + representative + `support_needed` routes, AC5 adversarial clause/paraphrase/template/generated-text guards, verbatim household free-text exemption, backward-compatible snapshot/fingerprint regression, and worktree `src` import provenance).
* Bare verification command in `src/core` (`python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v`) exits `0`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md                                                              |
| Phase details                    | .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md                                                   |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/133-aftercare-concern-2142-plan-critique.md (`Revise` executed once; `PC-001` through `PC-004` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-14/133-aftercare-concern-2142-research.md                                                       |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/133-aftercare-concern-2142-changes.md is created by implementation as its evidence record     |
| Planning execution and readiness | Complete; implementation-ready after disposing all single-pass critique findings                                                   |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions automatically to Implement                                                |

## Sources

* `.copilot-tracking/research/2026-11-14/133-aftercare-concern-2142-research.md`: Codebase evidence `C1`-`C16`, contrarian bypass discoveries, snapshot compatibility rules, and worktree `sys.path` root cause.
* `docs/prd-zava-north-homes-retrofit-demonstrator.md`: `FR-049` and `AC-063` requirements for accessible aftercare concern raising, non-digital parity, and neutral evaluator/generated wording.
* `docs/reference/research/ux/content-standard.md`: Plain-language standard, jargon exclusions, per-field guidance, and non-gatekept accessibility adjustments.
* `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py`, and `src/core/src/zava_forward/core/aftercare_store.py`: Target implementation modules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden Neutral-Text Guard and Accessible Register Contract in aftercare.py

* Intent: Close all clause-boundary, separator, and paraphrase bypasses in `neutral_text` / `strip_unsafe_sentences`, enforce `assert_templates_neutral` across all `aftercare.py` templates and generated strings, and add optional `support_needed` accessibility adjustments and plain-language `intake_error_summary` to `intake_form`, `intake_errors`, and `AftercareRegister`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden neutral_text, strip_unsafe_sentences, and template assertions in aftercare.py

* Requirement and evidence: Issue #133 AC5; Research `C4`, `C5`, `C6`, `C7`
* Expected result: `_variants`, `_UNCERTAIN`, `_NEGATED_CLAIM`, `PARAPHRASE_PATTERNS`, and `strip_unsafe_sentences` block literal phrases, invisible/width/hyphen evasions, additional causal/blame/savings paraphrases, and second-clause injections across newlines, colons, question/exclamation marks, dashes, and parentheses, while `assert_templates_neutral` and `neutral_text` guard every template and generated string in `aftercare.py`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add accessible support adjustments and plain-language error summary to intake_form, intake_errors, and AftercareRegister

* Requirement and evidence: Issue #133 AC1; Research `C1`, `C3`, `C5`, `C6`, `C12`, `C15`
* Expected result: `SUPPORT_OPTION_CODES`, `normalize_support_needed`, optional `support_needed` field in `intake_form()` and `intake_errors()`, `intake_error_summary()`, and backward-compatible `support_needed` storage/validation in `AftercareRegister.raise_concern` and `from_state` work cleanly without affecting `intake_errors({})` or `aftercare.js`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Add Accessible Household Digital Intake, Support Adjustments, and Template Guards in aftercare_intake.py and aftercare_store.py

* Intent: Deliver accessible household/representative self-service digital intake alongside existing staff-recorded non-digital channels in `AftercareService`, persist `support_needed` end-to-end with backward-compatible snapshots/fingerprints, and guard all templates and generated messages in `aftercare_intake.py` and `aftercare_store.py`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Extend AftercareService with household digital route, support_needed persistence, and backward-compatible state validation

* Requirement and evidence: Issue #133 AC1; Research `C2`, `C8`, `C9`, `C10`, `C11`, `C15`
* Expected result: `AftercareService` provides `household_form()`, `submit_household_concern()`, `household_receipt()`, and `/api/aftercare/household-form` + `/api/aftercare/household-concerns` routes alongside existing staff-gated `form()` and `record_concern()`, supports `support_needed` on both routes, keeps household `statement` and `representative_basis` verbatim, never exposes sensor context on household readback, and preserves existing `zf-aftercare-intake/1` snapshots and SHA-256 fingerprints.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Guard all fixed templates and generated strings in aftercare_intake.py and aftercare_store.py

* Requirement and evidence: Issue #133 AC5; Research `C9`, `C11`, `C13`, `C15`
* Expected result: Every fixed notice, label, error message, unknown entry, and dynamically formatted status/error/receipt/owner string in `aftercare_intake.py` and `aftercare_store.py` passes `assert_templates_neutral` at import time and `neutral_text` at runtime, using plain language without system jargon.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Worktree Test Resolution, Focused AC1/AC5 Tests, Documentation, and Bare Verification

* Intent: Ensure bare `unittest discover` imports from the active worktree `src/core/src`, add focused tests proving AC1 and AC5 and backward compatibility, update `src/core/README.md`, and pass full bare `mypy`, `ruff`, and `unittest` verification.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add worktree-local src resolver and focused AC1/AC5 unit and contract tests

* Requirement and evidence: Issue #133 AC1, AC5; Research `C4`, `C8`, `C10`, `C11`, `C12`, `C13`, `C14`
* Expected result: `src/core/tests/aftercare_fixture.py` guarantees `zava_forward.core` loads from the worktree's `src/core/src` under bare `unittest discover`, and focused tests in `test_aftercare.py`, `test_aftercare_intake.py`, and `test_aftercare_store.py` verify household/representative digital and non-digital routes, `support_needed` adjustments, adversarial neutral-text guards, verbatim household free-text exemption, store template neutrality, and snapshot backward compatibility within the 14-test addition cap.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Update src/core/README.md and run bare verification plus compatibility checks

* Requirement and evidence: Repository documentation and Focused-tier validation rules; Research `C14`, `C15`, `C16`
* Expected result: `src/core/README.md` accurately documents the accessible household/staff routes, optional support adjustments, hardened neutral-text guards, and remaining external gates; bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*aftercare*.py' -v` pass in `src/core`, alongside `test_dependency_rule.py` and `src/api/tests/test_aftercare_screen.py`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md

## Dependencies

* `zava_forward.core.chat_privacy`, `zava_forward.core.controls`, `zava_forward.core.workflows`, `zava_forward.core.ai_registry`, and `zava_forward.core.synthetic.sensor_scenarios`: Existing `src/core` siblings imported by `aftercare_intake` and tests (`test_dependency_rule.py` enforces `core`-only imports).
* Downstream read-only consumer `src/api/src/zava_forward/api/web/aftercare.js` and `src/api/tests/test_aftercare_screen.py`: Expects `form.fields` option entries to be `{value, label}` pairs and all visible strings to avoid causation, blame, savings promises, and banned jargon.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 (`PC-001`, High): Defaulted `next_update` breaks cross-UTC-day digital replay | applied | Updated `P02-T01` and `P03-T01` so digital/extended fingerprints hash caller-supplied `requested_next_update` (`None` when omitted, stored in `receipt["original"]["next_update"]`) and `work(doc)` resolves `request_id` replay before computing `today + 7 days` or checking `next_update >= today`. |
| Run 1 (`PC-002`, High): Savings paraphrase hits `_comparison` disclaimer, soft-wrap/hyphen gaps, and banned-phrase echo in `ValueError` | applied | Updated `P01-T01` to exempt narrow negated-verb disclaimers (`do/does/did not ... promise/claim/guarantee savings`), run `BANNED_PHRASES` on whitespace-collapsed text, preserve `\n` during `_UNCERTAIN`/`_NEGATED_CLAIM` stripping before second-stage whitespace collapse, match `\bmis[-_ ]?us(?:e|ed|es|ing)\b`, raise a non-echoing `ValueError`, and check `owner`/`sensor_context` neutrality in `from_state`. |
| Run 1 (`PC-003`, Medium): Direct subscripts on `channel`, `recorded_by`, and `support_needed` fail for `digital` and legacy records | applied | Updated `P01-T02` and `P02-T01` so `intake_errors` delegates directly to `normalize_support_needed`, `from_state` enforces canonical `list[str]` when present, and `_receipt`, `_display`, and `_validate` use `.get(...)` safely for `digital` and legacy records. |
| Run 1 (`PC-004`, Medium): `aftercare_fixture.py` must satisfy `ruff` `F401`/`I001` and evict preloaded stale `zava_forward.core*` modules | applied | Updated `P03-T01` so `aftercare_fixture.py` evicts stale `sys.modules["zava_forward.core*"]` outside `CORE_SRC` and all three `test_aftercare*.py` modules import and reference `CORE_SRC` cleanly. |

## Follow-Up Items

* Obtain assistive-technology and WCAG 2.2 AA acceptance evidence on a served resident-facing UI wired to `/api/aftercare/household-form` and `/api/aftercare/household-concerns` (outside `src/core`-only scope; owned by follow-up UI/UX slice on #133).
* Resolve evaluator role authorization and Data Protection Officer lawful-basis sign-off on outcome data (open governance dependencies on Issue #133).
* Deliver a served human-review screen and approved release evidence before enabling any model binding for `aftercare-concern-pack` (`FR-036`, Issue #133 AC6).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/133-aftercare-concern-2142-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none

