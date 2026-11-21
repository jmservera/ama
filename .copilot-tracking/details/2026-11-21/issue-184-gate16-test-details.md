---
title: Issue 184 gate run16 test fix details
ms.date: 2026-11-21
---

# Details

Phase 1 in `ReceiverJobContractTests.test_receiver_job_is_manual_with_its_own_identity_and_command`: replace the needle with `triggerType: empty(cronExpression) ? 'Manual' : 'Schedule'`, add `param cronExpression string = ''`, `manualTriggerConfig: empty(cronExpression) ?` and `scheduleTriggerConfig: empty(cronExpression) ? null`.
Phase 2 validation: sequential unittest runs, ruff check and format, mypy.
