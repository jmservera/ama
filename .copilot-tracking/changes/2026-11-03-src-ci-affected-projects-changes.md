# Changes: src-ci affected projects (2026-11-03)

* `.github/workflows/src-ci.yml`: new `src-changes` job; dynamic matrix; step gating; `if` on namespace and mssql; path filter and namespace job include the new tool and tests. Job names, concurrency cancel-in-progress and workflow_dispatch/push behaviour unchanged (all selected).
* `tools/ci-affected.py`, `tools/test_ci_affected.py`: selection logic and 13 unit tests.
