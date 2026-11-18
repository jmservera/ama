<!-- markdownlint-disable-file -->
# RPI Review: Resolve RV-001 through RV-004 Constant-Time Suffix Guard, Deferred/Negated Launch Qualification, and URL-Safe Blocker Spans (Issue #1204 Child Loop 4)

## Metadata

* Task ID: issue-1204-rv4-fixes
* Task slug: delivery-1204-coordinator-guard-rv4-fixes
* Parent task ID: issue-1204-rv3-fixes (`delivery-1204-coordinator-guard-rv3-fixes`)
* Review date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-changes.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Execution status: Complete
* Outcome: Defects found

## Assessed Boundary and Reconciliation

* Reconciled `P01`, `P01-T01`, and `P01-T02` completion markers, phase details, critique dispositions (`PC-001`..`PC-003`), changes evidence, Focused validation outputs (`11` tests in `test_check_coordinator_handoff.py` passing in `0.250s`, `33` tests in `test_rpi_phase_witness.py` passing, Ruff clean), and zero `.copilot-tracking/` literals in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`.
* Independent read-only `rubber-duck` review confirmed closure of the targeted `CONDITIONAL_GUARD_SUFFIX_RE` and `\s+--\s+` whitespace paths, URL-safe `;` masking, and `11`-testFocused validation, while surfacing four blocking edge cases (`RV-001`..`RV-004`) and one non-blocking CLI identity check (`RV-005`).

## Severity Summary

* Critical: `0`
* High: `4` (`RV-001`, `RV-002`, `RV-003`, `RV-004`)
* Medium: `0`
* Low: `1` (`RV-005`)

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Quadratic regex backtracking in `MD_LINK_RE` and `ISSUE_REF_RE` plus repeated whole-line negation rescans

* Evidence: tools/check-coordinator-handoff.py (`MD_LINK_RE`, `ISSUE_REF_RE`, `GLOBAL_WAIT_OR_PAUSE_RE`, `_is_claim_negated`, `_launches_ready_issue_in_current_tick`, `_extract_cited_blocker_numbers`).
* Impact: Unclosed `[` runs (`"[a" * 4000`) in `MD_LINK_RE` (`\[([^\]]+)\]`) and long alphanumeric runs (`"a" * 8000` or `"a/b" * 4000`) in `ISSUE_REF_RE` (`(?:([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+))?#(\d+)`) scan quadratically (`O(N^2)`), and repeated match checks re-run `BACKTICK_TOKEN_RE` and `CLAUSE_SPLIT_RE` from index `0` on every match instead of indexing clauses once per prose block.
* Recommended destination: `rpi-implement` (via child remediation loop `issue-1204-rv5-fixes`).

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Hard-wrapped multi-line summaries bypass line-by-line prose guards in `_validate_section`

* Evidence: tools/check-coordinator-handoff.py (`_validate_section` prose loops for `STALE_CARRY_RE`, `IDLE_CLAIM_RE`, `WAITING_OR_PAUSE_RE`, `UNVERIFIED_BLOCKER_RE`, and `_extract_cited_blocker_numbers`).
* Impact: Hard-wrapped Markdown prose such as `"Nothing\nchanged."` or `"Waiting on\nPR #999."` splits trigger tokens across adjacent lines and evades idle, waiting, table-ordering, stale-carry, and blocker verification checks.
* Recommended destination: `rpi-implement` (via child remediation loop `issue-1204-rv5-fixes`).

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Coordinator `.agent.md` waiting rule omits lane-level concurrent-launch qualification and validator accepts post-target `"starting #1310 after ..."`

* Evidence: .github/agents/ama-backlog-delivery-coordinator.agent.md (`ready to start` rule) and tools/check-coordinator-handoff.py (`NON_CURRENT_LAUNCH_SUBCLAUSE_RE`).
* Impact: `.github/agents/ama-backlog-delivery-coordinator.agent.md` states unqualified `bars waiting summaries unless active tmux sessions are at the declared session cap...` without stating the lane-specific concurrent-launch exception enforced by `check-coordinator-handoff.py`, while `NON_CURRENT_LAUNCH_SUBCLAUSE_RE` accepts post-target conditional/deferred phrases such as `"starting #1310 after approval"` or `"starting #1310 once CI passes"` as current-tick launches.
* Recommended destination: `rpi-implement` (via child remediation loop `issue-1204-rv5-fixes`).

<!-- rpi:review id=RV-004 -->
### RV-004 [High]: Blocker verification truncates spans at 300 characters, treats `Next action` cells as blocker evidence, and discards repository qualifiers

* Evidence: tools/check-coordinator-handoff.py (`_extract_cited_blocker_numbers`, `_extract_classification_tables`, `_inspect_blocker_links`, `_extract_verified_evidence_numbers`).
* Impact: Blocker citations past 300 characters in a long clause are ignored; `#<n>` mentions in a `Next action` column (for example `Unblocks #999 later`) satisfy blocker link and `verified_blocker_evidence_nums` checks; and `octo/other#1641` (or `https://github.com/octo/other/pull/1641`) collides with local `#1641` because `owner/repo` qualifiers are discarded.
* Recommended destination: `rpi-implement` (via child remediation loop `issue-1204-rv5-fixes`).

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: CLI live-session check validates session count without optional live session identity comparison

* Evidence: tools/check-coordinator-handoff.py (`check_handoff_text`, `_build_arg_parser`, `main`) and .github/agents/ama-backlog-delivery-coordinator.agent.md (`--active-sessions`).
* Impact: When active session count stays constant (for example `1/8`), a stale session token such as `` `rpi-1100` `` passes `--expect-active-sessions 1` unless live session names can also be passed via `--active-sessions <csv>`.
* Recommended destination: `rpi-implement` (via child remediation loop `issue-1204-rv5-fixes`).

## Implementation-Time Updates and Follow-Up Assessment

* No unrecorded implementation-time divergences exist in `issue-1204-rv4-fixes`.
* Plan follow-up item (wiring `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` in a separate full-gate PR under `#1294`) remains valid and outside Focused-tier scope.

## Validation Coverage

* Ran `ruff check`, `ruff format --isolated --line-length 100 --check`, `python3 tools/check-coordinator-handoff.py`, `python3 -m unittest tools/test_check_coordinator_handoff.py -v` (`11` tests, `0.250s`), `python3 -m unittest tools/test_rpi_phase_witness.py -q` (`33` tests), and `git --no-pager diff --check`; skipped `tools/rpi-checks.py` per caller Focused-tier boundary.
