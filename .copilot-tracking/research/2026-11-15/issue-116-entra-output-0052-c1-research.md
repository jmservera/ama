<!-- markdownlint-disable-file -->

# Task Research: issue-116-entra-output-0052-c1

| Field              | Value                                                                          |
|--------------------|--------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                     |
| Researcher / agent | rpi-research (via RPI Agent)                                                   |
| Status             | Complete                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-research.md |

## Research Brief

* What to research: Cycle 1 (`c1`) parent rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (after `PR #1761` merged) and root causes of the two hosted CI test failures on `PR #1766` (Issue #116, branch `feat/ai-116-entra-output-0052`):
  1. `src-api` `test_content_standard.py` (`CopyAudit.test_ai_label_is_exact_and_never_implies_approval`) failing on `src/core/src/zava_forward/core/data_protection.py:233`.
  2. `src-core` `test_human_review_effectiveness_223.py` (`HumanReviewEffectiveness223Tests.test_blank_worksheet_has_no_spoilers_and_human_sessions_pool_safely`) failing at line `401` (`AssertionError: 6 != 7`).
* Why it matters: `PR #1766` must rebase cleanly onto the updated parent branch (`feat/demo-164-chat-grounding-provenance-0900` at `7f83f4749`) preserving both `#164` and `#116` contracts while resolving both CI regressions without weakening role/field-level visibility rechecks on AI outputs or non-author review record views.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases of the automatic `c1` RPI loop for Issue #116 (`PR #1766`).
* Scope: Git ancestry `9a0dd54fa..origin/feat/demo-164-chat-grounding-provenance-0900` vs `9a0dd54fa..HEAD`, `src/api/src/zava_forward/api/server.py`, `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai_tasks.py`, `src/api/tests/test_content_standard.py`, `src/core/tests/test_human_review_effectiveness_223.py`, `src/core/tests/test_data_protection.py`, and `src/api/tests/test_ai_tasks.py`.
* Non-goals: Running `tools/rpi-checks.py --all`, Docker builds, pushing to remote (`coordinator` reviews and pushes), or altering unrelated modules.
* Criteria: Clean rebase preserving `#164` (`chat_evaluation` reporting and multi-turn chat eval) and `#116` (`s.ai_live_report(u)`, output visibility rechecks, document derivative/necessity hold); zero `human-approved` violations in `test_content_standard.py`; `test_human_review_effectiveness_223.py` passing (`7 == 7`) while non-author review viewers still receive `projection.NOTE_HELD` redaction; `mypy`, `ruff check`, `ruff format --line-length 100 --check`, and `rename-zava-tests.py` passing.
* Requested outputs: Verified `C#` evidence log, overlap analysis for parent rebase, root-cause verification for both CI failures, evaluated alternatives, convergence selection, and planning readiness.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                               |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1: What commits and file hunks diverge between `HEAD` (`09416f614`) and `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`)? Q2: Why does `test_content_standard.py` fail on `data_protection.py:233`? Q3: Why does `test_human_review_effectiveness_223.py:401` report `6 != 7`, and how should `_record_view` preserve author-owned review text without leaking to non-authors or leaking AI outputs? |
| Codebase scope                   | `src/core/`, `src/api/`, `src/agents/`                                                                                              |
| External scope                   | none                                                                                                                                |
| Initial internal candidate areas | `src/core/src/zava_forward/core/data_protection.py`, `ai_tasks.py`, `human_review_effectiveness.py`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_ai_tasks.py`, `src/core/tests/test_human_review_effectiveness_223.py` |
| Initial external candidate areas | none                                                                                                                                |
| Research posture                 | focused                                                                                                                             |
| Posture provenance               | caller-supplied failure targets and rebase target (`PR #1766` Cycle 1 CI fix + parent rebase)                                       |
| Explicit limits / deadline       | Focused validation tier (`unittest`, `mypy`, `ruff`, `rename-zava-tests.py`); do not push                                           |
| Posture-specific completion basis | focused scope coverage with direct local reproduction of both CI failures and diff inspection of parent branch                       |
| Edits allowed during research?   | no, research-only                                                                                                                   |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Keep line lengths <= 100 chars for `ruff format --check`; preserve both `#164` and `#116` invariants; leave frozen clean commit     |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                                             | Scoped authority or output contract                                                   | Selected / skipped reason                                                       |
|---------------------|-----------------------------------|------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches all repository files and tracking outputs | Enforces content standard, focused validation tier, privacy-safe git author, no push  | Selected: mandatory repository governance                                       |
| Research specialist | `hve-core-all:rpi-researcher`     | Registered subagent for independent research lanes               | Bounded subagent lane artifact                                                        | Skipped (inline preferred): 4-file root-cause trace fits direct inline inspection |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered  | Resulting decision or selected further research                                                                 |
|------------------|-------------------------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with exact rebase branch, exact CI failure locations, and validation commands | N/A (non-interactive) | Execute `focused` convergence research inline in `/home/azureuser/source/ama-demo-wt/feat-116-entra-output-0052` |
| Convergence      | All 3 waves completed with local test reproduction confirming exact failure lines                     | N/A (non-interactive) | Converged on clean rebase resolution + docstring replacement + `is_author` guard in `ai_tasks._record_view`      |

## Scope and Success Criteria

* Scope: Parent diff (`9a0dd54fa..origin/feat/demo-164-chat-grounding-provenance-0900`), Cycle 0 commit (`09416f614`), and the two failing unit tests in `src/api/tests/test_content_standard.py` and `src/core/tests/test_human_review_effectiveness_223.py`.
* Assumptions:
  * Actual checked-out branch name in `/home/azureuser/source/ama-demo-wt/feat-116-entra-output-0052` is `feat/ai-116-entra-output-0052` (matching Cycle 0 state `.copilot-tracking/rpi-sessions/2026-11-15/issue-116-entra-output-0052-state.json`). Verified via `git branch --show-current`.
* Success criteria:
  * Exact overlapping files and hunks for the rebase are identified (`C1`, `C2`).
  * Exact root causes of both CI failures are reproduced and traced (`C3`-`C6`).
  * Contrarian checks verify line-length formatting (`<= 100`), non-author redaction preservation, and absence of any other `"human-approved"` occurrences (`C3`, `C7`).

## Task Research Requests

* Explicit requests:
  1. Rebase current branch onto `origin/feat/demo-164-chat-grounding-provenance-0900` preserving both `#164` and `#116` changes.
  2. Replace forbidden `'human-approved'` with `'human-authorized'` in `src/core/src/zava_forward/core/data_protection.py:233` (`"""Verify whether a human-authorized text-only derivative may be sent to an external model."""`).
  3. Update `_record_view(store, user, rec)` in `src/core/src/zava_forward/core/ai_tasks.py` so when `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))`, the reviewer's own `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` are not replaced with `projection.NOTE_HELD`, while keeping `withheld` checks on `ai_output`, `shown_output`, `citations`, `unresolved`, and `review_evidence["compared"]`, and keeping `not reason_ok` / `withheld` redaction for non-author viewers.
* Inferred research questions:
  * Q1: Which files modified in `9a0dd54fa..origin/feat/demo-164-chat-grounding-provenance-0900` overlap with `9a0dd54fa..HEAD` (`09416f614`), and what is the exact combined hunk?
  * Q2: Are there any other occurrences of `"human-approved"` in `src/core` or `src/api` Python sources, and does the replacement docstring satisfy `ruff format --line-length 100 --check`?
  * Q3: Why did `test_human_review_effectiveness_223.py:401` drop from `7` detected defects to `6`, and does `Store._rec_view` or any other helper share the same bug?

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Focused validation tier only; no Docker / full `rpi-checks.py --all` gate; no `git push`                | Caller intake       | Restricts implementation and verification to targeted unit suites, mypy, and ruff  |

## Research Questions

|  # | Sub-question                                                                                                                     | Type            | Priority | Status   |
|---:|----------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What commits and hunks diverge between `09416f614` and `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`)?      | breadth         | H        | answered |
| Q2 | Why does `test_content_standard.py` fail on `data_protection.py:233`, and are any other files or line-length rules affected?     | straightforward | H        | answered |
| Q3 | Why does `test_human_review_effectiveness_223.py:401` fail (`6 != 7`), and how does `is_author` in `_record_view` preserve security? | depth/contrarian| H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-research.md`, `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-changes.md`, `.copilot-tracking/rpi-sessions/2026-11-15/issue-116-entra-output-0052-state.json`.
* Reused (verified) findings: Cycle 0 commit `09416f614` sits directly on `9a0dd54fa` in branch `feat/ai-116-entra-output-0052`.
* New context verified: `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by two commits (`02ab20cac` `#1753` and `7f83f4749` `#1761`).

## Executed Research Cycles

### Cycle 1

* **Wave 1 (Wider — inline)**:
  * Inspected `git log` and `git diff --name-status` across `9a0dd54fa..origin/feat/demo-164-chat-grounding-provenance-0900` and `9a0dd54fa..HEAD` (`C1`, `C2`). Confirmed only two non-tracking files appear in both diffs: `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_ai_tasks.py`. Notice `src/core/src/zava_forward/core/ai_tasks.py` was not modified on the parent branch, while `src/core/src/zava_forward/core/ai_eval.py` was newly added on the parent branch (`7f83f4749`) and does not collide with `src/agents/src/zava_forward/agents/ai_eval.py`.
  * Ran `test_content_standard.py` and `test_human_review_effectiveness_223.py` locally (`PYTHONPATH=src/core/src:src/core/tests:src/api/src:src/api/tests:src/agents/src`), reproducing the exact two CI failures (`2` failures out of `35` tests).
* **Wave 2 (Deeper — inline)**:
  * Inspected the overlapping hunk in `src/api/src/zava_forward/api/server.py:904-937` (`C1`): `#1761` imported `chat_eval` alongside `ai_eval` and added `"chat_evaluation": chat_eval.run_eval()` to `/api/ai/report`, keeping `"live": s.ai_live_report()`, whereas `#116` (`09416f614`) updated `"live": s.ai_live_report(u)` to enforce caller `can_see_reason` projection. Combining both yields `"evaluation": ai_eval.run_eval(), "chat_evaluation": chat_eval.run_eval(), "live": s.ai_live_report(u), "registry": ai_registry.registry(), "consumption": consumption`.
  * Inspected `src/api/tests/test_ai_tasks.py` (`C2`): `#1761` inserted two `Endpoints` tests at baseline line `681` (`test_report_separates_chat_multi_turn_evaluation_from_single_turn_evaluation` and `test_report_chat_failure_does_not_alter_single_turn_results_and_live_stays_disabled`), while `#116` added tests at the end of `TaskTests` and at the end of `Endpoints`.
  * Traced Failure 1 (`C3`, `C4`): `CopyAudit.test_ai_label_is_exact_and_never_implies_approval` (`src/api/tests/test_content_standard.py:159-166`) asserts `"human-approved"` does not appear in any `.py` file under `src/api/src/zava_forward/api` or `src/core/src/zava_forward/core` (except `"human-approved by"`). Repository-wide `grep` confirmed `src/core/src/zava_forward/core/data_protection.py:233` is the sole matching Python line (`"""Validate a bounded, human-approved scoped necessity exception for document AI processing."""`).
  * Traced Failure 2 (`C5`, `C6`): In `test_human_review_effectiveness_223.py:368-404`, `sub_two` (`Liam Brooks`, role `Retrofit Coordinator`) edits hedged scenario `S-223-05` (`human_review_effectiveness.py:295-327`), whose `competent_text` includes `"BSL interpreter and written confirmation"` (`ZF-223-B` `resident.adjustment`). Because `Retrofit Coordinator` is in `RESIDENT_VIEW_ROLES` (`controls.py:15`) rather than `DEFAULT_REASON_ROLES` (`projection.py:34-39`), `reason_ok` is `False` and `withheld` includes `resident.adjustment`. Inside `ai_tasks._record_view` (`ai_tasks.py:262-308`), returned by `ai_tasks.review` (`ai_tasks.py:550`), `out["override_text"]`, `out["reviewer_reason"]`, and `out["review_evidence"]["reason"]` were overwritten with `projection.NOTE_HELD`, causing `score_human_session` to evaluate `projection.NOTE_HELD` instead of the reviewer's authored edit and miss the `1` defect detected by `sub_two` (`6 != 7`).
* **Wave 3 (Contrarian — inline)**:
  * Checked whether naive replacement `"human-authorized"` inside the old sentence (`    """Validate a bounded, human-authorized scoped necessity exception for document AI processing."""`) would exceed `ruff format --line-length 100 --check`: confirmed it is `101` characters (`> 100`)! Using the caller-specified docstring `    """Verify whether a human-authorized text-only derivative may be sent to an external model."""` is `98` characters (`<= 100`), avoids `"human-approved"` and all `BANNED` web words, and passes both `test_content_standard.py` and `ruff format --line-length 100 --check`.
  * Checked whether skipping `override_text` / `reviewer_reason` / `reason` / `review_evidence["reason"]` redaction when `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))` could leak unauthorized fields across users or leak model-echoed data to the author (`C5`, `C7`):
    1. Only the author (`user["email"] == rec["resolved_by"]`) sees the unredacted fields they just submitted themselves; any other viewer (`non_author["email"] != rec["resolved_by"]`) continues to hit `not is_author` and receives `projection.NOTE_HELD` whenever `projection.contains_withheld_value(out["override_text"], withheld)` is true or `not reason_ok`.
    2. Even for `is_author`, `ai_output`, `shown_output`, `citations`, `unresolved`, and `review_evidence["compared"]` still enforce `FORBIDDEN` and `withheld` checks unconditionally, and `ai_tasks.live_report` (`ai_tasks.py:553-585`) still enforces `can_see_reason(user)` independently across aggregated records.
    3. Checked `Store._rec_view` (`store.py:1546-1595`): `_rec_view` projects `priority` records (which have per-item `reason` and `cites`, not reviewer `override_text` or `resolved_by` edit text), so no regression exists there (`C7`).
* **Re-entry decision**: Complete; no unresolved questions or missing evidence remain.

## Evidence Log

| ID  | Path and lines                                                                 | Verified finding                                                                                                                                            |
|-----|--------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/api/src/zava_forward/api/server.py:904-937`                               | Parent `#1761` added `chat_eval` import and `"chat_evaluation": chat_eval.run_eval()` in `/api/ai/report`; `#116` changed `"live": s.ai_live_report(u)`.   |
| C2  | `src/api/tests/test_ai_tasks.py:681-745, 1180-1285`                            | Parent `#1761` added two chat-report tests in `Endpoints`; `#116` added role-recheck tests at separate offsets.                                            |
| C3  | `src/core/src/zava_forward/core/data_protection.py:224-236`                    | Line `233` docstring contains `"human-approved"`, the only disallowed occurrence across `src/core` and `src/api` Python modules.                            |
| C4  | `src/api/tests/test_content_standard.py:159-167`                               | `test_ai_label_is_exact_and_never_implies_approval` rejects `"human-approved"` (unless `"human-approved by"`) in all `core/*.py` and `api/*.py` files.      |
| C5  | `src/core/src/zava_forward/core/ai_tasks.py:262-308, 506-551`                  | `_record_view` unconditionally redacts `override_text` on `withheld` and `reason` / `reviewer_reason` / `review_evidence["reason"]` on `not reason_ok`, even when `user` is `rec["resolved_by"]`. |
| C6  | `src/core/tests/test_human_review_effectiveness_223.py:368-404` and `src/core/src/zava_forward/core/human_review_effectiveness.py:295-327, 995-1035` | `Liam Brooks` (`Retrofit Coordinator`, `reason_ok=False`) edits `S-223-05`; `_record_view` overwrote his own `override_text` / `reviewer_reason` with `NOTE_HELD`, causing `6 != 7`. |
| C7  | `src/core/src/zava_forward/core/store.py:1546-1595`                            | `Store._rec_view` projects `priority` ranking rows rather than reviewer `override_text`/`reviewer_reason` fields and requires no change.                    |

## Synthesized Findings

* **Q1 (Parent rebase resolution)**: Rebasing `feat/ai-116-entra-output-0052` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) picks up `#1753` (`02ab20cac`) and `#1761` (`7f83f4749`). Only `src/api/src/zava_forward/api/server.py` has a direct line conflict on `/api/ai/report`, resolved by keeping both `"chat_evaluation": chat_eval.run_eval()` and `"live": s.ai_live_report(u)` (`C1`). Any hunk adjacency in `src/api/tests/test_ai_tasks.py` preserves both `#164` and `#116` tests (`C2`).
* **Q2 (Content standard fix)**: Replacing line `233` of `src/core/src/zava_forward/core/data_protection.py` with `"""Verify whether a human-authorized text-only derivative may be sent to an external model."""` removes the forbidden `'human-approved'` phrase (`C3`, `C4`) and stays at `98` columns (`<= 100` for `ruff format --check`).
* **Q3 (Author-scoped review record projection)**: In `src/core/src/zava_forward/core/ai_tasks.py`, computing `is_author = bool(user.get("email") and rec.get("resolved_by") == user.get("email"))` inside `_record_view(store, user, rec)` and gating the `override_text`, `reason`, `reviewer_reason`, and `review_evidence["reason"]` `NOTE_HELD` replacements with `not is_author` restores `7 == 7` in `test_human_review_effectiveness_223.py` while keeping `withheld`/`FORBIDDEN` redaction on `ai_output`, `shown_output`, `citations`, `unresolved`, and `review_evidence["compared"]` for all callers and full redaction on `override_text`, `reason`, `reviewer_reason`, and `review_evidence["reason"]` for non-author callers (`C5`, `C6`).

## Alternatives Considered

| Option | Description | Pros | Cons | Disposition |
|--------|-------------|------|------|-------------|
| Option A: Grant `Retrofit Coordinator` `DEFAULT_REASON_ROLES` visibility | Add `Retrofit Coordinator` to `projection.DEFAULT_REASON_ROLES` | Would make `reason_ok=True` for Liam Brooks | Violates `projection.py` role matrix, breaks existing role visibility contracts (`test_role_endpoint_inventory.py`, `test_ai_tasks.py`), and widens sensitive data access | Rejected |
| Option B: Return raw unprojected `rec` from `ai_tasks.review` | Bypass `_record_view` on `review()` return | Fixes `score_human_session` | Fails to filter `ai_output`, `shown_output`, `citations`, `unresolved`, and `review_evidence["compared"]` if the stored AI draft contained withheld values | Rejected (`C5`) |
| Option C: Keep `_record_view` and preserve only reviewer-authored fields (`override_text`, `reviewer_reason`, `reason`, `review_evidence["reason"]`) when `is_author` is true, plus replace `'human-approved'` in `data_protection.py:233` and rebase onto parent | Surgical `is_author` check inside `_record_view` + exact docstring update + clean rebase | Preserves full `withheld`/`FORBIDDEN` checks on AI/workflow fields for all viewers, preserves `NOTE_HELD` redaction of reviewer fields for non-author viewers, fixes both CI failures, and keeps `ruff`/`mypy` clean | Requires focused unit test covering both author and non-author `_record_view` calls | **Selected** (`C1`-`C7`) |

## Decisions, Risks, and Readiness

* **Current confirmed decisions**:
  * Converge on Option C: rebase `feat/ai-116-entra-output-0052` onto `origin/feat/demo-164-chat-grounding-provenance-0900`, resolve `/api/ai/report` in `server.py` (and any `test_ai_tasks.py` conflict) preserving both `#164` and `#116`, update `data_protection.py:233` docstring, add `is_author` guard in `ai_tasks._record_view`, and add a focused unit test in `src/api/tests/test_ai_tasks.py` covering author vs non-author `_record_view` projection.
* **Key risks & mitigations**:
  * *Line-length formatting in `src/core` and `src/api`*: Verify `(cd src/core && ruff format --isolated --line-length 100 --check src tests)` and `(cd src/api && ruff format --isolated --line-length 100 --check src tests)` explicitly.
  * *Post-rebase interaction with `#164` chat evaluation*: Run `test_ai_tasks.py` (which exercises `/api/ai/report` including `chat_evaluation` and `ai_live_report(u)`) after rebase.
* **Potential further research**: None required for `c1`.
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`

## Artifact Self-Check

* [x] Research brief, scope, non-goals, posture (`focused`), and extension provenance recorded.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order before convergence synthesis.
* [x] Every material claim maps to stable `C1`-`C7` codebase `path:line` evidence.
* [x] Alternatives evaluated and Option C selected with evidence-based rationale.
* [x] Research remained strictly read-only on source files; `Planning Readiness: Ready` recorded.
