# Issue 1258 C6 critique (2026-11-09)

One original independent critique, executed once by a separate read-only `rubber-duck` agent against the final candidate plan, research and details before any commit, merge or source edit. Not repeated.

## Execution and verdict

Executed. Verdict: Revise. Four blocking and two non-blocking findings, two unsupported claims. No finding conflicts with a confirmed owner decision and none needs a user decision.

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | `ranking.snapshot` is untyped and called at test lines 74, 232 and 304; annotating `snap` alone does not fix them | Applied: details annotate the `ranking.snapshot` signature only, with a mypy re-check |
| 2 | Blocking | Fixture `dict[str, bytes]` conflicts with the transport body `bytes or None` at fixture line 69 | Applied: `_put` narrows the optional body explicitly with a 400 response |
| 3 | Blocking | Formatter leaves E501 for the docstring at wiring test line 361 | Applied: a manual same-text wrap is planned and verified |
| 4 | Blocking | API test path `../core/tests` from `src/api/tests` is wrong | Applied: run from `src/api` with the CI `PYTHONPATH` form |
| 5 | Non-blocking | Profile matrix ambiguous | Applied: core regressions run in both venvs; API wiring in the api venv |
| 6 | Non-blocking | Merge preservation evidence unspecified | Applied: name targeted tests and diff merged hunks against both parents |

Unsupported claims: the explanation of why C5 missed mypy is removed from the research; the `snap` return shape is verified by mypy, with the `ignore_errors` limitation recorded.

## Gate

Plan corrected directly; no edit, merge or push has occurred.
