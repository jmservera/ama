# Changes, issue 200 live (2026-11-18)

Tier: FOCUSED (documentation only; no src, workflow, Dockerfile, SQL or infra edit). Never ran rpi-checks.py --all.

Files: docs/reference/research/src-repoint-live-audit-200-2026-11-18.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry).

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| 1 | pyproject src layout, no PYTHONPATH=mvp | Already ticked; unchanged |
| 2 | Workflow paths, tests, Docker context, requirements to src | Proven (audit note) |
| 3a | Image behaviour non-root, no-data, read-only | Proven locally (check-container.py PASS) |
| 3b | New tag deployed and verified; historical revisions keep tags | Partly proven: live revision --0000031 healthy on src image, historical tags intact; fresh push not performed (needs ACR public window) |
| 4-7 | Bicep, data path, tests, historical identifiers | Already ticked; unchanged |

Validation: docker build and src/check-container.py api PASS; read-only az containerapp checks; link and diff review. Throwaway resources: none (local image removed).
