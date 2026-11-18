<!-- markdownlint-disable-file -->
# RPI Plan: Issue #221 Operator Suspension, Incident and Restart Record (Criteria 5 & 6)

## Task Metadata

* Task ID: issue-221-operator-suspension-2235
* Task slug: issue-221-operator-suspension-2235
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-221-operator-suspension-2235-plan-critique.md

## Executive Summary

This plan closes the two remaining unticked software acceptance criteria on GitHub Issue #221 (**Operator suspension, incident and restart record**):

1. **Criterion 5 (`RULE-024`)**: Guardrail breach and incident suspension records must explicitly name and validate a distinct human `restart_authority`, rejecting blank values, generic or unappointed placeholders (`TBD`, `none`, `unknown`, `Unavailable...`), chat-memory citations, AI/automated attributions, and self-designation or self-approval across the breach recorder, release recorder, suspending operator, and restart proposer.
2. **Criterion 6 (`NFR-014`)**: End-to-end automated unit and drill tests across `src/core` and `src/api` must verify breach-triggered suspension, AI dispatch/proposal containment, manual case fallback continuity, **emergency and statutory Awaab's Law hazard response continuity** on paused scopes, denial of premature/automatic/placeholder/mismatched/self-approved restarts, and clearance only by a distinct authorised human.

### User Decisions and Requirements Highlights

* **Enforce strict `RULE-024` `restart_authority` validation**: Implement a shared, strictly typed `restart_authority` validator in `src/core` and enforce it across `governance.py` (`breach_record`, `breach_restart`) and `continuity.py` (`suspend`, `restart_propose`, `restart_decide`).
* **Preserve immediate emergency containment**: When `restart_authority` is omitted at `continuity.suspend` time (such as an automated harm-threshold breach), `suspend` still succeeds immediately using the canonical `"Unavailable: OD-35 authority unappointed"` sentinel while guaranteeing `restart_propose` and `restart_decide` fail closed until a valid human authority is recorded.
* **Prove `NFR-014` drill end-to-end across `core` and `api`**: Add comprehensive drill tests covering JSON store, SQL store, workflow hazard bypass, and HTTP/assistant continuity without fabricating real human sign-off in `docs/reference/method/operator-suspension-drill-protocol.md`.
* **Local validation and commit only**: Pass `mypy`, `ruff check`, `ruff format --check`, and `unittest` cleanly, then commit locally on `feat/ai-221-operator-suspension-2235` with the Copilot trailer without pushing.

### What You May Not Know

* Earlier work (`b2340f8af`) stamped `restart_rule="RULE-024"` and `automatic_restart=False`, but `continuity.restart_propose` and `continuity.restart_decide` only checked `.startswith("Unavailable")`, allowing explicit placeholders like `"TBD"` or `"none"` or self-emails passed at suspension/breach time to satisfy exact string equality at restart time.
* In `governance.breach_restart`, `different_person` previously checked `b["recorded_by"]` (the breach recorder) without checking `rel["recorded_by"]` (the post-breach `RULE-020` release recorder), allowing one manager to record the post-breach release and approve their own restart.
* Audience-limited projections in `continuity.control_record` and `limited_export` intentionally redact free-text `restart_authority` (verified by a privacy canary in `src/api/tests/test_continuity_epoch_export.py`); that redaction boundary must remain intact.

### Unresolved Decisions or Blockers

* None within software scope. Live operational `OD-35` restart authority appointment and witnessed human execution of `docs/reference/method/operator-suspension-drill-protocol.md` remain human governance prerequisites (`actual_hold=True`) tracked in [Follow-Up Items](#follow-up-items).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for Issue #221 remaining criteria 5 and 6 in worktree `/home/azureuser/source/ama-demo-wt/feat-221-operator-suspension-2235` on branch `feat/ai-221-operator-suspension-2235` targeting `feat/demo-164-chat-grounding-provenance-0900` (caller prompt).
* Criterion 5: Ensure the guardrail breach / incident suspension record explicitly names and validates `restart_authority` per `RULE-024`, requiring a distinct human restart authority and rejecting blank, placeholder, non-human/automatic, and self-approval designations (caller prompt; `docs/brds/agentic-retrofit-programme-brd.md` `RULE-024`, `AC-078`).
* Criterion 6: Add comprehensive unit and drill tests proving the end-to-end suspension, manual fallback continuity (including statutory hazard response), and authorised restart drill per `NFR-014` (caller prompt; `docs/prds/zava-forward-retrofit-programme-demonstrator.md` `FR-053`, `AC-072`, `NFR-014`; `docs/reference/method/operator-suspension-drill-protocol.md`).
* Preserve immediate emergency AI suspension when `restart_authority` is omitted at `continuity.suspend` by recording `"Unavailable: OD-35 authority unappointed"` and failing closed on restart, while never fabricating human completion of the blank drill record in `docs/reference/method/operator-suspension-drill-protocol.md` (research `C4`, `C15`).
* Write all 4 dated RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` (caller prompt).
* Validate `python3 -m mypy` (0 errors), `python3 -m ruff check . && python3 -m ruff format --check .`, and relevant `unittest` suites across `src/core` and `src/api`, then commit cleanly on `feat/ai-221-operator-suspension-2235` with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer without pushing (caller prompt).

## Goals

* Enforce `RULE-024` distinct-human `restart_authority` validation consistently across governance guardrail breach records (`governance.py`) and AI continuity suspension/restart records (`continuity.py`).
* Eliminate placeholder, chat-memory, AI/automated, breach-recorder self-designation, suspender self-designation, proposer self-designation, and release-recorder self-approval loopholes without breaking emergency incident containment or audience-limited privacy redaction.
* Deliver deterministic end-to-end `NFR-014` and `RULE-024` drill test suites in both `src/core` and `src/api` covering suspension, containment, manual case continuity, statutory Awaab's Law hazard continuity on paused scopes, negative restart denials, and distinct authorised human restart.

## Scope and Non-Goals

### In Scope

* Strictly typed `src/core/src/zava_forward/core/restart_authority.py` validation helper for `RULE-024` authority strings and distinct human actor enforcement.
* `RULE-024` wiring in `src/core/src/zava_forward/core/governance.py` (`breach_record`, `breach_restart`) and `src/core/src/zava_forward/core/continuity.py` (`suspend`, `restart_propose`, `restart_decide`).
* Documentation update in `src/core/README.md` describing the strengthened `RULE-024` restart-authority and two-person separation rules.
* Comprehensive unit and end-to-end drill tests in `src/core/tests/test_operator_suspension_drill.py`, `src/core/tests/test_governance.py`, and `src/api/tests/test_operator_suspension.py`.

### Non-Goals

* Fabricating a live human `OD-35` appointment or filling the blank human drill table in `docs/reference/method/operator-suspension-drill-protocol.md`.
* Pushing commits to `origin` or opening/modifying remote pull requests.
* Changing audience-limited free-text redaction in `continuity.control_record` or `limited_export` (free-text `restart_authority` remains protected from non-reason viewers).

## Functional Requirements

* **FR-1 (`RULE-024` Restart Authority Validation on Guardrail Breach Record)**: `governance.breach_record` must require a non-empty human `restart_authority` (<= 200 chars), reject placeholders (`unknown`, `unavailable`, `Unavailable...`, `none`, `null`, `n/a`, `na`, `tbd`, `todo`, `tbc`, `pending`, `placeholder`, `unapproved`, `unappointed`, `unassigned`, `unset`, `default`, `-`, `--`, `?`), reject chat-memory references and AI/automation attributions (`ai`, `bot`, `automation`, `automated`, `automatic`, `copilot`, `llm`, `cron`, `daemon`, `ai assistant`, `ai agent`, `automated system`), reject self-designation matching the recording operator (`email`, `name`, `code`, `oid`, or `self`), and record `restart_rule="RULE-024"`, `automatic_restart=False`, and `actor` identity metadata.
  * Observable acceptance criteria: Recording a guardrail breach with blank, placeholder, `"Unavailable: OD-35 authority unappointed"`, memory-reference, or AI/bot `restart_authority` raises `ValueError`; naming the recording operator raises `PermissionError`; valid human/delegation authority records `restart_authority`, `restart_rule="RULE-024"`, and `automatic_restart=False`.
* **FR-2 (`RULE-024` Distinct Human Enforcement on Guardrail Breach Restart)**: `governance.breach_restart` must refuse truthy/non-false `automatic` flags, verify the authorising manager is distinct from BOTH the breach recorder (`b.get("actor")` and `b.get("recorded_by")`) AND the post-breach `RULE-020` release recorder (`rel.get("recorded_by")`, enriched via `self.staff`), check `authority_ref` non-empty length bounds and absence of chat-memory citations (`ValueError`), enforce `PermissionError` (with non-echoing messages) when stored `b["restart_authority"]` or supplied `authority_ref` is unappointed (`"Unavailable..."`), placeholder, AI/automated, self-designated, or mismatched (`authority_ref != b["restart_authority"]`), reject memory references in `remediation_evidence`, and stamp `restart_rule="RULE-024"` and `automatic_restart=False` on `b["restart"]`.
  * Observable acceptance criteria: Restart attempts by the breach recorder, by the post-breach release recorder, with `automatic=True`, with mismatched or placeholder `authority_ref`, or before a post-breach `Release` raise `PermissionError` (or `ValueError` on blank/memory-reference fields) without echoing confidential `restart_authority` / `authority_ref` values; restart by a distinct manager citing the exact valid `restart_authority` clears the pause and stamps `b["restart"]["restart_rule"] == "RULE-024"`.
* **FR-3 (`RULE-024` Validation on AI Continuity Suspension and Restart)**: `continuity.suspend` must default omitted/`None` `restart_authority` to `"Unavailable: OD-35 authority unappointed"` so immediate emergency containment always succeeds, while rejecting any explicitly supplied blank, placeholder, chat-memory, AI/automated, or suspender-self-designated `restart_authority` without echoing confidential input; `continuity.restart_propose` and `continuity.restart_decide` must refuse `automatic` flags, refuse `"Unavailable..."` or any invalid/placeholder/AI/self-designated `restart_authority` with `PermissionError`, enforce unconditional three-person human separation across suspender (`s.get("actor")`, `s.get("recorded_by")`), proposer (`prop.get("actor")`, `prop.get("by")`), and restart adjudicator (`email`, `name`, `code`, `oid`) for both `"Restart"` and `"Keep suspended"`, require exact `authority_ref == s["restart_authority"]` (`PermissionError`), and stamp `restart_rule="RULE-024"` and `automatic_restart=False` on `rec`.
  * Observable acceptance criteria: `suspend` with omitted `restart_authority` suspends the scope and blocks `restart_propose` and `restart_decide`; `suspend` with explicit `"TBD"`, `"AI bot"`, or suspender identity fails without leaking canary values; `restart_propose` and `restart_decide` reject `automatic=True`, self-approval (including `"Keep suspended"`), and mismatched/placeholder authority (`PermissionError`); distinct OID-bound `ai_restart` human approval succeeds for constructed drill evidence while `actual_hold` remains `True`.
* **FR-4 (`NFR-014` Manual Fallback and Statutory Hazard Continuity Drill)**: Automated end-to-end drill tests in `src/core` and `src/api` must verify the full incident/breach -> containment -> manual fallback -> statutory Awaab's Law hazard progression -> denied premature/unauthorized restarts -> authorised distinct-human restart lifecycle.
  * Observable acceptance criteria: All new and existing `core` and `api` tests pass on both JSON and SQL stores and over the HTTP API harness.

## Non-Functional Requirements

* **NFR-1 (Type Safety and Static Hygiene)**:
  * Objective threshold or evaluation condition: `0` `mypy` errors under `strict = true` and `0` `ruff check` / `ruff format --check` issues across `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Run `python3 -m mypy` and `python3 -m ruff check . && python3 -m ruff format --check .` in `src/core` and `src/api`.
  * Observable acceptance criteria: Clean exit code `0` for `mypy`, `ruff check`, and `ruff format --check` in both packages.
* **NFR-2 (Privacy and Emergency Containment Preservation)**:
  * Objective threshold or evaluation condition: `0` leaks of free-text `restart_authority` to non-reason viewers in `continuity_view`/`limited_export`, and `100%` immediate containment success when `restart_authority` is omitted on harm-threshold breach suspension.
  * Operating condition or verification approach, if needed: Run `test_continuity_epoch_export.py`, `test_rai_harm_threshold_incident.py`, `test_continuity.py`, `test_operator_suspension.py`, `test_governance.py`, and `test_operator_suspension_drill.py`.
  * Observable acceptance criteria: All privacy canary and harm-threshold suspension regression suites pass unchanged.

## Acceptance Criteria

* [x] AC-1 (Issue #221 Criterion 5): Guardrail breach (`governance.breach_record` / `breach_restart`) and incident suspension (`continuity.suspend` / `restart_propose` / `restart_decide`) records explicitly name `restart_authority` with `restart_rule="RULE-024"` and `automatic_restart=False`, rejecting blank, placeholder, chat-memory, AI/automated, and self-approval designations across recorder, suspender, proposer, and post-breach release recorder (including across Entra `TrustedProxyProvider` OID-linked principals via `actors_for_store`).
* [x] AC-2 (Issue #221 Criterion 6 — Core Drill): `src/core/tests/test_operator_suspension_drill.py` and `src/core/tests/test_governance.py` verify end-to-end `RULE-024` + `NFR-014` suspension and guardrail breach pause across JSON and SQL stores, proving paused scopes block AI/routine progression while unaffected manual case work and statutory Awaab's Law hazard response (`raise_hazard`, referral, receipt, acceptance, repair evidence) continue unimpeded on paused homes until distinct human restart clearance.
* [x] AC-3 (Issue #221 Criterion 6 — API Drill): `src/api/tests/test_operator_suspension.py` verifies the end-to-end 8-step `NFR-014` operator suspension, incident snapshot, pending/ready/in-flight containment, manual case & statutory hazard fallback continuity, `"Keep suspended"` retention, negative `RULE-024` restart matrix, and distinct OID-bound `ai_restart` clearance over HTTP and SQL store.
* [ ] AC-4 (Validation & Hygiene): `mypy`, `ruff check`, `ruff format --check`, and `unittest` suites pass with 0 errors in `src/core` and `src/api`, all 4 dated RPI artifacts exist under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/`, and changes are committed cleanly on `feat/ai-221-operator-suspension-2235` without pushing.

## Test Ownership and Critique Lock

* Canonical production targets: `src/core/src/zava_forward/core/restart_authority.py` (new), `src/core/src/zava_forward/core/governance.py`, `src/core/src/zava_forward/core/continuity.py`, `src/core/README.md`
* Generated targets: `none`
* Test ownership targets:
  * `src/core/tests/test_operator_suspension_drill.py` (new strictly typed module; max 12 test methods covering `restart_authority` semantic edge cases + `Store`/`SqlStore` end-to-end `RULE-024` & `NFR-014` drill with statutory hazard continuity)
  * `src/core/tests/test_governance.py` (existing `GovMixin`; max 3 focused test methods covering `breach_record` / `breach_restart` `RULE-024` negative matrix and release-recorder separation on both `JsonGov` and `SqlGov`)
  * `src/api/tests/test_operator_suspension.py` (existing strictly typed HTTP/SQL suite; update `test_nfr_014_suspension_and_manual_fallback_drill` and add max 2 focused test methods covering HTTP `RULE-024` placeholder/AI/self-designation rejection and full statutory hazard referral continuity during suspension)
* Exact test removals: `none`
* Semantic vs. regression coverage:
  * Semantic coverage: new tests assert `RULE-024` authority rejection/acceptance, three-actor separation, `"Keep suspended"` retention, and end-to-end `NFR-014` manual + statutory hazard fallback continuity during active guardrail/continuity pauses.
  * Regression coverage: existing `test_governance.py`, `test_continuity.py`, `test_continuity_epoch_export.py`, `test_rai_harm_threshold_incident.py`, and `test_operator_suspension.py` confirm zero regressions in emergency containment, audience-limited redaction, and ledger verification.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md                                                            |
| Phase details                    | .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md                                                 |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/issue-221-operator-suspension-2235-plan-critique.md with Revise disposition resolved across PC-001..PC-004 |
| Relevant research                | .copilot-tracking/research/2026-11-14/issue-221-operator-suspension-2235-research.md                                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/issue-221-operator-suspension-2235-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                       |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions to Implement (`rpi-implement`) automatically                                    |

## Sources

* `.copilot-tracking/research/2026-11-14/issue-221-operator-suspension-2235-research.md`: Primary codebase and specification evidence (`C1`-`C16`) and convergence design.
* `docs/brds/agentic-retrofit-programme-brd.md`: Authoritative `RULE-024`, `RULE-020`, `AC-078`, and `OD-35` guardrail breach and restart authority requirements.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Authoritative `FR-053`, `FR-028`, `AC-072`, and `NFR-014` operator suspension, manual fallback, and restart drill requirements.
* `docs/reference/method/operator-suspension-drill-protocol.md`: Canonical 8-step synthetic drill protocol and governance boundary prohibiting fabricated human sign-off.
* `src/core/src/zava_forward/core/governance.py` and `src/core/src/zava_forward/core/continuity.py`: Existing guardrail breach and AI task continuity control implementations.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement RULE-024 Restart Authority Validation in Core

* Intent: Enforce distinct human `restart_authority` validation and multi-person restart separation across `restart_authority.py`, `governance.py`, and `continuity.py` while preserving immediate emergency suspension and privacy redaction.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Create strictly typed `restart_authority.py` validator module

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1; research `C1`, `C4`, `C8`, `C9`, `C16`
* Expected result: `src/core/src/zava_forward/core/restart_authority.py` defines `UNAPPOINTED_RESTART_AUTHORITY`, `RULE_024`, `reject_automatic_restart`, `validate_restart_authority`, and `ensure_distinct_restart_actor` with full strict type annotations, rejecting blank, placeholder, `"Unavailable..."` (unless explicitly permitted for default containment), chat-memory, AI/automation, and disallowed-actor self-designation strings without false positives on human job titles.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce RULE-024 authority and actor separation in `governance.py` and `continuity.py`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-2; research `C5`, `C6`, `C7`, `C14`, `C15`
* Expected result: `governance.breach_record` and `breach_restart` reject invalid/placeholder/AI/self-designated `restart_authority`, enforce distinct breach-recorder, release-recorder, and restart-authoriser identities, reject memory citations in `remediation_evidence`, and stamp `restart_rule="RULE-024"` and `automatic_restart=False`; `continuity.suspend`, `restart_propose`, and `restart_decide` preserve omitted-authority containment while rejecting invalid explicit `restart_authority`, `automatic` flags, and suspender/proposer self-designation or self-approval, and update `src/core/README.md`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Add Comprehensive RULE-024 & NFR-014 End-to-End Drill Tests and Validate

* Intent: Prove Criterion 5 and Criterion 6 across `src/core` (JSON & SQL stores + workflow statutory hazard bypass) and `src/api` (HTTP + assistant continuity + statutory hazard response) and pass all static and runtime checks.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add `src/core` RULE-024 unit tests and end-to-end NFR-014 guardrail/continuity drill suite

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, AC-1, AC-2; research `C1`, `C2`, `C4`, `C10`, `C12`
* Expected result: `src/core/tests/test_operator_suspension_drill.py` (strictly typed) and `src/core/tests/test_governance.py` verify `restart_authority` validation edge cases, breach/release/restart three-person separation, and the full end-to-end `NFR-014` drill on `Store` and `SqlStore` including manual fallback on unaffected scopes and statutory Awaab's Law hazard workflow progression on a breach-paused and AI-suspended home.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Strengthen `src/api` HTTP end-to-end NFR-014 operator suspension and fallback drill tests and run full validation

* Requirement and evidence: FR-3, FR-4, NFR-1, NFR-2, AC-3, AC-4; research `C2`, `C4`, `C11`, `C13`, `C14`, `C15`, `C16`
* Expected result: `src/api/tests/test_operator_suspension.py` exercises the complete 8-step `NFR-014` HTTP/service drill (breach suspension, snapshot completeness, pending/ready/in-flight containment, manual call + statutory hazard referral/acceptance continuity, `"Keep suspended"` retention, HTTP 400/403 `RULE-024` negative matrix, and distinct OID-bound `ai_restart` approval), and `mypy`, `ruff check`, `ruff format --check`, and `unittest` pass with 0 errors across `src/core` and `src/api`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md

## Dependencies

* `src/core/src/zava_forward/core/controls.py`: Provides `is_memory_reference` and `different_person` primitives reused alongside `restart_authority.py`.
* `src/core/src/zava_forward/core/workflows.py`: Provides `raise_hazard`, `log_call`, and hazard referral/acceptance routes exercised during the `NFR-014` fallback drill to verify statutory hazard continuity during active pauses.
* Worktree `PYTHONPATH` execution order: Tests and linters must target this worktree's `src/` directories (`PYTHONPATH=src:tests` in `src/core` and `PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests` in `src/api`) rather than editable installs from sibling checkouts.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High]: Wrong suspension actor field (`s.get("by")`), `or` short-circuiting on partial `actor` dicts, and gated `"Keep suspended"` actor separation | resolved | Updated `FR-2`, `FR-3`, and `P01-T02` to pass non-short-circuiting prior-actor sequences (`s.get("actor")` and `s.get("recorded_by")`; `prop.get("actor")` and `prop.get("by")`; `b.get("actor")`, `b.get("recorded_by")`, and `self.staff`-enriched `rel.get("recorded_by")`), and to enforce `ensure_distinct_restart_actor` unconditionally in `continuity.restart_decide` for both `"Restart"` and `"Keep suspended"`. |
| `PC-002` [High]: `PermissionError` exception contract and privacy-canary echo hazard in `validate_restart_authority`, `restart_decide`, and `breach_restart` | resolved | Updated `FR-2`, `FR-3`, `P01-T01`, and `P01-T02` so `restart_authority.py` uses static non-echoing `label`/`RULE-024` messages that never interpolate raw `value` or actor PII, and `restart_decide` / `breach_restart` raise `ValueError` only for blank/overlong/memory-reference fields while raising `PermissionError` for non-blank unappointed (`"Unavailable..."`), placeholder, AI/automated, self-designated, or mismatched `authority_ref` and stored `restart_authority`. |
| `PC-003` [Medium]: `P02-T01` `"CM-101"` fails `controls.MEMORY_REF`, and `P01-T01` exact-only matching misses composite placeholders and embedded actor `name`/`code` | resolved | Updated `P01-T01` to match actor `code` and `name` (`len >= 3`) on case-insensitive alphanumeric boundaries and unambiguous composite placeholder words/phrases (`tbd`, `todo`, `tbc`, `placeholder`, `unappointed`, `unassigned`, `unapproved`, `same operator`, `same person`) on word boundaries, and updated `P02-T01` to test valid `controls.MEMORY_REF` inputs (`"CM-0123456789ab"`, `"memory:thread-1"`, `"chat-memory"`). |
| `PC-004` [Medium]: `P02` drill tasks omit `drill(self)` open-suspension collision, `App` auth-provider split, post-breach `Release` prerequisite, hazard-hold interaction, and full `src/api` test discovery | resolved | Updated `P02`, `P02-T01`, and `P02-T02` to type store helpers with `typing.Any` in `test_operator_suspension_drill.py` (leaving `src/core/pyproject.toml` untouched), verify `log_call` (plus `record_repair` + independent `release_hazard` before `advance`) after `breach_restart`, execute the 8-step HTTP `NFR-014` drill on a clean `Base` fixture (with `drill(self)` retained in `test_incident_snapshot_and_reopen`), record a post-breach `Release` (`scope_kind="tranche"`) before `/api/governance/restart` with explicit `PasswordProvider`/`TrustedProxyProvider` routing, and run full `unittest discover -s tests` in both `src/core` and `src/api`. Accepted residual risk: live human `OD-35` appointment and witnessed protocol completion remain human governance prerequisites outside software scope. |

## Follow-Up Items

* **Live operational OD-35 appointment and witnessed human drill record**: Outside immediate software scope because `docs/reference/method/operator-suspension-drill-protocol.md` forbids agents from fabricating real human `OD-35` appointments or witnessing live operational drills; owned by Building Safety Lead, Executive Sponsor, and Project Owner before operational pilot release (`actual_hold=True` remains enforced in software).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/issue-221-operator-suspension-2235-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none
