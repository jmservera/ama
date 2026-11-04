# Changes: deploy API HTTP/1.1 image (2026-11-04)

* Live (owner-approved): image `crcutovertestrzsrg.azurecr.io/zava-forward-api:4d56cf609` (digest `sha256:505b8a43c98de481435d4252a6396071d58a55319278a991a6f380f4f0078474`) deployed to `ca-cutover-test-demo-api`; revision `--0000024` active, 100 percent traffic, no command/args override. Prior revision `--0000022` retained for rollback.
* Registry restored to private and read back.
* Results: 9 x 160 at 40 parallel on `/healthz`, `/welcome.html`, `/style.css`, 200 at 40 parallel, 300 sequential: all 200. 200 unauthenticated `/api/me` and `/api/cases`: all 401. Empty-body 500s: 0.
* Pipelined GET-with-body closes the connection: proven by `test_keepalive.py` (4 tests pass); a raw pipelined probe through Easy Auth returned one 200 and no close because the proxy mediates.
* Docs: `infra/README.md`, `docs/reference/log.md`.
* Acceptance for #810: the 0 empty-body 500 criterion is met by this sample. Authenticated calls were not tested (no new roles), so the issue stays `Refs`.
