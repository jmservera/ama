<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #164 PR #1761 Cycle 1 Hosted CI src-api Fix

## Metadata

* Task ID: issue-164-pr1761-ci-cycle1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-164-pr1761-ci-cycle1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-164-pr1761-ci-cycle1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Resolve the PR #1761 (`feat/ai-164-chat-revocation-0042`, Issue #164) hosted `src-api` CI failure in `test_manager_report_local_http_and_bad_period` (`src/api/tests/test_ai_consumption_api.py`, line 2089) so `chat_evaluation` is expected in `set(held)` when metering is held, update Cycle 1 `.copilot-tracking/` changes and review artifacts, pass the caller-specified `src/api` `unittest` (`-B`), `ruff check`, `ruff format --check`, and `mypy` command, and commit locally with `Refs #164` and the Copilot trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/issue-164-pr1761-ci-cycle1-research.md (`C1` through `C4`), .copilot-tracking/plans/2026-11-15/issue-164-pr1761-ci-cycle1-plan.md, .copilot-tracking/details/2026-11-15/issue-164-pr1761-ci-cycle1-phase-details.md, src/api/tests/test_ai_consumption_api.py (lines 2040-2200), and src/api/src/zava_forward/api/server.py (lines 890-980).
* Decisions, dependencies, and acceptance criteria considered: Application runtime code (`src/api/src/zava_forward/api/server.py` and `src/agents/src/zava_forward/agents/chat_eval.py`) and `chat-case-conversation` disabled enablement state remain untouched; focused validation tier applies to this test-only Cycle 1 alignment; commit stays local with `Refs #164`, the Copilot co-author trailer, and an empty `git status --short`.
* Assessment boundary: Assesses plan and phase-detail credibility from the supplied Cycle 1 research, plan, phase details, and inspected slices of `src/api/tests/test_ai_consumption_api.py` and `src/api/src/zava_forward/api/server.py`. Does not execute tests or linters, inspect `chat_eval.py` directly beyond `C2` and `C3`, or observe hosted CI runs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Held `/api/ai/report` key-set and `chat_evaluation` parity (`C1`, `C2`, `C3`, `P01`, `P01-T01`) | Covered | `P01-T01` updates line 2089 of src/api/tests/test_ai_consumption_api.py to assert `set(held) == {"evaluation", "chat_evaluation", "live", "registry", "consumption"}` and adds `held["chat_evaluation"]` key-set, `version`, and `enablement["state"] == "disabled"` assertions across both `"meter-capacity-reached"` and `"meter-evidence-invalid"` subtests. |
| Focused `src/api` validation suite (`C4`, `P01`, `P01-T01`) | Covered | Plan non-functional requirements, acceptance criteria, and `P01-T01` specify the exact caller `PYTHONPATH=... python3 -B -m unittest tests/test_ai_consumption_api.py tests/test_ai_tasks.py`, `ruff check src tests`, `ruff format --check src tests`, and `mypy tests/test_ai_consumption_api.py` command in `src/api`, including `line-length = 100` formatting care. |
| Cycle 1 `.copilot-tracking/` changes and review artifacts | Covered | Plan user requirements, acceptance criteria, and handoff preserve original `issue-164-chat-eval-revocation` evidence while routing Cycle 1 changes and review artifacts under `.copilot-tracking/*/2026-11-15/issue-164-pr1761-ci-cycle1-*`. |
| Local commit closeout (`Refs #164`, Copilot trailer, clean tree, no push) | Covered | Plan user requirements, non-goals, and acceptance criteria enforce a local-only commit with `Refs #164`, the Copilot trailer, no `git push`, and an empty `git status --short`. |

## Verdict

* Verdict: Pass
* Rationale: The plan and phase details match the verified `GET /api/ai/report` held-response contract in src/api/src/zava_forward/api/server.py (lines 924-939) and the exact failing assertion in src/api/tests/test_ai_consumption_api.py (line 2089), cover both consumption-hold subtests with parity checks mirroring `held["evaluation"]`, run the exact caller-mandated validation command with `-B` and 100-column `ruff format` awareness, and satisfy RPI tracking and local-commit constraints without unintended scope expansion.

## Findings

* None. No actionable `PC-xxx` defects were found within the supplied criterion boundary.

## Strengths and Residual Risk

* Direct endpoint contract verification: src/api/src/zava_forward/api/server.py (lines 924-939) catches `ai_consumption.DispatchHeld` strictly around `consumption` and returns HTTP 200 with all five keys (`evaluation`, `chat_evaluation`, `live`, `registry`, `consumption`), confirming `P01-T01` tests true runtime behavior rather than weakening an assertion.
* Full target-method verification: Inspection of `test_manager_report_local_http_and_bad_period` through line 2150 of src/api/tests/test_ai_consumption_api.py confirms no other assertion in the method checks an exact `/api/ai/report` top-level key set without `chat_evaluation`.
* Format and clean-worktree discipline: `P01-T01` explicitly flags `ruff format --check` (`line-length = 100`) because adding `"chat_evaluation"` pushes the single-line `assertEqual(set(held), ...)` statement past 100 characters, and `-B` avoids untracked bytecode files.
* Accepted residual risk (no-push scope and publication hygiene): Hosted `src-api` CI remains unobserved until the caller pushes PR #1761; if PR #1761 requires an external full RPI gate receipt (`tools/rpi-checks.py --all`) prior to push, the new local commit will invalidate any earlier receipt and require an external receipt refresh against `origin/main` before push, and commit creation during closeout must apply repository-local privacy-safe `user.email` (`{id}+{login}@users.noreply.github.com`).

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* This read-only critique did not execute `unittest`, `ruff`, or `mypy`, and relied on supplied research item `C3` for repository-wide search coverage outside the inspected ranges of src/api/tests/test_ai_consumption_api.py and src/api/src/zava_forward/api/server.py.

## Recommended Next Action

* Highest-impact finding: None
* Action owner: planning_parent
* Smallest next action: Finalize the plan critique disposition (`Pass`) and proceed to `P01-T01` implementation, focused `src/api` validation, Cycle 1 review recording, and local commit closeout.
* User response required: No
