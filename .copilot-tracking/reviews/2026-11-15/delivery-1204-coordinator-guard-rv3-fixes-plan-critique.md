<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resolve RV-001 through RV-003 Linear-Time Negation, Ready-Row Launch Guard, and Qualified Blocker Citations (Issue #1204 Child Loop 3)

## Metadata

* Task ID: issue-1204-rv3-fixes
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Child remediation task `issue-1204-rv3-fixes` (`delivery-1204-coordinator-guard-rv3-fixes`, child of `issue-1204-rv2-fixes`) must resolve all three High-severity findings routed from parent review (`RV-001` nested regex repetition ReDoS -> linear-time `O(N)` prohibition parser; `RV-002` historical or non-ready launch wait suppression -> current-tick `ready_issue_nums` launch guard; `RV-003` qualified PR blocker citations such as `waiting for hosted CI on PR #999` and `waiting on parent PR #999`) under Focused validation (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`) without running `tools/rpi-checks.py`, modifying `.github/agents/ama-backlog-delivery-coordinator.agent.md`, mutating prior review/critique artifacts, or pushing/opening a PR.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md, .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, tools/check-coordinator-handoff.py, and tools/test_check_coordinator_handoff.py.
* Decisions, dependencies, and acceptance criteria considered: `D-1204-1` through `D-1204-4` from research, `FR-01`..`FR-04`, `NFR-01`..`NFR-02`, `P01-T02` depending on `P01-T01`, test-method count lock (`11` methods with `0` removals and `self.subTest` additions), live `.agent.md` conformance at SHA-256 `cbe27e1616b101a313482ec2fc3cdd72977e68309497b53e9223aaab8a96457b`, `< 0.5s` linear-time negation checking, current-tick `ready_rows` launch enforcement, and qualified blocker `#<n>` verification.
* Assessment boundary: Evaluates credibility, algorithmic completeness, edge-case safety, and regression test fidelity of the supplied candidate plan and phase details against the current source files and parent review log; does not execute tests or modify source/plan files.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `RV-001` / `FR-01` | Partial | Linear-time `O(N)` token scanner removes nested quantifiers and preserves all live `.agent.md` prohibition clauses, but raw `'[^']*'` single-quote masking spans across paired English possessives/apostrophes (`PC-004`). |
| `RV-002` / `FR-02` | Partial | `ready_issue_nums` membership closes non-ready launches (`rpi-1204`), and prefix checks catch pre-verb `Previously`, but prefix-only `HISTORICAL_LAUNCH_RE` misses post-object qualifiers (`Started #1310 earlier`, `Launched #1310 last tick`, `Launched rpi-1310 yesterday`) and participle/passive `not`/`*n't` negations (`Not starting #1310`) (`PC-002`). |
| `RV-003` / `FR-03` | Partial | Bounded span extraction catches `waiting for hosted CI on PR #999` and `waiting on parent PR #999`, but `paus(?:e|ed|ing) ... (?:on|for|due to)` leaves `...` underspecified (risking greedy `#<n>` swallowing or lazy cross-clause matching) and `BLOCKER_SPAN_STOP_RE` omits `:`, `, so/but/yet/then`, purpose `to launch/start`, and negation stops (`PC-003`). |
| `FR-04` / `P01-T02` | Partial | Preserves the `11`-method test lock via `self.subTest`, but `"Never claim " + ("idle or " * 80) + "nothing changed."` already finishes in `< 1ms` on the unfixed greedy regex because backtracking triggers only when a non-governed suffix fails at `$` (`PC-001`). |
| `NFR-01` | Partial | Eliminates nested quantifiers in prohibition and launch regexes, contingent on pinning `BLOCKER_TRIGGER_RE` without unbounded/ambiguous filler (`PC-003`). |
| `NFR-02` | Covered | Plan explicitly forbids `.copilot-tracking/` literals in code, tests, docstrings, comments, and commit messages. |
| `D-1204-1`..`D-1204-4` | Covered | Preserves `.github/agents/ama-backlog-delivery-coordinator.agent.md` unchanged, maintains `test_rpi_phase_witness.py` invariants, and keeps Focused validation scope without running `tools/rpi-checks.py`. |
| `P01` / `P01-T01` | Partial | Clear single-phase decomposition; requires targeted specification refinements for `PC-002`, `PC-003`, and `PC-004`. |

## Verdict

* Verdict: Revise
* Rationale: The single-phase architecture and linear-time tokenization strategy directly address `RV-001`..`RV-003` while preserving live `.agent.md` conformance, but three High-severity gaps and one Medium-severity gap in `P01-T01` and `P01-T02` would leave the ReDoS regression test unable to fail on the unfixed regex (`PC-001`), leave natural post-object historical qualifiers (`Started #1310 earlier`, `Launched #1310 last tick`) and `not starting #1310` unguarded (`PC-002`), and risk blocker-swallowing or cross-clause false positives in `_extract_cited_blocker_numbers` (`PC-003`) plus possessive quote-masking collisions (`PC-004`). All four items are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned `RV-001` timing subtest exercises only the greedy accepting path and does not trigger backtracking on the unfixed regex

* Related IDs: `RV-001`, `FR-01`, `FR-04`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md (`P01-T02`), .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md (`FR-04`), and tools/check-coordinator-handoff.py (lines 79-99, `_GOV_LIST_ITEM` and `_PROHIBITION_BODY`).
* Concern: `P01-T02` specifies a single performance subtest on `"Never claim " + ("idle or " * 80) + "nothing changed."`. In the unfixed `_PROHIBITION_BODY`, `trailing_clause` (`"Never claim " + ("idle or " * 80)`) consumes `idle or` pairs greedily straight to `\s*$` and succeeds on the very first path in `< 1ms` with zero backtracking. Exponential $O(2^{N/2})$ backtracking occurs when a trailing ungoverned token (such as `and` or `still`) fails `\s*$` before the claim, as in `"Never claim " + ("idle or " * 80) + "and nothing changed."`.
* Impact: The planned regression test would pass even if the exponential ReDoS defect remained in `tools/check-coordinator-handoff.py`, failing to lock the actual `RV-001` failure mode.
* Smallest useful change: Update `FR-04` and `P01-T02` so the `< 0.5s` `time.perf_counter()` subtest exercises both the accepting path (`"Never claim " + ("idle or " * 80) + "nothing changed."` -> `0` violations) and the failing-suffix backtracking path (`"Never claim " + ("idle or " * 80) + "and nothing changed."` with a `ready to start` row -> `unsupported-idle-ready-work` in `< 0.5s`).
* Action owner: planning parent
* Exact resolving evidence: Updated `FR-04` in .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md and `P01-T02` in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md asserting `< 0.5s` completion and expected verdicts on both the accepting and `"and nothing changed."` rejecting inputs.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Prefix-only historical check and missing participle `not`/`*n't` negation allow `RV-002` bypasses on `ready to start` launches

* Related IDs: `RV-002`, `FR-02`, `FR-04`, `P01-T01`, `P01-T02`
* Evidence: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-review.md (`RV-002`), .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md (`P01-T01` item 2 and `P01-T02`), and tools/check-coordinator-handoff.py (lines 142-152, 325-334).
* Concern: First, `P01-T01` item 2 checks `HISTORICAL_LAUNCH_RE` (`previously|earlier|already|yesterday|formerly|(?:last|prior|previous)\s+(?:tick|check|run|turn|wave)`) only in the same-clause prefix before `m.start()`. In standard English, `earlier`, `yesterday`, `already`, `previously`, and `last/prior/previous tick|check|run|turn|wave` routinely appear after the launched target (`"Started #1310 earlier; waiting on PR #1641."`, `"Launched rpi-1310 last tick; waiting on PR #1641."`, `"Launched #1310 yesterday; waiting on PR #1641."`), where the prefix before `m.start()` is empty. Second, `READY_LAUNCH_RE` matches `-ing` and `-ed` forms (`starting`, `launching`, `started`, `launched`), whose grammatical negations (`"Not starting #1310; waiting on PR #1641."`, `"isn't launching #1310"`, `"has not started #1310"`) match neither `PROHIBITION_HEAD_RE` nor `HOLD_PREPOSITION_SUFFIX_RE`.
* Impact: Post-object historical launch mentions and explicit `"Not starting #1310"` statements still evaluate `_launches_ready_issue_in_current_tick` to `True` and suppress `unsupported-waiting-ready-work` while `ready to start` work sits unlaunched below capacity.
* Smallest useful change: In `FR-02` and `P01-T01` item 2, bound each `READY_LAUNCH_RE` match's enclosing launch subclause by `CLAUSE_SPLIT_RE` and `\bwhile\b`, strip `since\s+(?:the\s+)?(?:last|prior|previous)\s+(?:tick|check|run|turn|wave)` so current-tick `"since the last check"` phrasing remains valid, and reject when `HISTORICAL_LAUNCH_RE` (plus future-tick deferral `(?:next|later|future)\s+(?:tick|check|run|turn|wave)`, keeping bare `"next"` valid) matches anywhere in that launch subclause; also reject pre-match `\b(?:not|\w+n't)\s*$` alongside `HOLD_PREPOSITION_SUFFIX_RE`, and add subtests in `P01-T02` for post-object `"Started #1310 last tick; waiting on PR #1641."` and `"Not starting #1310; waiting on PR #1641."`.
* Action owner: planning parent
* Exact resolving evidence: Updated `FR-02`/`FR-04` in .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md and `P01-T01`/`P01-T02` in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md specifying full-subclause historical/future-tick scanning (excluding `since [the] last/prior/previous ...`), pre-match `not`/`*n't` rejection, and corresponding regression subtests.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Underspecified `BLOCKER_TRIGGER_RE` pause pattern and incomplete `BLOCKER_SPAN_STOP_RE` clause boundaries risk swallowing `#<n>` blockers or falsely flagging subsequent launch clauses

* Related IDs: `RV-003`, `FR-03`, `NFR-01`, `P01-T01`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md (`P01-T01` item 3), tools/check-coordinator-handoff.py (lines 62-69 `CLAUSE_SPLIT_RE`, lines 120-128 `WAITING_OR_PAUSE_RE`, lines 1349-1366), and tools/test_check_coordinator_handoff.py (line 282).
* Concern: `P01-T01` item 3 writes `BLOCKER_TRIGGER_RE` with an unexpanded `...` placeholder in `paus(?:e|ed|ing) ... (?:on|for|due to)`. Implementing `...` with a greedy wildcard (such as `[^.;!?]{0,40}`) causes `"Paused on PR #999 for hosted CI."` to consume `" on PR #999 "` inside the trigger up to `"for"`, missing `#999`; implementing it with a lazy wildcard (`{0,40}?`) causes `"Check paused before launching work for #1310."` to jump across `"before launching work"` to `"for"` and falsely flag `#1310`. In addition, `BLOCKER_SPAN_STOP_RE` omits `:`, `, (?:so|but|yet|then|whereas)\b` (present in `CLAUSE_SPLIT_RE`), infinitival `to` before launch verbs (`"Status: waiting on active session slot to launch #1310."`), and negated continuations (`without`, `never`, `not`), so valid multi-clause or session-cap summaries (for example `"Waiting for hosted CI on PR #1642, so starting #1310 next."` or `"Waiting on PR #1642, but #1310 is starting now."`) scan into the next clause and falsely raise `unverified-blocker-reference` against `ready to start` `#1310`.
* Impact: Ambiguous trigger matching and missing stop boundaries can either miss unlisted `#<n>` blockers on `Paused on PR #999 for ...` or cause false `unverified-blocker-reference` failures on valid multi-clause coordinator status summaries.
* Smallest useful change: Pin `BLOCKER_TRIGGER_RE` in `P01-T01` item 3 to the exact flat `O(N)` alternation `r"\b(?:paus(?:e|ed|ing)\s+(?:(?:the\s+)?(?:run|schedule|delivery|check|tick)\s+)?(?:on|for|due\s+to)|blocked\s+(?:on|by)|waiting\s+(?:on|for))\b"`, and expand `BLOCKER_SPAN_STOP_RE` to include `[.;!?:]`, `\s+--\s+`, `,\s+(?:so|but|yet|then|while|whereas)\b`, `\b(?:while|without|never|must\s+not|do\s+not|don't|cannot|can't)\b`, `\b(?:before|until|instead\s+of|prior\s+to|then|to|so|and(?:\s+now)?)\s+(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)\b`, and `,\s+and\s+(?:#\d+|\[#\d+\]|`?rpi-\d+)\s+(?:is|are|was|were|has|have|merged|closed|started|launched|dispatched|spawned)\b`.
* Action owner: planning parent
* Exact resolving evidence: Updated `FR-03` in .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md and `P01-T01`/`P01-T02` in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md with the exact flat `BLOCKER_TRIGGER_RE` and expanded `BLOCKER_SPAN_STOP_RE` plus a subtest covering `"Paused on PR #999 for hosted CI."`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Unbounded `'[^']*'` single-quote masking in `_trailing_clause_has_governing_prohibition` spans across paired English possessives

* Related IDs: `RV-001`, `FR-01`, `P01-T01`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md (`P01-T01` item 1).
* Concern: `P01-T01` item 1 masks inline literals in `rest = trailing_clause[pm.end():]` by replacing `\"[^\"]*\"|'[^']*'|`[^`]*`` with `" qtok "`. Because `'[^']*'` has no non-word boundary guards, two apostrophes in ordinary English possessives or contractions after a prohibition head (for example `"Never report sessions' failure and ticks' idle tick."`) match `' failure and ticks'` as a single-quoted literal and collapse it to `" qtok "`, erasing `"and"` and ungoverned tokens so the positive second conjunct is misclassified as negated.
* Impact: Paired apostrophes in prose can mask `"and"` and ungoverned tokens inside `_trailing_clause_has_governing_prohibition`, reintroducing a narrow coordinated-conjunction negation bypass.
* Smallest useful change: Guard the single-quote branch of the literal-masking regex in `P01-T01` item 1 with non-alphanumeric lookarounds: `r'"[^"]*"|(?<![A-Za-z0-9])\'[^\']*\'(?![A-Za-z0-9])|`[^`]*`'`.
* Action owner: planning parent
* Exact resolving evidence: Updated literal-masking pattern in `P01-T01` item 1 of .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md using non-alphanumeric boundaries around `'[^']*'`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Replacing `_PROHIBITION_BODY` nested regex repetition with token-level scanning cleanly eliminates ReDoS risk in `O(N)` time while preserving all existing `.github/agents/ama-backlog-delivery-coordinator.agent.md` polarity checks (`Scheduled checks and turns must never claim "nothing changed", emit an idle or waiting summary, or pause on an unverified blocker...`, `never rely on \`gh issue list ...\` counts copied from previous ticks`).
* Extracting verified blocker IDs from both GitHub `/issues/` and `/pull/` URLs and `URL_RE`-stripped prose prevents URL fragment false positives (`https://example.com/1288#999`) while catching unlisted PR and URL blockers.
* Residual risk: Line-oriented prose scanning in `_validate_section` remains heuristic rather than full English dependency parsing, which is appropriate for deterministic offline Markdown validation once `PC-001`..`PC-004` are incorporated.

## Questions or Blocking Evidence Gaps

* None. All supplied artifacts and source files are present and sufficient; no user clarification is needed.

## Limitations

* Read-only assessment of supplied plan, phase details, review log, research, `.agent.md`, validator, and unit tests; Focused validation commands were not executed during plan critique.

## Recommended Next Action

* Highest-impact finding: `PC-002`
* Action owner: planning parent
* Smallest next action: Directly revise `FR-01`..`FR-04` in .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md and `P01-T01`..`P01-T02` in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md to incorporate `PC-001`..`PC-004`, then finalize the plan for `rpi-implement` without another critique pass.
* User response required: no
