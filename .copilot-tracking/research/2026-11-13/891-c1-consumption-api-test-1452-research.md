---
title: 891 c1 consumption API test research
---

## Findings

* Failure: test_ai_consumption_api.py `test_actual_chat_adapter_preserves_metering_without_proposal_eligibility`, modes revoked and provider-failure, expects unjoined_outputs + 1.
* Cause: core/chat_panel.py now records a settled ineligible output for failed turns, joining the attempt. No unjoined leak remains.
* Disposition: executed. Planning Readiness: Ready. Coverage per mode to be confirmed by running the test.
* Fix is test-only: assert the settled output record and unchanged unjoined count.
