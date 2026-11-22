# Changes, issue 1274 live

Tier: focused (documentation only; no pinned action or image changed).

* Added docs/reference/research/issue-1274-live-evidence-2026-11-22.md.
* Updated docs/reference/README.md index and appended docs/reference/log.md.

Validation: tools/test_install_actionlint.py 12 OK; tools/test_rpi_checks 123 OK; real actionlint 1.7.7 download verified; git diff reviewed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Failing endpoints, logs, installers | Proven for actionlint (#1243, #1271) and AWF v0.28.23 checksums.txt 504 (#1271); #1273 cause not retained | jobs 128696067639, 128680975934, 128681102295 |
| 2 Bounded fail-closed retrieval | Proven (already ticked) | 12 tests OK |
| 3 Focused regressions | Proven (already ticked) | 12 + 123 tests OK |
| 4 Real checksum verification, reviewed hosted CI | Proven for actionlint 1.7.7 locally and run 42497999337 on main; unproven for AWF 0.28.23 and for a hosted run on a new head (nothing changed, no push) | evidence note |
| 5 Resume route | Already ticked, unchanged | issue comment 2026-11-11 |
