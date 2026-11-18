<!-- markdownlint-disable-file -->
# Phase Details: Resolve RV-001 through RV-005 Pre-Indexed Clause Raw Slices, Coordinated Wait-Segment Verification, Next-Check Capacity/Drain Tails, and Complete Subtest Coverage (Issue #1204 Child Loop 8)

## Metadata

* Task ID: issue-1204-rv8-fixes
* Task slug: delivery-1204-coordinator-guard-rv8-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-review.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan-critique.md
* Phase status: complete

<!-- rpi:phase id=P01 -->
## P01: Pre-Indexed Clause Raw Slices, Coordinated Wait-Segment Verification, Next-Check Capacity/Drain Tails, and Subtest Coverage

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `RV-001`..`RV-003` Fixes in `tools/check-coordinator-handoff.py`

#### Purpose

Eliminate per-match clause string slicing in `_is_claim_negated_at`, enforce independent blocker citation across coordinated `and`/`or`/`plus`/`as well as` wait segments, and allow bounded next-check timing qualifiers on legitimate capacity/drain wait spans.

#### Concrete Changes

1. **Pre-Indexed `ClauseTokens.raw` (`RV-001`)**:
   * Add `raw: str` field to `ClauseTokens` (`@dataclass(frozen=True)`).
   * Pass `raw=clause_raw` once inside `_build_clause_tokens(text, span_masked, c_start, c_end)`.
   * In `_is_claim_negated_at`, replace `clause_raw = idx.raw_text[ct.start : ct.end]` with `clause_raw = ct.raw` (`O(1)` reference, zero per-match string allocation).
2. **Coordinated Wait-Segment Verification (`RV-002`, `PC-001`, `PC-002`)**:
   * Define `COORDINATED_WAIT_SPLIT_RE = re.compile(r"(?:,\s*(?:(?:and|or|plus|as\s+well\s+as)\b\s*)?(?!(?:until|before|for|pending|awaiting|till|at|during|under|in|on|with|without)\b)|\b(?:and|or|plus|as\s+well\s+as)\b)", re.IGNORECASE)` and `SHARED_REF_LIFECYCLE_SEG_RE = re.compile(r"^\s*(?:(?:its|their|the)\s+)?(?:hosted\s+ci|ci|required\s+checks?|status\s+checks?|pr\s+checks?|merge\s+checks?|checks?|merge(?:ability)?|automerge|rebase|builds?|tests?|pipelines?)\s*$", re.IGNORECASE)`.
   * In `_extract_wait_and_blocker_spans`, extend `INTRO_PREFIX_BETWEEN_RE` to cover compound trigger prefixes (`Paused and waiting on ...`), strip trailing conjunction bridges right before `next_start` via `TRAILING_NEXT_TRIGGER_BRIDGE_RE` when `stop_m is None` and `i + 1 < len(triggers)` (since Python `re.Pattern.search(..., pos, endpos)` stops lookaheads at `endpos`), and compute `link_masked_span = MD_LINK_RE.sub(lambda m: "_" * len(m.group(0)), idx.span_masked_text[tm.end() : end_pos])` alongside `target_span = text[tm.end() : end_pos]`.
   * Split `target_span` at `COORDINATED_WAIT_SPLIT_RE.finditer(link_masked_span)` into `segments: list[str]`.
   * When `not target_span.strip()`: mark `has_uncited_wait = True` unless `_is_exempt_capacity_or_drain_wait(target_span, ...)`.
   * Otherwise extract `seg_refs_list = [_extract_refs_from_fragment(seg, enforce_link_validity=False, include_label_refs=True) for seg in segments]`, append unseen refs to `cited`, and verify every `j, seg in enumerate(segments)`:
     * Valid if `seg_refs_list[j]` is non-empty, OR `_is_exempt_capacity_or_drain_wait(seg, ...)`, OR `SHARED_REF_LIFECYCLE_SEG_RE.match(seg)` with `((j > 0 and bool(seg_refs_list[j - 1])) or (j + 1 < len(segments) and bool(seg_refs_list[j + 1])))`.
     * Otherwise set `has_uncited_wait = True`.
3. **Bounded Next-Check Timing Tail on Capacity/Drain Spans (`RV-003`, `PC-003`)**:
   * Define `NEXT_CHECK_TIMING_TAIL_PAT` matching `(?:(?:\s+|,\s*)(?:(?:until|before|for|pending|awaiting|till)\s+(?:(?:a|an|the)\s+)?(?:next\s+)?(?:scheduled\s+|coordinator\s+)?(?:check|tick|run|poll|cycle|pass|turn|window)|at\s+the\s+next\s+(?:scheduled\s+|coordinator\s+)?(?:check|tick|run|poll|cycle|pass|turn|window)))?`.
   * Place `NEXT_CHECK_TIMING_TAIL_PAT` after numeric drain threshold qualifiers and immediately before `[\s)]*$` in both `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE`.

#### Completion Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0` (`0` violations on `.github/agents/ama-backlog-delivery-coordinator.agent.md`) and all existing `11` test methods pass.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `RV-001`..`RV-004` Subtests in `tools/test_check_coordinator_handoff.py`, Record Exact Two-File Check Scope (`RV-005`), and Run Focused Validation

#### Purpose

Lock regression coverage for `RV-001`..`RV-004` inside existing `def test_*` methods without altering the `11`-method inventory, record exact two-file tracking-literal scope (`RV-005`), and verify Focused validation.

#### Test Ownership and Coverage Lock

* Canonical target: `tools/test_check_coordinator_handoff.py`
* Exact removals: `none`
* Maximum new `def test_*` method additions: `0` (preserve exact `11` methods; add `self.subTest` blocks inside existing methods)
* Required subtest scenarios:
  1. `RV-001`: `"never " + ("starting #1310 " * 4000)` completes in `< 0.25s` and still rejects `unsupported-waiting-ready-work` when paired with `Waiting on PR #1641;`.
  2. `RV-002`: `"Waiting on PR #1641 and stakeholder approval."`, `"Waiting on stakeholder approval and PR #1641."`, and `"Waiting on PR #1641 or external vendor."` each fail with `unverified-blocker-pause`, while `"Waiting on PR #1641 CI and status checks."` passes with `[]`.
  3. `RV-003` & `RV-004`: `"Waiting for a free worker session slot until the next check."` at `1/1` capacity and `"Waiting on PR drain below 15 until the next scheduled check."` during PR drain each pass with `[]`; `"Waiting on PR #1641 while starting `rpi-1310-no-push` now."` passes with `[]` despite `no` inside the backticked session token.
  4. `RV-005`: `delivery-1204-coordinator-guard-rv8-fixes-changes.md` explicitly records the tracking-directory literal assertion against `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`.

#### Validation Commands

* `python3 -m unittest tools/test_check_coordinator_handoff.py -q`
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`
* `python3 tools/check-coordinator-handoff.py`
* `python3 -m unittest tools/test_rpi_phase_witness.py -q`
