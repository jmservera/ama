# Plan
* Change the `Shared queue` exclusion anchor in `src/api/checks/connected_home_browser_check.py` from `loadPage(0)` to `loadPage(start)`.
* Run the targeted tests, ruff and mypy. No manifest digest change.
