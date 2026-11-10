# Issue 1258 API wiring-test lint diagnostic review (2026-11-09)

Refs #1258. One original self-review, executed after implementation against `.copilot-tracking/changes/2026-11-09-ranking-archive-blob-1258-lint-diagnostic-changes.md`. Not repeated, and not a substitute for independent exact-head review.

## Execution and outcome

Executed once. Outcome: diagnostic complete; maintained pinned lint check FAILS. Not conformant for publication.

## Checks

* Order: research, plan, details and critique were committed (`a7ae689a`) before the producer ran. The pre-plan probes are labelled as research and kept.
* The producer used the maintained `pyproject.toml` and pinned 0.17.1 with no `--isolated`, rule selection, suppression, `--fix` or format write. `git status --short` empty before and after.
* Exits are genuine (1, 1, 1, 1) with hashed external logs.
* Source equivalence to `9b1e2567` and tested head `59d8ad8a` proven by blob ids and a 1358-file non-tracking manifest hash.

## Findings

* F-1 (blocking for publication): 10 Ruff errors (9 E501, 1 I001) plus one format diff in `src/api/tests/test_ranking_publication_wiring.py`, inherited byte-identically from C5 and applicable to the `src-api` CI Lint step.
* F-2: the earlier hosted-equivalent "ruff clean" claim for C5 never covered this file.

## Routing

Publication stays blocked. A new explicit finite owner source-correction grant is needed (a lint-only fix of the wiring test and its format). It must not be done through a child task or another issue's budget. Hosted CI, independent exact-head review and human approvals remain outstanding.
