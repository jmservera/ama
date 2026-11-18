---
description: "Primary evidence artifact for rebasing feat/ai-116-entra-output-0052 (7b882614d..e7d05fab4) onto origin/feat/demo-164-chat-grounding-provenance-0900 (0c1fa1da4)"
---
<!-- markdownlint-disable-file -->

# Task Research: issue-116-entra-output-0052-c1-rebase

| Field              | Value                                                                                 |
|--------------------|---------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                            |
| Researcher / agent | RPI Agent (`rpi-research`)                                                            |
| Status             | Complete                                                                              |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-rebase-research.md |

## Research Brief

* What to research: Exact commit ancestry, merge-tree conflict boundaries, semantic interactions in `src/core/src/zava_forward/core/store.py` (and any auto-merged files) when rebasing `feat/ai-116-entra-output-0052` (`7b882614d..e7d05fab4`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, after `PR #1769`), tracking-record update rules for `c1` changes/review files, and exact Focused-tier validation prerequisites.
* Why it matters: `e7d05fab4` passed independent review on `7f83f4749`, while `PR #1769` (`0c1fa1da4`, `Refs #83`) subsequently merged into the stacked parent branch `feat/demo-164-chat-grounding-provenance-0900`. A clean, non-regressing rebase inside `C1` preserves both `#83` handoff SLA visibility/escalation and `#116` `MEMBERSHIP_REVISION`/role-visibility controls without spending a new correction cycle.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in this confirmed automatic RPI continuation loop.
* Scope: `7f83f4749..0c1fa1da4` vs `7f83f4749..e7d05fab4`, `src/core/src/zava_forward/core/store.py`, auto-merging files in `0c1fa1da4`, `.copilot-tracking/` `c1` changes/review files, and Focused-tier unit/lint/format/type/rename-regression commands.
* Non-goals: Pushing to `origin`, running Docker builds or `tools/rpi-checks.py --all`, opening a new correction cycle `c2`, or refactoring unrelated modules.
* Criteria: Every conflict hunk and auto-merged overlap between `0c1fa1da4` and `7b882614d..e7d05fab4` is located with exact `path:line` evidence, semantic compatibility between `#83` handoff views and `#116` role-visibility projections is verified, and Focused validation tooling availability is confirmed.
* Requested outputs: Convergent rebase, conflict-resolution, tracking-update, and validation recommendation ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                   |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | What exact conflicts and semantic interactions arise when rebasing `7b882614d..e7d05fab4` onto `0c1fa1da4`, and how should they be resolved and validated? |
| Codebase scope                   | `src/core/`, `src/api/`, `src/agents/`, `tools/rename-zava-tests.py`, `.copilot-tracking/` (`2026-11-15` `c1` artifacts)                 |
| External scope                   | none                                                                                                                                    |
| Initial internal candidate areas | `src/core/src/zava_forward/core/store.py`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` |
| Initial external candidate areas | none                                                                                                                                    |
| Research posture                 | focused                                                                                                                                 |
| Posture provenance               | caller-specified (bounded rebase continuation inside C1 with named commits, file, tracking artifacts, and Focused validation commands)   |
| Explicit limits / deadline       | Rebase continuation inside C1 (no new correction cycle spent); Focused validation tier; no `git push`; no `ask_user`; clean frozen tree |
| Posture-specific completion basis | focused scope and materiality                                                                                                          |
| Edits allowed during research?   | no, research-only                                                                                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                    |
| Known constraints / excluded sources | Code-only local git and test/linter inspection; preserve original C1 critique/review outcomes while recording rebase onto `0c1fa1da4` |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                   | Match and provenance                                   | Scoped authority or output contract                                         | Selected / skipped reason                                                       |
|---------------------|---------------------------------------------|--------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`           | `applyTo: "**"` matches repository and tracking paths  | Focused validation tier, privacy-safe git email, preserve review provenance | Selected: governs validation tier, commit config, and evidence preservation     |
| Skill               | `rpi-research`                              | Explicit caller request for full RPI continuation loop | Read-only 3-wave primary research artifact contract                         | Selected: active phase skill                                                    |
| Skill               | `web-design-guidelines` / frontend skills   | Web UI styling/design skills                           | Frontend review rules                                                       | Skipped: backend Python (`store.py`) rebase and tracking update only; no web UI changes |
| Research specialist | `hve-core-all:rpi-researcher`               | Delegated research worker                              | Separate lane file for independent broad research                           | Skipped: single tightly coupled local git rebase investigation (`<= 5` probes)  |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                           |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------|
| Intake           | Caller supplied exact commits (`7b882614d..e7d05fab4` onto `0c1fa1da4`), conflict target, and checks. | No interaction needed | Proceed in `focused` posture with inline 3-wave inspection in non-interactive automatic mode |
| Direction change | None                                                                                                  | Not applicable       | Brief unchanged                                                                           |
| Convergence      | Single cycle answered Q1-Q4 completely with zero ambiguity.                           | No interaction needed | Converge on Selected Recommendation and hand off to `rpi-plan`                            |

## Scope and Success Criteria

* Scope: Rebase of `7b882614d` and `e7d05fab4` onto `0c1fa1da4`, `store.py` conflict resolution, auto-merge verification across all files touched by `0c1fa1da4`, updates to `c1` changes and review artifacts, and Focused validation commands.
* Assumptions: `origin/feat/demo-164-chat-grounding-provenance-0900` is at `0c1fa1da4`; `e7d05fab4` is clean atop `7b882614d` atop `7f83f4749`; verify via read-only `git merge-tree` and diff inspection.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect rebase of `feat/ai-116-entra-output-0052` (`7b882614d..e7d05fab4`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), resolve `src/core/src/zava_forward/core/store.py` conflict preserving both `0c1fa1da4`'s `handoffs` changes and `7b882614d`'s `MEMBERSHIP_REVISION` / role-visibility changes, update `c1` changes and review artifacts, run the 4 specified Focused validation commands, and commit cleanly without pushing.
* Inferred research questions: Verify whether `e7d05fab4` (the second commit in `7b882614d..e7d05fab4`) also conflicts or applies cleanly after `7b882614d` is rebased, whether any auto-merged file (`server.py`, `test_role_endpoint_inventory.py`, etc.) has subtle semantic or lint/type interaction between `#83` (`0c1fa1da4`) and `#116` (`7b882614d`), and whether the system `python3` environment has `ruff`, `mypy`, and test dependencies directly available for the exact caller validation commands.
* Caller constraints and non-goals: Rebase continuation inside C1 (no new correction cycle spent); do not push; leave `git status --short` empty; do not call `ask_user`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Stay inside C1 rebase continuation; preserve both `0c1fa1da4` handoffs and `7b882614d` role-visibility | Caller prompt       | Constrains conflict resolution and tracking updates; excludes unrelated refactors   |
| exclude                                                  | Do not push to remote, do not run Docker/full gate, and do not prompt via `ask_user`                    | Caller prompt       | Restricts implementation and closeout to local commit and Focused validation tier   |

## Research Questions

|  # | Sub-question                                                                                                                                   | Type (depth / breadth / straightforward) | Priority | Status |
|---:|------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|--------|
| Q1 | What files changed in `0c1fa1da4` (`PR #1769`) relative to `7f83f4749`, and which commits in `7b882614d..e7d05fab4` conflict during rebase?    | straightforward                          | H        | answered |
| Q2 | What are the exact conflicting hunks in `src/core/src/zava_forward/core/store.py`, and how do `0c1fa1da4` handoffs and `7b882614d` `MEMBERSHIP_REVISION`/role-visibility combine cleanly? | depth                                    | H        | answered |
| Q3 | Do any auto-merged files or `#83` handoff tests interact semantically or at lint/format/mypy level with `#116`'s role-visibility projections?  | depth                                    | H        | answered |
| Q4 | How should `issue-116-entra-output-0052-c1-changes.md` and `issue-116-entra-output-0052-c1-review.md` be updated, and do the exact caller `python3` validation commands run cleanly in this environment? | straightforward                          | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-15/issue-116-entra-output-0052-c1-state.json`, `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md`
* Reused (verified) findings: `e7d05fab4` sits atop `7b882614d` atop `7f83f4749`; `origin/feat/demo-164-chat-grounding-provenance-0900` is at `0c1fa1da4` (`PR #1769`, `Refs #83`).
* Superseded / stale: `c1` rebased onto `7f83f4749` (`PR #1761`); that parent base is now superseded by `0c1fa1da4` (`PR #1769`).

## Research Cycle Log

### Cycle 1

* Active direction controls: `narrow` (C1 rebase continuation preserving both `#83` handoffs and `#116` role visibility), `exclude` (no `git push`, no Docker/full gate, no `ask_user`)
* Active research posture and completion basis: `focused`; focused scope and materiality
* Explicit limits or deadline effect: Keeps work bounded inside C1 rebase continuation with Focused validation tier

#### Wave 1: Wider

* Plan and independent lanes: Inline read-only survey of commit graph (`7f83f4749..0c1fa1da4` vs `7f83f4749..e7d05fab4`), `git merge-tree --write-tree --messages 0c1fa1da4 7b882614d`, touched file sets for `0c1fa1da4`, `7b882614d`, and `e7d05fab4`, and local `python3` tooling (`ruff`, `mypy`, `PYTHONPATH` namespace resolution).
* Worker evidence relationships or inline fallback: Inline (`Q1 -> C1, C2, C4`; `Q4 -> C5, C6`).
* Reflection: `0c1fa1da4` touches 17 files (`10` code/test files + `7` tracking files). Replaying `7b882614d` onto `0c1fa1da4` auto-merges `server.py` and `test_role_endpoint_inventory.py` and conflicts only in `src/core/src/zava_forward/core/store.py`; `e7d05fab4` touches none of `0c1fa1da4`'s files. Next wave must inspect every hunk in `store.py`, `sqlstore.py`, and `taskqueues.py`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact conflict markers in `store.py` (`C2`), semantic vs formatting diff between `0c1fa1da4` and `7b882614d` (`C3`), and `MEMBERSHIP_REVISION` / queue fingerprint handling across `store.py`, `sqlstore.py`, and `taskqueues.py`.
* Plan and independent lanes: Inline diff comparison of Ruff-formatted `0c1fa1da4:src/core/src/zava_forward/core/store.py` vs `7b882614d:src/core/src/zava_forward/core/store.py` plus inspection of `sqlstore.py` and `taskqueues.py`.
* Worker evidence relationships or inline fallback: Inline (`Q2 -> C2, C3`; `Q3 -> C3, C5`).
* Reflection: Comparing Ruff-formatted `0c1fa1da4` `store.py` with `7b882614d` `store.py` proves that the 2 conflict markers (`_queue_candidates` and `_work_context`) are pure overlap between `7b882614d`'s multi-line Ruff formatting and `0c1fa1da4`'s `handoff_policy` cache-key element + enriched `handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` call (`detail` at line `731` already auto-merges to `0c1fa1da4`'s 4-argument `handoff_view(...)`), while `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` carry over cleanly from `0c1fa1da4` and all `#116` role-visibility methods in `store.py` (`draft`, `_clean_doc_ai_metadata`, `add_document`, `read_document`, `ai_run`, `_rec_view`, `ai_priority`, `funding_draft`, `ai_live_report`) remain untouched in lines `1016..2075`.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether (a) `0c1fa1da4`'s auto-merged additions in `server.py` and `test_role_endpoint_inventory.py` violate `src/api/pyproject.toml` Ruff/mypy rules or interact adversely with `#116` role-matrix canary tests, (b) bare `cd src/core && python3 -m mypy` fails without `PYTHONPATH`, or (c) untracked `c1-rebase` `.copilot-tracking/` files interfere with `git rebase`.
* Plan and independent lanes: Inline verification of `src/core/pyproject.toml`, `src/api/pyproject.toml`, bare `cd src/core && python3 -m mypy`, `python3 tools/rename-zava-tests.py`, and `test_taskqueues.py` `_queue_candidates` assertions.
* Worker evidence relationships or inline fallback: Inline (`Q3 -> C5`; `Q4 -> C5, C6`).
* Reflection: Contrarian checks confirm bare `cd src/core && python3 -m mypy` succeeds across `336` files (`EXIT:0`), `python3 tools/rename-zava-tests.py` passes `25` tests (`EXIT:0`), `store.py`/`server.py`/`test_role_endpoint_inventory.py` match their `pyproject.toml` lint/format configs, and backing up untracked `c1-rebase` `.copilot-tracking/` files to the session workspace during `git rebase` guarantees a spotless working tree before and after rebase. Recommend running `#83` handoff tests (`test_handoff_escalation_83.py`, `test_handoff_escalation_api_83.py`) and `test_role_endpoint_inventory.py` alongside the 4 caller Focused commands so cross-feature auto-merges are directly verified too.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| Rebase `7b882614d..e7d05fab4` onto `0c1fa1da4` resolving the 2 `store.py` conflict hunks (`_queue_candidates` and `_work_context`) by keeping `0c1fa1da4`'s `handoff_policy` key and 4-arg `handoff_view(...)` alongside `7b882614d`'s formatting and lines `1016..2075` role-visibility changes | `C1`, `C2`, `C3`, `C4` | accepted | Preserves 100% of both `#83` (`0c1fa1da4`) and `#116` (`7b882614d..e7d05fab4`) behavior with `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` inherited cleanly from `0c1fa1da4` | Selected Recommendation |
| Record the `0c1fa1da4` rebase and validation in `c1-changes.md` and `c1-review.md` (preserving original `c1` `Conformant` outcome) plus complete `c1-rebase` RPI tracking in a clean commit atop rebased `e7d05fab4` | `C6` | accepted | Satisfies caller Scope item #3 and repository rule to preserve original critique/review outcomes while leaving `git status --short` empty | Selected Recommendation |
| Squash `7b882614d` and `e7d05fab4` during rebase instead of preserving commit granularity and appending the rebase-tracking commit | `C4`, `C6` | rejected | Rewriting reviewed commit contents beyond conflict resolution obscures reviewed `c0`/`c1` provenance | Alternative rejected |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope covered; every question (`Q1`-`Q4`) is answered from direct git, source, configuration, and tool execution evidence (`C1`-`C6`), and further research is redundant.
* Revised brief or revalidation required: none
* Readiness effect: Ready (`C1`-`C6`)

## Evidence Log

* Delegation: inline: bounded local git rebase and Focused validation inspection (`<= 5` tightly coupled probes; delegation overhead unjustified).

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `origin/feat/demo-164-chat-grounding-provenance-0900` advanced from `7f83f4749` (`PR #1761`) to `0c1fa1da4` (`PR #1769`, `Refs #83`), modifying `progress.py`, `server.py`, `test_handoff_escalation_api_83.py`, `test_role_endpoint_inventory.py`, `exception_register.py`, `sqlstore.py`, `store.py`, `taskqueues.py`, `workflows.py`, and `test_handoff_escalation_83.py`. | `src/core/src/zava_forward/core/taskqueues.py:7` | read / git show | high | `taskqueues.MEMBERSHIP_REVISION` bumped `3 -> 4` in `0c1fa1da4`; `sqlstore.py:761-768` includes `[..., taskqueues.MEMBERSHIP_REVISION, policy]` |
| C2 | Read-only `git merge-tree --write-tree --messages 0c1fa1da4 7b882614d` auto-merges `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py` cleanly and reports a single content conflict in `src/core/src/zava_forward/core/store.py` (`_queue_candidates` and `_work_context`), while `detail` (`d["handoff"] = handoff_view(...)`) auto-merges cleanly. | `src/core/src/zava_forward/core/store.py:474` | git merge-tree | high | Conflict markers at merged lines `476-487` (`_queue_candidates`) and `625-635` (`_work_context`) |
| C3 | Diffing Ruff-formatted `0c1fa1da4` `store.py` against `7b882614d` `store.py` confirms `0c1fa1da4` adds `json.dumps(self.data.get("handoff_policy"), sort_keys=True)` in `_queue_candidates` and `handoff_view(c, as_of=self.as_of, policy=..., staff=...)` in `_work_context` and `detail`, while `7b882614d`'s role-visibility changes (`draft`, `_clean_doc_ai_metadata`, `add_document`, `read_document`, `ai_run`, `_rec_view`, `ai_priority`, `funding_draft`, `ai_live_report`) occupy non-overlapping lines `1016..2075`. | `src/core/src/zava_forward/core/store.py:1019` | python3 / ruff / difflib | high | Zero semantic conflict between `#83` handoffs and `#116` role-visibility projections |
| C4 | Commit `e7d05fab4` (`fix(core): preserve reviewer-authored notes in _record_view and fix docstring`) touches only `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai_tasks.py`, `src/api/tests/test_ai_tasks.py`, and 7 `.copilot-tracking/.../issue-116-entra-output-0052-c1-*` files, none of which overlap `0c1fa1da4`. | `src/core/src/zava_forward/core/ai_tasks.py:262` | git diff | high | Replays cleanly onto rebased `7b882614d` |
| C5 | `src/core/pyproject.toml` and `src/api/pyproject.toml` configure Ruff (`line-length = 100`, `py312`) and `mypy` (`strict = true`); bare `(cd src/core && python3 -m mypy)` passes on `336` files and `python3 tools/rename-zava-tests.py` passes `25` tests, while `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests` resolves `zava_forward.{core,agents,api}` for `unittest`. | `src/core/pyproject.toml:31` | view / bash | high | All 4 caller Focused validation commands work directly with `python3` |
| C6 | `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` record the prior `7f83f4749` rebase and note `PR #1769` (`0c1fa1da4`) under `Residual Work`. | `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md:102` | view | high | Updating both after rebasing onto `0c1fa1da4` satisfies Scope item #3 while preserving `c1`'s original `Conformant` review verdict |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `0c1fa1da4` (`PR #1769`) is 1 commit ahead of `7f83f4749`; rebasing `7b882614d..e7d05fab4` conflicts only when replaying `7b882614d` on `src/core/src/zava_forward/core/store.py`, and `e7d05fab4` replays cleanly afterward. | `C1`, `C2`, `C4` | high | Ready for deterministic rebase in `P01` |
| Q2 | `store.py` has 2 conflict markers (`_queue_candidates` and `_work_context`); keeping `json.dumps(self.data.get("handoff_policy"), sort_keys=True)` in `_queue_candidates` and `handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` in `_work_context` (matching auto-merged `detail`), while keeping all `7b882614d` formatting and lines `1016..2075` role-visibility changes, preserves both `0c1fa1da4` (`MEMBERSHIP_REVISION = 4` in `taskqueues.py` + `handoff_policy` in `sqlstore.py`/`store.py`) and `7b882614d`. | `C1`, `C2`, `C3` | high | Exact line-level conflict resolution defined |
| Q3 | Auto-merged `server.py` and `test_role_endpoint_inventory.py` cleanly combine `#83`'s new `/api/handoffs/{unowned,escalated,escalate-overdue}` endpoints with `#116`'s role-visibility checks; running `#83` handoff suites + `test_content_standard.py` + `test_human_review_effectiveness_223.py` alongside the 4 caller Focused commands verifies full cross-feature compatibility. | `C2`, `C5` | high | Include `#83` and `#116` C1 regression tests in Focused validation |
| Q4 | Both `c1-changes.md` and `c1-review.md` should be updated in a clean post-rebase tracking commit (alongside `c1-rebase` RPI artifacts) recording the new rebased commit SHAs atop `0c1fa1da4`, preserving `c1`'s original `Conformant` verdict, and verifying all 4 caller `python3` commands. | `C5`, `C6` | high | Satisfies Scope items #3-#5 cleanly |

## Key Discoveries

* Only `src/core/src/zava_forward/core/store.py` conflicts when rebasing `7b882614d..e7d05fab4` onto `0c1fa1da4` (`C2`), and `e7d05fab4` has zero file overlap with `0c1fa1da4` (`C4`).
* The two `store.py` conflict blocks (`_queue_candidates` and `_work_context`) are pure formatting-vs-handoff-argument overlaps, while `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` come cleanly from `0c1fa1da4` and every `#116` role-visibility change in `store.py` (`1016..2075`) applies cleanly (`C1`, `C3`).
* All four caller Focused validation commands (`PYTHONPATH=... python3 -m unittest ...`, `cd src/core && python3 -m ruff ... && python3 -m mypy`, `cd src/api && python3 -m ruff ...`, and `python3 tools/rename-zava-tests.py`) work directly on the host `python3` (`C5`).

### Complete Examples (when applicable)

```python
    def _queue_candidates(self, queue):
        """Index IDs, never viewer-projected context; called under the store lock."""
        key = (
            self.version,
            self.as_of,
            controls.today(),
            json.dumps(ranking.CURRENT, sort_keys=True),
            json.dumps(self.data.get("handoff_policy"), sort_keys=True),
        )
```

```python
            building_reasons=buildings.blockers(data, cases, c),
            resident_reasons=resident_gate(c),
            technical_missing=missing_items(c),
            handoff=handoff_view(
                c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff")
            ),
        )
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Temporarily back up untracked `c1-rebase` `.copilot-tracking/` files to the session workspace, fetch `origin feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), rebase `7b882614d..e7d05fab4` onto `0c1fa1da4` resolving the 2 `store.py` hunks (`_queue_candidates` and `_work_context`) to preserve both `0c1fa1da4` handoff SLA visibility/cache invalidation and `7b882614d` formatting + role-visibility changes, restore `c1-rebase` `.copilot-tracking/` files, update `issue-116-entra-output-0052-c1-changes.md` and `issue-116-entra-output-0052-c1-review.md` to record the rebase onto `0c1fa1da4` (while preserving `c1`'s original `Conformant` verdict), run the 4 caller Focused validation commands plus targeted `#83`/`#116` cross-feature checks, complete `rpi-review`, and commit the tracking updates cleanly with the Copilot trailer without pushing.
* Rationale: Preserves reviewed commit lineage (`7b882614d'` and `e7d05fab4'` atop `0c1fa1da4`), keeps `0c1fa1da4` and `#116` semantics 100% intact, records full RPI continuation evidence inside C1 without spending a new correction cycle, and leaves `git status --short` empty.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`
* Implementation impact: Rebased `src/core/src/zava_forward/core/store.py` in `7b882614d'`, updated `issue-116-entra-output-0052-c1-changes.md` and `issue-116-entra-output-0052-c1-review.md`, and `c1-rebase` RPI tracking artifacts.
* Confidence: high: every conflict line and validation tool was verified directly against `0c1fa1da4` and `7b882614d..e7d05fab4`.

File tree (when new, changed, or removed files are involved):

```text
src/core/src/zava_forward/core/store.py (conflict resolution during rebase of 7b882614d onto 0c1fa1da4)
.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md (updated)
.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md (updated)
.copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-rebase-research.md (new)
.copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md (new)
.copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md (new)
.copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan-critique.md (new)
.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-rebase-changes.md (new)
.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-rebase-review.md (new)
.copilot-tracking/rpi-sessions/2026-11-15/issue-116-entra-output-0052-c1-rebase-state.json (new)
```

### Alternative: Squash `7b882614d` and `e7d05fab4` or Amend `e7d05fab4'` In-Place With Tracking Edits

* Approach: Fold the rebase-continuation tracking updates directly into `e7d05fab4'` via `git commit --amend` instead of adding a clean `docs(tracking)`/`chore` commit atop rebased `e7d05fab4'`.
* Trade-offs: Saves one commit in `git log`, but mutates the already-reviewed `e7d05fab4` tree beyond mechanical rebase replay and creates a circular SHA reference if `c1-changes.md`/`c1-review.md` record the rebased commit SHA of `e7d05fab4'`.
* Evidence refs: `C4`, `C6`
* Rejection rationale: Keeping `7b882614d'` and `e7d05fab4'` as pure rebased commits and recording the exact rebased SHAs + `c1-rebase` evidence in a clean commit atop `e7d05fab4'` avoids circular SHA edits and preserves exact reviewed commit diffs.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Verify privacy-safe repository-local `git config --local user.email` (`{id}+{login}@users.noreply.github.com` from `gh api user`) before running `git rebase` and `git commit` so rebased commits and the final tracking commit carry the compliant committer address.
* Follow-up: Shared post-provider record-visibility scrubbing helper across `ai_tasks._record_view`, `Store._rec_view`, and `ChatIsolation.scrub_thread`; external OD-14 / OD-19 and Microsoft Entra B2B tenant configuration.
* Residual uncertainty: none within repository rebase and Focused-tier validation scope.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Rebase `feat/ai-116-entra-output-0052` (`7b882614d..e7d05fab4`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) inside C1 without spending a new correction cycle | confirmed | user | Parent branch advanced when `PR #1769` merged | `C1`, `C2` | Target base is `0c1fa1da4`; no `git push` |
| Resolve `store.py` `_queue_candidates` and `_work_context` hunks by preserving `0c1fa1da4`'s `handoff_policy` key and 4-arg `handoff_view(...)` together with `7b882614d`'s formatting and lines `1016..2075` role-visibility changes (`taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` inherited from `0c1fa1da4`) | proposed | evidence | Preserves 100% of `#83` and `#116` semantics | `C1`, `C2`, `C3` | Clean single-file conflict resolution during `git rebase` |
| Add a clean commit atop rebased `e7d05fab4'` updating `c1-changes.md` and `c1-review.md` plus `c1-rebase` RPI artifacts | proposed | evidence / constraint | Avoids circular SHA references and preserves reviewed `7b882614d'`/`e7d05fab4'` diffs | `C4`, `C6` | Leaves `git status --short` empty |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none | none | none | none | non-blocking |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Inspect shared scrubbing helper refactor design across `ai_tasks.py`, `store.py`, and `chat_isolation.py` | Reduces duplicate redaction checks | Post-merge refactoring cycle | deferred | `Q3`; `C3` |

## Planning Readiness

* Status: Ready
* Decision state: Converged on clean rebase onto `0c1fa1da4`, 2-hunk `store.py` conflict resolution, `c1` changes/review addendum + `c1-rebase` tracking commit, and Focused validation.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`
* Preconditions met: Exact conflict hunks, auto-merged diffs, commit boundaries, tracking files, and host `python3` validation tools verified.
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                     |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                                       |
| Lane evidence or inline fallback | Inline fallback: tightly coupled local git rebase and Focused validation inspection (`<= 5` direct probes)    |
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C6`)                                                                                            |
| Blockers                         | none                                                                                                         |
| Continuation owner and state     | Confirmed automatic RPI Agent (`automatic` continuation to `Plan`)                                           |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C6`)                                                                                            |
| Output mode and planning support | `convergence`; yes — supports direct `rpi-plan` handoff                                                      |
| Acting owner                     | Confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (`passed`), Planning Readiness `Ready` (`passed`), self-check (`passed`)       |
| Continuation result              | Automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-rebase-research.md                      |
| Notes for planning or re-entry   | Temporarily move untracked `c1-rebase` `.copilot-tracking/` files to session workspace before `git rebase` and restore immediately after |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Focused scope is completely covered with direct codebase and git merge-tree evidence (`C1`-`C6`); additional cycles would be redundant.

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
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log (Waves 1-3), Evidence Log (`C1`-`C6`), Findings, Key Discoveries, Alternatives, Open Questions, Current/Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources.
* Missing or limited sections: none

