# Plan: resident redress route without detriment (Refs #86)

1. Core: `NON_DETRIMENT_COMMITMENTS`, `redress_route_view(c)` in `resident_decisions.py`; expose `d["redress_route"]` in `store.py`.
2. Screen: render route, commitments, reviewable decisions and open formal requests in `role-screens.js` (`resident-service-issues`), read-only.
3. Tests: core view tests (routes, preserved duties, open request send state, no mutation, opening leaves decisions untouched); screen test.
4. Validate: targeted unittest with TMPDIR=/dev/shm/zf-tmp, ruff, mypy. Critique: one pass, recorded in the review file.
