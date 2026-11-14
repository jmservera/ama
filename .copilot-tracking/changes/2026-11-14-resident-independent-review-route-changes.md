# Changes: resident redress route without detriment (Refs #86)

* `src/core/.../resident_decisions.py`: `NON_DETRIMENT_COMMITMENTS`, `REDRESS_ROUTES`, `redress_route_view`.
* `src/core/.../store.py`: case detail exposes `redress_route`.
* `src/api/.../web/role-screens.js`: read-only panel on `resident-service-issues` (commitments, routes, reviewable decisions, formal requests and send status).
* Tests: `test_resident_decisions` (view, send status, no mutation), `test_resident_service_screen` (panel, fallback, no controls).
* Validation (TMPDIR=/dev/shm/zf-tmp, targeted only): core `JsonResidentDecisions` 126 OK (1 skipped); api `test_resident_service_screen`, `test_content_standard`, `test_design_system`, `test_accessibility_baseline`, `test_dependency_rule` 59 OK; `ruff check` and `ruff format --check` clean; `mypy` on the two core files clean. No `unittest discover`, no hosted CI observed, SQL variant not run.
* Classification: focused tier (read-only view, no permission, dependency or gate change).

## Cycle 3 formatting correction (Refs #86)

* `src/core/tests/test_resident_decisions.py`: `ruff format` trailing-comma fix near line 2609; no behaviour change.
* Validation: `ruff format src/core src/api` (1 file reformatted) and `ruff check src/core src/api` clean. Tests not re-run (format only).
