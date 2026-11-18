---
description: "Primary evidence artifact for PR #1745 Cycle-2 rebase of Issue #1288 onto origin/feat/demo-164-chat-grounding-provenance-0900"
---
<!-- markdownlint-disable-file -->

# Task Research: quality-1288-sensor-ai-2142-c2

| Field              | Value                                                                         |
|--------------------|-------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                    |
| Researcher / agent | rpi-research (RPI Agent)                                                      |
| Status             | Complete                                                                      |
| Artifact path      | .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md |

## Research Brief

* What to research: Exact commit divergence, rebase conflict surface, fact/citation contracts, and test interactions between `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`, Issue #1288, PR #1745) and `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`, specifically `00442e5e9` for Issue #157 / PR #1645 and adjacent chat/sensor commits).
* Why it matters: PR #1745 conflicts in `src/core/src/zava_forward/core/chat_case_answers.py` (`_sensor(r: Reply)`), and resolving it carelessly could regress either Issue #1288's retained sensor conflict refusal/provenance rules or Issue #157's `_damp(r)` fallback and `sensor.detail` notice when `not cite` and `not conflict`.
* Audience or intended use: Plan, critique, implementation (rebase + conflict resolution), and review phases in this confirmed automatic RPI loop.
* Scope: `feat/quality-1288-sensor-ai-2142` vs `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`), `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/src/zava_forward/core/chat_panel.py`, `src/core/src/zava_forward/core/sensor_view.py`, `src/core/src/zava_forward/core/assistants.py`, `src/core/tests/test_chat_domain_questions.py`, `src/core/tests/test_sensor_view_conflicts.py`, `src/api/tests/test_quality_sensor_grounding.py`, and `src/api/tests/test_quality_sensors_correlation.py`.
* Non-goals: Pushing to remote, running unscoped `unittest discover -s tests` without `-p`, modifying unrelated features on `origin/feat/demo-164-chat-grounding-provenance-0900`, or changing Azure/SQL/deployment files.
* Criteria: Identify every conflicting or semantically interacting hunk across the rebase onto `5f50fc238`, verify exact fact/citation invariants for `not cite` with `conflict` vs without `conflict` (withheld, unavailable, empty, stale), and verify focused test expectations across both `#157` and `#1288`.
* Requested outputs: Convergence recommendation for rebasing `feat/quality-1288-sensor-ai-2142` onto `5f50fc238` and resolving `_sensor(r: Reply)` (plus any subtle semantic interactions).
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                               |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How do `a2a39b2cf` (#1288) and `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`, including `00442e5e9` #157) diverge, and what exact `_sensor(r)` / `sensor_facts()` / citation behavior satisfies both #1288 and #157? |
| Codebase scope                       | `src/core`, `src/api`, `.copilot-tracking`, git history up to `5f50fc238` and `a2a39b2cf`                                           |
| External scope                       | none                                                                                                                                |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/tests/test_chat_domain_questions.py`, `src/core/tests/test_sensor_view_conflicts.py`, `src/api/tests/test_quality_sensor_grounding.py`, `src/api/tests/test_quality_sensors_correlation.py` |
| Initial external candidate areas     | none                                                                                                                                |
| Research posture                     | focused                                                                                                                             |
| Posture provenance                   | default (bounded internal rebase/conflict-resolution task with named commits, files, and focused `-p` test selectors)               |
| Explicit limits / deadline           | Do NOT push; NEVER run unscoped `unittest discover -s tests` without `-p`; commit locally with `Refs #1288` and Copilot trailer     |
| Posture-specific completion basis    | focused scope and materiality                                                                                                       |
| Edits allowed during research?       | no, research-only                                                                                                                   |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Read-only git/file inspection during Research; do not start rebase or mutate source files before Implement                          |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                              | Scoped authority or output contract                   | Selected / skipped reason                                                       |
|---------------------|-----------------------------------|---------------------------------------------------|-------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and tracking    | Focused validation tier, git author/email, PR/commit rules | Selected: governs local git identity, focused validation tier, and tracking rules |
| Skill               | `git-merge`                       | Git rebase/conflict resolution topic              | Rebase/conflict hygiene                               | Skipped in Research (read-only phase); standard git merge-tree/diff inspection suffices |
| Skill               | `web-design-guidelines`           | Applies if web files change during rebase         | Web Interface Guidelines review                       | Deferred to Implement/Review if rebase carries `src/api/.../web/*.js` commits   |
| Research specialist | `hve-core-all:rpi-researcher`     | General RPI research subagent                     | Delegated lane artifact                               | Skipped: single tightly coupled rebase conflict trace fits inline focused waves |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                 |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI execution with complete commit SHAs, branch target, conflict details, and `-p` commands | N/A (non-interactive) | Proceed in focused convergence mode to inspect `a2a39b2cf` vs `5f50fc238`       |
| Direction change | None at intake                                                                                        | N/A                  | Keep active brief                                                               |
| Convergence      | No material ambiguity remains after Cycle 1 three-wave inspection                     | N/A (non-interactive) | Select Option A (`git rebase 5f50fc238` resolving `_sensor(r)` to check `sensor.conflict` before `sensor.detail` + `_damp(r)`) and advance to Plan |

## Scope and Success Criteria

* Scope: Read-only comparison of `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`) and `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`), focusing on `chat_case_answers.py`, `chat_panel.py`, `sensor_view.py`, `assistants.py`, `src/api` files touched by `a2a39b2cf`, and both `#157` and `#1288` test suites.
* Assumptions: `chat_case_answers.py` is claimed to be the sole merge-conflict file, which must be verified via `git merge-tree` rather than trusted blindly; semantic interactions across other commits between merge-base and `5f50fc238` (e.g. `#164`, `#151`, `#188`, `#186`, `#189`) must also be verified.
* Success criteria:
  * Every research question is answered with concrete `path:line` and commit evidence.
  * Findings, decisions, and readiness claims cite `C#` Evidence Log IDs.
  * Alternatives (rebase vs merge vs cherry-pick; branch ordering inside `_sensor(r)` and `sensor_facts()`) are compared with trade-offs and one convergence recommendation is selected.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Run full RPI loop (`research`, `plan`, `rpi-plan-critique`, `implement`, `review`) to rebase `feat/quality-1288-sensor-ai-2142` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`), preserving both `#1288` `sensor.conflict` handling and `#157` `_damp(r)` fallback when `not cite` and `not conflict`, verify with targeted `-p` tests + `mypy` + `ruff`, and commit locally without pushing.
* Inferred research questions: What commits sit between the merge-base and `5f50fc238` vs `a2a39b2cf`? Does `git merge-tree` show any other file conflicts or silent semantic clashes (e.g. `sensor.detail` populated from `conflict_notice`, `provenance` rules from `#164` commit `2b1d40db0`, or withdrawal rules from `#151` commit `5feef51d8`)?
* Caller constraints and non-goals: Research-only in this phase; never run unscoped `unittest discover -s tests` without `-p`; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                 | Source / checkpoint   | Effect on active brief, evidence, or revalidation                 |
|----------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-------------------------------------------------------------------|
| narrow                                                   | Target base `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`)       | Caller prompt / Intake| Scopes branch ancestry and conflict analysis to `5f50fc238`       |
| exclude                                                  | Never run unscoped `unittest discover -s tests` without `-p`; do NOT push to remote   | Caller prompt / Intake| Constrains test verification commands and final git state         |

## Research Questions

|  # | Sub-question                                                                                                                                    | Type            | Priority | Status   |
|---:|-------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What is the exact commit ancestry and `git merge-tree` conflict footprint between `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`) and `5f50fc238`? | straightforward | H        | answered |
| Q2 | What exact changes did `00442e5e9` (`#157`, PR #1645) and other upstream commits (`2b1d40db0` `#164`, `5feef51d8` `#151`, etc.) make to `chat_case_answers.py`, `chat_panel.py`, `sensor_view.py`, `assistants.py`, and tests? | depth           | H        | answered |
| Q3 | How do `sensor_facts()`, `_sensor(r)`, `_damp(r)`, `SENSOR_RULE_PATHS`, and citation/provenance checks interact across all `not cite` cases (`conflict`, `withheld`, `unavailable`, `none`, and clean `cite`)? | depth           | H        | answered |
| Q4 | Do any subtle regressions arise between `#1288` (`sensor.detail` fallback to `conflict_notice`, `RULE_PARTS` in `chat.js`, `#164` provenance assertions, or `#157` `test_chat_domain_questions.py`) when combined? | breadth         | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md`, `.copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md`, `.copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-review.md`, `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json`.
* Reused (verified) findings: Cycle-1 (`a2a39b2cf`) implemented `sensor.conflict` and `sensor.source` facts in `chat_case_answers.py`, `SENSOR_RULE_PATHS` in `chat_panel.py`, `RULE_PARTS` in `chat.js`, conflict blocking in `sensor_view.py` and `assistants.py`, and `"conflict"` badges in `sensor_badges.py` / `ops.js` / `assistants.js`.
* Superseded / stale: Cycle-1 was based on `f5f76b6cc`; `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by 11 commits to `5f50fc238` (including `2b1d40db0` PR `#1734` which merged the case-domain `_damp(r)` / `DOMAIN_BOUNDARY` / `RULES_FIRST` changes into `chat_case_answers.py` and `chat_panel.py`).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`); exclude unscoped test discovery without `-p` and remote push.
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: No remote push; all test commands must use explicit `-p` patterns.

#### Wave 1: Wider

* Plan and independent lanes: Inspect merge-base, commit divergence on both sides, `git merge-tree --write-tree --messages 5f50fc238 a2a39b2cf`, and changed-file stats across `a2a39b2cf` and `f5f76b6cc..5f50fc238` inline (single coupled git/module seam).
* Worker evidence relationships or inline fallback: Inline focused wave mapped `Q1` -> `C1`, `C2` (`f5f76b6cc` merge-base; 1 commit `a2a39b2cf` on HEAD; 11 commits on `5f50fc238`; sole content conflict in `src/core/src/zava_forward/core/chat_case_answers.py`; clean auto-merge in `chat_panel.py`; zero overlap in `sensor_view.py`, `assistants.py`, `sensor_badges.py`, or `src/api/.../web/*.js`).
* Reflection: `chat_case_answers.py` is verified as the sole textual merge conflict, and `chat_panel.py` auto-merges cleanly; Wave 2 needs exact hunk-level inspection of `chat_case_answers.py`, `chat_panel.py`, and upstream domain-grounding tests.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: `Q2` and `Q3` — exact upstream diff on `chat_case_answers.py` and `chat_panel.py` (`2b1d40db0`), how `_damp(r)` and `sensor_facts()` work, and where the upstream domain-question tests live.
* Plan and independent lanes: Read `chat_case_answers.py`, `chat_panel.py`, `chat_isolation.py`, `chat_privacy.py`, `sensor_view.py`, and upstream test files at `5f50fc238` and `a2a39b2cf`.
* Worker evidence relationships or inline fallback: Inline investigation mapped `Q2` and `Q3` -> `C2`–`C8`:
  * The `_damp(r)` / `sensor.detail` change described in the prompt was squashed into `origin/feat/demo-164-chat-grounding-provenance-0900` via `2b1d40db0` (`PR #1734`, `Refs #164, Refs #1530`), verified against `git ls-remote origin refs/heads/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238f78e37e31baaed87f5d1eb81943cf14`).
  * `src/core/tests/test_chat_domain_questions.py` does not exist at `5f50fc238`; the actual domain-question tests in `2b1d40db0` live in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`), `src/core/tests/test_chat_panel.py` (`HybridAttributionTests`), and `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` (`CaseDomainGroundingTests`) (`C6`, `C7`).
  * In `chat_case_answers.py`, `a2a39b2cf` adds `sensor.conflict` and `sensor.source` to `sensor_facts()`, adds the `if conflict:` early-return branch when `not cite` in `_sensor(r)`, and adds `Reading source: {r.facts['sensor.source']}` when `cite` is present (`C3`, `C4`). Meanwhile `2b1d40db0` replaces the non-conflict `not cite` fallback in `_sensor(r)` with `detail = r.fact("sensor.detail"); if detail: r.say(f"No retained sensor reading is shown for this case. {detail}"); return _damp(r)` (`C2`).
* Reflection: Both hunks in `_sensor(r)` compose cleanly, provided `conflict = r.fact("sensor.conflict")` runs BEFORE `detail = r.fact("sensor.detail")`. Wave 3 must challenge subtle interactions (`sensor.detail` dual assignment, `_indexes(r.facts, "sensor")`, `skill_sources` `"sensor"` in `common`, `redact()`, and `Ran 0 tests` trap on `-p 'test_chat_domain_questions.py'`).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether `put("sensor.detail", view.get("detail") or view.get("conflict_notice"))`, `_indexes(r.facts, "sensor")`, `skill_sources(..., common=(..., "sensor"))`, `chat_privacy.redact()`, or `ai_registry.is_registered()` cause silent citation, privacy, or test regressions after rebasing onto `5f50fc238`.
* Plan and independent lanes: Inspect `sensor_facts()`, `_indexes()`, `ChatIsolation._sensor_facts()`, `ChatPanel._source_kind()`, `chat_privacy.PATTERNS`, `ai.py` / `ai_tasks.py`, and all test assertions in `test_quality_sensor_grounding.py`, `test_chat_case_answers.py`, and `test_regulatory_chat_case_domain_grounding.py`.
* Worker evidence relationships or inline fallback: Inline contrarian audit mapped `Q3` and `Q4` -> `C3`–`C10`:
  * **Trap 1 (Order of `r.fact("sensor.conflict")` vs `r.fact("sensor.detail")`):** Because `sensor_facts()` sets `put("sensor.detail", view.get("detail") or view.get("conflict_notice"))` (`C3`), `sensor.detail` is ALSO truthy during a sensor conflict! If `detail = r.fact("sensor.detail")` were evaluated before `if conflict:`, `Reply.fact()` would record `"ZF-1/sensor.detail"` (`case-record`) in `r.cites` AND/OR emit `"No retained sensor reading is shown for this case."`, breaking `test_conflicting_readings_block_proactive_flag_and_route_chat_without_picking_one` (`assertNotIn("No retained sensor reading is shown", ...)` and `decision-rule` citation expectations, `C8`). Evaluating `conflict = r.fact("sensor.conflict")` first and returning immediately avoids touching `sensor.detail` on conflict, while preserving `sensor.detail` fallback if any external caller inspects `facts["sensor.detail"]`.
  * **Trap 2 (`_indexes(r.facts, "sensor")` collision check):** `_indexes` matches `rf"{re.escape(prefix)}\.(\d+)\."` (`C2`), which matches `sensor.0.task_key` / `sensor.0.state` (`sensor_review_drafts`) and never matches `sensor.state`, `sensor.detail`, `sensor.conflict`, `sensor.source`, or `sensor.latest.*`. Likewise `SENSOR_RULE_PATHS` (`"sensor.source"`, `"sensor.conflict"`, etc., `C5`) never matches `sensor.0.*`, so `sensor.0.state` stays `"case-record"` as expected by `CaseDomainGroundingTests` (`C7`).
  * **Trap 3 (`skill_sources` `"sensor"` in `common` & role denial):** `ChatIsolation._sensor_facts()` catches `PermissionError` from `self.sensors(denied, case_id)` before `skill_sources()` runs (`C9`), so unauthorized roles (`Programme Support Officer`) never receive `sensor.latest.*` facts; `_sensor(r)` falls through `not cite` and `not conflict` to `_damp(r)`, which returns a valid grounded `answer` citing `workflow/domain-boundary` without numeric sensor values (`C2`, `C8`).
  * **Trap 4 (`-p 'test_chat_domain_questions.py'` running 0 tests):** Running `unittest discover -s tests -p 'test_chat_domain_questions.py'` exits 0 with `Ran 0 tests` because the `#157`/`#164` domain tests are actually in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`) and `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` (`CaseDomainGroundingTests`) (`C6`, `C7`). Our Plan and Implement validation must execute all caller-requested commands AND explicit `-p 'test_chat_case_answers.py'`, `-p 'test_chat_panel.py'`, `-p 'test_regulatory_chat_case_domain_grounding.py'`, and `-p 'test_quality_sensors.py'`, plus add a dedicated seam unit test in `DomainAnswerTests`.
  * **Trap 5 (Tracked parent state file during `git rebase`):** `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json` was committed in `a2a39b2cf` (`C1`). Any unstaged modification to that tracked file must be clean before invoking `git rebase 5f50fc238` and restored/committed cleanly afterward.
* Reflection: All contrarian traps are resolved with concrete code/git facts; no missing evidence remains.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|--------------------|--------------------------|----------------------------|
| Rebase `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`) onto `5f50fc238` rather than merging `5f50fc238` into the topic branch | `C1`, `C2` | accepted | Keeps the single Issue #1288 feature commit linear on top of `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`) for PR #1745 without merge-commit noise, plus a Cycle-2 resolution/tracking commit (or clean rebased commit history). | Selected Recommendation (Option A) |
| Check `conflict = r.fact("sensor.conflict")` BEFORE `detail = r.fact("sensor.detail")` inside `if not cite:` in `_sensor(r)`, then delegate `not cite and not conflict` to `detail` + `return _damp(r)`, and keep `sensor.source` when `cite` is present | `C2`, `C3`, `C4`, `C8` | accepted | Prevents `r.fact("sensor.detail")` from polluting citations or emitting `"No retained sensor reading is shown"` when readings conflict, while preserving 100% of `#157`/`#164` `_damp(r)` behavior when `not conflict`. | Selected Recommendation (Option A) |
| Run explicit `-p 'test_chat_case_answers.py'`, `-p 'test_chat_panel.py'`, `src/agents` `-p 'test_regulatory_chat_case_domain_grounding.py'`, and `src/api` `-p 'test_quality_sensors.py'` in addition to the caller's `-p` commands, and add a focused unit test in `DomainAnswerTests` | `C6`, `C7`, `C8` | accepted | `test_chat_domain_questions.py` does not exist at `5f50fc238`, so relying on `-p 'test_chat_domain_questions.py'` alone would run 0 domain tests. | Selected Recommendation & Plan validation |
| Merge `origin/feat/demo-164-chat-grounding-provenance-0900` into `feat/quality-1288-sensor-ai-2142` via `git merge` | `C1` | rejected | Caller primarily requested Cycle-2 rebase onto `5f50fc238` and branch has only 1 commit (`a2a39b2cf`) above `f5f76b6cc`; rebasing keeps linear stacked PR history. | Rejected Alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope covered completely; merge-base, conflict hunks, citation/fact interactions, and test locations verified directly from git objects.
* Revised brief or revalidation required: none
* Readiness effect: Ready (`C1`–`C10`)

## Evidence Log

* Delegation: inline: single tightly coupled rebase conflict and citation-contract trace across `chat_case_answers.py`, `chat_panel.py`, and focused test suites did not benefit from separate subagent context.

### Codebase Evidence

| ID  | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|-----|-----------------|------------------------|------|------------|-------|
| C1  | Merge-base between `a2a39b2cf` (`feat/quality-1288-sensor-ai-2142`) and `5f50fc238` (`origin/feat/demo-164-chat-grounding-provenance-0900`) is `f5f76b6cc`; `git merge-tree --write-tree 5f50fc238 a2a39b2cf` shows `src/core/src/zava_forward/core/chat_case_answers.py` as the sole content conflict and clean auto-merge on `chat_panel.py`. | `src/core/src/zava_forward/core/chat_case_answers.py:344` | bash (`git merge-base`, `git merge-tree`) | high | Verified against `git ls-remote origin` (`5f50fc238f78e37e31baaed87f5d1eb81943cf14`) |
| C2  | Upstream commit `2b1d40db0` (`PR #1734`, `Refs #164, Refs #1530`) added `DOMAIN_BOUNDARY`, `ORIGIN_RULE`, `RULES_FIRST`, `_damp(r)` (`lines 613-632`), `sensor.{i}.task_key`/`state` in `case_facts()`, and updated `_sensor(r)` (`lines 388-395` at `5f50fc238`) so `not cite` emits `No retained sensor reading is shown for this case. {detail}` when `detail := r.fact("sensor.detail")` and returns `_damp(r)`. | `src/core/src/zava_forward/core/chat_case_answers.py:20` | bash (`git diff f5f76b6cc..5f50fc238`) | high | `_indexes(r.facts, "sensor")` uses `sensor\.(\d+)\.` so it only matches `sensor_review_drafts` |
| C3  | In `a2a39b2cf`, `sensor_facts(view)` sets `sensor.detail` to `view.get("detail") or view.get("conflict_notice")`, `sensor.conflict` to `view.get("conflict_notice")`, and `sensor.source` to `grounding.get("source_text")` when `values` exist. | `src/core/src/zava_forward/core/chat_case_answers.py:159` | view | high | `sensor.detail` is populated on conflict too, so `_sensor(r)` must check `sensor.conflict` before calling `r.fact("sensor.detail")` |
| C4  | In `a2a39b2cf`, `_sensor(r)` handles `conflict = r.fact("sensor.conflict")` under `if not cite:` by emitting the conflict refusal + `sensor.not_retained` + `Case stage:` and returning early, and emits `Reading source: {r.facts['sensor.source']}` when `cite` is present. | `src/core/src/zava_forward/core/chat_case_answers.py:344` | view | high | Preserves both conflict refusal and clean-reading provenance line |
| C5  | `chat_panel.py` in `a2a39b2cf` adds `"sensor.source"` and `"sensor.conflict"` to `SENSOR_RULE_PATHS`, and `5f50fc238` adds `"pas2035"` and `"sensor"` to `skill_sources` `common` plus `RULES_SOURCE_ROOTS` and `RULES_FIRST`. | `src/core/src/zava_forward/core/chat_panel.py:370` | view / bash (`git show 5f50fc238:...`) | high | Cleanly auto-merges; `sensor.0.state` remains `"case-record"` while `sensor.conflict` and `sensor.source` are `"decision-rule"` |
| C6  | `src/core/tests/test_chat_domain_questions.py` does not exist at `5f50fc238`; core domain-answer tests from `2b1d40db0` reside in `DomainAnswerTests` inside `src/core/tests/test_chat_case_answers.py`. | `src/core/tests/test_chat_case_answers.py:322` | bash (`git show 5f50fc238:...`) | high | Running `-p 'test_chat_domain_questions.py'` alone runs 0 tests |
| C7  | End-to-end case-domain grounding tests from `2b1d40db0` reside in `CaseDomainGroundingTests` in `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` (testing `_sensor` -> `_damp` hazard, `sensor.0.state`, and missing-evidence phrasing). | `src/agents/tests/test_regulatory_chat_case_domain_grounding.py:38` | bash (`git show 5f50fc238:...`) | high | Asserts `[Origin: decision_rule]`, `ZF-1/sensor.0.state`, and `No damp, ventilation or sensor evidence` |
| C8  | Issue #1288 grounding tests in `src/api/tests/test_quality_sensor_grounding.py` assert `ZF-1/sensor.source` (`decision-rule`), `ZF-1/sensor.conflict` (`decision-rule`), `"no values are shown"` when consent is declined, and `assertNotIn("No retained sensor reading is shown", reply["reply"])` when readings conflict. | `src/api/tests/test_quality_sensor_grounding.py:72` | view | high | Confirms exact compatibility requirements for both conflict and declined-consent paths |
| C9  | `ChatIsolation._sensor_facts()` catches `(PermissionError, ValueError, LookupError)` from `self.sensors(user, case_id)` and returns `{}` for unauthorized roles before `skill_sources()` executes. | `src/core/src/zava_forward/core/chat_isolation.py:114` | view | high | Role-denied users get empty `sensor.*` facts even with `"sensor"` in `skill_sources` `common` |
| C10 | Upstream commits `ee4f2005e` (`#217`) and `8829c15cc` (`#222`) modified `ai.py`, `ai_registry.py`, and `ai_tasks.py` without touching `assistants.py`, `sensor_view.py`, `sensor_badges.py`, or `src/api/.../web/*.js`. | `src/core/src/zava_forward/core/ai.py:271` | bash (`git diff`) | high | Zero file overlap outside `chat_case_answers.py` and `chat_panel.py` |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* Caller prompt referenced `00442e5e9` (`#157`, `PR #1645`) and `src/core/tests/test_chat_domain_questions.py`, whereas in this repository `00442e5e9` is `style(tools): format ci-affected files` and the exact `_damp(r)` / `sensor.detail` code was merged into `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`) in `2b1d40db0` (`PR #1734`) with tests in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`) and `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` (`CaseDomainGroundingTests`); resolved by primary repository git history (`C1`, `C2`, `C6`, `C7`) -> preserve exact functional contract and run both the caller's exact commands and the actual domain test files with `-p`.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `a2a39b2cf` is 1 commit ahead of `f5f76b6cc` and `5f50fc238` is 11 commits ahead; `chat_case_answers.py` is the sole merge conflict (`chat_panel.py` auto-merges cleanly). | `C1`, `C5`, `C10` | high | Ready for surgical `git rebase 5f50fc238` |
| Q2 | Upstream `2b1d40db0` changed `_sensor(r)` when `not cite` to emit `No retained sensor reading is shown for this case. {detail}` (when `sensor.detail` exists) and `return _damp(r)`, with domain tests in `test_chat_case_answers.py` and `test_regulatory_chat_case_domain_grounding.py`. | `C2`, `C6`, `C7` | high | Must preserve `_damp(r)` delegation whenever `not cite` and `not conflict` |
| Q3 | In `_sensor(r)`, checking `conflict = r.fact("sensor.conflict")` first under `if not cite:` (before `detail = r.fact("sensor.detail")`) keeps conflict replies free of `"No retained sensor reading is shown"` and `case-record` `sensor.detail` citations, while non-conflict `not cite` states (`consent-withheld`, `no-readings`, `unavailable`, role-denied) emit `detail` (if present) and delegate to `_damp(r)`. Clean `cite` keeps `Reading source: {r.facts['sensor.source']}`. | `C2`, `C3`, `C4`, `C5`, `C8`, `C9` | high | Exact conflict resolution for `chat_case_answers.py` is completely specified |
| Q4 | No semantic clashes exist in `_indexes(r.facts, "sensor")`, `SENSOR_RULE_PATHS`, `skill_sources`, or `chat_privacy.redact()`, but `-p 'test_chat_domain_questions.py'` matches 0 files; adding a seam test to `DomainAnswerTests` in `test_chat_case_answers.py` and running explicit `-p` selectors on the real domain test files closes the verification gap. | `C2`, `C5`, `C6`, `C7`, `C8`, `C9` | high | Include seam test in `test_chat_case_answers.py` and targeted `-p` runs in Plan |

## Key Discoveries

* `chat_case_answers.py` is confirmed by `git merge-tree` to be the only conflicting file when rebasing `a2a39b2cf` onto `5f50fc238` (`C1`).
* Evaluating `conflict = r.fact("sensor.conflict")` strictly before `detail = r.fact("sensor.detail")` inside `if not cite:` is essential because `sensor_facts()` populates `sensor.detail` with `conflict_notice` as a fallback (`C3`, `C8`).
* Both `if conflict:` (early return when `not cite`) and `if r.fact("sensor.source"):` (provenance line when `cite` is present) from `a2a39b2cf` must be retained alongside `2b1d40db0`'s `detail` + `return _damp(r)` fallback (`C2`, `C4`).
* Domain-question tests on `5f50fc238` live in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`) and `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` (`CaseDomainGroundingTests`), not `test_chat_domain_questions.py` (`C6`, `C7`).

### Complete Examples

```python
def _sensor(r: Reply) -> None:
    cite = r.fact("sensor.latest.citation")
    if not cite:
        conflict = r.fact("sensor.conflict")
        if conflict:
            r.say(
                "Retained sensor readings conflict, so no single value is selected. "
                + conflict
                + " Use the ordinary quality check, or ask the quality team to inspect the home."
            )
            if r.fact("sensor.not_retained"):
                r.say(r.facts["sensor.not_retained"])
            if r.fact("stage"):
                r.say(f"Case stage: {r.facts['stage']}.")
            return
        detail = r.fact("sensor.detail")
        if detail:
            r.say(f"No retained sensor reading is shown for this case. {detail}")
        return _damp(r)
    temperature = r.fact("sensor.latest.temperature_c")
    humidity = r.fact("sensor.latest.humidity_pct")
    observed = r.fact("sensor.latest.observed_at")
    r.say(
        f"Latest retained reading [{cite}]: temperature_c {temperature} degC, "
        f"humidity_pct {humidity} %RH (relative humidity), observed {observed}."
    )
    if r.fact("sensor.source"):
        r.say(f"Reading source: {r.facts['sensor.source']}")
    for path in ("sensor.freshness", "sensor.health", "sensor.watch", "sensor.thresholds"):
        if r.fact(path):
            r.say(r.facts[path])
    if r.fact("sensor.not_retained"):
        r.say(r.facts["sensor.not_retained"])
    r.say("These readings are synthetic and not calibrated. A person decides any action.")
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: **Option A — Rebase `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`), resolve `_sensor(r)` in `chat_case_answers.py` with `conflict` checked before `detail` + `return _damp(r)` while keeping `sensor.source`, add a focused seam test in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`), and commit Cycle-2 artifacts locally without pushing.**
* Rationale: Keeps linear branch ancestry atop `5f50fc238` for PR #1745, preserves 100% of `#1288` conflict refusal/provenance semantics (`C3`, `C4`, `C8`) and `#157`/`#164` `_damp(r)` domain fallback (`C2`, `C6`, `C7`), and directly tests the combined `_sensor(r)` contract in `src/core`.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`
* Implementation impact: Rebase `a2a39b2cf` onto `5f50fc238` resolving `src/core/src/zava_forward/core/chat_case_answers.py`, add focused seam test in `src/core/tests/test_chat_case_answers.py`, and commit Cycle-2 `.copilot-tracking/` artifacts + test locally.
* Confidence: `high`: verified via `git merge-tree` and full inspection of all interacting modules and tests.

File tree:

```text
src/core/src/zava_forward/core/chat_case_answers.py        (rebase conflict resolution in _sensor)
src/core/tests/test_chat_case_answers.py                   (focused seam test for conflict vs _damp fallback)
.copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md
.copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md
.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md
.copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan-critique.md
.copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-c2-changes.md
.copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-c2-review.md
.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-c2-state.json
```

### Alternative: Option B — `git merge 5f50fc238` into `feat/quality-1288-sensor-ai-2142`

* Approach: Create a merge commit combining `a2a39b2cf` and `5f50fc238` rather than rebasing `a2a39b2cf`.
* Trade-offs: Avoids rewriting local `a2a39b2cf`, but introduces a non-linear merge commit for a 1-commit topic branch when the caller specifically asked for a Cycle-2 rebase onto `5f50fc238`.
* Evidence refs: `C1`
* Rejection rationale: Rebase produces a cleaner linear stacked branch on `5f50fc238` and matches the primary caller instruction (`PR #1745 Cycle-2 rebase onto latest origin/feat/demo-164-chat-grounding-provenance-0900 at 5f50fc238`).

### Alternative: Option C — Evaluate `detail = r.fact("sensor.detail")` before `if conflict:` or delegate conflict cases into `_damp(r)`

* Approach: Run `detail = r.fact("sensor.detail")` unconditionally under `if not cite:` or fall through to `_damp(r)` after emitting the conflict message.
* Trade-offs: Reuses `_damp(r)` footer on conflicts, but records `ZF-1/sensor.detail` (`case-record`) or emits `"No retained sensor reading is shown for this case."`, violating Issue #1288's explicit test and requirement that conflicting readings exist and must not say no reading is shown (`C3`, `C8`).
* Evidence refs: `C2`, `C3`, `C8`
* Rejection rationale: Directly violates `test_conflicting_readings_block_proactive_flag_and_route_chat_without_picking_one` (`assertNotIn("No retained sensor reading is shown", reply["reply"])`) and the caller's explicit specification.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure tracked `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json` has no unstaged edit when `git rebase 5f50fc238` starts, then persist updated parent/child state cleanly after rebase completes.
* Follow-up: Parent Cycle-1 follow-ups (`RV-001` CSS `#employee-chat` height at 720px; `RV-002` live conflict browser check state) remain out-of-scope follow-up items.
* Residual uncertainty: Hosted GitHub Actions CI on PR #1745 remains unobserved locally because pushing is explicitly prohibited (`Do NOT push`).

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Rebase `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`) onto `5f50fc238` and resolve `_sensor(r)` with `conflict` checked before `detail` + `_damp(r)` while retaining `sensor.source` | confirmed | caller + evidence | Satisfies both Issue #1288 conflict/provenance contract and `#157`/`#164` (`2b1d40db0`) `_damp(r)` fallback with linear history | `C1`–`C9` | Plan scopes rebase conflict resolution, seam test in `test_chat_case_answers.py`, and targeted `-p` validation |
| Run both caller-specified `-p` commands and explicit `-p` runs on `test_chat_case_answers.py`, `test_chat_panel.py`, `test_regulatory_chat_case_domain_grounding.py`, and `test_quality_sensors.py` | confirmed | evidence | `test_chat_domain_questions.py` does not exist at `5f50fc238` (`Ran 0 tests`); running the actual domain test files ensures real verification while honoring the `-p`-only rule | `C6`, `C7`, `C8` | Prevents false-green 0-test pass |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none     | none                               | none  | none   | follow-up      |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L        | Inspect hosted CI run after owner pushes PR #1745 | Confirms hosted workflow parity on `5f50fc238` base | Owner push of `feat/quality-1288-sensor-ai-2142` | deferred | `C1`; caller `Do NOT push` constraint |

## Planning Readiness

* Status: Ready
* Decision state: Convergence selection confirmed (Option A)
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`
* Preconditions met: Merge-base (`f5f76b6cc`), target (`5f50fc238`), sole conflict file (`chat_case_answers.py`), citation/fact ordering, and exact `-p` test files verified.
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record |
|----------------------------------|--------|
| Research execution status        | Complete |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order |
| Lane evidence or inline fallback | Inline focused investigation (single tightly coupled git/module rebase seam) |
| Research disposition             | executed |
| Planning Readiness               | Ready (`C1`–`C10`) |
| Blockers                         | none |
| Continuation owner and state     | Confirmed automatic RPI Agent parent; automatic continuation to `Plan` (`rpi-plan`) |

## Advisory Next Step

| Field                            | Record |
|----------------------------------|--------|
| Research disposition             | executed |
| Planning Readiness               | Ready (`C1`–`C10`) |
| Output mode and planning support | convergence; yes, convergence recommendation selected with complete evidence |
| Acting owner                     | confirmed automatic RPI Agent |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness `Ready` (passed); Research self-check (passed); pre-transition state write to `Plan` (passed) |
| Continuation result              | automatic continuation to `Plan` (`rpi-plan`) |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md |
| Notes for planning or re-entry   | Keep tracked `quality-1288-sensor-ai-2142-state.json` clean before running `git rebase 5f50fc238`; test both `test_chat_domain_questions.py` (caller command) and `test_chat_case_answers.py` / `test_regulatory_chat_case_domain_grounding.py` (actual domain tests) with `-p`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All conflicting and adjacent chat/sensor files between `f5f76b6cc`, `a2a39b2cf`, and `5f50fc238` were inspected directly; further research would be redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log (Wider, Deeper, Contrarian, Parent Synthesis, Re-entry), Evidence Log, Findings, Key Discoveries, Alternatives and Decision State, Open Questions, Current/Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none

