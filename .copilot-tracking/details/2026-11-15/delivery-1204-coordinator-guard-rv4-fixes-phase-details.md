<!-- markdownlint-disable-file -->
# Phase Details: Resolve RV-001 through RV-004 Constant-Time Suffix Guard, Deferred/Negated Launch Qualification, and URL-Safe Blocker Spans (Issue #1204 Child Loop 4)

## Metadata

* Task ID: issue-1204-rv4-fixes
* Task slug: delivery-1204-coordinator-guard-rv4-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-review.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan-critique.md
* Phase status: complete

<!-- rpi:phase id=P01 -->
## P01: Constant-Time Conditional Suffix, Subclause Launch Qualification, URL-Safe Blocker Spans, and Subtests

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update `tools/check-coordinator-handoff.py` for `RV-001` through `RV-004`

#### Purpose

Eliminate quadratic whitespace scanning, reject deferred/adverb-negated launches, preserve URLs and trailing sentence stops across blocker spans, and stop blocker extraction at coordinated subject-verb launch clauses.

#### Context

1. Linear-time `--` split and conditional guard suffix (`_has_conditional_guard_suffix`, `RV-001`, `PC-001`):
   * Replace `\s+--\s+` with `(?<=\s)--\s+` in both `CLAUSE_SPLIT_RE` and `BLOCKER_SPAN_STOP_RE`.
   * Remove `CONDITIONAL_GUARD_SUFFIX_RE`.
   * Strip trailing spaces/tabs/quotes/backticks and take up to 8 right-split whitespace tokens via `raw_tail = trailing_clause.rstrip(" \t\"'`").rsplit(None, 8)`, lowercase `tokens = [tok.lower() for tok in raw_tail[-7:]]`, pop up to 4 trailing `TRAILING_PREP_DET_TOKENS` items, and check `(len(tokens) >= 2 and tokens[-2].lstrip("\"'`([") == "only" and tokens[-1] == "after") or (len(tokens) >= 3 and tokens[-3].lstrip("\"'`([") == "permitted" and tokens[-2:] == ["only", "when"])` so non-alphabetic tokens such as `#1204` remain preserved and block false guard matching.
2. Subclause-wide negation, subject-first launches, and deferred/future launch qualification (`_launches_ready_issue_in_current_tick`, `RV-002`, `PC-003`):
   * Split subclauses on `SUBCLAUSE_SPLIT_RE = re.compile(r"\bwhile\b|,\s+and\b", re.IGNORECASE)`.
   * Add a subject-first branch to `READY_LAUNCH_RE` matching `(?:(?:issue|worker|session)\s+)?(?:#(\d+)(?![A-Za-z0-9_-])|`?rpi-(\d+)(?:-[A-Za-z0-9_.-]+)?`?)\s+(?:is|has)\s+(?:now\s+)?(?:launch(?:ed|ing)|start(?:ed|ing)|dispatch(?:ed|ing)|spawn(?:ed|ing))\b`.
   * Replace `$-anchored` `LAUNCH_NEG_OR_HOLD_PREFIX_RE` with unanchored `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE` searched across `prefix = line[sub_start : m.start()]`, matching `\b(?:before|until|without|instead\s+of|prior\s+to|unless|if|not|no|never|cannot|can't|must\s+not|do\s+not|don't|unable\s+to|fail(?:ed|ing|s)?\s+to|defer\w*|postpon\w*|skip\w*|(?:hold(?:ing)?|held)\s+off(?:\s+on)?|will|would|could|should|might|may|(?:plan(?:ning|ned|s)?|intend(?:ing|ed|s)?)\s+(?:to|on)|going\s+to)\b|n't\b`.
   * Replace `HISTORICAL_LAUNCH_SUBCLAUSE_RE` with `NON_CURRENT_LAUNCH_SUBCLAUSE_RE` matching `\b(?:previously|earlier|already|yesterday|formerly|later|tomorrow|eventually|soon)\b|(?<!since\s)(?<!since\sthe\s)\b(?:last|prior|previous|next|future|following|subsequent|upcoming)\s+(?:tick|check|run|turn|wave|slot|window|cycle|pass)\b`.
3. URL-masked blocker span and coordinated launch stop (`_extract_cited_blocker_numbers`, `RV-003`, `RV-004`, `PC-002`):
   * Slice `span = line[tm.end() : tm.end() + 300]`.
   * Mask `BACKTICK_TOKEN_RE` to `_` and mask `URL_RE` while preserving trailing `.;!?:,` punctuation (`core = m.group(0).rstrip(".;!?:,")`, `"_" * len(core) + m.group(0)[len(core):]`) before calling `BLOCKER_SPAN_STOP_RE.search(masked_span)`.
   * Add constrained coordinated subject-verb launch stop `,\s+and\s+(?:(?:now|meanwhile|concurrently)\s+)?(?:(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)\b|(?:we|coordinator|delivery|independent\s+(?:lanes?|work|issues?)|(?:(?:issue|worker|session)\s+)?(?:#\d+|_+|rpi-\d+(?:-[A-Za-z0-9_.-]+)?))\s+(?:(?:is|are|has|have)\s+(?:now\s+)?)?(?:launch(?:ed|ing|es)|start(?:ed|ing|s)|dispatch(?:ed|ing|es)|spawn(?:ed|ing|s)|running|continu(?:e|es|ed|ing)|proceed(?:s|ed|ing))\b)` to `BLOCKER_SPAN_STOP_RE`.

#### Completion Expectations

* Worst-case clause and whitespace scaling is strictly linear `O(N)`.
* Live `.agent.md` passes with `0` violations.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

#### Purpose

Prove closure of `RV-001`..`RV-004` and `PC-001`..`PC-003` with targeted `self.subTest` assertions inside the existing 11 test methods.

#### Context

* Test ownership lock: `tools/test_check_coordinator_handoff.py` (`0` removals, `0` added test methods keeping `11` methods total).
* Add 8,000-space scaling assertions (`(" " * 8000) + "nothing changed."` and `"only after" + (" " * 8000) + "x nothing changed."` in `< 0.1s`) plus `"Only after #1204 nothing changed."` rejection, deferred/adverb-negated/modal `-ing` launch assertions plus below-capacity `, and` concurrent-launch acceptance, unlisted `https://github.com/jmservera/ama/pull/999` and `, and #999 before continuing` / `, and PR #999 check run` blocker assertions, and PR-drain `"Waiting on PR #1641, and #1310 is starting now."` + `"Waiting on https://github.com/jmservera/ama/pull/1641; #1310 is starting now."` acceptance assertions.
* Run Focused validation (`ruff check`, `ruff format --isolated --line-length 100 --check`, `python3 tools/check-coordinator-handoff.py`, `python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `python3 -m unittest tools/test_rpi_phase_witness.py -q`, `git --no-pager diff --check`; do NOT run `tools/rpi-checks.py`).

#### Completion Expectations

* All `11` test methods and all Focused checks exit `0`.
