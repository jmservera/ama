<!-- markdownlint-disable-file -->
# Phase Details: Resolve RV-001 through RV-003 Linear-Time Negation, Ready-Row Launch Guard, and Qualified Blocker Citations (Issue #1204 Child Loop 3)

## Metadata

* Task ID: issue-1204-rv3-fixes
* Task slug: delivery-1204-coordinator-guard-rv3-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md
* Routed review: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-review.md
* Phase status: complete

<!-- rpi:phase id=P01 -->
## P01: Linear-Time Prohibition Scanner, Ready-Row Launch Check, Qualified Blocker Extraction, and Subtests

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement Linear-Time Prohibition Scanner, Ready-Row Launch Guard, and Qualified Blocker Extraction in `tools/check-coordinator-handoff.py`

#### Purpose

Remove catastrophic regex backtracking and close the historical-launch and qualified-PR-citation validator bypasses.

#### Context

1. Linear-time `O(N)` prohibition suffix check (`_trailing_clause_has_governing_prohibition`, `RV-001`):
   * Delete `_GOV_VERB`, `_GOV_LIST_ITEM`, `_PROHIBITION_BODY`, `PROHIBITION_SUFFIX_RE`, and `HANDOFF_NEGATION_SUFFIX_RE`.
   * Check optional flat `CONDITIONAL_GUARD_SUFFIX_RE = re.compile(r"\b(?:permitted\s+only\s+when|only\s+after)\s+(?:(?:on|for|an?|the|any|global)\s+){0,4}[\"'`]*\s*$", re.IGNORECASE)` when `allow_conditional_guards=True`.
   * Find `PROHIBITION_HEAD_RE = re.compile(r"\b(?:(never|cannot|can't|must\s+not|do\s+not|don't)(?:\s+ever)?|(forbid\w*|prohibit\w*|bars?|excludes?|reject\w*))\b", re.IGNORECASE)` matches in `trailing_clause` and inspect at most the last 4 matches in reverse.
   * For a candidate match `pm`, take `rest = trailing_clause[pm.end():]`, replace `\"[^\"\n]*\"|(?<![A-Za-z0-9])'[^'\n]*'(?![A-Za-z0-9])|`[^`\n]*`` with `" qtok "` in one linear pass (`PC-004`), tokenize words via `re.findall(r"[A-Za-z0-9_']+", rest.lower())`, and ensure no disallowed characters (`;`, `:`) appear.
   * Strip trailing determiners/prepositions (`on`, `for`, `a`, `an`, `the`, `any`, `global`) from the token list.
   * For modal/adverbial heads (`pm.group(1)`): accept empty or `["be"]`, or require `tokens[0]` to match flat `GOV_VERB_TOKEN_RE` (`repeat\w*|claim\w*|report\w*|emit\w*|say\w*|stat\w*|writ\w*|assert\w*|accept\w*|allow\w*|permit\w*|launch\w*|start\w*|dispatch\w*|spawn\w*|paus\w*|wait\w*|cop(?:y|ies|ied|ying)|carr(?:y|ies|ied|ying)|cach\w*|reus\w*|rel(?:y|ies|ied|ying)`) and every `tok in tokens[1:]` to either be in `GOV_CONTINUATION_TOKENS` (`qtok`, `or`, `nor`, `on`, `for`, `over`, `a`, `an`, `the`, `any`, `global`, `idle`, `waiting`, `pause`, `tick`, `ticks`, `summary`, `summaries`, `state`, `states`, `claim`, `claims`, `count`, `counts`, `sha`, `shas`, `session`, `sessions`, `snapshot`, `snapshots`) or match `GOV_VERB_TOKEN_RE`. Notice `"and"` is excluded from `GOV_CONTINUATION_TOKENS`, rejecting coordinated positive conjuncts in `O(N)` time!
   * For verb heads (`pm.group(2)`, e.g. `bars`, `forbids`): require every `tok in tokens` to be in `GOV_CONTINUATION_TOKENS` or match `GOV_VERB_TOKEN_RE`.
   * Update `_is_claim_negated(line, match_start, *, allow_conditional_guards: bool = True) -> bool` and pass `allow_conditional_guards=False` from `check_agent_instructions`.
2. Ready-row non-historical launch guard (`_launches_ready_issue_in_current_tick`, `RV-002`):
   * Match `READY_LAUNCH_RE` with bounded `{0,4}` qualifier words capturing `#(\d+)` or `` `?rpi-(\d+)(?:-[A-Za-z0-9_.-]+)?`? ``.
   * Compute `ready_issue_nums = {r.issue_number for r in ready_rows if r.issue_number is not None}`.
   * Accept a match `m` only when `target_num in ready_issue_nums`, `not _is_claim_negated(line, m.start())`, the subclause prefix before `m.start()` neither ends with `HOLD_PREPOSITION_SUFFIX_RE` (`before|until|without|instead of|prior to|not|n't|no`) nor contains negation, and the full enclosing launch subclause (`sub_start`..`sub_end`) does not match `HISTORICAL_LAUNCH_RE` (`previously|earlier|already|yesterday|formerly|(?<!since\s)(?<!since\sthe\s)\b(?:last|prior|previous)\s+(?:tick|check|run|turn|wave)`) (`PC-002`).
3. Bounded blocker-span `#<n>` extraction (`_extract_cited_blocker_numbers`, `RV-003`, `PC-003`):
   * Match flat `BLOCKER_TRIGGER_RE` (`\b(?:paus(?:e|ed|ing)\s+(?:(?:the\s+)?(?:run|schedule|delivery|check|tick)\s+)?(?:on|for|due\s+to)|blocked\s+(?:on|by)|waiting\s+(?:on|for))\b`).
   * Skip triggers negated by `_is_claim_negated(line, tm.start())`.
   * Slice `line[tm.end() : tm.end() + 200]` and truncate at `BLOCKER_SPAN_STOP_RE` (`[.;!?:]`, `\s+--\s+`, `,\s+(?:so|but|yet|then|while|whereas)\b`, `\bwhile\b`, `\b(?:never|cannot|can't|must\s+not|do\s+not|don't)\b`, or `\b(?:before|until|instead\s+of|then|to|and(?:\s+now)?)\s+(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)\b`).
   * Extract deduplicated issue/PR ints from `GITHUB_ISSUE_PR_URL_RE` inside `URL_RE` spans and `ISSUE_REF_RE` inside `URL_RE`-stripped prose within the truncated span.

#### Completion Expectations

* Worst-case clause runtime is strictly linear `O(N)`.
* Live `.agent.md` passes with `0` violations.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add Performance and Behavioral Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

#### Purpose

Prove `RV-001` (`O(N)` timing), `RV-002` (historical and non-ready launch rejection), and `RV-003` (qualified PR blocker citation rejection) with deterministic subtests inside the existing 11 test methods.

#### Context

* Test ownership lock: `tools/test_check_coordinator_handoff.py` (`0` removals, `0` added test methods keeping `11` methods total; add `self.subTest` cases inside `test_adversarial_rv001_handoff_bypasses_rejected`).
* Add `time.perf_counter()` subtest verifying both `"Never claim " + ("idle or " * 80) + "and nothing changed."` (failing-suffix ReDoS path asserting `unsupported-idle-ready-work`) and `"Never claim " + ("idle or " * 80) + "nothing changed."` complete in `< 0.5` seconds (`PC-001`).
* Add subtests rejecting `"Previously launched rpi-1204; waiting on PR #1641."`, `"Previously started #1310; waiting on PR #1641."`, `"Started #1310 last tick; waiting on PR #1641."`, `"Not starting #1310; waiting on PR #1641."`, and `"Launched rpi-1204; waiting on PR #1641."` when `#1310` is `ready to start` below capacity (`unsupported-waiting-ready-work`, `PC-002`).
* Add subtests rejecting `"Waiting for hosted CI on PR #999."` and `"Waiting on parent PR #999."` when `#999` is absent from verified table evidence (`unverified-blocker-reference`).
* Run Focused validation suite (`ruff check`, `ruff format --isolated --line-length 100 --check`, `python3 tools/check-coordinator-handoff.py`, `python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `python3 -m unittest tools/test_rpi_phase_witness.py -q`, `git --no-pager diff --check`; do NOT run `tools/rpi-checks.py`).

#### Completion Expectations

* All `11` test methods and all Focused checks exit `0`.
