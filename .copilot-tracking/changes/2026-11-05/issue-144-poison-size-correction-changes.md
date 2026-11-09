# Changes: issue 144 poison-copy size correction (2026-11-05)

Plan: [plan](../../plans/2026-11-05/issue-144-poison-size-correction-plan.md).

* `queue_azure.py`: new `POISON_TEXT_BYTES` (45,000) and `poison_text()`; `_poison` now stores a base64 copy of at most 45,000 raw UTF-8 bytes (60,000 base64 bytes, under 65,536). Longer originals keep a valid-UTF-8 prefix after an explicit `[truncated original_bytes=N]` marker. Write-before-delete and failed-write retention are unchanged.
* `test_queue_azure.py`: five regressions (large ASCII, multibyte, oversized valid task over the delivery limit, small message kept whole, large-message failed write keeps the message).

## Light commands (PYTHONDONTWRITEBYTECODE=1, external caches)

* Fail-before: disposable `git archive` copy of the previous head with the new tests in `/tmp/p144-pre`: 21 run, 3 failures (ASCII, multibyte, oversized task), exit 1; the small and failed-write cases passed as expected.
* After: `unittest test_queue_azure test_worker test_dispatch test_dependency_rule` with PYTHONPATH to this worktree, import path verified: 46 OK, exit 0. `ruff check --no-cache`, `ruff format --no-cache --check` (43 files), `mypy --cache-dir=/tmp/mypy-144c` (47 files incl. tests): clean.

## Not run

FULL gate (pending; 233 holds heavy admission), browser, SQL, Docker, scanners, Azure. The earlier passed receipt for `9f14e6cb9` is historical, not validation of this head.
