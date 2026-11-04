# Plan: deploy API HTTP/1.1 image (2026-11-04)

* [x] Build `zava-forward-api:4d56cf609` from `src/` context.
* [x] Short ACR public window, push, restore in reverse, verify readback.
* [x] Update the app to the new image and clear command/args.
* [x] Burst, 401 and pipelining checks; rollback target `--0000022` if any failure.
* [x] Docs: `infra/README.md`, `docs/reference/log.md`; issue comment; PR with `Refs #810`.
* Critique: executed once at plan time; no conflicts with confirmed decisions (no new roles, network paths or SQL change).
