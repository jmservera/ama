# Changes: 432 chat failure meter forwarding

* `src/agents/src/zava_forward/agents/chat.py`: `unavailable()` helper attaches `meter_id`/`meter_root` (str or None) to every `ModelUnavailable`; admission exits get None, post-dispatch exits take the envelope values.
* `src/agents/tests/test_chat_model.py`: 4 new tests (RED first: 4 errors, then green), incl. real `Ai` reserve/check/complete holds.
* core and dispatch.py unchanged (ids already preserved in `Ai.evidence` envelopes).

Validation: all agents test modules OK except `test_paired_report_command` (timed out at 100s in this environment, unrelated, did not complete); core `test_ai_consumption` 34 OK; ruff check/format OK; mypy src OK.
Residual: `_bounded` timeout and a raising provider return a fresh envelope without ids.
