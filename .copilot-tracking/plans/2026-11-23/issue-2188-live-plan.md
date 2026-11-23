# Issue 2188 live plan (2026-11-23)

* [x] Phase 1: replace `docker_lock` with `docker_slots` (BoundedSemaphore 4), `docker_gate` mutex, `trivy_lock` in `tools/rpi-checks.py`.
* [x] Phase 2: update `test_sql_and_image_resources_are_serial` to prove images overlap (peak 4) and mssql is exclusive; run `tools.test_rpi_checks`.
* [x] Phase 3: research note with per-criterion table under docs/reference/research/, log entry, changes record, review, commit.
