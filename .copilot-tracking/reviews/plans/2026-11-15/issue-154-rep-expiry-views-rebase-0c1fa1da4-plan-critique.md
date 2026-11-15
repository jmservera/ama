<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #154 Rebase Continuation onto 0c1fa1da4

## Metadata

* Task ID: issue-154-rep-expiry-views-rebase-0c1fa1da4
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Rebase `feat/ux-154-rep-expiry-views` (`99a596629`, anchored on `02ab20cac`) onto newly merged parent tip `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, after PR #1761 `7f83f4749` and PR #1769 `0c1fa1da4`); resolve the sole merge conflict in `src/api/tests/test_role_endpoint_inventory.py` by preserving both `0c1fa1da4`'s handoff overdue/escalation entries (`/api/handoffs/unowned`, `/api/handoffs/escalated`, `/api/handoffs/escalate-overdue`) and `99a596629`'s representative view/session-expiry entries (`/api/cases/ZF-1/representative-view?representative_ref=SYN-REP`, `/api/cases/ZF-1/representative-view`, `"representative-view"`); update `#154` `.copilot-tracking/` changes and review artifacts with the rebased base (`0c1fa1da4`) and validation results; run focused `unittest`, `ruff`, `mypy`, and `tools/rename-zava-tests.py` checks; and commit locally with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing while leaving `git status --short` empty.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-research.md (`C1` through `C7`), .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan.md, .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-phase-details.md, .copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md, .copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md, .copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json, and src/api/tests/test_role_endpoint_inventory.py.
* Decisions, dependencies, and acceptance criteria considered: `FR-REB-01`, `FR-REB-02`, `NFR-REB-01`, `NFR-REB-02`, `AC1` through `AC4`, `Test Ownership and Change Budget Lock`, repository local noreply git configuration, non-amend commit guidance, preservation of original `#154` critique/review outcomes, and non-push dirty-tree constraints.
* Assessment boundary: Single-pass read-only credibility assessment across all supplied requirements, evidence log items (`C1` through `C7`), phases (`P01` through `P03`), tasks (`P01-T01` through `P03-T01`), acceptance criteria, and dependencies without open-ended codebase or git mutation.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Scope #1, `C1`, `C2`, `C5`, `P01`, `P01-T01` | Covered | Configures repository-local privacy-safe noreply email before `git rebase`, fetches `origin/feat/demo-164-chat-grounding-provenance-0900`, replays `99a596629` onto `0c1fa1da4` while keeping tracked `#154` files clean until `git rebase --continue` succeeds, and verifies `0c1fa1da4` ancestry and clean `server.py` auto-merge. |
| Caller Scope #2, `C3`, `C4`, `FR-REB-01`, `AC1`, `P01-T01` | Covered | Preserves `/api/handoffs/unowned` and `/api/handoffs/escalated` in `GET_ENDPOINTS`, `("/api/handoffs/escalate-overdue", {})` in `POST_ENDPOINTS`, `/api/cases/ZF-1/representative-view?representative_ref=SYN-REP` in `GET_ENDPOINTS`, `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})` in `POST_ENDPOINTS`, and `"representative-view"` in `test_inventory_covers_dynamic_case_actions_added_by_integration` inside src/api/tests/test_role_endpoint_inventory.py. |
| Caller Scope #3, `C7`, `FR-REB-02`, `AC3`, `P03`, `P03-T01` | Covered | Updates .copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md, .copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md, and .copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json after rebase completion to record `0c1fa1da4`, the rebased feature SHA, and post-rebase validation while repairing the verified missing JSON comma at line 35 of .copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json and preserving original `#154` review outcomes. |
| Caller Scope #4, `C6`, `NFR-REB-01`, `AC2`, `P02`, `P02-T01` | Covered | Executes caller-specified `unittest` (`test_role_endpoint_inventory.py`, `test_representative_expiry_api.py`, `test_resident_journey_design.py`), `src/core` (`ruff check`, `ruff format --check`, `mypy`), `src/api` (`ruff check`, `ruff format --check`, `mypy`), and `python3 tools/rename-zava-tests.py`. |
| Caller Scope #5, `C7`, `NFR-REB-02`, `AC4`, `P01-T01`, `P03-T01` | Covered | Uses `gh api user` privacy-safe `{id}+{login}@users.noreply.github.com` local config and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, avoids unrequested `git commit --amend` by placing post-rebase tracking artifacts in a clean commit after `rpi-review` state finalization, performs zero remote pushes, and verifies `git status --short` is empty at exit. |

## Verdict

* Verdict: Pass
* Rationale: Every caller requirement, research finding (`C1` through `C7`), conflict hunk in src/api/tests/test_role_endpoint_inventory.py, validation gate, and git/tracking sequencing rule is completely and accurately specified across .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan.md and .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-phase-details.md with zero substantive gaps or unresolved decisions.

## Findings

No actionable `PC-xxx` findings were identified within the supplied assessment boundary.

## Strengths and Residual Risk

* Pre-rebase `git merge-tree` verification (`C2` through `C5`) deterministically bounds the conflict surface to a single adjacency hunk across `GET_ENDPOINTS` and `POST_ENDPOINTS` in src/api/tests/test_role_endpoint_inventory.py and confirms disjoint auto-merge hunks in src/api/src/zava_forward/api/server.py.
* Deferring edits to tracked `#154` artifacts until after `GIT_EDITOR=true git rebase --continue` (`C7`, `P01` and `P03`) prevents dirty-worktree rebase failures while repairing the pre-existing JSON syntax error at line 35 of .copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json.
* Accepted residual risk 1: `P01-T01` fetches `origin/feat/demo-164-chat-grounding-provenance-0900` and rebases onto that ref expecting `0c1fa1da4`; `P01-T01` explicitly validates `git --no-pager log -n 2 --oneline` so any unexpected upstream movement beyond `0c1fa1da4` is immediately detected (and rebasing onto explicit commit `0c1fa1da4` remains directly available if the remote branch advances).
* Accepted residual risk 2: Because the final local tracking commit runs after `rpi-review` writes its review log and transitions the session state JSON to `Follow-up` (`P03` Context and Validation Expectations), `rpi-review` will observe uncommitted `.copilot-tracking/` updates in the working tree while the rebased code commit is already on `HEAD`; `P03` and `NFR-REB-02` explicitly document that `AC4`'s empty `git status --short` check applies after post-Review state persistence prior to final response.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique stayed strictly read-only within supplied artifacts and did not execute `git rebase` or run the post-rebase test suite, which belong to `P01` and `P02` during `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Mark .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan.md `Planning status` as `Ready`, record the `Pass` critique disposition, and hand off `P01` (`P01-T01`) to `rpi-implement` via the confirmed automatic `RPI Agent` parent.
* User response required: no
