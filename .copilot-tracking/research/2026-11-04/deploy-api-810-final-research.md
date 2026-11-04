# Research: deploy API HTTP/1.1 image (2026-11-04)

* Disposition: reused. Evidence: `docs/reference/research/easy-auth-intermittent-500-2026-11-03.md` and PR #1048 (root cause: API HTTP/1.0 close-per-response; sidecar `HttpIOException`).
* Live state before: `ca-cutover-test-demo-api--0000022`, digest image plus `python -c` command/args override; registry private (Deny, public disabled, exports disabled).
* Owner approval for live #810 changes: 2026-11-04 (task statement).
* Planning Readiness: Ready.
