# Issue 1258 API wiring-test lint diagnostic details (2026-11-09)

Phase details for `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-lint-diagnostic-plan.md`.

## Phase 1: ordering gate

Commit the research, plan, details and critique as tracking-only files. Verify with `git status --short` that no other path changed.

## Phase 2: producer (run after the Phase 1 commit)

Working directory `src/api`; tool `/tmp/lint1258/venv/bin/ruff` (pinned `ruff==0.17.1`, isolated venv, no global change). Files: `src/zava_forward/api/server.py tests/test_ranking_publication_wiring.py tests/test_case_journey.py`.

1. `ruff --version` (must print 0.17.1).
2. `ruff check --output-format=concise <files>` using the maintained `pyproject.toml`.
3. `ruff format --check --force-exclude <files>` so the configured format exclude applies, as in CI.
4. Corroboration with the exact CI commands: `ruff check .` and `ruff format --check .`.
5. Record each exit code and `sha256sum` of every raw log and exit file in `/tmp/lint1258/run/`. Keep `/tmp/lint1258/research/` unchanged.
6. `git rev-parse <ref>:<path>` for the three files and `pyproject.toml` at `HEAD`, `9b1e2567`, `52f9b61b` (C5), `59d8ad8a` and `8d6f029c`.
7. `git diff --stat 59d8ad8a HEAD -- . ':!.copilot-tracking'` and `git rev-parse` of non-tracking tree equivalence.
8. `git status --short` before and after to prove no source mutation.

## Phase 3: records

Write changes, review, state, then the local handoff `/tmp/lint1258/handoff-1258-lint-diagnostic.md`. Commit with the repository-local privacy email and the Copilot trailer; no push.
