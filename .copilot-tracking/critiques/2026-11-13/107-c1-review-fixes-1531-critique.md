# Plan critique: #107 F1-F4 (1531)

Executed once by `rubber-duck`. Verdict: Revise (3 findings), all compatible; applied directly.

* C1 admission (`ai_consumption.py` price-register model regex allows 120) disagrees with the 80 limit: tighten to 80 and reject secret shapes at admission. Accepted.
* C2 existing tests expect old length behaviour (`test_assistants_identity.py`, `test_ai_consumption_api.py:1146`): update, using hyphenated 80/81 boundary values. Accepted.
* C3 shared limit must also cover `ai.py:220` (120) and `bounded_model` (512): all use one `IDENTITY_CHARS = 80`. Accepted.
