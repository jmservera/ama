# Changes: alignment onto final main (#107 continuation)

Plan: [plan](../plans/2026-11-07-assistant-release-integrity-107-align-plan.md). Original: [changes](2026-11-07-assistant-release-integrity-107-changes.md).

* Final base origin/main 0f420dc9514db22081cb48fa733267d9d33a0d24 (score-only commit on 312fa3dcc, #1245). Rubric run 42361331168 completed success.
* Backup ref `backup/issue-107-4aa717009-pre-rebase` = 4aa717009d2a0c785b66a2426ff2ba38f31a658f. Rebase produced test commit 7fd297547; `git range-diff` reports it identical (`=`). The test and original artifacts are unchanged; no commit dropped, no source delta beyond the original test.

## Formatter diagnostic (qualification)

Canonical config `src/api/pyproject.toml` `[tool.ruff.format] exclude` lists `tests/test_assistant_release.py`; CI and `tools/rpi-checks.py` run `ruff format --check .`, which passes (116 files). Explicit-path `ruff format --check tests/test_assistant_release.py` bypasses the exclusion and reports "would be reformatted" for both the base file (baseline, before the test) and the candidate. Whether the added block alone contributes was not separated; the file is deliberately excluded, so I did not reformat legacy code or the added block, and I claim no explicit-path pass.

## Results on final head (from `src/api`, PYTHONDONTWRITEBYTECODE=1, PYTHONPATH=tests:../core/tests:../agents/tests)

| Command | Result |
| --- | --- |
| `ruff check .` (src/api, src/core) | passed |
| `ruff format --check .` | 116 files already formatted |
| `mypy` | no issues, 188 files |
| `unittest test_assistant_release -q` | 46 OK, exit 0 |
| `unittest test_assistant_release test_assistants test_continuity -q` | 188 OK, 58 skipped |

All 58 skips: 'needs disposable SQL Server (ZF_TEST_MSSQL=1)'. No browser skips in these selectors. Not run: FULL gate, SQL Server, images, scanners, heavy lock, push.
