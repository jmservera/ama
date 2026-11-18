<!-- markdownlint-disable-file -->
# Review: Issue #76 Correction Cycle 1 — PR #1768 `mssql` CI Parity Fix and Rebase onto `#1641`

## Scope and Evidence

* Task ID: issue-76-c1
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`)
* Assessed boundary: Rebase of `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), `Store._work_context` merge resolution preserving `#83` and `#76`, staff-order-invariant `_match_staff` and `project_safety_clock_and_owner` (`MEMBERSHIP_REVISION = 5`), strictly typed permutation and email-seeded `SqlStore` parity unit tests in `src/core/tests/test_hazard_safeguarding_clock_owner.py`, focused-tier validation (`FR-1`–`FR-4`, `NFR-1`–`NFR-3`, `AC-1`–`AC-5`), and local commit closeout boundaries.
* Plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-research.md, `git diff origin/feat/demo-164-chat-grounding-provenance-0900`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/taskqueues.py`, `src/core/tests/test_hazard_safeguarding_clock_owner.py`, `src/core/README.md`, and independent bounded review check.

## Opening Review State

* Interpreted review goal: Verify that Correction Cycle 1 (`issue-76-c1`) completely and deterministically resolves the PR #1768 `MssqlParity` staff-ordering failure, cleanly rebases onto `0c1fa1da4` without regressing `#83` or `#76`, satisfies every planned functional/non-functional requirement and critique disposition (`PC-001`–`PC-003`), and preserves strict focused-tier validation and local-commit boundaries.
* Review scope: Full task (`P01` and `P02`)
* Evidence readiness: Ready — plan, phase details, one-pass critique, research, changes record, and executed validation outputs are complete and reconciled.
* Acceptance basis: `FR-1`–`FR-4`, `NFR-1`–`NFR-3`, `AC-1`–`AC-5`, critique dispositions `PC-001`–`PC-003`, and caller intake brief.
* First comparison boundary: Reconcile `P01`/`P02` completion markers and diff against `0c1fa1da4` and `8bd8a4f4d`.
* Active read-only boundaries: Read-only comparison across codebase and tracking inputs; write authority restricted strictly to `.copilot-tracking/reviews/logs/2026-11-15/ux-76-hazard-clock-owner-c1-review.md`.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed on 2026-11-15 across full task scope (`P01` and `P02`), comparing `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md`, `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md`, `.copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-research.md`, the rebased Git diff against `0c1fa1da4`, an independent `rubber-duck` technical review check, and executed focused-tier validation (`3,514` `src/core` unit tests, `mypy`, `ruff`, and `#76` API/DOM tests).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Rebase onto `#1641` (`0c1fa1da4`) and Resolve `Store._work_context` | Reconciled | Branch rebased onto `0c1fa1da4` (`8bd8a4f4d`); `Store._work_context` passes both `#83` `handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` and `#76` `staff=staff_list`. |
| `P01` / `P01-T02` | Deterministic Staff Lookup, Sorted Role Fallback, and Queue Revision Separation | Reconciled | `_match_staff` runs 3 separate passes (`code.strip()` -> `email.strip().lower()` -> `name.strip().lower()`) over canonically sorted `staff`; `project_safety_clock_and_owner` sorts `roster` before role-based fallback scanning; `MEMBERSHIP_REVISION = 5` synced in `taskqueues.py` and `src/core/README.md`. |
| `P02` / `P02-T01` | Permutation and Email-Ordered SQL Parity Unit Tests and Focused Validation | Reconciled | `src/core/tests/test_hazard_safeguarding_clock_owner.py` verifies all `STAFF` permutations, duplicate-role fallback determinism, and `Store` (`[Sam, Pam, Kim]`) vs email-seeded `SqlStore` (`[Kim, Pam, Sam]`) parity under strict `mypy` (`0` `type: ignore` suppressions, `0` `pyproject.toml` edits). |
| `P02` / `P02-T02` | Diff-Boundary Check, Privacy-Safe Git Identity, and Review/Commit Reconciliation | Reconciled | Diff boundary verified (`0` test removals, `1` new test file, `0` C1 `src/api/` edits); local `user.email` configured to `8036360+jmservera@users.noreply.github.com`; ready for single post-Review local `Refs #76` commit. |
| `## Follow-Up Items` | Owner-authorized push and hosted `mssql` CI check on `PR #1768` | Reconciled | Preserved outside active `P01`/`P02` completion claims per caller `Do NOT push` instruction; note also that shared remote `origin/feat/demo-164-chat-grounding-provenance-0900` advanced past `0c1fa1da4` (`#1770`, `#1771`) after Step 0 rebase, so coordinator/owner will rebase onto latest target head when pushing. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/store.py` | Resolved 6-line rebase conflict onto `0c1fa1da4` keeping `#83` handoff escalation arguments and `#76` `staff=staff_list`. | `git merge-base --is-ancestor 0c1fa1da4 HEAD` (`0`); clean `store.py` | Passed (`test_handoff_escalation_83.py` 11/11, `test_hazard_safeguarding_clock_owner_76.py` 3/3) | Reconciled (`FR-1`, `AC-1` met) |
| `P01-T02` | `src/core/src/zava_forward/core/taskqueues.py`, `src/core/README.md` | Implemented `_staff_sort_key`, 3-pass `_match_staff` (`code` > `email` > `name` with `.strip()`), sorted `roster` role fallback in `project_safety_clock_and_owner`, and `MEMBERSHIP_REVISION = 5`. | Code diff inspected; `README.md` synced | Passed (`mypy`, `ruff check`, `ruff format --check`, unit tests) | Reconciled (`FR-1`, `FR-2`, `FR-3`, `AC-1`, `AC-2` met) |
| `P02-T01` | `src/core/tests/test_hazard_safeguarding_clock_owner.py` | Added 4 strictly typed unit tests covering `_match_staff` precedence, all `STAFF` permutations on `owner_code="PM-01"` + `owner="Sam Example"`, duplicate-role fallback, and `Store` vs email-seeded `SqlStore` parity on `make_cases(120)`. | File created; fails against pre-fix single-pass `_match_staff` | Passed (`4/4` targeted, `15/15` `test_sqlreads.py`, `3,514` full `src/core` tests, `mypy` 339 files) | Reconciled (`FR-4`, `NFR-1`, `NFR-2`, `AC-2`–`AC-4` met) |
| `P02-T02` | `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md`, `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md`, `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md` | Verified diff boundaries, configured `gh api user` noreply email (`8036360+jmservera@users.noreply.github.com`), and reconciled tracking state for clean post-Review local commit. | `git config --local user.email` and `git diff --name-status 0c1fa1da4` verified | Passed | Reconciled (`NFR-2`, `NFR-3`, `AC-5` met) |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01`, `P02`, `## Handoff` | Checked `[x]` completion markers across `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02` and updated handoff to `Review`. | Executed implementation and passing focused validation; no new user decision required. | Plan checklist, Phase Index (`Complete`), and `changes.md` synchronized. | Not needed (`PC-001`–`PC-003` already resolved in Plan). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three one-pass critique findings (`PC-001` `Any`-typed untyped collaborator calls and email-seeded `SqlStore` parity test, `PC-002` `P02-T02` local commit/closeout mapping, and `PC-003` `code.strip()` normalization in `_match_staff` Pass 1) were resolved in the plan and verified in the implemented code and tests.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No pause required; `P01-T01` -> `P01-T02` -> `P02-T01` -> `P02-T02` executed strictly in dependency order.
* Justification assessment: Supported by concrete code, typecheck, and test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Push rebased `feat/ux-76-hazard-clock-owner` to `origin` (`PR #1768`) and verify hosted GitHub Actions `mssql` job (`MssqlParity`) | Caller explicitly instructed `Do NOT push or run rpi-checks.py` during this local RPI session (and `origin/feat/demo-164-chat-grounding-provenance-0900` subsequently merged `#1770`/`#1771` after `0c1fa1da4`). | Repository owner / delivery coordinator: rebase onto latest `origin/feat/demo-164-chat-grounding-provenance-0900` if needed, push `feat/ux-76-hazard-clock-owner`, and verify hosted `mssql` CI. | Open distinct `follow_up` (not a defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Sibling `#83` handoff role-fallback scan in `workflows.py` iterates unsorted `staff` when multiple staff share the escalation role

* Related scope: Out-of-scope upstream `#83` (`0c1fa1da4`) observation noted during cross-store audit
* Evidence: src/core/src/zava_forward/core/workflows.py (`_resolve_escalation_target` role scan introduced in `#1769` / `0c1fa1da4`)
* Impact: Does not affect Issue #76 safety clock/owner projections or `MssqlParity` (`test_sqlreads.STAFF` has a single `Retrofit Programme Manager`), and `workflows.py` handoff logic belongs to `#83` rather than `#76`. In a future multi-manager roster where two `Retrofit Programme Manager` rows exist in different orders across stores, sorting `staff` inside `workflows._resolve_escalation_target` would provide the same duplicate-role tie-break invariance added to `taskqueues.py` in `P01-T02`.
* Destination: follow_up
* Smallest useful next action: Track as an optional `follow_up` hardening item for `#83` (`workflows._resolve_escalation_target`) if multi-manager handoff escalation rosters are introduced.

## Defects

* None (`0` Critical, `0` High, `0` Medium, `0` implementation defects in Issue #76 Correction Cycle 1 scope).

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow_up` | Optional future hardening in `workflows._resolve_escalation_target` (`#83`) | Non-blocking observation in sibling `#83` module outside `#76` C1 scope |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Owner/coordinator-authorized push of `feat/ux-76-hazard-clock-owner` to `PR #1768` (rebasing onto latest `origin/feat/demo-164-chat-grounding-provenance-0900` if desired after `#1770`/`#1771` merged) and verification of the hosted GitHub Actions `mssql` container job (`MssqlParity`).
* Optional `RV-001` follow-up to sort `staff` during role-based fallback in `workflows._resolve_escalation_target` (`#83`).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01` and `P02` complete; final local commit executes immediately at RPI closeout).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner.py" -v` | `src/core` | Passed | `Ran 4 tests in 0.537s — OK` |
| `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner_76.py" -v` | `src/core` | Passed | `Ran 3 tests in 0.291s — OK` |
| `python3 -m unittest discover -s tests -p "test_handoff_escalation_83.py" -v` | `src/core` | Passed | `Ran 11 tests in 1.099s — OK` |
| `python3 -m unittest discover -s tests -p "test_sqlreads.py" -v` | `src/core` | Passed | `Ran 15 tests in 49.436s — OK` |
| `mypy` (`strict = true`) | `src/core` (339 files) | Passed | `Success: no issues found in 339 source files` |
| `ruff check .` & `ruff format --check .` | `src/core` (286 files) | Passed | `All checks passed! 286 files already formatted` |
| `python3 -m unittest discover -s tests -q` | `src/core` (full package suite) | Passed | `Ran 3514 tests in 985.644s — OK (skipped=419)` |
| `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner_api_76.py" -v` | `src/api` (`#76` API/UI guard) | Passed | `Ran 2 tests in 2.587s — OK` |
| Hosted `MssqlParity` (`ZF_TEST_MSSQL=1`) | GitHub Actions `mssql` job | Skipped | Deferred to post-push hosted CI per caller `Do NOT push` boundary; exact clustered-PK `email` ordering failure reproduced and verified locally in `test_store_and_email_seeded_sqlstore_match_on_mixed_owner_code_dataset` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every requirement (`FR-1`–`FR-4`, `NFR-1`–`NFR-3`), acceptance criterion (`AC-1`–`AC-5`), and critique disposition (`PC-001`–`PC-003`) is satisfied with verified code, strict static typing, and passing focused-tier unit and SQL-parity tests, with zero open defects in task scope.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct_follow_up | Owner/coordinator push to `PR #1768` + hosted `mssql` CI check; optional `RV-001` sort in `workflows._resolve_escalation_target` (`#83`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier complete and passing (`3,514` `src/core` unit tests, `test_sqlreads.py`, `test_hazard_safeguarding_clock_owner.py`, `mypy`, `ruff`, and `#76` API tests; hosted `mssql` container deferred until push)
* Blockers: None
