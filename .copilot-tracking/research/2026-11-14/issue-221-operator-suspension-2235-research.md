<!-- markdownlint-disable-file -->

# Task Research: issue-221-operator-suspension-2235

| Field              | Value                                                                                      |
|--------------------|--------------------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                                 |
| Researcher / agent | rpi-research (coordinated by RPI Agent)                                                    |
| Status             | Complete                                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-14/issue-221-operator-suspension-2235-research.md       |

## Research Brief

* What to research: Inspect existing operator suspension, guardrail breach, incident, and restart implementation across `src/core` and `src/api` to verify gaps and strengthening needed for Issue #221 remaining criteria 5 (`Guardrail breach record names restart authority per RULE-024`) and 6 (`Suspension and manual fallback drill is tested (NFR-014)`).
* Why it matters: Ensures every guardrail breach and incident suspension record explicitly names and enforces `restart_authority` per `RULE-024` (rejecting blank, placeholder/unappointed default, self-approval, and automatic restart) and proves end-to-end suspension, manual fallback continuity (including statutory hazard response), and authorised restart drills (`NFR-014`).
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases in the confirmed automatic RPI session for Issue #221.
* Scope: `src/core` (`continuity.py`, `governance.py`, `rai_release.py`, `store.py`, `sqlstore.py`, `ai_tasks.py`), `src/api` (`server.py` and suspension/drill tests), and authoritative requirements in `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/case_study_48_addendum.md`, and `docs/reference/method/operator-suspension-drill-protocol.md`.
* Non-goals: Fabricating real human OD-35 restart authority appointments or filling the blank human drill record in `docs/reference/method/operator-suspension-drill-protocol.md`; modifying unrelated UI or infrastructure modules; pushing to remote.
* Criteria: Every codebase claim backed by `path:line` `C#` evidence; explicit verification of `RULE-024`, `RULE-020`, `FR-053`, `AC-072`, `AC-078`, and `NFR-014` contracts; clear gap analysis against any prior partial slice; concrete convergence recommendation ready for planning.
* Requested outputs: Completed 3-wave primary research artifact with convergence recommendation and Planning Readiness verdict.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How do `src/core` and `src/api` currently implement guardrail breach / incident suspension `restart_authority` (`RULE-024`) and suspension/manual-fallback drills (`NFR-014`), and what exact enforcement and test gaps remain for Issue #221 criteria 5 and 6? |
| Codebase scope                   | `src/core/`, `src/api/`, `docs/brds/`, `docs/prds/`, `docs/reference/method/`, `.copilot-tracking/`                                                                |
| External scope                   | none                                                                                                                                                               |
| Initial internal candidate areas | `src/core/src/zava_forward/core/continuity.py`, `src/core/src/zava_forward/core/governance.py`, `src/core/src/zava_forward/core/rai_release.py`, `src/api/src/zava_forward/api/server.py`, `src/core/tests/test_governance.py`, `src/api/tests/test_operator_suspension.py` |
| Initial external candidate areas | none                                                                                                                                                               |
| Research posture                 | balanced                                                                                                                                                           |
| Posture provenance               | default (bounded internal engineering task with named targets and adjacent `core`/`api`/store interactions)                                                        |
| Explicit limits / deadline       | Worktree `/home/azureuser/source/ama-demo-wt/feat-221-operator-suspension-2235`, branch `feat/ai-221-operator-suspension-2235`, do not push                        |
| Posture-specific completion basis | balanced scope coverage and adequate evidence across `RULE-024`, `NFR-014`, `core`, `api`, and drill tests                                                        |
| Edits allowed during research?   | no, research-only                                                                                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                               |
| Known constraints / excluded sources | Constructed test fixtures must preserve the honest boundary that OD-35 human appointment is not fabricated (`docs/reference/method/operator-suspension-drill-protocol.md`) |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches repository and tracking paths | Enforces regulatory/OD-35 human approval boundaries, validation tiers, and local git config rules | Selected: mandatory repo instructions |
| Skill               | `rpi-research`                   | Explicit RPI phase skill for Research             | Three-wave research artifact contract        | Selected: active phase skill   |
| Skill               | `python-foundational`            | Python codebase topic match                       | Python typing/testing conventions            | Skipped: existing `src/core` and `src/api` patterns provide direct local conventions |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered specialist for independent lanes  | Delegated lane artifact under `subagents/`   | Skipped: tightly coupled `core`/`api` inspection fits low-latency inline investigation |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive session with explicit caller scope, branch, acceptance criteria 5 & 6, and validation commands | N/A (non-interactive)     | Proceed directly in balanced convergence mode      |
| Direction change | None at intake                                              | N/A                       | Maintain caller scope on Issue #221 criteria 5 & 6 |
| Convergence      | No external ambiguity or scope conflict found after Cycle 1 synthesis; non-interactive confirmed automatic RPI loop | N/A (non-interactive)     | Converge on shared `restart_authority` RULE-024 validator + `continuity`/`governance` enforcement + `core`/`api` NFR-014 drill suites |

## Scope and Success Criteria

* Scope: `src/core` and `src/api` operator suspension, guardrail breach record, incident record, manual fallback continuity, statutory hazard continuity, and restart authority validation plus unit/drill tests for Issue #221 criteria 5 and 6.
* Assumptions: Prior commits on parent history may have partially touched `governance.py` or `continuity.py`; every file in the current worktree must be inspected directly rather than assumed.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect existing operator suspension / incident / restart implementation in `src/core` and `src/api`; ensure guardrail breach / incident suspension record explicitly names and validates `restart_authority` per `RULE-024` (requiring distinct human restart authority, rejecting blank/placeholder/self-approval); add comprehensive unit/drill tests proving end-to-end suspension, manual fallback continuity (including statutory hazard response), and authorised restart drill (`NFR-014`).
* Inferred research questions: How do `continuity.py`, `governance.py`, `rai_release.py`, `sqlstore.py`, `store.py`, and `server.py` interact during guardrail breaches vs operator suspensions? Are placeholder strings, blank strings, self-approval (suspender/recorder/proposer approving their own restart), and mismatched authority references rejected consistently across both guardrail breach records and incident suspension records, in both JSON/memory and SQL stores?
* Caller constraints and non-goals: Write all 4 RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/`, pass `mypy`, `ruff check`, `ruff format --check`, and `unittest`, and commit locally without pushing.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focus on Issue #221 remaining criteria 5 (`RULE-024` restart authority) and 6 (`NFR-014` suspension & manual fallback drill tests) | Caller intake prompt | Keeps implementation surgical to `RULE-024` and `NFR-014` across `src/core` and `src/api` |
| exclude                                                  | Do not push branch to remote; do not fabricate real human drill sign-off | Caller intake & repo instructions | Restricts git operations to local commit and keeps drill tests explicitly fixture-scoped |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status   |
|---:|------------------|------------------------------------------|-----------|----------|
| Q1 | What exact requirements do `RULE-024`, `RULE-020`, `AC-078`, `FR-053`, `AC-072`, and `NFR-014` specify in the BRD, PRD, Addendum, and Drill Protocol? | breadth | H | answered |
| Q2 | How are guardrail breach records (`governance.py` / `rai_release.py`) and operator suspension/incident/restart records (`continuity.py` / `store.py` / `sqlstore.py` / `server.py`) currently implemented, and what validation gaps exist for `restart_authority` (blank, placeholder, self-approval, authority mismatch, rule linkage)? | depth | H | answered |
| Q3 | What drill and unit tests currently exist in `src/core/tests/` and `src/api/tests/`, and what end-to-end drill scenarios (breach-triggered suspension, dispatch/proposal blocking, manual case work continuity, emergency/statutory hazard response continuity, unauthorized/premature/self-approved/placeholder restart denial, and distinct human authorised restart) are missing or under-tested for `NFR-014`? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * `docs/reference/method/operator-suspension-drill-protocol.md`
  * `.copilot-tracking/research/2026-11-14-221-operator-suspension-restart-authority-research.md`
  * `.copilot-tracking/changes/2026-11-14-221-operator-suspension-restart-authority-changes.md`
  * `.copilot-tracking/reviews/2026-11-14-221-operator-suspension-restart-authority-review.md`
* Reused (verified) findings:
  * Commit `b2340f8af` added `restart_rule="RULE-024"` and `automatic_restart=False` to `governance.breach_record` and `continuity.suspend`, added `automatic` flag refusals to `breach_restart` and `restart_decide`, and added `authority != b.get("restart_authority")` comparison in `breach_restart` (verified directly in `governance.py:551-579` and `continuity.py:440-510`).
  * `docs/reference/method/operator-suspension-drill-protocol.md` establishes the 8-step synthetic drill protocol and the strict boundary that constructed fixture tests prove system enforcement without fabricating real human OD-35 appointments.
* Superseded / stale:
  * The brief prior note in `.copilot-tracking/reviews/2026-11-14-221-operator-suspension-restart-authority-review.md` assumed string-equality matching and `automatic=True` checking were sufficient for criterion 5 and that wrapping `drill(self)` satisfied criterion 6, overlooking placeholder/non-human/self-designated `restart_authority` acceptance (e.g., `"TBD"`, `"none"`, `"AI bot"`, or self-email passing both record and restart!) and missing release-recorder self-approval checks and end-to-end `core` + `api` guardrail-breach/hazard fallback drills.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to Issue #221 criteria 5 & 6; exclude remote push and fabricated human sign-off
* Active research posture and completion basis: `balanced`; balanced scope coverage and adequate evidence across requirements, `src/core`, `src/api`, and drill suites
* Explicit limits or deadline effect: none blocking; full local codebase and requirement sources available in worktree

#### Wave 1: Wider

* Plan and independent lanes: Survey Issue #221 body, BRD (`RULE-024`, `RULE-020`, `AC-078`, `OD-35`), PRD (`FR-053`, `FR-028`, `AC-072`, `NFR-014`), Case Study 48 Addendum (`MN-4.1`, `MN-4.3`), Drill Protocol (`docs/reference/method/operator-suspension-drill-protocol.md`), and locate all suspension/breach/restart modules and tests across `src/core` and `src/api`.
* Worker evidence relationships or inline fallback: Inline investigation mapped Q1 -> `C1`-`C4` and Q2/Q3 candidate surfaces -> `C5`-`C13`.
* Reflection: Both `continuity.py` (AI task/release incident suspension) and `governance.py` (home/work-package/archetype/workstream guardrail breach pause) implement `RULE-024` controls and must enforce consistent human `restart_authority` rules while preserving emergency suspension when `restart_authority` is omitted.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Inspect exact validation logic in `continuity.py`, `governance.py`, `controls.py`, `rai_release.py`, `workflows.py`, `server.py`, `test_governance.py`, `test_operator_suspension.py`, `test_continuity.py`, `test_continuity_epoch_export.py`, and `test_rai_harm_threshold_incident.py`, plus `pyproject.toml` typing/lint rules in `src/core` and `src/api`.
* Plan and independent lanes: Trace every `restart_authority` and `authority_ref` write/read/projection path and every drill step in `core` and `api`.
* Worker evidence relationships or inline fallback: Inline trace produced `C5`-`C16`, uncovering four concrete gaps:
  1. Placeholder (`"TBD"`, `"TODO"`, `"none"`, `"n/a"`, `"unknown"`, `"unavailable"`, `"placeholder"`, `"pending"`, `"unappointed"`, `"-"`), chat-memory, and automated/AI (`"AI"`, `"bot"`, `"copilot"`, `"automation"`, `"llm"`) strings are accepted as `restart_authority` in `governance.breach_record` and (when explicitly supplied) in `continuity.suspend`, and can subsequently pass `restart_propose`, `restart_decide`, and `breach_restart` if echoed back!
  2. Self-designation and self-approval gaps: `breach_record` and `suspend` allow the recording/suspending operator to name their own email/name/code/oid as `restart_authority`; `restart_propose` neither blocks `automatic=True` nor rejects suspender/proposer self-named `restart_authority`; `restart_decide` does not check `actor["name"]` or record `restart_rule="RULE-024"` on `s["restart"]`; and `breach_restart` allows the manager who recorded `rel` (`rel["recorded_by"]`) to also authorise `breach_restart` using their own release decision!
  3. `src/core` lacks an end-to-end `NFR-014` / `RULE-024` drill test proving that during a guardrail breach pause, `guard_case_event` blocks ordinary case progression on the paused scope while manual work on unaffected scopes and statutory Awaab's Law hazard workflows (`raise_hazard` and hazard progression) continue unimpeded on the paused home until distinct human restart authorisation.
  4. `src/api/tests/test_operator_suspension.py` lacks a dedicated step-by-step protocol drill test covering guardrail-breach suspension over HTTP/service, placeholder/unappointed/self-approval refusal across `suspend`/`restart_propose`/`restart_decide`, full statutory hazard response continuity during suspension, `"Keep suspended"` retention, and distinct OID-bound human `ai_restart` clearance.
* Reflection: Deep inspection identified exact line-level root causes; contrarian testing is required next to ensure stricter `restart_authority` validation does not break emergency containment or legitimate human role titles or privacy projections.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge stricter `restart_authority` validation against (a) emergency containment when `restart_authority` is omitted at `suspend()` time, (b) legitimate UK housing association job titles containing words like `"Assistant"` or `"Service"`, (c) audience-limited redaction of `restart_authority` in `continuity.control_record` and `limited_export`, and (d) existing `test_governance.py` / `test_continuity.py` / `test_operator_suspension.py` / `test_rai_harm_threshold_incident.py` fixtures.
* Plan and independent lanes: Cross-check all 47 occurrences of `restart_authority` and `authority_ref` across `src/`.
* Worker evidence relationships or inline fallback: Inline contrarian audit (`C4`, `C6`, `C7`, `C11`, `C14`, `C15`):
  * Contrarian finding 1 (`C4`, `C15`): `continuity.suspend` MUST still succeed when `restart_authority` is omitted (or `None` or equal to the canonical default `"Unavailable: OD-35 authority unappointed"`), because emergency containment on a harm threshold breach (`test_rai_harm_threshold_incident.py:55-71`, Drill Protocol step 2) cannot fail closed on suspension; instead it records `"Unavailable: OD-35 authority unappointed"` and refuses restart at `restart_propose` and `restart_decide`. Explicit non-default values passed to `suspend` MUST still be validated against blank, placeholder, non-human, memory-ref, and self-designation rules!
  * Contrarian finding 2 (`C8`): Using `rai_release.NON_HUMAN_TOKENS` verbatim would reject `"Assistant Director of Assets"` (`"assistant"`) or `"Building Safety Services"` (`"service"`). Dedicated automation token detection (`{"ai", "bot", "automation", "automated", "automatic", "copilot", "llm", "cron", "daemon"}` plus multi-word phrases like `"ai assistant"`, `"ai agent"`, `"automated system"`) blocks non-human attributions without false positives on human job titles.
  * Contrarian finding 3 (`C7`, `C14`): `test_continuity_epoch_export.py:711` places a privacy canary in `restart_authority` and asserts audience-limited responses never expose it. `control_record` must keep `restart_authority` held/omitted for non-reason viewers while safely exposing closed boolean/constant fields if needed.
* Reflection: All three contrarian challenges materially sharpened the design and prevented regressions in emergency containment, role naming, and privacy projection.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| Add pure strictly-typed `restart_authority.py` helper in `zava_forward.core` enforcing `RULE-024` human authority rules (rejecting blank, placeholders, `"Unavailable..."`, chat-memory refs, AI/automation tokens, and self-designation) | C1, C4, C5, C6, C8, C9, C16 | accepted | Centralizes `RULE-024` validation under `mypy --strict` and keeps `governance.py` and `continuity.py` consistent | Selected Recommendation |
| Preserve `UNAPPOINTED_RESTART_AUTHORITY` default in `continuity.suspend` when `restart_authority` is omitted, while rejecting explicit bogus placeholders/AI/self-designation at `suspend` and rejecting `UNAPPOINTED_RESTART_AUTHORITY` at `breach_record`, `breach_restart`, `restart_propose`, and `restart_decide` | C4, C6, C13, C15 | accepted | Preserves immediate emergency suspension on threshold breaches while guaranteeing restart is impossible without a valid distinct human authority | Selected Recommendation |
| Enforce distinct human separation across breach recorder, release recorder (`rel["recorded_by"]`), suspender, and restart proposer (`actor` email/name/code/oid), plus `automatic=True` refusal in `restart_propose` and `RULE-024` metadata on restart records | C1, C5, C6, C10, C12 | accepted | Closes release-recorder self-approval and proposer/suspender self-designation loopholes | Selected Recommendation |
| Reject `"assistant"` and `"service"` as standalone forbidden tokens | C8 | rejected | False-positive hazard for human titles like `"Assistant Director"` or `"Building Safety Services"`; targeted AI/automation tokens and phrases are exact | Alternative rejected |
| Add comprehensive `NFR-014` + `RULE-024` drill tests in both `src/core/tests/` (typed drill suite + `test_governance.py`) and `src/api/tests/test_operator_suspension.py` | C2, C3, C4, C11, C12, C13, C16 | accepted | Directly proves Criterion 5 and Criterion 6 across JSON store, SQL store, workflow hazard routes, and HTTP/assistant continuity | Selected Recommendation |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Balanced scope coverage achieved; all three research questions answered with primary codebase and specification citations, and contrarian challenges resolved without open blockers.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded, tightly coupled `src/core` and `src/api` modules and requirement docs inspected directly with zero context-window pressure.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `RULE-024` and `AC-078` mandate that a guardrail breach pauses the affected home, work package, archetype, or workstream until restart is authorised under `OD-35` and `RULE-020`, naming scope, owner, evidence, containment, resident impact, remediation, and restart authority while emergency/statutory hazard response continues outside the pause | `docs/brds/agentic-retrofit-programme-brd.md:677` | grep / view | high | Also traced at line 1173 |
| C2 | `FR-053`, `FR-028`, `AC-072`, and `NFR-014` require operator suspension on critical harm or threshold breach to block new dispatch and pending/ready proposal reliance, record impacted versions/owner/restart decision, preserve manual and hazard routes, and deny restart until corrective tests and distinct authorised human approval are recorded | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:394` | grep / view | high | Traced to `BRD::RULE-020` and `BRD::RULE-024` |
| C3 | Case Study 48 Addendum Responsible AI Release Position (`MN-4.1`, `MN-4.3`) requires owned harm monitoring and witnessed suspension, communication, manual continuity, and separately approved restart drill under `FR-053`/`AC-072`/`NFR-014` | `docs/case_study_48_addendum.md:1022` | grep | high | Governance constraint |
| C4 | `Operator Suspension and Manual Fallback Drill Protocol` defines the 8-step synthetic drill, specifies default `"Unavailable: OD-35 authority unappointed"` refusal behavior, and forbids agents from fabricating real human drill sign-off | `docs/reference/method/operator-suspension-drill-protocol.md:27` | view | high | Steps 1-8 and Blank Drill Record |
| C5 | `governance.breach_record` and `governance.breach_restart` record `restart_rule="RULE-024"` and `automatic_restart=False`, but `breach_record` accepts placeholders/non-human/self-designated `restart_authority`, and `breach_restart` fails to check `different_person(user, rel["recorded_by"])` or re-validate `restart_authority` | `src/core/src/zava_forward/core/governance.py:541` | view | high | Lines 541-583 |
| C6 | `continuity.suspend`, `restart_propose`, and `restart_decide` manage AI task/release suspension and epoch fencing, but `suspend` accepts explicit placeholder/AI/self-designated `restart_authority`, `restart_propose` lacks `automatic` refusal and full `restart_authority` validation, and `restart_decide` only checks `.startswith("Unavailable")` and equality | `src/core/src/zava_forward/core/continuity.py:421` | view | high | Lines 421-547 |
| C7 | `continuity.control_record` and `limited_export` redact protected free-text fields (including `restart_authority`) for non-reason viewers | `src/core/src/zava_forward/core/continuity.py:706` | view | high | Lines 706-790 |
| C8 | `rai_release.py` defines `named()` and `named_human()`, where `NON_HUMAN_TOKENS` includes `"assistant"` and `"service"` | `src/core/src/zava_forward/core/rai_release.py:44` | view | high | Lines 44-74 |
| C9 | `controls.py` provides `different_person()`, `text()`, and `is_memory_reference()` (`MEMORY_REF`) refusing chat-memory citations as evidence | `src/core/src/zava_forward/core/controls.py:39` | view | high | Lines 39-61 |
| C10 | `workflows.raise_hazard` and hazard progression bypass `guard_case_event` deliberately so emergency and statutory hazard response remains open during any governance pause or AI suspension | `src/core/src/zava_forward/core/workflows.py:377` | view / grep | high | Confirmed alongside `governance.py:488` |
| C11 | `server.py` exposes `/api/continuity/suspend`, `/api/continuity/restart-propose`, `/api/continuity/restart-decide` (with `trusted_route`), `/api/governance/breach`, and `/api/governance/restart`, mapping `ValueError` to 400 and `PermissionError` to 403 | `src/api/src/zava_forward/api/server.py:1476` | view | high | Lines 1476-1500 |
| C12 | `test_governance.py` tests basic breach pause/restart on `JsonGov` and `SqlGov`, using `QI-1` as breach recorder, `pm1` as release recorder, and `pm2` as restart authoriser, with `"OD-35 demo"` as `restart_authority` | `src/core/tests/test_governance.py:222` | view | high | Lines 222-275 |
| C13 | `test_operator_suspension.py` tests snapshot completeness, negative restart matrix, and wraps `drill(self)` in `test_nfr_014_suspension_and_manual_fallback_drill`, without testing placeholder/AI/self-designated `restart_authority` rejection or full statutory hazard progression + `"Keep suspended"` in an explicit 8-step `NFR-014` drill | `src/api/tests/test_operator_suspension.py:296` | view | high | Lines 296-375, 699-707, 961-981 |
| C14 | `test_continuity_epoch_export.py` asserts that a privacy canary passed in `restart_authority` is never leaked in audience-limited projections | `src/api/tests/test_continuity_epoch_export.py:711` | grep | high | Privacy regression guard |
| C15 | `test_rai_harm_threshold_incident.py` posts `/api/continuity/suspend` on live harm threshold breach without supplying `restart_authority`, relying on the default unappointed sentinel so containment succeeds immediately | `src/api/tests/test_rai_harm_threshold_incident.py:55` | view | high | Emergency containment invariant |
| C16 | `src/core/pyproject.toml` and `src/api/pyproject.toml` enforce `mypy` (`strict = true`) and `ruff` (`line-length = 100`, `E,F,I,B,UP`) on all non-legacy modules and `test_operator_suspension.py` | `src/core/pyproject.toml:30` | view | high | Also `src/api/pyproject.toml:33` |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `RULE-024` / `AC-078` and `FR-053` / `AC-072` / `NFR-014` require every guardrail breach and incident suspension record to identify `restart_authority` (under `OD-35` and `RULE-020`), forbid automatic or self-approved restart, preserve manual case work and statutory hazard response throughout suspension/pause, and verify the end-to-end drill with synthetic fixtures without fabricating real human OD-35 appointments | C1, C2, C3, C4 | high | Defines exact functional and governance boundaries for criteria 5 & 6 |
| Q2 | Existing `governance.py` and `continuity.py` stamp `restart_rule="RULE-024"` and `automatic_restart=False`, but still accept placeholder (`"TBD"`, `"none"`, `"unknown"`, etc.), automated/AI, chat-memory, and self-designated `restart_authority` strings, omit `automatic` and full `restart_authority` checks in `restart_propose`, and permit release-recorder self-approval in `breach_restart` | C5, C6, C7, C8, C9, C14, C15 | high | Requires a shared `restart_authority` validator wired into `governance.py` and `continuity.py` while keeping omitted `suspend` `restart_authority` defaulting to `"Unavailable: OD-35 authority unappointed"` |
| Q3 | Existing tests cover continuity snapshots and basic breach pause, but lack negative coverage for placeholder/AI/self-designated `restart_authority` and release-recorder self-approval, and lack a comprehensive end-to-end `NFR-014` + `RULE-024` drill across both `core` (guardrail breach pause + manual unaffected work + statutory hazard lifecycle on paused home + authorised restart) and `api` (8-step HTTP/service operator suspension, fallback, hazard lifecycle, `"Keep suspended"`, and distinct OID-bound human restart) | C10, C11, C12, C13, C16 | high | Ready to plan targeted `core` and `api` implementation and drill suites |

## Key Discoveries

* **Critical validation bypass (`C5`, `C6`)**: Because `continuity.restart_propose` and `continuity.restart_decide` only check `s["restart_authority"].startswith("Unavailable")`, an operator passing `restart_authority="TBD"` or `"none"` or `"AI bot"` or their own email at `suspend()` (or `breach_record()`) creates a record whose placeholder/self-authority can later satisfy exact string equality at `restart_decide()` / `breach_restart()`.
* **Two-person release-restart bypass (`C5`, `C12`)**: In `governance.breach_restart`, `k.different_person` checks `b["recorded_by"]` but not `rel["recorded_by"]`, allowing one manager to both record the post-breach `Release` and authorise `breach_restart`.
* **Emergency containment preservation (`C4`, `C15`)**: Omitted `restart_authority` in `continuity.suspend` MUST continue to default to `"Unavailable: OD-35 authority unappointed"` so live harm-threshold breaches suspend immediately while guaranteed to block `restart_propose` and `restart_decide`.

### Complete Examples

```python
# Pure strictly-typed RULE-024 restart authority validation contract
UNAPPOINTED_RESTART_AUTHORITY = "Unavailable: OD-35 authority unappointed"

def validate_restart_authority(
    value: object,
    *,
    label: str = "the restart authority (OD-35)",
    limit: int = 200,
    allow_unappointed_default: bool = False,
    disallowed_actors: Sequence[Mapping[str, Any]] = (),
) -> str:
    ...
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach:
  1. Create strictly typed `src/core/src/zava_forward/core/restart_authority.py` implementing `UNAPPOINTED_RESTART_AUTHORITY`, `validate_restart_authority(...)`, and `ensure_distinct_restart_actor(...)` per `RULE-024`:
     * Rejects blank, whitespace-only, non-string, or >`limit` values (`ValueError`).
     * Rejects placeholder/unappointed tokens and prefixes (`unknown`, `unavailable`, `none`, `null`, `n/a`, `na`, `tbd`, `todo`, `tbc`, `pending`, `placeholder`, `unapproved`, `unappointed`, `unassigned`, `unset`, `default`, `self`, `same operator`, `-`, `--`, `?`, and `unavailable*`) with `ValueError` unless `allow_unappointed_default=True` and the stripped text equals `UNAPPOINTED_RESTART_AUTHORITY`.
     * Rejects chat-memory citations (`controls.is_memory_reference`) and AI/automation attributions (`ai`, `bot`, `automation`, `automated`, `automatic`, `copilot`, `llm`, `cron`, `daemon`, `ai assistant`, `ai agent`, `automated system`) with `ValueError`.
     * Rejects self-designation where `restart_authority` matches any disallowed actor's `email`, `name`, `code`, or `oid` (`PermissionError` citing `RULE-024`).
  2. Wire `restart_authority.py` into `governance.py` (`breach_record`, `breach_restart`) and `continuity.py` (`suspend`, `restart_propose`, `restart_decide`):
     * `governance.breach_record`: validates `restart_authority` (disallowing placeholders, `Unavailable*`, AI/automation, and the breach recorder `user`), records `actor` identity metadata (`email`, `name`, `code`, `oid`), `restart_rule="RULE-024"`, `automatic_restart=False`.
     * `governance.breach_restart`: refuses `automatic` truthy/non-false flags, enforces distinct actor from BOTH the breach recorder (`b["recorded_by"]` / `b.get("actor")`) AND the post-breach release recorder (`rel["recorded_by"]`), re-validates stored `b["restart_authority"]` and `authority_ref` via `validate_restart_authority` (rejecting placeholders/AI/recorder-self-designation), requires exact match with `b["restart_authority"]`, and stamps `restart_rule="RULE-024"` and `automatic_restart=False` on `b["restart"]`.
     * `continuity.suspend`: defaults omitted/`None` `restart_authority` to `UNAPPOINTED_RESTART_AUTHORITY`, validates via `validate_restart_authority(..., allow_unappointed_default=True, disallowed_actors=(user,))`, and stores `name` alongside `email`/`code`/`oid` in `actor`.
     * `continuity.restart_propose`: refuses `automatic` flags (`PermissionError` citing `RULE-024`) and validates stored `s["restart_authority"]` via `validate_restart_authority(..., allow_unappointed_default=False, disallowed_actors=(s.get("actor"), user))` (wrapped as `PermissionError` if stored record has unappointed/invalid authority so `restart_propose` keeps its documented `PermissionError` contract).
     * `continuity.restart_decide`: enforces distinct human actor across `email`, `name`, `code`, and `oid` against both suspender and proposer, validates both `s["restart_authority"]` and `body["authority_ref"]` under `RULE-024`, requires exact match, and stamps `restart_rule="RULE-024"` and `automatic_restart=False` on the decision record.
  3. Add comprehensive unit and end-to-end `NFR-014` + `RULE-024` drill tests:
     * `src/core/tests/test_operator_suspension_drill.py` (strictly typed under `mypy`) + targeted additions in `src/core/tests/test_governance.py`: tests `restart_authority` validator edge cases, placeholder/AI/memory/self-approval refusals, release-recorder self-approval refusal, and a full end-to-end `NFR-014`/`RULE-024` guardrail-breach & operator-suspension manual fallback drill (paused home/archetype blocks routine case mutations while unaffected manual cases and emergency/statutory Awaab's Law hazard workflows continue unimpeded on the paused home across both `Store` and `SqlStore`).
     * `src/api/tests/test_operator_suspension.py`: strengthens `test_nfr_014_suspension_and_manual_fallback_drill` and `test_breach_record_names_authority_and_drill_sequence` to exercise the full 8-step protocol over HTTP and service boundaries (breach trigger, pending/ready/in-flight containment, manual call & full statutory hazard referral/acceptance continuity during suspension, placeholder/AI/self-approval refusal at `suspend`/`restart-propose`/`restart-decide`, `"Keep suspended"` retention, and distinct OID-bound `ai_restart` clearance).
  4. Update `src/core/README.md` if needed to reflect the `RULE-024` distinct release/breach/restart authority rules accurately.
* Rationale: Closes every placeholder, automation, and self-approval loophole for Criterion 5 while preserving emergency containment and audience privacy, and delivers complete `core` + `api` drill verification for Criterion 6 under strict `mypy` and `ruff`.
* Evidence refs: C1, C2, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16
* Implementation impact: `src/core/src/zava_forward/core/restart_authority.py` (new), `src/core/src/zava_forward/core/governance.py`, `src/core/src/zava_forward/core/continuity.py`, `src/core/README.md`, `src/core/tests/test_governance.py`, `src/core/tests/test_operator_suspension_drill.py` (new), `src/api/tests/test_operator_suspension.py`.
* Confidence: high: all affected modules, callers, and 47 repository call sites were verified directly.

File tree:

```text
src/
  core/
    README.md                                              (updated)
    src/zava_forward/core/
      restart_authority.py                                 (created, mypy --strict)
      governance.py                                        (updated)
      continuity.py                                        (updated)
    tests/
      test_governance.py                                   (updated)
      test_operator_suspension_drill.py                    (created, mypy --strict)
  api/
    tests/
      test_operator_suspension.py                          (updated, mypy --strict)
```

### Alternative: Require non-default `restart_authority` before `continuity.suspend` can contain an incident

* Approach: Refuse `continuity.suspend` whenever `restart_authority` is omitted or `"Unavailable: OD-35 authority unappointed"`.
* Trade-offs: Simplifies `suspend` validation to one mode, but blocks emergency AI containment when an operator responds to an approved harm-threshold breach before OD-35 is appointed.
* Evidence refs: C4, C13, C15
* Rejection rationale: Directly violates Drill Protocol step 2 (`C4`) and breaks live harm-threshold incident containment (`C15`). Containment must always succeed immediately while restart fails closed.

### Alternative: Reuse `rai_release.named_human` verbatim for `restart_authority`

* Approach: Call `rai_release.named_human` directly on `restart_authority`.
* Trade-offs: Zero new token set, but rejects `"assistant"` and `"service"`, blocking valid human role references like `"Assistant Director of Assets"` or `"Building Safety Services Lead"` and lacks placeholder checks for `"TBD"`, `"TODO"`, `"N/A"`, `"pending"`, or actor self-matching.
* Evidence refs: C8
* Rejection rationale: Dedicated `restart_authority.py` validation avoids false positives on human titles while catching placeholders, memory citations, AI/automation attributions, and actor self-approval.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Constructed fixture drills verify software controls (`FR-053`, `AC-072`, `NFR-014`, `RULE-024`); real operational OD-35 appointment and witnessed human completion of `docs/reference/method/operator-suspension-drill-protocol.md` remain human governance gates outside software execution (`C4`).
* Follow-up: none
* Residual uncertainty: none within software scope

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Centralize `RULE-024` `restart_authority` and distinct-actor validation in `zava_forward.core.restart_authority` and enforce across `governance.py` and `continuity.py` | confirmed | evidence / caller criteria | Eliminates placeholder, non-human, and self-approval loopholes consistently across guardrail breaches and AI incident suspensions | C1, C5, C6, C8, C9, C16 | Checked by `mypy --strict`, `ruff`, and unit tests |
| Preserve `UNAPPOINTED_RESTART_AUTHORITY` default on omitted `continuity.suspend` `restart_authority` while failing closed on restart | confirmed | constraint (`C4`, `C15`) | Keeps emergency containment available while blocking premature/unappointed restart | C4, C6, C13, C15 | Existing harm-threshold incident flows remain intact |
| Prove `NFR-014` suspension, manual case fallback, statutory hazard continuity, and distinct human restart in both `src/core` and `src/api` test suites without filling the blank human drill table | confirmed | caller criteria / repo governance (`C4`) | Satisfies software verification for Criterion 6 while respecting human governance boundaries | C2, C4, C10, C13 | Tests added in `core` and `api` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Live operational OD-35 restart authority appointment and witnessed human drill record | Named human appointment by Building Safety Lead & Executive Sponsor and witnessed completion of `docs/reference/method/operator-suspension-drill-protocol.md` | Project Owner / Building Safety / Sponsor | Required before live operational pilot activation (`actual_hold` stays `True` in software) | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | None needed for Issue #221 software criteria 5 & 6 | N/A | Only if live Entra app-role schema for `OD-35` changes | no | Q1, Q2; C1, C4 |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected (`restart_authority.py` + `governance.py`/`continuity.py` enforcement + `core`/`api` `NFR-014` drill suites)
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16
* Preconditions met: All target modules, existing tests, privacy invariants, and `mypy`/`ruff` configurations verified
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                                                      |
| Lane evidence or inline fallback | Inline investigation across `docs/`, `src/core/`, and `src/api/` (`C1`-`C16`)                                                  |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (`C1`-`C16`)                                                                                                             |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `Plan` (`rpi-plan`)                                                   |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C16`)                                                                                           |
| Output mode and planning support | convergence; yes, Planning Readiness is `Ready`                                                              |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Cycle 1 three waves passed; self-check passed; pre-transition state write required before `rpi-plan`         |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/issue-221-operator-suspension-2235-research.md                         |
| Notes for planning or re-entry   | Preserve `UNAPPOINTED_RESTART_AUTHORITY` default when `restart_authority` is omitted in `continuity.suspend` and keep `restart_authority` redacted in `continuity.control_record` for non-reason viewers |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All codebase and specification questions for Issue #221 criteria 5 & 6 are answered with line-cited evidence; further research would be redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none

