<!-- markdownlint-disable-file -->
# Issue 189 C3 type applicability changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/type-applicability-189-c3-plan.md). Refs #189 only. Source commit 66ceb71f9 (tree 7471ffee4) on planning commit 9ab0eb858.

## Applicability result

The maintained CI command mypy (src-ci.yml line 94, from src/api, strict, files src tests checks, mypy 2.4.0) applies to both files. Main ef28d4da4 in an isolated worktree and venv: exit 0, 199 files. Branch 795f871f9 before C3: exit 1, 8 errors, 202 files, all in two files added by #189 (522adc394) and absent from main. The C2 wording "pre-existing" is corrected: they were introduced by this workstream; the old claim and failed run stay preserved in capture-189-c2-browser.

## Source change (two files, +23/-7)

* tests/test_simulator_admin.py: SessionProvider Protocol; typed Callable aliases for auth.PasswordProvider, test_auth.principal and Base.setUp; removed the unused type-ignore on the class line; one narrowing guard (assert user is not None).
* checks/simulator_control_browser_check.py: typed make_provider and make_app aliases at the two construction sites.
* No Any added (Any was already imported and used), no cast, no ignore, no pyproject.toml change, no deleted check. The Stop wait, file assertion and axe lines are not in the diff. Existing Provider, Application and handler Any aliases are left as they were.

## Validation (demo-targeted tier; CI install profile, ruff 0.17.1, mypy 2.4.0; raw files outside the repository)

| Check | Exit | Result |
|-------|------|--------|
| mypy (src/api) | 0 | no issues in 202 files |
| ruff check . and ruff format --check . | 0 and 0 | passed, 127 files formatted |
| test_simulator_admin | 0 | 27 tests OK, 0 skips |
| test_live_control | 0 | 34 tests OK, 0 skips |
| browser/axe check x5 | 0,0,0,0,0 | 13 axe scans each, 0 violations |
| delayed-Stop probe old wait and new wait | 1 and 0 | old fails deterministically, new passes: synchronisation intact |

One invocation error (unittest tests.test_simulator_admin without the tests path) is retained as superseded-invocation-error files and was rerun via discover. Five browser passes are evidence, not proof. Not run: core suites, SQL, Azure, models, global matrix, rpi-checks, workspace scripts. Web guidelines review: not applicable, no web UI file changed. Raw evidence: capture-189-type-applicability/ (60 files incl. main-baseline/, hashes.sha256 sha256 af9304687153e80f03bd39926483e1dae217ddbeb7fefebc2f585ec74800b09a, verified).

## Cycle ledger

C1, C2, C3 spent; two of five remain; no reset or grant.
