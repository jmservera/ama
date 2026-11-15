---
description: "Primary evidence artifact for Issue #134 profile journey contract and connected same-home journey acceptance slice"
---
<!-- markdownlint-disable-file -->

# Task Research: issue-134-same-home-walk-0018

| Field              | Value                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                              |
| Researcher / agent | RPI Agent (`rpi-research`)                                                              |
| Status             | Complete                                                                                |
| Research disposition | executed                                                                              |
| Planning Readiness | Ready                                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-134-same-home-walk-0018-research.md        |

## Research Brief

* What to research: Existing same-home walk and profile journey contract coverage across `src/core`, `src/api/src/zava_forward/api/static/role-screens.js`, `src/api/checks/role_screens_browser_check.py`, `src/api/tests/`, `src/core/tests/`, and `docs/reference/research/ux/profile-journey-contract.md`, plus remaining code-testable gaps for the six staff profiles and resident portal (handover dependencies, shared facts, role-appropriate redaction of vulnerability reasons on contractor views, and plain-language next-action continuity across same-home transitions).
* Why it matters: Delivers a stacked child slice (`Refs #134`) on `feat/ux-134-same-home-walk-0018` targeting `feat/demo-233-same-home-tensions-0825` (`#1639`) that verifies and completes code-testable profile journey contract and connected same-home walkthrough invariants while preserving human/resident approval and live accessibility sign-off boundaries.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`, and coordinator review for Issue #134.
* Scope: `src/core/`, `src/api/` (including `role-screens.js`, resident portal/API surfaces, `role_screens_browser_check.py`, `scenario-manifest.json`, and unit tests), and `docs/reference/research/ux/profile-journey-contract.md` plus directly coupled UX/contract docs if needed.
* Non-goals: Claiming live human approval, direct user validation (`#155`, OQ-004/005/011), assistive-technology sign-off, closing `#134` prematurely (`Refs #134` only), or pushing to remote.
* Criteria: Every codebase claim cites `path:line` (`C#`), covers all four acceptance items in the caller brief, checks recipe SHA / manifest coupling if `role_screens_browser_check.py` changes, and respects Fluent 2 / WCAG 2.2 / plain-language / human-boundary rules.
* Requested outputs: Convergence recommendation with exact gap analysis, target files, invariants, and test plan for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                                  |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q5 covering existing contract helpers, six staff profiles + resident portal same-home continuity, contractor vulnerability redaction, handover invariants, and tests |
| Codebase scope                       | `src/core/`, `src/api/`, `docs/reference/research/ux/`, `docs/prds/`, `.copilot-tracking/`                                                                             |
| External scope                       | `web-design-guidelines` canonical source URL if `role-screens.js` or web UI files require edits                                                                        |
| Initial internal candidate areas     | `docs/reference/research/ux/profile-journey-contract.md`, `src/core/src/zava_forward/`, `src/api/src/zava_forward/api/static/role-screens.js`, `src/api/checks/role_screens_browser_check.py` |
| Initial external candidate areas     | Vercel web-interface-guidelines source referenced by `.agents/skills/web-design-guidelines/SKILL.md` (when web UI edits are needed)                                    |
| Research posture                     | focused                                                                                                                                                                |
| Posture provenance                   | caller-specified bounded slice with named files, acceptance criteria, and focused validation tier                                                                      |
| Explicit limits / deadline           | Focused validation tier; stacked branch `feat/ux-134-same-home-walk-0018` targeting `feat/demo-233-same-home-tensions-0825`; no push                                   |
| Posture-specific completion basis    | focused scope and materiality: all named files, six staff profiles + resident portal invariants, redaction, continuity, and manifest couplings verified                |
| Edits allowed during research?       | no, research-only                                                                                                                                                      |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                                                   |
| Known constraints / excluded sources | Never read private datasets; preserve human/resident approval and live AT sign-off boundaries; use `Refs #134`                                                         |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                            | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|---------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` repository instructions                         | Enforces AMA governance, branch/commit rules, UX/accessibility, validation tiers | Selected: governs all repository changes and evidence boundaries                          |
| Skill               | `redesign-existing-projects`          | Existing web UI (`role-screens.js`) UX/contract alignment       | Preserves Fluent 2, WCAG 2.2 AA, plain language, and existing functionality      | Deferred to Plan/Implement if `role-screens.js` edits are needed; read-only in Research   |
| Skill               | `web-design-guidelines`               | Required by repo Web Development Guidance before web edits      | Web UI audit rules with `file:line` reporting                                    | Deferred to Implement/Review if web files are edited                                      |
| Skill               | `accessibility`                       | Accessibility / textual state / keyboard / status announcements | WCAG 2.2 AA and ARIA authoring practices                                         | Deferred if UI/DOM semantics change; UX docs inspected directly in Research               |
| Research specialist | `hve-core-all:rpi-researcher`         | General bounded research lane worker                            | Subagent lane markdown under `.copilot-tracking/research/subagents/`             | Skipped: tightly coupled bounded slice across 4 named areas is faster and cleaner inline  |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                          |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI execution with complete caller brief, target branch, scope, acceptance criteria, and validation tier | N/A (autonomous)     | Proceed directly with focused three-wave inline research on `issue-134-same-home-walk-0018` |
| Direction change | None at intake                                                                                                         | N/A                  | Maintain caller-defined 5-point scope                                                    |
| Convergence      | Completed Cycle 1 (Wider, Deeper, Contrarian) with full codebase evidence (`C1`-`C22`) | N/A (autonomous)     | Select Option B: extend `profile_journey_contract.py` + `role-screens.js` same-home next-action line + author `docs/reference/research/ux/profile-journey-contract.md` + add focused `src/core` and `src/api` acceptance tests |

## Scope and Success Criteria

* Scope: Inspect `src/core`, `src/api/src/zava_forward/api/static/role-screens.js`, `src/api/checks/role_screens_browser_check.py`, resident portal / staff API models and routes, `docs/reference/research/ux/profile-journey-contract.md`, and related tests in `src/core/tests/` and `src/api/tests/`.
* Assumptions:
  * Earlier slices on `feat/demo-233-same-home-tensions-0825` (including `2026-11-14-134-profile-contract-1114` and `2026-11-14-issue-233-same-home-walk-1248`) may have partially implemented helpers or UI walk links; actual current branch state must be verified from source.
  * `scenario-manifest.json` pins SHA-256 hashes of verification recipes such as `role_screens_browser_check.py`.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one convergence recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Inspect existing same-home walk and profile journey contract coverage in `src/core`, `role-screens.js`, `role_screens_browser_check.py`, and `docs/reference/research/ux/profile-journey-contract.md`.
  2. Verify and complete remaining code-testable profile journey contract and connected same-home walkthrough invariants across the six staff profiles and resident portal (handover dependencies, shared facts, role-appropriate redaction of vulnerability reasons on contractor views, plain-language next-action continuity across same-home transitions).
  3. Identify focused unit tests to add/strengthen in `src/api/tests/` and `src/core/tests/`.
  4. Keep human/resident approval and live accessibility walkthrough sign-off boundaries explicit.
* Inferred research questions: How are the six staff profiles and resident portal represented in `src/core` and `src/api`? Where are vulnerability reasons exposed or redacted on contractor views? How is same-home transition / next-action continuity modeled and rendered across staff and resident views? What does `scenario-manifest.json` check?
* Caller constraints and non-goals: Focused validation tier; no push; `Refs #134`; do not fabricate human/resident approval or live AT sign-off.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Focused slice on code-testable profile journey contract and connected same-home walkthrough invariants  | Caller intake       | Constrains scope to code-testable invariants + explicit approval/AT boundaries     |
| exclude                                                  | Do not push to remote; do not claim `Closes #134` or live user/AT sign-off                              | Caller intake       | Restricts closeout to local frozen commit and `Refs #134`                          |

## Research Questions

|  # | Sub-question                                                                                                                                   | Type            | Priority | Status   |
|---:|------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What does `docs/reference/research/ux/profile-journey-contract.md` require across perspectives, six staff profiles, resident portal, and ACs?  | depth           | H        | answered |
| Q2 | What profile journey contract and same-home walk helpers/models already exist in `src/core` and `src/core/tests/` on this branch?              | depth           | H        | answered |
| Q3 | How do `src/api` routes, resident portal endpoints, `role-screens.js`, and `role_screens_browser_check.py` implement same-home walk, shared facts, handover dependencies, contractor vulnerability-reason redaction, and plain-language next-action continuity? | depth | H | answered |
| Q4 | What gaps, inconsistencies, or unverified invariants remain across the six staff profiles and resident portal?                                 | breadth         | H        | answered |
| Q5 | What manifest/hash couplings (`scenario-manifest.json`, `test_scenario_manifest.py`, `test_needs_inventory.py`) and boundary guards constrain changes? | straightforward | M        | answered |

## Cycle 1 Execution: Wider, Deeper, Contrarian

### Wave 1: Wider (Breadth Discovery)

* **UX reference inventory (`C1`, `C2`, `C3`)**: `docs/reference/research/ux/profile-journey-contract.md` does not yet exist in the repository (`docs/reference/research/ux/` holds 12 sibling UX docs). Currently, the profile journey contract lives only as a section inside `docs/prds/zava-forward-retrofit-programme-demonstrator.md:2815-2875` (`## Profile Journey Contract for the Next Prototype`, governing `AC-034` through `AC-043`, `FR-041` through `FR-054`, and `NFR-015` through `NFR-018`). Notice also that the web asset path in `src/api` is `src/api/src/zava_forward/api/web/role-screens.js` (served at `/static/role-screens.js`, `C13`), not `api/static/role-screens.js`.
* **Core journey modules (`C4`-`C11`)**: `src/core/src/zava_forward/core/` already separates:
  * `profile_journey_contract.py` (`C4`): five-element single-perspective contract schema (`ELEMENTS`: `entry_trigger`, `needed_context`, `decision_or_action`, `withheld_fields`, `handover_output`), `validate(walkthrough)`, and `gaps(root, reg)`.
  * `perspective_walkthroughs.py` (`C5`) and `journey_acceptance.py` (`C6`): explicit deferral/partial registers for the 10 perspectives (`AC-034` to `AC-043`), keeping `elements_met == 0` and `passed == []` until real user/accessibility review occurs.
  * `journey_trace.py` (`C7`) and `home_case.py` (`C8`): single-home audit trace (`epc_conflict` -> `correction` -> `independent_decisions` -> `handover` -> `financial_closure`, `order_findings`, `user_validation="not-established"`) and canonical home-case aggregator.
  * `projection.py` (`C9`), `job_pack.py` (`C10`), `taskqueues.py` (`C11`), and `quality.py` (`C12`): role-scoped projections across the six primary staff profiles (`Retrofit Programme Manager`, `Retrofit Coordinator`, `Resident Liaison Officer`, `Building Safety Liaison`, `Quality Inspector`, `Grants and Evidence Officer`), `Programme Support Officer`, and `Contractor`, plus deterministic task-context (`work`) and handover blockers (`quality.handover_blockers`).
* **Resident portal surfaces (`C14`, `C15`)**: `src/api/src/zava_forward/api/resident_preview/app.py` and `src/core/src/zava_forward/core/resident_summary.py` project resident-safe single-home views (`case_id`, `address`, `postcode`, `stage`, `measures`, `closed`, plain-language `next_step` from `STAGE_TEXT`, `timeline`, `appointments`, `documents`, `approval_boundary`, non-consent read-only notices) with zero internal staff notes, contacts, hazards, finance, or vulnerability labels.

### Wave 2: Deeper (Exact Invariant & Traceability Inspection)

* **Six staff profiles + contractor + resident portal projection rules (`C9`, `C10`, `C11`, `C14`, `C15`)**:
  * `projection.REASON_ROLES` (`C9`) grants raw `resident.adjustment` visibility only to `Resident Liaison Officer`, `Building Safety Liaison`, and `Retrofit Programme Manager`. For the remaining three primary staff profiles (`Retrofit Coordinator`, `Quality Inspector`, `Grants and Evidence Officer`) and `Programme Support Officer`, `projection.staff_detail` replaces `resident.adjustment` with `projection.REDACTED` (`"Extra support noted"`), replaces contact/appointment notes with `projection.NOTE_HELD`, and redacts `"Safeguarding"` categories/clocks to `"Safety review"` / `"Safety clock"`.
  * `projection.contractor_summary` and `projection.contractor_detail` (`C9`) strip `resident`, `contacts`, `hazards`, `safety_clocks`, `funding`, `finance`, `grants`, `documents`, and `work`, exposing only `id`, `address`, `town`, `postcode`, `measures`, `named_contact`, and boolean `needs_notice` (`bool(resident.priority_support or resident.adjustment)`). `job_pack.CaseJobPackMixin.job_pack` (`C10`) projects `ACCESS_NOTICE` (`"Notice needed before the visit"`) or `ACCESS_CLEAR` (`"No extra notice recorded"`) and never includes `resident.adjustment` or `projection.REDACTED`.
  * `taskqueues.case_work_context` (`C11`) computes deterministic `work.owner`, `work.reason`, `work.next_action`, `work.blockers`, and `work.handoff` across every staff profile. Unaccepted handoffs (`Offered`, `Received`, `Escalated`) keep `confirmed_receiver = None` and `chase_owner = from_name`; accepted handoffs (`Accepted`, `Completed`) set `confirmed_receiver = to_name` and `chase_owner = accountable_owner`. None of the generated `next_action` or `correction` strings in `gates.py` or `taskqueues.py` use banned internal vocabulary (`C16`).
* **Web specialist screens (`C13`, `C17`, `C18`)**:
  * `role-screens.js` (`C13`) registers 13 specialist screens, enforces `c.id !== caseId` mismatch withholding, renders `Same home: case ${c.id}`, renders `journeyStageMap(c, screen.id)` across all 8 journey stages while preserving `case=${c.id}` links, and renders `contractor-job-pack` with `Needs notice`, `"The reason for any notice is not shared with contractors."`, `Submission and review are separate`, and `Not shown for this role` (`screenWithheld`).
  * Gap found in `role-screens.js` (`C13`, lines 145-153): while sidebar queue rows render `row.work && workSummary(row.work)`, `section.screen-evidence` (`Selected home ${c.id}`) does not display `c.work.owner` and `c.work.next_action` when a staff profile navigates directly between specialist screens for `case=${c.id}` (for example when `c.id` is not on queue page 0). Adding a plain `<p data-same-home-next-action="${c.id}">` inside `section.screen-evidence` when `c.work?.next_action` is present makes plain-language next-action continuity visible across every staff same-home screen transition without leaking `c.work` onto contractor views.
* **Core contract gap (`C4`)**: `profile_journey_contract.py` currently checks only static 5-field dictionary presence (`validate`) and unrecorded perspective gaps (`gaps`). It lacks executable connected same-home walkthrough validators checking:
  1. Shared home facts (`id`, `address`, `postcode`, `stage`, normalized `measures`, `closed`) and sibling-home isolation across all 6 staff profiles, contractor surfaces, and resident portal.
  2. Role-appropriate vulnerability-reason redaction across reason-visibility staff roles, redacted staff roles, contractor views (`contractor_summary`, `contractor_detail`, `work_orders`, `job_pack`), and resident portal views.
  3. Handover dependencies and non-equivalence (unreleased hazard stop, unresolved stock conflict, missing/stale resident scope acceptance, missing checklist evidence, self-acceptance, open defect, work-order `Completed` / job-pack `Acknowledged` non-equivalence to quality `Accepted` / `Handed over`, audit-trace causal order, and `user_validation == "not-established"`).
  4. Plain-language next-action continuity across staff transitions, unaccepted-vs-accepted handoff chase ownership, and resident portal `STAGE_TEXT` alignment without banned internal jargon (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).

### Wave 3: Contrarian (Counter-Evidence, Guardrails & Regression Risks)

* **Contrarian check 1 — Existing deferral tests (`C5`, `C6`, `C19`)**: Could marking walkthrough elements `"met"` or acceptance criteria `"pass"` satisfy `#134`? **Rejected**: `test_perspective_walkthroughs.py` asserts `elements_met == 0` and `test_journey_acceptance.py` asserts `passed == []` because `AC-034` to `AC-043` require real user/accessibility walkthroughs (`#155`, OQ-004/005/011). Code-testable connected same-home invariants must verify software behavior while explicitly reporting `human_signoff = "not-established"`, `resident_approval = "not-established"`, and `accessibility_walkthrough = "not-established"`.
* **Contrarian check 2 — UX doc guardrails (`C20`, `C21`)**: Creating `docs/reference/research/ux/profile-journey-contract.md` automatically enrols it into `test_epic149_ux_journey_requirement_traceability.py` (`C20`) and `test_live_doc_links.py` (`C21`). Specifically:
  * Every `.md` file in `docs/reference/research/ux/` must cite valid `REQ_ID` tokens (`FR-*`, `NFR-*`, `AC-*`, `SA-*`, `OD-*`) that exist verbatim in `SPEC_FILES` (`PRD`, `BRD`, `SRS`) and contain `"journey"`.
  * Every `test_[a-z0-9_]+\.py` filename mentioned in `docs/reference/research/ux/*.md` is dynamically imported and inspected by `ControlClaimsMapToTests` (`C20`): it must exist, define `test*` methods, and contain zero `@unittest.skip` decorators or `__test__ = False`.
  * Forbidden conformance phrases (`conforms to wcag`, `users validated`, `design accepted`, `conformance achieved`) fail `AcceptanceBoundary`.
  * AMA Knowledge Base rules require indexing the new file in `docs/reference/README.md` and appending an entry to `docs/reference/log.md`.
* **Contrarian check 3 — Web & browser check guardrails (`C16`, `C17`, `C18`, `C22`)**:
  * `test_content_standard.py` (`C16`) scans every line of `role-screens.js` (including comments!) for `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b`. Any edit to `role-screens.js` must avoid all six word families even in JS comments.
  * `test_role_screens_conformance.py` (`C17`) enforces CSS class registration in `style.css`, native interactive controls only, zero inline styles, and exact `setTimeout` count; `test_role_screens_connected_journey.py` (`C18`) pins `journeyStageMap(` call count to 3 and checks `.screen-record` panel titles; `connected_home_browser_check.py` (`C18`) inspects `.screen-evidence .screen-record` panels, `:scope > h2`, `a[href]`, and `text_markers`. A plain `<p data-same-home-next-action="${c.id}">` with no CSS class, no `.screen-record`, no heading, no link, and no `tabindex` preserves every existing assertion while surfacing `Current owner` and `Next action` across all staff specialist screens.
  * `scenario_manifest.py` (`C22`) hashes `workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, and `test_workbench.py` (not `role_screens_browser_check.py`). Because `role_screens_browser_check.py` already covers read-only accessibility, keyboard reachability, non-colour status, and `contractor-job-pack` (`226a`), no changes to `role_screens_browser_check.py` or `scenario-manifest.json` are needed, though `test_scenario_manifest.py` and `test_needs_inventory.py` will still be run to verify clean manifest state.

## Answers to Research Questions

* **Q1 (`C1`, `C2`, `C20`, `C21`)**: `docs/reference/research/ux/profile-journey-contract.md` is currently missing and must be created as the canonical UX reference extracted and expanded from `PRD` `## Profile Journey Contract for the Next Prototype` (`AC-034` to `AC-043`, `FR-041` to `FR-054`, `NFR-015` to `NFR-018`), documenting the five-element contract per perspective, the connected same-home invariants across the six staff profiles, contractor view, and resident portal, code-verified test mappings, and explicit human/resident/AT non-equivalence boundaries.
* **Q2 (`C4`-`C12`, `C19`)**: `src/core` already provides `profile_journey_contract.py` (`ELEMENTS`, `validate`, `gaps`), `perspective_walkthroughs.py`, `journey_acceptance.py`, `journey_trace.py`, `home_case.py`, `projection.py`, `job_pack.py`, `taskqueues.py`, and `quality.py`, but `profile_journey_contract.py` lacks executable connected same-home multi-role invariant validators (`SIX_STAFF_PROFILES`, shared facts, vulnerability redaction, handover dependencies, plain-language next-action continuity, and live `Store` bundle assembly).
* **Q3 (`C9`, `C10`, `C13`, `C14`, `C15`, `C18`)**: Staff API routes (`/api/cases/{id}`), contractor routes (`/api/cases/{id}`, `/api/workorders`), `job_pack`, and `resident_preview` (`/api/preview/cases/{id}`) enforce server-side role projection and vulnerability redaction, and `role-screens.js` renders `Same home: case ${c.id}`, `journeyStageMap`, and `contractor-job-pack` (`Needs notice` without reason). Adding `<p data-same-home-next-action="${c.id}">` in `role-screens.js` completes selected-home next-action continuity across all staff specialist screen transitions.
* **Q4 (`C4`, `C13`, `C19`)**: Four concrete deliverables close all code-testable gaps for this slice: (1) extend `profile_journey_contract.py` with pure, typed connected same-home validators and `Store` multi-profile walk evaluation; (2) surface `Current owner` + plain-language `Next action` on `section.screen-evidence` in `role-screens.js` for staff views; (3) create `docs/reference/research/ux/profile-journey-contract.md` (indexed in `docs/reference/README.md` and logged in `docs/reference/log.md`); and (4) add comprehensive unit and full-stack HTTP + Node screen tests in `src/core/tests/test_profile_journey_contract.py` and `src/api/tests/test_same_home_profile_journey_acceptance.py`.
* **Q5 (`C16`, `C17`, `C20`, `C21`, `C22`)**: `scenario-manifest.json` is untouched because `role_screens_browser_check.py` requires no edits; `test_scenario_manifest.py`, `test_needs_inventory.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_live_doc_links.py`, `test_content_standard.py`, and `test_role_screens_conformance.py` guard all couplings and must run in validation.

## Options and Convergence Recommendation

| Option | Summary | Pros | Cons | Verdict |
|---|---|---|---|---|
| Option A | Docs + tests only (create `profile-journey-contract.md` and tests without extending `profile_journey_contract.py` or `role-screens.js`) | Minimal code diff | Leaves connected same-home contract rules scattered across tests rather than reusable in `zava_forward.core.profile_journey_contract`, and leaves `section.screen-evidence` without selected-home `next_action` continuity when navigating across screens | Rejected |
| Option B | Extend `profile_journey_contract.py` with connected same-home validators + add plain-language `next_action` continuity line in `role-screens.js` + author `docs/reference/research/ux/profile-journey-contract.md` (+ KB index/log) + strengthen `src/core` and `src/api` tests | Puts deterministic invariants in `src/core`, completes UI same-home next-action continuity safely, establishes the missing canonical UX contract doc, and verifies live Store + HTTP API + resident preview + Node `role-screens.js` end-to-end | Touches `role-screens.js` (requires `redesign-existing-projects` + `web-design-guidelines` fetch/audit per AMA Web Development Guidance) | **Selected** |
| Option C | Mutate `perspective_walkthroughs.py` / `journey_acceptance.py` statuses to `"met"` / `"pass"` and edit `role_screens_browser_check.py` | Appears to advance status counters | Violates explicit human/resident/AT approval boundaries and breaks `test_perspective_walkthroughs.py` and `test_journey_acceptance.py` | Rejected |

## Evidence Log

| ID  | Source (`path:line`) | Summary |
|-----|----------------------|---------|
| C1  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:2815-2875` | Defines `## Profile Journey Contract for the Next Prototype`, the 5 contract elements, same-home walk requirement, and `AC-034` to `AC-043`. |
| C2  | `docs/reference/README.md:955-975,1065-1085` | Knowledge base task index and UX reference directory listing where `research/ux/profile-journey-contract.md` must be indexed alongside `log.md`. |
| C3  | `docs/reference/research/ux/content-standard.md:1-140` | Plain-language content standard banning internal terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) and requiring owner + next action on stops. |
| C4  | `src/core/src/zava_forward/core/profile_journey_contract.py:1-65` | Existing 5-element single-perspective `ELEMENTS`, `validate(walkthrough)`, and `gaps(root, reg)` implementation. |
| C5  | `src/core/src/zava_forward/core/perspective_walkthroughs.py:1-145` | 10-perspective register (`AC-034` to `AC-043`) keeping all walkthrough elements `"unmet"` pending real user/AT validation. |
| C6  | `src/core/src/zava_forward/core/journey_acceptance.py:1-120` | Connected journey acceptance status (`partial` / `deferred`, `passed == []`) preserving human validation boundaries. |
| C7  | `src/core/src/zava_forward/core/journey_trace.py:1-155` | Single-home audit trace checking causal ordering (`epc_conflict` -> `correction` -> `independent_decisions` -> `handover` -> `financial_closure`) and `user_validation="not-established"`. |
| C8  | `src/core/src/zava_forward/core/home_case.py:1-130` | Canonical single-home case projection (`home_case`) and role boundary checks. |
| C9  | `src/core/src/zava_forward/core/projection.py:1-265` | Role-scoped projections: `REASON_ROLES`, `REDACTED` (`"Extra support noted"`), `NOTE_HELD`, safeguarding redaction, and minimal `contractor_summary`/`contractor_detail` (`needs_notice`, `named_contact`). |
| C10 | `src/core/src/zava_forward/core/job_pack.py:1-190` | Contractor job pack (`ACCESS_NOTICE` / `ACCESS_CLEAR`) and receipt (`Acknowledged` != quality `Accepted` or `Handed over`). |
| C11 | `src/core/src/zava_forward/core/taskqueues.py:170-330` | Deterministic `case_work_context` computing `owner`, `reason`, `next_action`, `blockers`, and pending-vs-accepted `handoff` (`confirmed_receiver`, `chase_owner`). |
| C12 | `src/core/src/zava_forward/core/quality.py:70-105,310-395` | `handover_blockers`, independent `accept_quality` (`accepted_by != submitted_by`), and `hand_over_quality` safety + resident scope checks. |
| C13 | `src/api/src/zava_forward/api/web/role-screens.js:110-160,605-650,1425-1470` | Specialist role-screen shell (`Same home: case ${c.id}`, `journeyStageMap`), and `contractor-job-pack` (`Needs notice`, `"The reason for any notice is not shared with contractors."`, `screenWithheld`). |
| C14 | `src/api/src/zava_forward/api/resident_preview/app.py:1-215` | Resident preview portal (`STAGE_TEXT`, `case_detail`, `approval_boundary`, read-only preview controls, sibling isolation). |
| C15 | `src/core/src/zava_forward/core/resident_summary.py:1-140` | Core resident summary projection (`STAGE_TEXT`, plain-language `next_step`, zero internal staff/contractor fields). |
| C16 | `src/api/tests/test_content_standard.py:1-125` | Lexical copy audit scanning `AUDITED_FILES` (including `role-screens.js`) for banned internal terms. |
| C17 | `src/api/tests/test_role_screens_conformance.py:1-155` | Static conformance guard checking CSS classes, native interactive controls, zero inline styles, and exact `setTimeout` calls in `role-screens.js`. |
| C18 | `src/api/checks/role_screens_browser_check.py:1-420` & `src/api/checks/connected_home_browser_check.py:430-725` | Browser verification harnesses for read-only specialist screens, keyboard Tab reachability, and same-home/sibling leak checks. |
| C19 | `src/core/tests/test_profile_journey_contract.py:1-90`, `test_perspective_walkthroughs.py:1-70`, `test_journey_acceptance.py:1-75` | Core tests pinning existing `validate`/`gaps` API and requiring `elements_met == 0` and `passed == []`. |
| C20 | `src/api/tests/test_epic149_ux_journey_requirement_traceability.py:1-210` | Enforces valid `REQ_ID` + `"journey"` citations, real runnable `test_*.py` references, relative links, and forbidden conformance-claim bans across all `docs/reference/research/ux/*.md` files. |
| C21 | `src/core/tests/test_live_doc_links.py:1-95` | Repository-wide Markdown relative link verifier across `docs/`. |
| C22 | `src/api/src/zava_forward/api/scenario_manifest.py:1-120` | Confirms `scenario-manifest.json` binds `workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, and `test_workbench.py` (not `role_screens_browser_check.py`). |

## Residual Risks and Open Boundaries

* Live user walkthroughs (`#155`, OQ-004/005/011), real assistive-technology runs (`#151`), and named human/resident approvals are outside code automation and must remain explicitly marked `"not-established"` / `"partial"` / `"deferred"` (`Refs #134`, never `Closes #134`).
* Any edit to `role-screens.js` must load `redesign-existing-projects` and `web-design-guidelines`, fetch the canonical web-interface-guidelines rules, avoid banned words even in comments (`C16`), and introduce zero new CSS classes, timers, or unlabelled interactive elements (`C17`).

## Self-Check and Readiness

* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order.
* [x] Every question Q1-Q5 is answered with workspace-relative `path:line` evidence (`C1`-`C22`).
* [x] Research remained strictly read-only on repository source files.
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`

