<!-- markdownlint-disable-file -->

# Task Research: issue-154-rep-expiry-views-rebase-0c1fa1da4

| Field              | Value                                                                                              |
|--------------------|----------------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                         |
| Researcher / agent | rpi-research (under RPI Agent)                                                                     |
| Status             | Complete                                                                                           |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-research.md      |

## Research Brief

* What to research: Exact commit ancestry, file overlap, three-way merge conflict boundary, semantic route/store interactions, and validation commands required to rebase `feat/ux-154-rep-expiry-views` (`99a596629`, anchored on `02ab20cac`) onto newly merged parent tip `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, incorporating PR #1761 `7f83f4749` and PR #1769 `0c1fa1da4`).
* Why it matters: Ensures the rebase continuation preserves both PR #1769's overdue/unowned/escalated handoff route inventory entries and `#154`'s representative task-limited view and session-expiry entries without regressions, spending zero correction cycles.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` on branch `feat/ux-154-rep-expiry-views`.
* Scope: Git commits `02ab20cac..0c1fa1da4` and `02ab20cac..99a596629`, overlapping files `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py`, `.copilot-tracking/` `#154` changes/review/state artifacts, and focused validation runners.
* Non-goals: Pushing to remote, opening or editing GitHub PRs, modifying `src/api/src/zava_forward/api/web/role-screens.js`, or altering non-conflicting `#154` / `#164` / `#83` business logic.
* Criteria: Every claim grounded in workspace `path:line` and read-only git inspection (`git merge-tree`); conflict hunks and route assertions verified cleanly.
* Requested outputs: Converged conflict-resolution, artifact-update, validation, and local-commit plan input.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                     |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Which files overlap between `0c1fa1da4` and `99a596629`, what exact merge conflicts occur, and are there semantic or typing/lint interactions post-merge? |
| Codebase scope                       | `src/api/tests/test_role_endpoint_inventory.py`, `src/api/src/zava_forward/api/server.py`, `src/api/pyproject.toml`, `src/core/pyproject.toml`, `.copilot-tracking/` |
| External scope                       | none                                                                                                                                                      |
| Initial internal candidate areas     | `src/api/tests/test_role_endpoint_inventory.py`, `src/api/src/zava_forward/api/server.py`, `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md` |
| Initial external candidate areas     | none                                                                                                                                                      |
| Research posture                     | focused                                                                                                                                                   |
| Posture provenance                   | default (bounded internal rebase continuation with named source commit `99a596629`, target commit `0c1fa1da4`, and single conflict file)                  |
| Explicit limits / deadline           | Do not push; leave clean working tree (`git status --short` empty); do not invoke interactive prompts.                                                    |
| Posture-specific completion basis    | focused scope and materiality                                                                                                                             |
| Edits allowed during research?       | no, research-only                                                                                                                                         |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                                      |
| Known constraints / excluded sources | Read-only git/file inspection during research; preserve privacy-safe noreply git identity and `Co-authored-by` trailer.                                   |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                    | Match and provenance                                   | Scoped authority or output contract                                    | Selected / skipped reason                                                       |
|---------------------|----------------------------------------------|--------------------------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA repo) | `applyTo: "**"` matches workspace and tracking paths   | Enforces KB reading, validation tiering, noreply git config, no-push   | Selected: mandatory repository governance                                       |
| Skill               | `git-merge` / `web-design-guidelines`        | Installed plugin/project skills                        | Git merge helper / Web UI guidelines                                   | Skipped: backend/test Python rebase only (`role-screens.js` untouched)          |
| Research specialist | `hve-core-all:rpi-researcher`                | General research lane subagent                         | Bounded subagent lane artifact                                         | Skipped (inline preferred): two overlapping files inspected directly in 4 calls |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered  | Resulting decision or selected further research                                 |
|------------------|-------------------------------------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------|
| Intake           | Explicit non-interactive caller brief specifies exact commits, conflict resolution, and validations.  | N/A (non-interactive) | Execute focused 3-wave cycle inline.                                            |
| Direction change | None.                                                                                                 | N/A                   | Keep strict rebase + conflict-resolution + `#154` tracking update scope.        |
| Convergence      | `git merge-tree --write-tree --messages 0c1fa1da4 99a596629` confirms exact single-file conflict.     | Converged             | Proceed to `rpi-plan` with `Planning Readiness: Ready`.                         |

## Scope and Success Criteria

* Scope: Rebase `99a596629` onto `0c1fa1da4`, resolve `src/api/tests/test_role_endpoint_inventory.py`, update `#154` `.copilot-tracking/` artifacts, and run focused validation.
* Assumptions:
  * `src/api/src/zava_forward/api/server.py` auto-merges cleanly without semantic collisions.
  * `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json` should remain valid JSON when updated.
* Success criteria:
  * Every research question is answered with `path:line` evidence.
  *Findings, decisions, and readiness claims cite Evidence Log IDs (`C1`–`C7`).
  * Alternatives are compared and one convergence recommendation is selected.

## Task Research Requests

* Explicit requests: Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), identify and prepare resolution for the single merge conflict in `src/api/tests/test_role_endpoint_inventory.py`, prepare updates to `#154` changes and review artifacts, and verify focused validation commands.
* Inferred research questions: Whether `server.py` auto-merge or `pyproject.toml` lint/mypy rules introduce secondary interactions when `7f83f4749` (#1761) and `0c1fa1da4` (#1769) combine with `99a596629` (#154), and whether updating tracked `#154` artifacts must occur after `git rebase` completes so the working tree is clean during `git rebase`.
* Caller constraints and non-goals: Do not push; leave `git status --short` empty; exit without interactive prompts.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------|
| narrow                                                   | Focused validation tier specified by caller (`unittest`, `ruff`, `mypy`, `tools/rename-zava-tests.py`). | Caller intake       | Scopes validation checks without altering business logic.        |
| exclude                                                  | Do not push and do not call `ask_user`.                                                                 | Caller intake       | Local commit only; automatic non-interactive completion.         |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | What commits landed between `02ab20cac` and `0c1fa1da4`, and which files overlap with `99a596629`?                                                | straightforward                          | H        | answered |
| Q2 | What exact lines conflict in `src/api/tests/test_role_endpoint_inventory.py`, and how do both sides' route assertions work together?              | depth                                    | H        | answered |
| Q3 | Does `src/api/src/zava_forward/api/server.py` or `pyproject.toml` have any semantic, route-order, lint, or `mypy` collision after auto-merge?     | depth                                    | H        | answered |
| Q4 | In what order must `git rebase`, `#154` tracking updates, and commits run so `git rebase` runs on a clean tracked tree and leaves zero dirty files?| straightforward                          | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-research.md`, `.copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-plan.md`, `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md`, `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json`, and `.copilot-tracking/plans/2026-11-13/435-uni-post1542-rebase-2013-plan.md`.
* Reused (verified) findings:
  * `99a596629` delivered Issue #154 C3 across 10 source/test/config files (`resident_journey_design.py`, `resident_decisions.py`, `resident_showcase.py`, `resident_demo/app.py`, `server.py`, `test_resident_journey_design.py`, `test_representative_expiry_api.py`, `test_role_endpoint_inventory.py`, and `src/{core,api}/pyproject.toml`) plus 7 `.copilot-tracking/` files.
* Superseded / stale:
  * Parent tip moved from `02ab20cac` to `0c1fa1da4` after PR #1761 (`7f83f4749`) and PR #1769 (`0c1fa1da4`) merged.
  * `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json` had a missing JSON comma between `confirmed_decisions[2]` and `confirmed_decisions[3]` at line 35 that should be repaired when updating `#154` tracking artifacts.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (focused validation tier), exclude (no push, no interactive prompt).
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: none.

#### Wave 1: Wider

* Plan and independent lanes: Inline breadth inspection of `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git diff 02ab20cac..0c1fa1da4 --stat`, `git show --stat 99a596629`, and `comm -12` file-overlap analysis.
* Worker evidence relationships or inline fallback: Inline:
  * Q1 -> Two commits landed on parent branch `origin/feat/demo-164-chat-grounding-provenance-0900`: `7f83f4749` (PR #1761, #164 chat eval & revocation) and `0c1fa1da4` (PR #1769, #83 BG-010 unaccepted handoff SLA visibility and escalation). Exactly two files overlap with `99a596629`: `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py` (`C1`, `C2`).
* Reflection: Overlap is minimal (2 files). Proceed to Wave 2 to inspect exact line diffs and run read-only `git merge-tree`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact diffs on `server.py`, `test_role_endpoint_inventory.py`, `pyproject.toml`, and `git merge-tree --write-tree --messages 0c1fa1da4 99a596629`.
* Plan and independent lanes: Inline inspection of both sides' hunks and `RoleEndpointInventory` route-coverage regexes.
* Worker evidence relationships or inline fallback: Inline:
  * Q2 -> `git merge-tree` confirms `server.py` auto-merges cleanly and `src/api/tests/test_role_endpoint_inventory.py` has the sole content conflict (`C2`, `C3`, `C4`):
    * `0c1fa1da4` added `"/api/handoffs/unowned", "/api/handoffs/escalated"` to `GET_ENDPOINTS` (`test_role_endpoint_inventory.py:22`) and `("/api/handoffs/escalate-overdue", {})` to `POST_ENDPOINTS` (`test_role_endpoint_inventory.py:30`).
    * `99a596629` added `"/api/cases/ZF-1/representative-view?representative_ref=SYN-REP"` to `GET_ENDPOINTS` (`test_role_endpoint_inventory.py:29`), `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})` to `POST_ENDPOINTS` (`test_role_endpoint_inventory.py:35`), and `"representative-view"` to `test_inventory_covers_dynamic_case_actions_added_by_integration` (`test_role_endpoint_inventory.py:144`).
    * Adjacency of lines 29 and 30 triggers git's 3-line context conflict across the `GET_ENDPOINTS` tail and `POST_ENDPOINTS` head.
  * Q3 -> `server.py` hunks in `0c1fa1da4` (`_parse_max_age_hours` at lines 188-205, `get_kind` at line 322, `/api/handoffs/unowned` + `/api/handoffs/escalated` at lines 840-856, `chat_eval` at lines 936-966, and `/api/handoffs/escalate-overdue` at lines 1484-1500) are 30+ lines away from `99a596629`'s `/representative-view` GET/POST handlers (lines 992-1018 and 1578-1605). Neither `7f83f4749` nor `0c1fa1da4` modified `src/core/pyproject.toml` or `src/api/pyproject.toml`, and `test_role_endpoint_inventory.py` is already in `[tool.ruff.format].exclude` and `per-file-ignores` (`C5`, `C6`).
* Reflection: Both route sets are orthogonal and required by `test_inventory_covers_every_route_in_the_server` (`test_role_endpoint_inventory.py:67-71`) and `test_inventory_covers_dynamic_case_actions_added_by_integration` (`test_role_endpoint_inventory.py:142-145`). Wave 3 tests contrarian risks around rebase working-tree cleanliness, commit amending policy, and JSON validity.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries:
  1. What happens if tracked `#154` files (`issue-154-rep-expiry-views-changes.md`, `issue-154-rep-expiry-views-review.md`, `issue-154-rep-expiry-views-state.json`) are edited before `git rebase`?
  2. Should the post-rebase `.copilot-tracking/` updates amend the rebased commit or create a clean follow-on commit?
  3. Could `test_every_role_against_every_endpoint` fail when both `/api/handoffs/*` and `/api/cases/ZF-1/representative-view` run in the same `RoleEndpointInventory` matrix?
* Plan and independent lanes: Inline verification against git rebase rules, repository instructions, and `RoleEndpointInventory` assertions.
* Worker evidence relationships or inline fallback: Inline:
  * Modifying tracked `#154` files before `git rebase` would dirty the tracked index/worktree and block `git rebase` (`cannot rebase: You have unstaged changes`). Untracked child-task files under `.copilot-tracking/*/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-*` do not overlap any commit in `02ab20cac..99a596629` or `02ab20cac..0c1fa1da4`, so `git rebase` runs cleanly while tracked `#154` files remain untouched until after `git rebase --continue` finishes (`C7`).
  * Repository instructions state "obtain the owner's permission before amending an existing commit"; creating a clean commit on top of the rebased `99a596629` commit for the `#154` tracking updates and rebase-continuation RPI records avoids amending while keeping commit history explicit and clean.
  * In `test_every_role_against_every_endpoint`, `/api/handoffs/unowned`, `/api/handoffs/escalated`, and `/api/handoffs/escalate-overdue` are read/escalate handoff endpoints that do not mutate resident authority grants or `ZF-1` contacts/hazards, so both endpoint sets coexist without fixture interference (`C3`, `C4`).
* Reflection: All three contrarian checks resolved cleanly and deterministically.

#### Parent Synthesis and Disposition

| Material / claim                                                                                                 | Evidence IDs | Parent disposition | Evidence-based rationale                                                                 | Primary-artifact treatment |
|------------------------------------------------------------------------------------------------------------------|--------------|--------------------|------------------------------------------------------------------------------------------|----------------------------|
| Only `test_role_endpoint_inventory.py` conflicts during rebase of `99a596629` onto `0c1fa1da4`                   | C1, C2, C3   | accepted           | Proven via `git merge-tree --write-tree --messages 0c1fa1da4 99a596629`.                 | Selected recommendation    |
| Combine both `0c1fa1da4` handoff inventory entries and `99a596629` `representative-view` entries                 | C3, C4       | accepted           | Required by `test_inventory_covers_every_route_in_the_server` and dynamic action check.  | Selected recommendation    |
| Edit tracked `#154` changes/review/state files only after `git rebase --continue`, then commit as a clean commit | C6, C7       | accepted           | Keeps tracked worktree clean for `git rebase` and honors repository non-amend guidance.  | Selected recommendation    |
| Amend rebased commit with tracking updates                                                                       | C7           | rejected           | Unnecessary history rewrite after `git rebase --continue`; separate commit is cleaner.   | Rejected alternative       |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Complete coverage of commit range, exact 3-way merge conflict simulation, route inventory invariants, and validation commands with zero open uncertainties.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded two-file rebase overlap (`server.py` and `test_role_endpoint_inventory.py`) verified directly in 4 read-only git/view calls.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `origin/feat/demo-164-chat-grounding-provenance-0900` is at `0c1fa1da4`, two commits ahead of `99a596629`'s parent `02ab20cac` (`7f83f4749` PR #1761 and `0c1fa1da4` PR #1769). | `src/api/src/zava_forward/api/server.py:1` | bash (`git fetch` / `git log`) | high | Verified exact commit SHAs after fetch |
| C2 | `git merge-tree --write-tree --messages 0c1fa1da4 99a596629` auto-merges `server.py` cleanly and reports a single content conflict in `src/api/tests/test_role_endpoint_inventory.py`. | `src/api/tests/test_role_endpoint_inventory.py:19` | bash (`git merge-tree`) | high | Zero other conflicting paths |
| C3 | `0c1fa1da4` adds `"/api/handoffs/unowned"` and `"/api/handoffs/escalated"` to `GET_ENDPOINTS` and `("/api/handoffs/escalate-overdue", {})` to `POST_ENDPOINTS`. | `src/api/tests/test_role_endpoint_inventory.py:22` | bash (`git diff`) | high | Matches new routes in `server.py:322,840,1484` |
| C4 | `99a596629` adds `"/api/cases/ZF-1/representative-view?representative_ref=SYN-REP"` to `GET_ENDPOINTS`, `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})` to `POST_ENDPOINTS`, and `"representative-view"` to `test_inventory_covers_dynamic_case_actions_added_by_integration`. | `src/api/tests/test_role_endpoint_inventory.py:29` | view | high | Also lines `35` and `144` |
| C5 | `server.py` hunks from `0c1fa1da4` (lines 188-205, 322, 840-856, 936-966, 1484-1500) are disjoint from `99a596629`'s `/representative-view` GET/POST handlers (lines 992-1018, 1578-1605). | `src/api/src/zava_forward/api/server.py:989` | bash (`git diff`) | high | Clean auto-merge |
| C6 | `src/api/pyproject.toml` excludes `tests/test_role_endpoint_inventory.py` from `ruff format` and `E501` line-length checks while preserving `test_representative_expiry_api` mypy overrides. | `src/api/pyproject.toml:45` | view | high | Zero `pyproject.toml` changes in `02ab20cac..0c1fa1da4` |
| C7 | Existing parent state file `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json` is tracked in `99a596629` and has a missing comma after `confirmed_decisions[2]` at line 35; editing tracked `#154` files after `git rebase --continue` avoids dirty-tree rebase errors and allows clean JSON repair. | `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json:35` | view | high | Tracked in commit `99a596629` |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `0c1fa1da4` adds PR #1761 (`7f83f4749`) and PR #1769 (`0c1fa1da4`); only `server.py` and `test_role_endpoint_inventory.py` overlap with `99a596629`. | C1, C2 | high | Confirms exact rebase target and 2-file overlap. |
| Q2 | `test_role_endpoint_inventory.py` conflicts solely because `GET_ENDPOINTS` line 29 (`99a596629`) and `POST_ENDPOINTS` line 30 (`0c1fa1da4`) are adjacent; keeping both sets satisfies all inventory tests. | C2, C3, C4 | high | Deterministic union resolution in `GET_ENDPOINTS`, `POST_ENDPOINTS`, and dynamic case actions. |
| Q3 | `server.py` merges cleanly with no route-order or fixture interference; `pyproject.toml` configs have zero overlap. | C5, C6 | high | No production code edits required beyond git auto-merge. |
| Q4 | Untracked `issue-154-rep-expiry-views-rebase-0c1fa1da4-*` artifacts do not block `git rebase`; tracked `#154` artifacts are updated post-rebase and committed in a clean commit with `Co-authored-by`. | C7 | high | Ready for `rpi-plan` -> `rpi-implement` -> `rpi-review`. |

## Key Discoveries

* `git merge-tree` proved prior to mutating git state that `src/api/tests/test_role_endpoint_inventory.py` is the single merge conflict when rebasing `99a596629` onto `0c1fa1da4` (`C2`).
* Preserving `"/api/handoffs/unowned"`, `"/api/handoffs/escalated"`, and `("/api/handoffs/escalate-overdue", {})` alongside `"/api/cases/ZF-1/representative-view?representative_ref=SYN-REP"`, `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})`, and `"representative-view"` satisfies every assertion in `RoleEndpointInventory` (`C3`, `C4`).
* Repairing the missing comma in `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json` while recording the rebased base `0c1fa1da4` restores strict JSON validity (`C7`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Keep tracked files clean before running `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` in `rpi-implement`; resolve `src/api/tests/test_role_endpoint_inventory.py` with the exact union of `0c1fa1da4` handoff inventory entries and `99a596629` `representative-view` entries and complete `git rebase --continue`; run all focused validations (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `tools/rename-zava-tests.py`); update `#154` `.copilot-tracking/` changes, review, and state artifacts plus child rebase-continuation RPI artifacts; and create one clean tracking commit on top of the rebased feature commit without pushing.
* Rationale: Preserves exact rebased feature commit provenance, avoids `git commit --amend`, ensures `git rebase` runs on a clean tracked tree, and leaves `git status --short` empty after final state persistence.
* Evidence refs: C1, C2, C3, C4, C5, C6, C7
* Implementation impact: Rebase `99a596629` -> new SHA on `0c1fa1da4` (resolving `src/api/tests/test_role_endpoint_inventory.py`), update `#154` tracking artifacts, add `issue-154-rep-expiry-views-rebase-0c1fa1da4` tracking artifacts, commit locally.
* Confidence: high: 3-way merge already simulated via `git merge-tree`.

```text
src/api/tests/test_role_endpoint_inventory.py (conflict resolved during rebase)
.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md (updated)
.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md (updated)
.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json (updated + JSON comma fixed)
.copilot-tracking/*/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-* (new child RPI records)
```

### Alternative: Amend Rebased Feature Commit With Post-Rebase Tracking Artifacts

* Approach: Fold the updated `#154` tracking files and child rebase-continuation RPI files into the rebased feature commit via `git commit --amend`.
* Trade-offs: Produces one commit above `0c1fa1da4`, but rewrites the rebased feature commit a second time after `git rebase --continue` and conflicts with repository guidance against unrequested commit amending.
* Evidence refs: C7
* Rejection rationale: Separate clean tracking commit preserves the rebased feature commit intact and records the post-rebase validation SHA cleanly.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure final RPI state write occurs before the final `git commit` so `git status --short` is completely empty on exit.
* Follow-up: Parent Issue #154 sibling criteria (`C2` portal screens and `C5` / `#155` usability sessions) remain separate backlog items.
* Residual uncertainty: none

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Resolve `test_role_endpoint_inventory.py` by preserving both `0c1fa1da4` handoff entries and `99a596629` `representative-view` entries | confirmed | user / evidence | Both route families exist in merged `server.py` and are enforced by `RoleEndpointInventory` | C2, C3, C4, C5 | Zero production code modifications outside git rebase auto-merge |
| Perform `git rebase` before editing tracked `#154` artifacts, and commit final tracking state cleanly without pushing | confirmed | constraint / evidence | Prevents dirty-tree rebase failure and leaves `git status --short` empty | C7 | Clean frozen branch tip ready for inspection/push |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none | none | none | none | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | none | Rebase boundary is fully determined | Only if new commits land on parent branch | no | Q1–Q4; C1–C7 |

## Planning Readiness

* Status: Ready
* Decision state: Converged on union resolution in `src/api/tests/test_role_endpoint_inventory.py`, post-rebase `#154` artifact updates, focused validation suite execution, and clean local commit.
* Evidence basis: C1, C2, C3, C4, C5, C6, C7
* Preconditions met: Remote ref `origin/feat/demo-164-chat-grounding-provenance-0900` fetched at `0c1fa1da4`; exact conflict boundary verified read-only via `git merge-tree`.
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                   |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                     |
| Lane evidence or inline fallback | inline: two-file rebase overlap inspected directly via read-only git and file views        |
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (C1–C7)                                                                              |
| Blockers                         | none                                                                                       |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `rpi-plan`                        |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (C1–C7)                                                                                                |
| Output mode and planning support | convergence; yes — unambiguous conflict boundary and validation command set                                  |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness Ready (passed); pre-transition state write (next) |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-research.md                |
| Notes for planning or re-entry   | Keep tracked `#154` files unmodified until `git rebase --continue` succeeds in `rpi-implement`.              |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All rebase overlap, conflict hunks, lint/type-check rules, and tracking artifact updates are verified from primary workspace evidence (`C1`–`C7`).

## Sources

No external sources used.
