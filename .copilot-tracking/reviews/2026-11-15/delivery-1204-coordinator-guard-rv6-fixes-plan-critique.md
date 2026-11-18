<!-- markdownlint-disable-file -->
# Plan Critique: Resolve RV-001 through RV-005 Subclause Indexing, Capacity-Aware Ready Launch Verification, Uncited Pause Rejection, Target-Only Blocker Link Evidence, and Active-Row Session Matching (Issue #1204 Child Loop 6)

## Metadata

* Task ID: issue-1204-rv6-fixes
* Task slug: delivery-1204-coordinator-guard-rv6-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-phase-details.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Critique execution status: Complete
* Verdict: Revise

## Supplied Inputs and Criterion Boundary

Assessed `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-phase-details.md` against parent review findings `RV-001`..`RV-005` (`.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md`), Issue #1204 acceptance criteria 1–4, `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, and `tools/test_check_coordinator_handoff.py`.

## Coverage Assessment and Limitations

* All five routed findings (`RV-001`..`RV-005`) and the `11`-method test ownership lock (`FR-06`) are covered.
* Four planner-owned technical refinements (`PC-001`..`PC-004`) are identified below to prevent subtle false positives, false negatives, or duplicate diagnostics before implementation begins. None conflicts with user decisions or requires user input.

## Findings

### PC-001: Bounding `required_ready_launches` by `20 - declared_open_prs` Weakens Ready-Launch Enforcement When PR Drain Is Inactive

* Severity: High
* Related IDs: `FR-02`, `P01-T02`
* Evidence: `P01-T02` proposes `pr_slots = max(0, 20 - declared_open_prs)` inside `required_ready_launches = min(len(ready_issue_nums), session_slots, pr_slots)`. In `.github/agents/ama-backlog-delivery-coordinator.agent.md`, PR-drain admission throttling applies only when `Open PRs > 20` or during active hysteresis (`Open PRs > 15` with drain recorded), which `at_capacity_or_draining` already models. Starting an RPI session begins in `Research` rather than immediately opening a PR; capping launches by `20 - declared_open_prs` at `Open PRs: 19` (`Active sessions: 1/8`) would allow leaving a second `ready to start` issue unstarted without an active PR drain.
* Impact: Under-enforces `RV-002` when `declared_open_prs` is between `16` and `19` without active PR drain.
* Smallest useful change: Compute `required_ready_launches = min(len(ready_issue_nums), session_slots)` when `not at_capacity_or_draining` (where `session_slots = max(0, session_cap - declared_active_sessions)` if `declared_active_sessions is not None` else `len(ready_issue_nums)`).
* Action owner: Primary planner (`direct_planner_correction`; user response required: `no`).
* Resolving evidence: Updated `FR-02` and `P01-T02` in plan and phase details.

### PC-002: Consolidate `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` Heads and Suppress Duplicate `unverified-blocker-pause` Violations per Prose Block

* Severity: Medium
* Related IDs: `FR-03`, `P01-T02`
* Evidence: If `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` places `\bstatus:\s*waiting\b` before `\bwaiting\s+(?:on|for|until)\b` without consuming optional trailing `on|for|until`, `"Status: waiting on #1288."` matches at `"Status: waiting"` leaving `" on #1288"` (still works), whereas `"Pausing schedule due to an unverified blocker in infra."` matches both `UNVERIFIED_BLOCKER_RE` and `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` (with zero refs), emitting two `unverified-blocker-pause` entries for the same prose block.
* Impact: Redundant duplicate violation lines on single-sentence unverified blocker pauses and potential split trigger heads.
* Smallest useful change: Consume optional trailing prepositions (`(?:\s+(?:on|for|until|due\s+to|because(?:\s+of)?))?`) directly in `status:\s*waiting`, `waiting\s+summary`, `all\s+lanes\s+waiting`, and `paus(?:e|ed|ing)...` branches of `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`, and emit at most one `unverified-blocker-pause` violation per prose block when `has_unverified_phrase or has_uncited_non_capacity_wait`.
* Action owner: Primary planner (`direct_planner_correction`; user response required: `no`).
* Resolving evidence: Updated `FR-03` and `P01-T02` in plan and phase details.

### PC-003: Check Mismatched Blocker Link Labels in `_inspect_blocker_links` Including Bare-Self Target URLs

* Severity: Medium
* Related IDs: `FR-04`, `P01-T02`
* Evidence: If a `human-blocked` row uses `[PR #999](https://github.com/jmservera/ama/issues/1288)` on row `#1288`, `_inspect_blocker_links` already rejects bare-self `/issues/1288` for `has_valid_blocker_link`, while on `[PR #999](https://github.com/jmservera/ama/pull/1641)` `has_valid_blocker_link` is `True` (`#1641` is valid) even though the label falsely claims `PR #999`. Recording `mismatched_links: tuple[str, ...]` on `IssueRow` during table parsing lets `_validate_section` report `mismatched-blocker-link` deterministically at `row.lineno` while `_extract_verified_evidence_refs` (`include_label_refs=False`) never credits `#999`.
* Impact: Ensures row-accurate diagnostics and prevents label spoofing across all table states (`active session`, `human-blocked`, `dependency-blocked`).
* Smallest useful change: Detect mismatched `#<n>` link labels (`n != row.issue_number` where `(rq or inherited_repo, n)` is not in `issue_pr_target_refs`) on `IssueRow` blocker cells and emit `mismatched-blocker-link` at `row.lineno`, alongside `include_label_refs=False` in `_extract_verified_evidence_refs`.
* Action owner: Primary planner (`direct_planner_correction`; user response required: `no`).
* Resolving evidence: Updated `FR-04` and `P01-T02` in plan and phase details.

### PC-004: Deduplicate `stale-session-classification` Diagnostics Across `listed_session_tokens` and `active_sessions`

* Severity: Low
* Related IDs: `FR-05`, `P01-T02`
* Evidence: When a handoff lists ``Active sessions: 1/8 (`rpi-999`)`` and `--active-sessions rpi-999` is also passed on the CLI while `#1204` is marked `active session`, running bidirectional checks independently for `listed_session_tokens` and `active_sessions` would emit duplicate `stale-session-classification` messages for `#1204` and `rpi-999`.
* Impact: Duplicate violation messages on the same row/session.
* Smallest useful change: Track emitted `(kind, issue_num)` keys in a per-section `seen_session_mismatch: set[tuple[str, int]]` set so each stale row or unclassified live session is reported once.
* Action owner: Primary planner (`direct_planner_correction`; user response required: `no`).
* Resolving evidence: Updated `FR-05` and `P01-T02` in plan and phase details.

## Closeout Summary

* Critique execution status: `Complete`
* Verdict: `Revise` (`0` Critical, `1` High, `2` Medium, `1` Low)
* Highest-impact finding: `PC-001` (avoid bounding `required_ready_launches` by `20 - declared_open_prs` when PR drain is inactive)
* Action owner: Primary planner (`direct_planner_correction`)
* Smallest next action: Apply `PC-001`..`PC-004` directly to the plan and phase details, record `## Critique Disposition`, mark planning `ready`, and advance to `Implement` without repeating critique.
* User response required: `no`
