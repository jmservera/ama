---
description: "Primary evidence artifact for Issue #133 Criterion 5: deterministic no-causation, no-blame, no-savings-promise enforcement across aftercare generated and templated text"
---
<!-- markdownlint-disable-file -->

# Task Research: 133-no-causation-blame-savings

| Field              | Value                                                                                 |
|--------------------|---------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                            |
| Researcher / agent | rpi-research (RPI Agent automatic loop)                                               |
| Status             | Complete                                                                              |
| Artifact path      | .copilot-tracking/research/2026-11-15/133-no-causation-blame-savings-research.md      |

## Research Brief

* What to research: Every generated, templated, and caller-drafted aftercare text path across `zava_forward.core` and `zava_forward.api` (acknowledgements, receipts, investigation summaries, remedy templates, sensor context notes, evaluator view summaries, UI labels/templates, and optional `FR-036` AI concern-pack proposal drafts/summaries) to determine gaps against Issue #133 Criterion 5 (`No causation, blame or savings promise appears in any generated or templated text`).
* Why it matters: Issue #133 has 4/6 criteria proven; Criterion 5 requires deterministic, boundary-enforced validation ensuring no causation claim (lifestyle attribution or measure causation proof), resident blame language, or financial/energy savings promise can appear in persisted, proposed, or rendered aftercare text.
* Audience or intended use: Planning (`rpi-plan`), critique (`rpi-plan-critique`), implementation (`rpi-implement`), and post-implementation review (`rpi-review`) on branch `feat/ai-133-no-causation-blame-savings`.
* Scope: `src/core/src/zava_forward/core/aftercare*.py`, `src/core/src/zava_forward/core/proposals.py`, `src/api/src/zava_forward/api/**`, `src/agents/**` (if any aftercare concern-pack helper exists), and `src/core/tests/test_aftercare*.py` + `src/api/tests/test_aftercare*.py`.
* Non-goals: Criterion 1 (non-digital accessible intake route acceptance proof beyond neutral-copy enforcement), DPO external sign-off on outcome data, or live Azure deployment.
* Criteria: Deterministic boundary enforcement across all generated/templated/proposal aftercare surfaces without false-positive rejection of neutral resident factual reports (e.g., resident reporting higher bills, damp/mould symptoms, or investigator recording `cannot_determine`).
* Requested outputs: Convergence recommendation with exact file/line inventory of every generated/templated/drafted text path, bypass analysis, and test coverage plan.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                         |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Where is aftercare generated/templated/proposal text produced, validated, persisted, or rendered, and which paths or phrasing forms currently bypass `neutral_text` / boundary enforcement? |
| Codebase scope                   | `src/core/`, `src/api/`, `src/agents/`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`           |
| External scope                   | none                                                                                                          |
| Initial internal candidate areas | `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/src/zava_forward/core/proposals.py`, `src/api/src/zava_forward/api/app.py`, `src/api/src/zava_forward/api/web/aftercare.js`, `src/core/tests/test_aftercare.py`, `src/api/tests/test_aftercare*.py` |
| Initial external candidate areas | none                                                                                                          |
| Research posture                 | focused                                                                                                       |
| Posture provenance               | caller-specified bounded internal scope                                                                       |
| Explicit limits / deadline       | Single session automatic RPI loop ending in local commit without push                                         |
| Posture-specific completion basis| All in-scope generated/templated/proposal aftercare paths, bypass vectors, and false-positive constraints are mapped with `path:line` evidence |
| Edits allowed during research?   | no, research-only                                                                                             |
| Resolved evidence root           | `.copilot-tracking/`                                                                                          |
| Known constraints / excluded sources | Code-only internal research; preserve neutral resident symptom quotes/categories while blocking generated/templated/proposal causation, blame, or savings promises |

## Extension Provenance & Participation

| Extension | Type | Disposition | Rationale & Scoped Contract |
|-----------|------|-------------|-----------------------------|
| Repository instructions (`.github/copilot-instructions.md`) | Instructions | Selected | Governs focused validation tier, no-echo error reporting, plain-language copy rules (`content-standard.md`), and local git commit conventions |
| `rpi-research` | Skill | Selected | Primary active phase protocol for three-wave research synthesis |
| `web-design-guidelines` | Skill | Skipped (no UI layout/markup redesign) | Only backend boundary enforcement and tests are modified unless static JS copy needs adjustment; `aftercare.js` literals already pass `neutral_text` |
| `RPI Researcher` | Subagent | Skipped (inline fallback) | Bounded internal single-subsystem trace across tightly coupled `aftercare*.py`, `quality.py`, `server.py`, `aftercare.js`, and tests; investigated inline |

* Intake checkpoint rationale: Non-interactive automatic RPI session with explicit caller scope, target branch, acceptance criterion, and validation commands; no clarification needed.

## Prior-Knowledge Gate & Decomposed Questions

* `Q1`: Which modules implement aftercare concern intake, receipts/acknowledgements, investigation outcomes, remedies, evaluator views, and `FR-036` concern-pack proposals (accounting for actual repo layout vs shorthand paths)?
* `Q2`: Which generated, templated, caller-drafted, or persisted/restored text surfaces currently bypass `neutral_text`?
* `Q3`: What lexical, normalization, or multi-clause bypasses exist inside `neutral_text` (`BANNED_PHRASES`, `PARAPHRASE_PATTERNS`, `_NEGATED_CLAIM`, `_UNCERTAIN`)?
* `Q4`: How should prohibited caller/generated/template text be handled at each boundary (deterministic rejection vs sanitization) without censoring verbatim resident own-words symptom reports or violating `test_content_standard.py` / `test_epic104_bounded_ai_invariants.py` / `test_role_endpoint_inventory.py`?
* `Q5`: How are `test_aftercare*` suites structured across `src/core` and `src/api` under `mypy_path` and `PYTHONPATH`?

## Cycle 1 Execution

### Wave 1 — Wider (Surface & Contract Inventory)

* Mapped actual repository module paths against caller shorthand:
  * Core domain register and `neutral_text`: `src/core/src/zava_forward/core/aftercare.py:1-489` (`C1`).
  * Staff-assisted intake service and `/api/aftercare/*` contract: `src/core/src/zava_forward/core/aftercare_intake.py:1-850` (`C2`; no separate `src/api/.../aftercare_intake.py`).
  * Proposal task registry (`CONCERN_PACK_TASK = "aftercare-concern-pack"`): `src/core/src/zava_forward/core/ai_registry.py:20,136-143` (`C3`; no `core/proposals.py`). Registered `unapproved` and `disabled` (`FR-036`), guarded by `src/agents/tests/test_epic104_bounded_ai_invariants.py:51-79,201-228` (`C4`).
  * Durable store adapter: `src/core/src/zava_forward/core/aftercare_store.py:1-145` (`C5`).
  * Case handover quality aftercare note path: `src/core/src/zava_forward/core/quality.py:392-402` (`add_aftercare`), wired at `POST /api/cases/{cid}/quality-aftercare` in `src/api/src/zava_forward/api/server.py:327` (`C6`).
  * HTTP server & CSV export: `src/api/src/zava_forward/api/server.py:124-127,196-200,628-643` (`C7`; no `api/app.py`).
  * Staff web screen module: `src/api/src/zava_forward/api/web/aftercare.js:1-664` (`C8`), audited for plain-language copy by `src/api/tests/test_content_standard.py:13-48` (`C9`) and for `neutral_text` literal compliance by `src/api/tests/test_aftercare_screen.py:372-377` (`C10`).
  * PRD requirements: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:309,322,424` (`FR-036`, `FR-049`, `AC-063`: optional AI concern pack stays a proposal requiring human acceptance, never replaces human review, and no causation, blame, or savings promise appears in generated or templated text) (`C11`).

### Wave 2 — Deeper (Boundary & Pattern Gap Analysis)

* **Gap G1 — Unguarded write & proposal-review text fields in `AftercareRegister` (`aftercare.py`)**:
  * `record_outcome` (`src/core/src/zava_forward/core/aftercare.py:324-345`, `C12`) stores `evidence` via `_text(evidence, "Outcome evidence")` without `neutral_text`, allowing investigation outcome summaries to persist resident blame, lifestyle causation, or savings promises.
  * `set_remedy` (`src/core/src/zava_forward/core/aftercare.py:347-357`, `C13`) stores `evidence` without `neutral_text` (and leaves non-`completed` optional `evidence` unstripped/unguarded).
  * `review_pack` (`src/core/src/zava_forward/core/aftercare.py:467-481`, `C14`) stores `reviewer` and `reason` on the `FR-036` concern-pack proposal without `neutral_text`.
  * `_context` (`src/core/src/zava_forward/core/aftercare.py:180-188`, `C15`) validates sensor-context values with `neutral_text`, but not keys; `raise_concern` (`aftercare.py:274`) and `record_closure` (`aftercare.py:370`) do not run `neutral_text` on `owner` / `recorded_by`, even though `owner` is interpolated into templated receipts (`aftercare_intake.py:420`) and templated pack `recorded_facts` (`aftercare.py:438`).
* **Gap G2 — Unguarded service intake, error-mapping, and templated string paths in `AftercareService` (`aftercare_intake.py`) and `quality.py`**:
  * `AftercareService.record_outcome` and `set_remedy` (`src/core/src/zava_forward/core/aftercare_intake.py:648-668`, `C16`) run `_free_text` (length and synthetic PII guard) without `neutral_text`, and `_context_errors` (`aftercare_intake.py:286-308`, `C17`) checks key/value format, length, and PII without checking `neutral_text` to return a structured `errors["context"]` `ValidationError`.
  * `quality.py:add_aftercare` (`src/core/src/zava_forward/core/quality.py:392-402`, `C6`) records staff handover aftercare notes without `controls.is_memory_reference` or `neutral_text`.
  * Several templated strings are emitted without self-checking through `neutral_text` at the boundary: `form["title"]`, `ACCESSIBLE_ROUTE`, `PROTECTION`, `PACK_MANUAL_ROUTE`, `PACK_NOT_REVIEWED`, and `intake_errors()` messages in `aftercare.py:132-170,380,461` (`C18`), plus `SYNTHETIC_NOTICE`, `CLOSURE_NOTE`, `SENSOR_NOTE`, `FIXED_UNKNOWNS`, `WINDOWS`, `owner_note`, `manual_route`, and `_comparison` unknown `reason` in `aftercare_intake.py:61-92,439,465-466,482,535-537,757-766,803-805` (`C19`).
* **Gap G3 — Snapshot / persisted-state restore bypass (`from_state` and `_validate`)**:
  * `AftercareRegister.from_state` (`src/core/src/zava_forward/core/aftercare.py:194-230`, `C20`) restores concerns (`owner`, `accessible_route`, `sensor_context`, `outcome.evidence`, `remedy.evidence`), closures (`recorded_by`), and `FR-036` concern packs (`owner`, `recorded_facts`, `questions_for_investigator`, `ai_summary`, `notice`, `manual_route`, `review.reason`, and absence of `sensor_context`) without running `neutral_text`.
  * `AftercareService._validate` (`src/core/src/zava_forward/core/aftercare_intake.py:211-263`, `C21`) restores persisted `receipts` (`what_happens_next`, `protection`, `accessible_route`, `synthetic_notice`) without running `neutral_text`.
* **Gap G4 — Lexical gaps in `BANNED_PHRASES` and `PARAPHRASE_PATTERNS` (`aftercare.py:49-91`)**:
  * Missing deterministic coverage for common housing-retrofit lifestyle blame/causation phrases (e.g., drying clothes/laundry indoors, keeping/leaving windows shut or failing to ventilate/heat, occupant/resident lifestyle or heating habits, improper/incorrect use, user/operator error, negligence, blamed on, fault of the resident/household/tenant), measure-causation proof claims (e.g., `proven to cause`, `proves that`, `proves the`, `attributable to`, `caused the damp/mould/cold/higher`, `is why your`), and financial/energy savings promises (e.g., currency/percent savings `save £200` / `save 20%`, `saves money`, `saving money`, `payback`, `pay(s) for itself`, `cut/slash/reduce (your )?(energy )?(bills|costs)`, `promised savings`, `energy/bill/cost/financial savings`, `cheaper bills`, `cheaper to run`) (`C1`).

### Wave 3 — Contrarian (Bypass & Regression Challenge)

* **Contrarian Finding CF1 — Multi-clause `_UNCERTAIN` whitewash bug (`aftercare.py:119-120`)**:
  * In `neutral_text` (`src/core/src/zava_forward/core/aftercare.py:113-124`, `C22`), `if _UNCERTAIN.search(cleaned): return text` short-circuits the entire input string whenever *any* clause contains an uncertainty marker (such as `"is unknown"` or `"does not show"`). Consequently, `"Overnight flow is unknown. However, the damp is down to the tenant and bills will drop by 20%."` bypasses every regex in `PARAPHRASE_PATTERNS`!
  * Resolution: Split normalized text into clauses/sentences (on `.`, `!`, `?`, `;`, `\n`, and coordinating conjunction boundaries like `\b(?:but|however|therefore|so|and yet|yet)\b`) and scope `_UNCERTAIN` qualification strictly to the clause under evaluation, while `BANNED_PHRASES` and unnegated `PARAPHRASE_PATTERNS` still fail any non-uncertain clause (and explicit blame/lifestyle/savings-promise patterns are never excused even inside an uncertain clause unless directly negated by `_NEGATED_CLAIM`).
* **Contrarian Finding CF2 — Unicode & whitespace normalization bypass (`aftercare.py:113-118`)**:
  * `neutral_text` currently checks `text.lower()` without stripping zero-width/invisible characters (`\u200b-\u200f\u2060\ufeff\u00ad`), applying `unicodedata.normalize("NFKC", ...)`, normalizing curly apostrophes (`\u2018`/`\u2019` -> `'`), or collapsing runs of whitespace (`\s+` -> `" "`). Thus `"will  save"`, `"caused\nby"`, `"resident\u2019s fault"`, and `"will\u200bsave"` bypass `BANNED_PHRASES` and regex checks (`C22`). Normalizing before matching while returning the original `text` unchanged closes all encoding/whitespace bypasses deterministically.
* **Contrarian Finding CF3 — Preserving verbatim resident own-words reports vs system/staff/AI text**:
  * Resident `statement` and `representative_basis` are verbatim household reports (`aftercare_intake.py:251`, `test_aftercare_intake.py:134`, `C23`). A resident must never have their concern refused because they report `"The installer said this would cut my bills and now the wall is damp"`. By contrast, all templated copy, receipts/acknowledgements, sensor-context keys/notes, staff investigation `outcome.evidence`, staff `remedy.evidence`, `quality.py:add_aftercare` notes, evaluator summaries, and `FR-036` concern-pack templates, `ai_summary` drafts (plus optional sanitizer helper `sanitize_draft_text` / boundary rejection), and `review.reason` notes are system-, staff-, or AI-authored text and must strictly pass `neutral_text`.
* **Contrarian Finding CF4 — Copy audit, endpoint inventory, and test module collision**:
  * `src/api/tests/test_content_standard.py:13` (`C9`) forbids `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, and `envelope(s)` in visible web copy; plain-language validation messages must avoid these words and never echo rejected input.
  * `src/api/tests/test_role_endpoint_inventory.py:72-77` (`C24`) enforces exact coverage of every `/api/*` server route, and `ai_registry.py:140` (`C3`) requires `aftercare-concern-pack` to remain disabled with no bound model route. Adding service-level `propose_pack` / `review_pack` helpers on `AftercareService` (alongside `AftercareRegister`) without adding unapproved live model HTTP routes preserves both invariants.
  * `src/api/pyproject.toml:56` (`C25`) sets `mypy_path = ["src", "tests", "../core/src", "../core/tests"]`, and `src/api` runs unittest with `PYTHONPATH=../core/tests:../agents/tests`. Creating a duplicate filename `src/api/tests/test_aftercare_intake.py` would collide with `src/core/tests/test_aftercare_intake.py`! Therefore, intake service/route tests belong in `src/core/tests/test_aftercare_intake.py` and HTTP served API/UI tests belong in `src/api/tests/test_aftercare_served.py` and `src/api/tests/test_aftercare_screen.py` (all matched by `test_aftercare*` in `src/core` and `src/api`).

## Evidence Log

| ID | Location | Summary |
|----|----------|---------|
| `C1` | `src/core/src/zava_forward/core/aftercare.py:49-125` | `BANNED_PHRASES`, `PARAPHRASE_PATTERNS`, `_UNCERTAIN`, `_NEGATED_CLAIM`, and `neutral_text` implementation |
| `C2` | `src/core/src/zava_forward/core/aftercare_intake.py:1-850` | `AftercareService` wrapping `AftercareRegister` and serving `/api/aftercare/*` |
| `C3` | `src/core/src/zava_forward/core/ai_registry.py:20,136-143` | `CONCERN_PACK_TASK = "aftercare-concern-pack"` registered unapproved and disabled (`FR-036`) |
| `C4` | `src/agents/tests/test_epic104_bounded_ai_invariants.py:51-79,201-228` | Cross-capability invariant suite verifying `aftercare-concern-pack` remains disabled and owner-gated |
| `C5` | `src/core/src/zava_forward/core/aftercare_store.py:1-145` | `DocumentStateStore` atomic persistence over `Store` / `SqlStore` |
| `C6` | `src/core/src/zava_forward/core/quality.py:392-402` | `add_aftercare` handover note path wired to `/api/cases/{cid}/quality-aftercare` |
| `C7` | `src/api/src/zava_forward/api/server.py:124-127,196-200,327,628-643` | `App.aftercare` composition, `concern_export_row`, and HTTP route delegation |
| `C8` | `src/api/src/zava_forward/api/web/aftercare.js:1-664` | Client-side aftercare workspace templates and labels |
| `C9` | `src/api/tests/test_content_standard.py:13-48` | Lexical guard banning internal terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) in web copy |
| `C10` | `src/api/tests/test_aftercare_screen.py:372-377` | Screen test verifying every literal string in `aftercare.js` passes `aftercare.neutral_text` |
| `C11` | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:309,322,424` | `FR-036`, `FR-049`, and `AC-063` product requirements |
| `C12` | `src/core/src/zava_forward/core/aftercare.py:324-345` | `AftercareRegister.record_outcome` stores `evidence` without `neutral_text` |
| `C13` | `src/core/src/zava_forward/core/aftercare.py:347-357` | `AftercareRegister.set_remedy` stores `evidence` without `neutral_text` |
| `C14` | `src/core/src/zava_forward/core/aftercare.py:467-481` | `AftercareRegister.review_pack` stores `reviewer` and `reason` without `neutral_text` |
| `C15` | `src/core/src/zava_forward/core/aftercare.py:180-188,274,370` | `_context` omits key check; `owner` and `recorded_by` bypass `neutral_text` |
| `C16` | `src/core/src/zava_forward/core/aftercare_intake.py:648-668` | `AftercareService.record_outcome` and `set_remedy` omit `neutral_text` validation |
| `C17` | `src/core/src/zava_forward/core/aftercare_intake.py:286-308,695-702` | `_context_errors` omits `neutral_text`, causing raw `ValueError` instead of field `ValidationError({"context": ...})` |
| `C18` | `src/core/src/zava_forward/core/aftercare.py:132-170,380,461` | Templated form metadata, `intake_errors()`, `PROTECTION`, and `PACK_MANUAL_ROUTE` not all wrapped in `neutral_text` |
| `C19` | `src/core/src/zava_forward/core/aftercare_intake.py:61-92,439,465-466,482,535-537,757-766,803-805` | Service templated strings (`SYNTHETIC_NOTICE`, `CLOSURE_NOTE`, `SENSOR_NOTE`, `owner_note`, `manual_route`, `FIXED_UNKNOWNS`, `WINDOWS`, `_comparison` unknown `reason`) not all wrapped in `neutral_text` |
| `C20` | `src/core/src/zava_forward/core/aftercare.py:194-230` | `AftercareRegister.from_state` omits `neutral_text` checks on restored concerns, closures, and packs |
| `C21` | `src/core/src/zava_forward/core/aftercare_intake.py:211-263` | `AftercareService._validate` omits `neutral_text` checks on restored receipts |
| `C22` | `src/core/src/zava_forward/core/aftercare.py:113-124` | `neutral_text` lacks NFKC/invisible/apostrophe/whitespace normalization and short-circuits whole strings on a single `_UNCERTAIN` match |
| `C23` | `src/core/tests/test_aftercare_intake.py:134-145` | Resident `statement` and `representative_basis` are verbatim household records |
| `C24` | `src/api/tests/test_role_endpoint_inventory.py:27,52,72-77` | Route inventory enforces exact server `/api/*` endpoint registration |
| `C25` | `src/api/pyproject.toml:55-60` | `mypy_path` shares `tests` and `../core/tests`, prohibiting duplicate test module names across `src/core/tests` and `src/api/tests` |

## Synthesis, Alternatives & Selected Recommendation

### Alternatives Considered

1. **Selected Recommendation — Hardened deterministic `neutral_text` + universal boundary rejection across write, proposal, restore, and render surfaces (with verbatim resident input preserved)**:
   * Normalize text inside `neutral_text` (`NFKC`, strip zero-width/soft-hyphen chars, normalize curly quotes/apostrophes, collapse whitespace) while returning the original string when valid.
   * Fix the multi-clause `_UNCERTAIN` bypass so uncertainty markers qualify only their own clause and never excuse explicit lifestyle blame, causation claims, or financial/energy savings promises.
   * Expand `BANNED_PHRASES` and `PARAPHRASE_PATTERNS` to cover resident lifestyle attribution (drying laundry/clothes indoors, closed windows / ventilation failure, heating habits, occupant lifestyle, misuse/user error/negligence), measure-causation proof claims (`proven to cause`, `proves that/the`, `attributable to`, `caused the damp/mould/cold/higher`, `is why your`), and financial/energy savings promises (`save £/$`, `save N%`, `saves/saving money`, `payback`, `pay(s) for itself`, `cut/slash/reduce bills/costs`, `energy/bill/cost/financial savings`, `cheaper bills / cheaper to run`).
   * Enforce `neutral_text` at every boundary:
     * `AftercareRegister`: `intake_form`, `intake_errors`, `raise_concern` (`owner`, `accessible_route`, `sensor_context` keys & values), `add_sensor_context` (keys & values), `record_outcome` (`evidence`), `set_remedy` (`evidence`), `record_closure` (`recorded_by`), `view` (`protection`), `evaluator_view` (`notice`), `propose_pack` (`recorded_facts`, `questions_for_investigator`, `ai_summary`, `notice`, `manual_route`, `approval`), `review_pack` (`reviewer`, `reason`), and `from_state` (all restored concerns, closures, and packs).
     * `AftercareService`: `form`, `_receipt`, `_display`, `concerns`, `record_outcome` (`ValidationError({"evidence": ...})`), `set_remedy` (`ValidationError({"evidence": ...})`), `_context_errors` / `add_sensor_context` (`ValidationError({"context": ...})`), `propose_pack` and `review_pack` service methods (bounded, owner-gated, `ValidationError` on prohibited `ai_summary` / `reason` without adding live model calls or unapproved HTTP endpoints), `evaluator_view` / `_comparison`, and `_validate` (all restored receipts and register state).
     * `quality.py:add_aftercare`: guard `note` with `controls.is_memory_reference` and `aftercare.neutral_text` so `/api/cases/{cid}/quality-aftercare` also rejects causation, blame, and savings promises with HTTP 400.
   * Why selected: Deterministic fail-closed rejection before persistence, proposal registration, restore, or rendering guarantees zero prohibited phrasing can enter or leave the system, avoids inventing unverified rewritten claims on compliance records, preserves existing `ValueError`/`ValidationError` contracts (`test_aftercare.py`, `test_epic104_bounded_ai_invariants.py`), and leaves verbatim household `statement` / `representative_basis` untouched.
2. **Rejected Alternative A — Silent regex rewriting/redaction of staff outcome evidence and AI drafts into canned text**:
   * Why rejected: Silently mutating staff investigation evidence (`outcome.evidence`, `remedy.evidence`) or reviewer reasons corrupts audit fidelity and conflicts with existing unit/agent tests (`test_aftercare.py:430`, `test_epic104_bounded_ai_invariants.py:219`) that require `ValueError` refusal when `propose_pack` or `add_sensor_context` receives prohibited phrasing. Fail-closed boundary rejection (`ValueError` / `ValidationError` with plain-language guidance and zero echo) forces neutral observational wording before persistence or registration.
3. **Rejected Alternative B — Applying `neutral_text` to resident `statement` / `representative_basis`**:
   * Why rejected: Violates `FR-049` / Criterion 3 spirit and verbatim intake requirements (`aftercare_intake.py:251`, `test_aftercare_intake.py:134`) by refusing residents who describe what they were promised or what they believe went wrong in their own words. Criterion 5 explicitly scopes the prohibition to *generated or templated text* (and staff/AI summaries, templates, notes, and drafts).

## Decisions, Risks & Readiness

* **Current Decisions**:
  * Preserve verbatim resident `statement` and `representative_basis`; enforce `neutral_text` across all templated outputs, receipts, acknowledgements, sensor context keys/values, investigation outcome summaries, remedy notes/templates, quality aftercare notes, evaluator views, snapshot restores, and `FR-036` concern-pack drafts and review reasons.
  * Place unit tests in `src/core/tests/test_aftercare.py`, `AftercareService` intake/route/pack boundary tests in `src/core/tests/test_aftercare_intake.py`, and full HTTP served `/api/aftercare/*` + `/api/cases/{cid}/quality-aftercare` boundary tests in `src/api/tests/test_aftercare_served.py` (with JS template checks in `src/api/tests/test_aftercare_screen.py`), avoiding `mypy_path` / `PYTHONPATH` duplicate-module collisions.
  * Validation tier: **Focused tier** (pure Python core/API validation & unit/served tests; no infrastructure, SQL schema, workflow, Dockerfile, or dependency-manifest changes).
* **Open Risks / Non-Goals**:
  * Criterion 1 of Issue #133 (human/operational accessible non-digital route acceptance beyond software representation) and DPO position on outcome data remain separate Issue #133 items outside Criterion 5.
* **Cycle Re-entry Evaluation**: Single three-wave cycle saturated all codebase references (`48` files matched across `src/`); zero unresolved in-scope uncertainties remain.
* **Research Disposition**: `executed`
* **Planning Readiness**: `Ready`

