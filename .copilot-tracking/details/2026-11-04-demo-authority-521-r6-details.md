# Details: demo authority 521 r6 (2026-11-04)

* Phase 1: read-only `az containerapp show/revision list/job list/job execution list` on group `ama`; no secret values read; env var values limited to the expiry setting.
* Phase 2: documentation only in `infra/README.md` (Live state check section) and `docs/reference/log.md`.
* Phase 3: `unittest discover` on `test_resident_showcase*.py` from `src/core` (89 run, 27 skipped without SQL Server), `ruff check`, `mypy --cache-dir=/tmp/mypy-530`.
