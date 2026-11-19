# Changes: issue 111 live (2026-11-19)

Added docs/reference/research/issue-111-live-demo-evidence-2026-11-19.md, an index row and a log entry. No source change; FOCUSED tier (documentation only).

| Criterion | Status |
| --- | --- |
| Outputs reproducible from retained readings | Proven (46 tests OK, 11 skipped, 1 expected failure) |
| Thresholds sourced or labelled exercise | Proven (same run) |
| R1 to R3 complete before use beyond exercise rule | Unproven: needs competent building-physics reviewer, Asset and agreed R3 limits; not waived |

Validation: `python3 -m unittest discover -s tests -p "*sensor_analysis*"` in src/core: OK. Link and diff review of docs. mypy/ruff n/a (no Python change). No Azure resources created.
