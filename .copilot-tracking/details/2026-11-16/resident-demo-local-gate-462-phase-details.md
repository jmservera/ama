---
title: "Phase details: resident-demo-local-gate-462"
description: "Step details for the Issue #462 local candidate plan"
ms.date: 2026-11-16
---

## Phase 1 Threat-model document

* Create `docs/reference/research/resident-demo-threat-model-2026-11-16.md` from research F3 (assets, boundaries, table T1 to T10, accepted risks, what it does not claim). Plain ASCII, YAML frontmatter, `*` lists.
* Link it from `src/api/README.md` in the "Synthetic resident showcase (#462)" section.
* Add an index row to `docs/reference/README.md` and an append-only entry to `docs/reference/log.md`.
* Verify: relative links resolve (script), no credential-like strings, `git diff` review.

## Phase 2 Dependencies and previews

* `gh issue view 444`, `gh pr view 455` states; confirm `resident_preview*` files unchanged versus base (`git diff --stat base -- <paths>`).

## Phase 3 Local verification

Run from the worktree with a venv that has the `src/*` packages installed (pip, no `PYTHONPATH=mvp`).

* Lint and types: `ruff check` and `ruff format --check` on the resident files; `mypy` as configured by the repository.
* Unit: core `test_resident_showcase*`, api `test_resident_demo_*`, infra `test_resident_demo_*`, `test_secret_lifecycle`.
* SQL Server parity: throwaway loopback SQL Server container, `ZF_SQL_PORT` and `ZF_SQL_PASSWORD` set to a random throwaway value, then `python -m checks.resident_demo_browser_check` (also covers the real view and the browser journeys) and `test_resident_showcase_sql` where it needs SQL.
* Docker non-root: `docker build -f src/api/Dockerfile.resident-demo src` and `python -m checks.resident_demo_image_check`; confirm `docker inspect` user is 10001.
* Browser journeys: `resident_demo_browser_check`, `resident_account_check`, `resident_summary_browser_check`, `resident_preview_browser_check`.
* Critique amendments: run `test_resident_showcase_sql` and apply `infra/sql/resident-showcase.sql` on the same throwaway container and record its image and version; prove non-root with `docker inspect` and `docker exec <c> id -u`, not only the `USER` line.
* A failing check blocks the candidate; fix with a failing-first test or record the blocker.

## Phase 4 Review

* Write the changes artifact from real command output, reconcile plan markers, run one review over base..working tree, record outcome and route findings.

## Phase 5 Gate

* Set repo-local git email; commit with the required trailers; `git fetch origin main` and confirm base equals the given sha.
* Run `python3 tools/rpi-checks.py --all --base 5e0c7f74432ffce73cfeaa672e4e40a605ca6274 --out /tmp/ama-gate-462-20261116T082915Z < /dev/null`, then `--verify-receipt`.
* Finalise the state file (next action: gate pending) before the single candidate commit. The witness log and receipt are external. If the gate fails, fix in a new commit and re-run into a new output directory.
* Record `commit-complete --claim-commit <sha>`. Make no further commit.
