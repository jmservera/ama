# Changes: issue 749 stored chat rules fallback

Recorded after implementation (2026-11-01) from commit 1ab45d61f on branch fix/employee-chat-grounded-when-ai-off (Refs #749, PR #752).

* `src/core/src/zava_forward/core/chat_panel.py`: stored-path rules-based grounded fallback plus `RULES_NOTE`.
* `src/core/tests/test_chat_panel.py`: `StoredRulesFallbackTests` (fails before the fix).
* `src/api/tests/test_chat_panel.py`, `src/api/tests/test_ai_consumption_api.py`, `src/agents/tests/test_chat_eval.py`: expectations updated to the new behaviour.
* `.copilot-tracking/reviews/2026-11-01/issue-749-review.md` and the rpi-sessions state file: review evidence.
* Validation (per review record): core chat tests 118 OK; focused tier; no SQL, infra or security surface change. The API and agents test runs are not recorded in the review artifact.
* Not done: live redeploy verification (owner).
* Gap: no pre-implementation critique was run; research and plan were written afterwards.
