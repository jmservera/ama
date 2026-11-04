# Issue 810 Easy Auth 500 fix changes (2026-11-04)

* `src/api/src/zava_forward/api/server.py`: handler `protocol_version = "HTTP/1.1"`, `timeout = 300`, `Connection: close` when closing, close on unread request body.
* `src/api/tests/test_keepalive.py`: keep-alive reuse and unread-body close tests.
* Docs: research note, `infra/README.md`, knowledge-base index and log.
* Live changes (ca-cutover-test-demo-api, rg ama): CPU 1.0/2Gi (reverted), stub command overrides `--0000017` to `--0000020` (replaced), final `--0000022` HTTP/1.1 launcher override with original resources and ingress `Http`. No credentials printed or stored; temporary files in /tmp removed.
* Validation: full `src/api` suite 1793 tests, 5 unrelated import errors (browser tooling); live 0 x 500 in 2,180 requests.
