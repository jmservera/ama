<!-- markdownlint-disable-file -->
# Phase Details: Resolve RV-001 through RV-006 Single-Subclause Hold Indexing, Independent Multi-Trigger Spans, Strict Capacity/Drain Anchors, Bare Self-URL Rejection, Tableless Blocker Checks, and Mixed Declared Session Matching (Issue #1204 Child Loop 7)

## Metadata

* Task ID: issue-1204-rv7-fixes
* Task slug: delivery-1204-coordinator-guard-rv7-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-review.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan-critique.md
* Phase status: complete

<!-- rpi:phase id=P01 -->
## P01: Single-Subclause O(N) Hold Indexing, Per-Trigger Wait Spans, Strict Capacity Anchors, Bare Self-URL Rejection, Tableless Blocker Guard, and Mixed Session Matching

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `RV-001`..`RV-006` Fixes in `tools/check-coordinator-handoff.py`

#### Purpose

Close all six edge-case findings (`RV-001`..`RV-006`) and critique refinements (`PC-001`..`PC-004`) in `tools/check-coordinator-handoff.py` with strict linear `O(N)` scaling and zero false positives.

#### Concrete Changes

1. **Single-Subclause `O(N)` Hold/Non-Current Memoization (`RV-001`, `PC-004`)**:
   * In `_launched_ready_issues_in_current_tick`, maintain `non_current_by_subclause: dict[int, bool]` and `min_hold_end_by_subclause: dict[int, int]` (using `-1` when no hold/negation match exists in `[sub_start, sub_end)`).
   * Check `si not in non_current_by_subclause` scanning `NON_CURRENT_LAUNCH_SUBCLAUSE_RE.search(idx.span_masked_text, sub_start, sub_end)` first; if `non_current_by_subclause[si]` is `True`, `continue` immediately.
   * Check `si not in min_hold_end_by_subclause` computing `min((hm.end() for hm in LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE.finditer(idx.span_masked_text, sub_start, sub_end)), default=-1)` once per `si`; if `min_hold_end != -1 and min_hold_end <= m.start()`, `continue`.
2. **Independent Per-Trigger Wait/Blocker Span Clamping (`RV-002`)**:
   * In `_extract_wait_and_blocker_spans`, collect `triggers = [tm for tm in WAIT_OR_BLOCKER_SPAN_TRIGGER_RE.finditer(text) if not _is_claim_negated_at(idx, tm.start())]`.
   * Define `INTRO_PREFIX_BETWEEN_RE = re.compile(r"^[\s:,\-\u2013\u2014]*$")`.
   * For `i, tm in enumerate(triggers)`: compute `natural_end` from `BLOCKER_SPAN_STOP_RE.search(idx.span_masked_text, tm.end())`; if `i + 1 < len(triggers)` and `triggers[i + 1].start() < natural_end`:
     * If `INTRO_PREFIX_BETWEEN_RE.match(text[tm.end() : triggers[i + 1].start()])`: `continue`.
     * Otherwise clamp `end_pos = triggers[i + 1].start()`.
3. **Head-Anchored Capacity and PR-Drain Wait Exemption (`RV-003`, `PC-002`)**:
   * Evaluate `_is_exempt_capacity_or_drain_wait(target_span, *, at_session_capacity, pr_drain_active)` on `target_span = text[tm.end():end_pos]`:
     * Reject immediately if `EXTRA_BLOCKER_CONJUNCTION_RE` (`\b(?:and|or|plus|because|due\s+to)\b`) or `NON_CAPACITY_BLOCKER_WORD_RE` (`\b(?:approv\w*|stakeholders?|owners?|reviews?|humans?|sign-?offs?|decisions?|feedback|input|repl(?:y|ies)|responses?|clearances?|permissions?|legal|security|outages?|upstream|ci|checks|(?:ci|pr|hosted|status|required|merge)\s+check|plans?)\b`) matches `target_span`.
     * Anchor `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` to the head of `target_span` (`^\s*(?:(?:on|for|until|at|during|under)\s+)?(?:(?:a|an|the|any|next|active)\s+)?...`).
4. **Bare Self-Issue GitHub URL Rejection (`RV-004`, `PC-001`)**:
   * Add `BARE_GITHUB_ISSUE_URL_RE = re.compile(r"^(?:https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/|(?:(?:\./)?|/)?(?:([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/)?)issues/(\d+)/?$", re.IGNORECASE)`.
   * Helper `_infer_row_repo_key(raw_issue: str) -> str`: inspect `MD_LINK_RE`, `URL_RE`, and `_iter_issue_refs` on `raw_issue`, returning normalized repo key (`""` for default `jmservera/ama` or unqualified `#<N>`).
   * Helper `_is_bare_self_issue_url(url: str, issue_number: int | None, self_repo_key: str = "") -> bool`: strip whitespace and trailing `.,;:!?`; if `issue_number is None`: return `False`; split `#` fragment — if `frag_clean` is non-empty and `frag_clean != str(issue_number)`, return `False`; strip `?query`; match `BARE_GITHUB_ISSUE_URL_RE`: return `int(num) == issue_number and (repo is None or _normalize_repo_key(repo) == _normalize_repo_key(self_repo_key))`.
   * Enforce `_is_bare_self_issue_url` in both `_inspect_blocker_links` and `_extract_refs_from_fragment` (when `enforce_link_validity=True`).
5. **Tableless and Ready-Work `blocked on/by` Enforcement (`RV-005`, `PC-003`)**:
   * Emit `unverified-blocker-pause` unconditionally on `has_unverified_phrase or has_uncited_non_capacity_wait`; gate `missing-classification-table`, `summary-before-classification-table`, `unsupported-idle-unclassified`, and `unsupported-waiting-ready-work` on `has_blocker_or_wait_claim = is_waiting_or_pause or bool(cited_blocker_refs) or has_uncited_non_capacity_wait or has_unverified_phrase`; include `\bblocked\s+(?:on|by)\b` before `HOLD_CONTINUATION_RE` in `_has_global_wait_or_pause`.
6. **Mixed Declared Session Active-Row Coverage (`RV-006`)**:
   * Pass `require_active_rows_covered=True` when calling `_verify_sessions_against_table` on non-empty `listed_session_tokens`.

#### Completion Expectations

* `python3 tools/check-coordinator-handoff.py` exits `0` with `0` violations; all `RV-001`..`RV-006` and `PC-001`..`PC-004` reproducers are caught cleanly.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `RV-001`..`RV-006` and `PC-001`..`PC-004` Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

#### Purpose

Lock regression subtests for `RV-001`..`RV-006` and `PC-001`..`PC-004` inside existing `11` test methods in `tools/test_check_coordinator_handoff.py` and verify Focused checks.

#### Concrete Changes

* Preserve exact `11` `def test_*` methods (`0` removals, `0` new `def test_*` methods):
  * `RV-004` + `PC-001`: bare `https://github.com/jmservera/ama/issues/1288`, `[self](https://github.com/jmservera/ama/issues/1288)`, `[self](issues/1288)`, and `https://github.com/jmservera/ama/issues/1288#1288` emit `missing-blocker-link`, while `https://github.com/octo/other/issues/1288` passes.
  * `RV-005` + `PC-003`: tableless `"Blocked on stakeholder approval."` emits `unverified-blocker-pause` + `missing-classification-table`; `"Blocked on #1288."` below capacity with unlaunched `#1310` `ready to start` emits `unsupported-waiting-ready-work`.
  * `RV-002` + `RV-003` + `PC-002`: `"Waiting on PR #1641 because pausing the run for stakeholder approval."`, `"Waiting for stakeholder approval of the capacity plan."`, and `"Waiting for user input at 1/1 active sessions."` emit `unverified-blocker-pause`, while `"Waiting for a free worker session slot until the next check."` at `1/1` capacity passes.
  * `RV-006`: mixed declared sessions `2/8 (\`rpi-1302\`, \`maintenance\`)` with `#1204` and `#1302` `active session` rows emits `stale-session-classification`, while `1/8 (\`maintenance\`)` with `0` `active session` rows passes.
  * `RV-001` + `PC-004`: single-subclause `("starting #1310 " * 2000) + "after approval"`, `"not starting #1310 " * 2000`, and hold-free multi-ready single-subclause launches complete in `< 0.20s`, and backticked `` `rpi-1310-no-push` `` does not false-suppress `starting #1311`.

#### Completion Expectations

* `python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `ruff check`, `ruff format --isolated --line-length 100 --check`, and `test_rpi_phase_witness.py` all exit `0`.
