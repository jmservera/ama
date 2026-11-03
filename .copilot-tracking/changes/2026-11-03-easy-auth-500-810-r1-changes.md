# Changes: issue 810 slice 1 (2026-11-03)

* Added `docs/reference/research/easy-auth-intermittent-500-2026-11-03.md`.
* Edited `docs/reference/README.md` (index row) and `docs/reference/log.md` (entry).
* Added RPI artifacts under `.copilot-tracking/` and the session state file.
* Azure: read-only reads and bursts (about 600 GET requests to demo apps). No resource changed. Apps were warmed with `/healthz`.
* Not run: unit tests, ruff, mypy (no code change), gate, benchmarks, full suites.
* Divergence: none.
