# Changes: issue 203 live re-measurement (Refs #203)

No source change. Added docs/reference/research/issue-203-live-20261119T1527Z-2026-11-19.md and its evidence folder; index and log updated.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | mvp/ and prototype/ references only intentional | Proven (checker 0 violations; 8 tests OK); allow-list judgement left to owner |
| 2-4 | Links, index/log, rubric | Already ticked; not re-proven |
| 5 | Deployed app and CI green from src/ | Unproven: app healthy, PR CI green, but no CI on main head, no deploy run, digest provenance unreadable |

Validation: FOCUSED tier, docs only. checker + unittest tools.test_check_legacy_references; mypy/ruff not applicable (no Python change). Not run: rpi-checks --all (not required).
