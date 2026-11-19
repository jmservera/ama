# Details: issue 1258 live rerun (2026-11-19)

## Phase 1: note

Add `docs/reference/research/issue-1258-live-criteria-proof-2026-11-19.md` with the commands run, the 57-test result and a per-criterion table. Add a row to `docs/reference/README.md` and append to `docs/reference/log.md`.

## Validation

Targeted: `python3 -m unittest test_ranking_publication -q` in `src/core`. Markdown link and diff review. Mypy and ruff are not applicable (no Python change).
