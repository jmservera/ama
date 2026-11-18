<!-- markdownlint-disable-file -->
# Review: Cycle 1 (`c1`) Parent Rebase and CI Fixes for PR #1766 / Issue #116

## Scope and Evidence

* Task ID: issue-116-entra-output-0052-c1
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Rebase of `feat/ai-116-entra-output-0052` onto `origin/feat/demo-164-chat-grounding-provenance-0900` at `7f83f4749` (following `PR #1761`), content-standard docstring fix in `src/core/src/zava_forward/core/data_protection.py`, reviewer-author projection fix in `src/core/src/zava_forward/core/ai_tasks.py` (`_record_view`), focused `TasksMixin` regression coverage in `src/api/tests/test_ai_tasks.py`, and Focused-tier local validation (`unittest`, `mypy`, `ruff`, `tools/rename-zava-tests.py`). Excludes Docker image builds, `tools/rpi-checks.py --all`, `git push`, and external tenant governance.
* Plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-c1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-research.md, git diff and ancestry inspection (`7f83f4749..HEAD`), `src/api/src/zava_forward/api/server.py`, `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai_tasks.py`, `src/api/tests/test_ai_tasks.py`, and Focused-tier validation execution outputs.

## Opening Review State

* Interpreted review goal: Verify once with read-only discipline that Cycle 1 (`c1`) satisfies all functional and non-functional requirements (`FR-1`..`FR-3`, `NFR-1`), acceptance criteria, test-bounds locks, and single-pass critique dispositions (`PC-001`..`PC-003`) without weakening role or field-level visibility controls.
* Review scope: Full task (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Evidence readiness: Ready; plan, phase details, plan critique, changes record, research artifact, rebased commit `7b882614d`, and Focused validation outputs are complete and reconciled.
* Acceptance basis: Caller requirements #1-#4, `FR-1`..`FR-3`, `NFR-1`, test-bounds lock (`0` removals, `1` focused method added on `TasksMixin`), and critique dispositions `PC-001`..`PC-003`.
* First comparison boundary: Compare reconciled `P01`-`P03` markers and source diffs against `7f83f4749` (`PR #1761`) and verify non-regression of `#164` and `#116` invariants.
* Active read-only boundaries: Write authority restricted strictly to `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md`; no source, test, plan, details, critique, research, or changes edits during Review.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full single-pass review on 2026-11-15 across all reconciled `c1` tracking artifacts, git commit ancestry (`7f83f4749..HEAD`), changed source/test files (`server.py`, `data_protection.py`, `ai_tasks.py`, `test_ai_tasks.py`), and Focused-tier validation outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Parent Branch Rebase and `/api/ai/report` Conflict Resolution | Reconciled | Checked off in plan and marked `Complete` in phase details; rebased `c0` commit `7b882614d` sits directly atop `7f83f4749` (`PR #1761`) with both `"chat_evaluation": chat_eval.run_eval()` and `"live": s.ai_live_report(u)` preserved in `server.py`. |
| `P02` / `P02-T01` | Content Standard Docstring Fix and Reviewer-Author `_record_view` Projection Fix | Reconciled | Checked off in plan and marked `Complete` in phase details; `data_protection.py` uses the exact 98-column `human-authorized` docstring and `ai_tasks._record_view` scopes author retention via `is_author` while keeping unconditional `withheld`/`FORBIDDEN` redaction on AI/workflow outputs, citations, unresolved markers, and `review_evidence["compared"]` plus `not reason_ok` / `withheld` redaction for non-author viewers. |
| `P03` / `P03-T01` | Focused `TasksMixin` Regression Test and Focused-Tier Validation | Reconciled | Checked off in plan and marked `Complete` in phase details; exactly `1` test method added on `TasksMixin` (`0` tests removed) and all Focused validation commands passed. |
| `Follow-Up Items` | Carry-forward shared scrubbing helper and external OD-14/OD-19/Entra governance | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` completion claims in both plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_ai_tasks.py` | Rebased `feat/ai-116-entra-output-0052` onto `7f83f4749` (`PR #1761`); resolved `/api/ai/report` payload conflict in `server.py` to retain both `"chat_evaluation": chat_eval.run_eval()` and `"live": s.ai_live_report(u)`, and preserved `#164` and `#116` tests in `test_ai_tasks.py`. | `7b882614d` is a direct descendant of `7f83f4749`. | Passed (`Endpoints` `/api/ai/report` tests in `test_ai_tasks.py` and `test_ai_consumption_api.py`, `src/api` `mypy` & `ruff`). | Reconciled and conformant |
| `P02`, `P02-T01` | `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/ai_tasks.py` | Replaced disallowed `'human-approved'` phrase in `validate_necessity_exception` docstring with `'human-authorized'`; updated `ai_tasks._record_view` to preserve `override_text`, `reviewer_reason`, `reason`, and `review_evidence["reason"]` when `is_author` is `True` while enforcing `withheld`/`FORBIDDEN` checks on `ai_output`, `shown_output`, `workflow_output`, `citations`, `unresolved`, and `review_evidence["compared"]` for all viewers and `not reason_ok` / `withheld` `NOTE_HELD` redaction for non-author viewers. | `git diff src/core/` confirms exact surgical edits matching `FR-2`, `FR-3`, and `PC-002`. | Passed (`test_content_standard.py`, `test_human_review_effectiveness_223.py`, `test_data_protection.py`, `test_ai_tasks.py`, `src/core` `mypy` & `ruff`). | Reconciled and conformant |
| `P03`, `P03-T01` | `src/api/tests/test_ai_tasks.py` | Added `test_record_view_preserves_author_review_notes_while_holding_tainted_outputs_and_non_author_views` on `TasksMixin` covering `JsonTasks` and `SqlTasks` for author (`Retrofit Coordinator`) vs non-author `reason_ok=False` (`Programme Support Officer`) and non-author `reason_ok=True` (`Building Safety Liaison` lacking `FINANCE_VIEW`). | Respects test-bounds lock (`0` removals, `1` method added on `TasksMixin`, `0` new files). | Passed (`229` unit tests across `8` suites, `mypy` + `ruff` across `core`/`agents`/`api`, `25` tests in `rename-zava-tests.py`). | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P03`, `P03-T01` | Configured `zava_forward.pth` (plus `python-pptx` and `Pillow`) in the external session-workspace virtualenv instead of `pip install --no-build-isolation -e`, and aligned `P03-T01` wording so the single frozen local commit includes the completed `c1` review artifact. | `pip install --no-deps --no-build-isolation -e` hit missing `bdist_wheel` on system setuptools; user decision: none (ordinary local validation-environment refinement preserving caller intent). | Synchronized `P03`, `P03-T01`, `Handoff`, and `Phase Index` across plan, phase details, and changes record. | Not material; `PC-001`..`PC-003` remained satisfied with `0` untracked worktree build artifacts. | Reconciled and justified |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three single-pass critique findings (`PC-001` external venv + `pyproject.toml`-respecting Ruff checks, `PC-002` non-author `withheld` check on reason fields + unconditional `workflow_output` check in `_record_view`, and `PC-003` `git fetch origin`, `TasksMixin` test placement, and `#164`/`src/agents` regression suites) were directly applied in the plan/details and faithfully implemented.
* Material revisions: None. No discovery altered requirements, scope, architecture, acceptance criteria, dependencies, or evidence boundaries.
* Dependent-work pause assessment: Execution respected `P01 -> P02 -> P03` dependency order with no premature advancement.
* Justification assessment: Supported by git ancestry, clean diffs, and passing validation evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Extract shared post-provider record-visibility scrubbing helper across `ai_tasks._record_view`, `Store._rec_view`, and `ChatIsolation.scrub_thread` | Refactoring across modules is outside surgical `c1` CI fix scope | Later refactoring cycle (`follow-up`) | Open; properly kept outside active `Pxx`/`Pxx-Txx` claims and routed as distinct follow-up work. |
| Organisational control-owner confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration | External governance and live tenant administration outside repository code | Control owners / deployment administrator (`follow-up`) | Open; properly kept outside active `Pxx`/`Pxx-Txx` claims and routed as distinct external follow-up work. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No defects, decision gaps, or material evidence gaps were identified within the assessed Cycle 1 (`c1`) task boundary.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| none | none | No defect remediation required for the assessed `c1` boundary | Conformant implementation |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Concurrent parent-branch advance (`PR #1769`, `0c1fa1da4`, `Refs #83`; plus `PR #1770`, `d8cb35d25`, `Refs #133`): Completed inside Cycle 1 via child rebase continuation `issue-116-entra-output-0052-c1-rebase` (rebased `7b882614d..e7d05fab4` onto `origin/feat/demo-164-chat-grounding-provenance-0900` at `d8cb35d25` atop `0c1fa1da4`, producing `fc44a697c..41091c2a0`; see Rebase Continuation Record below and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-rebase-review.md`).
* Shared post-provider record-visibility scrubbing helper across `ai_tasks._record_view`, `Store._rec_view`, and `ChatIsolation.scrub_thread`: Optional engineering-quality refactoring follow-up.
* External governance items (`OD-14`, `OD-19`, live Microsoft Entra B2B tenant settings): Owned by organisational control owners outside repository scope.

## Cycle 1 Rebase Continuation Record (`0c1fa1da4` / `PR #1769` -> `d8cb35d25` / `PR #1770`)

* Continuation task: `issue-116-entra-output-0052-c1-rebase` (executed inside Cycle 1 without spending a new correction cycle; original `c1` `Outcome: Conformant` preserved untouched below).
* Rebase ancestry: `git fetch origin feat/demo-164-chat-grounding-provenance-0900` fetched `d8cb35d25` (`PR #1770`, `Refs #133`), whose direct parent is `0c1fa1da4` (`PR #1769`, `Refs #83`). Rebasing `7b882614d..e7d05fab4` onto `origin/feat/demo-164-chat-grounding-provenance-0900` produced `fc44a697c` (`7b882614d'`) and `41091c2a0` (`e7d05fab4'`), satisfying both `git merge-base --is-ancestor 0c1fa1da4 HEAD` and `git merge-base --is-ancestor d8cb35d25 HEAD`.
* Conflict resolution verified: Resolved the sole conflict file `src/core/src/zava_forward/core/store.py` (`_queue_candidates` and `_work_context`) preserving both `0c1fa1da4`'s `handoff_policy` cache-key tuple element and 4-argument `handoff_view(c, as_of=self.as_of, policy=..., staff=...)` calls (alongside auto-merged `detail` and inherited `taskqueues.MEMBERSHIP_REVISION = 4` + `sqlstore._queue_fingerprint`) and `7b882614d`'s Ruff formatting and `#116` role-visibility projections; `41091c2a0` replayed cleanly with zero conflicts.
* Post-rebase Focused validation: `115` caller unit tests (`test_ai_tasks.py`, `test_design_system.py` mapped from absent `test_design_system_source_contract.py`, `test_data_protection.py` — `OK`), `174` cross-feature `#83`/`#133`/`#116` unit tests (`OK`), `src/core` `ruff check`/`ruff format --check` (`284` files) + `mypy` (`0` issues in `337` files), `src/api` `ruff check`/`ruff format --check` (`197` files), and `tools/rename-zava-tests.py` (`25` tests — `OK`). Full continuation review is recorded in `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-rebase-review.md`.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `<venv>/bin/python -m unittest src/api/tests/test_content_standard.py src/core/tests/test_human_review_effectiveness_223.py src/core/tests/test_data_protection.py src/api/tests/test_ai_tasks.py -q` | Caller primary `core` + `api` suites (`JsonTasks` & `SqlTasks`) | Passed | `Ran 141 tests in 40.627s — OK` |
| `<venv>/bin/python -m unittest src/core/tests/test_ai_eval.py src/agents/tests/test_ai_eval.py src/agents/tests/test_chat_heldout.py src/api/tests/test_ai_consumption_api.py` | Rebased `#164` (`PR #1761`) eval/chat + consumption suites | Passed | `48` eval/chat tests (`189` combined in `58.853s — OK`) + `40` consumption API tests (`OK`) |
| `(cd src/core && <venv>/bin/python -m mypy && ruff check . && ruff format --check . && ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 src/zava_forward/core/data_protection.py && ruff format --isolated --line-length 100 --check src/zava_forward/core/data_protection.py)` | `src/core` static types, lint, and formatting | Passed | `mypy`: `0` issues in `336` files; `ruff`: `All checks passed!`, `283 files already formatted`; `--isolated` checks on `data_protection.py`: passed |
| `(cd src/agents && <venv>/bin/python -m mypy && ruff check . && ruff format --check .)` | `src/agents` static types, lint, and formatting | Passed | `mypy`: `0` issues in `66` files; `ruff`: `All checks passed!`, `62 files already formatted` |
| `(cd src/api && <venv>/bin/python -m mypy && ruff check . && ruff format --check .)` | `src/api` static types, lint, and formatting | Passed | `mypy`: `0` issues in `280` files; `ruff`: `All checks passed!`, `196 files already formatted` |
| `<venv>/bin/python tools/rename-zava-tests.py` | Repository migration regression | Passed | `Ran 25 tests in 0.745s — OK` |
| `python3 tools/rpi-checks.py --all` / Docker builds | Full repository gate | Skipped | Explicitly excluded by caller (`Focused tier, no Docker/full gate`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned phases (`P01`..`P03`), caller requirements (`#1`..`#4`), functional and non-functional requirements (`FR-1`..`FR-3`, `NFR-1`), test-bounds locks (`0` removals, `1` focused method added on `TasksMixin`), and critique dispositions (`PC-001`..`PC-003`) are complete, reconciled, and verified by `229` passing unit tests, `mypy`/`ruff` across `src/core`, `src/agents`, and `src/api`, and `tools/rename-zava-tests.py`.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Coordinator / optional child loop to rebase onto concurrent `PR #1769` (`0c1fa1da4`), optional shared record-scrubbing helper refactor, and external OD-14/OD-19/Entra governance sign-off |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `229` unit tests across `8` suites (`Passed`), `mypy` + `ruff` across `src/core`, `src/agents`, and `src/api` (`Passed`), `tools/rename-zava-tests.py` (`25` tests `Passed`); full Docker/`rpi-checks.py --all` gate `Skipped` per caller Focused-tier instruction
* Blockers: none
