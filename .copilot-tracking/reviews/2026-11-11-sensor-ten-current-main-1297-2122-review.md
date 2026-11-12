---
title: Sensor ten-test MSSQL current-main review (issue 1297, AC2)
ms.date: 2026-11-11
---

Review execution: executed once, by the implementing agent against the committed-candidate files (not independent). Independent exact-head review remains required. Changes: [changes](../changes/2026-11-11-sensor-ten-current-main-1297-2122-changes.md).

## Outcome

Conformant for the bounded scope: the plan's gates all held (non-blocking lock, resources, proven loopback ownership, exact ten IDs, zero skips, exit 0, verified cleanup, no source edits). Not a conformance claim for AC5 or the whole issue.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Not a runner-dispatched receipt

* Evidence: direct selector invocation on host Python with cached image; the runner's venv, pull and `SQL_SELECTORS` steps were not exercised.
* Destination: AC5 full local gate under the coordinator's separate admission.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Self-review only

* Evidence: the review was produced by the same agent that ran the observation.
* Destination: coordinator independent exact-head assessment of the raw log and tree.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Stale editable installs

* Evidence: the host's editable `zava_forward` packages point at another checkout; source identity here rests on `PYTHONPATH` precedence proven by printed `__file__` paths.
* Destination: accepted residual; no repair attempted.

## Adverse observations

* A first set comparison against the runner IDs failed because of a harness regex mismatch (IDs include the module path); corrected in the checker only, the test output was unchanged. No test failure, retry or SQL rerun occurred.
