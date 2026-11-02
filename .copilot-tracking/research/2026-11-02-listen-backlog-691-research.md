# Research: listen backlog for employee app (issue 691 follow-up)

* Disposition: executed. Planning Readiness: Ready.
* Evidence (issue 691 latest comment, PR 780): after PR 764 deploy, bursts of 500 on static assets; Easy Auth sidecar logs "Failed to forward request to 127.0.0.1:8088" in 1-2 ms while the app listens.
* Finding: `src/api/src/zava_forward/api/server.py` `main()` used the stdlib `ThreadingHTTPServer` directly (request_queue_size=5, daemon_threads False). `resident_demo` and `resident_preview` use `_Server` subclasses with daemon_threads only.
* Local reproduction: 30 parallel non-blocking connects to a listening socket; stdlib backlog completed 6 of 30, backlog 128 completed 30 of 30. The 1-2 ms sidecar failure fits a full accept queue poorly (a full queue usually causes SYN drops and connect timeouts rather than fast failures), so this is a hypothesis with live proof pending. Plausible locally; it is not proven as the sole live cause.
