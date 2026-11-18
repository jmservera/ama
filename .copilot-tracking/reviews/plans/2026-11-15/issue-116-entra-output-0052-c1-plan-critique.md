<!-- markdownlint-disable-file -->
# RPI Plan Critique: Cycle 1 (`c1`) Parent Rebase and CI Fixes for PR #1766 / Issue #116

## Metadata

* Task ID: issue-116-entra-output-0052-c1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Cycle 1 (`c1`) of Issue #116 (`PR #1766`, branch `feat/ai-116-entra-output-0052` at `09416f614` before rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` at `7f83f4749`). Confirmed caller requirements: (1) run `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, resolving overlap cleanly while preserving `#164` and `#116` changes; (2) replace `'human-approved'` with `'human-authorized'` in `src/core/src/zava_forward/core/data_protection.py:233` (`"""Verify whether a human-authorized text-only derivative may be sent to an external model."""`); (3) in `src/core/src/zava_forward/core/ai_tasks.py` inside `_record_view(store, user, rec)`, preserve the reviewer's own `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` when `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))`, while keeping `withheld` checks on `ai_output`, `shown_output`, `citations`, `unresolved`, and `review_evidence["compared"]` and keeping `not reason_ok` / `withheld` redaction for non-author viewers; (4) validate locally at Focused tier (`unittest`, `mypy`, `ruff check`, `ruff format --line-length 100 --check`, `python3 tools/rename-zava-tests.py`), record `c1` RPI artifacts, and create a clean local commit without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-research.md, .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md, .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md, .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-changes.md, .github/workflows/src-ci.yml, src/core/pyproject.toml, src/api/pyproject.toml, src/api/src/zava_forward/api/server.py, src/core/src/zava_forward/core/data_protection.py, src/core/src/zava_forward/core/ai_tasks.py, src/core/src/zava_forward/core/projection.py, src/core/src/zava_forward/core/continuity.py, src/api/tests/test_content_standard.py, src/core/tests/test_human_review_effectiveness_223.py, src/api/tests/test_ai_tasks.py, src/api/tests/test_ai_consumption_api.py, and read-only git inspection against `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`).
* Decisions, dependencies, and acceptance criteria considered: Option C convergence (surgical `is_author` check in `_record_view`, 98-column `human-authorized` docstring in `data_protection.py:233`, parent rebase onto `7f83f4749`), Focused validation tier without Docker or `tools/rpi-checks.py --all`, test-bounds lock (`0` removals, maximum `1` new test method in `src/api/tests/test_ai_tasks.py`), privacy-safe local commit with Copilot trailer, and no `git push`.
* Assessment boundary: Evaluates plan and phase-detail credibility, conflict completeness, security/projection invariants, and local command executability against current repository files and git ancestry (`9a0dd54fa..09416f614` vs `9a0dd54fa..7f83f4749`). Does not execute a live rebase, mutate working files, or verify hosted GitHub Actions execution or external organisational governance items (`OD-14`, `OD-19`, live Entra B2B tenant settings).

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern                                                                                                                                                     |
|------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-1, C1, C2, P01, P01-T01               | Partial  | Covers `server.py` `/api/ai/report` merge, but omits `git fetch origin` in `P01-T01` and understates a guaranteed rebase conflict in `src/api/tests/test_ai_tasks.py` (`PC-003`). |
| FR-2, C3, C4, P02, P02-T01               | Covered  | Exact 98-character docstring at `src/core/src/zava_forward/core/data_protection.py:233` removes the sole disallowed `"human-approved"` token and stays within 100 columns. |
| FR-3, C5, C6, C7, P02, P02-T01           | Partial  | Preserves author fields via `is_author` and fixes `test_human_review_effectiveness_223.py`, but omits `withheld` checks on non-author reason fields when `reason_ok=True` and on top-level `workflow_output` (`PC-002`). |
| NFR-1, P03, P03-T01                      | Partial  | Package-wide `ruff ... --isolated src tests` and bare `mypy` without editable package installs fail on the current worktree (`PC-001`); `TaskTests` class name does not exist and `#164` parent regression suites are omitted (`PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: Core root-cause fixes for both `PR #1766` CI failures (`FR-2` docstring replacement and `FR-3` `is_author` scoping) and the `/api/ai/report` conflict design are sound, but three direct planner corrections are needed before implementation: `NFR-1` and `P03` specify `ruff --isolated src tests` and unprovisioned `mypy` invocations that currently fail on valid repository code (`PC-001`), `P02-T01` omits `withheld`-value redaction on non-author reason fields when `reason_ok=True` (`PC-002`), and `P01-T01` / `P03-T01` miss `git fetch origin`, a guaranteed hunk conflict and the actual `TasksMixin` class name in `src/api/tests/test_ai_tasks.py`, and post-rebase `#164` verification suites (`PC-003`).

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `NFR-1` and `P03` specify `ruff --isolated src tests` and unprovisioned `mypy` commands that fail in this worktree

* Related IDs: NFR-1, P03, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md (`NFR-1`, `Dependencies`), .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md (`P03`, `P03-T01`), src/core/pyproject.toml, src/api/pyproject.toml, src/api/tests/test_ai_consumption_api.py, .github/workflows/src-ci.yml
* Concern: Two validation assumptions in `NFR-1` and `P03` are false in `/home/azureuser/source/ama-demo-wt/feat-116-entra-output-0052`. First, `NFR-1` and `P03` mandate `ruff check --isolated src tests && ruff format --isolated --line-length 100 --check src tests` in `src/core` and `src/api`; `--isolated` forces Ruff to ignore `pyproject.toml` (`[tool.ruff.lint.per-file-ignores]` and `[tool.ruff.format].exclude` for migrated `v0.21.0` modules including `ai_tasks.py`, `server.py`, `test_ai_tasks.py`, and `aftercare.py`), producing thousands of pre-existing lint and formatting errors (`>3 MB` output) whereas Caller Requirement #4 and `.github/workflows/src-ci.yml` use project configuration (`ruff check . && ruff format --line-length 100 --check .`, which passes cleanly across all `281` `src/core` and `196` `src/api` files). Second, `Dependencies` assumes `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api` are already editable-installed in the active Python environment, but no `.venv` exists in this worktree and `/usr/bin/python3` has no `zava_forward` distributions installed, causing `(cd src/api && mypy)` to fail with `4` errors on `src/api/tests/test_ai_consumption_api.py:24-25` (`import-not-found` and `unused-ignore` on `# type: ignore[import-untyped]` imports from `zava_forward.agents`).
* Impact: Implementation will hit false-positive validation failures on `P03` `ruff` and `src/api` `mypy` commands as written, or risk creating an untracked/ignored worktree `.venv` without cleanup.
* Smallest useful change: Revise `NFR-1` and `Dependencies` in `.copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md` and `P03` / `P03-T01` in `.copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md` to (1) provision an external session-workspace virtualenv (under `/home/azureuser/.copilot/session-state/a11ca27c-12dd-430f-ae05-7850842d627c/files/venv` with `--system-site-packages`, never `/tmp`) and install `-e src/core -e src/agents -e src/api` (`--no-deps --no-build-isolation`) before running `<venv>/bin/python -m mypy` and `<venv>/bin/python -m unittest`, and (2) replace package-wide `--isolated src tests` Ruff invocations with `ruff check . && ruff format --line-length 100 --check .` (plus optional targeted `ruff format --isolated --line-length 100 --check src/zava_forward/core/data_protection.py`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `NFR-1`, `Dependencies`, `P03`, and `P03-T01` text specifying editable distribution setup in an external session-workspace venv and `pyproject.toml`-respecting `ruff check . && ruff format --line-length 100 --check .` commands.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: `P02-T01` omits `withheld`-value redaction on non-author reason fields when `reason_ok` is `True` and on top-level `workflow_output`

* Related IDs: FR-3, P02, P02-T01, P03-T01, C5
* Evidence: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md (`FR-3`), .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md (`P02-T01`), src/core/src/zava_forward/core/ai_tasks.py (`_record_view` lines `262-308`, `live_report` lines `575-583`), src/core/src/zava_forward/core/projection.py (`DEFAULT_REASON_ROLES`, `RESIDENT_VIEW_ROLES`, `FINANCE_VIEW`)
* Concern: Caller Requirement #3 states `"keep not reason_ok / withheld redaction for non-author viewers"`, yet `P02-T01` specifies redacting `reason`, `reviewer_reason`, and `review_evidence["reason"]` only when `not is_author and not reason_ok`. Roles in `DEFAULT_REASON_ROLES` (`reason_ok=True`) can still lack `FINANCE_VIEW` or `RESIDENT_VIEW_ROLES` (for example `Building Safety Liaison` lacks both `FINANCE_VIEW` and `RESIDENT_VIEW_ROLES`; `Resident Liaison Officer` lacks `FINANCE_VIEW`). Unlike `ai_tasks.live_report` (`src/core/src/zava_forward/core/ai_tasks.py:577-583`), which checks both `not reason_ok` and `projection.contains_withheld_value(raw_reason, withheld)`, `P02-T01` omits `projection.contains_withheld_value(..., withheld)` on those three reason fields for non-author viewers and checks `review_evidence["compared"]["workflow"]` against `withheld` without checking top-level `out.get("workflow_output")`.
* Impact: A non-author viewer with `reason_ok=True` who lacks finance or resident-authority visibility could read withheld strings embedded in another reviewer's `reason`, `reviewer_reason`, or `review_evidence["reason"]`, or in top-level `workflow_output`, via `_record_view`.
* Smallest useful change: Update `FR-3` in `.copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md` and `P02-T01` / `P03-T01` in `.copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md` so that when `not is_author`, `reason`, `reviewer_reason`, and `review_evidence["reason"]` are replaced with `projection.NOTE_HELD` whenever `not reason_ok or projection.contains_withheld_value(val, withheld)` (matching `ai_tasks.live_report`), and `workflow_output` is checked alongside `shown_output` against `withheld` unconditionally while preserving all four reviewer-authored fields unredacted when `is_author` is `True`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-3`, `P02-T01`, and `P03-T01` specifications incorporating `not reason_ok or projection.contains_withheld_value(..., withheld)` for non-author reason fields and unconditional `withheld` checking on `workflow_output`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P01-T01` and `P03-T01` miss `git fetch origin`, a guaranteed conflict and the `TasksMixin` class name in `src/api/tests/test_ai_tasks.py`, and `#164` parent regression checks

* Related IDs: FR-1, P01, P01-T01, P03, P03-T01, C1, C2
* Evidence: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md (`P01`, `P01-T01`, `P03`, `P03-T01`), .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-research.md (`C1`, `C2`), src/api/tests/test_ai_tasks.py (`class TasksMixin` line `25`, `Endpoints.test_mode_flag_and_review_over_http` lines `1081-1099`), src/api/tests/test_ai_consumption_api.py, src/core/tests/test_ai_eval.py, src/agents/tests/test_chat_heldout.py
* Concern: Three execution details across `P01` and `P03` diverge from actual git ancestry and file symbols: (1) `P01-T01` omits `git fetch origin` before `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` despite Caller Requirement #1 (`git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`), and describes `src/api/tests/test_ai_tasks.py` as only a conditional adjacent hunk even though `09416f614` (`@@ -679,14 +1079,205 @@`) reformatted lines `679-692` directly across `7f83f4749`'s `@@ -681,6 +681,66 @@` insertion before `Endpoints.test_mode_flag_and_review_over_http`, guaranteeing a rebase conflict in both `server.py` and `test_ai_tasks.py`; (2) `P01` and `P03` reference `TaskTests` in `src/api/tests/test_ai_tasks.py`, which does not exist (`TasksMixin` at line `25` is the shared mixin inherited by `JsonTasks` and `SqlTasks`); and (3) `P03` Focused validation omits parent `#1761`'s `#164` regression suites (`src/core/tests/test_ai_eval.py`, `src/agents/tests/test_ai_eval.py`, `src/agents/tests/test_chat_heldout.py`, `/api/ai/report` key-set checks in `src/api/tests/test_ai_consumption_api.py`, and `src/agents` `mypy` / `ruff`), which directly exercise `#116`-modified `ChatIsolation`, `ChatPanel`, `chatthreads.py`, `agents/ai_eval.py`, and `/api/ai/report` in hosted `src-ci.yml`.
* Impact: Implementers following `P01-T01` and `P03-T01` literally will skip `git fetch origin`, target a nonexistent `TaskTests` class, encounter an unplanned conflict hunk in `src/api/tests/test_ai_tasks.py`, and leave the newly rebased `#164` + `#116` multi-turn chat evaluation and `src/agents` checks unverified before commit.
* Smallest useful change: Update `P01-T01`, `P03`, and `P03-T01` in `.copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md` (and `P03-T01` in `.copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md`) to: (1) execute `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900` and explicitly resolve conflicts in both `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_ai_tasks.py` (`Endpoints` immediately before `test_mode_flag_and_review_over_http`), (2) add the `1` focused `_record_view` author/non-author regression test method on `TasksMixin` in `src/api/tests/test_ai_tasks.py` so it runs across both `JsonTasks` and `SqlTasks`, and (3) include `src/core/tests/test_ai_eval.py`, `src/agents/tests/test_ai_eval.py`, `src/agents/tests/test_chat_heldout.py`, `src/api/tests/test_ai_consumption_api.py` (at least its `/api/ai/report` coverage), and `src/agents` `mypy`/`ruff` in `P03` Focused validation.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01`, `P03`, and `P03-T01` plan/detail sections specifying `git fetch origin`, deterministic conflict resolution in `src/api/tests/test_ai_tasks.py`, `TasksMixin` as the target class, and post-rebase `#164` + `src/agents` Focused checks.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strengths:
  * Exact reproduction and root-cause isolation of both `PR #1766` hosted CI failures (`data_protection.py:233` content-standard check and `ai_tasks._record_view` self-redaction in `test_human_review_effectiveness_223.py:401`).
  * Good contrarian line-length check verifying that the caller-specified 98-character docstring in `src/core/src/zava_forward/core/data_protection.py:233` avoids a 101-column `ruff format --check` regression.
  * Clean rebase safeguard using the session-state `files/` directory rather than `/tmp` while backing up untracked `c1` `.copilot-tracking/` artifacts before `git rebase`, plus verified repository-local privacy-safe `git config --local user.email` (`8036360+jmservera@users.noreply.github.com`).
  * Read-only cross-check of `7f83f4749:src/core/src/zava_forward/core/ai_eval.py` confirms `#116`'s `ChatIsolation` / `ChatPanel` / `chatthreads` updates preserve `ChatForbidden` ordering on mid-thread role revocation and leave all six frozen `chat_bindings` digests unchanged.
* Residual risks (accepted under caller scope):
  * Focused-tier local validation intentionally excludes Docker image builds, Trivy scans, Playwright browser checks, and `tools/rpi-checks.py --all`, which remain covered by hosted CI and coordinator review after push.
  * Duplication across `ai_tasks._record_view`, `Store._rec_view`, and `ChatIsolation.scrub_thread` (`RV-001`) and external governance items (`OD-14`, `OD-19`, live Entra B2B tenant configuration) remain tracked follow-ups outside `c1`.

## Questions or Blocking Evidence Gaps

* None. All three findings (`PC-001`..`PC-003`) are direct planner corrections resolved by existing repository and caller evidence without user input.

## Limitations

* Critique executed strictly read-only against `HEAD` (`09416f614`) and `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) without running `git rebase` or modifying repository files; post-rebase behavior of `#164` suites was verified statically from commit diffs and must be executed during `P03` after rebase.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `NFR-1` / `Dependencies` / `FR-3` / `P03-T01` in `.copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md` and `P01-T01` / `P02-T01` / `P03` / `P03-T01` in `.copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md` to resolve `PC-001`, `PC-002`, and `PC-003`, mark the plan ready without re-running `rpi-plan-critique`, and proceed to `rpi-implement`.
* User response required: No
