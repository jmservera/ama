# Issue 2254 live research (2026-11-22)

Disposition: executed. Planning Readiness: Ready.

Evidence: docs/reference/research/issue-2254-live-probe-2026-11-22.md (live probe: tile 23, map 23, list 22; ZF-2025-0148 differs).

Cause: SqlStore._repair_identity_columns (src/core/src/zava_forward/core/sqlstore.py) does not compare or rebuild the hazard column, so a stale cases.hazard disagrees with the body-derived tile and map.

Limits: live SQL private, stored column unreadable; cause inferred and reproduced locally (test_sqlreads.py).
