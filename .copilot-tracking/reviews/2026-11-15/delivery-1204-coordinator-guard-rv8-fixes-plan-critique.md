<!-- markdownlint-disable-file -->
# Plan Critique: Resolve RV-001 through RV-005 Pre-Indexed Clause Raw Slices, Coordinated Wait-Segment Verification, Next-Check Capacity/Drain Tails, and Complete Subtest Coverage (Issue #1204 Child Loop 8)

## Metadata

* Task ID: issue-1204-rv8-fixes
* Task slug: delivery-1204-coordinator-guard-rv8-fixes
* Assessed plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan.md
* Assessed phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-phase-details.md
* Supplied evidence: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, tools/check-coordinator-handoff.py, tools/test_check_coordinator_handoff.py
* Critique execution status: Complete
* Verdict: Revise

## Criterion Boundary and Coverage Assessment

Assessed `FR-01`..`FR-05`, `NFR-01`..`NFR-02`, test ownership lock (`11` test methods), and interactions with Markdown links, serial-comma lists, shared PR lifecycle phrases, and `PR_DRAIN_WAIT_SPAN_RE` thresholds.

* `FR-01` (`ClauseTokens.raw`): Credible; eliminates all `O(K * N)` per-match clause slice allocations in `_is_claim_negated_at`.
* `FR-02` (`COORDINATED_WAIT_SPLIT_RE` / `SHARED_REF_LIFECYCLE_TAIL_RE`): Needs two targeted refinements (`PC-001`, `PC-002`) so Markdown link labels containing `and`/`or` are not split mid-link, forward shared lifecycle heads (`Waiting on CI and status checks on PR #1641`) are accepted, and 3-item serial-comma lists (`Waiting on PR #1641, stakeholder approval, and PR #1642`) cannot hide an uncited middle blocker.
* `FR-03` (`NEXT_CHECK_TIMING_TAIL_PAT`): Credible with explicit ordering after numeric drain qualifiers (`PC-003`).
* `FR-04` and `FR-05`: Credible and complete once `PC-001`..`PC-002` subtests are included.
* Limitations: None; all inputs were inspected directly.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `idx.span_masked_text` Leaves Markdown Link Labels Unmasked, Splitting `[CI and checks](...)` Mid-Link, and Backward-Only Shared Lifecycle Attachment Rejects Forward `CI and checks on PR #1641`

* Related IDs: `FR-02`, `P01-T01`, `P01-T02`
* Evidence: `_build_clause_index` masks inline backticks and raw `https?://` URLs in `span_masked_text`, leaving `[label](...)` link labels unmasked (`[CI and checks](______)` or `[review and reply](#1288#issuecomment-42)`). Splitting `masked_span` directly on `and`/`or` bisects valid Markdown links and loses `[label](target)` parsing. In addition, checking `SHARED_REF_LIFECYCLE_TAIL_RE` only backward (`j > 0 and prev_had_ref`) rejects valid forward attachment such as `"Waiting on CI and status checks on PR #1641."`.
* Impact: False-positive `unverified-blocker-pause` on valid Markdown blocker links whose label contains `and`/`or` or on forward `CI and checks on PR #<N>` phrasing.
* Action owner: Planner (`direct_planner_correction`, user response required: `no`)
* Exact resolving evidence: Mask `MD_LINK_RE` spans in `masked_span` before applying `COORDINATED_WAIT_SPLIT_RE`, and allow `SHARED_REF_LIFECYCLE_SEG_RE` segments when adjacent (`j - 1` or `j + 1`) to a cited segment.
* Smallest useful change: Update `FR-02` and `P01-T01`/`P01-T02` to mask `MD_LINK_RE` on `masked_span` prior to splitting and accept `SHARED_REF_LIFECYCLE_SEG_RE` adjacent to either the preceding or following cited segment.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Conjunction-Only Splitting Misses Uncited Middle Items in Serial-Comma Lists (`Waiting on PR #1641, stakeholder approval, and PR #1642`)

* Related IDs: `FR-02`, `P01-T01`, `P01-T02`
* Evidence: Splitting only on `(?:,\s*)?\b(?:and|or|plus|as\s+well\s+as)\b` leaves `" PR #1641, stakeholder approval"` as a single first segment in `"Waiting on PR #1641, stakeholder approval, and PR #1642."` (or comma-only `"Waiting on PR #1641, stakeholder approval."`), allowing the uncited `"stakeholder approval"` item to piggyback on `PR #1641`.
* Impact: Incomplete closure of `RV-002` for serial-comma blocker lists.
* Action owner: Planner (`direct_planner_correction`, user response required: `no`)
* Exact resolving evidence: Include non-prepositional list commas `,\s*(?!(?:until|before|for|pending|awaiting|till|at|during|under|in|on|with|without)\b)` in `COORDINATED_WAIT_SPLIT_RE` alongside `(?:,\s*)?\b(?:and|or|plus|as\s+well\s+as)\b`.
* Smallest useful change: Extend `COORDINATED_WAIT_SPLIT_RE` in `FR-02` and `P01-T01` to split non-prepositional comma list items and add a 3-item serial-comma regression case in `P01-T02`.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Place `NEXT_CHECK_TIMING_TAIL_PAT` After Numeric Threshold Qualifiers in `PR_DRAIN_WAIT_SPAN_RE`

* Related IDs: `FR-03`, `P01-T01`
* Evidence: `PR_DRAIN_WAIT_SPAN_RE` matches optional numeric drain tails such as `until <= 15`; placing `NEXT_CHECK_TIMING_TAIL_PAT` immediately before `[\s)]*$` after that `*` group ensures both `"until <= 15"` and `"below 15 until the next scheduled check"` parse unambiguously without backtracking conflicts.
* Impact: Prevents accidental ordering ambiguity when editing `PR_DRAIN_WAIT_SPAN_RE`.
* Action owner: Planner (`direct_planner_correction`, user response required: `no`)
* Exact resolving evidence: Specify exact placement after the numeric/drain qualifier loop and before `[\s)]*$` in `P01-T01`.
* Smallest useful change: Note exact placement in `P01-T01` phase details.

## Closeout Summary

* Critique execution status: Complete
* Verdict: Revise (`0` Critical, `1` High, `1` Medium, `1` Low)
* Highest-impact finding: `PC-001` (`MD_LINK_RE` masking before coordinated wait splitting and bidirectional adjacent lifecycle attachment)
* Action owner: Primary planner
* Smallest next action: Apply `PC-001`..`PC-003` directly to the `rv8-fixes` plan and phase details and transition to `Implement`.
* User response required: no
