<!-- markdownlint-disable-file -->
# Details: Issue #201 current-main evidence checkpoint

## Phase 1: local checks

* Python 3.12.3; `python3 -m venv /tmp/venv-201-2333`; `pip install ruff==0.17.1 ./src/core ./src/agents ./src/api pillow python-pptx PyYAML`.
* Commands: `python3 tools/rename-zava-tests.py`; `python -m unittest tests.test_scenario_manifest` and `tests.test_needs_inventory` from `src/core`; `ruff check .` and `ruff format --check .` in each `src/<project>`; `tests.test_dependency_rule` in each project; `git ls-files mvp prototype`; a grep for `mvp`, `prototype`, `zavaforward_mvp` imports in `src`, `infra`, `tools`.

## Phase 2: pack section

* Append "Current-main cut-over local verification (2026-11-13, Refs #201)" to `docs/architecture/cutover-evidence-pack.md`: identity pin, command table, criterion map (proven local, unproven, live or owner gated), limits.

## Phase 3: validation

* Relative-link check of the new section, ASCII scan of added lines, `git diff --check`.

## Phase 4: review and commit

* Review artifact with raw outputs; Conventional Commit with the Copilot trailer; no push; remove the venv.
