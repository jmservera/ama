<!-- markdownlint-disable-file -->
# Review: Issue #220 Affected-Person Challenge and Correction Route Safeguards

## Scope and Evidence

* Task ID: issue-220-criterion-5-affected-person-challenge-2305
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Locally verifiable `src/core` non-retaliation, non-inferred-refusal, and non-delayed-hazard-response acceptance criterion for Issue #220 across `zava_forward.core.challenges`, `zava_forward.core.resident_decisions` (`Store` and `SqlStore`), `src/core/tests/test_issue_220_challenge_route.py`, and `src/core/README.md`; excludes `src/api` web panel wiring, live operational resident/staff acceptance audits, owner `max_days` policy approval, and remote git push per caller instructions.
* Plan: .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/220-affected-person-challenge-2305-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/220-affected-person-challenge-2305-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/220-affected-person-challenge-2305-research.md (`C1`-`C12`), `git diff src/` across `src/core/src/zava_forward/core/{challenges,resident_decisions}.py` and `src/core/README.md`, `src/core/tests/test_issue_220_challenge_route.py`, and targeted `mypy`, `ruff`, and `unittest` execution in `src/core`.

## Opening Review State

* Interpreted review goal: Verify that the completed `src/core` implementation satisfies `FR-1`..`FR-5`, `NFR-1`, `NFR-2`, `AC-1`..`AC-6`, and critique dispositions `PC-001`..`PC-003` for Issue #220 Criterion 5 without modifying `pyproject.toml` or introducing `.copilot-tracking/` references into `src/`.
* Review scope: Full task (`P01` and `P02`)
* Evidence readiness: Ready; research, finalized plan, phase details, single-pass critique, changes log, source diffs, and targeted validation outputs are complete and reconciled.
* Acceptance basis: Plan `FR-1`..`FR-5`, `NFR-1`, `NFR-2`, `AC-1`..`AC-6`, Critique Dispositions (`PC-001`..`PC-003`), and caller targeted `mypy`/`ruff`/`unittest` verification constraints.
* First comparison boundary: Plan checklist markers and critique dispositions (`PC-001`..`PC-003`) against `challenges.py` and `resident_decisions.py` diffs.
* Active read-only boundaries: Read-only inspection across repository sources and prior RPI artifacts; writes restricted exclusively to `.copilot-tracking/reviews/logs/2026-11-14/220-affected-person-challenge-2305-review.md`.
* Initial blockers: none.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation comparison on 2026-11-14 across all planned markers (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`), critique dispositions (`PC-001`..`PC-003`), `src/` diffs, and fresh targeted `src/core` validation outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| `P01`, `P01-T01` | Store-Independent Challenge Register Lifecycle and Safeguard Invariants | Reconciled | `[x]` in plan, `complete` in phase details, and backed by `challenges.py` diff |
| `P01`, `P01-T02` | Store-Backed Affected-Person Challenge Lifecycle and Transactional Safeguards | Reconciled | `[x]` in plan, `complete` in phase details, and backed by `resident_decisions.py` diff |
| `P02`, `P02-T01` | Deterministic Challenge Route Safeguard Unit Suite | Reconciled | `[x]` in plan, `complete` in phase details, and backed by `test_issue_220_challenge_route.py` (`28` total tests passing with `test_challenges.py`) |
| `P02`, `P02-T02` | Component Documentation and Targeted Validation | Reconciled | `[x]` in plan, `complete` in phase details, and backed by `src/core/README.md` diff and `mypy`/`ruff`/`unittest` zero-exit run |
| `Follow-Up Items` | `src/api` web panel exposure and human operational governance sign-off (`max_days`, live workflow acceptance) | Reconciled | Preserved outside active `Pxx` completion claims in both plan and changes record |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| `P01-T01` | `src/core/src/zava_forward/core/challenges.py` | Added `"human_decision"` to `SUBJECT_KINDS` and `"escalated"` to `STATUSES`; added `ChallengeRegister.update(...)`, `ChallengeRegister.escalate(...)`, `ChallengeSafeguardError`, `FORBIDDEN_ADVERSE_FIELDS`, `SAFEGUARDS`, `reject_adverse_mapping`, and `assert_no_adverse_challenge_effects`; filtered `permitted=True` explanations inside `updates` in `view(cid)` (`PC-002`) and unconditionally preserved `received_on` including `None` on active `referred_on_receipt` hazard referrals (`PC-003`) | Verified in `git diff src/core/src/zava_forward/core/challenges.py` | Passed (`mypy`, `ruff`, `test_challenges.py`, `ChallengeRegisterLifecycleAndSafeguardsTests`) | Reconciled and conformant |
| `P01-T02` | `src/core/src/zava_forward/core/resident_decisions.py` | Added `target_kind == "human_decision"` dependency binding and exact staleness derivation in `_dependency` and `priority_challenge_state`; registered `"challenge_update"` and `"challenge_escalate"` in `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS` for `validate_sql` replay; implemented `_res_challenge_update` and `_res_challenge_escalate`; made `_res_challenge_resolve` monotonic (`record["version"] + 1`); enforced pre-schema `reject_adverse_mapping` (`PC-001`) and post-mutation `assert_no_adverse_challenge_effects` | Verified in `git diff src/core/src/zava_forward/core/resident_decisions.py` | Passed (`mypy`, `ruff`, `JsonStoreChallengeSafeguardTests`, `SqlStoreChallengeSafeguardTests`) | Reconciled and conformant |
| `P02-T01` | `src/core/tests/test_issue_220_challenge_route.py` | Created strictly typed deterministic safeguard unit suite (9 test methods across `ChallengeRegister`, JSON `Store`, and SQLite `SqlStore`) proving zero retaliation/ranking penalties, zero inferred refusals, zero statutory/safety hazard clock or emergency response delays, and fail-closed `ChallengeSafeguardError` rejection across `source`, `policy`, `proposal`, and `human_decision` targets and all digital/non-digital channels | Verified in `src/core/tests/test_issue_220_challenge_route.py`; existing 19 tests in `test_challenges.py` preserved untouched | Passed (`28` tests in `1.212s`, `mypy`, `ruff`) | Reconciled and conformant |
| `P02-T02` | `src/core/README.md` | Updated `#version-bound-affected-person-challenges-220` and `## Affected-person challenge and correction route (#220)` to document expanded `src/core` controls, `test_issue_220_challenge_route.py`, and remaining human governance boundaries | Verified in `git diff src/core/README.md`; zero `.copilot-tracking/` references in `src/`; `pyproject.toml` untouched | Passed (`mypy`, `ruff check .`, `ruff format --check .`, targeted `unittest`) | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| `P01-T01` (`assert_no_adverse_challenge_effects`) | Local compatibility refinement: scanned `after_case["affected_challenges"]` recursively for `FORBIDDEN_ADVERSE_FIELDS` while enforcing top-level adverse-field prohibition and full non-`affected_challenges` top-level case equality so pre-existing legitimate `sensors[...]["consent"]` fields never false-positive | `sensor_view.py` and `sensor_consumer.py` store `"consent"` inside `case["sensors"]`; no user decision needed (local judgment preserving approved intent) | Recorded in `.copilot-tracking/changes/2026-11-14/220-affected-person-challenge-2305-changes.md` and verified by dedicated subtest in `test_issue_220_challenge_route.py` | Ready; `PC-001`..`PC-003` fully satisfied | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three findings from `.copilot-tracking/critiques/2026-11-14/220-affected-person-challenge-2305-critique.md` (`PC-001` High on full non-`affected_challenges` case immutability, recursive `affected_challenges` adverse-key inspection, and pre-schema `ChallengeSafeguardError` rejection in `_res_challenge_*`; `PC-002` Medium on filtering `permitted=True` explanations inside `rec["updates"]` in `ChallengeRegister.view(cid)`; and `PC-003` Low on unconditional preservation of `received_on` including `None` on active `referred_on_receipt` hazard referrals) were applied directly in the plan/details, implemented in `challenges.py` and `resident_decisions.py`, and proven by dedicated unit assertions in `test_issue_220_challenge_route.py`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No pause was needed; `P02` executed cleanly after `P01` completed.
* Justification assessment: Supported by direct source diffs and deterministic unit evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Expose `challenge_update`, `challenge_escalate`, and `target_kind="human_decision"` in `src/api/src/zava_forward/api/web/panels.js` | Caller scoped this task strictly to `src/core`; web changes require a separate `src/api` slice under `web-design-guidelines` and browser harness validation | Separate `src/api` web delivery slice | Open outside-scope follow-up; routed to distinct follow-up item (not a defect) |
| Live operational resident/staff acceptance evidence and owner-approved `max_days` hazard follow-up threshold (#220) | Human governance, comprehension sign-off, and live operational workflow comparison cannot be fabricated by unit code | Project owner and housing governance leads; commit uses `Refs #220` | Open outside-scope follow-up; routed to distinct governance follow-up (not a defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No actionable `RV-xxx` implementation defects, decision gaps, or material evidence gaps were found within the assessed `src/core` boundary.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | none | none | All in-scope `src/core` requirements, acceptance criteria, and critique dispositions are conformant |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `src/api` workbench UI exposure for `challenge_update`, `challenge_escalate`, and `target_kind="human_decision"` in `panels.js` under `web-design-guidelines`.
* Human operational workflow acceptance, representative resident/staff comprehension sign-off, and owner policy approval of the `max_days` hazard follow-up age threshold for Issue #220 (`Refs #220`).

## Blockers and Remaining Work

* Blockers: none.
* Remaining active work: none.

## Validation Evidence

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| `python3 -m mypy` | `src/core` (328 source & test files, `strict = true` for `challenges.py` and new test modules) | Passed | `Success: no issues found in 328 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (275 formatted files) | Passed | `275 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*challenge*.py' -v` | `src/core/tests/test_challenges.py` + `src/core/tests/test_issue_220_challenge_route.py` | Passed | `Ran 28 tests in 1.212s — OK` |
| Full un-scoped `unittest discover -s tests` and `tools/rpi-checks.py --all` | `src/core/tests` / repository-wide | Skipped | Explicitly prohibited by caller instructions (`Run ONLY targeted tests (NEVER run full unittest discover -s tests without -p)` and `Do NOT push`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Submitting, updating, escalating, and resolving an affected-person challenge or correction request against a `source`, `policy`, `proposal`, or `human_decision` across digital and non-digital routes in both `ChallengeRegister` and JSON `Store` / SQLite `SqlStore` enforces fail-closed `ChallengeSafeguardError` invariants, leaves priority ranking/support/funding/closure state unpenalized, records zero inferred resident refusals, and never delays, pauses, or resets active statutory/safety hazard clocks, unhanded hazard referrals, or new emergency hazard responses.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up (#220) | Expose `challenge_update` / `challenge_escalate` / `human_decision` in `src/api` workbench UI; obtain human live-workflow acceptance and owner `max_days` approval |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `mypy` (328 files), `ruff check .`, `ruff format --check .` (275 files), and targeted challenge unit tests (`28` passed in `1.212s`)
* Blockers: none
