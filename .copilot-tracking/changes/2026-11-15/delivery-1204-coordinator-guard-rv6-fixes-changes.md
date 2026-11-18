<!-- markdownlint-disable-file -->
# Implementation Changes: Resolve RV-001 through RV-005 Subclause Indexing, Capacity-Aware Ready Launch Verification, Uncited Pause Rejection, Target-Only Blocker Link Evidence, and Active-Row Session Matching (Issue #1204 Child Loop 6)

## Metadata

* Task ID: issue-1204-rv6-fixes
* Task slug: delivery-1204-coordinator-guard-rv6-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan-critique.md
* Declared scope: Full plan (`P01`: `P01-T01` through `P01-T03`)
* Execution status: Complete

## Phase Execution Summary

### P01: Subclause Indexing, Multi-Ready Launch Guard, Mandatory Pause Blocker Evidence, Link-Target Verification, and Active-Row Matching

* `P01-T01` (Complete): Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Scheduled-Check Anti-Idle and Live-Refresh Guard`, `1158` lines, pure ASCII, SHA-256 `49482f018d0fc899286ef9f28c785bfc1e131aa6a02b2b6111932c5dcbced9d5`) to state that lane-specific waiting alongside `ready to start` issues requires actively starting each `ready to start` issue up to available session capacity in the current check, and refreshed `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`.
* `P01-T02` (Complete): Updated `tools/check-coordinator-handoff.py` to:
  * Precompute `subclause_starts` and `subclause_ends` once per `ClauseIndex` and memoize `NON_CURRENT_LAUNCH_SUBCLAUSE_RE` per subclause index in `_launched_ready_issues_in_current_tick` (`RV-001`, `O(N)` scaling).
  * Aggregate `section_launched_ready` across section prose blocks and require `len(section_launched_ready) >= min(len(ready_issue_nums), session_slots)` when waiting below session/PR capacity (`RV-002`, `PC-001`).
  * Widen `BlockerRef = tuple[str, int | str]` to normalize generic non-GitHub URLs (`("url", normalized_url)`) and local anchors (`("anchor", normalized_anchor)`), expand `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` + `BLOCKER_SPAN_STOP_RE` across all unnegated wait/pause claims, and emit at most one `unverified-blocker-pause` per prose block when a non-capacity/non-drain wait/pause cites zero blocker references (`RV-003`, `PC-002`).
  * Pass `include_label_refs=False` in `_extract_verified_evidence_refs` so Markdown link labels never spoof table blocker evidence, and emit `mismatched-blocker-link` on `IssueRow.mismatched_links` when a blocker cell link label embeds an issue/PR number absent from its target (`RV-004`, `PC-003`).
  * Verify `listed_session_tokens` and live `active_sessions` bidirectionally against `classified_by_num` and `active_session_rows` with per-section deduplication (`RV-005`, `PC-004`).
* `P01-T03` (Complete): Added `self.subTest` cases inside existing `11` test methods in `tools/test_check_coordinator_handoff.py` covering `RV-001` (`4000` `while` subclauses in `< 0.25s`), `RV-002` + `PC-001` (multi-ready partial vs complete vs single-slot launches), `RV-003` + `PC-002` (uncited pauses, capacity/drain waits, generic URL blockers), `RV-004` + `PC-003` (`[PR #999](.../pull/1641)` spoofed link label), and `RV-005` + `PC-004` (`#1204` `active session` vs `rpi-999`).

## Amendments and Divergences

* None. All tasks executed as planned after single-pass `PC-001`..`PC-004` critique disposition.

## Validation Summary

* `python3 tools/check-coordinator-handoff.py`: passed (`1 target(s), 0 violations`).
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q`: passed (`Ran 11 tests in 0.448s — OK`).
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: passed (`All checks passed!`).
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: passed (`2 files already formatted`).
* `python3 -m unittest tools/test_rpi_phase_witness.py -q`: passed (`Ran 33 tests in 2.837s — OK`).
* `git --no-pager diff --check` and zero `.copilot-tracking/` literals in `tools/`: clean.

## Blockers and Follow-Ups

* Blockers: None.
* Follow-ups: Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
