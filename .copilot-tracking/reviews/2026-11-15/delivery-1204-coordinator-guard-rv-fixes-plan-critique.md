<!-- markdownlint-disable-file -->
# RPI Plan Critique: Resolve Coordinator Handoff Guard Review Defects RV-001 through RV-003 (Issue #1204 Child Loop)

## Metadata

* Task ID: issue-1204-rv-fixes
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Child remediation loop `issue-1204-rv-fixes` (`delivery-1204-coordinator-guard-rv-fixes`) under parent task `issue-1204` (`delivery-1204-coordinator-guard`) to resolve routed findings `RV-001`, `RV-002`, and `RV-003` while preserving Issue #1204 `AC1` through `AC4`, keeping the Focused validation tier (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`), not running `tools/rpi-checks.py`, not modifying original parent review or critique logs, and not pushing or opening a PR.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan.md, .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, tools/check-coordinator-handoff.py, tools/test_check_coordinator_handoff.py, and .github/agents/ama-backlog-delivery-coordinator.agent.md.
* Decisions, dependencies, and acceptance criteria considered: Issue #1204 `AC1` through `AC4`, child criteria `AC-RV1` through `AC-RV4`, research decisions `D-1204-1` through `D-1204-4`, test-method cap (`<= 12` methods, `0` removals in tools/test_check_coordinator_handoff.py), and `P01-T01` -> `P01-T02` dependency ordering.
* Assessment boundary: Evaluates plan and phase-detail credibility, exact symbol/regex accuracy, bypass closure, and validation completeness strictly from the seven supplied read-boundary artifacts without mutating plan/source files or running `tools/rpi-checks.py`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Issue #1204 `AC1`-`AC4` (`D-1204-1`..`D-1204-4`) | Covered | Child scope preserves five-category classification, anti-idle/unverified-blocker rules, live refresh rules, offline stdlib validator, witness invariants (`C9`), and Focused validation boundary. |
| `RV-001` / `AC-RV1` (clause-scoped negation and `waiting for`) | Partial | `P01-T01` scopes negation on `IDLE_CLAIM_RE`, `WAITING_OR_PAUSE_RE`, and `UNVERIFIED_BLOCKER_RE`, but leaves unscoped `NEGATION_GUARD_RE.search(line)` on `STALE_CARRY_RE` (`tools/check-coordinator-handoff.py:497`), splits raw `--` inside CLI flags like `--state`, and allows cross-clause `Never` prefix carryover (`PC-002`). |
| `RV-001` / `AC-RV2` (split tables, absent cited blockers, local `#anchor` links) | Partial | Pre-summary `tbl.end_line > lineno` ordering is sound, but standalone `blocked on #999` skips `CITED_BLOCKER_REF_RE` (`tools/check-coordinator-handoff.py:812`) and digit-prefixed broken anchors like `[bad](#999-missing)` fall through to `ISSUE_REF_RE` (`tools/check-coordinator-handoff.py:230`) (`PC-002`). |
| `RV-002` / `AC-RV3` (polarity-aware agent check and live `--expect-*` / pagination rules) | Partial | `P01-T01` specifies `[^.\n]{0,260}` and `[^.\n]{0,220}` regexes that fail on 80-column hard-wrapped sentences in `.github/agents/ama-backlog-delivery-coordinator.agent.md:214-217,305-307,817-819` (`PC-001`), and `gh api --paginate` guidance omits REST `/issues` PR filtering and validator provenance support (`PC-003`). |
| `RV-003` / `AC-RV4` / `P01-T02` (adversarial unit tests, HVE refresh, Focused checks) | Partial | Keeps `<= 12` test methods with `0` removals, but misnames `test_agent_instruction_guard_rejects_missing_contracts`, omits post-HVE CLI/ASCII/link check commands in `P01-T02`, and does not state preserving prior SHA-256 lineage in the refreshed HVE record (`PC-004`). |
| `P01` / `P01-T01` | Partial | Targets exact files under remediation, subject to `PC-001`, `PC-002`, and `PC-003` specification corrections. |

## Verdict

* Verdict: Revise
* Rationale: Single-phase task decomposition and Focused-tier boundaries align cleanly with `RV-001` through `RV-003`, but `P01-T01` specifies single-line `[^.\n]` polarity regexes that false-fail on hard-wrapped sentences in `.github/agents/ama-backlog-delivery-coordinator.agent.md`, leaves concrete validator bypasses in `STALE_CARRY_RE`, `blocked on #N`, and digit-prefixed `#anchor` links in `tools/check-coordinator-handoff.py`, and omits REST `/issues` PR filtering and provenance compatibility for `gh api --paginate`. Direct planner revisions resolve all four findings without user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `P01-T01` single-line `[^.\n]` polarity regexes fail on hard-wrapped `.agent.md` sentences, miss single-section inversions, and misname `check_agent_instructions`

* Related IDs: `RV-002`, `AC-RV3`, `P01`, `P01-T01`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md (`P01-T01`), .github/agents/ama-backlog-delivery-coordinator.agent.md (`lines 214-217`, `305-307`, `817-819`), tools/check-coordinator-handoff.py (`check_agent_instructions` at `line 309`), and tools/test_check_coordinator_handoff.py (`lines 77`, `113`)
* Concern: `.github/agents/ama-backlog-delivery-coordinator.agent.md` wraps prose paragraphs across lines at ~80 columns, placing `\n` between `"nothing changed"` and `"unclassified"` in all three occurrences (`lines 214-216`, `305-306`, `817-818`) and between `never` and `"unverified blocker"` (`lines 214-215`), so `P01-T01`'s `[^.\n]{0,260}` and `[^.\n]{0,220}` regexes on `unfenced_body` fail on the valid live file. In addition, checking only that at least one negated sentence exists misses an adversarial single-section inversion added alongside an intact section, `check_agent_instructions` does not verify presence of the new `--expect-open-issues`/`--open-issues` and `gh api --paginate` guidance, and the plan/details refer to `check_agent_text` rather than the existing public function `check_agent_instructions`.
* Impact: Implementing `P01-T01` literally causes `python3 tools/check-coordinator-handoff.py` to fail on the repository's valid wrapped Markdown, risks breaking existing callers/tests if `check_agent_instructions` is renamed, and leaves single-section polarity inversions and `--expect-*`/`--paginate` contract omissions unguarded.
* Smallest useful change: Update the plan and `P01-T01` to keep `check_agent_instructions` as the public entry point (optionally delegating to `check_agent_text`), split `unfenced_body` into paragraph/bullet clauses on `\n\s*\n` and `[.;!?]` with internal whitespace collapsed (`\s+` -> `" "`) before checking prohibition polarity (`never|cannot|must\s+not|do\s+not|forbid\w*|prohibit\w*`), reject any unnegated affirmative clause pairing `"nothing changed"` with `"unclassified"` (outside `"permitted only when ... zero open issues unclassified"`) or `"unverified blocker"`, and require `--expect-open-issues`, `--open-issues`, and `gh api --paginate` in `check_agent_instructions`.
* Action owner: planning_parent
* Exact resolving evidence: Revised plan and `P01-T01`/`P01-T02` phase details naming `check_agent_instructions`, line-wrap-safe clause normalization, single-section affirmative-inversion rejection, and `--expect-*`/`gh api --paginate` token checks.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `P01-T01` leaves bypasses in `STALE_CARRY_RE` negation, CLI `--flag` splitting, standalone `blocked on #N` claims, and digit-prefixed `#anchor` links

* Related IDs: `RV-001`, `AC-RV1`, `AC-RV2`, `P01`, `P01-T01`, `P01-T02`
* Evidence: tools/check-coordinator-handoff.py (`lines 48`, `91-95`, `216-236`, `497`, `799-863`) and .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md (`P01-T01`)
* Concern: Four concrete edge cases remain open in `P01-T01`: (1) `STALE_CARRY_RE` (`line 497`) still uses whole-line `not NEGATION_GUARD_RE.search(line)` and `CITED_BLOCKER_REF_RE` (`line 848`) is not match-scoped, while splitting `line[:match_start]` on bare `"--"` cuts inside CLI flags like `--state` or `--limit` in negated rules, and the parenthetical cross-clause `Never` bullet prefix would re-enable `"Do not launch: nothing changed"` bypasses; (2) `CITED_BLOCKER_REF_RE` (`line 91`) matches `blocked\s+(?:on|by)`, yet `_validate_section` (`line 812`) skips the `CITED_BLOCKER_REF_RE` loop when neither `IDLE_CLAIM_RE` nor `WAITING_OR_PAUSE_RE` matched (so `"Summary: blocked on #999"` silently passes), and `ref_row.state in {"ready to start", "merged"}` misses invalid states such as `unknown`; (3) in `_has_non_bare_self_link` (`lines 216-236`, misnamed `_cell_has_valid_blocker_link` in `P01-T01`), rejecting a digit-prefixed broken local anchor such as `[bad](#999-nonexistent)` in `MD_LINK_RE` falls through to `ISSUE_REF_RE` (`#(\d+)\b`), which matches `#999` before `-` and returns `True`.
* Impact: Handoffs containing `"Counts copied from previous handoff; do not launch"`, `"Summary: blocked on #999"`, or `[blocker](#999-nonexistent)` still bypass `check_handoff_text`, while CLI `--flag` tokens in negated rule prose trigger false positives.
* Smallest useful change: Update `P01-T01` (using exact symbol names `_has_non_bare_self_link`, `_extract_classification_tables`, and `_validate_section`) so `_is_claim_negated` splits `line[:match_start]` only at `[;.!?:]` or whitespace-bounded `\s+--\s+` with no cross-clause prefix override and guards every match of `STALE_CARRY_RE`, `IDLE_CLAIM_RE`, `WAITING_OR_PAUSE_RE`, `UNVERIFIED_BLOCKER_RE`, and `CITED_BLOCKER_REF_RE`; run `CITED_BLOCKER_REF_RE` checks whenever an unnegated blocker citation appears (requiring `ref_row` to exist with state in `{"active session", "human-blocked", "dependency-blocked"}` and a valid link when blocked); strip `MD_LINK_RE` spans before bare `ISSUE_REF_RE` matching, tighten `ISSUE_REF_RE` with `(?![A-Za-z0-9_-])`, and emit a deterministic violation on any invalid local `#anchor` Markdown link in `_validate_section`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` and `P01-T02` details covering `STALE_CARRY_RE` negation, `\s+--\s+` splitting, standalone `blocked on #999`, and digit-prefixed `[bad](#999-nonexistent)` anchor rejection.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Saturated-limit `gh api --paginate` guidance omits REST `/issues` PR filtering and `_validate_section` provenance compatibility

* Related IDs: `RV-002`, `AC-RV3`, `D-1204-2`, `P01-T01`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md (`P01-T01`), .github/agents/ama-backlog-delivery-coordinator.agent.md (`lines 216`, `268`, `465`, `804`), and tools/check-coordinator-handoff.py (`lines 609-619`)
* Concern: GitHub's REST `repos/{owner}/{repo}/issues?state=open` endpoint includes pull requests unless `.pull_request == null` is filtered out (or GraphQL `issues(states: OPEN)` is queried), so unqualified `gh api --paginate` instructions inflate `Open issues` counts when `--limit 500` saturates. Additionally, `_validate_section` (`tools/check-coordinator-handoff.py:609-619`) requires literal `"gh issue list"` and `"gh pr list"` substrings, which fails `missing-live-provenance` if a saturated run records `gh api --paginate` instead, and `Stabilization checkpoints` (`line 465`) and step 5 (`line 804`) repeat `--limit 500`/`--limit 200` without pointing to the saturation rule.
* Impact: When a backlog hits `500` open issues or `200` open PRs, following the planned pagination rule can either double-count PRs as open issues or fail provenance checks in `tools/check-coordinator-handoff.py`.
* Smallest useful change: Specify PR-excluding pagination in `.github/agents/ama-backlog-delivery-coordinator.agent.md` (for example filtering `select(.pull_request == null)` on REST `/issues?state=open&per_page=100` alongside `/pulls?state=open&per_page=100`, cross-referenced from `Stabilization checkpoints` and step 5) and allow `gh api --paginate` issue/PR provenance alongside `gh issue list` and `gh pr list` in `_validate_section`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` specification recording PR-filtered `gh api --paginate` guidance, cross-section alignment in `.agent.md`, and `_validate_section` provenance acceptance.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: `P01-T02` misnames the existing agent-mutation test method, omits final CLI/Markdown/ASCII commands in task validation, and omits parent HVE SHA-256 lineage preservation

* Related IDs: `RV-003`, `AC-RV4`, `D-1204-4`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md (`P01-T02`), .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan.md (`AC-RV4`, `Test Ownership and Validation Lock`), tools/test_check_coordinator_handoff.py (`line 80`), and .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md (`line 25`)
* Concern: `P01-T02` refers to `test_agent_instruction_negative_mutations`, whereas the existing method in `tools/test_check_coordinator_handoff.py:80` is `test_agent_instruction_guard_rejects_missing_contracts`. `P01-T02` `Validation Expectations` also omits `python3 tools/check-coordinator-handoff.py` and explicit Markdown link, bullet-style, and plain-ASCII (`ord(c) <= 127`) checks required by `AC-RV4`, and refreshing `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` without retaining the superseded parent SHA-256 (`6bca3f75...`) weakens traceability from the untouched parent review log.
* Impact: Could cause an unintended extra test method against the `<= 12` cap, incomplete `P01-T02` verification, or obscured SHA-256 audit lineage from the immutable parent review artifact.
* Smallest useful change: Name `test_agent_instruction_guard_rejects_missing_contracts` in `P01-T02`, add `python3 tools/check-coordinator-handoff.py` plus explicit Markdown link/style and ASCII checks to `P01-T02` `Validation Expectations`, and note the prior parent `.agent.md` SHA-256 (`6bca3f75...`) alongside the refreshed exact SHA-256 in `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T02` details with exact method name, complete validation command list, and preserved SHA-256 lineage note.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Single-phase scoping (`P01-T01` -> `P01-T02`) cleanly isolates all three routed review defects (`RV-001`, `RV-002`, `RV-003`), honors the `<= 12` test-method lock with `self.subTest(...)`, keeps the original parent review and critique logs untouched, and preserves the Focused validation boundary without touching `tools/rpi-checks.py` or remotes.
* Accepted residual risk: Wiring `tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static checks remains explicitly deferred to a separate full-tier gate-tooling PR per `#1294` and caller instructions, and offline tests validate deterministic static/artifact contracts rather than live multi-tick `tmux` scheduling.

## Questions or Blocking Evidence Gaps

* None. All four findings are bounded technical corrections fully determined by the supplied plan, phase details, review log, research artifact, and target source files.

## Limitations

* Assessment was strictly bounded to the seven caller-specified read-boundary files; `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` was evaluated only via its SHA-256 and scope references in `.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md` and the child plan/details, and no source edits or test executions were performed during critique.

## Recommended Next Action

* Highest-impact finding: `PC-001` (paired with `PC-002` in `P01-T01`)
* Action owner: planning_parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md` to address `PC-001` through `PC-004` and finalize the child plan without another critique pass.
* User response required: no
