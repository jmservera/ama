# Review: deploy.py --dry-run

Execution: once. Outcome: conformant for the scoped change, with open items routed to later work.
* Non-dry-run command construction is unchanged (refactored into a helper; existing 19 tests pass).
* Dry-run does zero I/O; verified by an empty fake-az call log.
* Open: full-suite error from missing orchestrator package (environment, pre-existing). Issue #148 criterion 4 (disposable Azure from-empty run) remains unmet, so use `Refs #148`, not Closes.
* Follow-ups: 1) install `src/orchestrator` and rerun the full suite; 2) disposable Azure rehearsal under human approval.

## Cycle 1 correction review

* Outcome: conformant for the `EXE001` finding. Diff limited to mode change, formatting and tracking notes. Directory-wide ruff findings in unrelated files are pre-existing and routed to later work.
