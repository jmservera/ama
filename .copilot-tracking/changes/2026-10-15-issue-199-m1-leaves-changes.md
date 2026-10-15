# Changes: M1 isolated leaves (refs #199)

## Files

* Renamed (git mv, content identical except import lines): `ai.py`, `profile.py`, `rulecards.py` to `src/core/src/zava_forward/core/`; `test_profile.py`, `test_rulecards.py` to `src/core/tests/`; `test_ai_identity.py` to `src/agents/tests/`.
* Edited: `mvp/zavaforward_mvp/{assistants,store,sqlstore,server}.py`; `mvp/tests/test_{ai_eval,assistant_release,assistants,auth,continuity}.py`; `mvp/Dockerfile`; `mvp/README.md`; `.github/workflows/{mvp-ci,mvp-validation}.yml`; `src/core/pyproject.toml`; `src/agents/pyproject.toml`; `src/README.md`; the parity matrix; `docs/reference/README.md`; `docs/reference/log.md`.
* Added: `mvp/Dockerfile.dockerignore`. Removed: `mvp/.dockerignore` (superseded).
* `mvp/requirements.in` and `requirements.txt` unchanged: no new third-party dependency; a fresh pip-compile only drifts in transitive `pycparser`, so the lock was not regenerated.

## Validation (local, Python 3.12.3, venv outside the repo, pip only)

| Command | Result |
| --- | --- |
| baseline on main: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests -q` | Ran 719 tests, OK, skipped=92 |
| after: same command in `mvp/` with `pip install --no-deps -e src/core` | Ran 702 tests, OK, skipped=92 |
| `python -m unittest discover -s tests` in `src/core` | 20 tests OK |
| same in `src/agents`, `api`, `orchestrator`, `importer` | 8, 4, 4, 4 tests OK |
| `ruff check .`, `ruff format --check .`, `mypy` in each of the five projects | all pass |
| `python -m compileall -q mvp/zavaforward_mvp`; `node --check` on `app.js` and `assistants.js` | pass |
| `pip wheel --no-deps --no-build-isolation src/core` | wheel contains `ai`, `profile`, `rulecards` |
| `docker build` and image checks | not run: permission denied on the Docker socket; rely on CI (`image` and `src-*` jobs) |
| SQL Server contract tests (`mssql` job) | skipped locally (no SQL Server); rely on CI |

Test count: 702 in `mvp` plus 17 moved (4 profile, 11 rulecards, 2 identity) equals the 719 baseline; skips unchanged at 92 (SQL Server contract tests and one azure-core test).

## Rubric

Temporary score dip accepted (owner, 2026-10-14); no `rubric_version` bump. Moved files leave the `mvp/**` globs but stay under `src/**/*`, so the registry still counts them.

## Divergences

* Ruff formatting is not applied to the moved files, to keep pure renames (exemptions in `pyproject.toml`, removal planned in M6).
