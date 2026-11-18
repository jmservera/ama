<!-- markdownlint-disable-file -->
# Phase Details: Resolve RV-001 through RV-005 Subclause Indexing, Capacity-Aware Ready Launch Verification, Uncited Pause Rejection, Target-Only Blocker Link Evidence, and Active-Row Session Matching (Issue #1204 Child Loop 6)

## Metadata

* Task ID: issue-1204-rv6-fixes
* Task slug: delivery-1204-coordinator-guard-rv6-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan-critique.md
* Phase status: complete

<!-- rpi:phase id=P01 -->
## P01: Subclause Indexing, Multi-Ready Launch Guard, Mandatory Pause Blocker Evidence, Link-Target Verification, and Active-Row Matching

<!-- rpi:task id=P01-T01 -->
### P01-T01: Clarify Capacity-Bounded Multi-Ready Concurrent Launch Rule in `.github/agents/ama-backlog-delivery-coordinator.agent.md` and Refresh HVE Assessment SHA

#### Purpose

Ensure `.agent.md` explicitly states that lane-specific waiting alongside `ready to start` issues requires actively starting each `ready to start` issue up to available session/PR admission capacity in the current check.

#### Concrete Changes

* In `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Scheduled-Check Anti-Idle and Live-Refresh Guard`), refine the `ready to start` bullet to specify `(up to available session and PR capacity)`.
* Refresh the `.agent.md` SHA-256 and line count in `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`.

#### Completion Expectations

* `test_rpi_phase_witness.py` (`33` tests) and `check_agent_instructions` pass with `0` violations.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement Subclause Indexing, Multi-Ready Launch Verification, Uncited Pause Rejection, Target-Only Blocker Link Evidence, and Bidirectional Active-Session Matching in `tools/check-coordinator-handoff.py`

#### Purpose

Close `RV-001`..`RV-005` in `tools/check-coordinator-handoff.py` with strict `O(N)` worst-case time complexity.

#### Concrete Changes

1. **Precomputed Subclause Bounds (`RV-001`)**:
   * Add `subclause_starts: tuple[int, ...]` and `subclause_ends: tuple[int, ...]` to `ClauseIndex`, computed once in `_build_clause_index` by splitting each clause `[c_start, c_end)` via `SUBCLAUSE_SPLIT_RE.finditer(span_masked, c_start, c_end)`.
   * Replace `_launches_ready_issue_in_current_tick` with `_launched_ready_issues_in_current_tick(text: str, idx: ClauseIndex, ready_issue_nums: set[int]) -> set[int]`, resolving `[sub_start, sub_end)` via `si = bisect_right(idx.subclause_starts, m.start()) - 1` (`O(log N)`), caching `NON_CURRENT_LAUNCH_SUBCLAUSE_RE.search(text, sub_start, sub_end)` per subclause index `si`, and checking `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE.search(text, sub_start, m.start())` without string slicing.
2. **Capacity-Bounded Multi-Ready Launch Check (`RV-002` / `PC-001`)**:
   * Pre-scan all prose blocks in `_validate_section` to collect `section_launched_ready: set[int]` (the union of actively launched `ready_issue_nums` across the section's prose blocks).
   * Compute `session_slots = max(0, session_cap - declared_active_sessions)` when `declared_active_sessions is not None` else `len(ready_issue_nums)`, and `required_ready_launches = min(len(ready_issue_nums), session_slots)`.
   * When `is_waiting_or_pause and ready_rows and not at_capacity_or_draining`: reject with `unsupported-waiting-ready-work` whenever `is_global_wait_or_pause` OR `len(section_launched_ready) < required_ready_launches`, reporting any unstarted ready issue IDs.
3. **Mandatory Verified Blocker Reference on Non-Capacity Waits/Pauses (`RV-003`)**:
   * Widen `BlockerRef = tuple[str, int | str]` so `_extract_url_blocker_refs` records normalized non-GitHub `http(s)://` URLs as `("url", normalized_url)` instead of returning `[]`.
   * Replace `BLOCKER_TRIGGER_RE` with `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` covering all `WAITING_OR_PAUSE_RE` and `BLOCKER_TRIGGER_RE` heads (`paus(?:e|ed|ing) ...`, `blocked on/by`, `waiting on/for/until`, `status: waiting`, `waiting summary`, `all lanes waiting`), and allow `:` inside `BLOCKER_SPAN_STOP_RE` (`[.;!?]`) unless followed by a launch verb (`:\s*(?:launch\w*|start\w*|dispatch\w*|spawn\w*)\b`) so `"Waiting summary: #1288"` keeps `#1288` in the span.
   * Return `(cited_refs, has_uncited_non_capacity_wait)` from `_extract_wait_and_blocker_spans(text, idx, at_session_capacity=..., pr_drain_active=...)`: for each disjoint unnegated wait/pause/blocker span `[tm.start(), end_pos)` (excluding `nothing ready to start`, which is governed by `ready_rows` / `unclassified_reasons`), extract refs from `text[tm.end():end_pos]`; if `span_refs` is empty and neither `(at_session_capacity and SESSION_CAPACITY_WAIT_RE.search(text, tm.start(), end_pos))` nor `(pr_drain_active and PR_DRAIN_WAIT_RE.search(text, tm.start(), end_pos))` matches, set `has_uncited_non_capacity_wait = True` and emit `unverified-blocker-pause`!
4. **Target-Only Table Blocker Link Evidence (`RV-004`)**:
   * Add `include_label_refs: bool = True` and `mismatched_labels_out: list[str] | None = None` to `_extract_refs_from_fragment` (with `row_issue_number: int | None = None`):
     * When `include_label_refs=False` (used by `_extract_verified_evidence_refs` on table `row.blocker_cells`), never add Markdown link `lbl` `#<n>` references to `verified_blocker_evidence_refs`; moreover, if `lbl` contains a `#<n>` reference (`lnum != row_issue_number`) that is absent from `target_refs` (either because `target_refs` has different issue/PR ref(s) or `target_refs` has no issue/PR ref at all while `lbl` claims `#<n>`), record a `mismatched-blocker-link` violation on that table row!
     * Keep `include_label_refs=True` when extracting prose citations so `Waiting on [PR #999](.../pull/1641)` requires BOTH `#999` and `#1641` to be verified in the table.
5. **Bidirectional Active-Row vs Live/Declared Session Matching (`RV-005`)**:
   * Helper `_check_session_table_alignment` for both `listed_session_tokens` and `active_sessions`:
     * Every `rpi-<N>` token in the session set must match a row in `classified_by_num` (when `class_tables` is non-empty) with `state == "active session"`, flagging `stale-session-classification` both when `N` is missing from `classified_by_num` and when `classified_by_num[N].state != "active session"`.
     * When `active_sessions is not None` (unless a non-`rpi-<N>` custom live session token explicitly embeds bounded `(?<!\d)N(?!\d)`), and likewise for `listed_session_tokens` when `listed_session_tokens` is non-empty and `not has_non_issue_session_token`, every `active session` row `#N` must appear in the session issue set, flagging `stale-session-classification` when `#N` has no matching active session (e.g., `#1204` marked `active session` while the only live session is `rpi-999`).

#### Completion Expectations

* `tools/check-coordinator-handoff.py` passes `ruff check`, `ruff format --isolated --line-length 100 --check`, and live `.agent.md` check (`0` violations).

<!-- rpi:task id=P01-T03 -->
### P01-T03: Add `RV-001`..`RV-005` Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

#### Purpose

Lock `RV-001`..`RV-005` with targeted `self.subTest` cases inside existing test methods (`11` test methods preserved).

#### Concrete Changes

* Add `self.subTest` cases inside `tools/test_check_coordinator_handoff.py` for:
  * `"while will be starting #1310 " * 4000` completing in `< 0.15s` (`RV-001`).
  * Waiting while `#1310` AND `#1311` are `ready to start` at `1/8` capacity: starting only `#1310` fails `unsupported-waiting-ready-work`; starting both `#1310` and `#1311` passes (`[]`); at `7/8` capacity (`1` free slot), starting `#1310` passes (`[]`) (`RV-002`).
  * Generic uncited pauses (`"Pausing the run due to an approval from another stakeholder."`, `"Waiting on PR #1641; pausing the run due to stakeholder sign-off."`, `"Paused the check until reply arrives."`, and `"Waiting on https://unverified.example.com/gate."`) failing `unverified-blocker-pause` / `unverified-blocker-reference`, while `"Waiting on https://example.com/1288."` passes when `https://example.com/1288` is in the blocker cell (`RV-003`).
  * `[PR #999](https://github.com/jmservera/ama/pull/1641)` in a table blocker cell flagging `mismatched-blocker-link` and rejecting `"Waiting on PR #999."` as `unverified-blocker-reference` (`RV-004`).
  * `#1204` classified `active session` when `active_sessions={"rpi-999"}` (even with `Active sessions: 1/8 (\`rpi-999\`)` in metadata!) flagging `stale-session-classification` for both `#1204` (no live session) and `rpi-999` (unclassified live session) (`RV-005`).

#### Completion Expectations

* `unittest` (`11` test methods), `ruff check`, `ruff format --isolated --line-length 100 --check`, `test_rpi_phase_witness.py` (`33` tests), zero `.copilot-tracking/` literals check, and `git --no-pager diff --check` all exit `0`.
