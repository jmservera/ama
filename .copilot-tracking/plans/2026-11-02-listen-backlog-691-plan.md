# Plan: listen backlog 691

* [x] Add `_Server` (request_queue_size=128, daemon_threads) to server.py and use it in main().
* [x] Set request_queue_size=128 on resident_demo and resident_preview `_Server`.
* [x] Regression test `src/api/tests/test_listen_backlog.py`.
* [x] Gate: `python3 tools/rpi-checks.py --changed --base origin/main --lock-timeout 600`.
* Critique (single pass): minimal and compatible; no conflicts. Does not close 691; live verification after deploy is required.
