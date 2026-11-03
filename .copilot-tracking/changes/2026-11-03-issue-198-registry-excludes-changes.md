# Issue 198 changes: drop dead mvp excludes (2026-11-03)

* `.github/rubric/artifacts.json`: removed `mvp/data/**` and `mvp/web/vendor/**` excludes from `solution-code`.
* `.github/rubric/README.md`: recorded the removal and the no-change score expectation; removed "legacy exclusions remain defensive"; added the 17 count next to the stale 19.
* No knowledge-base files changed, so no `log.md` entry.

## Validation

* Run: JSON parse (pass); `test_prepare.py` 72 passed, 1 failed. The failure, `test_given_pr_deleting_scored_file_when_gated_then_drop_counts`, is the one known seed-66 pre-existing failure recorded in the README; not re-run on main in this session.
* Run: ruff on `.github/rubric/scripts` reports 17 errors and mypy reports 1 (`prepare.py:336`). No Python file changed, so these are pre-existing and not touched.
* Not run: gate, benchmarks, full suites, the other rubric test files, the rubric workflow itself.
* Tier: focused. No security, infrastructure, SQL or deployment change.

## Divergence

* A first attempt to edit `artifacts.json` through a Python one-off matched nothing and changed no file; the edit was then made with the edit tool.
