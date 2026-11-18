<!-- markdownlint-disable-file -->
# Plan Critique: Resolve RV-001 through RV-007 Fallback Prohibition Crash, Linear Bridge Trimming, Pre-Indexed Session Numerals, Causal/Pause Coverage, and Subtest Matrix (Issue #1204 Child Loop 9)

## Metadata

* Task ID: issue-1204-rv9-fixes
* Task slug: delivery-1204-coordinator-guard-rv9-fixes
* Assessed plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-plan.md
* Assessed phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-phase-details.md
* Supplied evidence: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, tools/check-coordinator-handoff.py, tools/test_check_coordinator_handoff.py, .github/agents/ama-backlog-delivery-coordinator.agent.md
* Critique execution status: Complete
* Verdict: Revise

## Criterion Boundary and Coverage Assessment

Assessed `FR-01`..`FR-06`, `NFR-01`..`NFR-02`, `P01-T01`..`P01-T02`, the 11-method test ownership lock in `tools/test_check_coordinator_handoff.py`, regex edge cases, worst-case backtracking behavior on 50,000-character pathological inputs, and false-positive risk against `.github/agents/ama-backlog-delivery-coordinator.agent.md`.

* `.github/agents/ama-backlog-delivery-coordinator.agent.md` false-positive check: Verified clean (`check_agent_instructions` returns `[]` under `FR-01`..`FR-05` and with `PC-001`..`PC-002` applied).
* Backtracking check (`FR-02`, `FR-04`, `FR-05`, `NFR-01`): Verified linear `< 5 ms` runtime on 50,000-character non-matching whitespace and repetition inputs across `_strip_trailing_trigger_bridge`, `INTRO_PREFIX_BETWEEN_RE`, `SESSION_CAPACITY_WAIT_SPAN_RE`, `PR_DRAIN_WAIT_SPAN_RE`, `COORDINATED_WAIT_SPLIT_RE`, and `SHARED_REF_LIFECYCLE_SEG_RE`.
* `FR-01` (`RV-001` / `RV-007` quoted prohibition negation): Replacing `pm.end()` with `pm.end` resolves the `TypeError`, but multi-token and colon/period-containing outer quoted prohibitions still evaluate `_is_claim_negated_at == False` (`PC-002`).
* `FR-02` (`RV-002` linear trailing bridge trimming): Linear scan eliminates `O(N^2)` backtracking, but omits causal connectors (`because`, `because of`, `due to`, `owing to`) between adjacent wait/blocker triggers (`PC-001`).
* `FR-03` (`RV-003` `STANDALONE_ISSUE_NUM_RE` pre-indexing): Credible and exact; reduces custom session matching in `_verify_sessions_against_table` to `O(C + A)` without runtime regex compilation.
* `FR-04` and `FR-05` (`RV-004` / `RV-005` causal/pending splits and bare/subject-first pause triggers): Require targeted regex boundary fixes (`PC-001`) because `COORDINATED_WAIT_SPLIT_RE` splits predicative `is pending` / `are pending`, post-comma `, pending <ref>`, and leading `Status: paused due to/pending <ref>` spans into empty uncited segments, breaking `P01-T02`'s own `RV-004` positive subtest.
* `FR-06` (`RV-006` / `RV-007` subtest coverage): Preserves the 11 `def test_*` methods, but needs uncited/ready-work quoted prohibition assertions (`PC-002`) and table-anchor alignment on `#1288#issuecomment-10` vs `#1288#issuecomment-42` (`PC-003`).
* Limitations: None; all supplied artifacts and target source files were inspected directly.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `COORDINATED_WAIT_SPLIT_RE`, `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`, and `_strip_trailing_trigger_bridge` Emit Empty Uncited Segments on Predicative `is/are pending`, `, pending <ref>`, Leading Causal Pause Tails, and Causal Multi-Trigger Bridges

* Related IDs: `FR-04`, `FR-05`, `FR-02`, `P01-T01`, `P01-T02`
* Evidence:
  1. `FR-04` appends `|\b(?:pending|awaiting)\b(?![ \t]+...)` to `COORDINATED_WAIT_SPLIT_RE`. On `P01-T02` item 4's own positive case (`"Waiting on PR #1641 because #1288#issuecomment-42 is pending."`), `COORDINATED_WAIT_SPLIT_RE` splits at `\bbecause\b` and then splits again at trailing predicative `pending`, producing `[' PR #1641 ', ' #1288#issuecomment-42 is ', '']`. The empty final segment `''` has no refs, is not capacity-exempt, and fails `SHARED_REF_LIFECYCLE_SEG_RE`, raising a false-positive `unverified-blocker-pause`. For the same reason, `FR-04`'s addition of `(?:is|are)\s+pending` to `SHARED_REF_LIFECYCLE_SEG_RE` is unreachable on `"Waiting on PR #1641 and its checks are pending."` because `"its checks are pending"` is split into `"its checks are "` and `""` before `SHARED_REF_LIFECYCLE_SEG_RE` runs.
  2. In `", pending #1288#issuecomment-10"`, the comma branch of `COORDINATED_WAIT_SPLIT_RE` does not consume optional post-comma non-timing `(?:pending|awaiting)\b`, so `,` and `\bpending\b` match consecutively and emit an empty middle segment `''` (`[' PR #1641', '', ' #1288#issuecomment-10']`).
  3. `FR-05` adds `status:\s*paus(?:e|ed|ing)\b`, `paused\s+summary\b`, `all\s+lanes\s+paused\b`, and `(?:(?:scheduled\s+)?check|(?:coordinator\s+)?run|delivery|schedule|tick)\s+(?:is\s+)?paus(?:ed|ing)\b` to `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` without optional target-introducer prepositions (`on|for|until|due to|because(?: of)?|owing to`), and orders `paus(?:e|ed|ing)` with `e` before `ed` (which greedily matches `"pause"` inside `"paused"` if `\b` is not kept immediately on `paus(?:ed|ing|e)\b`). Because non-comma `COORDINATED_WAIT_SPLIT_RE` branches lack a preceding non-whitespace guard `(?<=\S)`, cited pause prose such as `"Status: paused due to PR #1641."`, `"Scheduled check paused because of PR #1641."`, and `"Status: paused pending #1288#issuecomment-10."` splits at the leading connector into `[' ', ' PR #1641']`, falsely triggering `unverified-blocker-pause`.
  4. When two triggers are joined by a causal bridge (`"Waiting on PR #1641 because blocked on #1288#issuecomment-10."` or `"Waiting on PR #1641 due to waiting on #1288#issuecomment-10."`), `FR-02`'s `_strip_trailing_trigger_bridge` and `INTRO_PREFIX_BETWEEN_RE` only handle `and|or|also|plus|as well as`, leaving trailing `' because '` on trigger 0 which `COORDINATED_WAIT_SPLIT_RE` splits into `[' PR #1641', '']`.
* Impact: Breaks `P01-T02`'s own `RV-004` positive subtest, leaves `(?:is|are)\s+pending` in `SHARED_REF_LIFECYCLE_SEG_RE` dead, and causes false-positive `unverified-blocker-pause` violations on valid cited causal and `pending` wait/pause summaries.
* Action owner: Planner (`direct_planner_correction`, user response required: `no`)
* Exact resolving evidence:
  * In `COORDINATED_WAIT_SPLIT_RE`, require non-comma connector branches to be bounded by non-whitespace tokens (`(?<=\S)[ \t]+...(?=[ \t]+\S)`), guard the `pending|awaiting` branch with negative lookbehinds for copular/aspectual predicates (`(?<!\bis)(?<!\bare)(?<!\bwas)(?<!\bwere)(?<!\bbe)(?<!\bbeen)(?<!\bstill)(?<!\bremain)(?<!\bremains)`), and include non-timing `(?:pending|awaiting)\b(?![ \t]+<timing_noun>)` inside the comma branch's optional post-comma connector group.
  * In `FR-05`, order pause alternations as `paus(?:ed|ing|e)\b` and attach `(?:\s+(?:on|for|until|due\s+to|because(?:\s+of)?|owing\s+to)\b)?` to the `status:\s*waiting\b`, `waiting\s+summary\b`, `all\s+lanes\s+waiting\b`, `status:\s*paus(?:ed|ing|e)\b`, `paused\s+summary\b`, `all\s+lanes\s+paused\b`, subject-first `...paus(?:ed|ing)\b`, and `paus(?:ed|ing|e)\b` branches in `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`.
  * In `FR-02`, include `because(?:\s+of)?`, `due\s+to`, and `owing\s+to` (alongside `and`, `or`, `also`, `plus`, `as\s+well\s+as`) in both `TRAILING_TRIGGER_CONNECTOR_WORDS_RE` (used by `_strip_trailing_trigger_bridge`) and `INTRO_PREFIX_BETWEEN_RE` (preserving `[\s:,\-\u2013\u2014]*` for em-dash/colon intro prefixes such as `Status: paused -- blocked on PR #1641.`).
* Smallest useful change: Update `FR-02`, `FR-04`, `FR-05`, and `P01-T01` with the bounded `COORDINATED_WAIT_SPLIT_RE`, word-bounded `paus(?:ed|ing|e)\b` + optional introducer tail on `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`, and causal connector support in `_strip_trailing_trigger_bridge` and `INTRO_PREFIX_BETWEEN_RE`.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `FR-01` Still Returns `_is_claim_negated_at == False` on Multi-Token and Colon/Period Quoted Prohibitions, Masked by a Cited-PR Fixture Coincidence in `P01-T02`

* Related IDs: `FR-01`, `FR-06`, `P01-T01`, `P01-T02`
* Evidence:
  1. In `_is_claim_negated_at` (`tools/check-coordinator-handoff.py` lines 1024-1029), when `match_start` lies inside a quoted literal `[lit_s, lit_e)` after leading words inside the quote (such as `Never say "we are waiting on stakeholder approval".` or `Never say "we are waiting on PR #1641".`), execution enters `_fallback_prohibition_check(ct, clause_raw, rel_pos)`. Even with `pm.end` fixed, for an outer prohibition (`pm.inside_literal_end is None`, `pm.end <= lit_s`), `rest = clause_raw[pm.end : rel_pos]` slices `' say "we are '` before the closing quote at `lit_e`. `INLINE_LITERAL_SPAN_RE.sub(" qtok ", rest)` does not match the unclosed quote, so `WORD_TOKEN_RE` extracts `['say', 'we', 'are']` and `_tokens_govern_claim` returns `False` because `'we'` and `'are'` are not in `GOV_CONTINUATION_TOKENS`.
  2. `P01-T02` item 1 (`Never say "we are waiting on PR #1641".`) passes `check_handoff_text` on default `_valid_handoff_markdown()` only by coincidence: `_is_claim_negated_at` returns `False`, treating `"waiting on PR #1641"` as an active wait that happens to cite classified `PR #1641` with zero `ready to start` rows. Using an uncited target (`Never say "we are waiting on stakeholder approval".`) or including a `ready to start` row immediately triggers a false violation.
  3. `_build_clause_index` runs `CLAUSE_SPLIT_RE` and `SENTENCE_SPLIT_RE` on `span_masked` (`BACKTICK_OR_URL_RE` only), leaving `[;.!?:]` unmasked inside double- and single-quoted `INLINE_LITERAL_SPAN_RE` literals. Quoted prohibitions such as `Do not report "Current status: paused" without a blocker link.` or `Do not report "Idle tick: nothing changed".` split at `:` inside the quotes before `_build_clause_tokens` runs, severing the prohibition head from the trigger.
* Impact: Incomplete closure of `RV-001` and `RV-007`; coordinator handoffs that quote prohibited multi-word or colon/period templates still fail with false-positive guard violations, and the planned `P01-T02` test misses the defect.
* Action owner: Planner (`direct_planner_correction`, user response required: `no`)
* Exact resolving evidence:
  * In `_build_clause_index`, build a length-preserving `clause_split_masked` string by masking interior characters of closed `INLINE_LITERAL_SPAN_RE` spans on `span_masked` for `CLAUSE_SPLIT_RE` and `SENTENCE_SPLIT_RE` indexing only (retaining unmasked quotes in `raw_text` and `span_masked_text` so affirmative quoted claims like `Summary: "Current status: paused."` still trigger).
  * In `_is_claim_negated_at`, when `ct.lit_starts[li] < rel_pos < ct.lit_ends[li]`, first check outer prohibitions at `lit_s` via the indexed token fast path (because an outer prohibition governing `qtok` governs the entire quoted literal), and otherwise delegate to `_fallback_prohibition_check` restricted to inner prohibitions for that literal (`pm.inside_literal_end == ct.lit_ends[li]`) while skipping any inner prohibition whose `clause_raw[pm.end : rel_pos]` matches `CLAUSE_SPLIT_RE` (so `Summary: "Never skip checks; status: paused."` still fires).
  * In `P01-T02` item 1, assert direct `checker._is_claim_negated(...)` truth values plus `check_handoff_text` clean/violation results on uncited/ready-work multi-token and colon-containing quoted prohibitions (`Never say "we are waiting on stakeholder approval".`, `Do not report "Current status: paused" without a blocker link.`, `Do not report "Idle tick: nothing changed".` with a `ready to start` row, `Note: "We never report waiting on stakeholder approval."`) and negative controls (`Summary: "Never skip checks; status: paused."`, `Never skip lint when saying "we are waiting on stakeholder approval".`).
* Smallest useful change: Update `FR-01`, `FR-06`, `P01-T01`, and `P01-T02` with quote-interior clause-split masking, outer-vs-inner literal prohibition evaluation in `_is_claim_negated_at` / `_fallback_prohibition_check`, and non-coincidental uncited/ready-work quoted prohibition subtests.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: `P01-T02` `RV-004` Positive Subtest Cites `#1288#issuecomment-42` Against Default Fixture Anchor `#1288#issuecomment-10`

* Related IDs: `FR-06`, `P01-T02`
* Evidence: `_valid_handoff_markdown` in `tools/test_check_coordinator_handoff.py` (line 42) classifies `#1288` with `[owner-question](#1288#issuecomment-10)`, whereas `P01-T02` item 4 writes `"Waiting on PR #1641 because #1288#issuecomment-42 is pending."` without specifying a matching `table_rows` override, which raises `unverified-blocker-reference` on the mismatched comment anchor.
* Impact: Causes avoidable test-authoring friction if `P01-T02` item 4 is transcribed without overriding `table_rows` or matching `#1288#issuecomment-10`.
* Action owner: Planner (`direct_planner_correction`, user response required: `no`)
* Exact resolving evidence: Use `#1288#issuecomment-10` (or explicitly pass matching `table_rows`) in `P01-T02` item 4, and add subtests covering `, pending #1288#issuecomment-10`, `and its checks are pending`, `because blocked on #1288#issuecomment-10`, and `Status: paused due to PR #1641.`.
* Smallest useful change: Align the anchor ID in `P01-T02` item 4 with `_valid_handoff_markdown` and list the four companion positive subtests from `PC-001`.

## Closeout Summary

* Critique execution status: Complete
* Verdict: Revise (`0` Critical, `2` High, `0` Medium, `1` Low)
* Highest-impact finding: `PC-001` (predicative `is/are pending`, `, pending <ref>`, leading causal pause tails, and causal multi-trigger bridges split into empty uncited segments, breaking `P01-T02`'s own `RV-004` positive subtest)
* Action owner: Primary planner (`planning_parent`)
* Smallest next action: Apply `PC-001`..`PC-003` directly (`direct_planner_correction`) to `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-phase-details.md`, then proceed to `Implement` without another critique pass.
* User response required: no
