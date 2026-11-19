# Details: issue-203-checker-live

Phase 1: regex `^docs/reference/research/(?:issue-\d+-|src-repoint-)[^/]*\d{4}-?\d{2}-?\d{2}[^/]*(?:/|\.md$)`. It matches `issue-198-rubric-live-r2-2026-11-18.md`, `issue-200-live-20261118T1618Z-evidence/x.txt` and `src-repoint-live-audit-200-2026-11-18.md`, not `docs/reference/research/ux/design-system.md`.
Phase 2: extend `ReferenceTests` in `tools/test_check_legacy_references.py`.
Phase 3: `python3 tools/check-legacy-references.py` must exit 0; `python3 -m unittest tools.test_check_legacy_references`; `python3 -m ruff check` and `format --isolated --line-length 100 --check` on the two Python files.
