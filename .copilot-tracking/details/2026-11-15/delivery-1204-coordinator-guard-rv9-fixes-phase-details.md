<!-- markdownlint-disable-file -->
# Phase Details: Resolve RV-001 through RV-007 Quoted Prohibition Attribute Fix, Linear Bridge/Session Indexing, Causal Blocker Verification, Bare Pause Enforcement, Comma Timing Lookahead, and Contiguous Lifecycle Chains (Issue #1204 Child Loop 9)

## Metadata

* Task ID: issue-1204-rv9-fixes
* Task slug: delivery-1204-coordinator-guard-rv9-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-plan.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-review.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-plan-critique.md
* Phase status: complete

<!-- rpi:phase id=P01 -->
## P01: Quoted Prohibition Fix, Linear Bridge and Session Indexing, Causal/Pause Blocker Guards, and Subtest Coverage

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `RV-001`..`RV-007` Fixes in `tools/check-coordinator-handoff.py`

#### Purpose

Eliminate the `_fallback_prohibition_check` `pm.end` crash, remove quadratic regex/nested-loop hotspots in multi-trigger bridge trimming and custom session coverage, enforce causal blocker verification and bare `Status: paused.` checks, fix comma-prefixed timing lookahead backtracking, and propagate contiguous shared lifecycle chains.

#### Concrete Changes

1. **Outer-vs-Inner Quoted Prohibition Evaluation and Quote-Interior Clause Masking (`RV-001`, `PC-002`)**:
   * In `_build_clause_index`, build `clause_split_masked` from `span_masked` by masking interior characters of closed `INLINE_LITERAL_SPAN_RE` spans (`m.group(0)[0] + "_" * (len(m.group(0)) - 2) + m.group(0)[-1]`) for `CLAUSE_SPLIT_RE` and `SENTENCE_SPLIT_RE` boundary discovery only (keeping `raw_text` and `span_masked_text` unchanged so affirmative quoted claims still trigger).
   * In `_fallback_prohibition_check(ct, clause_raw, rel_pos, *, only_literal_end=None)`, replace `clause_raw[pm.end() : rel_pos]` with `clause_raw[pm.end : rel_pos]`; when `only_literal_end is not None`, restrict evaluation to inner prohibitions with `pm.inside_literal_end == only_literal_end` and skip any inner prohibition where `CLAUSE_SPLIT_RE.search(clause_raw, pm.end, rel_pos)` matches.
   * In `_is_claim_negated_at`, when `ct.lit_starts[li] < rel_pos < ct.lit_ends[li]`, evaluate outer prohibitions (`pm.inside_literal_end is None`) at `lit_s` via the indexed token path AND fall back to `_fallback_prohibition_check(..., only_literal_end=ct.lit_ends[li])` for inner prohibitions inside that literal.
2. **Linear `_strip_trailing_trigger_bridge` Including Causal Connectors (`RV-002`, `PC-001`)**:
   * Remove `TRAILING_NEXT_TRIGGER_BRIDGE_RE`.
   * Implement `_strip_trailing_trigger_bridge(span_masked: str, start: int, end: int) -> int` that trims trailing whitespace, strips trailing coordinating or causal connector phrases (`as well as`, `because of`, `due to`, `owing to`, `because`, `and`, `or`, `also`, `plus`) when bounded by whitespace or comma, or strips a trailing comma, in strictly linear backward character checks; include the same connectors in `INTRO_PREFIX_BETWEEN_RE`.
3. **Pre-Indexed Custom Session Issue Numbers (`RV-003`)**:
   * Define `STANDALONE_ISSUE_NUM_RE = re.compile(r"(?<!\d)(\d+)(?!\d)")`.
   * Before iterating `active_session_rows`, compute `custom_session_issue_nums: set[int] = {int(m.group(1)) for custom_tok in custom_non_rpi_tokens for m in STANDALONE_ISSUE_NUM_RE.finditer(custom_tok)}` once (`O(S)`), and check `if row_num in custom_session_issue_nums: continue` in `O(1)`.
4. **Bounded Causal Blocker Splitting, Non-Backtracking Comma Lookahead, and Contiguous Lifecycle Propagation (`RV-004`, `RV-006`, `RV-007`, `PC-001`)**:
   * Update `COORDINATED_WAIT_SPLIT_RE` so the negative lookahead sits immediately after `,`, optional post-comma connectors consume coordinating, causal, and non-timing `pending|awaiting` tokens, non-comma connector branches require surrounding non-whitespace (`(?<=\S)[ \t]+...(?=[ \t]+\S)`), and `pending|awaiting` carries copular/aspectual negative lookbehinds (`(?<!\bis)(?<!\bare)(?<!\bwas)(?<!\bwere)(?<!\bbe)(?<!\bbeen)(?<!\bstill)(?<!\bremain)(?<!\bremains)`).
   * Update `SHARED_REF_LIFECYCLE_SEG_RE` to allow optional leading `(?:of\s+)?` and optional trailing lifecycle state (`(?:\s+(?:(?:is|are)\s+(?:still\s+)?(?:running|pending|queued|in\s+progress)|to\s+(?:pass|complete|finish|succeed)))?`).
   * In `_extract_wait_and_blocker_spans`, compute `life_attached: list[bool]` across `segments` using one forward sweep and one backward sweep so any contiguous run of `SHARED_REF_LIFECYCLE_SEG_RE` segments adjacent to a cited segment is accepted.
5. **Bare Pause Status and Subject-First Pause Enforcement (`RV-005`, `PC-001`)**:
   * Add `status:\s*paus(?:ed|ing|e)\b`, `paused\s+summary\b`, `all\s+lanes\s+paused\b`, and `(?:(?:scheduled\s+)?check|(?:coordinator\s+)?run|delivery|schedule|tick)\s+(?:is\s+)?paus(?:ed|ing)\b` (with optional `on|for|until|due to|because(?: of)?|owing to` introducer tails in `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`) to `CLAUSE_SPLIT_RE`, `WAITING_OR_PAUSE_RE`, `DIRECT_GLOBAL_WAIT_RE`, and `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`.

#### Completion Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0` (`0` violations on `.github/agents/ama-backlog-delivery-coordinator.agent.md`) and `python3 -m mypy tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` exits `0`.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `RV-001`..`RV-007` Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

#### Purpose

Lock regression coverage for `RV-001`..`RV-007` inside existing `11` test methods without adding or removing `def test_*` methods, and run Focused validation.

#### Test Ownership and Coverage Lock

* Canonical target: `tools/test_check_coordinator_handoff.py`
* Exact removals: `none`
* Maximum new `def test_*` method additions: `0` (preserve exact `11` methods; add `self.subTest` blocks inside existing methods)
* Required subtest scenarios:
  1. `RV-001` & `PC-002`: Non-coincidental uncited/ready-work quoted prohibitions (`Never say "we are waiting on stakeholder approval".`, `Do not report "Current status: paused" without a blocker link.`, `Do not report "Idle tick: nothing changed".` with a `ready to start` row, and `Note: "We never report waiting on stakeholder approval."`) evaluate with `0` violations, while negative controls (`Summary: "Never skip checks; status: paused."` and `Never skip lint when saying "we are waiting on stakeholder approval".`) still trigger `unverified-blocker-pause`.
  2. `RV-002`: `"Waiting on PR #1641" + (" " * 20000) + "and waiting on PR #1641 checks."` completes in `< 0.15s` with `[]`.
  3. `RV-003`: `1200` `active session` rows matched against `1200` custom non-`rpi-` session tokens (`worker-1`..`worker-1200`) completes in `< 0.25s` with `[]`.
  4. `RV-004`, `PC-001`, & `PC-003`: `"Waiting on PR #1641 because stakeholder approval is pending."`, `"Waiting on PR #1641 due to owner sign-off."`, and `"Waiting on PR #1641 pending stakeholder approval."` fail with `unverified-blocker-pause`, while `"Waiting on PR #1641 because #1288#issuecomment-10 is pending."`, `"Waiting on PR #1641, pending #1288#issuecomment-10."`, `"Waiting on PR #1641 because its hosted CI is running."`, `"Waiting on PR #1641 and its checks are pending."`, and `"Waiting on PR #1641 because blocked on #1288#issuecomment-10."` pass with `[]`.
  5. `RV-005` & `PC-001`: Tableless `"Status: paused."` with open issues fails with both `missing-classification-table` and `unverified-blocker-pause`, and classified `"Status: paused."` / `"Scheduled check paused."` without a blocker citation fails with `unverified-blocker-pause`, while `"Status: paused on PR #1641."` and `"Status: paused due to PR #1641."` pass when classified.
  6. `RV-006`: `"Waiting for a free worker session slot, until the next check."` at `1/1` capacity and `"Waiting for open PRs to drain below 10, pending the next check."` during PR drain pass with `[]`.
  7. `RV-007`: `"Waiting on PR #1641 and its hosted CI and status checks."` passes with `[]`, while `"Waiting on PR #1641 and its hosted CI and stakeholder approval."` fails with `unverified-blocker-pause`.

#### Validation Commands

* `python3 -m unittest tools/test_check_coordinator_handoff.py -q`
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`
* `python3 -m mypy tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`
* `python3 tools/check-coordinator-handoff.py`
* `python3 -m unittest tools/test_rpi_phase_witness.py -q`
