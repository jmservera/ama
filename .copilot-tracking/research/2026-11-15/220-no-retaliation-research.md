<!-- markdownlint-disable-file -->

# Task Research: 220-no-retaliation

| Field | Value |
| --- | --- |
| Date | 2026-11-15 |
| Researcher / agent | rpi-research (via RPI Agent) |
| Status | Complete |
| Research disposition | executed |
| Planning Readiness | Ready |
| Artifact path | .copilot-tracking/research/2026-11-15/220-no-retaliation-research.md |

## Research Brief

* What to research: Existing affected-person challenge, correction, dispute, and representative/nominee routes across `src/core` (`challenges.py`, `resident_decisions.py`, `store.py`, `sqlstore.py`, `workflows.py`, `nomination.py` or nomination logic, `ai_tasks.py`, `resident_portal.py`, `hazard.py`, `ranking.py`, `taskqueues.py`) and `src/api` (`server.py`, `resident.py`, `web/app.js`, `web/panels.js`, `web/resident.js`) to enforce and prove end-to-end non-retaliation, non-refusal, and zero-hazard-delay invariants across all challenge/correction entrypoints (resident digital, staff-recorded non-digital, representative/nominee, and AI proposal challenge/dispute routes) for Issue #220 Criterion 5 (`No retaliation, inferred refusal or delayed hazard response`).
* Why it matters: Closure audit batch 014 noted Criterion 5 remained unticked because wider assistant/form coverage, representative/third-party challenge non-retaliation invariants, challenge reopening, and end-to-end verification across digital, staff-recorded non-digital, representative, and assistant proposal paths were not comprehensively enforced and tested across all entrypoints with an explicit machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved` audit and view contract.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in this automatic RPI loop, plus PR `#1641` reviewers.
* Scope: `src/core/` challenge, resident decision, nomination/representative, workflow, AI proposal, hazard, ranking, store, and SQL store modules; `src/api/` HTTP endpoints and web modules excluding `web/role-screens.js`; unit and integration tests `src/core/tests/test_challenge_no_retaliation_220.py` and `src/api/tests/test_challenge_no_retaliation_api_220.py`; and directly related module READMEs.
* Non-goals: Modifying `src/api/src/zava_forward/api/web/role-screens.js` (to avoid conflicts with UX parent `#1639`), infrastructure/Bicep/Dockerfile changes, pushing to remote, or using `uv`.
* Criteria: Raising, updating, reopening, escalating, or resolving a challenge or correction request across resident digital, staff-recorded non-digital, representative/nominee, and AI proposal challenge/dispute routes must NEVER lower priority/ranking score, NEVER set or infer `refusal`, `no_access`, `sanction`, `withdrawn` (on case/consent), or negative engagement flags, NEVER close unrelated work items, and NEVER delay, pause, or extend any statutory or emergency hazard response clock (`awaiting_hazard_action`, Awaab's Law 24h/7d/14d clocks, or safeguarding clocks); any hazard concern mentioned in a challenge or correction request across any channel immediately routes/preserves independent hazard intake without waiting for challenge review, and exposes an explicit machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved` audit and view contract; `test_content_standard.py` passes cleanly.
* Requested outputs: Converged end-to-end implementation design across `src/core` and `src/api` plus comprehensive unit and API integration test contracts.
* Output mode: convergence

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | Q1-Q6 below |
| Codebase scope | `src/core/`, `src/api/`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/case_study_48_addendum.md`, `.copilot-tracking/` prior #220 artifacts |
| External scope | none (except `web-design-guidelines` rules fetch prior to any web edit if web files are changed in Implement) |
| Initial internal candidate areas | `src/core/src/zava_forward/core/challenges.py`, `resident_decisions.py`, `store.py`, `sqlstore.py`, `workflows.py`, `ai_tasks.py`, `resident_portal.py`, `hazard.py`, `ranking.py`, `taskqueues.py`, `src/api/src/zava_forward/api/server.py`, `resident.py`, `web/app.js`, `web/panels.js`, `src/api/tests/test_content_standard.py` |
| Initial external candidate areas | none during codebase research |
| Research posture | balanced |
| Posture provenance | default for multi-module (`src/core` + `src/api`) bounded task with cross-entrypoint invariant interactions |
| Explicit limits / deadline | Focused validation tier (`ruff`, `mypy`, `unittest` via `pip` only); no `web/role-screens.js` edits; no `git push` |
| Posture-specific completion basis | balanced scope coverage and adequate evidence across all challenge/correction entrypoints |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | Never modify `web/role-screens.js`; never use forbidden content-standard phrases (such as the hyphenated phrase prohibited by `test_content_standard.py`); never place `.copilot-tracking/` paths in production code or commit messages |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches workspace | Enforces KB/case-study grounding, web development guidance, focused validation tier, plain-language content standard, commit trailer | Selected: mandatory repository governance |
| Skill | `rpi-research` | Active RPI loop phase 1 | Three-wave cycle, canonical `C#` evidence log, convergence synthesis | Selected: canonical RPI research skill |
| Skill | `web-design-guidelines` / `redesign-existing-projects` | Web files (`web/app.js`, `web/panels.js`) if touched during implementation | UI/accessibility rules before web edits and review | Deferred to Implement/Review if web files require edits; Research is read-only |
| Research specialist | `hve-core-all:rpi-researcher` | General delegated lane worker | Independent lane evidence under `.copilot-tracking/research/subagents/` | Skipped (inline fallback): coupled cross-module contracts between `src/core` and `src/api` are faster and exact via direct `glob`/`grep`/`view` |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
| --- | --- | --- | --- |
| Intake | Non-interactive CLI session with explicit caller scope, entrypoint list, invariant list, test file names, and validation commands | Supplied in prompt | Execute full automatic RPI loop starting with balanced Cycle 1 research |
| Direction change | None required; Cycle 1 covered all challenge/correction entrypoints within scope | N/A | Maintain balanced posture |
| Convergence | Cycle 1 completed Wider, Deeper, and Contrarian waves with full evidence | Converged | Select Option 1 (end-to-end runtime invariant guard + reopen + representative/nominee + AI/assistant/form coverage + immediate hazard routing + `non_retaliation_assurance`/`hazard_clock_preserved` contract) |

## Scope and Success Criteria

* Scope: All challenge and correction entrypoints in `src/core` and `src/api` (excluding `web/role-screens.js`), plus `src/core/tests/test_challenge_no_retaliation_220.py`, `src/api/tests/test_challenge_no_retaliation_api_220.py`, and directly related documentation.
* Assumptions: Prior 2026-11-14 `src/core` additions (`220-affected-person-challenge-2305`) must be verified on current HEAD (`7f83f4749`) rather than assumed merged or complete.
* Success criteria:
  * Every research question is answered with exact `path:line` `C#` evidence.
  * Every challenge/correction entrypoint across digital, staff non-digital, representative/nominee, and AI proposal dispute/challenge paths is inventoried and checked against all four invariant dimensions and hazard-concern routing.
  * Alternatives are compared and one convergence recommendation is selected.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect challenge/correction implementation across `src/core` and `src/api`; enforce and prove end-to-end non-retaliation, non-refusal, zero-hazard-delay, immediate hazard intake routing across all channels, and machine-checkable `non_retaliation_assurance` / `hazard_clock_preserved` audit & view contracts; add `test_challenge_no_retaliation_220.py` and `test_challenge_no_retaliation_api_220.py`; keep `test_content_standard.py` green.
* Inferred research questions: Which prior #220 commits are present on `7f83f4749`? What exact API routes, portal endpoints, resident decision actions, representative/nominee checks, workflow handlers, and AI proposal challenge/review actions exist today? What fields does `test_content_standard.py` ban?
* Caller constraints and non-goals: Do not modify `web/role-screens.js`; use `pip` only (no `uv`); focused tier validation; commit locally with Copilot trailer; do not push.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
| --- | --- | --- | --- |
| exclude | Do not modify `src/api/src/zava_forward/api/web/role-screens.js` | Caller prompt | Any `src/api` web wiring must live in `server.py` / `resident.py` / `web/app.js` (or non-`role-screens.js` files) without touching `web/role-screens.js` |
| add | Require explicit machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved` in audit & view contracts across all challenge/correction entrypoints including reopen, representative/nominee, and AI proposal routes | Caller prompt | Audit events and view payloads across `challenges.py`, `resident_decisions.py`/`store.py`/`sqlstore.py`, `ai_tasks.py`/`workflows.py`, and `src/api` must expose consistent machine-checkable contract |
| exclude | Do not push to remote; no `uv` | Caller prompt | Local verification and clean local commit only |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| ---: | --- | --- | --- | --- |
| Q1 | Which challenge, correction, nomination/representative, and AI proposal dispute files and commits currently exist on HEAD `7f83f4749` across `src/core` and `src/api`? | breadth | H | answered |
| Q2 | How do resident digital, staff-recorded non-digital (`resident_decisions.py` / `server.py`), representative/nominee, and AI proposal challenge/dispute (`ai_tasks.py` / `assistants.py` / `challenges.py`) entrypoints currently handle raising, updating, reopening, escalating, and resolving challenges? | depth | H | answered |
| Q3 | How are case priority/ranking, refusal/no-access/sanction/withdrawn/negative-engagement flags, unrelated task closures, and statutory/emergency hazard clocks (`awaiting_hazard_action`, Awaab's Law 24h/7d/14d clocks, safeguarding clocks) modeled and protected across JSON `Store` and SQLite `SqlStore`? | depth | H | answered |
| Q4 | How is a hazard concern mentioned inside a challenge or correction request routed to immediate independent hazard intake across every channel (staff workbench, digital, representative, AI/assistant proposal challenge, `ChallengeRegister`), and where are gaps? | depth | H | answered |
| Q5 | What exact schema should `non_retaliation_assurance` and `hazard_clock_preserved` carry on challenge records, audit events, API responses, case/assistant views, and `web/panels.js` without touching `web/role-screens.js`? | depth | H | answered |
| Q6 | What rules and forbidden phrases does `test_content_standard.py` enforce across Python, JS, HTML, and Markdown files? | straightforward | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14/220-affected-person-challenge-2305-research.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/regulatory/README.md`, `docs/reference/research/sector/housing-association-primer.md`, GitHub Issue #220.
* Reused (verified) findings: Verified directly on HEAD `7f83f4749` that the 2026-11-14 `challenges.py` (`escalate`, `FORBIDDEN_ADVERSE_FIELDS`, `SAFEGUARDS`, `assert_no_adverse_challenge_effects`) and `resident_decisions.py` (`challenge_update`, `challenge_escalate`) additions are already committed (`C1`-`C4`).
* Superseded / stale: Closure audit batch 014 gaps remain open on HEAD `7f83f4749` (`reopen` / `challenge_reopen`, representative/nominee challenge metadata, wider `ai_task` and `assistants` proposal challenge coverage, store-backed immediate hazard intake routing on `hazard_concern`, expanded clock/no-access/withdrawn/safeguarding invariants, and explicit `non_retaliation_assurance` / `hazard_clock_preserved` audit & view contract).

## Cycle 1 Execution

### Wave 1 - Wider (Entrypoints, Stores, Clocks, and Contracts)

Mapped every challenge, correction, nomination, service-dispute, hazard-clock, AI-proposal, and HTTP/UI surface across `src/core` and `src/api`:

* Store-independent challenge register and safeguard helpers live in `src/core/src/zava_forward/core/challenges.py:18-525` (`ChallengeRegister`, `FORBIDDEN_ADVERSE_FIELDS`, `SAFEGUARDS`, `reject_adverse_mapping`, `assert_no_adverse_challenge_effects`).
* Store-backed case challenge, nomination, representative-authority, and service-dispute routes live in `src/core/src/zava_forward/core/resident_decisions.py:490-815` (`challenge_catalog`, `priority_challenge_state`, `followup_view`), `1015-1102` (`_res_authority_record`, `_res_authority_revoke`), `1146-1275` (`_res_nomination_record`, `_res_nomination_correct`, `_res_nomination_review`), `1374-1465` (`_res_service_open`, `_res_service_reopen`), and `1484-1665` (`_res_challenge_open`, `_res_challenge_update`, `_res_challenge_escalate`, `_res_challenge_resolve`).
* Both `Store` (`src/core/src/zava_forward/core/store.py:130-156,955-1035,1095-1140`) and `SqlStore` (`src/core/src/zava_forward/core/sqlstore.py:55-68,750-780`) inherit `ResidentDecisionMixin`; `_ranking()` (`store.py:958-970`) ranks strictly by `(-urgent, -score, id)` and never reads `affected_challenges`, `nomination_records`, or `service_requests`. Note that `resident_demo/app.py` and `resident_preview/app.py` are standalone consent-pack previews with no challenge routes; resident digital challenges enter through `channel="Digital"` on `ChallengeRegister` and `/api/cases/<cid>/resident` / `/api/cases/<cid>/followup` / `/api/assistants/proposals/<tid>/challenge`.
* Statutory and emergency hazard clocks live in `src/core/src/zava_forward/core/hazard.py:1-145` and `src/core/src/zava_forward/core/workflows.py:345-445`, with queue metrics (`awaiting_hazard_action`, `hazards_open`, `resident_overdue`) computed in `src/core/src/zava_forward/core/taskqueues.py:114-145`.
* AI task recommendations (`kind == "ai_task"`) are reviewed in `src/core/src/zava_forward/core/ai_tasks.py:350-405`; SQL-backed role assistant proposals (`assistant_tasks`) are projected and reviewed in `src/core/src/zava_forward/core/assistants.py:1094-1146,2041-2109`; staff form extraction drafts are reviewed in `src/core/src/zava_forward/core/form_review.py:140-260`.
* HTTP routes are dispatched in `src/api/src/zava_forward/api/server.py:570-625,1125-1230` (`/api/cases/<cid>/resident`, `/api/cases/<cid>/followup`, `/api/cases/<cid>/hazard-raise`, `/api/ai/review`, `/api/assistants/proposals/<tid>/review`), with UI rendering in `src/api/src/zava_forward/api/web/panels.js:430-575` and draft state preservation in `src/api/src/zava_forward/api/web/app.js:1092,1197,1206,1338`.

### Wave 2 - Deeper (Exact Gaps Against Issue #220 Criterion 5)

1. Missing reopen route across both challenge layers (`C1`, `C2`):
   * `ChallengeRegister.review` (`challenges.py:381-383`) and `escalate` (`challenges.py:400-401`) reject resolved challenges, and `ChallengeRegister.reopen(...)` does not exist.
   * `ResidentDecisionMixin` defines `challenge_open`, `challenge_update`, `challenge_escalate`, and `challenge_resolve` (`resident_decisions.py:1656-1663`), with no `challenge_reopen` action.
2. Incomplete adverse-effect and statutory-clock runtime enforcement (`C3`, `C4`):
   * `FORBIDDEN_ADVERSE_FIELDS` (`challenges.py:32-47`) lacks `no_access`, `non_access`, `withdrawn_flag`, `negative_engagement`, `engagement_penalty`, `safeguarding_delay`, `safeguarding_clock_paused`, and `awaabs_clock_delayed`.
   * `assert_no_adverse_challenge_effects` (`challenges.py:130-192`) is called in tests rather than inside `_res_challenge_*` / assistant challenge handlers at runtime, and does not yet inspect `no_access` / `access_attempts`, `withdrawn` status on case/decision/resident, `negative_engagement`, `work_orders` / `packages` / `handoff` / `resident_update`, `awaiting_hazard_action` preservation, Awaab's Law 24h/7d/14d deadlines (`aware_at`, `response_due_at`, `investigation_due_at`, `summary_due_at`, `make_safe_due_at`, `resident_update_due_at`), `safeguarding` clocks, or controlled verification when a challenge appends a brand-new independent hazard entry while leaving all pre-existing hazards untouched.
3. Representative / nominee / third-party challenge and correction coverage (`C5`):
   * `ChallengeRegister.submit` (`challenges.py:216-309`) and `_res_challenge_open` / `_res_challenge_update` (`resident_decisions.py:1533-1602`) have no `submitted_by` (`The resident`, `Their representative`, `Nominee`) or `representative_ref` tracking, and `CHALLENGE_CHANNELS` (`resident_decisions.py:553`) omits `"Assisted visit"` and `"Trusted intermediary"` from `INTAKE_CHANNELS` (`resident_decisions.py:37-44`).
4. Wider AI proposal (`ai_task`, `form_review`, and `assistants`) challenge/dispute coverage (`C6`, `C7`, `C8`):
   * `challenge_catalog` and `_priority_record` (`resident_decisions.py:570-660`) index only priority recommendations (`r.get("kind") != "ai_task"`), excluding `ai_task` recommendations (`kind == "ai_task"` in `store.data["recommendations"]`, `ai_tasks.py:358`) and `form_review` records (`c.get("forms", [])`, `form_review.py:140-260`).
   * SQLite `assistant_tasks` (`assistants.py:1094-1146,2041-2109`) supports `verify`, `accept`, `edit-accept`, and `reject`, but lacks a non-retaliatory affected-person/representative/staff challenge & correction route (`Assistants.challenge` + `POST /api/assistants/proposals/<tid>/challenge`).
5. Immediate independent hazard intake routing + machine-checkable assurance contract (`C1`, `C9`, `C10`):
   * Store-backed `_res_challenge_open` / `_res_challenge_update` (`resident_decisions.py:1535-1602`) lack `hazard_concern` and `hazard_intake` routing.
   * Neither `ChallengeRegister`, `ResidentDecisionMixin`, `Assistants`, nor HTTP audit/view payloads expose explicit machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved` fields.

### Wave 3 - Contrarian (Regression Traps, Schema Locks, and Content Standard Constraints)

1. Strict case-equality assertions in existing tests (`C11`, `C12`, `C13`):
   * `src/core/tests/test_resident_decisions.py:1616-1618` and `src/core/tests/test_issue_220_challenge_route.py:666-668` pop `"affected_challenges"` from the case after standard challenge actions and assert `after == before`.
   * `src/core/tests/test_resident_decisions.py:229` asserts `records[0]["corrections"][0]["challenge"] == before["affected_challenges"][0]`.
   * `src/core/tests/test_issue_220_challenge_route.py:722,780` updates a challenge with `"while damp repair continues"` and asserts exact hazard count `2`.
   * Design consequence: Store `non_retaliation_assurance` and `hazard_clock_preserved: True` directly on each stored `affected_challenges` record at write time (alongside `safeguards`), keep `followup_view` lossless on `affected_challenges`, never heuristically auto-append to `c["hazards"]` from free-text keywords, and append to `c["hazards"]` only when explicit `hazard_intake` is provided with `hazard_concern=True` (while always recording immediate `hazard_referral` on the challenge record whenever `hazard_concern=True`).
2. Intentional `nomination_record(hazard_concern=True)` fail-closed check (`C14`):
   * `src/core/tests/test_resident_decisions.py:343` explicitly expects `nomination_record(..., hazard_concern=True)` to raise `ValueError`. Keep `_res_nomination_record`'s fail-closed check intact while enforcing non-retaliation invariants across `nomination_record`, `nomination_correct`, and `nomination_review`.
3. Closed field-set validation in `_res_challenge_*` (`C15`):
   * `src/api/tests/test_resident_api.py:567-572` asserts unknown keys like `recorded_by="forged"` return HTTP `400`. Keep strict `required_fields <= set(body) <= required_fields | optional_fields` checks so unknown keys fail closed.
4. Browser harness required-input loop in `web/panels.js` (`C16`):
   * `src/api/src/zava_forward/api/web/panels.js:478-484` checks `!input.value.trim()` unless optional, and `challenge_browser_check.py:114-125` fills only the original 9 fields. Keep those 9 fields unchanged, give any new `<select>` non-empty default first options (`"The resident"` and `"No"`), and mark conditional `representative_ref` optional unless representative/nominee is chosen.
5. Content-standard, formatting, and typing constraints (`C17`, `C18`):
   * `src/api/tests/test_content_standard.py:13-53` bans the forbidden hyphenated phrase in Python, bans internal workflow nouns in `web/*.js` and `web/*.html`, and requires `"Owner: ... Next action: ..."` on failure strings in `panels.js` and `assistants.js`.
   * `src/core/pyproject.toml` and `src/api/pyproject.toml` enforce `mypy --strict` across `src` and `tests`, and exclude legacy modules from `ruff format` per ADR 0006.

## Evidence Log

| ID | Source (`path:line`) | Summary |
| --- | --- | --- |
| `C1` | `src/core/src/zava_forward/core/challenges.py:216-525` | `ChallengeRegister` implements `submit`, `update`, `review`, `escalate`, `resolve`, `confirm_hazard_handoff`, `hazard_referrals_overdue`, `overdue`, and `view`; lacks `reopen`, representative metadata, and `non_retaliation_assurance` / `hazard_clock_preserved`. |
| `C2` | `src/core/src/zava_forward/core/resident_decisions.py:1484-1665` | `ResidentDecisionMixin` implements `challenge_open`, `challenge_update`, `challenge_escalate`, and `challenge_resolve` in `RESIDENT_ACTIONS` / `FOLLOWUP_ACTIONS`; lacks `challenge_reopen`. |
| `C3` | `src/core/src/zava_forward/core/challenges.py:32-55` | `FORBIDDEN_ADVERSE_FIELDS` and `SAFEGUARDS` define initial safeguard constants; `test_issue_220_challenge_route.py:126-131` checks `SAFEGUARDS` equality and `FORBIDDEN_ADVERSE_FIELDS` iteration. |
| `C4` | `src/core/src/zava_forward/core/challenges.py:130-192` | `assert_no_adverse_challenge_effects` checks priority/score/urgent, `closed`, `decision`, `measure_decisions`, `hazards`, `service_requests`, and task/return closures; needs `no_access`, `withdrawn`, `negative_engagement`, `work_orders`/`packages`/`handoff`/`resident_update`, Awaab's Law 24h/7d/14d and safeguarding clocks, `awaiting_hazard_action`, and controlled `allow_new_independent_hazard`. |
| `C5` | `src/core/src/zava_forward/core/resident_decisions.py:37-44,553,1015-1102` | `INTAKE_CHANNELS` includes `"Assisted visit"` and `"Trusted intermediary"`, and `representative_authorities` tracks representative authority, whereas `CHALLENGE_CHANNELS` lists 4 channels and challenges lack `submitted_by` / `representative_ref`. |
| `C6` | `src/core/src/zava_forward/core/resident_decisions.py:570-660` | `challenge_catalog` and `_priority_record` exclude `kind == "ai_task"` (`ai_tasks.py:350-405`) and form-review suggestions (`form_review.py:140-260`). |
| `C7` | `src/core/src/zava_forward/core/assistants.py:1094-1146,2041-2109` | SQLite `assistant_tasks` supports `verify`, `accept`, `edit-accept`, and `reject`, with `_view` projecting `stale`, `actionable`, and `review_flag`, but has no affected-person/representative/staff challenge & correction route. |
| `C8` | `src/api/src/zava_forward/api/server.py:570-625,1125-1230` | HTTP endpoints expose `/api/cases/<cid>/resident`, `/api/cases/<cid>/followup`, `/api/cases/<cid>/hazard-raise`, `/api/ai/review`, and `/api/assistants/proposals/<tid>/review`. |
| `C9` | `src/core/src/zava_forward/core/workflows.py:372-391` | `raise_hazard` appends an active home-scoped safety record (`released=False`, `hold.status="Active"`, `aware_at`) and emits `safety_raised` / `safety_emergency` audit events via `hazard.persist_event`. |
| `C10` | `src/core/src/zava_forward/core/taskqueues.py:114-145` | `awaiting_hazard_action` counts open unreferred hazards (`not h.get("released") and not h.get("referred")`). |
| `C11` | `src/core/tests/test_resident_decisions.py:229,1605-1621` | Existing tests assert `records[0]["corrections"][0]["challenge"] == before["affected_challenges"][0]` and `after.pop("affected_challenges"); after == before` on standard challenges. |
| `C12` | `src/core/tests/test_issue_220_challenge_route.py:126-131,666-668,722-780` | Existing Issue #220 tests assert `shown["safeguards"] == SAFEGUARDS`, `stripped_after == case_before`, and exact hazard count `2` when challenge text mentions `"while damp repair continues"`. |
| `C13` | `src/api/checks/challenge_browser_check.py:114-143` | Browser check exercises `#affected-challenges`, `#challenge-open` (9 fields), and `#challenge-resolve-CH-1`, asserting unchanged `decision`, `measure_decisions`, `hazards`, `closed`, and `service_requests`. |
| `C14` | `src/core/tests/test_resident_decisions.py:343` | Existing test asserts `nomination_record(..., hazard_concern=True)` raises `ValueError` directing immediate safety reporting. |
| `C15` | `src/api/tests/test_resident_api.py:567-572` | Existing API test asserts unknown challenge payload keys (`recorded_by="forged"`) return HTTP `400` and mutate nothing. |
| `C16` | `src/api/src/zava_forward/api/web/panels.js:478-575` | `formFor` validates `!input.value.trim()` on inputs unless optional; `web/role-screens.js` is off-limits per caller constraint. |
| `C17` | `src/api/tests/test_content_standard.py:13-53` | Enforces plain-language content rules across Python and JS. |
| `C18` | `src/core/pyproject.toml:1-65` and `src/api/pyproject.toml:1-65` | Configure `mypy --strict` across `src` and `tests` and ADR 0006 `ruff.format` exclusions for legacy modules. |

## Synthesized Findings and Selected Recommendation

* **Selected Convergence Approach (Option 1)**:
  1. **`challenges.py` (`ChallengeRegister` + runtime safeguard contract)**:
     * Add `build_non_retaliation_assurance(*, hazard_concern: bool = False, independent_hazard_routed: bool = False) -> Record` and attach `non_retaliation_assurance` + `hazard_clock_preserved: True` to every `ChallengeRegister` record and `.view()`.
     * Expand `FORBIDDEN_ADVERSE_FIELDS` and `assert_no_adverse_challenge_effects` to enforce non-lowering of `score`/`urgent`/`priority`/ranking, rejection of `refusal`/`no_access`/`non_access`/`sanction`/`withdrawn`/`negative_engagement` inferences across case, `resident`, `decision`, and `measure_decisions`, non-closure of `tasks`, `returns`, `service_requests`, `work_orders`, `packages`, `handoff`, and `resident_update`, and strict preservation of `awaiting_hazard_action`, Awaab's Law 24h/7d/14d clocks (`aware_at`, `response_due_at`, `investigation_due_at`, `summary_due_at`, `make_safe_due_at`, `resident_update_due_at`), and `safeguarding` clocks, with `allow_new_independent_hazard: bool = False` verifying `after_hazards[:len(before_hazards)] == before_hazards` plus active intake state on any newly routed independent hazard.
     * Add `ChallengeRegister.reopen(...)` (preserving prior resolution history and keeping prior `"corrected"` staleness intact until separate human re-review) and `submitted_by` / `representative_ref` support across `submit`, `update`, and `reopen`.
  2. **`resident_decisions.py` (Store & SqlStore case challenge, representative, AI-task/form, and immediate hazard routing)**:
     * Expand `CHALLENGE_CHANNELS` to include `"Assisted visit"` and `"Trusted intermediary"`.
     * Add `challenge_reopen` (`_res_challenge_reopen`) to `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS`.
     * Add optional `submitted_by` (`"The resident"`, `"Their representative"`, `"Nominee"`), `representative_ref`, `hazard_concern` (`bool`), and `hazard_intake` (`{category, priority, source, aware_at, note?}`) to `challenge_open`, `challenge_update`, and `challenge_reopen` while keeping unknown keys rejected (`400`). When `hazard_concern=True`, immediately record `hazard_referral` (`status="referred_on_receipt"`, `independent_intake=True`, `waits_for_challenge_review=False`, `independent_route`, `hazard_clock_preserved=True`) and, if `hazard_intake` is supplied, immediately append an active independent case hazard entry (`c["hazards"]`) via the `raise_hazard` intake contract without waiting for challenge review.
     * Extend `challenge_catalog`, `_priority_record`, `_dependency`, and `priority_challenge_state` to support recorded `ai_task` recommendations (`kind == "ai_task"` for `case_id in rec.get("case_ids", [])`) and `form_review` extraction records (`f"form:{form['id']}"` on `c.get("forms", [])`) alongside priority recommendations, without mutating `store.data["recommendations"]`.
     * Wrap `_res_challenge_open`, `_res_challenge_update`, `_res_challenge_reopen`, `_res_challenge_escalate`, `_res_challenge_resolve`, `_res_nomination_record`, `_res_nomination_correct`, `_res_nomination_review`, `_res_service_open`, and `_res_service_reopen` with runtime `assert_no_adverse_challenge_effects`, attach `non_retaliation_assurance` and `hazard_clock_preserved: True` to every challenge record and `followup_view` (`challenge_non_retaliation` summary when challenges/targets are projected), and emit `non_retaliation_assurance=verified hazard_clock_preserved=true` in challenge audit details.
  3. **`assistants.py`, `server.py`, and `web/panels.js` / `web/app.js` (without touching `web/role-screens.js`)**:
     * Add `Assistants.challenge(user, tid, body)` in `assistants.py` supporting `open`, `update`, `reopen`, `escalate`, and `resolve` on SQLite `assistant_tasks` proposals across digital, staff non-digital, and representative/nominee channels, with immediate independent hazard referral/intake when `hazard_concern=True`, staleness marking (`challenged_stale`) on `"Correction recorded"` so an un-reverified corrected assistant proposal is not relied on, runtime `assert_no_adverse_challenge_effects` on the linked case, and `non_retaliation_assurance` + `hazard_clock_preserved: True` in `Assistants._view` and event history.
     * Expose `POST /api/assistants/proposals/<tid>/challenge` in `server.py`.
     * Update `web/panels.js` (`renderChallengePanel`) to support `"Assisted visit"` / `"Trusted intermediary"` channels, `submitted_by` (default `"The resident"`) + conditional optional `representative_ref`, `hazard_concern` selector (default `"No"`), reopening resolved challenges (`#challenge-reopen-${record.id}`), and plain-language display of the non-retaliation and safety-clock-preserved confirmation, while keeping `challenge_browser_check.py` and `test_content_standard.py` green and never touching `web/role-screens.js`.
  4. **Tests & Documentation**:
     * Add `src/core/tests/test_challenge_no_retaliation_220.py` and `src/api/tests/test_challenge_no_retaliation_api_220.py` proving every invariant across JSON `Store`, SQLite `SqlStore`, `ChallengeRegister`, `ai_task` & `form_review` challenges, `Assistants.challenge`, HTTP endpoints, representative/nominee channels, reopen/escalate/resolve flows, Awaab's Law 24h/7d/14d + safeguarding + `awaiting_hazard_action` clocks, and immediate hazard intake routing.
     * Update directly related sections in `src/core/README.md` and `src/api/README.md`.

* **Rejected Alternatives**:
  * Heuristic free-text keyword auto-creation of `c["hazards"]` entries: rejected because `test_issue_220_challenge_route.py:722,780` uses `"while damp repair continues"` and asserts exact hazard count `2` (`C12`).
  * Mutating top-level `c` fields outside `affected_challenges` on standard challenges without hazard intake: rejected because `test_resident_decisions.py:1616-1618` and `test_issue_220_challenge_route.py:666-668` assert `after == before` after popping `affected_challenges` (`C11`, `C12`).

## Self-Check

* [x] All three waves (Wider, Deeper, Contrarian) executed in order.
* [x] Every question Q1-Q6 answered with `path:line` `C#` evidence.
* [x] Convergence recommendation selected and alternatives recorded with evidence-based rejection rationale.
* [x] Research phase made zero edits to repository source files.
* [x] `Research disposition: executed` and `Planning Readiness: Ready` recorded.

