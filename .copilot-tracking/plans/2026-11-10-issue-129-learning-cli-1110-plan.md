<!-- markdownlint-disable-file -->
# Plan: issue 129 constructed learning-report CLI

* Task: `129-learning-cli-1110`; research: `.copilot-tracking/research/2026-11-10-issue-129-learning-cli-1110-research.md`; details: `.copilot-tracking/details/2026-11-10-issue-129-learning-cli-1110-details.md`; critique: `.copilot-tracking/plans/2026-11-10-issue-129-learning-cli-1110-critique.md`.
* Scope: LOCAL, Refs #129 and #123 only. Files: `src/core/src/zava_forward/core/learning_test_bundles.py` (module-local CLI), `src/core/tests/test_learning_test_bundles.py`, `src/core/README.md` (small section). Nothing else.

## Phases

* [ ] Phase 1: add the bounded input boundary and `main` to the module; `run_report`, `render_report`, `compare_bundle`, `BUNDLES`, comparators and zero rules untouched.
* [ ] Phase 2: add focused CLI and boundary regressions to the existing test file (red before, green after).
* [ ] Phase 3: add the command and limits to the Core README.
* [ ] Phase 4: run the targeted checks (module tests, Core configured Ruff check/format check and mypy), record in the changes file.

## Boundaries (explicit non-goals)

* No stored records, output files, database, UI, network, AI, cloud, recruitment, discovery, aggregation, price, approval, mapping or threshold inputs.
* No knowledge-base index, log or protocol edit; no registry, API, app, design, shared helper, config or dependency change.
* Real experiment, Atlas mapping, DPO retention and Finance validation stay unmet.

## Validation (owner demo targeted tier)

* Baseline preserved (exit 0, no output); module tests; real subprocess command tests; Core configured `ruff check`, `ruff format --check`, `mypy` (project configuration, no file-scoped substitute); no blanket full, `--changed`, SQL or browser gate.
