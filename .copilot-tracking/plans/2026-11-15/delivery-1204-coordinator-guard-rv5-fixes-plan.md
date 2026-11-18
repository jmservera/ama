<!-- markdownlint-disable-file -->
# Implementation Plan: Resolve RV-001 through RV-005 Linear-Time Clause Indexing, Wrapped Summary Normalization, Blocker Column/Repo Scoping, and Live Session Identity Verification (Issue #1204 Child Loop 5)

## Metadata

* Task ID: issue-1204-rv5-fixes
* Task slug: delivery-1204-coordinator-guard-rv5-fixes
* Parent task ID: issue-1204-rv4-fixes (`delivery-1204-coordinator-guard-rv4-fixes`)
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md (`satisfied-and-skipped`)
* Routed review source: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-review.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-changes.md
* Planning execution status: complete
* Planning status: complete

## Executive Summary

Parent review (.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-review.md) routed five validator and instruction-alignment findings: `RV-001` (quadratic regex cases in `MD_LINK_RE`, `ISSUE_REF_RE`, and `_strip_md_formatting` plus repeated whole-line rescans in `_is_claim_negated`, `GLOBAL_WAIT_OR_PAUSE_RE`, and `_extract_cited_blocker_numbers`), `RV-002` (hard-wrapped multi-line summaries including blockquotes and fence-adjacent prose bypassing line-by-line prose scanning), `RV-003` (coordinator `.agent.md` waiting rule omitting the lane-specific concurrent-launch exception while `NON_CURRENT_LAUNCH_SUBCLAUSE_RE` accepts post-target `"starting #1310 after approval"` or passive deferrals), `RV-004` (blocker verification truncating spans at 300 chars, counting `Next action` cells as blocker evidence, and discarding `owner/repo` qualifiers or leaking Markdown link labels), and `RV-005` (missing `--active-sessions <csv>` live session identity check). Preserving all prior review logs immutable and incorporating single-pass critique refinements `PC-001`..`PC-003`, this single-phase plan resolves `RV-001`..`RV-005` across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` under Focused validation.

## Sources and Evidence

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-review.md: Routed findings `RV-001`..`RV-005`.
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Issue #1204 acceptance criteria 1–4 and Focused validation boundary.
* .github/agents/ama-backlog-delivery-coordinator.agent.md: Live coordinator instructions.
* tools/check-coordinator-handoff.py and tools/test_check_coordinator_handoff.py.

## User Decisions and Requirements

* Prove all four Issue #1204 acceptance criteria with `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, and `tools/test_check_coordinator_handoff.py` (`unittest`).
* Use Focused validation only (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`); do NOT run `tools/rpi-checks.py`.
* Keep closed review and critique files immutable; commit locally on `fix/delivery-1204-coordinator-guard` without pushing or opening a PR.

## Goals

* Eliminate all remaining quadratic regexes and repeated per-match line rescans via `#`-anchored issue scanning, bracket-disjoint link scanning, and a single-pass `ClauseIndex` per prose block.
* Collapse hard-wrapped Markdown paragraphs and list-item continuations before running idle, waiting, stale-carry, and blocker checks.
* Align `.agent.md` lane-specific concurrent-launch wording with the validator and reject post-target deferred/conditional launches (`after`, `once`, `when`, `if`, `unless`, `until`, `before`, `pending`, `upon`, `awaiting`).
* Scan full blocker spans without arbitrary 300-char cutoffs, restrict table blocker evidence to blocker/evidence columns (excluding `Next action`), preserve `(repo_key, number)` blocker identities, and support `--active-sessions <csv>` live session identity verification.

## Scope and Non-Goals

* In scope: `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` (SHA-256 refresh), and child-loop-5 `.copilot-tracking/` RPI artifacts.
* Non-goals: Mutating prior review logs, running `tools/rpi-checks.py`, or pushing/opening a PR.

## Functional Requirements

* `FR-01` (`RV-001`, `PC-001`): Guarantee linear-time `O(N)` regex and clause scanning across `tools/check-coordinator-handoff.py`:
  * Replace `MD_LINK_RE` and `LINKED_SINGLE_ISSUE_CELL_RE` link-target groups with paren-and-bracket-disjoint `[^()\s]+` (`r"\[([^\[\]\n]+)\]\(([^()\s]+)\)"`); replace `ISSUE_REF_RE` with `HASH_ISSUE_RE = re.compile(r"#(\d+)(?![A-Za-z0-9_-])")` + `_iter_issue_refs(text)` scanning contiguous `[A-Za-z0-9_./-]+` characters before `#` in `O(1)` without regex backtracking or fixed-offset mid-token truncation; replace `DATED_H2_RE` `.*` with `_is_dated_h2(line)` (`line.startswith("## ")` + `ISO_DATE_TOKEN_RE`); replace `_strip_md_formatting` regex with `.strip("`*_~ \t\r\n")`, `ZERO_UNCLASSIFIED_GUARD_RE` `.*` with two sequential searches, and unbounded `HEADING_RE`/`KV_LINE_RE` trailing whitespace groups with `.strip()`.
  * Precompute a single-pass `ClauseIndex` per prose block (`span_masked_text` masking backticks and inline URLs once, `clause_starts`, `clause_ends`, per-clause pretokenized tokens emitting `"qtok"` for `INLINE_LITERAL_SPAN_RE` spans, prohibition state supporting `allow_conditional_guards: bool = True` via a `<= 160`-char tail window, and sentence bounds for hold-wait checks) so `_is_claim_negated_at`, global hold-wait detection (`waiting on/for ... before/until/... continuing`), `_launches_ready_issue_in_current_tick`, and `_extract_cited_blocker_refs` never rescan or re-slice the whole block per match (`O(N + M log N)`).
* `FR-02` (`RV-002`, `PC-002`): Normalize hard-wrapped prose blocks in `_validate_section` and `_iter_normalized_prose_clauses` via `_iter_section_prose_blocks(section_lines, table_line_numbers)`, joining continuation lines within non-table paragraphs, list items, and same-depth `>` blockquotes (stripping leading `>` markers on blockquote lines before joining), breaking blocks on fenced-code line gaps (`lineno != prev_lineno + 1`), blank lines, table lines, headings, list-item markers, blockquote-depth transitions, and recognized metadata KV lines (`KNOWN_METADATA_KEYS`, flushing metadata lines before unindented prose) so wrapped claims such as `"Nothing\nchanged."`, `"> Nothing\n> changed."`, and `"Waiting on\nPR #999."` are caught without leaking negation across fenced code blocks or metadata lines.
* `FR-03` (`RV-003`, `RV-005`, `PC-003`): Update `.github/agents/ama-backlog-delivery-coordinator.agent.md` (preserving all `rpi_phase_witness.py` required phrases) to:
  * Explicitly state that a `ready to start` row bars `"nothing changed"` or global idle summaries, and bars waiting summaries unless active `tmux` sessions are at the declared session cap (`M/N`), an active PR drain (`Open PRs > 15` with drain recorded) holds, or the note records only a lane-specific wait while actively launching ready work in the current check.
  * Document `--active-sessions <csv>` on the write-time `tools/check-coordinator-handoff.py` command, enforce `"--active-sessions"` in `check_agent_instructions` (`required_live_tokens`), and refresh the SHA-256 in `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`.
  * Expand `NON_CURRENT_LAUNCH_SUBCLAUSE_RE` in `tools/check-coordinator-handoff.py` to reject post-target conditional/deferred subordinators and passive deferrals (`after`, `once`, `when`, `whenever`, `if`, `unless`, `until`, `before`, `pending`, `upon`, `awaiting`, `deferred`, `postponed`, `skipped`, `failed`) inside launch subclauses.
* `FR-04` (`RV-004`, `RV-005`, `PC-001`, `PC-003`): Tighten blocker evidence and live session identity verification in `tools/check-coordinator-handoff.py`:
  * Remove the 300-character slice cap in `_extract_cited_blocker_refs`, search `BLOCKER_SPAN_STOP_RE.search(idx.span_masked_text, tm.end())` directly without slicing/re-masking `text[tm.end():]`, and inspect only disjoint `[max(tm.end(), covered_until), end_pos)` slices so both unstopped (>300-char) and stopped (`"waiting on #1641; " * 400`) spans run in strict `O(N)` time.
  * Restrict classification-table blocker link and evidence extraction by excluding `NON_BLOCKER_COL_HEADERS` (`\bnext\s+actions?\b`, `^actions?$`, `owner`, `notes?`, `summary`, `title`) first and matching blocker columns on word boundaries (`\b(?:blocker|evidence|link|dependency|reason|pr)\b`, falling back to remaining non-action/non-issue/non-category columns when no explicit blocker header matches) so `#<n>` references in `Next action` or `Priority` never count as blocker links or verified blocker evidence.
  * Represent blocker references as normalized `(repo_key, number)` tuples (`""` for local/unqualified and `jmservera/ama`, lowercase `"owner/repo"` for external GitHub URLs and `owner/repo#<n>` refs), resolving `MD_LINK_RE` `[label](target)` pairs before bare `#<n>` scanning so `[PR #1641](https://github.com/octo/other/pull/1641)` emits only `("octo/other", 1641)` without phantom local label leakage.
  * Add optional `active_sessions: set[str] | None = None` and CLI `--active-sessions <csv>` (evaluated on `is_latest` sections), flagging `stale-active-session-identity` (including when `active_sessions` is non-empty and `Active sessions` omits backtick session tokens), `stale-active-sessions-count`, and `stale-session-classification` when live `tmux` session names differ from recorded `Active sessions` tokens or `active session` rows.
* `FR-05` (`PC-001`..`PC-003`): Lock test ownership in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new test methods keeping `11` methods total; add `self.subTest` cases inside existing methods) covering:
  * `< 0.15s` linear scaling on `"[a" * 4000`, `"[a](b" * 4000`, `"a/b" * 4000`, `"`" * 4000 + "x"`, `"waiting on #1641 " * 400`, and `"waiting on #1641; " * 400` (`RV-001` / `PC-001`).
  * Rejection of hard-wrapped `"Nothing\nchanged."`, `"> Nothing\n> changed."`, and `"Waiting on\nPR #999."`, plus non-leakage of negation across fenced code blocks (`RV-002` / `PC-002`).
  * Rejection of `"Waiting on PR #1641 while starting #1310 after approval."`, `"Starting #1310 once CI passes; waiting on PR #1641."`, and `"Waiting on PR #1641 while #1310 is starting deferred."` (`RV-003` / `PC-003`).
  * Extraction/rejection of blocker citations past 350 characters, `#999` cited only in `Next action` (`| #1288 | human-blocked | #1288#issuecomment-42 | Unblocks #999 later |`), and external `octo/other#1641` / `[PR #1641](https://github.com/octo/other/pull/1641)` when only local `#1641` is classified (`RV-004` / `PC-003`).
  * Rejection of stale session identity via `--active-sessions rpi-1310` both when handoff lists ``1/8 (`rpi-1204`)`` and when handoff omits backtick names (`1/8`) (`RV-005` / `PC-003`).

## Non-Functional Requirements

* `NFR-01`: Stdlib-only Python 3.12+, strict linear `O(N)` worst-case input scaling, passing `ruff check` and `ruff format --isolated --line-length 100 --check`.
* `NFR-02`: Zero `.copilot-tracking/` path literals in `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, comments, docstrings, or commit messages.

## Acceptance Criteria

* All four Issue #1204 acceptance criteria and all `RV-001`..`RV-005` regression subtests pass with `0` violations on `.github/agents/ama-backlog-delivery-coordinator.agent.md` and Focused validation exit code `0`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Instruction Alignment, Linear-Time Validator Hardening, and Regression Subtests

* Intent: Resolve `RV-001`..`RV-005` across coordinator instructions, validator, HVE SHA record, and unit tests.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Align `.github/agents/ama-backlog-delivery-coordinator.agent.md` and Refresh HVE Assessment SHA

* Requirement and evidence: `FR-03`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-review.md
* Expected result: `.agent.md` states the lane-specific concurrent-launch rule and `--active-sessions <csv>` flag cleanly, `test_rpi_phase_witness.py` passes, and `delivery-1204-coordinator-guard-hve-assessment.md` records the current SHA-256.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement Linear-Time Clause Indexing, Wrapped Block Normalization, Blocker Column/Repo Scoping, and `--active-sessions` in `tools/check-coordinator-handoff.py`

* Requirement and evidence: `FR-01`..`FR-04`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-review.md
* Expected result: `RV-001`..`RV-005` resolved in `tools/check-coordinator-handoff.py` with `0` violations on `.agent.md`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Add `RV-001`..`RV-005` Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

* Requirement and evidence: `FR-05`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-review.md
* Expected result: All `11` test methods and all Focused checks exit `0`.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01`; `P01-T03` depends on `P01-T01` and `P01-T02`.

## Critique Disposition

Single-pass critique executed at .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-plan-critique.md (Verdict: `Revise`, `0` Critical, `1` High, `2` Medium, `0` Low; user response required: `no`):

* `PC-001` [High] (`direct_planner_correction`, applied): Excluded `(` in `MD_LINK_RE`/`LINKED_SINGLE_ISSUE_CELL_RE` (`[^()\s]+`), replaced `_strip_md_formatting` regex with `.strip("`*_~ \t\r\n")` and `ZERO_UNCLASSIFIED_GUARD_RE` `.*` with sequential searches, scanned contiguous `[A-Za-z0-9_./-]+` prefixes before `#` in `O(1)`, updated `ClauseIndex` to emit `"qtok"` for inline literals, mask inline URLs in clause/sentence bounds, and retain `allow_conditional_guards`, updated `_extract_cited_blocker_refs` to search `BLOCKER_SPAN_STOP_RE` over `idx.span_masked_text` across disjoint `[max(tm.end(), covered_until), end_pos)` slices without slicing `text[tm.end():]`, and added scaling subtests for `"[a](b" * 4000`, `"waiting on #1641; " * 400`, and `"`" * 4000 + "x"`.
* `PC-002` [Medium] (`direct_planner_correction`, applied): Updated `_iter_section_prose_blocks` (and `_iter_normalized_prose_clauses`) to break blocks on fenced-code line gaps (`lineno != prev_lineno + 1`) and blockquote-depth transitions, strip leading `>` on wrapped blockquote lines (`"> Nothing\n> changed."`), flush unpunctuated `KNOWN_METADATA_KEYS` lines before unindented prose, and added wrapped-blockquote and fence-boundary subtests.
* `PC-003` [Medium] (`direct_planner_correction`, applied): Excluded `NON_BLOCKER_COL_HEADERS` before word-bounded `BLOCKER_COL_RE` (`\b(?:blocker|evidence|link|dependency|reason|pr)\b`), resolved `MD_LINK_RE` `[label](target)` pairs before bare `#<n>` repo extraction (`[PR #1641](https://github.com/octo/other/pull/1641)`), flagged omitted backtick session tokens when `active_sessions` is non-empty on `is_latest` sections, added `"--active-sessions"` to `check_agent_instructions`, and added passive post-target deferrals (`deferred`, `postponed`, `skipped`, `failed`) to `NON_CURRENT_LAUNCH_SUBCLAUSE_RE`.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
