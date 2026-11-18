---
title: "RPI Phase Details: PR #1792 c2 Ruff Format Remediation (Issue #100)"
description: "Evidence-backed phase details for Issue #100 PR #1792 c2 Ruff line-length=100 formatting and Focused validation"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-100-mgmt-tokenomics-c2-lint
* Task slug: insight-100-mgmt-tokenomics-c2-lint
* Related plan: .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-research.md (`C1`-`C8`), .github/workflows/src-ci.yml, src/core/pyproject.toml, src/api/pyproject.toml

## Phase Index

| Phase ID | Name                                                               | Status | Detail sections        |
|----------|--------------------------------------------------------------------|--------|------------------------|
| P01      | Package-Scoped Ruff Formatting and AST Invariance                  | Complete | P01, P01-T01, P01-T02 |
| P02      | Focused Type-Check, Unit-Test Validation, and Git Identity Preparation | Complete | P02, P02-T01     |

<!-- rpi:phase id=P01 -->
## P01: Package-Scoped Ruff Formatting and AST Invariance

### Context

Hosted CI on `PR #1792` (`d3a2c5405`) passed `8/10` jobs and passed Step 5 (`Unit tests and dependency-rule test`) in both `src-core` (`132805147399`) and `src-api` (`132805147369`), failing only Step 6 (`Lint`: `ruff check . && ruff format --check .` inside `src/${{ matrix.project }}`) (`C1`, `C2`). Both `src/core/pyproject.toml` and `src/api/pyproject.toml` set `[tool.ruff] line-length = 100` (`C3`, `C4`), whereas `d3a2c5405` formatted `tokenomics.py` and `progress.py` using Ruff's repo-root default `line-length = 88`.

### Intent

Reformat `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py` from their respective package directories so `ruff check . && ruff format --check .` passes cleanly in both packages with zero AST changes.

### Boundaries

* Included: Running `python3 -m ruff format` inside `src/core` on `src/zava_forward/core/tokenomics.py` and inside `src/api` on `src/zava_forward/api/progress.py`; verifying `ruff check .`, `ruff format --check .`, and AST equivalence against `d3a2c5405`.
* Excluded: Any non-whitespace/non-formatting edits, edits to any other file in `src/core` or `src/api`, or edits to `pyproject.toml`.

### Likely Targets

* `src/core/src/zava_forward/core/tokenomics.py`: Collapse/re-wrap 5 line-length-88 hunks to `line-length = 100` (`C5`).
* `src/api/src/zava_forward/api/progress.py`: Re-wrap `dict(tokenomics.store_ai_consumption_economics(...))` in `_ai_economics` to `line-length = 100` (`C6`).

### Dependencies

* None.

### Validation Expectations

* `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check .)` exits `0`.
* `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check .)` exits `0`.
* `ast.dump` comparison between `git show d3a2c5405:<path>` and working-tree `<path>` succeeds for both files.

### Completion Evidence

* Clean exit (`0`) of `ruff check .` and `ruff format --check .` in both `src/core` (`302 files already formatted`) and `src/api` (`214 files already formatted`), `git diff --stat` showing only those 2 source files modified, and passing AST equality check recorded in `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Format `src/core/src/zava_forward/core/tokenomics.py` and verify `src/core` Ruff + AST invariance

#### Context

Read-only `ruff format --check --diff .` inside `src/core` identified `src/zava_forward/core/tokenomics.py` as the sole unformatted file out of 302 checked files, with 5 expression-wrapping hunks (`_reconcile_ledger(...)`, `resolved_ts` compound `if`, `hashed_id` ternary, `resolved_quality` ternary, and `_ratio_str(billed_decimal, accepted_outcome_count)`) (`C5`).

#### Intent

Apply `src/core`-scoped `ruff format` to `src/zava_forward/core/tokenomics.py` and confirm `ruff check .`, `ruff format --check .`, and AST equality.

#### Boundaries

* Included: `src/core/src/zava_forward/core/tokenomics.py`.
* Excluded: All other files under `src/core/`.

#### Likely Targets

* `src/core/src/zava_forward/core/tokenomics.py`: Ruff formatting at `line-length = 100`.

#### Dependencies

* None.

#### Validation Expectations

* Run `(cd src/core && python3 -m ruff format src/zava_forward/core/tokenomics.py && python3 -m ruff check . && python3 -m ruff format --check .)`.
* Verify `ast.dump(ast.parse(...))` matches `d3a2c5405:src/core/src/zava_forward/core/tokenomics.py`.

#### Completion Evidence

* `All checks passed!` and `302 files already formatted` in `src/core`, plus AST-equivalence pass.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Format `src/api/src/zava_forward/api/progress.py` and verify `src/api` Ruff + AST invariance

#### Context

Read-only `ruff format --check --diff .` inside `src/api` identified `src/zava_forward/api/progress.py` as the sole unformatted file out of 214 checked files, re-indenting `dict(tokenomics.store_ai_consumption_economics(...))` inside `_ai_economics` (`C6`).

#### Intent

Apply `src/api`-scoped `ruff format` to `src/zava_forward/api/progress.py` and confirm `ruff check .`, `ruff format --check .`, and AST equality.

#### Boundaries

* Included: `src/api/src/zava_forward/api/progress.py`.
* Excluded: All other files under `src/api/` (`server.py` remains untouched under `[tool.ruff.format] exclude`).

#### Likely Targets

* `src/api/src/zava_forward/api/progress.py`: Ruff formatting at `line-length = 100`.

#### Dependencies

* None.

#### Validation Expectations

* Run `(cd src/api && python3 -m ruff format src/zava_forward/api/progress.py && python3 -m ruff check . && python3 -m ruff format --check .)`.
* Verify `ast.dump(ast.parse(...))` matches `d3a2c5405:src/api/src/zava_forward/api/progress.py`.

#### Completion Evidence

* `All checks passed!` and `214 files already formatted` in `src/api`, plus AST-equivalence pass.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Type-Check, Unit-Test Validation, and Git Identity Preparation

### Context

Repository validation instructions (`owner decision D4, 2026-11-01, refined by issue #1294`) assign small non-gate Python formatting fixes to the Focused tier (`C8`). Research Wave 3 (`C7`) found that running `-p "test_tokenomics*.py"` in `src/core` runs `test_tokenomics_comparison.py` without `test_management_tokenomics_invariant_100.py`, and running `-p "test_management_tokenomics_100.py"` in `src/api` runs `0` tests because the `d3a2c5405` module is named `test_management_tokenomics_api_100.py`. Running both the exact caller commands and `-p "test_*tokenomics*.py"` (including `tests` on `src/api` `PYTHONPATH`) ensures full execution of every Issue `#100` unit and HTTP test alongside strict `mypy` in both packages.

### Intent

Execute all Focused `mypy` and `unittest` checks across `src/core` and `src/api`, record exact test counts and exit codes in the implementation changes artifact, and confirm repository-local privacy-safe git identity (`{id}+{login}@users.noreply.github.com`) so that once single-pass `rpi-review` writes the final review and session-state artifacts, a single clean local commit captures the entire `c2` deliverable without pushing.

### Boundaries

* Included: `mypy` in `src/core` and `src/api`; Focused `unittest` runs in `src/core` and `src/api`; `gh api user` + `git config --local` privacy-safe email verification; post-Review atomic local `git commit` on `feat/insight-100-mgmt-tokenomics` with `Refs #100` and `Co-authored-by` trailer.
* Excluded: `git push`, `git commit --amend`, rebasing, or changing global git configuration.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-changes.md`: Implementation and validation evidence log.
* Repository-local `.git/config` (worktree-local git config): Verify `user.email` matches `{id}+{login}@users.noreply.github.com`.

### Dependencies

* P01 (`P01-T01`, `P01-T02`).

### Validation Expectations

* `(cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_tokenomics*.py" -q)` exits `0`.
* `(cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_*tokenomics*.py" -v)` exits `0` and executes both `test_tokenomics_comparison.py` and `test_management_tokenomics_invariant_100.py` (`6` invariant tests).
* `(cd src/api && PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_management_tokenomics_100.py" -q)` (caller command observed) plus `(cd src/api && PYTHONPATH=../core/src:../agents/src:src:tests:../core/tests:../agents/tests python3 -W error::ResourceWarning -m unittest discover -s tests -p "test_*tokenomics*.py" -v)` exits `0` and executes `test_management_tokenomics_api_100.py` (`2` multi-endpoint HTTP tests).
* `(cd src/core && PYTHONPATH=src python3 -m mypy)` and `(cd src/core && python3 -m mypy)` exit `0`.
* `(cd src/api && PYTHONPATH=../core/src:../agents/src:src python3 -m mypy)` and `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` exit `0`.

### Completion Evidence

* Zero-error `mypy` outputs across 355 `src/core` files and 298 `src/api` files, verified non-zero executed test counts across all three tokenomics test suites, reconciled `changes.md`, and clean post-Review `git status --short` on local commit atop `d3a2c5405`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run Focused `mypy` and `unittest` suites across `src/core` and `src/api` and verify local git identity

#### Context

`src-ci.yml` runs bare `mypy` inside `src/core` and `src/api` (`C1`), and `.github/copilot-instructions.md` requires running `python3 -m mypy` inside modified `src/<project>` directories plus resolving the authenticated GitHub user via `gh api user` to configure `{id}+{login}@users.noreply.github.com` locally before committing.

#### Intent

Confirm type-checking, unit tests, and repository-local git identity all pass cleanly on the formatted codebase.

#### Boundaries

* Included: Executing `mypy`, `unittest`, and `gh api user` / `git config --local` checks; recording validation results in `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-changes.md`.
* Excluded: Modifying test files or pushing to remote.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-changes.md`: Record exact command results.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* All `mypy` and `unittest` commands listed under `P02` exit `0`, and `git config user.email` matches `{id}+{login}@users.noreply.github.com`.

#### Completion Evidence

* Exact command outputs and counts recorded in `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-changes.md`.

#### Unresolved Items

* None.
