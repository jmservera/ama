<!-- markdownlint-disable-file -->
# Details: issue 440 fourth stabilization checkpoint

## Phase 1

* Fetch `origin/main`, fast-forward the topic branch, record commit, tree, BRD/PRD/ADR/coordinator blob identities and the 323-commit range.
* List merged PRs already delivering #440 (#461, #688, #729, #689, #720, #733).

## Phase 2

Environment `/tmp/venv-440` (pip only, five `src/` distributions editable, ruff, mypy, playwright package without browsers). `PYTHONDONTWRITEBYTECODE=1`, mypy `--cache-dir=/tmp/mypy-440`.

* Per project: `ruff check .`, `ruff format --check . --no-cache`, `mypy`.
* ADR 0006 `tests.test_dependency_rule` in core, agents, api, orchestrator and importer.
* API focused: `tests.test_dependency_rule tests.test_keepalive tests.test_auth tests.test_entra_authoritative tests.test_ai_boundary tests.test_design_system`.
* Not run: full suites, benchmarks, SQL Server parity, Docker, Chromium, the gate.

## Phase 3

* Append "Fourth local stabilization checkpoint (2026-11-04)" to `docs/architecture/cutover-evidence-pack.md`.
* Append a dated entry to `docs/reference/log.md` with a blank line before the heading.

## Phase 4

Commit with the repository-local noreply email, Conventional Commit and Copilot trailer; push without force; open a PR to `main` using `Refs #440`.
