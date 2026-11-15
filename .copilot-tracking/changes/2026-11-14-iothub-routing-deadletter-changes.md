# Changes: IoT Hub routing contract tests (Refs #145)

* Added `infra/tests/test_iothub_routing_deadletter_bicep.py`: 4 compiled-template tests.
* An attempted enabled fallback plus quarantine consumer group was reverted after it failed 5 existing `test_iothub_module.py` tests that pin the disabled fallback.
* Validation: new tests 4 OK; `test_iothub_module.py` unchanged and passing at base; ruff isolated check and format clean (cache in /tmp). Hosted CI not run.
