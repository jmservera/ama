# Review: Issue #146 monitoring coverage (Refs #146)

Executed once, after implementation. Outcome: conformant with open follow-ups routed to later work. No second review.

## Assessed boundary

Diff of `feat/demo-146-bicep-monitoring-runbooks-2136` against `origin/main` ee068a4b: infra Bicep, workbook, runbook, core logging and AI-consumption markers, register and tests.

## Evidence

* `az bicep build` passes for all infra templates and modules.
* Infra tests (`test_bicep_policy`, `test_monitoring_alerts`, `test_monitoring_workbook`, `test_iothub_module`): pass. Core targeted (diagnostic logging, AI consumption, coverage): pass. Agents, importer, orchestrator suites pass. API logging, live and resident tests: pass after one fix.
* ruff check and format clean in core, api, agents, importer. mypy clean in core, agents, importer. API mypy has pre-existing playwright stub errors only.
* One review finding fixed in-task: the redaction withheld dot-leading temp file names, failing two ranking publication tests; token pattern widened and a test added.

## Findings (routed, not re-reviewed)

* F1 (Medium): the full `src/core` and `src/api` suites were not completed locally (very long run); targeted and affected suites ran. Route: hosted CI or the complete local gate before publication.
* F2 (Medium): `StorageQueueLogs` field values and the console markers are unverified against a deployed workspace. Route: synthetic drill before activation.
* F3 (Low): `import-jobs-poison` has no producer; remains a documented gap.
* F4 (Low): Container Apps `allLogs` platform export is not proven personal-data-free; needs DPO approval.
* F5 (Low): no criterion ticked; owners are proposals and approvals are absent.

## Outcome

Source-level coverage authored for the six criteria; none is operationally accepted.
