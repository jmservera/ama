<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #221 Operator Suspension, Incident and Restart Record (Criteria 5 & 6)

## Metadata

* Task ID: issue-221-operator-suspension-2235
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Close the two remaining unticked software acceptance criteria on Issue #221 in worktree `feat-221-operator-suspension-2235` on branch `feat/ai-221-operator-suspension-2235` without pushing: (1) Criterion 5 (`RULE-024`) requiring guardrail breach and incident suspension records to explicitly name and validate a distinct human `restart_authority` while rejecting blank, placeholder, non-human/automatic, and self-approval designations; (2) Criterion 6 (`NFR-014`) adding comprehensive unit and drill tests proving end-to-end suspension, manual fallback continuity (including statutory hazard response), and authorised restart; and (3) producing all 4 dated RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/`, passing `mypy`, `ruff check`, `ruff format --check`, and `unittest` across `src/core` and `src/api`, and committing cleanly without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-14/issue-221-operator-suspension-2235-research.md`, `.copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md`, `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md`, `src/core/src/zava_forward/core/governance.py`, `src/core/src/zava_forward/core/continuity.py`, `src/core/src/zava_forward/core/controls.py`, `src/core/src/zava_forward/core/workflows.py`, `src/core/pyproject.toml`, `src/core/tests/test_governance.py`, `src/api/tests/test_operator_suspension.py`, `src/api/tests/test_continuity_epoch_export.py`, `src/api/tests/test_rai_harm_threshold_incident.py`, and `docs/reference/method/operator-suspension-drill-protocol.md`.
* Decisions, dependencies, and acceptance criteria considered: `FR-1` through `FR-4`, `NFR-1` through `NFR-2`, `AC-1` through `AC-4`, `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), emergency omitted-authority containment (`UNAPPOINTED_RESTART_AUTHORITY`), audience-limited privacy redaction (`control_record` and `limited_export`), and the governance boundary keeping `docs/reference/method/operator-suspension-drill-protocol.md` human-completed (`actual_hold=True`).
* Assessment boundary: Evaluates plan and phase-detail accuracy, type/lint compatibility, behavioral invariants, and test-harness preconditions against the supplied source and test files. Does not evaluate live human `OD-35` appointment or external hosted CI execution, which are explicitly out of scope for this local branch task.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / FR-1 / FR-2 (`RULE-024` governance breach & restart) | Partial | Core module design covers `breach_record` and `breach_restart`, but `P01-T01` and `P01-T02` have `or` short-circuiting on actor dicts, email-only `rel["recorded_by"]` lookup, `PermissionError` vs `ValueError` mismatch on `authority_ref`, and exact-only name/code/placeholder checks (`PC-001`, `PC-002`, `PC-003`). |
| Caller Req 1 / FR-3 (`RULE-024` AI continuity suspend, propose & decide) | Partial | Preserves omitted-authority emergency containment (`C4`, `C15`), but `P01-T02` references nonexistent `s.get("by")` instead of `s.get("recorded_by")`, gates `ensure_distinct_restart_actor` on `decision == "Restart"` (regressing `"Keep suspended"` separation), and risks `ValueError`/canary-echo regressions (`PC-001`, `PC-002`). |
| Caller Req 2 / FR-4 / AC-2 (`NFR-014` core drill & statutory hazard continuity) | Partial | Covers `Store`, `SqlStore`, and `workflows` statutory hazard bypass (`C10`), but `P02-T01` tests `"CM-101"` which fails `controls.MEMORY_REF` (`{12,}` hex digits) and omits unreleased safety-hold interaction with post-restart progression (`PC-003`, `PC-004`). |
| Caller Req 2 / FR-4 / AC-3 (`NFR-014` API 8-step drill) | Partial | Covers the 8-step protocol (`C4`, `C13`), but `P02-T02` does not account for `drill(self)` leaving 5 open suspensions, single-provider `App` auth split (`PasswordProvider` vs `TrustedProxyProvider`), and post-breach `Release` prerequisite for `/api/governance/restart` (`PC-004`). |
| Caller Req 3 / NFR-1 / NFR-2 / AC-4 (Static checks, privacy, artifacts & local commit) | Partial | `mypy --strict`, `ruff`, privacy redaction, 4 RPI artifact paths, and no-push local commit are covered, except `plan.md` omits `src/core/pyproject.toml` from its target list, `P01-T01` must forbid echoing canary text in error messages, and `P02` omits full `src/api` `unittest discover` (`PC-002`, `PC-004`). |
| P01-T01 (`restart_authority.py` validator) | Partial | Typed module structure and `controls.is_memory_reference` typed reuse are sound; needs non-echoing exception text and token/boundary checks for composite placeholders and actor `name`/`code` (`PC-002`, `PC-003`). |
| P01-T02 (`governance.py` and `continuity.py` wiring) | Partial | Needs `s.get("recorded_by")` fix, non-short-circuiting actor lists with `self.staff` resolution, unconditional `restart_decide` actor separation, and `PermissionError` preservation for invalid non-blank `authority_ref` (`PC-001`, `PC-002`). |
| P02-T01 (`src/core` unit & drill tests) | Partial | Needs valid 12+ hex `CM-...` memory-reference test input and explicit post-restart progression check (`log_call` or `record_repair` + `release_hazard` before `advance`) (`PC-003`, `PC-004`). |
| P02-T02 (`src/api` HTTP drill & validation) | Partial | Needs clean fixture isolation from `drill(self)`, explicit post-breach `Release` step before `/api/governance/restart`, dual-provider auth handling, and full `src/api` test discovery (`PC-004`). |

## Verdict

* Verdict: Revise
* Rationale: The candidate architecture and convergence approach are strong, well-scoped, and properly preserve emergency containment (`UNAPPOINTED_RESTART_AUTHORITY`), human job titles (`"Assistant Director..."`), and the `OD-35` non-fabrication boundary. However, four concrete defects verified directly against the supplied source and test files (`PC-001` through `PC-004`, two High and two Medium) would cause actor-lookup misses, weaken `"Keep suspended"` separation, risk privacy-canary or `PermissionError` regressions, or break planned unit/HTTP drill tests if implemented verbatim. All four findings are direct planner corrections requiring zero user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Wrong suspension actor field (`s.get("by")`), `or` short-circuiting on partial `actor` dicts, and weakened `"Keep suspended"` actor separation in P01-T02

* Related IDs: FR-2, FR-3, AC-1, P01-T01, P01-T02; research C5, C6
* Evidence: `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md` (P01-T02, lines 130, 134, 137); `src/core/src/zava_forward/core/continuity.py:456,466,502,528-534`; `src/core/src/zava_forward/core/governance.py:508,553,571`
* Concern: `P01-T02` introduces three actor-separation defects: (1) it references `s.get("actor") or s.get("by")` for the suspending operator, whereas `continuity.suspend` stores `s["recorded_by"]` (`continuity.py:456`) and never `s["by"]`; (2) `s.get("actor") or s.get("recorded_by")` and `b.get("actor") or b.get("recorded_by")` short-circuit whenever `actor` is a truthy dict (ignoring `recorded_by` on pre-change or partial records where `actor` lacks `name` or `email`), while `rel.get("recorded_by")` in `governance.release_record` (`governance.py:508`) is only an email string without `name`/`code`/`oid` unless enriched via `self.staff`; and (3) `P01-T02` restricts `ensure_distinct_restart_actor` in `continuity.restart_decide` to `when decision == "Restart"`, weakening existing `continuity.py:528-533` where distinct-person checks run unconditionally before `decision` branching so neither suspender nor proposer can adjudicate and clear `s["proposal"]` via `"Keep suspended"`.
* Impact: Suspender separation fails on legacy/constructed records without `s["actor"]`, partial `actor` dicts skip `recorded_by` fallback, release-recorder separation checks only email unless resolved through `self.staff`, and gating separation on `decision == "Restart"` regresses the existing three-person control on `"Keep suspended"` decisions.
* Smallest useful change: Update `P01-T02` so `continuity.restart_propose` and `continuity.restart_decide` pass `s.get("actor")` and `s.get("recorded_by")` (plus `prop.get("actor")` and `prop.get("by")` in `restart_decide`) as separate sequence items rather than `or` expressions; `governance.breach_restart` passes `b.get("actor")`, `b.get("recorded_by")`, and `self.staff`-resolved `rel.get("recorded_by")`; and `continuity.restart_decide` enforces `ensure_distinct_restart_actor` unconditionally for both `"Restart"` and `"Keep suspended"`, stamping `restart_rule="RULE-024"` and `automatic_restart=False` on `rec`.
* Action owner: planner
* Exact resolving evidence: Revised `P01-T02` in `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md` specifying `s.get("recorded_by")`, non-short-circuiting prior-actor tuples with `self.staff` lookup for email-only records, and unconditional `ensure_distinct_restart_actor` execution in `continuity.restart_decide`.
* Decision route: Direct planner correction; planner can apply directly without user input.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `PermissionError` exception contract and privacy-canary leak hazard in `validate_restart_authority`, `restart_decide`, and `breach_restart`

* Related IDs: FR-2, FR-3, NFR-2, AC-1, P01-T01, P01-T02; research C6, C7, C14
* Evidence: `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md` (P01-T01 lines 90-100, P01-T02 lines 130-138); `src/core/src/zava_forward/core/continuity.py:372,534-536`; `src/core/src/zava_forward/core/governance.py:575-577`; `src/api/tests/test_continuity_epoch_export.py:1079-1113`; `src/api/tests/test_operator_suspension.py:678-684`
* Concern: Two contract hazards arise in `P01-T01` and `P01-T02`: (1) in `continuity.py:534-536`, blank `authority_ref` raises `ValueError` (HTTP 400), while `authority.startswith("Unavailable")` or `authority != s.get("restart_authority")` raises `PermissionError` (HTTP 403); calling `validate_restart_authority(body.get("authority_ref"), ...)` directly in `restart_decide` (and `breach_restart`) raises `ValueError` instead of `PermissionError` for non-blank `"Unavailable..."`, placeholder, or AI `authority_ref` strings, altering the exception and HTTP status contract expected by restart-decision callers; and (2) `test_continuity_epoch_export.py:1080-1113` places a privacy canary (`"SYNTHETIC-MUTATION-PRIVATE-122"`) in `restart_authority` and `authority_ref` and asserts `self.assertNotIn(canary, json.dumps(decided))` on HTTP error responses while `continuity.py:372` persists `str(error)[:400]` to the audit log on denials, yet `P01-T01` does not prohibit echoing the supplied `value` or actor identifiers in exception messages.
* Impact: Echoing input strings in `ValueError` or `PermissionError` messages leaks protected `restart_authority` / `authority_ref` values into HTTP error responses and immutable denial audit logs (violating `NFR-2`), and raising `ValueError` instead of `PermissionError` on `"Unavailable..."` or invalid non-blank `authority_ref` breaks the existing `restart_decide` `PermissionError` contract.
* Smallest useful change: Specify in `P01-T01` that `validate_restart_authority` and `ensure_distinct_restart_actor` use static `label` and `RULE-024` error messages that never interpolate raw `value` or actor PII, and specify in `P01-T02` that `restart_decide` and `breach_restart` validate non-empty string bounds (`1..200`) and chat-memory absence as `ValueError` first, then translate unappointed (`"Unavailable..."`), placeholder, AI/automated, self-designated, or mismatched `authority_ref` (and stored `restart_authority`) failures into `PermissionError`.
* Action owner: planner
* Exact resolving evidence: Revised `P01-T01` and `P01-T02` in `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md` requiring non-echoing exception messages and `PermissionError` enforcement for non-blank invalid/unappointed `authority_ref` in `restart_decide` and `breach_restart`.
* Decision route: Direct planner correction; planner can apply directly without user input.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P02-T01` memory-reference test input `"CM-101"` fails `controls.MEMORY_REF`, and `P01-T01` exact-only matching misses embedded actor `name`/`code` and composite placeholders

* Related IDs: FR-1, FR-3, AC-1, AC-2, P01-T01, P02-T01; research C8, C9
* Evidence: `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md` (P01-T01 lines 93-99, P02-T01 line 197); `src/core/src/zava_forward/core/controls.py:49-54`
* Concern: (1) `controls.MEMORY_REF` (`controls.py:49`) matches `CM-[0-9a-f]{12,}`, `memory:(?=\S)`, or `chat-memory`, requiring at least 12 hex characters after `CM-`; `P02-T01` specifies `"CM-101"` as its memory-reference test case, for which `controls.is_memory_reference("CM-101")` returns `False`. (2) `P01-T01` matches actor `name` and `code` only as exact whole strings (using substring checks only for `email` and `oid`) and matches placeholders (`tbd`, `todo`, `unappointed`, etc.) only as exact whole strings plus `startswith("unavailable")`, allowing composite strings like `"Alex Rivera (OD-35)"`, `"Approved by QI-1"`, `"OD-35: TBD"`, or `"Unappointed: awaiting sponsor"` to bypass `RULE-024`.
* Impact: `RestartAuthorityRule024Tests` in `P02-T01` will fail immediately on `"CM-101"`, and realistic composite self-designation or placeholder strings slip past `validate_restart_authority`.
* Smallest useful change: Update `P01-T01` so non-empty actor `code` and `name` (length >= 3) are checked on case-insensitive alphanumeric boundaries (`(?<![A-Za-z0-9])...(?![A-Za-z0-9])`) alongside `email`/`oid` substring matching, and unambiguous placeholder tokens/phrases (`tbd`, `todo`, `tbc`, `placeholder`, `unappointed`, `unassigned`, `unapproved`, `same operator`, `same person`) are checked on word boundaries alongside exact-match short forms (`unknown`, `none`, `null`, `n/a`, `na`, `pending`, `unset`, `default`, `self`, `-`, `--`, `?`) and `startswith("unavailable")` (preserving `"OD-35 demo"`, `"Delegation ref D-1"`, `"Constructed fixture authority, not OD-35 appointment"`, and `"SYNTHETIC-MUTATION-PRIVATE-122"`). Update `P02-T01` to test valid `controls.MEMORY_REF` citations (`"CM-0123456789ab"`, `"memory:thread-1"`, `"chat-memory"`).
* Action owner: planner
* Exact resolving evidence: Revised `P01-T01` boundary-matching rules and revised `P02-T01` memory-reference test inputs in `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md`.
* Decision route: Direct planner correction; planner can apply directly without user input.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `P02` drill tasks omit `drill(self)` open-suspension collision, `App` single-provider auth split, post-breach `Release` prerequisite, hazard-hold interaction, and full `src/api` test discovery

* Related IDs: FR-4, AC-2, AC-3, AC-4, P02, P02-T01, P02-T02; research C10, C11, C12, C13, C16
* Evidence: `.copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md` (lines 64-70, 119-135); `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md` (P02 lines 171-173, P02-T01 lines 194-205, P02-T02 lines 224-239); `src/api/tests/test_operator_suspension.py:362-375,595-607,783-853`; `src/core/src/zava_forward/core/governance.py:572-574`; `src/core/src/zava_forward/core/workflows.py:391-490`
* Concern: Four test-execution and plan-alignment details are missing or conflicting across `plan.md` and `phase-details.md`: (1) `test_nfr_014_suspension_and_manual_fallback_drill` (`test_operator_suspension.py:595`) currently calls `drill(self)`, which leaves 5 open suspensions including `"all"` and `CAP` (`lines 362-370`), so appending an 8-step HTTP `/api/continuity/suspend` sequence after `drill(self)` will fail with `"This scope is already suspended"`, whereas `test_incident_snapshot_and_reopen` (`line 605`) already executes `drill(self)`; (2) `P02-T02` calls `/api/continuity/restart-decide` (requiring `TrustedProxyProvider` for 200 and `PasswordProvider` for untrusted-route 403, `lines 808-853`) and `/api/governance/restart` (which requires a post-breach `Release` decision recorded by a manager distinct from both breach recorder and restart authoriser, `governance.py:572-574`) without specifying those prerequisites; (3) in `P02-T01` step 4/6, raising an unreleased safety hazard places an active home retrofit safety hold (`workflows.py:391`), so step 6 must either assert `log_call` (gated by `guard_case_event`) or complete `record_repair` + independent `release_hazard` before asserting `advance`; and (4) `P02` Validation Expectations runs only 4 modules in `src/api` rather than full `unittest discover -s tests`, and `plan.md` omits `src/core/pyproject.toml` (modified in `P02-T01` for `disallow_untyped_calls = false`) from its target lists and impact classification note.
* Impact: Implementing `P02-T01` and `P02-T02` without these explicit preconditions risks fixture collisions on `"already suspended"`, 403 failures on `/api/governance/restart`, safety-hold interference after `breach_restart`, incomplete `src/api` regression execution, and target-list drift between `plan.md` and `phase-details.md`.
* Smallest useful change: Update `P02`, `P02-T01`, and `P02-T02` in `phase-details.md` and `In Scope` / `Test Ownership and Critique Lock` in `plan.md` to: (a) run the 8-step HTTP/service `NFR-014` drill directly on a clean `Base` fixture in `test_nfr_014_suspension_and_manual_fallback_drill` (noting `test_incident_snapshot_and_reopen` retains `drill(self)` coverage); (b) include a post-breach `Release` (`scope_kind="tranche"` by `self.pm`) before `/api/governance/restart` (by `Programme Support Officer`) and explicit `PasswordProvider` vs `TrustedProxyProvider` request routing; (c) specify `log_call` (or `record_repair` + independent `release_hazard` before `advance`) for post-restart home progression in `P02-T01`; and (d) list `src/core/pyproject.toml` (focused-tier test-override impact only, no dependency/gate change) in `plan.md` and include full `unittest discover -s tests` in `src/api` validation.
* Action owner: planner
* Exact resolving evidence: Revised `P02`, `P02-T01`, and `P02-T02` in `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md` and aligned target/validation entries in `.copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md`.
* Decision route: Direct planner correction; planner can apply directly without user input.

## Strengths and Residual Risk

* Strong contrarian preservation of immediate emergency containment: keeping `UNAPPOINTED_RESTART_AUTHORITY` when `restart_authority` is omitted at `continuity.suspend` while failing closed at `restart_propose` and `restart_decide` protects live harm-threshold containment (`test_rai_harm_threshold_incident.py:55-71`) and Drill Protocol step 2.
* Careful avoidance of false positives on human housing-association job titles (`"Assistant Director of Assets"`, `"Building Safety Services Lead"`) instead of copying `rai_release.NON_HUMAN_TOKENS` verbatim.
* Honest governance boundary: synthetic fixture drills verify software controls (`RULE-024`, `FR-053`, `AC-072`, `NFR-014`) while keeping `actual_hold=True` and leaving `docs/reference/method/operator-suspension-drill-protocol.md` untouched for human `OD-35` appointment and witnessed drill completion.
* Residual risk (explicitly accepted in plan Follow-Up Items): live operational `OD-35` appointment and witnessed human completion of `docs/reference/method/operator-suspension-drill-protocol.md` remain human governance gates outside software scope.

## Questions or Blocking Evidence Gaps

* None. All supplied requirements, source modules, and test suites are sufficient to resolve `PC-001` through `PC-004` directly in planning.

## Limitations

* Assessment was strictly bounded to the caller-supplied research, plan, phase details, and named source/test files without open-ended repository exploration or test execution during critique.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planner
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md` and `.copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md` to apply `PC-001`, `PC-002`, `PC-003`, and `PC-004`, record their disposition in `Critique Disposition`, and finalize the plan for `rpi-implement` without another critique pass.
* User response required: no
