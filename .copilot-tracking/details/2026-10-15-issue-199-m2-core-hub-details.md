# Details: M2 core hub move

* Moves use `git mv`; edits to moved files are limited to import lines, path fixes in `ranking.py` and `factory.py`, and one docstring in `ledger.py`.
* `ranking.py` reads `policies/` next to the module; `src/core/pyproject.toml` declares it as package data and the image no longer copies `mvp/policies`.
* `factory.py` default data file is `Path.cwd()/data/zavaforward.json` because `parents[1]` would point into site-packages once installed (small behaviour note).
* Test imports: moved tests use `import dataset`; `mvp` tests reach core fixtures through `PYTHONPATH=.:../src/core/tests` (CI updated in `mvp-ci.yml` and `mvp-validation.yml`).
* SQL portability: no SQL was changed. `sqlstore.py` keeps its pre-existing SQLite-only DDL and `PRAGMA` statements, which `mssqlstore.py` overrides; the portability tests pass.
