# Plan: src-ci affected projects (2026-11-03)

1. Add `tools/ci-affected.py`: diff `BASE_SHA..HEAD_SHA`, output matrix (all five entries with `run` flag), `namespace`, `mssql`. Non-PR events select all.
2. Add `src-changes` job; matrix from its output; gate project steps on `matrix.run`; job-level `if` for namespace and mssql.
3. Rules: core => all; agents => agents + api; others self; project `*.md` ignored; infra, workflows, other src paths, unknown paths => all; gate tooling => namespace only.
4. Unit tests `tools/test_ci_affected.py`, run in the namespace job.
5. Validate YAML, actionlint, ruff, mypy, focused RPI gate.
