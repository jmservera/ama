<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resolve RV-001 through RV-005 Linear-Time Clause Indexing, Wrapped Summary Normalization, Blocker Column/Repo Scoping, and Live Session Identity Verification (Issue #1204 Child Loop 5)

## Metadata

* Task ID: issue-1204-rv5-fixes
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Child remediation task `issue-1204-rv5-fixes` (`delivery-1204-coordinator-guard-rv5-fixes`), child of `issue-1204-rv4-fixes`, resolving routed review findings `RV-001` through `RV-005` under Focused validation (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`) without running `tools/rpi-checks.py` and keeping prior review/critique artifacts immutable.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md, .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, tools/check-coordinator-handoff.py, tools/test_check_coordinator_handoff.py.
* Decisions, dependencies, and acceptance criteria considered: Issue #1204 acceptance criteria AC1 through AC4 (`D-1204-1` through `D-1204-4`), routed review findings `RV-001` through `RV-005`, test-method count lock (`11` `unittest` methods in `tools/test_check_coordinator_handoff.py` with `0` removals and subtests added inside existing methods), zero `.copilot-tracking/` path literals in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`, and Focused validation exit `0` without running `tools/rpi-checks.py`.
* Assessment boundary: Evaluates plan and phase-detail algorithmic completeness, regex/scanner complexity guarantees, Markdown normalization invariants, blocker column and repository-qualifier scoping, CLI/API session identity checks, and regression test coverage against the supplied source files; excludes live `tmux` schedule execution and `tools/rpi-checks.py` full-gate execution per caller constraints.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| `RV-001` / `FR-01` / `NFR-01` | Partial | `ClauseIndex` and `#`-anchored scanning address main rescans, but `MD_LINK_RE` still allows `(` inside `([^)\s]+)` (`O(N^2)` on `"[a](b" * 4000`), `_extract_cited_blocker_refs` still slices/masks `text[tm.end():]` per stopped trigger (`O(N^2)` on `"waiting on #1641; " * 400`), `_strip_md_formatting` has `O(N^2)` `[`*_~\s]+$`, and `qmasked_text` `'q'` runs do not match `"qtok"` in `GOV_CONTINUATION_TOKENS` (`PC-001`). |
| `RV-002` / `FR-02` | Partial | `_iter_section_prose_blocks` joins wrapped lines across paragraphs and list items, but omits breaking across stripped fenced code blocks (`lineno != prev_lineno + 1`), stripping `>` on wrapped blockquotes (`"> Nothing\n> changed."`), and flushing unpunctuated metadata KV lines before unindented prose (`PC-002`). |
| `RV-003` / `FR-03` / `P01-T01` | Covered | `.github/agents/ama-backlog-delivery-coordinator.agent.md` waiting-rule alignment, HVE SHA-256 refresh, and post-target conditional/deferred subordinator rejection in `NON_CURRENT_LAUNCH_SUBCLAUSE_RE` are well-scoped (extend post-target list to include passive deferrals such as `deferred`/`postponed`/`skipped`/`failed` alongside the planned subordinators). |
| `RV-004` / `FR-04` | Partial | Full-span scanning, column scoping, and `(repo_key, number)` tuples are planned, but substring `"pr"` in `BLOCKER_COL_KEYWORDS` falsely matches `Priority`/`Progress`/`Sprint`/`Approval`/`Next PR action`, and `[PR #1641](https://github.com/octo/other/pull/1641)` emits a phantom local `("", 1641)` from the link label unless Markdown links are resolved before bare `#<n>` scanning (`PC-003`). |
| `RV-005` / `FR-03` / `FR-04` | Partial | `--active-sessions <csv>` API/CLI surface is planned, but must also flag `stale-active-session-identity` when `Active sessions: 1/8` omits backtick tokens while `active_sessions` is non-empty, scope `active_sessions` to `is_latest` in multi-section checkpoints, and add `"--active-sessions"` to `check_agent_instructions` required live tokens (`PC-003`). |
| `P01` / `P01-T02` / `P01-T03` / `FR-05` / `NFR-02` | Partial | Task sequencing and the 11-method `unittest` ownership lock are sound, pending subtests in `P01-T03` covering the residual quadratic inputs, wrapped blockquote/fence boundaries, and column/link/session edge cases (`PC-001`..`PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: The single-phase plan cleanly maps all five routed findings (`RV-001`..`RV-005`), preserves prior review logs and the 11-method test structure, and stays strictly inside the Focused validation boundary, but three substantive algorithmic edge cases in `P01-T02` and `P01-T03` (`PC-001`..`PC-003`) would leave residual `O(N^2)` inputs, a `qtok` tokenization regression on `.agent.md`, a wrapped-blockquote/fence bypass, and substring/link-label collisions in blocker and session-identity verification if implemented verbatim.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Residual `O(N^2)` regex/slice paths and `ClauseIndex` inline-literal token mismatch in `RV-001` / `RV-004`

* Related IDs: `RV-001`, `RV-004`, `FR-01`, `FR-04`, `NFR-01`, `P01-T02`, `P01-T03`
* Evidence: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md (`FR-01`, `FR-04`), .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md (`P01-T02` items 1 and 4), tools/check-coordinator-handoff.py (lines 57, 69, 146, 292, 345, 369, 469)
* Concern: Four concrete complexity or correctness issues remain in the planned `O(N)` design:
  1. `MD_LINK_RE = re.compile(r"\[([^\[\]\n]+)\]\(([^)\s]+)\)")` (and `LINKED_SINGLE_ISSUE_CELL_RE`) still allows `(` inside `([^)\s]+)`, so `"[a](b" * 4000` (unclosed link parens without spaces) scans to EOF and backtracks on each `[a](` in `O(N^2)` time.
  2. In `_extract_cited_blocker_refs`, slicing and re-masking `span = text[tm.end() :]` per match while advancing `covered_until` only up to `stop_m` remains `O(N^2)` on stopped multi-clause inputs such as `"waiting on #1641; " * 400` because `covered_until` stops at each `;` while `text[tm.end() :]` copies and masks the entire remaining tail 400 times.
  3. Existing helpers `_strip_md_formatting` (`re.sub(r"^[`*_~\s]+|[`*_~\s]+$", "", cleaned)` on `"`" * 4000 + "x"`), `ZERO_UNCLASSIFIED_GUARD_RE` (`.*`), `_has_conditional_guard_suffix` (if slicing the entire prefix instead of a `<= 160`-char tail window), and `REPO_QUAL_SUFFIX_RE` (if sliced at a fixed 140-char offset mid-token or regex-searched across `"a/b/" * 35`) still permit superlinear scans or mid-path prefix truncation.
  4. `P01-T02` item 1 specifies masking inline literals to same-length `'q'` runs (`qmasked_text`), which produces arbitrary-length `'qqq...'` tokens rather than `"qtok"` in `GOV_CONTINUATION_TOKENS` (breaking `never claim "nothing changed"` in `.agent.md` and `test_fenced_code_blocks_and_negated_normative_prose_do_not_false_trigger`), omits passing `allow_conditional_guards: bool = True` to `_is_claim_negated_at` for `check_agent_instructions`, and does not mask inline URLs (`_mask_url_preserving_trailing_punct`) when computing clause/sentence boundaries (causing `https:` and `.com` inside URLs to split clauses and hold-wait sentences).
* Impact: Worst-case inputs (`"[a](b" * 4000`, `"waiting on #1641; " * 400`, `"`" * 4000 + "x"`) violate strict linear `O(N)` scaling (`NFR-01`), and `'qqq...'` literal masking or missing `allow_conditional_guards` breaks live `.agent.md` polarity checks.
* Smallest useful change: Update `FR-01`, `P01-T02` (items 1 and 4), and `P01-T03` so: (a) `MD_LINK_RE` and `LINKED_SINGLE_ISSUE_CELL_RE` use `[^()\s]+` for link targets; (b) `ClauseIndex` precomputes backtick-and-URL-masked text once per block, emits `"qtok"` tokens for `INLINE_LITERAL_SPAN_RE` spans, supports `allow_conditional_guards: bool = True` via a `<= 160`-char tail check, and `_extract_cited_blocker_refs` searches `BLOCKER_SPAN_STOP_RE.search(idx.span_masked_text, tm.end())` without slicing/re-masking `text[tm.end():]` so only disjoint `[max(tm.end(), covered_until), end_pos)` slices are inspected; (c) `_strip_md_formatting` uses `.strip("`*_~ \t\r\n")`, `ZERO_UNCLASSIFIED_GUARD_RE` uses two sequential linear searches instead of `.*`, and `_iter_issue_refs` extracts the contiguous `[A-Za-z0-9_./-]+` suffix before `#` in `O(1)` without regex backtracking or fixed-slice truncation; and (d) `P01-T03` adds `"[a](b" * 4000`, `"waiting on #1641; " * 400`, and `"`" * 4000 + "x"` to the `< 0.15s` scaling subtest.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-01`, `P01-T02`, and `P01-T03` in the plan and phase details specifying `[^()\s]+`, `ClauseIndex` `"qtok"` + URL-safe masking + `allow_conditional_guards`, disjoint `[scan_start, end_pos)` blocker-span scanning, `.strip("`*_~ \t\r\n")`, and scaling subtests for all three patterns.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Wrapped prose block normalization (`RV-002`) misses fenced-block line gaps, wrapped `>` blockquotes, and post-metadata line flushes

* Related IDs: `RV-002`, `FR-02`, `P01-T02`, `P01-T03`
* Evidence: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md (`FR-02`), .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md (`P01-T02` item 2, `P01-T03`), tools/check-coordinator-handoff.py (`_iter_unfenced_lines` line 264, `_iter_normalized_prose_clauses` line 472)
* Concern: Three Markdown block-boundary cases are unhandled in `_iter_section_prose_blocks`:
  1. `_iter_unfenced_lines` drops fenced code blocks while keeping original line numbers; without breaking blocks when `lineno != prev_lineno + 1`, prose lines immediately before and after a fenced code block (with no blank lines) merge into one block, allowing pre-fence negation to mask a post-fence idle or waiting claim.
  2. CommonMark hard-wrapped blockquotes (`"> Nothing\n> changed."`) retain `>` on continuation lines and join to `"> Nothing > changed."`, breaking `\bnothing\s+changed\b` and `\bwaiting\s+(?:on|for)\b` matching unless leading `>` markers are stripped within same-depth blockquote blocks.
  3. Recognized metadata KV lines (`KNOWN_METADATA_KEYS`, such as `* Active sessions: 0/8` or `* Target/base SHA: ...`) carry no trailing period; if followed immediately (without a blank line) by unindented prose (`Summary: nothing\nchanged.`), starting a block at the metadata line without flushing after the metadata line merges metadata text into the following prose block.
* Impact: Trivial CommonMark blockquote wrapping (`"> Nothing\n> changed."`) or fence-adjacent prose bypasses the `RV-002` fix or misattributes violations/negation across metadata lines.
* Smallest useful change: Specify in `FR-02`, `P01-T02` item 2, and `P01-T03` that `_iter_section_prose_blocks` (and `_iter_normalized_prose_clauses`) breaks blocks on `lineno != prev_lineno + 1` and blockquote-depth transitions, strips leading `>` markers on blockquote lines before joining, flushes recognized `KNOWN_METADATA_KEYS` lines as standalone blocks unless a continuation line is indented, and adds subtests for `"> Nothing\n> changed."` and fence-separated negation/idle lines.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-02`, `P01-T02` item 2, and `P01-T03` recording `lineno != prev_lineno + 1` splits, blockquote `>` stripping, metadata-block flushing, and corresponding `RV-002` subtests.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Blocker column substring collision, Markdown-linked external repo label leakage (`RV-004`), and `--active-sessions` omitted-token / agent-contract checks (`RV-005`)

* Related IDs: `RV-004`, `RV-005`, `FR-03`, `FR-04`, `FR-05`, `P01-T02`, `P01-T03`
* Evidence: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md (`FR-03`, `FR-04`, `FR-05`), .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md (`P01-T02` items 3, 4, and 5; `P01-T03`), tools/check-coordinator-handoff.py (lines 515-595, 702-712, 800-835, 955-971)
* Concern: Three edge cases affect `RV-004` and `RV-005` precision:
  1. Matching `BLOCKER_COL_KEYWORDS` (`blocker`, `evidence`, `link`, `dependency`, `reason`, `pr`) by plain substring treats `"pr"` inside `Priority`, `Progress`, `Sprint`, `Owner approval`, or `Next PR action` as a blocker column. Excluding `NON_BLOCKER_COL_HEADERS` (`\bnext\s+actions?\b`, `^actions?$`, `owner`, `notes?`, `summary`, `title`) first and matching blocker keywords on word boundaries (`\b...\b`) avoids false column inclusion.
  2. In `[PR #1641](https://github.com/octo/other/pull/1641)`, stripping only `URL_RE` leaves unqualified `#1641` in the link label `[PR #1641]`, emitting a phantom local `("", 1641)` tuple alongside `("octo/other", 1641)` in both `_extract_cited_blocker_refs` and `_extract_verified_evidence_refs`. Resolving `MD_LINK_RE` pairs first (inheriting the target GitHub URL's `repo_key` for matching `#<n>` in the label, then replacing `MD_LINK_RE` spans before bare prose scanning) prevents cross-repo label leakage.
  3. For `--active-sessions <csv>`, `_validate_section` must still flag `stale-active-session-identity` when `active_sessions` is non-empty (for example `{"rpi-1310"}`) and the handoff writes `* Active sessions: 1/8` with zero backtick session tokens (`listed_session_tokens == []`), validate live `active_sessions` issue numbers against `active session` rows in `classified_by_num`, apply `active_sessions` only to `is_latest` in multi-section checkpoint files, and include `"--active-sessions"` in `check_agent_instructions` (`required_live_tokens`). Additionally, in `P01-T02` item 3, include passive post-target deferrals (`deferred`, `postponed`, `skipped`, `failed`) alongside the planned subordinators in `NON_CURRENT_LAUNCH_SUBCLAUSE_RE`.
* Impact: Without word-bounded column selection, link-before-prose repo extraction, and omitted-token session identity checks, `Next PR action` / `Priority` cells or `[PR #1641](https://github.com/octo/other/pull/1641)` links misclassify blocker evidence and `Active sessions: 1/8` (without backtick names) bypasses `--active-sessions rpi-1310`.
* Smallest useful change: Refine `FR-03`, `FR-04`, `P01-T02` (items 3, 4, and 5), and `P01-T03` to specify word-bounded `BLOCKER_COL_RE` after `NON_BLOCKER_COL_HEADERS` exclusion, `MD_LINK_RE`-first `(repo_key, number)` extraction, omitted-token and `is_latest` handling for `active_sessions` plus `"--active-sessions"` in `check_agent_instructions`, passive post-target deferral tokens in `NON_CURRENT_LAUNCH_SUBCLAUSE_RE`, and subtests covering `[PR #1641](https://github.com/octo/other/pull/1641)` and tokenless `Active sessions: 1/8` with `--active-sessions rpi-1310`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-03`, `FR-04`, `P01-T02`, and `P01-T03` incorporating word-bounded blocker column selection, `MD_LINK_RE`-first repo-tuple resolution, full `active_sessions` / `check_agent_instructions` checks, and matching subtests.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strengths: Complete traceability from `RV-001`..`RV-005` to `FR-01`..`FR-05` and `P01-T01`..`P01-T03`; strict preservation of immutable historical review logs, `rpi_phase_witness.py` anchors, HVE SHA-256 evidence, zero `.copilot-tracking/` literals in Python sources, and the 11-method `unittest` lock.
* Accepted residual risk: Offline deterministic validation and static/contained HVE checks verify coordinator instruction rules and handoff/checkpoint Markdown artifacts without executing live multi-tick `tmux` Copilot schedules (`D-1204-3`), and wiring `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` remains an explicit separate full-gate follow-up item per `#1294`.

## Questions or Blocking Evidence Gaps

* None. All three findings (`PC-001`..`PC-003`) are bounded planner refinements fully resolved by the supplied repository evidence and caller direction.

## Limitations

* Read-only plan critique bounded to supplied artifacts; `tools/rpi-checks.py` was not executed per caller instructions.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md` to fold in `PC-001`..`PC-003`, record the critique disposition, and finalize the plan without another critique pass.
* User response required: no
