<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #156 PR #1727 Cycle-2 CI Mypy Union-Attr Fix

## Metadata

* Task ID: issue-156-pr-1727-mypy-c2
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/156-screen-design-traceability-mypy-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/156-screen-design-traceability-mypy-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Execute the Cycle-2 CI fix for Issue #156 (PR #1727, target branch `feat/demo-233-same-home-tensions-0825`) in worktree `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` on branch `feat/ux-156-design-traceability-1840`; resolve both strict `mypy` `[union-attr]` errors in `src/api/tests/test_screen_design_traceability.py` (`Match[str] | None` has no attribute `group` and `ClassDef | None` has no attribute `body`); preserve all existing `.copilot-tracking/` artifacts on the branch; add or update Cycle-2 RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` documenting the `assert match is not None` and `assert target_cls is not None` fix; pass `cd src/api && python3 -m mypy`, `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .`, and `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_screen_design_traceability.py -v`; and commit all changes cleanly on `feat/ux-156-design-traceability-1840` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/156-screen-design-traceability-mypy-c2-research.md, .copilot-tracking/plans/2026-11-14/156-screen-design-traceability-mypy-c2-plan.md, .copilot-tracking/details/2026-11-14/156-screen-design-traceability-mypy-c2-phase-details.md, src/api/tests/test_screen_design_traceability.py, src/api/tests/test_ux_design_traceability.py, src/api/pyproject.toml, .github/workflows/src-ci.yml, .github/copilot-instructions.md.
* Decisions, dependencies, and acceptance criteria considered: Confirmed decisions to create and switch to local branch `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` while keeping `docs/ux-156-design-traceability-1840` intact (`C8`), pair `self.assertIsNotNone(...)` with `assert match is not None` and `assert target_cls is not None` without adding `src/api/pyproject.toml` overrides (`C3` through `C7`), validate under the focused tier (`C1`, `C2`, `C8`), configure repository-local `{id}+{login}@users.noreply.github.com` via `gh api user`, leave the verified working tree uncommitted after `P01-T02` for `rpi-review` before creating one clean non-amended local commit on `feat/ux-156-design-traceability-1840`, and satisfy `FR-01` through `FR-03`, `NFR-01` through `NFR-02`, and `AC-01` through `AC-05`.
* Assessment boundary: Read-only credibility review of the supplied Cycle-2 research, final-candidate plan, phase details, named repository files, and read-only Git branch/worktree state. This critique does not mutate source, planning, or Git refs and does not execute hosted GitHub Actions runs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Step 1, FR-03 (preservation), AC-05, C8 | Covered | Plan and `P01` boundaries preserve all existing `.copilot-tracking/` artifacts and `docs/ux-156-design-traceability-1840`, verifying empty `git diff --diff-filter=D` before review and empty `git diff --diff-filter=D HEAD~1..HEAD` after commit. |
| Caller Step 2, FR-03 (Cycle-2 artifacts), AC-05 | Covered | Scope, `Implementation Context Record`, `P01-T02`, and post-review closeout cover `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` plus phase details, plan critique, and session state records. |
| Caller Step 3, FR-01, FR-02, NFR-01, NFR-02, AC-01..AC-04, C1..C7 | Covered | `P01-T01` narrows `Match[str] \| None` (`match`) and `ast.ClassDef \| None` (`target_cls`) in `src/api/tests/test_screen_design_traceability.py` using `self.assertIsNotNone(...)` plus `assert ... is not None`, matching `src/api/tests/test_ux_design_traceability.py:81-82`, Ruff `E,F,I,B,UP` (`line-length = 100`), and `src-ci.yml` (`src-api` `mypy`, `ruff`, and `unittest` checks). |
| Caller Step 4, FR-03 (branch and commit), AC-05, C8 | Covered | `P01-T02` creates and checks out local `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840`, sets repository-local noreply `user.email` from `gh api user`, and defers the single non-amended commit (`Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, no push, `ahead 1`) until `rpi-review` writes `.copilot-tracking/reviews/2026-11-14/156-screen-design-traceability-mypy-c2-review.md`. |
| P01, P01-T01, P01-T02 | Covered | Phase and task boundaries, test ownership lock (`none` removals, `0` method additions), verified sibling check (`tests/test_ux_design_traceability.py`), and completion evidence are complete and internally consistent. |

## Verdict

* Verdict: Pass
* Rationale: The final-candidate plan and phase details credibly and completely address both strict `mypy` `[union-attr]` errors in `src/api/tests/test_screen_design_traceability.py`, align local branch `feat/ux-156-design-traceability-1840` at `deadb7144` with PR #1727 (`origin/feat/ux-156-design-traceability-1840`), satisfy `.github/copilot-instructions.md` focused-tier validation and privacy-safe noreply Git identity rules, and sequence the single local commit after `rpi-review` so all Cycle-2 artifacts land cleanly without amending or pushing. Earlier candidate findings (`PC-001` on branch/noreply/post-review commit sequencing and `PC-002` on an unverified sibling test path) are fully resolved in the supplied plan and phase details.

## Findings

No open actionable findings remain for this final-candidate plan (`0` Critical, `0` High, `0` Medium, `0` Low). Prior candidate findings verified resolved:

* `PC-001` (Resolved): Executive Summary, `P01-T02`, and `Handoff` now specify creating/switching to local `feat/ux-156-design-traceability-1840` tracking `origin/feat/ux-156-design-traceability-1840`, configuring repository-local `user.email` as `{id}+{login}@users.noreply.github.com` from `gh api user`, leaving the working tree uncommitted for `rpi-review`, and executing one clean post-review commit with the `Co-authored-by` trailer and no push.
* `PC-002` (Resolved): Unverified `tests/test_epic149_ux_journey_requirement_traceability.py` was removed; sibling regression verification now targets only verified `src/api/tests/test_ux_design_traceability.py` (`C7`).

## Strengths and Residual Risk

* `P01-T01` pairs `self.assertIsNotNone(...)` with `assert match is not None` and `assert target_cls is not None`, matching sibling `src/api/tests/test_ux_design_traceability.py:81-82` (`C7`), preserving runtime diagnostics under `python -O`, keeping `src/api/pyproject.toml` untouched (`C6`), and staying within Ruff's 100-column limit and `E,F,I,B,UP` lint selection (`C5`).
* Branch alignment (`git checkout -b feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840`) was verified conflict-free against local branch and worktree refs while leaving `docs/ux-156-design-traceability-1840` untouched (`C8`).
* Accepted operational note for implementation: Read-only worktree inspection shows `src/api/tests/test_screen_design_traceability.py` already contains the uncommitted `match` and `target_cls` narrowing diff against `HEAD` (`deadb7144`) and an untracked `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md` file already exists from the prior cycle draft. `git checkout -b feat/ux-156-design-traceability-1840` at `deadb7144` carries these working-tree files cleanly without conflict; during `P01-T01` and `P01-T02`, `rpi-implement` should verify the existing working-tree diff in `src/api/tests/test_screen_design_traceability.py` and update `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md` via `edit` rather than `create`.
* Accepted residual risk: Because the caller explicitly prohibits `git push`, hosted GitHub Actions CI (`src-ci.yml`) on the new local commit head will remain unobserved until pushed; per `.github/copilot-instructions.md`, `P01-T02` explicitly records local focused-tier verification alongside the pending-push hosted CI status.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Assessment stayed strictly within the supplied Cycle-2 research, plan, phase details, five named repository files, and read-only Git status/branch checks; no validation test commands were executed and no source, plan, or Git state was modified.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning parent
* Smallest next action: Record the `Pass` critique disposition in `.copilot-tracking/plans/2026-11-14/156-screen-design-traceability-mypy-c2-plan.md` and transition directly to `rpi-implement` for `P01` (`P01-T01`, `P01-T02`).
* User response required: no
