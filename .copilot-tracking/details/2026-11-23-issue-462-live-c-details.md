# Details: issue 462 third pass

Phase 2: add one entry after `Referrer-Policy` in the `HEADERS` dict of `src/api/src/zava_forward/api/resident_demo/app.py`. In `src/api/tests/test_resident_demo_api.py` near line 723 assert the header value on the HTML response. Validate from `src/api` with the unittest runner limited to `test_resident_demo_api` and the resident preview tests, then `PYTHONPATH=../core/src:../agents/src python3 -m mypy` and `ruff check` plus `ruff format --check` on changed files.

Phase 3: note `docs/reference/research/resident-showcase-live-r8-2026-11-23.md`, a row in `docs/reference/README.md`, an appended entry in `docs/reference/log.md`.
