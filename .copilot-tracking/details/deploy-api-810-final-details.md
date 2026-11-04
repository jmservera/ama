# Details: deploy API HTTP/1.1 image (2026-11-04)

* ACR window: allow-exports true, default-action Deny, public enabled, rule for the VM IP as /32, 45 s wait, `login --expose-token`, `docker push`, then rule removed using the bare IP, public disabled, exports false; readback verified.
* App update: first YAML update changed the image and removed `command` but `args` remained (revision `--0000023`, never served verified traffic); the second update removed `args` too (revision `--0000024`, 100 percent traffic).
* Tests: `/tmp` scripts (not committed) using http.client over HTTPS; keep-alive unit tests in `src/api/tests/test_keepalive.py`.
