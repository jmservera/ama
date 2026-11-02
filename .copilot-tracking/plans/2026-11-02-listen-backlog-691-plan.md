# Plan: listen backlog 691

* [x] Add `_Server` (request_queue_size=128 only; daemon_threads removed after review as an unneeded shutdown change) to server.py and use it in main().
* [x] Set request_queue_size=128 on resident_demo and resident_preview `_Server`.
* [x] Regression test `src/api/tests/test_listen_backlog.py`.
* [x] Gate: `python3 tools/rpi-checks.py --changed --base origin/main --lock-timeout 3300 --out <new external dir>`.
* No separate critique artifact exists; the plan was self-checked only. Refs 691 only; live verification after deploy is required.
