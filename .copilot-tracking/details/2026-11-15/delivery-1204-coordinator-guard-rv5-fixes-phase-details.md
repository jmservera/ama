<!-- markdownlint-disable-file -->
# Phase Details: Resolve RV-001 through RV-005 Linear-Time Clause Indexing, Wrapped Summary Normalization, Blocker Column/Repo Scoping, and Live Session Identity Verification (Issue #1204 Child Loop 5)

## Metadata

* Task ID: issue-1204-rv5-fixes
* Task slug: delivery-1204-coordinator-guard-rv5-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-review.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan-critique.md
* Phase status: complete

<!-- rpi:phase id=P01 -->
## P01: Instruction Alignment, Linear-Time Validator Hardening, and Regression Subtests

<!-- rpi:task id=P01-T01 -->
### P01-T01: Align `.github/agents/ama-backlog-delivery-coordinator.agent.md` and Refresh HVE Assessment SHA

#### Purpose

Align `.agent.md`'s `ready to start` waiting rule with lane-specific concurrent launches and document `--active-sessions <csv>`.

#### Context

* Update lines 274–296 of `.github/agents/ama-backlog-delivery-coordinator.agent.md` so:
  1. `ready to start` bars `"nothing changed"` or global idle summaries, and bars waiting summaries unless active `tmux` sessions are at the declared session cap (`M/N`), an active PR drain (`Open PRs > 15` with drain recorded) holds, or the note records only a lane-specific wait while actively launching ready work in the current check.
  2. The write-time validation command includes `--active-sessions <csv>` alongside `--expect-active-sessions <n>` and `--open-issues <csv>`.
* Refresh the recorded line count and SHA-256 in `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`.

#### Completion Expectations

* `tools/test_rpi_phase_witness.py` and `check_agent_instructions` pass with `0` violations.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement Linear-Time Clause Indexing, Wrapped Block Normalization, Blocker Column/Repo Scoping, and `--active-sessions` in `tools/check-coordinator-handoff.py`

#### Purpose

Eliminate all remaining `O(N^2)` patterns and rescans, normalize wrapped summaries, reject post-target conditional launches, scope blocker verification to full spans/blocker columns/repo-qualified IDs, and verify `--active-sessions` identities.

#### Context

1. Linear-time regexes and `ClauseIndex` (`RV-001`, `PC-001`):
   * `MD_LINK_RE = re.compile(r"\[([^\[\]\n]+)\]\(([^()\s]+)\)")` and `LINKED_SINGLE_ISSUE_CELL_RE` using `[^()\s]+`.
   * Replace `ISSUE_REF_RE` with `HASH_ISSUE_RE = re.compile(r"#(\d+)(?![A-Za-z0-9_-])")` and `_iter_issue_refs(text)` scanning contiguous `[A-Za-z0-9_./-]+` characters immediately before `#` in `O(1)` (validating exact `owner/repo` shape with one `/` and non-empty `owner`/`repo` without regex backtracking or fixed-slice truncation).
   * Replace `DATED_H2_RE` with `_is_dated_h2(line)` (`line.startswith("## ") and bool(ISO_DATE_TOKEN_RE.search(line))`), replace `_strip_md_formatting` regex with `.strip("`*_~ \t\r\n")`, replace `ZERO_UNCLASSIFIED_GUARD_RE` `.*` with two sequential searches, and remove trailing `\s*$` backtracking from `HEADING_RE` and `KV_LINE_RE`.
   * Precompute `ClauseIndex` once per prose block (`span_masked_text` masking backticks and inline URLs preserving trailing punctuation, `clause_starts`, `clause_ends`, per-clause pretokenized tokens emitting `"qtok"` for `INLINE_LITERAL_SPAN_RE` spans + `next_other_idx` + `prev_non_prep_idx` + `PROHIBITION_HEAD_RE` matches + `allow_conditional_guards` `<= 160`-char tail check, and sentence bounds for hold-wait checks) so `_is_claim_negated_at(idx, pos, allow_conditional_guards=...)` runs in `O(log N)` without rescanning `text`, and global hold-wait (`waiting on/for ... before/until/... continuing`) runs in one pass per sentence rather than via an unbounded `[^.;!\n]*` regex.
2. Hard-wrapped prose block normalization (`RV-002`, `PC-002`):
   * Add `_iter_section_prose_blocks(section_lines, table_line_numbers)` joining continuation lines inside non-table paragraphs, list items, and same-depth `>` blockquotes (stripping leading `>` markers on blockquote lines before joining) with `" "`, while breaking blocks on `lineno != prev_lineno + 1` (fenced-code gaps), blank lines, table lines, headings, list-item markers (`^(?:[*+-]|\d+[.)])[ \t]+`), blockquote-depth changes, and recognized metadata KV lines (`KNOWN_METADATA_KEYS`, flushing metadata lines before unindented prose). Run `STALE_CARRY_RE`, `IDLE_CLAIM_RE`, `WAITING_OR_PAUSE_RE`, global hold-wait, `_launches_ready_issue_in_current_tick`, `UNVERIFIED_BLOCKER_RE`, and `_extract_cited_blocker_refs` over normalized `(block_lineno, block_text)` blocks, and feed `_iter_normalized_prose_clauses` from normalized prose blocks in `check_agent_instructions`.
3. Post-target deferred/conditional launch rejection (`RV-003`, `PC-003`):
   * Add `after|once|when|whenever|if|unless|until|before|pending|upon|awaiting|deferred|postponed|skipped|failed` to `NON_CURRENT_LAUNCH_SUBCLAUSE_RE`.
4. Full-span, column-scoped, repo-qualified blocker verification (`RV-004`, `PC-001`, `PC-003`):
   * In `_extract_cited_blocker_refs(text, idx)`, search `BLOCKER_SPAN_STOP_RE.search(idx.span_masked_text, tm.end())` directly without slicing/re-masking `text[tm.end():]`, and extract references only from disjoint `[max(tm.end(), covered_until), end_pos)` slices while updating `covered_until = max(covered_until, end_pos)` for strict `O(N)` single-pass extraction.
   * Normalize blocker references to `(repo_key, number)` (`""` for unqualified local refs and `jmservera/ama`, lowercase `"owner/repo"` for external `github.com/<owner>/<repo>/(?:issues|pull)/<n>` URLs and `owner/repo#<n>` refs), resolving `MD_LINK_RE` `[label](target)` pairs first (inheriting target GitHub URL `repo_key` for matching `#<n>` in the label, then masking `MD_LINK_RE` spans before bare `#<n>` scanning) so `[PR #1641](https://github.com/octo/other/pull/1641)` emits only `("octo/other", 1641)`.
   * In `_extract_classification_tables`, exclude `NON_BLOCKER_COL_HEADERS` (`\bnext\s+actions?\b`, `^actions?$`, `\bowner\b`, `\bnotes?\b`, `\bsummary\b`, `\btitle\b`, `\bpriority\b`, `\bprogress\b`, `\bsprint\b`) first, then select `blocker_cells` from columns matching word-bounded `BLOCKER_COL_RE` (`\b(?:blocker|evidence|link|dependency|reason|pr)\b`) or fallback remaining non-issue/non-category/non-action columns, excluding `Next action` from both `has_valid_blocker_link` and `verified_blocker_evidence_refs`.
5. Live session identity verification (`RV-005`, `PC-003`):
   * Add `active_sessions: set[str] | None = None` to `_validate_section`, `check_handoff_text`, and `check_handoff_file` (evaluated on `is_latest` sections), plus `--active-sessions <csv>` (`none`/empty supported for zero sessions) in `build_arg_parser()` and `main()` and `"--active-sessions"` in `check_agent_instructions` (`required_live_tokens`), emitting `stale-active-session-identity` (including when `active_sessions` is non-empty and `Active sessions` omits backtick session tokens), `stale-active-sessions-count`, and `stale-session-classification` when live `tmux` session names diverge from the handoff.

#### Completion Expectations

* Worst-case input scaling across brackets, unclosed link parens, backticks, slashes, whitespace, and repeated stopped/unstopped triggers is strictly `O(N)`.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Add `RV-001`..`RV-005` Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

#### Purpose

Prove closure of `RV-001`..`RV-005` and `PC-001`..`PC-003` inside the existing 11 `unittest` methods.

#### Context

* Test ownership lock: `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new test methods keeping `11` methods total).
* Add subtests for `"[a" * 4000`, `"[a](b" * 4000`, `"a/b" * 4000`, `"`" * 4000 + "x"`, `"waiting on #1641 " * 400`, and `"waiting on #1641; " * 400` scaling (`< 0.15s`), hard-wrapped `"Nothing\nchanged."`, `"> Nothing\n> changed."`, `"Waiting on\nPR #999."`, and fence-separated negation/idle non-leakage, `"starting #1310 after approval"`, `"Starting #1310 once CI passes"`, and `"#1310 is starting deferred"`, >350-char blocker span citations, `Next action`-only `#999` non-evidence, external `octo/other#1641` / `[PR #1641](https://github.com/octo/other/pull/1641)` blocker mismatch, and `--active-sessions` CLI/API identity mismatch (including omitted backtick tokens).
* Run Focused validation without `tools/rpi-checks.py`.

#### Completion Expectations

* All `11` test methods and all Focused checks exit `0`.
