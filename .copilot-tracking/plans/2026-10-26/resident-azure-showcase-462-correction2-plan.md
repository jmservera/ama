# Issue 462 correction cycle 2: research and plan (2026-10-26T00:05Z)

Written before the edit. Gate 2 (head 323d955e, receipt SHA a8492f7c...9119) failed at
`0015-project-core.log`: mypy `import-not-found` for the optional `mssql_python` at
`resident_showcase_sql.py:60` and `tests/test_resident_showcase_sql.py:35`. Reproduced (status 1, the same
two errors) with the gate-2 core venv python and an external mypy cache. Gate-2 venvs and logs untouched.

Prior art: other packages declare optional or absent third-party modules with a module-scoped
`[[tool.mypy.overrides]]` `ignore_missing_imports = true` (agents, api, importer pyproject files). In core,
the older SQL modules (mssqlstore, lawstore) avoid the error only through blanket `ignore_errors`, which is
not a pattern to extend.

Plan: add one override in `src/core/pyproject.toml` with `module = ["mssql_python"]` and
`ignore_missing_imports = true`. No dependency added, no module-wide ignore, no runner or allowlist change,
no SQL deny test change; the opt-in loud failure is unchanged. Validate: mypy clean in the gate-2 core venv
python; ruff; core full unit; then one clean-candidate targeted run (SQL 18 with 0 skipped, browser, image)
under the shared lock.

Critique (2026-10-26T00:08Z, one independent rubber-duck pass): no blocking or non-blocking issues; verdict proceed as written with the override targeting module "mssql_python". Applied unchanged.
