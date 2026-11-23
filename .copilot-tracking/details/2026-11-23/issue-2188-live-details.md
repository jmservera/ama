# Issue 2188 live details (2026-11-23)

Phase 1: `IMAGE_CONCURRENCY = 4`. `dispatch`: mssql acquires `docker_gate`, then all slots; image groups acquire `docker_gate` briefly, then one slot. `image()` wraps the three Trivy calls in `trivy_lock`.
Phase 2: fake `sql`/`image` record active counts; assert image peak >1 and never overlapping mssql.
