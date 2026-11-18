<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resolve Validator Edge-Case Defects RV-001 through RV-003 (Issue #1204 Child Loop 2)

## Metadata

* Task ID: issue-1204-rv2-fixes
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Bounded child remediation loop `issue-1204-rv2-fixes` (`delivery-1204-coordinator-guard-rv2-fixes`) resolving routed validator defects `RV-001` (High), `RV-002` (Medium), and `RV-003` (Medium) in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` under Focused validation without mutating prior review/critique artifacts, without running `tools/rpi-checks.py`, and without pushing or opening a PR.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md, .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, tools/check-coordinator-handoff.py, and tools/test_check_coordinator_handoff.py.
* Decisions, dependencies, and acceptance criteria considered: Issue #1204 AC1 through AC4 (`D-1204-1` through `D-1204-4`), routed review defects `RV-001` through `RV-003`, single-phase dependency `P01-T02` after `P01-T01`, Focused validation commands (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`), locked `11`-method test suite boundary (`0` removals, `0` new methods, `self.subTest` additions only), and unchanged `.github/agents/ama-backlog-delivery-coordinator.agent.md` SHA-256 `cbe27e1616b101a313482ec2fc3cdd72977e68309497b53e9223aaab8a96457b`.
* Assessment boundary: Evaluates plan and phase-details correctness, regex/parser semantics, regression coverage, and edge-case closure strictly from the supplied tracking artifacts and current `tools/` implementation files; does not inspect files outside the caller read boundary or execute `tools/rpi-checks.py`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `RV-001` / `FR-01` (`_is_claim_negated`) | Partial | Anchored prohibition-suffix design closes coordinated-conjunction bypasses, but `P01-T01` Context #1 omits literal backticks preserved by `BACKTICK_TOKEN_RE`, trailing quotes/determiners (`"`, `an`) before `match_start`, gerund verb inflections, and multi-occurrence `finditer` scanning in `check_agent_instructions` (`PC-001`). |
| `RV-002` / `FR-02` (PR blocker lookup)   | Partial | Checking `classified_by_num` before `verified_blocker_evidence_nums` preserves rejection of `ready to start` / `merged` issues, but `CITED_BLOCKER_REF_RE` omits `PR #<n>` citations and raw `ISSUE_REF_RE` scanning of `non_issue_cells` leaks URL `#fragment` digits (`PC-002`). |
| `RV-002` / `FR-03` (concurrent waits)    | Partial | Separating global stall/pause patterns from concurrent launches preserves pre-summary table and unclassified checks, but unscoped `start(?:ed|ing)` in `CONCURRENT_LAUNCH_RE` false-passes routine `"Check started ...; waiting ..."` prose and `GLOBAL_WAIT_OR_PAUSE_RE` lacks `_is_claim_negated` gating and `prior to`/`instead of`/`until` forms (`PC-002`). |
| `RV-003` / `FR-04` (linked Issue IDs)    | Partial | `MD_LINK_RE` label parsing covers `[#1288](https://.../issues/1288)`, but `P01-T01` Context #4 does not reject mismatched `/issues/<other>` targets, `javascript:`/`data:` targets, or self-number `#1288` non-heading anchors in the `Issue` column (`PC-003`). |
| `RV-003` / `FR-05` (`P01-T02` subtests)  | Partial | Locked `11`-method `self.subTest` plan is clean, but `P01-T02` needs aligned PR numbers (`PR #1642`) on the active-launch fixture plus subtests for the `PC-001` through `PC-003` edge cases (`PC-002`, `PC-003`). |
| `P01` / `P01-T01` / `P01-T02`            | Partial | Single-phase sequencing, Focused validation commands, and artifact immutability boundaries are sound once `PC-001` through `PC-003` are folded into the plan and phase details. |

## Verdict

* Verdict: Revise
* Rationale: The single-phase remediation structure and target boundary rightly preserve `.github/agents/ama-backlog-delivery-coordinator.agent.md` and prior review logs, but `P01-T01` contains concrete regex and parser defects (`PC-001`, `PC-002`, `PC-003`) that would break two existing unit tests (`test_check_coordinator_handoff.py` lines 368 and 500), break `check_agent_instructions` on quoted `"nothing changed"` and `"pause on an unverified blocker"`, and leave false-pass loopholes on non-delivery `"started"` prose and `"Waiting on PR #999"`. All three findings are direct planner corrections requiring zero user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Anchored negation suffix specification breaks valid backticked CLI flags, trailing quotes/determiners, gerund prohibitions, and multi-mention agent clauses

* Related IDs: `RV-001`, `FR-01`, `P01`, `P01-T01`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md (`P01-T01` Context item 1), .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md (`FR-01`), tools/check-coordinator-handoff.py (lines 242-260 and 422-441), and tools/test_check_coordinator_handoff.py (lines 107-120, 368-369, and 500-505)
* Concern: Four concrete mismatches exist between `P01-T01` Context item 1 and `tools/check-coordinator-handoff.py`:
  1. `P01-T01` specifies `rely\s+on(?:\s+_[A-Za-z0-9_.\s-]*_)?`, assuming `_is_claim_negated` replaces backticks with underscores, whereas `BACKTICK_TOKEN_RE.sub(lambda m: re.sub(r"[;.!?:,]", "_", m.group(0)), line)` at `tools/check-coordinator-handoff.py:250-253` preserves literal backticks `` `...` `` (and CLI characters such as `--`, `/`, `=`, and `'`).
  2. In `check_agent_instructions` (`tools/check-coordinator-handoff.py:425`), `nc_idx = low_clause.find("nothing changed")` places `match_start` after the opening quote/backtick (`never claim "` or ``never claim `"``), and in both `check_agent_instructions` (`line 435`) and `UNVERIFIED_BLOCKER_RE` (`line 116`), `match_start` lands at `unverified` after the determiner `an ` (`must never claim "nothing changed" or pause on an `). Ending the suffix regex at `pause(?:\s+on)?` + `\s*$` without optional determiners (`(?:a|an|any|the)\s+`) and opening quote/backtick wrappers (`["'`]*`) fails valid negated clauses.
  3. `PROHIBITION_SUFFIX_RE` includes verbs such as `forbid\w*|prohibit\w*|bars?|excludes?|reject\w*` that govern `-ing` gerunds (`claiming`, `reporting`, `emitting`, `pausing on`, `waiting on/for`, `copying`, `carrying over`, `caching`, `relying on`), which are absent from the bare-infinitive verb list in `P01-T01`.
  4. `check_agent_instructions` (`tools/check-coordinator-handoff.py:425,435`) checks only the first `.find(...)` index in `clause`, so a single clause with a negated first mention and an unnegated second mention (`Never claim "nothing changed" early, and always claim "nothing changed" while open issues remain unclassified`) still bypasses `inverted-guard-polarity`.
* Impact: Implementing `P01-T01` literally breaks existing passing unit tests (`test_fenced_code_blocks_and_negated_normative_prose_do_not_false_trigger` at line 368 and `cli-double-dash-flags-preserve-same-clause-negation` at line 500), risks false failures on `.github/agents/ama-backlog-delivery-coordinator.agent.md`, and leaves a two-mention same-clause bypass in `check_agent_instructions`.
* Smallest useful change: Update `FR-01` and `P01-T01` Context item 1 so the anchored prohibition suffix matches literal backticked spans (`` `[^`]+` ``), allows inflected reporting/pausing/copying verbs (including `-ing` forms and `(?:or|nor)` list items without `and`), permits optional trailing determiners (`(?:a|an|any|the)\s+`) and opening quote/backtick characters (`["'`]*`) immediately before `match_start`, and iterates all occurrences of `"nothing changed"` and `"unverified blocker"` in each `check_agent_instructions` clause via `re.finditer`; add a two-mention clause subtest in `P01-T02`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-01` in `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md` and `P01-T01`/`P01-T02` in `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md` specifying literal `` `[^`]+` `` handling, inflected governed verbs, trailing determiner/quote allowance before `\s*$`, and `re.finditer` occurrence scanning in `check_agent_instructions`.
* Decision route: direct_planner_correction
* User response required: no

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Concurrent launch detection, global wait gating, and PR blocker extraction leave false-pass loopholes on non-delivery `"started"` prose, `"PR #<n>"` citations, and URL `#fragment` digits

* Related IDs: `RV-002`, `FR-02`, `FR-03`, `P01`, `P01-T01`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md (`P01-T01` Context items 2-3 and `P01-T02`), .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md (`FR-02`, `FR-03`), and tools/check-coordinator-handoff.py (lines 52, 102-125, 306-338, and 783-858)
* Concern: Three gaps remain in `FR-02` and `FR-03` (`P01-T01` Context items 2-3):
  1. `CONCURRENT_LAUNCH_RE` matches bare `\b(?:launch(?:ed|ing)|start(?:ed|ing)|dispatch(?:ed|ing)|spawn(?:ed|ing))\b` without requiring a concrete delivery target (`rpi-<n>`, `#<n>`, `session(s)`, `worker(s)`, `lane(s)`, `wave(s)`, `issue(s)`), so non-launch prose such as `"Started scheduled check at 12:00Z; waiting on #1288"` or `"Waiting on #1288 since starting the check"` suppresses `unsupported-waiting-ready-work` even when `ready to start` issues remain unlaunched (including when `Active sessions: 0/8`). In addition, `GLOBAL_WAIT_OR_PAUSE_RE` omits `_is_claim_negated` gating (which would misclassify negated `"must never ... pause on an unverified blocker"` at `test_check_coordinator_handoff.py:368`) and misses `before we start`, `prior to starting`, `instead of starting`, and `until starting/launching` stall phrasings.
  2. `CITED_BLOCKER_REF_RE` (`tools/check-coordinator-handoff.py:121-124`) matches `(?:upstream\s+)?(?:issue\s+|blocker\s+)?#(\d+)` but omits `(?:(?:parent|upstream)\s+)?(?:pr\s+|pull\s+request\s+)?` (and optional `hosted\s+ci\s+(?:on|for)\s+`), allowing `"Waiting on PR #999"` to evade `cited_blocker_nums` entirely. Correspondingly, the `P01-T02` subtest `"Launched rpi-1204; waiting for hosted CI on PR #1642 while starting #1310 next."` must pair with `PR #1642` in `#1204`'s table row so prose and table blocker evidence agree.
  3. Extracting `ISSUE_REF_RE` directly from raw `row.non_issue_cells` without stripping URLs (after extracting `/(?:issues|pull)/(\d+)`) and Markdown link `(target)` strings admits non-issue HTML URL fragments (such as `https://example.com/gate#999`) or local numeric heading anchors (`[section](#42)`) into `verified_blocker_evidence_nums`.
* Impact: Handoffs with unlaunched `ready to start` capacity can bypass `unsupported-waiting-ready-work` via routine `"check started"` wording or bypass `unverified-blocker-reference` via `"Waiting on PR #999"` or URL `#fragment` digits, while negated `"pause on"` rules risk false positives.
* Smallest useful change: Revise `FR-02`, `FR-03`, `P01-T01` Context items 2-3, and `P01-T02` to: (a) require a concrete delivery object after `CONCURRENT_LAUNCH_RE` verbs, disallow past-tick/temporal prefixes (`before`, `until`, `without`, `instead of`, `prior to`, `since`, `after`, `previously`, `earlier`, or negation) in that clause, and require `declared_active_sessions` / `active_session_rows` consistency or an explicit launch of a `ready_rows` issue; (b) gate `GLOBAL_WAIT_OR_PAUSE_RE` with `not _is_claim_negated(line, m.start())` and cover `(?:before|prior\s+to|instead\s+of|until)\b[^.;!\n]{0,40}\b(?:continu\w*|start\w*|launch\w*|proceed\w*|dispatch\w*|spawn\w*)\b`; (c) extend `CITED_BLOCKER_REF_RE` to cover optional `(?:hosted\s+ci\s+(?:on|for)\s+)?(?:(?:parent|upstream)\s+)?(?:pr\s+|pull\s+request\s+|issue\s+|blocker\s+)?#(\d+)`, strip URLs and link `(target)` parts before running `ISSUE_REF_RE` on `non_issue_cells`, and add positive/negative subtests in `P01-T02` (with `PR #1642` in the active-launch row).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-02`, `FR-03`, `P01-T01` Context items 2-3, and `P01-T02` subtest specifications in `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md`.
* Decision route: direct_planner_correction
* User response required: no

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Markdown-linked `Issue` cell parsing does not validate mismatched `/issues/<other>` targets, unsafe schemes, or self-number `#<n>` local anchors

* Related IDs: `RV-003`, `FR-04`, `FR-05`, `P01`, `P01-T01`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md (`P01-T01` Context item 4 and `P01-T02`), .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md (`FR-04`, `FR-05`), and tools/check-coordinator-handoff.py (lines 317-328 and 349-386)
* Concern: `P01-T01` Context item 4 parses `MD_LINK_RE.search(raw_issue)` labels via `BARE_ISSUE_CELL_RE` and notes broken `#anchor` checks, but does not specify rejecting: (a) full-cell anchor mismatch when extra issues are packed into one cell (`[#1288](...) #1289`), (b) `javascript:`/`data:` link targets or GitHub `/issues/(\d+)` URLs whose number disagrees with the label (`[#1288](https://github.com/jmservera/ama/issues/9999)`), or (c) self-number fragments `[#1288](#1288)` in the `Issue` column when no `#1288` heading slug exists (note `_inspect_blocker_links` at line 322 skips `slug == str(issue_number)` rather than recording `broken_anchors`).
* Impact: Malformed or spoofed Markdown links in the `Issue` column can silently classify under the label number without surfacing `invalid-issue-id` or `broken-blocker-anchor`.
* Smallest useful change: Specify in `FR-04`, `P01-T01` Context item 4, and `P01-T02` that a linked `Issue` cell must match a single `#<num>` label across the stripped cell, reject `javascript:`/`data:` targets or mismatched `/issues/<other>` numbers as `invalid-issue-id` (`issue_num = None`), and record any `#anchor` target not in `valid_heading_slugs` (and not a `GITHUB_FRAGMENT_ANCHOR_RE`) in `broken_anchors`, with a negative subtest in `test_classification_table_rejects_invalid_states_duplicates_and_self_only_links` or `test_adversarial_rv001_handoff_bypasses_rejected`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-04` and `P01-T01`/`P01-T02` in `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md` covering single-issue linked cells, URL/scheme consistency, and non-heading `#anchor` rejection.
* Decision route: direct_planner_correction
* User response required: no

## Strengths and Residual Risk

* Single-phase decomposition (`P01-T01` implementation followed by `P01-T02` `self.subTest` regression coverage and Focused validation) is well-scoped, keeps `.github/agents/ama-backlog-delivery-coordinator.agent.md` and prior review/critique artifacts untouched, and respects the locked `11`-method test structure.
* Checking `classified_by_num` ahead of `verified_blocker_evidence_nums` (`FR-02`) and keeping `missing-classification-table`, `summary-before-classification-table`, and `unsupported-idle-unclassified` active on both global and lane-specific waits (`FR-03`) preserve fail-closed coordinator invariants.
* Accepted residual risk: Wiring `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` remains an explicit future follow-up because gate-tool edits require the full gate tier under `#1294`.

## Questions or Blocking Evidence Gaps

* none

## Limitations

* Assessment stayed strictly within the caller-supplied read boundary without inspecting `.github/agents/ama-backlog-delivery-coordinator.agent.md` directly or running `tools/rpi-checks.py`; existing agent contract invariants were cross-checked via `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, the research log, and the parent review log.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md` to incorporate `PC-001`, `PC-002`, and `PC-003`, mark planning metadata `Complete` / `ready`, and proceed to `rpi-implement` without a repeat critique pass.
* User response required: no
