# Changes: listen backlog 691

* src/api/src/zava_forward/api/server.py: `_Server`, used by main().
* src/api/src/zava_forward/api/resident_demo/app.py, resident_preview/app.py: request_queue_size = 128.
* src/api/tests/test_listen_backlog.py: new tests.
* src/api/src/zava_forward/api/server.py: request_queue_size = 128 only (daemon_threads removed after independent review).
* src/api/tests/test_listen_backlog.py: burst test skips off Linux or when somaxconn < 128 and asserts >= 20 of 30; without the fix it fails (6 of 30).

## Gate (author-reported)

* Command: `python3 tools/rpi-checks.py --changed --base origin/main --lock-timeout 3300 --out /tmp/gate691final.AyEx/r`
* Receipt: /tmp/gate691final.AyEx/r/receipt.json (external, not committed). Summary: status passed, scope partial (focused tier), head 2fed4795ae6b, base fb6cdcd64f14, groups preflight, project-api, namespace, static, image-api, logo-0600, failure none.
* Later commits only touch this tracking file; the receipt covers code head 2fed4795ae6b. Independent review and hosted CI remain required.
