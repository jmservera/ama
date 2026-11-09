<!-- markdownlint-disable-file -->
# Plan: pinned-tool validation of recovered #123, 2026-11-09

Research: [research](../../research/2026-11-09/pinned-validation-123-research.md). Details: [details](../../details/2026-11-09/pinned-validation-123-details.md).

## Phases

* [ ] Phase 1: confirm pins from `src/core/pyproject.toml`; create a venv outside the repository; `pip install ruff==0.17.1 mypy==2.4.0` only.
* [ ] Phase 2: from `src/core`, run `ruff check .`, `ruff format --check .`, `mypy` and the 146-test selection with `PYTHONPATH=src:tests`; record versions, counts, skips, exits and import paths.
* [ ] Phase 3: `git diff --check`; confirm no source or manifest change.
* [ ] Phase 4: record changes and one review; commit only this evidence; write handoff.

## Stop conditions

A pinned check failing: diagnose; change core only for a concrete coupled defect, else report blocker. No push, PR edit, global install, pin loosening, full gate. Critique not separately executed; scope is a bounded rerun (author-recorded).
