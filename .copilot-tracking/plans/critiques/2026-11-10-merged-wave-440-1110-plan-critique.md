<!-- markdownlint-disable-file -->
# Merged-wave 440 plan critique (2026-11-10)

One critique of the final candidate plan and details, executed once at 2026-11-10T02:05Z by the authoring agent (no nested agent, per the brief). Verdict: proceed with amendments; all findings compatible and applied directly to the details by amendment below. No finding conflicts with a confirmed decision; no user decision needed.

## Findings

* F1 (medium) R3 runs the whole `test_resident_decisions` module, so the named representative cases could be hidden inside one aggregate count. Amendment: run with `-v`, extract the pass or skip line of each named case in the research list, and report them separately from the aggregate.
* F2 (medium) R6 needs `playwright` in the owned venv, which is declared only in the `api` `dev` extra (`playwright==1.64.0`), while the cached Chromium revision (1248) may not match. Amendment: install only that declared pin in the owned venv; if the browser launch fails it is recorded as blocked (environment), not as product failure and not as a pass.
* F3 (low) R8 and R9 overlap for core `test_version` and `test_dependency_rule`. Amendment: run those two in R8 only for core and drop the core repetition from R9; R9 covers api, agents, orchestrator and importer once each. Counts stay per process.
* F4 (low) The no-source-change gate is only checked at the end. Amendment: record `git status --short` and `git diff --stat` before and after the run series, and the source tree id before and after.
* F5 (low) The finance API count has three prior values (14 and 7 in different records, and the module's current `def test` count). Amendment: count from the actual run and compare with the `def test` count in the same source, not with either history.
* F6 (low) Dry-run no-I/O is asserted by tests with a `FakeAzure`; that proves the adapter contract against a fake, not a real build. Amendment: the checkpoint must label it fake-builder evidence and not live rebuild, with the named `DryRunTests` lines extracted from R4.

## Not changed

Scope, exclusions (PR 1351, 152 helper, parent 89, 132 hooks, old worker), tier and the no-edit boundary are unchanged. The critique is not repeated for this task.
