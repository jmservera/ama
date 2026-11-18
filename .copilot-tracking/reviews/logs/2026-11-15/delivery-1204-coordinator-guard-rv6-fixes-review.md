<!-- markdownlint-disable-file -->
# Review: Resolve RV-001 through RV-005 Subclause Indexing, Capacity-Aware Ready Launch Verification, Uncited Pause Rejection, Target-Only Blocker Link Evidence, and Active-Row Session Matching (Issue #1204 Child Loop 6)

## Scope and Evidence

* Task ID: issue-1204-rv6-fixes
* Review date: 2026-11-15
* Review scope: Full task (`P01`: `P01-T01` through `P01-T03`)
* Assessed boundary: Issue #1204 acceptance criteria 1–4, routed parent review findings `RV-001`..`RV-005`, critique dispositions `PC-001`..`PC-004`, Focused validation tier (`unittest`, `ruff check`, `ruff format --check`), and HVE agent conformance (`test_rpi_phase_witness.py`).
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md, .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md, and independent read-only `rubber-duck` subagent verification.

## Opening Review State

* Interpreted review goal: Verify complete closure of parent `RV-001`..`RV-005` and full conformance with Issue #1204 acceptance criteria 1–4 without regressions or quadratic scaling paths.
* Review scope: Full task (`P01-T01`..`P01-T03`)
* Evidence readiness: Complete across plan, details, critique, changes record, Focused test outputs, and independent subagent lens.
* Acceptance basis: Issue #1204 acceptance criteria 1–4, `FR-01`..`FR-06`, `NFR-01`..`NFR-02`, and `PC-001`..`PC-004`.
* First comparison boundary: Plan-to-change reconciliation and adversarial edge-case verification of `tools/check-coordinator-handoff.py`.
* Active read-only boundaries: Write only this canonical review artifact; leave source, plan, details, critique, and changes artifacts untouched.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed 2026-11-15 across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and `rv6-fixes` RPI artifacts with independent read-only `rubber-duck` verification.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01-T01` | Capacity-bounded multi-ready launch rule in `.agent.md` + HVE SHA refresh | Reconciled | `.agent.md` passes `check-coordinator-handoff.py` and `test_rpi_phase_witness.py` (`33` tests). |
| `P01-T02` | Subclause indexing, multi-ready launch guard, uncited pause rejection, target-only link evidence, and bidirectional session check | Reconciled with edge-case defects | Core `RV-001`..`RV-005` scenarios pass, but independent adversarial review exposed six residual edge cases (`RV-001`..`RV-006` below). |
| `P01-T03` | `self.subTest` regression cases inside `11` existing test methods + Focused validation | Reconciled | `11` test methods (`0.448s`), `ruff check`, and `ruff format --check` pass. |
| `Follow-Up Items` | Dedicated gate-tooling PR to wire `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` | Reconciled | Outside Focused validation scope per `#1294`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` | Clarified `(up to available session capacity)` on concurrent `ready to start` launches | SHA-256 `49482f018d0fc899286ef9f28c785bfc1e131aa6a02b2b6111932c5dcbced9d5` | `33` witness tests + `0` guard violations | Reconciled |
| `P01-T02` | `tools/check-coordinator-handoff.py` | Implemented subclause indexing, capacity-bounded ready launch counting, wait/blocker span checking, `mismatched-blocker-link`, and session-table cross-checks | Changes log + `git diff` | Focused tests pass; `RV-001`..`RV-006` edge cases remain | Residual edge-case defects |
| `P01-T03` | `tools/test_check_coordinator_handoff.py` | Added `self.subTest` cases for `RV-001`..`RV-005` | `Ran 11 tests in 0.448s` | `unittest`, `ruff check`, `ruff format --check` exit `0` | Needs subtests for `RV-001`..`RV-006` |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time plan amendments or divergences occurred after `PC-001`..`PC-004` disposition. | None | Plan, details, and changes markers fully aligned | `PC-001`..`PC-004` applied prior to Implement | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`..`PC-004` were applied directly before implementation and verified in unit subtests.
* Material revisions: None during `Implement`.
* Dependent-work pause assessment: No pause required.
* Justification assessment: Supported by Focused validation evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation | Modifying gate tooling requires full-tier validation (`#1294`), whereas this task prohibits running `tools/rpi-checks.py` | Separate follow-up PR | Distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Quadratic Prefix Rescanning Inside Single Long Subclauses in `_launched_ready_issues_in_current_tick`

* Related scope: `P01-T02`
* Evidence: `tools/check-coordinator-handoff.py` (`_launched_ready_issues_in_current_tick`) checks `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE.search(text, sub_start, m.start())` on every `READY_LAUNCH_RE` match before checking memoized `is_non_current` and without indexing earliest hold/negation end offset per subclause. Repeating `"starting #1310 "` 2,000 times inside one subclause before `"after approval"` scales quadratically (`~3.19s` at 2,000 repetitions).
* Impact: Reintroduces `O(K^2)` worst-case latency on single-subclause inputs with repeated launch phrases.
* Destination: `rpi-implement`
* Smallest useful next action: Check memoized `is_non_current` first per subclause `si` and memoize `min_hold_end = min((hm.end() for hm in LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE.finditer(text, sub_start, sub_end)), default=None)` once per subclause so `min_hold_end is not None and min_hold_end <= m.start()` runs in `O(1)` per match (`O(N)` total).

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Earlier Cited Wait Span Masks Subsequent Uncited Pause Trigger Separated by Non-`and`/`or` Connectors

* Related scope: `P01-T02`
* Evidence: `tools/check-coordinator-handoff.py` (`_extract_wait_and_blocker_spans` / `BLOCKER_SPAN_STOP_RE`) allows `"Waiting on PR #1641 because pausing the run for stakeholder approval."` to pass when `#1641` is verified because `covered_until` advances to the period at the end of the sentence, skipping the uncited `pausing the run for stakeholder approval` trigger.
* Impact: Allows an uncited pause claim to piggyback on an earlier verified lane wait in the same sentence.
* Destination: `rpi-implement`
* Smallest useful next action: Collect all unnegated `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` matches and clamp each trigger's span upper bound at the next unnegated trigger start (skipping a prefix trigger only when the text between `tm.end()` and the next trigger start is pure punctuation/whitespace such as `Status: waiting — blocked on #1641`), validating every substantive wait/pause trigger independently in `O(N)`.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Broad Session-Capacity Keyword Match Excuses Uncited Stakeholder/Approval Waits When Sessions Are Full

* Related scope: `P01-T02`
* Evidence: `tools/check-coordinator-handoff.py` (`SESSION_CAPACITY_WAIT_RE` / `PR_DRAIN_WAIT_RE`) matches loose keywords (`capacity`, `cap`, `sessions`, `prs`), letting `"Waiting for stakeholder approval of the capacity plan."` pass without any verified blocker reference whenever `at_session_capacity` holds.
* Impact: Permits pausing or waiting on unverified human/external blockers at full worker concurrency as long as the prose mentions a capacity-related noun.
* Destination: `rpi-implement`
* Smallest useful next action: Anchor `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` to explicit slot/capacity saturation or PR-drain throttling targets and disqualify spans mentioning unverified human/review/CI blockers (`approval`, `stakeholder`, `owner`, `review`, `human`, `sign-off`, `decision`, `feedback`, `upstream`, `ci`, `checks`).

<!-- rpi:review id=RV-004 -->
### RV-004 [High]: Bare Self-Issue GitHub URLs Count as Valid Blocker Links on `human-blocked` and `dependency-blocked` Rows

* Related scope: `P01-T02`
* Evidence: `tools/check-coordinator-handoff.py` (`_inspect_blocker_links` and `_extract_verified_evidence_refs`) accepts `https://github.com/jmservera/ama/issues/1288` (and `[self](https://github.com/jmservera/ama/issues/1288)`) on `#1288`'s `human-blocked` row even though there is no `#issuecomment-...` fragment or external blocker issue/PR target.
* Impact: Bypasses the concrete blocker-link requirement when a row links to its own bare GitHub issue URL instead of `#1288`.
* Destination: `rpi-implement`
* Smallest useful next action: Reject bare self-issue URLs (`.../issues/<self>` without a non-empty `#fragment` when targeting the row's own repository or relative `/issues/<self>`) in both `_inspect_blocker_links` and `_extract_verified_evidence_refs`, while preserving comment/review fragment links (`.../issues/1288#issuecomment-10`) and cross-repository issue links (`octo/other/issues/1288`).

<!-- rpi:review id=RV-005 -->
### RV-005 [High]: Uncited `blocked on/by` Claims Without a Classification Table Bypass Both Pause and Missing-Table Guards

* Related scope: `P01-T02`
* Evidence: `tools/check-coordinator-handoff.py` (`_validate_section`) gates `unverified-blocker-pause` on `has_uncited_non_capacity_wait and first_table_end is not None` and skips table checks via `if not (is_idle or is_waiting_or_pause or cited_blocker_refs): continue`, allowing `"Blocked on stakeholder approval."` with no classification table to pass with `0` violations.
* Impact: Uncited `"Blocked on ..."` prose escapes validation when the classification table is omitted or placed after the claim.
* Destination: `rpi-implement`
* Smallest useful next action: Emit `unverified-blocker-pause` unconditionally on `has_unverified_phrase or has_uncited_non_capacity_wait`, and treat `has_uncited_non_capacity_wait` and `has_unverified_phrase` as wait/blocker claims that require a preceding classification table and full open-issue classification.

<!-- rpi:review id=RV-006 -->
### RV-006 [Medium]: Mixed Declared Session Tokens (`rpi-1302`, `maintenance`) Disable Offline Active-Row Identity Verification

* Related scope: `P01-T02`
* Evidence: `tools/check-coordinator-handoff.py` (`_validate_section`) passes `require_active_rows_covered=not has_non_issue_session_token` for `listed_session_tokens`, allowing `#1204` and `#1302` to both remain `active session` when `Active sessions: 2/8 (\`rpi-1302\`, \`maintenance\`)` has no session matching `#1204`.
* Impact: Offline handoff validation misses stale `active session` rows whenever a non-issue housekeeping tmux session is also listed.
* Destination: `rpi-implement`
* Smallest useful next action: Pass `require_active_rows_covered=True` whenever `listed_session_tokens` is non-empty, matching live-session validation while still permitting non-issue sessions when `active_session_rows` is empty.

## Defects

* `RV-001` [High] -> `rpi-implement`
* `RV-002` [High] -> `rpi-implement`
* `RV-003` [High] -> `rpi-implement`
* `RV-004` [High] -> `rpi-implement`
* `RV-005` [High] -> `rpi-implement`
* `RV-006` [Medium] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Index `min_hold_end` and check `is_non_current` once per subclause | Implementation defect |
| `RV-002` | `rpi-implement` | Clamp each wait/pause trigger span before subsequent triggers | Implementation defect |
| `RV-003` | `rpi-implement` | Tighten capacity/PR-drain wait span matchers and reject human/CI blocker words | Implementation defect |
| `RV-004` | `rpi-implement` | Reject bare same-repo `/issues/<self>` URLs without `#fragment` | Implementation defect |
| `RV-005` | `rpi-implement` | Enforce `unverified-blocker-pause` and table checks on uncited `blocked on/by` claims | Implementation defect |
| `RV-006` | `rpi-implement` | Require active-row session coverage for mixed declared session lists | Implementation defect |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated full-tier gate-tooling PR (`#1294`).

## Blockers and Remaining Work

* Blockers: None.
* Remaining active work: None inside `issue-1204-rv6-fixes`; routed findings `RV-001`..`RV-006` move to child task `issue-1204-rv7-fixes`.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 tools/check-coordinator-handoff.py` | `.github/agents/ama-backlog-delivery-coordinator.agent.md` | Passed | `1 target(s), 0 violations` |
| `python3 -m unittest tools/test_check_coordinator_handoff.py -q` | `tools/` unit tests (`11` test methods) | Passed | `Ran 11 tests in 0.448s — OK` |
| `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` | `tools/` lint | Passed | `All checks passed!` |
| `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` | `tools/` format | Passed | `2 files already formatted` |
| `python3 -m unittest tools/test_rpi_phase_witness.py -q` | `.github/agents/` witness suite | Passed | `Ran 33 tests in 2.837s — OK` |
| `python3 tools/rpi-checks.py` | Repository full gate | Skipped | Explicitly prohibited by caller instructions (`Focused` validation tier) |

## Outcome

* Outcome: Defects found
* Outcome rationale: Six concrete edge-case bypass/scaling defects (`RV-001`..`RV-006`) were identified by independent adversarial verification and routed to `rpi-implement` for child task `issue-1204-rv7-fixes`.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Resolve `RV-001`..`RV-006` in child task `issue-1204-rv7-fixes` |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Wire `check-coordinator-handoff.py` into `tools/rpi-checks.py` under `#1294` full tier |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused validation passed (`11` unit tests, `ruff check`, `ruff format --check`, `33` witness tests); `tools/rpi-checks.py` skipped per caller instructions.
* Blockers: none
