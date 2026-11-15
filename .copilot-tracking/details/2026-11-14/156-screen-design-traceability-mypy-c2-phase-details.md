<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #156 PR #1727 Cycle-2 CI Mypy Union-Attr Fix

## Metadata

* Task ID: issue-156-pr-1727-mypy-c2
* Task slug: 156-screen-design-traceability-mypy-c2
* Related plan: .copilot-tracking/plans/2026-11-14/156-screen-design-traceability-mypy-c2-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/156-screen-design-traceability-mypy-c2-research.md, src/api/tests/test_screen_design_traceability.py, src/api/tests/test_ux_design_traceability.py, src/api/pyproject.toml, .github/workflows/src-ci.yml

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Type-Narrow Optional Lookups and Verify Focused-Tier Checks | completed | P01, P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Type-Narrow Optional Lookups and Verify Focused-Tier Checks

### Context

Hosted CI run `43644223724` (job `132598509967`, `src-api` Type check) failed on PR #1727 (`deadb7144`) with two `[union-attr]` errors in `src/api/tests/test_screen_design_traceability.py` (`C1`, `C3`, `C4`). `src/api/pyproject.toml` configures `[tool.mypy] strict = true` over `src`, `tests`, and `checks`, and `[tool.ruff]` with `line-length = 100` and `select = ["E", "F", "I", "B", "UP"]` (`C2`, `C5`). Sibling `src/api/tests/test_ux_design_traceability.py` narrows optional lookups by pairing `self.assertIsNotNone(...)` with `assert ... is not None` (`C7`).

Test ownership and coverage lock:
* Canonical test target: `src/api/tests/test_screen_design_traceability.py` (no generated targets).
* Exact test removals: `none`.
* Maximum test-method additions: `0` (all 5 existing semantic traceability test methods remain intact; only static `None`-narrowing assertions are added inside 2 existing methods).
* Semantic vs regression coverage: Semantic assertions on Issue #156 screen matrix completeness, registered screens, markdown links/anchors, AST test existence, and non-acceptance wording are preserved identically; regression check runs `tests/test_screen_design_traceability.py` plus verified sibling `tests/test_ux_design_traceability.py` (`C7`).

### Intent

Align local branch `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840`, eliminate both `mypy` `[union-attr]` errors in `src/api/tests/test_screen_design_traceability.py`, pass all required `mypy`, `ruff`, and `unittest` checks in `src/api`, and record complete Cycle-2 implementation evidence while preserving all prior `.copilot-tracking/` files.

### Boundaries

* Included: Creating/switching local branch `feat/ux-156-design-traceability-1840` tracking `origin/feat/ux-156-design-traceability-1840` (`docs/ux-156-design-traceability-1840` kept intact), editing `src/api/tests/test_screen_design_traceability.py`, and writing `156-screen-design-traceability-mypy-c2-*` RPI tracking artifacts under `.copilot-tracking/`.
* Excluded: `docs/reference/research/ux/screen-design-traceability.md`, `src/api/pyproject.toml`, `.github/workflows/`, production `src/` packages, prior committed `.copilot-tracking/` files, branch deletion, history rewriting, and remote `git push`.

### Likely Targets

* `src/api/tests/test_screen_design_traceability.py`: Narrow optional `re.Match[str] | None` and `ast.ClassDef | None` values.
* `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md`: Record Cycle-2 implementation edits and validation command results.

### Dependencies

* None beyond existing `src/api` editable toolchain verified in `C2`.

### Validation Expectations

* `cd src/api && python3 -m mypy` -> `Success: no issues found in 280 source files` (exit `0`).
* `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` -> exit `0`.
* `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_screen_design_traceability.py -v` -> 5 tests `OK` (exit `0`).
* Sibling regression check: `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_ux_design_traceability.py -v` -> `OK` (exit `0`), plus `git status --short` verify no `.pyc` files are tracked and `git diff --diff-filter=D` is empty.

### Completion Evidence

* Clean diff in `src/api/tests/test_screen_design_traceability.py`, repository-local `git config --local user.email` set to `{id}+{login}@users.noreply.github.com`, passing command transcripts recorded in `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md`, reconciled plan/details checkboxes, and updated session state JSON ready for `rpi-review` (with the single non-amended local commit executed immediately after `rpi-review` writes `.copilot-tracking/reviews/2026-11-14/156-screen-design-traceability-mypy-c2-review.md`).

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Narrow `match` and `target_cls` in `test_screen_design_traceability.py`

#### Context

In `ScreenDesignTraceability.test_rows_are_complete_and_cover_every_issue`, `re.search(r"#(\d+)\]", row[0]).group(1)` fails `mypy` with `Item "None" of "Match[str] | None" has no attribute "group"  [union-attr]` (`C3`). In `ScreenDesignTraceability.test_tests_exist`, `node = next(..., None)` followed only by `self.assertIsNotNone(node, ...)` fails `mypy` on `node.body` with `Item "None" of "ClassDef | None" has no attribute "body"  [union-attr]` (`C4`).

#### Intent

Add explicit runtime + static narrowing for `match` and `target_cls` so `mypy --strict` narrows both optionals cleanly while preserving descriptive `unittest` failures even under `python -O`.

#### Boundaries

* Included: `test_rows_are_complete_and_cover_every_issue` and `test_tests_exist` in `src/api/tests/test_screen_design_traceability.py`.
* Excluded: Other methods in `test_screen_design_traceability.py` and all other files.

#### Likely Targets

* `src/api/tests/test_screen_design_traceability.py`: Replace direct `.group(1)` chaining with `match = re.search(...)`, `self.assertIsNotNone(match, row[0])`, `assert match is not None`, `seen.add(int(match.group(1)))`; rename `node` to `target_cls` and add `assert target_cls is not None` immediately after `self.assertIsNotNone(target_cls, f"{klass} not found in {path}")`.

#### Dependencies

* None.

#### Validation Expectations

* `python3 -m mypy tests/test_screen_design_traceability.py` and full `python3 -m mypy` in `src/api` pass with `0` errors; lines stay within Ruff's 100-column limit (`C5`).

#### Completion Evidence

* `git diff src/api/tests/test_screen_design_traceability.py` shows only the two narrowing blocks and passes Ruff format check.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Align Branch `feat/ux-156-design-traceability-1840`, Execute Focused-Tier Validation, Configure Noreply Git Identity, and Record Implementation Evidence

#### Context

Worktree `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` sits at `deadb7144` on local branch `docs/ux-156-design-traceability-1840` tracking `origin/feat/ux-156-design-traceability-1840`, with no local `feat/ux-156-design-traceability-1840` ref yet (`C8`). Creating and switching to local branch `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` preserves `docs/ux-156-design-traceability-1840` while satisfying caller Step 4 and PR #1727's `headRefName`. Per `.github/copilot-instructions.md` (`C8`), focused-tier validation applies to small test-only fixes: execute all planned local checks matching `src-ci.yml` (`src-api` unit test, lint/format, and `mypy` steps in `C1`), resolve `{id}+{login}@users.noreply.github.com` from `gh api user` and configure repository-local `git config --local user.email`, and verify no untracked bytecode or deleted `.copilot-tracking/` artifacts exist. To include `.copilot-tracking/reviews/2026-11-14/156-screen-design-traceability-mypy-c2-review.md` in one clean `ahead 1` commit on `feat/ux-156-design-traceability-1840` without amending, `P01-T02` leaves the verified working tree uncommitted for `rpi-review`, and post-`rpi-review` closeout executes `git commit` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` (no push) followed by verifying empty `git status --short` and empty `git diff --diff-filter=D HEAD~1..HEAD`.

#### Intent

Align local branch `feat/ux-156-design-traceability-1840`, prove the fix satisfies every caller-mandated command and repository focused-tier rule, configure repository-local Git noreply identity, and record durable implementation evidence in `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md`.

#### Boundaries

* Included: `git checkout -b feat/ux-156-design-traceability-1840` + `git branch --set-upstream-to=origin/feat/ux-156-design-traceability-1840 feat/ux-156-design-traceability-1840`; running `mypy`, `ruff check .`, `ruff format --check .`, and `unittest` (`tests/test_screen_design_traceability.py` and `tests/test_ux_design_traceability.py`) from `src/api`; configuring `git config --local user.email`; writing `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md`; reconciling plan/details markers.
* Excluded: Premature `git commit` before `rpi-review`, branch deletion, destructive commands, or `git push`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md`: Implementation summary, modified files, validation transcripts, focused-tier classification record (noting hosted CI on the new local head remains pending push), and commit-readiness confirmation.

#### Dependencies

* Completion of `P01-T01`.

#### Validation Expectations

* Zero exit status from all three required commands in `src/api` plus verified sibling `tests/test_ux_design_traceability.py`, verified `git config --local user.email` matching `{id}+{login}@users.noreply.github.com`, and `git diff --diff-filter=D` empty.

#### Completion Evidence

* Populated `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md` and checked `[x]` markers in plan and details.

#### Unresolved Items

* None.
