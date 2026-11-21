# Plan: issue 144 guard fix (2026-11-20)

* [ ] P1 Add `_drop_inheritable_capabilities` (ctypes capget/capset v3) and an injectable `drop_inheritable_fn` to `enforce_container_hardening`, called after NoNewPrivs and before reading `/proc/self/status`; zero-mask checks unchanged.
* [ ] P2 Add `prepare_private_scratch(env)` to `container_hardening.py` (creates `/tmp/zf`, `/state/zf`, mode 0700, owned by current uid, exist_ok; repoints TMPDIR, and ZF_STATE only when set); no-op unless enforced.
* [ ] P3 Call the helper before the guard in all twelve entrypoints.
* [ ] P4 Core tests, infra test update if needed, check-container.py for four images if docker works.
* [ ] P5 Docs: infra/README.md wording, module docstring, log entry, research note with per-criterion table.
* [ ] P6 mypy, ruff, unit tests; commit locally.
