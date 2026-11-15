<!-- markdownlint-disable-file -->
# Implementation Changes: Resolve RV-001 through RV-005 Pre-Indexed Clause Raw Slices, Coordinated Wait-Segment Verification, Next-Check Capacity/Drain Tails, and Complete Subtest Coverage (Issue #1204 Child Loop 8)

## Metadata

* Task ID: issue-1204-rv8-fixes
* Task slug: delivery-1204-coordinator-guard-rv8-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan-critique.md
* Declared scope: Full plan (`P01`: `P01-T01` through `P01-T02`)
* Execution status: Complete

## Phase Execution Summary

### P01: Pre-Indexed Clause Raw Slices, Coordinated Wait-Segment Verification, Next-Check Capacity/Drain Tails, and Subtest Coverage

#### P01-T01: `RV-001`..`RV-003` and `PC-001`..`PC-003` Fixes in `tools/check-coordinator-handoff.py`

* **Pre-indexed `ClauseTokens.raw` (`RV-001`)**: Added `raw: str` to `ClauseTokens`, populated `raw=clause_raw` once inside `_build_clause_tokens`, and replaced per-match `idx.raw_text[ct.start : ct.end]` slicing in `_is_claim_negated_at` with `ct.raw`, restoring strict `O(N)` scaling across single-clause multi-match prohibition prose (`"Waiting on PR #1641; never " + ("starting #1310 " * 4000)`).
* **Coordinated wait-segment verification (`RV-002`, `PC-001`, `PC-002`)**: Added `COORDINATED_WAIT_SPLIT_RE` and `SHARED_REF_LIFECYCLE_SEG_RE`, masked `MD_LINK_RE` spans prior to splitting so `[CI and checks](...)` links are never split mid-link, extended `INTRO_PREFIX_BETWEEN_RE` and added `TRAILING_NEXT_TRIGGER_BRIDGE_RE` for adjacent multi-trigger connectors when `BLOCKER_SPAN_STOP_RE.search(..., tm.end(), next_start)` reaches `next_start`, and required each coordinated segment inside `target_span` either to carry its own blocker reference, satisfy `_is_exempt_capacity_or_drain_wait`, or match `SHARED_REF_LIFECYCLE_SEG_RE` adjacent to a cited segment.
* **Bounded next-check timing tails on capacity and drain waits (`RV-003`, `PC-003`)**: Added `NEXT_CHECK_TIMING_TAIL_PAT` immediately before `[\s)]*$` in both `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` so legitimate bounded timing suffixes (`until the next check`, `until the next scheduled check`) pass at declared session cap or under active PR drain while uncited non-capacity tails remain rejected.

#### P01-T02: `RV-001`..`RV-004` Subtests in `tools/test_check_coordinator_handoff.py` and Exact Two-File Scope (`RV-005`)

* Preserved the exact `11` `def test_*` method inventory in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new `def test_*` methods) while adding `self.subTest` blocks covering:
  * Single-clause `4000`-phrase negated launch stress (`< 0.25s`) and coordinated uncited wait segments (`and stakeholder approval`, `stakeholder approval and PR #1641`, `or external vendor`, `or owner sign-off`, below-cap `a free slot and PR #1641`, 3-item serial-comma list `PR #1641, stakeholder approval, and PR #1642`, and back-to-back triggers `Waiting on stakeholder approval and waiting on PR #1641 checks`).
  * Positive capacity and drain next-check timing suffixes (`Waiting for a free worker session slot until the next check.` at `1/1`, `Waiting on PR drain below 15 until the next scheduled check.` during PR drain), backticked `` `rpi-1310-no-push` `` launch token, bidirectional shared lifecycle attachment (`PR #1641 CI and status checks`, `PR #1641 and its hosted CI`, `CI and status checks on PR #1641`), Markdown link labels containing `and` (`[CI and checks](...)`), and compound `Paused and waiting on PR #1641.`.
  * Tableless waiting/pause reporting (`missing-classification-table` + `unverified-blocker-pause`) and classified uncited wait blocking `ready to start` work (`unsupported-waiting-ready-work` + `unverified-blocker-pause`).

## Implementation Discoveries and Local Judgment Updates

* **Immediately relevant current-state update (`P01-T01`)**: In Python's `re` engine, `Pattern.search(s, pos, endpos)` treats `endpos` as end-of-input even for positive lookaheads `(?=...)`. When two wait/blocker triggers appear consecutively (`"Waiting on #1641 and waiting on PR #1641 checks."` or `"Paused and waiting on PR #1641."`), bounding `BLOCKER_SPAN_STOP_RE.search` at `next_start` prevented its lookahead branch from stripping the trailing `" and "` connector before `next_start`, leaving a whitespace-only trailing split segment. Extending `INTRO_PREFIX_BETWEEN_RE` for compound trigger prefixes (`Paused and waiting on ...`) and stripping `TRAILING_NEXT_TRIGGER_BRIDGE_RE` over `[tm.end(), next_start)` when `stop_m is None` and `i + 1 < len(triggers)` preserved both `O(N)` bounded scanning and accurate per-segment checks. Updated `FR-02` in the plan and `P01-T01` in phase details accordingly.

## Validation Evidence

* `python3 tools/check-coordinator-handoff.py` -> exited `0` (`Coordinator handoff guard check passed (1 target(s), 0 violations).` on `.github/agents/ama-backlog-delivery-coordinator.agent.md`).
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q` -> exited `0` (`Ran 11 tests in 0.645s — OK`).
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> exited `0` (`All checks passed!`).
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> exited `0` (`2 files already formatted`).
* `python3 -m unittest tools/test_rpi_phase_witness.py -q` -> exited `0` (`Ran 33 tests in 3.528s — OK`).
* Exact two-file tracking-directory literal check (`RV-005`): `grep` for `.copilot-tracking` across `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` -> `0` matches (`No matches found.`; pre-existing RPI witness tools elsewhere under `tools/` intentionally inspect tracking directories and are outside Issue #1204's two-file scope).
* `git --no-pager diff --check` -> exited `0` (no whitespace or conflict-marker defects).
* Explicit skip: `tools/rpi-checks.py` intentionally not executed per caller Focused-tier instruction (`Do NOT run tools/rpi-checks.py`).

## Blockers and Remaining Work

* Blockers: none.
* Remaining in-scope `Pxx` / `Pxx-Txx` work: none (`P01`, `P01-T01`, and `P01-T02` complete).

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
