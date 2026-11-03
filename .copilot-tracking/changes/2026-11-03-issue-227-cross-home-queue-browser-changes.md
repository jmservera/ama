# Changes: issue #227 cross-home queue browser evidence

* `src/api/checks/safety_screens_browser_check.py`: added `check_queue`, extracted `scan_axe`.
* `src/api/README.md`: describes the added coverage.
* No production code or knowledge-base file changed, so no log.md entry.

Validation run (focused): ruff check pass; mypy pass; browser check passes for both roles (all PASS, 0 FAIL) with PYTHONPATH pointing at this worktree (installed editable packages belong to another worktree). Axe scan SKIPPED (pinned axe file not available). Not run: gate, full suites, benchmarks, assistive technology.
