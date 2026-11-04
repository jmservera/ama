# Changes: issue #350 slice 1 (2026-11-04)

* Added `test_anonymous_api_is_401_for_browser_style_requests_and_pages_still_redirect` to `src/api/tests/test_auth.py`.
* No product, infrastructure or knowledge-base content changed other than a `docs/reference/log.md` entry.

Validation (focused tier): `python3 -m unittest test_auth` in `src/api` with PYTHONPATH set to the sibling `src/*/src` and test folders: 41 tests OK. `ruff check` and `mypy --cache-dir=/tmp/mypy-530` on the file: clean. Not run: complete gate, benchmarks, full suites, any live Azure or browser check.

Divergence: branch is `feat/issue-350-r5` because `feat/agent-chat-skills-530` is checked out in another worktree.
