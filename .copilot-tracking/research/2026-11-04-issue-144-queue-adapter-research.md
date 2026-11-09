# Research: issue 144 queue adapter (2026-11-04)

Disposition: executed (reuse of the worker run loop research).

* Merged evidence: #294, #301, #303 (images, dispatch ports), #682 (scale load, restart audit, hosting contract), #1009 (run loop, fail-closed serve). Issue comments of 2026-10-31 and 2026-11-03 list C1 to C5 as unmet.
* Gap for C1: `TaskQueue` has only `InMemoryQueue`. Bicep already declares the `agent-tasks` and `agent-tasks-poison` queues and `QUEUE_ENDPOINT`.
* Constraint: agents identity installs no third-party packages (test_dependency_rule forbids `azure*`), so the adapter uses the Queue REST API through the standard library with an injected transport and token source.
* Planning Readiness: Ready.
