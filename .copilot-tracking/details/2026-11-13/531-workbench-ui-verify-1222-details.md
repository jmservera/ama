# Details
Modules listed in research.md. Run core modules from src/core with `python -m unittest <dotted>` and API modules from src/api with PYTHONPATH=../core/tests:../agents/tests (documented repo form, not mvp). Logs under /tmp/log531 (outside repo); counts parsed from "Ran N tests" and skipped from the final status line. Any failure is recorded, not fixed (no src edits).

## Critique dispositions (rubber-duck, verdict Revise; executed once)
* Env isolation: run with `env -i` allowlist (PATH, HOME=/tmp/h531, ZF_DATA=/tmp/h531/data.json synthetic) instead of only unsetting two vars. Applied.
* Path verification: use venv python explicitly; print module __file__ for core/agents/api and test modules. Applied.
* Loopback HTTP in API tests is local-only (127.0.0.1), accepted and noted; no external network. Brief-mandated pip upgrade kept; failure recorded as blocker. Partially applied.
* Exit codes captured directly after each producer; missing counts recorded as unavailable. Applied.

## Implementation amendments (post-review reconciliation)
* test_workbench_live_defaults imports Playwright; it is excluded by the brief and recorded as unavailable, not run.
* Final API invocation: PYTHONPATH=tests:../core/tests:../agents/tests, `env -i` allowlist (supersedes `env -u`), local node dir added to PATH for static UI-asset tests.
* Plan phases 1-3 executed; commit step follows review.
