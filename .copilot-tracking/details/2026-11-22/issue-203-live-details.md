# Details: issue-203-live (2026-11-22)

Phase 1: `python3 tools/check-legacy-references.py`; `python3 -m unittest tools.test_check_legacy_references`; `gh run list` for src-ci and src-deploy; `az containerapp show` and `revision list` (read-only); `curl /healthz`; api console log for `build: commit=`.
Phase 2: new note `docs/reference/research/issue-203-live-20261122-2026-11-22.md`, `docs/reference/README.md` row, `docs/reference/log.md` appended entry. Never edit earlier log entries.
Phase 3: validate links with `check-legacy-references.py --files`, git diff review.
