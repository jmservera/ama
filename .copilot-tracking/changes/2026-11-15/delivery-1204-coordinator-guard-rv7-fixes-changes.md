<!-- markdownlint-disable-file -->
# Implementation Changes: Resolve RV-001 through RV-006 Single-Subclause Hold Indexing, Independent Multi-Trigger Spans, Strict Capacity/Drain Anchors, Bare Self-URL Rejection, Tableless Blocker Checks, and Mixed Declared Session Matching (Issue #1204 Child Loop 7)

## Metadata

* Task ID: issue-1204-rv7-fixes
* Task slug: delivery-1204-coordinator-guard-rv7-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan-critique.md
* Declared scope: Full plan (`P01`: `P01-T01` through `P01-T02`)
* Execution status: Complete

## Phase Execution Summary

### P01: Single-Subclause O(N) Hold Indexing, Per-Trigger Wait Spans, Strict Capacity Anchors, Bare Self-URL Rejection, Tableless Blocker Guard, and Mixed Session Matching

* Completed `P01-T01` in `tools/check-coordinator-handoff.py`:
  * `RV-001` / `PC-004`: Memoized `non_current_by_subclause` and `min_hold_end_by_subclause` (integer sentinel `-1` via `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE.search(idx.span_masked_text, sub_start, sub_end)`) per subclause index `si` in `_launched_ready_issues_in_current_tick`, eliminating quadratic prefix rescanning inside single long subclauses.
  * `RV-002`: Evaluated every unnegated `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` match independently in `_extract_wait_and_blocker_spans`, skipping only pure introductory prefixes (`INTRO_PREFIX_BETWEEN_RE`) and bounding `BLOCKER_SPAN_STOP_RE.search` by `next_start` so stop scanning remains strictly telescoping `O(N)`.
  * `RV-003` / `PC-002`: Added `_is_exempt_capacity_or_drain_wait` with full-span head/tail anchored `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE`, rejecting coordinating/causal extra-blocker conjunctions (`EXTRA_BLOCKER_CONJUNCTION_RE`) and non-capacity blocker vocabulary (`NON_CAPACITY_BLOCKER_WORD_RE`) while preserving singular `"next check"` prose.
  * `RV-004` / `PC-001`: Added `_is_bare_self_issue_url` (`BARE_GITHUB_ISSUE_URL_RE`) aligned with `_normalize_repo_key(DEFAULT_LOCAL_REPO) == ""` and enforced it in both `_inspect_blocker_links` and `_extract_refs_from_fragment` (`enforce_link_validity=True`), rejecting fragment-free or `#<self>`-fragment self-issue GitHub/relative URLs while preserving `#issuecomment-...` fragments, `/pull/<n>` URLs, and cross-repository `/issues/<self>` URLs.
  * `RV-005` / `PC-003`: Emitted `unverified-blocker-pause` unconditionally on `has_unverified_phrase or has_uncited_non_capacity_wait`, gated table-presence, ordering, unclassified, and ready-work checks on `has_blocker_or_wait_claim`, and extended `WAITING_ON_FOR_RE` to match `blocked on|by` before `HOLD_CONTINUATION_RE` in `_has_global_wait_or_pause`.
  * `RV-006`: Enabled `require_active_rows_covered=True` unconditionally whenever `listed_session_tokens` is non-empty so mixed declared session lists still require every `active session` row to match an active tmux session token.
* Completed `P01-T02` in `tools/test_check_coordinator_handoff.py`:
  * Preserved all `11` existing `def test_*` methods (`0` removed, `0` new methods added) and added focused `self.subTest` regression cases covering `RV-001` (`2,500`-repeat single-subclause hold and trailing non-current qualifier under `0.25s`), `RV-002` (multi-trigger spans where a verified blocker precedes an uncited second trigger plus introductory `Status: waiting — blocked on PR #1641` acceptance), `RV-003` (capacity/drain spoofing with stakeholder/owner/plan/vendor phrases at `1/1` cap or PR drain), `RV-004` (bare self-issue GitHub/relative URLs with or without `#<self>` rejected while `#issuecomment-42` and external-repo `/issues/1288` pass), `RV-005` (`Blocked on stakeholder approval.` without a table and `Blocked on PR #1641 before starting new work; starting #1310 now.` with ready work), and `RV-006` (mixed `rpi-1302, maintenance` catching unbacked `#1204 | active session` while `1/8 (maintenance)` with zero active rows passes).

## Implementation-Time Updates and Local Refinements

* Local judgment (`FR-01`, `FR-02`, `FR-03` preserved intent): Used `.search(masked, sub_start, sub_end)` in `_launched_ready_issues_in_current_tick` (non-overlapping leftmost regex match yields exact minimum `.end()` without scanning past the first hold token), passed `next_start` as `endpos` to `BLOCKER_SPAN_STOP_RE.search(idx.span_masked_text, tm.end(), next_start)` so `400+` repeated triggers in a punctuation-free span remain strictly `O(N)`, and anchored the tail of `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` so arbitrary trailing words (`Waiting for a free slot for external vendor.`) also fail exemption.

## Validation Evidence

* `python3 tools/check-coordinator-handoff.py`: Passed (`1 target(s), 0 violations`).
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q`: Passed (`Ran 11 tests in 0.526s OK`).
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: Passed (`All checks passed!`).
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`: Passed (`2 files already formatted`).
* `python3 -m unittest tools/test_rpi_phase_witness.py -q`: Passed (`Ran 33 tests in 3.082s OK`).
* `git --no-pager diff --check`, JSON schema parse across `.copilot-tracking/rpi-sessions/2026-11-15/*.json`, `11`-method test ownership assertion, and zero-literal tracking-directory check across `tools/`: Passed.
* `python3 tools/rpi-checks.py`: Skipped explicitly per user instructions (Focused tier).

## Blockers and Remaining Work

* Blockers: none.
* Remaining work in declared scope: none (`P01`, `P01-T01`, and `P01-T02` complete).

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
