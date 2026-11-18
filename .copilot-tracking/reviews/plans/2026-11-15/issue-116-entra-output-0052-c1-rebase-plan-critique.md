<!-- markdownlint-disable-file -->
# RPI Plan Critique: Cycle 1 Rebase Continuation (`c1-rebase`) Onto Merged Parent Tip `0c1fa1da4` (`PR #1769`)

## Metadata

* Task ID: issue-116-entra-output-0052-c1-rebase
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Rebase `feat/ai-116-entra-output-0052` (`7b882614d..e7d05fab4`, currently at `e7d05fab4`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, after `PR #1769` merged) inside Cycle 1 with no new correction cycle spent; resolve the single conflict in `src/core/src/zava_forward/core/store.py` preserving both `0c1fa1da4` handoff changes and `7b882614d` `MEMBERSHIP_REVISION` / role-visibility changes; update `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` to record the rebase onto `0c1fa1da4`; run Focused validation (`unittest`, `src/core` `ruff` + `mypy`, `src/api` `ruff`, and `tools/rename-zava-tests.py`); commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; do not push; leave `git status --short` empty; and exit immediately without calling `ask_user`.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-rebase-research.md, .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md, .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md, .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md, .copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md, .copilot-tracking/rpi-sessions/2026-11-15/issue-116-entra-output-0052-c1-rebase-state.json, `src/core/src/zava_forward/core/store.py`, `src/core/pyproject.toml`, `src/api/pyproject.toml`, `src/api/tests/test_design_system.py`, and read-only inspection of `0c1fa1da4`, `7b882614d`, `e7d05fab4`, `git merge-tree --write-tree 0c1fa1da4 7b882614d`, and host `python3` validation commands.
* Decisions, dependencies, and acceptance criteria considered: Confirmed automatic RPI continuation inside Cycle 1 (`c1-rebase`); preservation of original `c1` `Outcome: Conformant` review verdict per `.github/copilot-instructions.md`; Focused validation tier; `FR-1`, `FR-2`, `NFR-1`, test-bounds lock (`0` test edits/removals), and clean post-review local commit without pushing.
* Assessment boundary: Evaluates merge-tree accuracy, `store.py` conflict resolution, cross-feature `#83`/`#164`/`#116` compatibility, shell/backup mechanics, validation command executability under host `python3`, and RPI pre-review/post-review commit ordering. Excludes Docker builds, `tools/rpi-checks.py --all`, hosted CI execution, and live Microsoft Entra tenant settings.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Scope #1 (fetch and rebase `7b882614d..e7d05fab4` onto `0c1fa1da4`); `C1`, `C4`; `FR-1`; `P01`, `P01-T01` | Partial | Commit ancestry and clean replay of `e7d05fab4` are verified, and `gh api user` noreply email resolution works, but `P01-T01` step 2 uses `.copilot-tracking/**/issue-116-entra-output-0052-c1-rebase-*` without `globstar` or directory-structure preservation (`PC-003`). |
| Caller Scope #2 (`store.py` conflict resolution preserving `#83` handoffs and `#116` `MEMBERSHIP_REVISION`/role visibility); `C2`, `C3`; `FR-1`; `P01-T01` | Covered | Read-only `git merge-tree --write-tree 0c1fa1da4 7b882614d` confirms `server.py` and `test_role_endpoint_inventory.py` auto-merge cleanly, `detail` in `store.py` auto-merges to 4-arg `handoff_view(...)`, `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` carry over untouched from `0c1fa1da4`, and `P01-T01`'s exact hunks for `_queue_candidates` and `_work_context` preserve 100% of `#83` and `#116`. |
| Caller Scope #3 (update `c1-changes.md` and `c1-review.md` for `0c1fa1da4`); `C6`; `FR-2`; `P02`, `P02-T01` | Covered | Appending dated `0c1fa1da4` rebase and validation sections to `issue-116-entra-output-0052-c1-changes.md` and `issue-116-entra-output-0052-c1-review.md` in a clean commit atop `e7d05fab4'` preserves `c1`'s original `Outcome: Conformant` and avoids circular SHA invalidation. |
| Caller Scope #4 (Focused validation commands); `C5`; `NFR-1`; `Acceptance Criteria`; `P02`, `P02-T01` | Partial | `ruff`, `mypy`, and `tools/rename-zava-tests.py` pass directly on host `python3`, but command #1 fails with `ModuleNotFoundError` because `src/api/tests/test_design_system_source_contract.py` does not exist in the repository (`PC-001`), and cross-feature command #2 fails with `ModuleNotFoundError: No module named 'tests'` on `src/api/tests/test_handoff_escalation_api_83.py` when `src/api` is omitted from `PYTHONPATH` (`PC-002`). |
| Caller Scope #5 (clean commit with Copilot trailer, no push, empty `git status --short`, no `ask_user`); `FR-2`; `P02-T01` | Partial | Single post-rebase tracking commit strategy is sound, but `P02-T01` `Completion Evidence` requires the post-`rpi-review` commit and empty `git status --short` inside an `rpi-implement` task that completes before `rpi-review` runs (`PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: The core rebase and `store.py` conflict-resolution design (`P01-T01`) is exact and verified against `git merge-tree`, `0c1fa1da4`, `7b882614d`, and `e7d05fab4`. However, two `High`-severity validation-command defects (`PC-001` and `PC-002`) will cause deterministic `ModuleNotFoundError` failures during `P02-T01`, and one `Medium`-severity execution-mechanics defect (`PC-003`) breaks the `P01-T01` tracking-file backup glob and conflates `P02-T01` pre-review implementation completion with the post-review closeout commit. All three findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Non-existent `src/api/tests/test_design_system_source_contract.py` target in `NFR-1`, `Acceptance Criteria`, and `P02-T01` causes `ModuleNotFoundError`

* Related IDs: Caller Scope #4, C5, NFR-1, Acceptance Criteria, P02, P02-T01
* Evidence: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md, .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md, .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-rebase-research.md, src/api/tests/test_design_system.py
* Concern: The plan (`NFR-1` and `Acceptance Criteria`) and phase details (`P02` / `P02-T01` `Validation Expectations` command #1) require `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/api/tests/test_ai_tasks.py src/api/tests/test_design_system_source_contract.py src/core/tests/test_data_protection.py -q` to exit `0`. Direct repository inspection across `e7d05fab4`, `7b882614d`, `0c1fa1da4`, `origin/main`, and full git history confirms `src/api/tests/test_design_system_source_contract.py` does not exist anywhere in the repository; the actual design-system source-contract suite is `src/api/tests/test_design_system.py` (`class DesignSystem`). Running the command as written fails immediately with `ModuleNotFoundError: No module named 'src/api/tests/test_design_system_source_contract'` (`exit code 1`).
* Impact: `P02-T01` cannot satisfy its `exit 0` gate as written, and the non-interactive caller constraint forbids calling `ask_user` mid-implementation.
* Smallest useful change: Update `NFR-1`, `Acceptance Criteria` (`Canonical test targets`), and `P02` / `P02-T01` `Validation Expectations` command #1 to run `src/api/tests/test_design_system.py` alongside `src/api/tests/test_ai_tasks.py` and `src/core/tests/test_data_protection.py`, and explicitly disclose in `NFR-1` (and in `c1-changes.md` / `c1-rebase-changes.md`) that caller-referenced `src/api/tests/test_design_system_source_contract.py` is absent in the repository and maps to `src/api/tests/test_design_system.py`.
* Action owner: planning_parent
* Exact resolving evidence: Revised plan and phase details using `src/api/tests/test_design_system.py` in `P02-T01` command #1 with explicit filename-mapping disclosure, where `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/api/tests/test_ai_tasks.py src/api/tests/test_design_system.py src/core/tests/test_data_protection.py -q` exits `0`.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Cross-feature validation command #2 omits `src/api` from `PYTHONPATH`, breaking `from tests.test_mvp import DATA` in `test_handoff_escalation_api_83.py`

* Related IDs: C1, C5, NFR-1, P02, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md, 0c1fa1da4:src/api/tests/test_handoff_escalation_api_83.py:17
* Concern: `P02` / `P02-T01` `Validation Expectations` command #2 executes `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/core/tests/test_handoff_escalation_83.py src/api/tests/test_handoff_escalation_api_83.py ... -q` from the repository root. In `0c1fa1da4`, `src/api/tests/test_handoff_escalation_api_83.py:17` imports `from tests.test_mvp import DATA as _MVP_DATA`. Because `PYTHONPATH` contains `src/api/tests` rather than `src/api` and the working directory is the repository root, Python cannot resolve the `tests` namespace package under `src/api/` and fails with `ModuleNotFoundError: No module named 'tests'`.
* Impact: `P02-T01` validation command #2 will fail on the rebased branch despite a valid rebase.
* Smallest useful change: Add `src/api` to `PYTHONPATH` in `P02` / `P02-T01` command #2 (`PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api:src/api/src:src/api/tests`) or split the API `#83` test invocation to run from `cd src/api` so `from tests.test_mvp import DATA` resolves cleanly.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02` / `P02-T01` command #2 in `.copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md` with `src/api` on `PYTHONPATH` (or `cd src/api`), verified to import `tests.test_mvp` and exit `0`.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P01-T01` tracking backup glob fails without `globstar`/path preservation and `P02-T01` conflates pre-review task completion with the post-review commit

* Related IDs: FR-1, FR-2, P01, P01-T01, P02, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md, .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md
* Concern: Two execution-ordering and shell-mechanics gaps exist in `issue-116-entra-output-0052-c1-rebase-phase-details.md`:
  1. `P01-T01` step 2 instructs moving `.copilot-tracking/**/issue-116-entra-output-0052-c1-rebase-*` into a flat backup folder `/home/azureuser/.copilot/session-state/f0c59e3e-4b74-4f53-a238-646f1d96d6c1/files/c1-rebase-backup/`. Under default non-interactive Bash (`globstar` off), `.copilot-tracking/**/issue-116-entra-output-0052-c1-rebase-*` matches zero paths because `research/2026-11-15/...` is two directories below `.copilot-tracking` and `reviews/plans/2026-11-15/...` is three directories below `.copilot-tracking`; moving all files into one flat directory also discards their relative directory paths needed in step 6.
  2. `P02-T01` sets `Completion Evidence` to `Clean git log -n 4 atop 0c1fa1da4 and empty git status --short` after `rpi-review` writes `c1-rebase-review.md` and `c1-rebase-state.json` reaches `Follow-up` (`completed`). However, `rpi-implement` must mark `P02` / `P02-T01` complete before handing off to read-only `rpi-review`. Requiring the post-review commit as `P02-T01` completion evidence leaves `P02-T01` unverified when `rpi-review` inspects the working tree.
* Impact: Step 2 of `P01-T01` fails with `mv: cannot stat` or misplaces restored `.copilot-tracking/` files, and `P02-T01` creates a premature-completion mismatch during `rpi-review`.
* Smallest useful change: Replace `P01-T01` steps 2 and 6 with path-preserving `find .copilot-tracking -name 'issue-116-entra-output-0052-c1-rebase-*' -print0 | tar --null -cf /home/azureuser/.copilot/session-state/f0c59e3e-4b74-4f53-a238-646f1d96d6c1/files/c1-rebase-backup.tar -T -` followed by removing those matched untracked files before `git rebase` and extracting/deleting `c1-rebase-backup.tar` immediately after `git rebase`. In `P02` / `P02-T01` (and Plan `P02-T01`), define `P02-T01`'s implementation completion evidence as passing Focused validation plus updated `c1-changes.md`, `c1-review.md`, and reconciled `c1-rebase` plan/details/changes ready for `rpi-review`, and explicitly place the single final local commit (bundling `c1-rebase-review.md` and finalized `c1-rebase-state.json` with the Copilot trailer and empty `git status --short`) in the automatic RPI parent's post-`rpi-review` closeout step.
* Action owner: planning_parent
* Exact resolving evidence: `P01-T01` uses `find` + `tar` path-preserving backup/restore in the session workspace, and `P02` / `P02-T01` separates `rpi-implement` pre-review completion from the post-`rpi-review` local commit.
* Decision route: Direct planner correction.

## Strengths and Residual Risk

* Exact merge-tree and line-level conflict verification: The candidate plan and phase details accurately identify that `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, and `Store.detail` (`d["handoff"] = handoff_view(...)`) auto-merge cleanly onto `0c1fa1da4`, `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` carry over untouched from `0c1fa1da4`, `e7d05fab4` replays with zero file overlap, and `store.py` has only two mechanical conflict blocks (`_queue_candidates` and `_work_context`) whose proposed resolutions preserve 100% of `#83` and `#116` semantics.
* Provenance-preserving C1 tracking strategy: Recording the `0c1fa1da4` rebase and new rebased commit SHAs (`7b882614d'` and `e7d05fab4'`) in a clean tracking commit atop `e7d05fab4'` preserves the reviewed code trees and `c1-review.md`'s original `Outcome: Conformant` without circular SHA edits.
* Accepted residual risk: Per caller Focused-tier boundaries, Docker builds, `tools/rpi-checks.py --all`, `git push`, and external governance items (`OD-09`, `OD-14`, `OD-19`, live Entra tenant configuration) remain outside this local rebase continuation.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Read-only critique verified `git merge-tree --write-tree 0c1fa1da4 7b882614d` and validation commands against `e7d05fab4` and `0c1fa1da4` blobs without mutating the working tree or executing `git rebase`; full post-rebase runtime execution across merged `0c1fa1da4` + `7b882614d'` + `e7d05fab4'` belongs to `rpi-implement` (`P02-T01`).

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md` and `.copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md` to resolve `PC-001`, `PC-002`, and `PC-003`, record the critique disposition, mark planning `ready`, and continue directly to `rpi-implement` without a second critique pass.
* User response required: no
