<!-- markdownlint-disable-file -->
# Critique: #185 main integration plan (2026-11-10)

Executed once, by the implementing agent, on the final candidate plan. No nested agent.

* C1: A clean `merge-tree` does not prove a working composition. Mitigated by post-merge selectors, TOML parse and mypy. Applied.
* C2: Pipelines can mask a failing test; each command uses `pipefail` and records its own exit. Applied.
* C3: A new main change might reach the adapter indirectly; research found no reference and the dependency-rule test is in the selector. Accepted.
* C4: Main-only test files are not exercised here; full discovery stays not run. Accepted, stated as a limit.
* C5: Topic extra and main README additions could collide; the merge result is inspected for both. Applied.

Verdict: proceed. No conflict with a confirmed user decision; no user decision needed.
