# Plan: issue 184 hardening test parameter

* [ ] Phase 1: in the jobs loop of the hardening test, resolve `[parameters('containerHardening')]` to the compiled parameter defaultValue and assert it equals 'enforced'; assert the template default itself is 'enforced'.
* [ ] Phase 2: run infra unittest group, ruff format check, squash to one commit.

Critique (single pass, 2026-11-21): verdict proceed. Compatible findings applied: the resolver must leave non-parameter values untouched and fail on an unknown parameter so the control is not relaxed; assert the resolved value. Bicep defaults unchanged.
