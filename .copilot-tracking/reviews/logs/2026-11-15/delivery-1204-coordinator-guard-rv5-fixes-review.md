<!-- markdownlint-disable-file -->
# Review Log: Resolve RV-001 through RV-005 Linear-Time Clause Indexing, Wrapped Summary Normalization, Blocker Column/Repo Scoping, and Live Session Identity Verification (Issue #1204 Child Loop 5)

## Metadata

* Task ID: issue-1204-rv5-fixes
* Task slug: delivery-1204-coordinator-guard-rv5-fixes
* Parent task ID: issue-1204-rv4-fixes (`delivery-1204-coordinator-guard-rv4-fixes`)
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan-critique.md
* Changes log: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-changes.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* HVE assessment: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md
* Review execution status: Complete
* Outcome: Defects found

## Scope and Compared Artifacts

Single-pass post-implementation review across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md`, `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md`, `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-changes.md`, and `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`, assisted by an independent read-only `rubber-duck` lens.

Reconciliation check:

* Plan checklist markers (`P01`, `P01-T01`..`P01-T03`), phase details (`Phase status: complete`), changes log (`Execution status: Complete`), and HVE SHA-256 (`1396ccb0d535ac1280b24fcd0b8c2ebedcdf39079d5274441bfdbe757cda8b5a`) are reconciled.
* Critique dispositions `PC-001`..`PC-003` were applied in `P01`.
* Focused validation commands passed (`11` test methods in `0.431s`, `ruff check`, `ruff format --isolated --line-length 100 --check`, `test_rpi_phase_witness.py` `33` tests), but independent adversarial review uncovered five concrete residual bypasses (`RV-001`..`RV-005`).

## Findings

### RV-001: Quadratic Subclause Rescanning Remains in `_launches_ready_issue_in_current_tick`

* Severity: High
* Category: Defect (`NFR-01` linear scaling)
* Evidence: In `tools/check-coordinator-handoff.py` (`_launches_ready_issue_in_current_tick`), every `READY_LAUNCH_RE` match runs `SUBCLAUSE_SPLIT_RE.finditer(idx.span_masked_text, c_start, c_end)` across the full enclosing clause. Repeating `"while will be starting #1310 "` 1,000 / 2,000 / 4,000 times inside one clause scales quadratically (`~0.47s` / `~1.86s` / `~7.44s`).
* Routing destination: `rpi-implement` (precompute `subclause_starts` / `subclause_ends` once in `ClauseIndex` so subclause lookup uses `O(log N)` binary search, memoize subclause non-current checks per subclause index, and add a `< 0.15s` 4,000-repetition scaling subtest).

### RV-002: Concurrent-Launch Check Allows Waiting When Only One of Multiple `ready to start` Issues Is Started Below Capacity

* Severity: High
* Category: Defect (`AC1` / `AC2` / `AC4`)
* Evidence: In `tools/check-coordinator-handoff.py` (`_launches_ready_issue_in_current_tick` and `_validate_section`), `_launches_ready_issue_in_current_tick` returns `True` as soon as *any* single `ready_issue_nums` target is actively launched. If both `#1310` and `#1311` are classified `ready to start` with `Active sessions: 1/8` (`7` open session slots), `"Waiting on PR #1641 while starting #1310 now."` passes while leaving `#1311` untouched.
* Routing destination: `rpi-implement` (accumulate launched `ready to start` issue numbers across the section's prose blocks and require every actionable `ready to start` issue up to available session/PR admission capacity to be actively started when reporting lane-specific waiting, aligning `.agent.md` wording accordingly).

### RV-003: Generic Unverified Pause/Waiting Claims Without Any Cited Blocker Reference Pass Validation

* Severity: High
* Category: Defect (`AC1` / `AC4` unverified blocker pause)
* Evidence: In `tools/check-coordinator-handoff.py` (`_validate_section`), blocker reference verification only iterates `for ref_repo, ref_num in cited_blocker_refs:`. When `cited_blocker_refs` is empty (for example `"Pausing the run due to an approval from another stakeholder."` while `#1288` happens to sit in `human-blocked` in the table and `ready_rows` is empty), the unverified pause passes without citing any classified issue, PR, or URL from the table.
* Routing destination: `rpi-implement` (require every unnegated waiting/pause summary block—unless waiting on declared session-slot saturation or active PR-drain hysteresis—to cite at least one verified blocker reference or blocked/active issue from the classification table, and check every individual wait/pause trigger span so an uncited pause clause is not masked by a separate cited wait clause).

### RV-004: Markdown Link Labels Can Fabricate Verified Blocker Evidence When Label and Target Numbers Diverge

* Severity: Medium
* Category: Defect (`AC2` / `AC4` blocker link evidence)
* Evidence: In `tools/check-coordinator-handoff.py` (`_extract_refs_from_fragment`), `[PR #999](https://github.com/jmservera/ama/pull/1641)` emits both `("", 1641)` from the URL target and `("", 999)` from the Markdown label. Placed in a table blocker cell, that fabricated `#999` label enters `verified_blocker_evidence_refs`, allowing `"Waiting on PR #999."` to pass without verified link evidence for `#999`.
* Routing destination: `rpi-implement` (in table blocker evidence extraction, credit only verified link-target references from `[label](target)` pairs—and flag mismatched `#<n>` link labels whose repo/number differs from both the link target and the row's own issue—while in prose blocker citation extraction continue requiring both label and target references to be verified).

### RV-005: `active session` Table Rows Are Not Verified Against Live `--active-sessions` Identities

* Severity: Medium
* Category: Defect (`AC3` / `AC4` live session refresh)
* Evidence: In `tools/check-coordinator-handoff.py` (`_validate_section`), `--active-sessions` checks whether `live_tok` conflicts with a non-`active session` row in `classified_by_num`, but neither rejects an `active session` row `#1204` when the only live session is `rpi-999` (`Active sessions: 1/8 (\`rpi-999\`)`), nor flags an unclassified live `rpi-999` session missing from the classification table.
* Routing destination: `rpi-implement` (when `active_sessions` is supplied on `is_latest` sections—and for `listed_session_tokens` in `Active sessions:`—require every `active session` row `#N` to match at least one live/declared session referencing issue `N`, and require every issue-scoped `rpi-<N>` session to appear in the classification table as `active session`).

## Assessment of Implementation Decisions and Plan Follow-Ups

* Descriptive implementation updates (`ruff format` line wrap) preserved user intent.
* Existing plan follow-up (`Wire python3 tools/check-coordinator-handoff.py into tools/rpi-checks.py static validation in a dedicated gate-tooling PR`) remains out of scope for Focused validation.

## Validation Summary

* Executed: `python3 -m unittest tools/test_check_coordinator_handoff.py -v` (`11` tests, `0.431s`, `OK`), `python3 -m ruff check` (`0`), `python3 -m ruff format --isolated --line-length 100 --check` (`0`), `python3 tools/check-coordinator-handoff.py` (`0`), `python3 -m unittest tools/test_rpi_phase_witness.py -q` (`33` tests, `OK`).
* Skipped by caller instruction: `tools/rpi-checks.py`.

## Routing Summary

* `RV-001`..`RV-005` -> `rpi-implement` in child follow-up task (`issue-1204-rv6-fixes`).
