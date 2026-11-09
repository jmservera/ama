---
title: "Details: #184 correction 1"
ms.date: 2026-11-08
---

* `src/api/src/zava_forward/api/live_simulator.py`: `run()` catches `StreamError`
  from `list_homes` and stops; `main()` keeps a cache used only on `HomeListError`
  and only for homes the current control still lists.
* `src/api/src/zava_forward/api/live_receiver.py`: `_watch`, `run_window(reload,
  clock, poll)`, `CONTROL_NOT_SENDING` for windows under 1 s.
* `infra/live-receiver-job.bicep`: receiver job. Simulator job file unchanged.
* Receiver grants (to be confirmed by the executor against the consumer's SQL):
  AcrPull; Event Hubs Data Receiver on `sensor-readings`; SELECT on `cases`,
  `sensor_register`, `sensor_consumer_control`, `sensor_consumer_policy`; SELECT
  and INSERT on `sensor_reading`, `sensor_delivery`,
  `sensor_data_quality_exception`.
* Tests in `src/api/tests/test_live_control.py`: `RefreshRegressionTests`,
  `ReceiverStopTests`, `ReceiverJobContractTests`.
