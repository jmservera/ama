<!-- markdownlint-disable-file -->
# Issue 176 plan: determinism audit slice

Date: 2026-11-01. Research: `.copilot-tracking/research/2026-11-01/issue-176-determinism-audit-research.md`.

## Phases

* [x] Phase 1: add `version` to sensor-scenarios manifest; keep goldens green.
* [x] Phase 2: add `determinism_audit.py` (replay scale, sensor backfill, sensor scenarios, stock fabric on a fictional register; check manifest fields; report original stock register as unavailable) with CLI.
* [x] Phase 3: tests in `src/core/tests/test_determinism_audit.py`.
* [x] Phase 4: update README matrix/acceptance rows and `docs/reference/log.md`.
* [x] Phase 5: focused validation (unit tests, ruff check, ruff format --check, mypy), commit, push, PR with `Refs #176`.

## Critique (single pass)

* Verdict: compatible. Scope tight; must not claim the stock register criterion; never touch mvp/ or prototype/; audit must write only to temp dirs outside the repo.
* Direct disposition: audit exit code reflects replay failures only; unavailable generator is reported, not hidden.
