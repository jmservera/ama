<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resolve RV-001 through RV-006 Single-Subclause Hold Indexing, Independent Multi-Trigger Spans, Strict Capacity/Drain Anchors, Bare Self-URL Rejection, Tableless Blocker Checks, and Mixed Declared Session Matching (Issue #1204 Child Loop 7)

## Metadata

* Task ID: issue-1204-rv7-fixes
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass plan critique for child remediation task `issue-1204-rv7-fixes` (`delivery-1204-coordinator-guard-rv7-fixes`) assessing whether `FR-01`..`FR-07` and `P01-T01`..`P01-T02` completely and safely close parent review findings `RV-001`..`RV-006` without regressions, false positives on existing `11` unit test methods, or edge-case bypasses.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan.md, .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, tools/check-coordinator-handoff.py, and tools/test_check_coordinator_handoff.py.
* Decisions, dependencies, and acceptance criteria considered: Issue #1204 acceptance criteria 1 through 4 (`D-1204-1`..`D-1204-4`), routed defects `RV-001`..`RV-006`, Focused validation tier only (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`, without running `tools/rpi-checks.py`), exact `11` `def test_*` test-method ownership lock (`FR-07`), and `NFR-01`..`NFR-02` (`O(N)` scaling and zero `.copilot-tracking/` literals in `tools/`).
* Assessment boundary: Evaluates parser/validator logic, time-complexity bounds, regex boundary behavior, existing test compatibility, and adversarial bypass resistance from the supplied read-only artifacts without mutating source files or executing `tools/rpi-checks.py`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-01` (`RV-001`) | Partial | Mathematical `min_hold_end <= m.start()` equivalence holds, but `dict[int, int \| None]` with `None` risks `O(K^2)` cache misses on hold-free multi-launch subclauses if `.get(si) is None` is used, and scanning raw `text` instead of `idx.span_masked_text` lets backticked session suffixes match hold words (`PC-004`). |
| `FR-02` (`RV-002`) | Covered | Per-trigger `triggers[i + 1].start()` upper-bound clamping with `INTRO_PREFIX_BETWEEN_RE` (`^[\s:,\-\u2013\u2014]*$`) bounded by `natural_end` validates each substantive wait/pause trigger in `O(N)` while preserving introductory prefixes and all existing passing tests. |
| `FR-03` (`RV-003`) | Partial | Unanchored `.search(span_text)` plus a 12-stem denylist lets non-denylisted uncited blockers with trailing capacity/drain context (for example `"Waiting for user input at 8/8 active sessions."`) bypass `RV-003`, while singular `checks?` in `NON_CAPACITY_BLOCKER_WORD_RE` risks false positives on coordinator `"check"` prose (`PC-002`). |
| `FR-04` (`RV-004`) | Partial | `_normalize_repo_key("jmservera/ama")` returns `""` in `tools/check-coordinator-handoff.py:369-373`, so `DEFAULT_REPO_KEY = "jmservera/ama"` in `P01-T01` item 4 causes `_normalize_repo_key(repo) == self_repo_key` (`"" == "jmservera/ama"`) to evaluate `False` on default-repo rows, and `BARE_GITHUB_ISSUE_URL_RE` misses `issues/<self>`, `./issues/<self>`, and `#<self>` fragments (`PC-001`). |
| `FR-05` (`RV-005`) | Partial | Unconditional `unverified-blocker-pause` and `has_blocker_or_wait_claim` close tableless and unclassified `blocked on/by` bypasses, but leaving `unsupported-waiting-ready-work` gated on `is_waiting_or_pause` lets `"Blocked on #1288."` bypass ready-work launch enforcement below capacity (`PC-003`). |
| `FR-06` (`RV-006`) | Covered | Passing `require_active_rows_covered=True` to `_verify_sessions_against_table` whenever `listed_session_tokens` is non-empty catches unbacked `active session` rows in mixed session lists while preserving valid non-issue-only session lists (`0` `active session` rows). |
| `FR-07` / `NFR-01`..`NFR-02` | Covered | Preserves all `11` `def test_*` methods (`0` added, `0` removed) via `self.subTest` additions, stdlib-only Python 3.12, and zero `.copilot-tracking/` literals in `tools/`. |
| `P01` / `P01-T01` | Partial | Needs targeted formula adjustments in items 1, 3, 4, and 5 for `PC-001`..`PC-004`. |
| `P01-T02` | Partial | Needs subtest cases covering `PC-001`..`PC-004` edge cases inside the existing `11` test methods. |

## Verdict

* Verdict: Revise
* Rationale: `FR-02`, `FR-06`, and `FR-07` are sound, but `P01-T01` item 4 contains a concrete repo-key normalization mismatch (`""` vs `"jmservera/ama"`) that defeats `RV-004` on default-repo rows (`PC-001`), `FR-03` leaves unanchored capacity/drain tail bypasses and a singular-`check` false-positive hazard (`PC-002`), `FR-05` omits `unsupported-waiting-ready-work` for `blocked on/by` claims (`PC-003`), and `FR-01` needs explicit key-membership memoization and `span_masked_text` scanning (`PC-004`). All four findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Repo-Key Normalization Mismatch in `P01-T01` Item 4 Breaks `RV-004` on Default-Repository Rows and Relative `issues/<self>` Links

* Related IDs: `FR-04`, `RV-004`, `P01`, `P01-T01`, `P01-T02`
* Evidence: tools/check-coordinator-handoff.py (`DEFAULT_LOCAL_REPO` at line 33 and `_normalize_repo_key` at lines 369-373) and .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md (`P01-T01` item 4)
* Concern: In `tools/check-coordinator-handoff.py:369-373`, `_normalize_repo_key("jmservera/ama")` returns `""` (empty string) for the local default repository. However, `P01-T01` item 4 defines `DEFAULT_REPO_KEY = "jmservera/ama"`, makes `_infer_row_repo_key("#1288")` return `DEFAULT_REPO_KEY` (`"jmservera/ama"`), and checks `_normalize_repo_key(repo) == self_repo_key` inside `_is_bare_self_issue_url`. For `| #1288 | human-blocked | https://github.com/jmservera/ama/issues/1288 |`, `_normalize_repo_key("jmservera/ama") == "jmservera/ama"` evaluates `"" == "jmservera/ama"` (`False`), failing to reject the exact `RV-004` reproducer. In addition, `BARE_GITHUB_ISSUE_URL_RE` requires a `/` immediately before `issues/(\d+)`, allowing slashless or dot-relative `[self](issues/1288)` and `[self](./issues/1288)` targets to pass, and `frag.strip()` accepts trivial self-number fragments (`.../issues/1288#1288`) even though `[self](#1288)` is already rejected.
* Impact: Implementing `P01-T01` item 4 as written fails the primary `RV-004` bare self-URL check on plain `#<N>` rows and leaves relative `issues/<self>` and `#<self>` URL bypasses open.
* Smallest useful change: Align `DEFAULT_REPO_KEY = ""` with `_normalize_repo_key(DEFAULT_LOCAL_REPO) == ""` (comparing `_normalize_repo_key(repo) == _normalize_repo_key(self_repo_key)` when `repo` is present), allow optional leading `./` or slashless `issues/(\d+)` in `BARE_GITHUB_ISSUE_URL_RE` (while keeping cross-repo `octo/other/issues/1288` distinct), treat empty or bare `#<self>` fragments (`frag_clean == "" or frag_clean == str(issue_number)`) as bare self-issue URLs while preserving `#issuecomment-...` and other real fragments, and add relative `issues/1288` coverage to `P01-T02`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-04`, `P01-T01` item 4, and `P01-T02` specifying normalized `""` repo-key comparison, relative `(?:(?:\./)?|/)?issues/(\d+)` matching, and `#<self>` fragment rejection while preserving `#issuecomment-...` and cross-repository `/issues/<self>` links.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Unanchored Capacity/Drain Span Search Permits Uncited Blocker Bypasses and Singular `check` False Positives

* Related IDs: `FR-03`, `RV-003`, `P01`, `P01-T01`, `P01-T02`
* Evidence: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan.md (`FR-03`), .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md (`P01-T01` item 3), and tools/check-coordinator-handoff.py (`WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` at lines 254-264)
* Concern: `P01-T01` item 3 uses unanchored `.search(span_text)` for `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` backed only by a 12-stem denylist (`NON_CAPACITY_BLOCKER_WORD_RE`). First, any uncited human/external wait phrased outside those 12 stems with trailing capacity/drain context -- such as `"Waiting for user input at 8/8 active sessions."`, `"Waiting for legal clearance during PR drain."`, `"Paused due to staging outage at 8/8 active sessions."`, or `"Waiting for a free session slot and user input."` -- matches the trailing capacity/drain substring and bypasses `RV-003` with `0` violations. Second, `NON_CAPACITY_BLOCKER_WORD_RE` includes singular `\bchecks?\b`, whereas coordinator prose and `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` (`Paused the check ...`) use `"check"` to mean the scheduled coordinator tick; valid capacity waits such as `"Paused the check for a free worker slot at 8/8 capacity."` or `"Waiting for a free session slot until the next check."` would falsely trigger `unverified-blocker-pause`.
* Impact: Leaves `RV-003` open to uncited blocker waits carrying trailing capacity/PR-drain qualifiers while risking false positives on legitimate coordinator `"check"` status sentences.
* Smallest useful change: Evaluate `_is_exempt_capacity_or_drain_wait` on the post-trigger slice `target_span = text[tm.end():end_pos]`, anchor `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` to the start of `target_span` (`^\s*(?:(?:on|for|until|at|during|under)\s+)?(?:(?:a|an|the|any|next)\s+)?...`), reject coordinating or causal extra-blocker tails (`\b(?:and|or|plus|because|due\s+to)\b`) inside `target_span`, narrow `checks?` in `NON_CAPACITY_BLOCKER_WORD_RE` to plural `\bchecks\b` or qualified `(?:ci|pr|hosted|status|required|merge)\s+check\b` (while adding `input|repl(?:y|ies)|responses?|clearances?|permissions?|legal|security|outages?`), and add subtests in `P01-T02` for both `"Waiting for user input at 2/2 active sessions."` (rejected) and `"Waiting for a free worker session slot until the next check."` (accepted).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-03`, `P01-T01` item 3, and `P01-T02` anchoring capacity/PR-drain matches at the post-trigger span head without coordinating/causal tails and narrowing singular `check` matching to CI/PR/status check phrases.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `blocked on/by` Claims Still Bypass `unsupported-waiting-ready-work` When Ready Issues Have Open Capacity

* Related IDs: `FR-05`, `RV-005`, `P01`, `P01-T01`, `P01-T02`
* Evidence: tools/check-coordinator-handoff.py (`WAITING_OR_PAUSE_RE` at lines 177-187, `_has_global_wait_or_pause` at lines 581-596, and `_validate_section` at lines 1248-1253) and .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md (`P01-T01` item 5)
* Concern: `P01-T01` item 5 introduces `has_blocker_or_wait_claim` for `missing-classification-table`, `summary-before-classification-table`, and `unsupported-idle-unclassified`, but leaves `unsupported-waiting-ready-work` (`tools/check-coordinator-handoff.py:1249`) gated on `is_waiting_or_pause` (which does not match `blocked on/by`) and leaves `_has_global_wait_or_pause` (`line 593`) checking only `WAITING_ON_FOR_RE` before `HOLD_CONTINUATION_RE`. Consequently, if `#1288` is `human-blocked` with a valid link, `#1310` is `ready to start` at `0/8` active sessions (not launched), and the summary states `"Blocked on #1288."` or `"Blocked on #1288 before continuing."`, `is_waiting_or_pause` is `False` and the handoff passes with `0` violations despite unstarted `ready to start` work.
* Impact: Permits a coordinator check to stall on a verified blocked lane via `"Blocked on #<id>."` without launching independent `ready to start` issues that have open session/PR capacity.
* Smallest useful change: Gate `unsupported-waiting-ready-work` on `has_blocker_or_wait_claim` instead of `is_waiting_or_pause`, include `\bblocked\s+(?:on|by)\b` alongside `WAITING_ON_FOR_RE` before `HOLD_CONTINUATION_RE` in `_has_global_wait_or_pause`, and add a subtest in `P01-T02` verifying `"Blocked on #1288."` with unstarted `#1310` `ready to start` below capacity emits `unsupported-waiting-ready-work` (while `"Launched rpi-1310; #1288 is blocked on #1288#issuecomment-10."` continues to pass).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-05`, `P01-T01` item 5, and `P01-T02` gating `unsupported-waiting-ready-work` on `has_blocker_or_wait_claim` and covering `blocked on/by` in `_has_global_wait_or_pause`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `min_hold_end_by_subclause` `None`-Sentinel Cache Miss Risk and Unmasked Backtick Hold Matching in `P01-T01` Item 1

* Related IDs: `FR-01`, `RV-001`, `NFR-01`, `P01`, `P01-T01`, `P01-T02`
* Evidence: tools/check-coordinator-handoff.py (`_launched_ready_issues_in_current_tick` at lines 599-629) and .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md (`P01-T01` item 1)
* Concern: `P01-T01` item 1 types `min_hold_end_by_subclause: dict[int, int | None]` with `default=None` (`None` representing "subclause scanned and contains no hold/negation match"). If implemented with `.get(si) is None` (matching the adjacent `non_current_by_subclause.get(si)` pattern at line 619), every hold-free subclause stores `None` and triggers a cache miss on every distinct ready launch match (`O(K^2)` when `K` distinct ready issues appear in a single subclause without a hold word). Additionally, scanning raw `text` rather than `idx.span_masked_text` allows hyphenated backticked worker names containing hold tokens (such as ``Launched `rpi-1310-no-push` and starting #1311``) to match `\bno\b` inside the backtick literal and suppress `#1311`.
* Impact: Risks reintroducing `O(K^2)` scaling on hold-free multi-launch subclauses and false hold suppression when backticked session identifiers contain hyphenated hold words.
* Smallest useful change: Specify explicit key-membership memoization (`if si not in min_hold_end_by_subclause:` or an integer sentinel `-1`) using `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE.search(idx.span_masked_text, sub_start, sub_end)` and `NON_CURRENT_LAUNCH_SUBCLAUSE_RE.search(idx.span_masked_text, sub_start, sub_end)` (same offsets, backticks and URLs masked), and add a hold-free multi-ready single-subclause scaling assertion to `P01-T02`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-01`, `P01-T01` item 1, and `P01-T02` specifying `si not in min_hold_end_by_subclause`, `idx.span_masked_text` subclause scans, and hold-free multi-issue subclause scale coverage.
* Decision route: direct planner correction

## Strengths and Residual Risk

* `FR-02` cleanly resolves `RV-002` in `O(N)` by clamping each trigger at `triggers[i + 1].start()` while delegating pure punctuation/whitespace introductory prefixes (`Status: waiting -- blocked on #1641`) only within `natural_end`, preserving all existing multi-wait and concurrent-launch unit tests.
* `FR-06` cleanly closes `RV-006` with a single-argument fix (`require_active_rows_covered=True` when `listed_session_tokens` is non-empty) while preserving valid zero-active-row housekeeping session declarations (`Active sessions: 1/8 (\`maintenance\`)`).
* `FR-07` and `NFR-02` preserve the exact `11` `def test_*` methods and keep `.copilot-tracking/` string literals out of `tools/`.
* Explicitly accepted residual scope: Wiring `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` remains deferred to a dedicated full-tier gate-tooling PR under `#1294` because running or editing `tools/rpi-checks.py` is outside this Focused task boundary.

## Questions or Blocking Evidence Gaps

* None. All findings are deterministic parser/regex refinements resolvable directly by the planning parent from existing codebase evidence.

## Limitations

* Per caller instructions and `rpi-plan-critique` read-only boundaries, this critique did not modify source files or run `tools/rpi-checks.py`.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Directly revise `FR-01`, `FR-03`, `FR-04`, `FR-05`, `P01-T01`, and `P01-T02` in `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md` to incorporate `PC-001`..`PC-004`, then finalize planning and proceed to implementation without another critique pass.
* User response required: no
