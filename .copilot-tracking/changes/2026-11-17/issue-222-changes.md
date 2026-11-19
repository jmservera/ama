# Issue 222 changes

Status: complete (doc-only). Tier FOCUSED.

* docs/reference/research/evaluation/cohort-evaluation-review-pack.md: appended "Executable evidence re-measured (2026-11-17, Refs #222)"; draft banner and AC table preserved.
* docs/reference/log.md: appended 2026-11-17 entry.

Validation: core `test_cohort_eval` 25 OK; agents cohort tests 36 OK; runner with and without --defects measured (see research). `git diff --check` clean; relative link to src/agents/README.md resolves. mypy, ruff format, and browser checks not applicable (no source change). sloptrim detect.py not found locally; scoring unavailable. No divergences. Criterion 6 unmet.
