<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resolve RV-001 through RV-004 Constant-Time Suffix Guard, Deferred/Negated Launch Qualification, and URL-Safe Blocker Spans (Issue #1204 Child Loop 4)

## Metadata

* Task ID: issue-1204-rv4-fixes
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Child remediation task `issue-1204-rv4-fixes` (`delivery-1204-coordinator-guard-rv4-fixes`), child of `issue-1204-rv3-fixes`, resolving routed findings `RV-001` through `RV-004` in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` under Focused validation (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`; do not run `tools/rpi-checks.py`, do not modify `.github/agents/ama-backlog-delivery-coordinator.agent.md` or prior review records, and do not push or open a PR).
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan.md, .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, tools/check-coordinator-handoff.py, and tools/test_check_coordinator_handoff.py.
* Decisions, dependencies, and acceptance criteria considered: Issue #1204 acceptance criteria 1 through 4; decisions `D-1204-1` through `D-1204-4`; routed findings `RV-001` through `RV-004`; `P01-T02` dependency on `P01-T01`; test ownership lock keeping `11` test methods in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new methods); `NFR-01` linear `O(N)` line scanning and Ruff cleanliness; `NFR-02` zero `.copilot-tracking/` path literals in code, tests, docstrings, comments, or commit messages.
* Assessment boundary: Evaluates algorithmic complexity, regex semantics, false-positive/false-negative parser edge cases, and regression test validity strictly from the supplied plan, phase details, review log, research, coordinator instructions, validator source, and test suite without open-ended external research or executing `tools/rpi-checks.py`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Issue #1204 AC1-AC3 (`D-1204-1`, `D-1204-2`, `D-1204-4`) | Covered | .github/agents/ama-backlog-delivery-coordinator.agent.md remains untouched and verified (`0` violations), preserving all coordinator instruction contracts and `rpi_phase_witness.py` strings (`C9`). |
| `FR-01` / `RV-001` / `NFR-01` | Partial | Removing `CONDITIONAL_GUARD_SUFFIX_RE` leaves `\s+--\s+` quadratic backtracking active inside `CLAUSE_SPLIT_RE` (and `BLOCKER_SPAN_STOP_RE`) on 8,000 spaces, and `re.findall(r"[A-Za-z']+", ...)` strips `#<n>` and numeric tokens after `only after` (`PC-001`). |
| `FR-02` / `RV-002` | Partial | Unanchored `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE` leaks across `, and` clauses when subclauses split only on `while`, misses `held off` and `planning/intending on` before `-ing` gerunds, and leaves subject-first `#<n> is starting` unhandled below capacity (`PC-003`). |
| `FR-03` / `RV-003` & `RV-004` | Partial | `URL_RE` consumes trailing `.`, `;`, and `:` so masking the full match erases sentence stops after bare URLs, while `,\s+and\b[^.;!?\n]{0,50}\b(?:...|run\w*|continu\w*|proceed\w*)\b` truncates unlisted secondary blockers such as `, and #999 before continuing` or `, and PR #999 check run` (`PC-002`). |
| `FR-04` / `P01-T01` / `P01-T02` | Partial | Preserves the `11`-method test lock and Focused validation boundary, but `"Will start #1310; waiting on PR #1641."` passes vacuously without hitting `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE` (`PC-003`), and regression subtests are needed for `PC-001` and `PC-002`. |
| `NFR-02` & Focused tier boundary | Covered | Explicitly forbids `.copilot-tracking/` literals in code/tests/commits and excludes `tools/rpi-checks.py`, `git push`, and PR creation. |

## Verdict

* Verdict: Revise
* Rationale: Single-phase scoping, artifact immutability, and Focused validation boundaries are sound, but three concrete parser/regex defects in `P01-T01` and `P01-T02` (`PC-001` through `PC-003`) would leave quadratic whitespace scanning in `CLAUSE_SPLIT_RE`, introduce new blocker-extraction bypasses and cross-sentence false positives in `_extract_cited_blocker_numbers`, and leave the modal launch guard vacuously tested. All three findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Residual `O(N^2)` whitespace backtracking in `CLAUSE_SPLIT_RE` (`\s+--\s+`) and non-alphabetic token stripping in `_has_conditional_guard_suffix`

* Related IDs: `FR-01`, `NFR-01`, `P01-T01`, `P01-T02` (`RV-001`)
* Evidence: tools/check-coordinator-handoff.py (`CLAUSE_SPLIT_RE` line 72, `BLOCKER_SPAN_STOP_RE` line 217, `_is_claim_negated` line 340); .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan.md (`FR-01`, `FR-04`); .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md (`P01-T01`, `P01-T02`)
* Concern: Deleting `CONDITIONAL_GUARD_SUFFIX_RE` eliminates only one source of multi-thousand-space quadratic scanning. Both `_is_claim_negated` and `_launches_ready_issue_in_current_tick` call `CLAUSE_SPLIT_RE.finditer(masked_line)`, whose `\s+--\s+` branch puts whitespace in the alternation start set and scans/backtracks `N - i` spaces at every space offset `i` (`N * (N + 1) / 2` steps, ~32M operations on 8,000 spaces before `"nothing changed."`). Separately, tokenizing `_has_conditional_guard_suffix` with `re.findall(r"[A-Za-z']+", trimmed.lower())` drops `#<n>` issue tokens, dates, and numbers (for example `"Only after #1204 nothing changed."` or `"Only after 2026-11-15 nothing changed."`), reducing `words` to `["only", "after"]` and falsely negating the idle claim.
* Impact: Worst-case whitespace scaling remains `O(N^2)` (threatening `P01-T02`'s `< 0.1s` assertion on 8,000 spaces), and `_has_conditional_guard_suffix` introduces a false-negative idle-claim bypass whenever non-alphabetic tokens separate `only after` or `permitted only when` from the claim.
* Smallest useful change: Replace `\s+--\s+` with `(?<=\s)--\s+` in both `CLAUSE_SPLIT_RE` and `BLOCKER_SPAN_STOP_RE` so `--` fails in `O(1)` at non-hyphen characters without scanning whitespace runs; implement `_has_conditional_guard_suffix` with `trimmed.lower().split()`, popping up to 4 exact `TRAILING_PREP_DET_TOKENS` items and stripping leading quote/bracket characters (`"'([`) only on the candidate head token (`only` or `permitted`); and test both `(" " * 8000) + "nothing changed."` and `"only after" + (" " * 8000) + "x nothing changed."` (`< 0.1s`) plus rejection of `"Only after #1204 nothing changed."`.
* Action owner: planning parent
* Exact resolving evidence: Revised `FR-01`, `FR-04`, `P01-T01`, and `P01-T02` specifying `(?<=\s)--\s+` in `CLAUSE_SPLIT_RE`/`BLOCKER_SPAN_STOP_RE`, whitespace-split token matching in `_has_conditional_guard_suffix`, and both 8,000-space and `#1204` suffix subtests.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Overbroad `, and ...` stop window and trailing-punctuation URL masking in `_extract_cited_blocker_numbers` cause blocker bypasses and cross-sentence false positives

* Related IDs: `FR-03`, `FR-04`, `P01-T01`, `P01-T02` (`RV-003`, `RV-004`)
* Evidence: tools/check-coordinator-handoff.py (`URL_RE` line 52, `BLOCKER_SPAN_STOP_RE` lines 216-223, `_extract_cited_blocker_numbers` lines 400-423); .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan.md (`FR-03`, `FR-04`); .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md (`P01-T01`, `P01-T02`)
* Concern: Two defects affect `_extract_cited_blocker_numbers` in `FR-03`. First, extending `BLOCKER_SPAN_STOP_RE` with `,\s+and\b[^.;!?\n]{0,50}\b(?:launch\w*|start\w*|dispatch\w*|spawn\w*|run\w*|continu\w*|proceed\w*)\b` bridges arbitrary prepositional blocker objects across `[^.;!?\n]{0,50}` and matches the noun `run` (`check run`, `CI run`). On `"Waiting on PR #1641, and #999 before continuing."`, `"Waiting on PR #1641, and #999 to proceed."`, or `"Waiting on PR #1641, and PR #999 check run."`, the stop matches at `, and` before `#999`, dropping unlisted blocker `#999` and bypassing `unverified-blocker-reference`. Second, `URL_RE` (`r"https?://[^\s)>`]+"`) consumes trailing sentence/clause punctuation (`.`, `;`, `:`, `,`, `!`, `?`); replacing the full `URL_RE` match with `"_" * len(m.group(0))` overwrites the delimiter in `"Waiting on https://github.com/jmservera/ama/pull/1641; #1310 is starting now."` or `"Waiting on https://github.com/jmservera/ama/pull/1641. Issue #1200 closed on main."`, causing `BLOCKER_SPAN_STOP_RE` to bleed into the next clause/sentence and falsely flag `#1310` or `#1200`.
* Impact: Coordinated unlisted blockers after `, and` evade `unverified-blocker-reference`, while valid full-URL blocker sentences followed by `.`, `;`, or `:` trigger false-positive `unverified-blocker-reference` violations on subsequent sentences.
* Smallest useful change: When masking `URL_RE` in `_extract_cited_blocker_numbers`, preserve trailing `.;!?:,` characters unmasked (`core = m.group(0).rstrip(".;!?:,")`; `"_" * len(core) + m.group(0)[len(core):]`), and restrict the `RV-004` `BLOCKER_SPAN_STOP_RE` addition to a direct coordinated subject + active launch/execution verb predicate (for example `,\s+and\s+(?:(?:now|meanwhile|concurrently)\s+)?(?:(?:we|coordinator|delivery|independent\s+(?:lanes?|work|issues?)|(?:issue|worker|session)\s+`?[^`\s,;]+`?|#\d+|`?rpi-\d+(?:-[A-Za-z0-9_.-]+)?`?)\s+)?(?:(?:is|are|has|have)\s+(?:now\s+)?)?(?:launch(?:ed|ing|es)|start(?:ed|ing|s)|dispatch(?:ed|ing|es)|spawn(?:ed|ing|s)|running|continu(?:e|es|ed|ing)|proceed(?:s|ed|ing))\b`, excluding bare noun `run` and `before/until/to` bridges), adding regression subtests for both cases in `P01-T02`.
* Action owner: planning parent
* Exact resolving evidence: Revised `FR-03`, `FR-04`, `P01-T01`, and `P01-T02` preserving trailing punctuation on masked URLs, constraining the `, and` stop branch to coordinated subject-verb launch clauses, and asserting rejection of `"Waiting on PR #1641, and #999 before continuing."` / `"Waiting on PR #1641, and PR #999 check run."` alongside acceptance of `"Waiting on https://github.com/jmservera/ama/pull/1641; #1310 is starting now."`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Vacuous `"Will start #1310"` modal subtest, missing `, and` subclause boundary, and `-ing` complement gaps in `_launches_ready_issue_in_current_tick`

* Related IDs: `FR-02`, `FR-04`, `P01-T01`, `P01-T02` (`RV-002`, `RV-004`)
* Evidence: tools/check-coordinator-handoff.py (`READY_LAUNCH_RE` lines 178-183, `WHILE_SPLIT_RE` line 198, `_launches_ready_issue_in_current_tick` lines 351-397); .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan.md (`FR-02`, `FR-04`); .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md (`P01-T01`, `P01-T02`)
* Concern: `READY_LAUNCH_RE` matches only `-ed`/`-ing` launch verbs (`launch(?:ed|ing)|start(?:ed|ing)|dispatch(?:ed|ing)|spawn(?:ed|ing)`) before `#<n>` or `rpi-<n>`. As a result, `FR-04`'s `"Will start #1310; waiting on PR #1641."` subtest never matches `READY_LAUNCH_RE` and passes vacuously without exercising `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE`, while actual `-ing` phrases that do match `READY_LAUNCH_RE` such as `"Planning on starting #1310"` (`on` rather than `to`) and `"Held off starting #1310"` (`held` rather than `hold`) are missed by `plan(?:ning|ned)?\s+to` and `hold(?:ing)?\s+off`. Furthermore, searching `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE` unanchored across `line[sub_start : m.start()]` while splitting subclauses only on `WHILE_SPLIT_RE` (`\bwhile\b`) causes negations/prepositions in an earlier clause before `, and` (such as `"Waiting on PR #1641 without force-pushing, and starting #1310 now."`) to leak into `prefix` and falsely reject a valid concurrent launch, and subject-first `", and #1310 is starting now"` (`RV-004`) is still rejected below capacity unless `READY_LAUNCH_RE` also recognizes subject-first `#<n> is/has starting/started`.
* Impact: The new modal/irrealis guard in `FR-02` is not falsifiably tested by `"Will start #1310"`, misses `held off` and `planning/intending on` `-ing` forms, and falsely flags valid `, and starting #1310 now` or `, and #1310 is starting now` concurrent launches below capacity.
* Smallest useful change: Split launch subclauses on `SUBCLAUSE_SPLIT_RE = re.compile(r"\bwhile\b|,\s+and\b", re.IGNORECASE)`; update `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE` to use `(?:hold(?:ing)?|held)\s+off` and `(?:plan(?:ning|ned)?|intend(?:ing|ed)?)\s+(?:to|on)`; add a subject-first branch to `READY_LAUNCH_RE` (or companion check) matching `(?:#(\d+)(?![A-Za-z0-9_-])|`?rpi-(\d+)(?:-[A-Za-z0-9_.-]+)?`?)\s+(?:is|has)\s+(?:now\s+)?(?:launch(?:ed|ing)|start(?:ed|ing)|dispatch(?:ed|ing)|spawn(?:ed|ing))\b` (unpacking the extra capture groups cleanly); and include `"Will be starting #1310; waiting on PR #1641."`, `"Planning on starting #1310; waiting on PR #1641."`, and `"Held off starting #1310; waiting on PR #1641."` alongside `"Will start #1310; waiting on PR #1641."` plus a below-capacity concurrent-launch acceptance subtest in `P01-T02`.
* Action owner: planning parent
* Exact resolving evidence: Revised `FR-02`, `FR-04`, `P01-T01`, and `P01-T02` covering `,\s+and\b` subclause splitting, `held off` and `planning/intending on` prefixes, subject-first `#<n> is starting` recognition, and non-vacuous `-ing` modal/deferred regression subtests.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Single-phase decomposition (`P01-T01` -> `P01-T02`), preservation of `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`sha256: cbe27e1616b101a313482ec2fc3cdd72977e68309497b53e9223aaab8a96457b`), immutable retention of prior review artifacts, and the `11`-method `unittest` ownership lock are crisp and well-bounded.
* Residual risk (accepted in research `C6`/`C7`): Offline deterministic regex and table heuristics validate coordinator handoff/status Markdown structure and high-value prose claims without full natural-language parsing or live multi-tick `tmux` runtime execution.

## Questions or Blocking Evidence Gaps

* None. All three findings have deterministic evidence-backed resolutions within the existing file scope.

## Limitations

* Per caller instructions for Focused-tier critique, `tools/rpi-checks.py` was not executed and no files outside `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan-critique.md` were modified.

## Recommended Next Action

* Highest-impact finding: `PC-001` (paired with High-severity `PC-002`)
* Action owner: planning parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md` to incorporate `PC-001` through `PC-003`, mark planning status `final` with critique disposition recorded, and proceed to `rpi-implement` without another critique pass.
* User response required: no
