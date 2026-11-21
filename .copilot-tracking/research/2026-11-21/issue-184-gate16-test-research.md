---
title: Issue 184 gate run16 test fix research
ms.date: 2026-11-21
---

# Research: gate run16 failure in ReceiverJobContractTests

* Disposition: executed. Planning Readiness: Ready.
* Base: candidate f19ef3715 (branch reset to it from d2585a4c9).
* Cause: infra/live-receiver-job.bicep line 93 is `triggerType: empty(cronExpression) ? 'Manual' : 'Schedule'`, line 36 `param cronExpression string = ''`, lines 96-97 select manual or schedule config. The test in src/api/tests/test_live_control.py asserts the literal `triggerType: 'Manual'`.
* Fix scope: test only; Bicep unchanged. Tier: focused (no src change).
* Issue #184 acceptance criteria: all three are already ticked; none is unticked, so no new live proof is required for this test-only change.
