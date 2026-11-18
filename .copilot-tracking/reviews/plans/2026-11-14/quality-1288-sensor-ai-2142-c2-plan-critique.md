<!-- markdownlint-disable-file -->
# RPI Plan Critique: PR #1745 Cycle-2 Rebase of Issue #1288 onto `origin/feat/demo-164-chat-grounding-provenance-0900`

## Metadata

* Task ID: quality-1288-sensor-ai-2142-c2
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements:
  1. Rebase `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`, PR #1745, Issue #1288) onto latest `origin/feat/demo-164-chat-grounding-provenance-0900` at `5f50fc238` (`5f50fc238f78e37e31baaed87f5d1eb81943cf14`).
  2. Resolve the sole merge conflict in `src/core/src/zava_forward/core/chat_case_answers.py` (`_sensor(r: Reply)`) preserving both Issue #1288's `conflict = r.fact("sensor.conflict")` early-return branch (emitting the conflict notice, `sensor.not_retained`, and `stage` without picking a value) plus `sensor.source` when `cite` is present, and upstream `#157`/`#164` (`2b1d40db0` on `5f50fc238`) behavior when `not cite` and `not conflict` (emitting `"No retained sensor reading is shown for this case. {detail}"` when `detail := r.fact("sensor.detail")` is present, then `return _damp(r)`).
  3. Validate under the focused tier using only `-p`-scoped `unittest discover` runs (never unscoped `unittest discover -s tests` without `-p`), plus `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` in `src/core` and `src/api`.
  4. Commit locally with `.copilot-tracking/` Cycle-2 artifacts and trailers (`Refs #1288`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`), using privacy-safe GitHub noreply identity, and do not push.
* Research and evidence considered:
  * .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md
  * .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md
  * .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md
  * .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md
  * .copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json
  * .copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-c2-state.json
  * .github/copilot-instructions.md
  * `HEAD` (`a2a39b2cf`) and `5f50fc238` versions of `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/src/zava_forward/core/chat_panel.py`, `src/core/src/zava_forward/core/sensor_view.py`, `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/pyproject.toml`, `src/api/pyproject.toml`, `src/api/src/zava_forward/api/web/chat.js`, `src/core/tests/test_chat_case_answers.py`, `src/core/tests/test_chat_panel.py`, `src/agents/tests/test_regulatory_chat_case_domain_grounding.py`, and `src/api/tests/test_quality_sensor_grounding.py`.
* Decisions, dependencies, and acceptance criteria considered:
  * Selected Option A (`git rebase 5f50fc238` rather than `git merge`) to keep PR #1745 history linear.
  * Ordering invariant inside `_sensor(r: Reply)` (`conflict = r.fact("sensor.conflict")` evaluated strictly before `detail = r.fact("sensor.detail")` under `if not cite:`) because `sensor_facts(view)` sets `sensor.detail` to `view.get("detail") or view.get("conflict_notice")`.
  * `P01` precedes `P02` because `DomainAnswerTests` in `src/core/tests/test_chat_case_answers.py` arrives from `5f50fc238` (`2b1d40db0`).
  * Worktree `PYTHONPATH` prefixing and strict `-p` test discovery discipline across `src/core`, `src/agents`, and `src/api`.
* Assessment boundary:
  * Evaluates rebase ancestry, hunk-level conflict resolution, citation/fact/skill-lens contracts across `chat_case_answers.py` and `chat_panel.py`, focused `-p` test and static validation coverage, RPI stage separation (`Implement` vs `Review`), and local commit/no-push hygiene from local repository state (`a2a39b2cf` and `5f50fc238`).
  * Cannot observe hosted GitHub Actions CI for PR #1745 because pushing to `origin` is prohibited by caller instruction.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / Research `C1`, `C5`, `C10` (Linear rebase of `a2a39b2cf` onto `5f50fc238`) | Covered | `P01-T01` configures privacy-safe local git identity before rebase, cleans tracked parent `quality-1288-sensor-ai-2142-state.json` prior to `git rebase 5f50fc238`, verifies `git merge-base` equals `5f50fc238f78e37e31baaed87f5d1eb81943cf14`, and verifies auto-merged `chat_panel.py` retains `SENSOR_RULE_PATHS`, `RULES_FIRST`, `RULES_SOURCE_ROOTS`, and `skill_sources` `common`. |
| Caller Req 2 / Research `C2`, `C3`, `C4`, `C8`, `C9` (`_sensor(r)` conflict resolution preserving both `#1288` and `#157`/`#164`) | Covered | `P01-T01` specifies exact `_sensor(r: Reply)` code checking `conflict = r.fact("sensor.conflict")` first under `if not cite:` (returning early without touching `r.fact("sensor.detail")`), delegating `not cite and not conflict` to `detail = r.fact("sensor.detail")` + `return _damp(r)`, and retaining `sensor.source` when `cite` is present. |
| Caller Req 3 / Research `C6`, `C7`, `C8` (Focused validation tier with `-p`-only `unittest discover` plus `mypy` and `ruff` in `src/core` and `src/api`) | Covered | `Test Ownership and Validation Lock` lists 12 explicit commands where every `unittest discover` call uses `-p '<file>.py'`, accounts for `test_chat_domain_questions.py` running `0` tests by pairing it with `test_chat_case_answers.py`, `test_chat_panel.py`, and `src/agents` `test_regulatory_chat_case_domain_grounding.py`, and runs `mypy`, `ruff check .`, and `ruff format --check .` in `src/core` and `src/api`. |
| Caller Req 4 (Local commit with Cycle-2 `.copilot-tracking/` artifacts, `Refs #1288`, Copilot trailer, and no push) | Partial | Privacy-safe git identity, trailers, and no-push constraints are covered, but `P02` in phase details conflates `Implement` completion with post-implementation `rpi-review` artifact creation and final commit (`PC-001`). |
| `P01` / `P01-T01` (Git identity, rebase onto `5f50fc238`, and `_sensor(r)` conflict resolution) | Covered | Exact conflict hunk, pre/post-rebase tracked parent state handling, and `chat_panel.py` auto-merge verification are complete and directly actionable. |
| `P02` / `P02-T01` (`DomainAnswerTests` seam test, `-p` verification, and local Cycle-2 commit) | Partial | `P02` lists `.copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-c2-review.md` and `post-implementation rpi-review recorded` inside `Implement` phase completion (`PC-001`), and `P02-T01`'s seam test checks `answer()` directly without exercising the merged `ChatPanel._rules_answer()` non-general skill-lens / `_source_kind` seam (`PC-002`). |

## Verdict

* Verdict: Revise
* Rationale: The rebase target (`5f50fc238`), `_sensor(r: Reply)` merge resolution (`sensor.conflict` preempting `sensor.detail` + `_damp(r)` while preserving `sensor.source`), and `-p`-scoped validation commands are technically sound and verified against both `a2a39b2cf` and `5f50fc238`. Two bounded planner-owned adjustments are needed before implementation: separating `P02` (`Implement`) completion evidence from the subsequent `Review` (`rpi-review`) log/closeout commit (`PC-001`), and covering the merged `ChatPanel._rules_answer()` non-general skill-lens and `_source_kind` contract inside the planned `DomainAnswerTests` seam test (`PC-002`). Neither requires user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: `P02` conflates `Implement`-phase completion with post-implementation `rpi-review` artifact generation

* Related IDs: Caller Req 4, `P02`, `P02-T01`
* Evidence: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md (`P02` `Likely Targets` and `Completion Evidence`), .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md (`User Decisions and Requirements`, `Acceptance Criteria`, `P02-T01`)
* Concern: `P02` in `.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md` lists `.copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-c2-review.md` under `Likely Targets` and requires `post-implementation rpi-review recorded` under `Completion Evidence`. However, `P01` and `P02` execute during `Implement` (`rpi-implement`), which reconciles phase completion markers (`[x]` / `completed`) and `quality-1288-sensor-ai-2142-c2-changes.md` before `Review` (`rpi-review`) runs.
* Impact: During `Implement`, a worker following `P02` literally could either fabricate `quality-1288-sensor-ai-2142-c2-review.md` prematurely inside `Implement` (violating independent `Review` stage separation) or block `P02` pre-review reconciliation waiting for a review artifact that does not exist yet; conversely, omitting an explicit post-`Review` tracking commit step would leave `c2-review.md` and final `state.json` uncommitted at session close.
* Smallest useful change: Scope `P02` and `P02-T01` `Likely Targets` and `Completion Evidence` strictly to `Implement` outputs (`src/core/tests/test_chat_case_answers.py`, passing commands 1 through 12, reconciled `c2-plan.md`, `c2-phase-details.md`, `c2-changes.md`, and `state.json` committed locally before `Review` with `Refs #1288` and Copilot trailer), and record in `## Handoff` / `Implementation Context Record` that post-implementation `rpi-review` writes `.copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-c2-review.md` and creates the final local tracking closeout commit (leaving `git status --short` empty without pushing).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02` / `P02-T01` in `.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md` and `P02-T01` / `## Handoff` in `.copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md` cleanly separating the `Implement` commit from the post-`rpi-review` closeout commit.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: `P02-T01` seam test omits the merged `ChatPanel._rules_answer()` non-general skill-lens and `_source_kind` interaction

* Related IDs: Caller Req 2, Research `C5`, `C6`, `C8`, `P02`, `P02-T01`
* Evidence: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md (`P02-T01`), src/core/src/zava_forward/core/chat_panel.py (`SENSOR_RULE_PATHS`, `skill_sources`, `RULES_SOURCE_ROOTS`, `ChatPanel._source_kind`, `ChatPanel._rules_answer` on `a2a39b2cf` and `5f50fc238`), src/api/tests/test_quality_sensor_grounding.py (`test_conflicting_readings_block_proactive_flag_and_route_chat_without_picking_one`)
* Concern: Rebase onto `5f50fc238` merges `a2a39b2cf`'s `SENSOR_RULE_PATHS` (`"sensor.source"`, `"sensor.conflict"`) with `2b1d40db0`'s `skill_sources` (`"sensor"` in `common`) and `RULES_SOURCE_ROOTS["sensor"] = ("hazards",)` in `chat_panel.py`. Existing `test_quality_sensor_grounding.py` exercises `sensor.conflict` only with `skill=None` (bypassing `skill_sources`), and `P02-T01` only calls `chat_case_answers.answer()` directly, leaving `ChatPanel._rules_answer()` under a non-general skill lens (for example `skill="resident-communications"`) and `_source_kind` (`ZF-1/sensor.conflict` and `ZF-1/sensor.source` as `"decision-rule"` vs `ZF-1/sensor.detail` and `ZF-1/sensor.0.state` as `"case-record"`) untested on the merged core seam.
* Impact: A regression in `chat_panel.py` auto-merge (`SENSOR_RULE_PATHS`, `skill_sources` `common`, or `RULES_SOURCE_ROOTS["sensor"]`) affecting non-general skill lenses on conflicting or fallback sensor replies would not be caught by the `src/core` unit seam test.
* Smallest useful change: Within the existing `Test Ownership and Validation Lock` (`src/core/tests/test_chat_case_answers.py` `DomainAnswerTests`, `1` test file modified, `0` removals, `<= 2` strict-typed `-> None` methods), extend `P02-T01` so `DomainAnswerTests` also exercises `ChatPanel._rules_answer(..., skill="resident-communications")` and `ChatPanel._source_kind(...)` across `sensor.conflict` (`decision-rule`, no `sensor.detail` citation), non-conflict `sensor.detail` + `_damp(r)` (`hazards` + `sensor.0.state` as `case-record` + `workflow/domain-boundary`), and clean `cite` (`sensor.source` as `decision-rule`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02-T01` specification in `.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md` and `Acceptance Criteria` in `.copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md` including `ChatPanel._rules_answer` non-general skill-lens and `_source_kind` assertions inside `DomainAnswerTests`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Exact hunk-level resolution in `P01-T01` correctly places `conflict = r.fact("sensor.conflict")` ahead of `detail = r.fact("sensor.detail")` under `if not cite:`, preventing `sensor_facts(view)`'s `put("sensor.detail", view.get("detail") or view.get("conflict_notice"))` fallback from polluting conflict citations with `{case_id}/sensor.detail` or emitting `"No retained sensor reading is shown for this case."`.
* Research and phase details proactively caught that `-p 'test_chat_domain_questions.py'` matches `0` files at `5f50fc238` and added explicit `-p` commands for the real domain and sensor suites (`test_chat_case_answers.py`, `test_chat_panel.py`, `src/agents` `test_regulatory_chat_case_domain_grounding.py`, `test_quality_sensors.py`, `test_sensor_staleness_ui_badge.py`, and `test_content_standard.py`) while keeping every test runner strictly `-p`-scoped.
* Pre-rebase restoration of tracked `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json` and local privacy-safe git identity setup via `gh api user` prevent dirty-worktree rebase refusal and committer-email drift.
* Residual risk (explicitly accepted by caller scope): Hosted GitHub Actions CI on PR #1745 cannot be observed locally because pushing to `origin` is prohibited (`Do NOT push`), and Cycle-1 follow-ups `RV-001` (`#employee-chat` 720px CSS target-size) and `RV-002` (live conflict state in `quality_sensors_browser_check.py`) remain out-of-scope follow-up items.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique is read-only and assessed against local git objects `a2a39b2cf` (`HEAD`) and `5f50fc238` (`origin/feat/demo-164-chat-grounding-provenance-0900`) without running unscoped test suites or mutating repository branches.
* Hosted CI checks on PR #1745 remain unobserved until the owner pushes the rebased branch.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001` and `PC-002` in `.copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md` and `.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md`, record dispositions in `## Critique Disposition`, mark planning status ready, and proceed directly to `Implement` without a second critique pass.
* User response required: no
