<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #117 Document Scan Rebase Continuation onto fa6f8d1dd

## Metadata

* Task ID: issue-117-doc-scan-rebase-fa6f8d1dd
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Rebase `feat/demo-117-doc-scan` (clean candidate commit `4d91dae33`, anchored on `243764945`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) in `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan` (Caller Step 1); run focused validation (`ruff check .`, `ruff format --check .`, `mypy`, and the `#117` document malware scan quarantine tests in `src/core` and `src/api`) on the rebased HEAD, leave `git status --short` empty, and do not push (Caller Step 2).
* Research and evidence considered: .copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md (`C1`–`C8`), .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md, .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md, .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md, .copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md, .copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json, .copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-state.json.
* Decisions, dependencies, and acceptance criteria considered: Confirmed single-hunk `Store.focus` union conflict resolution (`#76` `self._open_safety_items` + `#117` `is_available_case_document`), zero `server.py` route changes, worktree-local `PYTHONPATH`/`MYPYPATH` isolation against shared `~/.local` editable links, repository privacy-safe noreply git author + `Co-authored-by` trailer, preservation of original `#117` Review outcomes, empty `git status --short` on completion without pushing, and `FR-REB-01`–`FR-REB-02`, `NFR-REB-01`–`NFR-REB-02`, `AC1`–`AC4`.
* Assessment boundary: Evaluates plan and phase-details credibility, RPI stage sequencing, file-scope completeness, conflict-resolution soundness, and validation isolation solely from supplied artifacts without executing git operations, tests, or open-ended repository exploration.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Step 1 / `FR-REB-01` / `AC1` / `C1`–`C6` | Covered | Single conflict hunk in `src/core/src/zava_forward/core/store.py` (`Store.focus`), clean 3-way auto-merge in `chat_case_answers.py`, `projection.py`, and `taskqueues.py` (with `I001` import-order guard before `git rebase --continue`), and zero `server.py` diff are accurately planned in `P01-T01`. |
| `P01` / `P01-T01` (`NFR-REB-02` git config & rebase) | Covered | Configures local noreply `user.email` via `gh api user` before `git rebase`, keeps tracked `#117` files clean until `git rebase --continue`, and verifies `fa6f8d1dd` ancestry and `git diff --check`. |
| Caller Step 2 (validation) / `NFR-REB-01` / `AC2` / `C7`–`C8` | Partial | Per-project `ruff check .`, `ruff format --check .`, `mypy`, `#117` quarantine tests, `#76` `Store.focus` regression tests, `test_role_endpoint_inventory.py`, and `tools/rename-zava-tests.py` cover the code boundary, but `P02-T01` omits `zava_forward.agents.__file__` and the concrete assertion command despite `~/.local` holding an editable `zava-forward-agents` link to another worktree (`PC-002`). |
| Caller Step 2 (`git status --short` empty, no push) / `FR-REB-02` / `NFR-REB-02` / `AC3`–`AC4` / `P03` / `P03-T01` | Partial | `P03-T01` assigns a post-`rpi-review` commit and empty `git status --short` completion condition to an `rpi-implement` task that runs before read-only `rpi-review`, omits 4 untracked child `.copilot-tracking/` artifacts from `P03` Likely Targets, and does not explicitly guard preservation of original `#117` Review outcomes (`PC-001`). |

## Verdict

* Verdict: Revise
* Rationale: Rebase conflict analysis (`Store.focus` union atop `fa6f8d1dd`) and focused test selection are well grounded in `C1`–`C8`, but `P03`/`P03-T01` and `AC3`–`AC4` contain a stage-ordering inversion between `rpi-implement`, read-only `rpi-review`, and post-Review `RPI Agent` state persistence—and omit four untracked child `.copilot-tracking/` files from `P03` Likely Targets—that would leave `P03-T01` uncompletable before Review or leave untracked files in `git status --short` (`PC-001`), alongside an incomplete `zava_forward.agents.__file__` isolation check in `P02-T01` (`PC-002`). Both findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: `P03-T01` conflates pre-Review `rpi-implement` deliverables with post-Review parent closeout commit and omits four untracked child `.copilot-tracking/` artifacts

* Related IDs: `FR-REB-02`, `NFR-REB-02`, `AC3`, `AC4`, `P03`, `P03-T01`, `C7`
* Evidence: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md (`FR-REB-02`, `AC3`, `AC4`, `P03`, `P03-T01`); .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md (`P03` Likely Targets and Validation Expectations, `P03-T01` Intent and Likely Targets)
* Concern: `P03-T01` is an `rpi-implement` task checkbox that must be reconciled and checked `[x]` *before* `rpi-review` executes, yet its expected result and validation expectations require committing finalized tracking state *after* `rpi-review` (`issue-117-doc-scan-rebase-fa6f8d1dd-review.md` and `Follow-up` `state.json`) so `git status --short` is empty. Because `rpi-review` is read-only outside its own review log and runs before the parent `RPI Agent` persists final `Follow-up` state, `rpi-implement` cannot execute a post-Review commit inside `P03-T01`, and `rpi-review` evaluating `AC3`/`AC4` mid-Review would observe uncommitted review/state files. In addition, `P03` Likely Targets lists only 6 `.copilot-tracking/` files and omits `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md`, `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan-critique.md`, and `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-review.md`, and does not explicitly state that updating parent `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md` must append/reference post-rebase evidence without overwriting its original `Residual work` (`RV-001`) outcome.
* Impact: Either `P03-T01` cannot be truthfully completed during `rpi-implement` (triggering a `Plan-to-Change Reconciliation` or `AC4` discrepancy during `rpi-review`), or staging only the 6 listed `P03` Likely Targets leaves up to 4 untracked child RPI files (`??`) in `git status --short`, violating Caller Step 2 (`leave git status --short empty`) or repository original-Review preservation rules.
* Smallest useful change: Split pre-Review and post-Review responsibilities explicitly in `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md` (`FR-REB-02`, `AC3`, `AC4`, `P03`, `P03-T01`) and `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md` (`P03`, `P03-T01`): (1) scope `P03-T01` (`rpi-implement`) to appending post-rebase base/SHA/validation reconciliation to parent `#117` records (preserving original `Residual work` / `RV-001` Review outcomes), authoring child `-changes.md`, reconciling `P01`–`P03` plan markers, passing `python3 -m json.tool` and `git diff --check`, and leaving zero non-`.copilot-tracking/` dirty files (optionally committing the pre-Review `.copilot-tracking/` set); and (2) enumerate all 10 parent/child `.copilot-tracking/` artifacts (including `research`, `details`, `plan-critique`, and `review`) and assign the final local tracking commit (with privacy-safe noreply email and `Co-authored-by` trailer, leaving `git status --short` empty with no push) to parent `RPI Agent` post-Review closeout immediately after `rpi-review` writes `-review.md` and `state.json` transitions to `Follow-up`.
* Action owner: planning parent
* Exact resolving evidence: Updated `FR-REB-02`, `AC3`, `AC4`, `P03`, and `P03-T01` in `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md` and `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md` distinguishing `rpi-implement` pre-Review reconciliation (preserving original `#117` Review outcomes) from parent `RPI Agent` post-Review final `.copilot-tracking/` commit across all child and updated parent tracking paths.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: `P02-T01` worktree module-isolation check omits `zava_forward.agents.__file__` and concrete `Validation Expectations` command

* Related IDs: `NFR-REB-01`, `AC2`, `P02`, `P02-T01`, `C8`
* Evidence: .copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md (`Wave 3`, `C8`); .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md (`NFR-REB-01`); .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md (`P02` Boundaries and Validation Expectations, `P02-T01`)
* Concern: Research `C8` established via `pip list` (without executing a runtime import probe) that `~/.local` contains editable installs for all three distributions—`zava-forward-core`, `zava-forward-agents`, and `zava-forward-api`—pointing to sibling worktree `feat-164-chat-revocation-0042`. However, `NFR-REB-01` and `P02` Boundaries assert only `zava_forward.core.__file__` and `zava_forward.api.__file__` (omitting `zava_forward.agents.__file__`, which `src/api` imports via `../agents/src`), and `P02` Validation Expectations omits the explicit `python3 -c` path-assertion command from its runnable checklist.
* Impact: If PEP 420 namespace resolution or a `~/.local` editable finder resolves `zava_forward.agents` from `feat-164-chat-revocation-0042`, or if an implementer runs only the bulleted commands in `P02` Validation Expectations, cross-worktree module leakage could go undetected during `src/api` test runs.
* Smallest useful change: Update `NFR-REB-01` in `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md` and `P02` / `P02-T01` Validation Expectations in `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md` to include an explicit `python3 -c` assertion command verifying `zava_forward.core.__file__`, `zava_forward.agents.__file__`, and `zava_forward.api.__file__` all resolve under `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/` under the planned `PYTHONPATH` before running `unittest`.
* Action owner: planning parent
* Exact resolving evidence: Updated `NFR-REB-01` and `P02` Validation Expectations containing the concrete `python3 -c` worktree-prefix assertion covering `zava_forward.core`, `zava_forward.agents`, and `zava_forward.api`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Single-hunk conflict boundary is proven via read-only `git merge-tree` (`C2`, `C3`), and combining `#76`'s `staff_list` + `self._open_safety_items(c, staff=staff_list)` with `#117`'s `is_available_case_document(d)` in `Store.focus` preserves both features cleanly while keeping `server.py` untouched.
* Proactive check for `ruff` `I001` import sorting in auto-merged `src/core/src/zava_forward/core/taskqueues.py` (`C6`) during `P01-T01` avoids post-rebase `git commit --amend` churn.
* Including `test_hazard_safeguarding_clock_owner.py`, `test_role_endpoint_inventory.py`, and `tools/rename-zava-tests.py` alongside the `#117` quarantine test suites directly exercises the merged `Store.focus`, `taskqueues.py`, and `projection.py` hunks.
* Residual risk (accepted): If `origin/feat/demo-164-chat-grounding-provenance-0900` advances past `fa6f8d1dd` on `origin` during `git fetch` in `P01-T01`, `P01` Validation Expectations (`git --no-pager log -n 2 --oneline` directly atop `fa6f8d1dd`) will detect the ref movement immediately so execution stops rather than silently rebasing onto an unresearched base.

## Questions or Blocking Evidence Gaps

* none

## Limitations

* Read-only critique over supplied research, plan, phase-details, and parent `#117` tracking records; no `git rebase`, lint, type-check, or unit-test commands were executed during critique.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Directly revise `FR-REB-02`, `NFR-REB-01`, `AC3`, `AC4`, `P02`, and `P03`/`P03-T01` in the plan and phase details to apply `PC-001` and `PC-002`, record critique dispositions, and finalize the plan for `rpi-implement` without re-running critique.
* User response required: no
