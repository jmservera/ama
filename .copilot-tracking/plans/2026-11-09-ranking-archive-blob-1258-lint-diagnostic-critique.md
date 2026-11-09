# Issue 1258 API wiring-test lint diagnostic critique (2026-11-09)

One original self-critique of the final candidate plan, executed once before the plan commit. It does not replace independent review.

## Verdict

Approve with three findings, all applied directly.

## Findings

* Applied: use the maintained `pyproject.toml` and the pinned 0.17.1 only; never `--isolated`, `--select`, `--fix`, `--add-noqa` or `ruff format` without `--check`.
* Applied: explicit file paths bypass the configured format exclude, so `--force-exclude` is required and the exact CI `.` commands corroborate it. Without it `server.py` would be a false format failure.
* Applied: the probes already run in research were not the committed-plan producer. The producer is re-run after the plan commit and the earlier logs are kept unchanged.

## Gate

No significant or divergent issue needs a user decision.
