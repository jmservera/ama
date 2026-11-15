<!-- markdownlint-disable-file -->

# Task Research: aftercare-133-2346

| Field              | Value                                                                   |
|--------------------|-------------------------------------------------------------------------|
| Date               | 2026-11-14                                                              |
| Researcher / agent | rpi-research (via RPI Agent)                                            |
| Status             | Complete                                                                |
| Artifact path      | .copilot-tracking/research/2026-11-14/aftercare-133-2346-research.md    |

## Research Brief

* What to research: Current implementation, API surface, core domain logic, neutral-language guards, evaluator lived-performance views, and test coverage for Issue #133 (`Aftercare concern route and lived-performance review`), specifically auditing commit `94aa804a5` (`#1744`) against all remaining acceptance criteria in `src/core` and `src/api`.
* Why it matters: Identify exact gaps between delivered core models/helpers and the complete Issue #133 contract (accessible digital + staff-recorded non-digital intake channels, immutability across handover/financial closure, sensor non-dismissal rule, deterministic causation/blame/savings-promise guard across generated/templated/evaluator outputs, evaluator baseline/outcome/denominator/unknown preservation, and `FR-036` proposal-only AI concern pack).
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases for completing local engineering and verification on `feat/demo-133-aftercare-concern-2346`.
* Scope: `src/core`, `src/api`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (`FR-049`, `AC-063`, `FR-036`), and `docs/reference/research/ux/customer-journeys/` (`customer-journey-atlas.md`, `programme.md`, `residents.md`).
* Non-goals: Live external identity enrolment, DPO formal sign-off, paid LLM inference, or pushing to remote.
* Criteria: Every acceptance criterion of Issue #133 mapped to concrete `path:line` evidence; exact gap analysis for `src/core` and `src/api`; verification that tests avoid bulk `del sys.modules[...]`.
* Requested outputs: Convergence recommendation for completing Issue #133 engineering and tests cleanly across `src/core` and `src/api`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                              |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | What parts of Issue #133 are already implemented in `src/core` and `src/api`, and what exact engineering/API/guard/test gaps remain?                               |
| Codebase scope                       | `src/core/`, `src/api/`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/reference/research/ux/customer-journeys/`                              |
| External scope                       | none (bounded internal repository task)                                                                                                                            |
| Initial internal candidate areas     | `src/core/zava_core/` aftercare/handover/resident modules, `src/api/` routes/schemas/templates/services, PRD `FR-049`/`AC-063`/`FR-036`, journey maps `O13`/`O14`  |
| Initial external candidate areas     | none                                                                                                                                                               |
| Research posture                     | balanced                                                                                                                                                           |
| Posture provenance                   | default (bounded internal task with named source targets where adjacent API/template/evaluator surfaces in `src/api` could affect completeness)                    |
| Explicit limits / deadline           | Local worktree `/home/azureuser/source/ama-demo-wt/feat-133-aftercare-concern-2346`, branch `feat/demo-133-aftercare-concern-2346`, commit locally, do not push    |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across `src/core`, `src/api`, and PRD/journey contracts                                                              |
| Edits allowed during research?       | no, research-only                                                                                                                                                  |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                                                       |
| Known constraints / excluded sources | Do NOT use bulk `del sys.modules[...]` in test files; preserve `unknown` without coercion to `none` or `0`; keep AI concern packs proposal-only (`FR-036`)         |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                            | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|---------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches workspace inputs and tracking artifacts | Adds validation tiers, regulatory/UX/branch rules, and Markdown style            | Selected: mandatory repository instructions                                               |
| Skill               | `python-foundational`                 | Python typing, unittest, ruff, and mypy practices               | On-demand Python engineering guidance                                            | Skipped in research: read-only investigation does not require Python scaffolding templates |
| Skill               | `web-design-guidelines`               | Web UI guidelines when editing web/HTML surfaces                | UI review rules if `src/api` static HTML/JS changes                              | Deferred to Plan/Implement only if web UI files require changes                           |
| Research specialist | `hve-core-all:rpi-researcher`         | Visible subagent for independent delegated research lanes       | Lane artifact under `.copilot-tracking/research/subagents/2026-11-14/`           | Skipped (inline preferred): tightly coupled `src/core` + `src/api` trace fits fast inline search |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                    |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI execution with comprehensive caller brief specifying objective, constraints, validation, and git rules | N/A (non-interactive) | Proceed with `balanced` posture in `convergence` mode across `src/core` & `src/api` |
| Direction change | None at intake                                                                                                         | N/A                  | Active brief retained                                                              |
| Convergence      | Non-interactive CLI execution; single evidence-backed vertical refinement covers all three Issue #133 objectives | N/A (non-interactive) | Selected surgical `src/core` + `src/api` refinement; Planning Readiness `Ready`    |

## Scope and Success Criteria

* Scope: `src/core`, `src/api`, PRD `FR-049`/`AC-063`/`FR-036`, and UX journey maps `O13`/`O14` for aftercare concern intake, neutral-language guardrails, closure immutability, sensor non-dismissal, and evaluator lived-performance review.
* Assumptions: Commit `94aa804a5` delivered part of `src/core` for `#133`, while `src/api` endpoints/views or cross-surface templated/generated guards or staff-recorded non-digital parity may still have gaps (to verify from code and git history).
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs in convergence mode and one recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Accessible concern-intake route (digital + staff-recorded non-digital channels: `phone`, `paper`, `in_person`, `representative`, etc.) preserving original account, channel, owner, investigation outcome, and remedy status across handover/financial closure and never dismissing a resident report due to normal sensors.
  2. Deterministic no-causation, no-blame, and no-savings-promise guard enforced and tested across generated, templated, or evaluator/aftercare summary text.
  3. Evaluator baseline & outcome view showing baseline, outcomes, and unresolved concerns with stated denominators and unknowns (`unknown` preserved, never coerced to `none` or `0`), with optional AI concern pack kept as a registered proposal requiring human review (`FR-036`).
* Inferred research questions:
  * Q1: What exact requirements do PRD `FR-049`, `AC-063`, `FR-036` and journey maps `O13`/`O14` set for Issue #133?
  * Q2: What did commit `94aa804a5` and earlier commits (`#88`, `#91`, `#111`, `#129`, `#154`) already implement in `src/core`?
  * Q3: What routes, models, services, templates, or agent/summary outputs exist in `src/api` (and `src/agents` / `src/orchestrator` if touched by `src/api`) for aftercare concerns and evaluator lived-performance views, and what is missing?
  * Q4: Are there bypass paths, edge cases in the neutral-language guard, coercion bugs (`unknown` -> `0`/`none`), closure mutation paths, or test anti-patterns (`del sys.modules`) that could violate Issue #133?
* Caller constraints and non-goals: Research-only during `rpi-research`; no `del sys.modules[...]` bulk deletion in tests; commit locally on `feat/demo-133-aftercare-concern-2346` without pushing.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                         |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------|
| narrow                                                   | Target `src/core` and/or `src/api` local engineering and verification for Issue #133                    | Caller intake       | Bounds scope to local demonstrator packages and tests                     |
| exclude                                                  | Do NOT use bulk `del sys.modules[...]` in test files; do NOT push to remote                             | Caller intake       | Constrains test design and final git actions                              |

## Research Questions

|  # | Sub-question                                                                                                                | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What are the exact specifications in PRD (`FR-049`, `AC-063`, `FR-036`) and UX journeys (`O13`, `O14`) for Issue #133?      | straightforward | H        | answered |
| Q2 | What does `src/core` already implement for aftercare concern intake, closure protection, sensor non-dismissal, and guards?  | depth           | H        | answered |
| Q3 | How does `src/api` expose aftercare concern intake (digital + non-digital) and the evaluator lived-performance review view? | breadth         | H        | answered |
| Q4 | Where can generated, templated, or evaluator/aftercare text bypass neutral-language guards or coerce `unknown` values?       | depth           | H        | answered |

## Research Cycles

### Cycle 1

* Cycle goal: Audit existing `#133` engineering across `src/core` and `src/api`, identify every remaining gap against the three objectives and test constraints, and challenge assumptions before planning.
* Selected posture: `balanced`

#### Wave 1 — Wider

* Mode: Inline (tightly coupled across `aftercare.py`, `aftercare_intake.py`, `aftercare_store.py`, `server.py`, and `web/aftercare.js`)
* Breadth explored:
  * Git commit `94aa804a5` (`133-aftercare-concern-2142`), review log `.copilot-tracking/reviews/logs/2026-11-14/133-aftercare-concern-2142-review.md`, and Issue `#133` checklist (`gh issue view 133`).
  * Problem specification (`docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`), sector primer (`docs/reference/research/sector/housing-association-primer.md`), UX journeys (`docs/reference/research/ux/customer-journeys/programme.md`), and PRD (`docs/prds/zava-forward-retrofit-programme-demonstrator.md` covering `FR-049`, `AC-063`, `FR-036`, `CON-003`, `CON-008`).
  * Core modules (`aftercare.py`, `aftercare_intake.py`, `aftercare_store.py`, `ai_registry.py`, `resident_access.py`, `sensor_status_text.py`, `sensor_review_draft.py`, `quality.py`).
  * API and UI modules (`server.py`, `workbench.py`, `web/aftercare.js`, `web/role-screens.js`, `resident_demo/app.py`) and test/check modules (`aftercare_fixture.py`, `test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_store.py`, `test_aftercare_served.py`, `test_aftercare_screen.py`, `test_role_endpoint_inventory.py`, `checks/aftercare_browser_check.py`).
* Reflection: Core data structures and persistence (`AftercareRegister`, `AftercareService`, `DocumentStateStore`) exist, while targeted functional, deterministic-guard, UI-contract, and test-harness gaps remain across `src/core` and `src/api`.

#### Wave 2 — Deeper

* Mode: Inline
* Prioritized deep inspection findings:
  1. Test-isolation hazard (`aftercare_fixture.py`): `src/core/tests/aftercare_fixture.py:21-32` loops over `list(sys.modules)` and pops `zava_forward.core*` modules whenever loaded from the shared editable install (`/home/azureuser/source/ama/src/core/src`), directly violating the prompt constraint forbidding bulk `sys.modules` eviction during `unittest discover`. Prepending `CORE_SRC` to `sys.path` and updating namespace `__path__` in-place avoids evicting loaded classes (`C1`, `C2`).
  2. Accessible digital + non-digital channel & UI gaps:
     * `NON_DIGITAL_CHANNELS` in `src/core/src/zava_forward/core/aftercare.py:21` includes `("phone", "in_person", "paper", "assisted_visit")` without `"representative"`, whereas the brief specifies `phone`, `paper`, `in_person`, `representative`, etc. (`C3`, `C4`).
     * `SUPPORT_OPTIONS` (`aftercare.py:39-47`) uses `"callback_window"` without normalizing legacy/alternate `"call_back"` (`C3`).
     * `AftercareService.household_receipt` (`aftercare_intake.py:655-696`) allows reading `staff_recorded` concern receipts if their `request_id` is supplied instead of restricting `/api/aftercare/household-concerns/<id>` to `route == "digital"` (`C5`).
     * `src/api/src/zava_forward/api/web/aftercare.js:8-33,86-200,308-312` lacks channel labels (`phone`, `in_person`, `paper`, `assisted_visit`, `representative`, and digital self-service fallback), renders `"Unknown (Unknown)"` / `"via Unknown"` for digital receipts/concerns, renders `<p>Unknown</p>` when `form.owner_note` is absent on `household_form()`, and ignores `spec.multiple` on `support_needed` in `acField`/`acReadValues` (`C10`).
  3. Deterministic neutral-text guard gaps (`aftercare.py`, `aftercare_intake.py`):
     * `strip_unsafe_sentences` (`aftercare.py:250-261`) splits on unpunctuated newlines and joins kept fragments with `" "`, letting `"Bills will\nfall."` bypass fragment checks and reconstruct `"Bills will fall."` (`C6`).
     * `PARAPHRASE_PATTERNS` (`aftercare.py:102-157`) misses resident-blame phrasings around occupant thermostat/ventilation/window/lifestyle/habits use (e.g., `"occupant lifestyle"`, `"poor ventilation habits"`, `"incorrect thermostat settings"`, `"not ventilating properly"`, `"left windows closed"`, `"turned the thermostat down"`, `"drying clothes indoors"`, `"user error"`), finite causal verbs (`"stems from"`, `"arises from"`, `"results from"`, `"is responsible for"`), and broader `"due/owing/down to"` thermostat/ventilation/lifestyle blame or bill-reduction promises (`"guaranteed bill reduction"`, `"slash your bills"`) (`C7`).
     * Staff-authored `evidence` in `AftercareRegister.record_outcome` (`aftercare.py:579`), `AftercareRegister.set_remedy` (`aftercare.py:591`), `AftercareRegister.review_pack` (`aftercare.py:743`), snapshot restore `AftercareRegister.from_state` (`aftercare.py:451-497`), and `AftercareService.record_outcome`/`set_remedy` (`aftercare_intake.py:944-969`) are not checked with `neutral_text`, allowing staff outcome/remedy notes to record causation, resident blame, or savings promises while household verbatim `statement` and `representative_basis` stay unrestricted (`C8`, `C9`).
  4. Evaluator baseline/outcome view & `FR-036` optional AI concern pack:
     * `aftercareEvaluatorView` (`aftercare.js:202-237`) coerces missing/non-array/`"unknown"` `row.concerns` via `(row.concerns || []).length` to `"0"` and `"No concerns raised"`, can dereference null `cmp.baseline` if `status === "sufficient"` lacks nested objects, and renders `"Unknown of Unknown"` if `homes_with_usable_comparison` is null/`"unknown"` (`C11`).
     * `AftercareRegister.propose_pack` (`aftercare.py:701-730`) and `AftercareService.evaluator_view` (`aftercare_intake.py:1066-1110`) do not expose explicit `FR-036` `ai_registry` metadata (`approval_state: "unapproved"`, `live_authorized: False`, `requires_human_review: True`, `manual_route`) on packs and evaluator responses (`C12`, `C13`).

#### Wave 3 — Contrarian

* Mode: Inline
* Counter-evidence and challenges tested:
  1. Should `/api/aftercare/household-form` and `/api/aftercare/household-concerns` bypass staff auth in `src/api/src/zava_forward/api/server.py`?
     * Counter-evidence: `server.py:527-529,1358-1360` enforces authenticated staff sessions on every `/api/*` endpoint except `/api/login`, and `src/api/tests/test_role_endpoint_inventory.py:15-48,137-155` asserts that unauthenticated callers and contractors are denied across `server.py`. Resident-facing showcase routes live in separate isolated apps (`resident_demo/app.py`) under PRD `OD-54`/`CON-009` (`C14`, `C15`). Opening unauthenticated write endpoints on `server.py` would violate staff-server security invariants. Keeping the digital household contract in `AftercareService` (`handle` + `aftercare.js` view builders) while keeping `server.py` staff-authenticated preserves security boundaries.
  2. Would enforcing `neutral_text` on `quality.py:add_aftercare` help Objective 2?
     * Counter-evidence: `src/core/src/zava_forward/core/quality.py:392-395` prompts `"Say what the resident reported or what was done."` Blocking resident-reported quotes in `#87` quality handover logs would suppress verbatim resident reports (`C16`). Leaving `quality.py` untouched and scoping `neutral_text` to `#133` aftercare generated/templated/staff-outcome/remedy/pack/evaluator text avoids regressions while keeping household `statement` and `representative_basis` verbatim.
  3. Could tightening `PARAPHRASE_PATTERNS` for thermostat/ventilation blame cause false positives on legitimate resident-reported or uncertain text?
     * Counter-evidence: Statements like `"Not sure how to use the controls"`, `"Concern kind: control_use."`, `"Resident reported cold room"`, `"Cannot determine whether thermostat settings contributed"`, and `"We do not guarantee or promise savings."` must remain valid. Scoping patterns to blame/causal/promise constructions (while preserving `_UNCERTAIN` and `_NEGATED_CLAIM` single-clause exemptions) prevents false positives.
  4. Should `AftercareService.handle` expose HTTP routes to invoke or approve AI concern packs?
     * Counter-evidence: `src/core/tests/test_aftercare_intake.py:592-600` (`test_there_is_no_route_to_propose_or_accept_a_pack_so_no_record_can_change`) explicitly requires `POST /api/aftercare/concerns/<id>/{pack,packs,concern-pack}` to return `404`/`405` because `aftercare-concern-pack` is `disabled` and `unapproved` in `ai_registry.py:132-141` (`C12`, `C13`). Surfacing read-only `concern_pack_task` (`FR-036`) registry governance metadata in `evaluator_view` and `propose_pack` proves proposal-only human-review gating without opening an unapproved live endpoint.
* Re-entry decision: All four research questions (`Q1`–`Q4`) have direct codebase evidence and contrarian verification; source coverage is saturated under the `balanced` posture, so Cycle 2 is not needed.

## Candidate Research Areas

| Area | Status | Rationale | Evidence |
| --- | --- | --- | --- |
| `aftercare_fixture.py` in-place path setup without `sys.modules` eviction | Accepted | Eliminates class-identity breakage during `unittest discover` and satisfies explicit caller constraint | `C1`, `C2` |
| Non-digital `"representative"` channel, `"call_back"` support alias, and digital-only `household_receipt` scoping | Accepted | Completes digital + non-digital accessible concern intake (`phone`, `paper`, `in_person`, `assisted_visit`, `representative`) and hardens receipt isolation | `C3`, `C4`, `C5` |
| Deterministic neutral-text guard hardening (`strip_unsafe_sentences`, thermostat/ventilation/lifestyle blame, causal verbs, staff outcome/remedy/pack-review guard) | Accepted | Closes multiline strip bypass, thermostat/ventilation/lifestyle blame paraphrases, causal verbs, and staff outcome/remedy/pack evidence paths while preserving verbatim household text | `C6`, `C7`, `C8`, `C9` |
| `aftercare.js` channel/route/multi-support labels, `unknown` non-coercion, and `FR-036` concern-pack governance metadata in `evaluator_view` | Accepted | Ensures UI and evaluator contracts preserve `unknown` (never coerced to `none` or `0`), render digital + non-digital concerns cleanly, and surface `FR-036` human-review proposal status | `C10`, `C11`, `C12`, `C13` |
| Unauthenticated `/api/aftercare/household-*` exposure on staff `server.py` | Rejected | Violates staff authentication boundary in `server.py` and `test_role_endpoint_inventory.py`; resident portal auth remains gated by `OD-54` | `C14`, `C15` |
| Applying `neutral_text` to `quality.py:add_aftercare` | Rejected | `#87` handover notes capture what residents reported; filtering them would block verbatim resident accounts | `C16` |
| Live model endpoint for `aftercare-concern-pack` | Deferred | Task is `unapproved` and `disabled` in `ai_registry.py` under `FR-036`; requires separate release/threshold approval outside `#133` | `C12`, `C13` |

## Evidence Log

| ID | Location | Observation |
| --- | --- | --- |
| `C1` | `src/core/tests/aftercare_fixture.py:21-32` | Loops over `list(sys.modules)` and calls `sys.modules.pop` on `zava_forward.core*` modules outside `CORE_SRC`, risking duplicate class identity across `unittest discover`. |
| `C2` | `.github/workflows/src-ci.yml:86-88` | CI runs `python -m unittest discover -s tests -v` with package `PYTHONPATH`, expecting stable single-load module identity across test files. |
| `C3` | `src/core/src/zava_forward/core/aftercare.py:20-49` | Defines `ROUTES = ("digital", "staff_recorded")`, `NON_DIGITAL_CHANNELS = ("phone", "in_person", "paper", "assisted_visit")` (missing `"representative"`), `CONCERN_KINDS`, and `SUPPORT_OPTIONS` (`"callback_window"` without `"call_back"` alias). |
| `C4` | `src/core/src/zava_forward/core/aftercare_intake.py:68-73,559-564` | Maps `NON_DIGITAL_CHANNELS` via `CHANNEL_LABELS` into staff intake form options. |
| `C5` | `src/core/src/zava_forward/core/aftercare_intake.py:655-696` | `household_receipt` checks `request_id` match without checking `rec.get("route") == "digital"`, permitting staff-recorded concern receipts on the household endpoint if `request_id` is known. |
| `C6` | `src/core/src/zava_forward/core/aftercare.py:88-177,223-261` | `BANNED_PHRASES`, `PARAPHRASE_PATTERNS`, `neutral_text`, and `strip_unsafe_sentences`; `strip_unsafe_sentences` splits on `\s*\n+\s*` and joins kept fragments without re-validating the joined result. |
| `C7` | `src/core/src/zava_forward/core/aftercare.py:102-157` | `PARAPHRASE_PATTERNS` covers basic household fault/savings phrases but omits occupant lifestyle/habits, thermostat/ventilation/window blame phrasings, `"user error"`, finite `"stems/arises/results from"`, and `"is responsible for"`. |
| `C8` | `src/core/src/zava_forward/core/aftercare.py:451-497,565-600,732-748` | `record_outcome`, `set_remedy`, `review_pack`, and `from_state` do not run `neutral_text` on staff-recorded `evidence` or pack-review `reason`. |
| `C9` | `src/core/src/zava_forward/core/aftercare_intake.py:944-969` | `AftercareService.record_outcome` and `set_remedy` run `_free_text` (length + PII guard) without validating `neutral_text(evidence)`. |
| `C10` | `src/api/src/zava_forward/api/web/aftercare.js:8-33,86-190,308-312` | `AFTERCARE_LABELS` omits channel codes and digital route labels; `acField`/`acReadValues` ignore `spec.multiple` on `support_needed`; `aftercareFormView` renders `"Unknown"` when `owner_note` is absent on `household_form()`. |
| `C11` | `src/api/src/zava_forward/api/web/aftercare.js:191-237` | `aftercareEvaluatorView` coerces non-array/null/`"unknown"` `row.concerns` via `(row.concerns \|\| []).length` to `"0"` and `"No concerns raised"`, and assumes `cmp.baseline`/`cmp.late` objects exist whenever `cmp.status === "sufficient"`. |
| `C12` | `src/core/src/zava_forward/core/ai_registry.py:22,132-141` | Registers `CONCERN_PACK_TASK = "aftercare-concern-pack"` under `FR-036` as `kind="proposal-pack"`, `enabled=False`, `state="disabled"`, `approval_state="unapproved"`, `authorizes_live=False`. |
| `C13` | `src/core/tests/test_aftercare_intake.py:592-600` | Asserts `POST /api/aftercare/concerns/AC-001/{pack,packs,concern-pack}` returns `404` or `405` so unapproved AI packs cannot mutate concerns over HTTP. |
| `C14` | `src/api/src/zava_forward/api/server.py:527-529,628-635,1358-1398` | Enforces staff session authentication and `projection.allowed` before delegating `/api/aftercare/*` to `app.aftercare.handle`. |
| `C15` | `src/api/tests/test_role_endpoint_inventory.py:30,45,137-155` | Verifies role authorization across every `/api/*` route in `server.py`, denying unauthenticated and contractor callers. |
| `C16` | `src/core/src/zava_forward/core/quality.py:392-402` | `#87` `add_aftercare` records free-text resident handover contact notes and is distinct from `#133` structured aftercare concerns. |
| `C17` | `docs/reference/research/ux/customer-journeys/programme.md:92-120` | Defines Independent QA inspector / retrofit evaluator journey (`O13`/`O14`): normal sensors cannot negate a resident report; aftercare explanations stay staff-reviewed proposals. |
| `C18` | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:585-590,2030-2046` | Requires all AI features to be registered under `FR-036` before activation, preserves human decision rights (`CON-003`), and prohibits presenting scenarios/figures as guarantees (`CON-008`). |

## Findings and Answers

* `Q1` (PRD `FR-049`, `AC-063`, `FR-036` and UX journeys `O13`, `O14`):
  * Household or representative concerns (`discomfort`, `higher_bill`, `control_use`, `other`) must be raisable through accessible digital and staff-recorded non-digital channels without detriment, normal sensors never negate or close a resident report, handover/financial closure cannot erase open concerns or remedies, evaluator views report baseline/outcomes/unresolved counts with stated denominators and preserved unknowns without causation/blame/savings claims, and any AI concern pack remains a registered proposal under `FR-036` requiring named human review (`C12`, `C17`, `C18`).
* `Q2` (`src/core` current coverage and gaps):
  * `AftercareRegister`, `AftercareService`, and `DocumentStateStore` implement concern intake, idempotent replay, closure immutability, sensor non-dismissal, and baseline comparison, while missing `"representative"` in `NON_DIGITAL_CHANNELS`, `"call_back"` support aliasing, digital-only `household_receipt` scoping, `FR-036` registry fields on packs/evaluator responses, and `sys.modules`-safe worktree fixture loading (`C1`, `C3`, `C4`, `C5`, `C12`).
* `Q3` (`src/api` exposure and UI gaps):
  * `server.py` serves `/api/aftercare/*` behind staff session auth (`C14`, `C15`), and `web/aftercare.js` renders `#/aftercare` plus `aftercareScreens` view builders, while missing channel/route/support labels, `spec.multiple` support on `support_needed`, digital-form `owner_note` handling, and `FR-036` concern-pack governance display (`C10`).
* `Q4` (Neutral-language guard bypasses and `unknown` coercion):
  * `strip_unsafe_sentences` allows newline-split banned sentences to recombine (`C6`); `PARAPHRASE_PATTERNS` misses thermostat/ventilation/lifestyle blame, finite `"stems/arises/results from"`, `"is responsible for"`, and bill-reduction guarantees (`C7`); staff-recorded `outcome["evidence"]`, `remedy["evidence"]`, and `review_pack` `reason` skip `neutral_text` (`C8`, `C9`); and `aftercareEvaluatorView` coerces non-array/unknown `row.concerns` to `"0"` / `"No concerns raised"` (`C11`).

## Convergence Recommendation

* Selected approach: Surgical vertical refinement across `src/core` (`aftercare.py`, `aftercare_intake.py`, `aftercare_fixture.py`, `test_aftercare.py`, `test_aftercare_intake.py`, `README.md`) and `src/api` (`web/aftercare.js`, `test_aftercare_screen.py`, `test_aftercare_served.py`, `README.md`):
  1. Remove `sys.modules.pop` from `src/core/tests/aftercare_fixture.py` in favour of `sys.path` and in-place namespace `__path__` ordering (`C1`, `C2`).
  2. Add `"representative"` to `NON_DIGITAL_CHANNELS` and `CHANNEL_LABELS`, normalize `"call_back"` -> `"callback_window"` in `normalize_support_needed`, and restrict `household_receipt` to `route == "digital"` (`C3`, `C4`, `C5`).
  3. Fix `strip_unsafe_sentences`, expand `PARAPHRASE_PATTERNS` for occupant behaviour/thermostat/ventilation/lifestyle blame, finite causal verbs, and bill-savings guarantees, and enforce `neutral_text` on staff outcome/remedy/pack-review evidence and `from_state` restores while keeping household statements verbatim (`C6`, `C7`, `C8`, `C9`).
  4. Attach `FR-036` `ai_registry` proposal-only/human-review metadata to `propose_pack` and `AftercareService.evaluator_view`, update `web/aftercare.js` for channel/route/multi-support labels and strict `unknown` non-coercion, and add focused `core` + `api` tests (`C10`, `C11`, `C12`, `C13`).
* Rejected alternatives:
  * Expose unauthenticated `/api/aftercare/household-*` on `server.py`: Rejected because `server.py` is the authenticated staff server enforced by `test_role_endpoint_inventory.py` and `OD-54` (`C14`, `C15`).
  * Retain `sys.modules.pop` in `aftercare_fixture.py`: Rejected by explicit caller constraint and `unittest discover` class-identity safety (`C1`).

## Decisions, Risks, and Further Research

* Current decisions:
  * Preserve household `statement` and `representative_basis` verbatim while enforcing `neutral_text` on all generated, templated, evaluator, pack, and staff-authored outcome/remedy/closure/sensor text.
  * Keep `/api/aftercare/concerns/<id>/{pack,packs,concern-pack}` unexposed (`404`/`405`) while surfacing `FR-036` `aftercare-concern-pack` registry state (`unapproved`, `proposal-pack`, `live_authorized: False`, `requires_human_review: True`).
  * Load `web-design-guidelines` skill before modifying `src/api/src/zava_forward/api/web/aftercare.js`.
* Unresolved decisions / blockers: None for local `#133` engineering. Live resident-portal identity (`OD-54`) and live `aftercare-concern-pack` model activation (`FR-036`) remain gated outside `#133`.
* Validation tier: Focused tier (scoped feature refinement in `src/core` and `src/api` with no workflow, Bicep, Dockerfile, SQL-schema, dependency-manifest, or security-control weakening edits): run `mypy`, `ruff check . && ruff format --check .`, and `unittest` suites in `src/core` and `src/api`.
* Potential further research: None required for `#133`.

## Readiness and Handoff

* Output mode: `convergence` (planning-eligible: yes)
* Research disposition: `executed`
* Planning Readiness: `Ready`
* Artifact self-check:
  * Brief, extensions, participation, direction controls, 3 waves (Wider, Deeper, Contrarian), parent synthesis, `C1`–`C18` `path:line` evidence, convergence selection, rejected alternatives, and readiness recorded: Pass.
  * Zero source files modified during research: Pass.
* Continuation: Active automatic RPI Agent transitions directly to `Plan` (`rpi-plan`).
