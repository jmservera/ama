<!-- markdownlint-disable-file -->
# Changes: Issue #203 criteria 1 and 2

Plan: [../../plans/2026-11-13/issue-203-verify-cleanup-references-plan.instructions.md](../../plans/2026-11-13/issue-203-verify-cleanup-references-plan.instructions.md)

## Added

* `tools/check-legacy-references.py`: file-class policy for retired `mvp/` and `prototype/` paths (archive tag `v0.21.0` in the first 60 lines or within 10 lines), package names only in dated records or guards, and relative-link resolution for links on lines changed since the merge base (all lines for untracked files; `--files` and `--all-links` modes).
* `tools/test_check_legacy_references.py`: 7 tests, including a repository-wide zero-violation assertion.

## Modified

* Architecture diagrams (`zava-forward-{executive,technical}-architecture.excalidraw`): 25 `sources` locators repointed from `mvp/zavaforward_mvp/...` to existing `src/` files; rendered SVG and PNG have no such strings.
* Archive tag wording added beside retained history: rubric README, ADR 0001 and 0002, proper-warm PRD, gap analysis, Decision 1 specification, synthetic data README, `infra/README.md`, `src/*/README.md`, `src/*/pyproject.toml` comments, `src/core/tests/dataset.py` docstring, `tools/rename-zava.md`.
* `docs/reference/README.md`: lint checklist names the new check. `docs/reference/log.md`: one appended entry.

## Not changed

Regulatory snapshots, earlier log entries, historical `.copilot-tracking/` artifacts, `case_study_48_original.md`, `memory.md`, workflow names and files (Issue #202).

## Divergences and validation

* Link scope is changed lines, not whole changed files: `log.md` is append-only and holds 17 historical broken links that cannot be rewritten. `--all-links` reports 3582 historical link issues across all tracked Markdown (informational).
* `python3 tools/rename-zava-tests.py`: 25 tests pass in a venv with `tools/rename-zava-requirements.txt`; with system Python it errors on missing `pptx` and `PIL` identically before and after the change.
* `python3 -m unittest tools/test_check_legacy_references.py` OK; checker against `origin/main`: 0 reference and 0 link violations in 19 documents; `ruff check` and `ruff format --check` on the new files pass (the pre-existing `tools` directory has other ruff findings).
