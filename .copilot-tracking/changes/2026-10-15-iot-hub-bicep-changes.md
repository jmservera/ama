# Changes: IoT Hub Bicep module (issue 140)

* Added infra/modules/iothub.bicep and infra/tests/test_iothub_module.py.
* Edited infra/main.bicep, infra/modules/network.bicep, infra/README.md, docs/adrs/0003-*.md, docs/reference/log.md.
* Validation: az bicep build and lint clean; infra tests pass; mvp tests: 565 pass (84 skipped).
* Divergence: live what-if not run (no subscription access); recorded as open.
