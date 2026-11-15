<!-- markdownlint-disable-file -->
# Review: Resolve RV-001 through RV-005 Pre-Indexed Clause Raw Slices, Coordinated Wait-Segment Verification, Next-Check Capacity/Drain Tails, and Complete Subtest Coverage (Issue #1204 Child Loop 8)

## Scope and Evidence

* Task ID: issue-1204-rv8-fixes
* Review date: 2026-11-15
* Review scope: Full task (`P01`: `P01-T01` through `P01-T02`)
* Assessed boundary: Issue #1204 acceptance criteria 1–4, routed parent review findings `RV-001`..`RV-005`, critique dispositions `PC-001`..`PC-003`, Focused validation tier (`unittest`, `ruff check`, `ruff format --check`), and HVE agent conformance (`test_rpi_phase_witness.py`).
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-review.md, `.github/agents/ama-backlog-delivery-coordinator.agent.md`, and independent read-only `rubber-duck` verification.

## Opening Review State

* Interpreted review goal: Verify complete closure of parent `RV-001`..`RV-005` and `PC-001`..`PC-003` plus end-to-end Issue #1204 conformance without runtime crashes, quadratic scaling paths, bypasses, or false positives.
* Review scope: Full task (`P01-T01`..`P01-T02`)
* Evidence readiness: Complete across plan, details, critique, changes record, Focused validation runs, and independent read-only subagent review.
* Acceptance basis: Issue #1204 acceptance criteria 1–4, `FR-01`..`FR-05`, `NFR-01`..`NFR-02`, and `PC-001`..`PC-003`.
* First comparison boundary: Plan-to-change reconciliation and adversarial edge-case verification of `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`.
* Active read-only boundaries: Write only this canonical review artifact; leave source, plan, details, critique, and changes artifacts untouched.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed 2026-11-15 across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and `rv8-fixes` RPI artifacts with independent read-only `rubber-duck` verification.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01-T01` | Pre-indexed `ClauseTokens.raw`, coordinated wait-segment verification, adjacent trigger bridge handling, and next-check timing tails | Reconciled with residual defects | Parent `RV-001` and `RV-005` closed, but `_fallback_prohibition_check` invokes integer `pm.end` as `pm.end()` (`RV-001`), `TRAILING_NEXT_TRIGGER_BRIDGE_RE` backtracks quadratically over whitespace (`RV-002`), custom non-RPI session matching scans quadratically (`RV-003`), causal `because`/`due to` uncited blockers piggyback on cited PRs (`RV-004`), bare `Status: paused.` bypasses `WAITING_OR_PAUSE_RE` (`RV-005`), comma-prefixed `, until the next check` backtracks into a false split (`RV-006`), and 3-segment contiguous lifecycle chains reject (`RV-007`). |
| `P01-T02` | `self.subTest` regression cases inside existing `11` test methods, exact two-file tracking-literal scope, and Focused validation | Reconciled | All `11` test methods (`0.645s`), `ruff check`, `ruff format --check`, and `33` witness tests pass; new defects `RV-001`..`RV-007` need targeted regression subtests. |
| `Follow-Up Items` | Dedicated gate-tooling PR to wire `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` | Reconciled | Outside Focused validation scope per `#1294`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `tools/check-coordinator-handoff.py` | Implemented `ClauseTokens.raw`, coordinated wait-segment splitting, and `NEXT_CHECK_TIMING_TAIL_PAT` | Changes log + `git diff` | Focused checks pass; `RV-001`..`RV-007` defects identified | Defects found |
| `P01-T02` | `tools/test_check_coordinator_handoff.py` | Added `rv8` `self.subTest` cases inside `11` existing test methods | `Ran 11 tests in 0.645s` | `unittest`, `ruff check`, `ruff format --check` exit `0` | Conformant for `rv7` findings; needs `RV-001`..`RV-007` subtests |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` multi-trigger bridge handling | Extended `INTRO_PREFIX_BETWEEN_RE` and added `TRAILING_NEXT_TRIGGER_BRIDGE_RE` when `BLOCKER_SPAN_STOP_RE` hits `next_start` | Local judgment during `Implement` after observing `endpos` lookahead cutoff | Reflected in `FR-02`, `P01-T01` phase details, and changes log | Preserved `PC-001`..`PC-003`, but `TRAILING_NEXT_TRIGGER_BRIDGE_RE` introduced left-unanchored whitespace backtracking (`RV-002`) | Needs linear backward bridge trim |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`..`PC-003` were reflected in the plan, details, and implementation, though comma-prefixed `, until the next check` backtracks `\s*` in `COORDINATED_WAIT_SPLIT_RE` (`RV-006`) and 3-item lifecycle chains exceed single-step adjacency (`RV-007`).
* Material revisions: None requiring user input.
* Dependent-work pause assessment: No pause required.
* Justification assessment: Route `RV-001`..`RV-007` to child loop 9.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation | Modifying gate tooling requires full-tier validation (`#1294`), whereas this task prohibits running `tools/rpi-checks.py` | Separate follow-up PR | Distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Critical]: `_fallback_prohibition_check` Calls Integer `pm.end` as a Method and Crashes on Multi-Token Quoted Prohibition Prose

* Related scope: `P01-T01` (`FR-01`)
* Evidence: In `tools/check-coordinator-handoff.py`, `_fallback_prohibition_check` accesses `clause_raw[pm.end() : rel_pos]`, where `pm` is a `ProhibitionMatch` dataclass whose `end` attribute is an `int`. Inputs entering `_fallback_prohibition_check` (such as `Never say "we are waiting on PR #1641".` where non-initial tokens precede the trigger inside quotes) raise `TypeError: 'int' object is not callable`.
* Impact: Unhandled runtime crash on valid coordinator prose containing multi-word quoted prohibition examples.
* Destination: `rpi-implement`
* Smallest useful next action: Replace `pm.end()` with `pm.end` in `_fallback_prohibition_check` and add quoted multi-token prohibition regression subtests.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: `TRAILING_NEXT_TRIGGER_BRIDGE_RE` Backtracks Quadratically Over Whitespace Between Triggers

* Related scope: `P01-T01` (`FR-02`, `NFR-01`)
* Evidence: `TRAILING_NEXT_TRIGGER_BRIDGE_RE` begins with unanchored `\s+\b(?:and|or|also|plus|as\s+well\s+as)\s*$` and is invoked via `.search(idx.span_masked_text, tm.end(), next_start)`, causing `O(L^2)` backtracking over long whitespace spans (`8,000` spaces takes `0.79s`; `32,000` spaces takes `11.01s`).
* Impact: Violates strict `O(N)` scaling on multi-trigger handoff text with wide whitespace padding.
* Destination: `rpi-implement`
* Smallest useful next action: Replace `TRAILING_NEXT_TRIGGER_BRIDGE_RE.search` with a deterministic linear helper `_strip_trailing_trigger_bridge(span_masked: str, start: int, end: int) -> int` using `rstrip()` and trailing token inspection without regex backtracking, plus a scaling subtest.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Custom Non-RPI Session Coverage Scan Is Quadratic Across Active Issue Rows and Custom Session Tokens

* Related scope: `P01-T01` (`NFR-01`)
* Evidence: Session consistency validation executes `any(re.search(rf"(?<!\d){row_num}(?!\d)", custom_tok) for custom_tok in custom_non_rpi_tokens)` inside `for act_row in active_session_rows:`, compiling/searching per `(issue, session)` pair (`500` issues x `500` custom sessions takes `0.25s`; `2,000` x `2,000` takes `4.00s`).
* Impact: Quadratic scaling when many active issues and custom session tokens are present.
* Destination: `rpi-implement`
* Smallest useful next action: Extract integer tokens once across `custom_non_rpi_tokens` into `custom_session_issue_nums: set[int]` (`O(S)`) before iterating `active_session_rows`, reducing per-row lookup to `O(1)`.

<!-- rpi:review id=RV-004 -->
### RV-004 [High]: Unverified Causal Blockers (`because` / `due to` / `owing to`) Piggyback on a Verified Blocker Citation

* Related scope: `P01-T01` (`FR-02`)
* Evidence: `COORDINATED_WAIT_SPLIT_RE` splits on `and`/`or`/`plus`/`as well as` and commas, but not causal blocker clauses (`because`, `because of`, `due to`, `owing to`), allowing `"Waiting on PR #1641 because stakeholder approval is pending."` to pass without citing approval evidence.
* Impact: Permits an unverified human or external blocker to be asserted as the underlying pause reason behind a cited PR.
* Destination: `rpi-implement`
* Smallest useful next action: Include `\b(?:because(?:\s+of)?|due\s+to|owing\s+to)\b` in `COORDINATED_WAIT_SPLIT_RE` (and allow optional leading `(?:of\s+)?` in `SHARED_REF_LIFECYCLE_SEG_RE` for phrases like `"because of its hosted CI"`) so causal blocker clauses require verified evidence or shared lifecycle attachment.

<!-- rpi:review id=RV-005 -->
### RV-005 [High]: Bare `Status: paused.` Summaries Bypass `WAITING_OR_PAUSE_RE` and `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`

* Related scope: `P01-T01` (Issue #1204 AC 1 & AC 2)
* Evidence: `WAITING_OR_PAUSE_RE`, `DIRECT_GLOBAL_WAIT_RE`, and `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` recognize `status: waiting`, `waiting summary`, `all lanes waiting`, and `paused the run / paused on ...`, but omit `status: paused` / `paused summary` / `all lanes paused`. Consequently, a handoff stating `"Status: paused."` with open issues and no classification table passes offline validation without `missing-classification-table` or `unverified-blocker-pause`.
* Impact: Allows bare pause status headers to bypass both the mandatory classification-table check and verified-blocker enforcement.
* Destination: `rpi-implement`
* Smallest useful next action: Add `status:\s*paus(?:e|ed|ing)\b`, `paused\s+summary\b`, and `all\s+lanes\s+paused\b` to `WAITING_OR_PAUSE_RE`, `DIRECT_GLOBAL_WAIT_RE`, `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`, and `CLAUSE_SPLIT_RE`, and add regression subtests.

<!-- rpi:review id=RV-006 -->
### RV-006 [Medium]: Comma-Prefixed Timing Tails (`, until the next check`) Backtrack Over Whitespace in `COORDINATED_WAIT_SPLIT_RE`

* Related scope: `P01-T01` (`FR-02`, `FR-03`)
* Evidence: In `COORDINATED_WAIT_SPLIT_RE`, `,\s*(?:...)?(?!(?:until|...)\b)` allows `\s*` to backtrack to zero characters when `, until` follows, so `(?!until\b)` inspects the space character `" until"`, succeeds, and splits `"Waiting for a free worker session slot, until the next check."` into `" until the next check"`, triggering a false-positive `unverified-blocker-pause` at full capacity.
* Impact: Rejects valid comma-delimited timing qualifiers explicitly allowed by `NEXT_CHECK_TIMING_TAIL_PAT`.
* Destination: `rpi-implement`
* Smallest useful next action: Place the negative lookahead immediately after `,` with explicit optional whitespace inside the lookahead (`r",(?![ \t]*(?:until|before|for|pending|awaiting|till|at|during|under|in|on|with|without)\b)[ \t]*(?:(?:and|or|plus|as\s+well\s+as)\b[ \t]*)?"`) so whitespace cannot backtrack past the preposition check.

<!-- rpi:review id=RV-007 -->
### RV-007 [Low]: Contiguous Multi-Item Shared Lifecycle Lists (`PR #1641 and its hosted CI and status checks`) Reject Beyond Immediate Neighbor

* Related scope: `P01-T01` (`FR-02`, `PC-001`)
* Evidence: `_extract_wait_and_blocker_spans` checks only `j - 1` and `j + 1` for `seg_refs_list` non-emptiness, so `"Waiting on PR #1641 and its hosted CI and status checks."` accepts segment `1` (`its hosted CI`) but rejects segment `2` (`status checks`).
* Impact: False positive on 3+ item lifecycle lists describing a single cited PR.
* Destination: `rpi-implement`
* Smallest useful next action: Propagate citation adjacency across contiguous `SHARED_REF_LIFECYCLE_SEG_RE` segments in two linear sweeps (left-to-right and right-to-left) so any contiguous run of pure lifecycle nouns attached to a cited PR/issue segment passes while non-lifecycle blockers still fail.

## Validation Assessment

* Required checks run:
  * `python3 tools/check-coordinator-handoff.py`: Passed (`0` violations).
  * `python3 -m unittest tools/test_check_coordinator_handoff.py -q`: Passed (`11` test methods in `0.645s`).
  * `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: Passed.
  * `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: Passed.
  * `python3 -m unittest tools/test_rpi_phase_witness.py -q`: Passed (`33` tests in `3.528s`).
* Skipped checks:
  * `python3 tools/rpi-checks.py`: Explicitly prohibited by user prompt (Focused validation tier).
* Residual testing risks: `RV-001`..`RV-007` require code fixes and regression subtests in child loop 9.

## Outcome and Routing

* Execution status: Complete
* Outcome: Defects found (`1` Critical, `4` High, `1` Medium, `1` Low)
* Recommended destination: Child automatic RPI loop (`issue-1204-rv9-fixes` / `delivery-1204-coordinator-guard-rv9-fixes`) resolving `RV-001`..`RV-007` under Focused validation while keeping this review artifact immutable.
