<!-- markdownlint-disable-file -->
# Review: Issue #133 Aftercare Accessible Concern Routes and Neutral-Text Enforcement in src/core

## Scope and Evidence

* Task ID: 133-aftercare-concern-2142
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Accessible household and representative concern raising across digital and non-digital routes (`FR-049`, `AC-063`, Issue #133 AC1 locally verifiable core contract) and neutral-text enforcement across all generated and templated text in `src/core` (`aftercare.py`, `aftercare_intake.py`, `aftercare_store.py`, Issue #133 AC5), including worktree-local bare `unittest` discovery, `src/core/README.md` documentation, and Focused-tier local verification.
* Plan: .copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/133-aftercare-concern-2142-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/133-aftercare-concern-2142-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/133-aftercare-concern-2142-research.md; `src/core` git diff; Focused-tier local checks (`mypy`, `ruff check`, `ruff format --check`, bare `unittest discover` on `test_*aftercare*.py` and `test_dependency_rule.py`, and `src/api/tests/test_aftercare_screen.py`).

## Opening Review State

* Interpreted review goal: Verify once with evidence that `P01`, `P02`, and `P03` satisfy all plan requirements, acceptance criteria, single-pass critique dispositions (`PC-001`–`PC-004`), implementation-time local judgments, test-budget limits, and Focused-tier validation without regressions or scope drift.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; research, plan, phase details, plan critique, changes record, and source/test/README diffs are complete and reconciled.
* Acceptance basis: Plan `## Functional Requirements`, `## Non-Functional Requirements`, `## Acceptance Criteria`, `## Critique Disposition` (`PC-001`–`PC-004`), and caller bare-verification contract.
* First comparison boundary: Plan-to-change marker reconciliation and `src/core` code/test diff verification against Issue #133 AC1 and AC5; excludes out-of-scope served UI/WCAG assistive-technology testing, live operational owner naming, DPO sign-off, evaluator role wiring, and model binding (`## Follow-Up Items`).
* Active read-only boundaries: This review stage creates and updates only `.copilot-tracking/reviews/logs/2026-11-14/133-aftercare-concern-2142-review.md` and mutates no source, test, documentation, plan, critique, research, or changes files.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass full-task review on 2026-11-14 across `.copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md`, `.copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-14/133-aftercare-concern-2142-plan-critique.md`, `.copilot-tracking/changes/2026-11-14/133-aftercare-concern-2142-changes.md`, `.copilot-tracking/research/2026-11-14/133-aftercare-concern-2142-research.md`, the `src/core` Git diff, Focused-tier verification runs, and an independent read-only review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01`, `P01-T02` | `### P01: Harden Neutral-Text Guard and Accessible Register Contract in aftercare.py` | Reconciled with minor code divergence (`RV-001`, `RV-002`, `RV-004`) | Plan markers checked; `SUPPORT_OPTIONS` replaced `"call_back"` with `"callback_window"` (`RV-001`) and `strip_unsafe_sentences` joins kept lines without a final joined pass (`RV-002`). |
| `P02`, `P02-T01`, `P02-T02` | `### P02: Add Accessible Household Digital Intake, Support Adjustments, and Template Guards in aftercare_intake.py and aftercare_store.py` | Reconciled (`RV-003` design boundary noted) | Plan markers checked; digital and staff-recorded routes, `PC-001` cross-day replay, `PC-003` legacy snapshot defaults, and import/runtime template guards match planned design; `request_id` readback authorization boundary recorded in `RV-003`. |
| `P03`, `P03-T01`, `P03-T02` | `### P03: Worktree Test Resolution, Focused AC1/AC5 Tests, Documentation, and Bare Verification` | Reconciled | `aftercare_fixture.py` (`PC-004`), 9 added focused tests (`<= 14` budget, `0` removals), `src/core/README.md`, and bare verification in `src/core` match planned completion evidence. |
| `## Follow-Up Items` | `## Follow-Up Items` in plan and changes record | Reconciled | All three external UI/WCAG, governance/DPO, and `FR-036` pack-screen follow-ups remain outside active `P01`–`P03` completion claims with named owners/next actions. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/aftercare.py` | Hardened `_variants`, `_UNCERTAIN`, `_NEGATED_CLAIM`, `PARAPHRASE_PATTERNS`, `neutral_text` (non-echoing `ValueError` + `@lru_cache`), `strip_unsafe_sentences`, `assert_templates_neutral`, and `owner`/`sensor_context` checks (`PC-002`). | `aftercare.py` diff and `EvaluatorTests` / `TemplateGuardTests`. | Passed bare `mypy`, `ruff`, and 39 tests in `test_aftercare.py`. | Implemented; see `RV-002` (joined multi-line sanitizer recheck) and `RV-004` (`responsible for` phrasing). |
| `P01-T02` | `src/core/src/zava_forward/core/aftercare.py` | Added `SUPPORT_OPTIONS`, `SUPPORT_OPTION_CODES`, `normalize_support_needed`, optional `support_needed` field in `intake_form()`/`intake_errors()`, `intake_error_summary()`, and `AftercareRegister` persistence/legacy snapshot support (`PC-003`). | `aftercare.py` diff and `IntakeFormTests`. | Passed bare `mypy`, `ruff`, `test_aftercare.py`, and `test_aftercare_screen.py`. | Partial code-to-plan alignment: `"callback_window"` used instead of planned `"call_back"` (`RV-001`). |
| `P02-T01` | `src/core/src/zava_forward/core/aftercare_intake.py` | Added `household_form()`, `submit_household_concern()`, `household_receipt()`, `/api/aftercare/household-*` routes, cross-UTC-midnight replay (`PC-001`), `support_needed` propagation, and legacy 7-tuple SHA-256 fingerprint preservation (`PC-003`). | `aftercare_intake.py` diff and `IntakeTests`. | Passed 50 tests in `test_aftercare_intake.py` and 43 tests (`skipped=15`) in `test_aftercare_store.py`. | Reconciled with planned contract; pre-API auth design gap noted in `RV-003`. |
| `P02-T02` | `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/src/zava_forward/core/aftercare_store.py` | Added import-time `assert_templates_neutral` over fixed service/store constants and runtime `neutral_text` checks on dynamic labels and error responses while keeping verbatim household `statement` and `representative_basis` untouched. | `aftercare_intake.py` and `aftercare_store.py` diffs; `NeutralTextTests` and `StoreNeutralityTests`. | Passed bare `mypy`, `ruff`, `test_aftercare_intake.py`, and `test_aftercare_store.py`. | Reconciled. |
| `P03-T01` | `src/core/tests/aftercare_fixture.py`, `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/core/tests/test_aftercare_store.py` | Added worktree `src` resolver (`PC-004`) and 9 focused AC1/AC5/regression test methods (`0` removals). | Test diffs and `CORE_SRC` provenance assertions. | Passed 132 tests (`skipped=15`) under bare `unittest discover`. | Reconciled within locked `<= 14` test budget. |
| `P03-T02` | `src/core/README.md` | Updated `#133` section to document accessible digital/non-digital routes, `support_needed`, hardened `neutral_text`, and explicit "Not delivered" boundaries. | `src/core/README.md` diff and link/hygiene review (zero `.copilot-tracking/` leaks in changed production/README files). | Passed bare `mypy`, `ruff check .`, `ruff format --check .`, `test_*aftercare*.py`, `test_dependency_rule.py`, and `test_aftercare_screen.py`. | Reconciled. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`aftercare._check_neutral`) | Added `@lru_cache(maxsize=512)` around pure `_check_neutral(text)` helper to avoid repeating regex scans on identical owner/template strings during 1000-record `from_state` tests. | Observed test runtime overhead during `SnapshotTests` and `SqliteAdapter`; ordinary local engineering judgment, no user decision needed. | Recorded in `.copilot-tracking/changes/2026-11-14/133-aftercare-concern-2142-changes.md` (`## Implementation-Time Plan and Detail Updates`). | Not needed; preserves exact `neutral_text` semantics and exception behavior (`lru_cache` never caches raised `ValueError`). | Reconciled and justified. |
| `P01-T02` (`aftercare.SUPPORT_OPTIONS`) | Expanded `SUPPORT_OPTIONS` to 7 communication/visit options (`large_print`, `easy_read`, `interpreter`, `bsl`, `callback_window`, `paper_letter`, `support_person`), replacing the planned `"call_back"` key with `"callback_window"`. | Local judgment noted in changes record, but plan `## Functional Requirements` and phase details `P01-T02` still name `"call_back"`. | Recorded in changes record only; `"call_back"` was not retained as a valid code or updated in plan/details. | Minor code-to-plan drift (`RV-001`). | Gap routed to `rpi-implement` (`RV-001`). |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four single-pass critique findings (`PC-001` cross-day replay ordering, `PC-002` negated-verb disclaimer + hyphen folding + non-echoing `ValueError` + `owner`/`from_state` guards, `PC-003` `normalize_support_needed` + safe `.get(...)` defaults on `digital`/legacy records, and `PC-004` `sys.modules` eviction + clean `CORE_SRC` assertions) are recorded in plan `## Critique Disposition` and verified in code.
* Material revisions: No material discovery during implementation required pausing dependent work, requesting a user decision, or returning to planning; critique was executed once and not repeated.
* Dependent-work pause assessment: Execution proceeded in dependency order (`P01` -> `P02` -> `P03`) with no premature continuation.
* Justification assessment: Supported for `@lru_cache(maxsize=512)`; `SUPPORT_OPTIONS` code rename (`callback_window` vs `call_back`) is flagged as `RV-001`.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Assistive-technology and WCAG 2.2 AA acceptance evidence on a served resident-facing UI wired to `/api/aftercare/household-*` | Caller bounded this task to locally verifiable `src/core` criteria (`Non-Goals` exclude `src/api` and browser UI wiring). | Next UI/UX slice on Issue #133 (`src/api` wiring + browser/AT validation). | Open distinct follow-up; kept outside `P01`–`P03` claims. |
| Evaluator role authorization and DPO lawful-basis sign-off on outcome data | Requires named human governance and DPO decisions outside `src/core` code. | Governance / DPO review on Issue #133 AC4. | Open distinct follow-up; kept outside `P01`–`P03` claims. |
| Served human-review screen and approved release evidence before enabling any model binding for `aftercare-concern-pack` | `ai_registry` keeps `aftercare-concern-pack` disabled and `UNAPPROVED` until release evidence and UI review exist (`FR-036`). | Future AI governance & UI slice on Issue #133 AC6. | Open distinct follow-up; kept outside `P01`–`P03` claims. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: `strip_unsafe_sentences` joins kept line fragments without re-validating cross-line concatenation

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/aftercare.py` (`strip_unsafe_sentences`) splits input on `(?<=[.!?])\s+|\s*\n+\s*`, checks each fragment individually with `neutral_text`, and returns `" ".join(kept)`. If a banned claim is wrapped across unpunctuated lines (for example `"Bills will\nfall."`), each fragment passes `neutral_text` in isolation while `" ".join(kept)` reconstructs `"Bills will fall."` (whereas `neutral_text("Bills will\nfall.")` itself properly rejects the unsplit text).
* Impact: Callers using `strip_unsafe_sentences` as a sanitizer on line-wrapped text can emit a reconstructed causal, blame, or savings phrase unless the joined output is re-checked with `neutral_text`.
* Destination: `rpi-implement`
* Smallest useful next action: Re-validate the joined result of `strip_unsafe_sentences` with `neutral_text` (or only split on newline boundaries that follow terminal punctuation / drop unsafe joined paragraphs) and add a unit test for `"Bills will\nfall."`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: `SUPPORT_OPTIONS` replaced planned `"call_back"` code with `"callback_window"`

* Related scope: `P01-T02`
* Evidence: `.copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md` (`## Functional Requirements`) and `.copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md` (`P01-T02`) specify `("large_print", "interpreter", "call_back", "support_person")`, whereas `src/core/src/zava_forward/core/aftercare.py` defines `"callback_window"` instead of `"call_back"`.
* Impact: Callers submitting `"call_back"` per the plan specification receive a `support_needed` validation error.
* Destination: `rpi-implement`
* Smallest useful next action: Include `"call_back"` in `SUPPORT_OPTIONS` (or normalize `"call_back"` / reconcile the canonical option code) and cover it in `IntakeFormTests`.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: `household_receipt` relies on caller-chosen `request_id` without route scoping or a server-minted receipt secret

* Related scope: `P02-T01`
* Evidence: `src/core/src/zava_forward/core/aftercare_intake.py` (`household_receipt`) authorizes `GET /api/aftercare/household-concerns/<cid>?request_id=...` solely by checking `receipt["request_id"] == request_id` across all stored concerns, including `staff_recorded` concerns, where `REQUEST_ID` accepts caller-chosen 8–64 character strings (`^[A-Za-z0-9_-]{8,64}$`).
* Impact: While `AftercareService` is currently unwired to any network server, exposing `GET /api/aftercare/household-concerns/<cid>` over HTTP without authenticated household identity or a server-generated high-entropy receipt token would allow guesses of low-entropy client `request_id` values to read household concern status (though `sensor_context` and `history` are omitted).
* Destination: `rpi-plan`
* Smallest useful next action: Before wiring `/api/aftercare/household-*` into `src/api`, plan authenticated household/representative session binding or a server-minted high-entropy receipt read token restricted to `digital` receipts.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Open-ended causal phrasing `"is responsible for"` is not matched by `PARAPHRASE_PATTERNS`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/aftercare.py` (`PARAPHRASE_PATTERNS`) blocks `caused by`, `due/owing/down to`, `because`, `attributable/attributed to`, `result/consequence of`, `resulting/arising/stemming from`, `triggered/provoked/created/produced/induced/driven by`, and `led to / resulted in`, but does not match `"The retrofit is responsible for damp"` if passed as `ai_summary` to `propose_pack`.
* Impact: Low current impact because all module templates are fixed and verified neutral and `aftercare-concern-pack` remains `UNAPPROVED` and disabled with no model route in `ai_registry`, but open-ended model summaries would need `"responsible for"` pattern coverage or structured template-only rendering before live enablement.
* Destination: `rpi-implement`
* Smallest useful next action: Add `rf"\b(?:{_RETROFIT}|{_HOUSEHOLD}s?)\s+(?:is|are|was|were)\s+(?:likely\s+)?responsible\s+for\b"` to `PARAPHRASE_PATTERNS` with a focused test in `EvaluatorTests`.

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: Stricter `neutral_text` checks inside `AftercareRegister.from_state` require migration care once live state exists

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/aftercare.py` (`AftercareRegister.from_state`) validates persisted `owner` and `sensor_context` through `neutral_text` as specified by `PC-002`.
* Impact: Safe for the current synthetic demonstrator (all 132 tests and seeded datasets pass), but future expansions of `PARAPHRASE_PATTERNS` after live deployment could refuse to load historical `sensor_context` entries unless paired with a state-version migration policy.
* Destination: `follow-up`
* Smallest useful next action: Define a snapshot schema version bump or read-time legacy-context quarantine policy before moving `zf-aftercare-intake/1` from synthetic demonstration data to live persistent records.

## Defects

* `RV-001` [Medium] -> `rpi-implement`: Re-check joined output in `strip_unsafe_sentences` so cross-line split claims (`"Bills will\nfall."`) cannot be reconstructed.
* `RV-002` [Medium] -> `rpi-implement`: Restore or alias planned `"call_back"` code in `SUPPORT_OPTIONS` so code and plan `P01-T02` match cleanly.
* `RV-004` [Low] -> `rpi-implement`: Extend `PARAPHRASE_PATTERNS` to cover `"is/was responsible for"` causal phrasing in `propose_pack` summaries.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Hardening pass in `src/core/src/zava_forward/core/aftercare.py` (`strip_unsafe_sentences`) + 1 test in `test_aftercare.py` | Implementation defect within current accepted design |
| `RV-002` | `rpi-implement` | Align `SUPPORT_OPTIONS` `"call_back"` code in `src/core/src/zava_forward/core/aftercare.py` with `P01-T02` | Implementation drift from planned option code |
| `RV-003` | `rpi-plan` | Define household authentication or high-entropy server receipt token before `src/api` HTTP exposure | Architectural/security design choice for `household_receipt` |
| `RV-004` | `rpi-implement` | Add `"responsible for"` causal pattern to `PARAPHRASE_PATTERNS` in `aftercare.py` | Implementation hardening within existing regex guard |
| `RV-005` | `follow-up` | Pre-production state-version migration rule before non-synthetic deployment | Non-blocking lifecycle governance follow-up |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-005` (snapshot schema migration policy for future `neutral_text` expansions on live persisted state) plus the three canonical plan `## Follow-Up Items`: served resident/staff UI wiring with WCAG 2.2 AA assistive-technology evidence, evaluator role + DPO lawful-basis sign-off, and `aftercare-concern-pack` review screen + `FR-036` release evidence.

## Blockers and Remaining Work

* Blockers: none for completing this `src/core` RPI loop; Issue #133 overall closure remains gated on the external UI/WCAG, named operational owner, DPO/evaluator-role, and `FR-036` pack-screen criteria (`Refs #133`).
* Remaining active work: none in declared `P01`–`P03` plan scope; routed findings `RV-001`–`RV-004` belong to later user-selected RPI invocations.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (308 source files, bare) | Passed | `Success: no issues found in 308 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (255 files) | Passed | `255 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` | `src/core` (`test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_store.py`, bare) | Passed | `Ran 132 tests in 170.196s — OK (skipped=15)` (`15` skips are opt-in disposable MSSQL contract tests gated on `ZF_RESIDENT_MSSQL=1`) |
| `python3 -m unittest discover -s tests -p 'test_dependency_rule.py' -q` | `src/core` import boundary | Passed | `Ran 2 tests in 2.559s — OK` |
| `PYTHONPATH=../core/src:../agents/src:src python3 -m unittest discover -s tests -p 'test_aftercare_screen.py' -q` | `src/api` downstream screen compatibility | Passed | `Ran 17 tests in 0.892s — OK` |
| Hosted GitHub Actions CI | Repository PR workflows | Unavailable | Task explicitly forbids pushing (`Do NOT push`); hosted CI runs only on remote push/PR |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned execution (`P01`–`P03`) and Focused-tier bare verification in `src/core` completed with 132 passing tests (`skipped=15`), delivering accessible household/representative digital and non-digital concern routes, `support_needed` persistence, template-wide neutrality assertions, and clause/evasion hardening. Independent review identified concrete non-crashing defects and design follow-ups (`RV-001` cross-line re-join in `strip_unsafe_sentences`, `RV-002` `"callback_window"` vs planned `"call_back"` code, `RV-003` caller-chosen `request_id` readback token design before HTTP wiring, and `RV-004` `"responsible for"` causal phrasing), so per RPI review discipline the outcome is recorded honestly as `Defects found` and routed cleanly without mutating artifacts during Review.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Resolve `RV-001` (`strip_unsafe_sentences` joined recheck), `RV-002` (`"call_back"` option code alignment), and `RV-004` (`"responsible for"` pattern) in `src/core/src/zava_forward/core/aftercare.py` |
| Decision gap or invalid assumption | `rpi-plan` | Resolve `RV-003` (authenticated household binding or server-minted high-entropy receipt token for `household_receipt` before `src/api` route exposure) |
| Material evidence gap | none | No research gap identified within `src/core` scope |
| Non-blocking residual work | Distinct follow-up items | `RV-005` snapshot migration policy before live state cutover + plan `## Follow-Up Items` (served UI/WCAG AT evidence, evaluator role & DPO sign-off, `FR-036` pack review screen) |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused tier passed (`mypy`, `ruff check`, `ruff format --check`, 132 bare `test_*aftercare*.py` tests with 15 opt-in MSSQL skips, `test_dependency_rule.py`, and `src/api/tests/test_aftercare_screen.py`); hosted CI unavailable locally (`Do NOT push`).
* Blockers: none for `src/core` task completion; external UI/WCAG and governance criteria on Issue #133 remain open (`Refs #133`).

