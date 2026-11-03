# Plan: issue 230 programme check hardening

1. Edit the 230 scenario of `src/api/checks/role_screens_browser_check.py` for the six review follow-ups (details in the research file).
2. Update the story 230 paragraph in `src/api/README.md`.
3. Validate: story 230 browser check, `test_programme_screen` and `test_role_screens_conformance`, ruff, mypy with `--cache-dir=/tmp/mypy-230`. No gate, benchmarks or full suites.

Critique (executed once, inline): scope is test-only and creates no new behaviour; the stale "original text preserved" note sits in an earlier changes file whose original text must stay, so it is superseded in the changes file of this slice instead of rewritten. Accepted.

Stacked later slices: portfolio returned-work endpoint; assistive-technology validation (#155); Fluent adoption check (#150).
