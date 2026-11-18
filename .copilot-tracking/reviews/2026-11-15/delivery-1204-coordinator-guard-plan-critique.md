<!-- markdownlint-disable-file -->
# RPI Plan Critique: Prevent Unsupported Idle Ticks and Stale Coordinator Handoffs (Issue #1204)

## Metadata

* Task ID: issue-1204
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Issue #1204 (`fix(delivery): prevent unsupported idle ticks and stale coordinator handoffs`), task slug `delivery-1204-coordinator-guard`, on branch `fix/delivery-1204-coordinator-guard` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641); Focused validation tier (`unittest`, `ruff check`, and `ruff format --isolated --line-length 100 --check` on `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`); explicit caller prohibitions against running `tools/rpi-checks.py`, pushing to remote, or opening a pull request.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md, .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md, .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md, .github/agents/ama-backlog-delivery-coordinator.agent.md, tools/test_rpi_phase_witness.py, .github/copilot-instructions.md
* Decisions, dependencies, and acceptance criteria considered: Caller AC1 through AC4 (mapped to plan `AC-01` through `AC-06`), converged research decisions `D-1204-1` through `D-1204-4`, coordinator gates in `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`#1296` correction-cycle budget, `2026-11-15` local-before-PR rule, step 6 HVE static/behavior gate, stacked-PR closure rules, PR drain hysteresis, and `rpi_phase_witness.py` strings asserted by `tools/test_rpi_phase_witness.py`), and AMA repository Markdown/commit rules in `.github/copilot-instructions.md`.
* Assessment boundary: Evaluates completeness, internal consistency, edge-case soundness, and regression safety of the candidate plan and phase details strictly from supplied repository artifacts without open-ended external or out-of-scope codebase research.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-01 / AC-01 (Anti-idle and unverified-blocker guard) | Partial | Covered across coordinator liveness, schedule, and step 5 sections (`C1`, `C2`, `C4`), except bare same-issue `#N` references on `human-blocked` rows can still bypass link verification (`PC-003`). |
| FR-02 / AC-02 (Five-category classification table before idle/waiting) | Partial | Canonical five categories are defined, but lifecycle mapping omits open PRs awaiting hosted CI/auto-merge with zero `tmux` sessions and still-open stacked children merged into a parent branch (`PC-001`), and step 5 `Cover, in this order:` still places change/waiting prose ahead of the table (`PC-002`). |
| FR-03 / AC-03 (Live-command count/session/SHA refresh at write time) | Partial | Connected handoff, checkpoint, step 5, and final-report surfaces are identified (`C3`, `C4`), but bare `gh issue list --state open` / `gh pr list --state open` truncate at 30 items and `.agent.md` lacks the canonical metadata/table field schema expected by the validator (`PC-002`). |
| FR-04 / AC-04 (`tools/check-coordinator-handoff.py` validator) | Partial | Strong offline stdlib architecture (`C5`, `C7`, `C8`), but active-session row equality breaks multi-role `rpi-{number}-{role}` sessions, waiting-summary capacity checks omit 16-20 active PR drains and lower owner caps (`PC-001`), stacked `target SHA` vs `origin/main` and multi-entry checkpoints risk false SHA/count conflicts (`PC-002`), and `human-blocked` lacks self-only `#N` rejection (`PC-003`). |
| FR-05 / AC-05 (`tools/test_check_coordinator_handoff.py` and Ruff checks) | Partial | Caller-mandated `unittest` and Ruff commands match `AC-05`, but 25+ enumerated test scenarios in `P03-T01` need explicit `subTest` grouping to honor the `<= 16` test-method lock and include the new edge cases (`PC-003`, `PC-004`). |
| NFR-01 (Offline Python 3.12 stdlib + Ruff conformance) | Covered | Zero network calls, `sys.modules` registration before `exec_module`, Python 3.12 typing, and 100-char isolated Ruff checks are clearly specified (`C5`, `C7`). |
| NFR-02 / AC-06 (AMA style, `rpi_phase_witness.py` invariants, HVE evidence, local commit) | Partial | Witness invariants (`C9`), ASCII/Markdown rules (`C6`), and local-only commit rules are covered, but `P03` treats canonical HVE static/behavior qualification for `.agent.md` as conditional (`if needed`) and omits its mandatory step 6 fields from `P03-T01` (`PC-004`). |
| P01 / P01-T01 | Partial | Target hunks in `.github/agents/ama-backlog-delivery-coordinator.agent.md` are well-scoped; revise per `PC-001` and `PC-002`. |
| P02 / P02-T01 | Partial | Module/CLI boundary is sound; revise state/count/SHA/link invariants per `PC-001`, `PC-002`, and `PC-003`. |
| P03 / P03-T01 | Partial | Validation commands match caller constraints (excluding `tools/rpi-checks.py` and push/PR); revise HVE evidence deliverables and `subTest` method-budget alignment per `PC-001` through `PC-004`. |

## Verdict

* Verdict: Revise
* Rationale: The three-phase architecture, target files, offline standard-library design, and focused validation commands align well with Issue #1204 and caller constraints, but four substantive specification gaps (`PC-001` through `PC-004`) between `.github/agents/ama-backlog-delivery-coordinator.agent.md` and `tools/check-coordinator-handoff.py` would cause false rejections on legitimate coordinator ticks (open PRs running hosted CI with zero `tmux` sessions, stacked children merged into parent PRs, multi-role `rpi-{number}-{role}` sessions, step 5 summary ordering, and stacked `target SHA` vs `origin/main` SHAs), leave a self-`#N` link bypass on `human-blocked` rows, or under-specify mandatory step 6 HVE instruction-change evidence. All four findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Five-category lifecycle mapping and session/drain invariants reject valid hosted-CI, stacked-child, multi-worker, and PR-drain coordinator states

* Related IDs: `FR-02`, `FR-04`, `AC-02`, `AC-04`, `C1`, `C4`, `P01-T01`, `P02-T01`, `P03-T01`
* Evidence: .github/agents/ama-backlog-delivery-coordinator.agent.md (lines 165-206, 387-405, 799-801, 935-937); .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md (lines 95-100, 170-198, 268)
* Concern: Three real coordinator states conflict across `P01-T01` and `P02-T01`: (1) When worker `tmux` sessions have finished and open PRs are awaiting hosted GitHub Actions CI or queued auto-merge (`Active sessions: 0`, issues still open in `gh issue list --state open`), those open issues have no valid category under the draft rules because `merged` is rejected for open issues, `active session` requires a live `tmux` session and fails against `Active sessions: 0`, `human-blocked` is false, `ready to start` is rejected on waiting/idle summaries below cap, and `P01-T01` defines `dependency-blocked` only for blocking active/human-blocked issues or PRs without naming in-flight hosted PR checks/auto-merge. (2) Under `.agent.md` lines 387-405, stacked child issues merged into a parent topic branch (and `status:partially-delivered` issues) remain open on GitHub until `main` merge/completion; `P01-T01` does not restrict `merged` to issues closed on `main`, so classifying an open parent-merged stacked child as `merged` triggers `P02-T01` open-issue count/list failures. (3) `P02-T01` forbids duplicate issue rows while flagging `Active sessions` count vs `active session` row count, breaking multi-role sessions sharing one issue (`rpi-{number}-{role}`, `.agent.md` lines 166-168 and 799-801), and hardcodes `< 8` / `<= 20` on `waiting` summaries without honoring explicit lower owner session caps (`.agent.md` line 176) or active PR drains in the `16..20` hysteresis band before clearing at `<= 15` (`.agent.md` lines 194-198).
* Impact: Legitimate coordinator check summaries during hosted CI/auto-merge waits, stacked-branch delivery (including PR #1641 stacks), multi-role single-issue runs, or `16..20` PR drains either lack a legal five-category classification or fail `tools/check-coordinator-handoff.py`.
* Smallest useful change: In `P01-T01`, define exhaustive five-category membership relative to GitHub issue state: `merged` only for issues whose required delivery merged to `main` and closed the issue; `active session` for open issues with at least one live `tmux` `rpi-*` session; `human-blocked` with concrete gate/comment/ADR link; `dependency-blocked` with concrete link for upstream active/human-blocked issues/PRs, stacked child issues merged into a parent topic awaiting parent PR merge to `main`, or open PRs awaiting hosted CI/auto-merge when no `tmux` session is active; and `ready to start` for actionable work eligible now (including `status:partially-delivered` open issues with actionable scope, unpublished frozen candidates awaiting coordinator gate, or failing fixable PR checks). In `P02-T01` and `P03-T01`, validate `(declared_active_sessions == 0 and active_session_rows > 0)` and `active_session_rows > declared_active_sessions` (plus exact match against an explicit `tmux` session list when rendered, and rejecting `declared_active_sessions > 0` with zero `active session` rows unless non-issue sessions are explicitly listed) rather than strict `declared_active_sessions == active_session_rows`, and honor declared session caps (`M/N`) and declared active PR drain (`open_prs > 15` with active drain recorded) when checking `waiting` summaries alongside `ready to start` rows.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01`, `P02-T01`, and `P03-T01` specifications in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md (and corresponding `FR-02`/`FR-04` summary in .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md) covering hosted-CI/stacked-child `dependency-blocked` mapping, `merged` closed-on-main boundary, multi-role `active_session_rows <= declared_active_sessions` invariant, and drain/cap-aware waiting checks.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Producer-consumer mismatch on step 5 summary ordering, canonical handoff/checkpoint field schema, stacked SHA keys, and 30-row `gh` CLI truncation

* Related IDs: `FR-02`, `FR-03`, `FR-04`, `AC-02`, `AC-03`, `AC-04`, `C3`, `C4`, `C5`, `P01-T01`, `P02-T01`
* Evidence: .github/agents/ama-backlog-delivery-coordinator.agent.md (lines 358, 494-505, 832-851); .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md (lines 95-115, 176-205)
* Concern: Three contract gaps separate `.agent.md` instructions (`P01-T01`) from `tools/check-coordinator-handoff.py` (`P02-T01`): (1) Step 5 in `.agent.md` lines 833-838 instructs the coordinator to `Cover, in this order: what changed since the last check ...; what is running now ...; each open PR ...; what is waiting and why ...`, which puts `"Nothing changed..."` / `"No changes since last..."` and `"waiting on..."` ahead of any table unless `Cover, in this order:` itself is reordered to place the refreshed live-metrics header and five-category classification table first. (2) `P02-T01` parses `Open issues`, `Open PRs`, `Active sessions`, live-command provenance, `observed_at` vs `written_at` UTC timestamps, and conflicting `HEAD` / `base SHA` / `origin/main` / `target SHA` declarations, but `P01-T01` provides no canonical Markdown metadata/table schema in `.agent.md`; additionally, grouping `origin/main` SHA with stacked parent `target SHA` (or top-level `HEAD SHA` with per-PR `HEAD` cells, or scanning across multiple dated entries in append-only checkpoint files such as `docs/architecture/cutover-evidence-pack.md`) causes false conflict errors on stacked branches and multi-entry checkpoint records. (3) `P01-T01` prescribes bare `gh issue list --state open` and `gh pr list --state open`, both of which default to `--limit 30` in `gh` CLI and silently undercount larger backlogs.
* Impact: A coordinator following `.agent.md` literally can emit step 5 summaries, stacked-branch handoffs, or checkpoint entries that fail `check-coordinator-handoff.py --handoff <file>` or record 30-capped counts.
* Smallest useful change: In `P01-T01`, reorder step 5 `Cover, in this order:` so every check/handoff leads with (1) the live-refreshed counts/sessions/SHAs snapshot block using explicit high limits (for example `gh issue list --state open --limit 500`, `gh pr list --state open --limit 200`, `tmux list-sessions`, `git rev-parse`) and (2) the five-category issue-state classification table (`| Issue | State | Blocker or evidence link | Next action |`) before `"what changed"`, `"what is waiting"`, or any `"nothing changed"` / idle summary, illustrated by a compact fenced `markdown` template defining canonical field names (`Observed UTC`, `Written UTC`, `Open issues`, `Open PRs`, `Active sessions`, `HEAD SHA`, `Origin/main SHA`, `Target/base SHA`). In `P02-T01`, keep `gh issue list` / `gh pr list` prefix provenance matching (accepting `--limit` / `--json` flags), compare SHA consistency within each distinct normalized top-level metadata key (`head sha` vs `origin/main sha` vs `base/target sha`) rather than across stacked base vs `origin/main` or per-PR table cells, and scope snapshot consistency per dated checkpoint/handoff section when multiple dated sections appear in one file.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` sections in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md specifying step 5 lead-with-table ordering, `--limit` flags on `gh issue list` / `gh pr list`, the canonical fenced Markdown handoff/status block + table schema, distinct `origin/main` vs `target/base` top-level SHA keys, and per-section snapshot scoping.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Bare same-issue `#N` reference in non-issue columns still bypasses link verification on `human-blocked` rows

* Related IDs: `FR-01`, `FR-02`, `FR-04`, `AC-01`, `AC-02`, `AC-04`, `C1`, `C5`, `P02-T01`, `P03-T01`
* Evidence: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md (lines 32-34, 71-84); .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md (lines 172-175, 260)
* Concern: `P02-T01` accepts any `#<num>` in a non-issue column as a concrete blocker link and restricts same-issue `#<self>` rejection to `dependency-blocked` rows only. On a `human-blocked` row for `#1288`, a bare unlinked self-reference in another cell (for example `| #1288 | human-blocked | Blocked on owner in #1288 |`) passes without any URL, `#issuecomment-` anchor, Markdown document link, or distinct blocking issue/PR.
* Impact: Permits unverified self-referential `human-blocked` claims to pass validation without a concrete decision/comment/ADR/issue link, undermining `AC-01`, `AC-02`, and `AC-04`.
* Smallest useful change: In `P02-T01`, reject bare same-issue `#<self>` tokens on `human-blocked` rows as well unless accompanied by an `https?://` URL (including `#<self>` issue/comment URLs such as `https://.../issues/1288#issuecomment-...`), a Markdown `[label](target)` link, an explicit comment anchor (`#<self>#issuecomment-...`), or a distinct `#<other>` (`other != self`) issue/PR reference; add this negative case to `P03-T01`.
* Action owner: planning parent
* Exact resolving evidence: Updated `P02-T01` link-validation bullet and `P03-T01` negative test specification in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md (and `What You May Not Know` in .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md) enforcing non-bare-self links on both `human-blocked` and `dependency-blocked` rows.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Coordinator step 6 HVE static/behavior qualification fields and `<= 16` `subTest` method-lock discipline are left optional or implicit in `P03`

* Related IDs: `FR-05`, `NFR-02`, `AC-05`, `AC-06`, `C6`, `C7`, `P03`, `P03-T01`
* Evidence: .github/agents/ama-backlog-delivery-coordinator.agent.md (lines 757-760, 882-890); .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md (lines 59, 127); .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md (lines 222-226, 231, 253-270)
* Concern: Modifying `.github/agents/ama-backlog-delivery-coordinator.agent.md` is a behavior-bearing agent instruction change, for which `.agent.md` lines 757-760 and 882-890 require canonical HVE static and behavior evidence carrying five explicit attributes (`exact source identity`, `execution status`, `verdict`, `fidelity`, and `executor or profile limits`) before publication. `P03` currently marks `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` as `(if needed alongside plan critique)` and omits those five mandatory attributes from `P03-T01`. Separately, `P03-T01` enumerates ~25 distinct positive and negative test scenarios while `Test Ownership and Validation Lock` caps `tools/test_check_coordinator_handoff.py` at `At most 16 focused test methods`, without stating that scenarios are grouped via `self.subTest(...)` per contract family.
* Impact: Treating the HVE assessment artifact or its five required metadata fields as optional risks blocking step 6 pre-publication coordinator review and consuming an avoidable correction cycle; implementing each listed scenario as a separate `test_*` method would violate the plan's own 16-method validation lock.
* Smallest useful change: In `P03` and `P03-T01`, make `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` a required deliverable recording exact post-edit `.github/agents/ama-backlog-delivery-coordinator.agent.md` SHA-256 source identity, execution status, verdict, fidelity (static + contained trace/validator simulation, explicitly qualified as non-native-host runtime), and executor/profile limits, and specify `self.subTest(...)` grouping by contract family in `tools/test_check_coordinator_handoff.py` so all positive/negative cases execute within `<= 16` `test_*` methods.
* Action owner: planning parent
* Exact resolving evidence: Updated `P03` and `P03-T01` sections in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md requiring the five HVE static/behavior attributes in `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` and `subTest` contract grouping within `<= 16` test methods.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strengths: The plan cleanly connects all five relevant sections of `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`Liveness and stop decision`, `Recurring schedules`, `Stabilization checkpoints`, step 5 check summaries, and `Final report`), preserves `#1296`, `2026-11-15` CI-economy, and `tools/test_rpi_phase_witness.py` invariants (`C9`), keeps `tools/check-coordinator-handoff.py` 100% offline in Python 3.12 stdlib (`C5`, `C7`), and strictly honors the caller's Focused validation tier and local-only commit constraints.
* Residual risk: Because `tools/check-coordinator-handoff.py` is outside `.github/workflows/src-ci.yml` path triggers (`C8`) and `tools/rpi-checks.py` is excluded by caller direction, enforcement relies on focused local test execution and coordinator invocation until the deferred backlog follow-up wires it into static gate checks.

## Questions or Blocking Evidence Gaps

* None. All four findings (`PC-001` through `PC-004`) are fully resolved by existing repository rules in `.github/agents/ama-backlog-delivery-coordinator.agent.md` and caller acceptance criteria without user input.

## Limitations

* Assessment is bounded to static plan/detail consistency against supplied repository files and does not execute live multi-tick `tmux` or GitHub API coordinator schedules.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, `PC-003`, and `PC-004` across `.copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md` and `.copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md`, record critique disposition in the plan, and finalize the plan for `rpi-implement` without a second critique pass.
* User response required: No
